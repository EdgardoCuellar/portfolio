from flask import Flask, request, jsonify, abort
from transformers import AutoTokenizer, AutoModel
import torch
import chromadb
import os
from openai import OpenAI
from flask_cors import CORS
import re
import time
import html
from typing import List, Dict
import unicodedata

# ---------- Config ----------
CHROMA_DIR = "./chroma_db"
COL_NAME = "portfolio"
EMBED_MODEL = "google/embeddinggemma-300m"
MODEL_NAME = os.getenv("MODEL_NAME", "qwen/qwen3-4b-2507")
LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://127.0.0.1:1234/v1")
API_TOKEN = os.getenv("API_TOKEN", "JUDO1205")

# ---------- Clients ----------
client = chromadb.PersistentClient(path=CHROMA_DIR)
try:
    col = client.get_collection(COL_NAME)
except Exception:
    col = client.get_or_create_collection(COL_NAME)

print("[App.py] Loading embedding model:", EMBED_MODEL)
tokenizer = AutoTokenizer.from_pretrained(EMBED_MODEL)
model = AutoModel.from_pretrained(EMBED_MODEL)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def embed_texts(texts):
    with torch.no_grad():
        encoded = tokenizer(texts, padding=True, truncation=True, return_tensors="pt").to(device)
        out = model(**encoded)
        emb = out.last_hidden_state.mean(dim=1)  # mean pooling
        return emb.cpu().numpy()

llm = OpenAI(base_url=LMSTUDIO_URL, api_key="lm-studio")

# ---------- Flask ----------
app = Flask(__name__)
CORS(app,
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "x-api-key"],
     methods=["GET", "POST", "OPTIONS"])

# ---------- System instructions (improved) ----------
SYSTEM_INSTRUCTIONS = (
    "You are an assistant that answers questions using ONLY the provided CONTEXT chunks.\n"
    "RULES (strict):\n"
    "1) Detect the user's language and answer in that language. If detection fails, default to French.\n"
    "2) Be concise: 2–5 sentences for factual answers.\n"
    "3) Do NOT mention, print or list any sources, filenames, or indices in the answer.\n"
    "4) Use ONLY information present in the provided CONTEXT. If the answer cannot be found in the context, reply exactly:\n"
    "\"I don't know based on my documents — please check the portfolio or ask me directly.\"\n"
    "5) Do not invent facts or numbers. If asked for an opinion, prefix with 'Opinion:'.\n"
    "6) Keep generation temperature low (0.0–0.2) to avoid hallucinations.\n"
    "7) Speak in first person for personal facts (e.g., 'I built...','I used...').\n"
)

# ---------- Utilities ----------
def distance_to_similarity(dist):
    if dist is None:
        return 0.0
    try:
        d = float(dist)
    except Exception:
        return 0.0
    return 1.0 / (1.0 + d)

def detect_language_simple(text: str) -> str:
    t = text.lower()
    words = re.findall(r"\b\w+\b", t)
    french_tokens = ["bonjour", "merci", "vous", "quel", "quelle", "francais", "français", "où", "est-ce", "je", "j'", "merci", "voyage", "pays"]
    for tok in french_tokens:
        if tok in words:
            return "fr"
    english_tokens = ["hi", "hello", "thank", "you", "are you", "what", "where", "do you", "i am", "i'm", "the"]
    for tok in english_tokens:
        if tok in words:
            return "en"
    return "fr"  # prefer French default (your preference)

# ---------- Multi-query (reformulations) ----------

def normalize_query(q: str) -> str:
    q = q.lower()
    q = q.replace("t'as", "tu as")
    q = q.replace("t as", "tu as")
    q = q.replace("quel age", "quel âge")
    q = unicodedata.normalize("NFKC", q)  # normalise accents/unicode
    return q

def synthetic_reformulations(query: str, n: int = 5) -> List[str]:
    q = normalize_query(query.strip())
    reforms = [q]
    reforms.append(q.replace("â", "a").replace("é", "e"))  # accentless variant
    reforms.append(re.sub(r"[^\w\s]", " ", q))  # punctuation removed
    if "c#" in q:
        reforms.append(q.replace("c#", "c sharp"))
    if len(q) > 6:
        i = len(q)//2
        reforms.append(q[:i] + q[i+1:])
    return list(dict.fromkeys(reforms))[:n]

