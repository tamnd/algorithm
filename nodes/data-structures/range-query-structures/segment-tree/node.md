---
tag: P50MYS
kind: data-structure
slug: segment-tree
name: Segment tree
aliases:
- segment tree for range queries
area: data-structures/range-query-structures
level: core
summary: Binary tree over array segments answering range aggregates and point or range updates in O(log n).
implements: [range-query-structure]
prereqs: [range-query-problem, monoid, binary-tree, recursion]
see_also: [fenwick-tree, lazy-propagation, sparse-table, persistent-segment-tree, dynamic-segment-tree, segment-tree-beats, two-dimensional-segment-tree, merge-sort-tree]
sources:
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: sections Structure of the Segment Tree, Construction, Sum queries, Update queries, Implementation, Memory efficient implementation
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Section 9.3 (Segment tree) and Chapter 28 (Segment trees revisited)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 10, Section 10.3 (Segment Trees) and the Notes and Comments of Chapter 10
  - paper: "Jon L. Bentley, Solutions to Klee's rectangle problems, unpublished manuscript, Department of Computer Science, Carnegie-Mellon University, 1977"
    locator: the segment tree over the elementary intervals
---

A segment tree is a [binary tree](/binary-tree/) in which each node covers a contiguous range of an array and stores the aggregate of that range under an associative operation, so that the root covers the whole array and the two children of a node cover the two halves of its range. It implements the [range query structure](/range-query-structure/) for any [monoid](/monoid/): it builds in $O(n)$ time, and it answers a range query and performs a point update in $O(\log n)$ time each. With [lazy propagation](/lazy-propagation/) it also performs range updates in $O(\log n)$ time. It is the most general of the common structures for the [range query problem](/range-query-problem/), because it needs neither an inverse, as the [Fenwick tree](/fenwick-tree/) does, nor idempotence, as the [sparse table](/sparse-table/) does.

## In plain words

Write the numbers of a list as the leaves of a tree. Above each pair of leaves put a box with their combined value, for example their total. Above each pair of boxes put a box with the combined value of the two, and go on until one box at the top holds the total of the whole list.

To get the total of a stretch of the list, start at the top. If a box covers only items of the stretch, take its value. If it covers none of them, ignore it. Otherwise look at its two children. A stretch always splits into a few boxes, at most two on each row, so the answer needs only a few steps.

To change one item, change its leaf and then fix the boxes on the way from that leaf up to the top. There is one box on each row.

## The abstract type

A segment tree implements the [range query structure](/range-query-structure/) over a monoid $(S, \oplus, e)$: `build(A)`, `query(l, r)` for $A[l] \oplus \cdots \oplus A[r]$, and `set(i, x)`. The operation must be associative. It need not be commutative, because the tree combines the parts of a range in their left to right order. The identity $e$ is the answer for an empty part. With [lazy propagation](/lazy-propagation/) the tree also supports `apply(l, r, f)` for maps $f$ that act on aggregates, such as adding a constant to each item of a range.

## Representation

The array is $A[0 \ldots n-1]$ with $n \ge 1$. The tree is implicit and stored in an array $T$, as in a [binary heap](/binary-heap/). The node $1$ is the root and covers the range $[0, n-1]$. A node $v$ that covers $[lo, hi]$ with $lo < hi$ has

$$mid = \lfloor (lo + hi)/2 \rfloor, \qquad \mathrm{left}(v) = 2v \text{ covers } [lo, mid], \qquad \mathrm{right}(v) = 2v + 1 \text{ covers } [mid + 1, hi].$$

A node with $lo = hi$ is a leaf. The range of a node is not stored: each operation passes $lo$ and $hi$ down with $v$.

**Invariant (S).** For each node $v$ with range $[lo, hi]$: $T[v] = A[lo] \oplus A[lo + 1] \oplus \cdots \oplus A[hi]$.

Facts about the shape, for $n \ge 1$:

