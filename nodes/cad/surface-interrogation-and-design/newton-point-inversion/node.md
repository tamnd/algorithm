---
tag: BYMVEB
kind: algorithm
slug: newton-point-inversion
name: Newton point inversion
aliases:
- Newton foot point iteration
area: cad/surface-interrogation-and-design
level: core
summary: Solves (S(u, v) - P) . S_u = 0 and (S(u, v) - P) . S_v = 0 by Newton steps from the best sample of a coarse grid, the method of Piegl and Tiller.
solves: [point-projection-onto-a-surface]
model: real-ram
complexity:
  vars: {n: the number of grid intervals per parameter, m: the number of control points of the patch, k: the number of Newton iterations}
  time: {worst: O((n^2 + k) m)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1997
  people: [Les Piegl, Wayne Tiller]
  note: The NURBS Book gave the Newton iteration for point inversion and projection on NURBS curves and surfaces, with a start point from a coarse sample and three stopping tests. Its first edition appeared in 1995.
prereqs: [point-projection-onto-a-surface, newton-method-for-systems, bezier-patch]
see_also: [kantorovich-theorem, quadratic-convergence, minimum-distance-between-surfaces, surface-curvature, gauss-newton-algorithm, interval-projected-polyhedron, iterative-closest-point, parameter-correction]
sources:
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 6, Section 6.1, Point inversion and projection for curves and surfaces, pages 229 to 234 (the Newton iteration on the two equations, the start point from evenly spaced samples, the three stopping tests, and the clamping or wrapping of the parameters)
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 5, Section 5.5.2.2, Newton's method, and Section 5.5.2.3, bounding box and subdivision followed by minimization
  - paper: doi:10.1016/S0167-8396(03)00021-9
    title: Ying Liang Ma and W. T. Hewitt, Point inversion and projection for NURBS curve and surface, control polygon approach, Computer Aided Geometric Design 20(2), 79 to 99, 2003
    locator: the whole paper (the failures of a start point taken from samples, and a start point from the subdivided control net)
---

Newton point inversion finds the parameters $(u, v)$ of the point of a parametric surface $r(u, v)$ nearest to a given point $p$, by Newton's method on the two first order equations $(r - p) \cdot r_u = 0$ and $(r - p) \cdot r_v = 0$. It starts from the best sample of a coarse grid of parameters and stops when the point is reached, when the vector $r - p$ is normal to the surface, or when the steps stop moving the point. Piegl and Tiller gave this form in The NURBS Book, and most CAD kernels use a variant of it. It converges quadratically near a nondegenerate foot point, but it returns the nearest point of the whole surface only when the start grid is fine enough, a condition the method cannot check.

## In plain words

You want the spot on a curved sheet closest to a point. First, try a small grid of spots, for example eleven by eleven, and keep the closest one. That is a rough answer.

Then improve it. Near the rough answer, pretend the sheet is a simple bowl that matches the sheet in height, slope and bend. The bottom of that bowl is easy to compute. Jump there. Repeat. Each jump roughly doubles the number of correct digits, so a few jumps are enough.

Stop when the line from the point to the sheet is at a right angle to the sheet, or when the jumps become too small to matter. If a jump would make the distance larger, take half of it instead. If the rough answer was near the wrong valley, the jumps go to the bottom of that valley, and the method has no way to know.

## The problem

The input is a tensor product [Bézier patch](/bezier-patch/) $r(u, v)$ on $\Omega = [0, 1]^2$, given by its control net, a point $p$, a grid size $n$, and two tolerances: $\varepsilon_1$ for distances in space and $\varepsilon_2$ for cosines. The output is a parameter pair $(u, v) \in \Omega$ that satisfies the first order conditions of [point projection](/point-projection-onto-a-surface/) to the tolerance, and is the nearest point when the start lies in its basin. A [B-spline](/b-spline/) or [NURBS](/nurbs/) surface is handled the same way, with the evaluation done by the [de Boor algorithm](/de-boor-algorithm/).

Write $w = r(u, v) - p$, $f = w \cdot r_u$ and $g = w \cdot r_v$. The squared distance $D = |w|^2$ has gradient $2 (f, g)$ and half Hessian

$$H = \begin{pmatrix} r_u \cdot r_u + w \cdot r_{uu} & r_u \cdot r_v + w \cdot r_{uv} \\ r_u \cdot r_v + w \cdot r_{uv} & r_v \cdot r_v + w \cdot r_{vv} \end{pmatrix},$$

which is the Jacobian of $(f, g)$. At a foot point $p = r + t N$, $H = \mathrm{I} - t \, \mathrm{II}$ in terms of the [fundamental forms](/fundamental-forms/), so $H$ is singular exactly when $p$ is a center of principal curvature of the foot point.

## The algorithm

```pseudo id=main
NEWTON-INVERT(r, p, n, ε1, ε2, kmax)
L1  (u, v) ← the grid point (i/n, j/n), 0 ≤ i, j ≤ n, with the least D = |r − p|²
L2  repeat at most kmax times
L3      evaluate r, r_u, r_v, r_uu, r_uv, r_vv at (u, v); w ← r − p; f ← w·r_u; g ← w·r_v
L4      if |w| ≤ ε1 then return (u, v)                              ▷ point coincidence
L5      if, for u and for v, |cos(w, r_u)| ≤ ε2 or the parameter is on an edge with its derivative pointing out, then return (u, v)   ▷ zero cosine
L6      H ← the half Hessian above
L7      δ ← −A⁻¹ (f, g) on the parameters not frozen, with A = H if H is positive definite and A = I otherwise
L8      λ ← 1; while D(clamp((u, v) + λδ)) > D(u, v): λ ← λ/2; (u', v') ← clamp((u, v) + λδ)
L9      if |(u' − u) r_u + (v' − v) r_v| ≤ ε1 then return (u', v')      ▷ the point no longer moves
L10 return (u, v)
```

Lines L1 to L5 and L9 are the method of Piegl and Tiller. Their three tests are the point coincidence of line L4, the zero cosine of line L5, and the test of line L9 that the step no longer moves the point in space. They clamp a parameter that leaves the box to its end, or wrap it around for a closed surface. This version adds three guards, each a few lines. A parameter on an edge whose derivative points out of the box is *frozen*, because there the box constraint is active and the Newton step in that parameter is meaningless. Where $H$ is not positive definite, line L7 uses the first fundamental form $\mathrm{I}$, which is the Gauss-Newton matrix of the problem and always positive definite, so the step goes downhill. Line L8 halves a step that would raise $D$. Near a nondegenerate minimum none of the guards fires, and the method is the plain Newton iteration. If a direction is still not downhill after the frozen and clamped parts are dropped, the code falls back to the scaled gradient $-(f / E, g / G)$.

## Example

Take the bicubic patch with control points $P_{ij} = (i, j, z_{ij})$, $0 \le i, j \le 3$, where $z_{11} = z_{12} = z_{21} = z_{22} = 3$ and all other $z_{ij} = 0$. Since the $x$ and $y$ coordinates of the net are evenly spaced, $r(u, v) = (3u, 3v, h(u, v))$, a bump of height $h(\tfrac12, \tfrac12) = 1.6875$. Project $p = (1, 2, 2.5)$ with $n = 4$.

The $25$ grid samples have distances from $1.0771$ (at the center) to $3.7749$, so line L1 starts at $(0.5, 0.5)$. There $f = 1.5$, $g = -1.5$ and $H = \operatorname{diag}(19.96875, 19.96875)$, so the first step is $\delta = (-0.0751174, 0.0751174)$.

| iteration | $u$ | $v$ | $\lvert w \rvert$ | $f$ | $g$ |
|---|---|---|---|---|---|
| 0 | $0.5$ | $0.5$ | $1.0771054962$ | $1.5$ | $-1.5$ |
| 1 | $0.4248826291$ | $0.5751173709$ | $0.9690612209$ | $-5.6 \cdot 10^{-2}$ | $5.6 \cdot 10^{-2}$ |
| 2 | $0.4274146359$ | $0.5725853641$ | $0.9689144490$ | $-1.7 \cdot 10^{-4}$ | $1.7 \cdot 10^{-4}$ |
| 3 | $0.4274223332$ | $0.5725776668$ | $0.9689144476$ | $-1.5 \cdot 10^{-9}$ | $1.5 \cdot 10^{-9}$ |
| 4 | $0.4274223333$ | $0.5725776667$ | $0.9689144476$ | $-1.1 \cdot 10^{-15}$ | $-1.3 \cdot 10^{-15}$ |

Line L5 stops at iteration $4$. The residual is roughly squared at each step: $1.5$, $5.6 \cdot 10^{-2}$, $1.7 \cdot 10^{-4}$, $1.5 \cdot 10^{-9}$, with ratios $e_{k+1} / e_k^2$ of about $0.025$, $0.054$ and $0.054$. The foot point is $r = (1.282267, 1.717733, 1.617138)$, and $w = (0.282267, -0.282267, -0.882862)$ is a multiple of $r_u \times r_v = (-2.877462, 2.877462, 9)$, so $p$ is on the normal line. The point lies on the diagonal $u + v = 1$ because $p$ and the patch are symmetric about the plane $x + y = 3$. A $301 \times 301$ grid gives $0.968927$ as its best distance, a little worse than the Newton answer, as a grid must be.

## Correctness

The [full proof](proofs/correctness.md) shows five facts, in exact arithmetic. A point returned by line L5 satisfies the first order conditions of the box to the tolerance. Each direction of line L7 goes downhill unless the point already satisfies them, so the halving of line L8 ends and $D$ never increases: the answer is never worse than the best grid sample. Near an interior foot point at which $1 - t k_1 > 0$ and $1 - t k_2 > 0$, a strict local minimum with $p$ off the focal surface, the iterates take full Newton steps and $|x_{k+1} - x^*| \le C |x_k - x^*|^2$, with $C = |H(x^*)^{-1}| \cdot \gamma$ for the Lipschitz constant $\gamma$ of $H$. This is the standard local estimate for Newton's method, proved in the file. Last, if every point whose value of $D$ is within $\eta$ of the global minimum lies in that quadratic basin, a grid with spacing $h \le \sqrt 2 \, \eta / \Lambda$, for a bound $\Lambda$ on $|\nabla D|$, makes the method return the global minimum.

What is not proved is that a given grid is fine enough: $\eta$ depends on the second best local minimum, which the method does not know. On random bicubic patches, with control points jittered by up to $0.3$ around a $4 \times 4$ grid, heights in $[-1.5, 1.5]$ and $p$ in the box $[-0.5, 3.5]^2 \times [-2, 2]$, the answer was worse than a $101 \times 101$ grid in $4$ of $300$ cases for $n = 2$, in $1$ of $300$ for $n = 4$, and in none of $300$ for $n = 10$. These rates are measured on that class only.

## Complexity

Let the patch have $m = (d_1 + 1)(d_2 + 1)$ control points for bidegree $(d_1, d_2)$. One evaluation of the point and its derivatives up to order two costs $O(m)$ once the Bernstein values are known, which cost $O(d_1 + d_2)$. Line L1 makes $(n + 1)^2$ evaluations, $O(n^2 m)$ time. Each iteration costs $O(m)$ for line L3 and $O(m)$ for each halving of line L8. Near the solution no halving happens, and quadratic convergence makes $k$ about $\log_2 \log_2 (1 / \varepsilon)$ once the error is below $1 / (2C)$, so $k$ is $4$ to $6$ in double precision. The total is $O((n^2 + k) m)$ time and $O(m)$ extra space. For NURBS each evaluation costs $O((d_1 + 1)(d_2 + 1))$ after a search for the knot span, which is $O(\log K)$ for $K$ knots.

## Properties

- **Local.** It finds the stationary point whose basin holds the start, and the start is the only global ingredient.
- **Quadratic near a regular minimum.** The number of correct digits roughly doubles per step, as the example shows.
- **Monotone.** With the halving of line L8 the distance never increases, so the answer is at least as good as the start sample.
- **Floating point.** All steps are in floating point. The output satisfies the tests to the tolerances, and nothing is exact.

## Variants and improvements

- **Plain Piegl and Tiller.** Without the guards, the iteration is the textbook Newton method with clamping. It can cycle on an edge, where clamping one parameter leaves the other step wrong, and it can climb to a maximum where $H$ is indefinite. The guards remove both failures at the cost of one extra evaluation per step.
- **Curves.** For a curve $c(u)$ the iteration is $u \leftarrow u - \frac{(c - p) \cdot c'}{c' \cdot c' + (c - p) \cdot c''}$, with the same tests.
- **Better start points.** Ma and Hewitt subdivide the control net, discard the pieces whose control polygon is farther than the best distance found, and start Newton from the remaining pieces. With exclusion by proved bounds this makes the answer global up to the tolerance.
- **Certified.** The [interval Newton method](/interval-newton-method/) or the [interval projected polyhedron](/interval-projected-polyhedron/) method finds all stationary points in the box with proofs.
- **Gauss-Newton.** Dropping the terms $w \cdot r_{uu}$, $w \cdot r_{uv}$, $w \cdot r_{vv}$ from $H$ gives the [Gauss-Newton algorithm](/gauss-newton-algorithm/) for the least squares problem $\min |r - p|^2$. It needs no second derivatives. It converges quadratically for point inversion, where $w = 0$ at the solution and the dropped terms vanish there, and only linearly when $p$ is off the surface, with a rate that is good when the distance is small compared with the radius of curvature.
- **Many points.** When many points are projected onto one surface, as in [iterative closest point](/iterative-closest-point/) or [parameter correction](/parameter-correction/), the foot point of a neighbor is a better start than the grid.

## When to use it

Use it to snap picked points, to invert points known to lie on the surface, and in loops that project many points that move little, where a good start is always at hand. Use a subdivision method with exclusion, or a certified solver, when the answer must be the global minimum, for example when a distance is used as a tolerance check in inspection.

## Pitfalls

- **The wrong valley.** The best grid sample can lie in the basin of a local minimum that is not the global one. Then the method converges, quickly and accurately, to the wrong answer.
- **A start on a stationary point.** For the bump patch and $p = (1.5, 1.5, 1)$, below the top, the center $(0.5, 0.5)$ is a grid point for even $n$ and satisfies $f = g = 0$ exactly, by symmetry. Line L5 returns it at once with distance $0.6875$. But there $t = -0.6875$, $k = -1.5$ and $1 - t k = -0.03125 < 0$, so the center is not a minimum: the true minimum is $0.6872366$ near $(0.4641, 0.4641)$ and its three mirror images, which $n = 3$ finds. A second order check at line L5 catches this case.
- **Near the focal surface.** When $1 - t k_i$ is near $0$, $H$ is nearly singular, convergence slows, and the parameters are ill conditioned even when the distance is accurate. In the case above, runs from different grids agree on the distance to $10^{-10}$ and on $u$ only to about $10^{-5}$.
- **Singular parametrizations.** At a pole of a sphere or the apex of a cone, $r_u = 0$, the zero cosine test divides by zero, and $\mathrm{I}$ is singular. Treat such points as special cases.
- **Clamping alone.** Clamping a Newton step to the box without freezing the parameter can cycle along an edge, as the variant above notes.
- **Tolerances in model units.** $\varepsilon_1$ is a distance and must match the size of the model. A value of $10^{-12}$ is too strict for a part measured in meters with single precision data.

## Implementations

## History

Newton's method for the foot point on a parametric curve or surface is older than any single source. Piegl and Tiller gave the form used in most NURBS libraries in The NURBS Book (first edition 1995, second edition 1997), with the start from evenly spaced samples and the three stopping tests. Patrikalakis and Maekawa (2002) listed it with implicitization, subdivision and distance function methods for point and surface problems. Ma and Hewitt (2003) replaced the sampled start by a start from the subdivided control net, to make the choice of the basin more reliable.

## References
