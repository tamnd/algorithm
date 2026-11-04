---
tag: 83B4J8
kind: data-structure
slug: lcrq
name: LCRQ (linked concurrent ring queue)
aliases:
- linked concurrent ring queue
area: data-structures/concurrent-structures
level: research
summary: Queue built from linked fetch-and-add ring buffers, avoiding CAS retry loops on the hot ends.
---

Queue built from linked fetch-and-add ring buffers, avoiding CAS retry loops on the hot ends.
