import streamlit as st
import google.generativeai as genai

# Load API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use the correct model name (try gemini-1.5-flash or gemini-1.5-pro)
try:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
except Exception as e:
    st.error(f"Error initializing model: {e}")
    st.stop()

# Set up Streamlit app
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("🤖 Gemini AI Chatbot")
st.caption("Built with Google Generative AI + Streamlit")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Get user input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    try:
        # Get response from Gemini
        with st.spinner("Thinking..."):
            response = st.session_state.chat_session.send_message(user_input)
            bot_reply = response.text
        
        # Show assistant reply
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.chat_history.append({"role": "assistant", "text": bot_reply})
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        with st.chat_message("assistant"):
            st.markdown(error_msg)
        st.session_state.chat_history.append({"role": "assistant", "text": error_msg})

# Add a sidebar with additional options
with st.sidebar:
    st.header("Settings")
    
    # Clear chat history button
    if st.button("🗑 Clear Chat History", type="secondary"):
        st.session_state.chat_history = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    # Model information
    st.subheader("Model Info")
    st.write("*Model:* gemini-1.5-flash")
    st.write("*API Version:* v1beta")
    
    # Show available models (optional debugging)
    if st.button("🔍 List Available Models"):
        try:
            models = genai.list_models()
            st.write("Available models:")
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    st.write(f"- {m.name}")
        except Exception as e:
            st.write(f"Error listing models: {e}")
