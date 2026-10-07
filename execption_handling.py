from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()

class UserNotFoundException(Exception):
    def __init__(self,name:str):
        self.name = name


#global error handler
@app.exception_handler(UserNotFoundException)
def user_not_found_handle(request:Request,Exception:UserNotFoundException):
    return JSONResponse(status_code=404,content={
        "status":"error",
        "message":f"User {Exception.name} not found"
    })

@app.get("/user")
def get_user():
    return {"message":"Succesfully"}

@app.get("/users/{user_id}")
def get_user(user_id:int):
    if user_id !=1:
        raise HTTPException(status_code=400,
        detail= "user not found")
    return {"message":"Succesfully"}

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=0-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=0-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=0-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@app.get("/testing/{name}")
def get_user(name:str):
    if name != "mohit":
        raise UserNotFoundException(name)
    return {"name":name}