---
tag: CMK4NB
kind: problem
slug: access-path-selection
name: Access path selection
aliases:
- access method selection
area: databases/query-planning
level: core
summary: "Choose for each relation of a query between a full scan and the indexes that match its predicates, by their estimated cost, and keep the cheapest path for each interesting order."
prereqs: [b-plus-tree, selectivity, cost-model, interesting-orders]
see_also: [selinger-join-enumeration, index-selection, covering-index, bitmap-index, clustered-index, index-nested-loop-join, cardinality-estimation, heap-file]
sources:
  - paper: doi:10.1145/582095.582099
    title: "P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34"
    locator: "Section 4, Costs for single relation access paths (segment scans and index scans, the selectivity factors of the predicates, and the cheapest path for each interesting order); Section 5 for the inner relations of joins"
  - url: https://www.postgresql.org/docs/current/using-explain.html
    title: PostgreSQL documentation, Using EXPLAIN
    locator: "the plans on the table tenk1 with Seq Scan, Index Scan, Bitmap Index Scan, BitmapAnd, Bitmap Heap Scan and Index Only Scan, and the change from an index to a sequential scan as the condition becomes less selective"
---

Access path selection is the problem of choosing, for each relation that a query reads, how to read it: a full scan of the file, or a scan of one of the indexes whose key matches some of the predicates on the relation, with the other predicates applied as filters. The choice is made by estimated cost, from the sizes of the relation and of the indexes and the [selectivity](/selectivity/) of the predicates. Because an index scan returns tuples in key order, a path that costs more can still be the best one when a later step needs that order, so the answer is the cheapest path for each [interesting order](/interesting-orders/), not one path. Selinger and her colleagues stated the problem and its cost formulas for System R in 1979. This page is the single-relation problem; the [System R join enumeration](/selinger-join-enumeration/) uses its answers as the base case of the search over join orders, and also chooses the access path of each inner relation of a join.

## In plain words

A table is a stack of pages. To find the rows that a query wants, the database can read every page and keep the rows that match. Or it can look the rows up in an index, like the index at the back of a book, and read only the pages that hold them.

The index is faster when few rows match. When many rows match, it can be slower than reading everything, because the index sends you to the same pages many times, in a jumbled order. So the database estimates how many rows match and the cost of each way, and picks the cheapest. An index also returns the rows in sorted order, which can save a sort later, so that way can win even when it costs a little more.

## Definition

**Input.**

- A relation $R$ stored in a file of $N$ pages with $T$ tuples, such as a [heap file](/heap-file/).
- Its indexes $I_1, \ldots, I_m$. For each one: the list of key columns, whether it is clustered (the file is stored in key order), its height $h$ and its number of leaf pages $L$, and the columns it stores.
- The local predicates of the query on $R$, as a conjunction of terms, with an estimated selectivity $F$ for each term.
- The columns of $R$ that the rest of the query needs.
- The interesting orders of the query on columns of $R$.
- A [cost model](/cost-model/) for each kind of scan.

**Access paths.**

- A **full scan** reads all $N$ pages and applies every term as a filter.
- An **index scan** on an index $I$ uses the terms that *match* $I$: equality terms on a prefix of its key columns, followed by at most one range term on the next key column. It reads the part of the index that these terms select, fetches the matching tuples from the file, and applies the other terms as filters. Its output is in the key order of $I$.
- An **index-only scan** is an index scan on a [covering index](/covering-index/), one that stores every column the query needs, so it does not fetch from the file.

**Output.** For each interesting order $o$, the access path of least estimated cost whose output is in order $o$, and the access path of least cost overall. A plan can also reach order $o$ by a sort after the cheapest path, so the path kept for $o$ is the cheaper of the two.

**A simple cost model.** With $F$ the product of the selectivities of the matching terms, and pages as the unit of cost:

| access path | estimated pages read |
|---|---|
| full scan | $N$ |
| clustered index scan | $h + F \cdot L + F \cdot N$ |
| unclustered index scan | $h + F \cdot L + F \cdot T$ |
| index-only scan | $h + F \cdot L$ |

The unclustered index scan pays one page for each matching tuple, because consecutive index entries point to pages in no order. This is the worst case; a buffer that holds the recently read pages makes it smaller. Real cost models also count CPU work per tuple, as the [cost model](/cost-model/) page shows.

