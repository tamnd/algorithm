---
tag: QBH461
kind: algorithm
slug: convex-polygon-point-location
name: Point location in a convex polygon
aliases:
- wedge binary search for convex polygons
- wedge method
- point location in a convex polygon by wedges
area: geometry/point-location
level: core
summary: Decide whether a point lies inside a convex polygon, or in which wedge it lies, in O(log n) time by binary search.
solves: [planar-point-location, point-in-polygon]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {build: O(n) worst case, query: Θ(log n) worst case}
  space: {extra: O(1) worst case}
properties: {online: false, deterministic: true, recursive: false, static: true}
history:
  year: 1975
  people: [Michael Ian Shamos]
  note: Preparata and Shamos present the wedge method for a convex polygon at the start of their chapter on point location and credit it to Shamos's work of 1975 (the attribution is to be checked).
prereqs: [convex-polygon, orientation-test, binary-search, angular-sort]
see_also: [point-in-convex-polygon, point-in-polygon, planar-point-location, slab-method-point-location, kirkpatrick-point-location, polygon-orientation, rotating-calipers]
sources:
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 2, Section 2.2.1 (the wedge method for a convex polygon, with an interior point and a binary search on the angles), to be checked
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 7, Search and intersection, Section 7.4 (point in polygon) and the exercises on the logarithmic test for a convex polygon, to be checked
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 38, Point location, by Jack Snoeyink (the convex polygon as the simplest case)
---

The wedge method locates a query point $q$ in a convex polygon with $n$ vertices in $O(\log n)$ time, with no preprocessing beyond the choice of one interior point $c$. The rays from $c$ through the vertices cut the plane into $n$ wedges, and the vertices are sorted by angle around $c$, so a binary search on the angle finds the wedge of $q$. Inside the wedge, one orientation test against the single edge of the wedge tells whether $q$ is inside, on the boundary or outside. The answer also names the wedge, which is the edge that $q$ sees when it is outside, and the edge or vertex that $q$ lies on.

## In plain words

Stand at a point inside a convex fence and look at the posts. They go around you in order, so the posts sorted by direction are the posts in fence order. To find where a ball lies, find the two posts between which the ball is seen, by halving the range of posts each time. Then only the piece of fence between those two posts matters: the ball is inside if it is on your side of that piece, on the fence if it touches it, and outside if it is past it.

A fence with a thousand posts needs about ten halving steps and one final test.

## The problem

**Notation.** $P = (v_0, v_1, \ldots, v_{n-1})$ is the polygon, $n$ its number of vertices, $p = (x, y)$ a point, and $d = 2$. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive when $p, q, r$ turn counterclockwise. A query has output size $h = 1$. The predicate $\mathrm{incircle}$ is not used. Indices are taken modulo $n$.

**Input.** A convex polygon given by its vertices in counterclockwise order: at least three vertices that are not all on one line, no vertex repeated, and $\mathrm{orient}(v_i, v_{i+1}, v_j) \ge 0$ for all $i, j$. Consecutive collinear vertices are allowed. Vertical edges need no special case, since no step compares $x$-coordinates alone.

**Query.** A point $q$. The answer is ("vertex", $i$) if $q = v_i$, ("edge", $i$) if $q$ is in the relative interior of the edge $v_i v_{i+1}$, and otherwise ("inside", $i$) or ("outside", $i$), where $i$ is the wedge of $q$.

**Wedges.** Let $c$ be a point in the open interior. Wedge $i$ is the set of points $r \ne c$ whose direction from $c$ lies between the directions of $v_i$ (included) and $v_{i+1}$ (excluded), turning counterclockwise. The center $c$ itself is put in wedge 0. The implementation uses $c = (v_0 + v_1 + v_k)/3$, where $v_k$ is the first vertex not on the line $v_0 v_1$, and multiplies every vector from $c$ by 3, so all tests are on integers.

## The algorithm

Let $\theta(r)$ be the counterclockwise angle of $r - c$ measured from the direction of $v_0 - c$, in $[0, 2\pi)$.

```pseudo id=main
CONVEX-LOCATE(v[0 .. n−1], c, q)
L1  if q = c then return (inside, 0)
L2  lo ← 0, hi ← n                 ▷ invariant: θ(v[lo]) ≤ θ(q) < θ(v[hi]), with θ(v[n]) = 2π
L3  while hi − lo > 1 do
L4      mid ← ⌊(lo + hi) / 2⌋
L5      if θ(v[mid]) ≤ θ(q) then lo ← mid else hi ← mid
L6  i ← lo, o ← orient(v[i], v[i+1], q)
L7  if o > 0 then return (inside, i)
L8  if o < 0 then return (outside, i)
L9  if q = v[i] then return (vertex, i) else return (edge, i)
```

