import os
from pathlib import Path

import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def find_pdf_path():
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir / "CD.pdf",
        Path.cwd() / "CD.pdf",
        Path.home() / "Downloads" / "ai bot" / "CD.pdf",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return base_dir / "CD.pdf"


# extract text from pdf
def extract_text_from_pdf():
    pdf_path = find_pdf_path()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()

    return text


# ask question

def ask_question(query, full_text, model="llama3.2"):
    try:
        context = full_text[:30000]

        prompt = f"""
You are a helpful assistant that answers questions from a PDF.

PDF content:
{context}

Question: {query}
"""

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=60,
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ollama request failed: {response.text}")

        payload = response.json()
        return payload["message"]["content"]

    except Exception as e:
        return (
            "Error: Unable to reach Ollama on http://localhost:11434. "
            "Please make sure Ollama is running and the model is installed. "
            f"Details: {e}"
        )


# MAIN EXECUTION
if __name__ == "__main__":
    try:
        print("Reading PDF...")
        full_text = extract_text_from_pdf()
    except FileNotFoundError as exc:
        print(exc)
        raise SystemExit(1)

    if not full_text.strip():
        print("No text found in the PDF.")
        raise SystemExit(1)

    print("\nReady to chat! Type your question below. Type 'exit' or 'quit' to end.")

    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break

        answer = ask_question(query, full_text)
        print("Chatbot:", answer)

