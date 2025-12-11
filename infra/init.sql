CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS kpi_sales(
  week DATE, region TEXT, category TEXT, sku TEXT,
  units INT, sales NUMERIC, margins NUMERIC
);

CREATE TABLE IF NOT EXISTS kpi_forecast(
  week DATE, region TEXT, category TEXT, sku TEXT,
  forecast_units INT, actual_units INT
);

CREATE TABLE IF NOT EXISTS kpi_inventory(
  date DATE, dc TEXT, store TEXT, sku TEXT,
  on_hand INT, on_order INT, lead_time_days INT
);

CREATE TABLE IF NOT EXISTS promo_calendar(
  start_date DATE, end_date DATE, region TEXT, category TEXT, sku TEXT,
  promo_type TEXT, discount_pct NUMERIC
);

CREATE TABLE IF NOT EXISTS price_ladders(
  region TEXT, category TEXT, sku TEXT,
  reg_price NUMERIC, promo_price NUMERIC, markdown_floor NUMERIC
);

-- RAG store
CREATE TABLE IF NOT EXISTS rag_docs(
  id SERIAL PRIMARY KEY,
  doc_title TEXT,
  chunk TEXT,
  metadata JSONB,
  embedding VECTOR(768)
);
CREATE INDEX IF NOT EXISTS rag_docs_embedding_idx ON rag_docs USING ivfflat (embedding);