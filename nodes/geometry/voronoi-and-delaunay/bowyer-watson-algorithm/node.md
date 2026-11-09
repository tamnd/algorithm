---
tag: QVMB6E
kind: algorithm
slug: bowyer-watson-algorithm
name: Bowyer-Watson algorithm
aliases:
- Watson's algorithm
- Bowyer's algorithm
- cavity insertion
area: geometry/voronoi-and-delaunay
level: core
summary: Incremental Delaunay construction that re-triangulates the cavity of triangles whose circumcircle holds the new point.
solves: [delaunay-triangulation-construction]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1981
  people: [Adrian Bowyer, David F. Watson]
  note: Bowyer and Watson published the cavity method independently, in two papers in the same issue of The Computer Journal in 1981.
prereqs: [delaunay-triangulation, in-circle-test, empty-circle-property, orientation-test]
see_also: [lawson-flip-algorithm, delaunay-triangulation-construction, randomized-incremental-construction, guibas-stolfi-algorithm, fortunes-algorithm, local-delaunay-criterion, regular-triangulation, delaunay-refinement]
sources:
  - paper: doi:10.1093/comjnl/24.2.162
    title: A. Bowyer, Computing Dirichlet tessellations, The Computer Journal 24(2), 1981
    locator: the whole paper (insertion of a point by deletion of the simplices whose circumsphere holds it, in any dimension)
  - paper: doi:10.1093/comjnl/24.2.167
    title: D. F. Watson, Computing the n-dimensional Delaunay tessellation with application to Voronoi polytopes, The Computer Journal 24(2), 1981
    locator: the whole paper (the same cavity method for Delaunay simplices in d dimensions)
  - paper: doi:10.1007/BF01758770
    title: L. J. Guibas, D. E. Knuth and M. Sharir, Randomized incremental construction of Delaunay and Voronoi diagrams, Algorithmica 7, 1992
    locator: the expected O(n) structural change for a random insertion order and the history DAG for point location
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 3 (the Bowyer-Watson algorithm with ghost triangles and its correctness)
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Sections 9.3 and 9.4 (randomized incremental Delaunay and its analysis by backwards analysis)
---

The Bowyer-Watson algorithm builds the [Delaunay triangulation](/delaunay-triangulation/) of a point set by inserting the points one at a time. To insert a point $p$, it removes every triangle whose circumcircle holds $p$ strictly inside, which leaves a hole called the **cavity**, and joins $p$ to every edge on the border of the cavity. It uses only the [orientation test](/orientation-test/) and the [in-circle test](/in-circle-test/), so it is exact on integer input. The method works the same way in any dimension. The total number of structural changes is $\Theta(n^2)$ in the worst case and $O(n)$ expected for a random insertion order.

## In plain words

Start with one triangle. To add a new point, look for all triangles whose circle through their three corners has the new point inside. These triangles are now bad, because a good triangle must have an empty circle.

The bad triangles always form one connected hole around the new point, and from the new point you can see every edge of the hole's border. So remove the bad triangles and draw a line from the new point to each corner of the hole. The new triangles have empty circles, and the triangles you did not touch are still good.

Outside the current shape there are extra pretend triangles with one corner far away. They let a point outside the shape use the same steps as a point inside it.

## The problem

The input is a finite list $P$ of points $p = (x, y)$ with integer coordinates; repeats are allowed. The output is a [triangulation](/triangulation-of-point-set/) $T$ of the distinct points of $P$ in which no point lies strictly inside the circumcircle of a triangle: the [empty circle property](/empty-circle-property/). Each triangle is a counterclockwise triple of points. If all points lie on one line, or there are fewer than three distinct points, there is no triangle and the output is empty.

Notation: $n = |P|$, $h$ is the number of convex hull vertices, $\mathrm{orient}(a, b, c)$ is the sign of $(b - a) \times (c - a)$ (positive for a counterclockwise turn), and for counterclockwise $a, b, c$, $\mathrm{incircle}(a, b, c, d)$ is positive when $d$ is strictly inside the circle through $a, b, c$, zero on it and negative outside. General position is not assumed. With four or more cocircular points the Delaunay triangulation is not unique, and the algorithm returns one of them; see [uniqueness](/delaunay-triangulation-uniqueness/).

