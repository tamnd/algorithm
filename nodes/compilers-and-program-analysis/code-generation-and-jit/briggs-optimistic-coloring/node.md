---
tag: Y67E03
kind: algorithm
slug: briggs-optimistic-coloring
name: Optimistic coloring
aliases:
- Chaitin-Briggs allocator
- Briggs allocator
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Pushes a spill candidate on the stack instead of spilling it at once and spills only if no color is free when it is popped.
---

Pushes a spill candidate on the stack instead of spilling it at once and spills only if no color is free when it is popped.
