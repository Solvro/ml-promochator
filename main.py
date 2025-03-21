import logging
import os
import uuid
from ipaddress import IPv4Address
from typing import Annotated

from fastapi import Body, FastAPI, Header, HTTPException, Request, Response
from slowapi import Limiter
from starlette.middleware.sessions import SessionMiddleware

from src.components.graph.utils import clear_memory, run_graph
from src.components.models import InputRecommendationGeneration
from src.graph import create_recommendation_workflow

from src.database.schemas.feedback import Feedback, FeedbackCreate
from src.database.db import SessionDep


# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

graph = create_recommendation_workflow()


def get_ip_address(request: Request):
    """
    Extracts the client's IP address from the request headers.

    This function checks for the `X-Forwarded-For` header, which is used when requests pass through a proxy.
    If the header is not present, it falls back to using the `host` attribute of the request client.

    Parameters:
        request (Request): The incoming FastAPI request object.

    Returns:
        str (str): The client's IP address.
    """
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        logger.info(f'Request from: {x_forwarded_for}')
        return request.headers.get('X-Forwarded-For')
    host = request.client.host
    if host:
        logger.info(f'Request from: {host}')
        return host
    return "127.0.0.1" # Default fallback IP


limiter = Limiter(key_func=get_ip_address)

app = FastAPI(
    title='PromoCHATor',
    version='1.0',
    description='An API for recommending supervisors for thesis',
)

# Add Session Middleware with a secret key. This middleware manages a session cookie.
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('SESSION_SECRET_KEY'),  # any string can be key
    max_age=3600,  # in seconds
)

app.state.limiter = limiter

@app.post("/recommend/invoke")
async def invoke(
    request: Request,
    x_forwarded_for: Annotated[IPv4Address, Header()] = None,
    body: dict = Body(..., description='Input JSON'),
):
    """
    Endpoint to invoke the recommendation engine.

    This endpoint takes in a user's question about finding a suitable supervisor for their thesis 
    and processes the request using a recommendation system.

    Parameters:
        request (Request): The FastAPI request object.
        x_forwarded_for (IPv4Address): The client's IP address extracted from headers.
        body (dict): The request payload containing the input data.

    Returns:
        RecommendationState: Final state containing the model's response.

    Raises:
        HTTPException: If the input data is missing or if an internal server error occurs.
    """
    try:
        # Retrieve or create the thread_id for this session
        session = request.session
        if 'thread_id' not in session:
            session['thread_id'] = str(uuid.uuid4())

        input_data = body.get('input', {})
        if not input_data:
            raise HTTPException(status_code=422, detail="Missing 'input' field in the request body.")

        request_data = InputRecommendationGeneration(**input_data)

        result = await run_graph(graph, request_data, session['thread_id'])

        return {'output': result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error invoking runnable: {str(e)}') from e


# Endpoint to clear session cookie and memory for it
@app.post('/recommend/clear-session')
async def clear_session(response: Response, request: Request):
    detail = ''

    session = request.session
    if 'thread_id' in session:
        await clear_memory(graph, session['thread_id'])
        detail += f'Memory cleared for {session["thread_id"]}.'

    response.delete_cookie('session')
    detail += ' Session cookie cleared.'

    return {'detail': detail}


@app.post("/recommend/feedback", status_code=201)
async def feedback(feedback: FeedbackCreate, session: SessionDep):
    """
    Endpoint to submit feedback on a recommendation.

    This endpoint allows users to submit feedback regarding the adequacy of a supervisor recommendation.
    The feedback is stored in the database.

    Parameters:
        feedback (FeedbackCreate): The feedback data submitted by the user.
        session (SessionDep): The database session dependency for database operations.
    """
    feedback_db = Feedback(**feedback.model_dump())
    session.add(feedback_db)
    session.commit()


# if __name__ == '__main__':
#     import uvicorn

#     uvicorn.run(
#         'main:app',
#         host='0.0.0.0',
#         port=8000,
#         proxy_headers=True,
#         forwarded_allow_ips='127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16',
#     )