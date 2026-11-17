---
tag: 4YEZ3N
kind: technique
slug: gravitational-softening
name: Gravitational softening
aliases:
- Plummer softening
- softening length
area: scientific-computing/n-body-and-particle-methods
level: core
summary: Replaces the 1/r^2 force by one with 1/(r^2 + eps^2) so close encounters need no tiny time steps; eps sets the smallest resolved scale.
---

Replaces the 1/r^2 force by one with 1/(r^2 + eps^2) so close encounters need no tiny time steps; eps sets the smallest resolved scale.
