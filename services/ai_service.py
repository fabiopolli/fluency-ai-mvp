import os
import json
import boto3
from typing import List

class AIService:
    def __init__(self, supabase_client):
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.supabase = supabase_client
        self.embedding_model = "amazon.titan-embed-text-v1"
        self.llm_model = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    def get_embedding(self, text: str) -> List[float]:
        body = json.dumps({"inputText": text})
        response = self.bedrock.invoke_model(
            body=body,
            modelId=self.embedding_model,
            accept="application/json",
            contentType="application/json"
        )
        return json.loads(response.get("body").read()).get("embedding")

    def retrieve_context(self, query_text: str) -> List[dict]:
        embedding = self.get_embedding(query_text)
        rpc_params = {
            "query_embedding": embedding,
            "match_threshold": 0.5,
            "match_count": 2
        }
        response = self.supabase.rpc("match_documents", rpc_params).execute()
        return response.data

    def generate_response(self, question: str, context_docs: List[dict]) -> str:
        context_text = "\n".join([doc['content'] for doc in context_docs])
        prompt_config = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [
                {
                    "role": "user",
                    "content": f"Você é um tutor da Fluency Academy.\nCONTEXTO:\n{context_text}\n\nPERGUNTA:\n{question}"
                }
            ]
        }
        response = self.bedrock.invoke_model(
            modelId=self.llm_model,
            body=json.dumps(prompt_config)
        )
        result = json.loads(response.get("body").read())
        return result["content"][0]["text"]