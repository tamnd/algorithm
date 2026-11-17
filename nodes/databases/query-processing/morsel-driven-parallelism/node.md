---
tag: DJF10W
kind: technique
slug: morsel-driven-parallelism
name: Morsel-driven parallelism
aliases:
- morsel-wise scheduling
area: databases/query-processing
level: research
summary: Split the input of each pipeline into small morsels that worker threads take dynamically, which balances load on many cores.
---

Split the input of each pipeline into small morsels that worker threads take dynamically, which balances load on many cores.
