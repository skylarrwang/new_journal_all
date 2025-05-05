from vision_parse import VisionParser
import inspect
from dotenv import load_dotenv
load_dotenv()

# get the gemini api key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

pdf_path = "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/12_06_1977.pdf"
custom_prompt = "Try to identify the title of the article, the author, and the date of the article."


# Initialize parser with Google Gemini model
parser = VisionParser(
    model_name="gemini-2.0-flash-lite",
    api_key=gemini_api_key, # Get the Gemini API key from https://aistudio.google.com/app/apikey
    temperature=0.7,
    custom_prompt=custom_prompt,
    top_p=0.4,
    image_mode="url",
    detailed_extraction=False, # Set to True for more detailed extraction
    enable_concurrency=True,
)

# Parse the PDF file
parsed_data = parser.convert_pdf(pdf_path)

for i, page_content in enumerate(parsed_data):
    print(f"\n--- Page {i+1} ---\n{page_content}")

# put it in a markdown file
with open("DEC_NEW_ISSUE_VISION_PARSE_Flash_Lite.md", "w") as f:
    for i, page_content in enumerate(parsed_data):
        f.write(f"\n--- Page {i+1} ---\n{page_content}")
