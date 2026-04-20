from unstructured.partition.auto import partition
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from dao.chromadb_dao import store_chunks, get_chunks



file_path = "uploads/test_text.pdf"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def process_document_mock():
    elements = partition(filename=file_path)
    if elements:
        print("ok")
    return None


def process_document(file_path):
    
    #Partioning as semantic parser, semantically splitting text for chunking 
    elements = partition(filename=file_path) 
    
    texts = []

    for el in elements:
        if not el.text:
            continue

        texts.append({"type": el.category , "text": el.text})
    
    chunks = chunk_sections(elements)
    chunks = create_embeddings(chunks)
    store_chunks(chunks)
    return "ok" #TO REDEFINE

    

#Chunking for LLM and retrieval
def chunk_sections(section):
    all_chunks = []
    text_splitter  = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,        
        separators=["\n\n", "\n" , "." , " "]
    )

    for sec in section:
        chunks = text_splitter.split_text(sec["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "title": sec["title"],
                    "chunk_index": i
                    }
                }
            )
    return all_chunks


#Embeddings
def create_embeddings(chunks):

    for chunk in chunks:
        embedding = model.encode(chunk["text"])
        chunk["embedding"] = embedding.tolist()

    return chunks

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
        Title: {meta.get("title")}
        Chunk Index: {meta.get("chunk_index")}
        Content: {doc}
        """
        context_parts.append(part)


    context = "\n\n".join(context_parts)
    prompt = build_prompt(user_query, context)


def build_prompt(user_query, context):
    prompt = f"""
    You are an assistant that answers questions using the provided context.
    Context: {context}
    Question: {user_query}
    Answer clearly and only using the context. If the answer is not present say "I don't know"
    """
    return prompt