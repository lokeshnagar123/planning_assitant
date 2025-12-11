import psycopg2, os
DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/planning")

def kpi_timeseries(category, region, lookback=6):
    conn = psycopg2.connect(DB_URL); cur = conn.cursor()
    cur.execute("""
      SELECT f.week, f.forecast_units, f.actual_units, s.sales, s.margins
      FROM kpi_forecast f
      LEFT JOIN kpi_sales s
        ON s.week=f.week AND s.region=f.region AND s.category=f.category AND s.sku=f.sku
      WHERE f.category=%s AND f.region=%s
      ORDER BY f.week DESC LIMIT %s
    """,(category, region, lookback))
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def nearest_docs(query_terms, topk=4):
    conn = psycopg2.connect(DB_URL); cur = conn.cursor()
    like = "%" + " ".join(query_terms) + "%"
    cur.execute("""
      SELECT doc_title, chunk, metadata
      FROM rag_docs
      WHERE chunk ILIKE %s OR doc_title ILIKE %s
      LIMIT %s
    """, (like, like, topk))
    docs = [{"title":t, "chunk":c, "meta":m} for (t,c,m) in cur.fetchall()]
    cur.close(); conn.close()
    return docs