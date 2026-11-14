---
tag: TCCNNQ
kind: problem
slug: geodesics-on-parametric-surfaces
name: Geodesics on parametric surfaces
aliases:
- parametric geodesic computation
area: cad/surface-interrogation-and-design
level: advanced
summary: Find shortest curves between points on a parametric surface by solving the geodesic equations as an initial or boundary value problem, for design and fibre layup.
prereqs: [fundamental-forms, parametric-surface, runge-kutta-methods]
see_also: [shooting-method, bvp-boundary-value-problem, classical-runge-kutta-4, discrete-geodesic-problem, mmp-geodesic-algorithm, fast-marching-method, developable-surface, lines-of-curvature]
sources:
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 10, Geodesics (Section 10.2.1, geodesic equations on parametric surfaces; Section 10.3.2, the shooting method; Section 10.3.3, the relaxation method; Section 10.4, initial approximations; Section 10.8, geodesics on developable surfaces)
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 4-3 (Christoffel symbols); Section 4-4 (geodesics and their differential equations); Section 4-6 (geodesics minimize arc length locally); Section 5-3 (complete surfaces, the theorem of Hopf and Rinow); Section 5-5 (Jacobi fields and conjugate points)
---

Computing geodesics on a parametric surface means finding curves $r(u(t), v(t))$ whose acceleration is normal to the surface, either from a start point and a start direction (an initial value problem) or between two given points (a boundary value problem). Shortest paths on a smooth surface are geodesics, so the boundary value problem is how a CAD system measures distances on a surface and lays out paths of least length. The geodesic equations are a system of two second order ordinary differential equations whose coefficients are the Christoffel symbols of the first [fundamental form](/fundamental-forms/).

## In plain words

On a flat sheet the shortest way between two points is a straight line. On a curved surface the shortest way bends, but only as much as the surface forces it to: an ant that walks straight ahead, never turning left or right, follows such a curve. These curves are the geodesics. There are two tasks. In the first, the ant knows where it starts and in which direction it walks, and we trace its path step by step. In the second, we know the start and the end, and we must find the right start direction, usually by guessing it, tracing the path, seeing where it ends, and correcting the guess. The second task can have many answers: on a cylinder a path can wind around any number of times before it reaches the end point.

## Definition

**Input.** A regular parametric surface $r : D \to \mathbb{R}^3$ of class $C^3$ on a domain $D \subset \mathbb{R}^2$, with first form coefficients $E, F, G$. This page uses the unit normal $n = r_u \times r_v / |r_u \times r_v|$, and $H = (k_1 + k_2)/2$ for this $n$; neither choice affects geodesics.

**Geodesic.** A curve $\alpha(t) = r(u(t), v(t))$ is a geodesic if the tangential part of $\alpha''(t)$ is zero for every $t$, that is, $\alpha'' \cdot r_u = 0$ and $\alpha'' \cdot r_v = 0$. A geodesic has constant speed, because $\frac{d}{dt}|\alpha'|^2 = 2\, \alpha'' \cdot \alpha' = 0$ as $\alpha'$ is tangent.

**The equations.** Differentiate the definitions $E = r_u \cdot r_u$, $F = r_u \cdot r_v$, $G = r_v \cdot r_v$:

- $r_{uu} \cdot r_u = E_u/2$, $r_{uv} \cdot r_u = E_v/2$, $r_{uv} \cdot r_v = G_u/2$, $r_{vv} \cdot r_v = G_v/2$;
- $F_u = r_{uu} \cdot r_v + r_u \cdot r_{uv}$, so $r_{uu} \cdot r_v = F_u - E_v/2$;
- $F_v = r_{uv} \cdot r_v + r_u \cdot r_{vv}$, so $r_{vv} \cdot r_u = F_v - G_u/2$.

Now $\alpha'' = r_u u'' + r_v v'' + r_{uu} u'^2 + 2 r_{uv} u' v' + r_{vv} v'^2$. Take the dot product with $r_u$ and with $r_v$ and set both to zero:

