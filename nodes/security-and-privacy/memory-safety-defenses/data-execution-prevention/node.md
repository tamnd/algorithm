---
tag: NS1DRS
kind: technique
slug: data-execution-prevention
name: Data execution prevention
aliases:
- W xor X
- non-executable memory
area: security-and-privacy/memory-safety-defenses
level: intro
summary: Marks each page either writable or executable but never both, so that injected data cannot run as code.
---

Marks each page either writable or executable but never both, so that injected data cannot run as code.
