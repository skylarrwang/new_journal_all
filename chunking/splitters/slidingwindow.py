from .base import BaseTextSplitter

class SlidingWindowTextSplitter(BaseTextSplitter):
    def __init__(self, text: str, window_size: int = 1000, step_size: int = 100):
        super().__init__(text)
        self.window_size = window_size
        self.step_size = step_size
        