$$\begin{pmatrix} E & F \\ F & G \end{pmatrix} \begin{pmatrix} u'' \\ v'' \end{pmatrix} = - \begin{pmatrix} \tfrac12 E_u\, u'^2 + E_v\, u' v' + (F_v - \tfrac12 G_u)\, v'^2 \\ (F_u - \tfrac12 E_v)\, u'^2 + G_u\, u' v' + \tfrac12 G_v\, v'^2 \end{pmatrix}.$$

The matrix is the first form, which is invertible, so this is equivalent to

$$u'' + \Gamma^1_{11} u'^2 + 2 \Gamma^1_{12} u' v' + \Gamma^1_{22} v'^2 = 0, \qquad v'' + \Gamma^2_{11} u'^2 + 2 \Gamma^2_{12} u' v' + \Gamma^2_{22} v'^2 = 0,$$

where the Christoffel symbols are

$$\begin{pmatrix} \Gamma^1_{11} \\ \Gamma^2_{11} \end{pmatrix} = \mathrm{I}^{-1} \begin{pmatrix} \tfrac12 E_u \\ F_u - \tfrac12 E_v \end{pmatrix}, \quad \begin{pmatrix} \Gamma^1_{12} \\ \Gamma^2_{12} \end{pmatrix} = \mathrm{I}^{-1} \begin{pmatrix} \tfrac12 E_v \\ \tfrac12 G_u \end{pmatrix}, \quad \begin{pmatrix} \Gamma^1_{22} \\ \Gamma^2_{22} \end{pmatrix} = \mathrm{I}^{-1} \begin{pmatrix} F_v - \tfrac12 G_u \\ \tfrac12 G_v \end{pmatrix}.$$

They depend only on $E, F, G$ and their first derivatives, so geodesics are intrinsic: a bending of the surface that keeps lengths keeps its geodesics. As a first order system in $y = (u, v, u', v')$, the right side is $C^1$ for a $C^3$ surface, so through every point and every tangent vector passes exactly one geodesic.

**The problems.**

- *Initial value problem.* Given $(u_0, v_0) \in D$ and a tangent vector $(p, q)$, find the geodesic with $(u, v)(0) = (u_0, v_0)$ and $(u', v')(0) = (p, q)$, up to a given length or until it leaves $D$.
- *Boundary value problem.* Given two points $A = r(u_A, v_A)$ and $B = r(u_B, v_B)$, find a geodesic $(u, v) : [0, 1] \to D$ with $(u, v)(0) = (u_A, v_A)$ and $(u, v)(1) = (u_B, v_B)$, and usually the shortest one.

## Variants

- **Shortest path versus geodesic.** A shortest curve between two interior points that stays in the interior of $D$ is a geodesic, and a geodesic is shortest between any two of its points that are close enough (do Carmo, Section 4-6). A long geodesic need not be shortest, and a boundary value problem can have several geodesic solutions, so the shortest one is a global optimum among them.
- **Bounded patches.** On a trimmed patch or a patch with a hole, the shortest path between two points can run along the boundary for a while. That part is not a geodesic, and the equations above do not describe it.
- **Geodesic distance field.** Find the distance from one point to all points of the surface. On meshes this is the [discrete geodesic problem](/discrete-geodesic-problem/), solved exactly by the [MMP algorithm](/mmp-geodesic-algorithm/) or approximately by the [fast marching method](/fast-marching-method/) for the [eikonal equation](/eikonal-equation/).
- **Geodesic offsets.** Curves at constant geodesic distance from a given curve on the surface, traced along geodesics that start orthogonal to it.
- **Developable surfaces.** A [developable surface](/developable-surface/) is isometric to a planar region, so its geodesics are the images of straight lines of the development (Patrikalakis and Maekawa, Section 10.8).

## Examples

### The cylinder: infinitely many geodesics between two points

