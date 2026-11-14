---
tag: RG4XP6
kind: definition
slug: lines-of-curvature
name: Lines of curvature
aliases:
- curvature lines
- principal curvature lines
area: cad/surface-interrogation-and-design
level: core
summary: "Curves on a surface whose tangent is a principal direction at every point. Away from umbilics they form an orthogonal net, given by a quadratic equation in du and dv."
prereqs: [surface-curvature, fundamental-forms]
see_also: [umbilic-point, surface-curvature, geodesics-on-parametric-surfaces, isophote, ruled-surface, developable-surface, surface-of-revolution, runge-kutta-methods]
sources:
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 3-2 (lines of curvature and the theorem of Olinde Rodrigues); Section 3-3 (the differential equation of the lines of curvature); Section 3-4 (a parametrization by lines of curvature near a non-umbilical point)
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 9, Umbilics and Lines of Curvature (Section 9.4, integration of the lines of curvature)
  - paper: "Takashi Maekawa, Franz-Erich Wolter and Nicholas M. Patrikalakis, Umbilics and lines of curvature for shape interrogation, Computer Aided Geometric Design 13(2), 133 to 161, 1996"
    title: Maekawa, Wolter and Patrikalakis 1996
    locator: the differential equation of the lines of curvature, and their integration on parametric surfaces near and away from umbilics
---

A line of curvature on a regular surface is a curve whose tangent at every point is a principal direction of the surface, that is, a direction in which the normal curvature is largest or smallest. Away from [umbilic points](/umbilic-point/) the two principal directions are distinct and orthogonal, so the lines of curvature cover the surface with two families of curves that cross at right angles. They are the integral curves of a quadratic differential equation in the coefficients of the [fundamental forms](/fundamental-forms/), and CAD systems draw them to show how a surface bends.

## Definition

Let $r(u, v)$ be a regular $C^3$ surface. This page uses the unit normal $n = r_u \times r_v / |r_u \times r_v|$, the coefficients $E, F, G$ of the first form $\mathrm{I}$, and $L = r_{uu} \cdot n$, $M = r_{uv} \cdot n$, $N = r_{vv} \cdot n$ of the second form $\mathrm{II}$. The mean curvature is $H = (k_1 + k_2)/2$ for this $n$, and $K = k_1 k_2$ (see [surface curvature](/surface-curvature/)). Replacing $n$ by $-n$ changes the signs of $L, M, N$, of the principal curvatures and of $H$, but no result on this page depends on that choice.

A tangent direction $d = (du, dv) \ne 0$ is a *principal direction* if it is an eigenvector of the shape operator $W = \mathrm{I}^{-1} \mathrm{II}$, where $\mathrm{I}$ and $\mathrm{II}$ are the symmetric $2 \times 2$ matrices of the two forms. A regular curve $\alpha(t) = r(u(t), v(t))$ is a *line of curvature* if $(u'(t), v'(t))$ is a principal direction for every $t$.

### The differential equation

**Theorem.** A direction $d = (du, dv) \ne 0$ is principal if and only if

$$(LF - ME)\, du^2 + (LG - NE)\, du\, dv + (MG - NF)\, dv^2 = 0.$$

*Proof.* Since $\mathrm{I}$ is invertible, $W d = k d$ holds if and only if $\mathrm{II}\, d = k\, \mathrm{I}\, d$. The vector $\mathrm{I}\, d$ is not zero, because $\mathrm{I}$ is positive definite. So $d$ is principal if and only if the two plane vectors $\mathrm{I}\, d = (E\, du + F\, dv,\ F\, du + G\, dv)$ and $\mathrm{II}\, d = (L\, du + M\, dv,\ M\, du + N\, dv)$ are parallel, that is, if and only if their $2 \times 2$ determinant is zero:

$$(E\, du + F\, dv)(M\, du + N\, dv) - (F\, du + G\, dv)(L\, du + M\, dv) = (EM - FL)\, du^2 + (EN - GL)\, du\, dv + (FN - GM)\, dv^2.$$

This is the negative of the left side of the theorem. $\square$

The same equation is the determinant condition

$$\det \begin{pmatrix} dv^2 & -du\, dv & du^2 \\ E & F & G \\ L & M & N \end{pmatrix} = 0.$$

A line of curvature is therefore a solution of the first order equation $Q(u', v') = 0$, where $Q(d) = a\, du^2 + b\, du\, dv + c\, dv^2$ with $a = LF - ME$, $b = LG - NE$, $c = MG - NF$. The eigenvalue that belongs to a principal direction $d$ is $k = \mathrm{II}(d, d)/\mathrm{I}(d, d)$, so it is one of the principal curvatures.

### The discriminant

**Theorem.** $b^2 - 4ac = 4 (EG - F^2)^2 (H^2 - K)$.

