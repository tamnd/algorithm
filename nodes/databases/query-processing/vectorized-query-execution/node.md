---
tag: JW00TB
kind: technique
slug: vectorized-query-execution
name: Vectorized query execution
aliases:
- vector-at-a-time execution
- X100 execution model
area: databases/query-processing
level: advanced
summary: Operators exchange batches of column values instead of single tuples, which amortizes call overhead and lets tight loops use SIMD.
prereqs: [iterator-model, decomposition-storage-model]
see_also: [data-centric-query-compilation, pipelining-and-materialization, morsel-driven-parallelism, late-materialization, vectorization, loop-fusion, hash-aggregation, dictionary-encoding]
sources:
  - url: https://www.cidrdb.org/cidr2005/papers/P19.pdf
    title: Peter Boncz, Marcin Zukowski and Niels Nes, MonetDB/X100, hyper-pipelining query execution, Proceedings of CIDR 2005, 225 to 237
    locator: Section 3 (TPC-H Query 1 on MySQL, a commercial system and MonetDB/MIL), Section 4 (the X100 vectorized engine) and Section 5.1.1 (the effect of the vector size, Figure 10)
  - paper: doi:10.14778/3275366.3275370
    title: Timo Kersten, Viktor Leis, Alfons Kemper, Thomas Neumann, Andrew Pavlo and Peter Boncz, Everything you always wanted to know about compiled and vectorized queries but were afraid to ask, Proceedings of the VLDB Endowment 11(13), 2209 to 2222 (2018)
    locator: the comparison of the Tectorwise and Typer engines (Table 3 for TPC-H at scale factor 100 on one thread)
  - paper: doi:10.1109/69.273032
    title: Goetz Graefe, Volcano, an extensible and parallel query evaluation system, IEEE Transactions on Knowledge and Data Engineering 6(1), 120 to 135 (1994)
    locator: the tuple-at-a-time iterator interface that vectorized engines change
---

Vectorized query execution keeps the operator tree and the open, next and close calls of the [iterator model](/iterator-model/), but each call of next returns a batch of about a thousand tuples, stored as one array (a vector) per column. Each operator does its work with primitives, short loops that apply one operation to a whole vector, such as "compare every value with a constant" or "multiply two vectors". The cost of the call and of interpreting the plan is then paid once per vector and not once per tuple, and the loops are simple enough for the compiler to unroll and to turn into SIMD instructions. Boncz, Zukowski and Nes introduced the model in the MonetDB/X100 engine (2005), which later became the commercial system Vectorwise.

## In plain words

A cashier scans one item, prints a line, asks the next person a question, and then scans the next item. Most of the time goes to the asking and printing, not to the scanning. Now he takes a full basket at a time. He scans all items in one go, then prints all lines in one go. The work per item is the same, but the small costs around each item are paid once per basket. The basket must not be too big, or it does not fit on the counter and he walks back and forth. In a database, the basket is a vector of values, and the counter is the CPU cache.

## When it applies

- The data is in memory or in a fast cache, so the CPU and not the disk decides the speed. On disk-bound plans the per-tuple cost of the iterator model hides behind the I/O.
- The plan does the same few operations on many rows: scans, filters, arithmetic, hash joins and aggregations over large tables, as in analytic queries.
- The data is stored by column, as in the [decomposition storage model](/decomposition-storage-model/), so a vector of one column can be read as one array.
- The engine should stay an interpreter, with no code generation while the query runs. Every primitive is compiled ahead of time, once for each type.

## The template

A batch holds up to $K$ positions, one vector per column, and a selection vector with the positions that are still live. Filters shorten the selection vector and leave the column vectors as they are.

```pseudo id=main
NEXT(op)                                   ▷ returns a batch of at most K tuples, or EOF
L1  b ← NEXT(child of op)
L2  if b = EOF then return EOF
L3  for each primitive P of op, in order do P(b)      ▷ hole: the work of op as loops over vectors
L4  return b
SELECT-LESS(b, col, c)                     ▷ a filter primitive: keep the live positions with col < c
L5  j ← 0
L6  for i ← 0 to |b.sel| - 1 do
L7      p ← b.sel[i];  b.sel[j] ← p;  j ← j + (b.col[p] < c)   ▷ no branch on the data
L8  b.sel ← b.sel[0 .. j - 1]
MUL(b, x, y, z)                            ▷ a map primitive: z ← x · y at the live positions
L9  for each p in b.sel do b.z[p] ← b.x[p] · b.y[p]
```

Every primitive is a loop over at most $K$ values of fixed type, with no call inside. A query engine has many of them, one for each operation, type and kind of operand (vector or constant), made from templates when the engine is built.

