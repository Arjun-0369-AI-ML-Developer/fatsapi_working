from jose import jwt,JWTError
from fastapi import FastAPI,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext

app = FastAPI()
secret_key = "mysecret"
Algorithm = "HS256"

Access_token_expire_minutes = 30
pwd_context = CryptContext(schemes=["bcrypt"])

oauuth2_schema = OAuth2PasswordBearer(tokenUrl="login")

fake_user_db = {
    "admin":{"username":"admin",
    "hashed_password":pwd_context.hash("1234")}
}

print("-=-=-=- fake_user_db -=-=-=-==-=-=",fake_user_db)

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plan_password,hased_password):
    return pwd_context.verify(plan_password,hased_password)

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode,secret_key,algorithm=Algorithm)
    return token



@app.post("/login")
def login(from_data:OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db.get(from_data.username)
    print("-=-=-=-=-= user -=-=-=-=-",user)
    if not user or not verify_password(from_data.password,user["hashed_password"]):
        raise HTTPException(status_code=400,detail="Invalid username or password")

    access_token = create_token({"sub":from_data.username})
    print("-=-=-=-=-= access_token -=-=-=-=-",access_token)

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }



def verify_token(token:str = Depends(oauuth2_schema)):
    try:
        payload = jwt.decode(token,secret_key,algorithms=[Algorithm])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401,details = "Invalid token")
        return username
    except jwt.error:
        raise HTTPException(status_code=401,detail="Invalid Token")



@app.get("/protected")
def protected_route(username:str = Depends(verify_token)):
    return {
        "message": "Hello you have access to this protected route!",
        "user":username
    }