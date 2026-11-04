---
tag: M62E1N
kind: concept
slug: aba-problem
name: ABA problem
aliases:
- ABA
- ABA hazard
area: concurrency/memory-reclamation
level: intro
summary: A CAS succeeds although the location changed A to B and back to A, so the comparison is misled.
---

A CAS succeeds although the location changed A to B and back to A, so the comparison is misled.
