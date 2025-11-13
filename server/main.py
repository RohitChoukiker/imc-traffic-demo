# main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.ingestion import build_index
from services.retrieval import HybridRetriever
from llm_generation.llm_handler import generate_answer_claude


app = FastAPI(title="IMC Smart City RAG Assistant")

# CORS config
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        FRONTEND_URL,
        "*"  # fallback
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 1000000

retriever: HybridRetriever | None = None

def get_retriever() -> HybridRetriever:
    global retriever
    if retriever is None:
        try:
            retriever = HybridRetriever()
        except FileNotFoundError:
            raise HTTPException(
                status_code=400,
                detail="FAISS index not found. Please run /rag/rebuild-index first."
            )
    return retriever
@app.post("/rag/query")
def query_rag(request: QueryRequest):
    
    try:
        retriever = get_retriever()

        # Step 1: Retrieve relevant data (regex + semantic FAISS search)
        retrieved_chunks = retriever.search(request.query, top_k=request.top_k)
        if not retrieved_chunks:
            return {
                "query": request.query,
                "thought": "No relevant data found in Excel.",
                "context_used": [],
                "answer": "I could not find any relevant information."
            }

        # Step 2: Prepare context for LLM
        context = "\n".join([str(item) for item in retrieved_chunks])

        # Step 3: Call Claude API
        prompt = (
            f"User query: {request.query}\n\n"
            f"Relevant data:\n{context}\n\n"
            "Answer clearly using the above data."
        )
        answer = generate_answer_claude(prompt)

        # Check if we have structured data that can be formatted as a table
        table_data = None
        if retrieved_chunks and isinstance(retrieved_chunks, list) and len(retrieved_chunks) > 0:
            # Handle different types of retrieved data
            records_to_process = []
            
            # If we have dictionary records directly (from regex lookup)
            if isinstance(retrieved_chunks[0], dict):
                records_to_process = retrieved_chunks
            # If we have metadata objects (from semantic search)
            elif isinstance(retrieved_chunks[0], dict) and 'metadata' in retrieved_chunks[0]:
                records_to_process = [item['metadata'] for item in retrieved_chunks if isinstance(item, dict) and 'metadata' in item]
            
            if records_to_process:
                # Get all unique keys from all records
                all_keys = set()
                for record in records_to_process:
                    if isinstance(record, dict):
                        all_keys.update(record.keys())
                
                # Convert to list and sort for consistency
                columns = sorted(list(all_keys))
                
                # Create rows
                rows = []
                for record in records_to_process:
                    if isinstance(record, dict):
                        row = []
                        for col in columns:
                            value = record.get(col, '')
                            # Convert to string and replace empty values with "NA"
                            str_value = str(value) if value is not None else ''
                            if str_value.strip() == '' or str_value.lower() in ['nan', 'none', 'null']:
                                row.append('NA')
                            else:
                                row.append(str_value)
                        rows.append(row)
                
                if rows:
                    table_data = {
                        "columns": columns,
                        "rows": rows
                    }

        return {
            "query": request.query,
            "thought": "Analyzing your query and searching through csv data...",
            "context_used": retrieved_chunks,
            "answer": answer,
            "table": table_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rag/rebuild-index")
def rebuild_index_endpoint():
    """
    Rebuild the FAISS index from the Excel CSV
    """
    global retriever
    try:
        INDEX_PATH = os.path.join("vector_db", "faiss_index.index")
        META_PATH = os.path.join("vector_db", "chunks_metadata.pkl")

       
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            print("💾 FAISS index and metadata already exist. Skipping embedding.")
            return {"message": "💾 FAISS index and metadata already exist. Skipping embedding."}

     
        build_index()
        retriever = None
        return {"message": "✅ Excel FAISS index rebuilt successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "✅ Excel RAG Assistant is running!"}






