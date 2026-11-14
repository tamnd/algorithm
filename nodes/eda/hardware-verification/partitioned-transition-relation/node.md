---
tag: NQG9VW
kind: technique
slug: partitioned-transition-relation
name: Partitioned transition relation
aliases:
- early quantification
- conjunctive partitioning
area: eda/hardware-verification
level: advanced
summary: Keeps the transition relation as a list of BDD conjuncts and quantifies each variable as soon as no later conjunct uses it, so image computation stays small.
---

Keeps the transition relation as a list of BDD conjuncts and quantifies each variable as soon as no later conjunct uses it, so image computation stays small.
