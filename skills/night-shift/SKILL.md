---
name: night-shift
description: Run queued tasks overnight under an explicit auto-approval policy; safe ops proceed, ask-tier ops (payment, send-message, publish, purchase) stop with a structured ASK line and "asked" status, risky ops park with a reason; ends with a morning digest. Use when the user wants batch work done while away without babysitting approvals.
---

# Night Shift

## Files

- Queue: `.zcode/night-shift/queue.jsonl`, one task per line: `{"id", "prompt", "allowed-dirs", "risk"}`
- Policy: `.zcode/night-shift/policy.json` with tiers: `"safe": [...]` (may
  auto-proceed), `"ask": ["payment","send-message","publish","purchase"]`
  (stop and ask the human, do not run), and anything unlisted parks.
- Run log: `.zcode/night-shift/run.jsonl`, one event per line

## Procedure

1. VALIDATE QUEUE: parse every line. A malformed line parks immediately with
   reason "malformed".
2. POLICY GATE: decide the tier of each operation a task needs:
   - safe (listed in `safe` AND inside the task's allowed-dirs): auto-proceed.
   - ask tier (listed in `ask`): do NOT execute. End the turn with one line
     `ASK: <what and why>`, record the task with status "asked" plus the ask
     text in run.jsonl, and move on to the next task.
   - anything else: park the task with the exact reason. Never invent new
     safe or ask categories mid-run.
3. RUN each task as a fresh subagent (Agent tool) with a self-contained brief:
   the task prompt, the allowed dirs, and the rule "if you need an ask-tier
   operation, output ASKED: <what and why>; if you need anything outside
   the policy, output PARKED: <reason>".
4. RECORD one log event per task: started, completed, asked (with the ASK
   text as reason), parked, or failed, with timestamps and a two-line
   summary.
5. SCRATCH BRANCH: any commit happens on `night-shift/<task-id>`, never on
   the user's current branch. Never push.
6. DIGEST: run `skills/night-shift/scripts/digest.py --log
   .zcode/night-shift/run.jsonl` and present the report.

## Hard rules

- Max 3 fix attempts per task, then mark it failed.
- A parked or asked task resolves only by human decision, in a normal
  session. Ask-tier operations are never executed unattended.
- Empty queue: say so and exit. Do not invent work.
