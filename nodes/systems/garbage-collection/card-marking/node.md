---
tag: 45B69W
kind: technique
slug: card-marking
name: Card marking
aliases:
- card table
- card-based remembered set
area: systems/garbage-collection
level: advanced
summary: Divide the heap into cards and mark dirty cards on writes to track old-to-young pointers.
---

Divide the heap into cards and mark dirty cards on writes to track old-to-young pointers.