**Ghost triangles.** For each counterclockwise hull edge $v \to u$ the structure holds a ghost triangle $(u, v, G)$, where $G$ is a symbolic vertex at infinity. The ghost $(u, v, G)$ is in conflict with $p$ when $\mathrm{orient}(u, v, p) > 0$ (so $p$ is strictly outside the hull edge), or when $\mathrm{orient}(u, v, p) = 0$ and $p$ is strictly inside the segment $uv$. A real triangle $t$ is in conflict with $p$ when $p$ is strictly inside its circumcircle. With ghosts, every triangle has three neighbours, and a point outside the hull needs no special case.

## The algorithm

```pseudo id=main
BOWYER-WATSON(P)
L1  S ← the distinct points of P, in the given order
L2  if all points of S lie on one line then return the empty list
L3  T ← a counterclockwise triangle abc of S and its three ghost triangles
L4  for each other point p of S, in order do
L5      t0 ← a triangle of T in conflict with p
L6      C ← all triangles reached from t0 through neighbours in conflict with p
L7      B ← the edges xy of triangles in C whose neighbour across xy is not in C
L8      remove the triangles of C from T
L9      for each edge xy of B do add the triangle (x, y, p) to T
L10 return the real (non-ghost) triangles of T
```

- **Line L1** removes duplicates. A copy of an inserted point would lie on circles but strictly inside none, so it would have no cavity.
- **Line L2.** Collinear input has no triangle. The code finds the first point that is not on the line of the first two points.
- **Line L3** sets up the first triangle and one ghost on each of its three edges.
- **Line L5** finds one conflict triangle. The code scans all triangles. Point location with a walk ([triangle walk](/triangle-walk-point-location/)) or with the history DAG of the [Delaunay triangulation](/delaunay-triangulation/) page makes this step fast.
- **Line L6** is a graph search over the triangles, with an explicit stack. It only follows neighbours in conflict; the correctness proof shows that this reaches every conflict triangle.
- **Line L7.** Each edge of the cavity border is kept with the orientation it has in its cavity triangle. One of its ends can be the ghost vertex $G$.
- **Lines L8 and L9** replace the cavity by the fan of triangles from $p$. A new triangle $(x, G, p)$ is a new ghost, stored as $(p, x, G)$.

## Example

Insert the six points $(0,0), (6,0), (3,5), (3,2), (6,4), (0,4)$ in this order. Line L3 makes the triangle $(0,0), (6,0), (3,5)$ and three ghosts.

| new point | cavity C | border edges | triangles after |
| --- | --- | --- | --- |
| (3,2) | the triangle (0,0) (6,0) (3,5) | its 3 edges | 3 real, 3 ghosts |
| (6,4) | triangle (6,0) (3,5) (3,2) and the ghost on edge (6,0) (3,5) | (6,0)-G, G-(3,5), (3,5)-(3,2), (3,2)-(6,0) | 4 real, 4 ghosts |
| (0,4) | triangle (3,5) (0,0) (3,2) and the ghost on edge (3,5) (0,0) | (3,5)-G, G-(0,0), (0,0)-(3,2), (3,2)-(3,5) | 5 real, 5 ghosts |

The point $(3,2)$ is strictly inside the circle through $(0,0), (6,0), (3,5)$, which has center $(3, 8/5)$ and squared radius $289/25$. The point $(6,4)$ is outside the circle through $(0,0), (6,0), (3,2)$ (center $(3, -5/4)$, squared radius $169/16$), so that triangle stays. Line L10 returns the five triangles

$$(0,0)(6,0)(3,2),\quad (3,2)(6,0)(6,4),\quad (3,5)(3,2)(6,4),\quad (3,2)(3,5)(0,4),\quad (0,0)(3,2)(0,4).$$

