from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Service 1 is running"}

@app.get("/hello")
def hello():

    return {"message": "Hello from Service 1"}
