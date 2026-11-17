---
tag: 2VN9MN
kind: algorithm
slug: symmetric-hash-join
name: Symmetric hash join
aliases:
- pipelined hash join
- double pipelined hash join
area: databases/stream-and-incremental-processing
level: core
summary: Keep a hash table for each input; each arriving tuple is inserted in its own table and probes the other, producing results at once.
---

Keep a hash table for each input; each arriving tuple is inserted in its own table and probes the other, producing results at once.
