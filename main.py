from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ddtrace.trace import tracer
import uvicorn
import json


templates = Jinja2Templates(directory='templates')

app = FastAPI()

## Definindo o nome do serviço ##
service_name = 'preencher'

## Criando um endpoint/rota ##
@app.get('/home', response_class=HTMLResponse)

## Criando uma função
async def home(request: Request):

    ## Criando um span ##
    with tracer.trace('home', service=service_name, resource='/home') as span:

        ## Setando uma span tag##
        span.set_tag("user", "preencher")

        body = {"user":"preencher"}
        ## Gerando um log ##
        with open('logs/arquivo.json', 'a', encoding='utf-8') as arquivo:
            json.dump(body, arquivo)
            arquivo.write(',\n') 
        return templates.TemplateResponse(request=request, name='index.html')


if __name__ == '__main__':
    uvicorn.run(app='main:app', port=8000,  reload=True)