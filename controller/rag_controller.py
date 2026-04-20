import os
from requests import Response
from fastapi import routerAPI, HTTPException, File, UploadFile
from services.rag_service import process_document, do_query


router = routerAPI()

#Process Should Be:
#1.Upload
#2.Parsing
#3.Chunking
#4.Embedding
#5.Storage

#Upload da File
UPLOAD_DIR = "uploads"

@router.post("/documents/upload/")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
   
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    if process_document(file_path):
        return Response.ok
    else:
        return Response.error


@router.post("/chat/query")
def chat_query(query: str):
    return do_query(query)

@router.get("/documents")
def get_list_documents():
    return os.listdir(UPLOAD_DIR)

@router.delete("/documents/{id}")
def delete_document(id: str):
    file_path = os.path.join(UPLOAD_DIR, id)
    if os.path.exists(file_path):
        os.remove(file_path)
        return Response.ok
    else:
        return Response.error
    
            

    