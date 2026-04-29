import chromadb
import logging

logger = logging.getLogger(__name__)


client = chromadb.PersistentClient(path="./vector_db")

collection = client.get_or_create_collection(name="documents")

def store_chunks(chunks):
    logger.info("Storing chunks")
    stored_chunks = 0
    
    for chunk in chunks:

        meta = chunk["metadata"]
        ids = f"{meta['document_id']}___{stored_chunks}"
        logger.info(f"Storing chunk IDS:{ids}")
        
        try:
            collection.add(
                ids=ids,
                documents=[chunk["text"]],
                embeddings=[chunk["embedding"]],
                metadatas=[chunk["metadata"]]        
            )
            stored_chunks += 1
        except Exception as e:
            logger.error(f"Error storing chunk {e}")
            return
    logger.info("Chunks stored")
    return stored_chunks


def get_chunks(query_embedding, uuid, n_results):
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results = n_results
    )
    return results

def delete_chunks(uuid):
    count_before= collection.count()
    collection.delete(where={"document_id": uuid})
    count_after = collection.count()
    logger.info(f"Deleted {count_before - count_after} chunks")
    return count_after < count_before

def delete_all():
    count_before= collection.count()
    collection.delete_all()
    count_after = collection.count()
    logger.info(f"Deleted {count_before - count_after} chunks")
    return count_after < count_before