## Variants

- **Index intersection.** Several indexes each match one term. The scan reads the matching tuple identifiers of each index, intersects the lists, and fetches only the tuples in the intersection. With a [bitmap index](/bitmap-index/), or a bitmap built from a B+ tree index, the intersection is an AND of bitmaps, and the fetch reads the pages in file order.
- **Index union.** For a disjunction of terms on different columns, the union of the identifier lists replaces a full scan.
- **Inner relations of joins.** In an [index nested-loop join](/index-nested-loop-join/), the join predicate $R.a = S.b$ becomes the term $a = $ (the current value of $S.b$) for each outer tuple. The access path of the inner relation then depends on the join order, so it is chosen inside the join enumeration.
- **Parametric choice.** If a predicate has a parameter whose value is not known when the plan is made, the selectivity is not known, and the best path can change with the value.

## Examples

Take $R$ with $N = 1000$ pages and $T = 100\,000$ tuples. It has an unclustered B+ tree $I_a$ on $a$ and a clustered B+ tree $I_b$ on $b$, each with height 3 and 400 leaf pages.

**Query 1:** WHERE $a = 7$ AND $b > 50$, with $F = 1/1000$ for $a = 7$ and $F = 0.9$ for $b > 50$.

| path | matching terms | estimated pages | output order |
|---|---|---|---|
| full scan | none | 1000 | none |
| $I_a$ | $a = 7$ | $3 + 1 + 100 = 104$ | $(a)$ |
| $I_b$ | $b > 50$ | $3 + 360 + 900 = 1263$ | $(b)$ |

The leaf pages of $I_a$ for one value round up to 1, and the 100 matching tuples cost one page each. The answer is $I_a$, with $b > 50$ as a filter. It returns about $100 \cdot 0.9 = 90$ tuples.

**Query 2:** WHERE $b > 50$ ORDER BY $b$. Now $I_a$ matches no term. The cheapest path with no order is the full scan, at 1000 pages. Its result has about 90 000 tuples on 900 pages, and an external sort with one merge pass writes and reads them once more, which adds 1800 pages, for 2800 in all. The path $I_b$ costs 1263 and returns the order $(b)$. A choice by cost alone would take the full scan; with $(b)$ as an interesting order, the answer is $I_b$.

## Known algorithms

- **Enumeration of the paths.** For each relation, list the full scan and each index with at least one matching term or with a key order that is interesting. Estimate the cost of each, and keep the cheapest one for each interesting order and the cheapest one overall. This is the method of System R. It takes time linear in the number of indexes for each order.
- **Index combinations.** For intersections and unions, the number of subsets of indexes grows as $2^m$. Systems limit the search with rules, for example by adding indexes to an intersection in order of selectivity while the estimated cost falls.
- **Heuristic rules.** Simple optimizers use fixed rules, such as "use an index if one matches an equality term". They need no statistics, but they take an index scan even when many tuples match and a full scan is cheaper, and they do not see that an order can pay for a more expensive path, as in query 2.

## Bounds

For one relation and one index per path, the search is a scan of $m + 1$ candidates for each of the $k + 1$ orders, which is $O(mk)$ cost evaluations. The hard part is the input: the costs depend on selectivity estimates, and an error in $F$ moves the break-even point between an index scan and a full scan. With the model above, an unclustered index scan beats a full scan only when about $F \cdot T < N$, that is, when fewer tuples match than the file has pages. In query 1 that is 100 tuples against 1000 pages.

## Reductions

- **Base case of join enumeration.** The System R enumeration starts from the best access paths of each relation, one for each interesting order, and builds plans for larger sets from them.
- **Dual of index selection.** [Index selection](/index-selection/) chooses which indexes to build for a workload. Its tools call the optimizer with indexes that do not exist yet, so the access path selection of each query is the inner step of the index selection.
- **Inputs from estimation.** The selectivities come from [cardinality estimation](/cardinality-estimation/) with [histograms](/histogram/) and distinct value counts.

## Applications

Every relational database system with a cost-based optimizer solves this problem for each table of each query. PostgreSQL, for example, shows its choice in EXPLAIN as a sequential scan, an index scan, an index-only scan, or a bitmap heap scan over one bitmap index scan or a BitmapAnd of several, and it moves from an index to a sequential scan as a condition becomes less selective.

## References
