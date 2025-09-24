# Personal Assistant Chatbot
A full-stack chatbot that answers questions about ME! (Siwan) using **Next.js (frontend), FastAPI (backend), and LangChain + Chroma (RAG with Markdown data)**.

## Features
* Chat UI built with Next.js + React
* Real-time Streaming responses
* FastAPI backend connected to Ollama LLM (Model: Gemma3)
* RAG: Chatbot answers based on markdown files 
* Fast semantic vector search

## Structure
```
personal-assistant/
├── api/                # FastAPI backend
│   ├── index.py        # /api/chat endpoint
│   └── config.py       # CORS setup
├── data/               # Personal knowledge base (markdown files)
│   ├── personal_info.md
│   ├── resume.md
│   └── fun_facts.md
├── scripts/
│   └── build_db.py     # build Chroma DB from markdown
├── chroma_db/          # generated vector DB (ignored in git)
├── frontend/ (or app/) # Next.js frontend
└── README.md
```

## Setup
1. Clone the repo

```
git clone https://github.com/your-username/personal-assistant.git
cd personal-assistant
```

2. Install Dependencies
** Backend **
```
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

** Frontend **
```
npm install
```

3. Environment variables
Create `.env.local` in project root:

```
OPENAI_API_KEY=sk-your-openai-key
```

## Usage
1. Build Vector DB

Whenever you update `data/*.md`, rebuild embeddings:
```
python scripts/build_db.py
```
2. Run Frontend & Backend Concurrently
```
npm run dev
```