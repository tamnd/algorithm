---
tag: GH08T5
kind: algorithm
slug: funnel-algorithm
name: Funnel algorithm
aliases:
- Lee-Preparata funnel algorithm
- funnel shortest path
- string pulling
area: geometry/polygons
level: advanced
summary: Computes the shortest path in a triangulated polygon in linear time after triangulation.
solves: [euclidean-shortest-path-in-polygon]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1984
  people: [Der-Tsai Lee, Franco P. Preparata]
  note: Lee and Preparata gave the funnel method for shortest paths in a triangulated simple polygon in 1984; Guibas, Hershberger, Leven, Sharir and Tarjan extended it to shortest path trees in 1987.
prereqs: [euclidean-shortest-path-in-polygon, polygon-triangulation, triangulation-dual-tree, deque, orientation-test]
see_also: [euclidean-shortest-path, visibility-graph-of-polygon, ear-clipping, breadth-first-search, shortest-path-tree, a-star-search, simple-polygon, hertel-mehlhorn]
sources:
  - paper: "Der-Tsai Lee and Franco P. Preparata, Euclidean shortest paths in the presence of rectilinear barriers, Networks 14(3), 1984, 393 to 410"
    locator: the funnel, its apex and its two concave chains, and the linear time shortest path in a triangulated simple polygon
  - paper: doi:10.1007/BF01840360
    title: Leonidas J. Guibas, John Hershberger, Daniel Leven, Micha Sharir and Robert E. Tarjan, Linear-time algorithms for visibility and shortest path problems inside triangulated simple polygons, Algorithmica 2, 1987, 209 to 233
    locator: the funnel splitting procedure for the shortest path tree from one source
  - paper: "John Hershberger and Jack Snoeyink, Computing minimum length paths of a given homotopy class, Computational Geometry: Theory and Applications 4(2), 1994, 63 to 97"
    locator: the funnel stored as a deque, and the fact that a locally shortest path is the shortest path in its homotopy class
---

The funnel algorithm finds the [shortest path](/euclidean-shortest-path-in-polygon/) between two points $s$ and $t$ inside a [triangulated](/polygon-triangulation/) [simple polygon](/simple-polygon/). It first follows the [dual tree](/triangulation-dual-tree/) of the triangulation from the triangle of $s$ to the triangle of $t$. The diagonals crossed on the way are the *portals*. The algorithm then pushes the path through the portals one at a time. It keeps the shortest paths to the two ends of the current portal as a *funnel*: a common part up to the *apex*, then two concave chains stored in a [deque](/deque/). Each point enters and leaves the deque at most once, so after the triangulation the algorithm runs in $O(n)$ time. Lee and Preparata published it in 1984. In game programming it is known as string pulling, where it straightens paths found on navigation meshes.

## In plain words

Cut the polygon into triangles and walk from the triangle that holds the start to the triangle that holds the goal. Each time you pass from one triangle to the next, you cross a doorway.

Imagine strings tied at the start and pulled tight to the two sides of the current doorway. Together they look like a funnel, joined at one end and open at the doorway. When you reach the next doorway, one of its sides is new. Pull a string to it. It may slide off some corners on its own side, which are no longer needed. If it crosses over to the other side, the funnel's neck moves forward to the corner where the strings now meet, and that corner becomes part of the final path.

At the goal, the string to the goal is the answer.

## The problem

**Input.** A simple polygon $P$ with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order, with exact coordinates, a triangulation $T$ of $P$ into $n - 2$ triangles with positive area given as triples of vertex indices, and two points $s$ and $t$ in the closed polygon. Straight vertices are allowed, and $s$ and $t$ may lie on the boundary or on diagonals.

**Output.** The shortest path from $s$ to $t$ in $P$, as the list $s = p_0, p_1, \ldots, p_k = t$ of its points, where each inner point is a reflex vertex of $P$ at which the path really bends.

**Notation.** $\operatorname{orient}(a, b, c)$ is positive when $a, b, c$ turn left and negative when they turn right, as in the [orientation test](/orientation-test/). A portal $(\ell, r)$ is a diagonal with $\ell$ on the left and $r$ on the right as seen by someone walking from $s$ towards $t$. The *left chain* $L$ and the *right chain* $R$ are lists of points that start at the apex. The sign $\sigma$ is $+1$ for the right side and $-1$ for the left side, so that the left side uses the mirror images of the tests.

## The algorithm

