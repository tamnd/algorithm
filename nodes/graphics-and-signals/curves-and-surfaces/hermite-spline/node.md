---
tag: V6BWHE
kind: definition
slug: hermite-spline
name: Hermite spline
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: A parametric curve made of cubic segments. Each segment is fixed by its two end points and its two end tangent vectors, so the curve passes through the points and is C1.
prereqs: [parametric-curve]
see_also: [cubic-hermite-spline, hermite-interpolation, catmull-rom-spline, kochanek-bartels-spline, natural-cubic-spline, bezier-curve, parametric-continuity, spline]
sources:
  - paper: doi:10.1145/321217.321225
    title: James Ferguson, Multivariable curve interpolation, Journal of the ACM 11(2), 221-228 (1964)
    locator: the parametric cubic segment fixed by end points and end tangents, used at Boeing for curves and surfaces
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 7, Polynomial Curve Constructions (cubic Hermite interpolation), and Chapter 9, Constructing Spline Curves (C1 piecewise cubic interpolation)
  - book: isbn:9780201848403
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition in C, Addison-Wesley, 1996
    locator: Chapter 11, Representing Curves and Surfaces (Hermite curves and the Hermite basis matrix)
---

A Hermite spline is a [parametric curve](/parametric-curve/) in the plane or in space made of cubic segments. Each segment is fixed by four vectors: its start point, its end point, and the tangent vectors at the two ends. Two adjacent segments share the end point and the tangent, so the curve passes through every given point and its first derivative is continuous. The segment form goes back to Ferguson at Boeing (1964), and it is the common form behind the [Catmull-Rom spline](/catmull-rom-spline/), the [Kochanek-Bartels spline](/kochanek-bartels-spline/) and the [natural cubic spline](/natural-cubic-spline/), which differ only in how they choose the tangents. The page [cubic Hermite spline](/cubic-hermite-spline/) in the numerical area treats the function case: a graph $y = f(x)$ with given or estimated slopes, where the parameter is the coordinate $x$. This page treats the geometric case. The values are points in $\mathbb{R}^d$, the parameter is not a coordinate, the curve can turn back and cross itself, and the tangents are vectors whose length changes the shape.

## Definition

**Hermite segment.** Let $p_0, p_1 \in \mathbb{R}^d$ be points and $m_0, m_1 \in \mathbb{R}^d$ be vectors. The cubic Hermite segment is

$$C(u) = H_0(u)\,p_0 + H_1(u)\,m_0 + H_2(u)\,m_1 + H_3(u)\,p_1, \qquad u \in [0, 1],$$

with the cubic Hermite basis

$$H_0(u) = 2u^3 - 3u^2 + 1, \quad H_1(u) = u^3 - 2u^2 + u, \quad H_2(u) = u^3 - u^2, \quad H_3(u) = -2u^3 + 3u^2 .$$

It is the unique polynomial curve of degree at most 3 with $C(0) = p_0$, $C(1) = p_1$, $C'(0) = m_0$ and $C'(1) = m_1$. Proof: write $C(u) = a + bu + cu^2 + eu^3$ with vector coefficients. The four conditions are $a = p_0$, $b = m_0$, $a + b + c + e = p_1$ and $b + 2c + 3e = m_1$. This system has the unique solution

$$a = p_0, \quad b = m_0, \quad c = 3(p_1 - p_0) - 2m_0 - m_1, \quad e = -2(p_1 - p_0) + m_0 + m_1,$$

and collecting the terms in $p_0, m_0, m_1, p_1$ gives the four basis functions. Each basis function has exactly one of the four end values equal to 1 and the others equal to 0, which is the defining property of a Hermite basis.

**Hermite spline.** Let $t_0 < t_1 < \dots < t_n$ be knots, $P_0, \dots, P_n$ points and $D_0, \dots, D_n$ tangent vectors, where $D_i$ is the derivative $dC/dt$ at $t_i$. On $[t_i, t_{i+1}]$, with $h_i = t_{i+1} - t_i$ and local parameter $u = (t - t_i)/h_i$, the spline is the Hermite segment with

