from fastapi import FastAPI


app = FastAPI()



@app.get("/home")
def home():
    return {
        "message":"Hello Mini"
    }

@app.get("/add")
def home(a:int,b:int):
    return {
        "result":a+b
    }