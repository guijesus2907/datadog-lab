O laboratório abordará APM, Distributed Tracing e Logs no backend, e, na parte do frontend, somente RUM e geração de logs pelo Browser Logs, sem integração entre RUM e APM.

Você pode substituir os trechos correspondentes do README pelas versões abaixo.

Escrita

## 📐 Arquitetura do Laboratório

O ecossistema é composto por três serviços de backend e uma interface web instrumentada com os SDKs do Datadog:

1. **`main.py`****(Porta 8000):** Servidor frontend/portal que renderiza a página inicial (`index.html`).
2. **`validador_1.py`****(Porta 8001):** Primeiro validador. Recebe uma chamada `GET /validation-1`, inicia o rastreamento, gera um log local e propaga o contexto para o próximo serviço.
3. **`validador_2.py`****(Porta 8002):** Segundo validador. Recebe uma requisição `POST /validation-2`, extrai o contexto do Datadog, continua o Trace e gera o log de encerramento.
4. **`index.html`****(Frontend):** Interface web instrumentada com os SDKs do Datadog RUM e Browser Logs, permitindo monitorar interações dos usuários, sessões, recursos do navegador e gerar logs a partir de eventos como cliques em botões.

---

## 🔬 Roteiro de Instrumentação Praticado

Este laboratório aborda os seguintes conceitos de observabilidade com o Datadog.

### 1\. Injeção e extração de contexto distribuído (Distributed Tracing)

Demonstra como propagar o contexto de rastreamento entre os serviços FastAPI por meio de cabeçalhos HTTP, permitindo visualizar as operações no APM.

### 2\. Correlação entre Logs e Traces no backend

Demonstra como registrar identificadores de Trace e Span nos logs dos validadores, permitindo investigar as operações do backend na plataforma Datadog.

### 3\. Real User Monitoring (RUM)

O **Real User Monitoring (RUM)** será utilizado para demonstrar o monitoramento da experiência dos usuários diretamente no navegador.

A instrumentação será realizada no arquivo `index.html` por meio do SDK JavaScript do Datadog Browser RUM.

Os principais recursos abordados serão:

- **Monitoramento de sessões:** coleta de informações sobre as sessões dos usuários.
- **Interações do usuário:** identificação de ações realizadas na interface, como cliques em botões.
- **Monitoramento de recursos:** acompanhamento dos recursos e das requisições carregados pelo navegador.
- **Long Tasks:** identificação de tarefas longas que podem afetar a responsividade da página.
- **Session Replay:** reprodução de sessões elegíveis para auxiliar na análise da experiência de navegação.

A configuração será realizada por meio do método `DD_RUM.init()`, utilizando o Application ID, o Client Token e os parâmetros de monitoramento da aplicação.

### 4\. Geração de logs no frontend (Browser Logs)

Além do RUM, será abordada a geração e o envio de logs diretamente do navegador utilizando o SDK Browser Logs do Datadog.

O método `DD_LOGS.init()` será responsável por inicializar o SDK, permitindo enviar mensagens e encaminhar erros do frontend para o Datadog.

Exemplo de geração de log ao clicar em um botão:

javascript

```
function logar() {
    window.DD_LOGS &&
        window.DD_LOGS.logger.info('Botão clicado', {
            name: 'usuario-exemplo',
            id: 1
        });
}

const botao = document.getElementById('botao');
botao.addEventListener('click', logar);
```

Esse exemplo demonstra como registrar uma mensagem informativa acompanhada de atributos adicionais durante uma interação do usuário.

**Importante:** o RUM e o Browser Logs serão explorados como instrumentações do frontend, com objetivos complementares: o RUM para monitoramento da experiência do usuário e o Browser Logs para geração e envio de mensagens e erros do navegador. Não será abordada a integração entre RUM e APM nem a correlação de traces do frontend com o backend.

---

## 📊 O que validar na plataforma Datadog?

Após iniciar as aplicações e interagir com o frontend, acesse a plataforma Datadog para verificar os resultados.

- **APM \> Services:** verificar os serviços `validador_1` e `validador_2`.
- **APM \> Traces:** analisar o encadeamento dos Spans gerados pelos validadores.
- **Log Management:** verificar os logs gerados pelo backend, conforme a configuração de ingestão do Agent.
- **Digital Experience Monitoring \> RUM \> Applications:** verificar as sessões, ações, recursos e demais dados coletados pelo RUM.
- **Log Management — Browser Logs:** verificar as mensagens enviadas pelo SDK Browser Logs e os erros encaminhados pelo navegador.

### ✅ Resultado esperado

Ao concluir o laboratório, será possível compreender e praticar:

- **APM e Distributed Tracing:** monitoramento das operações e comunicação entre os serviços backend.
- **Logs do backend:** geração e análise de registros das aplicações Python.
- **RUM:** monitoramento das sessões e interações dos usuários no navegador.
- **Browser Logs:** geração e envio de logs e erros do frontend para a plataforma Datadog.

O objetivo é demonstrar os recursos de observabilidade do Datadog no backend e no frontend, mantendo o RUM e a geração de logs do navegador independentes da instrumentação de APM.
