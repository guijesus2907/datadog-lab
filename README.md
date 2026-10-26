# Datadog-lab 🧪

Projeto estruturado para a **passagem de conhecimento de instrumentações Datadog (APM, Distributed Tracing e Logs)** em aplicações baseadas em Python utilizando FastAPI e Uvicorn.

## 📐 Arquitetura do Laboratório

O ecossistema é composto por 3 componentes que se comunicam de forma distribuída:
1. **`main.py` (Porta 8000):** Servidor frontend/portal que renderiza a página inicial (`index.html`).
2. **`validador_1.py` (Porta 8001):** Primeiro validador. Recebe uma chamada `GET /validation-1`, inicia a árvore de rastreamento (Trace), gera um log local e propaga o contexto via cabeçalhos HTTP para o próximo serviço.
3. **`validador_2.py` (Porta 8002):** Segundo validador. Recebe uma requisição `POST /validation-2`, extrai o contexto do Datadog enviado pelo serviço anterior, continua o mesmo Trace criando um Span filho e gera o log de encerramento.

---

## 📋 Pré-requisitos

Para executar e praticar com este laboratório, você precisará de:
* **Python** (versão 3.8 ou superior recomendada)
* **Datadog Agent** instalado e rodando localmente na sua máquina ([Guia de Instalação do Agent](https://datadoghq.com))
* **Conta Trial da Datadog** (ambiente para visualização das métricas, traces e logs)

### 🚀 Como obter uma Conta Trial gratuitamente?
Não é necessário inserir cartão de crédito. Você pode iniciar um ambiente de testes completo seguindo um dos caminhos oficiais da Datadog:
1. Através do **[Datadog Learning Center](https://learn.datadoghq.com/)**, basta iniciar qualquer laboratório prático para que uma organização sandbox/trial seja provisionada automaticamente para o seu perfil.
2. Diretamente pela página de **[Datadog Free Trial](https://www.datadoghq.com/free-trial/)**, preenchendo o formulário de inscrição para obter acesso gratuito por 14 dias.

---

## 🛠️ Configuração do Ambiente Local

### 1. Preparar o Ambiente Virtual e Instalar Dependências
No seu terminal, prepare o ambiente virtual e instale as bibliotecas necessárias para o laboratório:

```bash
# Criar e ativar o ambiente virtual (Opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # No Linux/Mac
# venv\Scripts\activate  # No Windows

# Instalar as bibliotecas utilizadas no projeto
pip install fastapi uvicorn requests jinja2 ddtrace
```

### 2. Configurar as Variáveis de Ambiente do Datadog
Antes de inicializar as aplicações, configure as variáveis no seu terminal para que o Datadog separe e identifique os serviços corretamente no painel APM:

**No Linux/macOS:**
```bash
export DD_ENV="dev"
export DD_VERSION="1.0.0"
export DD_LOGS_INJECTION="true"
```

**No Windows (Prompt de Comando - CMD):**
```cmd
set DD_ENV=dev
set DD_VERSION=1.0.0
set DD_LOGS_INJECTION=true
```

**No Windows (PowerShell):**
```powershell
$env:DD_ENV="dev"
$env:DD_VERSION="1.0.0"
$env:DD_LOGS_INJECTION="true"
```

---

## 🔬 Executando o Laboratório

Como a aplicação é dividida em microsserviços, você precisará abrir **3 terminais distintos** (ou executar em background) para subir todos os componentes com o inicializador do Datadog (`ddtrace-run`):

### Terminal 1: Portal Main (Porta 8000)
```bash
ddtrace-run python main.py
```

### Terminal 2: Validador 1 (Porta 8001)
```bash
ddtrace-run python validador_1.py
```

### Terminal 3: Validador 2 (Porta 8002)
```bash
ddtrace-run python validador_2.py
```

---

## 🔬 Roteiro de Instrumentação Praticado

Este laboratório demonstra dois conceitos avançados de observabilidade manual do Datadog:

### 1. Injeção e Extração de Contexto Distribuído (Distributed Tracing)
Para interligar microsserviços que usam requisições HTTP normais, o código injeta metadados ocultos nos cabeçalhos ao enviar a mensagem e lê no destino:

* **No Origem (`validador_1.py`):**
  ```python
  headers = {}
  HTTPPropagator.inject(span.context, headers)
  requests.post("http://127.0.0.1:8002/validation-2", json=body, headers=headers)
  ```
* **No Destino (`validador_2.py`):**
  ```python
  contexto_pai = HTTPPropagator.extract(request.headers)
  tracer.context_provider.activate(contexto_pai)
  ```

### 2. Correlação entre Logs e Traces (Trace ID nos Logs)
Ambos os validadores escrevem registros no arquivo físico local `../logs/arquivo.json`. Para garantir que você consiga clicar em um Log e ver o Trace correspondente (ou vice-versa), os IDs gerados pelo contexto ativo do span são embutidos diretamente no dicionário de dados:

```python
body = {
    "service": service_name,
    "dd.trace_id": span.context.trace_id,
    "dd.span_id": span.context.span_id,
    # ... outros metadados
}
```

---

## 📊 O que validar na plataforma Datadog?

Após rodar as aplicações, acesse o seu navegador em `http://127.0.0` e interaja com o frontend para gerar tráfego de rede. Em seguida, acesse o painel da Datadog para auditar os resultados:

* 📉 **APM > Services:** Verifique a criação dinâmica dos catálogos de serviço nomeados como `validador_1` e `validador_2`.
* 🌿 **APM > Traces:** Localize a operação `/validation_primary`. Abra o **Flame Graph** (Gráfico de Chama) e certifique-se de que a requisição do `validador_1` aparece interligada na mesma linha do tempo com a barra filha do recurso `/validation_final` (pertencente ao `validador_2`).
* 🪵 **Log Management:** Caso tenha configurado o Datadog Agent para ler a pasta `../logs/`, verifique se as propriedades estruturadas `dd.trace_id` e `dd.span_id` criaram o vínculo automático de rastreamento de ponta a ponta na aba de correlação de logs do APM.
