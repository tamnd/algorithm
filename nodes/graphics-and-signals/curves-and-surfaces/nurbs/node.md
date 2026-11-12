---
tag: P5FN0V
kind: definition
slug: nurbs
name: NURBS
aliases:
- non-uniform rational B-spline
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: A NURBS curve is a B-spline curve in homogeneous coordinates with positive weights, divided by its weight. It is piecewise rational, projectively invariant, and gives conics such as circles exactly.
prereqs: [b-spline, de-boor-algorithm]
see_also: [rational-bezier-curve, knot-vector, knot-refinement, boehm-knot-insertion, tensor-product-surface, convex-hull-property, partition-of-unity, finite-element-method]
sources:
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 4, Rational B-spline curves and surfaces (Section 4.2, the definition and properties of NURBS curves); Chapter 7, Conics and circles (the rational quadratic arc, the conic type from the weights, and full circles from arcs); Chapter 12, Standards and data exchange
  - paper: "Kenneth J. Versprille, Computer-aided design applications of the rational B-spline approximation form, PhD thesis, Syracuse University, 1975"
    locator: the rational B-spline form for curves and surfaces in design
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the chapters on conics, rational Bézier curves and rational B-spline curves
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter IX and Chapter X, the B-spline basis and the evaluation of B-spline series, which NURBS use in homogeneous coordinates
  - paper: doi:10.1016/j.cma.2004.10.008
    title: T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis, CAD, finite elements, NURBS, exact geometry and mesh refinement, Computer Methods in Applied Mechanics and Engineering 194 (2005), 4135 to 4195
    locator: NURBS as the basis functions of finite element analysis
---

NURBS, non-uniform rational B-splines, are the curves and surfaces $C(u) = \sum_i w_i P_i N_{i,p}(u) \big/ \sum_i w_i N_{i,p}(u)$, where the $N_{i,p}$ are the [B-splines](/b-spline/) of a [knot vector](/knot-vector/) that need not be uniform, the $P_i$ are control points, and the $w_i$ are positive weights. Equivalently, a NURBS curve is a polynomial B-spline curve in homogeneous coordinates, with the control points $(w_i P_i, w_i)$, followed by the division by the last coordinate. Each span is a [rational Bézier curve](/rational-bezier-curve/). With all weights equal it is a B-spline curve. Unlike polynomial curves, NURBS represent conic sections exactly, among them circles, and the form is invariant under projective maps. For these reasons NURBS are the standard representation of free-form and analytic geometry in CAD systems and their exchange formats.

## Definition

Let $p \ge 1$ be the degree, $n \ge p$, and $t_0 \le \cdots \le t_{n+p+1}$ a knot vector with $t_p < t_{n+1}$; $N_i = N_{i,p}$ are its B-splines. A **NURBS curve** of degree $p$ in $\mathbb{R}^d$ is given by control points $P_0, \ldots, P_n \in \mathbb{R}^d$ and weights $w_0, \ldots, w_n > 0$, and it is

$$C(u) = \frac{\sum_{i=0}^{n} w_i P_i \, N_i(u)}{\sum_{i=0}^{n} w_i \, N_i(u)} = \sum_{i=0}^{n} R_i(u) \, P_i, \qquad R_i(u) = \frac{w_i N_i(u)}{\sum_j w_j N_j(u)},$$

for $u$ in the domain $[t_p, t_{n+1}]$, with the limit from the left at $u = t_{n+1}$. The denominator $W(u) = \sum_j w_j N_j(u)$ is positive on the domain, because the $N_j$ are nonnegative there, at least one of them is positive at each $u$, and the weights are positive. The $R_i$ are the **rational basis functions**.

