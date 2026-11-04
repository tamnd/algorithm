---
tag: 7TXX03
kind: problem
slug: range-update-range-query
name: Range update range query
aliases:
- range add range sum
- range update range sum query
area: data-structures/range-query-structures
level: core
summary: Add a value to a range and answer sums or minimums over ranges.
prereqs: [range-query-problem, segment-tree, difference-array]
see_also: [lazy-propagation, fenwick-tree, range-update-point-query, point-update-range-sum-query, range-assignment-query, segment-tree-beats, square-root-decomposition, dynamic-partial-sums-lower-bound]
sources:
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: section Range updates (Lazy Propagation), subsections Addition on segments and Adding on segments, querying for maximum
  - url: https://cp-algorithms.com/data_structures/fenwick.html
    title: cp-algorithms, Fenwick Tree
    locator: section Range Update and Range Query
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 28 (Segment trees revisited), Section 28.1 (Lazy propagation)
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 2.1, the lower bound for dynamic partial sums
---

The range update range query problem keeps an integer array $A[0 \ldots n-1]$ under two operations: add a value $c$ to each item of a range $[l, r]$, and return the sum, or the minimum, of a range. It is the dynamic [range query problem](/range-query-problem/) with updates on whole ranges instead of single items. A [segment tree](/segment-tree/) with [lazy propagation](/lazy-propagation/) does both operations in $O(\log n)$ time for sums and for minimums, and for sums two [Fenwick trees](/fenwick-tree/) do the same with less code. The $\Omega(\log n)$ cell-probe lower bound of the [dynamic partial sums](/dynamic-partial-sums-lower-bound/) problem applies, so these solutions are optimal up to a constant factor.

## In plain words

You keep a list of numbers, for example the number of booked seats on each leg of a train trip. A booking from station 3 to station 7 adds one seat to each leg of that stretch. A question asks for the total of the bookings on some stretch, or for the leg with the fewest free seats.

Changing each item of a long stretch one by one is slow, and so is adding up a long stretch one by one. The solutions keep partial results for big pieces of the list. A change to a whole piece is written once on the piece, as a note to pass down later, and not on each item of it.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of integers. Then a sequence of operations of two kinds, with $0 \le l \le r \le n - 1$:

- $\mathrm{add}(l, r, c)$: set $A[i] \leftarrow A[i] + c$ for each $l \le i \le r$;
- $\mathrm{sum}(l, r)$: return $\sum_{i=l}^{r} A[i]$, or in the minimum version $\mathrm{min}(l, r)$: return $\min_{l \le i \le r} A[i]$.

**Output.** The answers of the queries, each for the array as it is after all earlier operations.

**General form.** Let $(S, \oplus)$ be a monoid of values and $F$ a set of maps $S \to S$ that is closed under composition. An update applies $f \in F$ to each item of a range. A segment tree with lazy tags solves the problem in $O(\log n)$ time per operation, counting one $\oplus$, one application and one composition as one step, when the maps act on aggregates: there is a function $\mathrm{apply}$ with $f(x_1) \oplus \cdots \oplus f(x_k) = \mathrm{apply}(f, x_1 \oplus \cdots \oplus x_k, k)$ for all $x_1, \ldots, x_k$. For $\oplus = +$ and $f(v) = v + c$, the aggregate of a node of length $k$ becomes $s + kc$; for $\oplus = \min$ it becomes $m + c$.

## Variants

- **Range add, range sum.** The base case above.
- **Range add, range minimum or maximum.** A lazy segment tree; there is no Fenwick tree version, because $\min$ has no inverse.
- **[Range assignment](/range-assignment-query/).** The update sets each item to $c$. Assignments compose by "the later one wins"; see also [range assignment and sum](/range-assignment-and-sum-query/).
- **Affine updates.** The update is $v \mapsto a v + b$, often modulo a prime, with range sums. The maps compose as affine maps, and a node of length $k$ with sum $s$ gets the sum $a s + k b$.
- **Range add, point query.** Only single items are read; see [range update point query](/range-update-point-query/). A [difference array](/difference-array/) and one Fenwick tree are enough.
- **Range chmin.** The update is $v \mapsto \min(v, x)$ with range sums. This map does not act on a sum with a known formula, and the [segment tree beats](/segment-tree-beats/) handles it with an amortized bound.
- **Offline or static after the updates.** When all updates come before all queries, apply them to a difference array in $O(n + u)$ time and then use [prefix sums](/prefix-sums/).

