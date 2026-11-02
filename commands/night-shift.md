---
description: Run queued overnight tasks under the auto-approval policy (safe, ask, park tiers), or render the digest
allowed-tools: Read, Bash, Write, Edit, Grep, Glob, Agent
argument-hint: [run | digest]
---
Invoke the `night-shift` skill with this input: **$ARGUMENTS**

With "digest" (or empty args), render the morning report from the run log and
stop (groups asked tasks separately). With "run", execute the queue under the
policy: safe ops proceed, ask-tier ops stop with an `ASK: <what and why>`
line and "asked" status, the rest park.