- The tree has exactly $n$ leaves, one for each index, and $n - 1$ inner nodes, since each inner node has two children. So it has $2n - 1$ nodes.
- A node of range length $m \ge 2$ has children of lengths $\lceil m/2 \rceil$ and $\lfloor m/2 \rfloor$. So a node at depth $d$ covers at most $\lceil n / 2^d \rceil$ indices, and the height is $\lceil \lg n \rceil$.
- A node at depth $d$ has an index less than $2^{d+1}$. Since $2^{\lceil \lg n \rceil} < 2n$, every index is less than $4n$, and an array $T$ of $4n$ cells is enough. When $n$ is not a power of two, some cells stay unused.
- The ranges of the nodes at one depth are pairwise disjoint.

## Operations

```pseudo id=main
BUILD(v, lo, hi)                              ▷ make T[v] for A[lo .. hi]; call BUILD(1, 0, n − 1)
L1  if lo = hi then T[v] ← A[lo]; return
L2  mid ← ⌊(lo + hi) / 2⌋
L3  BUILD(2v, lo, mid)
L4  BUILD(2v + 1, mid + 1, hi)
L5  T[v] ← T[2v] ⊕ T[2v + 1]

QUERY(v, lo, hi, l, r)                        ▷ ⊕ of A over [lo, hi] ∩ [l, r]; call QUERY(1, 0, n − 1, l, r)
L6  if r < lo or hi < l then return e
L7  if l ≤ lo and hi ≤ r then return T[v]
L8  mid ← ⌊(lo + hi) / 2⌋
L9  return QUERY(2v, lo, mid, l, r) ⊕ QUERY(2v + 1, mid + 1, hi, l, r)

UPDATE(v, lo, hi, i, x)                       ▷ A[i] ← x; call UPDATE(1, 0, n − 1, i, x)
L10 if lo = hi then T[v] ← x; return
L11 mid ← ⌊(lo + hi) / 2⌋
L12 if i ≤ mid then UPDATE(2v, lo, mid, i, x)
L13 else UPDATE(2v + 1, mid + 1, hi, i, x)
L14 T[v] ← T[2v] ⊕ T[2v + 1]
```

**Build** (lines L1 to L5) fills the tree from the leaves up, in post order. A leaf copies its item. An inner node combines its two children after both are built. Each of the $2n - 1$ nodes is visited once, with at most one $\oplus$, so build costs $\Theta(n)$ time and $n - 1$ applications of $\oplus$.

**Query** (lines L6 to L9) returns the aggregate of the part of $[l, r]$ inside the range of $v$. A node outside the query gives $e$ (line L6). A node inside the query gives its stored value (line L7). A node that is partly inside splits the work between its children, and line L9 combines the two answers in left to right order. The cost is $O(\log n)$, see the complexity section.

**Update** (lines L10 to L14) walks from the root to the leaf of $i$, sets the leaf, and recomputes each node on the way back up. Only the nodes on this path have $i$ in their range, so only they change. The path has at most $\lceil \lg n \rceil + 1$ nodes, so update costs $O(\log n)$ time and at most $\lceil \lg n \rceil$ applications of $\oplus$.

## Example

Let $A = [5, 2, 8, 1, 9, 3, 7, 4]$ and $\oplus = +$, $e = 0$. BUILD gives these nodes, one row per depth:

| depth | nodes, as index: range = value |
|---|---|
| 0 | 1: [0, 7] = 39 |
| 1 | 2: [0, 3] = 16, 3: [4, 7] = 23 |
| 2 | 4: [0, 1] = 7, 5: [2, 3] = 9, 6: [4, 5] = 12, 7: [6, 7] = 11 |
| 3 | leaves 8 to 15: 5, 2, 8, 1, 9, 3, 7, 4 |

Then run three operations.

