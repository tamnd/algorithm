---
tag: EZ8WX8
kind: definition
slug: rational-bezier-curve
name: Rational Bezier curve
aliases:
- weighted Bezier curve
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The curve sum w_i P_i B_i^n(t) / sum w_i B_i^n(t), a Bezier curve with a positive weight on each control point. It gives conic arcs, such as circles, exactly.
prereqs: [bezier-curve, bernstein-polynomials]
see_also: [nurbs, bezier-curve, de-casteljau-algorithm, convex-hull-property, variation-diminishing-property, control-points, parametric-curve, curve-evaluation]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 12, Conics, and Chapter 13, Rational Bezier and B-Spline Curves (weights, the standard form, the shape factor and the circle)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: the sections on rational Bezier curves, homogeneous coordinates and the representation of conics and circles
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: the chapter on rational Bezier curves (the projective view and conic sections)
---

A rational Bézier curve of degree $n$ is the curve $R(t) = \sum_i w_i P_i B_i^n(t) \big/ \sum_i w_i B_i^n(t)$ for $t \in [0, 1]$, where $P_0, \dots, P_n$ are [control points](/control-points/), $w_0, \dots, w_n$ are positive weights and $B_i^n$ are the [Bernstein polynomials](/bernstein-polynomials/). With equal weights it is a polynomial [Bézier curve](/bezier-curve/). A larger weight pulls the curve towards its point. The rational form represents conic arcs, among them circle arcs, exactly, and it is invariant under projective maps; for these reasons it is the basis of [NURBS](/nurbs/).

## Definition

Let $n \ge 1$, let $P_0, \dots, P_n \in \mathbb{R}^d$ and let $w_0, \dots, w_n > 0$. The rational Bézier curve with these points and weights is

$$R(t) = \frac{\sum_{i=0}^n w_i P_i B_i^n(t)}{\sum_{i=0}^n w_i B_i^n(t)}, \qquad t \in [0, 1].$$

The denominator is positive on $[0, 1]$, because the weights are positive and the $B_i^n$ are nonnegative with sum 1. Some authors allow zero or negative weights; then the denominator can vanish, and the properties below can fail.

**Homogeneous form.** Put $W_i = (w_i P_i, w_i) \in \mathbb{R}^{d+1}$. The polynomial Bézier curve $W(t) = \sum_i W_i B_i^n(t)$ has the coordinates $(N(t), D(t))$, with the numerator $N$ and the denominator $D$ of $R$. So $R(t) = N(t) / D(t)$ is the central projection of $W(t)$ onto the hyperplane where the last coordinate is 1. Points and derivatives of $R$ follow from those of $W$; the [de Casteljau algorithm](/de-casteljau-algorithm/) applied to the $W_i$ gives $R(t)$ after one division, and it also gives the two halves of a split.

The curve has these properties.

1. **End points and end tangents.** $R(0) = P_0$, $R(1) = P_n$, and $R'(0) = n \frac{w_1}{w_0} (P_1 - P_0)$, $R'(1) = n \frac{w_{n-1}}{w_n} (P_n - P_{n-1})$. Proof for $t = 0$: $N(0) = w_0 P_0$, $D(0) = w_0$, $N'(0) = n (w_1 P_1 - w_0 P_0)$ and $D'(0) = n (w_1 - w_0)$, by the derivative rule of Bézier curves. So $R'(0) = (N'(0) D(0) - N(0) D'(0)) / D(0)^2 = n w_1 (P_1 - P_0) / w_0$. The end $t = 1$ follows by symmetry.
2. **Convex hull.** The functions $w_i B_i^n / \sum_j w_j B_j^n$ are nonnegative and sum to 1, so the curve lies in the convex hull of the points. See the [convex hull property](/convex-hull-property/).
3. **Variation diminishing.** A line crosses the curve at most as often as the polygon. See the [variation diminishing property](/variation-diminishing-property/).
4. **Projective invariance.** Let $f(x) = (A x + b) / (c \cdot x + e)$ be a projective map with $c \cdot P_i + e > 0$ for all $i$. Then $f(R(t))$ is the rational Bézier curve with the points $f(P_i)$ and the weights $w_i (c \cdot P_i + e)$. Proof: in homogeneous form, $f$ is the linear map $M(x, h) = (A x + b h, c \cdot x + e h)$, and $M W_i = w_i (c \cdot P_i + e) \big(f(P_i), 1\big)$. A linear map commutes with the Bernstein sum. Affine maps are the case $c = 0$, $e = 1$, with the weights unchanged. A polynomial Bézier curve is invariant only under affine maps; its perspective image is in general a rational curve.
5. **Weight scaling.** Multiplying all weights by the same $c > 0$ does not change the curve.
6. **Reparametrization.** For $\rho > 0$, the weights $\rho^i w_i$ give the same point set, with $t$ replaced by $s = \rho t / (1 - t + \rho t)$. Proof: $s$ maps $[0, 1]$ onto $[0, 1]$, $1 - s = (1 - t)/(1 - t + \rho t)$, so $B_i^n(s) = \rho^i B_i^n(t) / (1 - t + \rho t)^n$, and the factor $(1 - t + \rho t)^n$ cancels in the ratio. With properties 5 and 6, any positive weights can be brought to the standard form $w_0 = w_n = 1$.
7. **Effect of one weight.** As $w_i \to \infty$ with the other weights fixed, $R(t) \to P_i$ for each $t \in (0, 1)$. As $w_i \to 0$, the curve tends to the rational curve without $P_i$ in its sum.

