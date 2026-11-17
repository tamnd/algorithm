---
tag: 2XEK6A
kind: definition
slug: compensation-log-record
name: Compensation log record
aliases:
- CLR
area: databases/logging-and-recovery
level: core
summary: A redo-only log record written when an update is undone, which points to the next record to undo so rollback is never repeated.
---

A redo-only log record written when an update is undone, which points to the next record to undo so rollback is never repeated.
