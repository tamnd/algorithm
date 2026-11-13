---
tag: 3XKRGT
kind: technique
slug: loop-unrolling
name: Loop unrolling
aliases:
- loop unwinding
area: compilers-and-program-analysis/loop-transformations
level: intro
summary: Replicates the body of a loop k times and divides the trip count by k, which cuts branch overhead and exposes instruction parallelism.
---

Replicates the body of a loop k times and divides the trip count by k, which cuts branch overhead and exposes instruction parallelism.
