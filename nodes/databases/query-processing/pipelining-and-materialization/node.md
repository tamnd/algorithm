---
tag: BE56FT
kind: concept
slug: pipelining-and-materialization
name: Pipelining and materialization
aliases:
- pipeline breaker
- pipelined execution
area: databases/query-processing
level: core
summary: Operators either pass tuples to the next operator as they are produced or write a full intermediate result; blocking operators break pipelines.
---

Operators either pass tuples to the next operator as they are produced or write a full intermediate result; blocking operators break pipelines.
