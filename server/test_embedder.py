#!/usr/bin/env python3
"""
Test script to verify the embedder is working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from embedding.embedder import ChunkEmbedder

def test_embedder():
    print("🧪 Testing embedder...")
    
    # Test chunks
    test_chunks = [
        "This is a test chunk for embedding",
        "Another test chunk to verify the process",
        "Third chunk to ensure everything works"
    ]
    
    try:
        # Initialize embedder
        print("📥 Initializing embedder...")
        embedder = ChunkEmbedder(model_name="sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        
        # Test embedding
        print("🔄 Testing embedding process...")
        embeddings = embedder.embed_chunks(test_chunks, batch_size=2)
        
        print(f"✅ Embeddings created successfully!")
        print(f"📊 Shape: {embeddings.shape}")
        print(f"📊 Number of embeddings: {len(embeddings)}")
        print(f"📊 Expected: {len(test_chunks)}")
        
        if len(embeddings) == len(test_chunks):
            print("✅ Test passed! Embedder is working correctly.")
        else:
            print("❌ Test failed! Number of embeddings doesn't match number of chunks.")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_embedder()
