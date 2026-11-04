---
tag: 0AQA6S
kind: technique
slug: read-copy-update
name: Read-copy-update
aliases:
- RCU
area: concurrency/memory-reclamation
level: core
summary: Readers run without locks, writers copy and publish, and the old version is freed after a grace period.
---

Readers run without locks, writers copy and publish, and the old version is freed after a grace period.
