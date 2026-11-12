---
tag: XRW8YW
kind: definition
slug: fundamental-forms
name: Fundamental forms of a surface
aliases:
- first and second fundamental form
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Two quadratic forms on the tangent plane of a parametric surface. The first, E F G, gives lengths, angles and area; the second, L M N, gives the normal curvature in each direction.
prereqs: [parametric-surface]
see_also: [surface-curvature, parametric-surface, surface-of-revolution, ruled-surface, arc-length-parametrization, numerical-integration, symmetric-eigenproblem, frenet-frame]
sources:
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 2-5, The First Fundamental Form, Area; Section 3-2, The Definition of the Gauss Map and Its Fundamental Properties (the second fundamental form, normal curvature and Meusnier's theorem); Section 3-3, The Gauss Map in Local Coordinates; Section 4-3, The Gauss Theorem and the Equations of Compatibility
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 19, W. Boehm, Differential Geometry II (the first and second fundamental forms of a parametric patch)
---

The fundamental forms of a surface are two quadratic forms on its tangent plane at each point. The first fundamental form measures tangent vectors, so it gives the length of curves on the surface, the angle between them and the area of regions. The second measures how the surface leaves its tangent plane, so it gives the curvature of the surface in each direction. Both are computed from the first and second partial derivatives of a parametrization, and together they hold all the local geometry: lengths, angles, area and [curvature](/surface-curvature/).

## Definition

Let $S(u, v)$ be a regular [parametric surface](/parametric-surface/) with continuous second derivatives, and let $n = S_u \times S_v / |S_u \times S_v|$ be its unit normal. A tangent vector at $S(u, v)$ is $a_1 S_u + a_2 S_v$, written as the pair $a = (a_1, a_2)$.

**The first fundamental form** is the restriction of the dot product of space to the tangent plane:

$$\mathrm{I}(a, b) = E\, a_1 b_1 + F\, (a_1 b_2 + a_2 b_1) + G\, a_2 b_2, \qquad E = S_u \cdot S_u,\ F = S_u \cdot S_v,\ G = S_v \cdot S_v.$$

Its matrix $\begin{pmatrix} E & F \\ F & G \end{pmatrix}$ is positive definite at a regular point, because $EG - F^2 = |S_u \times S_v|^2 > 0$. With it:

- A curve $(u(t), v(t))$ in the domain maps to a curve on the surface of length $\int \sqrt{E u'^2 + 2F u' v' + G v'^2}\, dt$.
- Two tangent vectors meet at the angle $\theta$ with $\cos \theta = \mathrm{I}(a, b) / \sqrt{\mathrm{I}(a, a)\, \mathrm{I}(b, b)}$. The coordinate lines meet at right angles exactly where $F = 0$.
- A domain region $D$ maps to a region of area $\iint_D \sqrt{EG - F^2}\, du\, dv$.

**The second fundamental form** is

$$\mathrm{II}(a, b) = L\, a_1 b_1 + M\, (a_1 b_2 + a_2 b_1) + N\, a_2 b_2, \qquad L = S_{uu} \cdot n,\ M = S_{uv} \cdot n,\ N = S_{vv} \cdot n.$$

Since $S_u \cdot n = 0$, differentiation gives $S_{uu} \cdot n = -S_u \cdot n_u$, and so on, so $L = -S_u \cdot n_u$, $M = -S_u \cdot n_v = -S_v \cdot n_u$, $N = -S_v \cdot n_v$. The second form is minus the derivative of the normal paired with the derivative of the point. It changes sign when $n$ is replaced by $-n$, and the first form does not.

**Normal curvature.** For a tangent direction $d = (d_1, d_2)$,

$$k_n(d) = \frac{\mathrm{II}(d, d)}{\mathrm{I}(d, d)}$$

is the curvature at the point of the normal section, the curve cut from the surface by the plane through $n$ and $d$, with sign $+$ when it bends toward $n$. Proof: let $\gamma(s) = S(u(s), v(s))$ be any curve on the surface in arc length with tangent direction $d$. Then $\gamma'' = \kappa \nu$ with $\nu$ the principal normal of the curve, and $\gamma'' \cdot n = (u'^2 S_{uu} + 2u'v' S_{uv} + v'^2 S_{vv} + u'' S_u + v'' S_v) \cdot n = \mathrm{II}((u', v'), (u', v'))$, while $\mathrm{I}((u', v'), (u', v')) = |\gamma'|^2 = 1$. So $\kappa\, (\nu \cdot n) = \mathrm{II}(d, d)/\mathrm{I}(d, d)$ for every curve in direction $d$, which is Meusnier's theorem. For the normal section $\nu = \pm n$, which gives the claim. $\square$

The maximum and minimum of $k_n$ over directions are the principal curvatures, and their product and mean are the Gaussian and mean curvatures. They are the eigenvalues of $\mathrm{I}^{-1} \mathrm{II}$, which is the subject of [surface curvature](/surface-curvature/).

**Change of parameters.** If $(u, v) = \varphi(\bar u, \bar v)$ with Jacobian $J$, the matrices change as $\bar{\mathrm{I}} = J^T \mathrm{I} J$ and $\bar{\mathrm{II}} = \pm J^T \mathrm{II} J$, with the sign of $\det J$. So $k_n$ of a geometric direction does not depend on the chart, up to the sign of the normal.

**Two classical theorems.** The Gauss theorem (Theorema Egregium) says that the Gaussian curvature can be computed from $E$, $F$, $G$ and their derivatives alone, so it is kept by every bending that keeps lengths. The Bonnet theorem says that forms $\mathrm{I}$ and $\mathrm{II}$ that satisfy the Gauss and Codazzi-Mainardi equations come from a surface, which is unique up to a rigid motion (do Carmo, Section 4-3).

### Computing the forms

```pseudo id=main
FUNDAMENTAL-FORMS(S, u, v)
L1  S_u, S_v, S_uu, S_uv, S_vv ← the partial derivatives of S at (u, v)
L2  E ← S_u · S_u;  F ← S_u · S_v;  G ← S_v · S_v
L3  m ← S_u × S_v
L4  if m = 0 then error "the parametrization is not regular here"
L5  n ← m / |m|
L6  return E, F, G, S_uu · n, S_uv · n, S_vv · n
```

The implementation gets line L1 by running $S$ on second order jets in two variables: each number carries its value, its two first partials and its three second partials, and each operation updates all six by the rules of calculus. So the partials are exact up to rounding, with no step size to choose, and one evaluation costs a constant factor more than one evaluation of $S$. Lines L2 to L6 cost a constant number of operations and one square root. Lengths and areas then need quadrature: the implementation uses composite Simpson rules, with $O(n)$ evaluations for a length and $O(n^2)$ for an area on an $n \times n$ grid, and the error is that of the [quadrature rule](/numerical-integration/), not of the forms.

## Examples and non-examples

In each chart below the normal is $S_u \times S_v / |S_u \times S_v|$.

- **The sphere.** $S = R(\cos u \cos v, \cos u \sin v, \sin u)$ gives $E = R^2$, $F = 0$, $G = R^2 \cos^2 u$, and $L = R$, $M = 0$, $N = R \cos^2 u$. This normal points into the sphere. So $\mathrm{II} = \mathrm{I}/R$ and $k_n = 1/R$ in every direction. The meridian from pole to pole has length $\int R\, du = \pi R$, and the area is $\iint R^2 \cos u\, du\, dv = 4\pi R^2$.
- **The same sphere in another chart.** The stereographic chart $S = R(2u, 2v, u^2 + v^2 - 1)/(1 + u^2 + v^2)$ gives other values of $E, F, G, L, M, N$, but again $\mathrm{II} = \pm \mathrm{I}/R$, so $k_n = \pm 1/R$ in every direction. The numbers depend on the chart, and the normal curvature does not.
- **The cylinder.** $S = (A \cos u, A \sin u, v)$ gives $E = A^2$, $F = 0$, $G = 1$, and $L = -A$, $M = N = 0$, with the normal pointing out. With $\bar u = A u$ the first form becomes that of the plane, $E = G = 1$, $F = 0$: the cylinder can be unrolled with no stretch, and the first form alone cannot tell it from the plane. The second form can: $k_n = -1/A$ around the cylinder and $0$ along it.
- **The torus.** $S = ((R + a \cos u) \cos v, (R + a \cos u) \sin v, a \sin u)$ gives $E = a^2$, $F = 0$, $G = (R + a \cos u)^2$, and $L = a$, $M = 0$, $N = (R + a \cos u) \cos u$, with the normal into the tube. The parallel at $u$ has length $2\pi (R + a \cos u)$, and the area is $\iint a (R + a \cos u)\, du\, dv = 4\pi^2 R a$.
- **The saddle.** $S = (u, v, uv)$ gives $E = 1 + v^2$, $F = uv$, $G = 1 + u^2$, and $L = 0$, $M = 1/w$, $N = 0$ with $w = \sqrt{1 + u^2 + v^2}$. Here $F \ne 0$ away from the axes, so the coordinate lines are not orthogonal: at $(0.8, -0.5)$ they meet with $\cos \theta = uv / \sqrt{(1 + v^2)(1 + u^2)} \approx -0.27937$. The coordinate directions have $k_n = 0$, because they are the straight rulings of the surface.
- **Non-example: a singular point.** For the cone $S = (u \cos v, u \sin v, u)$ at the apex $u = 0$, $S_v = 0$, so $EG - F^2 = 0$ and no normal exists. The forms are not defined there, and the routine stops at line L4.
- **Non-example: a metric alone.** A positive definite form $E, F, G$ given at random does not come with a surface and a second form. The pair must satisfy the Gauss and Codazzi-Mainardi equations first, which is what the Bonnet theorem needs.

## Related definitions

- [Surface curvature](/surface-curvature/): principal, Gaussian and mean curvature and the principal directions, computed from the two forms. This page defines the forms and what each one measures directly; that page is about the curvatures that come from them and their uses.
- [Parametric surface](/parametric-surface/): the regular maps on which the forms are defined.
- [Surface of revolution](/surface-of-revolution/) and [ruled surface](/ruled-surface/): two families with simple forms, $F = M = 0$ for the first and $N = 0$ for the second.
- [Frenet frame](/frenet-frame/): the curve analog, where curvature and torsion play the role of the forms.
- [Arc-length parametrization](/arc-length-parametrization/): for curves on a surface, arc length is measured with the first form.

## References