There are $h = 5$ hull vertices, and $2n - 2 - h = 5$ triangles, as [Euler's formula](/euler-formula/) requires.

## Correctness

**Theorem.** For every finite list $P$ of points with integer coordinates, BOWYER-WATSON returns a Delaunay triangulation of the distinct points of $P$, or the empty list when they lie on one line.

The proof keeps the invariant that $T$ is a Delaunay triangulation of the inserted points together with one ghost on each hull edge. Use the [paraboloid lifting map](/paraboloid-lifting-map/): $p$ is strictly inside the circle of $t$ exactly when the lifted $p$ is strictly below the plane of the lifted $t$. Three lemmas follow from this. (1) The conflict triangles are connected through shared edges, so line L6 finds them all. (2) $p$ is strictly on the inner side of every border edge, so the fan of line L9 tiles the cavity without overlaps. (3) Each new edge $px$ has an empty circle through $p$ and $x$, and each border edge separates a new triangle from a triangle that is not in conflict, so every edge is locally Delaunay. The [local Delaunay criterion](/local-delaunay-criterion/) then gives the empty circle property. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Per insertion.** A triangulation of $i$ points has at most $2i$ triangles and ghosts. The scan of line L5 takes $O(i)$ time, and lines L6 to L9 take time linear in the cavity size $|C|$, which is also $O(i)$.
- **Worst case.** The total time is $O(n^2)$. This is reached: for the points $(k, k^2)$ inserted in decreasing order of $k$, the total cavity size observed in tests is near $n^2/2$ (19700 for $n = 200$). For the same points in increasing order it is near $n$.
- **Random order.** If the insertion order is a uniformly random permutation and the points are in [general position](/general-position-delaunay/), the expected number of triangles created at step $i$ is less than $6$, by [backwards analysis](/backwards-analysis/). So the expected total cavity size is less than $6n$. The proof is in [the complexity proof](proofs/complexity/). In tests on random integer points the observed total is between $3.1n$ and $3.6n$.
- **With fast location.** Line L5 is then the bottleneck. With the history DAG of Guibas, Knuth and Sharir, or with conflict lists, the expected total time is $O(n \log n)$, which is optimal by the [lower bound](/voronoi-construction-lower-bound/).
- **Space.** $\Theta(n)$ for the triangles and the edge table.

## Properties

- **Exact.** The predicates are polynomials of degree 2 (orientation) and 4 (in-circle) in the coordinates, evaluated on integers.
- **Online.** Each point is inserted into a valid Delaunay triangulation of the points before it. The points do not need to be known in advance.
- **Any dimension.** The cavity rule and the proof do not use the plane. In $d$ dimensions the cavity is a set of simplices whose circumspheres hold $p$.
- **Degenerate input.** A point on a circumcircle is not a conflict, so cocircular points give one valid Delaunay triangulation. A point on a hull edge is handled by the segment rule of the ghosts.

## Variants and improvements

- **Lawson insertion.** Split the triangle that holds $p$ and then flip edges that are not locally Delaunay, as in the [Lawson flip algorithm](/lawson-flip-algorithm/). In general position the flips remove exactly the cavity triangles, so both methods give the same triangulation.
- **Randomized incremental construction.** Insert in random order and locate with a history DAG; see [randomized incremental construction](/randomized-incremental-construction/) and the [Delaunay triangulation](/delaunay-triangulation/) page.
- **Super triangle.** Many codes start with a large triangle that holds all points and remove its corners at the end. With finite corners the result can miss hull edges, which is why this page uses ghosts.
- **Weighted points.** With the power test in place of the in-circle test, the same method builds the [regular triangulation](/regular-triangulation/).
- **Mesh refinement.** [Delaunay refinement](/delaunay-refinement/) and [Ruppert's algorithm](/ruppert-algorithm/) insert circumcenters with this method.

## When to use it

Use it when points arrive one at a time, when the code must work in three or more dimensions, or when a simple exact Delaunay code is needed. For a static planar input, [Guibas-Stolfi divide and conquer](/guibas-stolfi-algorithm/) or [Fortune's sweep](/fortunes-algorithm/) have a deterministic $O(n \log n)$ bound. A randomized insertion order is necessary: sorted input can give quadratic time.

## Pitfalls

- **Inserting points in sorted order.** Line L4 has no protection against bad orders. Shuffle the points first, or use a spatial order such as a [Hilbert curve](/hilbert-curve/) together with a walk.
- **A tolerance in the conflict test of lines L5 and L6.** With floating point and a tolerance, the cavity can be not connected or not star-shaped, and line L9 then makes overlapping triangles. Use exact predicates, such as integers or [Shewchuk's expansions](/shewchuk-expansion-sum/).
- **Counting a point on the circle as a conflict in line L6.** With $\mathrm{incircle} \ge 0$, the cavity can grow past a cocircular point and lose star-shapedness. Use strict inequality.
- **A super triangle in line L3 that is too small.** Its corners can then be inside the circumcircle of a true hull triangle, and the final removal of the corners leaves holes. Ghost triangles avoid this problem.

## Implementations

## History

Adrian Bowyer and David Watson found the method independently, and The Computer Journal printed their papers one after the other in 1981. Both worked in $d$ dimensions. Bowyer computed the Dirichlet (Voronoi) tessellation, and Watson the Delaunay tessellation and the Voronoi polytopes. Guibas, Knuth and Sharir analysed the randomized incremental version in 1992. They showed that the expected structural change is linear and added the history DAG for point location. The method is now the core of most Delaunay mesh generators.

## References
