---
tag: JVVDBX
kind: algorithm
slug: escape-analysis
name: Escape analysis
aliases:
- escape analysis for objects
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Finds objects that do not outlive their method or thread, so they can be put on the stack and their locks removed.
---

Finds objects that do not outlive their method or thread, so they can be put on the stack and their locks removed.
