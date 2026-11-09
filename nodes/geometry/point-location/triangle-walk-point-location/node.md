---
tag: 47K91B
kind: algorithm
slug: triangle-walk-point-location
name: Triangle walk point location
aliases:
- walking point location
- straight walk in a triangulation
- visibility walk
- stochastic walk
- Lawson's oriented walk
area: geometry/point-location
level: advanced
summary: Locate a point in a triangulation by walking from triangle to triangle toward the query point.
solves: [planar-point-location]
model: real-ram
complexity:
  vars: {n: the number of vertices of the triangulation}
  time: {build: O(n) worst case, query: O(n) worst case}
  space: {extra: O(n) worst case}
properties: {online: true, deterministic: true, recursive: false, static: false}
history:
  year: 1977
  people: [Charles L. Lawson, Peter J. Green, Robin Sibson, Olivier Devillers, Sylvain Pion, Monique Teillaud]
  note: Walks were used to locate points in triangulations for surface interpolation and Delaunay construction from the late 1970s, by Lawson and by Green and Sibson. Devillers, Pion and Teillaud compared the straight, visibility and stochastic walks and their termination in 2002.
prereqs: [triangulation, orientation-test, delaunay-triangulation, in-circle-test, planar-point-location]
see_also: [kirkpatrick-point-location, lawson-flip-algorithm, local-delaunay-criterion, paraboloid-lifting-map, regular-triangulation, delaunay-triangulation-construction, trapezoidal-map, markov-chain]
sources:
  - paper: doi:10.1142/S0129054102001047
    title: Olivier Devillers, Sylvain Pion and Monique Teillaud, Walking in a triangulation, International Journal of Foundations of Computer Science 13(2), 2002
    locator: Sections 2 and 3, the straight, visibility and stochastic walks and their termination (DOI to be checked)
  - paper: doi:10.1007/BF02122779
    title: Herbert Edelsbrunner, An acyclicity theorem for cell complexes in d dimensions, Combinatorica 10(3), 1990
    locator: the in-front relation of a regular triangulation is acyclic, and a non-regular triangulation can have a cycle (DOI to be checked)
  - paper: doi:10.1016/j.comgeo.2004.02.002
    title: Luc Devroye, Christophe Lemaire and Jean-Michel Moreau, Expected time analysis for Delaunay point location, Computational Geometry 29(2), 2004
    locator: the expected cost of the straight walk in a random Delaunay triangulation (DOI to be checked)
---

A walk answers [planar point location](/planar-point-location/) in a [triangulation](/triangulation/) with no extra structure. It starts at some triangle and moves to a neighbor across an edge that separates the current triangle from the query point $q$, until the current triangle contains $q$. The *straight walk* crosses the edges met by the segment from a start point to $q$, and always ends. The *visibility walk* crosses any edge whose line separates the triangle from $q$: it always ends in a [Delaunay triangulation](/delaunay-triangulation/), but in other triangulations it can loop forever. The *stochastic walk* picks the first edge to test at random, and ends with probability $1$ in every triangulation. A walk costs $O(n)$ steps in the worst case and needs only the neighbor pointers that most triangulation codes keep anyway.

## In plain words

Imagine a floor covered by triangular tiles and a target spot somewhere on it. You stand on one tile and want to reach the tile under the target. Look at the three sides of your tile. If the target lies beyond one of the sides, step over that side onto the next tile, and look again. When the target is beyond none of the sides, you are on the right tile.

When two sides face the target, you must choose. You can follow a straight string stretched from your start to the target, which always works. You can take the first good side in a fixed order, which is simple but can send you around in a circle when the tiles are long and thin. Or you can pick the first side to look at by tossing a coin, which gets you out of every circle sooner or later.

## The problem

