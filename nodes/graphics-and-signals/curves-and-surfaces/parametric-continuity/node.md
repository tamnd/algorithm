---
tag: WGBTZC
kind: definition
slug: parametric-continuity
name: Parametric continuity
aliases:
- Ck continuity
- geometric continuity Gk
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: How smoothly two curve pieces join. C^k asks the derivatives of the parametrization to agree up to order k. G^k asks this only after some reparametrization, so it measures the shape.
prereqs: [parametric-curve]
see_also: [hermite-spline, natural-cubic-spline, b-spline, bezier-curve, knot-vector, frenet-frame, arc-length-parametrization, smooth-function]
sources:
  - paper: doi:10.1109/38.41470
    title: Brian A. Barsky and Tony D. DeRose, Geometric continuity of parametric curves, three equivalent characterizations, IEEE Computer Graphics and Applications 9(6), 60-69 (1989)
    locator: parametric continuity, reparametrization, the beta-constraints and the arc-length characterization of G^k
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the chapter on geometric continuity (G1 and G2 joints of Bezier curves, beta-constraints)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 2.3 (continuity of the B-spline basis functions at a knot of multiplicity k)
---

Parametric continuity measures how smoothly two pieces of a [parametric curve](/parametric-curve/) join. A joint is $C^k$ if the two pieces have the same point and the same derivatives of orders $1, \dots, k$ there, computed with respect to the common parameter. This is a property of the parametrization: it changes when the knot intervals change or when one piece is moved along at a different speed, and the trace stays the same. Geometric continuity $G^k$ is the version for the shape. A joint is $G^k$ if the pieces can be reparametrized so that they meet $C^k$. $G^1$ means a common tangent direction, and $G^2$ adds a common curvature vector. The two notions answer different questions. In animation the parameter is time, and $C^1$ and $C^2$ mean continuous velocity and acceleration. In design only the shape is seen, and $G^1$ and $G^2$ are the conditions that the eye and the reflection lines on a car body detect. Spline constructions are labelled by the order they reach: the [Hermite spline](/hermite-spline/) is $C^1$, the [natural cubic spline](/natural-cubic-spline/) is $C^2$, and a [B-spline](/b-spline/) of degree $p$ is $C^{p-r}$ at a knot of multiplicity $r$.

## Definition

Let $A : [s_0, s_1] \to \mathbb{R}^d$ and $B : [s_1, s_2] \to \mathbb{R}^d$ be pieces of a curve, each $k$ times continuously differentiable, that meet at the parameter $s_1$.

**Parametric continuity.** The joint is $C^k$ if

$$A^{(j)}(s_1) = B^{(j)}(s_1), \qquad j = 0, 1, \dots, k .$$

A curve is $C^k$ if every joint is $C^k$. $C^0$ means only that the pieces meet.

**Local parameters.** In practice each piece is stored on a local parameter $u \in [0, 1]$, with $s = s_i + h_i u$ and $h_i = s_{i+1} - s_i$ the knot interval. Then $\frac{d^j}{ds^j} = h_i^{-j} \frac{d^j}{du^j}$, and the $C^k$ conditions read

$$\frac{1}{h_A^{\,j}}\, A^{(j)}(1) = \frac{1}{h_B^{\,j}}\, B^{(j)}(0), \qquad j = 0, \dots, k,$$

with the derivatives taken in $u$. The same two segments can be $C^1$ for one choice of knot intervals and only $C^0$ for another.

**Geometric continuity.** Suppose the joint is regular, $A'(s_1) \ne 0$. The joint is $G^k$ if there is a reparametrization $\varphi$ of $B$, $k$ times continuously differentiable with $\varphi' > 0$, such that $A$ and $B \circ \varphi$ meet $C^k$ (Barsky and DeRose 1989). Barsky and DeRose prove that this is equivalent to two other conditions.

