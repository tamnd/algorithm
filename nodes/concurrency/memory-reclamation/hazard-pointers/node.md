---
tag: 319C81
kind: algorithm
slug: hazard-pointers
name: Hazard pointers
aliases:
- Michael's hazard pointers
area: concurrency/memory-reclamation
level: core
summary: Readers publish the pointers they access; a retired node is freed only if no hazard pointer names it.
---

Readers publish the pointers they access; a retired node is freed only if no hazard pointer names it.
