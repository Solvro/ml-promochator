import logging

from ipaddress import IPv4Address
from typing import Annotated

from fastapi import Body, FastAPI, Header, HTTPException, Request
from slowapi import Limiter

from src.components.models import InputRecommendationGeneration
from src.graph import recommendation_graph

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def my_get_ipaddr(request: Request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        logger.info(f'Request from: {x_forwarded_for}')
        return request.headers.get('X-Forwarded-For')
    host = request.client.host
    if host:
        logger.info(f'Request from: {host}')
        return host
    return '127.0.0.1'


limiter = Limiter(key_func=my_get_ipaddr)


app = FastAPI(
    title='PromoCHATor',
    version='1.0',
    description='An API for recommending supervisors for thesis',
)

app.state.limiter = limiter


@app.post('/recommend/invoke')
# @limiter.limit("1/minute")
async def invoke(
    request: Request,
    x_forwarded_for: Annotated[IPv4Address, Header()],
    body: dict = Body(..., description='Input JSON'),
):
    try:
        input_data = body.get('input', {})
        if not input_data:
            raise HTTPException(status_code=422, detail="Missing 'input' field in the request body.")

        request_data = InputRecommendationGeneration(**input_data)

        final_state = await recommendation_graph.ainvoke(
            {
                'faculty': request_data.faculty,
                'question': request_data.question,
            }
        )

        return {'output': final_state['recommendation']}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error invoking runnable: {str(e)}')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        proxy_headers=True,
        forwarded_allow_ips='127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16',
    )
