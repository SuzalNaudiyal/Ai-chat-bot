import io
from pathlib import Path

import fitz
import streamlit as st

from main import ask_question, extract_text_from_pdf


st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #1f2937 100%);
            color: #e5e7eb;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stChatMessage {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 1rem 1.2rem;
        }
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(15, 23, 42, 0.8);
            color: #fff;
        }
        .stButton > button {
            border-radius: 12px;
            background: linear-gradient(90deg, #8b5cf6, #3b82f6);
            color: white;
            border: none;
            font-weight: 600;
        }
        .sidebar .block-container {
            background: rgba(15, 23, 42, 0.7);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def get_default_pdf_text():
    return extract_text_from_pdf()


def extract_text_from_uploaded_file(uploaded_file):
    file_bytes = uploaded_file.read()
    pdf_bytes = io.BytesIO(file_bytes)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "".join(page.get_text() for page in doc)
    return text


with st.sidebar:
    st.title("📄 PDF AI Assistant")
    st.caption("Ask questions about your PDF in a modern chat app.")

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file is not None:
        st.session_state["pdf_text"] = extract_text_from_uploaded_file(uploaded_file)
        st.session_state["pdf_name"] = uploaded_file.name
        st.success(f"Loaded: {uploaded_file.name}")

    if "pdf_text" not in st.session_state:
        try:
            st.session_state["pdf_text"] = get_default_pdf_text()
            st.session_state["pdf_name"] = "CD.pdf"
        except Exception as exc:
            st.session_state["pdf_name"] = "No PDF found"
            st.error(f"Could not read the default PDF: {exc}")

    st.markdown(f"**Current document:** {st.session_state['pdf_name']}")
    if st.button("Reload default PDF"):
        try:
            st.session_state["pdf_text"] = get_default_pdf_text()
            st.session_state["pdf_name"] = "CD.pdf"
            st.rerun()
        except Exception as exc:
            st.error(f"Reload failed: {exc}")


st.title("AI PDF Chat")
st.caption("Ask anything about your document and get answers from the PDF content.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me a question about the PDF."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about the PDF...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        answer = ask_question(prompt, st.session_state["pdf_text"])

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
