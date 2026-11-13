---
tag: CR25E3
kind: algorithm
slug: document-at-a-time-evaluation
name: Document-at-a-time evaluation
aliases:
- DAAT
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Reads all query posting lists in parallel in docid order and scores each document fully before moving on, keeping a heap of the best k.
---

Reads all query posting lists in parallel in docid order and scores each document fully before moving on, keeping a heap of the best k.
