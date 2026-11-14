---
tag: T1RFAW
kind: problem
slug: minimum-distance-between-surfaces
name: Minimum distance between surfaces
aliases:
- surface distance computation
- curve and surface distance
area: cad/surface-interrogation-and-design
level: core
summary: Find the closest pair of points on two curves or surfaces, where both normals lie along the joining line, for clearance checks, collision and offsets.
prereqs: [point-projection-onto-a-surface, parametric-surface]
see_also: [newton-point-inversion, surface-surface-intersection, gjk-algorithm, convex-hull-property, interval-projected-polyhedron, hausdorff-distance, collision-detection, gouge-detection]
sources:
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 7, Distance functions, Section 7.2.1 (the definition of the distance between curves and surfaces), Section 7.2.2 (the geometric meaning of the stationary points, where the joining line is normal to both), Section 7.3 (the computation of all stationary points) and Section 7.4 (examples)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 6, Section 6.1, Point inversion and projection for curves and surfaces, pages 229 to 234 (the point case, which the alternating method of this page repeats)
  - paper: doi:10.1109/56.2083
    title: Elmer G. Gilbert, Daniel W. Johnson and S. Sathiya Keerthi, A fast procedure for computing the distance between complex objects in three-dimensional space, IEEE Journal of Robotics and Automation 4(2), 193 to 203, 1988
    locator: the whole paper (the distance between convex hulls of point sets, used here as a lower bound for patches)
---

The minimum distance problem asks for the pair of points, one on each of two parametric surfaces $r_1(u, v)$ and $r_2(s, t)$, that are closest to each other, and for the distance between them. The same problem for a curve and a surface, or for two curves, has fewer parameters and the same structure. At an interior closest pair at positive distance, the joining segment is normal to both surfaces, which gives four equations in four unknowns. CAD systems use the answer for clearance checks between parts, for collision and gouge tests in machining, and to decide whether two faces can meet before an intersection is computed.

## In plain words

Two curved sheets float in space without touching. You want the two spots, one on each sheet, that are closest to each other, and the gap between them.

At such a pair the straight line between the spots meets both sheets at a right angle. If it did not, you could slide one spot a little and make the gap smaller. This gives four equations, two for each sheet.

The equations also hold at pairs that are not the closest: at pairs that are farthest apart in some directions, and at pairs that are closest only nearby. Curved sheets can have many such pairs. So the problem is the same as finding the nearest spot to a point, only harder: there are twice as many unknowns, and if the sheets touch, the equations hold along a whole curve.

## Definition

**Input.** Two regular parametric surfaces $r_1 : \Omega_1 \to \mathbb{R}^3$ and $r_2 : \Omega_2 \to \mathbb{R}^3$ of class $C^2$ on closed parameter boxes, usually [Bézier patches](/bezier-patch/), [B-splines](/b-spline/) or [NURBS](/nurbs/). A tolerance $\varepsilon > 0$.

**Output.** Parameters $x^* = (u^*, v^*, s^*, t^*) \in \Omega_1 \times \Omega_2$ that minimize

$$D(u, v, s, t) = |r_1(u, v) - r_2(s, t)|^2,$$

the two points $r_1(u^*, v^*)$ and $r_2(s^*, t^*)$, and the distance $d = \sqrt{D(x^*)}$. In the numerical version $d$ is within $\varepsilon$ of the true minimum. $D$ is continuous on a compact set, so the minimum exists.

**Stationary conditions.** Write $w = r_1(u, v) - r_2(s, t)$. If $x^*$ is a minimizer inside $\Omega_1 \times \Omega_2$, then

$$w \cdot r_{1,u} = 0, \qquad w \cdot r_{1,v} = 0, \qquad w \cdot r_{2,s} = 0, \qquad w \cdot r_{2,t} = 0.$$

If moreover $d > 0$, then $w = d \, n$ for a unit vector $n$ with $n = \pm N_1 = \pm N_2$, where $N_1$ and $N_2$ are the unit normals at the two points. So the joining line is a common normal, and the normals of the two surfaces are parallel.

*Proof.* $D$ is differentiable, with $D_u = 2 w \cdot r_{1,u}$ and $D_v = 2 w \cdot r_{1,v}$, because $r_2$ does not depend on $u$ and $v$, and $D_s = -2 w \cdot r_{2,s}$ and $D_t = -2 w \cdot r_{2,t}$, because $w$ depends on $s$ through $-r_2$. At an interior minimum all four partial derivatives vanish, since a one-sided change of any single parameter must not lower $D$. This gives the four equations. If $d > 0$, then $w \ne 0$. The first two equations say that $w$ is perpendicular to $r_{1,u}$ and $r_{1,v}$, which span the tangent plane of $r_1$ because $r_1$ is regular, so $w$ is parallel to $N_1$. In the same way the last two give $w \parallel N_2$. $\square$

