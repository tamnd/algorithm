---
tag: 78FNHM
kind: algorithm
slug: bottom-up-cube
name: Bottom-up cube computation (BUC)
aliases:
- BUC
- iceberg cube computation
area: databases/query-processing
level: advanced
summary: Compute an iceberg cube from the group-by ALL toward more specific group-bys, and skip each partition whose row count is below the threshold.
model: word-ram
complexity:
  vars: {n: the number of input rows, D: the number of cube dimensions, q: the number of aggregates, minsup: the threshold on COUNT(*)}
  time: {worst: O(2^D n (log n + q)), best: O(D n log n)}
  space: {extra: Θ(n + D)}
properties: {deterministic: true, exact: true, recursive: true, online: false, in_place: false}
history:
  year: 1999
  people: [Kevin Beyer, Raghu Ramakrishnan]
  note: "Beyer and Ramakrishnan gave BUC for sparse cubes and for iceberg cubes, where only the cells with enough rows are wanted."
prereqs: [data-cube, group-by-aggregation]
see_also: [sort-based-aggregation, hash-aggregation, counting-sort, materialized-view, view-selection, hru-greedy-view-selection]
sources:
  - paper: doi:10.1145/304182.304214
    title: Kevin Beyer and Raghu Ramakrishnan, Bottom-up computation of sparse and iceberg CUBEs, Proceedings of ACM SIGMOD 1999, 359 to 370
    locator: the BUC algorithm and its pruning by minimum support
  - paper: "Sameet Agarwal, Rakesh Agrawal, Prasad M. Deshpande, Ashish Gupta, Jeffrey F. Naughton, Raghu Ramakrishnan and Sunita Sarawagi, On the computation of multidimensional aggregates, Proceedings of VLDB 1996, 506 to 521"
    locator: the PipeSort and PipeHash methods
  - paper: doi:10.1023/A:1009726021843
    title: Jim Gray, Surajit Chaudhuri, Adam Bosworth, Andrew Layman, Don Reichart, Murali Venkatrao, Frank Pellow and Hamid Pirahesh, Data cube, a relational aggregation operator generalizing group-by, cross-tab, and sub-totals, Data Mining and Knowledge Discovery 1(1), 29 to 53 (1997)
    locator: the CUBE operator and the ALL value
---

Bottom-up cube computation (BUC) computes an iceberg cube: the cells of the [data cube](/data-cube/) whose group holds at least $\text{minsup}$ rows, which is CUBE with `HAVING COUNT(*) >= minsup`. It starts with the cell where every dimension is ALL, sorts the rows on one more dimension, and splits them into blocks with the same value. It goes on only into blocks that hold at least $\text{minsup}$ rows, because a block that is too small cannot have a qualifying cell below it. Earlier methods such as PipeSort and PipeHash go the other way, from the finest group-by to coarser ones, so they cannot skip a fine cell that is too small.

## In plain words

A shop wants totals for every mix of product, city and year, but only where at least three sales happened. You start with one pile that holds every sale and write its total. Then you split the pile by product. A product pile with fewer than three sales cannot give a mix with three sales, so you put it away at once. For each big product pile, you split it by city, then by year, and write the totals of the piles that are big enough. When the product splits are done, you split the full pile by city, and then by year, in the same way. Each mix is reached by one path, so no total is written twice.

## The problem

The input is a relation $R$ of $n$ rows, $D$ cube dimensions $A_1, \ldots, A_D$, aggregates $f_1, \ldots, f_q$, and a threshold $\text{minsup} \ge 1$. A cell is a tuple $c = (c_1, \ldots, c_D)$ where each $c_i$ is a value of $A_i$ or the marker ALL. Its group $R_c$ is the set of rows that agree with $c$ on every dimension where $c_i$ is not ALL. The output is every cell with $|R_c| \ge \text{minsup}$, with $f_1, \ldots, f_q$ of $R_c$. With $\text{minsup} = 1$, it is the full CUBE of Gray et al. without empty cells. A null is a value like any other here, as in SQL GROUP BY, and is different from ALL.

The cost model is the [word RAM](/word-ram/), with the rows in memory. It counts row operations, and does not count the output.

## The algorithm

$X$ is a working copy of the rows, and $\text{cell}$ is a global tuple of $D$ entries. A call works on a range of $X$ that holds the rows of the current cell.

