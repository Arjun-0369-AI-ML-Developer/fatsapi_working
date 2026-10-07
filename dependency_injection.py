from fastapi.responses import JSONResponse
from fastapi import FastAPI,status,HTTPException,Request
from fastapi import Depends

app = FastAPI()

def common_logic():
    return { "message": "Common Logic Executed"}
@app.get("/user")
def home():
    return {"message":"Data Successfully"}

@app.get("/users")
def home(data = Depends(common_logic)):
    return data