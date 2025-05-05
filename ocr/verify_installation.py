import PyPDF2
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import ocrmypdf
import os

print("PyPDF2 version:", PyPDF2.__version__)
print("PyMuPDF version:", fitz.version)
print("Tesseract version:", pytesseract.get_tesseract_version())
print("Environment setup successful!")

# Test OCRmyPDF (if you have a sample PDF)
# ocrmypdf.ocr('input.pdf', 'output_searchable.pdf', language='eng')
