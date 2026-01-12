import streamlit as st
import google.generativeai as genai
import os

# Configuração da página e Estilo Claro
st.set_page_config(page_title="ClaroBot - Vendas 2025", page_icon="🚀")

st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; }
    .claro-header { color: #ee1d23; font-weight: bold; font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

# 1. Configuração da API e Base de Conhecimento
# A API Key deve estar definida no ambiente como API_KEY
genai.configure(api_key=os.environ.get("API_KEY", "SUA_CHAVE_AQUI"))

SYSTEM_PROMPT = """
Você é o ClaroBot, um consultor de vendas especialista em internet fibra da Claro (Referência 2025). 
Seu objetivo é ser simpático, rápido e focado em fechar vendas.

Base de Conhecimento (Planos 2025):
- Claro Fibra 600 Mega: R$ 99,90 (R$ 79,90 no Combo Multi). Inclui Globoplay, McAfee e Wi-Fi 6.
- Claro Fibra 1 Giga: R$ 149,90 (R$ 129,90 no Combo Multi). Inclui Globoplay, McAfee e Wi-Fi Plus.

REGRA DE OURO - VIABILIDADE:
- Se o cliente mencionar o bairro "Vergel" ou "Vergel do Lago", você deve parar a venda imediatamente e dizer: "Infelizmente, acabo de consultar aqui e o bairro Vergel ainda não possui viabilidade técnica para Fibra Óptica no momento. Mas guardaremos seu contato para avisar assim que chegar!".

FLUXO DE VENDA:
1. Comece saudando e pedindo o CEP e o número da residência para consulta.
2. Após o CEP, mostre as opções de planos de forma atrativa.
3. Se o cliente escolher, peça: Nome Completo, CPF e Endereço para reserva da porta.
4. Finalize orientando-o a aguardar o contato humano para agendamento da instalação.

Mantenha as mensagens curtas e use emojis 🚀.
Sempre termine com uma pergunta para manter o engajamento.
"""

# Inicialização do Modelo (Usando a versão recomendada nas diretrizes)
model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    system_instruction=SYSTEM_PROMPT
)

# 2. Interface de Chat
st.markdown('<p class="claro-header">🔴 ClaroBot - Ultravelocidade Fibra</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou o assistente virtual da Claro. 🔴 Quer voar na internet? 🚀 Para começar, qual o seu **CEP** e o **número** da sua casa?"}
    ]

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Lógica de Resposta
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera resposta do Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Preparar histórico para o chat
        history = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages
        ]
        
        try:
            chat = model.start_chat(history=history[:-1])
            response = chat.send_message(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro na API: {e}")
