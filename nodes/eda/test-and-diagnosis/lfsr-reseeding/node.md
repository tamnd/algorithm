---
tag: NQ6987
kind: technique
slug: lfsr-reseeding
name: LFSR reseeding
aliases:
- Koenemann reseeding
area: eda/test-and-diagnosis
level: advanced
summary: Koenemann's test compression that stores a seed per test cube and expands it with an LFSR, the seed found by solving linear equations over GF(2) for the care bits.
---

Koenemann's test compression that stores a seed per test cube and expands it with an LFSR, the seed found by solving linear equations over GF(2) for the care bits.