$$p_0 = P_i, \quad p_1 = P_{i+1}, \quad m_0 = h_i D_i, \quad m_1 = h_i D_{i+1} .$$

The factor $h_i$ comes from the chain rule: $dC/dt = (1/h_i)\, dC/du$. With this factor, both segments that meet at $t_i$ have the derivative $D_i$ there, so the spline is $C^1$ in $t$ (see [parametric continuity](/parametric-continuity/)). Many texts use $h_i = 1$ for all $i$, and then $D_i$ is the tangent in the local parameter.

**Properties that follow from the definition.**

- *Interpolation.* $C(t_i) = P_i$ for every $i$.
- *Locality.* The data $P_i, D_i$ enter only the two segments that meet at $t_i$.
- *Second derivatives.* In the local parameter, $C''(0) = 6(p_1 - p_0) - 4m_0 - 2m_1$ and $C''(1) = -6(p_1 - p_0) + 2m_0 + 4m_1$. In general the values from the two sides of a knot differ, so a Hermite spline is $C^1$ but not $C^2$. Asking them to be equal at every inner knot gives a linear system for the tangents. With the end conditions $C'' = 0$ this system defines the [natural cubic spline](/natural-cubic-spline/).
- *Bézier form.* The same segment is the cubic [Bézier curve](/bezier-curve/) with control points

$$b_0 = p_0, \quad b_1 = p_0 + \tfrac{1}{3} m_0, \quad b_2 = p_1 - \tfrac{1}{3} m_1, \quad b_3 = p_1,$$

because a cubic Bézier curve has $C'(0) = 3(b_1 - b_0)$ and $C'(1) = 3(b_3 - b_2)$. So each segment lies in the convex hull of these four points (see [convex hull property](/convex-hull-property/)), but not in general in the hull of the data $p_0, p_1$ alone.
- *Affine invariance.* $H_0 + H_3 = 1$, so the point weights sum to 1 and the tangent weights do not enter the sum. If $x \mapsto Ax + v$ is an affine map, the segment of the mapped data ($Ap_0 + v$, $Ap_1 + v$, $Am_0$, $Am_1$) is the image of the segment. Tangents are vectors and take only the linear part $A$.
- *Signs.* $H_0$, $H_3$ and $H_1 = u(1-u)^2$ are nonnegative on $[0, 1]$, and $H_2 = -u^2(1-u)$ is not positive. The basis is not a partition of unity with nonnegative weights, and the segment is not an average of its data.
- *Spline space.* The $C^1$ piecewise cubics with breaks $t_0, \dots, t_n$ form a space of dimension $2(n + 1)$: two values per knot. It is the space of cubic [B-splines](/b-spline/) with every inner knot of multiplicity 2, by the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/).

**Matrix form.** With the row vector $U = (1, u, u^2, u^3)$,

$$C(u) = U \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ -3 & -2 & -1 & 3 \\ 2 & 1 & 1 & -2 \end{pmatrix} \begin{pmatrix} p_0 \\ m_0 \\ m_1 \\ p_1 \end{pmatrix} .$$

The cost of one point is $O(d)$ for $d$ coordinates, after a search for the span $[t_i, t_{i+1}]$ that takes $O(\log n)$ time by binary search.

## Examples and non-examples

**An arch.** Take $p_0 = (0, 0)$, $p_1 = (4, 0)$, $m_0 = (0, 6)$ and $m_1 = (0, -6)$. At $u = 1/2$ the basis values are $H_0 = 1/2$, $H_1 = 1/8$, $H_2 = -1/8$ and $H_3 = 1/2$, so

$$C(1/2) = \tfrac12 (0, 0) + \tfrac18 (0, 6) - \tfrac18 (0, -6) + \tfrac12 (4, 0) = (2, 1.5),$$