- *Arc length.* The joint is $G^k$ if and only if the [arc-length parametrizations](/arc-length-parametrization/) of the two pieces meet $C^k$. So $G^k$ depends only on the traces and the direction of travel.
- *Beta-constraints.* With local parameters on $[0, 1]$, the joint is $G^k$ if and only if there are numbers $\beta_1 > 0, \beta_2, \dots, \beta_k$ with $B(0) = A(1)$ and

$$\begin{aligned}
B'(0) &= \beta_1 A'(1), \\
B''(0) &= \beta_1^2 A''(1) + \beta_2 A'(1), \\
B'''(0) &= \beta_1^3 A'''(1) + 3\beta_1\beta_2 A''(1) + \beta_3 A'(1),
\end{aligned}$$

and so on by the chain rule (the Faà di Bruno formula). The numbers are the derivatives of the reparametrization at the joint: $\beta_j = \psi^{(j)}(0)$ for the map $\psi$ with $B = \tilde A \circ \psi$, where $\tilde A$ is $A$ continued past the joint.

**The first two orders in words.** $G^1$ at a regular joint is a common unit tangent vector $T$. $G^2$ is $G^1$ together with a common curvature vector $\kappa N$, where $\kappa$ is the curvature and $N$ the principal normal of the [Frenet frame](/frenet-frame/). For a curve with velocity $C'$ and acceleration $C''$,

$$\kappa N = \frac{\lVert C' \rVert^2 C'' - (C' \cdot C'')\, C'}{\lVert C' \rVert^4},$$

so $G^2$ can be checked from first and second derivatives in exact arithmetic. For space curves $G^3$ adds the continuity of the torsion and of the derivative of the curvature with respect to arc length.

**Relations.**

- At a regular joint, $C^k$ implies $G^k$: take $\varphi$ the identity, so $\beta_1 = 1$ and $\beta_j = 0$ for $j \ge 2$.
- $G^k$ does not imply $C^k$: any $\beta_1 \ne 1$ gives a $G^1$ joint that is not $C^1$.
- At a joint with zero velocity, $C^k$ does not imply $G^1$: the trace can have a corner or a cusp. This is why $G^k$ is defined only for regular joints.
- Changing the knot intervals rescales the parameter of each piece linearly. A $G^1$ joint with ratio $\beta_1$ becomes $C^1$ when $h_B / h_A = \beta_1$. A $G^2$ joint with $\beta_2 \ne 0$ is $C^2$ for no choice of knot intervals, because a linear rescaling has no second derivative.

**Bézier joints.** For two [Bézier curves](/bezier-curve/) of degree $n$ with control points $a_0, \dots, a_n$ and $b_0, \dots, b_n$, on unit intervals, $A'(1) = n(a_n - a_{n-1})$ and $B'(0) = n(b_1 - b_0)$. So the joint is $C^0$ when $b_0 = a_n$, $G^1$ when also $b_1 - b_0 = \beta_1 (a_n - a_{n-1})$ with $\beta_1 > 0$, that is, $a_{n-1}, a_n, b_1$ lie on a line in this order, and $C^1$ when $\beta_1 = 1$. The $C^2$ condition for unit intervals is $b_2 - 2b_1 + b_0 = a_n - 2a_{n-1} + a_{n-2}$.

The implementation computes the $C^k$ order of a joint and the numbers $\beta_1, \beta_2$ in exact rational arithmetic. Its tests check the $C^k$ order against a Taylor shift of the polynomial pieces, and check each $G^2$ answer by building the reparametrization $u = s/\beta_1 - \beta_2 s^2 / (2\beta_1^3)$, composing it with $B$ and confirming a $C^2$ joint, and by comparing the curvature vectors.

## Examples and non-examples

**$G^2$ but only $C^0$.** Let $A(t) = (t, t^2)$ on $[0, 1]$, so $A(1) = (1, 1)$, $A'(1) = (1, 2)$ and $A''(1) = (0, 2)$. Take $\beta_1 = 2$, $\beta_2 = 1$ and the quadratic piece