- **Line L5** compares two angles without computing them. With $u = v_0 - c$, a vector $w$ is in the first half, angles $[0, \pi)$, if $u \times w > 0$, or $u \times w = 0$ and $u \cdot w > 0$; otherwise it is in the second half. If $v_{mid} - c$ and $q - c$ are in different halves, the one in the first half has the smaller angle. If they are in the same half, $\theta(v_{mid}) \le \theta(q)$ exactly when $(v_{mid} - c) \times (q - c) \ge 0$. Here $\times$ is the 2D cross product, so each test is a sign of a degree 2 polynomial in integers.
- **Line L2.** Since $\theta(v_0) = 0 \le \theta(q)$ and every angle is below $2\pi$, the invariant holds at the start. At the end, $\mathrm{hi} = \mathrm{lo} + 1$, so $q$ is in wedge $\mathrm{lo}$.
- **Lines L6 to L9.** Inside wedge $i$, the polygon is the triangle $c\, v_i\, v_{i+1}$, so only the edge $v_i v_{i+1}$ separates inside from outside. On the line of that edge, the wedge contains exactly the segment from $v_i$ (included) to $v_{i+1}$ (excluded), so $o = 0$ means that $q$ is $v_i$ or in the edge.

## Example

The polygon is $v_0 = (0,0)$, $v_1 = (3,0)$, $v_2 = (6,0)$, $v_3 = (8,3)$, $v_4 = (6,6)$, $v_5 = (2,6)$, $v_6 = (0,3)$. The vertices $v_0, v_1, v_2$ are collinear, so the center uses $v_3$: $3c = (0,0) + (3,0) + (8,3) = (11, 3)$, that is $c = (11/3, 1)$. The scaled vectors $3v_i - 3c$ are $(-11,-3)$, $(-2,-3)$, $(7,-3)$, $(13,6)$, $(7,15)$, $(-5,15)$, $(-11,6)$, and $u = (-11,-3)$.

For $q = (5, 4)$, the scaled vector is $w = (4, 9)$, and $u \times w = -11 \cdot 9 - (-3) \cdot 4 = -87 < 0$, so $q$ is in the second half. So are $v_3, v_4, v_5$.

| step | lo | hi | mid | $(3v_{mid} - 3c) \times w$ | decision |
|---|---|---|---|---|---|
| 1 | 0 | 7 | 3 | $13 \cdot 9 - 6 \cdot 4 = 93$ | $\theta(v_3) \le \theta(q)$, lo ← 3 |
| 2 | 3 | 7 | 5 | $-5 \cdot 9 - 15 \cdot 4 = -105$ | $\theta(v_5) > \theta(q)$, hi ← 5 |
| 3 | 3 | 5 | 4 | $7 \cdot 9 - 15 \cdot 4 = 3$ | $\theta(v_4) \le \theta(q)$, lo ← 4 |

So $q$ is in wedge 4, between $v_4 = (6,6)$ and $v_5 = (2,6)$. Then $\mathrm{orient}((6,6), (2,6), (5,4)) = (2-6)(4-6) - (6-6)(5-6) = 8 > 0$, so $q$ is inside. Other queries, checked by the test file:

| query | answer | reason |
|---|---|---|
| $(9, 6)$ | outside, wedge 3 | $\mathrm{orient}(v_3, v_4, q) = -9$ |
| $(1, 5)$ | outside, wedge 5 | $\mathrm{orient}(v_5, v_6, q) = -1$, just outside the edge from $(2,6)$ to $(0,3)$ |
| $(4, 0)$ | edge 1 | $o = 0$ on the edge from $(3,0)$ to $(6,0)$, between two collinear vertices |
| $(0, 3)$ | vertex 6 | the ray test gives $\times = 0$, so $q$ is on the ray of $v_6$ |
| $(3, 1)$ | inside, wedge 6 | $q$ is left of $c$ at the same height |

## Correctness

**Theorem.** For every convex polygon in counterclockwise order with at least three vertices not on one line, and every query point $q$, CONVEX-LOCATE returns ("vertex", $i$) if $q = v_i$, ("edge", $i$) if $q$ is in the relative interior of $v_i v_{i+1}$, and otherwise ("inside", $i$) or ("outside", $i$) with $q$ in wedge $i$.

