---
tag: MYT44B
kind: concept
slug: geometry-primitives
name: Geometry primitives
aliases:
- geometric primitives
- geometric predicates
- basic geometric operations
area: geometry/polygons
level: intro
summary: Basic geometric operations such as cross product, dot product, orientation tests and segment intersection used in computational geometry.
prereqs: [point-and-vector, dot-product, cross-product]
see_also: [orientation-test, oriented-triangle-area, segment-intersection-detection, point-in-polygon, convex-polygon, polygon-simplicity-test, shoelace-formula, in-circle-test]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Section 33.1, Line-segment properties (cross products, the turn test, and the procedures SEGMENTS-INTERSECT, DIRECTION and ON-SEGMENT)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Sections 1.3 to 1.5 (Area2, Left, LeftOn, Collinear, Between and the segment intersection code) and Chapter 7, Section 7.4 (point in polygon)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 1, Section 1.2, Degeneracies and Robustness
  - paper: doi:10.1007/PL00009321
    title: Jonathan Richard Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates, Discrete and Computational Geometry 18(3), 1997
    locator: the sections on the orient2d and incircle predicates
---

Geometry primitives are the small, fixed-size tests and constructions that planar algorithms call in their inner loops: the [dot product](/dot-product/), the [cross product](/cross-product/), the [orientation test](/orientation-test/), the on-segment test, the segment intersection test, the signed area of a polygon, and the tests for convexity, simplicity and point containment. An algorithm is only as correct as its primitives, so each one must be exact on degenerate input: collinear points, a point on an edge, equal points. With integer coordinates each primitive below is an exact integer computation.

## In plain words

Large geometry programs, such as a convex hull or a map overlay, ask the same few small questions again and again. Does this walk turn left or right? Is this point on that segment? Do these two segments touch? Which of these two distances is shorter? Each question is answered with a few multiplications and subtractions of coordinates, and only the sign of the result matters. If one answer is wrong, the large program can loop for ever or produce nonsense, so these small questions must always get the right answer. The safe way is to keep the coordinates as whole numbers or exact fractions, and to treat the special cases, such as three points on one line, on purpose.

## The idea

**Notation.** $P$ is the input point set and $n$ the input size. A point is $p = (x, y)$, and $\operatorname{orient}(p, q, r) = \operatorname{sign}\big((q - p) \times (r - p)\big)$, positive for a counterclockwise turn. A polygon is a cyclic vertex sequence $v_0, \ldots, v_{n-1}$, with indices taken modulo $n$.

**Predicates and constructions.** A *predicate* returns a sign or a yes/no answer; a *construction* returns new coordinates. The *degree* of a predicate is the degree of the polynomial in the input coordinates whose sign it computes. Integer input of absolute value below $B$ gives values of size $O(B^k)$ for a predicate of degree $k$, so a predicate of fixed degree is exact with fixed-length integers. Constructions are rational: the crossing point of two lines has coordinates of degree 3 over degree 2. The rule of exact geometric computation is to evaluate every predicate exactly, even on constructed points, which with integer input means `Fraction` or integer homogeneous coordinates.

**The primitives.**

| Primitive | Exact formula | Degree | Page |
|---|---|---|---|
| dot product | $u \cdot v = u_x v_x + u_y v_y$ | 2 | [dot product](/dot-product/) |
| cross product | $u \times v = u_x v_y - u_y v_x$ | 2 | [cross product](/cross-product/) |
| orientation | $\operatorname{sign}((q - p) \times (r - p))$ | 2 | [orientation test](/orientation-test/) |
| distance comparison | $\operatorname{sign}(\lvert p - q\rvert^2 - \lvert r - s\rvert^2)$ | 2 | [Euclidean distance](/euclidean-distance/) |
| point on closed segment $ab$ | $\operatorname{orient}(a, b, p) = 0$ and $(p - a) \cdot (p - b) \le 0$ | 2 | below |
| closed segments intersect | four orientations and four on-segment tests | 2 | [segment intersection detection](/segment-intersection-detection/) |
| in-circle | sign of a 3 by 3 determinant of lifted points | 4 | [in-circle test](/in-circle-test/) |
| signed polygon area | $2A = \sum_{i} v_i \times v_{i+1}$ | 2 | [shoelace formula](/shoelace-formula/) |

**Segment intersection with all degenerate cases.** Let $d_1 = \operatorname{orient}(c, d, a)$, $d_2 = \operatorname{orient}(c, d, b)$, $d_3 = \operatorname{orient}(a, b, c)$ and $d_4 = \operatorname{orient}(a, b, d)$. The closed segments $ab$ and $cd$ meet if and only if

1. $d_1 d_2 < 0$ and $d_3 d_4 < 0$ (a proper crossing at one interior point of both), or
2. some $d_i = 0$ and the matching endpoint lies on the other segment: $d_1 = 0$ and $a \in cd$, or $d_2 = 0$ and $b \in cd$, or $d_3 = 0$ and $c \in ab$, or $d_4 = 0$ and $d \in ab$.

*Proof.* If case 1 holds, $a$ and $b$ are strictly on opposite sides of the line $cd$, so the segment $ab$ crosses that line at one point $x$ strictly between $a$ and $b$; by the same argument for $cd$, the line $ab$ crosses $cd$ at one point strictly between $c$ and $d$; both points are the unique common point of the two lines, which are not parallel, so $x$ is in both segments. If case 2 holds, the named endpoint is a common point. Conversely, let $x$ be a common point. If $x$ is an endpoint, say $x = a$, then $a \in cd$, so $d_1 = 0$ and case 2 holds. Otherwise $x$ is interior to both segments. If the segments are collinear, all $d_i = 0$, and an endpoint of one lies in the other (two overlapping intervals on a line contain an endpoint of one of them), so case 2 holds. If they are not collinear, the lines meet only at $x$; $a$ and $b$ are on the line $ab$ on opposite sides of $x$, and neither is on the line $cd$ unless it equals $x$, so $d_1 d_2 < 0$, and in the same way $d_3 d_4 < 0$, which is case 1. $\square$

