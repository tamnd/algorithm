---
tag: BE5K54
kind: concept
slug: convex-hull-property
name: Convex hull property of Bezier and B-spline curves
aliases:
- convex hull property
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: A curve whose basis functions are nonnegative and sum to 1 lies in the convex hull of its control points. Each B-spline span lies in the hull of its p + 1 active points.
prereqs: [control-points, convex-hull, convex-combination]
see_also: [variation-diminishing-property, partition-of-unity, b-spline, rational-bezier-curve, bezier-clipping, curve-intersection, bezier-triangle, axis-aligned-bounding-box]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 4, The de Casteljau Algorithm, and Chapter 5, The Bernstein Form of a Bezier Curve (the convex hull property), Chapter 8, B-Spline Curves, and Chapter 13, Rational Bezier and B-Spline Curves
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Section 2.2, Bezier representation (page 11), and the chapters on B-splines and rational curves
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: the lists of properties of the B-spline basis functions and of B-spline and NURBS curves (the strong convex hull property)
---

The convex hull property says that a curve $C(t) = \sum_i P_i N_i(t)$ lies in the [convex hull](/convex-hull/) of its [control points](/control-points/) when the basis functions $N_i$ are nonnegative and sum to 1 at each parameter. Bézier curves on $[0, 1]$, B-spline curves on their valid domain and rational curves with positive weights all have it. For a B-spline curve of degree $p$ the bound is local: each span lies in the hull of its $p + 1$ active control points. The property gives bounds on a curve without any evaluation, and these bounds drive clipping, culling and intersection methods.

## In plain words

Put pins in a board at the control points and stretch a rubber band around all of them. The curve never leaves the region inside the band. This is so because each point of the curve is an average of the control points with weights that are never negative.

For a B-spline curve the rule is stronger. Each short piece of the curve depends only on a few neighbor points, so the piece stays inside the band around those few points. If these few points are on one straight line, the piece is a straight segment.

The rule says where the curve can be. It says nothing about how often the curve bends back and forth inside that region. That is a different property.

## The idea

**The general fact.** Let $N_0, \dots, N_n$ be functions on a domain $D$ with $N_i(t) \ge 0$ and $\sum_i N_i(t) = 1$ for each $t \in D$. Then for each $t \in D$, $C(t) = \sum_i P_i N_i(t)$ is a [convex combination](/convex-combination/) of $P_0, \dots, P_n$, so it is in their convex hull. Both conditions are needed. Without nonnegativity, a weight can be negative and the point leaves the hull. Without the sum 1, the combination is not affine, and the curve depends on the choice of origin.

**Bézier curves.** The [Bernstein polynomials](/bernstein-polynomials/) $B_i^n(t) = \binom{n}{i} t^i (1 - t)^{n-i}$ are nonnegative on $[0, 1]$, and they sum to $(t + 1 - t)^n = 1$. So the part of a [Bézier curve](/bezier-curve/) on $[0, 1]$ lies in the hull of all $n + 1$ control points. Outside $[0, 1]$ some $B_i^n$ are negative, and the extended curve leaves the hull.

**B-spline curves.** For a nondecreasing [knot vector](/knot-vector/) $u_0, \dots, u_{n+p+1}$, the [B-splines](/b-spline/) $N_{i,p}$ of the [Cox-de Boor recursion](/cox-de-boor-recursion/) are nonnegative, and they form a [partition of unity](/partition-of-unity/) on $[u_p, u_{n+1})$. On a span $[u_k, u_{k+1})$ with $p \le k \le n$, only $N_{k-p,p}, \dots, N_{k,p}$ are nonzero. So the restriction of the curve to this span is a convex combination of the $p + 1$ points $P_{k-p}, \dots, P_k$, and it lies in their hull. This is the strong convex hull property. The whole curve lies in the union of these $n - p + 1$ small hulls, which can be much smaller than the hull of all points. On parameters outside $[u_p, u_{n+1}]$ the sum can be less than 1, and the bound can fail.

**Rational curves.** A [rational Bézier curve](/rational-bezier-curve/) or a [NURBS](/nurbs/) curve is $C(t) = \sum_i w_i P_i N_i(t) / \sum_j w_j N_j(t)$. Its basis functions $w_i N_i / \sum_j w_j N_j$ sum to 1. They are nonnegative for all weights $w_i > 0$, so the property holds with positive weights. A negative weight can move the curve out of the hull, as an example below shows.

