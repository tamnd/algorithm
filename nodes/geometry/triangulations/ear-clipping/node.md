---
tag: 7DYMFT
kind: algorithm
slug: ear-clipping
name: Ear clipping
aliases:
- Meisters ear clipping
- ear clipping triangulation
- ear removal
area: geometry/triangulations
level: intro
summary: Repeatedly cut off an ear; runs in O(n^2) for a simple polygon.
solves: [polygon-triangulation]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1975
  people: [Gary H. Meisters]
  note: Meisters proved in 1975 that every simple polygon with four or more vertices has two ears, which makes repeated ear removal a correct triangulation method.
prereqs: [polygon-triangulation, ear, two-ears-theorem, orientation-test, simple-polygon]
see_also: [monotone-polygon-triangulation, seidel-polygon-triangulation, chazelle-polygon-triangulation, triangulation-dual-tree, polygon-with-holes-triangulation, art-gallery-theorem, linked-list]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.2 (diagonals, ears and Meisters' theorem) and Section 1.6, Triangulation, Implementation (ear removal in O(n^2) time)
  - paper: "Gary H. Meisters, Polygons have ears, American Mathematical Monthly 82(6), 648 to 651 (1975)"
    locator: the two ears theorem and the triangulation by repeated removal of an ear
  - paper: "Hossam ElGindy, Hazel Everett and Godfried Toussaint, Slicing an ear using prune-and-search, Pattern Recognition Letters 14(9), 719 to 722 (1993)"
    locator: finding one ear of a simple polygon in O(n) time
  - paper: "Martin Held, FIST, Fast industrial-strength triangulation of polygons, Algorithmica 30(4), 563 to 596 (2001)"
    locator: an ear clipping triangulator with a grid for the ear test and heuristics for degenerate and invalid input
  - url: https://www.geometrictools.com/Documentation/TriangulationByEarClipping.pdf
    title: David Eberly, Triangulation by Ear Clipping, Geometric Tools
    locator: Sections 2 and 3 (the ear test against reflex vertices, and the bridge to a hole)
---

Ear clipping triangulates a [simple polygon](/simple-polygon/) by cutting off one [ear](/ear/) at a time: a vertex whose two neighbors can be joined by a diagonal, so that the triangle at the vertex lies inside the polygon. Each cut removes one vertex, and after $n - 3$ cuts the last three vertices form the last triangle. It solves the [polygon triangulation](/polygon-triangulation/) problem in $\Theta(n^2)$ time with only the [orientation test](/orientation-test/), so it is exact on integer input. It is slower than the $O(n \log n)$ [monotone method](/monotone-polygon-triangulation/), but it is short, robust and easy to get right, and it is the method of many graphics libraries.

## In plain words

Walk around the polygon and look at each corner that points outward. Draw the short line that joins the two neighbors of that corner. If no other corner of the polygon lies in the small triangle that this line cuts off, the corner is an ear: the triangle is inside the polygon, and you can cut it off with scissors.

Cut it off. The rest is still a polygon, with one corner fewer. Repeat. A classic theorem says that a polygon with four or more corners always has at least two ears, so you never get stuck. When three corners are left, they form the last triangle.

The slow part is the test. To check one corner you look at every other corner, and after each cut only the two neighbors of the cut corner need a new check.

## The problem

The input is a simple polygon $P$ given by its vertex list $v_0, \ldots, v_{n-1}$, in clockwise or counterclockwise order. The vertices are distinct, and two edges meet only when they are consecutive, at their common vertex. Consecutive collinear vertices (an interior angle of exactly $\pi$) are allowed. The output is a list of $n - 2$ triangles with corners among the vertices, with disjoint interiors, whose union is $P$. Each triangle is given by three vertex indices in counterclockwise order.

Notation: $n$ is the number of vertices. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$; it is positive for a counterclockwise turn. For a vertex $v$ of the current polygon, $\mathrm{prev}(v)$ and $\mathrm{next}(v)$ are its neighbors. No general position is assumed.

## The algorithm

```pseudo id=main
EAR-CLIPPING(P)                           ▷ P = v[0 .. n − 1], simple, n ≥ 3
L1  if the signed area of P is negative then reverse P
L2  link the vertices in a circular list with prev and next
L3  for each vertex v do ear[v] ← IS-EAR(v)
L4  W ← the list of the vertices v with ear[v] = true
L5  while more than 3 vertices remain do
L6      take a vertex v from W           ▷ skip v if it is removed or ear[v] = false
L7      output the triangle (prev(v), v, next(v))
L8      remove v from the circular list
L9      for each x in {prev(v), next(v)} do ear[x] ← IS-EAR(x); if ear[x] then add x to W
L10 output the triangle of the last three vertices

IS-EAR(v)
L11 if orient(prev(v), v, next(v)) ≤ 0 then return false
L12 return true if no other remaining vertex lies in the closed triangle (prev(v), v, next(v))
```

- **Line L1** makes the order counterclockwise, so that a convex corner is a left turn. The signed area is the [shoelace formula](/shoelace-formula/).
- **Line L11** rejects reflex vertices and also vertices with an angle of exactly $\pi$: their triangle is flat.
- **Line L12** tests the closed triangle, boundary included. A vertex on the segment from $\mathrm{prev}(v)$ to $\mathrm{next}(v)$ would touch the cut, so it must block the ear. Lemma 1 of the proof shows that lines L11 and L12 together hold exactly when $v$ is an ear.
- **Line L9.** Removing an ear changes the ear status of no vertex except its two neighbors (Lemma 2). So only they are tested again. The list $W$ can hold old entries; line L6 skips them.

## Example

Take the polygon with the seven vertices $v_0 = (0,0)$, $v_1 = (6,0)$, $v_2 = (6,4)$, $v_3 = (4,4)$, $v_4 = (3,1)$, $v_5 = (2,4)$, $v_6 = (0,4)$, in counterclockwise order: a rectangle with a notch cut down from the top edge. The vertex $v_4$ is reflex: $\mathrm{orient}(v_3, v_4, v_5) = -6$. The corners $v_0$ and $v_1$ are convex, but $v_4$ lies inside their triangles, so they are not ears at the start.

| step | remaining vertices | ears | clipped triangle |
|---|---|---|---|
| 1 | $v_0 \ldots v_6$ | $v_2, v_3, v_5, v_6$ | $(v_5, v_6, v_0)$ |
| 2 | $v_0 \ldots v_5$ | $v_2, v_3, v_5$ | $(v_4, v_5, v_0)$ |
| 3 | $v_0 \ldots v_4$ | $v_0, v_2, v_3$ | $(v_4, v_0, v_1)$ |
| 4 | $v_1 \ldots v_4$ | all four | $(v_4, v_1, v_2)$ |
| end | $v_2, v_3, v_4$ | | $(v_4, v_2, v_3)$ |

The work list is a stack, so the last ear found is clipped first. After step 2 the reflex vertex $v_4$ is a neighbor of $v_0$, and the triangle $(v_4, v_0, v_1)$ is free of other vertices, so $v_0$ becomes an ear. The output has $5 = n - 2$ triangles, and their doubled areas $8 + 10 + 6 + 12 + 6 = 42$ add up to the doubled area of the polygon.

## Correctness

**Theorem.** For a simple polygon with $n \ge 3$ vertices, EAR-CLIPPING outputs $n - 2$ counterclockwise triangles with corners among the vertices, with pairwise disjoint interiors, whose union is the polygon.

The proof is in [proofs/correctness.md](proofs/correctness.md). It rests on three facts. Lemma 1: lines L11 and L12 hold exactly when the segment from $\mathrm{prev}(v)$ to $\mathrm{next}(v)$ is a diagonal, that is, when $v$ is an ear. Lemma 2: after an ear is cut, the remaining vertices form a simple polygon, and the ear status of each vertex other than the two neighbors stays the same. The [two ears theorem](/two-ears-theorem/) then says that while four or more vertices remain, some vertex is an ear, and by the loop invariant it is in $W$. So line L6 always finds an ear, and each pass of the loop that clips removes one vertex.

## Complexity

- **Ear tests.** IS-EAR costs $O(n)$: one orientation test, then one point-in-triangle test (three orientation tests) for each remaining vertex. Line L3 runs it $n$ times and line L9 runs it twice for each of the $n - 3$ clips, so there are at most $3n - 6$ calls and $O(n^2)$ time.
- **The work list.** Each entry of $W$ comes from line L4 or line L9, so $W$ receives at most $n + 2(n - 3)$ entries, and line L6 takes each at most once.
- **Total.** $O(n^2)$ time in the worst case on the [real RAM](/real-ram/), with exact integer arithmetic on integer input. The bound is tight for this algorithm: on a convex polygon each of the $n$ tests of line L3 scans all $n - 3$ other vertices, which gives $\Theta(n^2)$.
- **Space.** $\Theta(n)$ for the links, the flags and $W$.

A faster ear test does not change the worst case, but it helps a lot on typical input. When no three vertices are collinear, only reflex vertices can block an ear: if some vertex lies in the triangle of $v$, the one farthest from the segment between the neighbors of $v$ is reflex. A grid or a [kd-tree](/kd-tree/) on the reflex vertices then makes each test local. FIST uses such a grid.

## Properties

- **Exact.** All decisions are signs of degree 2 polynomials in the input coordinates. With integers or `fractions.Fraction` there is no rounding.
- **Output is not unique.** The triangulation depends on which ear is cut first. A different order of $W$ gives a different valid triangulation.
- **Deterministic.** For a fixed input order the output is fixed.
- **No Steiner points.** Every triangle corner is an input vertex.

## Variants and improvements

- **Test only reflex vertices.** With no three vertices collinear, keep the list of reflex vertices and test only them in line L12. The worst case stays $\Theta(n^2)$, and the cost becomes $O(n r)$ for $r$ reflex vertices. With collinear vertices the shortcut is wrong; see the pitfalls.
- **Prune-and-search for one ear.** ElGindy, Everett and Toussaint find one ear in $O(n)$ time by recursing on a half of the polygon cut off by a diagonal. This does not make the full triangulation faster than $O(n^2)$, because many ears are needed.
- **Best ear first.** Clip the ear with the largest smallest angle, or the shortest diagonal. This gives better-shaped triangles at no change of the worst case.
- **Polygons with holes.** Join each hole to the outer boundary by a bridge edge, which makes one weakly simple polygon, then clip ears. See [triangulation of a polygon with holes](/polygon-with-holes-triangulation/).
- **Faster algorithms.** [Monotone partition plus monotone triangulation](/monotone-polygon-triangulation/) runs in $O(n \log n)$, [Seidel's algorithm](/seidel-polygon-triangulation/) in $O(n \log^* n)$ expected time, and [Chazelle's algorithm](/chazelle-polygon-triangulation/) in $O(n)$.

## When to use it

Use ear clipping for polygons of up to a few thousand vertices, for a first implementation, and when the code must be short and exact. Font glyphs, map polygons and user-drawn shapes are typical. For large polygons with many reflex vertices use the monotone method or Seidel's algorithm. For good triangle shapes use [constrained Delaunay triangulation](/constrained-delaunay-triangulation/) or a [mesh generator](/mesh-generation/), since ear clipping makes long thin triangles.

## Pitfalls

- **An open triangle test.** Testing only the interior of the triangle in line L12 accepts an ear when a vertex lies on the segment from $\mathrm{prev}(v)$ to $\mathrm{next}(v)$. The cut then touches the boundary, and later triangles overlap or the polygon splits. The comb and collinear tests in the test file catch this.
- **Accepting flat corners.** With `orient(...) < 0` instead of `≤ 0` in line L11, a vertex with an angle of $\pi$ is clipped as a triangle of zero area, and the count $n - 2$ fails.
- **The wrong orientation.** On a clockwise polygon, without line L1, every convex corner looks reflex and the loop finds no ear.
- **Updating only one neighbor.** Both neighbors of the cut vertex change their triangle, so both must be tested again. A stale flag of `true` can clip a non-ear.
- **Testing only reflex vertices on degenerate input.** The polygon $(0,0), (1,0), (2,0), (1,2)$ has no reflex vertex. A reflex-only test calls $(1,2)$ an ear, but the vertex $(1,0)$ lies on the segment between its neighbors, and the last three vertices are collinear. Line L12 tests all vertices, so it rejects this cut.
- **Floating-point orientation.** A near-collinear corner can get the wrong sign, and the output can then hold crossing triangles. Use exact arithmetic, or an exact predicate such as Shewchuk's adaptive test, never a tolerance.

## Implementations

The Python version keeps the circular list in two dictionaries and the work list as a stack. The tests check every output against a brute-force validator: $n - 2$ distinct non-degenerate triangles, the sum of their doubled areas equal to the doubled area of the polygon, no two edges meeting except at a common endpoint, no vertex inside a triangle, and every diagonal strictly inside the polygon. Random simple polygons are grown on small integer grids, which makes many collinear vertices.

## History

Gary Meisters proved in 1975 that every simple polygon with at least four vertices has two non-overlapping ears, and he noted that cutting ears one at a time triangulates the polygon. O'Rourke's book gives the $O(n^2)$ implementation that updates only the two neighbors of the cut vertex. ElGindy, Everett and Toussaint found one ear in linear time in 1993. Held's FIST (2001) made ear clipping robust on large and faulty industrial data.

## References
