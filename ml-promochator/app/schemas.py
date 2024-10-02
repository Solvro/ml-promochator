from pydantic import BaseModel

class RecommendResponse(BaseModel):
    text: str

class RecommendRequest(BaseModel):
    text: str