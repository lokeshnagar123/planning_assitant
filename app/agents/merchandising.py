import os, httpx
from app.rag.retriever import kpi_timeseries, nearest_docs

OLLAMA = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3:8b")

def _chat(system_prompt, user_prompt):
    resp = httpx.post(f"{OLLAMA}/api/chat", timeout=120, json={
        "model": LLM_MODEL,
        "messages": [
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ],
        "stream": False
    })
    resp.raise_for_status()
    return resp.json()["message"]["content"]

def explain_forecast_drop(category, region, week):
    kpis = kpi_timeseries(category, region, lookback=6)
    docs = nearest_docs(["promo","OTB",category])
    system = open("app/rag/prompts/merchandising_explain.txt", "r", encoding="utf-8").read()
    user = f"Explain the forecast drop for {category} in {region} during week {week}."
    answer = _chat(system, user)
    citations = {
        "kpi_source": "kpi_forecast + kpi_sales (last 6 weeks)",
        "docs": [d["title"] for d in docs]
    }
    return {"answer": answer, "citations": citations, "kpis": kpis}