```pseudo id=main
FUNNEL(P, T, s, t)
L1  if s = t then return [s]; find triangles T_s and T_t of T that contain s and t
L2  find the path T_s = T_0, T_1, …, T_m = T_t in the dual tree by breadth-first search
L3  for i ← 1 to m: (ℓ_i, r_i) ← the diagonal shared by T_{i−1} and T_i, with ℓ_i on the left
L4  E ← (left, ℓ_1), (right, r_1), then for i ≥ 2 the endpoint of portal i that is not in portal i − 1, with its side, then (right, t)
L5  L ← [s]; R ← [s]; path ← [ ]                                  ▷ L[0] = R[0] is the apex
L6  for each (side, v) in E, with X the chain of that side, Y the other, σ its sign do
L7      while |X| ≥ 2 and σ · orient(X[−2], X[−1], v) ≥ 0 do pop the back of X
L8      if |X| = 1 then while |Y| ≥ 2 and σ · orient(Y[0], Y[1], v) > 0 do append Y[0] to path; pop the front of Y; X[0] ← Y[0]
L9      push v at the back of X
L10 return path followed by R
```

Lines L1 to L3 build the *sleeve*, the chain of triangles between $s$ and $t$. If $T_{i-1}$ has the counterclockwise edge $u \to w$ in common with $T_i$, then walking out of $T_{i-1}$ across it puts $w$ on the left, so the portal is $(w, u)$. Consecutive portals are two sides of the same triangle, so they share exactly one endpoint, and line L4 lists the new endpoint of each portal with its side. The goal $t$ comes last, as a new point on the right.

Line L7 removes from the back of the new point's own chain the points that a string to $v$ no longer touches: on the right chain, a point stays only if the chain turns strictly right there on its way to $v$. Collinear points are removed too, so the output has no straight inner points. If the own chain is reduced to the apex, line L8 checks whether $v$ lies strictly beyond the first edge of the other chain. If so, the string to $v$ must wrap around that chain, the apex moves one step along it, and the old apex becomes part of the final path. Line L9 adds $v$. At the end the right chain runs from the apex to $t$, and line L10 returns the finished part of the path followed by it.

## Example

Take the U-shaped polygon $P = (0,0), (8,0), (8,6), (5,6), (5,2), (3,2), (3,6), (0,6)$, with $s = (1,5)$ in the left arm and $t = (7,5)$ in the right arm. Ear clipping gives a sleeve of six triangles, whose five portals as $(\ell, r)$ pairs are $((3,2), (0,6))$, $((3,2), (0,0))$, $((5,2), (0,0))$, $((5,2), (8,0))$ and $((5,6), (8,0))$. The events are the new endpoints, then $t$.

| event | line L7 pops | line L8 moves the apex | left chain $L$ | right chain $R$ | path |
|---|---|---|---|---|---|
| left $(3,2)$ | | | $(1,5), (3,2)$ | $(1,5)$ | |
| right $(0,6)$ | | | $(1,5), (3,2)$ | $(1,5), (0,6)$ | |
| right $(0,0)$ | $(0,6)$: orient $= 6$ | no: orient $= -13$ | $(1,5), (3,2)$ | $(1,5), (0,0)$ | |
| left $(5,2)$ | | | $(1,5), (3,2), (5,2)$ | $(1,5), (0,0)$ | |
| right $(8,0)$ | $(0,0)$: orient $= 40$ | to $(3,2)$: orient $= 11$ | $(3,2), (5,2)$ | $(3,2), (8,0)$ | $(1,5)$ |
| left $(5,6)$ | | | $(3,2), (5,2), (5,6)$ | $(3,2), (8,0)$ | $(1,5)$ |
| right $(7,5)$ | $(8,0)$: orient $= 23$ | to $(5,2)$: orient $= 6$ | $(5,2), (5,6)$ | $(5,2), (7,5)$ | $(1,5), (3,2)$ |

At the event $(8,0)$, the right chain loses $(0,0)$, and then $(8,0)$ lies strictly left of the first left edge from $(1,5)$ to $(3,2)$, so the string has to wrap around $(3,2)$ and the apex moves there. The next test, $\operatorname{orient}((3,2), (5,2), (8,0)) = -4$, stops the move. At $t$ the same happens at $(5,2)$. The result is $(1,5), (3,2), (5,2), (7,5)$, of length $2 + 2\sqrt{13} \approx 9.21$, which bends at the two reflex corners at the bottom of the notch.

## Correctness

The algorithm keeps a funnel invariant over the portals. After the events of portal $i$, the finished path followed by $L$ is the shortest path from $s$ to $\ell_i$, and the finished path followed by $R$ is the shortest path from $s$ to $r_i$. The left chain turns strictly left and the right chain strictly right, so the region between them and the portal is a funnel whose only reflex corners are the inner chain points. A shortest path from $s$ to the new endpoint $v$ crosses the previous portal, so it is the shortest path to the apex followed by the shortest path through the funnel and the next triangle. Lines L7 and L8 find the point where a tight string from $v$ touches the funnel, and the result is a locally shortest path. In a simple polygon a locally shortest path is the shortest path. Every pop removes a point that was pushed earlier, so the loop stops after $O(m)$ steps. The [full proof](proofs/correctness/) gives the details.

## Complexity

