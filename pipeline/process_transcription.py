import os
import re
import sys
from pathlib import Path

def find_three_consecutive_headers(text):
    """Find the position of the first of three consecutive headers."""
    lines = text.split('\n')
    header_count = 0
    first_header_pos = None
    
    for i, line in enumerate(lines):
        if line.strip().startswith('**') and line.strip().endswith('**'):
            if header_count == 0:
                first_header_pos = i
            header_count += 1
            if header_count == 3:
                return first_header_pos
        else:
            header_count = 0
            first_header_pos = None
    
    return None

def process_file(file_path):
    """Process a single file according to the specified rules."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all [ADVERTISEMENT] labels
        ad_pattern = r'\[ADVERTISEMENT\]'
        ad_matches = list(re.finditer(ad_pattern, content))
        
        if not ad_matches:
            print(f"No advertisements found in {file_path}")
            return
        
        # Process each advertisement section
        new_content = []
        last_pos = 0
        
        for ad_match in ad_matches:
            # Add content before this advertisement
            new_content.append(content[last_pos:ad_match.start()])
            
            # Get the text after this advertisement
            text_after_ad = content[ad_match.end():]
            
            # Find the position of the first of three consecutive headers
            first_header_line = find_three_consecutive_headers(text_after_ad)
            
            if first_header_line is not None:
                # Convert line number to character position
                lines_before_header = text_after_ad.split('\n')[:first_header_line]
                chars_before_header = len('\n'.join(lines_before_header)) + 1  # +1 for the newline
                first_header_pos = ad_match.end() + chars_before_header
                last_pos = first_header_pos
            else:
                # If no three consecutive headers found, keep everything after the advertisement
                last_pos = ad_match.end()
        
        # Add any remaining content after the last advertisement
        new_content.append(content[last_pos:])
        
        # Combine all parts and write back to file
        final_content = ''.join(new_content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"Successfully processed {file_path}")
        print(f"Found and processed {len(ad_matches)} advertisements")
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_transcription.py <filepath>")
        sys.exit(1)
        
    target_file = Path(sys.argv[1])
    if target_file.exists():
        print(f"Processing file: {target_file}")
        process_file(target_file)
    else:
        print(f"File not found: {target_file}") 