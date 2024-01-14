import json
from fastapi import FastAPI
from messages_type import Messages
from model import model_query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.post("/query")
async def root(messages: Messages): 
    print("query invoked")
    print(messages)   
    res = model_query(messages)
    return {"message": f"{res}"}