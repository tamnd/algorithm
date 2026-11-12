---
tag: T0NMNV
kind: definition
slug: natural-cubic-spline
name: Natural cubic spline
aliases:
- natural spline
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The C2 cubic spline curve through given points with zero second derivative at both ends. Its tangents solve a tridiagonal system, and it minimizes the integral of the squared second derivative.
prereqs: [hermite-spline, thomas-algorithm]
see_also: [cubic-spline-interpolation, curve-interpolation, catmull-rom-spline, smoothing-spline, parametric-continuity, b-spline]
sources:
  - paper: doi:10.1090/S0025-5718-1957-0093894-6
    title: John C. Holladay, A smoothest curve approximation, Mathematical Tables and Other Aids to Computation 11(60), 233-243 (1957)
    locator: the minimum property of the natural cubic spline among functions with a square integrable second derivative
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter IV (piecewise cubic interpolation, the end conditions and the tridiagonal system for the slopes) and Chapter V (best approximation properties of complete cubic spline interpolation)
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 9, Constructing Spline Curves (C2 cubic spline interpolation of points, end conditions and the choice of knots)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 9.2.3, Cubic Spline Curve Interpolation
---

A natural cubic spline is the piecewise cubic curve that passes through given points $P_0, \dots, P_n$ at given knots $t_0 < \dots < t_n$, has a continuous second derivative, and has zero second derivative at both ends. It is the [Hermite spline](/hermite-spline/) whose tangents are not chosen by a local rule but by the condition $C^2$ at every inner knot. That condition is a tridiagonal linear system for the tangents, with the same matrix for every coordinate, so the [Thomas algorithm](/thomas-algorithm/) finds the curve in $O(n)$ time per coordinate. Among all curves through the points at the same knots with a square integrable second derivative, it has the least value of $\int \lVert C''(t) \rVert^2\, dt$ (Holladay 1957). This is the mathematical form of the thin elastic strip, the draughtsman's spline, which gave splines their name. The function case $y = f(x)$, written with the second derivatives (moments) as unknowns, with the clamped end conditions and the error bounds, is on [cubic spline interpolation](/cubic-spline-interpolation/). This page treats the curve case: vector data, a parameter that the user must choose, and the tangent form.

## Definition

Let $t_0 < t_1 < \dots < t_n$ be knots, $n \ge 1$, and $P_0, \dots, P_n$ points in $\mathbb{R}^d$. The *natural cubic spline* is the curve $C : [t_0, t_n] \to \mathbb{R}^d$ with

1. $C$ is a cubic polynomial on each $[t_i, t_{i+1}]$;
2. $C(t_i) = P_i$ for $i = 0, \dots, n$;
3. $C$ is twice continuously differentiable on $[t_0, t_n]$;
4. $C''(t_0) = C''(t_n) = 0$ (the natural end conditions).

**The tangent system.** Write $h_i = t_{i+1} - t_i$, $\delta_i = (P_{i+1} - P_i)/h_i$ and $D_i = C'(t_i)$. By the [Hermite spline](/hermite-spline/) formulas, the second derivative of segment $i$ is $(6\delta_i - 4D_i - 2D_{i+1})/h_i$ at its left end and $(-6\delta_i + 2D_i + 4D_{i+1})/h_i$ at its right end. Equal values at each inner knot and zero values at the two ends give

$$2D_0 + D_1 = 3\delta_0,$$

$$\frac{1}{h_{i-1}} D_{i-1} + 2\left(\frac{1}{h_{i-1}} + \frac{1}{h_i}\right) D_i + \frac{1}{h_i} D_{i+1} = 3\left(\frac{\delta_{i-1}}{h_{i-1}} + \frac{\delta_i}{h_i}\right), \qquad 1 \le i \le n - 1,$$

$$D_{n-1} + 2D_n = 3\delta_{n-1}.$$

For uniform knots ($h_i = 1$) the inner rows are $D_{i-1} + 4D_i + D_{i+1} = 3(P_{i+1} - P_{i-1})$.

**Existence and uniqueness.** In every row the diagonal entry is twice the sum of the two off-diagonal entries, so the matrix is strictly diagonally dominant and therefore nonsingular. The system has exactly one solution, and the conditions 1 to 4 define exactly one curve. The same reason makes Gaussian elimination without pivoting stable here, which is the [Thomas algorithm](/thomas-algorithm/): $O(n)$ operations to factor the matrix once, then $O(n)$ per coordinate. The total cost is $O(nd)$ time and $O(nd)$ space.

**The minimum property.** Let $G$ be any curve on $[t_0, t_n]$ with $G(t_i) = P_i$ for all $i$, $G$ continuously differentiable and $G''$ square integrable. Then

$$\int_{t_0}^{t_n} \lVert G'' \rVert^2\, dt = \int_{t_0}^{t_n} \lVert C'' \rVert^2\, dt + \int_{t_0}^{t_n} \lVert G'' - C'' \rVert^2\, dt,$$