| step | operation | nodes used | result or change |
|---|---|---|---|
| 1 | QUERY$(2, 6)$ | node 5 = 9, node 6 = 12 and leaf 14 = 7 by line L7; node 4 and leaf 15 give 0 by line L6 | $9 + 12 + 7 = 28$ |
| 2 | UPDATE$(3, 6)$ | the path 1, 2, 5, 11 | leaf 11 = 6, node 5 = 14, node 2 = 21, node 1 = 44 |
| 3 | QUERY$(1, 4)$ | leaf 9 = 2, node 5 = 14, leaf 12 = 9 | $2 + 14 + 9 = 25$ |

In step 1, the root splits into nodes 2 and 3. Node 2 covers $[0, 3]$ and is partly inside, so it splits into node 4, which is outside, and node 5, which is inside. Node 3 splits into node 6, which is inside, and node 7, which splits into leaf 14, inside, and leaf 15, outside. So the query visits 9 nodes and adds 3 stored values.

## Correctness

The invariant (S) holds after BUILD, and each UPDATE keeps it, because it recomputes exactly the nodes whose range holds $i$, from the bottom up. Given (S), QUERY$(v, lo, hi, l, r)$ returns the aggregate of $A$ over $[lo, hi] \cap [l, r]$, by induction on $hi - lo$: the intersection is empty in line L6, the whole range in line L7, and otherwise the union of the intersections with the two child ranges, which are adjacent with the left one first. Associativity lets line L9 combine the two parts, and the identity covers an empty part. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Query.** Call a visited node *partial* when its range meets $[l, r]$ but is not inside it. Only a partial node calls its children. A partial node with range $[lo, hi]$ has $lo < l \le hi$ or $lo \le r < hi$, so its range holds the index $l$ together with $l - 1$, or the index $r$ together with $r + 1$. The ranges at one depth are disjoint, so at each depth at most one node holds $l$ and at most one holds $r$. So each depth has at most 2 partial nodes, and at most 4 visited nodes, since each visited node other than the root is a child of a partial node. With height $\lceil \lg n \rceil$, a query visits at most $4 \lceil \lg n \rceil + 1$ nodes and applies $\oplus$ fewer times than that. So it costs $O(\log n)$ in the worst case. The bound is tight up to a constant: for $n = 1024$ the query $(1, 1022)$ has two partial nodes on each depth from 1 to 9 and visits 39 nodes, against the bound 41.

**Update and build.** These follow from the walk-through above: one root to leaf path for an update, and each node once for build.

| operation | time | applications of $\oplus$ |
|---|---|---|
| build | $\Theta(n)$ | $n - 1$ |
| query $(l, r)$ | $O(\log n)$ worst case | at most $4 \lceil \lg n \rceil$ |
| update (set $A[i]$) | $\Theta(\log n)$ worst case | at most $\lceil \lg n \rceil$ |
| range update with lazy propagation | $O(\log n)$ worst case | $O(\log n)$ |
| space | $2n - 1$ nodes in an array of $4n$ cells | |

The times count one $\oplus$ as $O(1)$. For an operation such as the [greatest common divisor](/range-gcd-query/), multiply by its cost. In the [cell-probe model](/cell-probe-model/), the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/) shows that $\Omega(\log n)$ per operation is necessary for sums, so the segment tree is optimal up to a constant factor.

## Variants

