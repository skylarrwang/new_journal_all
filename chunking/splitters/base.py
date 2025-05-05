from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseTextSplitter(ABC):
    def __init__(self, text: str):
        self.text = text
        self.split_text_docs = []
    
    @abstractmethod
    def split_text(self) -> List[str]:
        """Split the input text into chunks."""
        pass
    
    def get_docs_metadata(self) -> Dict[str, Any]:
        """Get metadata about the split documents."""
        return {"num_chunks": len(self.split_text_docs)}