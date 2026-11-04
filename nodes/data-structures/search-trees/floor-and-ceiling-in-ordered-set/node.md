---
tag: B8GREY
kind: problem
slug: floor-and-ceiling-in-ordered-set
name: Floor and ceiling in an ordered set
aliases:
- Floor and ceiling
- predecessor and successor queries
area: data-structures/search-trees
level: core
summary: Queries returning the largest key at most a given key, or the smallest key at least a given key.
prereqs: [ordered-set, total-order]
see_also: [bst-floor-and-ceiling, predecessor-problem, binary-search, ordered-symbol-table, skip-list, fusion-tree, sorted-search-lower-bound, predecessor-lower-bound]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1 (Symbol tables), the ordered symbol table API, floor() and ceiling(), and Section 3.2 for the tree versions
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: the introduction to Part III (operations on dynamic sets), SUCCESSOR and PREDECESSOR
  - paper: doi:10.1145/1132516.1132551
    title: Mihai Pătraşcu and Mikkel Thorup, Time-space trade-offs for predecessor search, STOC 2006
    locator: the whole paper
---

The floor and ceiling problem asks, for a set $S$ of keys from a [total order](/total-order/) and a query key $k$, for the largest element of $S$ that is at most $k$ (the floor) and the smallest element that is at least $k$ (the ceiling). The query key need not be in $S$. In the static case $S$ is fixed and [binary search](/binary-search/) solves it in $O(\log n)$ comparisons; in the dynamic case $S$ also changes by inserts and deletes, and a balanced search tree solves it in $O(\log n)$ time per operation. For integer keys it is the [predecessor problem](/predecessor-problem/), which has faster solutions on the [word RAM](/word-ram/).

## In plain words

You have a set of numbers and one more number, which may or may not be in the set. The floor is the closest number of the set that is not above it. The ceiling is the closest number of the set that is not below it. If your number is in the set, both are your number. If it is below everything in the set, there is no floor; if it is above everything, there is no ceiling.

The point of the problem is to answer this fast for many questions, without looking at all the numbers each time.

## Definition

Let $(U, <)$ be a total order and $S \subseteq U$ a finite set with $n$ elements. For $k \in U$:

$$\mathrm{floor}_S(k) = \max\{s \in S : s \le k\}, \qquad \mathrm{ceiling}_S(k) = \min\{s \in S : s \ge k\},$$

where the maximum or the minimum of an empty set is NIL.

**Static version.** Preprocess $S$ into a data structure, then answer queries $\mathrm{floor}_S(k)$ and $\mathrm{ceiling}_S(k)$.

**Dynamic version.** Keep a data structure for a set $S$ that starts empty, under the operations insert$(x)$, delete$(x)$, floor$(k)$ and ceiling$(k)$.

The strict versions are $\mathrm{lower}_S(k) = \max\{s \in S : s < k\}$ (the predecessor) and $\mathrm{higher}_S(k) = \min\{s \in S : s > k\}$ (the successor). Each version can be computed from the others with one membership test: $\mathrm{floor}_S(k) = k$ if $k \in S$ and $\mathrm{lower}_S(k)$ otherwise.

## Variants

- **Predecessor and successor.** The strict forms above. In the literature on integer keys, the "predecessor problem" often means the floor query.
- **Integer keys.** $U = \{0, 1, \ldots, 2^w - 1\}$ on a word RAM with $w$-bit words: the [predecessor problem](/predecessor-problem/).
- **Nearest neighbour in one dimension.** Return whichever of the floor and the ceiling is nearer to $k$.
- **With values.** In an [ordered symbol table](/ordered-symbol-table/), return the value stored with the floor key.
- **Offline.** All queries are known in advance; sort them together with $S$ and answer all of them in one merge.
- **External memory.** $S$ is on disk in blocks of $B$ keys, and the cost is the number of block reads.

## Examples

Let $S = \{20, 30, 35, 40, 45, 50, 60, 65, 70, 80\}$.

| $k$ | floor | ceiling | lower | higher |
|---|---|---|---|---|
| 62 | 60 | 65 | 60 | 65 |
| 45 | 45 | 45 | 40 | 50 |
| 10 | NIL | 20 | NIL | 20 |
| 90 | 80 | NIL | 80 | NIL |
| 20 | 20 | 20 | NIL | 30 |

