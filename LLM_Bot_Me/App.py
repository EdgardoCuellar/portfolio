# app.py
import os
from flask import Flask, request, jsonify, abort
from sentence_transformers import SentenceTransformer
import chromadb
from openai import OpenAI

# ----- CONFIG via ENV (safe defaults where reasonable) -----
LMSTUDIO_BASE = os.getenv("LMSTUDIO_BASE", "http://localhost:1234/v1")
LMSTUDIO_API_KEY = os.getenv("LMSTUDIO_API_KEY", "lm-studio")  # change for security
MODEL_NAME = os.getenv("MODEL_NAME", "liquid/lfm2-1.2b")
API_TOKEN = os.getenv("API_TOKEN", "JUDO1205")  # simple auth token for /qa
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "portfolio")

# ----- INIT clients -----
# OpenAI-compatible client pointing to local LM Studio
client = OpenAI(base_url=LMSTUDIO_BASE, api_key=LMSTUDIO_API_KEY)

# Embedding model (local SBERT) for retrieval
embed = SentenceTransformer(EMBED_MODEL)

# chroma vector DB
chroma_client = chromadb.Client()
try:
    col = chroma_client.get_collection(COLLECTION_NAME)
except Exception:
    col = chroma_client.create_collection(COLLECTION_NAME)

app = Flask(__name__)

# ----- SYSTEM INSTRUCTIONS used to build prompts -----
SYSTEM_INSTRUCTIONS = """
You are an assistant that knows Edgardo's portfolio and CVs. Answer concisely,
be factual, and cite the source filename when you use the provided context.
If the information is not present in the provided context, explicitly say:
"I don't know based on my documents — please check the portfolio or ask me directly."
Do not invent qualifications or facts. If asked for opinion or ambiguous requests, answer clearly and state assumptions.
"""

def retrieve_context(query, k=4):
    q_emb = embed.encode([query]).tolist()
    res = col.query(query_embeddings=q_emb, n_results=k)
    # defensive access
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    out = []
    for d, m in zip(docs, metas):
        source = m.get("source", "unknown") if isinstance(m, dict) else "unknown"
        out.append((d, source))
    return out

def build_prompt(question, contexts):
    ctx_texts = []
    for idx, (chunk, source) in enumerate(contexts, 1):
        ctx_texts.append(f"[{idx}] Source: {source}\n{chunk}")
    ctx_block = "\n\n---\n\n".join(ctx_texts)
    prompt = f"{SYSTEM_INSTRUCTIONS}\n\nCONTEXT:\n{ctx_block}\n\nQUESTION: {question}\n\nAnswer concisely and list sources used (by index). If you cannot answer from the provided context, reply exactly: \"I don't know based on my documents — please check the portfolio or ask me directly.\""
    return prompt

def ask_llm_openai_chat(prompt, max_tokens=400, temperature=0.1):
    """
    Use the OpenAI-compatible client (pointing to LM Studio) via chat completions.
    """
    try:
        # Following the style in your snippet: client.chat.completions.create(...)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # parse response safely
        # Many OpenAI-like servers return choices[0].message.content
        choices = getattr(response, "choices", None) or response.get("choices", None)
        if choices:
            first = choices[0]
            # Try attribute access first, fallback to dict style
            msg = None
            if hasattr(first, "message") and getattr(first.message, "content", None):
                msg = first.message.content
            elif isinstance(first, dict) and "message" in first and "content" in first["message"]:
                msg = first["message"]["content"]
            elif isinstance(first, dict) and "text" in first:
                msg = first["text"]
            # final fallback: convert whole response to string
            if msg:
                return msg
        # fallback for other response schemas
        return str(response)
    except Exception as e:
        # don't crash — return an error string
        return f"Error calling LM Studio: {e}"

@app.route("/qa", methods=["POST"])
def qa():
    token = request.headers.get("x-api-key") or request.args.get("api_key")
    if token != API_TOKEN:
        abort(401)
    data = request.json or {}
    q = data.get("question", "").strip()
    if not q:
        return jsonify({"error": "No question provided"}), 400

    contexts = retrieve_context(q, k=4)
    prompt = build_prompt(q, contexts)
    answer = ask_llm_openai_chat(prompt)
    return jsonify({"answer": answer})

@app.route("/", methods=["GET"])
def health():
    return "OK - Portfolio QA service running."

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port)
