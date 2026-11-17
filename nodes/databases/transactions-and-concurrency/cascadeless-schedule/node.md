---
tag: E7X2PT
kind: definition
slug: cascadeless-schedule
name: Cascadeless schedule
aliases:
- ACA schedule
- avoiding cascading aborts
area: databases/transactions-and-concurrency
level: core
summary: A schedule in which transactions read only values written by committed transactions, so one abort never forces another.
---

A schedule in which transactions read only values written by committed transactions, so one abort never forces another.
