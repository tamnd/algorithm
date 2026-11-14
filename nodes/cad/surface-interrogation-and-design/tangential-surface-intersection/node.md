---
tag: 087SH2
kind: concept
slug: tangential-surface-intersection
name: Tangential surface intersection
aliases:
- tangent surface intersection
- singular intersection curve
area: cad/surface-interrogation-and-design
level: advanced
summary: The case where two surfaces meet with parallel normals, at a point or along a curve, so marching fails and the shape of the intersection depends on second and higher derivatives.
prereqs: [surface-surface-intersection, fundamental-forms]
see_also: [marching-surface-intersection, subdivision-surface-intersection, sederberg-meyers-loop-detection, surface-curvature, rolling-ball-blend, condition-number, newton-method-for-systems, minimum-distance-between-surfaces]
sources:
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Section 6.3 (the transversal case, with the tangent along the cross product of the normals) and Section 6.4, Intersection curve at tangential intersection points (6.4.1 Tangential direction, 6.4.2 Curvature and curvature vector, 6.4.3 Third and higher order derivative vector)
  - paper: doi:10.1016/S0167-8396(99)00018-7
    title: Xiuzi Ye and Takashi Maekawa, Differential geometry of intersection curves of two surfaces, Computer Aided Geometric Design 16(8), 767 to 788, 1999
    locator: the whole paper (tangent, curvature, torsion and higher derivatives of the intersection curve at transversal and tangential points; general locator)
  - paper: doi:10.1016/0010-4485(89)90126-7
    title: R. P. Markot and R. L. Magedson, Solutions of tangential surface and curve intersections, Computer-Aided Design 21(7), 421 to 427, 1989
    locator: the whole paper (general locator)
---

A tangential intersection is a common point of two surfaces where their normals are parallel, so that the surfaces share a tangent plane there. The usual tools of [surface surface intersection](/surface-surface-intersection/) fail at such a point: the tangent $N_1 \times N_2$ of the curve is zero, and the Newton corrector of [marching](/marching-surface-intersection/) has a singular matrix. Near the point the surfaces can meet in only that point, in two branches that cross, or along a whole curve where they touch. The second fundamental forms of the two surfaces decide between these cases, and higher derivatives decide when the forms do not.

## In plain words

Two surfaces usually cut each other at an angle. The cut is a clean curve, and a program can follow it step by step.

Sometimes the surfaces only touch. A ball resting on a table touches it at one point. A pipe lying on the table touches it along a line. A saddle laid on a flat sheet can touch it along two lines that cross. At such places the two surfaces have the same tilt, so the program cannot tell which way the curve goes.

To decide what happens, look at how each surface bends near the place where they touch. If one bends away from the other in every direction, they meet at one point only. If they bend the same amount in one direction, they can touch along a curve. A very small shift of one surface can change the answer completely.

## The idea

**The transversal case.** Let $N_1$ and $N_2$ be the unit normals, with $\cos \theta = N_1 \cdot N_2$ and $\sin \theta > 0$. The intersection curve is tangent to both surfaces, so its unit tangent is $t = N_1 \times N_2 / \sin \theta$. Let $k$ be its curvature vector. Differentiating $t \cdot N_i = 0$ along the curve gives $k \cdot N_i = \kappa_i$, the normal curvature of $S_i$ in the direction $t$, that is $\mathrm{II}_i(t, t)$ for the [second fundamental form](/fundamental-forms/) of $S_i$ with respect to $N_i$. As $k \perp t$, $k = \alpha N_1 + \beta N_2$, and the two conditions give

$$k = \frac{(\kappa_1 - \kappa_2 \cos \theta) N_1 + (\kappa_2 - \kappa_1 \cos \theta) N_2}{\sin^2 \theta}.$$

Both $t$ and $k$ have $\sin \theta$ in the denominator. As the curve comes near a point where the normals are parallel, these formulas lose all accuracy, and at the point they are not defined.

