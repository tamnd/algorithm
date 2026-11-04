---
tag: 714B67
kind: technique
slug: warp-aggregated-atomics
name: Warp-aggregated atomics
aliases:
- warp-level atomic aggregation
area: parallel/gpu-algorithms
level: advanced
summary: Threads in a warp combine their atomic updates into one atomic per warp to reduce contention.
---

Threads in a warp combine their atomic updates into one atomic per warp to reduce contention.