def llm_reformulations(query: str, n: int = 3, timeout_s: int = 6) -> List[str]:
    """
    Optional: use the LLM to create paraphrases (slower). If the LLM fails quickly fallback to synthetic.
    """
    prompt = (
        "Create up to %d concise paraphrases of the following user question. "
        "Return each paraphrase on its own line. Keep meaning identical and keep language same as input.\n\n"
        "QUESTION:\n%s" % (n, query)
    )
    try:
        resp = llm.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            max_tokens=500,
            timeout=timeout_s
        )
        choices = getattr(resp, "choices", None) or resp.get("choices", None)
        if not choices:
            return synthetic_reformulations(query, n)
        text = ""
        first = choices[0]
        if hasattr(first, "message"):
            text = first.message.content
        elif isinstance(first, dict):
            text = first.get("message", {}).get("content") or first.get("text") or ""
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if not lines:
            return synthetic_reformulations(query, n)
        return lines[:n]
    except Exception as e:
        print("[llm_reformulations] error:", e)
        return synthetic_reformulations(query, n)

# ---------- Retrieval helper ----------
def retrieve_for_query(q: str, k: int = 60):
    q_emb = embed_texts([q])[0] 
    res = col.query(
        query_embeddings=[q_emb.tolist()], 
        n_results=k, 
        include=["documents", "metadatas", "distances"]
    )
    
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    
    items = []
    for doc, meta, dist in zip(docs, metas, dists):
        src = meta.get("source", "unknown") if isinstance(meta, dict) else "unknown"
        priority = meta.get("priority", 1.0) if isinstance(meta, dict) else 1.0
        sim = distance_to_similarity(dist)
        
        # Ajouter un bonus pour les correspondances exactes de mots-clés
        bonus = 0.0
        query_words = set(q.lower().split())
        doc_words = set(doc.lower().split())
        matching_words = query_words.intersection(doc_words)
        if matching_words:
            bonus = 0.1 * len(matching_words)  # Bonus de 0.1 par mot correspondant
        
        boosted = sim * float(priority) + bonus
        
        items.append({
            "chunk": doc,
            "source": src,
            "dist": dist,
            "sim": sim,
            "priority": float(priority),
            "boosted_sim": boosted
        })
    
    return items

# ---------- Reciprocal Rank Fusion (RRF) ----------
def rrf_combine(ranked_lists: List[List[Dict]], rrf_k: int = 60, top_n: int = 15):
    """
    Input: ranked_lists = list of lists of candidate dicts (ordered by relevance).
    Output: aggregated list of candidates sorted by RRF score.
    Implementation uses chunk text as key (should be stable).
    """
    scores = {}
    # for ranking purposes we'll iterate lists and add 1/(k+rank)
    for ranked in ranked_lists:
        for rank, item in enumerate(ranked, start=1):
            key = item.get("chunk", "")  # text as key
            scores.setdefault(key, 0.0)
            scores[key] += (1.0 / (rrf_k + rank)) * (1.0 + item["boosted_sim"] * 2.0)
            # keep best metadata snapshot
            if "_meta" not in item:
                item["_meta"] = {"source": item.get("source"), "sim": item.get("sim"), "boosted": item.get("boosted_sim")}
            # store representative item
            if "_repr" not in item:
                item["_repr"] = item
            # store last seen repr in dict for retrieval
            # we will retrieve repr using key later
    # sort by score
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    out = []
    for key, sc in sorted_items[:top_n]:
        # find a representative item from ranked_lists
        repr_item = None
        for lst in ranked_lists:
            for it in lst:
                if it.get("chunk", "") == key:
                    repr_item = it
                    break
            if repr_item:
                break
        if repr_item is None:
            repr_item = {"chunk": key, "source": "unknown", "sim": 0.0, "priority": 1.0, "boosted_sim": 0.0}
        repr_item["rrf_score"] = sc
        out.append(repr_item)
    return out

# ---------- Reranker prompt (more explicit) ----------
def build_rerank_prompt(question: str, candidates: List[Dict], top_n: int = 3):
    """
    Instruct the LLM to focus only on relevance to the question (not on grammar/format).
    Return indices only.
    """
    chunks_text = []
    for i, c in enumerate(candidates, start=1):
        snippet = c.get("chunk", "")
        snippet = snippet if len(snippet) < 1500 else snippet[:1500] + "..."
        chunks_text.append(f"[{i}] {snippet}")
    instr = (
        "You are a strict relevance re-ranker. GIVEN the user QUESTION, rank the candidates purely by how well "
        "each candidate answers or contains the factual information requested. DO NOT judge style, grammar, or verbosity. "
        "Prefer candidates that contain explicit factual answers or direct statements related to the question.\n\n"
        f"QUESTION:\n{question}\n\nCANDIDATES:\n" + "\n\n".join(chunks_text) + f"\n\nReturn the indices of the top {top_n} candidates in a single line, highest relevance first, like: 3,1,5\n"
    )
    return instr

