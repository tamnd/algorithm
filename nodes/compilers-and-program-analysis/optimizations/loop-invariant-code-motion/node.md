---
tag: T991RF
kind: technique
slug: loop-invariant-code-motion
name: Loop-invariant code motion
aliases:
- LICM
- hoisting
area: compilers-and-program-analysis/optimizations
level: intro
summary: Moves computations whose operands do not change inside a loop to a preheader before the loop, when this is safe.
---

Moves computations whose operands do not change inside a loop to a preheader before the loop, when this is safe.
