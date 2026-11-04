---
tag: V66CR9
kind: technique
slug: lock-striping
name: Lock striping
aliases:
- lock splitting
area: data-structures/concurrent-structures
level: core
summary: Partition a structure into segments each guarded by its own lock, so operations on different stripes run in parallel.
---

Partition a structure into segments each guarded by its own lock, so operations on different stripes run in parallel.
