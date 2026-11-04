---
tag: R3QGVQ
kind: concept
slug: open-nested-transactions
name: Open nested transactions
aliases:
- open nesting
area: concurrency/transactional-memory
level: research
summary: Inner transactions commit their effects early, so each needs a compensating action if the outer one aborts.
---

Inner transactions commit their effects early, so each needs a compensating action if the outer one aborts.
