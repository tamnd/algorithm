---
tag: 71PV3T
kind: problem
slug: range-assignment-query
name: Range assignment query
aliases:
- range assign range query
area: data-structures/range-query-structures
level: advanced
summary: Overwrite every element of a range with one value and answer queries over ranges.
prereqs: [range-query-problem, segment-tree, range-update-range-query]
see_also: [lazy-propagation, range-assignment-and-sum-query, chtholly-tree, square-root-decomposition, disjoint-set, balanced-binary-search-tree, segment-tree-maximum-subsegment-sum, dynamic-partial-sums-lower-bound]
sources:
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: section Range updates (Lazy Propagation), subsection Assignment on segments
  - url: https://cp-algorithms.com/data_structures/disjoint_set_union.html
    title: cp-algorithms, Disjoint Set Union
    locator: section Applications of DSU, subsection Painting subarrays offline
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: the lower bound for dynamic partial sums
---

The range assignment query problem keeps an array $A[0 \ldots n-1]$ under two operations: set every item of a range $[l, r]$ to one value $c$, and return an aggregate, such as the sum or the minimum, of a range. It is the [range update range query](/range-update-range-query/) problem with the update "overwrite" in place of "add". Two assignments compose by the rule that the later one wins, so a [segment tree](/segment-tree/) with [lazy propagation](/lazy-propagation/) solves it in $O(\log n)$ time per operation, and the [Chtholly tree](/chtholly-tree/), a sorted map of runs of equal items, is a simpler method when the operations are random.

## In plain words

Think of a long fence of boards, each with a color, or a row of seats, each with a price. One kind of order paints every board from board 3 to board 7 blue, or sets every seat of a block to one price. Another kind asks a question about a stretch, such as the total price of the seats in it or the cheapest seat.

Painting one board at a time is slow for long stretches. The fast methods write the new color once on a big piece of the fence, as a note, and pass the note down to the smaller pieces only when a later order needs them. A newer note on a piece replaces the older one, because the last paint is the one you see.

## Definition

**Input.** An array $A[0 \ldots n-1]$ over a set $S$ with a [monoid](/monoid/) operation $\oplus$. Then a sequence of operations, with $0 \le l \le r \le n - 1$:

- $\mathrm{assign}(l, r, c)$: set $A[i] \leftarrow c$ for each $l \le i \le r$;
- $\mathrm{query}(l, r)$: return $A[l] \oplus A[l+1] \oplus \cdots \oplus A[r]$.

**Output.** The answers of the queries, each for the array as it is after all earlier operations.

**The tag.** The map $f_c(v) = c$ is constant. For two assignments, $f_{c'} \circ f_c = f_{c'}$: the later one wins. On a range of length $k$, the aggregate after $f_c$ is $c^{\oplus k} = c \oplus \cdots \oplus c$ with $k$ factors, which does not depend on the old items. For $\oplus = +$ it is $kc$, and for $\min$ and $\max$ it is $c$. For a general monoid, $c^{\oplus k}$ costs $O(\log k)$ operations by repeated squaring, or $O(1)$ for idempotent operations.

## Variants

- **Assignment and sum.** The base case; see [range assignment and sum](/range-assignment-and-sum-query/).
- **Assignment and minimum or maximum.** The same tree, with the aggregate $c$ for an assigned node.
- **Assignment and add together.** A tag is a map $v \mapsto a v + b$ with $a \in \{0, 1\}$: $a = 0$ is an assignment to $b$, and $a = 1$ is an add of $b$. These maps are closed under composition, since $(a_2, b_2) \circ (a_1, b_1) = (a_2 a_1, a_2 b_1 + b_2)$.
- **Assignment and a complex query.** The query asks for the [maximum sum subsegment](/segment-tree-maximum-subsegment-sum/), or the number of runs of equal items. The record of an assigned node of length $k$ still follows from $c$ and $k$ alone.
- **Point queries only.** Only single items are read. A tree that keeps the tag with the latest time on each node of the range answers a point query with the latest tag on its root path.
- **Offline painting.** All assignments come first, and the final array is the only output. Process the assignments from the last to the first, and paint only the cells that have no color yet. A [disjoint-set union](/disjoint-set/) structure links each painted cell to the next cell to its right, so each cell is painted once, in $O((n + u)\,\alpha(n))$ time for $u$ assignments.
- **Counting colors.** The query asks for the number of distinct values of a range, which combines this problem with the [range distinct count](/range-distinct-count-query/).

