---
tag: BKMHC8
kind: data-structure
slug: zone-map
name: Zone map
aliases:
- min-max index
- small materialized aggregates
- block range index
area: systems/database-algorithms
level: core
summary: "The minimum and maximum of a column in each block of rows. A scan skips each block whose interval misses the predicate. It helps only when the data is sorted or clustered on the column."
model: external-memory-model
complexity:
  vars: {n: the number of rows, b: the number of rows in one block, m: the number of rows that qualify}
  time: {worst: "O(n)", best: "O(n / b)"}
  space: {extra: "Θ(n / b)"}
prereqs: [clustered-index, external-memory-model]
see_also: [bitmap-index, predicate-pushdown, selectivity, database-cracking, range-partitioning, learned-index, histogram, bloom-filter]
sources:
  - url: http://www.vldb.org/conf/1998/p476.pdf
    title: "Guido Moerkotte, Small materialized aggregates: a light weight index structure for data warehousing, Proceedings of VLDB 1998"
    locator: pp. 476 to 487, small materialized aggregates (min, max, count, sum) per bucket of consecutive pages, and their use to skip buckets and to answer aggregates
  - url: https://www.postgresql.org/docs/current/brin.html
    title: PostgreSQL documentation, BRIN indexes
    locator: the block range index, its summary of each range of table pages, and the remark that it works best when values correlate with the physical order of rows
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 8 (the cost model of page I/Os, and why the physical order of a file decides the cost of a range selection)
---

A zone map stores, for each block of consecutive rows of a table, the minimum and the maximum of a column in that block. A scan with a predicate $lo \le A \le hi$ reads only the blocks whose interval $[\min, \max]$ meets $[lo, hi]$, and skips the others without a read. It costs a few bytes per block, needs no tree and no sort order of its own, and it is never wrong: a skipped block cannot hold a qualifying row. It skips many blocks only when the table is sorted or [clustered](/clustered-index/) on the column; on rows in random order it skips almost nothing.

## In plain words

A library keeps its books in boxes. On the lid of each box, it writes the oldest and the newest year of the books inside. To find the books from the 1960s, you read the lids, and you open only the boxes whose range of years includes some part of the 1960s.

If the books were put into the boxes in order of year, only one or two boxes need opening. If the books were thrown into the boxes at random, almost every box has an old book and a new book, so almost every lid says "maybe", and you open nearly all of them. The lids never make you miss a book. They only save work when the boxes are in order.

## The abstract type

A zone map is an auxiliary filter on a table, not a full index. It supports:

- `build(T, b)`: compute the bounds of each block of $b$ rows.
- `scan(T, lo, hi)`: return the rows with $lo \le A \le hi$, reading only the blocks that can hold such rows.
- `append(T, v)` and `update(T, r, x)`: change the table and keep the bounds valid.

The result of `scan` must equal the result of a full scan. The number of blocks read is the cost to reduce, in the [external memory model](/external-memory-model/) where a block of $b$ rows is one I/O.

## Representation

Rows $0, \ldots, n-1$ are in blocks $0, \ldots, \lceil n/b \rceil - 1$, and block $k$ holds rows $kb$ to $\min(kb + b, n) - 1$. For each block, the zone map keeps two values, $lo_k$ and $hi_k$.

**Invariant (validity).** For every row $r$ in block $k$: $lo_k \le A(r) \le hi_k$.

The bounds are *tight* when $lo_k$ and $hi_k$ are the actual minimum and maximum of the block. Tight bounds skip the most blocks, but the scan needs only validity. Moerkotte's small materialized aggregates also keep the count and the sum of each block.

## Operations

```pseudo id=main
SCAN(Z, lo, hi)                           ▷ the rows with lo ≤ A ≤ hi
L1  result ← empty
L2  for each block k do
L3      if hi_k < lo or lo_k > hi then
L4          skip block k                  ▷ no row of block k can qualify
L5      else
L6          read block k
L7          for each row r of block k do
L8              if lo ≤ A(r) ≤ hi then add r to result
L9  return result
```

```pseudo id=update
UPDATE(Z, r, x)                           ▷ set A(r) to x
L10 k ← ⌊r / b⌋
L11 A(r) ← x
L12 lo_k ← min(lo_k, x), hi_k ← max(hi_k, x)
```

`build` is one pass that takes the minimum and maximum of each block. `append` starts a new block with $lo = hi = v$, or widens the bounds of the last block. UPDATE only widens the bounds. After many updates and deletes the bounds are valid but loose, and a later pass recomputes them block by block.

## Example

The column holds the numbers 1 to 16 in two orders, with $b = 4$, so there are four blocks. The query is $6 \le A \le 9$.

| order | rows of each block | zone map $[lo_k, hi_k]$ | blocks read | rows found |
|---|---|---|---|---|
| unsorted | 5 12 1 16, 9 3 14 7, 2 11 15 6, 13 4 10 8 | [1, 16] [3, 14] [2, 15] [4, 13] | 4 of 4 | 4, 7, 11, 15 |
| sorted | 1 2 3 4, 5 6 7 8, 9 10 11 12, 13 14 15 16 | [1, 4] [5, 8] [9, 12] [13, 16] | 2 of 4 | 5, 6, 7, 8 |

In the unsorted order, each block holds a small and a large value, so every interval contains part of $[6, 9]$ and nothing is skipped. In the sorted order, blocks 0 and 3 are skipped. An update that sets row 0 of the sorted column to 30 widens block 0 to $[1, 30]$ (the bound 1 stays, because an update never shrinks a bound); a later query for $[6, 9]$ then reads block 0 too, and still returns the right rows.

