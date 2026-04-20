from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    document_id: str = None

class Source(BaseModel):
    text: str
    metadata: dict

class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]