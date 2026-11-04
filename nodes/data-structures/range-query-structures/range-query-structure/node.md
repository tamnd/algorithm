---
tag: 011DTF
kind: abstract-type
slug: range-query-structure
name: Range query structure
aliases:
- range query data structure
area: data-structures/range-query-structures
level: intro
summary: Abstract interface for answering range aggregates, optionally with point or range updates.
prereqs: [range-query-problem, monoid]
see_also: [segment-tree, fenwick-tree, sparse-table, sqrt-tree, square-root-decomposition, lazy-propagation, dynamic-partial-sums-lower-bound, priority-queue]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9 (Range queries) and Chapter 28 (Segment trees revisited), Section 28.1 (Lazy propagation)
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 2.1, the lower bound for dynamic partial sums
  - paper: "Andrew C. Yao, Space-time tradeoff for answering range queries, Proceedings of the 14th Annual ACM Symposium on Theory of Computing (STOC 1982)"
    locator: the one-dimensional semigroup case
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: sections Structure of the Segment Tree, Range updates (Lazy Propagation)
---

A range query structure is an abstract data type that holds a sequence $A[0 \ldots n-1]$ over a [monoid](/monoid/) $(S, \oplus, e)$ and answers `query(l, r)`, the product $A[l] \oplus \cdots \oplus A[r]$, while it allows point or range updates of the sequence. It is the interface of the [range query problem](/range-query-problem/), separated from any one data structure. A [segment tree](/segment-tree/) implements all its operations in $O(\log n)$ time; a [Fenwick tree](/fenwick-tree/), a [sparse table](/sparse-table/) and a [square-root decomposition](/square-root-decomposition/) implement parts of it at other costs.

## In plain words

Think of a list of numbers in a box. You can ask the box one kind of question: give me the combined value of the items from this position to that position, where "combined" may mean the total, the smallest, or another fixed rule. You may also tell the box to change one item, or to change all items of a stretch in the same way, for example to add five to each of them.

The type says only what the answers must be. It does not say how the box finds them. A plain list can do it, but slowly. A tree of partial results answers each question and each change in a few steps. Some boxes allow no changes at all and pay for this with faster questions.

## Operations

Let $(S, \oplus, e)$ be a monoid: $\oplus$ is associative and $e \oplus x = x \oplus e = x$ for each $x \in S$. A value $R$ of the type is a sequence $A = (A[0], \ldots, A[n-1])$ of elements of $S$, with $n = |R|$ fixed after `build`. Let $F$ be a set of functions $S \to S$ (the *update maps*), for example $F = \{v \mapsto v + c\}$ for the sums of integers.

| operation | signature | what it does |
|---|---|---|
| `build` | $\text{build}(A) \to R$ | stores a copy of the sequence $A$ |
| `size` | $\text{size}(R) \to \mathbb{N}$ | returns $n$ |
| `query` | $\text{query}(R, l, r) \to S$ | for $0 \le l \le r+1 \le n$: returns $A[l] \oplus \cdots \oplus A[r]$, and $e$ when $l = r + 1$ |
| `get` | $\text{get}(R, i) \to S$ | returns $A[i]$, the same as $\text{query}(R, i, i)$ |
| `set` | $\text{set}(R, i, x) \to R$ | for $0 \le i < n$: $A[i]$ becomes $x$ |
| `apply` | $\text{apply}(R, l, r, f) \to R$ | for $f \in F$: $A[i]$ becomes $f(A[i])$ for each $l \le i \le r$ |

The empty range $l = r + 1$ returns the identity $e$, which lets code split a range at any point without a special case. A *static* structure has only `build`, `size`, `query` and `get`. A *dynamic* structure adds `set`, and a structure with *range updates* adds `apply`. Some structures need less than a monoid: a sparse table needs only an idempotent semigroup, and a structure without the empty range needs no identity.

### Example

Take integers with $\oplus = +$ and $e = 0$, and $F$ the maps $v \mapsto v + c$.

| step | operation | result | sequence after |
|---|---|---|---|
| 1 | build$([5, 2, 8, 1, 9, 3, 7, 4])$ | | 5 2 8 1 9 3 7 4 |
| 2 | query$(1, 4)$ | 20 | 5 2 8 1 9 3 7 4 |
| 3 | set$(3, 6)$ | | 5 2 8 6 9 3 7 4 |
| 4 | query$(1, 4)$ | 25 | 5 2 8 6 9 3 7 4 |
| 5 | apply$(0, 2, v \mapsto v + 10)$ | | 15 12 18 6 9 3 7 4 |
| 6 | query$(0, 3)$ | 51 | 15 12 18 6 9 3 7 4 |
| 7 | query$(4, 3)$ | 0 | 15 12 18 6 9 3 7 4 |

## Laws

For each sequence $A$ of length $n$, each structure $R$ and all indices in range:

$$\begin{aligned}
&(\text{R1})\quad \text{query}(\text{build}(A), l, r) = A[l] \oplus \cdots \oplus A[r],\\
&(\text{R2})\quad \text{query}(R, i, i) = \text{get}(R, i), \qquad \text{query}(R, l, l - 1) = e,\\
&(\text{R3})\quad \text{query}(R, l, r) = \text{query}(R, l, m) \oplus \text{query}(R, m + 1, r) \quad \text{for } l \le m + 1 \le r + 1,\\
&(\text{R4})\quad \text{get}(\text{set}(R, i, x), j) = \begin{cases} x & j = i \\ \text{get}(R, j) & j \ne i \end{cases}\\
&(\text{R5})\quad \text{get}(\text{apply}(R, l, r, f), j) = \begin{cases} f(\text{get}(R, j)) & l \le j \le r \\ \text{get}(R, j) & \text{otherwise} \end{cases}\\
&(\text{R6})\quad \text{size}(\text{set}(R, i, x)) = \text{size}(\text{apply}(R, l, r, f)) = \text{size}(R).
\end{aligned}$$