**A larger case.** Take $n = 10\,000$ values drawn uniformly from $0$ to $10^6 - 1$ by `random.Random(2)`, in blocks of $b = 100$ rows (100 blocks).

| query | rows found | blocks read, random order | blocks read, sorted |
|---|---|---|---|
| $500\,000 \le A \le 509\,999$ | 98 | 100 | 2 |
| $0 \le A \le 9\,999$ | 113 | 68 | 2 |

## Correctness

SCAN skips block $k$ only when $hi_k < lo$ or $lo_k > hi$. By the invariant, every row $r$ of the block has $A(r) \le hi_k < lo$ or $A(r) \ge lo_k > hi$, so no row of the block qualifies. Every other block is read and filtered by line L8. So SCAN returns exactly the rows of a full scan. `build` makes tight bounds, `append` and UPDATE replace a bound by the minimum or maximum of itself and the new value, and old values that leave a block can only make the bounds loose, never invalid. The full proof is below.

## Complexity

The space is two values per block, $\Theta(n / b)$, a small fraction of the table. A scan reads all bounds, $O(n/b)$ values, plus the blocks that are not skipped. The worst case reads every block, $\Theta(n / b)$ I/Os and $\Theta(n)$ row tests, which is a full scan plus the bounds.

**Sorted data.** If the column is non-decreasing in row order and the bounds are tight, then SCAN reads exactly the blocks that hold at least one qualifying row, plus at most one more block, and the extra block appears only when no row qualifies. Proof: a block that is read but holds no qualifying row has its minimum below $lo$ and its maximum above $hi$, since a bound that lies in $[lo, hi]$ is the value of some row of the block. In sorted order, any row with a value in $[lo, hi]$ lies between the rows of that minimum and that maximum, so inside this block. Hence no row qualifies at all, and no other block can be such a block. With $m \ge 1$ qualifying rows, they are consecutive, so SCAN reads at most $\lceil (m + b - 1) / b \rceil$ blocks, at most one more than the $\lceil m / b \rceil$ blocks that any method must read.

**Random order.** If the $b$ values of a block are drawn independently from one distribution, with $p_{<} = \Pr[A < lo]$ and $p_{>} = \Pr[A > hi]$, then the block is skipped exactly when all $b$ values are below $lo$ or all are above $hi$, so

$$\Pr[\text{block skipped}] = p_{<}^{\,b} + p_{>}^{\,b}.$$

For a query in the middle of the range with $p_{<} = 0.5$ and $p_{>} = 0.49$, and $b = 100$, the expected number of skipped blocks out of 100 is below $10^{-28}$. For the query at the low end, $p_{<} = 0$ and $p_{>} = 0.99$, and the expected number is $100 \times 0.99^{100} \approx 36.6$; the run of the table above skipped 32. So on unordered data a zone map skips blocks only for predicates near the ends of the range.

## Variants

- **Small materialized aggregates.** Moerkotte keeps min, max, count and sum for each bucket of pages. A bucket that lies wholly inside $[lo, hi]$ adds its count and sum to `COUNT` and `SUM` without a read; only the boundary buckets are read.
- **BRIN.** PostgreSQL's block range index keeps a summary for each range of table pages (by default 128 pages), with min and max for ordered types. The ranges are summarized in a batch after inserts.
- **Per-page and per-file statistics.** Columnar file formats keep min and max for each column chunk and page, and readers skip the parts that cannot match. This is the same structure at several levels.
- **Other summaries.** A [Bloom filter](/bloom-filter/) per block skips blocks for equality predicates on columns that are not sorted; a small [histogram](/histogram/) per block gives selectivity estimates.
- **Make the data clustered.** Sort the table on the column, or keep it clustered by insertion time for time-ordered data. Sorting on several columns with a space-filling curve spreads the benefit over several columns, each less than a pure sort. [Database cracking](/database-cracking/) reaches the same order as a side effect of queries.

## When to use it

Use a zone map on a large table that is sorted or naturally clustered on the column: time-stamped event logs, append-only fact tables loaded in date order, or tables sorted on a key. It costs almost nothing to keep, so analytic systems keep one on every column. Do not expect it to help on a column whose values are spread at random over the blocks; use a [bitmap index](/bitmap-index/) or a B+ tree for such a column.

## Pitfalls

- **Unclustered data.** The zone map stays correct but skips nothing, as the formula above shows. Check the correlation between the column and the row order before you rely on it.
- **Shrinking a bound on update.** Setting $hi_k$ to the new value of a row that was the maximum makes the bound invalid if another row is larger, and the scan then misses rows. Only widen on updates; recompute a bound from the whole block.
- **NULLs and special values.** A NULL is not ordered with the other values. Keep a flag for "the block has NULLs" and do not let NULL enter min or max. A floating-point NaN breaks min and max in the same way.
- **Predicates on an expression.** The bounds are for $A$, not for $f(A)$. They carry over to $f(A)$ only when $f$ is monotone, so a predicate on an expression, a type cast or a different collation of strings usually cannot use the zone map.

## Implementations

## History

Moerkotte introduced small materialized aggregates in 1998 as a light index for data warehouses: aggregates per bucket of consecutive pages, used to skip buckets and to answer aggregates. The idea spread under the names zone map, min-max index and block range index (BRIN in PostgreSQL), and is part of the column statistics of analytic file formats.

## References
