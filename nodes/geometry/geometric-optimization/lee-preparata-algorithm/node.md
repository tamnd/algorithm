---
tag: A26CZG
kind: algorithm
slug: lee-preparata-algorithm
name: Lee-Preparata algorithm
aliases:
- Lee-Preparata shortest path in a simple polygon
- Lee-Preparata shortest path algorithm
area: geometry/geometric-optimization
level: advanced
summary: Shortest path between two points of a simple polygon. Triangulate, take the dual tree path, and push a funnel through its diagonals in linear time; O(n log n) with the triangulation of 1984.
solves: [euclidean-shortest-path-in-polygon]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1984
  people: [Der-Tsai Lee, Franco P. Preparata]
  note: Lee and Preparata reduced the shortest path in a simple polygon to a walk through the triangles of a triangulation, with a funnel of two concave chains; the walk is linear and the triangulation, then O(n log n), dominated.
prereqs: [euclidean-shortest-path-in-polygon, polygon-triangulation, triangulation-dual-tree, orientation-test]
see_also: [funnel-algorithm, euclidean-shortest-path, visibility-graph, ear-clipping, chazelle-polygon-triangulation, shortest-path-tree, minimum-link-path, deque]
sources:
  - paper: "Der-Tsai Lee and Franco P. Preparata, Euclidean shortest paths in the presence of rectilinear barriers, Networks 14(3), 1984, 393 to 410"
    locator: the shortest path between two points of a triangulated simple polygon by the funnel, in time linear in the number of triangles, after an O(n log n) triangulation
  - paper: doi:10.1007/BF01840360
    title: Leonidas J. Guibas, John Hershberger, Daniel Leven, Micha Sharir and Robert E. Tarjan, Linear-time algorithms for visibility and shortest path problems inside triangulated simple polygons, Algorithmica 2, 1987, 209 to 233
    locator: Section 2, the funnel and the shortest path tree from one point to all vertices in linear time after triangulation
  - paper: doi:10.1007/BF02574703
    title: Bernard Chazelle, Triangulating a simple polygon in linear time, Discrete and Computational Geometry 6, 1991
    locator: the linear time triangulation, which makes the whole method Θ(n)
  - paper: "John Hershberger and Jack Snoeyink, Computing minimum length paths of a given homotopy class, Computational Geometry: Theory and Applications 4(2), 1994, 63 to 97"
    locator: the funnel as a deque, and the fact that a locally shortest path is the shortest path of its homotopy class
  - paper: "Michael R. Garey, David S. Johnson, Franco P. Preparata and Robert E. Tarjan, Triangulating a simple polygon, Information Processing Letters 7(4), 1978"
    locator: the O(n log n) triangulation that the 1984 bound uses
---

