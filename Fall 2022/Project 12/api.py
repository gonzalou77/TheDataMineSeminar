from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from .database import queries, database_path
from .import schemas

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get("/")
async def root():
    return JSONResponse({"message": "Hello World"})


@app.get("/titles/{title_id}", response_model = schemas.Title)
#@app.get("/titles/{title_id}")
async def get_title(title_id: str):
    conn = sqlite3.connect(database_path)
    with conn as c:
        results = queries.get_title(c, title_id=title_id)
    new_results = []
    for tup in results:
        new_results.append(list(tup))
        
    new_results = {key: new_results[0][i] for i, key in enumerate(schemas.Title.__fields__.keys())}
    return schemas.Title(**new_results)

    #new_results = []
    #for tup in results:
    #    new_results.append(list(tup))
    
    #for l in new_results:
    #    l[len(l)-1] = list(l[len(l)-1].split(','))
    
    #new_results = {key: new_results[0][i] for i, key in enumerate(schemas.Title.__fields__.keys())}
    #return schemas.Title(**new_results)

#@app.post("/titles/{title_id}")
#async def make_title(title: Title):
    #return Title