from fastapi import UploadFile,HTTPException,FastAPI,File
import os
import shutil
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/files",StaticFiles(directory=UPLOAD_DIR),name = "file")

@app.post("/upload")
def upload_file(file:UploadFile = File(...)):
    filename = file.filename
    print("-=-=-=--=-=----=-=- filename -=-=--=-=-=-",filename)
    file_path = os.path.join(UPLOAD_DIR,filename)
    print("-=-=-=--=-=----=-=- filepath-=-=--=-=-=-",file_path)

    if not filename:
        raise HTTPException(status_code=401,details = "file not selected")
    
    with open(file_path,"wb") as f:
        shutil.copyfileobj(file.file,f)

        return {
            "message":"File Uploaded Sucessfully",
            "filename":filename,
            "file_url":f"http://127.0.0.1:8000/file/{filename}"
        }


@app.get("/file/{filename}")
def get_file(filename:str):
    file_path = os.path.join(UPLOAD_DIR,filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=401,detail="File Not found")

    # return {
    #     "file_url":f"http://127.0.0.1:8000/file/{filename}"
    # }
    return FileResponse(file_path)


@app.get("/")
def home():
    return {
        "message":"File Upload api Running"
    }

