from fastapi import FastAPI
from ddtrace.propagation.http import HTTPPropagator
from ddtrace.trace import tracer
import requests
import json
import uvicorn

app = FastAPI()

## Definindo o nome do serviço ##
service_name = "validador_1"


## Criando um endpoint/rota ##
@app.get("/validation-1")


## Criando uma função
async def validation_1():

## Criando um span ##
    with tracer.trace('home', service=service_name, resource='/validation_primary') as span:

        ## Setando uma span tag##
        span.set_tag("user", "preencher")

         ## Criando estrutura do log
        body = {"service":service_name, 
                "message":"Etapa 1 finalizada",
                "env": "dev",
                "version": 1,
                "dd.trace_id":span.context.trace_id,
                "dd.span_id":span.context.span_id,
                "user":"preencher", 
                }
        
        ## Gerando um log ##
        with open('../logs/arquivo.json', 'a', encoding='utf-8') as arquivo:
            json.dump(body, arquivo)
            arquivo.write(',\n')

        headers = {}
        HTTPPropagator.inject(span.context, headers)

        requests.post("http://127.0.0.1:8002/validation-2", json=body, headers=headers)

if __name__ == '__main__':
    uvicorn.run(app='validador_1:app', port=8001,  reload=True)

