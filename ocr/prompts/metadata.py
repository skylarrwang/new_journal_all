extract_headers = '''You will be provided with an image of the first page of a magazine. This page may include a portion of the table of contents, which typically contains the following details for each article:

Title of the article
Starting page number
Author name (if available)
If the table of contents is present, extract the relevant information.
Be careful about spacing and alignment of author names, and also be aware that the formatting may be different for each article.
Return it in the following JSON format, where each entry corresponds to an article in the contents section:
{
    "title": "Title of the article",
    "page": "Starting page number",
    "author": "Author name (if available)"
}
If the table of contents is not present, please return an empty string.'''

verify_contents = '''You will be given a list of dictionaries with "title", "page", and "author" fields.
There may be some misalignments in the data. Please look at this image and verify the data is correct.
If the data is incorrect, please return the correct data in JSON format as a list of dictionaries with "title", "page", and "author" fields.
If the data is correct, please return the original data.'''