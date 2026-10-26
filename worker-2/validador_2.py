from fastapi import FastAPI, Request
from ddtrace.trace import tracer
from ddtrace.propagation.http import HTTPPropagator
import json
import uvicorn

app = FastAPI()

## Definindo o nome do serviço ##
service_name = "validador_2"

@app.post("/validation-2")
async def validation_2(request: Request):

        contexto_pai = HTTPPropagator.extract(request.headers)

        tracer.context_provider.activate(contexto_pai)

        ## Criando um span ##
        with tracer.trace('home', service=service_name, resource='/vaidation_final') as span:

            ## Setando uma span tag##
            span.set_tag("user", "Lucas")

            ## Criando estrutura do log
            body = {"service":service_name,
                    "message":"Etapa 2 finalizada", 
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


if __name__ == '__main__':
    uvicorn.run(app='validador_2:app', port=8002,  reload=True)


