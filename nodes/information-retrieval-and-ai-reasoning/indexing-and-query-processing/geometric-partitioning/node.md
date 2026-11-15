---
tag: J597QM
kind: algorithm
slug: geometric-partitioning
name: Geometric partitioning
aliases:
- Lester-Moffat-Zobel geometric partitioning
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: advanced
summary: Keeps index partitions whose sizes grow geometrically by a ratio r, or at most p of them, trading merge cost against the number of partitions a query reads.
solves: [dynamic-index-maintenance]
model: external-memory-model
complexity:
  vars: {T: the number of postings added so far, b: the number of postings in the in-memory buffer, m: the number of buffer flushes (the floor of T/b), r: the radix (the ratio between partition sizes), p: the bound on the number of partitions in the fixed-p variant}
  time: {build: O(r T log(T/b) / log r), insert: O(r log(T/b) / log r) amortized, partitions_per_query: O(log(T/b) / log r), build_fixed_p: O(T (T/b)^(1/p))}
  space: {memory: O(b), disk: O(T)}
properties: {deterministic: true, online: true, recursive: false, comparison: true, in_place: false}
prereqs: [logarithmic-merging, k-way-merge, dynamic-index-maintenance]
see_also: [log-structured-merge-tree, decomposable-searching-problem, single-pass-in-memory-indexing, inverted-index, posting-list, external-merge-sort, amortized-cost, tiered-index]
sources:
  - paper: doi:10.1145/1099554.1099739
    title: Nicholas Lester, Alistair Moffat and Justin Zobel, Fast on-line index construction by geometric partitioning, Proceedings of the 14th ACM International Conference on Information and Knowledge Management (CIKM 2005), pages 776 to 783
    locator: Section 3 (merge-based update, rebuild, in-place update and remerge) and Section 4 (geometric partitioning, the radix r and the fixed number p of partitions)
  - paper: doi:10.1145/1386118.1386125
    title: Nicholas Lester, Alistair Moffat and Justin Zobel, Efficient online index construction for text databases, ACM Transactions on Database Systems 33(3), Article 19, 2008
    locator: the journal version, with geometric partitioning and its comparison with in-place and remerge strategies
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 7 (dynamic inverted indices), Section 7.2 (incremental index updates)
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 4, Section 4.5 (dynamic indexing and logarithmic merging, the case of ratio 2)
---

Geometric partitioning keeps an [inverted index](/inverted-index/) up to date while documents arrive, by holding the index in a few partitions on disk whose sizes grow by a factor $r$ from one level to the next. A full in-memory buffer of $b$ postings is merged with the smaller partitions in one multiway merge, and the partitions behave like the digits of a counter in base $r$. Lester, Moffat and Zobel proposed it in 2005, with a second form that fixes the number of partitions at $p$ and lets $r$ grow. [Logarithmic merging](/logarithmic-merging/) is close to the case $r = 2$, but it merges pairwise; this page covers the general radix, the cost in postings written as a function of $r$, and the fixed-$p$ form. The [log-structured merge tree](/log-structured-merge-tree/) uses the same idea for key-value stores.

## In plain words

A growing index on disk can be kept as one big file, but then each batch of new documents forces a rewrite of the whole file. It can also be kept as many small files, but then each search has to open all of them. Geometric partitioning is a middle way. It keeps a few files, each one about $r$ times larger than the one before. New documents fill a buffer in memory. When the buffer is full, it is joined with the small files into one new file. Large files are rewritten only rarely. A larger $r$ means fewer files to search but more rewriting. A smaller $r$ means less rewriting but more files.

## The problem

Postings arrive one at a time. After each arrival a query for a term must return its full posting list. The cost to measure is the number of postings written to disk by merges, and the number of partitions a query must read. With one partition, the remerge strategy, each flush rewrites the whole index, and $m$ flushes write $b(1 + 2 + \cdots + m) = \Theta(m^2 b)$ postings. With no merge at all, a query reads $m$ partitions. The general problem is [dynamic index maintenance](/dynamic-index-maintenance/).

## The algorithm

Partition $P_k$, for $k = 1, 2, \ldots$, is one sorted index on disk. It is either empty or holds $j \cdot r^{k-1} b$ postings with $1 \le j \le r - 1$, so it is full when it holds $(r - 1) r^{k-1} b$. $Z$ is the buffer in memory.

