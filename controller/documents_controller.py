from fastapi import APIRouter
from dao.documents_dao import get_documents, delete_document, get_documents
from dao.chromadb_dao import delete_chunks, delete_all



router = APIRouter()

@router.get("/document/getall")
def get_allDocuments():
    return get_documents()

@router.post("/document/delete")
def delete_listDocument(list_uuid : list[str]):
    for uuid in list_uuid:
        delete_document(uuid)
        delete_chunks(uuid)
    return


@router.get("/document/deleteAll")
def delete_allDocuments():
    docs = get_documents()
    if docs:
        for doc in docs:
            delete_document(doc["uuid"])
    ccount = delete_all()
    return