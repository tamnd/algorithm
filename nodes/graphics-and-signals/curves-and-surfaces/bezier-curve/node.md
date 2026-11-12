---
tag: J18ZK3
kind: definition
slug: bezier-curve
name: Bezier curve
aliases:
- Bézier curve
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: The polynomial curve sum P_i B_i^n(t) on [0, 1] with n + 1 control points P_i and the Bernstein basis of degree n. It starts at P_0, ends at P_n, and is tangent to the polygon there.
prereqs: [bernstein-polynomials, parametric-curve]
see_also: [control-points, de-casteljau-algorithm, rational-bezier-curve, b-spline, bezier-patch, convex-hull-property, hermite-spline, curve-evaluation]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 1, Bezier, How a Simple System Was Born (the history at Renault and Citroen), Chapter 5, The Bernstein Form of a Bezier Curve (derivatives, end conditions, affine invariance), and Chapter 6, Bezier Curve Topics (degree elevation)
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Section 2.2, Bezier representation (page 11), Section 2.4, Derivatives (page 15), and Section 3.11, Degree elevation (page 37)
  - paper: doi:10.1016/S0167-8396(99)00024-2
    title: Paul de Faget de Casteljau, De Casteljau's autobiography, My time at Citroen, Computer Aided Geometric Design 16(7), 583-586 (1999)
    locator: his work on curves defined by poles at Citroen from 1959
  - paper: doi:10.1016/j.cagd.2012.03.001
    title: Rida T. Farouki, The Bernstein polynomial basis, a centennial retrospective, Computer Aided Geometric Design 29(6), 379-419 (2012)
    locator: the parallel work of de Casteljau at Citroen and Bezier at Renault, and the Bernstein form of the curves
---

A Bézier curve of degree $n$ is the [parametric curve](/parametric-curve/) $B(t) = \sum_{i=0}^n P_i B_i^n(t)$, $t \in [0, 1]$, where $P_0, \dots, P_n$ are $n + 1$ points called [control points](/control-points/) and $B_i^n$ are the [Bernstein polynomials](/bernstein-polynomials/). The curve starts at $P_0$, ends at $P_n$, and in general does not pass through the inner points, which pull it into shape. Paul de Casteljau at Citroën and Pierre Bézier at Renault developed these curves for car body design around 1960. Today they are the curve pieces of fonts, vector graphics and CAD.

## Definition

Let $n \ge 0$ and let $P_0, \dots, P_n$ be points of $\mathbb{R}^d$, usually with $d = 2$ or $d = 3$. The Bézier curve with these control points is

$$B(t) = \sum_{i=0}^{n} P_i \binom{n}{i} t^i (1 - t)^{n-i}, \qquad t \in [0, 1].$$

The polygon $P_0 P_1 \cdots P_n$ is the control polygon. The number $n$ is the degree of the representation; each coordinate of $B$ is a polynomial of degree at most $n$. The degree is exactly $n$ when the leading coefficient $\sum_i (-1)^{n-i} \binom{n}{i} P_i$, the $n$-th forward difference $\Delta^n P_0$, is not zero. By property 7 of the [Bernstein basis](/bernstein-polynomials/), every polynomial curve of degree at most $n$ has exactly one set of $n + 1$ control points for degree $n$.

The curve has these properties.

1. **End points.** $B(0) = P_0$ and $B(1) = P_n$, because $B_i^n(0)$ and $B_i^n(1)$ are 0 except for $i = 0$ and $i = n$.
2. **Derivative.** $B'(t) = n \sum_{i=0}^{n-1} (P_{i+1} - P_i) B_i^{n-1}(t)$. Proof: by the derivative rule of the basis, $B'(t) = n \sum_i P_i (B_{i-1}^{n-1} - B_i^{n-1})$; shift the index in the first sum. So the derivative is a Bézier curve of degree $n - 1$ (the hodograph) with the control vectors $n \Delta P_i = n (P_{i+1} - P_i)$.
3. **End tangents.** $B'(0) = n (P_1 - P_0)$ and $B'(1) = n (P_n - P_{n-1})$. The second derivative at 0 is $n (n - 1)(P_2 - 2P_1 + P_0)$. So the first $k + 1$ control points fix the derivatives of order up to $k$ at $t = 0$.
4. **Affine invariance.** For an affine map $A(x) = Mx + v$, $A(B(t)) = \sum_i A(P_i) B_i^n(t)$, because $\sum_i B_i^n(t) = 1$. So to move, turn or scale the curve, transform the control points. The same is false for a perspective map: the image of a Bézier curve under a projective map is a [rational Bézier curve](/rational-bezier-curve/).
5. **Convex hull.** For $t \in [0, 1]$, $B(t)$ is a convex combination of the control points, so the curve lies in their convex hull. See the [convex hull property](/convex-hull-property/).
6. **Symmetry.** The control points in the opposite order $P_n, \dots, P_0$ give the curve $B(1 - t)$: the same point set, traced backwards.
7. **Global control.** If $P_i$ moves by a vector $v$, then $B(t)$ moves by $v B_i^n(t)$, which is not zero for every $t \in (0, 1)$. One control point changes the whole curve. [B-splines](/b-spline/) give local control.
8. **Linear precision.** If $P_i = P_0 + \frac{i}{n}(P_n - P_0)$, then $B(t) = P_0 + t (P_n - P_0)$, by the identity $\sum_i \frac{i}{n} B_i^n(t) = t$.
9. **Degree elevation.** The same curve is the Bézier curve of degree $n + 1$ with the control points $Q_j = \frac{j}{n+1} P_{j-1} + \left(1 - \frac{j}{n+1}\right) P_j$ for $j = 0, \dots, n + 1$, where $P_{-1}$ and $P_{n+1}$ have coefficient 0. Proof: put the degree elevation identity of the basis into $\sum_i P_i B_i^n$ and collect the coefficient of $B_j^{n+1}$.

