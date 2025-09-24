from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from .config import setup_cors

class ChatMessage(BaseModel):
    id: str
    role: str
    content: str

class ChatInput(BaseModel):
    messages: list[ChatMessage]

CHROMA_DIR = "chroma_db"

app = FastAPI()
setup_cors(app)
load_dotenv(".env.local")

# load persisted Chroma DB
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

# Retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 3}) # top 3 relevant docs

# Prompt
prompt = """
    You are Siwan's personal assistant bot. 
    Use the context below to answer the question concisely. 
    If the answer is not in the context, say you don't have enough information.
    Always answer in a friendly manner."""

llm = ChatOllama(model="gemma3", 
                 temperature=0.7)

@app.post("/api/chat")
async def chat(data: ChatInput):
    """
    Chat endpoint
    - Recieves a message
    - Retrieves relevant information from vector DB
    - Sends prompt + context + message to LLM
    - streams Ollama response back to the frontend
    """
    user_msg = data.messages[-1].content

    # Retrieve relevant information from vector DB
    docs = retriever.get_relevant_documents(user_msg)
    context = "\n\n".join([d.page_content for d in docs])

    # Final Prompt for LLM
    query = f"""
    {prompt}

    Context:
    {context}

    User: {user_msg}
    """

    async def generate():
        async for chunk in llm.astream([HumanMessage(query)]):
            if chunk.content:
                yield chunk.content

    return StreamingResponse(generate(), media_type="text/plain")