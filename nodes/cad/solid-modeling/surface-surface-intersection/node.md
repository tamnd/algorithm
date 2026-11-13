---
tag: HYBHKS
kind: problem
slug: surface-surface-intersection
name: Surface surface intersection
aliases:
- surface intersection problem
area: cad/solid-modeling
level: core
summary: Compute all curves and isolated points where two parametric or implicit surfaces meet, with their topology, the basic step of Booleans on curved solids.
prereqs: [parametric-surface, implicit-surface, trimmed-surface]
see_also: [marching-surface-intersection, subdivision-surface-intersection, curve-intersection, solid-boolean-operations, resultant, homotopy-continuation, interval-newton-method, rolling-ball-blend]
sources:
  - paper: doi:10.1109/38.180122
    title: Nicholas M. Patrikalakis, Surface-to-surface intersections, IEEE Computer Graphics and Applications 13(1), 89 to 95, 1993
    locator: the whole survey (the statement of the problem, the classes of methods, which are lattice evolution, marching, subdivision and analytic methods, and the open issues of robustness)
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 5, Intersection problems, Section 5.8, Surface/surface intersections (the parametric and implicit cases, subdivision methods and marching methods)
  - paper: doi:10.1016/0167-8396(87)90020-3
    title: Robert E. Barnhill, Gerald Farin, M. Jordan and Bruce R. Piper, Surface/surface intersection, Computer Aided Geometric Design 4(1-2), 3 to 16, 1987
    locator: the whole paper (a marching method for parametric surfaces and its start points and step control)
  - paper: doi:10.1016/0167-8396(88)90029-5
    title: Thomas W. Sederberg and Ray J. Meyers, Loop detection in surface patch intersections, Computer Aided Geometric Design 5(2), 161 to 171, 1988
    locator: the whole paper (a closed intersection loop forces two points with parallel normals, and the normal cone test that excludes loops)
  - book: isbn:9781558600676
    title: Christoph M. Hoffmann, Geometric and Solid Modeling, An Introduction, Morgan Kaufmann, 1989
    locator: the chapter on surface intersections (general locator, the chapter number and title are not confirmed)
---

Surface surface intersection, often called SSI, is the problem of finding the set where two surfaces meet: the curves, the isolated points and, when the surfaces overlap, the shared regions, together with how these pieces are connected. The surfaces are [parametric](/parametric-surface/), such as [NURBS](/nurbs/) patches, or [implicit](/implicit-surface/), such as planes, quadrics and tori. Every Boolean operation on curved solids needs it, because the new edges of the result are the intersection curves of the faces, and the faces are then cut along these curves into [trimmed surfaces](/trimmed-surface/). The hard part is not accuracy but topology: a method must not miss a small closed loop, must not jump from one branch to another, and must find the singular points where branches cross.

## In plain words

Two curved sheets in space cross each other. Where they cross, they form one or more curves. Some curves run from edge to edge of the sheets, some close on themselves like a ring, and some cross each other at a point. When the sheets only touch, the answer can be a single point.

The task is to find all of these curves and points, each one to a given accuracy, and to know which pieces join which. A list of points that are close to the answer is not enough. A tiny ring that the method misses means that a hole in the final model is missing too.

There is no simple formula for the curve in general, so methods either follow the curve step by step or cut the sheets into small pieces until each piece is easy.

## Definition

**Input.** Two surfaces $S_1$ and $S_2$ in $\mathbb{R}^3$. Each is given as a parametric patch $S_i : D_i \to \mathbb{R}^3$, polynomial or rational, on a rectangle $D_i$ (possibly with trimming loops), or as the zero set $\{x : f_i(x) = 0\}$ of a polynomial $f_i$, restricted to a box. A tolerance $\varepsilon > 0$ for the numerical case.

**Output.** The intersection $I = S_1 \cap S_2$ as a finite structure:

- a list of *branches*, each a curve segment or a closed loop, given in space and in the parameter domain of each parametric surface;
- the *endpoints* of open branches, which lie on the boundary of a domain;
- the *singular points*, where two or more branches meet, and the *isolated points*, where the surfaces touch;
- the *overlap regions*, where the surfaces coincide on a set of positive area;
- the incidence of branches and points.

In the exact version each branch is given by an exact algebraic description and the topology is that of $I$. In the numerical version each branch is a sequence of points, or a spline, within distance $\varepsilon$ of both surfaces and of the true branch, and the branches, loops and singular points are in one to one correspondence with those of $I$.

