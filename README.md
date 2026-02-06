# 🎓 Fluency Academy AI Tutor - MVP

![CaseFluency-ezgif com-speed](https://github.com/user-attachments/assets/2c6bd45f-be9f-4e5a-9886-63fb73fb8152)

Este repositório apresenta um case de estudo de um tutor inteligente de alta performance. O sistema utiliza uma arquitetura robusta de **RAG (Retrieval-Augmented Generation)** para fornecer respostas precisas e contextualizadas sobre a metodologia e cronograma da escola, baseando-se em documentos oficiais.

## 🏗️ Arquitetura e Engenharia de IA

O projeto foi desenhado sob os pilares de **Clean Architecture**, **Sustentabilidade** e **FinOps**:

* **Camada de Guardrails**: Implementação de filtros determinísticos via Regex no FastAPI para interceptar intenções administrativas (preços, suporte), garantindo resposta instantânea e custo zero de LLM.
* **Mecanismo de RAG**: Processamento de documentos com `amazon.titan-embed-text-v1` e busca por similaridade vetorial executada diretamente no PostgreSQL (Supabase) via `pgvector`.
* **Orquestração de LLM**: Uso do **Claude 3.5 Sonnet** via Amazon Bedrock, escolhido pela sua janela de contexto estável e tom pedagógico superior.
* **Observabilidade**: Registro de eventos através de `BackgroundTasks` do FastAPI, permitindo auditoria assíncrona sem impactar o tempo de resposta do usuário.
* **Modularização**: Código desacoplado em camadas (`services/`), facilitando a manutenção e testes unitários.

## 🛠️ Stack Tecnológica

* **Linguagem**: Python 3.10+
* **Backend**: FastAPI
* **Frontend**: Streamlit
* **IA/LLM**: Amazon Bedrock (Claude 3.5 Sonnet & Titan Embeddings)
* **Vector DB**: Supabase (PostgreSQL + pgvector)
* **DevOps**: Docker & Docker Compose

## 🚀 Como Executar e Testar

### 1. Pré-requisitos
* Docker Desktop instalado e rodando.
* Credenciais da AWS com acesso ao Bedrock liberado.
* URL e Key de um projeto Supabase com a função `match_documents` criada.

### 2. Configuração
Renomeie o arquivo `.env.example` para `.env` e preencha com suas chaves:
```env
AWS_ACCESS_KEY_ID=sua_chave
AWS_SECRET_ACCESS_KEY=seu_segredo
AWS_REGION=us-east-1
SUPABASE_URL=sua_url
SUPABASE_KEY=sua_key
```

### 3. Inicialização via Docker
Na raiz do projeto, execute o comando para subir o ecossistema completo (API + UI):
```bash
docker-compose up --build

### 4. Roteiro de Testes
Após a inicialização, abra o navegador em `http://localhost:8501` e teste os seguintes cenários:

* **Cenário 1 (Guardrail/FinOps)**: Pergunte *"Qual o preço do curso?"*.
    * **Resultado esperado**: Resposta instantânea vinda do código (Regex), sem gasto de tokens.
* **Cenário 2 (RAG/Conhecimento)**: Pergunte *"Como funciona o cronograma de 12 meses?"*.
    * **Resultado esperado**: O tutor buscará no banco vetorial e explicará a jornada pedagógica baseada nos documentos.
* **Cenário 3 (Segurança/Contexto)**: Pergunte *"Qual a previsão do tempo?"*.
    * **Resultado esperado**: O tutor informará que seu conhecimento é restrito à Fluency Academy, evitando alucinações fora de escopo.

## 🧐 Documentação Técnica Adicional

* **Swagger API:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Roadmap de Desenvolvimento:** Consulte o arquivo `ROADMAP.md` para o histórico detalhado de cada etapa concluída.

---
**Desenvolvido por Fabio Polli** |
