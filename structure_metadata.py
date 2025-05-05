import json
import re

def process_filepath(filepath):
    # Extract magazine_id using regex
    magazine_id_match = re.search(r'articles/([^/]+)/split_articles', filepath)
    magazine_id = magazine_id_match.group(1) if magazine_id_match else None
    
    # Extract article_id using regex
    article_id_match = re.search(r'article_(\d+)\.md$', filepath)
    article_id = int(article_id_match.group(1)) if article_id_match else None
    
    return magazine_id, article_id

def update_embeddings_file(input_path, output_path):
    # Read the original file
    with open(input_path, 'r') as file:
        embeddings = json.load(file)

    # Process each item
    for item in embeddings:
        if 'filepath' in item:
            magazine_id, article_id = process_filepath(item['filepath'])
            
            # Add new fields
            item['magazine_id'] = magazine_id
            item['article_id'] = article_id
            
            # Optionally, remove the original filepath if you don't need it anymore
            # del item['filepath']
    
    # Write the updated data back to a new file
    with open(output_path, 'w') as file:
        json.dump(embeddings, file, indent=2)
    
    print(f"Processed {len(embeddings)} items")
    print(f"Sample transformation for first item:")
    print(f"Magazine ID: {embeddings[0]['magazine_id']}")
    print(f"Article ID: {embeddings[0]['article_id']}")

# Run the update
input_file = "embeddings.json"  # adjust path as needed
output_file = "embeddings_updated.json"  # adjust path as needed
update_embeddings_file(input_file, output_file)
