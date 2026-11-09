---
tag: HPKK4H
kind: algorithm
slug: chazelle-polygon-triangulation
name: Chazelle's linear-time polygon triangulation
aliases:
- Chazelle triangulation
- Chazelle's linear-time triangulation
- linear-time polygon triangulation
- Chazelle's algorithm
area: geometry/triangulations
level: research
summary: Triangulates a simple polygon in O(n) time, using a complicated decomposition.
solves: [polygon-triangulation]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: true}
history:
  year: 1991
  people: [Bernard Chazelle]
  note: Chazelle computed the horizontal visibility map of a simple polygon in linear time with a merge-sort-like up-phase over boundary chains, keeping coarse submaps, followed by a down-phase that refines them. A triangulation follows in linear time. The result settled the complexity of polygon triangulation, but the algorithm is regarded as too complicated to implement.
prereqs: [polygon-triangulation, trapezoidal-map, tarjan-van-wyk-triangulation, monotone-polygon, simple-polygon, orientation-test]
see_also: [seidel-polygon-triangulation, monotone-polygon-triangulation, ear-clipping, polygon-simplicity-test, kirkpatrick-point-location, planar-subdivision, triangulation-dual-tree, polygon-with-holes-triangulation]
sources:
  - paper: "Bernard Chazelle, Triangulating a simple polygon in linear time, Discrete and Computational Geometry 6(5), 485 to 524 (1991), doi:10.1007/BF02574703"
    locator: the submaps and their granularity, the up-phase and down-phase, the ray-shooting oracle, and the linear bound
  - paper: "Bernard Chazelle, Triangulating a simple polygon in linear time, Proceedings of the 31st Annual Symposium on Foundations of Computer Science (FOCS 1990), 220 to 230"
    locator: the conference version (pages to be checked)
  - paper: "Alain Fournier and Delfin Y. Montuno, Triangulating simple polygons and equivalent problems, ACM Transactions on Graphics 3(2), 153 to 174 (1984)"
    locator: the linear-time conversion between a trapezoidal decomposition and a triangulation
  - paper: "Nancy M. Amato, Michael T. Goodrich and Edgar A. Ramos, A randomized algorithm for triangulating a simple polygon in linear time, Discrete and Computational Geometry 26(2), 245 to 265 (2001)"
    locator: a randomized expected linear-time algorithm built on the same ideas (pages to be checked)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 2, the history of triangulation algorithms and the status of Chazelle's algorithm
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3 notes and comments, on Chazelle's linear-time algorithm
---

Chazelle's algorithm solves the [polygon triangulation](/polygon-triangulation/) problem in $\Theta(n)$ deterministic time, which is optimal. It was published in 1991, after a line of results that brought the bound down from $O(n \log n)$ through [Tarjan and Van Wyk's](/tarjan-van-wyk-triangulation/) $O(n \log \log n)$. Like that algorithm, it computes the **horizontal visibility map** of the polygon, the [trapezoidal map](/trapezoidal-map/) of its edges, and then turns the map into triangles in linear time. The map is built in two phases over chains of the boundary, using coarse summaries of the map called submaps. The algorithm is a landmark in theory, but it is widely regarded as too complicated to implement, and no practical implementation is in use. The code on this page implements only its last stage, from the visibility map to the triangles, on a map computed by brute force.

## In plain words

From every corner of a shape, shine a flashlight to the left and to the right, but only into the shape. Each beam stops at the first wall. The beams cut the shape into slabs, and from the slabs a triangulation follows quickly. So the real question is how fast the beams can be found.

Chazelle found all the beams in time proportional to the number of corners. He cut the boundary into pieces, then pieces of pieces, like the levels of merge sort. For each piece he kept only a rough sketch of its beams, small enough to merge cheaply. At the top, the sketch of the whole boundary was then sharpened, step by step, into the full set of beams.

The method is famous for being correct and fast on paper but too complex to program.

## The problem

The input is a simple polygon $P$ with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order. Edge $i$ joins $v_i$ and $v_{i+1}$, with indices modulo $n$. The output is a list of $n - 2$ triangles, as counterclockwise index triples, with disjoint interiors and union $P$.

"Above" compares points by $(y, x)$ in lexicographic order, which acts as a symbolic shear and gives every vertex its own height. A **chord** at a vertex $v$ is the horizontal segment from $v$ to the first edge it meets, drawn when it starts into the interior. The **visibility map** is the set of all chords. The code assumes distinct vertices with no three collinear.

## The algorithm

**Chazelle's construction of the map.** The algorithm treats the boundary as a polygonal chain and the visibility map as a map of a chain. A **submap** of a chain keeps only some of the chords, so that its regions are larger. The **granularity** of a submap bounds how much of the chain each region may hold. A submap is **conformal** when each region is bounded by few chords. Conformal submaps of bounded granularity are much smaller than the chain itself, and they still carry enough information to answer ray-shooting queries.

