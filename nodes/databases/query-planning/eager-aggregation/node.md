---
tag: B4N0ZP
kind: technique
slug: eager-aggregation
name: Eager aggregation
aliases:
- group-by pushdown
- aggregation pushdown
area: databases/query-planning
level: advanced
summary: Move a grouping below a join when the conditions of Yan and Larson hold, so the join works on fewer rows.
---

Move a grouping below a join when the conditions of Yan and Larson hold, so the join works on fewer rows.
