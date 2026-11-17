---
tag: TE6F11
kind: algorithm
slug: tiled-shading
name: Tiled shading
aliases:
- tiled light culling
- Forward+
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Split the screen into tiles, cull the lights against each tile's depth bounds in a compute pass, and shade each pixel with its tile's light list.
---

Split the screen into tiles, cull the lights against each tile's depth bounds in a compute pass, and shade each pixel with its tile's light list.
