---
tag: 10RK1C
kind: definition
slug: control-dependence
name: Control dependence
aliases:
- control dependence graph
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Node n is control dependent on branch b if one edge out of b forces n to run and another can skip it, found from post-dominance frontiers.
---

Node n is control dependent on branch b if one edge out of b forces n to run and another can skip it, found from post-dominance frontiers.
