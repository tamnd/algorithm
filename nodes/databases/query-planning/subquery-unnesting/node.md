---
tag: 0C9G7B
kind: technique
slug: subquery-unnesting
name: Subquery unnesting
aliases:
- subquery decorrelation
- query unnesting
area: databases/query-planning
level: core
summary: Rewrite a correlated nested subquery as a join or an outer join with grouping, so that it is evaluated once instead of once per row.
---

Rewrite a correlated nested subquery as a join or an outer join with grouping, so that it is evaluated once instead of once per row.
