---
tag: G8X0J3
kind: algorithm
slug: xor-swap
name: XOR swap
aliases:
- XOR swap algorithm
- exclusive-or swap
area: techniques/bit-tricks
level: intro
summary: Swapping x and y with three XORs, x ^= y, y ^= x, x ^= y, without a temporary; fails if x and y alias the same location.
---

Swapping x and y with three XORs, x ^= y, y ^= x, x ^= y, without a temporary; fails if x and y alias the same location.
