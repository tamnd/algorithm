---
tag: KV05KE
kind: technique
slug: devirtualization
name: Devirtualization
aliases:
- call site specialization
area: compilers-and-program-analysis/optimizations
level: core
summary: Replaces a virtual or indirect call by a direct call when analysis shows one target, often guarded by a type test.
---

Replaces a virtual or indirect call by a direct call when analysis shows one target, often guarded by a type test.
