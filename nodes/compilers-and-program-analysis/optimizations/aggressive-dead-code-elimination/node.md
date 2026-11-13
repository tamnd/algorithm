---
tag: VFFWX5
kind: algorithm
slug: aggressive-dead-code-elimination
name: Aggressive dead code elimination
aliases:
- ADCE
- mark-sweep dead code elimination
area: compilers-and-program-analysis/optimizations
level: core
summary: Marks instructions with side effects as live, then marks what they depend on through data and control dependence, and deletes the rest.
---

Marks instructions with side effects as live, then marks what they depend on through data and control dependence, and deletes the rest.
