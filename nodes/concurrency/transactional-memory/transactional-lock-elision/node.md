---
tag: 70FJV6
kind: technique
slug: transactional-lock-elision
name: Transactional lock elision
aliases:
- TLE
- speculative lock elision
- lock elision
area: concurrency/transactional-memory
level: advanced
summary: Runs a lock's critical section as a hardware transaction, falling back to actually taking the lock on abort.
---

Runs a lock's critical section as a hardware transaction, falling back to actually taking the lock on abort.
