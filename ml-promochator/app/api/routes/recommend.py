from fastapi import APIRouter, HTTPException

from app.schemas import RecommendResponse, RecommendRequest
from app.services.rag.retrieval import recommend_supervisor
from app.api.deps import SessionDep

router = APIRouter()

@router.post("", response_model=RecommendResponse)
async def recommend(
    *, session: SessionDep, recommend_in: RecommendRequest
) ->RecommendResponse:
    if recommend_in is None:
        raise HTTPException(status_code=422, detail="No text provided.")
    
    answer = RecommendResponse()
    answer.text = recommend_supervisor(recommend_in.text, session)
    return answer