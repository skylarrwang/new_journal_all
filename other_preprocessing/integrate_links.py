import json
import csv
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_pdf_filename(publication_date, volume, issue):
    """Convert publication date, volume, and issue to PDF filename format."""
    try:
        month, year = publication_date.split('/')
        # Pad month, volume, and issue with zeros
        month = month.zfill(2)
        volume = str(volume).zfill(2)
        issue = str(issue).zfill(2)
        return f"{month}_{year[-2:]}_v{volume}_i{issue}.pdf"
    except Exception as e:
        logger.error(f"Error generating PDF filename: {e}")
        return None

def integrate_links():
    """Integrate PDF links with article chunks."""
    try:
        # Read the links from CSV
        links = {}
        try:
            with open('all_links.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        filename, url = row
                        links[filename] = url
            logger.info(f"Loaded {len(links)} PDF links from all_links.csv")
        except FileNotFoundError:
            logger.error("all_links.csv not found. Please ensure the file exists.")
            return

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

        # Add links to chunks
        updated_count = 0
        missing_links = 0
        
        for chunk in chunks:
            pdf_filename = get_pdf_filename(
                chunk['publication_date'],
                chunk['volume'],
                chunk['issue']
            )
            
            if pdf_filename and pdf_filename in links:
                chunk['pdf_link'] = links[pdf_filename]
                updated_count += 1
            else:
                missing_links += 1
                if pdf_filename:
                    logger.warning(f"No PDF link found for {pdf_filename}")

        # Save updated chunks
        with open('all_article_chunks.json', 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2)

        logger.info(f"Processed {len(chunks)} chunks:")
        logger.info(f"- Updated {updated_count} chunks with PDF links")
        logger.info(f"- {missing_links} chunks missing PDF links")

    except Exception as e:
        logger.error(f"Error in integrate_links: {e}")

if __name__ == "__main__":
    integrate_links() 