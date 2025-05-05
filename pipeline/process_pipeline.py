import os
import subprocess
from pathlib import Path
import logging
import shutil
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the absolute path of the project root
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

def setup_workspace(issue_name):
    """Create a workspace directory for the issue if it doesn't exist."""
    workspace = PROJECT_ROOT / "processed" / "articles" / issue_name
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace

def process_magazine(pdf_path, workspace):
    """Run process_magazine.py on the PDF"""
    try:
        # Run process_magazine.py from the pipeline directory
        subprocess.run(
            ["python", str(PROJECT_ROOT / "pipeline" / "process_magazine.py"), str(pdf_path)],
            check=True,
            cwd=str(PROJECT_ROOT)
        )
        
        # Move the resulting markdown file to the workspace
        markdown_file = pdf_path.parent / "markdowns" / pdf_path.with_suffix('.md').name
        if markdown_file.exists():
            shutil.move(str(markdown_file), str(workspace / markdown_file.name))
            return workspace / markdown_file.name
        else:
            logging.error(f"Markdown file not found: {markdown_file}")
            return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to process magazine: {e}")
        return None

def process_transcription(markdown_file, workspace):
    """Run process_transcription.py on the markdown file."""
    logger.info(f"Processing transcription: {markdown_file}")
    try:
        subprocess.run(
            ["python", str(PROJECT_ROOT / "pipeline" / "process_transcription.py"), str(markdown_file)],
            check=True,
            cwd=str(PROJECT_ROOT)
        )
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to process transcription: {e}")
        return False

def split_articles(markdown_file, workspace):
    """Run split_articles.py on the processed markdown file."""
    logger.info(f"Splitting articles: {markdown_file}")
    try:
        subprocess.run(
            ["python", str(PROJECT_ROOT / "pipeline" / "split_articles.py"), str(markdown_file)],
            check=True,
            cwd=str(PROJECT_ROOT)
        )
        
        # Move all article files to the workspace
        for article_file in Path(".").glob("article_*.md"):
            shutil.move(str(article_file), str(workspace / article_file.name))
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to split articles: {e}")
        return False

def process_issue(issue_name):
    """Process a single issue through the entire pipeline."""
    logger.info(f"Starting processing for issue: {issue_name}")
    
    # Create workspace
    workspace = setup_workspace(issue_name)
    
    # Get PDF path
    pdf_path = PROJECT_ROOT / "sample_data" / "tnjarchive" / f"{issue_name}.pdf"
    if not pdf_path.exists():
        logger.error(f"PDF file not found: {pdf_path}")
        return False
    
    # Process magazine
    markdown_file = process_magazine(pdf_path, workspace)
    if not markdown_file:
        return False
    
    # Process transcription
    if not process_transcription(markdown_file, workspace):
        return False
    
    # Split articles
    if not split_articles(markdown_file, workspace):
        return False
    
    logger.info(f"Successfully processed issue: {issue_name}")
    return True

def main():
    """Process all PDFs in the tnjarchive directory"""
    # Get all PDF files from the tnjarchive directory
    pdf_dir = PROJECT_ROOT / "sample_data" / "tnjarchive"
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        logging.error("No PDF files found in tnjarchive directory")
        return
    
    logging.info(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF
    for i, pdf_path in enumerate(pdf_files, 1):
        issue_name = pdf_path.stem
        logging.info(f"Processing file {i}/{len(pdf_files)}: {issue_name}")
        
        try:
            # Check if this issue has already been processed
            workspace = PROJECT_ROOT / "processed" / "articles" / issue_name
            if workspace.exists() and any(workspace.glob("*.md")):
                logging.info(f"Skipping {issue_name} - already processed")
                continue
                
            # Process the issue
            success = process_issue(issue_name)  # Pass just the issue name
            if success:
                logging.info(f"Successfully processed {issue_name}")
            else:
                logging.error(f"Failed to process {issue_name}")
            
        except Exception as e:
            logging.error(f"Failed to process {issue_name}: {str(e)}")
            continue
    
    logging.info("Processing complete")

if __name__ == "__main__":
    main() 