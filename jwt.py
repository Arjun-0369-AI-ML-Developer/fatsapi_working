from fastapi import FastAPI,HTTPException,Depends,Header
from jose import jwt
from datetime import datetime,timedelta,timezone

app = FastAPI()

secret_key = "mysecret"

Algorithm = "HS256"


#Create Token
def create_token(data:dict):
    to_encode = data.copy()
    print("-=-=--==-=-=- to_encode -=-=--=-=-=",to_encode)
    print("-=-=--==-=-=- data -=-=--=-=-=",data)
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    print("-=-=--==-=-=- expire -=-=--=-=-=",expire)
    to_encode.update({"exp":expire})
    token = jwt.encode(to_encode,secret_key,algorithm=Algorithm)
    print("-=-=-=-=-=- token -=-=-=-=-=-=-",token)
    return token


@app.post("/login")
def login(username:str,password:str):
    if username != "admin" and password != "1234":
        raise HTTPException(status_code=401,detail="Invalid username and. password")
    token = create_token({"sub":username})
    return {
        "access_token":token
    }

def verify(token:str = Header(None)):
    try:
        payload = jwt.decode(token,secret_key,algorithms =[Algorithm])
        return payload
    except:
        raise HTTPException(status_code=401,detail = "Invalid or expired Token")

@app.get("/secure")
def secure_data(user = Depends(verify)):
    return {
        "messages":"Secure Data Accessed",
        "user":user
    }