The Lee-Preparata algorithm finds the [shortest path](/euclidean-shortest-path-in-polygon/) between two points $s$ and $t$ inside a [simple polygon](/simple-polygon/) with $n$ vertices. It first [triangulates](/polygon-triangulation/) the polygon. The triangles form a tree, the [dual tree](/triangulation-dual-tree/), so exactly one chain of triangles leads from the triangle of $s$ to the triangle of $t$, and the shortest path stays inside that chain. The algorithm then walks along the chain and keeps the shortest paths to the two ends of the current diagonal as a *funnel*: a common part up to an *apex*, then two inward-bending chains. Each vertex enters and leaves the funnel at most once, so the walk takes $O(n)$ time. Lee and Preparata (1984) used an $O(n \log n)$ triangulation; with [Chazelle's linear time triangulation](/chazelle-polygon-triangulation/) (1991) the whole algorithm runs in $\Theta(n)$ time. The walk alone, given the chain of triangles, is the [funnel algorithm](/funnel-algorithm/).

## In plain words

Cut the room into triangles. Because the room has no pillars, there is only one way to go from the triangle where you start to the triangle where you end without going back. The best route never leaves this chain of triangles.

Walk along the chain. Each step crosses a doorway between two triangles. Imagine two strings tied at the start and pulled tight to the two sides of the current doorway. They share a first part, then split into two bent arms, like a funnel.

At the next doorway, one side is new. Pull a string to it. It may slip off corners on its own arm. If it swings past the other arm, the point where the arms meet moves forward, and the corner it leaves behind is fixed on the final route.

At the end, pull the string to the goal. It is the shortest route.

## The problem

Notation: $P$ is a simple polygon with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order. $s$ and $t$ are points of the closed polygon. $\pi(x, y)$ is the shortest path from $x$ to $y$ in $P$. $\operatorname{orient}(a, b, c)$ is twice the signed area of the triangle $abc$: positive for a left turn, zero for collinear points, as in the [orientation test](/orientation-test/). A *portal* is a diagonal crossed by the walk, written $(\ell, r)$ with $\ell$ on the walker's left and $r$ on the right. The sign $\sigma$ is $+1$ for the right side and $-1$ for the left, so the left side uses mirrored tests.

**Input.** $P$ with exact (integer or rational) coordinates, and $s$, $t$ in the closed polygon. Three consecutive vertices may be collinear. $s$ and $t$ may lie on the boundary, on a diagonal, or at a vertex.

**Output.** $\pi(s, t)$ as a list $s = p_0, p_1, \ldots, p_k = t$. Each inner point is a reflex vertex of $P$ at which the path turns.

No general position is needed. The path may run along edges of $P$ and may touch the boundary.

## The algorithm

```pseudo id=main
LEE-PREPARATA(P, s, t)
L1  if s = t then return [s];  triangulate P
L2  build the dual tree: one node per triangle, one edge per shared diagonal
L3  T_s ← a triangle that contains s;  T_t ← a triangle that contains t
L4  find the path T_s = T_0, T_1, …, T_m = T_t in the dual tree by breadth-first search
L5  for i ← 1 to m: (ℓ_i, r_i) ← the diagonal of T_{i−1} and T_i, with ℓ_i on the left
L6  E ← (left, ℓ_1), (right, r_1), the new endpoint of each later portal with its side, then (right, t)
L7  L ← [s];  R ← [s];  done ← [ ]                    ▷ L[0] = R[0] is the apex
L8  for each (side, v) in E, with X the chain of that side, Y the other chain, σ its sign do
L9      while |X| ≥ 2 and σ · orient(X[−2], X[−1], v) ≥ 0 do pop the back of X
L10     if |X| = 1 then while |Y| ≥ 2 and σ · orient(Y[0], Y[1], v) > 0 do append Y[0] to done; pop the front of Y; X[0] ← Y[0]
L11     push v at the back of X
L12 return done followed by R
```

Line L1 can use any triangulation. The implementation clips ears, which is simple and slow; the 1984 paper used an $O(n \log n)$ method. Line L5 orients each portal: if $u \to w$ is the counterclockwise edge of $T_{i-1}$ shared with $T_i$, then crossing it puts $w$ on the left, so $(\ell_i, r_i) = (w, u)$. Two consecutive portals are two sides of one triangle, so they share one endpoint, and line L6 lists only the new one.

Line L9 drops the points of the new point's own chain that a tight string to $v$ no longer touches. On the right chain a point stays only if the chain turns strictly right there toward $v$. Line L10 runs when the own chain has shrunk to the apex: if $v$ lies strictly beyond the first edge of the other chain, the string must wrap around that chain, so the apex moves one step along it and the old apex is final. The deques give $O(1)$ time per push and pop at either end.

## Example

Take the room with two walls $P = (0,0), (4,0), (4,4), (5,4), (5,0), (12,0), (12,6), (9,6), (9,2), (8,2), (8,6), (0,6)$. One wall rises from the floor between $x = 4$ and $x = 5$ up to $y = 4$, and one hangs from the ceiling between $x = 8$ and $x = 9$ down to $y = 2$. Let $s = (1,1)$ and $t = (11,5)$. Ear clipping gives 10 triangles, and the dual tree path visits all of them. The 9 portals $(\ell, r)$ are $((0,6),(4,0))$, $((0,6),(4,4))$, $((0,6),(5,4))$, $((8,6),(5,4))$, $((8,2),(5,4))$, $((8,2),(5,0))$, $((9,2),(5,0))$, $((9,2),(12,0))$ and $((9,6),(12,0))$.

| event | line L9 pops | line L10 moves the apex | left chain $L$ | right chain $R$ | done |
|---|---|---|---|---|---|
| left $(0,6)$ | | | $(1,1), (0,6)$ | $(1,1)$ | |
| right $(4,0)$ | | no: orient $= -14$ | $(1,1), (0,6)$ | $(1,1), (4,0)$ | |
| right $(4,4)$ | $(4,0)$: orient $= 12$ | no: orient $= -18$ | $(1,1), (0,6)$ | $(1,1), (4,4)$ | |
| right $(5,4)$ | none: orient $= -3$ | | $(1,1), (0,6)$ | $(1,1), (4,4), (5,4)$ | |
| left $(8,6)$ | $(0,6)$: orient $= -40$ | to $(4,4)$: orient $= -6$ | $(4,4), (8,6)$ | $(4,4), (5,4)$ | $(1,1)$ |
| left $(8,2)$ | $(8,6)$: orient $= -16$ | to $(5,4)$: orient $= -2$ | $(5,4), (8,2)$ | $(5,4)$ | $(1,1), (4,4)$ |
| right $(5,0)$ | | no: orient $= -12$ | $(5,4), (8,2)$ | $(5,4), (5,0)$ | $(1,1), (4,4)$ |
| left $(9,2)$ | none: orient $= 2$ | | $(5,4), (8,2), (9,2)$ | $(5,4), (5,0)$ | $(1,1), (4,4)$ |
| right $(12,0)$ | $(5,0)$: orient $= 28$ | to $(8,2)$: orient $= 2$ | $(8,2), (9,2)$ | $(8,2), (12,0)$ | $(1,1), (4,4), (5,4)$ |
| left $(9,6)$ | none: orient $= 4$ | | $(8,2), (9,2), (9,6)$ | $(8,2), (12,0)$ | $(1,1), (4,4), (5,4)$ |
| right $(11,5)$ | $(12,0)$: orient $= 18$ | to $(9,2)$: orient $= 3$ | $(9,2), (9,6)$ | $(9,2), (11,5)$ | $(1,1), (4,4), (5,4), (8,2)$ |

At the event $(8,6)$ the left chain loses $(0,6)$, and then $(8,6)$ lies strictly right of the first right edge from $(1,1)$ to $(4,4)$ (orient $-6$, and $\sigma = -1$), so the string wraps over the top of the first wall and the apex moves to $(4,4)$. At $(8,2)$ the apex moves on to $(5,4)$, the other top corner of the wall. At $(12,0)$ and at $t$ the apex moves to the two bottom corners of the second wall. The result is $(1,1), (4,4), (5,4), (8,2), (9,2), (11,5)$, of length $3\sqrt{2} + 1 + \sqrt{13} + 1 + \sqrt{13} = 2 + 3\sqrt{2} + 2\sqrt{13} \approx 13.454$. Every inner point is a reflex corner of a wall.

## Correctness

The full proof is in [proofs/correctness](proofs/correctness.md). It has four parts.

1. **The sleeve.** The dual graph of a triangulation of a simple polygon is a tree. A path between two points of the chain $T_0, \ldots, T_m$ that leaves it must come back through the same diagonal, and that detour can be cut short. So $\pi(s, t)$ lies in the chain, and so do the shortest paths to all portal endpoints.
2. **The portals.** Line L5 orients each portal correctly, and line L6 lists each portal endpoint once, with its side.
3. **The funnel invariant.** After the events of portal $i$, done followed by $L$ is $\pi(s, \ell_i)$, done followed by $R$ is $\pi(s, r_i)$, $L$ turns strictly left and $R$ strictly right. For a new endpoint $v$, lines L9 to L11 produce a path to $v$ that lies in the polygon and bends only around reflex vertices with the polygon outside the bend. In a simple polygon such a taut path is the shortest path.
4. **Termination.** Every pop and every apex move removes a point that was pushed earlier, so the loops run $O(m)$ times in total.

## Complexity

- **The walk.** $O(n)$. The chain has $m + 1 \le n - 2$ triangles, the breadth-first search on the dual tree takes $O(n)$, and the events take $O(m)$ in total by the counting in part 4.
- **Locating $s$ and $t$.** $O(n)$ by testing every triangle, or $O(\log n)$ with a [point location](/planar-point-location/) structure when many queries share one polygon.
- **The triangulation.** $O(n \log n)$ as in 1984, $\Theta(n)$ with Chazelle's algorithm, $O(n \log^* n)$ expected with [Seidel's randomized method](/seidel-polygon-triangulation/). This step dominates, so the stated bound is $O(n \log n)$ and the best bound is $\Theta(n)$, which is optimal because the input must be read.
- **Space.** $O(n)$ for the triangles, the dual tree and the two chains.
- **The implementation.** Ear clipping by testing every vertex against every candidate ear takes $O(n^3)$ in the worst case. It is meant for checking, not for speed.

