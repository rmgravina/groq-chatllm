import streamlit as st
import maritalk
import icecream as ic
from dotenv import load_dotenv
import os
from st_pages import Page, show_pages, add_page_title
from annotated_text import annotated_text, annotation
import json
from groq import Groq

# Instanciando o cliente Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# Importando as variáveis do arquivo .env
load_dotenv()
st.set_page_config(page_title="Groq AI - Cade", page_icon="🦜", layout="wide", initial_sidebar_state="expanded")

show_pages(
    [
        Page("app.py", "Início", "🎉"),
        Page("pages\chat_bot.py", "Assistente virtual", "🤖"),
        Page("pages\chat_docs.py", "Pergunte sobre o documento", "✨")
    ]
)

with open('_auth_api_users_.json', 'r') as file:
    admin_users = json.load(file)


st.title("✨ Pergunte sobre o documento")
st.write("⚡ Agent: Zero-shot classification")
st.divider()

api_key = None
for user in admin_users:
    if user["username"] == st.session_state['LOGGED_IN_USER']:
        api_key = os.getenv('GROQ_API_KEY')

with st.sidebar:
    st.header("🔑 API Key")

    if api_key:
        st.success("✅ API Key habilitada.")

    else:
        api_key = st.text_input("Digite sua API Key", type="password")
        st.info('💡 Para obter sua API Key, acesse o Groq Cloud.')

    st.divider()
    model_name = st.selectbox("🤖 Modelo", ["mixtral-8x7b-32768", "llama2-70b-4096", "gemma-7b-it"])
    input_max_new_tokens = st.slider("🧮 Número máximo de tokens gerados", min_value=2, max_value=8000, step=2, value=256)
    input_temperature = st.slider("🌡️ Temperatura", min_value=0.0, max_value=1.0, step=0.01, value=0.7)

# To be implemented: Modelo local (generate_raw())
    
#    choice_seed = st.radio("🌱 Seed", ("Aleatório", "Fixo"))
#    if choice_seed == "Aleatório":
#        input_seed = None
#    else:
#        input_seed = st.number_input("Esolha um valor:",
#                                     value=0,
#                                     step=1,
#                                     max_value=100000,
#                                     help="O valor escolhido não interfere na qualidade do modelo, apenas parametriza para que as respostas sejam sempre replicáveis para a mesma pergunta."
#                                     )


uploaded_file = st.file_uploader("Realize o upload", type=("txt", "md"))
question = st.text_input("Pergunte algo:", placeholder="Você pode resumir o documento?", disabled=not uploaded_file)

if uploaded_file:
    content = uploaded_file.getvalue().decode("latin-1")
    prompt = """
    {}

    {}
    """.format(question, content)

if st.button("⚡ Gerar resposta"):
    if api_key == "":
        st.error("❌ API Key não encontrada.")
        st.stop()

    elif uploaded_file is None:
        st.warning("Realize o upload de um arquivo.", icon="⚠")
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

    with st.spinner("⏳ Aguarde..."):
        try:
                
            response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    }],
                    model=model_name,
                    temperature=input_temperature,
                    max_tokens=input_max_new_tokens,
        ).choices[0].message.content # Adicionar seed quando pertinente
            
            st.success("✅ Pronto!")
            annotated_text(
                
                annotation(response, "🤖", border='1px dashed blue')
            )

        except:
            st.error("❌ Erro ao gerar resposta.")
            st.toast("💥 O número de tokens excedeu o limite, diminua o valor máximo de novos tokens ou o tamanho da pergunta!")
            st.stop()

    if st.button("🔁 Realizar outra pergunta"):
        st.experimental_rerun()