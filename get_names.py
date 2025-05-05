import json
import re

def clean_name(name):
    # Remove special characters and extra spaces from the end of the name
    cleaned = name.strip()
    # Remove any special characters at the end of the name while preserving periods
    cleaned = re.sub(r'[^a-zA-Z\s\.]$', '', cleaned)
    # Replace multiple spaces with single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned

def extract_names():
    # Read the JSON file
    with open('all_chunks.json', 'r') as f:
        data = json.load(f)
    
    # Set to store unique names
    names = set()
    
    # Iterate through the chunks and extract names
    for chunk in data:
        if 'author' in chunk:
            cleaned_name = clean_name(chunk['author'])
            # Only add if the cleaned name is not empty
            if cleaned_name:
                names.add(cleaned_name)
    
    # Convert set to sorted list
    name_list = sorted(list(names))
    
    # Create the CSV string
    csv_string = '[' + ', '.join(f'"{name}"' for name in name_list) + ']'
    
    # Write to output file
    with open('names.csv', 'w') as f:
        f.write(csv_string)
    
    print(f"Found {len(name_list)} unique names")
    print("Names have been written to names.csv")

def capitalize_names():
    try:
        # Read the existing CSV file
        with open('names.csv', 'r') as f:
            content = f.read()
            # Convert string list to actual list by splitting on commas
            # and cleaning up the quotes and brackets
            content = content.strip('[]')
            names = [name.strip().strip('"') for name in content.split(',')]
        
        # Properly capitalize each name
        capitalized_names = []
        for name in names:
            # Split name into words
            words = name.split()
            # Capitalize first letter, make rest lowercase for each word
            capitalized_words = [word[0].upper() + word[1:].lower() if word else '' for word in words]
            capitalized_name = ' '.join(capitalized_words)
            capitalized_names.append(capitalized_name)
        
        # Sort the names
        capitalized_names.sort()
        
        # Create the CSV string
        csv_string = '[' + ', '.join(f'"{name}"' for name in capitalized_names) + ']'
        
        # Write back to the file
        with open('names.csv', 'w') as f:
            f.write(csv_string)
        
        print(f"Properly capitalized {len(capitalized_names)} names")
        print("Updated names have been written to names.csv")
    
    except FileNotFoundError:
        print("Error: names.csv file not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # extract_names()
    capitalize_names()
