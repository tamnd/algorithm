---
tag: Q254YN
kind: concept
slug: control-points
name: Control points
aliases:
- control polygon
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: The points whose weighted average with a nonnegative basis gives a Bezier, B-spline or NURBS curve. They shape the curve, and in general it does not pass through the inner ones.
prereqs: [bezier-curve]
see_also: [curve-from-control-polygon, b-spline, nurbs, knot-vector, convex-hull-property, variation-diminishing-property, curve-interpolation, bezier-patch]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 4, The de Casteljau Algorithm, Chapter 5, The Bernstein Form of a Bezier Curve, Chapter 6, Bezier Curve Topics (degree elevation), and Chapter 8, B-Spline Curves
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Section 2.2, Bezier representation (page 11), Section 3.4, Convergence under subdivision (page 29), and Section 3.11, Degree elevation (page 37)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 1 (Bezier and rational Bezier curves), Chapter 3 (B-spline curves and the local effect of a control point) and Chapter 4 (NURBS curves and the effect of a weight)
---

Control points are the coefficients of a curve or surface in a basis of nonnegative functions that sum to one, such as the [Bernstein polynomials](/bernstein-polynomials/) of a [Bézier curve](/bezier-curve/) or the [B-splines](/b-spline/) of a spline. The curve is a moving weighted average of these points, so it follows them, but in general it passes only through some of them. The points joined in order form the control polygon, and it is the main tool to design, bound and refine the curve. For a B-spline curve the control points are also called de Boor points.

## In plain words

Think of the control points as magnets on a table. The curve is a thin wire that starts at the first magnet and ends at the last one. Each magnet in between pulls the wire towards it, but the wire does not touch it. The magnets are joined by straight lines in order, and this broken line is the control polygon.

To change the shape, you move a magnet, and the wire follows. For a Bézier curve, one magnet pulls on the whole wire. For a B-spline, each magnet pulls only on a short part of it. The wire always stays inside the region that the magnets span, and it never wiggles across a straight line more often than the broken line does. If you cut the wire in two, each half gets its own set of magnets, and these sets lie closer to the wire than the old one.

## The idea

A curve of this kind has the form

$$C(t) = \sum_{i=0}^{n} P_i N_i(t),$$

where the $P_i$ are points and the basis functions $N_i$ are nonnegative on the parameter domain and sum to 1. The $P_i$ are the control points, and the polygon $P_0 P_1 \cdots P_n$ is the control polygon. For a surface, a grid or a mesh of points is the control net or control mesh.

- **Bézier.** $N_i = B_i^n$, the Bernstein polynomials of degree $n$. There are $n + 1$ control points, and the curve has degree at most $n$.
- **B-spline.** $N_i = N_{i,p}$, the B-splines of degree $p$ on a [knot vector](/knot-vector/) $u_0 \le \dots \le u_{n+p+1}$, so $n + 1$ control points need $n + p + 2$ knots. The $P_i$ are the de Boor points, after Carl de Boor.
- **NURBS.** Each control point also has a weight $w_i > 0$, and $C(t) = \sum_i w_i P_i N_i(t) / \sum_i w_i N_i(t)$. A larger $w_i$ pulls the curve towards $P_i$. See [NURBS](/nurbs/) and [rational Bézier curve](/rational-bezier-curve/).

The two conditions on the basis give the properties that make the points useful.

1. **The curve is a weighted average.** For each $t$, $C(t)$ is a convex combination of the $P_i$. So the curve lies in their convex hull ([convex hull property](/convex-hull-property/)), and an affine map of the plane maps the curve to the curve of the mapped points. To move, turn or scale a curve, transform its control points.
2. **The curve is a smoothed polygon.** The curve crosses a line at most as often as the control polygon does ([variation diminishing property](/variation-diminishing-property/)). So a convex control polygon gives a convex curve, and a monotone polygon gives a monotone curve.
3. **The ends are fixed.** For a Bézier curve and for a B-spline curve with $p + 1$ equal knots at each end, the curve starts at $P_0$ and ends at $P_n$, and it is tangent there to the first and the last edge of the polygon.
4. **The reach of one point.** Moving $P_i$ by a vector $v$ moves $C(t)$ by $v N_i(t)$. For a Bézier curve $B_i^n(t) > 0$ on all of $(0, 1)$, so one point changes the whole curve. For a B-spline $N_{i,p}$ is zero outside $[u_i, u_{i+p+1})$, so the point changes at most $p + 1$ spans. This is local control.
5. **The polygon is not unique.** The same curve has many control polygons. Degree elevation of a Bézier curve, [knot insertion](/boehm-knot-insertion/) in a B-spline and subdivision with the [de Casteljau algorithm](/de-casteljau-algorithm/) give new polygons with more points and the same curve. Under repeated subdivision or elevation, the polygons converge to the curve.

The control points are the object. The task of computing the curve, or a fine polygon close to it, from the control points is a separate problem: see [curve from control polygon](/curve-from-control-polygon/). The inverse task, to find control points for a curve that passes through given points, is [curve interpolation](/curve-interpolation/).

## Examples

- **The pull of one point.** The quadratic Bézier curve with $P_0 = (0, 0)$, $P_1 = (1, 2)$, $P_2 = (2, 0)$ has its top at $B(1/2) = (1, 1)$, only half way up to $P_1$. Move $P_1$ to $(1, 4)$. Then $B(1/2)$ moves by $(0, 2) \cdot B_1^2(1/2) = (0, 2) \cdot \frac12$, to $(1, 2)$.
- **Degree elevation.** The same quadratic is the cubic with the control points $(0, 0)$, $(2/3, 4/3)$, $(4/3, 4/3)$, $(2, 0)$, from $Q_j = \frac{j}{3} P_{j-1} + \left(1 - \frac{j}{3}\right) P_j$. The new inner points are lower than $P_1$, so the new polygon is closer to the curve.
- **Subdivision.** Split the quadratic at $t = 1/2$. The two halves have the control polygons $(0, 0), (1/2, 1), (1, 1)$ and $(1, 1), (3/2, 1), (2, 0)$. The middle point $(1, 1)$ is now a control point, and it is on the curve.
- **A uniform cubic B-spline.** With integer knots, the point where two spans of a cubic B-spline curve meet is $(P_{i-1} + 4 P_i + P_{i+1}) / 6$. For $P_{i-1} = (0, 0)$, $P_i = (3, 6)$ and $P_{i+1} = (6, 0)$, it is $(3, 4)$, below the de Boor point $(3, 6)$. Moving $P_i$ changes only the four spans that use it.
- **Animation timing.** The CSS function `cubic-bezier(x1, y1, x2, y2)` describes a timing curve by its two inner control points. The end points are fixed at $(0, 0)$ and $(1, 1)$.

## Where it is used

- **Design.** CAD systems and drawing programs show the control polygon, and the user drags its points. The "handles" of a cubic path in a drawing program are the two inner control points of each piece.
- **Fonts and vector graphics.** Glyph outlines and SVG paths store control points of quadratic or cubic pieces.
- **Bounds and culling.** The convex hull, or the bounding box of the control points, bounds the curve without any evaluation. [Bézier clipping](/bezier-clipping/) and subdivision methods for [curve intersection](/curve-intersection/) use these bounds.
- **Surfaces.** A [Bézier patch](/bezier-patch/) has a grid of control points, and a [subdivision surface](/subdivision-surface/) refines a control mesh.
- **Spline functions.** For a spline function, the control points are $(\xi_i, c_i)$, with the coefficients $c_i$ and the Greville abscissae $\xi_i$. The sign changes of the $c_i$ bound the roots of the function.

## References
