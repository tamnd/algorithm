---
tag: EPC3SV
kind: technique
slug: inline-caching
name: Inline caching
aliases:
- inline cache
- Deutsch-Schiffman inline cache
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Caches at each call site the receiver type and method found last time and checks the type on the next call before using it.
---

Caches at each call site the receiver type and method found last time and checks the type on the next call before using it.