**The local model.** Let $p$ be a common point with $N_1(p) = \pm N_2(p)$. Move $p$ to the origin and turn the frame so that the common normal is $e_3$. Near $p$ each surface is a graph $z = f_i(x, y)$ with $f_i(0) = 0$ and $\nabla f_i(0) = 0$, and the Hessian of $f_i$ at $0$ is the matrix of $\mathrm{II}_i$ with respect to $e_3$. The common points near $p$ are the zeros of

$$d(x, y) = f_1(x, y) - f_2(x, y), \qquad d(0) = 0, \quad \nabla d(0) = 0, \quad H = \nabla^2 d(0) = \mathrm{II}_1 - \mathrm{II}_2.$$

The normals of the graphs are parallel exactly where $\nabla f_1 = \nabla f_2$, that is where $\nabla d = 0$. A direction $v$ in the tangent plane with $H(v, v) = 0$ is a direction in which the two normal curvatures agree; in the words of Patrikalakis and Maekawa, the Dupin indicatrices of the two surfaces meet there.

**The cases.** The determinant of $H$ sorts the point.

- *$\det H > 0$, isolated point.* $H$ is definite, say $H(v, v) \ge \lambda |v|^2$ with $\lambda > 0$. Taylor's theorem gives $d(v) \ge \lambda |v|^2 / 2 - C |v|^3 > 0$ for $0 < |v| < \lambda / (2C)$, so near $p$ the surfaces meet only at $p$.
- *$\det H < 0$, branch point.* $H(v, v) = 0$ has two distinct directions, and two intersection branches cross at $p$ in these directions. This follows from the Morse lemma, and is the branch point case of Patrikalakis and Maekawa (Section 6.4.1, cited, not proved here).
- *$\det H = 0$, $H \ne 0$, one double direction.* The second order terms do not decide. If the surfaces touch along a curve through $p$, then $\det H = 0$: along the curve $\nabla d = 0$, so its derivative $H t$ along the tangent $t$ of the curve is $0$, and $H$ is singular. The converse is false, as the examples show.
- *$H = 0$, contact of higher order.* The normal curvatures agree in every direction, and the third or higher derivatives decide.

**A tangential curve, when $H$ has rank one.** Turn the frame so that $H = \mathrm{diag}(0, h)$ with $h \ne 0$. Then $\partial_y d (0) = 0$ and $\partial_{yy} d(0) = h \ne 0$, so by the implicit function theorem the zeros of $\partial_y d$ near $0$ form a curve $y = g(x)$. Every point near $p$ with parallel normals has $\nabla d = 0$, so it lies on this curve. Put $\delta(x) = d(x, g(x))$. The surfaces touch along a curve through $p$ exactly when $\delta = 0$ on an interval about $0$. If they touch along a curve, the curve is in the set $\nabla d = 0$, so in the graph of $g$, and $\delta$ vanishes on its projection, which is an interval. Conversely, if $\delta = 0$ on an interval, then $d = 0$ and $\partial_y d = 0$ on the graph of $g$ there, and $\partial_x d = \delta' - g' \, \partial_y d = 0$, so the normals are parallel along it. So a two dimensional degenerate problem becomes a one dimensional test on $\delta$.

**Sensitivity.** A tangential intersection is unstable. In the examples below, moving one surface by $\varepsilon$ along the normal moves the intersection by a distance of order $\sqrt{\varepsilon}$, and it changes the topology: a point becomes a small circle or nothing, and a line becomes two lines or nothing. So a method in floating point can only decide such a case within a tolerance, and an exact answer needs exact arithmetic or an explicit tolerance in the model. The ratio of the change of the output to the change of the input, $\sqrt{\varepsilon} / \varepsilon$, has no bound as $\varepsilon \to 0$, so the [condition number](/condition-number/) of the problem is infinite at the point.

