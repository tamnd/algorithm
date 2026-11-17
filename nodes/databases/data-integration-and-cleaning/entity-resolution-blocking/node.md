---
tag: EEW6T2
kind: technique
slug: entity-resolution-blocking
name: Blocking for entity resolution
aliases:
- record blocking
- standard blocking
area: databases/data-integration-and-cleaning
level: core
summary: Group records by cheap keys and compare only pairs within the same block, which avoids the quadratic number of comparisons.
---

Group records by cheap keys and compare only pairs within the same block, which avoids the quadratic number of comparisons.
