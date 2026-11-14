---
tag: 4PXAM0
kind: definition
slug: umbilic-point
name: Umbilic point
aliases:
- umbilic
- umbilical point
area: cad/surface-interrogation-and-design
level: advanced
summary: A point where the two principal curvatures of a surface are equal, a singularity of the lines of curvature, classed as star, lemon or monstar.
prereqs: [lines-of-curvature, surface-curvature]
see_also: [lines-of-curvature, surface-curvature, fundamental-forms, interval-projected-polyhedron, polynomial-system-solving]
sources:
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 9, Umbilics and Lines of Curvature (Section 9.2, lines of curvature near umbilics; Section 9.3, the Monge form and the classification of generic umbilics)
  - paper: doi:10.1088/0305-4470/10/11/009
    title: "M. V. Berry and J. H. Hannay, Umbilic points on Gaussian random surfaces, Journal of Physics A 10(11), 1977"
    locator: pp. 1809 to 1821 (the names star, lemon and monstar, the index and the number of straight lines of curvature through a generic umbilic)
  - paper: "Takashi Maekawa, Franz-Erich Wolter and Nicholas M. Patrikalakis, Umbilics and lines of curvature for shape interrogation, Computer Aided Geometric Design 13(2), 133 to 161, 1996"
    title: Maekawa, Wolter and Patrikalakis 1996
    locator: computation of the umbilics of polynomial parametric surfaces and the lines of curvature through them
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 3-2 (umbilical points, and a connected surface made only of umbilical points lies in a plane or a sphere)
---

An umbilic point of a regular surface is a point where the two principal curvatures are equal, so that the surface bends by the same amount in every direction, to second order. There every tangent direction is principal, the two families of [lines of curvature](/lines-of-curvature/) meet in a singular point, and the usual principal frame does not exist. Generic umbilics are isolated and have one of three local patterns of lines of curvature, called star, lemon and monstar, and CAD systems locate them because they spoil curvature line plots and the integration of those lines.

## Definition

Let $r(u, v)$ be a regular $C^3$ surface with unit normal $n = r_u \times r_v / |r_u \times r_v|$, first form coefficients $E, F, G$, and second form coefficients $L = r_{uu} \cdot n$, $M = r_{uv} \cdot n$, $N = r_{vv} \cdot n$. The mean curvature is $H = (k_1 + k_2)/2$ for this $n$, and $K = k_1 k_2$, as on the [surface curvature](/surface-curvature/) page. A point $p$ is an *umbilic* if $k_1(p) = k_2(p)$, that is, if $H^2 - K = 0$. Changing $n$ to $-n$ changes the sign of both curvatures and keeps this condition, so the umbilics do not depend on the orientation.

**Theorem.** At a point $p$ the following are equivalent.

1. $p$ is an umbilic.
2. $\mathrm{II} = k\, \mathrm{I}$ at $p$ for some real $k$, that is $(L, M, N) = k (E, F, G)$.
3. The three coefficients $LF - ME$, $LG - NE$ and $MG - NF$ of the line of curvature equation all vanish.
4. $LF - ME = 0$ and $LG - NE = 0$.

When they hold, $k = k_1 = k_2$, and every tangent direction is a principal direction.

*Proof.* (1) implies (2). The shape operator $W = \mathrm{I}^{-1} \mathrm{II}$ is self-adjoint for the inner product $\mathrm{I}$. In a basis that is orthonormal for $\mathrm{I}$ its matrix is symmetric, so it is diagonalizable, and with both eigenvalues equal to $k$ it is $k$ times the identity. So $W = k\, \mathrm{Id}$, and $\mathrm{II} = \mathrm{I} W = k\, \mathrm{I}$. (2) implies (3): substitute $L = kE$, $M = kF$, $N = kG$; each coefficient becomes $k(EF - FE)$, $k(EG - GE)$ or $k(FG - GF)$, which is zero. (3) implies (4) trivially. (4) implies (2): $E > 0$, so put $k = L/E$. Then $LF - ME = 0$ gives $M = kF$, and $LG - NE = 0$ gives $N = kG$. (2) implies (1): $W = k\, \mathrm{Id}$ has the double eigenvalue $k$. Finally, with $W = k\, \mathrm{Id}$, every $d \ne 0$ satisfies $W d = k d$. $\square$

So at an umbilic the second fundamental form gives no preferred direction, and the principal directions are undefined. The equation of the lines of curvature degenerates to $0 = 0$ there.

### Finding umbilics

