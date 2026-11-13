---
tag: FMPTMB
kind: technique
slug: loop-tiling
name: Loop tiling
aliases:
- loop blocking
- cache blocking
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Splits the iteration space of a nest into blocks that fit in cache and runs each block fully, for data reuse and parallelism.
---

Splits the iteration space of a nest into blocks that fit in cache and runs each block fully, for data reuse and parallelism.
