import streamlit as str
import google.generativeai as genai

if "GOOGLE_API_KEY" in str.secrets:
    genai.configure(api_key=str.secrets["GOOGLE_API_KEY"])
else:
    str.error("API Key not configured in Streamlit Secrets.")

SYSTEM_INSTRUCTION = """
You are Galo Mestre, the brain of an intelligent aviculture system.
Your objective is to manage sensor alerts, feeding, and environment management.
"""

str.title("🐓 Galo Mestre - Intelligent Control")

if "messages" not in str.session_state:
    str.session_state.messages = []

for message in str.session_state.messages:
    with str.chat_message(message["role"]):
        str.write(message["content"])

if user_input := str.chat_input("How can I help with the poultry farm today?"):
    str.session_state.messages.append({"role": "user", "content": user_input})
    with str.chat_message("user"):
        str.write(user_input)
        
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        response = model.generate_content(user_input)
        
        str.session_state.messages.append({"role": "assistant", "content": response.text})
        with str.chat_message("assistant"):
            str.write(response.text)
    except Exception as e:
        str.error(f"Error communicating with Gemini: {e}")
