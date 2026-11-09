---
tag: T2GH1M
kind: algorithm
slug: partition-tree-query
name: Partition tree query
aliases:
- simplex range query on partition tree
- halfplane query on a partition tree
area: geometry/range-searching
level: research
summary: Descend the partition tree, reporting whole cells inside the query simplex and recursing into cells it crosses.
solves: [simplex-range-searching]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension (fixed), k: the number of reported points, r: the fan-out of the tree}
  time: {count: O(n^(1-1/d)) worst case, report: O(n^(1-1/d) + k) worst case}
  space: {extra: O(r log n) worst case}
properties: {online: true, deterministic: true, recursive: false, static: true}
history:
  year: 1982
  people: [Dan E. Willard, Jiří Matoušek, Timothy M. Chan]
  note: Willard's polygon retrieval descended a partition tree in this way; Matoušek's partition theorem (1992) bounded the cells crossed at each level, and Chan (2012) made the total O(n^(1-1/d)).
prereqs: [partition-tree, simplex-range-searching]
see_also: [partition-tree, partition-theorem, simplex-range-searching, halfspace-range-searching, kd-tree-range-search, range-tree-query, geometric-cutting, range-searching-lower-bound]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 16, Section 16.1, Partition Trees (the halfplane query on a partition tree and its O(n^(1/2+epsilon)) analysis)
  - paper: doi:10.1007/BF02293051
    title: Jiří Matoušek, Efficient partition trees, Discrete and Computational Geometry 8, 1992, pages 315 to 334
    locator: the query on a partition tree with simplicial partitions of crossing number O(r^(1-1/d)) (DOI to be checked)
  - paper: doi:10.1007/s00454-012-9410-z
    title: Timothy M. Chan, Optimal partition trees, Discrete and Computational Geometry 47(4), 2012, pages 661 to 690
    locator: the O(n^(1-1/d)) query bound for simplex range counting (DOI to be checked)
  - paper: doi:10.1137/0211012
    title: Dan E. Willard, Polygon retrieval, SIAM Journal on Computing 11(1), 1982, pages 149 to 165
    locator: the first query on a partition tree in the plane, in O(n^0.774) time (DOI to be checked)
---

The partition tree query answers a simplex range query on a [partition tree](/partition-tree/): count or report the points inside a closed triangle, halfplane or other intersection of $\ell$ closed halfplanes. It walks down from the root and decides each node by its cell: a cell outside one of the halfplanes is skipped, a cell inside all of them contributes its whole count (or its whole block of points), and only a cell crossed by a boundary line is opened, or scanned if it is a leaf. With the simplicial partitions of Matoušek's [partition theorem](/partition-theorem/), a line crosses $O(\sqrt{r})$ of the $r$ cells of a node in the plane and $O(r^{1 - 1/d})$ in $\mathbb{R}^d$, and the query takes $O(n^{1 - 1/d} \log^{O(1)} n)$ time with Matoušek's trees and $O(n^{1 - 1/d})$ with Chan's, plus $O(k)$ for reporting, all in the worst case.

## In plain words

The points are already sorted into groups, groups inside groups, and each group has a known outline. To count the points in a triangle, start with the biggest groups.

If a group's outline is completely outside the triangle, none of its points count. If it is completely inside, all of its points count, and the stored total is added at once. Only if an edge of the triangle passes through the outline do we look inside the group, at its smaller groups, or at its points when the group is small.

The tree was built so that a straight edge passes through only a few groups at each level. So the search opens few groups and skips or counts all the others in one step each.

## The problem

**Input.** A [partition tree](/partition-tree/) on a multiset $P$ of $n$ points in the plane, and a closed range $\Delta = \bigcap_{i=1}^{\ell} \{x : a_i x_1 + b_i x_2 \le c_i\}$ given by $\ell$ halfplanes; a triangle with vertices $p, q, t$ is the case $\ell = 3$, with each edge giving the halfplane on the side of the third vertex.

**Output.** The number $|P \cap \Delta|$, counting copies, and if asked, the points themselves.

**Notation.** $v$ a node, $S(v)$ its points, $C(v)$ its cell, a convex polygon with $S(v) \subseteq C(v)$; here $C(v)$ is the convex hull of $S(v)$, stored as a lower and an upper chain from left to right. For a cell and a halfplane $a x_1 + b x_2 \le c$, write $\mathrm{lo}$ and $\mathrm{hi}$ for the smallest and largest value of $a x_1 + b x_2$ over the cell. The model is the [real RAM](/real-ram/), with exact arithmetic in the implementation.