- **Bottom-up (iterative) segment tree.** Store the leaves at $T[n \ldots 2n-1]$ and node $v$ at $T[v]$ with $T[v] = T[2v] \oplus T[2v+1]$, for $v = n - 1$ down to $1$. A query walks up from both ends of the range. This uses $2n$ cells and no recursion. When $n$ is not a power of two, some nodes cover two pieces that are not adjacent, so a query must keep a left result and a right result apart to stay correct for an operation that is not commutative.
- **Range updates.** [Lazy propagation](/lazy-propagation/) stores a pending map at each node and pushes it to the children only when they are visited. See [range update range query](/range-update-range-query/) and [range assignment](/range-assignment-query/).
- **Descent.** To find the first index $j \ge l$ where the aggregate of $A[l \ldots j]$ reaches a bound (for example the $k$-th one in a 0/1 array), walk down the tree and choose a child by its stored value. This takes $O(\log n)$ time, not $O(\log^2 n)$ as a [binary search](/binary-search/) over queries would.
- **Rich node values.** A node may store a tuple. The [maximum subsegment sum](/segment-tree-maximum-subsegment-sum/) stores four numbers, and a [merge sort tree](/merge-sort-tree/) stores the sorted list of its range.
- **[Persistent segment tree](/persistent-segment-tree/).** An update copies the $O(\log n)$ nodes of its path, so every old version stays available. This answers the [range k-th smallest query](/range-kth-smallest-query/).
- **[Dynamic segment tree](/dynamic-segment-tree/).** Create nodes only when an update reaches them, for a huge index range with few updates.
- **[Segment tree beats](/segment-tree-beats/).** Range "set each item to the minimum of itself and $x$" with amortized $O(\log n)$ cost.
- **[Two-dimensional segment tree](/two-dimensional-segment-tree/).** A segment tree over rows whose nodes are segment trees over columns.
- **The segment tree of computational geometry.** Bentley's segment tree stores a set of intervals at the nodes over the elementary intervals of their endpoints, for stabbing queries: report the intervals that hold a point. It has the same shape but a different use, see the [interval tree](/interval-tree/) for the related structure.

## When to use it

Use a segment tree when the operation has no inverse (min, max, gcd, the product of matrices) and the array changes, or when you need range updates. For sums with point updates, a [Fenwick tree](/fenwick-tree/) is shorter and has a smaller constant. For a static array and an idempotent operation, a [sparse table](/sparse-table/) answers in $O(1)$. For a static array and a sum, [prefix sums](/prefix-sums/) are enough. For queries that do not split into two parts, such as the [range mode](/range-mode-query/), use [square-root decomposition](/square-root-decomposition/) or [Mo's algorithm](/mo-algorithm/).

## Pitfalls

- **An array of $2n$ cells for the recursive layout.** With node $v$ and children $2v$ and $2v + 1$, the indices reach almost $4n$ when $n$ is just above a power of two. For $n = 10$ the tree uses node 25, more than $2n = 20$, and for $n = 2080$ it uses node 8065, close to $4n = 8320$. Allocate $4n$ cells, or use the bottom-up layout.
- **The wrong identity.** Line L6 must return the identity of $\oplus$: $0$ for a sum, $+\infty$ for a minimum, $0$ for a gcd, the identity matrix for a product. Returning $0$ for a minimum gives wrong answers for ranges of positive numbers.
- **Swapped arguments.** For an operation that is not commutative, line L9 and lines L5 and L14 must put the left child first.
- **The midpoint of a half-open range.** With half-open ranges $[lo, hi)$, the leaf test is $hi - lo = 1$ and the children are $[lo, mid)$ and $[mid, hi)$. Mixing this with the closed form of lines L2 and L11 gives an infinite recursion on a range of length 2.
- **A forgotten recomputation.** An update that sets the leaf but skips line L14 leaves stale values in the ancestors.

## Implementations

The Python class follows the main block, with the closed ranges and the node numbering of the page. It takes the operation and its identity as arguments, so the same class gives sums, minimums and gcds. The recursion depth is $\lceil \lg n \rceil + 1$.

## History

Bentley described the segment tree in 1977, in an unpublished manuscript on Klee's rectangle problems, as a tree over the elementary intervals of a set of segments; de Berg and coauthors give this origin in the notes of their Chapter 10. The form used for range aggregates over an array, with one node per range of a recursive halving and the value of a monoid at each node, is the standard form of competitive programming texts such as the Handbook of Laaksonen and cp-algorithms.

## References
