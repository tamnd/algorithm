---
tag: 2MY7Y5
kind: data-structure
slug: priority-search-tree
name: Priority search tree
aliases:
- McCreight priority search tree
- PST
area: geometry/range-searching
level: core
summary: Tree that is both a heap and a search tree on the points, answering three-sided range queries in O(log n + k) time.
implements: [range-query-structure]
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of reported points}
  time: {build: O(n log n) worst case, three_sided: O(log n + k) worst case, lowest_in_x_range: O(log n) worst case, update: O(log n) worst case}
  space: {total: O(n) worst case}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1985
  people: [Edward M. McCreight]
  note: McCreight introduced the priority search tree, with three-sided queries in O(log n + k) time, linear space and logarithmic updates.
prereqs: [three-sided-range-query, binary-heap, binary-search-tree]
see_also: [priority-search-tree-query, three-sided-range-query, cartesian-tree, treap, range-tree, interval-tree, priority-r-tree, range-minimum-query]
sources:
  - paper: doi:10.1137/0214021
    title: Edward M. McCreight, Priority search trees, SIAM Journal on Computing 14(2), 1985, pages 257 to 276
    locator: the structure, the three-sided query, and insertion and deletion in O(log n) time on a balanced tree (DOI to be checked)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 10, Section 10.2, Priority Search Trees (a heap on x with a search on y, for queries unbounded to the left); notes in Section 10.5
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2, the priority search tree and three-sided queries
---

A priority search tree stores a set $P$ of $n$ points in the plane in a balanced binary tree that is a search tree on $x$ and a heap on $y$ at the same time. Each node covers a block of the points in $x$-order and stores the lowest point of that block not already stored higher up. It answers the [three-sided range query](/three-sided-range-query/) $[x_1, x_2] \times (-\infty, y_0]$ in $O(\log n + k)$ time with $O(n)$ space, in the worst case, which a [range tree](/range-tree/) can only match with $O(n \log n)$ space. McCreight's dynamic version supports insertions and deletions in $O(\log n)$ worst case time.

## In plain words

A search tree on the left-to-right position can find the points between two vertical lines quickly, but it does not know their heights. A heap on the height can find the lowest points quickly, but it does not know their positions. The priority search tree is both at once.

Each branch of the tree covers a stretch of positions, as in a search tree, and holds the lowest point of its stretch that no higher branch holds, as in a heap. To find the points between two vertical lines and below a height, walk down from the top. A branch whose point is already too high can be skipped with everything under it, because everything under it is higher still.

## The abstract type

The priority search tree is a [range query structure](/range-query-structure/) for points in the plane. It is built from a multiset $P$ of $n$ points and answers:

- **THREE-SIDED$(x_1, x_2, y_0)$**: all points $p \in P$ with $x_1 \le p_x \le x_2$ and $p_y \le y_0$, each copy once;
- **LOWEST$(x_1, x_2)$**: a point with the smallest $p_y$ among those with $x_1 \le p_x \le x_2$, or none;
- in McCreight's dynamic version, **INSERT$(p)$** and **DELETE$(p)$**.

**Notation.** $n = |P|$, $p = (p_x, p_y)$ a point, $k$ the number of reported points, $H = \lceil \log_2 n \rceil$ the height. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used. The model is the [real RAM](/real-ram/), and only coordinates are compared.

**Degenerate input.** No general position is assumed. The points are ordered by $(p_x, p_y, \text{index})$, and position $j$ is the $j$-th point of that order. The heap order uses the key $(p_y, p_x, j)$, which is distinct for every point even when points coincide. The query ranges are closed.

## Representation

- **Shape.** A balanced binary tree over the positions $0, \dots, n - 1$: the root covers the block $[0, n)$, and a node covering $[lo, hi)$ with $hi - lo \ge 2$ has children covering $[lo, mid)$ and $[mid, hi)$, $mid = \lfloor (lo + hi)/2 \rfloor$. The code numbers the nodes as in a heap (root 1, children $2v$ and $2v + 1$).
- **Stored points.** Each node $v$ stores at most one point, $\mathrm{pt}(v)$: among the positions of its block that are not stored at a proper ancestor of $v$, the one with the smallest key. If there is none, $v$ is empty, and so is its whole subtree.

