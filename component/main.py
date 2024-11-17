from fastapi import FastAPI
import json
app=FastAPI()

Rooms=[
    {"id":1,'name':'Product 1'},
    {"id":2,'name':'Product 2'}
]

@app.get("/")

def home():

    return json.dumps(Rooms)