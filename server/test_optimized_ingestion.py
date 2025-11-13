#!/usr/bin/env python3
"""
Test script to verify the optimized ingestion process
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_sources.csv_connector import load_csv_file
from utils.chunker import chunker
from embedding.embedder import ChunkEmbedder

def test_optimized_ingestion():
    print("🧪 Testing optimized ingestion process...")
    
    try:
        # Load CSV data
        print("📂 Loading CSV data...")
        csv_data = load_csv_file()
        print(f"📊 Loaded {len(csv_data)} tables")
        
        # Process first 1000 rows for testing
        all_chunks, all_metadata = [], []
        
        for table, rows in csv_data.items():
            if not rows:
                print(f"⚠️ Table '{table}' is empty, skipping")
                continue
                
            print(f"📋 Processing table: {table} with {len(rows)} rows")
            
            # Take first 1000 rows for testing
            test_rows = rows[:1000]
            print(f"🧪 Testing with first {len(test_rows)} rows from {table}")
            
            # Process in batches like the optimized version
            batch_size = 100
            total_batches = (len(test_rows) + batch_size - 1) // batch_size
            
            for batch_idx in range(0, len(test_rows), batch_size):
                batch_end = min(batch_idx + batch_size, len(test_rows))
                batch_rows = test_rows[batch_idx:batch_end]
                batch_num = (batch_idx // batch_size) + 1
                
                print(f"🔄 Processing batch {batch_num}/{total_batches} ({batch_idx+1}-{batch_end} of {len(test_rows)} rows)")

                for row in batch_rows:
                    chunks = chunker.chunk_rows([row])
                    all_chunks.extend(chunks)
                    for c in chunks:
                        all_metadata.append({
                            "chunk": c,
                            "table": table,
                            "row_data": row
                        })
                
                print(f"📊 Batch {batch_num} completed. Total chunks so far: {len(all_chunks)}")
        
        print(f"📊 Total chunks created: {len(all_chunks)}")
        print(f"📊 Total metadata entries: {len(all_metadata)}")
        
        if len(all_chunks) == 0:
            print("❌ No chunks were created. Check your data and chunking process.")
            return
        
        # Test embedding with optimized batch size
        print("🔄 Testing embedding with optimized batch size...")
        embedder = ChunkEmbedder(model_name="sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        
        # Test with first 100 chunks only
        test_chunks = all_chunks[:100]
        print(f"🧪 Testing embedding with {len(test_chunks)} chunks...")
        
        embeddings = embedder.embed_chunks(test_chunks, batch_size=32)
        
        print(f"✅ Embeddings created successfully!")
        print(f"📊 Shape: {embeddings.shape}")
        print(f"📊 Number of embeddings: {len(embeddings)}")
        
        if len(embeddings) == len(test_chunks):
            print("✅ Test passed! Optimized ingestion process is working correctly.")
            print("🚀 You can now run the full ingestion process.")
        else:
            print("❌ Test failed! Number of embeddings doesn't match number of chunks.")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_optimized_ingestion()
