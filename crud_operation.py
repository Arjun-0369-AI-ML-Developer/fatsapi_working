from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todo = []

class testing(BaseModel):
    id:int
    email:str
    name:str
    age:int

@app.post("/new_register")
def created_user(todos : testing):
    todo.append(todos)
    print(todo)
    return {"msg":"data created","data":todo}

@app.get("/todo")
def home():
    return {"data":todo}

@app.get("/todo/{todo_id}")
def home1(todo_id :int):
    for abc in todo:
        # print("-=-=--=-= todo -=-=-=-",todo)
        print("-=-=--= abc -=-=-=--=-",abc)
        # print("-=-=--= abc -=-=-=--=-",abc.id)
        if abc.id == todo_id:
            print("-=-=--=-=- abc -=-=--=-",abc)
            return abc
    return {"error":"To do not found"}


@app.put("/todo/{todo_id}")
def update_todo(todo_id:int,updated_todo:testing):
    for index,item in enumerate(todo):
        print("-=-=-=-= index -=-=-=",index)
        print("-=-=-=-= item -=-=-=",item)
        if item.id == todo_id:
            todo[index]= updated_todo
            return {"message": "Data updated","data":todo[index]}
    return {"error":"Todo not found"}

