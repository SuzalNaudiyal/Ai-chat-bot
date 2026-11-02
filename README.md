# PDF AI Chat

A local PDF question-answering chatbot with a Streamlit web interface and an optional terminal interface. It uses Ollama for local AI responses.

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com/download) with the `llama3.2` model

## Setup

From this directory, install the Python packages:

```bash
python3 -m pip install -r requirements.txt
```

Install and start Ollama, then download the model:

```bash
ollama pull llama3.2
ollama serve
```

## Run the web app

In another terminal, run:

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501). Upload a PDF in the sidebar, or place `CD.pdf` next to `main.py` to load it automatically.

## Run the terminal version

```bash
python3 main.py
```

The local PDF and environment files are intentionally excluded from Git.