**Smaller hulls under refinement.** The control points of the two halves from the [de Casteljau algorithm](/de-casteljau-algorithm/) are convex combinations of the old points, so the new hulls are inside the old one. Under repeated subdivision the hulls shrink towards the curve: the distance of the control points from the curve falls by a factor of about 4 per halving (see [curve generation from a control polygon](/curve-from-control-polygon/)). Degree elevation and knot insertion also give smaller hulls.

**The function form.** For a polynomial $f(t) = \sum_i c_i B_i^n(t)$, the property applied to the points $(i/n, c_i)$ gives $\min_i c_i \le f(t) \le \max_i c_i$ on $[0, 1]$, and more: the graph of $f$ lies in the hull of the points $(i/n, c_i)$. So if all $c_i > 0$, $f$ has no root in $[0, 1]$.

**A different property.** The [variation diminishing property](/variation-diminishing-property/) bounds the number of times the curve crosses a line, not the region that it fills. A curve can have the convex hull property and not the variation diminishing property, as the last example shows. Both hold for Bézier and B-spline curves, but they have different proofs: convexity for this one, total positivity or corner cutting for the other.

## Examples

- **A quadratic.** The control points $(0, 0), (1, 2), (2, 0)$ give the arch $B(t) = (2t, 4t(1 - t))$. Its top $(1, 1)$ is inside the triangle of the points. The bounding box of the control points is $[0, 2] \times [0, 2]$, but the curve fills only $[0, 2] \times [0, 1]$, so the bound is valid and not tight. One split at $t = 1/2$ gives the polygons $(0, 0), (1/2, 1), (1, 1)$ and $(1, 1), (3/2, 1), (2, 0)$, with the boxes $[0, 1] \times [0, 1]$ and $[1, 2] \times [0, 1]$, which are tight in height.
- **Outside the domain.** The same polynomial at $t = 2$ gives $B(2) = (4, -8)$, because $B_1^2(2) = -4$ is negative. The point is far outside the triangle.
- **A straight B-spline span.** Take a cubic B-spline curve in which the four points $P_{k-3}, \dots, P_k$ of one span are on a line. The hull of the four points is a segment, so the span is a straight segment, while the neighbor spans can bend. This is how designers put a straight part into a smooth spline curve.
- **A quadratic B-spline knot point.** With the knots $0, 0, 0, 1, 2, 2, 2$ and the points $P_0 = (0, 0)$, $P_1 = (2, 0)$, $P_2 = (2, 2)$, $P_3 = (4, 2)$, the span $[0, 1)$ is in the triangle $P_0 P_1 P_2$ and the span $[1, 2]$ is in the triangle $P_1 P_2 P_3$. The point at $u = 1$ is $(P_1 + P_2)/2 = (2, 1)$, which is in both triangles.
- **A negative weight.** The rational quadratic with the points $(1, 0), (1, 1), (0, 1)$ and the weights $1, -1/2, 1$ has the denominator $1 - 3t + 3t^2 > 0$. At $t = 1/2$ the numerator is $\frac14 (1, 0) - \frac14 (1, 1) + \frac14 (0, 1) = (0, 0)$ and the denominator is $\frac14$, so $C(1/2) = (0, 0)$. The hull is the triangle with $x + y \ge 1$, and $(0, 0)$ is outside it.
- **Hull without variation diminishing.** Use the basis $(1 - t)^2, t^2, 2t(1 - t)$ for the points $P_0 = (0, 0)$, $P_1 = (2, 0)$, $P_2 = (1, 2)$, in this order. The basis is nonnegative and sums to 1, so the curve is in the hull, and it is the arch through $(0, 0)$, $(1, 1)$, $(2, 0)$. The line $y = 1/2$ crosses the polygon $P_0 P_1 P_2$ once, on the edge $P_1 P_2$, but it crosses the curve twice.

## Where it is used

- **Culling and bounds.** A box or a hull of the control points bounds the curve, the [Bézier patch](/bezier-patch/) or the [Bézier triangle](/bezier-triangle/). Ray tracers and collision tests reject a patch when the ray or the object misses its [bounding box](/axis-aligned-bounding-box/).
- **Intersection by subdivision.** If the hulls of two curves are disjoint, the curves do not meet. Subdivision methods for [curve intersection](/curve-intersection/) split the curves until the boxes are disjoint or small.
- **Bézier clipping.** [Bézier clipping](/bezier-clipping/) uses the hull of the points $(i/n, d_i)$ of a distance function to cut away parameter ranges in which no root can be.
- **Root finding.** For a polynomial in Bernstein form, coefficients of one sign show that there is no root in $[0, 1]$, and the hull of $(i/n, c_i)$ gives an interval that contains all roots.
- **Design.** A designer can see a safe region for the curve from the control polygon alone, and straight or flat parts follow from collinear or coplanar points.

## References
