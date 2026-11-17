---
tag: 80XPYE
kind: technique
slug: write-behind-logging
name: Write-behind logging
aliases:
- WBL
area: databases/logging-and-recovery
level: research
summary: A protocol for non-volatile memory that writes data first and logs only commit timestamp ranges, so recovery needs no redo.
---

A protocol for non-volatile memory that writes data first and logs only commit timestamp ranges, so recovery needs no redo.
