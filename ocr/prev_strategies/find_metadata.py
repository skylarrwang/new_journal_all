def parse_journal_articles(text):
    # Split into pages
    pages = text.split("--- Page")
    
    articles = []
    current_article = {
        'title': None,
        'author': None,
        'text': [],
        'pages': [],
        'continues_from': None,
        'continues_to': None
    }
    
    for page in pages:
        # Extract page number
        page_num = extract_page_number(page)
        
        # Split page into potential article segments
        segments = page.split('\n\n')  # Double newline often separates articles
        
        for segment in segments:
            # Check for new article markers:
            # 1. Title-like formatting (all caps or prominent position)
            # 2. No continuation marker
            if is_new_article_start(segment):
                if current_article['title']:
                    articles.append(current_article)
                current_article = new_article_dict()
                current_article['title'] = extract_title(segment)
            
            # Check for article endings (often has author)
            if has_author_signature(segment):
                current_article['author'] = extract_author(segment)
            
            # Check for continuations
            if "continued from" in segment.lower():
                current_article['continues_from'] = extract_continuation_page(segment)
            
            current_article['pages'].append(page_num)
            current_article['text'].append(segment)
    
    return articles

def is_new_article_start(text):
    # Heuristics for article starts:
    # - Capitalized text
    # - No continuation marker
    # - Typical title length
    # - Position on page
    pass

def extract_author(text):
    # Look for patterns like:
    # "- by Author Name"
    # "-Author Name"
    # "Author Name is ..." (biographical note)
    author_patterns = [
        r'-\s*by\s+(.*?)$',
        r'-\s*(.*?)$',
        r'by\s+(.*?)$'
    ]
    pass

def extract_title(text):
    # Look for:
    # - First prominent line
    # - All caps sections
    # - Text before author or body
    pass