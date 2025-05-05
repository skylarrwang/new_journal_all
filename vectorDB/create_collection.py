from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter
from sentence_transformers import SentenceTransformer
import uuid
import json
from dotenv import load_dotenv
import os
from tqdm import tqdm
# load environment variables
load_dotenv()
QDRANT_CLOUD_URL = os.getenv("QDRANT_CLOUD_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# ---- Configuration ----
COLLECTION_NAME = "new_journal_chunks"
EMBEDDING_PATH = "../all_chunks_formatted_date.json"

# Qdrant Cloud instance
qdrant = QdrantClient(
    url=QDRANT_CLOUD_URL,
    api_key=QDRANT_API_KEY,
)

# ---- Create Collection if Not Exists ----
# Only needs to be run once
def create_collection():
    if not qdrant.collection_exists(collection_name=COLLECTION_NAME):
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),  # 384 for MiniLM
        )
        print(f"Collection {COLLECTION_NAME} created.")
    else:
        print(f"Collection {COLLECTION_NAME} already exists.")

# create_collection()

def load_chunks_from_json(json_path: str):
    with open(json_path, "r") as file:
        chunks = json.load(file)
    print(f"Loaded {len(chunks)} chunks from {json_path}")
    return chunks

# ---- Generate Embeddings and Upload ----
def embed_and_upload(chunks):
    points = []
    # Add progress bar for processing chunks
    for chunk in tqdm(chunks, desc="Processing chunks", unit="chunk"):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=chunk["embedding"],
            payload={
                "pub_date": chunk["publication_date"],
                "link_to_pdf": chunk["pdf_link"],
                "volume": chunk["volume"],
                "issue": chunk["issue"],
                "author": chunk["author"],
                "title": chunk["title"],
                "page": chunk["page"],
                "id": chunk["chunk_index"],
                "text": chunk["text"],
            }
        )
        points.append(point)

    # Add progress bar for uploading
    # Upload in batches of 100 to show progress
    batch_size = 100
    total_batches = (len(points) + batch_size - 1) // batch_size
    
    with tqdm(total=len(points), desc="Uploading to Qdrant", unit="point") as pbar:
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=batch,
            )
            pbar.update(len(batch))
    
    print(f"\nSuccessfully uploaded {len(points)} points to {COLLECTION_NAME}.")

def delete_all_points():
    print("Deleting all points from collection...")
    qdrant.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(),
    )
    print(f"Deleted all points from {COLLECTION_NAME}.")

def test_connection():
    print("Testing connection...")
    print(qdrant.get_collection(collection_name=COLLECTION_NAME))

# Main execution
print("Starting data upload process...")
chunks = load_chunks_from_json(EMBEDDING_PATH)
#delete_all_points()  # Uncomment if needed
embed_and_upload(chunks)
#test_connection()
print("Process completed!")