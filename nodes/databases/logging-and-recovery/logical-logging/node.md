---
tag: 2G2F02
kind: technique
slug: logical-logging
name: Logical logging
aliases:
- operation logging
area: databases/logging-and-recovery
level: core
summary: Log the high-level operation, such as insert this key, instead of the bytes changed, so undo can work on a page that has since changed.
---

Log the high-level operation, such as insert this key, instead of the bytes changed, so undo can work on a page that has since changed.
