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
    model_name = st.selectbox("🤖 Modelo", ["mixtral-8x7b-32768","llama3-70b-8192", "llama3-8b-8192", "llama2-70b-4096", "gemma-7b-it"])

    if model_name == "mixtral-8x7b-32768":
        max_tokens = 32768
    
    elif model_name == "llama2-70b-4096":
        max_tokens = 4096

    else:
        max_tokens = 8192

    input_max_new_tokens = st.slider("🧮 Número máximo de tokens gerados", min_value=2, max_value=max_tokens, step=2, value=256)
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

col1, col2 = st.columns([1, 2])

with col1:

    uploaded_file = st.file_uploader("Realize o upload", type=("txt", "md"))

    if uploaded_file:
            
            content = uploaded_file.getvalue().decode("latin-1")
            
            with st.container(height=300):
                st.markdown(content)
    
    button_action = {
        "resumir_docs": {
            "name": "⚡ Resumir documento",
            "action": "Leia o conteúdo do documento abaixo e faça um resumo do mesmo, trazendo uma lista com os seguintes itens: - Tipo do Documento (O que é o documento) - Resumo (resumir); - Principais Pontos (elencar tudo o que for pertinente saber sobre o documento, de forma objetiva). A resposta deve ser sempre no idioma Portugues (pt-br)."
        },
        "extrair_ner": {
            "name": "🔍 Identificar Entidades",
            "action": "Leia o conteúdo do documento abaixo e extraia as Entidades Nomeadas. A resposta deve ser um JSON sempre no idioma Portugues (pt-br)."
        },
        "identificar_infracoes": {
            "name": "🚨 Identificar infrações",
            "action": "Leia o conteúdo do documento abaixo e identifique se existem infrações relacionadas aos crimes que o Conselho Administrativo de Defesa Econômica investiga (Ex: Cartel, Formação de preços, Gunjumping, Fraudes em Licitações, e demais crimes do mercado). A resposta deve ser sempre no idioma Portugues (pt-br)."
        }
    }

    for button, action_data in button_action.items():

        if st.button(action_data["name"], use_container_width=True):

            question = action_data["action"]

            prompt = """
            {}

            {}
            """.format(question, content)


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
                    
                    st.toast("✅ Sucesso!")

                    with col2:

                        st.subheader("📝 Resultado")    
                        with st.container(height=400):
                            st.markdown(response)

                        @st.experimental_fragment
                        def download_button():
                            return st.download_button(label="📥 Baixar resultado", data=response, file_name="resultado.txt", mime="text/plain")
                        download_button()

                except:
                    st.error("❌ Erro ao gerar resposta.")
                    st.toast("💥 O número de tokens excedeu o limite, diminua o valor máximo de novos tokens ou o tamanho da pergunta!")
                    st.stop()