## Examples

Let $A = [5, 2, 8, 1, 9, 3, 7, 4]$.

| step | operation | array after | answer |
|---|---|---|---|
| 1 | assign$(2, 5, 6)$ | 5 2 6 6 6 6 7 4 | |
| 2 | sum$(0, 7)$ | | 42 |
| 3 | min$(1, 4)$ | | 2 |
| 4 | assign$(0, 3, 1)$ | 1 1 1 1 6 6 7 4 | |
| 5 | sum$(2, 6)$ | | $1 + 1 + 6 + 6 + 7 = 21$ |
| 6 | max$(0, 4)$ | | 6 |

In a lazy segment tree on this array, step 1 puts the tag 6 on the nodes of $[2, 3]$ and $[4, 5]$, and sets their sums to $2 \cdot 6 = 12$. Step 4 covers the node of $[0, 3]$; its tag 1 replaces the older tag 6 of the child $[2, 3]$ when it is pushed down.

**Offline painting.** On 8 empty cells, the assignments $(1, 4, a)$, $(3, 6, b)$ and $(0, 2, c)$, in this order, give the final row $c\,c\,c\,b\,b\,b\,b\,.$, with cell 7 unpainted. In reverse order, $(0, 2, c)$ paints cells 0 to 2, $(3, 6, b)$ paints cells 3 to 6, and $(1, 4, a)$ finds no unpainted cell: the union-find structure jumps from cell 1 straight to cell 7, past its range.

## Known algorithms

| method | assign | query | space | notes |
|---|---|---|---|---|
| plain array | $O(r - l + 1)$ | $O(r - l + 1)$ | $n$ | |
| segment tree with [lazy propagation](/lazy-propagation/) | $O(\log n)$ | $O(\log n)$ | $O(n)$ | worst case; for a general monoid times $O(\log n)$ for $c^{\oplus k}$ |
| [square-root decomposition](/square-root-decomposition/) with a block tag | $O(\sqrt n)$ | $O(\sqrt n)$ | $O(n)$ | a full block gets the tag, a partial block is rebuilt |
| [Chtholly tree](/chtholly-tree/) (map of runs) | $O(\log n)$ amortized, plus the runs removed | $O((t + 1) \log n)$ for $t$ runs in the range | $O(\text{runs})$ | no worst-case bound for queries |
| offline painting with [union-find](/disjoint-set/) | $O((n + u)\,\alpha(n))$ in total | only the final array | $O(n)$ | |

**The map of runs.** Keep the array as a sorted map of maximal runs $[a, b]$ of equal items, in a [balanced search tree](/balanced-binary-search-tree/). An assignment splits at most two runs, at $l$ and at $r + 1$, then deletes all runs inside $[l, r]$ and inserts one run. Each assignment creates at most three runs, so at most $n + 3u$ runs are ever created, and each is deleted at most once. A query walks over the runs inside its range, and an adversary can keep many short runs alive, so a query can cost $\Theta(n)$. With random ranges, assignments merge runs fast and the walks stay short in practice.

## Bounds

**Lower bound.** The operation assign$(i, i, c)$ is a point update, and query$(0, p)$ with $\oplus = +$ is a prefix sum. So a structure for assignment and sum solves dynamic partial sums, and in the [cell-probe model](/cell-probe-model/) with words of $\Theta(\log n)$ bits it needs $\max(t_u, t_q) = \Omega(\log n)$ by the bound of Patrascu and Demaine; see the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/). The lazy segment tree reaches it.

**Upper bound.** $O(\log n)$ worst case per operation for sums, minimums, maximums and every record whose value on an assigned range follows from $c$ and the length in $O(1)$ time.

## Reductions

- **Point update to range assignment.** assign$(i, i, c)$ is the point update $A[i] \leftarrow c$, so every bound for point updates with range queries applies.
- **Range assignment to affine updates.** Assignment to $c$ is the affine map $v \mapsto 0 \cdot v + c$, so a structure for affine range updates with range sums also handles assignments.
- **Offline painting to union-find.** The reverse-order method turns $u$ assignments into $O(n + u)$ find and union operations.

## Applications

- Painting a fence or a strip of pixels, and asking for the total cost or the color count of a stretch.
- Timelines and calendars, where a booking sets the state of every slot of an interval.
- Memory or disk maps, where an allocation marks a block of addresses with an owner.
- Simulations with random range updates, where the [Chtholly tree](/chtholly-tree/) is short and fast.

## References
