---
tag: A84DF7
kind: algorithm
slug: local-register-allocation
name: Local register allocation
aliases:
- bottom-up local allocation
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Allocates registers in one basic block in order, and when none is free spills the value whose next use is farthest away.
---

Allocates registers in one basic block in order, and when none is free spills the value whose next use is farthest away.