**Notation.** $n$ is the number of vertices of the triangulation and $T \le 2n - 5$ its number of triangles. $q$ is the query point, $t$ the current triangle with counterclockwise corners, and $s$ the centroid of the start triangle. $\mathrm{orient}(a, b, c)$ is the sign of $(b_x - a_x)(c_y - a_y) - (b_y - a_y)(c_x - a_x)$: positive when $a, b, c$ turn counterclockwise. An edge $ab$ of $t$, in counterclockwise order, *faces* $q$ if $\mathrm{orient}(a, b, q) < 0$, so the line of $ab$ strictly separates $q$ from the interior of $t$. $\mathrm{incircle}(a, b, c, d) > 0$ means that $d$ lies strictly inside the circle through the counterclockwise triangle $abc$. Costs are on the [real RAM](/real-ram/).

The input is a set of triangles with integer or rational corners that tile a convex region edge to edge: two triangles meet in a common edge, a common vertex, or not at all. The neighbor across each edge is known; the code finds it in a table indexed by the directed edge. A query point $q$ and a start triangle get one of four answers: the vertex $q$, the edge whose relative interior contains $q$, the triangle whose interior contains $q$, or "outside". The answer depends only on $q$, not on the walk or the start.

**Degenerate input.** Vertical edges and equal $x$-coordinates play no role, since no step uses a vertical direction. The straight walk needs care when the line from $s$ to $q$ passes through a vertex. Its side function treats a vertex on the directed line $sq$ as lying to its left. This is a symbolic perturbation: it is the same as moving the line, with both its end points, an infinitely small distance to the right, so the moved segment passes through no vertex and the walk is well defined. A query point on an edge or a vertex is in several closed triangles; every walk stops at the first closed triangle that contains $q$, and the vertex or edge answer is the same from each of them.

## The algorithm

```pseudo id=main
STRAIGHT-WALK(q, t)
L1  if q is in the closed triangle t then return the answer for q in t
L2  s ← the centroid of t; (u, w) ← the edge of t with u right of the line sq and w left of it
L3  loop
L4      t ← the neighbor across (u, w); if there is none then return "outside"
L5      if q is in the closed triangle t then return the answer for q in t
L6      v ← the third corner of t; if v is left of sq then (u, w) ← (u, v) else (u, w) ← (v, w)
VISIBILITY-WALK(q, t)
L7  loop
L8      k₀ ← 0, or a random edge for the stochastic walk; test the edges of t in the order k₀, k₀ + 1, k₀ + 2 and stop at the first one that faces q; if none faces q then return the answer for q in t
L9      t ← the neighbor across that edge; if there is none then return "outside"
```

- **Line L2.** "Left" means $\mathrm{orient}(s, q, p) \ge 0$ and "right" means $\mathrm{orient}(s, q, p) < 0$. Since $s$ is inside $t$, the corners are not all on one side, and going counterclockwise around $t$ the side changes from right to left at exactly one edge. That edge is where the ray from $s$ toward $q$ leaves $t$. The code works with $3s$ and $3q$, so the centroid is an integer point.
- **Lines L4 to L6.** The segment enters the new triangle $t = (w, u, v)$ through the edge $wu$, with $u$ on the right and $w$ on the left. It leaves through the edge whose ends are on opposite sides: $uv$ if $v$ is on the left, $vw$ if $v$ is on the right. If there is no neighbor, the segment leaves the convex region before reaching $q$, so $q$ is outside.
- **Line L8.** The deterministic walk always starts the test at the stored first edge. The stochastic walk draws $k_0$ uniformly from $\{0, 1, 2\}$ at every triangle, so each edge that faces $q$ is tested first with probability at least $1/3$. The *remembering* variant skips the edge it just crossed, which never faces $q$, and saves one test per step.
- **Line L9.** An edge on the boundary of a convex region that faces $q$ proves that $q$ is outside.

The code also gives the Lawson flip algorithm, which makes a triangulation Delaunay by flipping edges that fail the [in-circle test](/in-circle-test/), and records the path of each walk.

## Example

The *pinwheel* has six vertices: the outer corners $(0,0)$, $(14,0)$, $(0,14)$ and the inner points $(7,1)$, $(12,1)$, $(5,7)$. It has seven triangles, with the first corner as stored.

