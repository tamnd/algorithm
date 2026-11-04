---
tag: DZSEHS
kind: concept
slug: lowest-set-bit
name: Lowest set bit
aliases:
- isolating the lowest set bit
- x & -x
- rightmost set bit
area: techniques/bit-tricks
level: intro
summary: The value x & -x isolates the least significant 1-bit of x; x & (x-1) clears it.
---

The value x & -x isolates the least significant 1-bit of x; x & (x-1) clears it.
