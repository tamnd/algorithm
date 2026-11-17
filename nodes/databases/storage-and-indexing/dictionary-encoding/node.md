---
tag: 4407VK
kind: technique
slug: dictionary-encoding
name: Dictionary encoding
aliases:
- order-preserving dictionary encoding
- domain encoding
area: databases/storage-and-indexing
level: core
summary: Replace each value of a column by a small integer code from a dictionary of its distinct values; ordered codes keep range predicates.
---

Replace each value of a column by a small integer code from a dictionary of its distinct values; ordered codes keep range predicates.
