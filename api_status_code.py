from fastapi import FastAPI, status,HTTPException

app = FastAPI()

@app.post("/create_user",status_code= status.HTTP_201_CREATED)
def create_user():
    return {"message":"User Created"}

@app.get("/user")
def user():
    return {
        "status":"Sucess",
        "message":"User Fetched",
        "data":{
            "name":"Mohit",
            "age":24
        }
    }



@app.get("/user/{user_id}")
def get_user(user_id:int):
    if user_id !=1:
        raise HTTPException(status_code=400,detail="User Not Found")
    return {
        # "id":1,
        "name":"Surjeet",
        "Age":29
    }