from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ddtrace.trace import tracer
import uvicorn
import json

templates = Jinja2Templates(directory='templates')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Definindo o nome do serviço ##
service_name = "preencher"

## Criando um endpoint/rota ##
@app.get('/home', response_class=HTMLResponse)

## Criando uma função
async def home(request: Request):
 
        return templates.TemplateResponse(request=request, name='index.html')

if __name__ == '__main__':
    uvicorn.run(app='main:app', port=8000,  reload=True)