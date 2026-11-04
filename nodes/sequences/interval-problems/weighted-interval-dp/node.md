---
tag: YZT11N
kind: algorithm
slug: weighted-interval-dp
name: Weighted interval scheduling dynamic programming
aliases:
- Weighted interval DP with binary search predecessors
area: sequences/interval-problems
level: core
summary: Sort by finish time, compute predecessors, and use the recurrence OPT(j)=max(OPT(j-1), w_j+OPT(p(j))).
---

Sort by finish time, compute predecessors, and use the recurrence OPT(j)=max(OPT(j-1), w_j+OPT(p(j))).
