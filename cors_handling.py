from fastapi import FastAPI,Depends,Header,HTTPException,status,File,Request,UploadFile

from fastapi.responses import JSONResponse
from jose import jwt
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
def home():
    return {
        "message":"Working Correct"
    }