Laws (R2) to (R6) fix all answers. *Proof.* Apply (R3) $r - l$ times to split $\text{query}(R, l, r)$ into $\text{query}(R, l, l) \oplus \cdots \oplus \text{query}(R, r, r)$, and use (R2) to make each term a `get`. Laws (R4) and (R5) give the value of each `get` after any sequence of updates, by induction on the number of updates, starting from (R1) with $l = r$. So two implementations that meet the laws return the same answer to each query of each sequence of operations. $\square$

Law (R3) is where associativity is used. It holds for every split point, so an implementation may cut the range wherever its own stored parts end. Law (R3) does not ask for commutativity: the parts are combined in their left to right order.

A structure with `apply` needs more of the maps than (R5) states. To keep stored aggregates of ranges correct without visiting each item, the maps must act on aggregates: there must be a way to compute $f(x_1) \oplus \cdots \oplus f(x_k)$ from $x_1 \oplus \cdots \oplus x_k$ and $k$. For $\oplus = +$ and $f(v) = v + c$ the new sum is the old sum plus $kc$. For $\oplus = \min$ and $f(v) = v + c$ the new minimum is the old minimum plus $c$. This is the condition of [lazy propagation](/lazy-propagation/).

## Implementations

| implementation | needs | build | query | set | apply | space |
|---|---|---|---|---|---|---|
| plain [array](/array/) | monoid | $O(n)$ | $O(n)$ | $O(1)$ | $O(n)$ | $n$ |
| [prefix sums](/prefix-sums/) | group | $O(n)$ | $O(1)$ | $O(n)$ | $O(n)$ | $n + 1$ |
| [Fenwick tree](/fenwick-tree/) | group | $O(n)$ | $O(\log n)$ | $O(\log n)$ | add: two trees, $O(\log n)$ | $n$ |
| [square-root decomposition](/square-root-decomposition/) | monoid | $O(n)$ | $O(\sqrt n)$ | $O(\sqrt n)$ | $O(\sqrt n)$ with block tags | $n + O(\sqrt n)$ |
| [segment tree](/segment-tree/) | monoid | $O(n)$ | $O(\log n)$ | $O(\log n)$ | none | $2n$ to $4n$ |
| segment tree with [lazy propagation](/lazy-propagation/) | monoid, maps that act on aggregates | $O(n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $4n$ plus tags |
| [sparse table](/sparse-table/) | idempotent semigroup | $O(n \log n)$ | $O(1)$ | none | none | at most $n(\lfloor \lg n \rfloor + 1)$ |
| [disjoint sparse table](/disjoint-sparse-table/) | semigroup | $O(n \log n)$ | $O(1)$ | none | none | $O(n \log n)$ |
| [sqrt tree](/sqrt-tree/) | semigroup | $O(n \log \log n)$ | $O(1)$ | $O(\sqrt n)$ | none | $O(n \log \log n)$ |
| [Fischer-Heun RMQ](/fischer-heun-rmq/) | min or max, returns an index | $O(n)$ | $O(1)$ | none | none | $2n + o(n)$ bits |

All costs are worst case, with one $\oplus$ as one step. The Fenwick tree needs the inverse to turn two prefix values into a range value. The square-root decomposition with a set rebuilds one block. A range add on the Fenwick tree for range sums uses two trees, see [range update range query](/range-update-range-query/).

## Lower bounds

**Dynamic sums, cell-probe model.** For integers modulo $2^w$ with $\oplus = +$ and $w = \Theta(\log n)$, Patrascu and Demaine proved that each structure with `set` (or add) and `query` has $\max(t_u, t_q) = \Omega(\log n)$ in the [cell-probe model](/cell-probe-model/), amortized and with randomization; see the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/). So the segment tree and the Fenwick tree are optimal for this type up to a constant factor.

**Dynamic minimum, comparison model.** Let $\oplus = \min$ over a total order with a top element $\top$, and suppose that `query` also returns an index where the minimum is reached. Then $n$ items can be sorted by one `build`, followed by $n$ rounds of a `query(0, n-1)` and a `set` of the found index to $\top$. In the [comparison model](/comparison-model/) the sort needs $\lceil \lg(n!) \rceil$ comparisons in the worst case, so

$$b(n) + n \bigl(q(n) + u(n)\bigr) \ge \lceil \lg(n!) \rceil = n \lg n - O(n),$$

where $b$, $q$ and $u$ are the comparison counts of `build`, `query` and `set`. A segment tree builds with $n - 1$ comparisons, so for such a structure $q(n) + u(n) = \Omega(\log n)$.

**Static semigroups.** When the structure may store only values of the form $A[i] \oplus \cdots \oplus A[j]$ and a query may only combine them, Yao studied how many $\oplus$ steps a query needs as a function of the number of stored values. With $O(n \log n)$ stored values one step is enough, as the disjoint sparse table shows.

## References
