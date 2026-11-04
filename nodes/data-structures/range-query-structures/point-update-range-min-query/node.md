---
tag: ZE0P4A
kind: problem
slug: point-update-range-min-query
name: Point update range minimum query
aliases:
- dynamic RMQ
- range minimum with point updates
area: data-structures/range-query-structures
level: core
summary: Support changing one element and answering range minimum queries.
model: comparison-model
complexity:
  vars: {n: the length of the array}
  time: {amortized: Ω(log n)}
prereqs: [range-minimum-query, idempotent-operation, monoid]
see_also: [segment-tree, point-update-range-sum-query, sparse-table, square-root-decomposition, priority-queue, comparison-sort-lower-bound, fenwick-tree, lazy-propagation]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 9, Range queries, Section 9.3 Segment tree (other queries, such as minimum queries, with point updates)
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: the section More complex queries, subsection Finding the maximum, and the section Update queries
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 8.1, Lower bounds for sorting (the decision-tree model and the bound lg(n!) on the number of comparisons)
---

The point update range minimum query problem keeps an array of $n$ items from a totally ordered set under two operations: change one item, and return the smallest item, or its position, in a range $[l, r]$. It is the dynamic form of the [range minimum query](/range-minimum-query/). Minimum has no inverse, so the subtraction trick of the [point update range sum query](/point-update-range-sum-query/) does not apply, and it is [idempotent](/idempotent-operation/), but the overlap trick of the [sparse table](/sparse-table/) does not survive updates. A [segment tree](/segment-tree/) solves it in $O(\log n)$ time per operation, and a sorting argument shows that $\Omega(\log n)$ comparisons per operation are needed in the [comparison model](/comparison-model/) for a structure that is built with $O(n)$ comparisons.

## In plain words

You keep a row of numbers, for example the prices of a product in many shops. One kind of request says "shop 5 now asks 12". The other asks "what is the cheapest price among shops 3 to 9?".

Running totals do not help here, because you cannot take a minimum back out like you take a sum back out. A table of all answers would need a big rebuild after each change. The standard answer is a tree in which each box holds the cheapest price of one stretch of shops. A change fixes the boxes above one shop, and a question combines a few boxes. Both take a number of steps that grows with the number of digits of the row length, and no method that only compares prices can do much better.

## Definition

**Data.** An array $A[1 \ldots n]$ over a totally ordered set $(X, \le)$, given at the start.

**Operations.** A sequence of operations, each answered before the next one is read:

- $\textsc{update}(i, x)$ with $1 \le i \le n$: set $A[i] \leftarrow x$;
- $\textsc{min}(l, r)$ with $1 \le l \le r \le n$: return $\min \{A[k] : l \le k \le r\}$;
- the position form $\textsc{argmin}(l, r)$: return the least $k \in [l, r]$ with $A[k] = \textsc{min}(l, r)$.

**Cost.** The preprocessing cost, the cost $t_u$ of an update and the cost $t_q$ of a query. In the comparison model the cost counts comparisons between items; on the word RAM it is time.

The position form is at least as strong as the value form: one more array lookup gives the value. Over a structure that returns values, the position can be kept by storing pairs $(A[k], k)$ ordered first by value and then by index, so the two forms have the same cost up to a constant.

## Variants

- **Maximum.** The same problem with $\max$, or with $\min$ on the negated items.
- **Decrease only.** Updates only lower items: $A[i] \leftarrow \min(A[i], x)$. Prefix minima then work with a [Fenwick tree](/fenwick-tree/), because a prefix minimum changes in the same way as the new item.
- **Range assignment or range add.** Updates set or shift a whole range; a segment tree with [lazy propagation](/lazy-propagation/) solves them in $O(\log n)$.
- **Any idempotent monoid.** The same structures answer greatest common divisors, bitwise and, bitwise or, and maxima, since they use only associativity.
- **Static.** No updates; this is the [range minimum query](/range-minimum-query/), with $O(1)$ queries after $O(n)$ preprocessing.
- **Whole range only.** If every query is $[1, n]$, the problem is a [priority queue](/priority-queue/) with a [decrease-key](/decrease-key/) and an increase-key by position.

## Examples

Start with $A = [5, 2, 8, 6, 3, 7, 9, 1]$.

