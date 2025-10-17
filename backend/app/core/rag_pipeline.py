from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.langchain_utils import embeddings

def generate_routine_embeddings(routines: list):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.create_documents([r["title"] + " " + r["description"] for r in routines])
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore
