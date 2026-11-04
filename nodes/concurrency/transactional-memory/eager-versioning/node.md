---
tag: ZAQJVK
kind: concept
slug: eager-versioning
name: Eager versioning
aliases:
- direct update
- in-place update
area: concurrency/transactional-memory
level: advanced
summary: Writes are applied to memory in place, with an undo log that restores old values on abort.
---

Writes are applied to memory in place, with an undo log that restores old values on abort.
