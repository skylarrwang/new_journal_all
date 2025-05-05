import fitz
import base64
from typing import List
from PIL import Image
import io
import json
def pdf_to_image(pdf_path: str) -> List[str]:
    """Convert a PDF file into a base64-encoded PNG image."""
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        print("calculating matrix...")
        matrix = calculate_matrix(page)
        pix = page.get_pixmap(matrix=matrix)
        images.append(base64.b64encode(pix.tobytes("png")).decode("utf-8"))
    return images

def pdf_by_page(pdf_path: str, page_number: int) -> str:
    """Extract the table of contents from a PDF file."""
    doc = fitz.open(pdf_path)
    first_page = doc[page_number]

    # simple base64 encode the first page
    pix = first_page.get_pixmap()
    # print("finished getting pixmap")
    return base64.b64encode(pix.tobytes("png")).decode("utf-8")

def calculate_matrix(page: fitz.Page) -> fitz.Matrix:
        """Calculate transformation matrix for page conversion."""
        # Calculate zoom factor based on target DPI
        zoom = 76 / 72
        matrix = fitz.Matrix(zoom * 2, zoom * 2)
        # Handle page rotation if present
        if page.rotation != 0:
            matrix.prerotate(page.rotation)
        return matrix


def get_first_page_image(pdf_path: str) -> Image:
    """Convert first page of PDF to PIL Image with optimized settings."""
    doc = fitz.open(pdf_path)
    page = doc[0]  # Get first page
    
    # Use optimized matrix
    zoom = 150 / 72
    matrix = fitz.Matrix(zoom, zoom)
    
    # Get pixmap
    pix = page.get_pixmap(matrix=matrix)
    
    # Convert to PIL Image
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))
    
    doc.close()
    return img

def string_to_dict(string: str) -> dict:
    """Convert a string to a dictionary."""
    # clean the string to isolate the json
    string = string.split("```json")[1].split("```")[0]
    return json.loads(string)