so $C$ has the least value, and it is the only curve with that value. Proof, for each coordinate: let $e = G - C$, which is zero at every knot. Integrate by parts on each $[t_i, t_{i+1}]$: $\int C'' e'' = [C'' e'] - \int C''' e'$. The boundary terms add up to $C''(t_n) e'(t_n) - C''(t_0) e'(t_0) = 0$, because $C''$ and $e'$ are continuous and $C''$ is zero at both ends. On each piece $C'''$ is a constant $k_i$, so $\int_{t_i}^{t_{i+1}} C''' e' = k_i (e(t_{i+1}) - e(t_i)) = 0$. So $\int C'' e'' = 0$, and $\int (G'')^2 = \int (C'' + e'')^2 = \int (C'')^2 + \int (e'')^2$. The [cubic spline interpolation](/cubic-spline-interpolation/) page has the same argument for the function case.

**What the minimum means for a curve.** The integral $\int \lVert C'' \rVert^2 dt$ depends on the parametrization. It is not the bending energy $\int \kappa^2\, ds$ of an elastic strip, where $\kappa$ is the curvature and $s$ the arc length. The two agree up to a constant only for a unit-speed curve. So the minimum property holds for the chosen knots, and a different choice of knots gives a different natural spline with a different shape. Chord-length knots, $h_i = \lVert P_{i+1} - P_i \rVert$, make the speed roughly constant and the two energies roughly proportional. The choice of knots is part of [curve interpolation](/curve-interpolation/).

**Other properties.**

- *Global.* The inverse of the tridiagonal matrix is full, so each point changes every tangent. The effect decays geometrically: for uniform knots the change in $D_j$ caused by a change of $P_i$ shrinks by a factor of about $2 - \sqrt3 \approx 0.268$ for each step of $|i - j|$, with alternating sign.
- *Affine invariance.* The tangents are linear in the points and the points enter with weights that sum to 1, so an affine map of the points maps the spline.
- *Straight ends.* The curvature is zero at both ends. Near the ends the curve is flatter than the data suggest, which is the main reason to use clamped ends (given end tangents) or not-a-knot ends instead.
- *Spline space.* The curve is a cubic [B-spline](/b-spline/) curve with simple inner knots, $n + 3$ control points, and the natural end conditions as two extra equations.

## Examples and non-examples

**A zigzag.** Take the uniform knots $0, 1, 2, 3$ and the points $(0, 0)$, $(1, 1)$, $(2, 0)$, $(3, 1)$. The $x$ coordinates are $0, 1, 2, 3$, so $D_i^x = 1$ for all $i$ satisfies every row. For $y$ the system is

$$2D_0 + D_1 = 3, \quad D_0 + 4D_1 + D_2 = 0, \quad D_1 + 4D_2 + D_3 = 0, \quad D_2 + 2D_3 = 3,$$

with the solution $D_0^y = D_3^y = 5/3$ and $D_1^y = D_2^y = -1/3$. At $t = 1/2$ the curve is at $(1/2, 3/4)$, and at $t = 3/2$ it is at $(3/2, 1/2)$. The second derivatives at the knots are $(0, 0)$, $(0, -4)$, $(0, 4)$ and $(0, 0)$: continuous, and zero at the ends. The integral of $\lVert C'' \rVert^2$ is $16$. The Hermite spline through the same points with the tangents $(1, 1)$, $(1, 0)$, $(1, 0)$, $(1, 1)$ has the integral $20$, and the difference $4$ is the integral of the squared difference of the two second derivatives, as the identity says.

**Decay of a change.** Take 13 uniform knots, all points at $0$, and move the middle point to $1$. The tangents change by $\pm 0.80385$ next to it, then $\mp 0.21540$, $\pm 0.05774$, $\mp 0.01554$, and so on. The ratio of two neighbouring changes is about $-0.268$.

**Non-example: a Catmull-Rom curve.** A [Catmull-Rom spline](/catmull-rom-spline/) through the same points is $C^1$, and its second derivative jumps at the knots. It does not satisfy condition 3, so it is not a natural spline, and its integral of $\lVert C'' \rVert^2$ is larger.

**Non-example: a closed curve.** A natural spline has two free ends with zero curvature. For a closed curve the right conditions are periodic: $C'$ and $C''$ agree at $t_0$ and $t_n$, and the matrix becomes cyclic tridiagonal. This periodic spline is a different curve.

**Non-example: wrong knots.** With uniform knots and points that are spaced very unevenly, the curve can form loops and overshoot between close points, because the parameter assigns the same time to a short and a long chord. The curve is still the natural spline for those knots. The defect is in the knots.

## Related definitions

- [Cubic spline interpolation](/cubic-spline-interpolation/): the function case, the moment form of the system, the clamped and not-a-knot ends, and the error bounds.
- [Thomas algorithm](/thomas-algorithm/): the $O(n)$ solver for the tridiagonal system.
- [Hermite spline](/hermite-spline/): the segment form. The natural spline is the Hermite spline with the $C^2$ tangents.
- [Catmull-Rom spline](/catmull-rom-spline/): a local $C^1$ alternative.
- [Smoothing spline](/smoothing-spline/): the same energy plus a data misfit term, for noisy points.
- [Curve interpolation](/curve-interpolation/): the problem, with the choice of knots.
- [Parametric continuity](/parametric-continuity/): the $C^2$ condition. A curve can be $G^2$ with fewer constraints.

## References
