---
tag: JW00TB
kind: technique
slug: vectorized-query-execution
name: Vectorized query execution
aliases:
- vector-at-a-time execution
- X100 execution model
area: databases/query-processing
level: advanced
summary: Operators exchange batches of column values instead of single tuples, which amortizes call overhead and lets tight loops use SIMD.
---

Operators exchange batches of column values instead of single tuples, which amortizes call overhead and lets tight loops use SIMD.
