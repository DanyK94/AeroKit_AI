import chromadb

client = chromadb.PersistentClient(path="./vector_db")

collection = client.get_or_create_collection(name="documents")

def store_chunks(chunks):
    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"id_{i}"],
            documents=[chunk["text"]],
            embeddings=[chunk["embedding"]],
            metadatas=[chunk["metadata"]]        
        )

def get_chunks(query_embedding):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    return results