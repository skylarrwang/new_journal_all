import json
from supabase import create_client
import os
from dotenv import load_dotenv
from tqdm import tqdm
from datetime import datetime

def clean_article(article):
    required_fields = ['title', 'author', 'publication_date']
    if not article.get('title'):
        article['title'] = 'Unknown'
    if not article.get('author'):
        article['author'] = 'Unknown'
    if not article.get('publication_date'):
        article['publication_date'] = 'Unknown'
    return article

def migrate_to_supabase():
    return True

def migrate_to_supabase():
    # Load environment variables
    load_dotenv()
    
    # Initialize Supabase client
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: Missing Supabase credentials")
        return
        
    supabase = create_client(supabase_url, supabase_key)

    # Read the JSON file
    with open('cleaned_articles.json', 'r') as file:
        articles = json.load(file)
    
    success_count = 0
    error_count = 0
    skip_count = 0
    
    for article in tqdm(articles, desc="Uploading articles"):
        cleaned_article = clean_article(article)
        ##print("CLEANED ARTICLE: ", cleaned_article['publication_date'])
        formatted_publication_date = convert_date(cleaned_article['publication_date'])
        ##print("FORMATTED DATE: ", formatted_publication_date)
        try:
            # Create article object matching our schema
            article_data = {
                'title': cleaned_article['title'].strip(),
                'author': cleaned_article['author'].strip(),
                'publication_date': formatted_publication_date,
                'volume': cleaned_article.get('volume', '').strip(),
                'issue': cleaned_article.get('issue', '').strip(),
                'pdf_link': cleaned_article.get('pdf_link', '').strip(),
            }
            
           #  print(f"\nInserting: {article_data['title']}")
            
            # Insert the article
            response = supabase.table('articles').insert(article_data).execute()
            success_count += 1
            # print(f"Successfully inserted: {article_data['title']}")
                
        except Exception as e:
            error_count += 1
            print(f"\nError details:")
            print(f"Type: {type(e)}")
            print(f"Error: {str(e)}")
            print(f"Article data: {json.dumps(article_data, indent=2)}")
    
    print(f"\nMigration Summary:")
    print(f"Successfully inserted: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Skipped: {skip_count}")
    print(f"Total processed: {len(articles)}")

def convert_date(date_str) -> str | None:
    """
    Converts a date string from 'MM/YY' to 'YYYY-MM-01' for Supabase/Postgres date type.
    If the input is invalid, returns None (so Supabase stores NULL).
    """
    if not date_str or date_str.lower() == "unknown":
        return None
    try:
        dt = datetime.strptime(date_str, "%m/%Y")
        ##print("READ DATE: ", dt)
        return dt.strftime("%Y-%m-01")
    except Exception:
        return None

if __name__ == "__main__":
    migrate_to_supabase()
