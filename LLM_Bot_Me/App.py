from flask import Flask, request, jsonify, abort
from sentence_transformers import SentenceTransformer
import chromadb
import os
from openai import OpenAI
from flask_cors import CORS


client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_collection("portfolio")

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
embed = SentenceTransformer(EMBED_MODEL)

# LM Studio client
llm = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
MODEL_NAME = "liquid/lfm2-1.2b"

app = Flask(__name__)
CORS(app) 
API_TOKEN = os.getenv("API_TOKEN", "JUDO1205")

def retrieve_context(query, k=4):
    q_emb = embed.encode([query]).tolist()
    res = col.query(query_embeddings=q_emb, n_results=k)
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    return [(d, m.get("source", "unknown")) for d, m in zip(docs, metas)]


with open("prompts/analysis_system.txt", "r", encoding="utf-8") as f:
    SYSTEM_INSTRUCTIONS = f.read().strip()

def build_prompt(question, contexts):
    ctx_texts = [f"[{i}] Source: {s}\n{c}" for i, (c, s) in enumerate(contexts, 1)]
    ctx_block = "\n\n---\n\n".join(ctx_texts)
    return f"{SYSTEM_INSTRUCTIONS}\n\nCONTEXT:\n{ctx_block}\n\nQUESTION: {question}"

def ask_llm(prompt, max_tokens=400):
    response = llm.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.2,
    )
    return response.choices[0].message.content

@app.route("/qa", methods=["POST"])
def qa():
    token = request.headers.get("x-api-key")
    if token != API_TOKEN:
        abort(401)
    q = (request.json or {}).get("question", "").strip()
    if not q:
        return jsonify({"error": "No question provided"}), 400
    contexts = retrieve_context(q, k=4)
    prompt = build_prompt(q, contexts)
    return jsonify({"answer": ask_llm(prompt)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