The converse fails: a solution of the four equations, a *common normal pair*, can be a saddle or a maximum of $D$. On the boundary of a box the equations of the fixed parameters are replaced by sign conditions, as for [point projection](/point-projection-onto-a-surface/): on the edge $u = u_0$ of $\Omega_1$, the first equation becomes $w \cdot r_{1,u} \ge 0$. When the closest pair lies on an edge or a corner, the problem becomes a curve and surface problem, or a point and surface problem.

**Contact.** If $d = 0$, the four equations hold at every point of $r_1 \cap r_2$ for the trivial reason $w = 0$. The minimizers are then the whole intersection curve, not isolated points, and the Jacobian of the system is singular there. A method must test for intersection first, or report the intersection as the answer. See [surface surface intersection](/surface-surface-intersection/).

## Variants

- **Curve and surface.** A curve $c(\tau)$ and a surface $r(u, v)$: three equations $w \cdot c' = 0$, $w \cdot r_u = 0$, $w \cdot r_v = 0$ in three unknowns, with $w = c - r$. If $d = 0$ the curve meets the surface, a case of [curve surface intersection](/curve-surface-intersection/).
- **Two curves.** Two equations $w \cdot c_1' = 0$ and $w \cdot c_2' = 0$. For two lines in space it is the common perpendicular of skew lines.
- **Point and surface.** Two equations, the [point projection](/point-projection-onto-a-surface/) problem. It is the case where one surface shrinks to a point.
- **Clearance test.** Decide only whether $d \ge \delta$ for a given clearance $\delta$. A lower bound is enough to say yes and one pair of points is enough to say no, so the test is easier than the computation of $d$.
- **All common normals.** Return every solution of the four equations, which the distance functions of Patrikalakis and Maekawa, Chapter 7, need, and from which every local minimum can be read.
- **Signed distance.** For two closed surfaces that bound solids, the depth of penetration when they overlap. This needs the inside of each solid and is not the same as $d$, which is $0$ for any overlap.
- **Hausdorff distance.** The largest distance from a point of one surface to the other surface, a max of a min instead of a min of a min. See [Hausdorff distance](/hausdorff-distance/).

## Examples

- **Two spheres.** Spheres of radii $1$ and $2$ about $(0, 0, 0)$ and $(5, 0, 0)$ have $d = 5 - 1 - 2 = 2$, at the points $(1, 0, 0)$ and $(3, 0, 0)$. Every common normal pair lies on the line of the centers, and there are four of them, at distances $2$, $4$, $6$ and $8$. Only the first is a minimum.
- **Skew lines.** The lines $(\tau, 0, 0)$ and $(0, \sigma, 1)$ give $w = (\tau, -\sigma, -1)$, and the two equations are $\tau = 0$ and $\sigma = 0$. So $d = 1$, along the $z$ axis, the common perpendicular.
- **A sphere and a bump.** Let $r_2$ be the bicubic bump of the [Newton point inversion](/newton-point-inversion/) page, $r_2(s, t) = (3s, 3t, h(s, t))$ with top height $h(\tfrac12, \tfrac12) = 1.6875$, and let $r_1$ be the sphere of radius $0.2$ about $c = (1.5, 1.5, 1)$, below the top. For any point $y$ of the bump and $x$ of the sphere, $|x - y| \ge |c - y| - 0.2$, with equality on the segment from $c$ to $y$, so $d$ is the distance from $c$ to the bump minus $0.2$. That distance is $0.6872366$, attained at four points near $(s, t) = (0.4641, 0.4641)$ and its mirror images, so $d \approx 0.4872366$ with four closest pairs. The pair through the top, at distance $0.6875 - 0.2 = 0.4875$, is also a common normal pair, but not a minimum.
- **Coaxial cylinders.** The cylinders $x^2 + y^2 = 1$ and $x^2 + y^2 = 4$ have $d = 1$, attained along a whole family of pairs, one for each angle and each height. The solutions of the four equations are not isolated, and Newton's method on them has a singular Jacobian at every solution.
- **Contact.** The planes $z = 0$ and $z = x$ meet in the $y$ axis, $d = 0$, and every point of the axis gives a minimizing pair.

