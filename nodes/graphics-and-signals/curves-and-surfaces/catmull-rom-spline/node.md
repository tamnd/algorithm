---
tag: SBH6DE
kind: definition
slug: catmull-rom-spline
name: Catmull-Rom spline
aliases:
- Catmull-Rom curve
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: An interpolating C1 cubic spline curve. It is a Hermite spline whose tangent at each point is set from the two neighbouring points, so each segment depends on four points only.
prereqs: [hermite-spline]
see_also: [kochanek-bartels-spline, natural-cubic-spline, four-point-scheme, curve-interpolation, parametric-continuity, bezier-curve, cubic-hermite-spline]
sources:
  - paper: doi:10.1016/B978-0-12-079050-0.50020-5
    title: Edwin Catmull and Raphael Rom, A class of local interpolating splines, in R. E. Barnhill and R. F. Riesenfeld (eds.), Computer Aided Geometric Design, Academic Press, New York, 1974, 317-326
    locator: pages 317-326, the class of local interpolating splines built by blending interpolating polynomials
  - paper: doi:10.1145/54852.378511
    title: Phillip J. Barry and Ronald N. Goldman, A recursive evaluation algorithm for a class of Catmull-Rom splines, Computer Graphics 22(4), 199-204 (SIGGRAPH 1988)
    locator: the pyramid of Neville steps and one de Boor step for nonuniform knots
  - paper: doi:10.1016/j.cad.2010.08.008
    title: Cem Yuksel, Scott Schaefer and John Keyser, Parameterization and applications of Catmull-Rom curves, Computer-Aided Design 43(7), 747-755 (2011)
    locator: the uniform, centripetal and chordal knot choices, and the proof that the centripetal choice has no cusps or self-intersections inside a segment
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 9, Constructing Spline Curves (C1 piecewise cubic interpolation with estimated tangents)
---

A Catmull-Rom spline is an interpolating cubic spline curve. It is a [Hermite spline](/hermite-spline/) in which the tangent at each data point is fixed by the two neighbouring points, so the user gives only the points. Each segment depends on four consecutive points, the curve passes through all the inner ones, and its first derivative is continuous. Edwin Catmull and Raphael Rom described it in 1974 in the volume *Computer Aided Geometric Design*, edited by Barnhill and Riesenfeld (Academic Press), as one member of a class of local interpolating splines. It is the standard path through key positions in animation and the standard way to draw a smooth curve through clicked points, because a change to one point moves only four segments and no system of equations is solved.

## Definition

**Uniform Catmull-Rom spline.** Let $P_0, P_1, \dots, P_n$ be points in $\mathbb{R}^d$ with $n \ge 3$. The curve has the segments $C_1, \dots, C_{n-2}$. Segment $C_i$ joins $P_i$ to $P_{i+1}$ for $u \in [0, 1]$, and it is the cubic Hermite segment with the tangents

$$m_i = \tfrac12 (P_{i+1} - P_{i-1}), \qquad m_{i+1} = \tfrac12 (P_{i+2} - P_i).$$

The first and the last point only set the end tangents: the curve runs from $P_1$ to $P_{n-1}$. In matrix form, with $U = (1, u, u^2, u^3)$,

$$C_i(u) = \tfrac12\, U \begin{pmatrix} 0 & 2 & 0 & 0 \\ -1 & 0 & 1 & 0 \\ 2 & -5 & 4 & -1 \\ -1 & 3 & -3 & 1 \end{pmatrix} \begin{pmatrix} P_{i-1} \\ P_i \\ P_{i+1} \\ P_{i+2} \end{pmatrix} .$$

So the weights of the four points are

$$w_{-1} = -\tfrac12 u(1-u)^2, \quad w_0 = \tfrac12(3u^3 - 5u^2 + 2), \quad w_1 = \tfrac12(-3u^3 + 4u^2 + u), \quad w_2 = -\tfrac12 u^2(1-u).$$

