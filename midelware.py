from fastapi import FastAPI,Depends,Header,HTTPException,Request,status

from fastapi.responses import JSONResponse
import time

app = FastAPI()

# @app.middleware("http")
# async def my_middleware(request:Request,call_next):
#     print("Request Received")
#     response = await call_next(request)

#     print("request Send")
#     return response

# @app.get("/")
# def home():
#     return {"message": "Hello World"}

@app.middleware("http")
async def midelwares(request:Request,call_next):
    start_time = time.time()
    print("-=-=-=-- start time -=-=--=-=-",start_time)

    response = await call_next(request)

    process_time = time.time() - start_time
    print("-=-=-=- process time-=-=-=-=",process_time)

    print(f"Path:{request.url.path} | Process time {process_time}")
    return response

@app.get("/")
def home():
    return {"message": "Hello World"}