$$B(u) = (1, 1) + (2, 4)\,u + \left(\tfrac12, 5\right) u^2 ,$$

with $B'(0) = (2, 4) = 2A'(1)$ and $B''(0) = (1, 10) = 4A''(1) + A'(1)$. The velocities differ, so the joint is only $C^0$. The curvature vectors agree:

$$\kappa N_A = \frac{5\,(0, 2) - 4\,(1, 2)}{25} = \left(-\tfrac{4}{25}, \tfrac{2}{25}\right), \qquad \kappa N_B = \frac{20\,(1, 10) - 42\,(2, 4)}{400} = \left(-\tfrac{4}{25}, \tfrac{2}{25}\right).$$

The reparametrization $u = s/2 - s^2/16$ makes $B$ meet $A$ with $C^2$. A knot interval $h_B = 2$ for $B$ makes the joint $C^1$ but not $C^2$, because $\beta_2 \ne 0$.

**Two cubic Bézier curves.** $a = (0,0), (1,1), (2,1), (3,0)$ and $b = (3,0), (5,-2), (6,0), (7,2)$. Then $b_1 - b_0 = (2, -2) = 2(a_3 - a_2)$, so the joint is $G^1$ with $\beta_1 = 2$ and not $C^1$ on unit intervals. On the knot intervals $h_A = 1$ and $h_B = 2$ it is $C^1$.

**$C^1$ but not $G^1$.** $A(t) = (-(1 - t)^2, 0)$ and $B(t) = (0, t^2)$ on $[0, 1]$ meet at the origin with $A'(1) = B'(0) = (0, 0)$. The joint is $C^1$. The trace comes in along the $x$-axis and leaves along the $y$-axis, a right-angle corner. The velocity is zero at the joint, so $G^1$ is not defined, and the trace is not smooth.

**Smooth map, sharp trace.** $C(t) = (t^2, t^3)$ is one polynomial, so it is $C^\infty$ at $t = 0$, but $C'(0) = 0$ and the trace has a cusp there. Smoothness of the parametrization says nothing about the shape where the velocity vanishes.

**Spline constructions.** The [Catmull-Rom spline](/catmull-rom-spline/) and the Hermite spline are $C^1$. The [Kochanek-Bartels spline](/kochanek-bartels-spline/) is $C^1$ when its continuity parameter is 0 and only $C^0$ otherwise, since the incoming and the outgoing tangents differ. A cubic B-spline is $C^2$ at simple knots, $C^1$ at double knots and $C^0$ at triple knots, where the curve passes through a control point and can have a corner. The [knot vector](/knot-vector/) page shows how multiplicities are used.

**Non-example: a straight line at two speeds.** $A(t) = (t, 0)$ on $[0, 1]$ and $B(u) = (1 + 2u, 0)$. The joint is not $C^1$, since the speed jumps from 1 to 2, but it is $G^k$ for every $k$: the trace is a straight segment, and $\varphi(s) = s/2$ removes the jump. A test for smoothness of the shape that looks at $C^k$ rejects this joint, which is why design systems test $G^k$.

## Related definitions

- [Smooth function](/smooth-function/): $C^k$ for functions of one variable; a parametric curve is $C^k$ when each coordinate is.
- [Arc-length parametrization](/arc-length-parametrization/): the unit-speed parameter, in which $G^k$ becomes $C^k$.
- [Frenet frame](/frenet-frame/): the tangent, normal and binormal, with the curvature and torsion that $G^2$ and $G^3$ ask to be continuous.
- [Knot vector](/knot-vector/): knot multiplicities set the continuity order of a B-spline at each knot.
- [Hermite spline](/hermite-spline/), [natural cubic spline](/natural-cubic-spline/): $C^1$ and $C^2$ constructions through points.
- [Bézier curve](/bezier-curve/): the joint conditions on control points.

## References
