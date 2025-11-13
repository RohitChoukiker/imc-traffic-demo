#!/usr/bin/env python3
"""
Test script to verify the ingestion process with a small dataset
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_sources.csv_connector import load_csv_file
from utils.chunker import chunker
from embedding.embedder import ChunkEmbedder

def test_ingestion():
    print("🧪 Testing ingestion process...")
    
    try:
        # Load CSV data
        print("📂 Loading CSV data...")
        csv_data = load_csv_file()
        print(f"📊 Loaded {len(csv_data)} tables")
        
        # Process only first 10 rows from each table for testing
        all_chunks, all_metadata = [], []
        
        for table, rows in csv_data.items():
            if not rows:
                print(f"⚠️ Table '{table}' is empty, skipping")
                continue
                
            print(f"📋 Processing table: {table} with {len(rows)} rows")
            
            # Take only first 10 rows for testing
            test_rows = rows[:10]
            print(f"🧪 Testing with first {len(test_rows)} rows from {table}")
            
            for row in test_rows:
                chunks = chunker.chunk_rows([row])
                all_chunks.extend(chunks)
                for c in chunks:
                    all_metadata.append({
                        "chunk": c,
                        "table": table,
                        "row_data": row
                    })
        
        print(f"📊 Total chunks created: {len(all_chunks)}")
        print(f"📊 Total metadata entries: {len(all_metadata)}")
        
        if len(all_chunks) == 0:
            print("❌ No chunks were created. Check your data and chunking process.")
            return
        
        # Test embedding with a small batch
        print("🔄 Testing embedding with small batch...")
        embedder = ChunkEmbedder(model_name="sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        
        # Test with first 5 chunks only
        test_chunks = all_chunks[:5]
        print(f"🧪 Testing embedding with {len(test_chunks)} chunks...")
        
        embeddings = embedder.embed_chunks(test_chunks, batch_size=2)
        
        print(f"✅ Embeddings created successfully!")
        print(f"📊 Shape: {embeddings.shape}")
        print(f"📊 Number of embeddings: {len(embeddings)}")
        
        if len(embeddings) == len(test_chunks):
            print("✅ Test passed! Ingestion process is working correctly.")
        else:
            print("❌ Test failed! Number of embeddings doesn't match number of chunks.")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ingestion()
