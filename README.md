# Night Shift

Queue tasks before bed. Safe operations run unattended; risky ones park with a
reason. You wake up to a digest, not a stuck approval prompt.

## Why

The most upvoted complaint in agent communities: the agent politely waited 8
hours for a yes while the user slept. Night Shift replaces the yes/no loop with
a policy you set once.

## How it works

| Step | What happens |
|------|--------------|
| Queue | `.zcode/night-shift/queue.jsonl`, one task per line with allowed dirs and risk |
| Policy | Your `policy.json` lists what may auto-proceed; everything else parks |
| Run | Each task gets a fresh subagent, scoped to its allowed dirs, commits only on a scratch branch |
| Digest | Morning markdown report: completed, parked (with reasons), failed |

## Install

1. Clone or download this repo to a folder.
2. In ZCode: Plugin Marketplace -> Add -> Add Plugin Marketplace, paste that folder path.
3. Install *Night Shift*.

## Try it

```
/night-shift run
```

Expected: tasks execute in order, anything outside the policy parks with its
reason, and the digest closes the run.

## Honest limits

It never pushes and never auto-approves outside your policy file. A parked task
waits for a human decision.

<p align="center">
  <a href="https://z.ai/subscribe?ic=R0K78RJKNW"><img alt="z.ai coding plans - 10% OFF coupon" src="https://img.shields.io/badge/z.ai%20coding%20plans-10%25%20OFF%20coupon-blueviolet" /></a>
  <a href="https://zcode.z.ai/invite/ALWM9JUA"><img alt="Try ZCode free" src="https://img.shields.io/badge/Try%20ZCode-free%20invite-0969da" /></a>
</p>

## License

MIT.
