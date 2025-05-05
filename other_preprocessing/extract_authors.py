import json
import logging
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Patterns to exclude from author names
EXCLUDED_PATTERNS = [
    "(Unnamed)",
    "Unnamed",
    "Not specified",
    "[Author not specified]",
    "[Author Name not provided]",
    "The Editors",
    "by",
    "(Not explicitly stated, inferred from context)",
    "No author explicitly stated",
    "Yale Daily News",
    "[Various]",
    "Unknown",
    "N/A",
    "The New Journal",
    "(unattributed)",
    "(Unattributed)",
    "The New Journal Staff",
    "(Not explicitly stated in the provided text)",
    "[No Author]",
    "[Author Name Missing]",
    "TNJ Staff",
    "T.N.J.",
    "Yale Institute of Sacred Music",
    "The Yale Bookstore",
    "The \"Original\" Copy Center",
    "Yale University",
    "Our Harvard Correspondent",
    "Heart of Glass",
    "(No Author Specified)",
    "(Not listed)"
]

def standardize_name(name):
    """Standardize a name for comparison by removing class years and normalizing case."""
    # Remove class year suffixes like '14 or 'XX
    name = re.sub(r"\s+'[0-9]{2}$", "", name)
    # Remove multiple spaces
    name = re.sub(r'\s+', ' ', name)
    # Convert to lowercase for comparison
    return name.lower().strip()

def is_valid_author(author):
    """Check if an author name is valid."""
    if not author or len(author) > 50:
        return False
    
    # Check for excluded patterns
    author_lower = author.lower()
    return not any(pattern.lower() in author_lower for pattern in EXCLUDED_PATTERNS)

def create_display_name(name):
    """Create a display name following the specified rules."""
    # Remove brackets if present
    name = re.sub(r'[\[\]]', '', name)
    
    # Remove class year suffix
    name = re.sub(r"\s+'[0-9]{2}$", "", name)
    
    # Check if name is in "A. O. Scott" format (initials only)
    if re.match(r'^[A-Z]\.\s+[A-Z]\.\s+[A-Z][a-z]+$', name):
        return name
    
    # Remove middle initials for names with full first names
    # This matches names like "Alex O. Scott" but not "A. O. Scott"
    name = re.sub(r'([A-Za-z]+)\s+[A-Z]\.?\s+([A-Za-z]+)', r'\1 \2', name)
    
    # Convert to title case
    name = name.title()
    
    return name.strip()

def split_multiple_authors(author_string):
    """Split a string containing multiple authors into individual names."""
    # Split on common separators: " and ", ", ", " & "
    separators = [r'\s+and\s+', r',\s+', r'\s+&\s+']
    for sep in separators:
        if re.search(sep, author_string):
            return re.split(sep, author_string)
    return [author_string]

def extract_authors():
    """Extract all unique author names from article chunks and save to JSON."""
    try:
        # Read the chunks
        try:
            with open('all_article_chunks.json', 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            logger.info(f"Loaded {len(chunks)} article chunks")
        except FileNotFoundError:
            logger.error("all_article_chunks.json not found. Please run split_into_chunks.py first.")
            return
        except json.JSONDecodeError:
            logger.error("Error parsing all_article_chunks.json. The file may be corrupted.")
            return

        # First pass: collect all individual authors
        authors = {}  # Key: standardized name, Value: author object
        
        for chunk in chunks:
            author = chunk.get('author', '').strip()
            if is_valid_author(author):
                # Split multiple authors
                individual_authors = split_multiple_authors(author)
                
                for individual_author in individual_authors:
                    individual_author = individual_author.strip()
                    if is_valid_author(individual_author):
                        std_name = standardize_name(individual_author)
                        if std_name not in authors:
                            authors[std_name] = {
                                'name_variations': [individual_author],
                                'display_name': create_display_name(individual_author)
                            }
                        elif individual_author not in authors[std_name]['name_variations']:
                            authors[std_name]['name_variations'].append(individual_author)
                        
                        # If this was part of a multiple author string, add the full string as a variation
                        if len(individual_authors) > 1 and author not in authors[std_name]['name_variations']:
                            authors[std_name]['name_variations'].append(author)

        # Convert to list of author objects
        author_list = list(authors.values())

        # Write to JSON file
        with open('authors.json', 'w', encoding='utf-8') as f:
            json.dump(author_list, f, indent=2, ensure_ascii=False)

        logger.info(f"Extracted {len(author_list)} unique authors to authors.json")

    except Exception as e:
        logger.error(f"Error in extract_authors: {e}")

if __name__ == "__main__":
    extract_authors() 