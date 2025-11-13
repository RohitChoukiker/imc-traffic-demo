# embedding.py
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import torch

class ChunkEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = None):
        # Auto-select device
        if device is None:
            device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.device = device
        self.model = SentenceTransformer(model_name, device=self.device)
        print(f"Using model: {model_name} on {self.device.upper()}")

    def embed_chunks(self, chunks: List[str], batch_size: int = 256) -> np.ndarray:
        if not chunks:
            return np.array([])

        all_embeddings = []

        for i in tqdm(range(0, len(chunks), batch_size), desc="Embedding batches", unit="batch"):
            batch = chunks[i:i + batch_size]
            try:
                batch_embeddings = self.model.encode(
                    batch,
                    convert_to_tensor=True,
                    normalize_embeddings=True,
                    show_progress_bar=False
                )
                all_embeddings.append(batch_embeddings.cpu().numpy())
            except Exception as e:
                print(f"❌ Error in batch {i//batch_size + 1}: {e}")
                continue

        if not all_embeddings:
            return np.array([])

        return np.vstack(all_embeddings)

# Singleton instance
embedder = ChunkEmbedder()










# from typing import List
# import numpy as np
# from langchain.embeddings import HuggingFaceEmbeddings

# class ChunkEmbedder:
#     def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        
#         self.model = HuggingFaceEmbeddings(model_name=model_name)
#         print(f"✅ Using HuggingFace model: {model_name}")

#     def embed_chunks(self, chunks: List[str]) -> np.ndarray:
        
#         if not chunks:
#             return np.array([])
#         return np.array(self.model.embed_documents(chunks))
