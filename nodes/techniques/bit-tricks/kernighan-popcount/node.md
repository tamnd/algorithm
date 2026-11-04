---
tag: TVK2SZ
kind: algorithm
slug: kernighan-popcount
name: Kernighan's bit count
aliases:
- Brian Kernighan's method
- clear lowest set bit loop
area: techniques/bit-tricks
level: intro
summary: Repeatedly clears the lowest set bit with x &= x-1, so it runs in time proportional to the number of 1-bits.
---

Repeatedly clears the lowest set bit with x &= x-1, so it runs in time proportional to the number of 1-bits.
