# Night Shift

Queue tasks before bed. Safe operations run unattended; ask-tier operations
(payment, send-message, publish, purchase) stop with a clear ASK line instead
of running or parking silently; risky ones park with a reason. You wake up to
a digest, not a stuck approval prompt.

## Why

The most upvoted complaint in agent communities: the agent politely waited 8
hours for a yes while the user slept. Night Shift replaces the yes/no loop
with a policy you set once. v0.2.0 adds the third gear: some operations you
would actually approve in the morning (a payment, a message, a publish) are
better asked about than parked. The runner ends its turn with one line,
`ASK: <what and why>`, records status "asked", and the digest groups asked
tasks under "Needs your call", so the decisions you would have made anyway
happen in two minutes of reading, not two minutes of digging.

## How it works

| Step | What happens |
|------|--------------|
| Queue | `.zcode/night-shift/queue.jsonl`, one task per line with allowed dirs and risk |
| Policy | Your `policy.json` has two lists: `"safe"` (auto-proceed) and `"ask"` (`["payment","send-message","publish","purchase"]`, stop and ask); anything unlisted parks |
| Ask mode | When a task needs an ask-tier op, the runner stops, prints `ASK: <what and why>`, logs status "asked", and moves on |
| Run | Each task gets a fresh subagent, scoped to its allowed dirs, commits only on a scratch branch |
| Digest | Morning markdown report: completed, asked (grouped under "Needs your call"), parked (with reasons), failed |

Example `policy.json`:

```json
{
  "safe": ["edit-allowed-dirs", "tests", "linters", "scratch-branch-commit"],
  "ask": ["payment", "send-message", "publish", "purchase"]
}
```

## Install

1. Clone or download this repo to a folder.
2. In ZCode: Plugin Marketplace -> Add -> Add Plugin Marketplace, paste that folder path.
3. Install *Night Shift*.

Option B: copy the folder into your workspace `plugins/` directory.

## Try it

```
/night-shift run
```

Expected: tasks execute in order, anything in the ask tier stops with its
`ASK:` line, everything outside the policy parks with its reason, and the
digest closes the run with asked tasks in their own group.

## Honest limits

It never pushes and never auto-approves outside your policy file. Ask-tier
operations are never executed unattended: they wait for a human in a normal
session, same as parked tasks.

<p align="center">
  <a href="https://z.ai/subscribe?ic=R0K78RJKNW"><img alt="z.ai coding plans - 10% OFF coupon" src="https://img.shields.io/badge/z.ai%20coding%20plans-10%25%20OFF%20coupon-blueviolet" /></a>
  <a href="https://zcode.z.ai/invite/ALWM9JUA"><img alt="Try ZCode free" src="https://img.shields.io/badge/Try%20ZCode-free%20invite-0969da" /></a>
</p>

## License

MIT.