- **Up-phase.** Split the boundary into chains whose lengths are powers of two, as in merge sort. Going up the levels, merge the submaps of two neighboring chains into a submap of their union. The merge shoots rays from one chain against the other. It uses a point-location structure built on the submaps, and it coarsens the result back to the granularity allowed at that level. The granularity grows with the level, so the submaps stay small and the total work is linear.
- **Down-phase.** The up-phase ends with a coarse submap of the whole boundary. Each region of it is then refined into its part of the full visibility map, region by region, by recursively applying the same kind of reasoning with finer granularity, again in linear total time.
- **Finish.** Turn the visibility map into a triangulation in linear time.

The analysis chooses the granularity at each level so that the work of both phases adds up to $O(n)$. The details, with the precise definitions of conformality, fusion of submaps and the ray-shooting oracle, fill a 40-page paper.

**The last stage.** From the visibility map, every inside trapezoid has a top vertex and a bottom vertex. When the two are not adjacent on the polygon, the segment between them is a diagonal. These diagonals cut $P$ into **monotone mountains**, monotone polygons in which one of the two chains is a single edge. Every strictly convex vertex of a mountain other than the ends of that edge is an ear, so a single scan with a stack cuts off all the triangles. This is the stage the code implements, after a brute-force map:

```pseudo id=main
TRIANGULATE-FROM-VISIBILITY(P)            ▷ P simple, counterclockwise, no three vertices collinear
L1  for each vertex v do
L2      decide which horizontal rays at v start into the interior, from its two neighbors
L3      for each such ray, record the nearest edge that crosses the horizontal through v on that side
L4  read the inside trapezoids off the map: along each downward edge, consecutive chord ends bound one
L5  for each trapezoid whose top t and bottom b are not adjacent on P do add the diagonal tb
L6  for each face Q of P cut by the diagonals do         ▷ Q is a monotone mountain
        c[1 .. m] ← the vertices of Q from top to bottom; S ← empty stack
        for j ← 1 to m do
L7          push c[j]
L8          while S has three or more vertices and the corner at the second from the top is strictly convex do
                output the triangle of the top three; remove the second from the top
L9  return all triangles output for all faces
```

Lines L1 to L3 take $O(n^2)$ time here. In Chazelle's algorithm they are replaced by the linear-time construction above, which produces the same map.

## Example

Take the notched rectangle $v_0 = (0, 0)$, $v_1 = (6, 0)$, $v_2 = (6, 4)$, $v_3 = (4, 4)$, $v_4 = (3, 1)$, $v_5 = (2, 4)$, $v_6 = (0, 4)$, with doubled area 42. The chords are:

- at $v_1$, to the west, ending on $v_6 v_0$
- at $v_3$, to the east, ending on $v_1 v_2$
- at $v_4$, both ways, ending on $v_6 v_0$ and $v_1 v_2$
- at $v_6$, to the east, ending on $v_4 v_5$

That is 5 chords and 6 trapezoids. Two of them have a top and a bottom that are not adjacent, $(v_6, v_4)$ and $(v_4, v_1)$, so the diagonals are $v_4 v_6$ and $v_1 v_4$. The three faces are all mountains:

| face | top | bottom | base edge | chain from top to bottom | triangles |
|---|---|---|---|---|---|
| $v_0 v_1 v_4 v_6$ | $v_6$ | $v_0$ | $v_6 v_0$ | $v_6, v_4, v_1, v_0$ | $(v_4, v_1, v_0)$, $(v_6, v_4, v_0)$ |
| $v_1 v_2 v_3 v_4$ | $v_2$ | $v_1$ | $v_1 v_2$ | $v_2, v_3, v_4, v_1$ | $(v_2, v_3, v_4)$, $(v_2, v_4, v_1)$ |
| $v_4 v_5 v_6$ | $v_5$ | $v_4$ | $v_4 v_5$ | $v_5, v_6, v_4$ | $(v_5, v_6, v_4)$ |

In the first face the stack receives $v_6, v_4, v_1$, and the corner at $v_4$ is reflex, so nothing is cut yet. Then $v_0$ arrives. The corner at $v_1$ is convex, which cuts off $(v_4, v_1, v_0)$. Now the corner at $v_4$, between $v_6$ and $v_0$, is convex too, which cuts off $(v_6, v_4, v_0)$. The doubled areas of the five triangles are $6 + 12 + 6 + 12 + 6 = 42$.

## Correctness

The [correctness proof](proofs/correctness.md) covers the code. The ray sides and the nearest edges are correct. Reading consecutive chord ends along downward edges lists every inside trapezoid once. The main lemma is that the faces cut out by the diagonals are monotone mountains. The chords at the $m - 2$ middle vertices of a face cut it into $m - 1$ layers, each inside one trapezoid. Each layer contributes an edge of the face between two consecutive vertices in height order, either a wall or a diagonal. These edges form a path through all the vertices, so the last edge joins the top to the bottom. In a mountain every convex chain vertex is an ear, which justifies the stack loop. The correctness of Chazelle's linear-time map construction is proved in his paper.

