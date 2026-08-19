from fastapi import FastAPI
from fastapi.responses import FileResponse

app=FastAPI()

@app.get("/")
def home():
    return FileResponse("app/index.html")

@app.get("/api/hello")
def get_hello():
    return {"message":"FastAPI says Hi"}