## Properties

- **Exact.** Every branch is the sign of an orientation test on input points. With integer or rational coordinates the path is exact. Only its length, a sum of square roots, needs floating point.
- **Output.** The inner points are reflex vertices of $P$ where the path really turns. Straight points are dropped by the $\ge$ in line L9 and the strict $>$ in line L10.
- **Independent of the triangulation.** The chain of triangles depends on the triangulation, but the shortest path in a simple polygon is unique, so every triangulation gives the same output.
- **Final prefix.** Points moved into done never change, so the path can be reported in order while the walk is running.

## Variants and improvements

- **Shortest path tree.** Guibas, Hershberger, Leven, Sharir and Tarjan (1987) run the funnel through the whole dual tree and split it at each branching triangle. This gives the [shortest path tree](/shortest-path-tree/) from $s$ to all vertices in $O(n)$ time after triangulation.
- **Queries.** Guibas and Hershberger (1989) preprocess the polygon in $O(n)$ time so that the distance between any two points is found in $O(\log n)$ time.
- **Polygons with holes.** The dual graph has cycles, and the funnel only gives the shortest path inside one chosen chain of triangles, that is, in one homotopy class. For the true shortest path use the [visibility graph](/visibility-graph/) or the continuous Dijkstra method of the [Euclidean shortest path](/euclidean-shortest-path/) problem.
- **Parallel segment barriers.** The 1984 paper also treats shortest paths among disjoint parallel line segments, where the structure of the free space again allows an $O(n \log n)$ algorithm.
- **Minimum number of turns.** The [minimum link path](/minimum-link-path/) in a simple polygon uses the same sleeve, but grows visibility windows instead of funnels.
- **Other Lee-Preparata algorithms.** Lee and Preparata (1979) also gave a linear time algorithm for the kernel of a polygon, the set of points that see the whole polygon. It is a different algorithm.

