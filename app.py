import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from streamlit_lottie import st_lottie
import json
import os
from dotenv import load_dotenv
import maritalk
import icecream as ic
import os
from st_pages import Page, show_pages, add_page_title



# Importando as variáveis do arquivo .env
load_dotenv()
courier_auth_token = os.getenv('COURIER_AUTH_TOKEN')

st.set_page_config(page_title="Cade AI", page_icon="🤖")
show_pages(
    [
        Page("app.py", "Início", "🎉")
    ]
)


__login__obj = __login__(auth_token = courier_auth_token, 
                    company_name = "🤖 Cade AI",
                    width = 400, height = 400, 
                    logout_button_name = 'Sair ⛔', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://lottie.host/9f13f730-9b28-4df8-adc3-88cc436f2f99/VFDI3AXgWq.json')

LOGGED_IN = __login__obj.build_login_ui()


if st.session_state['LOGGED_IN'] == True:

    show_pages(
    [
        Page("app.py", "Início", "🎉"),
        Page("pages\chat_bot.py", "Assistente virtual", "🤖"),
        Page("pages\chat_docs.py", "Pergunte sobre o documento", "✨")
    ]
)
    c1, c2 = st.columns([7,7])

    with st.container():
        st.markdown(f"<h1 style='text-align: center; color: white; font-size: 2em;'> Olá, {st.session_state['LOGGED_IN_USER']}!</h1>", unsafe_allow_html=True)


    with st.container():


        with c1:

            st.divider()
            st.markdown("<h1 style='text-align: center; color: white; font-size: 1.8em;'>Defesa Econômica com Inteligência Artificial</h1>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center; color: white; font-size: 1em;'> <br> </h1>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center; color: white; font-size: 1em;'> 🤖 D.E.I.A 🤖 </h1>", unsafe_allow_html=True)
            st.divider()

        with c2:

            st_lottie("https://lottie.host/88b776bf-ded8-4dc9-b6e0-6a29f87f5269/jzFTpSjXh1.json", width = 350, height = 350)
    
    st.divider()
    
    st.write("""

O CadeAI é uma aplicação de chatbot que utiliza a API do Groq para gerar respostas baseadas em perguntas do usuário. Este projeto foi desenvolvido utilizando a linguagem de programação Python e a biblioteca Streamlit para criar a interface de usuário.

Esta aplicação consiste em duas partes principais:

1. 🤖 Assistente virtual: neste módulo, o usuário irá interagir com o assistente virtual. Na barra lateral, o usuário pode inserir sua própria chave de API do Groq. Depois disso, o usuário pode começar a fazer perguntas ao assistente virtual. Caso o usuário esteja autorizado, será liberado o uso da API institucional.

2. ✨ Pergunte sobre o documento: neste módulo, o usuário pode fazer upload de um documento de texto (.txt, .md) e fazer perguntas sobre o texto no documento. O assistente é capaz de ler o documento fornecido e gerar respostas com base no conteúdo do documento.""")
  
    


