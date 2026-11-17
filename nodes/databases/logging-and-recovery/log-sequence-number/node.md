---
tag: D6MZ35
kind: definition
slug: log-sequence-number
name: Log sequence number
aliases:
- LSN
- pageLSN
area: databases/logging-and-recovery
level: core
summary: A monotone address of a log record; each page stores the LSN of its last update so recovery knows which updates it already holds.
---

A monotone address of a log record; each page stores the LSN of its last update so recovery knows which updates it already holds.
