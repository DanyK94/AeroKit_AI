import os
import logging
from requests import Response
from models.rag_schemas import QueryRequest
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, File, UploadFile
from services.rag_service import process_document, do_query
from dao.documents_dao import add_document, update_status



router = APIRouter()

#Process Should Be:
#1.Upload
#2.Parsing
#3.Chunking
#4.Embedding
#5.Storage

#Upload da File
UPLOAD_DIR = "uploads"

logger = logging.getLogger(__name__)

@router.post("/documents/upload/")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
   
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    uuid = add_document(file.filename)

    logger.info(f"Processing {file_path} UUID: {uuid}")
    try:
        process_document(file_path, uuid)
    except Exception as e:
        update_status(uuid, "Error")
        raise HTTPException(status_code=500, detail=str(e))
    
    update_status(uuid, "File Processed")

    return {"status": "success"}

@router.post("/chat/query")
def chat_query(request: QueryRequest):
    return do_query(request.question, request.document_id)

@router.get("/documents")
def get_list_documents():
    return os.listdir(UPLOAD_DIR)

@router.delete("/documents/{id}")
def delete_document(id: str):
    file_path = os.path.join(UPLOAD_DIR, id)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"status": "success", "deleted": id}
    else:
        raise HTTPException(status_code=404, detail="Document not found")
    
            

    