On a sorted array $A[0..n-1]$, the floor of $k$ is $A[i - 1]$ where $i$ is the number of elements $\le k$ (NIL if $i = 0$), and the ceiling is $A[j]$ where $j$ is the number of elements $< k$ (NIL if $j = n$). For $k = 62$, $i = j = 7$, so the floor is $A[6] = 60$ and the ceiling is $A[7] = 65$.

## Known algorithms

| method | model | query | update | space |
|---|---|---|---|---|
| linear scan | comparison | $O(n)$ | $O(1)$ | $O(n)$ |
| [binary search](/binary-search/) on a sorted array | comparison | $O(\log n)$ | $O(n)$ | $O(n)$ |
| [BST floor and ceiling](/bst-floor-and-ceiling/) on a plain BST | comparison | $O(h)$ | $O(h)$ | $O(n)$ |
| balanced BST ([red-black tree](/red-black-tree/), [AVL tree](/avl-tree/)) | comparison | $O(\log n)$ worst | $O(\log n)$ worst | $O(n)$ |
| [skip list](/skip-list/) | comparison | $O(\log n)$ expected | $O(\log n)$ expected | $O(n)$ expected |
| [splay tree](/splay-tree/) | comparison | $O(\log n)$ amortized | $O(\log n)$ amortized | $O(n)$ |
| [B-tree](/b-tree/) | external memory | $O(\log_B n)$ block reads | $O(\log_B n)$ | $O(n/B)$ blocks |
| [fusion tree](/fusion-tree/) | word RAM | $O(\log_w n)$ | amortized; see the [fusion tree](/fusion-tree/) page | $O(n)$ |

For integer keys, the van Emde Boas structure answers queries in $O(\log w)$ time, and the [predecessor problem](/predecessor-problem/) page gives the full picture.

## Bounds

- **Comparison model.** Each algorithm that answers floor queries on $n$ keys with comparisons needs $\lceil \lg(n+1) \rceil$ comparisons in the worst case: the $n + 1$ answers NIL, $s_1, \ldots, s_n$ are all possible, so the decision tree has at least $n + 1$ leaves. Binary search meets this bound. See the [sorted search lower bound](/sorted-search-lower-bound/).
- **Dynamic, comparison model.** A dynamic structure with inserts and floor queries sorts: insert $n$ keys, then find the minimum with a ceiling query of the least possible key and step from each key $s$ to the next with a strict higher query. Sorting needs $\Omega(n \log n)$ comparisons, so the operations cost $\Omega(\log n)$ amortized.
- **Word RAM.** With $n$ keys of $w$ bits and space polynomial in $n$, Pătraşcu and Thorup (2006) give tight bounds for static predecessor search as a function of $n$, $w$ and the space. In some ranges of these parameters the bounds of the van Emde Boas structure and of the fusion tree are optimal. See the [predecessor lower bound](/predecessor-lower-bound/).

## Reductions

- **Floor from lower and membership**, and back: $\mathrm{floor}(k) = k$ if $k \in S$, else $\mathrm{lower}(k)$. In the other direction, for integer keys, $\mathrm{lower}(k) = \mathrm{floor}(k - 1)$.
- **Ceiling from floor by reversal.** Reverse the order (for integers, map $x$ to $-x$ or to $2^w - 1 - x$); the floor in the reversed order is the ceiling.
- **Rank gives floor.** If $\mathrm{rank}(k)$ is the number of keys $\le k$ and select returns the key of a given rank, then $\mathrm{floor}(k) = \mathrm{select}(\mathrm{rank}(k))$ for $\mathrm{rank}(k) \ge 1$; see [rank](/rank/).
- **Sorting reduces to the dynamic problem**, as in the bound above.
- **One-dimensional range search** reduces to it: the keys in $[lo, hi]$ are the keys from $\mathrm{ceiling}(lo)$ to $\mathrm{floor}(hi)$; see [one-dimensional range search](/one-dimensional-range-search/).

## Applications

- **Routing tables.** IP lookup by longest prefix match can be cast as a predecessor query over interval end points.
- **Time series.** The last reading at or before a given time is a floor query on the timestamps.
- **Memory allocation.** The free block at the lowest address at or above a given address is a ceiling query.
- **Interval maps.** If the intervals are disjoint and stored by their left end points, the interval that holds a point $p$ is the one whose left end is the floor of $p$.
- **Databases.** Range scans on an index start with a ceiling query, which a [B-tree](/b-tree/) answers in $O(\log_B n)$ block reads.

## References