To compute points, tangents and the control points of a part of the curve, use the [de Casteljau algorithm](/de-casteljau-algorithm/). It costs $O(n^2)$ operations per point. The general problem is [curve evaluation](/curve-evaluation/).

## Examples and non-examples

- **A quadratic.** The control points $(0, 0), (1, 2), (2, 0)$ give $B(t) = (2t,\ 4t(1 - t))$. With $x = 2t$, this is the parabola arc $y = x(2 - x)$ for $x \in [0, 2]$. The top point is $B(1/2) = (1, 1)$, half way from the base to $P_1 = (1, 2)$. The end tangents are $2(P_1 - P_0) = (2, 4)$ and $2(P_2 - P_1) = (2, -4)$.
- **A cubic.** The control points $(0, 0), (1, 2), (3, 2), (4, 0)$ give $B(1/2) = (2, 3/2)$, $B(1/4) = (29/32, 9/8)$ and $B'(1/4) = (33/8, 3)$. The end tangents are $(3, 6)$ and $(3, -6)$. The trace of these numbers is on the [de Casteljau algorithm](/de-casteljau-algorithm/) page.
- **Cubic Hermite data.** A cubic with end points $p_0, p_1$ and end derivatives $m_0, m_1$ has the control points $p_0,\ p_0 + m_0/3,\ p_1 - m_1/3,\ p_1$, by property 3. This converts a [Hermite spline](/hermite-spline/) or a [Catmull-Rom spline](/catmull-rom-spline/) piece to Bézier form.
- **In practice.** TrueType glyph outlines use quadratic pieces. PostScript Type 1 and CFF outlines use cubic pieces. The SVG path commands Q and C draw quadratic and cubic Bézier curves.
- **Non-example: a circle arc.** No arc of a circle is a Bézier curve of any degree. Proof: let $x(t), y(t)$ be polynomials, not both constant, with $x^2 + y^2 = r^2$ on $[0, 1]$. Then the identity holds for all $t$, because a polynomial with infinitely many roots is zero. Let $m = \max(\deg x, \deg y) \ge 1$, and let $a, b$ be the coefficients of $t^m$ in $x$ and $y$, not both 0. The coefficient of $t^{2m}$ in $x^2 + y^2$ is $a^2 + b^2 > 0$, but $r^2$ is a constant. A rational Bézier curve gives the arc exactly; see [rational Bézier curve](/rational-bezier-curve/).
- **The usual cubic arc is an approximation.** The cubic with control points $(1, 0), (1, k), (k, 1), (0, 1)$ and $k = 4(\sqrt 2 - 1)/3 \approx 0.55228$ meets the unit circle at $t = 0, 1/2, 1$. Between these parameters it is outside the circle, and its largest distance from the center is about $1.000273$, an error of about $2.7 \cdot 10^{-4}$ of the radius.
- **Non-example: points outside $[0, 1]$.** The same polynomial at $t = 2$ is a point of the extended curve, but it is not a convex combination of the control points. For the quadratic above, $B(2) = (4, -8)$, which is far outside the triangle of the control points.

## Related definitions

- [Bernstein polynomials](/bernstein-polynomials/): the basis. [Control points](/control-points/): the coefficients and the polygon, and what each one does.
- [Rational Bézier curve](/rational-bezier-curve/): a weighted ratio of two Bernstein forms. It gives conics exactly and is invariant under projective maps.
- [B-spline](/b-spline/) and [NURBS](/nurbs/): piecewise curves with local control. Each polynomial piece of a B-spline curve is a Bézier curve, and [knot insertion](/boehm-knot-insertion/) finds its control points.
- [Bézier patch](/bezier-patch/) and [Bézier triangle](/bezier-triangle/): the surfaces of the same construction, a tensor product and a triangular form.
- [Spline](/spline/) and [parametric continuity](/parametric-continuity/): joined Bézier pieces with $C^1$ continuity need $P_n - P_{n-1}$ of one piece equal to $Q_1 - Q_0$ of the next (for equal parameter lengths), by property 3.

## References
