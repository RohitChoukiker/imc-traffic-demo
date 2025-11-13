# retrieval.py
import os
import re
import pickle
import faiss
import numpy as np
import pandas as pd
import torch
from utils.embedder import ChunkEmbedder
from fastapi.encoders import jsonable_encoder
from utils.format_response import format_response


VECTOR_DB_DIR = "vector_db"
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data_sources/main.csv")

class HybridRetriever:
    def __init__(self, csv_path: str = CSV_PATH):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV not found at {csv_path}")
        
        # Load CSV
        self.df = pd.read_csv(csv_path, low_memory=False)
        print(f"✅ Loaded {len(self.df)} rows from CSV")

        # Fill NaN for JSON safety
        self.df = self.df.fillna("")

        # Paths
        index_path = os.path.join(VECTOR_DB_DIR, "faiss_index.index")
        meta_path = os.path.join(VECTOR_DB_DIR, "chunks_metadata.pkl")

        if not os.path.exists(index_path) or not os.path.exists(meta_path):
            raise FileNotFoundError("Run ingestion first!")

        # Load FAISS
        self.index = faiss.read_index(index_path)

        # Load metadata
        with open(meta_path, "rb") as f:
            self.metadata = pickle.load(f)

        # Clean metadata for JSON safety
        self.metadata = [self._make_json_safe(m) for m in self.metadata]

        # Device select
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.embedder = ChunkEmbedder(device=device)

    def _make_json_safe(self, obj):
        """Ensure dict/list values are JSON serializable"""
        if isinstance(obj, dict):
            return {k: self._make_json_safe(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_safe(v) for v in obj]
        elif isinstance(obj, (np.float32, np.float64)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        elif pd.isna(obj):
            return None
        return obj

    def _regex_lookup(self, query: str):
        query = query.strip()

        # Challan Number
        match = re.search(r"\bMP\d{6,}\b", query, re.IGNORECASE)
        if match:
            res = self.df[self.df["Challan Number"].astype(str) == match.group(0)]
            if not res.empty:
                return res.to_dict(orient="records")

        # Vehicle Number
        match = re.search(r"\b[A-Z]{2}\d{1,2}[A-Z]{0,3}\d{3,4}\b", query, re.IGNORECASE)
        if match:
            res = self.df[self.df["Vehicle Number"].astype(str).str.upper() == match.group(0).upper()]
            if not res.empty:
                return res.to_dict(orient="records")

        # DL Number
        match = re.search(r"\b[A-Z0-9]{8,15}\b", query, re.IGNORECASE)
        if match:
            res = self.df[self.df["DL Number"].astype(str) == match.group(0)]
            if not res.empty:
                return res.to_dict(orient="records")

        return None

    def _semantic_search(self, query: str, top_k: int = 1000000):
        query_vec = self.embedder.embed_chunks([query])
        if query_vec.shape[0] == 0:
            return []

        distances, indices = self.index.search(query_vec.astype("float32"), top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if 0 <= idx < len(self.metadata):
                results.append({
                    "rank": i + 1,
                    "score": float(distances[0][i]),   # ensure JSON-safe float
                    "metadata": self.metadata[idx]
                })
        return results

    def search(self, query: str, top_k: int = 1000000):
        regex_results = self._regex_lookup(query)
        if regex_results:
            print("🔎 Direct metadata match")
            return jsonable_encoder(regex_results)

        print("🤖 Using semantic FAISS search")
        return jsonable_encoder(self._semantic_search(query, top_k))


_retriever = None

def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = HybridRetriever()
    return _retriever



def query_data(query: str, top_k: int = 10):
    retriever = get_retriever()
    results = retriever.search(query, top_k)
    return format_response(results, query)