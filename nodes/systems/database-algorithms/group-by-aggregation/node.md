---
tag: KFFKTB
kind: problem
slug: group-by-aggregation
name: Group-by aggregation problem
aliases:
- grouping and aggregation
- GROUP BY evaluation
area: systems/database-algorithms
level: intro
summary: Split the rows of a relation into groups by a key and compute an aggregate such as COUNT, SUM or AVG over each group.
prereqs: [relational-algebra, sorting-problem, hash-table]
see_also: [hash-aggregation, external-merge-sort, element-distinctness, combiner, hash-partitioning, distinct-elements-problem, median, sliding-window-aggregation]
sources:
  - paper: doi:10.1023/A:1009726021843
    title: Jim Gray, Surajit Chaudhuri, Adam Bosworth, Andrew Layman, Don Reichart, Murali Venkatrao, Frank Pellow and Hamid Pirahesh, Data cube, a relational aggregation operator generalizing group-by, cross-tab, and sub-totals, Data Mining and Knowledge Discovery 1(1), 29 to 53 (1997)
    locator: the section on aggregate functions (distributive, algebraic and holistic aggregates) and the CUBE operator
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 73 to 169 (1993)
    locator: Section 4 (aggregation and duplicate removal by nested loops, sorting and hashing, with early aggregation)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 13 (external sorting) and Chapter 14, Section 14.6 (aggregate operations)
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Chapter 15 (one-pass grouping, and two-pass grouping based on sorting and on hashing)
  - paper: "Dina Bitton and David J. DeWitt, Duplicate record elimination in large data files, ACM Transactions on Database Systems 8(2), 255 to 265 (1983)"
    locator: duplicate removal during the runs of an external merge sort
---

The group-by aggregation problem asks, for a relation $R$, a list of grouping attributes $G$ and a list of aggregate functions, for one output row per distinct value of $G$ in $R$, with each aggregate computed over the rows of that group. It is the SQL `GROUP BY` clause and the $\gamma$ operator of the extended [relational algebra](/relational-algebra/). It is solved by sorting the rows on $G$ (see [external merge sort](/external-merge-sort/)) or by [hash aggregation](/hash-aggregation/). The cost depends on the number of groups and on the class of the aggregate: distributive, algebraic or holistic.

## In plain words

A shop has a list of sales. Each sale has a region and an amount. The manager wants, for each region, the number of sales and the total amount. You must put the sales of the same region together and then add them up.

There are two ways to put them together. You can sort the list by region, so the sales of one region come one after the other. Or you can keep a small table with one line for each region, and add each sale to its line as you read it.

Some answers, like the total, can be built from totals of parts of the list. The average needs two numbers per part, the total and the count. The middle value of each group needs all the values of the group at the same time.

## Definition

Let $R$ be a finite multiset of tuples over a set of attributes $U$. Let $G \subseteq U$ be the grouping attributes, and let $(f_1, A_1), \ldots, (f_p, A_p)$ be pairs of an aggregate function $f_j$ and an attribute $A_j \in U$. An aggregate function maps a finite non-empty multiset of values to a value. For each $g \in \pi_G(R)$, the group of $g$ is the multiset $R_g = \{\!\{ t \in R : t[G] = g \}\!\}$. The answer is the set

$$\gamma_{G;\, f_1(A_1), \ldots, f_p(A_p)}(R) = \bigl\{ \bigl(g, f_1(R_g[A_1]), \ldots, f_p(R_g[A_p])\bigr) : g \in \pi_G(R) \bigr\},$$

where $R_g[A]$ is the multiset of the $A$ values of the rows of $R_g$. There is one output row for each group, and no group is empty. The output has no particular order.

**Classes of aggregates** (Gray et al. 1997). Let $X$ be a multiset and $X_1, \ldots, X_r$ a partition of it into multisets.

- $f$ is *distributive* if there is a function $h$ with $f(X) = h(f(X_1), \ldots, f(X_r))$ for every partition. COUNT, SUM, MIN and MAX are distributive (for COUNT, $h$ is the sum).
- $f$ is *algebraic* if there are a fixed $M$, a function $s$ to $M$-tuples that is distributive, and a function $q$ with $f(X) = q(s(X))$. AVG is algebraic with $s(X) = (\text{SUM}(X), \text{COUNT}(X))$ and $q(a, c) = a / c$. Variance is algebraic with $M = 3$.
- $f$ is *holistic* if no state of bounded size describes a part. MEDIAN, MODE, rank and COUNT DISTINCT are holistic.

The cost model for the I/O bounds: $R$ takes $N$ pages on disk, the memory has $B$ pages of buffer, there are $D$ distinct groups, and the cost is the number of page reads and writes. Writing the output is not counted, as in Ramakrishnan and Gehrke.

## Variants

- **Duplicate elimination.** `SELECT DISTINCT` is group-by with $G = U$ and no aggregate.
- **Scalar aggregation.** $G = \emptyset$ makes one group of all rows. In SQL, a scalar aggregate over an empty table still returns one row (COUNT is 0 and SUM is NULL), while the definition above returns no row.
- **HAVING.** A filter on the output rows, applied after the aggregates.
- **Data cube, ROLLUP and GROUPING SETS.** Compute the group-by for many subsets of $G$ at once. The cube over $d$ attributes has $2^d$ group-bys. A distributive or algebraic aggregate of a coarse group can be computed from the finer groups, not from the base rows. This is the reason that Gray et al. introduced the three classes.
- **Streaming and windows.** Aggregates over a moving window of a stream; see [sliding-window aggregation](/sliding-window-aggregation/).
- **Approximate aggregates.** COUNT DISTINCT over a stream is the [distinct elements problem](/distinct-elements-problem/), solved in small space only approximately.

