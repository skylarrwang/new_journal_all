import os
import argparse
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import fitz  # PyMuPDF
import time
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
import re
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def configure_gemini():
    """Configure Gemini API with proper error handling"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test the model configuration
        test_response = model.generate_content("Test")
        if not test_response.text:
            raise ValueError("Model test failed - no response generated")
            
        return model
    except Exception as e:
        logger.error(f"Error configuring Gemini: {str(e)}")
        raise

def extract_text_from_pdf(pdf_path, start_page=0, num_pages=3):
    """Extract text from PDF with improved error handling"""
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            end_page = min(start_page + num_pages, len(doc))
            for page_num in range(start_page, end_page):
                page = doc[page_num]
                text += f"\n\n--- Page {page_num + 1} ---\n\n"
                text += page.get_text()
        return text, end_page
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def deduplicate_text(text):
    """Remove duplicate content while preserving structure"""
    lines = text.split('\n')
    unique_lines = []
    seen = set()
    
    for line in lines:
        # Skip empty lines and page markers
        if not line.strip() or line.startswith('--- Page'):
            unique_lines.append(line)
            continue
            
        # Normalize line for comparison
        normalized = re.sub(r'\s+', ' ', line.strip())
        if normalized not in seen:
            seen.add(normalized)
            unique_lines.append(line)
            
    return '\n'.join(unique_lines)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def process_with_gemini(text, is_first_chunk=False):
    """Process text with Gemini with improved error handling"""
    try:
        model = configure_gemini()
        
        base_prompt = """
        You are a magazine transcriber. Process this magazine content with the following rules:
        1. Preserve absolutely all text exactly as written. Never add or remove any text. 
        2. Use double newlines between paragraphs
        4. Mark advertisements with [ADVERTISEMENT] at the start of the advertisement. 
        8. For every distinct prose or poetry article, format the header consistently as: 
            **Title: [Title]**
            **Author: [Author]**
            **Page number(s): [Number(s)]**
            ...
        """
        
        if is_first_chunk:
            prompt = base_prompt + """
            First, list the publication date, volume, and issue number of the magazine, as
                Publication date: [Date]
                Volume: [Volume]
                Issue number: [Issue number]
            Then, extract and list:
            2. MASTHEAD (if present):
               - Format as: **Position: Name(s)**
            
            4. TABLE OF CONTENTS:
               - Copy over the table of contents exactly 
               - Format as: **Title - Author**
            
            5. ARTICLE CONTENT:
               - Include full text with specified formatting
            """
        else:
            prompt = base_prompt + """
            Extract ARTICLE CONTENT:
            - Make sure every article and poem has its own header. 
            - Format headers as shown above
            - Include full text without changes
            """
        
        response = model.generate_content(prompt + "\n\n" + text)
        
        if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
            logger.warning(f"Prompt feedback: {response.prompt_feedback}")
            
        if not hasattr(response, 'text') or not response.text:
            # Try processing smaller chunks
            chunks = text.split("\n\n")
            processed_chunks = []
            
            for chunk in chunks:
                if not chunk.strip():
                    continue
                    
                try:
                    chunk_response = model.generate_content(base_prompt + "\n\nProcess this content:\n\n" + chunk)
                    if hasattr(chunk_response, 'text') and chunk_response.text:
                        processed_chunks.append(chunk_response.text)
                except Exception as e:
                    logger.warning(f"Failed to process chunk: {str(e)}")
                    processed_chunks.append(chunk)  # Keep original if processing fails
                    
            return deduplicate_text("\n\n".join(processed_chunks))
            
        return deduplicate_text(response.text)
    except Exception as e:
        logger.error(f"Error processing with Gemini: {str(e)}")
        raise

def save_progress(pdf_path, current_page, results, progress_file):
    """Save processing progress to a JSON file"""
    progress = {
        "pdf_path": str(pdf_path),
        "current_page": current_page,
        "results": results
    }
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    logger.info(f"Progress saved to {progress_file}")

def load_progress(progress_file):
    """Load processing progress from a JSON file"""
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress = json.load(f)
        logger.info(f"Loaded progress from {progress_file}")
        return progress
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        logger.warning(f"Invalid progress file: {progress_file}")
        return None

def process_magazine(pdf_path, output_path=None):
    """Process a magazine PDF and convert it to markdown"""
    try:
        # Validate input path
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        # Set up output paths
        if output_path is None:
            output_dir = pdf_path.parent / "markdowns"
            output_path = output_dir / f"{pdf_path.stem}.md"
            progress_file = output_dir / f"{pdf_path.stem}_progress.json"
        else:
            output_path = Path(output_path)
            progress_file = output_path.parent / f"{output_path.stem}_progress.json"
            
        output_path.parent.mkdir(exist_ok=True)
        
        # Test Gemini configuration
        logger.info("Testing Gemini configuration...")
        configure_gemini()
        logger.info("Gemini configuration successful")
        
        # Get total number of pages
        with fitz.open(str(pdf_path)) as doc:
            total_pages = len(doc)
        
        # Try to load existing progress
        progress = load_progress(progress_file)
        if progress and progress["pdf_path"] == str(pdf_path):
            start_page = progress["current_page"]
            all_results = progress["results"]
            logger.info(f"Resuming from page {start_page + 1}")
        else:
            start_page = 0
            all_results = []
        
        # Process PDF in chunks
        chunk_size = 3  # Process 3 pages at a time
        
        while start_page < total_pages:
            logger.info(f"Processing pages {start_page + 1} to {min(start_page + chunk_size, total_pages)}...")
            text, end_page = extract_text_from_pdf(str(pdf_path), start_page=start_page, num_pages=chunk_size)
            
            if not text:
                logger.warning(f"No text extracted from pages {start_page + 1} to {end_page}")
                start_page = end_page
                save_progress(pdf_path, start_page, all_results, progress_file)
                continue
                
            is_first_chunk = (start_page == 0)
            try:
                result = process_with_gemini(text, is_first_chunk)
                if result:
                    all_results.append(result)
                    
                    # Save progress after each chunk
                    save_progress(pdf_path, end_page, all_results, progress_file)
                    
                    # Write current results to markdown file
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write("\n\n".join(all_results))
                else:
                    logger.warning(f"No result generated for pages {start_page + 1} to {end_page}")
            except Exception as e:
                logger.error(f"Failed to process pages {start_page + 1} to {end_page}: {str(e)}")
                # Try to process page by page
                for page in range(start_page, end_page):
                    try:
                        single_text, _ = extract_text_from_pdf(str(pdf_path), start_page=page, num_pages=1)
                        single_result = process_with_gemini(single_text, is_first_chunk and page == 0)
                        if single_result:
                            all_results.append(single_result)
                            save_progress(pdf_path, page + 1, all_results, progress_file)
                    except Exception as e:
                        logger.error(f"Failed to process page {page + 1}: {str(e)}")
                        # Keep original text if processing fails
                        all_results.append(single_text)
                        save_progress(pdf_path, page + 1, all_results, progress_file)
            
            start_page = end_page
            time.sleep(2)  # Delay between chunks
            
        # Clean up progress file when done
        if progress_file.exists():
            progress_file.unlink()
            
        logger.info(f"Processing complete! Output saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error processing magazine: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Process a magazine PDF and convert it to markdown')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--output', '-o', help='Path to save the output markdown file')
    
    args = parser.parse_args()
    process_magazine(args.pdf_path, args.output)

if __name__ == "__main__":
    main() 