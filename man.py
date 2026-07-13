import streamlit as str
import google.generativeai as genai

# 1. Configuração Secreta do Galo Mestre (Área Crítica Protegida 🔒)
INSTRUCAO_SISTEMA = """
Tu és o Galo Mestre, o cérebro de inteligência artificial da SNGcomercial para avicultura inteligente.
Teu objetivo é gerir alertas de sensores (DHT22, Humidade de Cama, Presença PIR), dar diagnósticos biológicos
e converter análises financeiras sempre focando no mercado de Angola (Moeda: Kwanza - KZ).
"""

# Configura a chave de API de forma segura
genai.configure(api_key=str.secrets["GOOGLE_API_KEY"])

str.set_page_config(page_title="Galo Mestre - IA Aviário", page_icon="🐓")
str.title("🐓 Galo Mestre v1.0")
str.write("O assistente inteligente para a gestão e biossegurança do teu aviário.")

# Inicializa o modelo com a instrução oculta
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=INSTRUCAO_SISTEMA
)

# Inicializa o histórico do chat na tela
if "messages" not in str.session_state:
    str.session_state.messages = []

# Mostra as mensagens anteriores na tela
for message in str.session_state.messages:
    with str.chat_message(message["role"]):
        str.write(message["content"])

# Caixa de texto onde o teu amigo vai digitar
if user_input := str.chat_input("Diz ao Galo Mestre o estado do teu galpão..."):
    str.session_state.messages.append({"role": "user", "content": user_input})
    with str.chat_message("user"):
        str.write(user_input)
        
    # Envia para o Gemini processar com base na instrução secreta
    response = model.generate_content(user_input)
    
    str.session_state.messages.append({"role": "assistant", "content": response.text})
    with str.chat_message("assistant"):
        str.write(response.text)
