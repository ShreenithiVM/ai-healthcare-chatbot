from fastapi import FastAPI
from utils.agent import run_agent

app = FastAPI()

@app.get("/")
def hello():
    return {"name": "abhi", "age" : 21, "dept" : "CSE"}

@app.post("/chat")
def chat(query: str):
    response = run_agent(query)
    return response
