---
tag: DTQ6PY
kind: problem
slug: range-assignment-and-sum-query
name: Range assignment and sum query
aliases:
- assign and sum over ranges
area: data-structures/range-query-structures
level: advanced
summary: Combined problem of assigning values to ranges while answering sums over ranges.
model: cell-probe-model
complexity:
  vars: {n: the length of the array}
  time: {amortized: Ω(log n)}
prereqs: [range-assignment-query, lazy-propagation, point-update-range-sum-query]
see_also: [segment-tree, chtholly-tree, fenwick-tree, square-root-decomposition, range-update-range-query, dynamic-partial-sums-lower-bound, segment-tree-beats, amortized-cost]
sources:
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: section Range updates (Lazy Propagation), subsections Assignment on segments (a vertex marked as covered by one value, and the push to the children) and Adding on segments, querying for maximum
  - url: https://cses.fi/problemset/task/1735
    title: CSES Problem Set, Range Updates and Sums (task 1735)
    locator: the statement (increase a range by x, set a range to x, sum of a range, n and q up to 2 * 10^5) and its example
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 2.1 (the lower bound for dynamic partial sums, which applies through point assignment)
---

The range assignment and sum query problem keeps an array of $n$ numbers under two operations: set every item of a range $[l, r]$ to one value $c$, and return the sum of the items of a range. It is the [range assignment query](/range-assignment-query/) with the sum as the aggregate, and the standard test case of [lazy propagation](/lazy-propagation/) with a tag that does not commute with addition. A [segment tree](/segment-tree/) whose nodes store a sum and an optional "assigned to $c$" tag solves it in $O(\log n)$ worst-case time per operation, since a node of length $k$ that is assigned $c$ has the sum $k c$. Because a point assignment is a point update, the $\Omega(\log n)$ cell-probe bound for [dynamic partial sums](/point-update-range-sum-query/) applies, so the lazy tree is optimal.

## In plain words

Think of a row of seats in a theatre, each with a price. One kind of order says "every seat from 10 to 40 now costs 25". The other kind asks "what do seats 5 to 60 cost together?".

Writing the new price on each seat is slow for long stretches. A faster way keeps notes on blocks of seats: "this whole block now costs 25 each". The total of a block is then its size times 25, with no need to look at the seats. When a later order touches only part of a block, the note is first copied to the two halves of the block. A new note on a block simply replaces the old one, because the last price set is the one that counts.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of numbers, then a sequence of operations, with $0 \le l \le r \le n - 1$:

- $\textsc{assign}(l, r, c)$: set $A[i] \leftarrow c$ for each $l \le i \le r$;
- $\textsc{sum}(l, r)$: return $A[l] + A[l+1] + \cdots + A[r]$.

**Output.** The answer of each sum, for the array as it is after all earlier operations; the operations are given one at a time (online).

**The algebra.** For lazy propagation, a node over a range of length $k$ stores its sum $s$ and a tag $\tau \in \{\bot\} \cup \mathbb{Z}$, where $\bot$ means "no pending assignment". The tag acts by $\tau(s) = k \tau$ if $\tau \ne \bot$ and $\tau(s) = s$ otherwise, and tags compose by $\tau_2 \circ \tau_1 = \tau_2$ if $\tau_2 \ne \bot$ and $\tau_1$ otherwise: the later one wins. The action needs the length $k$, which each node knows. The action is a monoid homomorphism on the pairs (sum, length) under addition: $\tau(s_1 + s_2) = \tau(s_1) + \tau(s_2)$ for the lengths $k_1 + k_2$. These are the conditions that make a lazy tree correct.

## Variants

- **Assignment, add and sum.** Both updates on one tree, as in CSES 1735. A tag is a pair $(a, b)$ with $a \in \{0, 1\}$ for the map $v \mapsto a v + b$: $(0, c)$ assigns $c$ and $(1, d)$ adds $d$. Composition is $(a_2, b_2) \circ (a_1, b_1) = (a_2 a_1, a_2 b_1 + b_2)$, and a node of length $k$ gets the sum $a s + k b$. So an add after an assignment becomes an assignment to $c + d$, and an assignment after an add erases the add.
- **Assignment and sum modulo $p$.** The same tree with all arithmetic modulo $p$; the sum $k c$ is reduced modulo $p$.
- **Sum of squares, or of powers.** A node assigned $c$ has the sum of squares $k c^2$; with adds as well, the node also keeps lower powers, since $(v + d)^2 = v^2 + 2 d v + d^2$.
- **Assignment with minimum or maximum as well.** An assigned node has the minimum and maximum $c$, so one tree can keep all three aggregates.
- **Static sum with one batch of assignments.** If all assignments come before all queries, paint in reverse order with union-find, as in the [range assignment query](/range-assignment-query/), then answer the sums with [prefix sums](/prefix-sums/) in $O(1)$ each.

## Examples

Let $A = [2, 3, 1, 1, 5, 3, 0, 4]$.

| step | operation | array after | answer |
|---|---|---|---|
| 1 | $\textsc{sum}(0, 7)$ | 2 3 1 1 5 3 0 4 | 19 |
| 2 | $\textsc{assign}(1, 5, 2)$ | 2 2 2 2 2 2 0 4 | |
| 3 | $\textsc{sum}(0, 7)$ | | 16 |
| 4 | $\textsc{assign}(3, 6, 7)$ | 2 2 2 7 7 7 7 4 | |
| 5 | $\textsc{sum}(2, 4)$ | | 16 |
| 6 | $\textsc{sum}(0, 7)$ | | 38 |

