import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(name="documents")

def store_chunks(chunks):
    for i, chunks in enumerate(chunks):
        collection.add(
            ids=[f"id_{i}"],
            documents=[chunks["text"]],
            embeddings=[chunks["embedding"]],
            metadatas=[chunks["metadata"]]        
        )

def get_chunks(query_embedding):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    return results