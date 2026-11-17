---
tag: NYGPH2
kind: algorithm
slug: lock-and-key-temporal-checking
name: Lock and key temporal checking
aliases:
- CETS
- compiler-enforced temporal safety
area: security-and-privacy/memory-safety-defenses
level: advanced
summary: Gives each allocation a unique key and lock, copies the key with each pointer, and checks that the lock still holds the key at each access.
---

Gives each allocation a unique key and lock, copies the key with each pointer, and checks that the lock still holds the key at each access.