Take $r(u, v) = (\cos u, \sin u, v)$ on all of $\mathbb{R}^2$. Then $E = G = 1$ and $F = 0$ are constant, all Christoffel symbols vanish, and the equations are $u'' = v'' = 0$. So the geodesics are exactly the curves $u = u_0 + pt$, $v = v_0 + qt$: helices, circles ($q = 0$) and rulings ($p = 0$).

- **From $A = (1, 0, 0)$ to $B = (1, 0, h)$, $h > 0$.** $A$ is $r(0, 0)$, and $B$ is $r(2\pi k, h)$ for every integer $k$. For each $k$, the curve $(u, v) = (2\pi k t, h t)$, $t \in [0, 1]$, is a geodesic from $A$ to $B$, and every geodesic from $A$ to $B$ on $[0, 1]$ has this form. So there are infinitely many, with lengths $\sqrt{h^2 + 4\pi^2 k^2}$. The shortest is the ruling, $k = 0$, of length $h$.
- **From $A = (1, 0, 0)$ to $B = (-1, 0, h)$.** Now $B = r(\pi + 2\pi k, h)$, and the geodesics have lengths $\sqrt{h^2 + \pi^2 (2k + 1)^2}$. The two helices $k = 0$ and $k = -1$ both have the least length $\sqrt{h^2 + \pi^2}$; they wind around the cylinder in opposite senses. Both are shortest paths: the map $r$ preserves length, any curve from $A$ to $B$ is the image of a plane curve from $(0, 0)$ to some $(\pi + 2\pi k, h)$, and that plane curve is at least as long as the segment, $\sqrt{h^2 + \pi^2 (2k+1)^2} \ge \sqrt{h^2 + \pi^2}$.

So a shortest path need not be unique, and a solver that returns one geodesic must say which one it returns.

### The sphere

The geodesics of a sphere are its great circles. Two points that are not antipodal lie on exactly one great circle, which gives two geodesic arcs, a short one and a long one, and more geodesics that wind around it several times. Two antipodal points lie on infinitely many great circles, and every half great circle between them is a shortest path of length $\pi R$.

### A paraboloid of revolution, by shooting

Take $r(u, v) = (u \cos v, u \sin v, u^2/2)$ for $u > 0$, so $E = 1 + u^2$, $F = 0$, $G = u^2$. The only nonzero Christoffel symbols are $\Gamma^1_{11} = u/(1 + u^2)$, $\Gamma^1_{22} = -u/(1 + u^2)$ and $\Gamma^2_{12} = 1/u$, and the equations are

$$u'' = \frac{u (v'^2 - u'^2)}{1 + u^2}, \qquad v'' = -\frac{2 u' v'}{u}.$$

