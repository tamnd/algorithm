---
tag: MES4WN
kind: algorithm
slug: map-side-join
name: Map-side join
aliases:
- broadcast join
- replicated join
- fragment-replicate join
area: parallel/mapreduce-and-bsp
level: core
summary: Replicate a small relation to every mapper and join locally, avoiding the shuffle for that side.
---

Replicate a small relation to every mapper and join locally, avoiding the shuffle for that side.
