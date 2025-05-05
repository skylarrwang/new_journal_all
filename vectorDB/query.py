from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings

model = OpenAIEmbeddings()
qdrant = Qdrant(
    url="http://localhost:6333",
    collection_name=COLLECTION_NAME,
)

query_vector = model.encode(["Find something Jane Doe wrote"], convert_to_numpy=True)[0]

hits = qdrant.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_vector.tolist(),
    limit=5,
    query_filter={
        "must": [
            {"key": "author", "match": {"value": "Jane Doe"}},
            {"key": "journal_issue", "match": {"value": "Vol. 1 No. 2"}},
        ]
    }
)

for hit in hits:
    print(f"Score: {hit.score:.3f}")
    print(f"Text: {hit.payload['text']}")
    print(f"Metadata: {hit.payload}")
    print("---")
