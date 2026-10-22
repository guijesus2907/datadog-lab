# Datadog-lab 🧪

Projeto estruturado para a **passagem de conhecimento de instrumentações Datadog** em aplicações baseadas em Python.

## 📋 Pré-requisitos

Para executar e praticar com este laboratório, você precisará de:
* **Python** (versão 3.8 ou superior recomendada)
* **Conta Trial da Datadog** (ambiente para visualização das métricas, traces e logs)

### 🚀 Como obter uma Conta Trial gratuitamente?
Não é necessário inserir cartão de crédito. Você pode iniciar um ambiente de testes completo seguindo um dos caminhos oficiais da Datadog:
1. Através do **[Datadog Learning Center](https://learn.datadoghq.com/)**, basta iniciar qualquer laboratório prático para que uma organização sandbox/trial seja provisionada automaticamente para o seu perfil.
2. Diretamente pela página de **[Datadog Free Trial](https://www.datadoghq.com/free-trial/)**, preenchendo o formulário de inscrição para obter acesso gratuito por 14 dias.

---

## 🛠️ Configuração do Ambiente Local

### 1. Clonar o Repositório e Configurar o Python
No seu terminal, prepare o ambiente virtual e instale as dependências básicas:

```bash
# Clonar o repositório
git clone <url-do-seu-repositorio>
cd Datadog-lab


# Instalar dependências iniciais (se houver um requirements.txt)
pip install -r requirements.txt
```

## 🔬 Roteiro de Instrumentação (Passo a Passo)

### 🧬 Tipo 1: Instrumentação Automática (Sem Alterar Código)
A maneira mais rápida de instrumentar uma aplicação Python é utilizando o pacote `ddtrace-run`, que injeta os patches em bibliotecas populares (como Flask, FastAPI, Django, requests) em tempo de execução.

```bash
# Instalar a ferramenta de rastreamento da Datadog
pip install ddtrace

# Executar seu script através do tracer do Datadog
ddtrace-run python seu_script.py
```

### 🧑‍💻 Tipo 2: Instrumentação Manual (Customizada)
Para criar spans específicos, monitorar funções internas ou adicionar tags customizadas ao contexto do Datadog APM:

```python
from ddtrace import tracer

# Criando um span manual para um bloco de código específico
with tracer.trace("operacao.calculo", resource="calcular_metricas") as span:
    # Adicionando metadados úteis para o troubleshooting
    span.set_tag("laboratorio.modulo", "modulo_1")
    
    # Execução do seu código lógico
    resultado = 42 + 10
    
    span.set_tag("resultado.sucesso", "true")
```

---

## 📊 O que validar na plataforma Datadog?

Após rodar a aplicação instrumentada e gerar tráfego, acesse o seu painel da Datadog para validar os entregáveis deste treinamento:
* 📉 **APM > Services:** Verifique se o serviço com o nome que foi definido em **service_name** no arquivo main.py está ativo no catálogo.
* 🌿 **APM > Traces:** Inspecione os gráficos de chama (Flame Graphs) e a árvore de chamadas do sistema.