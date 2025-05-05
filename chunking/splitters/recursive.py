from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from .base import BaseTextSplitter

class RecursiveTextSplitter(BaseTextSplitter):
    def __init__(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        super().__init__(text)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
    
    def split_text(self) -> List[str]:
        """Split text using recursive character splitting."""
        self.split_text_docs = self.splitter.split_text(self.text)
        return self.split_text_docs
    
