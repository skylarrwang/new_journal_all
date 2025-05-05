import re
from pathlib import Path

def extract_metadata_from_path(filepath):
    """Extract publication date, volume, and issue from filepath."""
    # Extract components from path format MM_YY_vXX_iYY
    pattern = r'(\d{2})_(\d{2})_v(\d{2})_i(\d{2})'
    match = re.search(pattern, str(filepath))
    if match:
        month, year, volume, issue = match.groups()
        pub_date = f"{month}/{year}"
        return {
            'publication_date': pub_date,
            'volume': volume.lstrip('0'),  # Remove leading zeros
            'issue': issue.lstrip('0')
        }
    return None

def find_special_sections(text):
    """Find MASTHEAD and TABLE OF CONTENTS sections."""
    special_sections = []
    
    # Find MASTHEAD section
    masthead_match = re.search(r'\*\*MASTHEAD:\*\*\n(.*?)(?=\n\*\*|$)', text, re.DOTALL)
    if masthead_match:
        special_sections.append(('masthead', masthead_match.group(0)))
    
    # Find TABLE OF CONTENTS section
    toc_match = re.search(r'\*\*TABLE OF CONTENTS:\*\*\n(.*?)(?=\n\*\*|$)', text, re.DOTALL)
    if toc_match:
        special_sections.append(('toc', toc_match.group(0)))
    
    return special_sections

def remove_special_sections(text, special_sections):
    """Remove special sections from the text."""
    result = text
    for _, section_text in special_sections:
        result = result.replace(section_text, '')
    return result.strip()

def find_article_boundaries(text, special_sections):
    """Find the positions of article boundaries in the text."""
    # First remove special sections from consideration
    remaining_text = remove_special_sections(text, special_sections)
    
    # Find all headers (lines starting and ending with **)
    headers = [(m.start(), m.end()) for m in re.finditer(r'^\*\*.*?\*\*$', remaining_text, re.MULTILINE)]
    
    # Find groups of three consecutive headers
    boundaries = []
    for i in range(len(headers) - 2):
        if (headers[i+1][0] - headers[i][1] <= 2 and  # Consecutive headers
            headers[i+2][0] - headers[i+1][1] <= 2):
            boundaries.append(headers[i][0])  # Start of first header in group
    
    return boundaries

def cleanup_small_files(output_dir, min_size=300):
    """Delete files that are smaller than min_size characters, excluding masthead and toc."""
    deleted_count = 0
    for file_path in output_dir.glob('*.md'):
        # Skip masthead and toc files
        if file_path.name in ['masthead.md', 'toc.md']:
            continue
            
        # Check file size
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content) < min_size:
                file_path.unlink()
                deleted_count += 1
    return deleted_count

def split_into_articles(input_file):
    """Split the input markdown file into separate articles."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata from filepath
    metadata = extract_metadata_from_path(input_file)
    
    # Find special sections
    special_sections = find_special_sections(content)
    
    # Create output directory
    output_dir = Path(input_file).parent / 'split_articles'
    output_dir.mkdir(exist_ok=True)
    
    # Write special sections first
    for section_type, section_text in special_sections:
        output_file = output_dir / f'{section_type}.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            # Add metadata to special sections too
            if metadata:
                f.write(f"Publication date: {metadata['publication_date']}\n")
                f.write(f"Volume {metadata['volume']}, Issue {metadata['issue']}\n\n")
            f.write(section_text)
    
    # Remove special sections and find article boundaries
    remaining_text = remove_special_sections(content, special_sections)
    boundaries = find_article_boundaries(remaining_text, special_sections)
    
    # Split and write articles
    for i, start_pos in enumerate(boundaries, 1):
        if i < len(boundaries):
            end_pos = boundaries[i]
        else:
            end_pos = len(remaining_text)
        
        article_content = remaining_text[start_pos:end_pos].strip()
        if article_content:
            output_file = output_dir / f'article_{i}.md'
            with open(output_file, 'w', encoding='utf-8') as f:
                # Add metadata at the top of each article
                if metadata:
                    f.write(f"Publication date: {metadata['publication_date']}\n")
                    f.write(f"Volume {metadata['volume']}, Issue {metadata['issue']}\n\n")
                f.write(article_content)
    
    # Clean up small files
    deleted_count = cleanup_small_files(output_dir)
    
    return len(special_sections), len(boundaries), deleted_count

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python split_articles.py <markdown_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    num_special, num_articles, num_deleted = split_into_articles(input_file)
    print(f"\nSuccessfully split {num_special} special sections and {num_articles} articles into {Path(input_file).parent}/split_articles")
    print(f"Deleted {num_deleted} files that were smaller than 300 characters") 