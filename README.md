---

📱 Versão Mobile — Ascensão IA

A versão mobile do Ascensão foi desenvolvida utilizando Python + Kivy, com foco em oferecer uma experiência completa de inteligência artificial personalizada diretamente no Android.
Ela integra autenticação de usuários, armazenamento em nuvem, síntese de voz, histórico de conversas e uma interface interativa inspirada em assistentes virtuais.


---

🚀 Funcionalidades Principais

🔐 Sistema de Login e Cadastro

Criação de conta com nome, email e senha.

Validações em tempo real (email, senha, campos vazios).

Máscara de senha e opção de mostrar/ocultar.

Dados armazenados no Firebase Realtime Database.



---

👤 Persistência de Dados do Usuário

As seguintes informações ficam salvas e acessíveis durante toda a execução do app:

Nome do usuário

Email

Foto de perfil

Histórico de conversas


Esses dados são mantidos na memória e evitam consultas desnecessárias ao Firebase.


---

🗣️ Assistente de Voz Integrado

O app possui um módulo de fala (fala() e parar_audio()).

Cada ação importante do usuário é acompanhada por resposta em áudio.

Botão para ativar/desativar narração.



---

🤖 Integração com IA — Modelo Qwen 7B

Envio de perguntas para a API definida no .env.

Respostas exibidas na tela e também narradas.

Salvamento automático da resposta no Firebase.



---

🖼️ Personalização do Perfil

O usuário pode:

Alterar a foto de perfil selecionando imagens disponíveis.

Alterar nome, email e senha.

As alterações são refletidas no Firebase em tempo real.



---

📜 Histórico de Conversas

Lista de todas as conversas salvas no Firebase.

Possibilidade de abrir qualquer conversa anterior.

Opção de excluir conversas individualmente.



---

🌐 Verificação de conexão

Antes de ações importantes, o aplicativo verifica acesso à internet via socket.create_connection.


---

🧩 Navegação por Telas (ScreenManager)

O app utiliza múltiplas telas:

Login

Cadastro

Home

Configurações

Mudar foto

Mudar nome

Mudar email

Mudar senha

Histórico de conversas

Tela "Aguardando" com animação



---

🎨 Interface Gráfica (Kivy)

Layout construído com o arquivo main.kv.

UI otimizada para telas móveis.

Animações, botões personalizados e imagens de fundo.

Popups com mensagens de confirmação.



---

🛠️ Tecnologias Utilizadas

Python 3

Kivy

Firebase Realtime Database

Requests

Threading (para evitar tela travada)

Kivy Animation

Kivy ScreenManager

dotenv para variáveis de ambiente



---

📂 Estrutura Geral da Aplicação

main.py

Contém:

Importações

Classes de telas

Funções de login/cadastro

Integração com Firebase

Integração com API de IA

Controle de áudio

Sistema de navegação

Popups e animações

Salvamento do histórico


main.kv

Contém:

Toda a interface do usuário

Organização de layout (FloatLayout, GridLayout, ScrollView etc.)

IDs utilizados pelo Python



---

🧠 Objetivo da Versão Mobile

A versão mobile é a base do ecossistema Ascensão, permitindo:

Testar as funcionalidades principais da IA

Criar contas reais com dados persistentes

Desenvolver interação com modelos de linguagem

Criar o núcleo da arquitetura que será expandido para web e integração com Java
