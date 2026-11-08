---
tag: TY8J2Y
kind: algorithm
slug: beneath-beyond
name: Beneath-beyond method
aliases:
- incremental convex hull
- incremental hull construction
- randomized incremental convex hull
- conflict graph convex hull
area: geometry/convex-hulls
level: core
summary: Adds points one at a time, deleting the visible facets and connecting the horizon; works in any dimension.
solves: [convex-hull-3d]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {expected: O(n log n)}
  space: {expected: O(n)}
properties: {online: false, deterministic: false, recursive: false}
history:
  year: 1981
  people: [Raimund Seidel, Michael Kallay]
  note: Seidel and Kallay described the incremental method for any dimension around 1981; Clarkson and Shor added the random order and the conflict graph in 1989.
prereqs: [convex-hull-3d, convex-polytope, orientation-test, randomized-incremental-construction]
see_also: [facet, general-position, quickhull, chan-algorithm, backwards-analysis, delaunay-triangulation-construction, convex-hull-lower-bound, euler-formula]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 11, Convex Hulls (the randomized incremental algorithm in three dimensions with a conflict graph and its expected O(n log n) analysis)
  - paper: doi:10.1007/BF02187740
    title: Kenneth L. Clarkson and Peter W. Shor, Applications of random sampling in computational geometry, II, Discrete and Computational Geometry 4(5), 1989
    locator: the randomized incremental convex hull with conflict lists and the bound on the expected total conflict size
  - book: isbn:9780387004242
    title: Branko Grünbaum, Convex Polytopes, second edition, Springer, 2003
    locator: Chapter 5 (the faces of the convex hull of a polytope and one more point, described by the points beneath and beyond each facet)
  - paper: "Raimund Seidel, A convex hull algorithm optimal for point sets in even dimensions, M.Sc. thesis, University of British Columbia, 1981"
    locator: the beneath-beyond algorithm in d dimensions
---

The beneath-beyond method builds the [convex hull](/convex-hull/) of a point set by adding the points one at a time. When a new point $p$ lies outside the current hull, the facets that $p$ can see are deleted, and each edge on the border of the deleted region, the *horizon*, is joined to $p$ by a new facet. The method works in any dimension. In three dimensions, with the points added in a random order and a *conflict graph* that records which facets each remaining point can see, the expected time is $O(n \log n)$, which is optimal. The analysis is the classic example of the Clarkson-Shor technique for [randomized incremental construction](/randomized-incremental-construction/).

## In plain words

Think of the hull as a tight bag around the points seen so far. Take the next point. If it is inside the bag, nothing changes. If it is outside, stand at the point and look at the bag. Cut out the faces that face you. The hole has a rim, made of the edges between a face you see and a face you do not see. Close the hole with a tent of new faces, one from each edge of the rim up to the new point.

To find fast which faces a new point sees, each waiting point keeps a list of the faces it sees, and each face keeps a list of the waiting points that see it. Only the points on the lists of nearby old faces can see a new face. In a random order these lists stay short on average.

## The problem

The input is a list $P$ of $n$ points in $\mathbb{R}^3$ with exact coordinates. The output is a set of triangles whose vertices are input points, oriented counterclockwise as seen from outside, whose union is the boundary of $\mathrm{conv}(P)$. If $P$ does not span $\mathbb{R}^3$ (all points on one plane), the output is empty and a planar method applies. This is the [3D convex hull problem](/convex-hull-3d/).

Notation: for points $a, b, c, d$ let $\mathrm{orient}(a, b, c, d) = ((b - a) \times (c - a)) \cdot (d - a)$, six times the signed volume of the tetrahedron. A triangle $(a, b, c)$ of the hull is a *facet*, and its outward normal is $(b - a) \times (c - a)$. A point $q$ is *beyond* the facet if $\mathrm{orient}(a, b, c, q) > 0$, on its plane if the value is 0, and *beneath* it if the value is negative. The point $q$ lies outside the current hull exactly when it is beyond at least one facet. The pair $(q, t)$ with $q$ beyond $t$ is a *conflict*, and the *conflict list* $C(t)$ of a facet $t$ is the set of waiting points beyond it.