and $C'(1/2) = (6, 0)$: the top of the arch, moving to the right. The Bézier control points are $(0, 0)$, $(0, 2)$, $(4, 2)$ and $(4, 0)$. If both tangents are doubled to $(0, 12)$ and $(0, -12)$, the top moves to $(2, 3)$. The directions are the same and the curve is different: the length of a tangent is part of the shape.

**A quarter circle.** The data $p_0 = (1, 0)$, $p_1 = (0, 1)$, $m_0 = (0, k)$, $m_1 = (-k, 0)$ with $k = 4(\sqrt2 - 1) \approx 1.65685$ give the usual cubic approximation of a quarter of the unit circle. Its Bézier points are at distance $k/3 \approx 0.55228$ from the ends. The midpoint $C(1/2) = (\sqrt2/2, \sqrt2/2)$ is on the circle. The distance from the origin is never exactly 1 elsewhere in the open interval. The largest radial error, over 100001 equally spaced samples, is $2.73 \times 10^{-4}$, near $u \approx 0.2113$ and at the symmetric point. No polynomial curve is exactly a circle (see [parametric curve](/parametric-curve/)).

**A knot where $C^2$ fails.** Take knots $0, 1, 2$, points $(0, 0)$, $(1, 1)$, $(2, 1)$ and tangents $(1, 1)$, $(1, 0)$, $(1, 0)$. At $t = 1$ the left segment has $C'' = -6(1, 1) + 2(1, 1) + 4(1, 0) = (0, -4)$ and the right segment has $C'' = 6(1, 0) - 4(1, 0) - 2(1, 0) = (0, 0)$. The position and the first derivative agree, and the second derivative jumps. The curvature jumps with it.

**Non-example: unscaled tangents.** Take knots $0, 1, 3$, so $h_0 = 1$ and $h_1 = 2$, and use $m_0 = D_i$ and $m_1 = D_{i+1}$ in both segments without the factor $h_i$. Then the left segment has $dC/dt = D_1$ at $t = 1$ and the right segment has $dC/dt = D_1/2$. The direction agrees and the speed halves, so the curve is $G^1$ but not $C^1$ in $t$. An animation along it changes speed with a jolt at the knot.

**Non-example: zero tangents.** If all $D_i = 0$, each segment is the straight line from $P_i$ to $P_{i+1}$, traversed with zero speed at both ends. The derivative is continuous (it is 0 at each knot), but the curve has corners at the inner points. A $C^1$ parametrization does not give a smooth trace unless the derivative is not zero. This is the reason for the regularity condition in [parametric continuity](/parametric-continuity/).

## Related definitions

- [Cubic Hermite spline](/cubic-hermite-spline/) in numerical analysis: the same basis for a function $y = f(x)$, with the slopes estimated from the data (for example the monotone PCHIP rule). The parameter there is the coordinate.
- [Hermite interpolation](/hermite-interpolation/): the general problem of matching values and derivatives, of which one segment is the case with two nodes and one derivative.
- [Catmull-Rom spline](/catmull-rom-spline/): the tangent at $P_i$ is half the chord $P_{i+1} - P_{i-1}$.
- [Kochanek-Bartels spline](/kochanek-bartels-spline/): tangents with tension, continuity and bias parameters, and different incoming and outgoing tangents.
- [Natural cubic spline](/natural-cubic-spline/): the tangents that make the curve $C^2$ with zero second derivative at the ends, from a tridiagonal system.
- [Bézier curve](/bezier-curve/): the same cubic with the control points $p_0$, $p_0 + m_0/3$, $p_1 - m_1/3$, $p_1$.
- [Parametric continuity](/parametric-continuity/): the $C^k$ and $G^k$ conditions at a joint.
- [Curve interpolation](/curve-interpolation/): the problem of passing a curve through points, which Hermite splines solve once the parameter values and the tangents are chosen.

## References
