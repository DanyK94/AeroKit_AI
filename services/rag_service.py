from unstructured.partition.auto import partition
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from dao.chromadb_dao import store_chunks, get_chunks
from clients.openai_client import getResponseFromAI
from models.rag_schemas import QueryResponse, Source, QueryRequest
import hashlib




file_path_mock = "uploads/test_text.pdf"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def process_document_mock():
    process_document(file_path_mock)
    return None


def process_document(file_path, uuid):   

    #doc_id = hashlib.md5(file_path.encode()).hexdigest()[:12]
    #Partioning as semantic parser, semantically splitting text for chunking 
    elements = partition(filename=file_path) 
    
    texts = []

    for el in elements:
        if not el.text:
            continue

        texts.append({"type": el.category , "text": el.text})
    
    chunks = chunk_sections(elements, uuid)
    chunks = create_embeddings(chunks)
    store_chunks(chunks)
    return "ok" #TO REDEFINE

    

#Chunking for LLM and retrieval
def chunk_sections(section, doc_id):
    all_chunks = []
    text_splitter  = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,        
        separators=["\n\n", "\n" , "." , " "]
    )

    for sec in section:
        chunks = text_splitter.split_text(sec.text)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "type" : sec.category,
                    "chunk_index": i,
                    "page" : getattr(sec, 'page_number',0),
                    "document_id": doc_id            
                    }
                }
            )

        #### NOTE: SWITCH TO PyPDF?
    return all_chunks


#Embeddings
def create_embeddings(sources: list[dict]):

    for chunk in sources:
        embedding = model.encode(chunk["text"])
        chunk["embedding"] = embedding.tolist()

    return sources

### RAG RESPONSE
# RETRIEVE CONTEXT
def do_query(user_query):
    query_embedding = model.encode(user_query).tolist()

    results = get_chunks(query_embedding)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []
    for doc, meta in zip(documents,metadatas):
        part = f"""
            Type: {meta.get("type", "Unknown")}
            Page: {meta.get("page", "N/A")}
            Chunk Index: {meta.get("chunk_index")}
            Content: {doc}
        """
        context_parts.append(part)


    context = "\n\n".join(context_parts)
    prompt = build_prompt(user_query, context)
    answer = getResponseFromAI(prompt)
    #queryResponse = QueryResponse(answer=answer, sources=metadatas)

    return {
        "answer": answer,
        "sources": [
            {"title": meta.get("title"), "text": doc[:200]}
            for doc, meta in zip(documents, metadatas)
        ]
    }



def build_prompt(user_query, context):
    prompt = f"""
    You are an assistant that answers questions using the provided context.
    Context: {context}
    Question: {user_query}
    Answer clearly and only using the context. If the answer is not present say "I don't know"
    """
    return prompt