## When to use it

Use it for one or a few shortest path queries in a simple polygon, or in any domain where a corridor of triangles or convex cells is already known, such as a navigation mesh path found by [A*](/a-star-search/). For many queries from one source, build the shortest path tree. For domains with holes and few vertices, use the visibility graph with [Dijkstra's algorithm](/dijkstra/); for large ones, use continuous Dijkstra.

## Pitfalls

- **Holes.** The method assumes a tree of triangles. On a domain with holes, breadth-first search picks one corridor, and the path found may not be the shortest.
- **Portal sides.** If a portal is oriented the wrong way, lines L9 and L10 test the wrong side and the path cuts through walls. Orient from the counterclockwise edge of the earlier triangle.
- **The goal event.** Forgetting the final event $(right, t)$, or adding $t$ without the tests, gives a path that ends at a portal or cuts a corner.
- **Floating point.** Orientation tests with a tolerance give inconsistent answers near collinear points. Use exact arithmetic.
- **Equal tests.** With $>$ in line L9 or $\ge$ in line L10, collinear points stay in the output as extra points. The length is still right.
- **Points at vertices or on diagonals.** Several triangles then contain $s$ or $t$; any choice is correct, but a point can appear twice in a row. Remove repeated points.

## Implementations

## History

Der-Tsai Lee and Franco P. Preparata published the method in 1984 in Networks, in a paper on Euclidean shortest paths among rectilinear barriers. They showed that, once the polygon is triangulated, the shortest path between two points follows from a walk through the triangles that takes linear time, so the $O(n \log n)$ triangulation of Garey, Johnson, Preparata and Tarjan (1978) was the bottleneck. Chazelle gave a related linear time result for shortest paths in triangulated polygons around the same time. In 1987 Guibas, Hershberger, Leven, Sharir and Tarjan extended the funnel to the shortest path tree. Chazelle's linear time triangulation (1991) made the whole problem $\Theta(n)$. The same walk, under the name string pulling, straightens paths on navigation meshes in games.

## References
