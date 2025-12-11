def citation_coverage(resp):
    c = resp.get("citations", {})
    return 1.0 if c.get("kpi_source") and c.get("docs") else 0.0