Two facts carry the proof. Since $c$ is strictly inside, $\mathrm{orient}(c, v_i, v_{i+1}) > 0$ for every $i$, and the boundary winds once around $c$, so the angles $\theta(v_0) < \theta(v_1) < \cdots < \theta(v_{n-1})$ increase from $0$ to below $2\pi$ and the binary search is valid. Inside wedge $i$, the polygon is the triangle $c\, v_i\, v_{i+1}$, so the edge $v_i v_{i+1}$ alone decides inside, on the edge, or outside. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Query time.** The loop of lines L3 to L5 halves $\mathrm{hi} - \mathrm{lo}$, which starts at $n$, so it runs $\lceil \log_2 n \rceil$ times at most. Each step is one half test of each vector and one cross product, $O(1)$ on the [real RAM](/real-ram/). So the query takes $O(\log n)$ time in the worst case; the test file counts the steps against $\lceil \log_2 n \rceil$.
- **Lower bound.** The polygon with its $n$ vertices, $n$ edges, interior and exterior gives $2n + 2$ answers, so by the counting argument on the [planar point location](/planar-point-location/) page every [algebraic decision tree](/algebraic-decision-tree/) needs $\lceil \log_3 (2n + 2) \rceil$ tests. So the query time is $\Theta(\log n)$. For the inside or outside question alone, the answer has two values and this counting argument gives no bound.
- **Build time and space.** Finding $v_k$ scans the vertices until one is off the line $v_0 v_1$, which is $O(1)$ for a strictly convex polygon and $O(n)$ in the worst case. The structure stores the vertex array as given and three integers, so the extra space is $O(1)$.
- **Bit size.** With coordinates of absolute value at most $M$, the scaled vectors have coordinates at most $6M$ and each cross product at most $72 M^2$ in absolute value.

## Properties

- **No preprocessing.** The vertex array in counterclockwise order is the structure.
- **Exact.** All tests are signs of integer polynomials of degree 2.
- **Wedge output.** For an outside point, wedge $i$ names the edge that the ray from $c$ through $q$ crosses. That edge is visible from $q$, which is a starting point for computing the tangents from $q$.
- **Static.** An insertion of a vertex shifts the array.

## Variants and improvements

- **Fan from a vertex.** The [point in convex polygon](/point-in-convex-polygon/) page uses the vertex $v_0$ as the center of a fan of triangles. That needs no interior point, but $v_0$ is on the boundary, so the points on the two edges at $v_0$ and outside the angle at $v_0$ need special cases.
- **Several convex polygons.** For a subdivision whose faces are convex, locate the face first with a general method such as [Kirkpatrick's hierarchy](/kirkpatrick-point-location/), and the polygon test is then not needed.
- **Tangents and extreme points.** The same angular binary search, with a different test at each step, finds the tangents from an outside point and the extreme vertex in a direction, in $O(\log n)$.
- **Star-shaped polygons.** The lemma holds for any polygon that is star-shaped from $c$ with $c$ in the open kernel, so the wedge method works for [star-shaped polygons](/star-shaped-polygon/) when a kernel point is known.

## When to use it

Use the wedge method for many queries against one convex polygon, for example a convex hull or a convex obstacle. For one query, the linear test of all edges is as fast in practice for small $n$. For a non-convex polygon, use [point in polygon](/point-in-polygon/) by crossing numbers for one query, or a [planar point location](/planar-point-location/) structure for many.

## Pitfalls

- **A center on the boundary.** If $c$ is the centroid of three collinear vertices, it lies on an edge, the wedges are not narrower than $\pi$, and the binary search breaks. Choose the third vertex off the line $v_0 v_1$, as the code does.
- **Division for the centroid.** Computing $c$ with floating-point division makes the ray tests inexact. Scale by 3, as the code does, or use `fractions.Fraction`.
- **Angles near $2\pi$.** A comparison by the sign of the cross product alone is wrong for angles more than $\pi$ apart. The half test of line L5 fixes the order.
- **Clockwise input.** If the vertices are clockwise, the angles decrease, and the search returns wrong wedges. Check the sign of the area once, and reverse the array if it is negative.
- **Collinear vertices.** A point on an edge between two collinear vertices must be reported on the edge of its own wedge, not as outside a neighbor wedge. Since the wedges are half-open and $o$ is computed on the wedge's own edge, this happens automatically.

## Implementations

## History

Preparata and Shamos give the wedge method at the start of their chapter on point location and attribute it to Shamos (1975). It is the base case that the general methods of the 1970s and 1980s extend: the [slab method](/slab-method-point-location/) uses the same binary search on sorted directions, along the $x$-axis, and [Kirkpatrick's method](/kirkpatrick-point-location/) ends each query in a triangle.

## References