**Homogeneous form.** Put $P_i^w = (w_i P_i, w_i) \in \mathbb{R}^{d+1}$ and $C^w(u) = \sum_i N_i(u) P_i^w$. This is an ordinary B-spline curve in $\mathbb{R}^{d+1}$, and $C(u)$ is the image of $C^w(u)$ under the map $(x, w) \mapsto x / w$, the central projection from the origin onto the hyperplane $w = 1$. Every algorithm for B-spline curves therefore works for NURBS: run it on the $P_i^w$ and divide at the end. The [de Boor algorithm](/de-boor-algorithm/) evaluates $C(u)$ this way, and [Boehm knot insertion](/boehm-knot-insertion/), the [Oslo algorithm](/oslo-algorithm/) and [knot refinement](/knot-refinement/) refine a NURBS curve; the new weights are the last coordinates of the new homogeneous points.

**A NURBS surface** of degrees $p, q$ has a net of control points $P_{ij}$ with weights $w_{ij} > 0$ and two knot vectors, and it is $S(u, v) = \sum_{i,j} w_{ij} P_{ij} N_{i,p}(u) N_{j,q}(v) \big/ \sum_{i,j} w_{ij} N_{i,p}(u) N_{j,q}(v)$: the projection of a [tensor product surface](/tensor-product-surface/) in homogeneous coordinates. It is in general not a tensor product of rational functions, because the denominator does not factor.

**Properties.** These follow from the B-spline properties of $C^w$.

- The $R_i$ are nonnegative, they sum to 1 on the domain, and $R_i$ is zero outside $[t_i, t_{i+p+1})$. So $C(u)$ is a convex combination of $P_{\mu-p}, \ldots, P_\mu$ on the span $\mu$: the strong [convex hull property](/convex-hull-property/) and [partition of unity](/partition-of-unity/) hold for the rational basis, and moving $P_i$ changes the curve only on $p + 1$ spans.
- On each span, $C$ is a quotient of two polynomials of degree at most $p$. At a knot of multiplicity $m$, $C$ is $C^{p-m}$, as $C^w$ is.
- **Affine and projective invariance.** An affine map of the $P_i$ maps the curve, with the same weights. A projective map $M$, applied to the homogeneous points $P_i^w$, maps the curve to the image curve; the new weights are the last coordinates of $M P_i^w$, and the image is again a NURBS curve if they are positive.
- **The weights.** If $w_i$ grows with all else fixed, the curve moves toward $P_i$ on the spans where $N_i \ne 0$, and $C(u) \to P_i$ as $w_i \to \infty$ at each $u$ with $N_i(u) > 0$. Multiplying all weights by one positive constant does not change the curve. On a single Bézier segment, multiplying $w_i$ by $\rho^i$ for a $\rho > 0$ changes only the parametrization.
- **Derivatives.** With $A(u) = \sum_i w_i P_i N_i(u)$, $C = A / W$ and $C' = (A' - W' C) / W$. Higher derivatives follow by the Leibniz rule.

## Examples and non-examples

**A quarter circle.** Take $p = 2$, the knots $(0, 0, 0, 1, 1, 1)$, the control points $(1, 0), (1, 1), (0, 1)$ and the weights $1, 1, 2$. On these knots the $N_i$ are the Bernstein polynomials $(1 - u)^2$, $2u(1 - u)$, $u^2$, so

$$C(u) = \frac{\bigl(1 - u^2, \; 2u\bigr)}{1 + u^2}, \qquad x^2 + y^2 = \frac{(1 - u^2)^2 + 4u^2}{(1 + u^2)^2} = 1 .$$

| $u$ | 0 | 1/4 | 1/2 | 3/4 | 1 |
|---|---|---|---|---|---|
| $C(u)$ | $(1, 0)$ | $(15/17, 8/17)$ | $(3/5, 4/5)$ | $(7/25, 24/25)$ | $(0, 1)$ |

Every value is a rational point of the unit circle. The often quoted weights $1, \sqrt2/2, 1$ give the same arc with a symmetric parametrization; they are $1, 1, 2$ multiplied by $\rho^i$ with $\rho = 1/\sqrt2$.

**The conic of a rational quadratic.** For any triangle $P_0, P_1, P_2$ and weights $w_0, w_1, w_2 > 0$ on the knots $(0, 0, 0, 1, 1, 1)$, let $(\tau_0, \tau_1, \tau_2)$ be the barycentric coordinates of $C(u)$ with respect to the triangle. Then $\tau_i = w_i B_i(u) / W(u)$, with $B_0 = (1 - u)^2$, $B_1 = 2u(1 - u)$, $B_2 = u^2$, so

