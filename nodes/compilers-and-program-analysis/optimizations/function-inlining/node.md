---
tag: H29A5E
kind: technique
slug: function-inlining
name: Function inlining
aliases:
- inline expansion
- procedure integration
area: compilers-and-program-analysis/optimizations
level: core
summary: Replaces a call by a copy of the body of the callee, which removes call overhead and exposes the body to optimization at the call site.
---

Replaces a call by a copy of the body of the callee, which removes call overhead and exposes the body to optimization at the call site.
