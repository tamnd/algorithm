---
tag: JFFV0J
kind: technique
slug: data-centric-query-compilation
name: Data-centric query compilation
aliases:
- produce-consume code generation
- push-based compiled execution
area: databases/query-processing
level: advanced
summary: Compile each pipeline of a plan into one tight loop that pushes tuples through its operators, keeping values in registers.
---

Compile each pipeline of a plan into one tight loop that pushes tuples through its operators, keeping values in registers.