*Proof.* Write $Q(d) = \det(\mathrm{I}\, d,\ \mathrm{II}\, d)$ up to sign, as in the proof above, and let $S$ be the symmetric matrix of $Q$, so that $b^2 - 4ac = -4 \det S$. Let $P$ be an invertible $2 \times 2$ matrix and put $\mathrm{I}' = P^{\mathsf T} \mathrm{I} P$, $\mathrm{II}' = P^{\mathsf T} \mathrm{II} P$. Then $\det(\mathrm{I}' d, \mathrm{II}' d) = \det(P^{\mathsf T}) \det(\mathrm{I} P d, \mathrm{II} P d)$, so $S' = \det(P)\, P^{\mathsf T} S P$ and $\det S' = \det(P)^4 \det S$. On the right side, $EG - F^2 = \det \mathrm{I}$ becomes $\det(P)^2 \det \mathrm{I}$, and $W' = P^{-1} W P$ is similar to $W$, so $H = \operatorname{tr} W / 2$ and $K = \det W$ do not change. So both sides are multiplied by $\det(P)^4$, and it is enough to check the identity for one $P$. Because $\mathrm{I}$ is positive definite, some $P$ gives $\mathrm{I}' = \mathrm{Id}$ and $\mathrm{II}' = \operatorname{diag}(k_1, k_2)$. Then $E = G = 1$, $F = M = 0$, $L = k_1$, $N = k_2$, so $a = c = 0$, $b = k_1 - k_2$, and the left side is $(k_1 - k_2)^2$. The right side is $4 \cdot 1 \cdot ((k_1 + k_2)^2/4 - k_1 k_2) = (k_1 - k_2)^2$. $\square$

So at every point there are two cases.

- **Non-umbilic point**, $H^2 > K$. The form $Q$ has two distinct real linear factors, so there are exactly two principal directions. They are eigenvectors of $W$ for the distinct eigenvalues $k_1 \ne k_2$, and $W$ is self-adjoint for $\mathrm{I}$, so they are orthogonal on the surface. In coordinates, the identity $Ec - Fb + Ga = 0$ holds for all six coefficients, and for $a \ne 0$ the roots $t_i = du/dv$ satisfy $t_1 t_2 = c/a$ and $t_1 + t_2 = -b/a$, which gives $E t_1 t_2 + F (t_1 + t_2) + G = 0$.
- **Umbilic point**, $H^2 = K$. Then $\mathrm{II}$ is a multiple of $\mathrm{I}$, all three coefficients $a, b, c$ vanish, and every direction is principal. The proof and the behaviour of the lines nearby are on the [umbilic point](/umbilic-point/) page.

### Lines of curvature as integral curves

On an open set $U$ free of umbilics, each family of principal directions is a smooth line field, because a simple eigenvalue of a smooth symmetric matrix and its eigenline depend smoothly on the entries. By the existence and uniqueness theorem for ordinary differential equations, exactly one line of curvature of each family passes through each point of $U$. Near a non-umbilic point there is a parametrization in which the coordinate curves are lines of curvature (do Carmo, Section 3-4).

**Coordinate test.** At a non-umbilic point, the two coordinate directions are principal if and only if $F = M = 0$. If $F = M = 0$, then $a = c = 0$ and $Q = (LG - NE)\, du\, dv$, whose zero directions are $du = 0$ and $dv = 0$. Conversely, $Q(1, 0) = a$ and $Q(0, 1) = c$, so both vanish. The two directions are then distinct principal directions, which are orthogonal, so $F = 0$, and $a = -ME = 0$ with $E > 0$ gives $M = 0$.

**Rodrigues' formula.** Along a line of curvature, $\frac{d}{dt} n(\alpha(t)) = -k(t)\, \alpha'(t)$, where $k(t)$ is the principal curvature of the direction $\alpha'(t)$ (do Carmo, Section 3-2). Conversely, a curve along which $n'$ is parallel to $\alpha'$ is a line of curvature.

### Tracing a line of curvature

A program traces a line of curvature from a seed point with an ODE solver such as a [Runge-Kutta method](/runge-kutta-methods/). At each stage it finds the principal curvature $k$ of the chosen family and a direction $x$ with $(W - kI)x = 0$, takes the longer of $(W_{12}, k - W_{11})$ and $(k - W_{22}, W_{21})$, and scales it to unit length in $\mathrm{I}$. A line field has no orientation, so the program flips $x$ when its $\mathrm{I}$ inner product with the previous direction is negative. Without this step the solver can turn back on itself. The field is undefined at umbilics and badly conditioned near them, so the step size must shrink there, and lines that run into an umbilic need the local analysis of the umbilic point page (Maekawa, Wolter and Patrikalakis 1996).

## Examples and non-examples

### A paraboloid at one point

Take $r(u, v) = (u, v, (u^2 + 2v^2)/2)$ at $(u, v) = (1, 1)$, with the upward normal $n = (-u, -2v, 1)/\sqrt{1 + u^2 + 4v^2}$. Here $r_u = (1, 0, 1)$, $r_v = (0, 1, 2)$, so $E = 2$, $F = 2$, $G = 5$, and $EG - F^2 = 6$. With $r_{uu} = (0, 0, 1)$, $r_{uv} = 0$, $r_{vv} = (0, 0, 2)$ and $|r_u \times r_v| = \sqrt 6$, we get $L = 1/\sqrt 6$, $M = 0$, $N = 2/\sqrt 6$.

