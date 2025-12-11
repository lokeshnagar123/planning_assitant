def suggest_transfers(sku, weekend_date):
    # Demo stub: in a fuller version youâ€™d query inventory & promo tables
    return {
      "plan": f"Transfer 80 units of {sku} from DC01 to Store-17 before {weekend_date}",
      "citations": {"kpi_source":"kpi_inventory", "policy":"Playbook: Merchandising_Playbook.txt"}
    }