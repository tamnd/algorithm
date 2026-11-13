---
tag: ZVWZT1
kind: algorithm
slug: marching-surface-intersection
name: Marching surface intersection
aliases:
- intersection curve tracing
- surface intersection by marching
area: cad/solid-modeling
level: core
summary: Traces each branch of a surface intersection curve from a start point by stepping along the tangent and correcting with Newton iterations onto both surfaces.
solves: [surface-surface-intersection]
model: real-ram
complexity:
  vars: {n: the number of points on the traced branch, i: the number of Newton iterations in one correction}
  time: {worst: O(n i)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1987
  people: [Robert E. Barnhill, Gerald Farin, M. Jordan, Bruce R. Piper]
  note: Barnhill, Farin, Jordan and Piper described a marching method for the intersection of two parametric surfaces, with start points, a step along the tangent and a correction onto both surfaces.
prereqs: [surface-surface-intersection, newton-method-for-systems, implicit-surface]
see_also: [subdivision-surface-intersection, homotopy-continuation, kantorovich-theorem, interval-newton-method, rolling-ball-blend, curve-intersection, trimmed-surface, isosurface-extraction]
sources:
  - paper: doi:10.1016/0167-8396(87)90020-3
    title: Robert E. Barnhill, Gerald Farin, M. Jordan and Bruce R. Piper, Surface/surface intersection, Computer Aided Geometric Design 4(1-2), 3 to 16, 1987
    locator: the whole paper (the marching scheme, the start points, the step length and the correction onto both surfaces)
  - paper: doi:10.1109/38.180122
    title: Nicholas M. Patrikalakis, Surface-to-surface intersections, IEEE Computer Graphics and Applications 13(1), 89 to 95, 1993
    locator: the section on marching methods and their failure modes (missed loops, branch jumping and singular points)
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 5, Intersection problems, Section 5.8.2.3, Marching methods, and Section 5.8.3 on implicit and implicit intersections
  - paper: doi:10.1016/0167-8396(88)90029-5
    title: Thomas W. Sederberg and Ray J. Meyers, Loop detection in surface patch intersections, Computer Aided Geometric Design 5(2), 161 to 171, 1988
    locator: the normal cone test that tells when a pair of patches can hold a closed loop, which a marcher needs to find all start points
---

Marching traces one branch of the intersection curve of two surfaces. It starts from a point on the curve and repeats two steps: a *predictor* step of length $h$ along the tangent of the curve, which is the cross product of the two surface normals, and a *corrector* that pulls the predicted point back onto both surfaces with [Newton's method for systems](/newton-method-for-systems/). The result is a sequence of points on the curve, each accurate to the Newton tolerance, which is the usual output of [surface surface intersection](/surface-surface-intersection/) in CAD systems. Marching is fast and accurate, but it finds only the branch of its start point: it misses closed loops that have no start point, and with a long step it can jump to another branch. Barnhill, Farin, Jordan and Piper described the method for parametric surfaces in 1987.

## In plain words

Two curved sheets cross along a curve. Stand on the curve and look along it: the direction of the curve is at right angles to both sheets' normals, so it is easy to compute. Take a small step in that direction. The step leaves the curve a little, because the curve bends. So pull the new point back onto both sheets, by a few rounds of Newton's method. Now you are on the curve again, a step further along. Repeat.

Stop when you are back where you started, which means the curve is a closed ring, or when you leave the region of interest. Then go back to the start and walk the other way.

The walk never visits a ring of the curve that it did not start on. Finding one starting point on every ring is a separate task.

## The problem

The input is two implicit surfaces $f(x) = 0$ and $g(x) = 0$ in $\mathbb{R}^3$, with gradients $\nabla f$ and $\nabla g$, a start point $x_0$ near the curve $C = \{f = g = 0\}$, a step length $h$, and a box that bounds the region. The output is one branch of $C$, the one through the point that $x_0$ converges to, as a polyline whose vertices satisfy $|f| \le \tau$ and $|g| \le \tau$ for the tolerance $\tau$, and a flag that tells whether the branch closed. This page uses quadrics for $f$ and $g$: planes, spheres and cylinders. For two parametric surfaces the same scheme runs in the four parameters, with the equations $S_1(u, v) = S_2(s, t)$. A point where $\nabla f \parallel \nabla g$ is where the curve can be singular, and the method treats it as a failure of the step, not as a normal case.

## The algorithm

```pseudo id=main
MARCH(f, g, x0, h, box)
L1  p0 ← CORRECT(x0)                         ▷ Newton onto f = g = 0
L2  A ← empty, B ← empty                     ▷ points after p0 and before p0
L3  for d in (+1, −1) do
L4      p ← p0, t' ← d · T(p0), δ ← h         ▷ T(p) = unit vector of ∇f(p) × ∇g(p)
L5      repeat: t ← T(p), with the sign that agrees with t'
L6          q ← CORRECT(p + δ t)
L7          if CORRECT failed or T(q) turns by more than α from t then δ ← δ / 2 and go to L5 (stop if δ < δ_min)
L8          if q is outside box then leave the loop
L9          if the trace has been farther than 2h from p0 and |q − p0| ≤ h then return the closed branch p0, A
L10         append q to A if d = +1, or to B if d = −1
L11         p ← q, t' ← t, δ ← min(h, 1.5 δ)
L12 return the open branch reverse(B), p0, A
```

CORRECT solves the two equations $F(x) = (f(x), g(x)) = 0$ in three unknowns with Newton steps of least length:

$$x \leftarrow x - J^\top (J J^\top)^{-1} F(x), \qquad J = \begin{pmatrix} \nabla f(x)^\top \\ \nabla g(x)^\top \end{pmatrix}.$$

Each step moves $x$ in the plane spanned by the two gradients, normal to the curve, so the correction does not slide along the curve. The $2 \times 2$ matrix $J J^\top$ is singular exactly when the gradients are parallel, and CORRECT reports a failure there. Another common form adds a third equation, the plane through the predicted point normal to $t$, and solves a square $3 \times 3$ Newton system.

Line L7 is the step control. A step is refused when Newton does not converge, or when the tangent turns by more than the angle $\alpha$, a sign that the step went past a sharp bend or onto another branch. Line L11 lets the step grow back towards $h$.

## Example

Viviani's curve is the intersection of the sphere $f = x^2 + y^2 + z^2 - 4$ and the cylinder $g = (x - 1)^2 + y^2 - 1$, which touches the sphere from inside at $(2, 0, 0)$. The curve is $(1 + \cos s, \sin s, 2 \sin(s/2))$ for $0 \le s < 4\pi$, a figure eight with a double point at $(2, 0, 0)$. Start at $x_0 = (0.1, 0, 1.9)$ with $h = 0.1$.

| iteration | point | $f$ | $g$ |
|---|---|---|---|
| L1, 0 | $(0.1, 0, 1.9)$ | $-3.8 \cdot 10^{-1}$ | $-1.9 \cdot 10^{-1}$ |
| L1, 1 | $(-0.005556, 0, 2.005556)$ | $2.2 \cdot 10^{-2}$ | $1.1 \cdot 10^{-2}$ |
| L1, 2 | $(-0.000015, 0, 2.000015)$ | $6.1 \cdot 10^{-5}$ | $3.1 \cdot 10^{-5}$ |
| L1, 3 | $(0, 0, 2)$ | $4.7 \cdot 10^{-10}$ | $2.4 \cdot 10^{-10}$ |
| L6, predictor | $(0, -0.1, 2)$ | $1.0 \cdot 10^{-2}$ | $1.0 \cdot 10^{-2}$ |
| L6, 1 | $(0.004938, -0.099383, 1.997531)$ | $3.1 \cdot 10^{-5}$ | $2.5 \cdot 10^{-5}$ |
| L6, 2 | $(0.004951, -0.099381, 1.997523)$ | $2.1 \cdot 10^{-10}$ | $1.5 \cdot 10^{-10}$ |

The residuals square at each iteration, as Newton's method does near a regular point. At $p_0 = (0, 0, 2)$ the gradients are $(0, 0, 4)$ and $(-2, 0, 0)$, and their cross product $(0, -8, 0)$ gives the first direction. The trace passes the double point twice, once on each lobe, because the predictor carries it straight through: there the gradients $(4, 0, 0)$ and $(2, 0, 0)$ are parallel, but no computed point falls on it. It closes after $153$ points with a polyline of length $15.2772$. With $h = 0.02$ it closes after $764$ points with length $15.2806$. The exact length, $\int_0^{4\pi} \sqrt{1 + \cos^2(s/2)} \, ds$, is $15.2808$.

## Correctness

The tangent of $C$ at a regular point is perpendicular to both gradients, so it is parallel to $\nabla f \times \nabla g$, which justifies line L5. Near a point where the gradients are independent, the Newton step of least length converges quadratically to a point of $C$ at distance $O(|F(x)|)$ from its start. The predictor is off the curve by $O(\delta^2)$, so each corrected point lies on the same branch and moves along it by $\delta + O(\delta^2)$. For a compact regular branch and a step below a bound that depends on its curvature and its distance to other branches, the trace visits the branch in order and closes it. The [full proof](proofs/correctness.md) states these assumptions and proves the claim, including the converse fact that the trace never leaves a tube around the branch of the start point, so it cannot find another component.

What is proved is local. The constants in the step bound are not computed by the method, so in practice $h$ and $\alpha$ are chosen by experience, and the success of the trace on a given model is measured, not proved.

## Complexity

The costs are in the [real RAM](/real-ram/) with square roots. One Newton iteration evaluates two quadrics and their gradients and solves a $2 \times 2$ system, $O(1)$ time. A point costs $O(i)$ for $i$ iterations, so the branch costs $O(ni)$ time for $n$ points, plus the refused steps of line L7, at most $\log_2(h / \delta_{\min})$ for each point. The space is $O(n)$ for the output. The number of points is about the length of the branch divided by $h$, and the accuracy between points is the chord error, about $h^2 \kappa / 8$ for curvature $\kappa$.

## Properties

- **Local and accurate.** Every output point is on both surfaces to the Newton tolerance, independently of $h$.
- **One branch per start point.** The method finds the component of the start point and nothing else.
- **Order is free.** The points come in order along the curve, which a spline fit or a [trimmed surface](/trimmed-surface/) needs.
- **Not exact.** All arithmetic is floating point. A decision such as "the branch closed" or "the gradients are parallel" compares computed numbers with tolerances.

## Variants and improvements

- **Parametric surfaces.** March in the four parameters $(u, v, s, t)$ with the three equations $S_1(u, v) - S_2(s, t) = 0$. The output points are then given in both parameter domains, as trimming curves need.
- **Start points.** Intersect the boundary curves of each patch with the other surface, which finds every open branch. For closed loops, subdivide until the [loop test](/surface-surface-intersection/) of Sederberg and Meyers excludes loops in each pair of patches, and start from the boundary points of the pieces. This hybrid is the usual production method.
- **Step control by curvature.** Choose $h$ from the curvature of $C$, computed from the second derivatives of the surfaces, to keep the chord error below a bound.
- **Certified tracing.** [Interval Newton methods](/interval-newton-method/) or the [Kantorovich theorem](/kantorovich-theorem/) prove that a box around each step contains a single piece of one branch, so the trace cannot jump. [Homotopy continuation](/homotopy-continuation/) uses the same predictor and corrector to follow solution paths of polynomial systems.
- **Singular points.** At a point where the gradients are parallel, branch points are found from the second derivatives, and the trace continues on each outgoing branch.

## When to use it

Use marching when the start points are known or can be found reliably, and when the output must be accurate and ordered: for the edges of Boolean operations, for trimming curves, and for fillet spines in the [rolling-ball method](/rolling-ball-blend/). Use [subdivision](/subdivision-surface-intersection/) when it matters more that no part of the curve is missed than that it is fast, or to find the start points for marching.

## Pitfalls

- **Missed loops.** A small closed loop with no start point is not found. The sphere $x^2 + y^2 + z^2 = 1$ and the plane $z = 1 - \delta$ meet in a circle of radius about $\sqrt{2\delta}$ that no boundary curve of a large patch meets. A start-point search on a coarse grid can miss it.
- **Several components.** The sphere of radius $2$ and the cylinder $x^2 + y^2 = 1$ meet in two circles at $z = \pm\sqrt 3$. A trace from one start point closes after one circle and never sees the other.
- **Branch jumping.** Where two branches pass close to each other, or cross at a singular point, a long step lands on the other branch, and the trace continues there. The two cylinders $x^2 + y^2 = 1$ and $x^2 + z^2 = 1$ meet in two ellipses that cross at $(\pm 1, 0, 0)$. Keep the step short near points where $|\nabla f \times \nabla g|$ is small, and check the turning angle as line L7 does.
- **Tangential contact.** Where the surfaces touch along the curve, $\nabla f \parallel \nabla g$ at every point, $J J^\top$ is singular, and the Newton step fails. Such curves need a different formulation, for example as the minima of $f^2 + g^2$.
- **Closing too early.** The closure test at line L9 can fire when the curve passes near its start point without closing. The guard of line L9, a trace that has first been farther than $2h$, helps but is not a proof; a robust code compares the tangents as well.

## Implementations

## History

Barnhill, Farin, Jordan and Piper's paper of 1987 described a marching method for two parametric surfaces, and Barnhill and Kersey refined it in 1990. Sederberg and Meyers in 1988 gave the normal cone test for loops, which made it possible to find start points on every closed branch. Patrikalakis's survey of 1993 placed marching beside lattice evolution, subdivision and analytic methods, and named the missed loops and the jumps between branches as its two main failures.

## References
