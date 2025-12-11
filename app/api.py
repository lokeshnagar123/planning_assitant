from fastapi import FastAPI
from app.agents.merchandising import explain_forecast_drop
from app.agents.inventory import suggest_transfers
from app.governance.audit import log_interaction
from app.governance.guardrails import assert_policy_compliance

app = FastAPI()

@app.post("/chat/explain-forecast")
def explain(payload: dict):
    result = explain_forecast_drop(payload["category"], payload["region"], payload["week"])
    assert_policy_compliance(result)
    log_interaction("explain_forecast", payload, result)
    return result

@app.post("/actions/inventory/transfers")
def transfers(payload: dict):
    result = suggest_transfers(payload["sku"], payload["weekend"])
    assert_policy_compliance(result)
    log_interaction("transfer_suggest", payload, result)
    return result