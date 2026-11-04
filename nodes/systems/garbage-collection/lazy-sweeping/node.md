---
tag: 60PT1Y
kind: technique
slug: lazy-sweeping
name: Lazy sweeping
aliases:
- lazy sweep
area: systems/garbage-collection
level: advanced
summary: Defer the sweep phase, sweeping each block only when the allocator needs it.
---

Defer the sweep phase, sweeping each block only when the allocator needs it.
