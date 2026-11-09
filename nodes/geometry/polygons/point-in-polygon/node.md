---
tag: EQ1YET
kind: problem
slug: point-in-polygon
name: Point in polygon
aliases:
- point-in-polygon test
- point containment in polygon
- point inclusion problem
- polygon containment test
area: geometry/polygons
level: intro
summary: Decide whether a query point lies inside, outside, or on the boundary of a polygon.
prereqs: [polygon, simple-polygon, jordan-curve-theorem, orientation-test]
see_also: [crossing-number-algorithm, winding-number-algorithm, point-in-convex-polygon, planar-point-location, even-odd-fill-rule, polygon-with-holes, geometry-primitives, greiner-hormann-algorithm]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 7, Section 7.4, Point in Polygon (the ray crossing test, the half-open rule for vertices on the ray, and the boundary cases)
  - paper: doi:10.1016/S0925-7721(01)00012-8
    title: Kai Hormann and Alexander Agathos, The point in polygon problem for arbitrary polygons, Computational Geometry 20(3), 2001
    locator: the whole paper (even-odd and winding number definitions, the degenerate cases, and an exact winding number algorithm)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 2, Section 2.2 (point location, with inclusion in a simple, convex and star-shaped polygon)
  - book: "Eric Haines, Point in polygon strategies, in Paul S. Heckbert (editor), Graphics Gems IV, Academic Press, 1994"
    locator: the whole article (the crossings test, angle summation, half-plane and grid methods, and their speed in practice)
---

The point in polygon problem asks whether a query point $q$ lies inside a polygon, outside it, or on its boundary. For a [simple polygon](/simple-polygon/) the inside is well defined by the [Jordan curve theorem](/jordan-curve-theorem/). For a self-intersecting polygon there are two standard meanings, the even-odd rule and the nonzero winding rule. A single query takes $\Theta(n)$ time, by the [crossing number algorithm](/crossing-number-algorithm/) or the [winding number algorithm](/winding-number-algorithm/), and no algorithm can do better without preprocessing. With preprocessing, a query takes $O(\log n)$ time. The problem is easy to state but hard to get right: the ray used to count crossings can pass through a vertex or run along an edge, and the point can lie on the boundary.

## In plain words

You have a closed fence made of straight pieces, and a point on the ground. Is the point inside the fence, outside it, or on the fence?

If you walk from the point in a straight line to somewhere far away, you cross the fence an odd number of times when you started inside. Counting the crossings is easy until your path touches a corner or runs along a straight piece of fence. Then you have to be careful about what counts as a crossing.

For a fence that crosses itself, like a five-pointed star drawn in one stroke, there are two answers for the middle. One rule says the middle is outside, because you cross the fence twice to get out. The other says it is inside, because the fence goes around it twice.

## Definition

