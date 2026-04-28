from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime
from dao.chromadb_dao import delete_chunks
import os, logging

logger = logging.getLogger(__name__)



client = MongoClient("mongodb://localhost:32768/")
db = client["aerokit_mbd"]
collection = db["documents"]

UPLOAD_DIR = "uploads"

def add_document(doc_title):
    doc_uuid = str(uuid4())
    time = datetime.now()
    document = {
        "uuid": doc_uuid,
        "title": doc_title,
        "time": time,
        "status": "To be processed"
    }
    collection.insert_one(document)
    return doc_uuid

def get_documents():
    documents = collection.find()
    list = []
    for document in documents:
        document.pop("_id", None)
        list.append(document)
    return list

def get_documentById(uuid):
    document = collection.find_one({"uuid": uuid})
    return document

def update_status(uuid, status):
    collection.update_one({"uuid": uuid}, {"$set": {"status": status}})
    return True


def delete_document(uuid):
    doc = get_documentById(uuid)
    if not doc:
        return False
    try:
        delete_file(os.path.join(UPLOAD_DIR, doc["title"])) #FILE
        collection.delete_one({"uuid": uuid})   #DB
        delete_chunks(uuid) #Chunks
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        return False
    return True


async def save_file(file):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(file.file.read())
    return file_path

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False