```pseudo id=main
BUC(R, minsup)                             ▷ R has n rows and D dimensions
L1  X ← a copy of the rows of R;  cell ← (ALL, ..., ALL)
L2  if n ≥ minsup then BUC-REC(0, n, 1)

BUC-REC(lo, hi, d0)                        ▷ X[lo .. hi - 1] are the rows of cell
L3  output cell with f_1, ..., f_q of X[lo .. hi - 1]
L4  for d ← d0 to D do
L5      sort X[lo .. hi - 1] on dimension d     ▷ counting sort when A_d has few values
L6      i ← lo
L7      while i < hi do
L8          j ← i + 1;  while j < hi and X[j].A_d = X[i].A_d do j ← j + 1
L9          if j - i ≥ minsup then              ▷ a smaller block is skipped
L10             cell[d] ← X[i].A_d;  BUC-REC(i, j, d + 1);  cell[d] ← ALL
L11         i ← j
```

A call only fixes dimensions after the last one its cell fixes, so the dimensions of each cell are fixed in increasing order. The inner calls of line L10 only reorder the rows inside their block, so the blocks of line L8 stay correct while the loop of line L7 runs. The next value of $d$ sorts the whole range again.

## Example

The relation has 8 sales (product, city, year, amount): (tea, Hanoi, 2023, 4), (tea, Hue, 2023, 3), (coffee, Hanoi, 2023, 5), (tea, Hanoi, 2024, 2), (coffee, Hanoi, 2024, 6), (coffee, Hue, 2024, 1), (tea, Hanoi, 2024, 7), (juice, Hue, 2023, 8). The cube dimensions are product, city and year, the aggregates are COUNT(\*) and SUM(amount), and $\text{minsup} = 3$.

| call | blocks on the next dimensions | cells output |
|---|---|---|
| (ALL, ALL, ALL) | product: coffee 3, juice 1 (skip), tea 4; city: Hanoi 5, Hue 3; year: 2023 4, 2024 4 | (ALL, ALL, ALL): 8, 36 |
| (coffee, ALL, ALL) | city: Hanoi 2, Hue 1; year: 2023 1, 2024 2 (all skip) | (coffee, ALL, ALL): 3, 12 |
| (tea, ALL, ALL) | city: Hanoi 3, Hue 1 (skip); year: 2023 2, 2024 2 (skip) | (tea, ALL, ALL): 4, 16 |
| (tea, Hanoi, ALL) | year: 2023 1, 2024 2 (skip) | (tea, Hanoi, ALL): 3, 13 |
| (ALL, Hanoi, ALL) | year: 2023 2 (skip), 2024 3 | (ALL, Hanoi, ALL): 5, 24 |
| (ALL, Hanoi, 2024) | none | (ALL, Hanoi, 2024): 3, 15 |
| (ALL, Hue, ALL) | year: 2023 2, 2024 1 (skip) | (ALL, Hue, ALL): 3, 12 |
| (ALL, ALL, 2023) | none | (ALL, ALL, 2023): 4, 20 |
| (ALL, ALL, 2024) | none | (ALL, ALL, 2024): 4, 16 |

The iceberg cube has 9 cells, and 13 blocks are skipped. The full cube of this relation has 29 non-empty cells, out of $(3+1)(2+1)(2+1) = 36$ possible ones. With $\text{minsup} = 1$, BUC sorts each row $2^3 - 1 = 7$ times, for 56 row sorts. With $\text{minsup} = 3$ it sorts 49.

## Correctness

The key fact is a lemma about one call. Let a call $\text{BUC-REC}(lo, hi, d_0)$ run with a cell $c$ that fixes a set $S$ of dimensions, all before $d_0$, and let $X[lo .. hi - 1]$ hold exactly $R_c$, with $|R_c| \ge \text{minsup}$. Then the call outputs once each cell $c'$ that agrees with $c$ on $S$, fixes $S \cup T$ for some $T \subseteq \{d_0, \ldots, D\}$, and has $|R_{c'}| \ge \text{minsup}$, and no other cell. The proof is by induction on $D - d_0$. Line L3 outputs $c$ itself ($T$ empty). For $T$ not empty, let $d$ be its smallest dimension: the block of line L8 for the value $c'_d$ holds $R_c$ restricted to $A_d = c'_d$, and the induction applies to the call on it. If that block is smaller than $\text{minsup}$, then $R_{c'}$ is a subset of the block, so $|R_{c'}| < \text{minsup}$ too, and skipping it loses nothing. This is the monotone property of COUNT that the pruning needs. Since $d$ is fixed by $T$, each $c'$ is reached by exactly one path. The top call of line L2 has $S$ empty, so the output is the whole iceberg cube. The full proof is in the proof file.

