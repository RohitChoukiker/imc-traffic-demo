# ingestion.py
import os
import pickle
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv
from utils.chunker import chunker
from utils.embedder import ChunkEmbedder
from data_sources.csv_connector import load_csv_file

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

VECTOR_DB_DIR = "vector_db"
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

embedder = ChunkEmbedder()  # Auto-select device

class FaissIndexer:
    def __init__(self):
        self.index = None
        self.metadata = []

    def add_to_index(self, embeddings: np.ndarray, batch_metadata: list):
        import faiss
        if self.index is None:
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings.astype("float32"))
        self.metadata.extend(batch_metadata)

    def save_index(self):
        import faiss
        index_path = os.path.join(VECTOR_DB_DIR, "faiss_index.index")
        meta_path = os.path.join(VECTOR_DB_DIR, "chunks_metadata.pkl")
        if self.index is not None:
            faiss.write_index(self.index, index_path)
            with open(meta_path, "wb") as f:
                pickle.dump(self.metadata, f)
            print(f"💾 FAISS index saved ({len(self.metadata)} chunks)")

def build_index():
    print("📂 Loading CSV data...")
    csv_data = load_csv_file()
    faiss_indexer = FaissIndexer()

    embed_batch_size = 256
    row_batch_size = 1000
    save_every_chunks = 5000
    total_chunks = 0

    for table, rows in csv_data.items():
        if not rows:
            continue
        print(f"📋 Processing table: {table} ({len(rows)} rows)")

        for batch_start in range(0, len(rows), row_batch_size):
            batch_rows = rows[batch_start:batch_start + row_batch_size]

            all_batch_chunks = []
            batch_metadata = []

            for row in batch_rows:
                chunks = chunker.chunk_rows([row])
                all_batch_chunks.extend(chunks)
                batch_metadata.extend([{"chunk": c, "table": table, "row_data": row} for c in chunks])

            for i in range(0, len(all_batch_chunks), embed_batch_size):
                sub_batch = all_batch_chunks[i:i + embed_batch_size]
                sub_meta = batch_metadata[i:i + embed_batch_size]

                embeddings = embedder.embed_chunks(sub_batch, batch_size=embed_batch_size)
                faiss_indexer.add_to_index(embeddings, sub_meta)
                total_chunks += len(sub_batch)

                if total_chunks % save_every_chunks == 0:
                    faiss_indexer.save_index()
                    print(f"💾 Intermediate save at {total_chunks} chunks")

            print(f"📊 Processed rows {batch_start + 1}-{batch_start + len(batch_rows)}")

    faiss_indexer.save_index()
    print(f"🎉 FAISS index building completed! Total chunks: {total_chunks}")

if __name__ == "__main__":
    INDEX_PATH = os.path.join(VECTOR_DB_DIR, "faiss_index.index")
    META_PATH = os.path.join(VECTOR_DB_DIR, "chunks_metadata.pkl")

    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        print("💾 FAISS index and metadata already exist. Skipping embedding.")
    else:
        build_index()


































# import os
# import pickle
# import numpy as np
# from tqdm import tqdm
# from dotenv import load_dotenv
# from utils.chunker import chunker
# from utils.embedder import embedder
# from data_sources.csv_connector import load_csv_file

# load_dotenv()
# os.environ["TOKENIZERS_PARALLELISM"] = "false"

# VECTOR_DB_DIR = "vector_db"
# os.makedirs(VECTOR_DB_DIR, exist_ok=True)

# class FaissIndexer:
#     def __init__(self):
#         self.index = None
#         self.metadata = []

#     def add_to_index(self, embeddings: np.ndarray, batch_metadata: list):
#         import faiss
#         if self.index is None:
#             dim = embeddings.shape[1]
#             self.index = faiss.IndexFlatIP(dim)
#         self.index.add(embeddings.astype("float32"))
#         self.metadata.extend(batch_metadata)

#     def save_index(self):
#         import faiss
#         index_path = os.path.join(VECTOR_DB_DIR, "faiss_index.index")
#         meta_path = os.path.join(VECTOR_DB_DIR, "chunks_metadata.pkl")
#         if self.index is not None:
#             faiss.write_index(self.index, index_path)
#             with open(meta_path, "wb") as f:
#                 pickle.dump(self.metadata, f)
#             print(f"💾 FAISS index saved ({len(self.metadata)} chunks)")

# def build_index():
#     print("📂 Loading CSV data...")
#     csv_data = load_csv_file()
#     faiss_indexer = FaissIndexer()

#     embed_batch_size = 256
#     row_batch_size = 1000
#     save_every_chunks = 5000
#     total_chunks = 0

#     for table, rows in csv_data.items():
#         if not rows:
#             continue
#         print(f"📋 Processing table: {table} ({len(rows)} rows)")

#         for batch_start in range(0, len(rows), row_batch_size):
#             batch_rows = rows[batch_start:batch_start + row_batch_size]

#             all_batch_chunks = []
#             batch_metadata = []

#             for row in batch_rows:
#                 chunks = chunker.chunk_rows([row])
#                 all_batch_chunks.extend(chunks)
#                 batch_metadata.extend([{"chunk": c, "table": table, "row_data": row} for c in chunks])

#             for i in range(0, len(all_batch_chunks), embed_batch_size):
#                 sub_batch = all_batch_chunks[i:i + embed_batch_size]
#                 sub_meta = batch_metadata[i:i + embed_batch_size]

#                 embeddings = embedder.embed_chunks(sub_batch, batch_size=embed_batch_size)
#                 faiss_indexer.add_to_index(embeddings, sub_meta)
#                 total_chunks += len(sub_batch)

#                 if total_chunks % save_every_chunks == 0:
#                     faiss_indexer.save_index()
#                     print(f"💾 Intermediate save at {total_chunks} chunks")

#             print(f"📊 Processed rows {batch_start + 1}-{batch_start + len(batch_rows)}")

#     faiss_indexer.save_index()
#     print(f"🎉 FAISS index building completed! Total chunks: {total_chunks}")

# if __name__ == "__main__":
#     build_index()