They sum to 1 for every $u$, so the curve is affine invariant.

**Nonuniform Catmull-Rom spline.** Give each point a knot, $t_0 < t_1 < \dots < t_n$. The tangent at $P_i$ is the derivative at $t_i$ of the quadratic that interpolates $P_{i-1}, P_i, P_{i+1}$ at $t_{i-1}, t_i, t_{i+1}$:

$$D_i = \frac{P_i - P_{i-1}}{t_i - t_{i-1}} - \frac{P_{i+1} - P_{i-1}}{t_{i+1} - t_{i-1}} + \frac{P_{i+1} - P_i}{t_{i+1} - t_i},$$

and segment $i$ is the Hermite segment on $[t_i, t_{i+1}]$ with the tangents $D_i$ and $D_{i+1}$ in the parameter $t$. With $t_i = i$ this gives $D_i = \frac12 (P_{i+1} - P_{i-1})$, the uniform case. The usual knot choice is

$$t_{i+1} - t_i = \lVert P_{i+1} - P_i \rVert^{\alpha},$$

with $\alpha = 0$ (uniform), $\alpha = 1/2$ (centripetal) or $\alpha = 1$ (chordal).

**Barry-Goldman evaluation.** Barry and Goldman (1988) showed that the nonuniform segment on $[t_1, t_2]$, with the four points $P_0, \dots, P_3$, is the top of a pyramid of linear interpolations. Write $L(A, B; a, b)(t) = \frac{b - t}{b - a} A + \frac{t - a}{b - a} B$. Then

$$A_k = L(P_{k-1}, P_k; t_{k-1}, t_k), \; k = 1, 2, 3, \qquad B_k = L(A_k, A_{k+1}; t_{k-1}, t_{k+1}), \; k = 1, 2,$$

$$C(t) = L(B_1, B_2; t_1, t_2).$$

The first two levels are Neville steps: $B_1$ and $B_2$ are the quadratics through $P_0, P_1, P_2$ and through $P_1, P_2, P_3$. The last level blends them with the weight of a de Boor step. The blend keeps the ends ($C(t_1) = B_1(t_1) = P_1$ and $C(t_2) = P_2$) and the end tangents of the two quadratics, which gives the formula for $D_i$ above.

**Properties.**

- *Interpolation and $C^1$.* $C_i(0) = P_i$ and $C_i(1) = P_{i+1}$. The segments that meet at $P_i$ both have the tangent $m_i$, so the curve is $C^1$ (see [parametric continuity](/parametric-continuity/)). It is not $C^2$ in general: the curvature can jump at a data point.
- *Locality.* Segment $i$ depends on $P_{i-1}, \dots, P_{i+2}$ only, so a change to one point changes at most four segments.
- *No convex hull property.* The weights $w_{-1}$ and $w_2$ are negative inside $(0, 1)$. The curve can leave the convex hull of its four points, unlike a [B-spline](/b-spline/) segment (see [convex hull property](/convex-hull-property/)).
- *Quadratic precision.* If the points are $P_k = Q(k)$ for a quadratic polynomial curve $Q$, the uniform spline is $Q$ itself. Proof: the central difference $\frac12 (Q(k+1) - Q(k-1))$ equals $Q'(k)$ for a quadratic, and a Hermite segment with exact end values and exact end derivatives reproduces every cubic, so it reproduces $Q$. The nonuniform spline has the same property for $P_k = Q(t_k)$, because its tangent is the derivative of the interpolating quadratic.
- *Cusps and loops.* For uniform knots a segment can form a loop or a cusp when the data points are spaced unevenly. Yuksel, Schaefer and Keyser (2011) proved that the centripetal choice $\alpha = 1/2$ is the only one in the family $\alpha \in [0, 1]$ that never gives a cusp or a self-intersection inside a segment.
- *Ends.* The curve does not reach $P_0$ and $P_n$. Common choices are a closed curve with indices taken modulo $n + 1$, a repeated end point ($P_{-1} = P_0$), or a reflected point ($P_{-1} = 2P_0 - P_1$).

