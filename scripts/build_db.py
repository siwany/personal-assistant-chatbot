import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

DATA_DIR = "data"
CHROMA_DIR = "chroma_db"

load_dotenv(".env.local")

def build_vector_db():
    """
    Build a vector database from markdown files in the data directory
    and store it in the chroma_db directory.
    """
    docs = []
    # Create directories if they don't exist
    os.makedirs(CHROMA_DIR, exist_ok=True)

    # Load documents
    for file in os.listdir(DATA_DIR):
        if file.endswith(".md"):
            loader = UnstructuredMarkdownLoader(os.path.join(DATA_DIR, file))
            docs.extend([d.metadata.update({"source": file}) or d for d in loader.load()])

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, 
                                              chunk_overlap=200,
                                              separators=["\n# ", "\n## ", "\n**", "\n"])
    chunks = splitter.split_documents(docs)

    # Create embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large",)

    # Build Vector DB
    vectordb = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_DIR
        )
    print(f"Built vector DB with {len(chunks)} chunks, stored in {CHROMA_DIR}")

if __name__ == "__main__":
    build_vector_db()