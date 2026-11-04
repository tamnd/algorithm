---
tag: TTCF1W
kind: technique
slug: double-buffering
name: Double buffering
aliases:
- read-ahead buffering
- overlapped I/O
area: sorting/external-sorting
level: intro
summary: Overlap I/O on one buffer with computation on another so that merging does not stall on disk reads.
---

Overlap I/O on one buffer with computation on another so that merging does not stall on disk reads.
