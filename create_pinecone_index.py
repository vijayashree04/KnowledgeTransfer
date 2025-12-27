import os
from pinecone import Pinecone, ServerlessSpec

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME", "kt-docs")
cloud = os.getenv("PINECONE_CLOUD", "aws")
region = os.getenv("PINECONE_REGION", "us-east-1")

if not api_key:
    raise ValueError("PINECONE_API_KEY is not set")

pc = Pinecone(api_key=api_key)

# Use 768 for Gemini text-embedding-004
dimension = 768

existing = [idx["name"] for idx in pc.list_indexes()]

if index_name in existing:
    print(f"Index '{index_name}' already exists.")
else:
    print(f"Creating index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(cloud=cloud, region=region),
    )
    print("Index created.")

print("Done.")