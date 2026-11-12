---
tag: TB1NXX
kind: definition
slug: ruled-surface
name: Ruled surface
aliases:
- linearly ruled surface
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: A surface S(u, v) = a(u) + v w(u) swept by a moving straight line. Its Gaussian curvature is never positive, and it is developable exactly when det(a', w, w') = 0 for all u.
prereqs: [parametric-surface]
see_also: [coons-patch, bilinear-interpolation, bezier-patch, surface-of-revolution, sweep-surface, fundamental-forms, surface-curvature, tensor-product-surface]
sources:
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 3-5, Ruled Surfaces and Minimal Surfaces (the directrix form, the line of striction, the curvature of a ruled surface, and developable surfaces)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 8, Construction of Common Surfaces (bilinear surfaces, the general cylinder and the ruled surface between two NURBS curves)
---

A ruled surface is the surface that a straight line sweeps as it moves through space. In CAD it is usually built from two curves $a(u)$ and $b(u)$, with the segment from $a(u)$ to $b(u)$ as the line at parameter $u$. Cylinders, cones, the saddle $z = xy$, the hyperboloid of one sheet and the helicoid are all ruled. The class matters in manufacture: a ruled surface can be cut by the flank of a cylindrical tool or by a straight wire, and a developable one, which is a special ruled surface, can be bent from a flat sheet with no stretch.

## Definition

Let $a : I \to \mathbb{R}^3$ be a curve, the directrix, and $w : I \to \mathbb{R}^3$ a curve of nonzero vectors, the ruling directions, both with continuous second derivatives. The ruled surface is

$$S(u, v) = a(u) + v\, w(u), \qquad u \in I,\ v \in J,$$

where $J$ is an interval, often $[0, 1]$ or all of $\mathbb{R}$. For fixed $u$ the $v$-curve is the straight line through $a(u)$ in direction $w(u)$, the ruling at $u$. The two-curve form used in CAD is the case $w = b - a$:

$$S(u, v) = (1 - v)\, a(u) + v\, b(u), \qquad (u, v) \in [0, 1]^2,$$

so $S(u, 0) = a(u)$ and $S(u, 1) = b(u)$. This is linear interpolation between the two curves, and it is the [Coons patch](/coons-patch/) whose other two boundaries are the straight segments $a(0) b(0)$ and $a(1) b(1)$.

**Derivatives.** $S_u = a'(u) + v\, w'(u)$, $S_v = w(u)$, $S_{vv} = 0$, $S_{uv} = w'(u)$. A point is regular when $S_u \times w \ne 0$, that is, when $a' + v w'$ is not parallel to $w$.

**Curvature.** At a regular point the [Gaussian curvature](/surface-curvature/) is

$$K = -\frac{\det(a', w, w')^2}{|S_u \times S_v|^4} \le 0.$$

Proof: by the [fundamental forms](/fundamental-forms/), $K = (LN - M^2)/(EG - F^2)$ with $L, M, N$ the components of $S_{uu}, S_{uv}, S_{vv}$ along the unit normal $n$. Here $S_{vv} = 0$, so $N = 0$ and $K = -M^2/(EG - F^2)$. Also $M = w' \cdot (S_u \times w) / |S_u \times w| = \det(w', a' + v w', w) / |S_u \times w| = \det(a', w, w') / |S_u \times w|$, since the $v w'$ part of the middle column repeats the first column and drops out, and the remaining determinant is a cyclic shift. With $EG - F^2 = |S_u \times S_v|^2$ this gives the formula. $\square$

So a ruled surface has no elliptic points. Along each ruling the factor $\det(a', w, w')$ is constant and only the denominator changes with $v$.

**Developable surfaces.** The ruled surface is developable when $\det(a'(u), w(u), w'(u)) = 0$ for all $u$. By the formula this is the same as $K = 0$ at every regular point. It is also the same as the condition that the tangent plane does not change along each ruling: the normal direction $S_u \times w = a' \times w + v\, (w' \times w)$ does not depend on $v$ exactly when $a' \times w$ and $w' \times w$ are parallel, and for $a' \times w \ne 0$ that holds exactly when $a'$, $w$ and $w'$ are linearly dependent. A developable surface is locally isometric to the plane, so a piece of it can be unrolled flat with all lengths kept. Away from singular points every developable surface is made of pieces of planes, cylinders, cones and tangent developables, the surfaces swept by the tangent lines of a space curve (do Carmo, Section 3-5).

### Evaluation and the curvature test

```pseudo id=main
RULED-K(a, a′, b, b′, u, v)
L1  w ← b(u) − a(u);  w′ ← b′(u) − a′(u)
L2  S_u ← (1 − v) a′(u) + v b′(u);  S_v ← w
L3  n ← S_u × S_v
L4  if n = 0 then error "singular point"
L5  δ ← det(a′(u), w, w′)
L6  return −δ² / (n · n)²
```

