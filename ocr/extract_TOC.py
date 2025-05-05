from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from .utils import pdf_by_page, string_to_dict
from .prompts.metadata import extract_headers as extract_headers_prompt, verify_contents as verify_contents_prompt
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
pdf_paths = {"feb_issue": "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/02_2025.pdf",
             "may_issue": "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/05_14_1968.pdf",
             "dec_issue": "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/12_06_1977.pdf"}

def get_metadata(pdf_path: str) -> dict:
    FOUND = False
    page_number = 1
    while not FOUND and page_number < 4:
        table_of_contents = pdf_by_page(pdf_path, page_number)

        # generate human message for the table of contents
        message = HumanMessage(
            content=[
                {"type": "text", "text": extract_headers_prompt},
                {"type": "image_url", "image_url": f"data:image/png;base64,{table_of_contents}"}
            ]
        )

        # set up the gemini image
        llm = ChatGoogleGenerativeAI(
            google_api_key=gemini_api_key,
            model="gemini-2.0-flash-lite",
            temperature=0.3,
            top_p=0.2
        )

        # print("nice")
        # generate the response
        first_pass_response = llm.invoke([message])

        # check if an author is returned
        if "author" in first_pass_response.content:
            # verify the response
            verify_message = HumanMessage(
                content=[
                    {"type": "text", "text": verify_contents_prompt},
                    {"type": "image_url", "image_url": f"data:image/png;base64,{table_of_contents}"}
                ]
            )

            verify_response = llm.invoke([verify_message])
            # print the response content
            print(verify_response.content)
            FOUND = True
            break
        else:
            page_number += 1

    if FOUND:
        return string_to_dict(verify_response.content)
    else:
        return "No author found"

if __name__ == "__main__":
    print("-----feb issue-----")
    print(get_metadata(pdf_paths["feb_issue"]))
    print("-----may issue-----")
    print(get_metadata(pdf_paths["may_issue"]))
    print("-----dec issue-----")
    print(get_metadata(pdf_paths["dec_issue"]))