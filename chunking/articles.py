"""
Given a full issue in markdown formatting,
split the issue into articles based on the headers.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ocr.extract_TOC import get_metadata

issue_markdown_path = "/Users/srwang/Documents/CPSC381/new_journal/new_journal/chunking/DEC_NEW_ISSUE_VISION_PARSE_Flash_Lite.md"
issue_pdf_path = "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/12_06_1977.pdf"

def split_issue(issue_pdf_path: str, issue_markdown_path: str) -> list[str]:
    """
    Split the issue into articles based on the headers.
    """
    issue_metadata = get_metadata(issue_pdf_path)
    if not issue_metadata:
        raise ValueError("No metadata found in the issue")
    
    #get titles
    titles = []
    for article in issue_metadata:
        titles.append(article["title"])
    
    #split the issue into articles based on the titles
    articles = titles_to_articles(issue_markdown_path, titles)
    print(articles)

    #save the articles to a file
    with open("articles.md", "w") as file:
        for article in articles:
            file.write("\n\n------DETECTED SPLIT------\n")
            file.write(article)

    return articles

def titles_to_articles(issue_path: str, titles: list) -> list:
    """Split journal issue into articles based on titles.
    
    Args:
        issue_path (str): Full journal text in markdown
        titles (list): List of article titles
    
    Returns:
        list: List of articles with their titles
    """
    articles = []
    remaining_text = ""
    with open(issue_path, "r") as file:
        remaining_text = file.read()
    
    # Sort titles by their position in the text to maintain order
    title_positions = [(title, remaining_text.find(title)) for title in titles]
    title_positions = sorted(title_positions, key=lambda x: x[1])
    
    # Split text between consecutive titles
    for i in range(len(title_positions)):
        current_title, start = title_positions[i]
        
        # Get end position (either next title or end of text)
        if i < len(title_positions) - 1:
            end = title_positions[i + 1][1]
        else:
            end = None
            
        if start != -1:  # If title was found
            article = remaining_text[start:end]
            articles.append(article.strip())
    
    return articles

if __name__ == "__main__":
    # Point to the markdown file instead of PDF
    split_issue(issue_pdf_path, issue_markdown_path)
    print("Done")