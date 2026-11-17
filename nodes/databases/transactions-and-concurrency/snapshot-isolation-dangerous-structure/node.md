---
tag: Q5KMJR
kind: theorem
slug: snapshot-isolation-dangerous-structure
name: Dangerous structure theorem
aliases:
- Fekete snapshot isolation theorem
- consecutive rw-antidependencies theorem
area: databases/transactions-and-concurrency
level: advanced
summary: Every non-serializable execution under snapshot isolation has two consecutive read-write antidependency edges between concurrent transactions.
---

Every non-serializable execution under snapshot isolation has two consecutive read-write antidependency edges between concurrent transactions.
