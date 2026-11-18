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
prereqs: [iterator-model, query-plan]
see_also: [exchange-operator, data-centric-query-compilation, vectorized-query-execution, morsel-driven-parallelism, sort-based-aggregation, hash-join, symmetric-hash-join, materialized-view]
sources:
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 73 to 169 (1993)
    locator: the discussion of the iterator interface, of pipelining between operators and of temporary files for intermediate results
  - paper: doi:10.14778/2002938.2002940
    title: Thomas Neumann, Efficiently compiling efficient query plans for modern hardware, Proceedings of the VLDB Endowment 4(9), 539 to 550 (2011)
    locator: the definition of a pipeline breaker and a full pipeline breaker
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Chapters 15 and 16 (iterators, and pipelining against materialization in physical query plans)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 12 (pipelined evaluation and the iterator interface)
---

In a [query plan](/query-plan/), the result of one operator is the input of the next. With pipelining, each tuple goes to the next operator as soon as it is made, and no intermediate result is stored. With materialization, the whole result of a subplan is stored first, in memory or in a temporary file, and the next operator reads it later. Some operators, such as a sort or the build side of a [hash join](/hash-join/), must read all of an input before they give any output, so they cut the plan into pipelines whatever the engine does.

## In plain words

Think of a kitchen. One cook cuts vegetables and hands each piece to the next cook, who puts it in the pan at once. Nothing waits on the table. That is pipelining. Now the second cook wants all pieces sorted by size before she starts. She must wait until the first cook has cut everything, and the pieces pile up on the table. That pile is materialization. Some steps always make a pile, like sorting. Other piles you make on purpose, for example when two dishes need the same cut vegetables, so you cut them once and keep them.

## The idea

**Pipelining.** Two operators are pipelined when the consumer takes each tuple of the producer as it comes, and the tuple is never written to a stored intermediate result. In the [iterator model](/iterator-model/), this happens by itself: the parent calls NEXT, and the child gives one tuple. In a push-based engine, the producer calls the consumer for each tuple. The space for an edge of the plan is then bounded by one tuple or one batch, and not by the size of the result.

**Blocking operators.** An operator is blocking on an input if it cannot give its first output tuple before it has read all of that input. Neumann (2011) states it at the level of the CPU: an operator is a pipeline breaker for an input side if it takes an incoming tuple out of the CPU registers, and a full pipeline breaker if it materializes all incoming tuples from that side before it goes on. The usual full pipeline breakers are:

- a sort, on its input;
- the build side of a hash join, which fills the hash table;
- [hash aggregation](/hash-aggregation/) and [sort-based aggregation](/sort-based-aggregation/) on unsorted input, since no group is final before the end;
- duplicate elimination by hashing or sorting, and the set operations built on it.

Selection, projection without duplicate removal, the probe side of a hash join, the outer side of a nested-loop join and aggregation over input sorted on the key are not blocking.

**Pipelines.** Cut each edge of the plan that enters a full pipeline breaker on its blocking side. The parts that are left are the pipelines. Inside a pipeline, tuples flow from one source (a scan, or the stored result of a breaker) to one sink (a breaker, or the output). A pipeline can start only after the pipelines that fill its sources are done, so the pipelines form a dependency graph, and the engine runs them in an order that fits it.

**Cost.** In the page I/O model, writing an intermediate result of $k$ pages to a temporary file and reading it again costs $2k$ I/Os, which pipelining saves. In memory, a pipeline also keeps the hot tuple in cache or in registers between operators. The price of pipelining is memory: all operators of a pipeline run at the same time, so their hash tables and buffers must fit in memory together. A blocking operator on the boundary of two pipelines holds its full state until the next pipeline has read it.

**When materialization is better.**

- **Reuse.** A result that is read more than once, such as a common subexpression or the inner input of a nested-loop join, is stored once and read many times, in place of being computed again for each use.
- **Memory.** If several hash tables in one pipeline do not fit in memory at the same time, storing an intermediate result splits the pipeline and frees memory.
- **Restart.** A stored result is a point to restart from after a failure. MapReduce writes the output of each map task to disk before the reduce tasks read it, so a failed reduce task does not run the map tasks again.
- **Different speeds.** A buffer between a fast producer and a slow consumer lets each run at its own speed for a while, as in the [exchange operator](/exchange-operator/), which keeps buffers between processes.

## Examples

**A pipelined plan with three pipelines.** Take $\gamma_{a;\,\text{SUM}(b)}(\sigma_p(R) \bowtie S)$, with a hash join that builds on $S$ and a hash aggregation on top. Pipeline 1 scans $S$ and fills the hash table of the join. Pipeline 2 scans $R$, applies $\sigma_p$, probes the hash table and updates the aggregation table, all for one tuple at a time. Pipeline 3 reads the aggregation table and returns the groups. Pipeline 2 needs both tables in memory at once. If $\sigma_p(R)$ has 100 pages and the join result has 200 pages, a fully materialized engine writes and reads both, which costs $2 \cdot 100 + 2 \cdot 200 = 600$ more I/Os than this plan.

**A chain of hash joins.** In a left-deep plan $((R \bowtie S) \bowtie T) \bowtie U$ that builds on $S$, $T$ and $U$, one pipeline streams $R$ through all three hash tables, and three short pipelines build them first. A plan that builds the hash table of a join on an intermediate result, such as $R \bowtie S$, must store that whole result in the table, so it has one more full pipeline breaker.

**Sort and merge join.** An external sort is blocking on its input, but its final merge pass can feed a [sort-merge join](/sort-merge-join/) one tuple at a time. The sort writes its runs, and the last merge is not written.

**A sorted input.** Aggregation over input that comes sorted on the grouping key is not blocking: a group is final when the key changes. The same query on unsorted input has a full pipeline breaker at the aggregation.

**A non-example: LIMIT over a sort.** LIMIT 1 over a scan stops after one tuple. LIMIT 1 over a sort still reads the whole input, because the sort is blocking. Pipelining above a breaker does not save the work below it.

**A non-example: a materialized view.** A [materialized view](/materialized-view/) is a stored query result that lives across queries and must be kept up to date. Materialization in this page is a temporary result inside one query plan, which is thrown away at the end of the query.

## Where it is used

- **Volcano-style engines.** The iterator model gives pipelining by default, and operators that need their whole input read it in OPEN. Spool or temporary-table operators store a result when it is read again.
- **Compiled engines.** [Data-centric query compilation](/data-centric-query-compilation/) turns each pipeline into one loop and places code at the full pipeline breakers, so the boundaries of the pipelines decide the shape of the generated code.
- **Vectorized engines.** [Vectorized execution](/vectorized-query-execution/) pipelines batches of values, so the space of an edge is one batch.
- **Parallel engines.** [Morsel-driven parallelism](/morsel-driven-parallelism/) schedules the work of one pipeline at a time, in small pieces, and synchronizes the threads only at the full pipeline breakers. The exchange operator inserts buffers between pipelined parts that run in different processes.
- **Streams.** A stream join such as the [symmetric hash join](/symmetric-hash-join/) is pipelined on both inputs, so it can give results before either input ends.
- **SQL.** Common table expressions can be computed once and stored, or merged into the query and pipelined. PostgreSQL 12 and later let the query choose with `MATERIALIZED` and `NOT MATERIALIZED`.

## References