**Degenerate input.** Points may coincide or lie on the boundary of $\Delta$ or of a cell. The range is closed. A degenerate triangle, with collinear vertices, is rejected; pass its halfplanes directly if a segment is meant.

## The algorithm

```pseudo id=main
PARTITION-TREE-QUERY(T, Δ)
L1  count ← 0; out ← empty; push the root of T on a stack
L2  while the stack is not empty do pop a node v
L3      for each halfplane a·x ≤ c of Δ: lo ← −EXTREME(C(v), −a); hi ← EXTREME(C(v), a)
L4      if lo > c for some halfplane then continue (the cell is outside Δ)
L5      if hi ≤ c for all halfplanes then add |S(v)| to count and the block of v to out; continue
L6      if v is a leaf then add each point of S(v) that satisfies all halfplanes
L7      else push the children of v
L8  return count and out
```

```pseudo id=extreme
EXTREME(C, (a, b))
L9  if b = 0 then return the larger of a·x1 at the leftmost and at the rightmost vertex of C
L10 K ← the upper chain of C if b > 0, else the lower chain, both from left to right
L11 binary search for the first edge (K_j, K_{j+1}) with a(x_{j+1} − x_j) + b(y_{j+1} − y_j) ≤ 0
L12 return a x + b y at K_j, or at the last vertex of K if no such edge exists
```

Line L3 computes, for each halfplane, the range of values of its linear function over the cell. Line L4 discards a cell all of whose points violate one constraint strictly. Line L5 accepts a cell all of whose points satisfy every constraint. EXTREME uses the fact that, walking the upper chain from left to right, the edges turn clockwise, so the value $a x_1 + b x_2$ with $b > 0$ first increases and then does not; the maximum is where it stops increasing. With simplices as cells, as in Matoušek's tree, line L3 evaluates the $d + 1$ vertices instead, in $O(1)$ time.

## Example

The [partition tree](/partition-tree/) on $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$ with $r = 4$, leaf size $2$ and seed $0$ has a root and four leaves, $A = \{(2,3), (5,4)\}$, $B = \{(7,2), (8,1)\}$, $C = \{(6,6), (9,6)\}$ and $D = \{(3,8), (4,7)\}$. Query the closed triangle with vertices $(1,0)$, $(10,0)$, $(10,9)$. Its halfplanes are $-9y \le 0$, $9x \le 90$ and $-9x + 9y \le -9$, the last being $x - y \ge 1$.

| step | node | values of $-9x + 9y$ over the cell, lo and hi | other halfplanes | decision |
|---|---|---|---|---|
| 1 | root | $-63$ and $45$ | inside both | crossed, push $D, C, B, A$ |
| 2 | $A$ | $-9$ and $9$ | inside | crossed leaf: scan, count $(5,4)$ |
| 3 | $B$ | $-63$ and $-45$ | inside | inside: add $2$ |
| 4 | $C$ | $-27$ and $0$ | inside | crossed leaf: scan, count $(9,6)$ |
| 5 | $D$ | $27$ and $45$ | inside | outside: skip |

The answer is $4$, the points $(5,4)$, $(7,2)$, $(8,1)$, $(9,6)$. The point $(5,4)$ lies on the edge $x - y = 1$, and the closed test counts it; at step 2, $\mathrm{lo} = -9 = c$, so line L4 does not skip $A$. The query visits $5$ nodes and scans $4$ points. The closed triangle with vertices $(3,1)$, $(9,5)$, $(3,7)$ gives the answer $2$, the points $(5,4)$ and $(6,6)$, with $B$ and $D$ outside and $A$ and $C$ scanned.

## Correctness

**Key invariant.** Every node's points lie in its cell, and the children's point sets partition the parent's. If even the smallest value over the cell exceeds $c$, every point of the node violates that halfplane; if the largest value is at most $c$ for every halfplane, every point of the node lies in $\Delta$. Every other node is resolved by its children or by a direct scan, so by induction on the height the count of each node is $|S(v) \cap \Delta|$. EXTREME is exact by the monotone sign of the increments along a chain. The full proof, with the bound on the number of visited nodes, is in [the correctness proof](proofs/correctness/).

## Complexity

A node that is opened at line L7, or scanned at line L6, has a cell crossed by one of the $\ell$ boundary lines of $\Delta$. If every partition in the tree has crossing number at most $\kappa$, so that a line crosses at most $\kappa$ of the cells of any node's children, the number of visited nodes satisfies $V(m) \le 1 + r + \ell \kappa \, V(2 \lceil m/r \rceil - 1)$ for $r \ge 4$.

