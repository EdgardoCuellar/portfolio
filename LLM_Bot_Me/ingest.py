import os
import chromadb
import pdfplumber
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import re

CHUNK_SIZE_WORDS = 200
COLLECTION_NAME = "portfolio"

client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_or_create_collection(COLLECTION_NAME)

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBED_MODEL)

PRIORITY_FILES = {
    "edgardo_profile.txt": 2.0,         
    "edgardo_question_reponse.txt": 2.0,
    "edgardo_informel.txt": 1.5,
}
DEFAULT_PRIORITY = 1.0


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

def ingest_qa_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # Suppose format: each Q line ends with '?' and answer follows until next question
    pattern = re.compile(r"(?m)(^.*\?.*?$)(.*?)(?=^.*\?.*?$|\Z)", re.DOTALL)
    matches = pattern.findall(text)
    qa_chunks = []
    for qline, ans in matches:
        qline_clean = qline.strip()
        ans_clean = ans.strip()
        if qline_clean and ans_clean:
            # store as chunk like "Q: ...\nA: ..."
            qa_chunks.append(f"Q: {qline_clean}\nA: {ans_clean}")
    return qa_chunks

def ingest(corpus_dir="corpus"):
    for fname in os.listdir(corpus_dir):
        path = os.path.join(corpus_dir, fname)
        if not os.path.isfile(path):
            continue

        ext = fname.lower().split(".")[-1]
        
        if ext == "txt" and "question_reponse" in fname:
            chunks = ingest_qa_file(path)
        else:
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
        priority_value = PRIORITY_FILES.get(fname, DEFAULT_PRIORITY)
        metadatas = [{"source": fname, "priority": priority_value} for _ in chunks]

        col.add(documents=chunks, metadatas=metadatas, ids=ids, embeddings=embeddings)
        print(f"Ingested {len(chunks)} chunks from {fname}")

if __name__ == "__main__":
    ingest()
