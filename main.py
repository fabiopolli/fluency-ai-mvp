import os
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client
from services.guardrails import GuardrailService
from services.ai_service import AIService

load_dotenv()

app = FastAPI(title="Fluency Academy AI Tutor")

# Inicialização de Clientes
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
ai_service = AIService(supabase)

class ChatRequest(BaseModel):
    message: str

def log_event(message: str, source: str):
    """Tarefa em background para auditoria."""
    print(f" [LOG] Mensagem: {message[:30]}... | Fonte: {source}")

@app.post("/chat")
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    user_msg = request.message
    
    # 1. Validação de Guardrail (Step 2)
    static_reply = GuardrailService.check(user_msg)
    if static_reply:
        background_tasks.add_task(log_event, user_msg, "guardrail")
        return {"source": "guardrail", "response": static_reply}
    
    # 2. RAG & Recuperação de Contexto (Step 3)
    docs = ai_service.retrieve_context(user_msg)
    
    if not docs:
        background_tasks.add_task(log_event, user_msg, "empty_rag")
        return {"source": "empty_rag", "response": "Não encontrei informações específicas no material pedagógico."}
    
    # 3. Geração de Resposta com Claude (Step 4)
    ai_reply = ai_service.generate_response(user_msg, docs)
    background_tasks.add_task(log_event, user_msg, "claude_35_sonnet")
    
    return {
        "source": "claude_35_sonnet",
        "response": ai_reply,
        "context_used": [d['content'] for d in docs]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)