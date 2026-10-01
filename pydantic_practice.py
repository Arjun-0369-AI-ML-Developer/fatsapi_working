from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class testing(BaseModel):
    name: str
    age: int
    work: str

class id(BaseModel): #Nested Model
    id:int
    email:str
    details:testing
    

@app.post("/created_user")
def created(user :testing):
    return {"message":"your msg. created","data":user}

#Nested Model

@app.post("/new_register")
def create_user(user :id):
    return {'message':"data created",'data':user}