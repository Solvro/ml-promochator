from fastapi import FastAPI, HTTPException, Body, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

# from src.graph import recommendation_graph
# from src.components.models import InputRecommendationGeneration

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="PromoCHATor",
    version="1.0",
    description="An API for recommending supervisors for thesis",
)

app.state.limiter = limiter


@app.post("/recommend/invoke")
@limiter.limit("1/5second")
async def invoke(
    request: Request,
    body: dict = Body(..., description="Input JSON"),
):
    print(f"request.client = {request.client}")
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
