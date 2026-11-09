---
tag: 024GPG
kind: algorithm
slug: lawson-flip-algorithm
name: Lawson's flip algorithm
aliases:
- Lawson edge flipping
- Lawson flip algorithm
- Lawson local optimisation
- edge-flipping algorithm
- flip algorithm for Delaunay triangulation
area: geometry/voronoi-and-delaunay
level: core
summary: Repeatedly flip non-locally-Delaunay edges; the result is the Delaunay triangulation.
solves: [delaunay-triangulation-construction]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {worst: O(n^2)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1977
  people: [Charles L. Lawson]
  note: Lawson used edge flips to optimise triangulations for surface interpolation; Sibson showed in 1978 that the local optimum is the Delaunay triangulation.
prereqs: [delaunay-triangulation, edge-flip, in-circle-test, triangulation-of-point-set]
see_also: [local-delaunay-criterion, paraboloid-lifting-map, delaunay-max-min-angle, flip-graph, bowyer-watson-algorithm, guibas-stolfi-algorithm, constrained-delaunay-triangulation, max-min-angle-triangulation]
sources:
  - paper: "C. L. Lawson, Software for C1 surface interpolation, in J. R. Rice (editor), Mathematical Software III, Academic Press, 1977"
    locator: the local optimisation procedure that swaps the diagonal of convex quadrilaterals until no swap improves the triangulation
  - paper: doi:10.1093/comjnl/21.3.243
    title: R. Sibson, Locally equiangular triangulations, The Computer Journal 21(3), 1978
    locator: the proof that a triangulation that is locally optimal at every edge is the Delaunay triangulation
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 9.1 (legal edges, edge flips and the algorithm that flips illegal edges until none is left)
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 2 (the flip algorithm, the Delaunay lemma and the bound of n(n - 1)/2 flips by the lifting map)
---

Lawson's flip algorithm turns any triangulation of a point set into a [Delaunay triangulation](/delaunay-triangulation/). It looks at each interior edge and the two triangles beside it. If the far corner of one triangle is strictly inside the circumcircle of the other, the edge is *not locally Delaunay*, and the algorithm replaces it by the other diagonal of the quadrilateral, an [edge flip](/edge-flip/). When no such edge is left, the triangulation is Delaunay. At most $n(n - 1)/2$ flips happen, so the worst-case time is $O(n^2)$, and on some inputs a quadratic number of flips is observed.

## In plain words

Start with any way to cut the region inside the points into triangles. Two triangles that share an edge make a four-sided shape. If the shape is convex, it has two diagonals, and we can swap one for the other.

Look at the circle through the three corners of one triangle. If the far corner of its neighbour is inside that circle, the triangles are thin in a bad way, and swapping the diagonal makes them fatter. Keep a list of edges to look at. Each swap can spoil the four outer sides of the shape, so put them back on the list.

When the list is empty, every edge is good. A local check then gives a global fact: no point is inside the circle of any triangle.

## The problem

The input is a finite list $P$ of points $p = (x, y)$ with integer coordinates; repeats are allowed. The output is the list of triangles of a Delaunay triangulation of the distinct points of $P$, each a counterclockwise triple, or the empty list if all points lie on one line.

Notation: $n$ is the number of distinct points and $h$ the number of points on the boundary of their convex hull. $\mathrm{orient}(a, b, c)$ is the sign of $(b - a) \times (c - a)$, positive for a counterclockwise turn. For counterclockwise $a, b, c$, $\mathrm{incircle}(a, b, c, d)$ is positive when $d$ is strictly inside the circle through $a, b, c$, zero on it and negative outside; it is the sign of a $3 \times 3$ determinant of integers, as on the [in-circle test page](/in-circle-test/). An interior edge $ab$ with triangles $abc$ and $bad$ is *locally Delaunay* when $\mathrm{incircle}(a, b, c, d) \le 0$. No general position is assumed: with four or more points on one circle the algorithm returns one of the Delaunay triangulations.

## The algorithm

```pseudo id=main
LAWSON(P)
L1  T ← a triangulation of the distinct points of P that uses all of them
L2  put every interior edge of T on a stack
L3  while the stack is not empty do
L4      pop an edge ab; skip it if it is not an interior edge of T now
        let abc and bad be its two triangles, with abc counterclockwise
L5      if incircle(a, b, c, d) > 0 then
L6          flip: replace abc and bad by adc and dbc
L7          push each of ad, db, bc, ca that is not on the stack
L8  return the triangles of T
```

- **Line L1.** Any triangulation works. The code sorts the points by $(x, y)$ and adds them one by one; each new point is outside the hull so far, and it is joined to every hull edge that it sees. This takes $O(n \log n)$ time.
- **Line L4.** An edge on the stack can be flipped away while it waits, and edges pushed by line L7 can be hull edges. Both are skipped.
- **Line L5.** The test is strict, so an edge whose four points lie on one circle is not flipped. This is what makes the algorithm stop on cocircular points.
- **Line L6.** When the test is positive, the quadrilateral $a, d, b, c$ is strictly convex, so the flip is always possible. The new edge $cd$ is locally Delaunay at once.
- **Line L7.** Only the four outer sides of the quadrilateral have new triangles beside them, so only they can have become bad.

## Example

Take the six points $(1,2)$, $(0,6)$, $(2,0)$, $(8,5)$, $(8,1)$ and $(4,0)$. They are in convex position, so $h = 6$ and every triangulation has $2n - 2 - h = 4$ triangles. Line L1 gives the fan from $(0,6)$: the triangles $(0,6)(1,2)(2,0)$, $(0,6)(2,0)(4,0)$, $(0,6)(4,0)(8,1)$ and $(0,6)(8,1)(8,5)$.

1. Edge $(0,6)$-$(8,1)$: the circle through $(0,6), (8,1), (8,5)$ has center $(59/16, 3)$, and $(4,0)$ is strictly inside it. Flip to $(4,0)$-$(8,5)$.
2. Edge $(0,6)$-$(4,0)$: $(2,0)$ is outside the circle through $(0,6), (4,0), (8,5)$. No flip.
3. Edge $(0,6)$-$(2,0)$: $(1,2)$ is strictly inside the circle through $(0,6), (2,0), (4,0)$. Flip to $(1,2)$-$(4,0)$. The flip pushes $(0,6)$-$(4,0)$ again.
4. Edge $(0,6)$-$(4,0)$: now its triangles are $(0,6)(1,2)(4,0)$ and $(0,6)(4,0)(8,5)$, and $(1,2)$ is strictly inside the circle through $(0,6), (4,0), (8,5)$. Flip to $(1,2)$-$(8,5)$.
5. Edges $(4,0)$-$(8,5)$ and $(1,2)$-$(4,0)$ pass the test, and the other popped edges are hull edges.

The result is $(0,6)(1,2)(8,5)$, $(1,2)(2,0)(4,0)$, $(1,2)(4,0)(8,5)$ and $(4,0)(8,1)(8,5)$, after $3$ flips and $6$ in-circle tests. Step 4 flips an edge that passed the test in step 2, because the flip of step 3 changed one of its triangles.

## Correctness

**Theorem.** For $n$ points not all on one line and any start triangulation that uses all of them, LAWSON makes at most $n(n - 1)/2$ flips and returns a triangulation in which no point lies strictly inside the circumcircle of a triangle. No general position is needed; if no four points lie on one circle, the result is the unique Delaunay triangulation.

The proof uses the [lifting map](/paraboloid-lifting-map/) $p \mapsto (p_x, p_y, |p|^2)$. A triangulation lifts to a surface of triangles over the hull. A point is strictly inside the circumcircle of a triangle exactly when its lift is strictly below the plane of the lifted triangle. A flip of a bad edge replaces a part of the surface by a lower one, strictly lower along the old edge, so the surface only goes down. An edge that has been flipped away can then never come back, which bounds the number of flips. When every edge is locally Delaunay, the surface is convex, so every lifted point is on or above the plane of every lifted triangle; this is the [local Delaunay criterion](/local-delaunay-criterion/). The stack keeps the invariant that every bad edge is on it. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Worst case.** $O(n \log n)$ for the start, and at most $n(n - 1)/2$ flips, each with $O(1)$ work and at most $4$ pushes, so $O(n^2)$ time in the worst case. Proved in [the complexity proof](proofs/complexity/).
- **The bound is reached.** For $m$ points on $y = x^2$ and $m$ points on $y = 10^7 - x^2$, with $x = 0, \ldots, m - 1$, the code makes $m(m - 2)$ flips for $m = 50, 100, 200, 400$. This is observed on these inputs, not proved for all $m$.
- **Random points.** On $n$ uniform random integer points the code makes about $2.6n$, $3.5n$, $4.1n$ and $5.0n$ flips for $n = 100, 200, 400, 800$. This is observed only.
- **Space.** $O(n)$: each edge is on the stack at most once at a time.

## Properties

- **Exact.** Both predicates are signs of integer polynomials.
- **Any start.** The result does not need a special start, only a triangulation that uses all points.
- **Monotone.** Every flip lowers the lifted surface and, in the plane, raises the sorted vector of angles, by the [max-min angle property](/delaunay-max-min-angle/).
- **Not unique on cocircular points.** On a grid the result depends on the start and on the stack order; all such results are Delaunay.

## Variants and improvements

- **Incremental insertion with flips.** Insert the points one by one into a Delaunay triangulation, split the triangle that holds the new point, and flip only around the new point. In random order this takes $O(n \log n)$ expected time; see [Bowyer-Watson](/bowyer-watson-algorithm/) and [Delaunay construction](/delaunay-triangulation-construction/).
- **Constrained edges.** Never flip a constrained edge, and the result is the [constrained Delaunay triangulation](/constrained-delaunay-triangulation/).
- **Weighted points.** With the power function in place of the in-circle test, flips give the [regular triangulation](/regular-triangulation/) when it uses all points; otherwise flips that remove a point are also needed.
- **Higher dimensions.** In three dimensions, flips can get stuck before the Delaunay tetrahedralization is reached, so the two-dimensional argument does not carry over; see [higher-dimensional Delaunay](/higher-dimensional-delaunay/).

## When to use it

Use it to repair a triangulation that is almost Delaunay, for example after points moved a little, or after a mesh step changed a few triangles, where only a few flips are needed. It is also the simplest correct method to write. For a fresh set of points in the worst case, an $O(n \log n)$ method such as [Guibas-Stolfi](/guibas-stolfi-algorithm/) or randomized incremental insertion is faster.

## Pitfalls

- **Non-strict test in line L5.** Flipping when $\mathrm{incircle} = 0$ can flip the same edge back and forth forever on four cocircular points.
- **Testing a stale edge in line L4.** An edge on the stack may already have been flipped away. Check that it still has two triangles before the test.
- **Checking convexity separately in line L6.** It is not needed: a positive in-circle test already proves that the quadrilateral is strictly convex. Code that skips a flip on a failed convexity test, because of rounding, can stop with a bad edge.
- **Forgetting an outer side in line L7.** All four sides of the quadrilateral need a new test. Pushing only two can leave a bad edge.
- **A start that misses some points in line L1.** The theorem needs every point as a vertex. A point left out is never added by flips.
- **Floating-point in-circle tests.** On nearly cocircular points a rounded test can flip in a cycle. Use exact integers, as here, or an adaptive exact predicate.

## Implementations

## History

Charles Lawson studied triangulations for the interpolation of surfaces. In 1972 he showed that any two triangulations of the same point set are joined by a sequence of edge flips, and in 1977 he proposed to flip the diagonal of convex quadrilaterals to make the smallest angle larger until no flip helps. Robin Sibson proved in 1978 that a triangulation that is optimal in this local sense at every edge is the Delaunay triangulation. The lifting-map view of flips, with the bound of $n(n - 1)/2$ flips, became the standard proof in the later textbooks. Flipping is also the core of the incremental methods, and of the randomized analysis of Guibas, Knuth and Sharir.

## References
