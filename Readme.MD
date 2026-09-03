# 🦊✨ RMG LLM - Streamlit App

RMG LLM é uma aplicação baseada num chatbot que utiliza a API do Groq para realizar inferência em modelos LLM opensource, com objetivo de para gerar respostas baseadas nas perguntas do usuário. Este projeto foi desenvolvido utilizando a linguagem de programação Python e a biblioteca Streamlit para criar a interface de usuário.

A aplicação consiste em duas partes:

1. 🤖 Assistente virtual: Este módulo permite que o usuário interaja com o assistente virtual. Na barra lateral, o usuário pode inserir sua própria chave de API do Groq. Posteriormente, o usuário pode fazer perguntas ao assistente virtual. Em caso de autorização do usuário, será habilitado o uso da API institucional.

2. ✨ Pergunte sobre o documento: Neste módulo, o usuário pode fazer o upload de um documento de texto (.txt, .md) e fazer perguntas com base no texto do documento. O assistente é capaz de ler o documento fornecido e gerar respostas com base no conteúdo do documento.

## ⚡ Instalação e Execução

Para usar esta aplicação, é necessário ter um ambiente Python no diretório e instalar todas as dependências listadas no arquivo 'requirements.txt'. 

Para instalar as dependências utilizando o pip, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

Posteriormente, você pode iniciar a aplicação com o seguinte comando:

```bash
streamlit run app.py
```

## 💡 Como usar

Ao iniciar a aplicação, o usuário será redirecionado para uma interface de login. Aqui, existem algumas opções que o usuário pode seguir:

- **Entrar 🎉:** Para os utilizadores que já possuem uma conta, basta inserir seu usuário e senha corretamente para acessar os recursos do aplicativo. Caso a senha ou o nome do usuário esteja errado, uma mensagem de erro "Usuário ou Senha inválidos!" aparecerá na tela.

- **Cadastrar ✨:** Para os utilizadores que ainda não possuem uma conta, é preciso informar seu nome, um endereço de e-mail válido, um nome de usuário único e uma senha. Se o nome, o e-mail ou o nome de usuário não forem válidos ou já estiverem em uso, mensagens de erro correspondentes serão exibidas na tela. Após clicar em 'Cadastrar', se as informações forem corretas, a conta será criada e a mensagem "Registration Successful" aparecerá.

- **Esqueceu a senha 🔑:** Caso o usuário esqueça sua senha, pode inserir o endereço de email associado à conta e pressionar 'Solicitar senha'. Em seguida, uma senha segura aleatória será enviada para o e-mail informado, se ele estiver registrado em nossa base.

- **Resetar a senha 🔥:** Para alterar uma senha, o usuário deve fornecer o e-mail associado à conta, a senha temporária que foi enviada para o e-mail, uma nova senha e, por fim, confirmar a nova senha. Se as informações estiverem corretas e as novas senhas coincidirem, a senha será alterada e a mensagem "Senha resetada com sucesso!" será exibida na tela.

- **Sair ⛔:** Finalmente, uma vez logado no sistema, o usuário terá a opção de sair ao clicar no botão 'Sair' na barra lateral. Quando o usuário sair, todos os dados da sessão serão redefinidos.


Após feito o login, o usuário irá ver uma tela inicial com algumas instruções e, no menu lateral, serão exibidas as opções de '🤖 Assistente virtual' e '✨ Pergunte sobre o documento'.

## 🔒 Autorização

Para habilitar o uso da API Master, o usuário deve ser liberado pela equipe de desenvolvimento (utilizando o script `_admin_console.py`). Se autorizado, o usuário não precisará mais inserir sua chave de API do Groq para usar a aplicação, e uma nova mensagem será exibida no menu lateral informado que a API Master está habilitada.

## 🤝 Contribuição

Contribuições são sempre bem-vindas!
<br>
Entre em contato com os [desenvolvedores](mailto:rmgravina@gmail.com).

## ✅ Licença

[MIT](http://opensource.org/licenses/MIT)