from fastapi import Depends,Request,FastAPI,status,Header

from fastapi import HTTPException

app = FastAPI()


def verify_token(token :str =Header(None)):
    if token != "mysecrettoken": 
        raise HTTPException(status_code=400,
        detail="Unauthorized")
    return {
        "user": "Authorized User"
    }

@app.get("/user")
def home():
    return {
        "data":"Send Sucessfully"
    }

@app.get("/secure-data")
def secure_data(user = Depends(verify_token)):
    return {
        "message":"Secure data acessed",
        "user":user
    }
