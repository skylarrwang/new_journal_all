markdown_prompt = """
Your task is to analyze the given image of a newspaper page and extract textual content in markdown format.

- Analyze this page carefully and extract all the content from the provided image in markdown format.
- If a title is detected, extract it as a header level 1 using "#"
- If an author is detected, extract it as header level 3 using "###". Authors may be written at the beginning of the article or at the end of the article. Look for patterns like "By Author Name" or "Author Name, Author Name" to identify the author. Format this as a header level 2 at the beginning of the article.
- If a date for the written article is detected, extract it as a header level 4 using "####".
- Strictly follow the markdown formatting rules and do not change any content in the original extracted text while markdown formatting. Do not repeat the extracted text.
"""

verify_markdown_prompt = """
- Compare if the extracted text matches with the image content:\n\n```markdown\n{{ first_pass_markdown }}\n```\n\n
- Strictly do not change any content in the original extracted text while applying markdown formatting and do not repeat the extracted text.
"""