## Complexity

Chazelle's algorithm takes $\Theta(n)$ time and space in the worst case. This is optimal, since the output has $n - 2$ triangles. The constant factors are large, and the structure is deep: several layers of submaps, oracles and point-location structures.

In the code, lines L1 to L3 take $O(n^2)$ time. The rest is linear apart from two sorts kept for simplicity: the chord ends along each edge, and the neighbors of each vertex when tracing the faces. A linked visibility map gives both orders directly. The mountain loop is linear, since each vertex is pushed once and removed at most once.

## Properties

- The algorithm is deterministic and worst-case optimal, and it uses only comparisons and orientation tests.
- It computes the full visibility map, which has uses of its own, such as point location in the polygon and ray shooting.
- With a linear-time triangulation, many problems on simple polygons become linear: testing simplicity, shortest paths between two points inside the polygon, visibility from a segment, and others that start from a triangulation.
- No simple deterministic linear-time triangulation is known. Finding one is a well-known open problem.

## Variants and improvements

- **Randomized linear time.** Amato, Goodrich and Ramos (2001) gave a randomized algorithm with expected $O(n)$ time. It uses random sampling in place of some of Chazelle's deterministic machinery. It is simpler but still far from practical.
- **Practical near-linear methods.** [Seidel's algorithm](/seidel-polygon-triangulation/) runs in expected $O(n \log^* n)$ time and is short to implement, so it is the usual choice when near-linear time matters.
- **Simplicity testing.** Run on any closed chain, the algorithm can detect a self-intersection, which gives a linear-time [simplicity test](/polygon-simplicity-test/).
- **Other last stages.** Instead of mountains, the map can be split into general [monotone pieces](/monotone-polygon-triangulation/), which are triangulated by a two-chain stack.

## When to use it

Cite Chazelle's algorithm when an $O(n)$ bound for triangulation is needed as a step in an analysis. Many results on simple polygons begin with "triangulate the polygon in linear time". Do not implement it. Use [ear clipping](/ear-clipping/) for small polygons, the [monotone partition sweep](/monotone-polygon-partition/) for a deterministic $O(n \log n)$ method, or [Seidel's algorithm](/seidel-polygon-triangulation/) for large inputs. The last stage, from a trapezoidal map to triangles through mountains, is practical and worth using whenever such a map is at hand.

## Pitfalls

- "Linear-time triangulation" in a paper usually means Chazelle's algorithm as a black box. Implementations that claim linear time almost always mean something else, such as expected time or a special class of polygons.
- The last stage needs the visibility map with its adjacencies to stay linear. Sorting the chord ends along each edge, as the code does, costs $O(n \log n)$.
- Only the chords that start into the interior belong to the map. Including outside rays changes the trapezoids.
- The mountain lemma needs every trapezoid with non-adjacent top and bottom to get its diagonal. Skipping some still gives monotone pieces in some cases, but no longer mountains, and the stack loop then fails.
- With the $(y, x)$ order, horizontal edges are slightly tilted, and the trapezoids of zero height next to them are real faces that must be kept.

## Implementations

The Python version computes the map by brute force with `visibility_map` (L1 to L3). It reads off the trapezoids and matches their left and right walls with `trapezoids` (L4), picks the diagonals with `diagonals` (L5), traces the faces, and triangulates each mountain with `triangulate_mountain` (L6 to L8). It is not Chazelle's algorithm: the up-phase, the down-phase and the submaps are not implemented.

The tests check:

- the map against an independent construction that shears the integer input by an explicit linear map and intersects each horizontal with each edge in exact rationals
- that the number of trapezoids is one more than the number of chords, and that their exact areas sum to the area of the polygon
- that every face is a monotone mountain
- that every result is a triangulation: $n - 2$ counterclockwise triangles, exact area sum, $n - 3$ diagonals, no crossings, and every diagonal midpoint strictly inside

The inputs are random simple polygons in four rotations, convex polygons, polygons with horizontal edges, large integers and `Fraction` coordinates.

## History

The $O(n \log n)$ algorithm of Garey, Johnson, Preparata and Tarjan (1978) raised the question of whether triangulation needs sorting. Chazelle and Incerpi gave an $O(n \log s)$ algorithm in 1984, where $s$ measures the winding of the boundary. In the same year Fournier and Montuno showed that triangulation and trapezoidal decomposition are equivalent in linear time. Tarjan and Van Wyk broke the $O(n \log n)$ barrier with $O(n \log \log n)$ in 1988, and Clarkson, Tarjan and Van Wyk gave a randomized $O(n \log^* n)$ bound in 1989. Chazelle presented the linear-time algorithm at FOCS 1990, and the journal version appeared in Discrete and Computational Geometry in 1991. Seidel's simple randomized algorithm appeared the same year, and Amato, Goodrich and Ramos gave a randomized linear-time algorithm in 2001.

## References