## Examples

Take the table of sales $(region, amount)$: (east, 10), (west, 5), (east, 7), (north, 3), (west, 5), (east, 1). Group by $region$:

| region | COUNT | SUM | MIN | MAX | AVG | MEDIAN | COUNT DISTINCT |
|---|---|---|---|---|---|---|---|
| east | 3 | 18 | 1 | 10 | 6 | 7 | 3 |
| north | 1 | 3 | 3 | 3 | 3 | 3 | 1 |
| west | 2 | 10 | 5 | 5 | 5 | 5 | 1 |

MEDIAN here is the lower median, the item of rank $\lfloor (n-1)/2 \rfloor$ from 0 in sorted order.

**AVG from parts.** Split the east rows into $\{10, 7\}$ and $\{1\}$. The averages of the parts are $17/2$ and $1$, and their mean $19/4$ is not the answer 6. The states $(17, 2)$ and $(1, 1)$ add to $(18, 3)$, and $18/3 = 6$.

**MEDIAN is holistic.** Take $X = \{1, 2, 3\} \cup \{4, 5\}$ and $Y = \{2, 2, 2\} \cup \{4, 5\}$. The parts have the same sizes and the same medians, 2 and 4. But the median of $X$ is 3 and the median of $Y$ is 2. So no function of the part medians and sizes gives the median.

**I/O.** With $N = 1000$ pages and $B = 100$ buffers, sort-based grouping makes 10 runs in pass 0 and aggregates during one merge pass: $2N + N = 3000$ I/Os. With $B = 10$ it makes 100 runs, merges them in 3 passes of fan-in 9, and costs $2N \cdot 4 - N = 7000$ I/Os. If the $D$ group states fit in memory, hash aggregation costs $N = 1000$ I/Os.

## Known algorithms

| algorithm | I/O cost (pages) | condition |
|---|---|---|
| sort, then scan | $2N \cdot P - N$ with $P = 1 + \lceil \log_{B-1} \lceil N/B \rceil \rceil$ passes | any $D$; $3N$ when $N \le B(B-1)$ |
| scan of input sorted on $G$ (stream aggregate) | $N$ | input already in $G$ order, for example by a clustered index |
| [hash aggregation](/hash-aggregation/), one pass | $N$ | the $D$ group states fit in $B$ pages |
| hash aggregation with partitioning | about $3N$ for one partition level | each partition's groups fit in memory |

- **Sort-based.** Sort on $G$ with [external merge sort](/external-merge-sort/), and aggregate in the last merge, so the sorted file is never written. Each run of equal keys is one group. Early aggregation inside the runs (combine equal keys while making a run) makes the runs shorter when there are few groups; Bitton and DeWitt (1983) used this for duplicate removal. The output comes out in $G$ order, which a later `ORDER BY` or merge join can use.
- **Hash-based.** A [hash table](/hash-table/) keyed by $G$ keeps one state per group. Its memory is proportional to $D$, not to $N$. When $D$ is too large, the input is split by a hash of $G$, as in the Grace hash join, and each part is aggregated alone. See [hash aggregation](/hash-aggregation/).
- **Holistic aggregates.** MEDIAN needs the whole group. A sort on $(G, A)$ gives it in one scan. A hash plan must keep all values of a group, or sort each group.

The implementation below is the sort-based plan, with each aggregate given by an initial state, a merge of states and a final step.

## Bounds

- **Comparison model.** Grouping needs $\Omega(n \log n)$ comparisons on $n$ rows in the worst case, also in the [algebraic decision tree](/algebraic-decision-tree/) model. The reduction is from [element distinctness](/element-distinctness/): group $n$ numbers by value and count the groups; the numbers are distinct if and only if there are $n$ groups. The reduction adds $O(n)$ work. Sorting matches the bound.
- **Hashing.** With a hash table, the expected time is $O(n)$ for distributive and algebraic aggregates, plus the cost of the output. This is outside the comparison model, so the lower bound does not apply.
- **Space.** The hash plan keeps $\Theta(D)$ states in memory, each of $O(1)$ size for a distributive or algebraic aggregate. A holistic aggregate can need space for all the values of the largest group.
- **I/O.** Sort-based grouping matches the cost of external sorting, $O(N \log_{B} (N/B))$ page I/Os. Two passes suffice when $N \le B(B-1)$ for sorting, and for hashing when the group states of each of the $B - 1$ partitions fit in memory.

## Reductions

- Duplicate elimination is group-by with no aggregate, and element distinctness reduces to it, as above.
- Group-by reduces to sorting: sort on $G$ and scan. It also reduces to building a dictionary on $G$.
- The MapReduce reduce step is a group-by on the key. A [combiner](/combiner/) is the partial aggregation of a distributive or algebraic function before the shuffle; [word count](/word-count/) is COUNT grouped by word.
- In parallel and distributed plans, rows are sent to workers by [hash partitioning](/hash-partitioning/) on $G$, so that each group is on one worker; distributive and algebraic aggregates are first computed locally, which cuts the data sent.

## Applications

- Reports and OLAP: totals by month, region and product, and the data cube over them.
- Duplicate removal for `DISTINCT`, `UNION` and set semantics in the [relational model](/relational-model/).
- Building histograms and statistics for the query optimizer.
- Log analysis and counting in batch systems: count the events of each user, the words of each document.

## References
