from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from .base import BaseTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

THRESHOLD_MAP = {
    "small": 85,
    "medium": 90,
    "large": 95,
    "xlarge": 99
}

class SemanticTextSplitter(BaseTextSplitter):
    def _initialize_splitter(self, embedding_model: str = "openai", breakpoint_threshold_amount: int = 90):
        """Initialize the semantic chunker with the current configuration."""
        if self.embedding_model == "openai":
            embeddings = OpenAIEmbeddings(api_key=self.api_key)
        elif self.embedding_model == "huggingface":
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-mpnet-base-v2"
            )
        else:
            raise ValueError(f"Invalid embedding model: {self.embedding_model}")
        
        self.splitter = SemanticChunker(
            embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=breakpoint_threshold_amount
        )

    def __init__(self, text: str, embedding_model: str = "openai", breakpoint_threshold_amount: int = 90):
        super().__init__(text)
        self.embedding_model = embedding_model
        self.original_breakpoint_threshold_amount = breakpoint_threshold_amount
        self.current_breakpoint_threshold_amount = breakpoint_threshold_amount
        self.split_text_docs = []
        if embedding_model == "openai":
            self.api_key = OPENAI_API_KEY
        self._initialize_splitter()
    
    def change_breakpoint_threshold(self, breakpoint_threshold_amount: int):
        """
        Change the breakpoint threshold and reinitialize the splitter.
        
        Args:
            breakpoint_threshold_amount: New threshold value (percentile) for creating breakpoints
        """
        self.current_breakpoint_threshold_amount = breakpoint_threshold_amount
        self._initialize_splitter()

    # def split_text(self, max_chunk_size: int = 2000) -> List[str]:
    #     self.split_text_docs = self.splitter.split_text(self.text)
    #     return self.split_text_docs

    def split_text(self, text: str = None, max_chunk_size: int = 2000, new_threshold: int = 90, num_attempts: int = 0) -> List[str]:
        """
        Split text using semantic chunking with progressive threshold increase.
        
        Args:
            text: Text to split (defaults to self.text if None)
            max_chunk_size: Maximum allowed size for each chunk
            threshold_increase: How much to increase threshold each attempt
            num_attempts: Current attempt number
        """
        if num_attempts > 2:
            # Base case: too many attempts
            self.split_text_docs.append(text if text is not None else self.text)
            return self.split_text_docs
        
        if text is None:
            text = self.text

        # Ensure threshold stays within valid range (0-100)
        self.change_breakpoint_threshold(new_threshold)
        
        initial_split = self.splitter.split_text(text)

        # Process each doc in order
        for doc in initial_split:
            if isinstance(doc, str) and len(doc) > max_chunk_size:
                # check how much the doc is over the max chunk size
                over_size = len(doc) - max_chunk_size
                # create a range mapper
                if over_size <= 100:
                    size_type = "xlarge"
                elif over_size <= 700:
                    size_type = "large"
                elif over_size <= 1700:
                    size_type = "medium"
                else:
                    size_type = "small"

                new_threshold = THRESHOLD_MAP[size_type]
                self.split_text(
                    text=doc,
                    max_chunk_size=max_chunk_size,
                    new_threshold=new_threshold,
                    num_attempts=num_attempts+1
                )
            else:
                # self.split_text_docs.append(f"======APPENDED ON ATTEMPT {num_attempts}====== WITH THRESHOLD {new_threshold}")
                self.split_text_docs.append(doc)
        
        # Reset threshold on final pass
        if num_attempts == 0:
            self.change_breakpoint_threshold(self.original_breakpoint_threshold_amount)

        return self.split_text_docs