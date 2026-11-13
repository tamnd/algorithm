---
tag: 8CBACT
kind: technique
slug: terminal-propagation
name: Terminal propagation
aliases:
- Dunlop-Kernighan terminal propagation
area: cad/partitioning-floorplanning-and-placement
level: core
summary: In min-cut placement, adds a fixed dummy terminal for each net with cells outside the region, so the partitioner sees the pull of those cells.
---

In min-cut placement, adds a fixed dummy terminal for each net with cells outside the region, so the partitioner sees the pull of those cells.