- **The equation.** $a = 2/\sqrt 6$, $b = 1/\sqrt 6$, $c = -4/\sqrt 6$. After multiplying by $\sqrt 6$, the equation is $2\, du^2 + du\, dv - 4\, dv^2 = 0$, with roots $du/dv = (-1 \pm \sqrt{33})/4$, that is $1.18614$ and $-1.68614$.
- **The curvatures.** $H = 9/(12\sqrt 6) = \sqrt 6/8 \approx 0.306186$ and $K = (2/6)/6 = 1/18$, so $H^2 - K = 11/288$ and $k_{1,2} = (3\sqrt 6 \pm \sqrt{22})/24$, that is $k_1 \approx 0.501620$ and $k_2 \approx 0.110752$. The direction $du/dv = -1.68614$ has normal curvature $k_1$, and $du/dv = 1.18614$ has $k_2$.
- **The discriminant.** $b^2 - 4ac = (1 + 32)/6 = 11/2$, and $4 \cdot 6^2 \cdot 11/288 = 11/2$.
- **Orthogonality.** $E t_1 t_2 + F (t_1 + t_2) + G = 2 \cdot (-2) + 2 \cdot (-1/2) + 5 = 0$. In space the unit tangents $t_i r_u + r_v$ are $(0.33471, 0.28218, 0.89908)$ and $(-0.84930, 0.50369, 0.15809)$, and their dot product is zero.

### A cylinder, and a helix that is not a line of curvature

On $r(u, v) = (\cos u, \sin u, v)$ with the outward normal $n = (\cos u, \sin u, 0)$, $E = G = 1$, $F = 0$, $L = -1$, $M = N = 0$. Then $a = c = 0$, $b = -1$, and the equation is $-du\, dv = 0$. The lines of curvature are the circles $v = \text{const}$ and the rulings $u = \text{const}$. The helix $(u, v) = (t, ht)$ with $h \ne 0$ has $Q(1, h) = -h \ne 0$, so it is not a line of curvature, although it is a geodesic.

### Planes of symmetry

If a reflection of space in a plane $\Pi$ maps the surface to itself, then each curve in which $\Pi$ cuts the surface transversally is a line of curvature. At such a point $p$ the reflection fixes $p$ and the tangent $T$ of the curve, and maps the tangent plane to itself. Its differential on the tangent plane fixes $T$ and negates the orthogonal tangent vector $e$, and since a reflection of space has only one eigenvalue $-1$, it fixes $n$. A rigid motion that maps the surface to itself and fixes $n$ at $p$ commutes with $W$ at $p$, so $W$ maps the eigenlines $\mathbb{R} T$ and $\mathbb{R} e$ of the reflection to themselves, and $T$ is principal. Examples are the meridians of a [surface of revolution](/surface-of-revolution/) and the diagonal $u = v$ of the saddle $z = uv$. At $(1, 1)$ on that saddle, $a = -2/\sqrt 3$, $b = 0$, $c = 2/\sqrt 3$, and $Q(1, 1) = Q(1, -1) = 0$.

### Non-examples: planes and spheres

On a plane or a sphere every point is an umbilic, $Q$ vanishes identically, and every curve satisfies the equation. The definition holds, but the lines of curvature do not form a net, and a CAD system cannot draw them. A surface that is nearly spherical has well defined but unstable lines of curvature: a small change of the surface can turn them by a large angle.

## Related definitions

- **Principal curvatures and directions.** The eigenvalues and eigenvectors of $W$, defined on the [surface curvature](/surface-curvature/) page.
- **Umbilic point.** A point with $k_1 = k_2$, where the line fields are singular; see [umbilic point](/umbilic-point/).
- **Asymptotic lines.** Curves whose tangent has normal curvature zero, the solutions of $L\, du^2 + 2M\, du\, dv + N\, dv^2 = 0$. They exist only where $K \le 0$.
- **Conjugate directions.** Directions $d, e$ with $\mathrm{II}(d, e) = 0$. At a non-umbilic point the principal directions are the only pair that is both orthogonal and conjugate. In a principal frame, $d = (\cos \theta, \sin \theta)$ and $e = (-\sin \theta, \cos \theta)$ give $\mathrm{II}(d, e) = (k_2 - k_1) \sin \theta \cos \theta$, which is zero only for $\theta$ a multiple of $\pi/2$.
- **Normal surface along a curve.** The [ruled surface](/ruled-surface/) $\alpha(t) + s\, n(\alpha(t))$ is a [developable surface](/developable-surface/) if and only if $\alpha$ is a line of curvature. The ruled surface test is $\det(\alpha', n, n') = 0$. Both $\alpha'$ and $n'$ are tangent to the surface, so $\alpha' \times n'$ is a multiple of $n$, and the determinant is $\pm |\alpha' \times n'|$. It vanishes if and only if $n'$ is parallel to $\alpha'$, which is Rodrigues' condition.
- **Geodesics.** Curves with zero geodesic curvature, a different family of curves on a surface; see [geodesics on parametric surfaces](/geodesics-on-parametric-surfaces/).

## References
