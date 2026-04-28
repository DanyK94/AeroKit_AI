import chromadb

client = chromadb.PersistentClient(path="./vector_db")

collection = client.get_or_create_collection(name="documents")

def store_chunks(chunks):
    for i, chunk in enumerate(chunks):
        ids = f"{chunk["document_id"]}_{chunk["page"]+"_"+chunk["chunk_index"]}"

        collection.add(
            uuid = chunk["document_id"],
            ids=ids,
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

def delete_chunks(uuid):
    collection.delete(uuid = uuid)
    return True