**Notation.** A polygon is a cyclic list of points $V = v_0, \ldots, v_{n-1}$ with edges $v_i v_{i+1}$, indices modulo $n$. A point is $p = (x, y)$, and $\operatorname{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, positive for a counterclockwise turn. The boundary $C$ is the union of the closed edges.

**Input.** A polygon $V$ and a query point $q$, with integer or rational coordinates. The polygon may be given clockwise or counterclockwise, and it may have collinear consecutive vertices.

**Output.** BOUNDARY if $q \in C$. Otherwise INSIDE or OUTSIDE, as follows.

- *Simple polygon.* $\mathbb{R}^2 \setminus C$ has exactly two connected components, one bounded. The answer is INSIDE if $q$ is in the bounded one.
- *Any closed polygon, even-odd rule.* The answer is INSIDE if a ray from $q$ that meets $C$ only at interior points of edges crosses $C$ an odd number of times. The parity does not depend on the ray.
- *Any closed polygon, nonzero rule.* The *winding number* $w(V, q)$ is the number of times the boundary, traversed once, goes counterclockwise around $q$: the total change of the angle of $v - q$ as $v$ runs along $C$, divided by $2\pi$. The answer is INSIDE if $w(V, q) \ne 0$.

For a simple polygon $w$ is $+1$ inside when the order is counterclockwise, $-1$ inside when it is clockwise, and $0$ outside, so the three definitions agree. In general the even-odd answer is $w \bmod 2$.

## Variants

- **Boundary convention.** Some applications want the boundary to count as inside (a closed region), some as outside (an open region), and graphics often splits it so that two polygons that share an edge never both claim a pixel there; see the [top-left fill rule](/top-left-fill-rule/). An algorithm that reports BOUNDARY separately supports all three.
- **Polygons with holes.** A [polygon with holes](/polygon-with-holes/) is given by an outer ring and inner rings. The even-odd rule over all rings gives the region; with the nonzero rule, the holes are oriented opposite to the outer ring.
- **Convex polygon.** If the polygon is known to be convex, a binary search answers in $O(\log n)$ time with no preprocessing beyond the input array; see [point in convex polygon](/point-in-convex-polygon/).
- **Star-shaped polygon with a known kernel point.** Sort the vertices by angle around the kernel point (they already are, in boundary order) and binary search for the wedge that contains $q$, again in $O(\log n)$ time.
- **Many queries.** Preprocess the polygon once and answer each query in $O(\log n)$ time; this is [planar point location](/planar-point-location/) in a subdivision with two faces.
- **Fill rules.** In vector graphics (PostScript, PDF, SVG) a path is filled by the even-odd or by the nonzero rule; see [even-odd fill rule](/even-odd-fill-rule/). The fill of a whole row of pixels is the batched version, [scanline polygon fill](/scanline-polygon-fill/).

## Examples

**Collinear vertices and rays along edges.** Take the square $V = (0,0), (2,0), (4,0), (4,4), (0,4)$, which has a straight vertex at $(2,0)$.

| $q$ | answer | the case |
|---|---|---|
| $(2, 2)$ | INSIDE | the ray to the right crosses one edge |
| $(2, 0)$ | BOUNDARY | $q$ is a vertex |
| $(3, 0)$ | BOUNDARY | $q$ is inside an edge |
| $(4, 4)$ | BOUNDARY | $q$ is a corner |
| $(-1, 0)$ | OUTSIDE | the ray to the right runs along the bottom edge, through three vertices |
| $(-1, 4)$ | OUTSIDE | the ray runs along the top edge |
| $(5, 2)$ | OUTSIDE | the ray meets nothing |

For $q = (-1, 0)$, a count that treats the two bottom edges as crossings, or that divides by $b_y - a_y$ to find where they meet the ray, gets a wrong count or fails. The half-open rule of the crossing number algorithm counts a vertex at the height of $q$ as lying below the ray. Then the horizontal edges never straddle the ray, each of the two vertical edges has exactly one endpoint strictly above it, and both of their crossings are to the right of $q$. The count is 2, which is even.

**A ray through a vertex.** In the triangle $(0,0), (4,0), (0,4)$, the ray from $q = (-1, 4)$ passes through the top vertex $(0,4)$ and touches the boundary only there. Both edges at $(0,4)$ go down from it, so the half-open rule counts neither, and the answer is OUTSIDE. A rule that counts each edge whose closed $y$-range contains $q_y$ would count two crossings here, which is right, but it would also count two at a vertex where the boundary passes through from below to above, which is wrong.

**The two fill rules.** The pentagram $V = (0,3), (-2,-3), (3,1), (-3,1), (2,-3)$, drawn in one stroke counterclockwise, has winding number $2$ around its center $q = (0, 0)$ and winding number $1$ in each of its five points, for example at $(0, 2)$. The even-odd rule says the center is OUTSIDE and $(0, 2)$ is INSIDE. The nonzero rule says both are INSIDE. The point $(0, 1)$ lies on the horizontal edge from $(3,1)$ to $(-3,1)$, so it is BOUNDARY under both rules, and $(-5, 1)$, whose ray runs along that edge, is OUTSIDE.

## Known algorithms

| algorithm | time per query | preprocessing | answers |
|---|---|---|---|
| [crossing number](/crossing-number-algorithm/) (ray casting) | $\Theta(n)$ | none | even-odd |
| [winding number](/winding-number-algorithm/) (signed crossings or quadrants) | $\Theta(n)$ | none | winding number |
| angle summation | $\Theta(n)$, with trigonometric functions | none | winding number, inexact |
| signed fan of triangles $v_0 v_i v_{i+1}$ | $\Theta(n)$ | none | winding number |
| [point in convex polygon](/point-in-convex-polygon/) | $O(\log n)$ | none (convex input) | inside or not |
| [slab method](/slab-method-point-location/) | $O(\log n)$ | $O(n^2)$ space, or $O(n)$ with persistence | any fixed rule |
| [trapezoidal map](/trapezoidal-map/) or [Kirkpatrick](/kirkpatrick-point-location/) | $O(\log n)$ | $O(n \log n)$ expected or $O(n)$ after a linear triangulation | any fixed rule |

The crossing number algorithm counts the edges that a horizontal ray from $q$ crosses, with the half-open rule: an edge counts only when exactly one endpoint is strictly above $q$, which handles rays through vertices and along horizontal edges. The winding number algorithm adds $+1$ for each such crossing on an upward edge and $-1$ for each on a downward edge. Both test for the boundary first with an exact on-segment test, and both use only degree 2 predicates, so they are exact with integer input.

Angle summation adds up the angles $\angle v_i q v_{i+1}$ and compares the sum with $2\pi$. It is slow because of the inverse trigonometric functions, and it needs a tolerance, so it is not exact near the boundary. The signed fan uses the identity that $w(V, q)$ is the number of triangles $v_0 v_i v_{i+1}$ that contain $q$, each counted with the sign of its orientation, for $q$ on no edge of any of these triangles.

## Bounds

**$\Omega(n)$ for a single query.** Without preprocessing, every algorithm must read all $n$ vertices in the worst case. Let $V$ be a regular polygon with $n \ge 4$ vertices and center $q$, so $q$ is INSIDE. For each $i$, let $V'$ be $V$ with $v_i$ replaced by a point $p$ just beyond $q$ on the ray from $v_i$ through $q$. The new edges $v_{i-1} p$ and $p v_{i+1}$ lie inside $V$ and meet its boundary only at their ends, so $V'$ is simple, and $q$ lies on the open diagonal $v_i p$ of the cut-off quadrilateral $v_{i-1} v_i v_{i+1} p$, so $q$ is OUTSIDE $V'$. An algorithm that never reads $v_i$ gives the same answer on $V$ and on $V'$, so it is wrong on one of them.

**$\Omega(\log n)$ per query after preprocessing.** Take a comb polygon whose $k$ teeth cross the line $y = 0$ in $k$ disjoint intervals. Consider any decision tree in which each test is the sign of a linear function of $q$ (the tests may depend on the polygon in any way). Each leaf is reached by an intersection of half-planes, a convex set, which meets the line $y = 0$ in an interval, and the answer is the same on all of it. Along the line the answer changes at least $2k$ times, so the tree has at least $2k + 1$ leaves and depth at least $\log_2(2k + 1)$. With $k = \Theta(n)$ this gives $\Omega(\log n)$, and the point location structures above meet it.

**Arithmetic.** The exact algorithms evaluate predicates of degree 2 in the coordinates. With integer coordinates of absolute value below $B$, the values have absolute value at most $8B^2$, so $B < 2^{30}$ fits in signed 64-bit integers.

## Reductions

- **To point location.** A polygon is a planar subdivision with an inside face, an outside face and the boundary, so point in polygon is a special case of [planar point location](/planar-point-location/), and every point location structure answers it.
- **Even-odd from the winding number.** The even-odd answer is $w(V, q) \bmod 2$, because the winding number is a sum of $\pm 1$ terms, one for each crossing of a ray.
- **From interval membership.** On a comb polygon, deciding whether $q$ on the line $y = 0$ is inside is deciding whether a number lies in a union of $k$ disjoint intervals. This is the reduction behind the $\Omega(\log n)$ bound.
- **In polygon clipping.** The [Greiner-Hormann algorithm](/greiner-hormann-algorithm/) and other [polygon clipping](/polygon-clipping/) methods use a point in polygon test to decide whether each piece of one boundary lies inside the other polygon.

## Applications

- **Geographic information systems.** Deciding which country, district or delivery zone contains a coordinate, and geofencing in mobile apps.
- **Graphics and user interfaces.** Filling paths by the even-odd or nonzero rule, hit testing a mouse click against a shape, and [scanline polygon fill](/scanline-polygon-fill/).
- **Geometric algorithms.** Classifying vertices in [polygon clipping](/polygon-clipping/), checking candidate points in mesh generation, and testing containment of one polygon in another (test one vertex, after checking that the boundaries do not cross).
- **Physics and games.** Collision tests of a point against a 2D shape, and deciding whether a unit stands in a region of a map.

## References
