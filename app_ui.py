import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Fluency Tutor AI", page_icon="🎓")
st.title("🎓 Fluency Academy Tutor")
st.markdown("Olá! Eu sou seu assistente pedagógico. Como posso te ajudar hoje?")

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Pergunte sobre a metodologia ou cronograma..."):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chamada para a sua API FastAPI que já está rodando
    try:
        with st.spinner("Pensando..."):
            response = requests.post(
                "http://localhost:8000/chat", 
                json={"message": prompt}
            ).json()
            
            answer = response.get("response", "Desculpe, ocorreu um erro na resposta.")
            source = response.get("source", "unknown")
            
            # Exibe resposta do assistente
            with st.chat_message("assistant"):
                st.markdown(answer)
                if source == "guardrail":
                    st.caption("ℹ️ Esta é uma resposta automática do suporte.")
            
            # Salva no histórico
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")