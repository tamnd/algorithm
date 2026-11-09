---
tag: WF7BGF
kind: algorithm
slug: monotone-polygon-triangulation
name: Monotone polygon triangulation
aliases:
- Garey-Johnson-Preparata-Tarjan triangulation
- triangulation of monotone polygons
- monotone partition and triangulation
- stack triangulation of a monotone polygon
area: geometry/triangulations
level: core
summary: Triangulate a y-monotone polygon in linear time, giving an O(n log n) algorithm for general simple polygons.
solves: [polygon-triangulation]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1978
  people: [Michael R. Garey, David S. Johnson, Franco P. Preparata, Robert E. Tarjan]
  note: Garey, Johnson, Preparata and Tarjan triangulated a monotone polygon in linear time with a stack and combined it with the plane sweep of Lee and Preparata, which cuts a simple polygon into monotone pieces, to get the first O(n log n) polygon triangulation.
prereqs: [polygon-triangulation, monotone-polygon, monotone-polygon-partition, orientation-test, simple-polygon]
see_also: [ear-clipping, seidel-polygon-triangulation, chazelle-polygon-triangulation, tarjan-van-wyk-triangulation, polygon-with-holes-triangulation, trapezoidal-map, planar-subdivision, triangulation-dual-tree]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Sections 3.2 (MakeMonotone, the five vertex types, Lemmas 3.4 and 3.5) and 3.3 (TriangulateMonotonePolygon and the O(n log n) theorem)
  - paper: "Michael R. Garey, David S. Johnson, Franco P. Preparata and Robert E. Tarjan, Triangulating a simple polygon, Information Processing Letters 7(4), 175 to 179 (1978)"
    locator: the linear-time triangulation of a monotone polygon and the O(n log n) bound for simple polygons
  - paper: "Der-Tsai Lee and Franco P. Preparata, Location of a point in a planar subdivision and its applications, SIAM Journal on Computing 6(3), 594 to 606 (1977)"
    locator: the regularization sweep that cuts a planar subdivision into monotone pieces
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 2, Polygon Partitioning (monotone partitioning and the triangulation of monotone polygons)
  - paper: "Stefan Hertel and Kurt Mehlhorn, Fast triangulation of simple polygons, Foundations of Computation Theory (FCT 1983), Lecture Notes in Computer Science 158, 207 to 218 (1983)"
    locator: the sweep that stops only at reflex vertices, in O(n + r log r) time
---

Monotone polygon triangulation is the classic $O(n \log n)$ method for the [polygon triangulation](/polygon-triangulation/) problem. It has two phases. A plane sweep adds diagonals at the vertices where the boundary turns back, and this cuts the [simple polygon](/simple-polygon/) into [monotone polygons](/monotone-polygon/), each of which meets every horizontal line in one segment at most. Then each monotone piece is triangulated in linear time by one top-to-bottom pass with a stack. The sort of the vertices dominates, so the total is $\Theta(n \log n)$ time and $\Theta(n)$ space. The method was published by Garey, Johnson, Preparata and Tarjan in 1978 and is the version taught in most textbooks.

## In plain words

Some shapes are easy to cut into triangles. If you slide a horizontal ruler down over the shape and the ruler always cuts it in one piece, the shape is called monotone. You can then cut it with a single pass from the top to the bottom: keep a pile of corners you have seen but not yet used, and each time a new corner comes in, cut off every triangle it can see from the pile.

A general shape is not monotone. Its boundary can turn back, making a cave that opens upward or downward. So first slide the ruler over the whole shape, and at each corner where the boundary turns back, draw one cut to a nearby corner. These cuts split the shape into monotone parts. Then triangulate each part with the pile method.

Sorting the corners from top to bottom is the slowest step.

## The problem

The input is a simple polygon $P$ given by its vertex list $v_0, \ldots, v_{n-1}$ in clockwise or counterclockwise order, with distinct vertices. Consecutive collinear vertices are allowed, and many vertices may share a $y$ coordinate. The output is a list of $n - 2$ triangles with corners among the vertices, given by index triples in counterclockwise order, with disjoint interiors and union $P$.

