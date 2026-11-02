# Changelog

## 0.2.0 - 2026-11-02

- Ask mode: policy.json gains `"ask": ["payment","send-message","publish","purchase"]`. Tasks that hit an ask-tier operation stop with a single `ASK: <what and why>` line and status "asked" in run.jsonl, instead of parking silently.
- Digest: digest.py now counts "asked" and renders asked tasks in their own "Needs your call" group, separate from parked/failed.
- SKILL.md policy gate documents the three tiers (safe auto-proceed, ask stop-and-ask, rest parks); subagents report `ASKED: <what and why>` back to the runner.
- Both manifests and the commands file updated; version 0.2.0.

## 0.1.0 - 2026-10-29

- Initial release: queue + policy gated overnight runner, scratch-branch commits, morning digest grouped failed/parked/completed.