The point itself is $S(u, v) = (1 - v)\, a(u) + v\, b(u)$: two curve evaluations and one interpolation. If $a$ and $b$ are [Bézier curves](/bezier-curve/) of degree $m$ with control points $a_i$ and $b_i$ (raise the degree of one if they differ), the surface is the [Bézier patch](/bezier-patch/) of degree $(m, 1)$ with the two rows $a_i$ and $b_i$, and the cost per point is $m(m + 1)$ linear interpolations for the two curves and one more for the ruling. The curvature test costs a constant number of arithmetic operations on top of the curve values and derivatives. These are exact operation counts in the real RAM model. The routine uses only $+$, $-$, $\times$ and $/$, so on rational input it decides exactly whether a point is flat, and $\delta = 0$ at all $u$ in a sample does not prove developability between the samples.

## Examples and non-examples

- **The saddle.** $a(u) = (u, 0, 0)$ and $b(u) = (u, 1, u)$ give $S(u, v) = (u, v, uv)$, the graph $z = xy$. Here $w = (0, 1, u)$, $w' = (0, 0, 1)$ and $\det(a', w, w') = \det((1, 0, 0), (0, 1, u), (0, 0, 1)) = 1$, and $|S_u \times S_v|^2 = 1 + u^2 + v^2$, so $K = -1/(1 + x^2 + y^2)^2$. The saddle is doubly ruled: the lines with $y$ fixed are rulings too. It is also the [bilinear patch](/bilinear-interpolation/) of the corners $(0, 0, 0)$, $(1, 0, 0)$, $(0, 1, 0)$, $(1, 1, 1)$.
- **The hyperboloid of one sheet.** Take $a(u)$ on the unit circle at height $z = -1$ and $b(u)$ the same point turned by an angle $\theta$ about the $z$ axis at height $z = +1$. With $\cos \theta = 3/5$ the segments sweep the hyperboloid $x^2 / (4/5) + y^2 / (4/5) - z^2 / 4 = 1$: the waist at $z = 0$ has radius squared $(1 + \cos \theta)/2 = 4/5$. Turning by $-\theta$ gives the second family of rulings on the same surface. $\det(a', w, w') \ne 0$, so the surface is not developable, and $K < 0$ everywhere. With a rational parametrization of the circle, every point and every value of $K$ checks exactly against the closed form $K = -1/(a^4 c^2 (x^2/a^4 + y^2/a^4 + z^2/c^4)^2)$ with $a^2 = 4/5$, $c^2 = 4$.
- **The helicoid.** $a(u) = (0, 0, bu)$ and $w(u) = (\cos u, \sin u, 0)$. Then $\det(a', w, w') = b$, $S_u = (-v \sin u, v \cos u, b)$ is orthogonal to $w$, and $K = -b^2/(b^2 + v^2)^2$. The helicoid is also a minimal surface, with mean curvature $0$.
- **Cylinders and cones.** A constant direction $w$ gives a general cylinder, with $w' = 0$, so $\delta = 0$. A constant directrix $a(u) = p$ gives a cone with apex $p$, with $a' = 0$, so $\delta = 0$. Both are developable. The cone is singular at the apex, where $S_u = 0$.
- **Tangent developables.** For a space curve $c$, the surface $c(u) + v\, c'(u)$ has $a' = w = c'$, so $\delta = \det(c', c', c'') = 0$. For the twisted cubic $c(u) = (u, u^2, u^3)$ this gives a developable surface that is not a cylinder or a cone. It is singular along $c$ itself, where $v = 0$ and $S_u = c'$ is parallel to $S_v$.
- **Non-example: the sphere.** Its Gaussian curvature is positive, and a ruled surface has $K \le 0$, so no piece of a sphere is ruled. The same argument rules out every surface with an elliptic point, such as the outer part of a torus.
- **Non-example: a ruled surface is not a sweep of a profile.** A [sweep surface](/sweep-surface/) moves a whole curve along a path, and a [surface of revolution](/surface-of-revolution/) turns one about an axis. Both are ruled only in special cases, such as a straight profile: the hyperboloid above is a surface of revolution of a hyperbola and also ruled, but the torus is not ruled.

## Related definitions

- [Coons patch](/coons-patch/): the sum of the ruled surfaces between opposite boundary curves, minus the bilinear corner patch. With two straight boundaries it is the ruled surface.
- [Bilinear interpolation](/bilinear-interpolation/): the ruled surface between two straight segments.
- [Bézier patch](/bezier-patch/) and [tensor-product surface](/tensor-product-surface/): a ruled surface between two polynomial curves is a tensor-product patch of degree 1 in $v$.
- [Fundamental forms](/fundamental-forms/) and [surface curvature](/surface-curvature/): the general formulas that the curvature proof above uses.
- [Sweep surface](/sweep-surface/) and [surface of revolution](/surface-of-revolution/): other surfaces made from curves.

## References
