# universal_chunker.py
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter

class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 50):
        """
        chunk_size: number of characters per chunk
        chunk_overlap: number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    @staticmethod
    def row_to_text(row: Dict) -> str:
        return " | ".join([f"{k}: {str(v).strip()}" for k, v in row.items() if v is not None and str(v).strip()])

    def chunk_texts(self, texts: List[str]) -> List[str]:
        return [chunk for text in texts for chunk in self.splitter.split_text(text)]

    def chunk_rows(self, rows: List[Dict]) -> List[str]:
        texts = [self.row_to_text(row) for row in rows]
        return self.chunk_texts(texts)

# Singleton instance
chunker = TextChunker()
