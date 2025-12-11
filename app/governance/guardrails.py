BLOCKED = ["change customer PII","financial disclosure","delete all data"]

def assert_policy_compliance(result):
    assert "citations" in result, "Missing citations"
    for term in BLOCKED:
        assert term not in str(result).lower()