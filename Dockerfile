# Imagem base leve do Python
FROM python:3.10-slim

# Diretório de trabalho no container
WORKDIR /app

# Instala dependências de sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala requisitos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto e a pasta de serviços
COPY . .

# Expõe as portas do FastAPI (8000) e Streamlit (8501)
EXPOSE 8000
EXPOSE 8501