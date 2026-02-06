import os
import json
import boto3
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as chaves do seu arquivo .env
load_dotenv()

# Configuração AWS Bedrock
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# Configuração Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def get_embedding(text):
    """
    Usa o modelo Amazon Titan para transformar texto em um vetor numérico (Embedding).
    O Titan gera um vetor de 1536 dimensões, que é o que configuramos no seu SQL.
    """
    body = json.dumps({"inputText": text})
    response = bedrock_runtime.invoke_model(
        body=body, 
        modelId="amazon.titan-embed-text-v1", # Modelo Titan que discutimos
        accept="application/json", 
        contentType="application/json"
    )
    response_body = json.loads(response.get("body").read())
    return response_body.get("embedding")

def ingest_knowledge():
    # Exemplos de conteúdo baseados na Fluency Academy
    knowledge_base = [
        {
            "content": "O cronograma da Fluency Academy é estruturado em 12 meses, focando em imersão diária.",
            "metadata": {"category": "cronograma", "source": "manual_aluno"}
        },
        {
            "content": "A metodologia Fluency baseia-se no Ciclo de Memorização Espaçada (SRS) para retenção de vocabulário.",
            "metadata": {"category": "metodologia", "source": "pedagogico"}
        },
        {
            "content": "Alunos têm acesso a aulas de conversação ilimitadas no plano Premium a partir do módulo 3.",
            "metadata": {"category": "conversação", "source": "comercial"}
        }
    ]

    print("🚀 Iniciando ingestão de dados no Supabase...")

    for item in knowledge_base:
        print(f"Gerando vetor para: {item['content'][:30]}...")
        
        # 1. Gera o vetor usando AWS Titan
        vector = get_embedding(item['content'])
        
        # 2. Salva no Supabase (Tabela 'documents' que criamos via SQL)
        data = {
            "content": item['content'],
            "metadata": item['metadata'],
            "embedding": vector
        }
        
        supabase.table("documents").insert(data).execute()

    print("✅ Dados ingeridos com sucesso!")

if __name__ == "__main__":
    ingest_knowledge()