import os
import json
import re
import math
import itertools
import logging
from pathlib import Path
from typing import List, Tuple

import chromadb
from chromadb.config import Settings
import pdfplumber
from bs4 import BeautifulSoup

import torch
from transformers import AutoTokenizer, AutoModel

# Optional: BM25 hybrid search
try:
    from rank_bm25 import BM25Okapi
    HAS_BM25 = True
except Exception:
    HAS_BM25 = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# ---------------- Config ----------------
CORPUS_DIR = "corpus"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "portfolio"

# Embedding model (local HF ID)
EMBED_MODEL = "google/embeddinggemma-300m"

# Chunking params
CHUNK_SENTENCES = 3           # number of sentences per chunk (sliding window)
CHUNK_SENTENCE_STEP = 1       # step in sentences (overlap = CHUNK_SENTENCES - step)
MAX_CHUNK_WORDS = 250         # hard max words per chunk (truncate if larger)
BATCH_SIZE = 16               # embedding batch size

# Priorities for files (you can tune)
PRIORITY_FILES = {
    "question_reponse.txt": 2.5,
    "edgardo_profile.txt": 1.5,
    "edgardo_informel.txt": 1.5,
}
DEFAULT_PRIORITY = 1.0

# Duplicate lexical mappings to improve recall (ex: C# -> C sharp)
LEXICAL_SYNONYMS = [
    ("C#", "C sharp"),
    ("C++", "C plus plus"),
    ("JS ", "JavaScript "),
]

# Output file for BM25 (optional)
BM25_META_FILE = "./bm25_index.json"

# ------------------ Chroma client ------------------
# use PersistentClient to keep DB on disk (ensure matching chroma version)
client = chromadb.PersistentClient(path=CHROMA_DIR)

# create or reset collection
def get_or_reset_collection(name: str, reset: bool = False):
    try:
        if reset:
            try:
                client.delete_collection(name)
                logging.info(f"Deleted existing collection '{name}'")
            except Exception:
                pass
        col = client.get_or_create_collection(name)
        logging.info(f"Using collection '{name}'")
        return col
    except Exception as e:
        logging.error("Error creating/getting Chroma collection: %s", e)
        raise

col = get_or_reset_collection(COLLECTION_NAME, reset=False)

# -------------- Embedding model (transformers) --------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logging.info(f"Loading embedding model {EMBED_MODEL} on {device}")
tokenizer = AutoTokenizer.from_pretrained(EMBED_MODEL)
model = AutoModel.from_pretrained(EMBED_MODEL).to(device)
model.eval()

def batch_embed_texts(texts: List[str], batch_size: int = BATCH_SIZE) -> List[List[float]]:
    """Compute embeddings in batches. Pool by mean of last_hidden_state."""
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        # tokenize (truncation) - adjust max_length if needed
        encoded = tokenizer(batch, padding=True, truncation=True, return_tensors="pt", max_length=1024).to(device)
        with torch.no_grad():
            out = model(**encoded)
            last_hidden = out.last_hidden_state  # (batch, seq_len, dim)
            # simple mean pooling (mask-aware)
            if encoded.get("attention_mask") is not None:
                mask = encoded["attention_mask"].unsqueeze(-1)  # (batch, seq_len, 1)
                summed = (last_hidden * mask).sum(dim=1)
                denom = mask.sum(dim=1).clamp(min=1e-9)
                vecs = (summed / denom).cpu().numpy()
            else:
                vecs = last_hidden.mean(dim=1).cpu().numpy()
        embeddings.extend(vecs.tolist())
    return embeddings

# -------------- Text extraction utilities --------------
def extract_text_from_pdf(path: str) -> str:
    out = []
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            t = p.extract_text()
            if t:
                out.append(t)
    return "\n".join(out)

