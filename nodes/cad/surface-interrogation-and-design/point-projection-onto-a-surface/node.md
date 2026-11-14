---
tag: AAS8GF
kind: problem
slug: point-projection-onto-a-surface
name: Point projection onto a parametric surface
aliases:
- point inversion
- foot point problem
- closest point on a surface
area: cad/surface-interrogation-and-design
level: core
summary: Given a point and a parametric curve or surface, find the parameters of the nearest point on it, or of the point itself when it lies on the surface.
prereqs: [parametric-surface, fundamental-forms]
see_also: [newton-point-inversion, minimum-distance-between-surfaces, curve-surface-intersection, surface-curvature, medial-axis, iterative-closest-point, parameter-correction, kkt-conditions]
sources:
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 6, Section 6.1, Point inversion and projection for curves and surfaces, pages 229 to 234 (the two first order equations, the start point from a coarse sample and the stopping tests)
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 5, Section 5.5, Point/surface intersection (implicitization, Newton's method, bounding boxes with subdivision and the distance function method), and Chapter 7, Sections 7.2 and 7.3, on distance functions and their stationary points
  - paper: doi:10.1016/S0167-8396(03)00021-9
    title: Ying Liang Ma and W. T. Hewitt, Point inversion and projection for NURBS curve and surface, control polygon approach, Computer Aided Geometric Design 20(2), 79 to 99, 2003
    locator: the whole paper (the subdivision of the control net, the exclusion of pieces that cannot hold the nearest point, and the Newton step on the remaining piece)
---

Point projection asks for the point of a parametric surface $r(u, v)$ that is nearest to a given point $p$, and for its parameters $(u, v)$. When $p$ lies on the surface the problem is called *point inversion*: find the parameters of a known point of the surface. The same problem for a curve $c(u)$ is the one dimensional case. Every CAD system solves it many times a second, to pick a point on a face, to measure how far a scanned point is from the model, and to map points of space into the parameter domain of a patch, and the hard part is to find the nearest point and not only a nearby one.

## In plain words

You have a curved sheet in space, drawn by a formula that turns two numbers into a point. You also have a point in space. You want the spot on the sheet that is closest to your point, and you want the two numbers that give that spot.

At the closest spot, the straight line from your point to the sheet meets the sheet at a right angle. This gives two equations. But they also hold at spots that are not the closest: at the farthest spot, at saddle spots, and at spots that are closest only in a small region.

So the problem has two parts. The easy part is to make a guess precise. The hard part is to be sure that no other spot is closer. If the point is on the sheet, you only want its two numbers.

## Definition

**Input.** A regular parametric surface $r : \Omega \to \mathbb{R}^3$ of class $C^2$ on a closed parameter box $\Omega = [u_0, u_1] \times [v_0, v_1]$, usually a [Bézier patch](/bezier-patch/), a [B-spline](/b-spline/) or a [NURBS](/nurbs/) surface. A point $p \in \mathbb{R}^3$. A tolerance $\varepsilon > 0$.

**Output.** Parameters $(u^*, v^*) \in \Omega$ that minimize the squared distance

$$D(u, v) = |r(u, v) - p|^2,$$

and the foot point $r(u^*, v^*)$ and the distance $|r(u^*, v^*) - p|$. In the numerical version the output distance is within $\varepsilon$ of the true minimum. When more than one point attains the minimum, the problem asks for one of them, or for all of them in the variant below.

**Regular.** The patch is regular where $r_u \times r_v \ne 0$. There the unit normal is $N = (r_u \times r_v) / |r_u \times r_v|$. This page uses the fundamental forms with $E = r_u \cdot r_u$, $F = r_u \cdot r_v$, $G = r_v \cdot r_v$, $L = r_{uu} \cdot N$, $M = r_{uv} \cdot N$, $N_2 = r_{vv} \cdot N$, written as the matrices $\mathrm{I} = \begin{pmatrix} E & F \\ F & G \end{pmatrix}$ and $\mathrm{II} = \begin{pmatrix} L & M \\ M & N_2 \end{pmatrix}$. With this sign of $N$, a principal curvature $k$, a root of $\det(\mathrm{II} - k \, \mathrm{I}) = 0$, is positive when the surface bends towards $N$. See [fundamental forms](/fundamental-forms/) and [surface curvature](/surface-curvature/).

**First order conditions.** At an interior minimum $(u^*, v^*)$ the gradient of $D$ vanishes:

$$f(u, v) = (r - p) \cdot r_u = 0, \qquad g(u, v) = (r - p) \cdot r_v = 0.$$

*Proof.* $D$ is differentiable and $D_u = 2 (r - p) \cdot r_u$, $D_v = 2 (r - p) \cdot r_v$ by the product rule. At an interior minimum of a differentiable function both partial derivatives vanish, because $D(u^* + h, v^*) \ge D(u^*, v^*)$ for all small $h$ of both signs. $\square$

At a regular point the two conditions say that $r - p$ is perpendicular to the tangent plane, so $p = r + t N$ for one real $t$, the signed distance: the point lies on the normal line of its foot point. On the boundary of $\Omega$ the conditions change. On the edge $u = u_0$ a minimum needs $g = 0$ and $f \ge 0$, since $D$ must not decrease as $u$ moves into the box. At the corner $(u_0, v_0)$ it needs $f \ge 0$ and $g \ge 0$. These are the [KKT conditions](/kkt-conditions/) of the box constraint.

**Second order test.** Let $(u, v)$ be an interior point at which $r$ is regular and $f = g = 0$, with $p = r + t N$. Then the Hessian of $D$ is

$$\nabla^2 D = 2 \, (\mathrm{I} - t \, \mathrm{II}).$$

*Proof.* Differentiate $D_u = 2 (r - p) \cdot r_u$ once more: $D_{uu} = 2 (r_u \cdot r_u + (r - p) \cdot r_{uu})$, and in the same way $D_{uv} = 2 (r_u \cdot r_v + (r - p) \cdot r_{uv})$ and $D_{vv} = 2 (r_v \cdot r_v + (r - p) \cdot r_{vv})$. Put $r - p = -t N$: then $(r - p) \cdot r_{uu} = -t L$, and the same for the other two. $\square$

Since $\mathrm{I}$ is positive definite, $\mathrm{I} - t \, \mathrm{II} = \mathrm{I}^{1/2} (\mathrm{Id} - t \, \mathrm{I}^{-1/2} \mathrm{II} \, \mathrm{I}^{-1/2}) \mathrm{I}^{1/2}$ has the same inertia as $\mathrm{Id} - t S$, where the symmetric matrix $S = \mathrm{I}^{-1/2} \mathrm{II} \, \mathrm{I}^{-1/2}$ has the principal curvatures $k_1, k_2$ as its eigenvalues. So the signs of the eigenvalues of the Hessian are the signs of $1 - t k_1$ and $1 - t k_2$. The stationary point is a strict local minimum when both are positive, it is not a minimum when one is negative, and the Hessian is singular exactly when $t = 1 / k_i$, that is, when $p$ is a center of principal curvature of the foot point. These centers form the focal surface of $r$. The Jacobian of the system $(f, g)$ is $\frac{1}{2} \nabla^2 D$, so Newton's method on $(f, g)$ has a regular solution exactly when $p$ is not on the focal surface.

## Variants

- **Point inversion.** The point $p$ is known to lie on the surface, up to rounding. The minimum distance is $0$ and the task is to find the parameters. Piegl and Tiller treat inversion and projection with one method.
- **Curves.** For a curve $c(u)$ the one condition is $(c(u) - p) \cdot c'(u) = 0$. If $c$ is a polynomial curve of degree $d$, the left side is a polynomial of degree at most $2d - 1$, so there are at most $2d - 1$ stationary parameters unless it vanishes identically. For a rational curve $c = P / w$ of degree $d$, the numerator of the condition is $(P - p \, w) \cdot (P' w - P w')$, of degree at most $d + 2d - 2 = 3d - 2$, because the terms of degree $2d - 1$ in $P' w - P w'$ cancel.
- **All foot points.** Return every global minimizer, or every stationary point. This is needed when $p$ is on the [medial axis](/medial-axis/) of a closed surface, where two or more foot points tie, and for the distance function of Patrikalakis and Maekawa, Chapter 7.
- **Local projection.** Return the stationary point nearest to a given start parameter. This is what a Newton method computes, and it is what a tracking task needs: a point that moves a little should get parameters that move a little.
- **Directional projection.** Project along a given direction $d$ instead of along the normal. This is the intersection of the line $p + s d$ with the surface, a case of [curve surface intersection](/curve-surface-intersection/).
- **Trimmed surfaces.** The minimum is over the trimmed region of a [trimmed surface](/trimmed-surface/), so the boundary of the domain is the trimming loop, not a box.

## Examples

- **Sphere.** For the sphere of radius $2$ about the origin and $p = (3, 4, 0)$, the foot point is $\frac{2}{5} p = (1.2, 1.6, 0)$ and the distance is $5 - 2 = 3$. For $p = 0$ every point of the sphere is a foot point, at distance $2$: the center of the sphere is its focal point, with $t = 2 = 1 / k$ for $k = 1/2$.
- **Paraboloid, one foot point.** Let $r(u, v) = (u, v, u^2 + v^2)$ and $p = (0, 0, h)$. Then $D = s + (s - h)^2$ with $s = u^2 + v^2$, and $dD/ds = 1 + 2 (s - h)$. For $h \le 1/2$ this is positive for all $s \ge 0$, so the only minimum is the origin, at distance $|h|$.
- **Paraboloid, a circle of foot points.** For $h > 1/2$ the minimum is at $s = h - 1/2$, a whole circle of foot points, at distance $\sqrt{h - 1/4}$. For $h = 1$ the circle has radius $\sqrt{1/2} \approx 0.7071$ and the distance is $\sqrt{3/4} \approx 0.8660$. The origin is still a stationary point, but now a local maximum of $D$ along every line through it. The second order test agrees: at the origin $\mathrm{I}$ is the identity, $\mathrm{II} = 2 \, \mathrm{I}$ with $N = (0, 0, 1)$, and $t = h$, so $1 - t k = 1 - 2h$, which changes sign at the focal point $h = 1/2$.
- **Saddle, a quintic.** Let $r(u, v) = (u, v, uv)$, a hyperbolic paraboloid, and $p = (1, 0.5, 2)$. The conditions are $u + u v^2 - 1 - 2v = 0$ and $v + u^2 v - 0.5 - 2u = 0$. The first gives $u = (1 + 2v) / (1 + v^2)$, and the second then becomes $2v^5 - v^4 + 4v^3 + 2v^2 - 4v - 5 = 0$ after the denominators are cleared. It has one real root, $v \approx 1.095811$, with $u \approx 1.450209$ and distance $\approx 0.852334$. The other four roots are complex, so this is the only stationary point on the whole plane. Since $D \ge (u - 1)^2 + (v - 0.5)^2$ grows without bound, $D$ has a minimum on the plane, so this point is the global minimum.
- **The nearest point is on an edge.** Let $r(u, v) = (u, v, 0)$ on $[0, 1]^2$ and $p = (2, 0.5, 1)$. The minimum is at $(1, 0.5)$, on the edge $u = 1$, at distance $\sqrt 2$. There $g = 0$ but $f = (r - p) \cdot r_u = -1$, so the interior conditions fail, and the edge condition, $f \le 0$ on the edge $u = u_1$, holds.
- **Singular parametrization.** For the sphere $r(u, v) = (2 \cos u \cos v, 2 \sin u \cos v, 2 \sin v)$ and $p = (0, 0, 5)$, the foot point is the pole $(0, 0, 2)$ at $v = \pi/2$, where $r_u = 0$. Both conditions hold for every $u$, the Jacobian is singular, and the answer for $u$ is arbitrary.

## Known algorithms

- **[Newton point inversion](/newton-point-inversion/).** Sample the patch on a coarse grid, take the best sample as the start, and solve $f = g = 0$ with Newton's method, with the steps clamped to the box. This is the method of Piegl and Tiller. It is fast, and it converges quadratically near a solution off the focal surface, but the global answer depends on the density of the start grid.
- **Subdivision with exclusion.** Split the control net with the [de Casteljau algorithm](/de-casteljau-algorithm/) or knot insertion. A piece whose control points are all farther from $p$ than the best distance found so far cannot hold the nearest point, by the [convex hull property](/convex-hull-property/), and is discarded. Newton then runs on the pieces that remain. Ma and Hewitt (2003) give such a method for NURBS curves and surfaces. Pieces that are excluded by a proved bound make the answer global up to the tolerance.
- **Algebraic.** Eliminate one parameter from $f = g = 0$ with a [resultant](/resultant/), as in the quintic example, and isolate the real roots of the result with [real root isolation](/real-root-isolation/). This finds all stationary points, at a cost that grows quickly with the degree. Patrikalakis and Maekawa, Section 5.5, list it with implicitization for point inversion.
- **Certified solvers.** The [interval projected polyhedron](/interval-projected-polyhedron/) method and the [interval Newton method](/interval-newton-method/) find all roots of $f = g = 0$ in the box with proofs, and the minimum is then chosen from a finite list.

## Bounds

**Existence.** $D$ is continuous on the compact box $\Omega$, so a minimum exists. It need not be unique, as the sphere and the paraboloid show.

**The number of stationary points.** For a curve the count is at most $2d - 1$ or $3d - 2$, proved above. For a polynomial tensor product patch of bidegree $(m, n)$, the polynomial $f$ has bidegree $(2m - 1, 2n)$ and $g$ has bidegree $(2m, 2n - 1)$. Bézout's theorem on $\mathbb{P}^1 \times \mathbb{P}^1$, which this page does not prove, then bounds the number of isolated complex solutions by $(2m - 1)(2n - 1) + 2m \cdot 2n = 8mn - 2m - 2n + 1$. This is $5$ for a bilinear patch, the degree of the quintic in the saddle example, and $61$ for a bicubic patch. A local method can converge to any of them.

**Stability.** Off the focal surface and away from ties, the foot point depends smoothly on $p$: the Jacobian of $(f, g)$ is nonsingular there, by the second order test, and the implicit function theorem applies. At a tie the foot point jumps, as for the paraboloid on its axis above the focal point. A small move of $p$ off the axis selects one point of the circle. So no method can return a foot point that is continuous in $p$ for all $p$.

The first order conditions, the second order test, the curve bounds, existence and stability are proved on this page. The bound for patches is cited. The speed of the methods on real models is measured, not proved.

## Reductions

- **To a square system.** Interior stationary points are the solutions of the two equations $f = g = 0$ in two unknowns, a case of [systems of nonlinear equations](/systems-of-nonlinear-equations/). Edges add one equation in one unknown each, and corners are evaluated directly.
- **To a plane curve.** If the surface has an implicit equation, which [implicitization](/implicitization/) gives for rational patches, point inversion reduces to evaluating that equation and solving for the parameters along it.
- **From the problem to minimum distance.** A point is a surface of dimension zero, so point projection is the case of [minimum distance between surfaces](/minimum-distance-between-surfaces/) in which one surface is a single point.
- **To curves.** Fixing $v$ turns the problem into projection onto the curve $u \mapsto r(u, v)$. Alternating between the two curve problems never increases $D$, a coordinate descent that is slower than Newton.

## Applications

- **Picking and snapping.** A user clicks near a face, and the system projects the 3D point onto the face to get its parameters.
- **Inspection.** The deviation of a measured point from the CAD model is its distance to the nearest face, the core of [CAD based inspection](/cad-based-inspection/).
- **Registration.** Each step of [iterative closest point](/iterative-closest-point/) projects every scanned point onto the model.
- **Surface fitting.** [Parameter correction](/parameter-correction/) projects each data point onto the current fit to update its parameter.
- **Trimming and Booleans.** Points of an intersection curve, found in space, are projected into the parameter domain of each face to form the trimming curves of a [trimmed surface](/trimmed-surface/).
- **Distance and offsets.** The [Hausdorff distance](/hausdorff-distance/) between a surface and a point set, and the test whether a point lies within a distance of an [offset surface](/offset-surface/), both need the nearest point.

## References
