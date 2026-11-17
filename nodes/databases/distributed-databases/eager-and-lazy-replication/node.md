---
tag: HN9ERD
kind: concept
slug: eager-and-lazy-replication
name: Eager and lazy replication
aliases:
- lazy replication
- eager replication
area: databases/distributed-databases
level: core
summary: Eager replication updates all copies inside the transaction, lazy replication after it commits; Gray et al. showed eager deadlocks grow fast with scale.
---

Eager replication updates all copies inside the transaction, lazy replication after it commits; Gray et al. showed eager deadlocks grow fast with scale.
