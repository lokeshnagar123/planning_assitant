import csv, psycopg2, os
DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/planning")

def load_csv(table, path, cols):
    conn = psycopg2.connect(DB_URL); cur = conn.cursor()
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            cur.execute(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join(['%s']*len(cols))})", [row[c] for c in cols])
    conn.commit(); cur.close(); conn.close()

if __name__ == "__main__":
    base="data/kpis"
    load_csv("kpi_sales",f"{base}/weekly_sales.csv",["week","region","category","sku","units","sales","margins"])
    load_csv("kpi_forecast",f"{base}/forecast_vs_actual.csv",["week","region","category","sku","forecast_units","actual_units"])
    load_csv("kpi_inventory",f"{base}/inventory_positions.csv",["date","dc","store","sku","on_hand","on_order","lead_time_days"])
    load_csv("promo_calendar",f"{base}/promo_calendar.csv",["start_date","end_date","region","category","sku","promo_type","discount_pct"])
    load_csv("price_ladders",f"{base}/price_ladders.csv",["region","category","sku","reg_price","promo_price","markdown_floor"])
    print("Loaded sample KPI tables.")