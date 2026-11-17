---
tag: XNDHHS
kind: algorithm
slug: parallel-hash-join
name: Parallel hash join
aliases:
- partitioned parallel hash join
- Gamma hash join
area: databases/distributed-databases
level: core
summary: Hash-partition both inputs across the nodes on the join key, then let each node join its pair of partitions locally.
---

Hash-partition both inputs across the nodes on the join key, then let each node join its pair of partitions locally.