The search on $x$ uses the blocks, so no split values are stored. In McCreight's paper and in de Berg et al. the split value of a node is the median $x$ of the points left after removing $\mathrm{pt}(v)$; the blocks here split all points of the subtree in the middle instead, which keeps the shape a fixed function of $n$. de Berg et al. swap the roles of the coordinates, with a heap on $x$ for queries $(-\infty, q_x] \times [q_y, q_y']$.

**Invariant.** (1) Every point is stored at exactly one node, and that node's block contains the point's position. (2) Along every path from the root, the keys of the stored points increase (heap order). (3) If a node is empty, both its children are empty.

From (1) and (2), $\mathrm{pt}(v)$ has the smallest key of all points stored in the subtree of $v$, and the points stored in that subtree are exactly the positions of the block of $v$ not stored above $v$.

## Operations

```pseudo id=main
BUILD(P)
L1  sort P by (p_x, p_y, index); position j holds the j-th point
L2  start at the root with its block [0, n) and the set R of all positions
L3  if R is empty then the node is empty; return
L4  pt(v) ← the position j ∈ R with the smallest key (p_y, p_x, j)
L5  if hi − lo ≥ 2 then build lc(v) with R ∩ [lo, mid) minus j, and rc(v) with R ∩ [mid, hi) minus j
```

```pseudo id=query
THREE-SIDED(x1, x2, y0)
L6  lo ← first position with p_x ≥ x1; hi ← last position with p_x ≤ x2
L7  for each node v reached from the root, depth first do
L8      if v is empty or its block is disjoint from [lo, hi] then skip v
L9      if pt(v)_y > y0 then skip v and its subtree
L10     if lo ≤ pt(v) ≤ hi then report pt(v)
L11     go on to lc(v) and rc(v)
```

LOWEST$(x_1, x_2)$ walks the same way without line L9: it keeps the best stored point with position in $[lo, hi]$, and does not descend below a node whose block lies inside $[lo, hi]$, since the stored point of such a node is the lowest of its subtree. The query is analysed in detail in [priority search tree query](/priority-search-tree-query/).

## Example

The points $(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)$ sorted by $x$ are $(2,3), (3,8), (4,7), (5,4), (6,6), (7,2), (8,1), (9,6)$ at positions $0$ to $7$. BUILD stores:

| node | block | candidates | stored point |
|---|---|---|---|
| 1 | $[0, 8)$ | all | $(8,1)$ |
| 2 | $[0, 4)$ | $(2,3), (3,8), (4,7), (5,4)$ | $(2,3)$ |
| 3 | $[4, 8)$ | $(6,6), (7,2), (9,6)$ | $(7,2)$ |
| 4 | $[0, 2)$ | $(3,8)$ | $(3,8)$ |
| 5 | $[2, 4)$ | $(4,7), (5,4)$ | $(5,4)$ |
| 6 | $[4, 6)$ | $(6,6)$ | $(6,6)$ |
| 7 | $[6, 8)$ | $(9,6)$ | $(9,6)$ |
| 10 | $[2, 3)$ | $(4,7)$ | $(4,7)$ |

All other nodes are empty. THREE-SIDED$(3, 7, 6)$ has $lo = 1$ and $hi = 5$. Node 1 holds $(8,1)$, low enough but outside $[1, 5]$, so it is not reported; node 2 holds $(2,3)$, likewise. Node 4 holds $(3,8)$ with $8 > 6$, so its subtree is skipped. Node 5 reports $(5,4)$; its child 10 holds $(4,7)$, too high. Node 3 reports $(7,2)$, node 6 reports $(6,6)$, and node 7 is skipped because its block $[6, 8)$ is outside $[1, 5]$. The answer is $(5,4), (7,2), (6,6)$, so $k = 3$. LOWEST$(3, 7)$ is $(7,2)$.

## Correctness

**Key invariant.** The heap order (2) means that every point in the subtree of $v$ has key at least that of $\mathrm{pt}(v)$, so line L9 skips only points with $p_y > y_0$. Line L8 skips only subtrees whose points all have positions outside $[lo, hi]$, by invariant (1). Every other stored point is tested at line L10, and position $j$ is in $[lo, hi]$ exactly when $x_1 \le p_x \le x_2$. So THREE-SIDED reports exactly the points of the range, each once. The full proof, with the bound on visited nodes, is in [the correctness proof](proofs/correctness/).

