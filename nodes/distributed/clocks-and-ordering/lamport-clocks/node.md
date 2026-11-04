---
tag: R8TGNF
kind: algorithm
slug: lamport-clocks
name: Lamport logical clocks
aliases:
- Lamport timestamps
- scalar logical clocks
area: distributed/clocks-and-ordering
level: intro
summary: Each process keeps a counter, increments it per event and attaches it to messages; the max rule keeps it consistent with causality.
---

Each process keeps a counter, increments it per event and attaches it to messages; the max rule keeps it consistent with causality.
