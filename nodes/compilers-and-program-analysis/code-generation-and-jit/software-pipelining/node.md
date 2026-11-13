---
tag: 3SECX7
kind: technique
slug: software-pipelining
name: Software pipelining
aliases:
- loop pipelining
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Overlaps iterations of a loop so that a new iteration starts before the previous ends, with a prologue, steady kernel and epilogue.
---

Overlaps iterations of a loop so that a new iteration starts before the previous ends, with a prologue, steady kernel and epilogue.
