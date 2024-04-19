import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
import json
import os
from dotenv import load_dotenv
import maritalk
import icecream as ic
import os
from st_pages import Page, show_pages, add_page_title
from groq import Groq

# Importando as variáveis do arquivo .env
load_dotenv()

# Instanciando o cliente Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

st.set_page_config(page_title="Chatbot", page_icon="🦜", layout="wide", initial_sidebar_state="expanded")

show_pages(
    [
        Page("app.py", "Início", "🎉"),
        Page("pages\chat_bot.py", "Assistente virtual", "🤖"),
        Page("pages\chat_docs.py", "Pergunte sobre o documento", "✨")
    ]
)

with open('_auth_api_users_.json', 'r') as file:
    admin_users = json.load(file)

st.title("🤖 Assistente virtual")
st.write("⚡ Agent: Chatbot")
st.divider()


api_key = None
for user in admin_users:
    if user["username"] == st.session_state['LOGGED_IN_USER']:
        api_key = os.getenv('GROQ_API_KEY')
        username = user["username"]

with st.sidebar:
    model_name = st.selectbox("🤖 Modelo", ["mixtral-8x7b-32768","llama3-70b-8192", "llama3-8b-8192", "llama2-70b-4096", "gemma-7b-it"])
    st.divider()
    st.header("🔑 API Key")

    if api_key:
        st.success("✅ API Key habilitada.")

    else:
        api_key = st.text_input("Digite sua API Key", type="password")
        st.info('💡 Para obter sua API Key, acesse o Groq Cloud.')
        username = st.session_state['LOGGED_IN_USER']


if "messages" not in st.session_state:
    
    st.session_state["messages"] = [{"role": "assistant", "content": "🖐 Olá, {}! \n\nBem vindo ao CadeTalk, como podemos te ajudar?".format(username)}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
                
    if not api_key:
        st.info("🔒 Por favor, insira sua Groq API key para continuar.")
        st.stop()


    try:
        client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "ping",
                    }],
                    model=model_name,
                    temperature=1.0,
                    max_tokens=1,
        )

    except:
        st.error("❌ API Key inválida.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
            messages=st.session_state.messages,
                    model=model_name,
                    temperature=1.0,
        ).choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
    print(st.session_state.messages)


if len(st.session_state.messages) > 1:
            
    if st.button("🧹 Limpar"):
        st.session_state["messages"] = [{"role": "assistant", "content": "🖐 Olá, {}! \n\nBem vindo ao CadeTalk, como podemos te ajudar?".format(username)}]
        
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        st.rerun()