## The algorithm

```pseudo id=main
BENEATH-BEYOND(P)
L1  put the points of P in a uniformly random order
L2  a, b, c, d ← the first four points of the order that are not on one plane; if none, return the empty set
L3  T ← the four facets of the tetrahedron abcd, each oriented so that the fourth point is beneath it
L4  for each other point q and each t ∈ T: if q is beyond t, add the conflict (q, t)
L5  for each other point p in the order do
L6      V ← the facets in conflict with p
L7      if V is empty then continue                       ▷ p is inside or on the hull
L8      H ← the edges (u, v) of facets f ∈ V whose other facet g is not in V      ▷ the horizon
L9      for each horizon edge (u, v), with f ∈ V and g ∉ V do
L10         t ← the triangle (u, v, p); add t to T
L11         for each q ≠ p in C(f) ∪ C(g): if q is beyond t, add the conflict (q, t)
L12     delete the facets of V from T, with their conflicts
L13 return T
```

The data structure is a map from each directed edge $(u, v)$ to the facet that contains it, so that line L8 finds the other facet $g$ of an edge as the facet that contains $(v, u)$. The conflict graph is stored twice: a list $C(t)$ for each facet and a set of facets for each waiting point. Line L6 reads the set of $p$, and line L12 removes each deleted facet from the sets of its conflicting points.

Line L10 gives the new facet the edge $(u, v)$ in the same direction as the visible facet $f$ that it replaces, so the new facet is oriented outward: the third vertex $w$ of $f$ satisfies $\mathrm{orient}(u, v, p, w) = -\mathrm{orient}(u, v, w, p) < 0$. Line L11 is correct because of a short geometric fact: a point that is beyond the new facet $(u, v, p)$ was beyond $f$ or beyond $g$. So the conflict list of the new facet is found by testing only the points of $C(f) \cup C(g)$.

**Any dimension.** In $\mathbb{R}^d$ the facets are $(d-1)$-simplices in general position, the horizon consists of $(d-2)$-faces (ridges) between a visible and an invisible facet, and each horizon ridge $r$ gives the new facet $\mathrm{conv}(r \cup \{p\})$. The orientation test is the sign of a $(d+1) \times (d+1)$ [determinant](/determinant/). Lines L1 to L13 stay the same.

## Example

Take the seven points

| name | a | b | c | d | e | f | g |
| --- | --- | --- | --- | --- | --- | --- | --- |
| point | (0,0,0) | (6,0,0) | (0,6,0) | (0,0,6) | (1,2,1) | (4,3,2) | (6,5,−1) |

which are in general position, and suppose that the random order is $a, b, c, d, e, f, g$. Line L2 takes the tetrahedron $abcd$. Its four outward facets and their conflict lists are

| facet | plane | conflict list |
| --- | --- | --- |
| $acb$ | $z = 0$ | $g$ |
| $abd$ | $y = 0$ | none |
| $adc$ | $x = 0$ | none |
| $bcd$ | $x + y + z = 6$ | $f, g$ |

The point $f = (4, 3, 2)$ is beyond $bcd$ because $4 + 3 + 2 = 9 > 6$. The point $g = (6, 5, -1)$ is beyond the plane $z = 0$ and beyond the plane $x + y + z = 6$, since $6 + 5 - 1 = 10 > 6$.

**Insert $e$.** No facet has $e$ in its conflict list, so $V$ is empty and $e$ is inside the hull. Nothing changes.

**Insert $f$.** $V = \{bcd\}$. Each edge of $bcd$ has an invisible neighbour, so the horizon is $bc, cd, db$. The new facets are $bcf$, $cdf$ and $dbf$. For $bcf$, line L11 tests the points of $C(bcd) \cup C(acb) = \{f, g\}$ without $f$: $g$ is beyond $bcf$. The other two new facets have empty conflict lists. After line L12 the hull has six facets: $acb$ ($g$), $abd$, $adc$, $bcf$ ($g$), $cdf$, $dbf$.

