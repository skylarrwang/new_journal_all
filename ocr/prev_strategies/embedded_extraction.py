import os
from fitz import open

"""
Use this doc as a reference for helpful PyMuPDF functions for embedded PDFs 
"""

FEB_ISSUE = "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/02_2025.pdf"
MAY_ISSUE = "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/05_14_1968.pdf"
DECEMBER_ISSUE = "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/12_06_1977.pdf"

def test_ocr(file_path):
    """
    Test the OCR functionality on an embedded PDF file.
    """

    # Check if the test path exists
    assert os.path.exists(file_path), f"Test file does not exist: {file_path}"

    # Perform OCR on the embedded PDF file
    doc = open(file_path)
    page = doc[3] # load the first page
    
    ## RETURN TEXT IN A RAW FORMAT
    # str
    plain_text = page.get_text("text")
    print("========================")
    print("Plain text:")
    print("========================")
    print(plain_text)
    
    ## RETURN TEXT IN A STRUCTURED FORMAT
    # List[Dict[str, Union[int, str]]]
    structured_text = page.get_text("dict")
    print("========================")
    print("Structured text:")
    print("========================")
    # print(structured_text)
    
    
    ## RETURN WORDS AND THEIR COORDINATES IN TUPLES
    # List[(x0, y0, x1, y1, "word", block_no, line_no, word_no)]
    words = page.get_text("words")
    print("========================")
    print("Words:")
    print("========================")
    for word in words:
        pass
       # print(word[4])
        
    ## Extract metadata
    metadata = doc.metadata
    print("========================")
    print("Metadata:")
    print("========================")
    print(metadata)
    
    

if __name__ == "__main__":
    test_ocr(FEB_ISSUE)
    # Run the test function
    