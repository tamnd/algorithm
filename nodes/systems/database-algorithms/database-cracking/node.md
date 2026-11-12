---
tag: N3RJND
kind: technique
slug: database-cracking
name: Database cracking
aliases:
- column cracking
- cracker index
area: systems/database-algorithms
level: research
summary: "Build an index as a side effect of queries. Each range query partitions only the pieces of a column copy that hold its bounds, so the column gets closer to sorted where queries go."
prereqs: [partition-around-pivot, quicksort, range-query-structure]
see_also: [quickselect, three-way-quicksort, zone-map, b-plus-tree, bulk-loading-b-tree, index-selection, adaptive-sorting, learned-index]
sources:
  - paper: "Stratos Idreos, Martin L. Kersten and Stefan Manegold, Database cracking, 3rd Biennial Conference on Innovative Data Systems Research (CIDR), 2007"
    locator: pp. 68 to 78; the cracker column, the cracker index, crack-in-two and crack-in-three, and the experiments in MonetDB
  - paper: doi:10.14778/2168651.2168652
    title: "Felix Halim, Stratos Idreos, Panagiotis Karras and Roland H. C. Yap, Stochastic database cracking: towards robust adaptive indexing in main-memory column-stores, PVLDB 5(6) (2012)"
    locator: pp. 502 to 513; the bad case of sequential workloads and cracking with extra random pivots
---

Database cracking builds an index on a column as a side effect of the queries, with no index build up front. The first range query on a column copies it into a *cracker column* and partitions it around the two bounds of the query, as one step of [quicksort](/quicksort/) would. A small *cracker index* remembers each bound and the position where it splits the column. Each later query partitions only the one or two *pieces* that hold its bounds, and the result is one contiguous slice. Pieces get smaller where queries go, so the cost per query falls from a full scan toward an index lookup, and the column becomes sorted only in the ranges that are used.

## In plain words

You have a big box of papers in random order, and people come to ask for "the papers from March to May". The first time, you go through the whole box once and make three heaps: before March, March to May, and after May. You write down where each heap starts.

The next person asks for "April to August". You do not go through the whole box again. You only sort through the heaps that hold April and August, and split them. Each request splits a few heaps, and the heaps get smaller and smaller. After many requests, the box is almost in order in the parts that people ask for, and each new request is fast. Parts that nobody asks for stay one big unsorted heap.

## When it applies

- The data is a column, or a table read mostly by range predicates $lo \le A < hi$ on one attribute.
- The workload is not known in advance, so you cannot choose the indexes ([index selection](/index-selection/)) and build them before the queries come.
- There is no idle time for a full sort or a [bulk load](/bulk-loading-b-tree/), or only a small part of the domain is queried.
- A copy of the column is allowed, and queries may reorder that copy. The approach is at its best in main-memory column stores, where a partition pass is cheap and the result is a contiguous array slice.

## The template

The cracker column $C$ holds (value, row id) pairs. The cracker index $I$ is an ordered map from pivot values $v$ to positions $\mathrm{pos}(v)$: all entries before $\mathrm{pos}(v)$ have value $< v$, and all entries from $\mathrm{pos}(v)$ on have value $\ge v$. Consecutive pivots $v_i < v_{i+1}$ bound a *piece*, the positions from $\mathrm{pos}(v_i)$ to $\mathrm{pos}(v_{i+1}) - 1$, whose values all lie in $[v_i, v_{i+1})$.

```pseudo id=main
CRACK-QUERY(C, I, lo, hi)                     ▷ the rows with lo ≤ A < hi
L1  if lo ≥ hi then return the empty set
L2  [a, b) ← the piece of C whose value range holds lo, found in I
L3  [c, e) ← the piece of C whose value range holds hi
L4  if lo ∉ I and hi ∉ I and [a, b) = [c, e) then
L5      (p, q) ← CRACK-IN-THREE(C[a..b), lo, hi); add lo ↦ p and hi ↦ q to I
L6  else
L7      if lo ∉ I then p ← CRACK-IN-TWO(C[a..b), lo); add lo ↦ p to I
L8      if hi ∉ I then q ← CRACK-IN-TWO(C[c..e), hi); add hi ↦ q to I
L9  return the row ids in C[pos(lo) .. pos(hi))
```