Notation: $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$. The **sweep order** puts $p$ above $q$ if $p_y > q_y$, or $p_y = q_y$ and $p_x < q_x$. It is a total order, and it equals the height order after a tiny clockwise rotation, so all statements about "horizontal lines" refer to that rotated picture and no general position is assumed. A polygon is monotone if its boundary splits at the highest and the lowest vertex into a **left chain** (counterclockwise from the top) and a **right chain**, both of which descend strictly in the sweep order.

## The algorithm

**Phase 1: monotone partition.** Sweep the vertices from top to bottom. Classify each vertex $v$ by its neighbors: a **start** vertex has both neighbors below and an interior angle less than $\pi$, a **split** vertex has both neighbors below and an angle more than $\pi$, an **end** vertex has both above and an angle less than $\pi$, a **merge** vertex has both above and an angle more than $\pi$, and every other vertex is **regular**. The status holds the edges that cross the sweep line with the interior of $P$ to their right, each with a **helper**: the lowest vertex seen so far that sees the edge horizontally to its left.

- **Start** $v$: insert the edge leaving $v$, with helper $v$.
- **End** $v$: if the helper of the edge entering $v$ is a merge vertex, add a diagonal from $v$ to it; delete that edge.
- **Split** $v$: find the status edge $e$ directly to the left of $v$, add the diagonal from $v$ to the helper of $e$, set the helper of $e$ to $v$, and insert the edge leaving $v$ with helper $v$.
- **Merge** $v$: handle the entering edge as for an end vertex; then find the edge $e$ directly to the left, add a diagonal to its helper if that is a merge vertex, and set the helper of $e$ to $v$.
- **Regular** $v$ with the interior to its right: handle the entering edge as for an end vertex and insert the leaving edge with helper $v$. With the interior to its left: find the edge $e$ to the left, add a diagonal to its helper if that is a merge vertex, and set the helper of $e$ to $v$.

Each split vertex gets a diagonal upward and each merge vertex gets a diagonal downward, and these are exactly the vertices where the polygon fails to be monotone. The [monotone partition](/monotone-polygon-partition/) page treats this phase on its own.

**Phase 2: triangulate each piece.** The piece $M$ has $m$ vertices.

```pseudo id=main
TRIANGULATE-MONOTONE(M)                   ▷ M monotone, counterclockwise, m ≥ 3
L1  u[1 .. m] ← merge the left and right chains into the sweep order
L2  S ← stack (u[1], u[2])
L3  for j ← 3 to m − 1 do
L4      if u[j] and top(S) lie on different chains then
L5          pop every vertex s of S except the bottom one, output the triangle (u[j], s, the vertex under s)
L6          S ← stack (u[j − 1], u[j])
        else
L7          last ← pop(S)
L8          while S is not empty and the corner at last between top(S) and u[j] is strictly convex do
                output (u[j], last, top(S)); last ← pop(S)
L9          push last; push u[j]
L10 pop the vertices of S and output the fan from u[m]
```

- **Line L1** costs $O(m)$: the two chains are already sorted, so they are merged like two sorted lists. The top and the bottom vertex belong to both chains.
- **Lines L4 to L6.** When the new vertex is on the other chain, it sees every vertex on the stack, and the stack is cut away as a fan. The old top $u_{j-1}$ stays, as the new bottom.
- **Line L8** is the ear test of a reflex chain. On the left chain it is $\mathrm{orient}(u_j, \mathrm{top}(S), \textit{last}) > 0$, and on the right chain the sign is reversed. The test is strict, so a flat corner stays on the stack and no flat triangle is output.
- **The invariant.** The stack holds a chain of vertices on one side whose corners are reflex or flat, with one vertex of the other chain at the bottom. The vertices below the sweep are untouched.

## Example

Take the rectangle with a notch cut down from the top: $v_0 = (0,0)$, $v_1 = (6,0)$, $v_2 = (6,4)$, $v_3 = (4,4)$, $v_4 = (3,1)$, $v_5 = (2,4)$, $v_6 = (0,4)$, counterclockwise. The sweep order is $v_6, v_5, v_3, v_2, v_4, v_0, v_1$, since the four top vertices share $y = 4$ and are ordered by $x$.

