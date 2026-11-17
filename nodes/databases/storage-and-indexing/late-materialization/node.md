---
tag: DADXAP
kind: technique
slug: late-materialization
name: Late materialization
aliases:
- late tuple reconstruction
area: databases/storage-and-indexing
level: advanced
summary: In a column store, pass row positions through the plan and fetch the other columns of a row only when an operator needs them.
---

In a column store, pass row positions through the plan and fetch the other columns of a row only when an operator needs them.