| tree | visited nodes and time | case |
|---|---|---|
| crossing number $\kappa$, constant $r \ge 4$ | $O(r (n/b)^{\log(\ell \kappa) / \log(r/2)})$ nodes, $O(\ell \log n)$ each here, $O(\ell)$ with triangle cells | worst case |
| Matoušek's partition tree, $\kappa = O(\sqrt{r})$, constant $r$ | $O(n^{1/2 + \varepsilon})$ for any fixed $\varepsilon > 0$ and $r$ large enough | worst case |
| Matoušek (1992), $r$ growing with $n$ | $O(n^{1 - 1/d} \log^{O(1)} n)$ | worst case |
| Chan (2012) | $O(n^{1 - 1/d})$ | worst case |
| reporting | the counting bound plus $O(k)$, since an inside node's block is copied | worst case |
| extra space | the stack holds at most $r$ nodes per level, $O(r \log_r n)$ | worst case |

On random points with $r = 16$ and leaf size $16$, a halfplane query whose boundary passes through two random points cost $191$ node visits and scanned points on average for $n = 1024$ and $2443$ for $n = 65536$. Matching Chazelle's lower bound, no structure with $O(n)$ space can do better than $\Omega(\sqrt{n})$ in the plane in the semigroup model; see [range searching lower bound](/range-searching-lower-bound/).

## Properties

- **Online and deterministic.** Each query is answered on its own, without randomness; the randomness is only in building the tree.
- **Iterative.** An explicit stack replaces recursion.
- **Semigroup friendly.** The answer is a sum of stored node counts and single points, with no subtraction, so the same walk sums weights from any commutative semigroup, for example a maximum.
- **Range shape.** Any intersection of $O(1)$ closed halfplanes works, not only triangles; convex polygons with $\ell$ edges cost a factor $\ell$.

## Variants and improvements

- **Halfplane queries.** With $\ell = 1$ at most $\kappa$ children are opened per node instead of $\ell \kappa$; de Berg et al. analyse this case first and then treat a triangle as three halfplanes.
- **Multi-level trees.** In a multi-level partition tree, line L5 does not add a count but queries a secondary structure stored at the node with the remaining halfplanes, which turns simplex queries into a chain of halfplane queries.
- **Reporting with shallow cuttings.** For halfplanes, reporting can stop early where the output is small; with [shallow cuttings](/shallow-cutting/) halfplane reporting takes $O(\log n + k)$ in the plane.
- **Optimal trees.** Chan's partition trees bound the total number of cells a line crosses at all levels together, which gives the clean $O(n^{1 - 1/d})$.
- **Cuttings at the top.** With extra space, the top levels are replaced by [cuttings](/geometric-cutting/), and the query switches to partition trees lower down, giving the space and query trade-off of [simplex range searching](/simplex-range-searching/).

## When to use it

Use it to count or report points in triangles, halfplanes and convex polygons with linear space, when the queries come one at a time. For axis-parallel boxes a [range tree query](/range-tree-query/) or a [kd-tree query](/kd-tree-range-search/) is simpler. For many queries given together, an offline method with [cuttings](/geometric-cutting/) or duality may be faster in total.

## Pitfalls

- **Closed ranges.** Testing $\mathrm{lo} \ge c$ instead of $\mathrm{lo} > c$ at line L4 drops cells that only touch the boundary, and loses points such as $(5,4)$ in the example.
- **Requiring a crossing for every constraint.** A node is outside if it fails one halfplane, and inside only if it passes all of them; mixing the two tests, for example accepting a node that is inside one halfplane and crossed by another, counts points outside the range.
- **Scanning hull vertices.** Testing a hull cell by evaluating all its vertices costs time linear in the cell at large nodes; use the binary search of EXTREME, or triangle cells.
- **Orientation of triangle edges.** The halfplane of an edge must be the side of the third vertex. Orient the triangle counterclockwise first, and reject a triangle with zero area.

## Implementations

## History

Willard (1982) introduced partition trees and answered polygon queries in the plane by this descent, in $O(n^{0.774})$ time. The same walk is used in all later partition trees: Haussler and Welzl (1987) built partition trees in every dimension with [epsilon-nets](/epsilon-net-theorem/), Matoušek (1992) proved the [partition theorem](/partition-theorem/) and the bound $O(n^{1 - 1/d} \log^{O(1)} n)$, and Chan (2012) reached $O(n^{1 - 1/d})$. de Berg et al. present the planar halfplane query in Chapter 16.

## References