| vertex | type | action |
|---|---|---|
| $v_6$ | start | insert $e_6 = v_6 v_0$ with helper $v_6$ |
| $v_5$ | regular, interior to the left | helper$(e_6) \leftarrow v_5$ |
| $v_3$ | start | insert $e_3 = v_3 v_4$ with helper $v_3$ |
| $v_2$ | regular, interior to the left | helper$(e_3) \leftarrow v_2$ |
| $v_4$ | merge | delete $e_3$; helper$(e_6) \leftarrow v_4$ |
| $v_0$ | regular, interior to the right | helper$(e_6) = v_4$ is a merge vertex: add $v_0 v_4$; delete $e_6$, insert $e_0$ |
| $v_1$ | end | delete $e_0$ |

The diagonal $v_0 v_4$ cuts $P$ into the monotone pieces $v_0 v_1 v_2 v_3 v_4$ and $v_0 v_4 v_5 v_6$. In the first piece the top is $v_3$, the bottom is $v_1$, and $u = v_3, v_2, v_4, v_0, v_1$. The stack starts as $(v_3, v_2)$. Then $v_4$ is on the other chain, so line L5 outputs $(v_4, v_2, v_3)$ and the stack becomes $(v_2, v_4)$. Next $v_0$ is on the same chain as $v_4$; the corner at $v_4$ between $v_2$ and $v_0$ is reflex ($\mathrm{orient}(v_0, v_2, v_4) = -6$), so line L9 gives the stack $(v_2, v_4, v_0)$. Line L10 outputs the fan from $v_1$, the triangles $(v_1, v_4, v_0)$ and $(v_1, v_2, v_4)$ in counterclockwise order. In the second piece $u = v_6, v_5, v_4, v_0$; at $v_4$ the corner at $v_5$ is convex, so line L8 outputs $(v_4, v_5, v_6)$, and line L10 outputs $(v_0, v_4, v_6)$. The five triangles have doubled areas $6 + 6 + 12 + 6 + 12 = 42$, the doubled area of $P$.

## Correctness

**Theorem.** For a simple polygon with $n \ge 3$ vertices, the two phases output $n - 2$ triangles with corners among the vertices, with disjoint interiors and union $P$.

The proof is in [proofs/correctness.md](proofs/correctness.md). For phase 2, the invariant says that the stack is a reflex chain of one side with a vertex of the other side at the bottom, and that the untriangulated rest $R$ is a monotone polygon whose vertices are the stack and the unprocessed vertices. A vertex on the other chain sees the whole stack, so the fan of line L5 is valid. On the same chain, each triangle of line L8 cuts off an [ear](/ear/) of $R$, since the vertices below lie below the triangle and the stack vertices lie outside the reflex chain. For phase 1, a polygon with no split and no merge vertex is monotone, and the sweep adds non-crossing diagonals that remove every split and merge vertex (de Berg et al., Lemmas 3.4 and 3.5).

## Complexity

- **Sorting.** $O(n \log n)$ to sort the vertices in the sweep order.
- **Phase 1.** Each vertex does $O(1)$ status operations. With a balanced search tree keyed by the $x$ coordinate at the sweep line, each costs $O(\log n)$, so the phase takes $O(n \log n)$.
- **Faces.** The pieces are the faces of the plane graph of the polygon edges and the diagonals. Sorting the edges around each vertex and walking the faces takes $O(n \log n)$.
- **Phase 2.** Each vertex is pushed at most twice and popped at most twice, so a piece with $m$ vertices takes $O(m)$, and the pieces have $O(n)$ vertices in total.
- **Total.** $\Theta(n \log n)$ time in the worst case and $\Theta(n)$ space. A monotone polygon alone takes $O(n)$.

