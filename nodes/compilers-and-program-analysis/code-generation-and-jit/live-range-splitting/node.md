---
tag: NYNRRJ
kind: technique
slug: live-range-splitting
name: Live range splitting
aliases:
- range splitting
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Splits the live range of a value into pieces with copies between them, so each piece can get its own register or be spilled.
---

Splits the live range of a value into pieces with copies between them, so each piece can get its own register or be spilled.