CRACK-IN-TWO$(S, v)$ is a two-pointer partition, as in [Hoare's scheme](/hoare-partition/): it moves the entries $< v$ before the entries $\ge v$ and returns the split point. CRACK-IN-THREE$(S, lo, hi)$ is the three-way partition of the Dutch national flag problem, as in [three-way quicksort](/three-way-quicksort/): it makes the groups $< lo$, $[lo, hi)$, $\ge hi$ in one pass. Both work in place on one piece and touch no other part of $C$.

In the else branch at most one of the two partitions works on a piece that the other could change: when both bounds are new and lie in different pieces, the two pieces are disjoint; when exactly one bound is new, only one partition runs. So the pieces of lines L2 and L3 stay valid.

**Invariant.** After every query, for every piece between consecutive pivots $v_i$ and $v_{i+1}$ (with $v_0 = -\infty$ and a last pivot followed by $+\infty$), every value in the piece lies in $[v_i, v_{i+1})$, and the positions of the pivots are non-decreasing. A partition of one piece around a value in its range splits it into two or three pieces that satisfy the same condition, and leaves all other pieces as they were. So line L9 returns exactly the rows with $lo \le A < hi$: they are the pieces from $\mathrm{pos}(lo)$ to $\mathrm{pos}(hi)$.

**Example.** The column is $13, 16, 4, 9, 2, 12, 7, 1, 19, 3, 14, 11, 8, 6$ (14 rows).

| query | pieces cracked | cracker column after it | cracker index | entries touched |
|---|---|---|---|---|
| $10 \le A < 14$ | all 14 rows, crack-in-three | 6 4 9 2 7 1 8 3, 13 12 11, 14 19 16 | 10 ↦ 8, 14 ↦ 11 | 14 |
| $7 \le A < 16$ | $[0, 8)$ for 7 and $[11, 14)$ for 16, crack-in-two each | 6 4 3 2 1, 7 8 9, 13 12 11, 14, 19 16 | 7 ↦ 5, 10 ↦ 8, 14 ↦ 11, 16 ↦ 12 | 11 |
| $1 \le A < 8$ | $[0, 5)$ for 1 and $[5, 8)$ for 8 | (unchanged) | adds 1 ↦ 0, 8 ↦ 6 | 8 |

The answers are $\{11, 12, 13\}$, $\{7, 8, 9, 11, 12, 13, 14\}$ and $\{1, 2, 3, 4, 6, 7\}$, each a slice of the cracker column. The second query scans 11 entries and the third 8, against 14 for a scan.

**Cost.** A query costs the sizes of the one or two pieces it cracks, plus $O(\log k)$ to search the cracker index of $k$ pivots. The worst case is $\Theta(n)$ per query. In a model where the values and the query bounds are independent and uniform, the piece that holds a fresh random point, after $k$ random cuts, has expected size $2n / (k + 2)$ (a random point falls more often into a long piece). After $j$ queries there are $2j$ cuts, so query $j + 1$ costs at most $2 \cdot 2n / (2j + 2) = 2n / (j + 1)$ in expectation, and $q$ queries cost at most $2n H_q = O(n \log q)$ in total, against $nq$ for scans and $\Theta(n \log n)$ for a full sort up front.

On 100,000 uniform values from `random.Random(6)` and 1,000 random range queries, the first query touches 100,000 entries, the 10th 23,687, the 100th 1,105 and the 1,000th 174. The total is 1,327,815, below the bound $2n H_{1000} \approx 1{,}497{,}094$, and 75 times less than 1,000 scans.

## Classic examples

- **Range selections in a column store.** The original setting: MonetDB answers $lo \le A < hi$ on a column by cracking a copy, and returns a view of the slice without copying the result.
- **Lazy quicksort.** If the queries cover every value, the cracker column ends sorted, and the work done is a [quicksort](/quicksort/) in which each partition step is paid by the query that needed it. Cracking stops when a piece is small enough to scan, like quicksort with a cutoff.
- **Order statistics on demand.** A query for the $k$-th smallest value cracks around a value guess, as [quickselect](/quickselect/) does; repeated selections on one array reuse the earlier partitions in the same way.
- **The partition step itself.** Each crack is one call of [partition around a pivot](/partition-around-pivot/), on a piece, not on the whole array.
- **Data skipping by order.** The pieces of a cracked column are like a [zone map](/zone-map/) built by the queries: each piece has known bounds and is skipped or read whole.

## Variations

- **Stochastic cracking.** Halim, Idreos, Karras and Yap (2012) add random pivots to each crack. A sequential workload, where each query asks for the next range, otherwise cracks the large unqueried piece at every query and costs $\Theta(n)$ each time. In the run above, 1,000 sequential ranges of the same size cost 50,060,522 touched entries, about $nq/2$, against 1,327,815 for random ranges.
- **Hybrid cracking and adaptive merging.** Graefe and Kuno's adaptive merging sorts runs on the first query and merges the queried ranges, which converges in fewer queries; hybrids combine cracking of the initial partitions with merging.
- **Sideways cracking.** For queries that select on one column and project others, maps of column pairs are cracked together, so that the other values move with the selected column and tuple reconstruction stays cheap.
- **Updates.** Inserts and deletes are kept in pending lists and merged into the pieces that a later query touches, again lazily.
- **Concurrency.** A crack writes to the column, so readers need latches on pieces. Small pieces can be left unlatched once they are no longer cracked.

## Pitfalls

- **Sequential or skewed workloads.** A crack costs the size of the piece, and a workload that always cuts the large remaining piece near its end pays a full pass each time. Stochastic cracking or a minimum piece size bounds this.
- **Duplicates and bounds.** Use one convention for pivots, here values $< v$ before $\mathrm{pos}(v)$, in both partitions and in the index. A mix of $<$ and $\le$ makes equal values land on both sides of a pivot, and queries miss rows.
- **The second partition on a changed piece.** If both bounds are new and lie in one piece, two crack-in-two calls must run on the right pieces: the second must use the piece found after the first split. Crack-in-three avoids the issue and does one pass.
- **Row order.** Cracking reorders the copy, so the result comes out in cracker order, not in row order. Sort the row ids if the next operator needs row order.
- **Memory for the copy.** The cracker column is a second copy of the column with row ids. On a table with many queried columns, the copies add up.

## Exercises

1. Run the three queries of the example and then the query $8 \le A < 10$. Which pieces does it crack, and how many entries does it touch?
2. Show that if every query has $hi = lo + 1$ and the values of $lo$ are a random permutation of the $n$ distinct values, the total work is the work of a randomized quicksort, $O(n \log n)$ in expectation.
3. Give a workload of $q$ queries on $n$ distinct values that costs $\Theta(nq)$ for $q \le n$.

## References