**Polygon tests built from the primitives.**

- *Signed area and orientation.* The [shoelace formula](/shoelace-formula/) gives twice the signed area as an integer. For a simple polygon it is positive if and only if the vertices are in counterclockwise order, see [polygon orientation](/polygon-orientation/).
- *Simplicity.* A polygon with $n \ge 3$ vertices is simple if and only if consecutive vertices differ, two adjacent edges meet only in their common vertex, and two non-adjacent edges do not meet at all (closed segments). Testing all pairs takes $O(n^2)$ primitive calls; a sweep in the manner of [Shamos and Hoey](/shamos-hoey-algorithm/) takes $O(n \log n)$. See [polygon simplicity test](/polygon-simplicity-test/).
- *Convexity.* A polygon is convex and simple if and only if all turns $\operatorname{orient}(v_{i-1}, v_i, v_{i+1})$ have one sign (zeros allowed for collinear vertices, with no reversal), and the edge directions turn around exactly once. The second condition is needed: a pentagram has five turns of one sign. See [convex polygon](/convex-polygon/) for an exact test.
- *Point in polygon.* The [crossing number algorithm](/crossing-number-algorithm/) counts how often a ray from the query point crosses the boundary, and the [winding number algorithm](/winding-number-algorithm/) counts signed crossings. Both need the rules for a ray through a vertex and for horizontal edges, and a separate on-boundary test. See [point in polygon](/point-in-polygon/).

**Handling degenerate input.** There are three ways. *General position* assumes that no degenerate case occurs, which is fine for a proof but not for a program. *Explicit cases* treat each zero sign, as in the segment test above. *Symbolic perturbation* (simulation of simplicity) moves the input by an infinitesimal amount in a fixed symbolic way, so that no sign is ever zero, and gives one consistent answer for each degenerate case. In each way the signs must be exact. Floating-point evaluation with a tolerance $\varepsilon$ does not fix the problem: the relation "within $\varepsilon$" is not transitive, and the answers of different tests can contradict each other. [Shewchuk's adaptive predicates](/shewchuk-expansion-sum/) give exact signs for float input at a cost close to plain float evaluation in the common case.

## Examples

**An L-shaped polygon.** $L = (0,0), (4,0), (4,2), (2,2), (2,4), (0,4)$. The shoelace sum is $2A = 24$, so the area is 12 and the order is counterclockwise. The turns are $16, 8, 4, -4, 4, 8$ (as values of $(v_i - v_{i-1}) \times (v_{i+1} - v_i)$): one negative turn at $(2, 2)$ shows a reflex vertex, so $L$ is not convex.

**A pentagram.** Take the pentagon $(0,3), (3,1), (2,-3), (-2,-3), (-3,1)$ and visit every second vertex: $(0,3), (2,-3), (-3,1), (3,1), (-2,-3)$. All five turns are negative ($-24, -22, -24, -24, -22$), yet the edge directions turn around twice and the polygon is not simple. Its shoelace value $2A = -32$ is not the area of a region: it is minus the sum of area times winding number, which counts the central pentagon twice and the five tips once.

**Collinear vertices.** The square $(0,0), (2,0), (4,0), (4,4), (0,4)$ has turns $8, 0, 8, 16, 16$. The zero at $(2, 0)$ is a straight vertex. The polygon is convex, but an algorithm that demands strict turns rejects it.

**Segment intersection.** For $ab = (0,0)(4,4)$ and $cd = (0,4)(4,0)$ the four orientations are $-1, 1, 1, -1$: a proper crossing, at parameter $t = 1/2$ of $ab$, the point $(2, 2)$. For $ab = (0,0)(3,1)$ and $cd = (1,2)(2,-1)$ the crossing point is $(3/2, 1/2)$, exact as a pair of fractions. For $ab = (0,0)(4,4)$ and $cd = (2,2)(5,0)$, $d_3 = 0$ and $c$ is on $ab$: the segments touch. For $(0,0)(2,2)$ and $(1,1)(3,3)$ all four orientations are 0 and the segments overlap. For $(0,0)(1,1)$ and $(2,2)(3,3)$ all four are also 0, but no endpoint lies on the other segment, so they are disjoint: a test that looks only at the signs gets this case wrong.

## Where it is used

- Convex hulls: [Andrew's monotone chain](/andrew-monotone-chain/) and [Graham scan](/graham-scan/) use only the orientation test after sorting.
- Intersections: the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) uses orientation to order segments and the segment test to find crossings.
- Polygons: [point in polygon](/point-in-polygon/), [point in convex polygon](/point-in-convex-polygon/), the [shoelace formula](/shoelace-formula/), [polygon clipping](/polygon-clipping/) and the [Minkowski sum of convex polygons](/minkowski-sum-convex-polygons/).
- Triangulations: [ear clipping](/ear-clipping/) uses orientation and point-in-triangle tests, and [Delaunay triangulation](/delaunay-triangulation/) adds the [in-circle test](/in-circle-test/).
- Robustness: [error-free transformations](/error-free-transformations/) and [Shewchuk's expansion arithmetic](/shewchuk-expansion-sum/) make the predicates exact for float input.

## References
