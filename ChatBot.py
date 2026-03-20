import streamlit as st
# import os
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate


#Criar o titulo 
st.title("My ChatBot")


with st.sidebar:

    st.markdown("##  Configurações")
    st.markdown("---")

    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Crie sua chave em console.groq.com/keys"
    )