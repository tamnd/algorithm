---
tag: KMWYHF
kind: technique
slug: borrow-checking
name: Borrow checking
aliases:
- ownership and borrowing
- non-lexical lifetimes
area: compilers-and-program-analysis/type-systems-and-inference
level: research
summary: Checks that each reference to owned memory lives no longer than its owner and that no mutable reference is aliased, without a garbage collector.
---

Checks that each reference to owned memory lives no longer than its owner and that no mutable reference is aliased, without a garbage collector.
