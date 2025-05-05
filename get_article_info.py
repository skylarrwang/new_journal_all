import json

def process_json():
    # Read the JSON file
    with open('all_chunks.json', 'r') as file:
        data = json.load(file)
    
    # Set to keep track of unique entries (using title + publication_date + author as key)
    seen_entries = set()
    cleaned_data = []
    
    # Process each object
    for item in data:
        # Remove unwanted keys
        if 'embedding' in item:
            del item['embedding']
        if 'chunk_index' in item:
            del item['chunk_index']
        if 'page' in item:
            del item['page']
            
        # Create a unique identifier for the article
        unique_key = f"{item['title']}|{item['publication_date']}|{item['author']}"
        
        # Only add if we haven't seen this article before
        if unique_key not in seen_entries:
            seen_entries.add(unique_key)
            cleaned_data.append(item)
    
    # Write the cleaned data to a new file
    with open('cleaned_articles.json', 'w') as file:
        json.dump(cleaned_data, file, indent=2)
    
    print(f"Processed {len(data)} entries")
    print(f"Found {len(cleaned_data)} unique articles")

def delete_text_from_json():
    with open('cleaned_articles.json', 'r') as file:
        data = json.load(file)
    
    for item in data:
        del item['text']
        
    with open('cleaned_articles.json', 'w') as file:
        json.dump(data, file, indent=2)


def format_year(year_str):
    # Convert 2-digit year to 4-digit year
    year = int(year_str)
    if 0 <= year <= 24:  # Current years (2000-2024)
        return f"20{year:02d}"
    else:  # Past years (1925-1999)
        return f"19{year:02d}"

def reformat_dates():
    # Read the JSON file
    with open('cleaned_articles.json', 'r') as file:
        data = json.load(file)
    
    # Process each object
    for item in data:
        if 'publication_date' in item:
            month, year = item['publication_date'].split('/')
            # Format with 4-digit year
            item['publication_date'] = f"{month}/{format_year(year)}"
    
    # Write back to file
    with open('cleaned_articles.json', 'w') as file:
        json.dump(data, file, indent=2)
    
    print("Updated all dates to 4-digit year format")

if __name__ == "__main__":
    # process_json()
    delete_text_from_json()
    reformat_dates()