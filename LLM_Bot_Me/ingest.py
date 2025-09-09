import os
import chromadb
import pdfplumber
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer

CHUNK_SIZE_WORDS = 200
COLLECTION_NAME = "portfolio"

client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_or_create_collection(COLLECTION_NAME)

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBED_MODEL)

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_html(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style"]):
        s.decompose()
    return soup.get_text(separator="\n")

def chunk_text(text, size=CHUNK_SIZE_WORDS):
    words = text.split()
    return [" ".join(words[i:i+size]).strip() for i in range(0, len(words), size)]

def ingest(corpus_dir="corpus"):
    for fname in os.listdir(corpus_dir):
        path = os.path.join(corpus_dir, fname)
        if not os.path.isfile(path):
            continue

        ext = fname.lower().split(".")[-1]
        if ext == "pdf":
            text = extract_text_from_pdf(path)
        elif ext in ("html", "htm"):
            text = extract_text_from_html(path)
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

        chunks = chunk_text(text)
        if not chunks:
            continue

        embeddings = embedder.encode(chunks).tolist()
        ids = [f"{fname}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": fname} for _ in chunks]

        col.add(documents=chunks, metadatas=metadatas, ids=ids, embeddings=embeddings)
        print(f"Ingested {len(chunks)} chunks from {fname}")

if __name__ == "__main__":
    ingest()