## Complexity

- **Sorting work.** With $\text{minsup} = 1$, every row is sorted exactly $2^D - 1$ times. A row lies in one cell of each of the $2^D$ group-bys, and the call of a cell that fixes $S$ sorts its rows on the $D - \max S$ dimensions after $S$, with $\max \emptyset = 0$. The sum of $D - \max S$ over all $S$ is $2^D - 1$. A larger $\text{minsup}$ can only remove calls.
- **Time.** With a comparison sort, the sorts cost $O(2^D n \log n)$ in the worst case, and the aggregates cost $O(q)$ per row per cell, at most $O(2^D n q)$. With a counting sort on a dimension with few values, a sort is linear in its range plus the number of values. When no value of any dimension occurs $\text{minsup}$ times, only the top call runs, and the cost is $O(D n \log n)$.
- **Output.** The full cube has at most $\prod_i (C_i + 1)$ cells for dimensions with $C_i$ values each, and at most $2^D n$ non-empty cells. The iceberg condition can make the output much smaller than both.
- **Space.** BUC needs the copy $X$ and a recursion depth of at most $D + 1$ calls. It does not keep any group-by in memory to compute another one.

## Properties

- **Depth-first order.** The output comes cell by cell in the order of the calls, not group-by by group-by. A consumer that wants one group-by at a time must collect them.
- **Pruning needs a monotone condition.** COUNT(\*) $\ge$ minsup works because the count of a cell is at most the count of its block. SUM of non-negative values $\ge t$ works for the same reason. AVG $\ge t$ does not, because a small cell can have a larger average than its block.
- **Each cell from its rows.** Every cell is computed from its own rows, so a holistic aggregate such as MEDIAN works with no extra state. The price is that no group-by is computed from a smaller parent result.
- **Deterministic.** The output set does not depend on how the sort breaks ties.

## Variants and improvements

- **One-row blocks.** A block of one row gives the same aggregates for all its cells below, so a system can write them all at once and stop the recursion there.
- **Order of the dimensions.** Putting the dimension with the most values first makes the blocks small soon, so the pruning starts early. This is a heuristic.
- **PipeSort.** Agarwal et al. compute the full cube from the finest group-by down. Group-bys that are prefixes of one sort order share one sort, and each group-by is computed from a parent with more attributes. This saves sorts for a dense cube, but it cannot use an iceberg condition, because a fine cell that fails the condition is still needed for the coarser cells.
- **PipeHash.** It is the same idea with hash tables, computing several smaller group-bys from one parent result in memory.
- **Disk.** If the rows do not fit in memory, the input is first split on one dimension into partitions that fit, and BUC runs on each.

## When to use it

Use BUC for a sparse cube with many dimensions, where most cells are small, or when only cells with a minimum count are wanted. For a dense cube with few dimensions and no threshold, the top-down methods that share sorts or compute a group-by from a parent result can do less work.

## Pitfalls

- **A non-monotone condition.** Pruning on AVG, or on SUM with negative values, drops cells that should be in the output.
- **Null against ALL.** A null in a dimension is a group of its own. Using null as the ALL marker merges it with the subtotal row. SQL keeps them apart with the `GROUPING` function.
- **Empty input.** SQL CUBE on an empty input gives one row for (ALL, ..., ALL) with COUNT 0. Any $\text{minsup} \ge 1$ removes that row, so BUC outputs nothing.
- **Too many cells.** With $\text{minsup} = 1$ and $D$ large, the output can approach $2^D n$ rows even when the input is small.

## Implementations

## History

Gray et al. defined the CUBE operator in 1996 and 1997. Agarwal et al. (1996) gave PipeSort and PipeHash, which compute all group-bys of a full cube and share work among them. Beyer and Ramakrishnan (1999) turned the order around for sparse and iceberg cubes. In the lattice of group-bys drawn with ALL at the bottom, BUC works upward, from ALL toward the finest group-by.

## References