**What methods do.** Patrikalakis and Maekawa compute the tangent at a tangential point from the quadratic equation for the directions where the normal curvatures agree, then the curvature vector from a linear system, and the third and higher derivatives in the same way, for parametric and implicit surfaces (Section 6.4). Ye and Maekawa give the curvature, the torsion and the higher derivatives of the intersection curve at transversal and at tangential points, and Markot and Magedson treated the solution of tangential surface and curve intersections in 1989. A [subdivision](/subdivision-surface-intersection/) method cannot stop near such a point by the [loop test](/sederberg-meyers-loop-detection/), because the normal cones of the two pieces always share the common normal line.

## Examples

- **The transversal formula on a sphere.** The unit sphere and the plane $z = 1 - \delta$ meet in a circle of radius $\rho = \sqrt{2 \delta - \delta^2}$. At a point of the circle the normals make the angle $\theta$ with $\sin \theta = \rho$, and the normal curvatures are $|\kappa_1| = 1$ for the sphere and $\kappa_2 = 0$ for the plane. The formula gives $|k| = |\kappa_1| \, |N_1 - \cos \theta \, N_2| / \sin^2 \theta = 1 / \sin \theta = 1 / \rho$, the curvature of the circle. As $\delta \to 0$, $\rho \to 0$ and the curvature has no limit.
- **Isolated point.** For $\delta = 0$ the plane touches the sphere at the north pole. Here $f_1 = 1 - \sqrt{1 - x^2 - y^2}$ in the frame at the pole, $f_2 = 0$, and $H = I$ is definite. A shift of $\varepsilon > 0$ into the sphere gives a circle of radius about $\sqrt{2 \varepsilon}$, and a shift away gives nothing.
- **Touching along a line.** The cylinder of radius $r$ with axis $y = 0$, $z = r$ lies on the plane $z = 0$ along the $x$ axis. Here $f_1 = r - \sqrt{r^2 - y^2}$, $f_2 = 0$, $H = \mathrm{diag}(0, 1/r)$, $g = 0$ and $\delta = 0$. The plane $z = \varepsilon$ with $0 < \varepsilon < 2r$ cuts the cylinder in the two lines $y = \pm \sqrt{2 r \varepsilon - \varepsilon^2}$, and the plane $z = -\varepsilon$ misses it.
- **Branch point.** The saddle $z = x y$ and the plane $z = 0$ have $d = x y$ and $H$ with $\det H = -1$. They meet in the two lines $x = 0$ and $y = 0$, which cross at the origin. The plane $z = \varepsilon$ meets the saddle in a hyperbola with two branches that do not cross.
- **The same $H$, three answers.** Take $f_2 = 0$ and $f_1 = y^2$, $y^2 + x^4$ or $y^2 - x^4$. In each case $H = \mathrm{diag}(0, 2)$, $g = 0$ and $\delta(x) = 0$, $x^4$ or $-x^4$. The first pair touches along the $x$ axis, the second meets only at the origin, and the third meets in the two curves $y = \pm x^2$, which are tangent to each other at the origin. So a double direction of the quadratic does not by itself give a tangential curve, and $\delta$ decides.

## Where it is used

- **Boolean operations.** Solids whose faces touch, such as a cylinder that rests on a plane face, give tangential intersections, and the [surface surface intersection](/surface-surface-intersection/) of a modeler must report the touching curve or point and not a pair of nearby cut curves.
- **Blends.** A [rolling ball blend](/rolling-ball-blend/) meets each base surface with the same tangent plane along its trimline, so the blend and the base surface intersect tangentially along a whole curve. The spine of the blend has no tangent where the two base surfaces have parallel normals.
- **Marching.** A [marching](/marching-surface-intersection/) method must detect when $\sin \theta$ becomes small, stop before the [Newton](/newton-method-for-systems/) corrector fails, and at a branch point continue along the directions from the quadratic.
- **Distance and contact.** A common point with parallel normals is where the distance between two surfaces has a double zero, so the same analysis applies to the contact case of the [minimum distance between surfaces](/minimum-distance-between-surfaces/), and to the curvature tests of [surface curvature](/surface-curvature/).

## References