| triangle | corners | edges that face $q = (9, 2)$, in stored order |
|---|---|---|
| 0 | $(12,1), (5,7), (7,1)$ | none: it contains $q$ |
| 1 | $(0,14), (5,7), (14,0)$ | to 2 |
| 2 | $(12,1), (14,0), (5,7)$ | to 3, to 0 |
| 3 | $(14,0), (12,1), (0,0)$ | to 4 |
| 4 | $(7,1), (0,0), (12,1)$ | to 5, to 0 |
| 5 | $(0,0), (7,1), (0,14)$ | to 6 |
| 6 | $(5,7), (0,14), (7,1)$ | to 1, to 0 |

**The visibility walk loops.** From triangle 1, the deterministic walk takes the first facing edge each time and goes $1, 2, 3, 4, 5, 6, 1, \ldots$ around the central triangle forever. In each step, $q$ lies strictly beyond the edge crossed, so, seen from $q$, each triangle of the ring lies in front of the one before it, and this in-front relation has a cycle. The edges $(0,0)(12,1)$ and $(7,1)(0,14)$ are not locally Delaunay, so this is not a Delaunay triangulation. The stochastic walk leaves the ring at triangle 2, 4 or 6 with probability $2/3$ each time. After Lawson flips, the visibility walk from every start triangle ends in triangle 0.

**A straight walk.** From triangle 1, with centroid $s = (19/3, 7)$, to $q = (2, 2)$. The line $sq$ has $(0,14)$, $(5,7)$ and $(0,0)$ on its right and $(14,0)$, $(12,1)$, $(7,1)$ on its left.

| step | triangle | edge crossed (right end, left end) | third corner and its side |
|---|---|---|---|
| 1 | 1 | $(5,7), (14,0)$ | |
| 2 | 2 | $(5,7), (12,1)$ | $(12,1)$, left |
| 3 | 0 | $(5,7), (7,1)$ | $(7,1)$, left |
| 4 | 6 | $(0,14), (7,1)$ | $(0,14)$, right |
| 5 | 5 | contains $q$ | |

The walk returns triangle 5 after 4 steps. The query $(10, 1)$ from triangle 1 returns the edge from $(7,1)$ to $(12,1)$, and $(20, 3)$ from triangle 5 returns "outside".

## Correctness

**Theorem.** (1) The straight walk ends after at most $T$ steps and returns the correct answer. (2) Whenever the visibility walk ends, its answer is correct. (3) In a triangulation in which every interior edge is locally Delaunay, the visibility walk, with any rule for choosing among the facing edges, never visits a triangle twice, so it ends after at most $T$ steps. (4) In every triangulation, the stochastic walk ends with probability $1$. (5) In the pinwheel, the deterministic visibility walk from triangle 1 to $(9,2)$ does not end.

Part (1) holds because a segment meets a triangle in one interval, so the moved segment enters each triangle at most once. Part (3) is Edelsbrunner's acyclicity argument for the Delaunay case: across each step, the power of $q$ with respect to the circumcircle of the current triangle never grows, and it stays equal only between triangles with one common circle, whose adjacency graph has no cycle. Part (4) uses part (1): from any triangle, the straight walk from a suitable point gives a path of at most $T$ visibility steps to the answer, and the stochastic walk follows it with probability at least $3^{-T}$. Cocircular points, as in a grid of squares, are covered by part (3). The full proofs are in [the correctness proof](proofs/correctness/).

## Complexity

- **Build time.** The neighbor table has one entry per directed edge, so it is built in $O(n)$ time in the worst case, with $O(n)$ space. Codes that store a triangulation usually keep these pointers anyway, and then there is nothing to build.
- **Query time.** The straight walk takes at most $T = O(n)$ steps of $O(1)$ orientation tests, and the visibility walk in a Delaunay triangulation also takes at most $T$ steps, so a query takes $O(n)$ time in the worst case. The bound is tight: in a strip of $\Theta(n)$ thin triangles side by side, a query at one end from the other end crosses all of them.
- **Stochastic walk.** The proof gives only the bound $T \cdot 3^{T}$ on the expected number of steps in an arbitrary triangulation. In a Delaunay triangulation it never takes more than $T$ steps.
- **Random points.** For $n$ points uniform in a convex region, the straight walk in the Delaunay triangulation between two fixed points crosses $O(\sqrt{n})$ triangles in expectation (Devroye, Lemaire and Moreau).