**Constraints.** The topology must be right: every component of $I$ is found once, two branches are not joined unless they meet, and loops are closed. Tangential contact, singular points and overlaps are part of the input, not an exception. A point $x$ with $\nabla f_1(x) \parallel \nabla f_2(x)$, or with parallel normals $N_1 \parallel N_2$ in the parametric case, is where the curve can be singular or tangential.

**Size.** The degrees of the surfaces, the number of patches, and the number of output points, which depends on $\varepsilon$.

**Model.** The [real RAM](/real-ram/) for the exact version, with exact signs of polynomials at algebraic points. Floating point with stated tolerances for the numerical version.

## Variants

- **Implicit and implicit.** Both surfaces are zero sets. The intersection is the space curve $f_1 = f_2 = 0$. Its tangent at a regular point is $\nabla f_1 \times \nabla f_2$.
- **Parametric and implicit.** Substitute the patch into the equation: $g(u, v) = f_2(S_1(u, v)) = 0$ is a plane algebraic curve in the domain of $S_1$. The problem becomes the tracing of a plane curve, and the space curve is its image under $S_1$.
- **Parametric and parametric.** The hardest case and the usual one for NURBS models: find all $(u, v, s, t)$ with $S_1(u, v) = S_2(s, t)$, three equations in four unknowns, which leaves a one-dimensional solution set.
- **Quadrics.** Two quadrics meet in a space curve of degree at most $4$. Closed-form methods find its parametrization and its topology exactly. Planes, cylinders, cones and spheres make up most faces of mechanical parts, so this case matters in practice.
- **Plane sections.** One surface is a plane. This is contouring, used for slicing in additive manufacturing and for plane cuts in drawing views.
- **Self-intersection.** One surface against itself, $S(u, v) = S(s, t)$ with $(u, v) \ne (s, t)$. It arises for [offset surfaces](/offset-surface/) and sweeps.
- **Curve and surface.** One of the two is a curve. It is a zero-dimensional problem, a system of three equations in three unknowns, and the 2D analog of two curves is [curve intersection](/curve-intersection/).

## Examples

All five are pairs of quadrics with a closed-form answer.

- **Sphere and plane.** $x^2 + y^2 + z^2 = 1$ and $z = 1 - \delta$ meet in the circle of radius $\sqrt{2\delta - \delta^2}$ for $0 < \delta < 2$, in one point for $\delta = 0$, and not at all for $\delta < 0$. For small $\delta$ the circle is a small loop, which a method that samples the surfaces too coarsely misses.
- **Sphere and coaxial cylinder.** $x^2 + y^2 + z^2 = 4$ and $x^2 + y^2 = 1$ meet in the two circles of radius $1$ at $z = \sqrt 3$ and $z = -\sqrt 3$. The answer has two components, and a method that follows the curve from one start point finds one of them.
- **Viviani's curve.** $x^2 + y^2 + z^2 = 4$ and $(x - 1)^2 + y^2 = 1$ meet in the curve $(1 + \cos t, \sin t, 2 \sin(t / 2))$, $0 \le t < 4\pi$. It passes through $(2, 0, 0)$ twice, at $t = 0$ and $t = 2\pi$, so it has a double point there. At that point the cylinder touches the sphere from inside and the gradients $(4, 0, 0)$ and $(2, 0, 0)$ are parallel.
- **Two equal cylinders.** $x^2 + y^2 = 1$ and $x^2 + z^2 = 1$ give $y^2 = z^2$, so the intersection is two ellipses, in the planes $y = z$ and $y = -z$. They cross at $(\pm 1, 0, 0)$, where both gradients are $(\pm 2, 0, 0)$. A method that follows one ellipse can turn onto the other at a crossing.
- **Coincident surfaces.** Two patches that are parts of one plane meet in a region. The answer is an overlap region, bounded by curves, not a curve.

## Known algorithms

