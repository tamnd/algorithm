---
tag: CVDNZN
kind: technique
slug: tail-call-optimization
name: Tail call optimization
aliases:
- tail call elimination
- proper tail calls
area: compilers-and-program-analysis/optimizations
level: core
summary: Compiles a call in tail position as a jump that reuses the caller's frame, so tail recursion runs in constant stack space.
---

Compiles a call in tail position as a jump that reuses the caller's frame, so tail recursion runs in constant stack space.
