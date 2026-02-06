# Roadmap: MVP AI Engineer - Fluency Academy

Este documento detalha o progresso da construção do MVP focado em Engenharia de IA para o processo seletivo da Fluency Academy.

---

## 📋 Status do Projeto
- [x] **Configuração de Infra:** AWS (IAM/Bedrock) e Supabase operacionais.
- [x] **Step 1: Ingestão de Dados (ETL):** Banco populado com embeddings Titan.
- [x] **Step 2: Camada de Guardrails:** FastAPI filtrando intenções administrativas (Regex).
- [x] **Step 3: Mecanismo de RAG:** Função RPC `match_documents` e busca vetorial integrada.
- [x] **Step 4: Orquestração Bedrock:** Claude 3.5 Sonnet integrado.
- [x] **Step 5: Observabilidade:** Adição de Background Tasks para log de eventos (Audit Log).
- [x] **Step 6: Refatoração Modular:** Organização do código em camadas (`services/`).
- [x] **Step 7: Interface UI:** Criação de interface visual com Streamlit.
- [x] **Step 8: Dockerização:** Criação de containers e orquestração via Docker Compose.

---

## 🚀 Detalhamento dos Passos

| Fase | Ação Técnica | Justificativa de Engenharia (O "Porquê") |
| :--- | :--- | :--- |
| **2. Guardrails** | Implementar lógica de **Regex** no FastAPI. | **FinOps:** Evita gastos com LLM para perguntas de resposta fixa. |
| **3. Mecanismo de RAG** | Desenvolver busca de similaridade no banco de dados. | **Núcleo da Vaga:** Recupera contexto relevante para reduzir alucinações. |
| **4. Orquestração** | Integrar o **Claude 3.5 Sonnet**. | **Qualidade:** Uso da ferramenta oficial (Bedrock) para raciocínio superior. |
| **5. Observabilidade** | Adicionar **Background Task** para logs. | **Produção:** Monitoramento eficiente sem travar a resposta ao usuário. |
| **6. Modularização** | Separar o código em pastas (`services/`). | **Sustentabilidade:** Segue Clean Architecture, facilitando manutenção. |
| **7. Interface UI** | Criar frontend reativo com **Streamlit**. | **UX:** Proporciona uma experiência de chat amigável para o usuário final. |
| **8. Dockerização** | Criar Dockerfile e Docker Compose. | **DevOps:** Garante que a aplicação rode em qualquer ambiente sem conflitos. |

---

## 🧐 Glossário de Decisões Técnicas (Arquitetura Sênior)

### 1. Ingestão e Embeddings (Amazon Titan)
* **Decisão:** Uso do modelo `amazon.titan-embed-text-v1`.
* **Justificativa:** Melhor integração nativa com AWS Bedrock e suporte ao padrão de 1536 dimensões.

### 2. Guardrail Determinístico (Regex)
* **Decisão:** Filtro de intenções administrativo/financeiro no backend.
* **Justificativa (FinOps):** Redução drástica de custos e latência para perguntas previsíveis.

### 3. Busca Vetorial In-Database (RPC/pgvector)
* **Decisão:** Cálculo de similaridade executado diretamente no PostgreSQL.
* **Justificativa:** Performance e escalabilidade ao processar dados onde eles residem.

### 4. Orquestração de Prompt (Claude 3.5 Sonnet)
* **Decisão:** Uso do Claude 3.5 Sonnet via Amazon Bedrock.
* **Justificativa:** Janela de contexto estável e tom pedagógico superior.

### 5. Modularização (Clean Architecture)
* **Decisão:** Separação do código em `services/` e controladores (`main.py`).
* **Justificativa:** Segue o princípio de Responsabilidade Única (SRP), facilitando manutenção.

### 6. Background Tasks (FastAPI)
* **Decisão**: Uso do recurso nativo `BackgroundTasks`.
* **Justificativa**: Permite logs de auditoria sem bloquear o tempo de resposta ao usuário.

### 7. Interface de Usuário (Streamlit)
* **Decisão**: Uso do Streamlit para o frontend.
* **Justificativa**: Permite criar uma interface de chat reativa com baixo overhead de código.

### 8. Containerização (Docker)
* **Decisão:** Uso de Docker Compose V2.
* **Justificativa:** Garante isolamento total do ambiente e facilita a orquestração de múltiplos serviços (API + UI).