## Complexity

| operation or measure | cost | case |
|---|---|---|
| space | at most $2n - 1$ tree nodes and $n$ stored points, $O(n)$ | worst case |
| BUILD | $O(n \log n)$: a sort, and $O(n)$ work per level | worst case |
| THREE-SIDED | $O(\log n + k)$; at most $4H + 2k + 5$ node visits | worst case |
| LOWEST | $O(\log n)$; at most $4H + 5$ node visits | worst case |
| INSERT, DELETE (McCreight, on a balanced tree with rotations) | $O(\log n)$ | worst case |

A node passes lines L8 and L9 only if its block straddles $lo$ or $hi$, at most two per level, or its point is reported. Each node that passes adds at most two children to visit, so the visits are $O(H + k)$. After sorting, the tree can also be built bottom-up in $O(n)$ time, like a heap.

## Variants

- **Cartesian tree with range minimum queries.** On the points sorted by $x$, a [range minimum query](/range-minimum-query/) structure over the $y$-values finds the lowest point of $[lo, hi]$ in $O(1)$; recursing on the two sides reports the answer in $O(\log n + k)$ time with the two binary searches, or $O(1 + k)$ in rank space. The [Cartesian tree](/cartesian-tree/) is the tree of these recursive minima.
- **Treap.** A [treap](/treap/) has the same heap and search order with random priorities; the priority search tree uses the $y$-coordinates as priorities and a balanced shape instead.
- **Dynamic.** McCreight keeps the tree balanced by rotations. Repairing the stored points after a rotation costs time proportional to the height of the rotated subtree, and a red-black tree needs $O(1)$ rotations per update, so insertion and deletion take $O(\log n)$ time in the worst case.
- **External memory.** Arge, Samoladas and Vitter's external priority search tree answers three-sided queries with $O(\log_B n + k/B)$ I/Os in $O(n/B)$ blocks. The [priority R-tree](/priority-r-tree/) uses the same idea for rectangles.
- **Interval stabbing.** An interval $[a, b]$ contains $q$ exactly when $a \le q$ and $-b \le -q$, so the intervals as points $(a, -b)$ and the query $(-\infty, q] \times (-\infty, -q]$ turn stabbing into a two-sided query; see [interval tree](/interval-tree/).

## When to use it

Use a priority search tree for three-sided or two-sided (dominance) reporting when linear space matters, and in particular when the set changes, since the [range tree](/range-tree/) and the Cartesian tree approach are hard to update. For four-sided queries, a [range tree](/range-tree/) on $y$ whose nodes hold two priority search trees, one open upward and one open downward, answers a box query as two three-sided queries at the split node, in $O(\log n + k)$ time with $O(n \log n)$ space; with linear space, use a [kd-tree](/kd-tree-range-search/).

## Pitfalls

- **Pruning on the $x$-range at a node whose point is outside it.** The point of node 1 in the example is outside $[x_1, x_2]$, yet the points below it can still be in the range. Line L10 only skips reporting that point; it does not stop the descent.
- **Splitting by the stored point's coordinate.** The search order must be on the blocks of the subtree, not on the $x$ of the stored point, which is just the lowest point of the block and can lie anywhere in it.
- **Ties in $y$.** With equal $y$-values and no tie-break, the heap order is not strict, and LOWEST may return a point that is not the agreed minimum. Use the key $(p_y, p_x, j)$.
- **Using it for four-sided queries.** Adding a test for $p_y \ge y_1$ at line L10 gives correct output but no output-sensitive bound: many points with $p_y < y_1$ can be visited and not reported.

## Implementations

## History

Edward McCreight introduced the priority search tree in a 1980 Xerox PARC report and the 1985 SIAM Journal on Computing paper, with linear space, $O(\log n + k)$ three-sided queries and $O(\log n)$ updates on a balanced tree. Vuillemin's Cartesian tree (1980) has the same heap and search order on a static set. de Berg et al., Section 10.2, present the static version with a heap on $x$, and Arge, Samoladas and Vitter (1999) gave the external-memory version.

## References