The full proofs are in [the complexity proof](proofs/complexity/). In the [algebraic decision tree](/algebraic-decision-tree/) model every method needs $\Omega(\log n)$ tests; the walk does not reach this, but it needs no preprocessing.

## Properties

- **No preprocessing.** The walk uses the triangulation as it is. It works on a triangulation that changes, which is why incremental [Delaunay construction](/delaunay-triangulation-construction/) uses it to find the triangle of each new point.
- **Local.** If the start triangle is close to $q$, the walk is short. A good start, such as the answer of the previous query, often makes it much faster than its worst case.
- **Exact.** All tests are orientation tests on integers or `fractions.Fraction`. The in-circle test is used only to build Delaunay triangulations.
- **Online.** Queries are answered one at a time, in any order, and the triangulation can be edited between them.

## Variants and improvements

- **Remembering walk.** Do not test the edge just crossed. It saves one orientation test per step, and Devillers, Pion and Teillaud show that the remembering stochastic walk also ends with probability $1$.
- **Jump and walk.** Sample about $n^{1/3}$ vertices, start from the one nearest to $q$, and walk. For random points in the plane this costs $O(n^{1/3})$ expected time (Mücke, Saias and Zhu, 1999).
- **Delaunay hierarchy.** Devillers keeps a sequence of Delaunay triangulations of random samples and walks in each from the answer of the coarser one, which gives $O(\log n)$ expected query time. It is close in spirit to [Kirkpatrick's hierarchy](/kirkpatrick-point-location/).
- **Higher dimensions.** The same walks work in tetrahedralizations, and the acyclicity of the Delaunay case holds in every dimension, since it holds for all [regular triangulations](/regular-triangulation/).

## When to use it

Use a walk when a triangulation is already stored with neighbor pointers, when it changes between queries, or when queries come in a stream of nearby points, as in incremental Delaunay construction, mesh interpolation and particle tracking in meshes. Use the visibility walk only in Delaunay triangulations, or switch to the stochastic or straight walk. For many queries on a fixed large map, a structure with $O(\log n)$ queries, such as the [trapezoidal map](/trapezoidal-map/), is faster.

## Pitfalls

- **Visibility walk in a general triangulation.** A fixed choice among facing edges can loop forever, as in the pinwheel. Use a random choice or the straight walk, or cap the number of steps.
- **Vertices on the walk line.** In the straight walk, a vertex exactly on the line through $s$ and $q$ makes the exit edge ambiguous. Break ties in one fixed direction, as line L2 does, and never with a floating-point tolerance.
- **Nonconvex regions.** A walk can leave a nonconvex region through a boundary edge while $q$ is inside, behind a notch. Walk in a triangulation of the convex hull, or of a large enclosing triangle.
- **Open tests.** A query on an edge is in no open triangle. Stop at the first closed triangle that contains $q$.
- **Rounding in the orientation test.** A floating-point orientation test can say that $q$ faces two opposite edges of neighboring triangles, and the walk then cycles between them. Use exact or filtered exact predicates.

## Implementations

## History

Walks are as old as computer triangulations. Lawson used one in 1977 in his work on surface interpolation over triangulations, and Green and Sibson walked through the Delaunay triangulation in 1978 to insert points into it. Edelsbrunner proved in 1990 that the in-front relation of a regular triangulation, and so of a Delaunay triangulation, is acyclic, and that other triangulations can have cycles, which is why the visibility walk ends for Delaunay and can loop elsewhere. In 2002, Devillers, Pion and Teillaud compared the straight, visibility and stochastic walks, proved that the stochastic walk always ends with probability $1$, and measured them in the CGAL library. Devroye, Lemaire and Moreau analyzed the straight walk in random Delaunay triangulations in 2004.

## References