**Conics.** Let $n = 2$ and let $P_0, P_1, P_2$ not be on one line. Put the shape factor

$$\kappa = \frac{w_1^2}{w_0 w_2},$$

which does not change under properties 5 and 6. Then the curve is an arc of a conic, and the conic is an ellipse if $\kappa < 1$, a parabola if $\kappa = 1$ and a hyperbola if $\kappa > 1$. Proof. Let $\lambda_0, \lambda_1, \lambda_2$ be the barycentric coordinates of $R(t)$ in the triangle $P_0 P_1 P_2$. They are $\lambda_i = w_i B_i^2(t) / D(t)$, so $\lambda_1^2 = 4 \kappa\, \lambda_0 \lambda_2$, which is the equation of a conic. In homogeneous barycentric coordinates the line at infinity is $\lambda_0 + \lambda_1 + \lambda_2 = 0$. Put $\lambda_1 = -(\lambda_0 + \lambda_2)$ in the conic: $\lambda_0^2 + (2 - 4\kappa) \lambda_0 \lambda_2 + \lambda_2^2 = 0$, with the discriminant $(2 - 4\kappa)^2 - 4 = 16 \kappa (\kappa - 1)$. So the conic has no real point at infinity (an ellipse) if $0 < \kappa < 1$, one double point (a parabola) if $\kappa = 1$, and two points (a hyperbola) if $\kappa > 1$. Conversely, each conic arc with the end points $P_0$ and $P_2$ whose end tangents meet at $P_1$, and that lies in the triangle $P_0 P_1 P_2$, has such a representation (Farin, Chapter 12).

**Circle arcs.** The arc of a circle with the end points $P_0$ and $P_2$, the tangents meeting at $P_1$ and the angle $2\theta < \pi$ at the center is the rational quadratic with the weights $1, \cos \theta, 1$. So the quarter circle has $w_1 = \cos(\pi/4) = \sqrt2 / 2$. A semicircle or more needs several pieces, because the end tangents of one piece must meet.

## Examples and non-examples

- **A quarter circle with rational points.** Take $P_0 = (1, 0)$, $P_1 = (1, 1)$, $P_2 = (0, 1)$ and the weights $1, 1, 2$. Then $D(t) = (1 - t)^2 + 2t(1 - t) + 2t^2 = 1 + t^2$ and
$$R(t) = \left(\frac{1 - t^2}{1 + t^2},\ \frac{2t}{1 + t^2}\right),$$
the classical rational parametrization of the unit circle. So $R(1/2) = (3/5, 4/5)$ and $R(1/3) = (4/5, 3/5)$, both exactly on the circle. The shape factor is $\kappa = 1/(1 \cdot 2) = 1/2$.
- **The same arc in standard form.** By property 6 with $\rho = 1/\sqrt2$, the weights $1, \sqrt2/2, 1$ give the same arc. Now $\kappa = 1/2$ again, and the arc is symmetric in $t$: $R(1/2) = (\sqrt2/2, \sqrt2/2) \approx (0.7071, 0.7071)$.
- **The speed is not constant.** For the weights $1, 1, 2$, $\lVert R'(t) \rVert = 2 / (1 + t^2)$, from 2 at $t = 0$ to 1 at $t = 1$. For motion at constant speed, see [arc length parametrization](/arc-length-parametrization/).
- **The three conic types.** With the same three points and $w_0 = w_2 = 1$, the weight $w_1 = 1/2$ gives an ellipse arc, $w_1 = 1$ gives the parabola arc of the polynomial Bézier curve, and $w_1 = 2$ gives a hyperbola arc.
- **Non-example: a polynomial curve.** No polynomial Bézier curve gives a circle arc (proved on the [Bézier curve](/bezier-curve/) page). The rational form is needed for an exact circle.
- **Non-example: a negative weight.** With the weights $1, -1/2, 1$ and the same points, the denominator $1 - 3t + 3t^2$ is still positive, but $R(1/2) = (0, 0)$ is outside the triangle of the points. With negative weights the curve is not in the convex hull; the computation is on the [convex hull property](/convex-hull-property/) page.

## Related definitions

- [Bézier curve](/bezier-curve/): the case of equal weights.
- [NURBS](/nurbs/): the piecewise rational form with B-splines in place of Bernstein polynomials. Each span of a NURBS curve is a rational Bézier curve.
- [Control points](/control-points/): the points $P_i$; here each one has a weight as well.
- [Rational de Casteljau evaluation](/de-casteljau-algorithm/): the homogeneous and the weighted forms of the algorithm, and the problem of [curve evaluation](/curve-evaluation/).
- [Parametric curve](/parametric-curve/): the general notion; a rational Bézier curve is a rational parametric curve with a positive denominator on $[0, 1]$.

## References
