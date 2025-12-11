import streamlit as st, requests, os
API = os.getenv("API_URL","http://127.0.0.1:8000")

st.title("Planning Assistant (Local Llamaâ€‘3)")
st.subheader("Explain forecast deltas & recommend actions with citations")

with st.form("explain"):
    category = st.text_input("Category", "Dairy")
    region = st.text_input("Region", "West")
    week = st.text_input("Week (YYYY-MM-DD)", "2025-06-08")
    submitted = st.form_submit_button("Explain")
    if submitted:
        r = requests.post(f"{API}/chat/explain-forecast",
                          json={"category":category,"region":region,"week":week})
        res = r.json()
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
        r = requests.post(f"{API}/actions/inventory/transfers",
                          json={"sku":sku,"weekend":weekend})
        st.json(r.json())