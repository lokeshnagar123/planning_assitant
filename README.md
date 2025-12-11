# Planning Assistant (Retail) â€” Local Llamaâ€‘3 via Ollama

Endâ€‘toâ€‘end demo for a merchandiser **Planning Assistant** focused on **Dairy** in **West** region of India:
- Explain **forecast deltas** with grounded narrative + **citations**
- Suggest **OTB notes / inventory transfers** with guardrails + audit
- **RAG** over policy/SOP/playbooks using local embeddings via Ollama

## Quick Start
1) Install Ollama (Windows): https://ollama.com/download
   - Run: `ollama serve`
   - Models: `ollama pull llama3:8b` and `ollama pull nomic-embed-text`

2) Start Postgres:
   - `docker compose up -d db`

3) Load sample KPIs & index RAG docs:
   - `python ingest\load_kpis.py`
   - `python ingest\index_docs.py`

4) Run API & UI:
   - API: `python -m uvicorn app.api:app --reload --port 8000`
   - UI:  `streamlit run app\ui\streamlit_app.py`

Open: http://localhost:8501