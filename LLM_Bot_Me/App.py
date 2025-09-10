# App.py (corrected & robust)
from flask import Flask, request, jsonify, abort
from sentence_transformers import SentenceTransformer
import chromadb
import os
from openai import OpenAI
from flask_cors import CORS
import re

# ---------- Chroma client (Persistent) ----------
client = chromadb.PersistentClient(path="./chroma_db")
# get or create collection safely
COL_NAME = "portfolio"
try:
    col = client.get_collection(COL_NAME)
except Exception:
    col = client.get_or_create_collection(COL_NAME)

# ---------- Embeddings model ----------
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
embed = SentenceTransformer(EMBED_MODEL)

# ---------- LM Studio client (OpenAI-compatible) ----------
llm = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
MODEL_NAME = os.getenv("MODEL_NAME", "liquid/lfm2-1.2b")

# ---------- Flask app ----------
app = Flask(__name__)

CORS(app,
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "x-api-key"],
     methods=["GET", "POST", "OPTIONS"])

API_TOKEN = os.getenv("API_TOKEN", "JUDO1205")

with open("prompts/analysis_system.txt", "r", encoding="utf-8") as f:
    SYSTEM_INSTRUCTIONS = f.read().strip()

# -----------------------
# Utilities
# -----------------------
def distance_to_similarity(dist):
    if dist is None:
        return 0.0
    try:
        d = float(dist)
    except Exception:
        return 0.0
    if 0.0 <= d <= 2.0:
        return max(0.0, 1.0 - (d / 2.0))
    return 1.0 / (1.0 + d)

# -----------------------
# Retrieval with scoring + priority boost
# -----------------------
def retrieve_with_scores(query, k=8, min_sim_threshold=0.15):
    q_emb = embed.encode([query]).tolist()
    res = col.query(query_embeddings=q_emb, n_results=k, include=["documents", "metadatas", "distances"])
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    items = []
    for doc, meta, dist in zip(docs, metas, dists):
        src = meta.get("source", "unknown") if isinstance(meta, dict) else "unknown"
        priority = meta.get("priority", 1.0) if isinstance(meta, dict) else 1.0
        sim = distance_to_similarity(dist)
        boosted = sim * float(priority)
        items.append({
            "chunk": doc,
            "source": src,
            "dist": dist,
            "sim": sim,
            "priority": float(priority),
            "boosted_sim": boosted
        })

    items = sorted(items, key=lambda x: x["boosted_sim"], reverse=True)
    filtered = [it for it in items if it["boosted_sim"] >= min_sim_threshold]
    if not filtered:
        filtered = items[:min(3, len(items))]
    # debug print
    print(f"[retrieve_with_scores] query='{query[:80]}...' -> {len(items)} candidates, {len(filtered)} filtered")
    for i, it in enumerate(filtered[:6], 1):
        print(f"  {i}. {it['source']} sim={it['sim']:.3f} prio={it['priority']} boosted={it['boosted_sim']:.3f}")
    return filtered

# -----------------------
# Re-ranker using the LLM (returns top_n candidate dicts)
# -----------------------
def rerank_candidates(question, candidates, top_n=3):
    """
    Re-rank candidates by asking the LLM. If LLM output cannot be parsed
    into indices, fallback to boosting-based ordering (already sorted).
    We also log the raw LLM output for debugging.
    """
    if not candidates:
        return []

    chunk_texts = []
    for i, c in enumerate(candidates, start=1):
        snippet = c["chunk"]
        snippet = snippet if len(snippet) < 1200 else snippet[:1200] + "..."
        chunk_texts.append(f"[{i}] Source: {c['source']}\n{snippet}")

    rerank_prompt = f"""
You are a strict relevance re-ranker. Given the user's question, return a comma-separated list
of the indices of the most relevant chunks (highest relevance first). Return only indices and nothing else.

QUESTION:
{question}

CANDIDATES:
{chr(10).join(chunk_texts)}

Return top {top_n} indices like: 3,1,5
"""
    try:
        resp = llm.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": rerank_prompt}],
            temperature=0.0,
            max_tokens=80,
        )
        # extract text robustly
        choices = getattr(resp, "choices", None) or resp.get("choices", None)
        text = ""
        if choices:
            first = choices[0]
            if hasattr(first, "message") and getattr(first.message, "content", None):
                text = first.message.content
            elif isinstance(first, dict):
                text = first.get("message", {}).get("content") or first.get("text") or ""
        # log raw reranker output for debugging
        print("[rerank_candidates] raw reranker output:", repr(text))

        # parse indices
        nums = re.findall(r"\d+", text)
        indices = [int(n) for n in nums][:top_n]
        ranked = []
        for idx in indices:
            if 1 <= idx <= len(candidates):
                ranked.append(candidates[idx-1])

        if not ranked:
            # fallback to top by boosted_sim (candidates already sorted)
            print("[rerank_candidates] parsing failed or empty -> fallback to boosted_sim")
            ranked = candidates[:min(top_n, len(candidates))]
        return ranked

    except Exception as e:
        print("[rerank_candidates] error:", e)
        return candidates[:min(top_n, len(candidates))]