$$w_0 w_2 \, \tau_1^2 = 4 \, w_1^2 \, \tau_0 \tau_2 ,$$

a quadratic equation: the curve is an arc of a conic. It is an ellipse if $w_1^2 < w_0 w_2$, a parabola if $w_1^2 = w_0 w_2$, and a hyperbola if $w_1^2 > w_0 w_2$. For the triangle $(1, 0), (1, 1), (0, 1)$ with $w_0 = w_2 = 1$, the midpoint $C(1/2)$ is $(2/3, 2/3)$ for $w_1 = 1/2$, $(3/4, 3/4)$ for $w_1 = 1$ and $(5/6, 5/6)$ for $w_1 = 2$; the circle needs $w_1 = \sqrt2/2$ and passes through $(\sqrt2/2, \sqrt2/2)$, between the first two.

**A full circle.** Take $p = 2$, the knots $(0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4)$, the nine control points $(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)$ on the corners and edge midpoints of a square, and the weights $1, 1, 2, 2, 4, 4, 8, 8, 16$. Each span is the quarter arc above, turned by a multiple of $90°$, with its weights scaled by a power of 2 so that neighboring arcs share a weight. The curve is the whole unit circle, with $C(1/2) = (3/5, 4/5)$. The double interior knots make it only $C^0$ as a parametrized curve at $u = 1, 2, 3$, but the circle is smooth there. The implementation of the de Boor algorithm checks $x^2 + y^2 = 1$ exactly for this curve, and the implicit equation of the conic for random rational quadratics.

**B-spline curves.** If all weights are equal, $W$ is constant by the partition of unity and $C$ is the polynomial B-spline curve $\sum_i N_i P_i$. So the B-spline curves are the NURBS curves with equal weights, and the Bézier curves are those on the knots $0^{p+1} 1^{p+1}$.

**Non-example: a circle from polynomials.** No polynomial B-spline curve traces an arc of a circle. On a span, such a curve is $(x(u), y(u))$ with polynomials $x, y$, and $x^2 + y^2 = 1$ on an interval implies it for all $u$. Then $(x + i y)(x - i y) = 1$ in the polynomials with complex coefficients, so $x + i y$ is a unit, a constant, and the curve is one point. This is why the rational form is needed.

**Non-example: weights that are not positive.** For the triangle above with weights $1, -1, 1$, the denominator $(1 - u)^2 - 2u(1 - u) + u^2 = (1 - 2u)^2$ is zero at $u = 1/2$, and the curve goes to infinity there. Zero weights also break the convex hull property. Such curves are rational B-spline curves, but they are not NURBS in the sense above.

## Related definitions

- [B-spline](/b-spline/): the basis functions $N_{i,p}$. NURBS with equal weights are B-spline curves.
- [Rational Bézier curve](/rational-bezier-curve/): a NURBS curve with one span. Each span of a NURBS curve, after [knot refinement](/knot-refinement/) to multiplicity $p$ at every interior knot, is one.
- [Knot vector](/knot-vector/): the "non-uniform" in the name. The knots need not be evenly spaced, and repeated knots set the smoothness.
- [Tensor product surface](/tensor-product-surface/): a NURBS surface is a tensor product B-spline surface in homogeneous coordinates.
- [Parametric curve](/parametric-curve/): a NURBS curve is a piecewise rational parametric curve; [arc-length parametrization](/arc-length-parametrization/) of it is in general not rational.
- [Finite element method](/finite-element-method/): isogeometric analysis, introduced by Hughes, Cottrell and Bazilevs (2005), uses the NURBS basis of a CAD model as the finite element basis, and refines it by knot insertion.

The rational B-spline form for design goes back to the thesis of Kenneth Versprille at Syracuse University (1975). The NURBS Book of Piegl and Tiller is the standard reference for the algorithms, and its Chapter 12 describes the use of NURBS in data exchange standards.

## References