In a lazy segment tree on this array, step 2 splits $[1, 5]$ into the canonical nodes $[1, 1]$, $[2, 3]$ and $[4, 5]$. They get the tag 2 and the sums $2$, $2 \cdot 2 = 4$ and $4$, and their ancestors are recomputed: $[0, 1]$ has the sum $2 + 2 = 4$, $[0, 3]$ has $8$, $[4, 7]$ has $4 + 4 = 8$, and the root has $16$. The leaves $[2, 2]$ and $[3, 3]$ still hold the old values 1 and 1, but the tag on $[2, 3]$ makes them irrelevant.

Step 4 splits $[3, 6]$ into $[3, 3]$, $[4, 5]$ and $[6, 6]$. To reach the leaf $[3, 3]$ the walk passes $[2, 3]$, so it first pushes the tag 2 down: both leaves get the value 2 and the tag on $[2, 3]$ is cleared. Then $[3, 3]$ gets 7, $[4, 5]$ gets the tag 7 in place of 2 and the sum 14, and $[6, 6]$ gets 7. Recomputing gives $[2, 3] = 9$, $[0, 3] = 13$, $[4, 7] = 14 + 7 + 4 = 25$ and the root $38$.

With adds as well, the CSES example with $A = [2, 3, 1, 1, 5, 3]$ (positions from 1) gives $\textsc{sum}(3, 5) = 7$, then after adding 2 on $[2, 4]$ the sum $11$, then after setting $[2, 4]$ to 5 the sum $15$.

## Known algorithms

| method | assign | sum | space | notes |
|---|---|---|---|---|
| plain array | $O(r - l + 1)$ | $O(r - l + 1)$ | $n$ | |
| [square-root decomposition](/square-root-decomposition/) | $O(\sqrt n)$ | $O(\sqrt n)$ | $O(n)$ | each block keeps a sum and an assigned value |
| segment tree with lazy propagation | $O(\log n)$ | $O(\log n)$ | $4n$ | worst case; the standard method |
| runs in an ordered map plus a [Fenwick tree](/fenwick-tree/) | $O(\log n)$ amortized | $O(\log n)$ | $O(n)$ | each removed run is a range add of $-v$, see below |
| [Chtholly tree](/chtholly-tree/) alone | $O(\log n)$ amortized | $O(t + \log n)$ for $t$ runs | $O(n)$ | fast only when assignments keep few runs |

**Runs with a Fenwick tree.** Keep the runs of equal values in an [ordered set](/ordered-set/), as in the Chtholly tree, and a Fenwick tree for range add and range sum, which is two Fenwick trees over the differences. An assignment splits at $l$ and $r + 1$, and for each run $[s, e]$ of value $v$ inside $[l, r]$ adds $c - v$ on $[s, e]$, then replaces the runs by one. Each assignment creates at most three runs and each run is removed at most once, so $u$ assignments on an array with $R_0$ runs cost $O((R_0 + u) \log n)$ in total, which is $O(\log n)$ amortized per operation when $R_0 \le n$ is counted once. The sums are plain Fenwick range sums in $O(\log n)$ worst case. This uses the [amortized cost](/amortized-cost/) of the runs and works for any query that a Fenwick tree with range adds can answer.

## Bounds

**Lower bound.** $\textsc{assign}(i, i, c)$ is the point update $A[i] \leftarrow c$, and $\textsc{sum}(0, p)$ is a prefix sum. So any structure for this problem solves dynamic partial sums, and in the [cell-probe model](/cell-probe-model/) with cells of $\Theta(\log n)$ bits, Patrascu and Demaine (2006) proved a trade-off between the amortized update time $t_u$ and query time $t_q$ which gives, in particular, $\max(t_u, t_q) = \Omega(\log n)$. See the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/).

**Upper bound.** $O(\log n)$ worst case per operation, with $O(n)$ preprocessing and $O(n)$ words, by the lazy segment tree. So the problem has the same complexity as the point update version, up to a constant.

## Reductions

- **Point update range sum to this problem.** A point update is an assignment of length one, which gives the lower bound.
- **This problem to affine range updates.** Assignment to $c$ is the map $v \mapsto 0 \cdot v + c$. A lazy tree for affine updates $v \mapsto a v + b$ with sums, where a node of length $k$ gets $a s + k b$, also solves this problem.
- **This problem to range add and range sum, amortized.** The runs method above turns each assignment into one range add per removed run, so any structure for [range add and range sum](/range-update-range-query/) gives an amortized solution with one more factor for the ordered set.
- **Range assignment and minimum.** The same tree with the record $\min$; an assigned node has the minimum $c$, so the same tag works.

## Applications

- Prices or capacities set for whole blocks of seats, rooms or time slots, with totals over a stretch.
- Simulation of painting, where each paint has a cost per cell and the question is the total cost of a stretch.
- Memory and disk maps, where an allocation sets the owner of a block of addresses and the query counts the used cells in a region, with $c \in \{0, 1\}$.
- Competitive programming problems such as CSES 1735, where assignment and add are mixed on one array.

## References