Item 4 shows that the umbilics are the common zeros of two functions of $(u, v)$, a square system whose solutions are isolated in the generic case. For a polynomial or rational surface, multiplying $L, M, N$ by $|r_u \times r_v|$ makes both equations polynomial, and a solver for [polynomial systems](/polynomial-system-solving/), such as the [interval projected polyhedron algorithm](/interval-projected-polyhedron/), can find all umbilics in a parameter box (Patrikalakis and Maekawa, Chapter 9; Maekawa, Wolter and Patrikalakis 1996). A program must not search for sign changes of $H^2 - K$: this function is never negative, so an umbilic is a minimum with value zero, and it is not bracketed by a change of sign. In floating point the test $H^2 - K = 0$ is also badly conditioned, because $H^2 - K$ is the difference of two nearly equal numbers and has a double zero at the umbilic. At a generic umbilic the two functions of item 4 have a simple common zero instead: in the Monge frame below they are $-(bx + cy)$ and $2P$ to first order, and the determinant of this linear map is $\pm\Delta \ne 0$.

### Index and the local pattern

The *index* of an isolated umbilic is the number of turns of a principal line field along a small circle around it, traversed once counterclockwise. A line has no orientation, so the index is a multiple of $1/2$. It does not depend on which of the two families is used, nor on the sign of $n$.

Put the umbilic at the origin with tangent plane $z = 0$ and $n = (0, 0, 1)$, and write the surface in Monge form,

$$z = \frac{k}{2}(x^2 + y^2) + \frac{1}{6}\left(a x^3 + 3b x^2 y + 3c x y^2 + d y^3\right) + O(\rho^4), \qquad \rho = \sqrt{x^2 + y^2}.$$

**Theorem.** If $\Delta = (a - c) c - b (b - d) \ne 0$, the umbilic is isolated and its index is $\frac{1}{2} \operatorname{sign} \Delta$.

*Proof.* For the graph $z = f(x, y)$, the gradient of $f$ is $O(\rho)$, so $\mathrm{I} = \mathrm{Id} + O(\rho^2)$ and $|r_x \times r_y| = 1 + O(\rho^2)$. Hence $W = \nabla^2 f + O(\rho^2)$, with

$$\nabla^2 f = \begin{pmatrix} k + ax + by & bx + cy \\ bx + cy & k + cx + dy \end{pmatrix} = \left(k + \tfrac{(a + c) x + (b + d) y}{2}\right) \mathrm{Id} + \begin{pmatrix} P & Q \\ Q & -P \end{pmatrix},$$

where $P = ((a - c)x + (b - d)y)/2$ and $Q = bx + cy$. A multiple of $\mathrm{Id}$ has no effect on the eigenvectors. The eigenvector of $\begin{pmatrix} P & Q \\ Q & -P \end{pmatrix}$ for its positive eigenvalue has angle $\theta$ with $(\cos 2\theta, \sin 2\theta)$ parallel to $(P, Q)$. The map $(x, y) \mapsto (P, Q)$ is linear with determinant $\Delta/2 \ne 0$, so on the circle of radius $\rho$ it stays at distance at least $m \rho$ from zero for some $m > 0$, while the error terms are $O(\rho^2)$. For small $\rho$ the traceless part of $W$ is therefore never zero on the circle, so there is no other umbilic nearby, and the straight line homotopy from $W$ to $\nabla^2 f$ does not pass through zero, so both have the same winding. A linear map with positive determinant winds once around zero in the same sense, and one with negative determinant winds once in the opposite sense. So $2\theta$ turns by $\pm 2\pi$, and $\theta$ turns by $\pm \pi$, which is an index of $\pm 1/2$. $\square$

**Straight lines of curvature.** A line of curvature reaches the umbilic along the direction $\theta$ only if $(\cos \theta, \sin \theta)$ is an eigenvector of the traceless part at the point $(\cos \theta, \sin \theta)$, that is

$$C(\theta) = Q \cos 2\theta - P \sin 2\theta = 0, \qquad P, Q \text{ taken at } (x, y) = (\cos \theta, \sin \theta).$$

$C$ is a binary cubic form in $(\cos \theta, \sin \theta)$, so it has one or three real root directions in $[0, \pi)$ when its roots are simple. The generic umbilics are then of three kinds (Berry and Hannay 1977; Patrikalakis and Maekawa, Section 9.3):

| kind | index | straight lines of curvature through the umbilic |
|---|---|---|
| star | $-1/2$ | 3 |
| monstar | $+1/2$ | 3 |
| lemon | $+1/2$ | 1 |

A monstar has the index of a lemon and the three straight lines of a star, so neither number alone fixes the kind. The three names are from Berry and Hannay (1977).

## Examples and non-examples

### A family that shows all three kinds