def extract_text_from_html(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style"]):
        s.decompose()
    return soup.get_text(separator="\n")

# simple sentence splitter (regex). Not perfect but fast/no-deps.
_SENT_SPLIT_RE = re.compile(r'(?<=[.!?…])\s+')

def sentence_split(text: str) -> List[str]:
    text = text.strip().replace("\r\n", " ").replace("\n", " ")
    # collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    sents = [s.strip() for s in _SENT_SPLIT_RE.split(text) if s.strip()]
    if not sents:
        # fallback: split by dots
        sents = [p.strip() for p in text.split(".") if p.strip()]
    return sents

def make_chunks_from_sentences(sentences: List[str], chunk_sents=CHUNK_SENTENCES, step=CHUNK_SENTENCE_STEP) -> List[str]:
    chunks = []
    n = len(sentences)
    for start in range(0, max(1, n), step):
        group = sentences[start:start+chunk_sents]
        if not group:
            continue
        chunk = " ".join(group).strip()
        # enforce max words
        words = chunk.split()
        if len(words) > MAX_CHUNK_WORDS:
            chunk = " ".join(words[:MAX_CHUNK_WORDS])
        chunks.append(chunk)
        if start+chunk_sents >= n:
            break
    return chunks

def normalize_text_simple(s: str) -> str:
    if s is None:
        return ""
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    # remplace plusieurs espaces / tab / sauts de ligne par un seul espace
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def normalize_question(q: str) -> str:
    q = q.strip()
    # supprime les préfixes usuels
    q = re.sub(r'^(?:\?+\s*|Q[:\-]\s*|Question[:\-]\s*)', '', q, flags=re.I)
    q = normalize_text_simple(q)
    # si la question ne finit pas par '?', on peut laisser comme ça (utile pour matching)
    return q

def normalize_answer(a: str) -> str:
    a = a.strip()
    a = re.sub(r'^(?:A[:\-]\s*|Réponse[:\-]\s*|Answer[:\-]\s*)', '', a, flags=re.I)
    a = normalize_text_simple(a)
    return a

def ingest_qa_with_questions_lines(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    # unify newlines and trim leading/trailing whitespace
    raw = raw.replace("\r\n", "\n").replace("\r", "\n").strip()

    # split into logical blocks separated by at least one blank line
    blocks = re.split(r'\n\s*\n', raw)
    chunks = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Case 1: explicit Q: / A: pairs inside block -> parse them
        m_q = re.search(r'(?im)^(?:q[:\-]\s*)?(.*?)(?=\n(?:a[:\-]|réponse[:\-])|\Z)', block)
        m_a = re.search(r'(?im)(?:a[:\-]\s*|réponse[:\-]\s*)(.*)$', block, flags=re.S)
        if m_q and m_a:
            q_raw = m_q.group(1).strip()
            a_raw = m_a.group(1).strip()
            qn = normalize_question(q_raw)
            an = normalize_answer(a_raw)
            if qn and an:
                chunks.append(f"Q: {qn}\nA: {an}")
            continue

        # Case 2: block is multiple lines, find lines starting with ? or Q: or 'Question'
        lines = [ln.strip() for ln in block.splitlines() if ln.strip() != ""]
        i = 0
        while i < len(lines):
            line = lines[i]
            # If it starts with ? or Q: treat as question
            if line.startswith("?") or re.match(r'^(?:q[:\-]|question\b)', line, flags=re.I):
                q_raw = re.sub(r'^[\?]+\s*', '', line)
                q_raw = re.sub(r'^(?:q[:\-]\s*|question[:\-]\s*)', '', q_raw, flags=re.I).strip()
                # answer is next non-empty line if exists
                a_raw = lines[i+1] if i+1 < len(lines) else ""
                qn = normalize_question(q_raw)
                an = normalize_answer(a_raw)
                if qn and an:
                    chunks.append(f"Q: {qn}\nA: {an}")
                i += 2
                continue
            # Otherwise, heuristic: pair current line with next line
            if i+1 < len(lines):
                q_raw = line
                a_raw = lines[i+1]
                qn = normalize_question(q_raw)
                an = normalize_answer(a_raw)
                if qn and an:
                    chunks.append(f"Q: {qn}\nA: {an}")
                i += 2
            else:
                # orphan single line at end -> ignore
                i += 1

    return chunks

def ingest_qa_answers_only(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    # split by double newlines as sections
    parts = [p.strip() for p in re.split(r'\n\s*\n', raw) if p.strip()]
    chunks = []
    for p in parts:
        # create a synthetic Q using first 6 words
        first_words = " ".join(p.split()[:6])
        q = f"Q: ? about {first_words}..."
        a = p.replace("\n", " ")
        chunks.append(f"{q}\nA: {a}")
    return chunks

def ingest_qa_file(path: str) -> List[str]:
    """Auto-detect QA format and return list of Q/A chunks."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    # quick detection: presence of lines starting with '?'
    if re.search(r'(?m)^\s*\?', raw) or re.search(r'(?im)^\s*q\s*[:\-]', raw):
        return ingest_qa_with_questions_lines(path)
    # fallback: if many blank-line separated paragraphs, treat as answers-only
    paragraphs = [p for p in re.split(r'\n\s*\n', raw) if p.strip()]
    if len(paragraphs) >= 3:
        return ingest_qa_answers_only(path)
    # final fallback: split into sentence-chunks
    sents = sentence_split(raw)
    return make_chunks_from_sentences(sents)

# -------------- general file ingestion to chunks --------------
def text_file_to_chunks(text: str) -> List[str]:
    # split into paragraphs (blank-line), if paragraphs short -> sentence sliding window
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    chunks = []
    if not paragraphs:
        # fallback to sentences
        sents = sentence_split(text)
        chunks = make_chunks_from_sentences(sents)
    else:
        for p in paragraphs:
            # if paragraph short -> sentence chunks
            if len(p.split()) <= MAX_CHUNK_WORDS:
                sents = sentence_split(p)
                if len(sents) <= CHUNK_SENTENCES:
                    chunks.append(p.strip())
                else:
                    chunks.extend(make_chunks_from_sentences(sents))
            else:
                # large paragraph -> sentence sliding window
                sents = sentence_split(p)
                chunks.extend(make_chunks_from_sentences(sents))
    # final cleaning: remove duplicates and very short chunks
    final = []
    seen = set()
    for c in chunks:
        c = re.sub(r'\s+', ' ', c).strip()
        if len(c.split()) < 3:
            continue
        if c in seen:
            continue
        seen.add(c)
        final.append(c)
    return final

# -------------- lexical synonym duplication --------------
def duplicate_with_synonyms(chunks: List[str]) -> List[str]:
    """For each chunk, optionally add a synonym-variant to improve lexical recall."""
    out = []
    for c in chunks:
        out.append(c)
        for a, b in LEXICAL_SYNONYMS:
            if a in c and b not in c:
                out.append(c.replace(a, b))
    return out

# -------------- BM25 index builder (optional) --------------
def build_bm25_index(all_chunks: List[str], meta_list: List[dict], dump_path: str = BM25_META_FILE):
    if not HAS_BM25:
        logging.warning("rank_bm25 not installed; skipping BM25 build.")
        return None
    tokenized = [c.split() for c in all_chunks]
    bm25 = BM25Okapi(tokenized)
    # store small metadata mapping for later hybrid query
    meta_dump = {
        "chunks": all_chunks,
        "metas": meta_list
    }
    with open(dump_path, "w", encoding="utf-8") as f:
        json.dump(meta_dump, f, ensure_ascii=False, indent=2)
    logging.info(f"BM25 index saved to {dump_path}")
    return bm25

# -------------- Main ingestion loop --------------
def ingest(corpus_dir: str = CORPUS_DIR, reset_collection: bool = False):
    col_local = get_or_reset_collection(COLLECTION_NAME, reset=reset_collection)

    all_chunks = []
    all_metas = []
    all_ids = []
    log_counts = {}

    for fname in sorted(os.listdir(corpus_dir)):
        path = os.path.join(corpus_dir, fname)
        if not os.path.isfile(path):
            continue
        logging.info(f"Processing file: {fname}")
        ext = fname.lower().split(".")[-1]

        # extract plain text
        if ext == "pdf":
            text = extract_text_from_pdf(path)
        elif ext in ("html", "htm"):
            text = extract_text_from_html(path)
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

        # choose ingestion method
        chunks = []
        if "question_reponse" in fname.lower() or "qa" in fname.lower():
            chunks = ingest_qa_file(path)
            logging.info(f"Detected QA file. QA chunks: {len(chunks)}")
        else:
            chunks = text_file_to_chunks(text)
            logging.info(f"Generated {len(chunks)} chunks from text")

        if not chunks:
            logging.warning(f"No chunks for file {fname}, skipping.")
            continue

        # optionally duplicate synonyms to help recall for tokens like C#
        chunks = duplicate_with_synonyms(chunks)

        # prepare ids/metas
        ids = [f"{fname}_{i}" for i in range(len(chunks))]
        priority_value = PRIORITY_FILES.get(fname, DEFAULT_PRIORITY)
        metas = [{"source": fname, "priority": priority_value, "chunk_index": i, "len_words": len(chunks[i].split())} for i in range(len(chunks))]

        # compute embeddings in batches
        logging.info(f"Embedding {len(chunks)} chunks from {fname} (model={EMBED_MODEL})")
        embeddings = batch_embed_texts(chunks, batch_size=BATCH_SIZE)

        # add to chroma
        try:
            col_local.add(documents=chunks, metadatas=metas, ids=ids, embeddings=embeddings)
            logging.info(f"Added {len(chunks)} chunks from {fname} to Chroma.")
        except Exception as e:
            logging.exception("Failed to add to Chroma: %s", e)
            raise

        # accumulate for BM25
        all_chunks.extend(chunks)
        all_metas.extend(metas)
        all_ids.extend(ids)
        log_counts[fname] = len(chunks)

    # after loop: optional BM25
    if HAS_BM25 and all_chunks:
        logging.info("Building BM25 index for hybrid search...")
        bm25 = build_bm25_index(all_chunks, all_metas)
    else:
        bm25 = None

    logging.info("Ingestion summary:")
    for k, v in log_counts.items():
        logging.info(f" - {k}: {v} chunks")
    logging.info(f"Total chunks ingested: {len(all_chunks)}")

    return {
        "total_chunks": len(all_chunks),
        "ids": all_ids,
        "bm25": bm25
    }

if __name__ == "__main__":
    # Reset collection flag -> change to True if you want to start fresh
    res = ingest(corpus_dir=CORPUS_DIR, reset_collection=False)
    logging.info("Done ingest. stats: %s", {k: v for k, v in res.items() if k != "bm25"})
