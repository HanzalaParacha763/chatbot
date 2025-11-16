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
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction=HUMANITIES_PROMPT
    )
    return model.start_chat()

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
st.text_input(
    "Ask something:",
    key="user_input",
    on_change=reset_input,
    placeholder="Type here...",
)


# ============================
# HANDLE MESSAGE
# ============================
if st.session_state.user_input.strip():
    user_msg = st.session_state.user_input.strip()

    st.session_state.chat_history.append(("You", user_msg))

    try:
        response = chat_session.send_message(user_msg)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    st.session_state.chat_history.append(("Bot", bot_reply))


# ============================
# DISPLAY CHAT
# ============================
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")
