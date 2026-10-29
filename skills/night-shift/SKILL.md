---
name: night-shift
description: Run queued tasks overnight under an explicit auto-approval policy; safe ops proceed, risky ops park with a reason; ends with a morning digest. Use when the user wants batch work done while away without babysitting approvals.
---

# Night Shift

## Files

- Queue: `.zcode/night-shift/queue.jsonl`, one task per line: `{"id", "prompt", "allowed-dirs", "risk"}`
- Policy: `.zcode/night-shift/policy.json`, lists safe operation categories
- Run log: `.zcode/night-shift/run.jsonl`, one event per line

## Procedure

1. VALIDATE QUEUE: parse every line. A malformed line parks immediately with
   reason "malformed".
2. POLICY GATE: an operation may auto-proceed ONLY if its category is listed
   safe in the policy AND it stays inside the task's allowed-dirs. Everything
   else parks the task with the exact reason. Never invent new safe categories
   mid-run.
3. RUN each task as a fresh subagent (Agent tool) with a self-contained brief:
   the task prompt, the allowed dirs, and the rule "if you need anything
   outside the policy, STOP and output PARKED: <reason>".
4. RECORD one log event per task: started, completed, parked, or failed, with
   timestamps and a two-line summary.
5. SCRATCH BRANCH: any commit happens on `night-shift/<task-id>`, never on the
   user's current branch. Never push.
6. DIGEST: run `skills/night-shift/scripts/digest.py --log
   .zcode/night-shift/run.jsonl` and present the report.

## Hard rules

- Max 3 fix attempts per task, then mark it failed.
- A parked task resumes only by human decision, in a normal session.
- Empty queue: say so and exit. Do not invent work.
