from fastapi import FastAPI, HTTPException, Body, Request, Header
from typing import Annotated
from slowapi import Limiter
from slowapi.util import get_ipaddr
from ipaddress import IPv4Address


# from src.graph import recommendation_graph
# from src.components.models import InputRecommendationGeneration


limiter = Limiter(key_func=get_ipaddr)


app = FastAPI(
    title="PromoCHATor",
    version="1.0",
    description="An API for recommending supervisors for thesis",
)

app.state.limiter = limiter


@app.post("/recommend/invoke")
@limiter.limit("1/10second")
async def invoke(
    request: Request,
    x_forwarded_for: Annotated[IPv4Address, Header()],
    body: dict = Body(..., description="Input JSON"),
):
    print(f"Request from: {x_forwarded_for}")
    try:
        input_data = body.get("input", {})
        if not input_data:
            raise HTTPException(
                status_code=422, detail="Missing 'input' field in the request body."
            )

        # request_data = InputRecommendationGeneration(**input_data)

        # final_state = await recommendation_graph.ainvoke(
        #     {
        #         "faculty": request_data.faculty,
        #         "question": request_data.question,
        #     }
        # )

        # return {"output": final_state["recommendation"]}
        return {"output": "request successfull"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error invoking runnable: {str(e)}"
        )
