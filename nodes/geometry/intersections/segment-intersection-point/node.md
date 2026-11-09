---
tag: DG9ZZA
kind: algorithm
slug: segment-intersection-point
name: Segment intersection point
aliases: [intersection of two segments, segment-segment intersection]
area: geometry/intersections
level: core
summary: Decides with four exact orientation tests whether two closed segments meet, and returns the common point or the overlapping segment.
model: real-ram
complexity:
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1976
  people: [Michael Ian Shamos, Dan Hoey]
  note: The test of two segments by the signs of four orientation determinants is folklore of computer graphics; Shamos and Hoey made it the basic predicate of their segment intersection sweep in 1976, and Cormen, Leiserson, Rivest and Stein give the standard form with the on-segment checks.
prereqs: [orientation-test, cross-product, point-and-vector, line-line-intersection]
see_also: [segment-intersection-detection, shamos-hoey-algorithm, bentley-ottmann-algorithm, all-segment-intersections, line-equation-from-segment, general-position, degeneracy-in-sweeps, floating-point-arithmetic]
sources:
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 33, Section 33.1, Line-segment properties (procedures SEGMENTS-INTERSECT, DIRECTION and ON-SEGMENT)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 7, Section 7.2, Segment-segment intersection (the parametric solution, the parallel and collinear cases, code SegSegInt)
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (FOCS 1976), 208-215
    locator: the pairwise segment test used inside the sweep
---

The segment intersection point algorithm takes two closed segments $[a, b]$ and $[c, d]$ in the plane and returns their common part: nothing, one point, or a segment when the two overlap on a common line. It uses four [orientation tests](/orientation-test/) and, for a proper crossing, one division, so with integer or rational input it is exact. It is the basic predicate of every [segment intersection sweep](/shamos-hoey-algorithm/), and it handles all degenerate cases: shared end points, an end point on the other segment, vertical segments, collinear overlap and segments of length zero.

## In plain words

Look at the line through the second segment. If the two end points of the first segment are on different sides of that line, and the same is true the other way round, the segments cross, and the crossing point is where the two lines meet.

If some end point is exactly on the other line, the segments can still touch. They touch only if that end point is also between the end points of the other segment. If all four end points are on one line, the segments are two intervals on that line. Then the common part is where the two intervals overlap, which can be empty, a single point or a piece of the line.

## The problem

The input is four points $a, b, c, d$ with integer or rational coordinates. The segment $[a, b]$ is the set $\{a + t(b - a) : 0 \le t \le 1\}$, closed, and it is the single point $a$ when $a = b$. The output is $[a, b] \cap [c, d]$, which is a convex set: empty, a point $p$, or a segment $[p, q]$ with $p < q$.

