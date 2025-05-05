from splitters import SemanticTextSplitter, RecursiveTextSplitter
from utils import save_docs_to_file, save_docs_as_json, save_docs_as_list


sample_data_path = "/Users/srwang/Documents/CPSC381/new_journal/new_journal/sample_data/12_06_1977.pdf"
full_article_path = "./test_markdowns/DEC_NEW_ISSUE_VISION_PARSE_Flash_Lite.md"
single_article_path = "./test_markdowns/SINGLE_ART.md"
small_article_path = "./test_markdowns/SMALL_ART.md"
bread_article_path = "./test_markdowns/BREAD.MD"
def test_single_article(file_name: str, markdown_text: str):
    semantic_splitter = SemanticTextSplitter(text=markdown_text, embedding_model="openai", breakpoint_threshold_amount=85)
    semantic_splitter.split_text()
    save_docs_to_file(semantic_splitter.split_text_docs, f"test_outputs/{file_name}_semantic_split_docs.txt")
    save_docs_as_json(semantic_splitter.split_text_docs, f"test_outputs/{file_name}_semantic_split_docs.json")
    # recursive_splitter = RecursiveTextSplitter(markdown_text)
    # recursive_splitter.split_text()
    # save_docs_to_file(recursive_splitter.split_text_docs, f"test_outputs/{file_name}_recursive_split_docs.txt")


with open(single_article_path, "r") as file:
    big_text = file.read()

with open(small_article_path, "r") as file:
    small_text = file.read()

with open(bread_article_path, "r") as file:
    bread_text = file.read()  

with open(full_article_path, "r") as file:
    full_text = file.read()  

# test_single_article("small_article", small_text)
# test_single_article("bread_article", bread_text)
# test_single_article("big_article_recursive", big_text)
test_single_article("full_article", full_text)
# take 