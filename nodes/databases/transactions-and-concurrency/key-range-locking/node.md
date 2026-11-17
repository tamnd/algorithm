---
tag: VVNHG6
kind: algorithm
slug: key-range-locking
name: Key-range locking
aliases:
- next-key locking
- ARIES/KVL
area: databases/transactions-and-concurrency
level: advanced
summary: Lock index keys together with the gap to the next key, so that a range scan stops phantoms without locking a predicate.
---

Lock index keys together with the gap to the next key, so that a range scan stops phantoms without locking a predicate.
