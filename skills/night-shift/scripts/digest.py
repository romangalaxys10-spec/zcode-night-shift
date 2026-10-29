#!/usr/bin/env python3
"""Render the night-shift morning digest from a run log (JSONL)."""
import argparse, json, sys
from collections import OrderedDict

def main():
    ap = argparse.ArgumentParser(description="night-shift digest")
    ap.add_argument("--log", required=True)
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown")
    a = ap.parse_args()
    tasks = OrderedDict()
    try:
        fh = open(a.log, encoding="utf-8")
    except OSError as e:
        print("cannot read log: %s" % e, file=sys.stderr)
        return 2
    with fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                tasks.setdefault("malformed-line-%d" % n,
                                 {"id": "line-%d" % n, "status": "parked",
                                  "reason": "malformed log line", "summary": ""})
                continue
            tid = str(ev.get("id", ev.get("task", "unknown")))
            t = tasks.setdefault(tid, {"id": tid, "status": "queued",
                                       "reason": "", "summary": ""})
            st = ev.get("status", "")
            if st:
                t["status"] = st
            if ev.get("reason"):
                t["reason"] = str(ev["reason"])
            if ev.get("summary"):
                t["summary"] = str(ev["summary"])
    counts = {"completed": 0, "parked": 0, "failed": 0, "queued": 0, "started": 0}
    for t in tasks.values():
        counts[t["status"]] = counts.get(t["status"], 0) + 1
    order = {"failed": 0, "parked": 1, "completed": 2, "started": 3, "queued": 4}
    rows = sorted(tasks.values(), key=lambda t: order.get(t["status"], 9))
    if a.format == "json":
        print(json.dumps({"counts": counts, "tasks": rows}, indent=2))
        return 0
    print("# Night shift digest\n")
    print("%(completed)s completed, %(parked)s parked, %(failed)s failed.\n" % counts)
    for t in rows:
        line = "- **%s** %s" % (t["status"].upper(), t["id"])
        if t["summary"]:
            line += ": " + t["summary"]
        if t["reason"]:
            line += " (reason: %s)" % t["reason"]
        print(line)
    if counts["parked"] or counts["failed"]:
        print("\nParked and failed tasks need your call before any retry.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
