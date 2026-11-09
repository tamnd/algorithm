---
tag: 3FKMS3
kind: problem
slug: one-dimensional-range-search
name: One-dimensional range search
aliases:
- 1D range search
- interval query on keys
- one-dimensional range reporting
area: geometry/range-searching
level: intro
summary: Report all keys of a symbol table that fall in a given interval [lo, hi].
prereqs: [binary-search, binary-search-tree]
see_also: [bst-range-search, orthogonal-range-searching, orthogonal-range-counting, range-emptiness-query, floor-and-ceiling-in-ordered-set, sorted-search-lower-bound, range-tree, b-tree]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Section 5.1, 1-Dimensional Range Searching
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 2, Section 2.3, Range-searching problems (section number to be checked)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2, Orthogonal range searching
  - paper: doi:10.1145/380752.380842
    title: Stephen Alstrup, Gerth Stølting Brodal and Theis Rauhe, Optimal static range reporting in one dimension, STOC 2001, pages 476 to 482
    locator: linear space and O(1 + k) query on the word RAM (DOI to be checked)
---

One-dimensional range search is the problem of storing a finite set $P$ of keys on a line so that, for a query interval $[lo, hi]$, the keys of $P$ inside the interval can be reported, counted or tested for existence. It is the base case of [orthogonal range searching](/orthogonal-range-searching/), and every structure for $d$ dimensions starts from it. A sorted array or a [balanced binary search tree](/balanced-binary-search-tree/) answers a reporting query in $O(\log n + k)$ time, where $k$ is the number of reported keys, and this is optimal in the comparison model.

## In plain words

A list of numbers is stored, for example the prices of all items in a shop. A question names a lowest and a highest price, and the answer is every item whose price lies between them, including the two ends. Other versions of the question ask only how many such items there are, or whether there is at least one.

If the prices are kept in sorted order, the answer is easy. Find where the lowest price would go, then walk forward until the prices become too large. The search costs a few steps, and the walk costs one step per item in the answer. A [search tree](/binary-search-tree/) does the same and also allows new items to arrive and old ones to leave.

## Definition

**Notation.** $P$ is the input set of keys (points on the real line, $d = 1$), $n = |P|$ the input size, and $k$ the output size of a reporting query, the number of keys in the range. The predicates $\mathrm{orient}$ and $\mathrm{incircle}$ are not needed in one dimension; the only predicate is the comparison of two keys.

**Input.** A multiset $P$ of $n$ keys from a totally ordered set, for example integers or rationals. Equal keys are allowed and are reported once per copy.

**Query.** Two keys $lo$ and $hi$. The range is the closed interval $[lo, hi] = \{x : lo \le x \le hi\}$. If $lo > hi$ the range is empty. Half-open ranges $[lo, hi)$ reduce to closed ones over integers ($hi - 1$) and are otherwise handled by replacing one $\le$ by $<$.

**Output.** One of:

- *reporting*: all keys $x \in P$ with $lo \le x \le hi$, in any order (or sorted, which is free for the structures below);
- *counting*: the number $|P \cap [lo, hi]|$;
- *emptiness*: whether $P \cap [lo, hi] = \emptyset$.

Keys may carry values. With a weight $w(x)$ from a commutative [monoid](/monoid/), the *aggregate* version asks for the sum of $w(x)$ over the keys in the range.

**Degenerate input.** Duplicates and query end points equal to keys are the only degeneracies in one dimension. The closed range includes the end points, so a key equal to $lo$ or $hi$ is reported.

## Variants

- **Static or dynamic.** In the static version $P$ is fixed and preprocessing is allowed. In the dynamic version keys are inserted and deleted between queries.
- **Reporting, counting, emptiness, aggregate.** See above. Emptiness is the special case of counting with the answer compared to zero, and also of reporting with $k \le 1$ asked for.
- **Successor and predecessor.** With $hi = +\infty$ and the first key wanted, the query is the successor query; see [floor and ceiling in an ordered set](/floor-and-ceiling-in-ordered-set/).
- **External memory.** Keys in blocks of size $B$ on disk; a [B-tree](/b-tree/) answers a query with $O(\log_B n + k/B)$ block reads.

## Examples

