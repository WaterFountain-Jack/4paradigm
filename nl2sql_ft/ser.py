from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List

class TrainData(BaseModel):
    query: str
    sql: str
    order: bool

class TrainDataRequest(BaseModel):
    data: List[TrainData]

class SuccessResponse(BaseModel):
    success: bool

app = FastAPI()

@app.post("/train_data")
async def tackle_train_data(request: TrainDataRequest):
    print("Received request data:", request.dict())  # 打印接收到的数据
    return SuccessResponse(success=True)

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # 打印异常信息
        print(f"Error occurred: {e}")
        return JSONResponse(
            status_code=422,
            content={"detail": str(e)},
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ser:app", host="0.0.0.0", port=18089)