Take $b = d = 0$ and $c = 1$, so $z = \frac{k}{2}(x^2 + y^2) + \frac{1}{6}(a x^3 + 3 x y^2)$. Then $\Delta = a - 1$, $P = (a - 1) x / 2$ and $Q = y$, and

$$C(\theta) = \sin \theta \cos 2\theta - (a - 1) \sin \theta \cos^2 \theta = \sin \theta \left( (3 - a) \cos^2 \theta - 1 \right).$$

The root $\theta = 0$ always exists. The other factor has two roots in $(0, \pi)$, at $\cos^2 \theta = 1/(3 - a)$, exactly when $a < 2$, and none when $a > 2$. So the umbilic is a star for $a < 1$, a monstar for $1 < a < 2$, and a lemon for $a > 2$.

| $a$ | $\Delta$ | index | real roots of $C$ | kind |
|---|---|---|---|---|
| $0$ | $-1$ | $-1/2$ | 3, at $\cos^2 \theta = 1/3$ and $\theta = 0$ | star |
| $3/2$ | $1/2$ | $+1/2$ | 3, at $\cos^2 \theta = 2/3$ and $\theta = 0$ | monstar |
| $3$ | $2$ | $+1/2$ | 1, at $\theta = 0$ | lemon |

At $a = 1$ and at $a = 2$ the umbilic is not generic: at $a = 1$, $\Delta = 0$ and the index changes, and at $a = 2$, $C(\theta) = -\sin^3 \theta$ and the three root directions merge into one.

### The monkey saddle cubic

$z = \frac{k}{2}(x^2 + y^2) + \frac{1}{6}(x^3 - 3 x y^2)$ has $(a, b, c, d) = (1, 0, -1, 0)$ and $\Delta = 2 \cdot (-1) = -2$, so it is a star. Its three straight lines are at $\theta = 0, \pi/3, 2\pi/3$, the directions of its threefold symmetry.

### Two umbilics of an elliptic paraboloid

On $r(u, v) = (u, v, (u^2 + 2v^2)/2)$ with the upward normal, $w = \sqrt{1 + u^2 + 4v^2}$, $E = 1 + u^2$, $F = 2uv$, $G = 1 + 4v^2$, $L = 1/w$, $M = 0$, $N = 2/w$. By item 2 an umbilic needs $M = kF$, so $kF = 0$ with $k = L/E > 0$, and $uv = 0$. On $v = 0$, $F = M = 0$ and the normal curvatures along the two axes are $L/E = 1/w^3$ and $N/G = 2/w$, which are never equal. On $u = 0$ they are $L/E = 1/w$ and $N/G = 2/w^3$, equal exactly when $w^2 = 2$, that is $v = \pm 1/2$. So the paraboloid has exactly two umbilics, at $(0, \pm 1/2, 1/4)$, with $k = 1/\sqrt 2$. Both have index $+1/2$.

### The triaxial ellipsoid

The ellipsoid $x^2/9 + y^2/4 + z^2 = 1$ has four umbilics, in the plane of its longest and shortest axes, at $(\pm 3\sqrt{5/8},\ 0,\ \pm\sqrt{3/8}) \approx (\pm 2.37171, 0, \pm 0.61237)$. There $|k| = 3/8$, and with the outward normal $k = -3/8$. Each is a lemon, with index $+1/2$, and the four indices sum to $2$, the Euler characteristic of the sphere, as the index theorem for line fields requires.

### Non-examples

- **A sphere or a plane.** Every point is an umbilic, so no point is an isolated umbilic and the index is not defined. A connected surface on which every point is an umbilic lies in a plane or in a sphere (do Carmo, Section 3-2).
- **A point with $H = 0$.** At the origin of $z = xy$, $k_1 = 1$ and $k_2 = -1$, so $H = 0$ but $H^2 - K = 1$. Every point with $K < 0$ has $H^2 - K > 0$, so a saddle point is never an umbilic.
- **A cylinder.** $k_1 = 0$ and $k_2 = \mp 1/A$ at every point, so no point is an umbilic, and the lines of curvature are the rulings and the circles.

## Related definitions

- **Lines of curvature.** The integral curves of the principal directions; see [lines of curvature](/lines-of-curvature/). The umbilics are their singular points.
- **Principal curvatures.** The eigenvalues of the shape operator; see [surface curvature](/surface-curvature/).
- **Planar point.** An umbilic with $k = 0$, where $\mathrm{II} = 0$.
- **Generic umbilic.** An umbilic with $\Delta \ne 0$ and a cubic $C$ with simple roots. These conditions are open, so a change of the surface that is small in $C^3$ moves a generic umbilic but keeps its kind.

## References
