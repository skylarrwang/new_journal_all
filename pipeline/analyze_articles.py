import os
from pathlib import Path
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_articles():
    """Analyze statistics of all article files in split_articles subdirectories."""
    # Get the absolute path of the project root
    project_root = Path(__file__).parent.parent.absolute()
    articles_dir = project_root / "processed" / "articles"
    
    # Initialize list to store file lengths
    file_lengths = []
    total_files = 0
    total_issues = 0
    longest_article = {"length": 0, "path": None}
    
    # Walk through all directories and files
    for issue_dir in articles_dir.iterdir():
        if not issue_dir.is_dir():
            continue
            
        total_issues += 1
        split_articles_dir = issue_dir / "split_articles"
        
        if not split_articles_dir.exists():
            logger.warning(f"No split_articles directory found in {issue_dir}")
            continue
            
        for file in split_articles_dir.glob("*.md"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    length = len(content)
                    file_lengths.append(length)
                    total_files += 1
                    
                    # Track longest article
                    if length > longest_article["length"]:
                        longest_article["length"] = length
                        longest_article["path"] = str(file)
            except Exception as e:
                logger.error(f"Error reading {file}: {e}")
    
    if not file_lengths:
        logger.error("No article files found")
        return
    
    # Calculate statistics
    lengths_array = np.array(file_lengths)
    stats = {
        'total_files': total_files,
        'total_issues': total_issues,
        'min_length': np.min(lengths_array),
        'max_length': np.max(lengths_array),
        'mean_length': np.mean(lengths_array),
        'median_length': np.median(lengths_array),
        'std_dev': np.std(lengths_array)
    }
    
    # Print results
    logger.info(f"Analysis of {stats['total_files']} article files across {stats['total_issues']} issues:")
    logger.info(f"Minimum length: {stats['min_length']} characters")
    logger.info(f"Maximum length: {stats['max_length']} characters")
    logger.info(f"Mean length: {stats['mean_length']:.2f} characters")
    logger.info(f"Median length: {stats['median_length']} characters")
    logger.info(f"Standard deviation: {stats['std_dev']:.2f} characters")
    
    # Print some percentiles
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    for p in percentiles:
        value = np.percentile(lengths_array, p)
        logger.info(f"{p}th percentile: {value:.2f} characters")
    
    # Print longest article info
    if longest_article["path"]:
        logger.info(f"\nLongest article ({longest_article['length']} characters) found at:")
        logger.info(f"Path: {longest_article['path']}")
        try:
            with open(longest_article["path"], 'r', encoding='utf-8') as f:
                content = f.read()
                # Print first few lines
                first_lines = content.split('\n')[:5]
                logger.info("\nFirst few lines of the longest article:")
                for line in first_lines:
                    logger.info(line)
        except Exception as e:
            logger.error(f"Error reading longest article content: {e}")

if __name__ == "__main__":
    analyze_articles() 