## Examples and non-examples

**One segment.** Take $P_0 = (0, 0)$, $P_1 = (1, 1)$, $P_2 = (2, 1)$, $P_3 = (3, 0)$. The tangents are $m_1 = \frac12 ((2, 1) - (0, 0)) = (1, 0.5)$ and $m_2 = \frac12 ((3, 0) - (1, 1)) = (1, -0.5)$. At $u = 1/2$ the weights are $(-\frac1{16}, \frac9{16}, \frac9{16}, -\frac1{16})$, so

$$C_1(1/2) = -\tfrac1{16}(0, 0) + \tfrac9{16}(1, 1) + \tfrac9{16}(2, 1) - \tfrac1{16}(3, 0) = (1.5, 1.125).$$

The midpoint lies above the chord from $P_1$ to $P_2$, because the curve keeps the bend of its neighbours. The weights $(-1, 9, 9, -1)/16$ are the weights of the [four-point scheme](/four-point-scheme/) of Dubuc and Dyn, Levin and Gregory, which inserts this midpoint at each step of a subdivision.

**A loop from uneven spacing.** Take $P_0 = (-11, -6)$, $P_1 = (0, 0)$, $P_2 = (1, 0)$, $P_3 = (12, -6)$. The uniform tangents are $m_1 = (6, 3)$ and $m_2 = (6, -3)$, six times longer than the chord $P_1 P_2$. The middle segment runs out to the right, turns back and crosses itself near $(0.5, 0.30)$, at the parameters $u \approx 0.11$ and $u \approx 0.89$ (found by intersecting the edges of a polyline with 2000 edges). With centripetal knots ($t = 0, 3.540, 4.540, 8.080$) and with chordal knots ($t = 0, 12.530, 13.530, 26.060$) the same segment has no crossing. The long chords now have long parameter intervals, so the divided differences in $D_i$ make the tangents short.

**Quadratic data.** The points $Q(k) = (k, k^2)$ for $k = -1, 0, 1, 2$ give the segment $C(u) = (u, u^2)$ for $u \in [0, 1]$: the parabola itself.

**Non-example: a cubic.** For $P_k = (k, k^3)$, $k = -1, 0, 1, 2$, the tangents are $(1, 1)$ at $P_1$ and $(1, 4)$ at $P_2$, while the true slopes of $y = x^3$ are 0 and 3. So the spline is not the cubic $y = x^3$: the precision is quadratic, not cubic.

**Non-example: a B-spline through the same points.** A uniform cubic [B-spline](/b-spline/) with the control points $P_0, \dots, P_3$ is $C^2$, but it does not pass through $P_1$ and $P_2$. The Catmull-Rom spline trades one order of smoothness and the convex hull property for interpolation and locality.

## Related definitions

- [Hermite spline](/hermite-spline/): the general form with free tangents. Catmull-Rom fixes the tangents from the neighbours.
- [Kochanek-Bartels spline](/kochanek-bartels-spline/): the tangents with tension, continuity and bias parameters. All three equal to zero gives the uniform Catmull-Rom spline.
- Cardinal spline: the tangent $(1 - \tau)\frac12 (P_{i+1} - P_{i-1})$ with a tension $\tau$. The value $\tau = 0$ is Catmull-Rom, and $\tau = 1$ gives zero tangents.
- [Natural cubic spline](/natural-cubic-spline/): also interpolates, and is $C^2$, but each point changes the whole curve.
- [Cubic Hermite spline](/cubic-hermite-spline/) in numerical analysis: the function case, where a three-point slope estimate of the same kind is one option.
- [Curve interpolation](/curve-interpolation/): the problem, with the choice of knots (uniform, chordal, centripetal) treated in general.
- [Four-point scheme](/four-point-scheme/): the subdivision scheme with the midpoint weights of the uniform spline.

## References
