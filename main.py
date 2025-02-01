from fastapi import FastAPI, HTTPException, Body, Request, Header
from typing import Annotated
from slowapi import Limiter
from ipaddress import IPv4Address
from src.graph import recommendation_graph
from src.components.models import InputRecommendationGeneration
from src.database.schemas.feedback import Feedback, FeedbackCreate
from src.database.db import SessionDep
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def my_get_ipaddr(request: Request):
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        logger.info(f"X-Forwarded-For header: ${x_forwarded_for}")
        logger.info(f"Request from based on X-Forwarded-For header: {x_forwarded_for}")
        return request.headers.get("X-Forwarded-For")
    host = request.client.host
    if host:
        logger.info(f"Request from based on Host header: {host}")
        return host
    return "127.0.0.1"


limiter = Limiter(key_func=my_get_ipaddr)


app = FastAPI(
    title="PromoCHATor",
    version="1.0",
    description="An API for recommending supervisors for thesis",
)

app.state.limiter = limiter


@app.post("/recommend/invoke")
# @limiter.limit("1/minute")
async def invoke(
    request: Request,
    x_forwarded_for: Annotated[IPv4Address, Header()],
    body: dict = Body(..., description="Input JSON"),
):
    try:
        input_data = body.get("input", {})
        if not input_data:
            raise HTTPException(
                status_code=422, detail="Missing 'input' field in the request body."
            )

        request_data = InputRecommendationGeneration(**input_data)

        final_state = await recommendation_graph.ainvoke(
            {
                "faculty": request_data.faculty,
                "question": request_data.question,
            }
        )

        return {"output": final_state["recommendation"]}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error invoking runnable: {str(e)}"
        )


@app.post("/recommend/feedback", status_code=201)
async def feedback(feedback: FeedbackCreate, session: SessionDep):
    feedback_db = Feedback(**feedback.model_dump())
    session.add(feedback_db)
    session.commit()
