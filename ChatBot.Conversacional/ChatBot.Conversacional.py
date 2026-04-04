import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# Configuração da página
st.set_page_config(
    page_title="Chat IA",
    page_icon="🤖",
    layout="wide"
)

# Carregar variáveis de ambiente
load_dotenv(dotenv_path=".env")

st.markdown("""
<style>

    /* Fonte + Reseta margens */
    * {
        font-family: 'Inter', sans-serif;
    }

    body {
        background: #0f172a;
    }

    .main {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        padding-bottom: 120px !important;
    }

    /* Header */
    .header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 0;
        background: linear-gradient(135deg, #4f46e5 0%, #ec4899 100%);
        border-radius: 1rem;
        color: white;
        box-shadow: 0 0 20px rgba(99,102,241,0.5);
    }
    
    .header h1 {
        font-size: 2.8rem;
        margin: 0;
        font-weight: 900;
    }

    .header p {
        margin-top: .5rem;
        opacity: .85;
        font-size: 1.05rem;
    }

    /* Chat Messages */
    .chat-message {
        padding: 1.3rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
        backdrop-filter: blur(4px);
        animation: fadeIn .4s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-message {
        background: rgba(99,102,241,0.3);
        border: 1px solid rgba(99,102,241,0.5);
        margin-left: auto;
        max-width: 80%;
        border-radius: 1.5rem 0.8rem 0.8rem 1.5rem;
        box-shadow: 0 0 12px rgba(99,102,241,0.3);
    }

    .assistant-message {
        background: rgba(51,65,85,0.4);
        border: 1px solid rgba(148,163,184,0.3);
        max-width: 80%;
        border-radius: 0.8rem 1.5rem 1.5rem 0.8rem;
        box-shadow: 0 0 12px rgba(15,23,42,0.3);
    }

    .message-avatar {
        font-size: 1.8rem;
        display: flex;
        align-items: center;
    }

    .message-content {
        flex: 1;
        color: #f1f5f9;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Input fixo */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1.3rem;
        background: rgba(15,23,42,0.95);
        border-top: 1px solid #334155;
        backdrop-filter: blur(6px);
        z-index: 999;
    }

    /* Estilo do input */
    div[data-baseweb="input"] input {
        background: #1e293b !important;
        color: white !important;
        border-radius: 0.75rem !important;
        border: 1px solid #475569 !important;
        padding: 12px !important;
    }

    /* Botão enviar */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #8b5cf6 100%);
        color: white;
        padding: 0.7rem 1rem;
        border-radius: 0.75rem;
        border: none;
        font-weight: 600;
        transition: 0.2s;
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 12px rgba(139,92,246,0.6);
    }

</style>
""", unsafe_allow_html=True)



with st.sidebar:
    st.markdown("### ⚙️ Configurações do Chat")

    model_name = st.selectbox(
        "Modelo IA",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma-2-9b-it"]
    )

    temperature = st.slider("Criatividade", 0.0, 1.0, 0.7, 0.1)

    max_tokens = st.slider("Comprimento Máximo", 256, 2048, 1024, 256)

    st.divider()

    if st.button("🧹 Limpar Conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("#### ℹ️ Sobre o sistema")
    st.markdown("""
    *Chat IA com Streamlit + Groq*
    
    Tecnologias:
    - ⚡ Groq API
    - 🧠 LangChain
    - 🎈 Streamlit
    """)


#Header 

st.markdown("""
<div class="header">
    <h1>🤖 Chat IA</h1>
    <p>Fale com seu assistente inteligente em tempo real</p>
</div>
""", unsafe_allow_html=True)



if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GROQ_API_KEY", "")



chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        avatar = "👤" if isinstance(message, HumanMessage) else "🤖"
        cls = "user-message" if isinstance(message, HumanMessage) else "assistant-message"

        st.markdown(f"""
        <div class="chat-message {cls}">
            <div class="message-avatar">{avatar}</div>
            <div class="message-content">{message.content}</div>
        </div>
        """, unsafe_allow_html=True)



st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)




with st.container():
    col1, col2 = st.columns([0.85, 0.15])

    with col1:
        user_input = st.text_input(
            "Digite algo...",
            placeholder="Digite sua mensagem...",
            label_visibility="collapsed",
            key="user_input"
        )

    with col2:
        submit = st.button("Enviar 📤", use_container_width=True)



if submit and user_input:
    if not st.session_state.api_key:
        st.error("⚠️ Nenhuma chave GROQ_API_KEY configurada.")
    else:
        st.session_state.messages.append(HumanMessage(content=user_input))

        llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=st.session_state.api_key
        )
        # Instrução fixa para manter o chatbot sempre em português
        st.session_state.messages.insert(0, AIMessage(content="Você é um assistente que sempre responde em português brasileiro, de forma clara e natural."))

        with st.spinner("🤖 Pensando..."):
            response = llm.invoke(st.session_state.messages)

        st.session_state.messages.append(AIMessage(content=response.content))

        st.rerun()