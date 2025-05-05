import os
import json
from pathlib import Path
import re
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_pdf_links() -> Dict[str, str]:
    """Load PDF links from pdf_links.json into a dictionary."""
    try:
        with open('pdf_links.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading PDF links: {e}")
        return {}

def extract_metadata(content: str, filepath: str, pdf_links: Dict[str, str], is_special_file: bool = False) -> Dict[str, str]:
    """Extract metadata from the first lines of the article and filepath."""
    lines = content.split('\n')
    metadata = {}
    
    # Extract date from filepath (format: MM_YY_vVV_iII)
    path_parts = Path(filepath).parts
    for part in path_parts:
        if '_v' in part:
            date_part = part.split('_v')[0]
            month, year = date_part.split('_')
            metadata['publication_date'] = f"{month}/{year}"
            
            # Construct PDF filename from path parts
            pdf_filename = f"{date_part}_v{part.split('_v')[1]}.pdf"
            metadata['pdf_link'] = pdf_links.get(pdf_filename)
            break
    
    if is_special_file:
        # For special files, we only need volume and issue
        if len(lines) > 1:
            vol_issue_match = re.search(r'Volume (\d+), Issue (\d+)', lines[1])
            if vol_issue_match:
                metadata['volume'] = vol_issue_match.group(1)
                metadata['issue'] = vol_issue_match.group(2)
        # Special files always start on page 1
        metadata['page'] = '1'
        return metadata
    
    # For regular articles, extract all metadata
    if len(lines) > 1:
        vol_issue_match = re.search(r'Volume (\d+), Issue (\d+)', lines[1])
        if vol_issue_match:
            metadata['volume'] = vol_issue_match.group(1)
            metadata['issue'] = vol_issue_match.group(2)
    
    if len(lines) > 3:
        title_match = re.search(r'\*\*Title: (.*?)\*\*', lines[3])
        if title_match:
            metadata['title'] = title_match.group(1)
    
    if len(lines) > 4:
        author_match = re.search(r'\*\*Author: (.*?)\*\*', lines[4])
        if author_match:
            metadata['author'] = author_match.group(1)
    
    # Extract page number
    if len(lines) > 5:
        page_match = re.search(r'\*\*Page number\(s\): (.*?)\*\*', lines[5])
        if page_match:
            page_str = page_match.group(1).strip()
            # Check if the first character is a number
            if page_str and page_str[0].isdigit():
                # Extract the first number from a range (e.g., "28-30" -> "28")
                start_page = re.match(r'(\d+)', page_str)
                if start_page:
                    metadata['page'] = start_page.group(1)
                else:
                    metadata['page'] = '1'
            else:
                metadata['page'] = '1'
        else:
            metadata['page'] = '1'
    else:
        metadata['page'] = '1'
    
    return metadata

def find_next_paragraph_break(text: str, start_pos: int) -> int:
    """Find the next paragraph break after start_pos."""
    next_break = text.find('\n\n', start_pos)
    if next_break == -1:
        next_break = text.find('\n', start_pos)
    return next_break

def split_article(filepath: str, pdf_links: Dict[str, str]) -> List[Dict[str, Any]]:
    """Split an article into chunks of text with metadata."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata from the first 5 lines
        metadata = extract_metadata(content, filepath, pdf_links)
        
        # Handle special files (toc.md or masthead.md)
        if filepath.endswith('toc.md') or filepath.endswith('masthead.md'):
            return [{
                'publication_date': metadata.get('publication_date', ''),
                'volume': metadata.get('volume', ''),
                'issue': metadata.get('issue', ''),
                'author': metadata.get('author', ''),
                'chunk_index': 0,
                'title': metadata.get('title', ''),
                'page': metadata.get('page', ''),
                'text': content,
                'pdf_link': metadata.get('pdf_link')
            }]
        
        # Skip the first 6 lines (metadata)
        lines = content.split('\n')
        content = '\n'.join(lines[6:])
        
        chunks = []
        current_pos = 0
        chunk_index = 1  # Start at 1 for unique indexing
        
        while current_pos < len(content):
            target_pos = current_pos + 1500  # Start with 1500 characters
            
            if target_pos >= len(content):
                # If we're at the end, take the remaining content
                chunk = content[current_pos:].strip()
                if chunk:
                    chunks.append({
                        'publication_date': metadata.get('publication_date', ''),
                        'volume': metadata.get('volume', ''),
                        'issue': metadata.get('issue', ''),
                        'author': metadata.get('author', ''),
                        'chunk_index': chunk_index,
                        'title': metadata.get('title', ''),
                        'page': metadata.get('page', ''),
                        'text': chunk,
                        'pdf_link': metadata.get('pdf_link')
                    })
                break
            
            # Find the next paragraph break after 1500 characters
            next_break = find_next_paragraph_break(content, target_pos)
            
            # If no paragraph break found or it's too far (beyond 2200), cap at 2200
            if next_break == -1 or next_break > current_pos + 2200:
                next_break = current_pos + 2200
            
            # Create the chunk
            chunk = content[current_pos:next_break].strip()
            if chunk:
                chunks.append({
                    'publication_date': metadata.get('publication_date', ''),
                    'volume': metadata.get('volume', ''),
                    'issue': metadata.get('issue', ''),
                    'author': metadata.get('author', ''),
                    'chunk_index': chunk_index,
                    'title': metadata.get('title', ''),
                    'page': metadata.get('page', ''),
                    'text': chunk,
                    'pdf_link': metadata.get('pdf_link')
                })
            
            current_pos = next_break
            chunk_index += 1
        
        return chunks
    
    except Exception as e:
        logging.error(f"Error processing {filepath}: {str(e)}")
        return []

def process_all_articles():
    """Process all articles in the split_articles directories."""
    project_root = Path(__file__).parent.parent.absolute()
    articles_dir = project_root / "processed" / "articles"
    
    # Load PDF links
    pdf_links = load_pdf_links()
    
    all_chunks = []
    total_articles = 0
    total_chunks = 0
    
    for issue_dir in articles_dir.iterdir():
        if not issue_dir.is_dir():
            continue
            
        split_articles_dir = issue_dir / "split_articles"
        if not split_articles_dir.exists():
            continue
            
        for file in split_articles_dir.glob("*.md"):
            try:
                chunks = split_article(str(file), pdf_links)
                all_chunks.extend(chunks)
                
                total_articles += 1
                total_chunks += len(chunks)
                logger.info(f"Processed {file.name}: {len(chunks)} chunks")
            except Exception as e:
                logger.error(f"Error processing {file}: {e}")
    
    # Save all chunks to a single JSON file
    output_file = project_root / "all_article_chunks.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=2)
    
    logger.info(f"Processed {total_articles} articles into {total_chunks} chunks")
    logger.info(f"All chunks saved to {output_file}")

def process_single_toc():
    """Process a single toc.md file for testing."""
    project_root = Path(__file__).parent.parent.absolute()
    test_file = project_root / "processed" / "articles" / "12_97_v30_i03" / "split_articles" / "toc.md"
    
    if not test_file.exists():
        logger.error(f"Test file not found: {test_file}")
        return
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            pdf_links = load_pdf_links()
            chunks = split_article(str(test_file), pdf_links)
            
            # Print metadata and content
            if chunks:
                logger.info(f"TOC metadata:")
                for key, value in chunks[0].items():
                    if key not in ['text', 'chunk_index', 'filepath']:
                        logger.info(f"{key}: {value}")
                
                logger.info("\nTOC content:")
                logger.info(chunks[0]['text'])
                
                # Save chunks to JSON for inspection
                output_file = project_root / "test_toc.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(chunks, f, indent=2)
                logger.info(f"\nFull TOC saved to {output_file}")
            else:
                logger.error("No chunks were generated")
                
    except Exception as e:
        logger.error(f"Error processing test file: {e}")

def split_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end > len(text):
            end = len(text)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def process_markdown_file(file_path: Path) -> List[Dict[str, Any]]:
    """Process a markdown file and return a list of chunks with metadata."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata
    lines = content.split('\n')
    metadata = {}
    current_section = None
    text_started = False
    text_lines = []

    for line in lines:
        if not text_started:
            if line.startswith('**'):
                current_section = line.strip('*')
                continue
            if line.startswith('Publication date:'):
                metadata['publication_date'] = line.split(': ')[1].strip()
            elif line.startswith('Volume:'):
                metadata['volume'] = line.split(': ')[1].strip()
            elif line.startswith('Issue number:'):
                metadata['issue'] = line.split(': ')[1].strip()
            elif line.startswith('**Title:'):
                metadata['title'] = line.split(': ')[1].strip('* ')
            elif line.startswith('**Author:'):
                metadata['author'] = line.split(': ')[1].strip('* ')
            elif line.startswith('**Page number(s):'):
                metadata['page'] = line.split(': ')[1].strip()
            elif line.strip() and not line.startswith('**'):
                text_started = True
                text_lines.append(line)
        else:
            text_lines.append(line)

    # Combine text lines
    text = '\n'.join(text_lines)
    
    # Split into chunks
    chunks = split_into_chunks(text)
    
    # Create chunk objects
    chunk_objects = []
    for i, chunk_text in enumerate(chunks, 1):  # Start index at 1
        chunk_obj = {
            'publication_date': metadata.get('publication_date', ''),
            'volume': metadata.get('volume', ''),
            'issue': metadata.get('issue', ''),
            'author': metadata.get('author', ''),
            'chunk_index': i,
            'title': metadata.get('title', ''),
            'page': metadata.get('page', ''),
            'text': chunk_text,
            'pdf_link': None  # Will be filled in later
        }
        chunk_objects.append(chunk_obj)
    
    return chunk_objects

def process_directory(input_dir: Path, output_file: Path):
    """Process all markdown files in a directory and save chunks to a JSON file."""
    all_chunks = []
    
    # Process each markdown file
    for file_path in input_dir.rglob('*.md'):
        print(f"Processing {file_path}")
        chunks = process_markdown_file(file_path)
        all_chunks.extend(chunks)
    
    # Save all chunks to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=2)
    
    print(f"Processed {len(all_chunks)} chunks from {len(list(input_dir.rglob('*.md')))} files")

if __name__ == "__main__":
    process_all_articles() 