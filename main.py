import json
from fastapi import FastAPI, Response, status
from messages_type import Messages
from model import model_query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.post("/query")
async def root(messages: Messages, response: Response): 
    print("query invoked")
    print(messages)
    
    # Should implement your own API key validation logic here
    if(messages.api_key != "some_api_key_here_logic_etc"):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid API Key"}
    
    res = model_query(messages)
    return {"message": f"{res}"}