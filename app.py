import streamlit as st
import google.generativeai as genai

# Load API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use full model path
model = genai.GenerativeModel("models/gemini-pro")
chat = model.start_chat(history=[])

st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("🤖 Gemini AI Chatbot")
st.caption("Built with Google Generative AI + Streamlit")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    try:
        response = chat.send_message(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"❌ Error: {e}"

    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.chat_history.append({"role": "assistant", "text": bot_reply})
