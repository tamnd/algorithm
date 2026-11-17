---
tag: 81GP9H
kind: algorithm
slug: baggy-bounds-checking
name: Baggy bounds checking
aliases:
- baggy bounds
area: security-and-privacy/memory-safety-defenses
level: advanced
summary: Pads each allocation to a power of two and stores its log size in a compact table, so that bounds checks need one lookup.
---

Pads each allocation to a power of two and stores its log size in a compact table, so that bounds checks need one lookup.