**The cost of the interface.** Let $N$ tuples flow through a pipeline of $d$ operators. The iterator model makes $\Theta(N d)$ calls of next. With vectors of $K$ tuples, it makes $\Theta(N d / K)$ calls, and the work inside the primitives stays $\Theta(N d)$ simple steps. For $K = 1024$, the number of calls drops by a factor of about a thousand.

**The vector size.** If $K$ is too small, the interface cost per tuple comes back; $K = 1$ is the iterator model. If $K$ is too large, the vectors no longer fit in the CPU cache, and each primitive writes its output to main memory and the next one reads it back. $K = N$ is full column-at-a-time materialization, as in MonetDB/MIL, which is then limited by memory bandwidth. Between the two ends, the vectors of one batch stay in cache from one primitive to the next. In the experiments of Boncz et al., the best vector size was about 1000, and all sizes between 128 and 8K worked well (a measurement, Section 5.1.1).

## Classic examples

- **TPC-H Query 1.** Boncz et al. ran Query 1 of TPC-H at scale factor 1 on an AthlonMP at 1533 MHz (a measurement). A commercial system took 28.1 s, MySQL 4.1 took 26.6 s, column-at-a-time MonetDB/MIL took 3.7 s, X100 took 0.50 s, and a hand-written C program took 0.22 s. In the MySQL profile, the operations that compute the answer took about 10% of the time; the rest went to the aggregation hash table and to the code that moves through records and fields.
- **Filters with selection vectors.** A filter does not copy the passing rows. It writes their positions into the selection vector, and later primitives only look at those positions. This is a form of [late materialization](/late-materialization/) inside one batch.
- **Hash aggregation and hash join.** The hash of a whole key vector is computed in one primitive, the bucket positions in a second, and the probe or update in a third. Each loop has independent iterations, so the CPU can have many cache misses in flight at the same time.
- **Compressed columns.** A scan can return codes of [dictionary encoding](/dictionary-encoding/) as a vector and let a primitive compare codes, so that values are decoded only when needed.

## Variations

- **SIMD primitives.** Primitives that are tight loops over arrays can use SIMD instructions, either from the compiler by [vectorization](/vectorization/) or written by hand. Kersten et al. (2018) measured gains of up to 8.4 times for SIMD in micro-benchmarks with AVX-512, but only about 10% on join queries (a measurement).
- **Push-based vectors.** The batches can also be pushed from the scans to the consumers, with the same primitives. The pipelines of [pipelining and materialization](/pipelining-and-materialization/) stay the same.
- **Parallel vectors.** With [morsel-driven parallelism](/morsel-driven-parallelism/), each thread runs the vectorized pipeline on its own morsel, and a morsel is split into vectors.
- **Fused primitives.** A few primitives that always come together, such as a compare and a sum, can be fused into one loop, as in [loop fusion](/loop-fusion/). This saves the write and read of the vector between them, at the cost of more primitives to build.

## Pitfalls

- **Vectors that leave the cache.** A vector size picked for one machine can be too large on another, or too large for an operator that keeps many vectors live. The output of each primitive then goes to main memory, and the gain shrinks.
- **Too many primitives.** One primitive per operation, type and operand kind gives a large number of functions. Engines make them from templates and still pay in build time and code size.
- **Copies between primitives.** Each primitive writes its result vector, and the next one reads it. Compiled engines keep the value in a register instead, so for simple pipelines on data in cache they need fewer instructions. Kersten et al. found the two models close overall in analytic workloads, with neither one faster on all queries (a measurement).
- **Row-at-a-time habits.** Code with a branch on each value inside a primitive loses the benefit. Write filters so that the loop has no branch that depends on the data, as in line L7.
- **Measuring.** The speed-ups above are measurements on given hardware and benchmarks. They are not bounds, and the gain on a new system must be measured again.

## Exercises

1. A pipeline has a scan, two filters with selectivity $1/2$ each, and a sum. For $N = 10^6$ tuples, count the calls of next in the iterator model and with $K = 1024$.
2. Write a primitive that computes $\text{SUM}(x)$ over the live positions of a batch, and one that adds $x$ into the groups of a hash aggregation, given a vector of group numbers.
3. Change SELECT-LESS so that it uses a branch on the data, and explain why its speed then depends on the selectivity, while the version with line L7 does not.
4. A machine has a cache of 1 MB, and a pipeline keeps 6 vectors of 8-byte values live at the same time. Find the largest $K$ for which they all fit, and compare it with the range found by Boncz et al.

## References
