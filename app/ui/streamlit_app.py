
# app/ui/streamlit_app.py
import streamlit as st
import requests
import os

API = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("Planning Assistant (Local Llamaâ€‘3)")
st.subheader("Explain forecast deltas & recommend actions with citations")

def post_json(url: str, payload: dict):
    try:
        r = requests.post(url, json=payload, timeout=30)
    except requests.exceptions.RequestException as e:
        return None, f"Network/connection error: {e}"

    if r.status_code != 200:
        # Return raw text so you can see FastAPI's error (traceback/HTML)
        return None, f"HTTP {r.status_code} from API: {r.text[:600]}"

    try:
        return r.json(), None
    except requests.exceptions.JSONDecodeError:
        return None, f"API returned nonâ€‘JSON. Raw content:\n{r.text[:600]}"

with st.form("explain"):
    category = st.text_input("Category", "Dairy")
    region = st.text_input("Region", "West")
    week = st.text_input("Week (YYYY-MM-DD)", "2025-06-08")
    submitted = st.form_submit_button("Explain")
    if submitted:
        res, err = post_json(f"{API}/chat/explain-forecast",
                             {"category": category, "region": region, "week": week})
        if err:
            st.error(err)
        else:
            st.write(res.get("answer"))
            st.write("**Citations:**", res.get("citations"))
            st.table(res.get("kpis"))

st.divider()
st.subheader("Inventory transfer suggestion")

with st.form("transfer"):
    sku = st.text_input("SKU", "SKU-001")
    weekend = st.text_input("Weekend (YYYY-MM-DD)", "2025-06-14")
    go = st.form_submit_button("Suggest")
    if go:
        res, err = post_json(f"{API}/actions/inventory/transfers",
                             {"sku": sku, "weekend": weekend})
        if err:
            st.error(err)
        else:
            st.json(res)