```pseudo id=main
GEOM-ADD(x)                            ▷ r ≥ 2, buffer capacity b
L1  add x to the buffer Z
L2  if |Z| = b then
L3      k ← 1
L4      while P_k holds (r - 1) r^(k-1) b postings do k ← k + 1
L5      P_k ← MULTIWAY-MERGE(Z, P_1, ..., P_k)    ▷ one pass, written to disk
L6      make Z and P_1, ..., P_(k-1) empty

QUERY(t)
L7  read the list of t from Z and from each partition that is not empty
L8  return the union of these lists, in increasing document id order
```

Line L1 puts the posting in the buffer. When the buffer is full (line L2), lines L3 and L4 look for the first partition that is not full. Line L5 merges the buffer with all partitions up to that one in a single pass, as a [k-way merge](/k-way-merge/), and stores the result as the new $P_k$. The partitions below $k$ were full, so their content now sits in $P_k$, and line L6 empties them. Because $P_1, \ldots, P_{k-1}$ held $(r - 1)(1 + r + \cdots + r^{k-2}) b = (r^{k-1} - 1) b$ postings, the buffer and these partitions add exactly $r^{k-1} b$ postings to $P_k$, one unit of its level. So, after $m$ flushes, $P_k$ holds $\delta_k r^{k-1} b$ postings, where $\delta_k$ is digit $k$ of $m$ in base $r$. Lines L7 and L8 answer a query from the buffer and all partitions.

## Example

Take $r = 3$ and count postings in units of $b$. Nine flushes give this trace. The digits are those of the flush count in base 3, with $P_1$ on the right.

| flush $t$ | $t$ in base 3 | first partition not full | merged at line L5 | sizes of $P_3, P_2, P_1$ after | written |
|---|---|---|---|---|---|
| 1 | 1 | $P_1$ | $Z$ | 0, 0, 1 | 1 |
| 2 | 2 | $P_1$ | $Z$, $P_1$ | 0, 0, 2 | 2 |
| 3 | 10 | $P_2$ | $Z$, $P_1$, $P_2$ | 0, 3, 0 | 3 |
| 4 | 11 | $P_1$ | $Z$ | 0, 3, 1 | 1 |
| 5 | 12 | $P_1$ | $Z$, $P_1$ | 0, 3, 2 | 2 |
| 6 | 20 | $P_2$ | $Z$, $P_1$, $P_2$ | 0, 6, 0 | 6 |
| 7 | 21 | $P_1$ | $Z$ | 0, 6, 1 | 1 |
| 8 | 22 | $P_1$ | $Z$, $P_1$ | 0, 6, 2 | 2 |
| 9 | 100 | $P_3$ | $Z$, $P_1$, $P_2$, $P_3$ | 9, 0, 0 | 9 |

The nine flushes write $27b$ postings, against $(1 + 2 + \cdots + 9) b = 45b$ for remerge into one index. The postings of flush 1 are written 5 times: twice at level 1, twice at level 2 and once at level 3. This is the case shown in the figure of Lester, Moffat and Zobel, nine bufferloads that end as one partition of $9b$.

For a longer run, take $m = 1000$ flushes. The postings written, in units of $b$, and the partitions are:

| strategy | postings written | partitions that can exist | nonempty after 1000 flushes |
|---|---|---|---|
| remerge, one partition | 500,500 | 1 | 1 |
| $r = 10$ | 14,500 | 4 | 1 |
| $r = 4$ | 7,560 | 5 | 4 |
| $r = 3$ | 6,670 | 7 | 4 |
| $r = 2$ | 5,060 | 10 | 6 |

## Correctness

After $m$ flushes and $s$ further postings, the buffer holds $s$ postings and partition $P_k$ holds $\delta_k r^{k-1} b$ postings, where $\delta_k$ is the $k$-th digit of $m$ in base $r$. A partition is full exactly when its digit is $r - 1$. A flush finds the first digit below $r - 1$, and the merge of line L5 holds $b + (r^{k-1} - 1) b + \delta_k r^{k-1} b = (\delta_k + 1) r^{k-1} b$ postings, which is the new digit $\delta_k + 1$ at level $k$ with all lower digits 0. This is the addition of 1 in base $r$. Each merge moves postings and never copies them, so the buffer and the partitions hold disjoint sets whose union is everything added, and a query that takes the union of all lists is correct. The full proof is in the proof file below.

## Complexity

