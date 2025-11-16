import streamlit as st
import google.generativeai as genai


# ============================
# PAGE SETTINGS
# ============================
st.set_page_config(page_title="Humanities Chatbot", page_icon="🎓")

st.title("🎓 Humanities Chatbot")


# ============================
# API KEY
# ============================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


# ============================
# SYSTEM INSTRUCTION
# ============================
HUMANITIES_PROMPT = """
You are an AI Humanities Chatbot.

Identity:
- You respond through philosophy, psychology, ethics, culture, literature, and history.
- You provide deeper meaning and reflective insights.

Response structure:
1. Surface answer
2. Humanities interpretation
3. A reflective question

Tone:
Warm, thoughtful, curious, grounded.

IMPORTANT RULES:
- Never output anything in JSON, XML, code blocks, or structured data.
- Never output or mention roles like "user", "model", "assistant", or "system".
- Never include metadata or internal formatting.
"""

# ============================
# LOAD MODEL + CHAT SESSION
# ============================
@st.cache_resource
def load_model_and_session():
    # Try different model names - use one that works
    try:
        model = genai.GenerativeModel(
            "gemini-1.5-flash",  # Try this model name
            system_instruction=HUMANITIES_PROMPT
        )
        return model.start_chat(history=[])
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

chat_session = load_model_and_session()


# ============================
# SESSION STATE
# ============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""


def reset_input():
    st.session_state.user_input = ""


# ============================
# INPUT BOX
# ============================
user_input = st.text_input(
    "Ask something:",
    key="user_input",
    placeholder="Type here...",
)

# ============================
# HANDLE MESSAGE
# ============================
if user_input and user_input.strip():
    user_msg = user_input.strip()

    st.session_state.chat_history.append(("You", user_msg))

    try:
        if chat_session is None:
            st.error("Chat session not initialized. Please check the model configuration.")
        else:
            with st.spinner("Thinking..."):
                response = chat_session.send_message(user_msg)
                bot_reply = response.text
            
            st.session_state.chat_history.append(("Bot", bot_reply))
            
            # Reset input after successful processing
            reset_input()
            
    except Exception as e:
        error_msg = f"⚠️ Error: {str(e)}"
        st.session_state.chat_history.append(("Bot", error_msg))
        st.error(f"Detailed error: {e}")
        reset_input()


# ============================
# DISPLAY CHAT
# ============================
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")

# Add a clear button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
