---
tag: 2R0MXX
kind: algorithm
slug: dangling-pointer-nullification
name: Dangling pointer nullification
aliases:
- DangNull
area: security-and-privacy/memory-safety-defenses
level: research
summary: Tracks which pointers refer to each object and sets them all to null when the object is freed, so use after free faults safely.
---

Tracks which pointers refer to each object and sets them all to null when the object is freed, so use after free faults safely.