- **Merge size.** Flush $t$ writes $(t \bmod r^{v+1}) b$ postings, where $v$ is the number of times $r$ divides $t$. After $m$ flushes the total is $b \sum_{t=1}^{m} (t \bmod r^{v_r(t)+1})$.
- **Writes for one posting.** At each level a posting is written at most $r - 1$ times: once when it enters the level and once for each later increase of that digit. The levels in use are at most $1 + \lfloor \log_r m \rfloor$. So each posting is written at most $(r - 1)(1 + \lfloor \log_r m \rfloor)$ times, and the build costs $O(r T \log(T/b) / \log r)$ postings written. For $r = 2$ this is $O(T \log(T/b))$, as for logarithmic merging.
- **Queries.** A query reads the buffer and at most $1 + \lfloor \log_r m \rfloor$ partitions. A larger $r$ means fewer partitions and more writes.
- **Fixed number of partitions.** If at most $p$ partitions may exist, the radix must grow with the index, to about $(T/b)^{1/p}$. Then each posting is written $O((T/b)^{1/p})$ times, and the build costs $O(T (T/b)^{1/p})$. With $p = 1$ this is remerge, with its $\Theta(T^2/b)$ cost. With $p = 2$ the cost is $O(T \sqrt{T/b})$ and each query reads at most two partitions.
- **Space.** $O(b)$ words of memory for the buffer, and $O(T)$ words of disk, plus room for the output of one merge.

## Properties

- **Online.** A posting can be found by queries right after GEOM-ADD returns.
- **One merge per flush.** Unlike the chain of pairwise merges of logarithmic merging, one flush does one multiway merge, so a posting moves up several levels in one write.
- **Tunable.** The radix $r$, or the bound $p$, sets the trade-off between update cost and query cost.
- **Deterministic.** The partition sizes depend only on $m$, $r$ and $b$.

## Variants and improvements

- **Fixed $p$.** Lester, Moffat and Zobel also describe the form in which the number of partitions is bounded by $p$, and the radix is chosen from the current size so that $p$ partitions are enough. The radix then grows slowly as the index grows.
- **Hybrid with in-place update.** Long posting lists can be kept in a separate structure that is updated in place, so that the merges only rewrite the short lists.
- **Ratio 2 with pairwise merges.** Manning, Raghavan and Schuetze present the case $r = 2$ as logarithmic merging, with a chain of pairwise merges for a carry. See [logarithmic merging](/logarithmic-merging/).
- **Leveled and tiered merge policies.** In a [log-structured merge tree](/log-structured-merge-tree/), a leveled policy keeps one run per level, like remerge at each level, and a tiered policy keeps up to $r$ runs per level, like geometric partitioning.
- **Deletions.** As for other merge schemes, deleted documents go to an invalidation list, and the merges drop their postings when they rewrite a partition.

## When to use it

Use geometric partitioning for a text index that grows all the time while it answers queries, when a full remerge at each flush is too slow and a large number of partitions would slow the queries. Pick $r$ from the ratio of queries to updates: a small $r$ for heavy update loads, a larger $r$, or the fixed-$p$ form with $p = 2$ or 3, when queries dominate. For a static collection, build once with [single-pass in-memory indexing](/single-pass-in-memory-indexing/).

## Pitfalls

- **Merging only with the next partition.** If line L5 merges the buffer only with $P_k$ and leaves $P_1, \ldots, P_{k-1}$ in place, the partitions below $k$ stay full, the next flush finds the same $k$ again, and the sizes no longer follow the counter. The merge must take all of $Z, P_1, \ldots, P_k$, as in line L5, and line L6 must empty the lower partitions.
- **Wrong full test.** The test of line L4 must compare with the capacity $(r - 1) r^{k-1} b$. With a smaller threshold such as $r^{k-1} b$, a level is merged up before it is full, the sizes stop following the base $r$ counter, and the bounds of the Complexity section no longer hold.
- **Claiming a fixed number of partitions with a fixed $r$.** With a fixed radix, the number of partitions grows as $\log_r(T/b)$. Only the fixed-$p$ form bounds it, and then the merge cost grows as a power of $T$.
- **Statistics per partition.** A ranking function needs collection-wide document frequencies. They must be summed over the partitions, or kept in a separate table, or the scores change with the partition layout.
- **Disk space during a merge.** The new partition is written before the old ones are deleted, so the largest merge needs free disk space for a copy of most of the index.

## Implementations

## History

Lester, Moffat and Zobel introduced geometric partitioning at CIKM 2005, after a study of the rebuild, in-place and remerge strategies for on-line index construction, and they extended the work in a 2008 journal paper in ACM Transactions on Database Systems. The same structure with ratio 2 appears as logarithmic merging in the textbook of Manning, Raghavan and Schuetze, and it is a form of the binary transformation of Bentley and Saxe for [decomposable searching problems](/decomposable-searching-problem/).

## References
