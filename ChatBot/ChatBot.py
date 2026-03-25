import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


#Criar o titulo 
st.title("My ChatBot")
st.markdown("---")

with st.sidebar:

    st.markdown("##  Configurações")
    st.markdown("---")

    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Crie sua chave em console.groq.com/keys"
    )

    st.markdown("---")

    contexto = st.text_area(
        "Contexto do assistente",
        value="Voce é um assistente academico da univille, especialista em Inteligencia Articifial. "
        "Explique conceitos de forma clara, didática e em português",
        height=170,
    )

    #Seleção do modelo
    modelo = st.selectbox(
        "Modelo Groq",
        [
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768",
            "llama3-70b-8192"
        ]
    )

    #configurações de temperatura
    temperatura = st.slider(
        "Temperatura (criatividade)",
        0.0, 1.0, 0.3
    )    

    #controle de memoria
    st.markdown("---")

    if st.button("Limpar conversa"):
        st.session_state.mensagens = []
        st.rerun()

    #nome do desenvolvedor
    st.markdown("---")
    st.markdown(
        "<small>Fundamento de IA - UNIVILLE - Laís Lessa</small>",
        unsafe_allow_html=True
    )

    if "mensagens" not in st.session_state:
        st.session_state.mensagens = st.session_state.get("messagens", [])

    for role, content in st.session_state.mensagens:
        with st.chat_message(role):
            st.markdown(content)