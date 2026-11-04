---
tag: WERYMV
kind: algorithm
slug: fixed-window-counter
name: Fixed window counter
aliases:
- fixed window rate limiter
area: systems/rate-limiting
level: intro
summary: Counts requests per aligned time window and resets at each boundary; cheap but allows double bursts at edges.
---

Counts requests per aligned time window and resets at each boundary; cheap but allows double bursts at edges.
