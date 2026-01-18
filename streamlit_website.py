import streamlit as st
import tempfile
import os
import importlib
import sys

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Avengers Personality Matcher",
    page_icon="🦸‍♂️",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align:center;'>🦸‍♂️ Avengers Personality Matcher</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; font-size:18px;'>"
    "Upload a WhatsApp chat and see which Avenger each person resembles!"
    "</p>",
    unsafe_allow_html=True
)

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader(
    "📂 Upload WhatsApp Chat (.txt)",
    type=["txt"]
)

if uploaded_file is None:
    st.info("👆 Upload a WhatsApp chat file to begin")
    st.stop()

# -------------------------------
# SAVE FILE TEMPORARILY
# -------------------------------
with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
    tmp.write(uploaded_file.read())
    chat_path = tmp.name

# -------------------------------
# MAKE CHAT PATH VISIBLE TO BACKEND
# -------------------------------
# backend.py expects a variable called `chat_path`
# We inject it BEFORE importing backend

sys.modules["__main__"].chat_path = chat_path

# -------------------------------
# RUN BACKEND
# -------------------------------
with st.spinner("🧠 Analyzing chat personalities..."):
    backend = importlib.import_module("backend_main")
    importlib.reload(backend)

# -------------------------------
# DISPLAY RESULTS
# -------------------------------
st.markdown("## 🔮 Results")

emoji_map = {
    "tony stark": "🧠⚙️",
    "steve rogers": "🛡️",
    "thor": "⚡",
    "loki": "🐍",
    "natasha romanoff": "🕷️",
    "clint barton": "🏹",
    "bruce banner": "🧪",
    "hulk": "💥",
    "peter parker": "🕸️",
    "doctor strange": "🌀",
    "thanos": "🫰"
}

cols = st.columns(3)

for i, (person, hero) in enumerate(backend.dict_f.items()):
    with cols[i % 3]:
        emoji = emoji_map.get(hero, "🦸‍♂️")
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #1f1f1f, #2c2c2c);
                padding: 20px;
                border-radius: 15px;
                color: white;
                text-align: center;
                margin-bottom: 20px;
            ">
                <h3>{person}</h3>
                <h1>{emoji}</h1>
                <h2>{hero.title()}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------------
# CLEANUP
# -------------------------------
os.remove(chat_path)
