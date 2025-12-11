import json, time, pathlib
LOG = pathlib.Path("audit.log")

def log_interaction(kind, payload, result):
    entry = {"ts": time.time(), "kind": kind, "payload": payload, "result": result}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry)+"\n")