---
tag: XHDB2T
kind: technique
slug: deferred-view-maintenance
name: Deferred view maintenance
aliases:
- lazy view maintenance
- deferred refresh
area: databases/stream-and-incremental-processing
level: advanced
summary: Record base changes in logs and bring a materialized view up to date later, at query time or on a schedule, not in each update.
---

Record base changes in logs and bring a materialized view up to date later, at query time or on a schedule, not in each update.