## Examples

Let $A = [5, 2, 8, 1, 9, 3, 7, 4]$.

| step | operation | array after | answer |
|---|---|---|---|
| 1 | add$(2, 5, 3)$ | 5 2 11 4 12 6 7 4 | |
| 2 | sum$(1, 4)$ | | $2 + 11 + 4 + 12 = 29$ |
| 3 | min$(3, 7)$ | | 4 |
| 4 | add$(0, 7, -2)$ | 3 0 9 2 10 4 5 2 | |
| 5 | sum$(0, 7)$ | | 35 |
| 6 | min$(2, 5)$ | | 2 |

**Two Fenwick trees for sums.** Write $A = A_0 + \Delta$, where $A_0$ is the start array, whose prefix sums are fixed, and $\Delta$ is the sum of all adds. Keep the difference array $D$ of $\Delta$, so $\Delta[i] = \sum_{j \le i} D[j]$; an add$(l, r, c)$ changes only $D[l] \mathrel{+}= c$ and $D[r+1] \mathrel{-}= c$. Then

$$\sum_{i=0}^{p} \Delta[i] = \sum_{i=0}^{p} \sum_{j=0}^{i} D[j] = \sum_{j=0}^{p} (p - j + 1) D[j] = (p + 1) \sum_{j=0}^{p} D[j] - \sum_{j=0}^{p} j \, D[j].$$

So two Fenwick trees, one over $D[j]$ and one over $j \, D[j]$, give each prefix sum of $\Delta$ with two prefix queries. An add is two point updates in each tree, and $\mathrm{sum}(l, r)$ is the difference of two prefix sums. After step 1 above, $D$ has $D[2] = 3$ and $D[6] = -3$, so for $p = 4$ the formula gives $5 \cdot 3 - 2 \cdot 3 = 9$, the three adds of 3 to the items 2, 3 and 4.

## Known algorithms

| method | add$(l, r, c)$ | sum$(l, r)$ | min$(l, r)$ | space |
|---|---|---|---|---|
| plain array | $O(r - l + 1)$ | $O(r - l + 1)$ | $O(r - l + 1)$ | $n$ |
| segment tree with [lazy propagation](/lazy-propagation/) | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $4n$ values and $4n$ tags |
| two [Fenwick trees](/fenwick-tree/) | $O(\log n)$ | $O(\log n)$ | not supported | $2n$ |
| [square-root decomposition](/square-root-decomposition/) with block tags | $O(\sqrt n)$ | $O(\sqrt n)$ | $O(\sqrt n)$ | $n + O(\sqrt n)$ |

The times are worst case. In the lazy segment tree, an add stores its value as a tag on the $O(\log n)$ nodes that make up the range, and any later visit of such a node pushes the tag to its two children first.

## Bounds

**Lower bound.** The operation add$(i, i, c)$ is a point update and sum$(0, p)$ is a prefix sum, so each structure for this problem solves the dynamic partial sums problem. In the [cell-probe model](/cell-probe-model/) with words of $\Theta(\log n)$ bits, Patrascu and Demaine proved $\max(t_u, t_q) = \Omega(\log n)$ for it, amortized and with randomization. So the $O(\log n)$ bounds of the table are optimal up to a constant factor.

**Upper bound.** $O(\log n)$ worst case per operation, by the lazy segment tree, for every monoid and family of maps that meets the condition of the definition.

## Reductions

- **Range add with range sums to point updates with prefix sums.** By the formula above, with two structures for point update and prefix sum.
- **Range add with point query to point update with range sum.** A point query of $A[i]$ is a prefix sum of the difference array.
- **Union of rectangles to range add with a count of zeros.** In a sweep over the $x$ axis, each rectangle adds $+1$ to its range of $y$ cells on entry and $-1$ on exit. A lazy segment tree with "add" updates and a query for the minimum and the count of the minimum gives the length of the covered part at each step, and so the area of the union in $O(m \log m)$ time for $m$ rectangles.

## Applications

- Booking and capacity checks: add the demand of each booking over its interval of time, and check that the maximum stays within the capacity.
- The area and the perimeter of a union of rectangles, by the sweep above.
- Dynamic programs in which a step adds a constant to a range of states and then takes a minimum over a range.
- Queries on paths of trees after [heavy-light decomposition](/heavy-light-decomposition/), where a path update becomes $O(\log n)$ range updates.

## References