- **Time.** $\Theta(n)$ worst case after the triangulation. The sleeve has $m + 1 \le n - 2$ triangles, and the breadth-first search in line L2 takes $O(n)$ time on the dual tree. Line L4 produces $m + 2$ events. Each event pushes one point in line L9, and each iteration of the loops in lines L7 and L8 removes a point from a chain, so all events together take $O(m)$ time.
- **Locating $s$ and $t$.** Testing every triangle takes $O(n)$ time, and a [point location](/planar-point-location/) structure answers in $O(\log n)$ when many queries share one polygon.
- **Triangulation.** $O(n)$ with Chazelle's algorithm, $O(n \log n)$ with practical methods, or $O(n^2)$ with simple [ear clipping](/ear-clipping/). In practice the triangulation dominates.
- **Space.** $\Theta(n)$ for the triangulation, the dual tree and the deque.

## Properties

- **Exact.** All decisions are signs of orientation tests on input points, so with integer or rational coordinates every branch is decided exactly. The output points are input points, so they are exact too. Only the length, a sum of square roots, needs floating point.
- **Output.** The inner points of the path are reflex vertices of $P$ at which the path bends, with no straight inner points.
- **Any triangulation.** The sleeve depends on the triangulation, but the shortest path is unique, so every triangulation gives the same path.
- **Monotone progress.** The finished part of the path only grows. Once a point leaves the funnel through line L8, it is final, which allows streaming the path in order.

## Variants and improvements

- **Shortest path tree.** Guibas, Hershberger, Leven, Sharir and Tarjan run the funnel from $s$ into the whole dual tree, splitting the funnel at each triangle with a finger search tree. This gives the shortest paths from $s$ to all vertices in $O(n)$ time after triangulation.
- **Homotopic paths.** Hershberger and Snoeyink apply the funnel to a sleeve given by a path in a polygonal domain with holes, which gives the shortest path in that homotopy class.
- **Simple stupid funnel.** A popular version for games, by Mikko Mononen, keeps only the two current funnel edges instead of whole chains. When the apex moves it restarts from the portal of the new apex. It is short to write, but it can examine a portal many times.
- **Portal sequences from other cell decompositions.** Any partition into convex cells works in place of triangles, such as a navigation mesh or the convex pieces of [Hertel and Mehlhorn](/hertel-mehlhorn/), as long as consecutive cells share a single segment. The new endpoint of a portal is then not always unique, and the general version adds the new endpoints of both sides in order.
- **Agents with a radius.** For a disk of radius $\rho$, the funnel is run on an offset domain, or the portal endpoints are moved inward by $\rho$ and the corners are replaced by arcs.

## When to use it

Use it for shortest paths in a simple polygon, or in any domain where a corridor of triangles or convex cells is already known, such as a path found by [A*](/a-star-search/) on a navigation mesh. For many queries from one source, use the shortest path tree. For domains with holes, where the corridor is not known in advance, use the [visibility graph](/visibility-graph-of-polygon/) with Dijkstra for small inputs, or continuous Dijkstra for large ones.

## Pitfalls

- **Left and right swapped.** If the portals are oriented the wrong way, the tests at lines L7 and L8 accept the wrong side and the path leaves the polygon. Orient each portal from the counterclockwise edges of the triangle before it.
- **The goal event.** Forgetting to add $t$ as a final event, or adding it to a chain without the tests, gives a path that ends at a portal or cuts a corner.
- **Floating point orientations.** Orientation tests in floating point with a tolerance make inconsistent decisions near collinear points, which can leave a point that should have been popped or move the apex too early. Use exact integer or rational arithmetic.
- **Collinear points.** With $\ge$ at line L7 and strict $>$ at line L8, the output has no straight inner points. If the apex moved on equality at line L8, it would add straight points. In the triangle $(0,0), (2,2), (0,2)$ with an extra vertex $(0,1)$ on its left side, the path from $(0,0)$ to $(0,2)$ runs along that side, and the changed test lists $(0,1)$ as a point of the path. The length would be right but the path would have an extra point.
- **Points on diagonals or at vertices.** If $s$ is a vertex of $P$ or lies on a diagonal, several triangles contain it. Any of them gives a correct sleeve, but a duplicate point can appear when $s$ is also a portal endpoint. Drop repeated points from the output.
- **Polygons with holes.** The dual graph has cycles, so the sleeve is not unique, and the funnel finds only the shortest path within the homotopy class of the chosen sleeve.

## Implementations

## History

Der-Tsai Lee and Franco P. Preparata introduced the funnel in 1984, in a paper on Euclidean shortest paths among rectilinear barriers. They showed that the shortest path between two points of a triangulated simple polygon can be found in linear time. In 1987 Guibas, Hershberger, Leven, Sharir and Tarjan turned the method into linear time algorithms for the shortest path tree and the visibility polygon. Hershberger and Snoeyink in 1994 described the funnel as a deque and used it for shortest paths of a given homotopy class. Combined with Chazelle's linear time triangulation of 1991, the funnel solves the shortest path problem in a simple polygon in $\Theta(n)$ time. Game developers adopted it under the name string pulling for navigation meshes.

## References
