---
tag: 326WHE
kind: definition
slug: developable-surface
name: Developable surface
aliases:
- torse
area: cad/surface-interrogation-and-design
level: core
summary: A surface of zero Gaussian curvature that unrolls onto the plane without stretching, made of pieces of cylinders, cones and tangent surfaces of curves.
prereqs: [ruled-surface, surface-curvature, fundamental-forms]
see_also: [developable-surface-approximation, flat-pattern-development, geodesics-on-parametric-surfaces, lines-of-curvature, offset-surface, discrete-gaussian-curvature, mesh-parameterization, frenet-frame]
sources:
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 3-3 (the equations of Weingarten); Section 3-4 (coordinates by lines of curvature near a non-umbilical point); Section 3-5 (ruled and developable surfaces); Section 4-2 (isometries, and local isometry from equal coefficients of the first form); Section 4-3 (the Gauss theorem); Section 4-6 (Minding's theorem on surfaces of constant curvature)
  - book: isbn:9783540420583
    title: Helmut Pottmann and Johannes Wallner, Computational Line Geometry, Springer, 2001
    locator: Chapter 6, Developable Surfaces (the dual representation as the envelope of a one-parameter family of planes, the edge of regression, and the classification into cylinders, cones and tangent surfaces)
---

A developable surface is a surface that can be unrolled onto the plane without stretching, tearing or shrinking: every small piece of it is isometric to a piece of the plane. Its Gaussian curvature is zero, and away from planar points it is a ruled surface whose tangent plane stays the same along each ruling, which is the classical name *torse*. Cylinders, cones and the surfaces swept by the tangent lines of a space curve are developable. In manufacture these are the shapes that can be bent from flat sheet metal, plywood, paper or cloth, so a CAD system needs to know whether a surface is developable and how to compute its flat pattern.

## Definition

Let $S$ be a regular smooth surface in $\mathbb{R}^3$ with a parametrization $r(u, v)$. This page uses the unit normal $n = r_u \times r_v / |r_u \times r_v|$, the coefficients $E, F, G$ of the first form and $L, M, N$ of the second form for this $n$ (see [fundamental forms](/fundamental-forms/)), $K = k_1 k_2$, and $H = (k_1 + k_2)/2$ (see [surface curvature](/surface-curvature/)). Replacing $n$ by $-n$ changes the signs of $L, M, N$ and $H$ but not $K$, and no statement on this page depends on the choice.

**Definition.** $S$ is *developable* if every point of $S$ has a neighbourhood $V$ and a map $\varphi : V \to \mathbb{R}^2$ onto an open set of the plane that keeps the length of every curve, that is, a local isometry to the plane (do Carmo, Section 4-2). The map $\varphi$ is a *development* of $V$, and its image is the flat pattern.

A point with $k_1 = k_2 = 0$ is a *planar point*. The facts that are used and not proved here are: the Gauss theorem that $K$ is a function of $E, F, G$ and their first and second derivatives (do Carmo, Section 4-3); the fact that two parametrizations on the same domain with equal $E, F, G$ define a local isometry (do Carmo, Section 4-2); the Weingarten equations, which with $F = M = 0$ read $n_u = -(L/E)\, r_u$ and $n_v = -(N/G)\, r_v$ (do Carmo, Section 3-3); coordinates by lines of curvature near a non-umbilic point (do Carmo, Section 3-4); and Minding's theorem (do Carmo, Section 4-6).

### Zero curvature

**Theorem 1.** If $S$ is developable, then $K = 0$ at every point.

*Proof.* Let $\varphi : V \to \mathbb{R}^2$ be a development. Then $r = \varphi^{-1}(x, y)$ is a parametrization of $V$ whose first form is that of the plane in the coordinates $x, y$: $E = G = 1$, $F = 0$. By the Gauss theorem, $K$ is given by a formula in $E, F, G$ and their derivatives, and the same formula applied to the plane gives $0$. So $K = 0$ on $V$. $\square$

**Theorem 2.** Let $S$ have $K = 0$ and no planar points. Then every point of $S$ has a neighbourhood that is a ruled surface $a(u) + v\, w(u)$ with $|w| = 1$ whose normal $n(u)$ depends on $u$ alone, with $n' \ne 0$.

*Proof.* At a point with $k_1 k_2 = 0$ that is not planar, $k_1 \ne k_2$, so the point is not an umbilic. Near it there is a parametrization $r(u, v)$ by lines of curvature, with $F = M = 0$, whose principal curvatures are $L/E$ and $N/G$. At every point exactly one of them is $0$. The sets where $L = 0$ and where $N = 0$ are closed and disjoint and cover a connected neighbourhood, so one of them, say $N = 0$, is all of it. The Weingarten equations give $n_v = 0$ and $n_u = -(L/E)\, r_u \ne 0$. So $n = n(u)$ depends on $u$ alone, and $n' = n_u$.

The vector $r_v$ is orthogonal to $n$, because it is tangent, and to $n_u$, because $n_u$ is parallel to $r_u$ and $F = 0$. Since $n$ and $n_u$ are orthogonal and nonzero, $r_v$ is parallel to the unit vector $w(u) = n \times n' / |n \times n'|$, which depends on $u$ alone. So each $v$-curve is a straight segment in direction $w(u)$. Put $a(u) = r(u, v_0)$ and $\lambda(u, v) = (r(u, v) - a(u)) \cdot w(u)$. Then $r(u, v) = a(u) + \lambda(u, v)\, w(u)$, and $\partial_v \lambda = r_v \cdot w \ne 0$, so $(u, \lambda)$ are new coordinates near the point. $\square$

In the new coordinates $a'$, $w$ and $w'$ are all orthogonal to $n(u)$: $a'$ because it is tangent, $w$ by its definition, and $w'$ because $n \cdot w = 0$ gives $n \cdot w' = -n' \cdot w = 0$. So $\det(a', w, w') = 0$, which is the [ruled surface](/ruled-surface/) test for a constant tangent plane along each ruling. The next theorem unrolls every such surface.

**Theorem 3.** Let $S(u, v) = a(u) + v\, w(u)$ with $|w| = 1$ and $\det(a', w, w') = 0$, and let $(u_0, v_0)$ be a regular point. Then a neighbourhood of $S(u_0, v_0)$ is isometric to an open set of the plane, by a map that takes each ruling to a straight segment.

*Proof.* First make the directrix orthogonal to the rulings. Let $\phi$ solve $\phi' = -a' \cdot w$ and put $\tilde a = a + \phi\, w$. Then $\tilde a' \cdot w = a' \cdot w + \phi' + \phi\, w' \cdot w = 0$, since $w \cdot w' = 0$ for a unit vector, and the surface is $\tilde a(u) + (v - \phi(u))\, w(u)$, the same surface in the coordinates $(u, v - \phi)$. Also $\det(\tilde a', w, w') = \det(a', w, w') = 0$. So write $a$ for $\tilde a$ from now on, with $a' \cdot w = 0$.

Both $a'$ and $w'$ are orthogonal to $w$, so $w' \times a'$ is parallel to $w$ and $\det(a', w, w') = w \cdot (w' \times a') = \pm |w' \times a'|$. Hence $a'$ and $w'$ are parallel. Let $v_0$ now be the new coordinate of the point. Since $S_u = a'(u_0) + v_0 w'(u_0) \ne 0$ at a regular point, one of $a'(u_0)$ and $w'(u_0)$ is nonzero; let $e(u)$ be that vector divided by its length, for $u$ near $u_0$. Then $e \perp w$, and $a' = \alpha\, e$, $w' = \beta\, e$ with $\alpha = a' \cdot e$ and $\beta = w' \cdot e$. With $h = \alpha + v \beta$,

$$S_u = h\, e, \qquad S_v = w, \qquad E = h^2, \quad F = 0, \quad G = 1,$$

and $h \ne 0$ near $(u_0, v_0)$. In the plane, let $\theta' = \beta$, $W = (\cos \theta, \sin \theta)$, $W^\perp = (-\sin \theta, \cos \theta)$, $A' = \alpha W^\perp$, and $P(u, v) = A(u) + v\, W(u)$. Then $P_u = (\alpha + v \beta) W^\perp = h W^\perp$ and $P_v = W$, so $P$ has the same $E, F, G$. Its Jacobian determinant is $\pm h \ne 0$, so by the inverse function theorem $P$ is one to one on a small neighbourhood, and $P \circ S^{-1}$ is an isometry there. Each line $v \mapsto P(u, v)$ is straight. $\square$

**Corollary.** A regular smooth surface is developable if and only if $K = 0$. Theorem 1 gives one direction. On a patch free of planar points, Theorems 2 and 3 give the other, with an explicit development. With planar points the direction from $K = 0$ to developable still holds, by Minding's theorem that two surfaces of the same constant curvature are locally isometric (do Carmo, Section 4-6), which this page does not prove. Near planar points the rulings need not be defined, as on a plane, or may be defined but fail to vary smoothly.

As a check of Theorem 3, the formula for $K$ in coordinates with $F = 0$ and $G = 1$ is $K = -h_{vv}/h$ with $h = \sqrt{E}$, and here $h = \alpha + v\beta$ is linear in $v$, so $K = 0$.

### The dual form and the three kinds

A developable surface without planar points is also the envelope of its tangent planes. In the notation of Theorem 2, the tangent plane along the ruling at $u$ is $\Pi(u) : n(u) \cdot x = h(u)$ with $h = n \cdot a$, a one-parameter family of planes. Since $h' = n' \cdot a + n \cdot a' = n' \cdot a$ and $n' \cdot w = 0$, the ruling lies in both $\Pi(u)$ and $\Pi'(u) : n'(u) \cdot x = h'(u)$, so the ruling is the line $\Pi \cap \Pi'$, with direction $n \times n'$. Conversely, for any smooth unit $n(u)$ with $n' \ne 0$ and any smooth $h(u)$, the lines $\Pi \cap \Pi'$ sweep a surface which, where it is regular, has the tangent plane $\Pi(u)$ along the whole line: a point $x(u, \lambda)$ of the line satisfies $n \cdot x = h$ and $n' \cdot x = h'$, and differentiating the first in $u$ gives $n \cdot x_u = 0$, while $n \cdot x_\lambda = 0$ because the line lies in $\Pi(u)$. This dual description, with planes as the data and rulings and points derived, is the one used for design (Pottmann and Wallner, Chapter 6).

**The edge of regression.** Let $\delta(u) = \det(n, n', n'')$. Where $\delta \ne 0$, the three planes $\Pi, \Pi', \Pi''$ meet in one point $x(u)$. Differentiating $n \cdot x = h$ and $n' \cdot x = h'$ and using the equations for $\Pi'$ and $\Pi''$ gives $n \cdot x' = 0$ and $n' \cdot x' = 0$, so $x'$ is parallel to $n \times n'$, the direction of the ruling, and $x(u)$ lies on the ruling. This proves the classification, on every interval of $u$ on which one case holds:

- **Cone.** $\delta \ne 0$ and $x' = 0$: all rulings pass through one point, the apex.
- **Tangent surface.** $\delta \ne 0$ and $x' \ne 0$: every ruling is the tangent line of the curve $x$, the *edge of regression*, where the surface is singular.
- **Cylinder.** $\delta = 0$ on the interval: $n$, $n'$ and $n''$ lie in one plane, so the spherical curve $n(u)$ is an arc of a great circle and all rulings, with direction $n \times n'$, are parallel to its axis.

So, away from the rulings where the case changes, a developable surface without planar points is a piece of a cone, a tangent surface or a cylinder.

## Examples and non-examples

### A circular cylinder

The cylinder of radius $R$ is $a(u) + v\, e_3$ with $a(u) = R (\cos(u/R), \sin(u/R), 0)$, so $a' \cdot w = 0$, $\alpha = 1$, $\beta = 0$. Theorem 3 gives $\theta = 0$, $A(u) = (0, u)$, and the development $(u, v) \mapsto (v, u)$: the metric is $du^2 + dv^2$, and a band of height $\ell$ unrolls to an $\ell \times 2\pi R$ rectangle. Every cylinder over a plane curve, with rulings orthogonal to that plane, unrolls the same way, with the curve becoming a straight segment of the same length.

### A frustum of a cone, the sheet metal transition

The ruled surface swept by the segments from $(\cos t, \sin t, 0)$ to $(2\cos t, 2\sin t, 1)$ joins a circle of radius $1$ to a circle of radius $2$, and it is part of the cone with apex $(0, 0, -1)$ and half angle $45°$. In the form of Theorem 3, $a(u) = (0, 0, -1)$, $\alpha = 0$, and $w(u)$ runs at unit speed along the circle of radius $\sin 45° = 1/\sqrt{2}$ on the unit sphere, so $\beta = 1$ and the metric is $v^2 du^2 + dv^2$: polar coordinates with angle $u$ and radius $v$. The two circles lie at slant distances $\sqrt{2}$ and $2\sqrt{2}$ from the apex, and $u$ runs over the length $2\pi / \sqrt{2} = \sqrt{2}\, \pi \approx 4.443$ of the spherical circle. So the flat pattern is the annular sector with radii $\sqrt{2}$ and $2\sqrt{2}$ and angle $\sqrt{2}\,\pi$. Its arcs have lengths $\sqrt{2} \cdot \sqrt{2}\,\pi = 2\pi$ and $2\sqrt{2} \cdot \sqrt{2}\,\pi = 4\pi$, the circumferences of the two circles, as they must.

### A cone that cannot be unrolled in one piece

The development of a cone with apex $p$ is a sector whose angle is the length of the spherical curve $w$, so it is one to one only while this length is below $2\pi$. For $w(t) = (\cos t, \sin t, \sin 4t)$ divided by its length, $0 \le t \le 2\pi$, the length is about $14.03$, which is more than twice $2\pi$. The cone $p + v\, w(t)$, $v > 0$, is embedded in space, since rays from $p$ in different directions meet only at $p$, but its development covers the plane around the apex more than twice. Developability is a local property, and a flat pattern of a large piece may overlap itself and need cuts.

### The tangent surface of a helix

Let $c(s)$ be a space curve in arc length with curvature $\kappa > 0$, tangent $T$ and principal normal $N$ (see [Frenet frame](/frenet-frame/)), and $S(s, v) = c(s) + v\, T(s)$. Then $S_s = T + v\kappa N$ and $S_v = T$, so

$$E = 1 + v^2 \kappa^2, \qquad F = 1, \qquad G = 1, \qquad EG - F^2 = v^2 \kappa^2.$$

The first form depends on $\kappa$ alone and not on the torsion, so the surface is isometric, on each of the sheets $v > 0$ and $v < 0$, to the tangent surface of a plane curve $\gamma$ with the same curvature $\kappa(s)$, which is a region of the plane: $\gamma(s) + v\, \gamma'(s)$ has the same $E, F, G$. For the helix $c(s) = (\cos(s/\sqrt{2}), \sin(s/\sqrt{2}), s/\sqrt{2})$ the curvature is $\kappa = 1/2$, so $\gamma$ is the circle of radius $2$, and the sheet $v > 0$ develops onto the outside of that circle, each ruling becoming a forward tangent ray. One turn of the helix has length $2\sqrt{2}\,\pi \approx 8.886$ and maps to an arc of angle $\sqrt{2}\,\pi$. The development is one to one while the arc is shorter than the full circle, $4\pi$, that is, for less than $\sqrt{2}$ turns of the helix. Each point outside the circle lies on exactly one forward tangent ray of the full circle, which is why a longer piece overlaps. The edge of regression is the helix itself, where $EG - F^2 = 0$.

### Non-examples

- **The sphere.** $K = 1/R^2 > 0$, so by Theorem 1 no piece of a sphere is isometric to the plane, and every flat map of the earth distorts lengths.
- **Ruled surfaces with $K < 0$.** The saddle, the hyperboloid of one sheet and the helicoid on the [ruled surface](/ruled-surface/) page are made of lines, but their tangent planes turn along each ruling, so they are not developable. Being ruled is not enough.
- **A torus.** $K$ vanishes on the top and bottom circles and nowhere else, so no open piece of the torus is developable. Zero curvature along a curve is not enough.

## Related definitions

- **Ruled surface.** A surface swept by a line; the developable ones are those with $\det(a', w, w') = 0$, as on the [ruled surface](/ruled-surface/) page, which also gives the formula for $K$ that this page does not repeat.
- **Gauss image.** Since $n_u \times n_v = K\, r_u \times r_v$ (do Carmo, Section 3-3), the Gauss map $n$ has rank less than $2$ everywhere exactly when $K = 0$. Theorem 2 shows more for a patch without planar points: the image of $n$ on the unit sphere is the regular curve $n(u)$, one point per ruling.
- **Lines of curvature.** On a developable surface without planar points, the rulings are the lines of curvature with $k = 0$, and their orthogonal trajectories are the other family; see [lines of curvature](/lines-of-curvature/). The normal surface along a curve is developable exactly when the curve is a line of curvature.
- **Geodesics.** A development keeps lengths, so it maps geodesics to straight segments; see [geodesics on parametric surfaces](/geodesics-on-parametric-surfaces/).
- **Offset surfaces.** The normal is constant along each ruling, so the [offset surface](/offset-surface/) $S + d\, n$ moves each ruling to a parallel line, along which the offset has the fixed normal $n(u)$, so the offset is again developable where it is regular.
- **Discrete developable surfaces.** The triangles around an interior vertex of a mesh unfold into the plane without distortion and without a gap exactly when their angles at the vertex sum to $2\pi$, the discrete form of $K = 0$; see [discrete Gaussian curvature](/discrete-gaussian-curvature/). For sheet metal parts made of flat faces and cylindrical bends, see [flat pattern development](/flat-pattern-development/).
- **Developable approximation.** Fitting developable patches to given data, see [developable surface approximation](/developable-surface-approximation/).

## References
