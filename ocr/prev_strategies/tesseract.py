import cv2
import numpy as np
from pdf2image import convert_from_path
import os
import pytesseract
from PIL import Image

# Configure poppler path for macOS
POPPLER_PATH = "/opt/homebrew/bin" if os.path.exists("/opt/homebrew/bin") else "/usr/local/bin"

FEB_ISSUE = "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/02_2025.pdf"
MAY_ISSUE = "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/05_14_1968.pdf"
DECEMBER_ISSUE = "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/12_06_1977.pdf"

def run_ocr(image, title):
    # Convert numpy array to PIL Image
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    
    # Run OCR and get confidence scores
    ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    # Calculate average confidence for detected text
    confidences = [float(conf) for conf in ocr_data['conf'] if conf != '-1']
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    print(f"\n{title} OCR Results:")
    print(f"Average Confidence: {avg_confidence:.2f}")
    print(f"Number of words detected: {len(confidences)}")
    print("Sample text:", ' '.join(ocr_data['text'][:5]))  # Print first 5 words
    
    return avg_confidence

def preprocess_pdf(pdf_path):
    # Convert first page of PDF to image
    images = convert_from_path(pdf_path, first_page=4, last_page=4, poppler_path=POPPLER_PATH)
    if not images:
        raise ValueError("No pages found in PDF")
    
    # Convert PIL Image to numpy array
    img = np.array(images[0])
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Apply thresholding to handle varying backgrounds
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY, 11, 2)
    
    # Denoise the image
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    
    return img, denoised

if __name__ == "__main__":
    img, denoised = preprocess_pdf(DECEMBER_ISSUE)
    
    # Run OCR on both images
    orig_confidence = run_ocr(img, "Original")
    denoised_confidence = run_ocr(denoised, "Denoised")
    print(orig_confidence)
    print(denoised_confidence)

    # Display images
    cv2.imshow("Original PDF Page", img)
    cv2.imshow("Denoised PDF Page", denoised)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
