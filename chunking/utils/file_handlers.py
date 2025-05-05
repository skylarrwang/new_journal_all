from typing import List
import os
import json

def save_docs_to_file(docs: List[str], path: str):
    with open(path, "w") as file:
        for doc in docs:
            file.write("------------- NEW DOC -------------------")
            file.write("\n")
            file.write(doc)
            file.write("\n")

def save_docs_to_dir(docs: List[str], dir_path: str):
    os.makedirs(dir_path, exist_ok=True)
    for i, doc in enumerate(docs):
        file_path = os.path.join(dir_path, f"doc_{i}.txt")
        with open(file_path, "w") as file:
            file.write("------------- NEW DOC -------------------")
            file.write("\n")
            file.write(doc)
            file.write("\n")

def save_docs_as_list(docs: List[str], path: str):
    with open(path, "w") as file:
        file.write("[")
        for doc in docs[:-1]:
            file.write(f"{doc}")
            file.write(",")
        file.write(str(docs[-1]))
        file.write("]")

def save_docs_as_json(docs: List[str], output_path: str) -> None:
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(docs, file, indent=2)