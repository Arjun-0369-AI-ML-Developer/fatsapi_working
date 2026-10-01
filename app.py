from fastapi import FastAPI
from pydantic import BaseModel # If you want to create validation then use


app = FastAPI()

class testing(BaseModel):
    name:str
    age:int
    work:str

@app.get("/")
def home():
    return {"message":"Hello without uvicorn"}
    
@app.get("/about")
def users():
    return {"users":["Mohit","Rohit"]}

#Dynamic Route
@app.get("/user/{user_id}")
def get_user(user_id):
    return {"user_id":user_id}

#Dynamic integer type Route
@app.get("/organisation/{organisation_id}")
def orgenization(organisation_id : int):
    return {"organisation_id":organisation_id }

#Optional Route
@app.get("/arjun")
def abc(name):
    return {'name':name}

@app.get("/pawan")
def abc(name:str =None):
    return {'name':name}

@app.get("/product")
def product(limit :int =10):
    return {"limit":limit}

@app.get("/items")
def get_user(name :str =None,price :int =10):
    return {"name":name,"price":price}

#create post request
@app.post("/create_user")
def new_created(name :str,age:int):
    return {"name":name,"age":age}

@app.post("/register_user")
def new_created(user:dict):
    return {"message":"new user register","data":user}

#create post with validation data
@app.post("/new_regster_user")
def created(user :testing):
    return {"message":"new user register","data":user}