# ***************** DETECT LANGUGE *****************
def detect_language_simple(text: str) -> str:
    """
    Very small heuristic to detect French vs English.
    Returns 'fr' or 'en'.
    """
    t = text.lower()
    # split into words
    words = re.findall(r"\b\w+\b", t)
    # tokens typical of French
    french_tokens = ["bonjour", "merci", "vous", "quel", "quelle", "qu'", "quels", "parle", "parles", "francais", "français", "où", "est-ce", "suis", "je suis", "avez", "voyage", "language", "langue", "pays", "très", "être", "étudiant", "étudiante", "études", "école", "économique", "beaucoup", "d'accord", "ça", "c'est", "j'ai", "j'", "l'", "là", "n'", "cette", "cette", "trop", "défaut", "défauts"]
    # if any french token appears -> fr
    for tok in french_tokens:
        if tok in words:
            return "fr"
    # fallback: if many ascii letters and common english tokens -> en
    english_tokens = ["hi", "hello", "thank", "you", "are you", "what", "where", "do you", "i am", "i'm", "the", "is", "it", "that", "this", "very", "a", "an", "and", "but", "or", "if", "for", "on", "in", "with", "as", "at", "by"]
    for tok in english_tokens:
        if tok in words:
            return "en"
            
    return "en"  # default to English

# -----------------------
# Prompt builder (expects contexts as list of candidate dicts)
# -----------------------
def build_prompt(question, contexts):
    ctx_texts = []
    for i, c in enumerate(contexts, 1):
        chunk = c.get("chunk", "")
        chunk = chunk if len(chunk) < 3000 else chunk[:3000] + "..."
        src = c.get("source", "unknown")
        # keep source only for internal/logging, not to be printed by model
        ctx_texts.append(f"[{i}] {chunk}")
    ctx_block = "\n\n---\n\n".join(ctx_texts)
    prompt = f"{SYSTEM_INSTRUCTIONS}\n\nCONTEXT:\n{ctx_block}\n\nQUESTION: {question}\n\nAnswer now."
    return prompt

# -----------------------
# Ask LLM (robust parsing)
# -----------------------
def ask_llm(prompt_user, max_tokens=400, temperature=0.15):
    try:
        response = llm.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": prompt_user}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
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


def _log_candidates(label, candidates, max_items=10):
    """Log candidates/top candidates in console in a readable way."""
    print(f"\n[{label}] - {len(candidates)} items")
    for i, c in enumerate(candidates[:max_items], start=1):
        src = c.get("source", "unknown")
        sim = c.get("sim", 0.0)
        boosted = c.get("boosted_sim", 0.0)
        snippet = c.get("chunk", "")[:300].replace("\n", " ")
        print(f"  {i}. {src} | sim={sim:.3f} boosted={boosted:.3f} | snippet: {snippet!r}")
    if len(candidates) > max_items:
        print(f"  ... ({len(candidates)-max_items} more)\n")
    else:
        print("")

@app.route("/qa", methods=["POST"])
def qa():
    token = request.headers.get("x-api-key") or request.args.get("api_key")
    if token != API_TOKEN:
        abort(401)
    data = request.json or {}
    q = data.get("question", "").strip()
    if not q:
        return jsonify({"error": "No question provided"}), 400

    lang = detect_language_simple(q)
    # small explicit instruction to the user part of prompt (so the model sees the language twice and obeys)
    lang_instr = "Réponds en français." if lang == "fr" else "Answer in English."

    # 1) retrieve candidates with scores & priority boost
    candidates = retrieve_with_scores(q, k=8, min_sim_threshold=0.12)

    # Log all candidates in console (for debugging)
    _log_candidates("ALL CANDIDATES", candidates, max_items=8)

    # 2) rerank candidates (ask LLM to rank) -> top_contexts
    top_candidates = rerank_candidates(q, candidates, top_n=3)

    # Log top candidates in console
    _log_candidates("TOP CANDIDATES (after rerank)", top_candidates, max_items=8)

    # 3) build prompt and call LLM
    prompt = lang_instr + "\n\n" + build_prompt(q, top_candidates)
    print(f"[/qa] Prompt length: {len(prompt)} chars")
    # Optionnel : print the first N chars of the prompt for quick inspection
    print(f"[/qa] Prompt preview:\n{prompt[:1200]}\n--- end prompt preview ---\n")

    answer = ask_llm(prompt, max_tokens=400, temperature=0.1)

    # 4) return only the answer to the frontend (no sources)
    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