| operation | array after | answer |
|---|---|---|
| $\textsc{min}(1, 8)$ | $[5, 2, 8, 6, 3, 7, 9, 1]$ | 1 (at position 8) |
| $\textsc{min}(3, 6)$ | $[5, 2, 8, 6, 3, 7, 9, 1]$ | 3 (at position 5) |
| $\textsc{update}(5, 10)$ | $[5, 2, 8, 6, 10, 7, 9, 1]$ | |
| $\textsc{min}(3, 6)$ | $[5, 2, 8, 6, 10, 7, 9, 1]$ | 6 (at position 4) |
| $\textsc{update}(7, 0)$ | $[5, 2, 8, 6, 10, 7, 0, 1]$ | |
| $\textsc{min}(4, 8)$ | $[5, 2, 8, 6, 10, 7, 0, 1]$ | 0 (at position 7) |
| $\textsc{min}(1, 3)$ | $[5, 2, 8, 6, 10, 7, 0, 1]$ | 2 (at position 2) |

The third row shows why a sparse table fails here: the stored minimum 3 of $A[4 \ldots 5]$ and of $A[5 \ldots 6]$ becomes wrong after the update, and so does every table entry whose range contains position 5, which is about $2n$ entries in a table over $n$ items.

## Known algorithms

| method | update | query | space | notes |
|---|---|---|---|---|
| plain array | $O(1)$ | $O(n)$ | $n$ | scan the range |
| [sparse table](/sparse-table/) | $O(n \log n)$ | $O(1)$ | $n \lg n$ | rebuild after each update |
| [square-root decomposition](/square-root-decomposition/) | $O(\sqrt n)$ | $O(\sqrt n)$ | $n + \sqrt n$ | recompute one block minimum |
| [segment tree](/segment-tree/) | $O(\log n)$ | $O(\log n)$ | $2n$ | bottom-up form, any monoid |
| balanced search tree by position | $O(\log n)$ | $O(\log n)$ | $O(n)$ | with subtree minima; also insertions and deletions |
| [Fenwick tree](/fenwick-tree/) of prefix minima | $O(\log n)$ | $O(\log n)$ | $n$ | only decreases and prefix queries |

All times are worst case. The segment tree is the standard choice: an update walks from a leaf to the root and recomputes $\lfloor \lg n \rfloor + 1$ minima, and a query combines at most $2 \lceil \lg n \rceil$ nodes. With square-root decomposition, an update that only lowers an item costs $O(1)$, since the block minimum changes to $\min(\text{old}, x)$.

## Bounds

**Lower bound (comparison model).** Let a structure for the position form be built from $A$ with $P(n)$ comparisons, and let its operations cost $t_u$ and $t_q$ comparisons, amortized. Then

$$ P(n) + n \, (t_u + t_q) \ge \lg (n!) = n \lg n - O(n). $$

*Proof.* Build the structure on $n$ distinct items. Repeat $n$ times: $k \leftarrow \textsc{argmin}(1, n)$, output $A[k]$, and $\textsc{update}(k, +\infty)$, where $+\infty$ is a new item larger than all others, whose comparisons need no work. The outputs are the items in increasing order, so the whole run is a comparison sort, which needs $\lg(n!)$ comparisons in the worst case by the decision-tree argument (CLRS, Section 8.1). $\square$

So any structure built with $P(n) = O(n)$ comparisons, such as a segment tree, has $t_u + t_q = \Omega(\log n)$ amortized, and the segment tree is optimal up to a constant. The bound is the [comparison sort lower bound](/comparison-sort-lower-bound/) in disguise, and the same argument gives the classic lower bound for [priority queues](/priority-queue/).

**Upper bound.** $O(\log n)$ worst case per operation, with $O(n)$ preprocessing and $2n$ words, by the segment tree.

**The static limit.** Without updates the queries take $O(1)$ time after $O(n)$ preprocessing on the word RAM, so the lower bound is about the cost of keeping the structure up to date, not about reading the answer.

## Reductions

- **Sorting to this problem.** The proof of the lower bound: $n$ queries of the whole range and $n$ updates sort $n$ items.
- **This problem to point update range "monoid" query.** Minimum is a monoid with identity $+\infty$, so any structure for an associative operation applies, in particular the segment tree.
- **Maximum to minimum.** Negate the items, or reverse the order.
- **Priority queue to this problem.** A priority queue over $n$ fixed keys with changes of priority is the special case with $l = 1$ and $r = n$.
- **Decrease-only prefix minima to a Fenwick tree.** With only decreases and prefix queries, the Fenwick tree with $\min$ in place of $+$ is correct, because the item that changes is the only one that can change a stored prefix minimum.

## Applications

- Dynamic programming whose transition takes the minimum of earlier values over a range, such as $D[i] = c_i + \min_{i - w \le j < i} D[j]$ with a variable window.
- Priority queues indexed by position, for example the set of tentative distances in [Dijkstra's algorithm](/dijkstra/) on dense graphs, kept in a segment tree over the vertices.
- Scheduling and simulation, to find the first free machine or the earliest event in a range of resources.
- Range maximum queries on changing data, such as the tallest building in a block of a street, or the highest price in a time window of a market.

## References