## Known algorithms

- **Newton on the four equations.** Solve the system with [Newton's method for systems](/newton-method-for-systems/) from the best pair of a coarse sample of both surfaces. It converges quadratically near a nondegenerate minimum, and like [Newton point inversion](/newton-point-inversion/) it gives the global answer only from a good start.
- **Alternating projection.** Project the current point of $r_1$ onto $r_2$, then the result back onto $r_1$, and repeat. Each step does not increase $D$, because each projection minimizes over half of the variables. It converges linearly, slowly when the surfaces are nearly parallel.
- **Subdivision with bounds.** By the [convex hull property](/convex-hull-property/), a Bézier patch lies in the convex hull of its control points, so the distance between the two hulls is a lower bound for $d$. Split both nets with the [de Casteljau algorithm](/de-casteljau-algorithm/), discard pairs of pieces whose lower bound exceeds the best distance found, and refine the rest. The distance between two hulls is the distance between two convex polytopes, which the [GJK algorithm](/gjk-algorithm/) computes.
- **All stationary points.** The [interval projected polyhedron](/interval-projected-polyhedron/) method, applied to the four polynomial equations in Bernstein form, finds all common normal pairs in the boxes. Patrikalakis and Maekawa, Section 7.3, use it for the distance functions.
- **Polygonal approximation.** Replace both surfaces by triangle meshes within a known tolerance and use a mesh distance or [collision detection](/collision-detection/) method. The error of the mesh adds to the error of the answer.

## Bounds

**Nonconvex.** $D$ is not convex in the parameters, even for two spheres: the four common normal pairs of the sphere example show a minimum, a maximum and two saddles. So no local method is guaranteed to find $d$.

**The hull bound.** If $S_1 \subseteq K_1$ and $S_2 \subseteq K_2$, then $d(S_1, S_2) \ge d(K_1, K_2)$, since the minimum over larger sets is not larger. With the convex hulls of the control nets this gives the lower bound of the subdivision method, and it is $0$ whenever the hulls overlap, which is why the nets must be subdivided.

**Accuracy from a sample.** The distance $\sqrt D = |r_1 - r_2|$ is Lipschitz on the parameter box, with a constant $\Lambda$ that the derivative nets bound. A grid of spacing $h$ in each of the four parameters has a sample within $h / 2$ of $x^*$ in each coordinate, so within $h \sqrt 4 / 2 = h$ in all, and its best value is within $\Lambda h$ of $d$. This gives an approximation with a proved error, at a cost of $(1 / h)^4$ samples.

**Degenerate cases.** When the minimizers are not isolated, as for the coaxial cylinders or at contact, the four equations have a singular Jacobian at every solution. So no method that relies on a regular solution of the system can certify those cases. Interval and subdivision methods still give a correct value of $d$, but not an isolated pair.

The stationary conditions, the common normal property, the hull bound and the sampling bound are proved on this page. The speed of the methods on real models is measured, not proved.

## Reductions

- **To a square system.** Interior common normal pairs are the solutions of four equations in four unknowns, a case of [systems of nonlinear equations](/systems-of-nonlinear-equations/).
- **From point projection.** A point is a degenerate surface, so point projection is a special case.
- **A sphere to a point.** The distance from a sphere of radius $R$ about $c$ to a surface is the distance from $c$ minus $R$, when that is positive, as in the bump example. The same holds for the offset of any surface by $R$: the distance between $S_1$ and $S_2$ is $R$ more than the distance between $S_1$ and the [offset surface](/offset-surface/) of $S_2$ at distance $R$, as long as both are positive.
- **To intersection.** Deciding $d = 0$ is deciding whether the two surfaces meet, so the problem is at least as hard as the decision version of [surface surface intersection](/surface-surface-intersection/).

## Applications

- **Clearance and interference.** Check that two parts of an assembly keep a gap, or find where they collide.
- **Machining.** A ball end tool gouges a surface when its center comes closer than the radius, the core of [gouge detection](/gouge-detection/). The distance between the tool path surface and the part decides it.
- **Offsets and blends.** If a surface has a common normal pair with itself of length $2R$, with the normals facing each other, its [offset surface](/offset-surface/) at distance $R$ passes twice through the midpoint. So the shortest such pair, with the largest curvature, bounds the offset distance at which the offset starts to intersect itself.
- **Robotics.** Distances between links and obstacles feed motion planners and collision avoidance.
- **Before intersection.** A positive lower bound on $d$ for two patches proves that they do not meet, so an intersection routine can skip the pair.

## References
