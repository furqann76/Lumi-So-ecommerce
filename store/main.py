from fastapi import FastAPI
from pydantic import BaseModel
import fitz
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import requests
from fastapi.middleware.cors import CORSMiddleware

# Config
PDF_PATH = "LumiSo_FAQ_and_Policies.pdf"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
LLAMA_MODEL_NAME = "llama3"
LLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama default endpoint

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with Django frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load PDF
def read_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# Chunk text
def split_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


# Prepare embeddings and FAISS index once at startup
text = read_pdf(PDF_PATH)
chunks = split_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chunk_vectors = embedder.encode(chunks)
dimension = chunk_vectors.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(np.array(chunk_vectors))


# Request schema
class Query(BaseModel):
    question: str


# Local LLaMA completion via Ollama or similar
def query_llama(context, question):
    prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}
Answer:"""

    data = {
        "model": LLAMA_MODEL_NAME,
        "prompt": prompt,
        "stream": False,  # Important for FastAPI to handle the response easily
    }

    response = requests.post(LLAMA_API_URL, json=data)
    response.raise_for_status()
    return response.json()["response"]


# FastAPI endpoint
@app.post("/ask")
async def ask_question(q: Query):
    question_vector = embedder.encode([q.question])
    D, I = faiss_index.search(np.array(question_vector), k=3)
    relevant_chunks = "\n\n".join([chunks[i] for i in I[0]])
    answer = query_llama(relevant_chunks, q.question)
    return {"question": q.question, "answer": answer}