The second one says $(G v')' = 2 u u' v' + u^2 v'' = 0$, so $u^2 v'$ is constant along every geodesic. This is Clairaut's relation for this surface.

Join $A = r(1, 0) = (1, 0, 0.5)$ to $B = r(1, \pi/2) = (0, 1, 0.5)$. Shooting on the unknown start vector $(p, q)$, with [classical Runge-Kutta 4](/classical-runge-kutta-4/) at 2000 steps on $[0, 1]$ and Newton's method with a finite difference Jacobian, starting from $(p, q) = (-0.3, \pi/2)$, reaches an end point error below $10^{-12}$ after 4 Newton steps. The result is $(p, q) = (-0.582864, 1.236313)$, and the length is $\sqrt{E p^2 + G q^2} = 1.485911$. The geodesic dips toward the axis to $u_{\min} = 0.832024$. Clairaut's relation predicts this value: at the lowest point $u' = 0$, so the speed is $u_{\min} |v'| = q / u_{\min}$, and $u_{\min} = q / 1.485911 = 0.832024$. For comparison, the arc of the circle $u = 1$ from $A$ to $B$ has length $\pi/2 \approx 1.570796$, and the straight chord in space has length $\sqrt 2 \approx 1.414214$, a lower bound for every curve.

## Known algorithms

- **Initial value problem.** Write the equations as a first order system in $(u, v, u', v')$ and integrate with a [Runge-Kutta method](/runge-kutta-methods/), with step size control. The speed $\sqrt{E u'^2 + 2F u'v' + G v'^2}$ is a conserved quantity, so its drift measures the integration error, and a program can rescale $(u', v')$ to fix it. The integration must stop when $(u, v)$ leaves $D$, or move to the neighbouring patch.
- **Shooting.** The [shooting method](/shooting-method/) treats the start vector $(p, q)$ as unknown, integrates the initial value problem on $[0, 1]$, and applies Newton's method to the two equations $(u(1), v(1)) = (u_B, v_B)$ (Patrikalakis and Maekawa, Section 10.3.2). The Jacobian is the derivative of the end point with respect to the start vector. It is singular exactly when $B$ is conjugate to $A$ along the geodesic (do Carmo, Section 5-5), for example at the antipode on a sphere, and there Newton's method fails.
- **Relaxation.** Discretize $[0, 1]$ into $m$ steps, replace the derivatives by finite differences, and solve the resulting nonlinear system in the $2(m - 1)$ interior unknowns with Newton's method, whose Jacobian is block tridiagonal (Patrikalakis and Maekawa, Section 10.3.3). This is a [boundary value problem](/bvp-boundary-value-problem/) solver, and it is more robust than shooting when the geodesic is long.
- **Initial guesses.** Both methods need a start near a solution. Good starts are a straight segment in the parameter domain, or a shortest path on a mesh of the surface computed by an algorithm for the [discrete geodesic problem](/discrete-geodesic-problem/) (Patrikalakis and Maekawa, Section 10.4). The start decides which of several geodesics the method finds.

## Bounds

- **Existence.** On a complete connected surface, every two points are joined by a shortest geodesic (Hopf and Rinow; do Carmo, Section 5-3). A patch on a bounded domain is not complete, and a shortest path may touch the boundary instead.
- **Number of solutions.** There is no bound in general: the cylinder example above has infinitely many geodesics between two points.
- **Accuracy.** For a smooth surface, classical Runge-Kutta 4 with $n$ equal steps has global error $O(n^{-4})$ in the initial value problem. Newton's method in shooting or relaxation converges quadratically near a solution whose Jacobian is nonsingular, that is, when $B$ is not conjugate to $A$.
- **Exact algorithms.** For a smooth parametric surface, geodesics are in general transcendental curves, and no finite exact algorithm computes them. Exact combinatorial algorithms exist only for polyhedral surfaces, on the [discrete geodesic problem](/discrete-geodesic-problem/) page.

## Reductions

- **Boundary value problem to root finding.** Shooting reduces the boundary value problem to two nonlinear equations in two unknowns, solved by [Newton's method for systems](/newton-method-for-systems/).
- **Developable surface to the plane.** On a developable patch whose development is one to one, unroll the patch to the plane, join the two images by a segment, and map the segment back. When the developed region is not convex, the shortest path in it can be a polygonal path that bends at boundary points, not a segment.
- **Smooth surface to mesh.** Tessellate the surface and solve the discrete problem. On a fine mesh that is close to the surface in position and in normals, the result is close to the smooth geodesic distance, and it serves as an initial guess for the smooth solvers.

## Applications

- **Fibre placement and composite layup.** A geodesic has zero geodesic curvature, so a fibre tow laid along it needs no bending in the plane of the tow. Fibre placement and filament winding use geodesic paths on the mould surface for this reason.
- **Distances on surfaces.** Geodesic distance gives the length of a seam, a weld or a cable that must lie on a surface, and geodesic offsets give curves at constant distance on the surface.
- **Ship hulls and sheet metal.** Bending a flat plate without stretching is an isometry, so a straight edge of the flat plate becomes a geodesic of the bent plate.
- **Interrogation.** Geodesics, with [lines of curvature](/lines-of-curvature/), are a family of curves that CAD systems compute on a surface to show its intrinsic shape.

## References
