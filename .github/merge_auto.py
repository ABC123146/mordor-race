#!/usr/bin/env python3
"""Merge Shortcut-dropped auto logs (logs/auto/<who>-<date>-<ts>.json) into logs/<who>.json."""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
auto = root / "logs" / "auto"
if auto.exists():
    files = sorted(auto.glob("*.json"))
    for f in files:
        m = re.match(r"(trev|trem)-(\d{4}-\d{2}-\d{2})", f.stem)
        if not m:
            f.unlink(); continue
        who, date = m.group(1), m.group(2)
        try:
            steps = int(json.loads(f.read_text()).get("steps", 0))
        except Exception:
            f.unlink(); continue
        tgt = root / "logs" / f"{who}.json"
        data = json.loads(tgt.read_text()) if tgt.exists() else {}
        if steps > 0:
            data[date] = steps
        tgt.write_text(json.dumps(data, indent=1) + "\n")
        f.unlink()
print("merged")
