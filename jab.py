#!/usr/bin/env python3
"""Nightly Mordor race jab. Reads the race ledger from the GitHub repo, sends an iMessage scoreboard taunt."""
import json, subprocess, datetime, hashlib, sys

RAW = "https://raw.githubusercontent.com/ABC123146/mordor-race/main/logs/"
TO = ["trevlyan28@icloud.com"]  # add Tremayne's iMessage here when he's ready
TOTAL_MI = 1779
STRIDE = 0.78
NAMES = {"trev": "Trev", "trem": "Tremayne"}

def readmap(who):
    out = subprocess.run(["curl", "-s", "-m", "30", RAW + who + ".json"], capture_output=True, text=True)
    try:
        return json.loads(out.stdout)
    except Exception:
        return {}

maps = {w: readmap(w) for w in NAMES}
today = datetime.date.today().isoformat()
mi = {w: min(TOTAL_MI, sum(maps[w].values()) * STRIDE / 1609.344) for w in NAMES}
kmv = {w: mi[w] * 1.609344 for w in NAMES}
today_steps = {w: int(maps[w].get(today, 0)) for w in NAMES}

lines = ["🌋 THE ROAD TO MORDOR, day report"]
for w in NAMES:
    t = f"{today_steps[w]:,} steps today" if today_steps[w] else "NOTHING logged today"
    lines.append(f"{NAMES[w]}: {t} · {kmv[w]:.1f} km total")

gap = kmv["trev"] - kmv["trem"]
if not any(maps.values()):
    lines.append("The race has not begun. Bag End waits.")
elif abs(gap) < 1.6:
    lines.append("Dead level. Tomorrow decides.")
else:
    lead, chase = ("trev", "trem") if gap > 0 else ("trem", "trev")
    lines.append(f"{NAMES[lead]} leads by {abs(gap):.1f} km. The Ring is his tonight.")
    taunts = [
        f"{NAMES[chase]}, the Eye watches you rest.",
        f"{NAMES[chase]}, Sam carried Frodo. Nobody is carrying you.",
        f"One does not simply catch up by sitting down, {NAMES[chase]}.",
        f"{NAMES[chase]}, even Gollum kept pace.",
        f"The Black Gate will not walk to you, {NAMES[chase]}.",
    ]
    lines.append(taunts[int(hashlib.md5(today.encode()).hexdigest(), 16) % len(taunts)])
lines.append("https://abc123146.github.io/mordor-race/")

msg = "\n".join(lines)
if "--dry" in sys.argv:
    print(msg); sys.exit(0)
SCRIPT = '''on run argv
tell application "Messages" to send (item 1 of argv) to participant (item 2 of argv) of (1st account whose service type = iMessage)
end run'''
for to in TO:
    subprocess.run(["osascript", "-e", SCRIPT, msg, to], check=True)
print("sent:", msg)
