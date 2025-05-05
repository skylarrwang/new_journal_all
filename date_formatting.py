import json
from datetime import datetime
from tqdm import tqdm

def convert_date(date_str) -> str | None:
    """
    Converts a date string from 'MM/YY' to 'YYYY-MM-01' for Supabase/Postgres date type.
    If the input is invalid, returns None (so Supabase stores NULL).
    If YY > 25, uses 19YY; else uses 20YY.
    """
    if not date_str or date_str.lower() == "unknown":
        return None
    try:
        month, year = date_str.split('/')
        year = int(year)
        if year > 25:
            full_year = 1900 + year
        else:
            full_year = 2000 + year
        return f"{full_year}-{int(month):02d}-01"
    except Exception:
        return None
    

if __name__ == "__main__":
    file_path = "all_chunks.json"
    new_file_path = "all_chunks_formatted_date.json"
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for item in tqdm(data, desc="Processing items"):
        item['publication_date'] = convert_date(item['publication_date'])
    
    with open(new_file_path, 'w') as file:
        json.dump(data, file, indent=2)