**Insert $g$.** $V = \{acb, bcf\}$. The edge $cb$ of $acb$ is shared with $bcf$, which is also visible, so it is not on the horizon. The horizon is $ac, ba, cf, fb$, a closed loop around the visible region. The new facets are $acg$, $bag$, $cfg$ and $fbg$, and no points are waiting. The final hull has the eight facets

$$abd,\ adc,\ cdf,\ dbf,\ acg,\ bag,\ cfg,\ fbg,$$

with six vertices and twelve edges, as [Euler's formula](/euler-formula/) requires: $6 - 12 + 8 = 2$. The point $e$ is inside.

## Correctness

The proof assumes [general position](/general-position/): no three points on a line and no four points on a plane. Then every facet of each intermediate hull is a triangle of input points, and a triangle $xyz$ of points of a set $S$ is a facet of $\mathrm{conv}(S)$ exactly when all other points of $S$ are strictly on one side of its plane.

The invariant of the loop of line L5 is: after the points of a set $S$ are processed, $T$ is the set of facets of $\mathrm{conv}(S)$, each oriented outward, and for each facet $t$ the list $C(t)$ holds exactly the waiting points beyond $t$. Line L4 sets it up. For the step, the key lemma is the beneath-beyond theorem in three dimensions: if $p$ is outside $\mathrm{conv}(S)$, the facets of $\mathrm{conv}(S \cup \{p\})$ are the facets of $\mathrm{conv}(S)$ that $p$ is beneath, and the triangles $uvp$ for the edges $uv$ of $\mathrm{conv}(S)$ that have one facet with $p$ beyond and one with $p$ beneath. The proof reduces each statement to a picture in the plane perpendicular to the edge $uv$, where the two facets at $uv$ bound a wedge that contains $S$. The same picture shows that a point beneath both $f$ and $g$ is beneath the new facet $uvp$, which justifies line L11. The full proof is in the correctness proof below.

Without general position the implementation still returns a correct boundary, because it treats a point on a facet plane as not visible. A point on the boundary of the current hull is then skipped, and a point that is outside the hull but on the plane of a facet $g$ gives new facets in the plane of $g$. So the output can have several coplanar triangles on one face and vertices in the middle of a face or an edge. The tests check this case against a brute-force computation of the facet planes.

## Complexity

The bounds below assume general position and are expectations over the random order of line L1, for every input.

- **Facets created.** A facet of $\mathrm{conv}(P_r)$, the hull of the first $r$ points, was created at step $r$ only if $p_r$ is one of its three vertices. By backwards analysis, the expected number of facets created at step $r$ is at most $3 / r$ times the number of facets of $\mathrm{conv}(P_r)$, which is at most $2r - 4$. So the expected total number of facets created is at most $6n$. Deleting a facet and building the horizon cost $O(1)$ per facet, so these steps cost $O(n)$ expected time.
- **Conflict updates.** Line L11 costs $O(|C(f)| + |C(g)|)$ for each horizon edge. The configuration of a horizon edge is the edge with its two facets, defined by four points, and its conflict set is $C(f) \cup C(g)$. Each such configuration is destroyed at most once. The Clarkson-Shor bound for configurations defined by at most four points, with $O(r)$ configurations on a set of $r$ points, gives an expected total of $O(n \log n)$. See the complexity proof below.
- **Total.** $O(n \log n)$ expected time on the [real RAM](/real-ram/) and $O(n)$ expected space, since the total size of the conflict lists at any time is at most the number of conflicts created.

The bound is optimal: the [convex hull lower bound](/convex-hull-lower-bound/) of $\Omega(n \log n)$ holds already for points on a paraboloid. For a bad insertion order, for example points on a curve inserted in an order where each new point sees a linear number of facets, the time can be quadratic. In $\mathbb{R}^d$ the same analysis gives $O(n \log n + n^{\lfloor d/2 \rfloor})$ expected time, which matches the worst-case number of facets from the Upper Bound Theorem (see [convex polytope](/convex-polytope/)).

## Properties

- **Randomized, Las Vegas.** The output is always correct, and only the running time depends on the random order.
- **Exact with integer input.** The only predicate is the orientation test, a polynomial of degree 3 in the coordinates. With coordinates of absolute value at most $M$ the determinant is at most $48 M^3$ in absolute value.
- **Any dimension.** The same steps work in $\mathbb{R}^d$, with ridges in place of edges.
- **Not online as written.** The conflict graph needs all points in advance. A history graph of the deleted facets replaces it in an online version.

## Variants and improvements

- **Deterministic incremental hull.** Without a conflict graph, find the visible facets of each new point by testing all current facets. This takes $O(n^2)$ time in three dimensions and is simple. If the points are first sorted lexicographically, each new point is a vertex of the new hull and sees a facet next to the previous point, so the visible region can be found by a search from there. This is Seidel's beneath-beyond algorithm in $\mathbb{R}^d$, with time $O(n \log n + n^{\lceil d/2 \rceil})$, optimal in even dimensions.
- **Randomized incremental construction.** The random order with conflict lists is due to Clarkson and Shor. It gives $O(n \log n + n^{\lfloor d/2 \rfloor})$ expected time in every dimension. Chazelle gave a deterministic algorithm with the same bound in 1993.
- **Quickhull.** [Quickhull](/quickhull/) is an incremental method that adds, for each facet, the point of its conflict list farthest from it. It needs no random order but has a quadratic worst case.
- **Delaunay triangulation.** Lifting planar points to the paraboloid $z = x^2 + y^2$ turns the lower hull into the [Delaunay triangulation](/delaunay-triangulation-construction/), and the randomized incremental Delaunay algorithm is this method in disguise.
- **Output-sensitive hulls.** [Chan's algorithm](/chan-algorithm/) gives $O(n \log h)$ in three dimensions for $h$ hull facets.

## When to use it

Use it for convex hulls in three dimensions and in low dimensions above three. It is the method behind most practical 3D hull codes. The expected bound holds for every input, and the random order removes the bad cases of a fixed order. Use exact predicates: with floating-point coordinates, an orientation sign error can make the horizon not a closed loop. For a planar hull, use [Andrew's monotone chain](/andrew-monotone-chain/), which is simpler.

## Pitfalls

- **Visible with $\ge 0$.** Treat a point on a facet plane as not seeing the facet. If such a facet is deleted, a point on its plane but outside it gives new triangles that fold back over the hull.
- **Wrong orientation of new facets.** The new facet must contain the horizon edge in the direction of the deleted facet, $(u, v, p)$, not $(v, u, p)$. With the wrong direction the new facet points inward, and the edge map gets two facets with the same directed edge $(v, u)$.
- **Deleting too early.** Line L11 reads $C(f)$ of the visible facet $f$. Delete the visible facets only after the new facets have their conflict lists.
- **Degenerate start.** The first four points may be on one plane. Line L2 must skip points until it finds four affinely independent ones, and a fully planar input needs its own case.
- **Floating-point orientation.** With a tolerance or an inexact sign, a point can see a facet but not its neighbour on the other side of a nearly flat edge, and the horizon breaks. Use integers, `fractions.Fraction`, or an adaptive exact predicate.

## Implementations

## History

Grünbaum's book on convex polytopes (1967) described the faces of the convex hull of a polytope and one more point in terms of the facets that the point is beneath or beyond. The method takes its name from these two words. Raimund Seidel and Michael Kallay turned this description into an algorithm for any dimension around 1981. Seidel's version, with a presorted order, is optimal in even dimensions. Clarkson and Shor showed in 1989 that a random insertion order with conflict lists gives expected time $O(n \log n + n^{\lfloor d/2 \rfloor})$, optimal in every dimension, and their random sampling bound became the standard tool for randomized incremental algorithms. Seidel later gave the simpler proof by backwards analysis.

## References
