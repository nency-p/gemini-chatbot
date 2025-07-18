import streamlit as st # type: ignore
import google.generativeai as genai # type: ignore

# Load API key from Streamlit secrets
genai.configure(api_key=st.secrets["AIzaSyBrdDhLHxumSpMerAmLkbE7lWoUG4dEuTY"])

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Set up Streamlit app
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("🤖 Gemini AI Chatbot")
st.caption("Built with Google Generative AI + Streamlit")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Get user input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message to session
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    try:
        # Get Gemini response
        response = chat.send_message(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"❌ Error: {e}"

    # Display and store response
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.chat_history.append({"role": "assistant", "text": bot_reply})