- **Analytic methods.** For quadrics and for some pairs of low degree, the curve is found in closed form. For general algebraic surfaces, elimination with the [resultant](/resultant/) or a [Gröbner basis](/groebner-basis/) turns the problem into a plane algebraic curve, whose topology can be found exactly but at a high cost in the degree.
- **Lattice evolution.** Intersect a grid of parameter lines of one surface with the other surface, a set of curve and surface problems, and connect the points. Loops between the grid lines are missed.
- **[Marching](/marching-surface-intersection/).** Start from a point on the curve and step along the tangent, the cross product of the two normals, with a Newton correction onto both surfaces after each step. It is fast and accurate, and it needs a start point on every branch. Barnhill, Farin, Jordan and Piper gave such a method in 1987.
- **[Subdivision](/subdivision-surface-intersection/).** Split both patches until the pieces are nearly flat, keep only the pairs whose bounding volumes overlap, and intersect the flat pieces as planes. By the [convex hull property](/convex-hull-property/) it misses no part of the curve, at a cost that grows quickly with the accuracy.
- **Hybrid methods.** Subdivide until each pair of pieces holds no closed loop, which the loop test of Sederberg and Meyers guarantees when the normal cones of the two pieces do not overlap, and then march from the boundary points of each pair. Most production systems combine the two ideas in this way.
- **Certified methods.** [Interval Newton methods](/interval-newton-method/) and [homotopy continuation](/homotopy-continuation/) give start points and step sizes with proofs that no branch is skipped.

The marching and subdivision pages describe one method each, with code and a proof. This page states what any method must deliver.

## Bounds

**Degree.** By Bézout's theorem, two algebraic surfaces of degrees $m$ and $n$ without a common component meet in a space curve of degree at most $mn$. A rational tensor-product patch of bidegree $(p, q)$ has an implicit equation of degree at most $2pq$, so a bicubic patch has degree at most $18$, and two bicubic patches meet in a curve of degree at most $324$. The intersection of two NURBS patches is therefore not a NURBS curve of low degree, and every system stores an approximation.

**Loops.** Sederberg and Meyers proved a sufficient test: if two smooth patches have a closed intersection loop, then there are two points, one on each patch, inside the loop, at which the normals are parallel. So if the cones of normals of two patches have no common direction, up to sign, the intersection has no closed loop and every branch meets the boundary of a patch.

**Discontinuity.** The topology of $I$ is not a continuous function of the input. In the sphere and plane example, the answer changes from a circle to a point to nothing as $\delta$ passes through $0$. The decision is a sign, and near a tangency it is the sign of a small number computed with large cancellation ([catastrophic cancellation](/catastrophic-cancellation/)). The same problem appears for the [orientation test](/orientation-test/) of polyhedral Booleans. The fixes are exact arithmetic on algebraic numbers, as in [exact geometric computation](/exact-geometric-computation/), or interval arithmetic that reports the uncertain cases.

The degree bound, the loop test and the discontinuity are proved. The speed and the failure rate of marching, subdivision and hybrid methods on industrial models are measured, not proved, and no general method with a proof of correct topology is also fast on NURBS models of high degree.

## Reductions

- **To plane curve tracing.** The parametric and implicit case is the tracing of $f_2(S_1(u, v)) = 0$ in the plane. The parametric and parametric case reduces to it by implicitizing one patch, at the cost of the high degree above.
- **From curve intersection.** Intersecting the cylinders $C_1 \times \mathbb{R}$ and $C_2 \times \mathbb{R}$ over two plane curves gives the vertical lines over the points of $C_1 \cap C_2$, so SSI solves [curve intersection](/curve-intersection/).
- **To systems of equations.** Each start point, each singular point and each point where a branch meets a patch boundary is a solution of a square system of polynomial equations, which [systems of nonlinear equations](/systems-of-nonlinear-equations/) solve.
- **To it from ray and surface intersection.** A ray lies in a plane, so the points where a ray meets a surface are found by intersecting that plane with the surface, a case of SSI, and then the resulting curves with the ray in the plane.

## Applications

- **Boolean operations on curved solids.** The new edges of $A \cup^* B$, $A \cap^* B$ and $A -^* B$ are the intersection curves of the faces; see [solid Boolean operations](/solid-boolean-operations/) and [boundary evaluation](/boundary-evaluation/).
- **Trimming.** The intersection curves, mapped into the parameter domains, become the trimming loops of [trimmed surfaces](/trimmed-surface/).
- **Blending.** The spine of a [rolling-ball blend](/rolling-ball-blend/) is the intersection of two offset surfaces.
- **Machining and slicing.** Plane sections give the contours of layers for 3D printing and the cuts of a tool path.
- **Interference.** Two parts touch or collide when their faces meet.

## References
