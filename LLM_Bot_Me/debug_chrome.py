# debug_chrome.py
import chromadb
import numpy as np
from numpy.linalg import norm
from transformers import AutoTokenizer, AutoModel
import torch

EMBED_MODEL = "google/embeddinggemma-300m"

print("Loading HF transformers model...")
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

client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_collection("portfolio")

query = "Avez-vous de l’expérience avec C# ?"
q = query.strip().replace("?", "")

q_emb = embed_texts([q])[0]

res = col.query(query_embeddings=[q_emb.tolist()], n_results=50, include=["documents","metadatas","distances"])
docs = res["documents"][0]
metas = res["metadatas"][0]

for i, (doc, meta) in enumerate(zip(docs, metas), 1):
    d_emb = embed_texts([doc])[0]
    sim = float(np.dot(q_emb, d_emb) / (norm(q_emb) * norm(d_emb)))
    print(f"{i:2d} {meta.get('source','?'):30} sim_local={sim:.4f} | {doc[:120].replace(chr(10),' ')}")