The $n \log n$ term comes only from the sorting, not from the problem: [Chazelle's algorithm](/chazelle-polygon-triangulation/) takes $O(n)$ time. For polygons with holes the same sweep works, and there $\Omega(n \log n)$ is a lower bound in the [algebraic decision tree](/algebraic-decision-tree/) model.

## Properties

- **Exact.** All decisions are orientation signs and comparisons of coordinates. With integers or `fractions.Fraction` nothing is rounded.
- **Handles holes.** Phase 1 never uses the fact that the boundary is one cycle, so a [polygon with holes](/polygon-with-holes-triangulation/) is partitioned in the same way.
- **Few diagonals.** Phase 1 adds at most one diagonal for each split and each merge vertex, so a polygon with $r$ reflex vertices gets at most $r$ diagonals.
- **Deterministic.** The output depends only on the input order.
- **No Steiner points.** Every triangle corner is an input vertex.

## Variants and improvements

- **Sweep only at reflex vertices.** Hertel and Mehlhorn stop the sweep only at the $r$ reflex vertices and triangulate in $O(n + r \log r)$ time.
- **Trapezoidal decomposition.** A trapezoidal map of the polygon gives the monotone pieces directly; [Seidel's algorithm](/seidel-polygon-triangulation/) builds it by random insertion in $O(n \log^* n)$ expected time.
- **Monotone mountains.** Splitting the trapezoids along their diagonals gives monotone mountains, polygons with one chain a single edge, which can be cut by ears in linear time.
- **Sorting avoided.** [Tarjan and Van Wyk](/tarjan-van-wyk-triangulation/) triangulate in $O(n \log \log n)$, and Chazelle in $O(n)$, both without a full sort.
- **Monotone in another direction.** Any direction can serve as the sweep direction. A polygon that is monotone in some direction can be found and triangulated in linear time.

## When to use it

Use it when $O(n \log n)$ worst-case time matters and the polygon is large or has many reflex vertices, so that [ear clipping](/ear-clipping/) is too slow. It also handles holes without bridges, and it is the standard first step of [point location](/kirkpatrick-point-location/) structures built from a [planar subdivision](/planar-subdivision/). For small polygons, ear clipping is shorter. For good triangle shapes, use a constrained Delaunay triangulation instead, since both methods make thin triangles.

## Pitfalls

- **Ties in $y$.** A horizontal edge makes its two end points neither above nor below each other. Without the tilted sweep order, vertices on a horizontal edge are misclassified and the pieces are not monotone. The rotated comb test catches this.
- **Forgetting a merge helper.** A merge vertex that is a helper must get its diagonal from the next vertex that replaces it, which can happen in the end, merge, and both regular cases. Missing one case leaves a non-monotone piece.
- **The sign on the right chain.** The ear test of line L8 has opposite signs on the two chains. Using one sign makes triangles on the outside.
- **A non-strict ear test.** With $\ge 0$ in line L8, a flat corner is cut off as a triangle of zero area.
- **Face tracing.** The pieces must be traced with an exact angular order around each vertex. A wrong turn rule merges two pieces or returns the outer face.
- **Linear status.** The Python implementation keeps the status as a list scanned linearly, which costs $O(n)$ per query. The $O(n \log n)$ bound needs a balanced search tree.

## Implementations

The Python version has three parts. `make_monotone` runs the sweep and returns the diagonals; `triangulate_monotone` runs the stack algorithm on one piece; `triangulate_polygon` makes the order counterclockwise, traces the pieces, and triangulates each. The tests check every result against a brute-force validator (count $n - 2$, exact sum of doubled areas, no crossing edges, no vertex inside a triangle). They also check that each piece of the partition is monotone and that the number of pieces is one more than the number of diagonals. Inputs include combs, a comb rotated by a quarter turn, spirals in both directions, zigzag monotone polygons, random simple polygons on small grids, `Fraction` coordinates and very large integers.

## History

Lee and Preparata introduced the sweep that cuts a planar subdivision into monotone pieces in 1977, for point location. Garey, Johnson, Preparata and Tarjan (1978) gave the linear stack method for monotone polygons and the resulting $O(n \log n)$ triangulation of simple polygons. Hertel and Mehlhorn (1983) made the cost depend on the number of reflex vertices. The question whether $O(n \log n)$ was optimal led to the $O(n \log \log n)$ algorithm of Tarjan and Van Wyk (1988) and to Chazelle's linear-time algorithm (1991).

## References