Notation: points are $p = (x, y)$. For vectors $u, w$ let $u \times w = u_x w_y - u_y w_x$ (the [cross product](/cross-product/)). $\mathrm{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$: positive when $p, q, r$ turn counterclockwise, zero when they are collinear, negative for a clockwise turn. We compare points lexicographically: $p < q$ when $p_x < q_x$, or $p_x = q_x$ and $p_y < q_y$. The box of $p$ and $q$ is the smallest axis-parallel rectangle that contains them. No [general position](/general-position/) is assumed.

## The algorithm

```pseudo id=main
SEGMENT-INTERSECTION(a, b, c, d)
L1  d1 ← orient(c, d, a); d2 ← orient(c, d, b); d3 ← orient(a, b, c); d4 ← orient(a, b, d)
L2  if d1 · d2 < 0 and d3 · d4 < 0 then
L3      t ← ((c − a) × (d − c)) / ((b − a) × (d − c))
L4      return the point a + t(b − a)
L5  if d1 = d2 = d3 = d4 = 0 then
L6      lo ← max(min(a, b), min(c, d)); hi ← min(max(a, b), max(c, d))
L7      if lo > hi then return nothing
L8      if lo = hi then return the point lo
L9      return the segment [lo, hi]
L10 if d1 = 0 and a is in the box of c, d then return the point a
L11 if d2 = 0 and b is in the box of c, d then return the point b
L12 if d3 = 0 and c is in the box of a, b then return the point c
L13 if d4 = 0 and d is in the box of a, b then return the point d
L14 return nothing
```

Line L1 computes the four signs. The test of line L2 is the proper crossing: $a$ and $b$ are strictly on opposite sides of the line $cd$, and $c$ and $d$ strictly on opposite sides of the line $ab$. Line L3 finds the parameter $t$ of the crossing on $[a, b]$ by solving $(d - c) \times (a + t(b - a) - c) = 0$, which is the [line-line intersection](/line-line-intersection/) of the two supporting lines. With rational input, $t$ is a rational number, so the point is exact.

When all four signs are zero (line L5), the four points are on one line. On a line, the lexicographic order is the order along the line, so each segment is an interval from its smaller end point to its larger one, and lines L6 to L9 intersect the two intervals. In all other cases the segments meet in at most one point, and that point is an end point. Lines L10 to L13 test each end point: it is on the other segment exactly when it is on the other line and in the box of the other segment.

## Example

The table shows eight pairs of segments, the signs of line L1 and the line that returns.

| $[a, b]$ | $[c, d]$ | $d_1, d_2, d_3, d_4$ | line | result |
| --- | --- | --- | --- | --- |
| (0,0)-(3,1) | (0,1)-(3,0) | $-, +, +, -$ | L4 | point $(3/2, 1/2)$, with $t = (-3)/(-6) = 1/2$ |
| (0,0)-(4,0) | (2,0)-(2,5) | $+, -, 0, +$ | L12 | point $(2, 0)$, an end point inside the other segment |
| (0,0)-(1,1) | (1,1)-(2,0) | $-, 0, 0, -$ | L11 | point $(1, 1)$, a shared end point |
| (0,0)-(4,4) | (2,2)-(6,6) | $0, 0, 0, 0$ | L9 | segment $(2,2)$-$(4,4)$ |
| (0,0)-(1,1) | (2,2)-(3,3) | $0, 0, 0, 0$ | L7 | nothing: $lo = (2,2) > hi = (1,1)$ |
| (1,0)-(1,5) | (1,3)-(1,9) | $0, 0, 0, 0$ | L9 | segment $(1,3)$-$(1,5)$, both vertical |
| (0,0)-(1,0) | (2,1)-(2,5) | $+, +, +, +$ | L14 | nothing: the lines meet outside both segments |
| (0,0)-(2,2) | (0,1)-(2,3) | $-, -, +, +$ | L14 | nothing: parallel lines |

In the second row, $d_3 = 0$ says that $c = (2, 0)$ is on the line through $a$ and $b$, and the box test says it is between them.

## Correctness

There are three cases. If line L2 holds, each segment meets the line of the other in exactly one interior point, and the two lines are not parallel, so the crossing is a single point and line L3 finds it. If all four signs are zero, the four points are on one line, the segments are intervals in the lexicographic order of that line, and lines L6 to L9 return the intersection of the intervals. In every other case the segments cannot share a segment of positive length (that would make all four signs zero), and a common point cannot be interior to both segments (that would make line L2 hold). So the common part is empty or one end point, and lines L10 to L13 find it. The full proof is in the correctness proof below.

## Complexity

- **Time.** $\Theta(1)$: four orientation tests of two multiplications each, at most one division for the crossing, and a constant number of comparisons. This holds on the [real RAM](/real-ram/) and also for fixed-width integer input with exact arithmetic of bounded width.
- **Space.** $\Theta(1)$.
- **Size of the numbers.** With integer coordinates of absolute value at most $M$, each cross product has absolute value at most $8M^2$, so the signs need integers about twice as wide as the input. The crossing point has a denominator of absolute value at most $8M^2$ and numerators of order $M^3$. Python integers and `fractions.Fraction` handle this with no extra care.

## Properties

- **Exact.** The decisions use only signs of degree-2 polynomials in the input. Only the crossing point needs a division.
- **Symmetric.** Exchanging the segments, or the two end points of a segment, gives the same set.
- **Total.** Every input has an answer, including segments of length zero, which act as points.
- **Closed segments.** End points count. For open segments, change the tests of lines L10 to L13 to strict inequalities and drop the touching cases.

## Variants and improvements

- **Yes or no only.** For a boolean test, return true at line L2, false at the end, and drop the division. This is SEGMENTS-INTERSECT of Cormen et al., the predicate of the [Shamos-Hoey algorithm](/shamos-hoey-algorithm/).
- **Parametric form.** O'Rourke solves for both parameters $s$ and $t$ with one common denominator and classifies the result by the ranges of $s$ and $t$. It needs the same exact arithmetic and a separate path for parallel segments.
- **Homogeneous coordinates.** The supporting lines are the cross products of the homogeneous end points, and their meet is the cross product of the two lines. This avoids division until the end; see [line representation](/line-representation/).
- **Segment against a line or a ray.** Drop the tests $d_3, d_4$ for a full line, or replace them by a sign of $t$ for a ray.

## When to use it

Use it whenever two segments must be compared: in sweeps for [segment intersection detection](/segment-intersection-detection/) and [reporting](/all-segment-intersections/), in [polygon clipping](/polygon-clipping/), in [polygon simplicity tests](/polygon-simplicity-test/) and in the edge tests of [convex polygon intersection](/convex-polygon-intersection/). With floats and no need for robustness, the same structure works with rounded arithmetic, but then use an exact or adaptive orientation predicate such as [Shewchuk's expansion arithmetic](/shewchuk-expansion-sum/) for the signs.

## Pitfalls

- **Only the proper-crossing test.** Code that stops after line L2 misses T-junctions, shared end points and collinear overlaps. Keep lines L5 to L13.
- **Collinear case by the $x$-coordinate only.** Two vertical collinear segments have equal $x$-ranges whatever their $y$-ranges. Compare the points lexicographically, as in line L6, or compare both coordinates.
- **The box test without $d = 0$.** In lines L10 to L13, a point in the box of the other segment need not be on it. The orientation must be zero too.
- **Floating-point signs with a tolerance.** With floats, testing $|d_i| < \varepsilon$ makes the four tests inconsistent: one test can say collinear while another says the point is strictly on one side. Use integers or `fractions.Fraction`, or an exact predicate.
- **Dividing when the segments are parallel.** The denominator of line L3 is zero for parallel lines. Line L3 runs only after the test of line L2, which rules this out.

## Implementations

## History

The four-sign test is old folklore of computer graphics and of the geometry of polygons. Shamos and Hoey used the pairwise test as the predicate of their sweep in 1976, and Bentley and Ottmann used the same primitive to compute the crossing points in 1979. The textbook forms are SEGMENTS-INTERSECT of Cormen, Leiserson, Rivest and Stein, which handles the touching cases with an on-segment check, and the parametric SegSegInt of O'Rourke, which also returns the overlap of collinear segments.

## References