Let $P = \{2, 5, 9, 12, 15, 19, 23, 27, 31\}$, so $n = 9$.

| query $[lo, hi]$ | reported keys | count | empty |
|---|---|---|---|
| $[10, 24]$ | $12, 15, 19, 23$ | 4 | no |
| $[9, 9]$ | $9$ | 1 | no |
| $[13, 14]$ | none | 0 | yes |
| $[-5, 1]$ | none | 0 | yes |
| $[31, 40]$ | $31$ | 1 | no |
| $[20, 10]$ | none, since $lo > hi$ | 0 | yes |

In a sorted array the query $[10, 24]$ finds the first index with a key $\ge 10$ (index 3, key 12) and the first index with a key $> 24$ (index 7, key 27). The answer is the slice of indices 3 to 6, and the count is $7 - 3 = 4$.

## Known algorithms

| structure | build | space | query (report) | query (count) | update |
|---|---|---|---|---|---|
| unsorted array, linear scan | $O(1)$ | $O(n)$ | $O(n)$ worst case | $O(n)$ worst case | $O(1)$ |
| sorted array with [binary search](/binary-search/) | $O(n \log n)$ | $O(n)$ | $O(\log n + k)$ worst case | $O(\log n)$ worst case | $O(n)$ worst case |
| [balanced binary search tree](/balanced-binary-search-tree/) with [range search](/bst-range-search/) | $O(n \log n)$ | $O(n)$ | $O(\log n + k)$ worst case | $O(\log n)$ worst case with subtree sizes | $O(\log n)$ worst case |
| [order statistic tree](/order-statistic-tree/) | $O(n \log n)$ | $O(n)$ | $O(\log n + k)$ worst case | $O(\log n)$ worst case | $O(\log n)$ worst case |
| [B-tree](/b-tree/), external memory | $O(n \log n)$ | $O(n/B)$ blocks | $O(\log_B n + k/B)$ I/Os | $O(\log_B n)$ I/Os | $O(\log_B n)$ I/Os |
| Alstrup, Brodal and Rauhe, word RAM, integer keys | polynomial, see the paper | $O(n)$ | $O(1 + k)$ worst case | | static |

The two binary searches of the sorted array are the lower and upper bound searches: the count is $\mathrm{upper}(hi) - \mathrm{lower}(lo)$, where $\mathrm{lower}(lo)$ is the number of keys $< lo$ and $\mathrm{upper}(hi)$ the number of keys $\le hi$.

## Bounds

- **Comparison model, lower bound.** Emptiness with $lo = hi = x$ is the membership query "is $x \in P$", which needs $\Omega(\log n)$ comparisons in the worst case; see the [sorted search lower bound](/sorted-search-lower-bound/). Reporting must also write the $k$ keys, so $\Omega(\log n + k)$ holds, and the balanced tree matches it.
- **Preprocessing.** Building a sorted array or a search tree from unsorted keys needs $\Omega(n \log n)$ comparisons in the comparison model, since the in-order listing sorts the keys.
- **Word RAM.** With integer keys of $w$ binary digits, the $\Omega(\log n)$ bound does not apply. Alstrup, Brodal and Rauhe (2001) give a static structure of linear size with $O(1 + k)$ query time for reporting; the related successor queries are bounded below by Pătraşcu and Thorup's cell probe results.

## Reductions

- **To two-dimensional searching.** One-dimensional range search is orthogonal range searching with $d = 1$, and the $d$-dimensional [range tree](/range-tree/) recurses on dimension until it reaches this problem.
- **From membership.** Membership reduces to emptiness by setting $lo = hi$.
- **Counting by two rank queries.** Counting reduces to two rank queries: $|P \cap [lo, hi]| = \mathrm{rank}_{\le}(hi) - \mathrm{rank}_{<}(lo)$. This is also what a [Fenwick tree](/fenwick-tree/) over compressed keys computes in the dynamic setting.

## Applications

- Database queries of the form "salary between $a$ and $b$" on an indexed column, answered by a B-tree index.
- The last level of [range trees](/range-tree/) and [layered range trees](/layered-range-tree/), and the canonical subsets of [segment trees](/segment-tree/).
- Time-window queries on event logs sorted by time.

## References