def rerank_candidates(question: str, candidates: List[Dict], top_n: int = 3):
    if not candidates:
        return []
    prompt = build_rerank_prompt(question, candidates, top_n=top_n)
    try:
        resp = llm.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role":"user","content":prompt}],
            temperature=0.0,
            max_tokens=80,
        )
        text = resp.choices[0].message.content if hasattr(resp.choices[0], "message") else ""
        nums = re.findall(r"\d+", text)
        indices = [int(n) for n in nums][:top_n]
        ranked = [candidates[i-1] for i in indices if 1 <= i <= len(candidates)]
        if ranked:
            return ranked
    except Exception as e:
        print("[rerank_candidates] LLM rerank failed:", e)

    # Fallback: tri par boosted_sim décroissant
    print("[rerank_candidates] fallback -> boosted_sim")
    return sorted(candidates, key=lambda x: x["boosted_sim"], reverse=True)[:top_n]


# ---------- Build final prompt to answer ----------
def build_answer_prompt(question: str, contexts: List[Dict], lang: str):
    # contexts: list of dicts with 'chunk'
    ctx_texts = []
    for i, c in enumerate(contexts, start=1):
        chunk = c.get("chunk", "")
        chunk = chunk if len(chunk) < 2500 else chunk[:2500] + "..."
        ctx_texts.append(f"[{i}] {chunk}")
    ctx_block = "\n\n---\n\n".join(ctx_texts)
    lang_instr = "Réponds en français." if lang == "fr" else "Answer in English."
    prompt = (
        f"{SYSTEM_INSTRUCTIONS}\n\n{lang_instr}\n\nCONTEXT:\n{ctx_block}\n\nQUESTION: {question}\n\n"
    )
    return prompt

def ask_llm(prompt_user: str, max_tokens: int = 400, temp: float = 0.1):
    try:
        response = llm.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role":"system","content":SYSTEM_INSTRUCTIONS},
                      {"role":"user","content":prompt_user}],
            max_tokens=max_tokens,
            temperature=temp,
        )
        choices = getattr(response, "choices", None) or response.get("choices", None)
        if choices:
            first = choices[0]
            if hasattr(first, "message") and getattr(first.message, "content", None):
                return first.message.content.strip()
            if isinstance(first, dict):
                return first.get("message", {}).get("content") or first.get("text") or str(first)
        return str(response)
    except Exception as e:
        print("[ask_llm] error:", e)
        return f"Error calling LLM: {e}"

# ---------- Main QA endpoint ----------
@app.route("/qa", methods=["POST"])
def qa():
    token = request.headers.get("x-api-key") or request.args.get("api_key")
    if token != API_TOKEN:
        abort(401)
    data = request.json or {}
    q = data.get("question", "").strip()
    use_llm_reforms = data.get("use_llm_reforms", False)  # optional flag
    if not q:
        return jsonify({"error": "No question provided"}), 400

    lang = detect_language_simple(q)
    start = time.time()

    # 1) multi-query generation
    reforms = synthetic_reformulations(q, n=5)
    if use_llm_reforms:
        try:
            llm_reforms = llm_reformulations(q, n=3)
            for r in llm_reforms:
                if r not in reforms:
                    reforms.append(r)
        except Exception:
            pass
    print("[multi-query] reformulations:", reforms)

    # 2) retrieve for each reformulation
    ranked_lists = []
    for r in reforms:
        items = retrieve_for_query(r, k=100)
        for item in items:
            if item["sim"] < 0.05:
                # Réduire l'impact des items peu similaires sans les exclure complètement
                item["boosted_sim"] *= 0.3  # Réduction du poids
        
        items_sorted = sorted(items, key=lambda x: x["boosted_sim"], reverse=True)
        ranked_lists.append(items_sorted)
    print(f"[retrieve] got {len(ranked_lists)} lists (k=100)")

    # 3) aggregate with RRF
    rrf_results = rrf_combine(ranked_lists, rrf_k=60, top_n=12)
    print("[rrf] top results preview:")
    for i, it in enumerate(rrf_results[:6], start=1):
        print(f"  {i}. {it.get('source')} rrf={it.get('rrf_score'):.4f} boosted={it.get('boosted_sim'):.3f}")

    # 4) rerank top candidates using LLM focused on relevance
    top_for_rerank = rrf_results[:24]  
    top_after_rerank = rerank_candidates(q, top_for_rerank, top_n=6)

    print("[top_after_rerank] chosen chunks:")
    for i, it in enumerate(top_after_rerank, start=1):
        print(f"  {i}. source={it.get('source')} sim={it.get('sim'):.3f} boosted={it.get('boosted_sim'):.3f}")

    # 5) build answer prompt and call LLM
    prompt = build_answer_prompt(q, top_after_rerank, lang)
    print(f"[/qa] Prompt length: {len(prompt)} chars")
    # optional debug: print prompt prefix
    print(f"[/qa] Prompt preview:\n{prompt}\n--- end prompt preview ---\n")

    answer = ask_llm(prompt, max_tokens=2048, temp=0.1)
    elapsed = time.time() - start
    print(f"[/qa] Completed in {elapsed:.2f}s")

    # return only the answer (no sources shown to frontend)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
