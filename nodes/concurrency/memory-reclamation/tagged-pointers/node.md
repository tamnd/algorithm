---
tag: 6NM0K3
kind: technique
slug: tagged-pointers
name: Tagged pointers (version counters)
aliases:
- Tagged pointers
- counted pointers
- version tags
- version-tagged pointers
area: concurrency/memory-reclamation
level: core
summary: Pair a pointer with a counter so that CAS detects intervening updates and mitigates ABA.
---

Pair a pointer with a counter so that CAS detects intervening updates and mitigates ABA.
