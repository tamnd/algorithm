---
tag: Q67BT1
kind: technique
slug: threaded-code
name: Threaded code
aliases:
- direct threading
- indirect threading
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Represents an interpreted program as a list of addresses of routines, each ending with a jump to the next, to cut dispatch cost.
---

Represents an interpreted program as a list of addresses of routines, each ending with a jump to the next, to cut dispatch cost.
