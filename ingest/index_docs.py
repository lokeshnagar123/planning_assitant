import os, glob, json, httpx, psycopg2
from pathlib import Path

DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/planning")
OLLAMA = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

def chunks(text, size=800, overlap=120):
    words = text.split()
    for i in range(0, len(words), size - overlap):
        yield " ".join(words[i:i+size])

def embed(text):
    r = httpx.post(f"{OLLAMA}/api/embeddings", json={"model": EMBED_MODEL, "prompt": text}, timeout=60)
    r.raise_for_status()
    return r.json()["embedding"]

conn = psycopg2.connect(DB_URL); cur = conn.cursor()
for folder, prefix in [("data/policies", "Policy"), ("data/playbooks", "Playbook")]:
    for path in glob.glob(f"{folder}/*"):
        title = f"{prefix}: {Path(path).name}"
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
        for ch in chunks(text):
            vec = embed(ch)
            cur.execute("""
                INSERT INTO rag_docs(doc_title, chunk, metadata, embedding)
                VALUES (%s,%s,%s,%s)
            """, (title, ch, json.dumps({"source": path}), vec))
conn.commit(); cur.close(); conn.close()
print("Indexed policy/playbook docs into rag_docs.")