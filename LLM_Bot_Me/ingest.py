# ingest.py
import os
from sentence_transformers import SentenceTransformer
import chromadb
import pdfplumber
from bs4 import BeautifulSoup

# Use a small, fast embedding model for local CPU embeddings
EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE_WORDS = 200
COLLECTION_NAME = "portfolio"

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_html(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    # remove scripts/styles
    for s in soup(["script", "style"]):
        s.decompose()
    text = soup.get_text(separator="\n")
    return text

def chunk_text(text, size=CHUNK_SIZE_WORDS):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i+size]).strip()
        if chunk:
            chunks.append(chunk)
    return chunks

def ingest(corpus_dir="corpus"):
    # load embedder
    embedder = SentenceTransformer(EMBED_MODEL)

    # chroma client
    client = chromadb.Client()
    # create or get collection
    try:
        col = client.get_collection(COLLECTION_NAME)
    except Exception:
        col = client.create_collection(COLLECTION_NAME)

    # iterate files in corpus
    for fname in sorted(os.listdir(corpus_dir)):
        path = os.path.join(corpus_dir, fname)
        if not os.path.isfile(path):
            continue
        ext = fname.lower().split(".")[-1]
        try:
            if ext == "pdf":
                text = extract_text_from_pdf(path)
            elif ext in ("html", "htm"):
                text = extract_text_from_html(path)
            else:  # txt, md, etc.
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
        except Exception as e:
            print(f"Failed to read {fname}: {e}")
            continue

        chunks = chunk_text(text)
        if not chunks:
            print(f"No chunks extracted from {fname}, skipping.")
            continue

        # compute embeddings
        embeddings = embedder.encode(chunks).tolist()

        # prepare ids / metadata
        ids = [f"{fname}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": fname} for _ in chunks]

        # add to chroma collection
        try:
            col.add(documents=chunks, metadatas=metadatas, ids=ids, embeddings=embeddings)
            print(f"Ingested {len(chunks)} chunks from {fname}")
        except Exception as e:
            print(f"Error adding chunks from {fname} to collection: {e}")

if __name__ == "__main__":
    corpus_dir = os.getenv("CORPUS_DIR", "corpus")
    if not os.path.isdir(corpus_dir):
        print(f"Corpus directory '{corpus_dir}' not found. Create it and add files (txt/pdf/html).")
    else:
        ingest(corpus_dir=corpus_dir)
