---
tag: HBSSZY
kind: algorithm
slug: minimum-zone-cylindricity
name: Minimum zone cylindricity
aliases:
- minimum zone cylinder
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Finds two coaxial cylinders of least radial gap that hold measured points, a nonlinear Chebyshev fit, by linear programs on linearized radii. It finds a local optimum only.
solves: [form-error-evaluation]
model: real-ram
complexity:
  vars: {n: the number of points, s: the number of iterations, k: the number of simplex pivots in one linear program}
  time: {worst: O(s k n²)}
  space: {extra: Θ(n²)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1995
  people: [Kirsten Carr, Placid Ferreira]
  note: Carr and Ferreira computed the minimum zone, minimum circumscribed and maximum inscribed cylinders by a sequence of linear programs that converge to a local optimum.
prereqs: [form-error-evaluation, linear-programming-problem, simplex-method]
see_also: [minimum-zone-flatness, minimum-width-annulus, least-squares-reference-feature, geometric-primitive-fitting, bland-rule, megiddo-fixed-dimension-lp, gauss-newton-algorithm, cad-based-inspection]
sources:
  - paper: doi:10.1016/0141-6359(94)00018-U
    title: Kirsten Carr and Placid Ferreira, Verification of form tolerances part II, cylindricity and straightness of a median line, Precision Engineering 17(2), 1995, 144 to 156
    locator: the formulation of the minimum zone cylinder by linearized distances to the axis and a sequence of linear programs that converge to a local optimum, and the minimum circumscribed and maximum inscribed cylinders
  - paper: doi:10.1016/0141-6359(94)00017-T
    title: Kirsten Carr and Placid Ferreira, Verification of form tolerances part I, basic issues, flatness, and straightness, Precision Engineering 17(2), 1995, 131 to 143
    locator: the linear programming formulation of the minimum zone for flatness and straightness that part II extends
  - paper: doi:10.1007/s00454-001-0039-6
    title: Pankaj K. Agarwal, Boris Aronov and Micha Sharir, Exact and approximation algorithms for minimum-width cylindrical shells, Discrete and Computational Geometry 26(3), 2001, 307 to 320
    locator: the exact minimum width cylindrical shell in polynomial time of high degree, and a faster constant factor approximation
  - paper: doi:10.1287/moor.2.2.103
    title: Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977
    locator: pages 103 to 107, the least-index rule and the proof that it does not cycle
  - url: https://www.iso.org/standard/66777.html
    title: ISO 1101:2017, Geometrical product specifications (GPS), Geometrical tolerancing, Tolerances of form, orientation, location and run-out, fourth edition
    locator: the standard as a whole (the cylindricity tolerance zone between two coaxial cylinders); no clause is quoted
---

Minimum zone cylindricity computes the cylindricity of a measured cylindrical feature: the least radial gap $R_{\mathrm{out}} - R_{\mathrm{in}}$ of two coaxial cylinders that hold all the measured points. For a fixed axis the gap is the range of the distances from the points to the axis, so the problem is to choose the axis, four numbers. The function of the axis is not convex, so this is a nonlinear Chebyshev fit. The method here, after Carr and Ferreira, linearizes the distances about the current axis, solves the [linear program](/linear-programming-problem/) that minimizes the linearized gap inside a box of trust, and keeps the new axis only if the true gap goes down. It finds a local minimum and has no global guarantee. This page is a method; the problem, with the other forms and the choice of reference, is [form error evaluation](/form-error-evaluation/), and the method for flatness and straightness is [minimum zone flatness](/minimum-zone-flatness/).

## In plain words

A shaft should be a perfect cylinder. A machine measures many points on it. We want two tubes with the same center line, one inside the other, so that all points lie between them, and with the walls as close as possible. The gap between the walls is the cylindricity.

If we knew the center line, the answer would be easy: take the nearest and the farthest point from the line. The hard part is the line. So we start with a good guess, then ask how each distance would change if we moved or tilted the line a little. With that simple rule, the best small move is a standard linear problem. We make the move only if the true gap gets smaller, and otherwise we try a smaller move. This ends at a line that no small move improves, but there may be a better line far away.

## The problem

The input is a set of points $q_1, \dots, q_n$ in $\mathbb{R}^3$, measured on a nominally cylindrical surface and corrected for the probe radius. For a line $L$, let $\rho_i(L)$ be the distance from $q_i$ to $L$. The zone shape is the region between two coaxial cylinders, and the objective is the least width
$$ C = \min_L \Bigl( \max_i \rho_i(L) - \min_i \rho_i(L) \Bigr), $$
the minimum zone cylindricity. The output is an axis and the two radii. The method below returns an axis $L$ with the width $W(L) \ge C$ of a true zone, which is a local minimum in practice.

The [least-squares cylinder](/least-squares-reference-feature/), fitted as in [geometric primitive fitting](/geometric-primitive-fitting/), is not the minimum zone cylinder. The zone about its axis is a true zone, so its width is never smaller than $C$. It is a good start for this method.

## The algorithm

```pseudo id=main
MIN-ZONE-CYLINDER(q_1..q_n)
L1  (p, u) ← start axis; W ← width about (p, u); b ← W
L2  repeat
L3      δ ← solution of the LP: minimize R − r subject to
            r ≤ ρ_i + g_i·δ ≤ R for all i, and δ in the box of size b
L4      (p', u') ← axis moved by δ
L5      W' ← max_i ρ_i(p', u') − min_i ρ_i(p', u')
L6      if W' < W then (p, u, W) ← (p', u', W'); b ← 2b
L7      else b ← b/4
L8  until b is below a tolerance; return (p, u), min ρ_i, max ρ_i
```

**Line L1, the start.** The code tries each principal direction of the points as the axis, with the center of a linear circle fit of the points projected on the normal plane, and keeps the thinnest zone. A least-squares cylinder is a better start when it is available, and the caller can pass any start.

**Line L3, the linear program.** In a frame $(e_1, e_2, u)$ at $p$, let $q_i - p$ have coordinates $(x_i, y_i, z_i)$ and $\rho_i = \sqrt{x_i^2 + y_i^2}$. Moving the axis to pass through $(\delta_1, \delta_2, 0)$ with the direction $(\delta_3, \delta_4, 1)$ changes the distance to first order to
$$ \rho_i - \frac{x_i \delta_1 + y_i \delta_2 + z_i (x_i \delta_3 + y_i \delta_4)}{\rho_i} = \rho_i + g_i \cdot \delta . $$
The program has six variables, $\delta$, $r$ and $R$, and $2n + 4$ constraints. The code shifts the variables so that the origin is feasible and solves it by a dense simplex method with Bland's rule. The tilt box is the shift box divided by the largest $\lvert z_i \rvert$, so both move the points by similar amounts.

**Lines L5 to L7, the safeguard.** The linear model is only first-order. The new axis is accepted only if the exact width is smaller, and then the box grows; otherwise the box shrinks. This makes the accepted widths strictly decrease.

## Example

**Alternating contacts.** Twenty-four points lie on three levels $z = -3, 0, 3$, at eight angles on each level, alternately at radius $4$ and $4.05$ about a known axis, and the set is moved by a random rigid motion. From a start tilted by about $0.02$ radians and shifted by $0.03$, the method returns the width $0.05$ to $10^{-9}$, the true axis.

**A lobed shaft.** Forty points on a shaft of radius $5$ and length $10$ with a three-lobe error of amplitude $0.01$ and uniform noise of $\pm 0.002$, seed 1. From the default start, the method stops after six accepted steps at the width $0.01997$. Moving the axis does little against a three-lobe error, so the width stays close to twice the amplitude.

**Noise-free cylinder.** Points on an exact cylinder in a random position give a width below $10^{-8}$.

These numbers are measured with the code on this page, not proved.

## Correctness

The [correctness file](proofs/correctness.md) proves:

- **A true zone.** For a fixed axis, the thinnest coaxial zone has the radii $\min_i \rho_i$ and $\max_i \rho_i$, so every reported value is the width of a zone that holds all points and is at least $C$.
- **The linearization** of the distances in the axis parameters, with a second-order remainder when no point is on the axis.
- **Each linear program** is feasible at the origin after the change of variables, is bounded, and is solved by the simplex method with Bland's rule, which does not cycle.
- **Monotone decrease.** The accepted widths strictly decrease, and the method stops.
- **Progress away from stationary axes.** If the zero step does not minimize the linearized width, a small enough box gives an accepted step.

It does not prove convergence to a stationary axis, and it does not prove that the result is the global minimum $C$. The problem is not convex. The tests compare the result with a grid of directions and positions around the true axis and check that the result is at least as good, and that no axis of a fine grid around the result is better. These checks are measured, not proved.

## Complexity

One iteration builds the program in $\Theta(n)$ and solves it. The dense tableau of the code has $2n + 4$ rows, so each pivot costs $\Theta(n^2)$, and $k$ pivots cost $O(k n^2)$; with $s$ iterations the time is $O(s k n^2)$ on the [real RAM](/real-ram/), and the tableau needs $\Theta(n^2)$ space. Because the dimension is fixed at six, the program can be solved in $O(n)$ time by [Megiddo's method](/megiddo-fixed-dimension-lp/) or in expected $O(n)$ time by Seidel's, which gives $O(s n)$. In the tests, $s$ is a few dozen and $k$ is small.

For the exact problem, Agarwal, Aronov and Sharir give a polynomial algorithm of high degree for the minimum width cylindrical shell, and a faster algorithm within a constant factor. These are not used in practice for inspection.

## Properties

- **Local.** The result depends on the start. There is no global guarantee.
- **Safe.** Every reported width is the width of a true zone, so it is an upper bound of $C$, and it is never worse than the start.
- **Not exact.** The answer is a floating point local optimum, with a tolerance on the box and the simplex.
- **Invariant.** The method is invariant under rigid motions of the data, up to the choice of the start and of the frame.

## Variants and improvements

- **Minimum circumscribed and maximum inscribed cylinders.** The same linearization with the objective $R$ alone, or $-r$ alone, gives the reference cylinders for a shaft and for a hole. Carr and Ferreira treat both.
- **Straightness of the median line.** Carr and Ferreira also evaluate the straightness of the axis of a cylinder, whose zone is a cylinder of the tolerance diameter.
- **Other local methods.** Nonlinear minimax solvers, pattern search over the four axis parameters, and smooth approximations of the maximum (for example a large power of the deviations) all give local optima. The safeguard of line L6 applies to any of them.
- **Exact and approximate algorithms.** The algorithm of Agarwal, Aronov and Sharir is exact. A grid of directions with an exact [minimum width annulus](/minimum-width-annulus/) for each projected set gives an upper bound with an error that shrinks with the grid step.
- **Roundness at several sections.** Measuring roundness at a few sections and straightness along a few lines is a cheaper check, but it is not cylindricity.

## When to use it

Use it to report cylindricity by the minimum zone, after a least-squares cylinder has given a start, on data of a few hundred to a few thousand points. Report the least-squares zone as well if the drawing asks for the Gaussian association. When the result must be certified as the global minimum, use an exact algorithm or a search over directions with a bound.

## Pitfalls

- **A poor start.** On a short part, the principal directions may not point along the axis. Start from the CAD axis or from a least-squares cylinder.
- **No box.** A full linear step can go far from where the linearization holds and increase the true width. Keep the trust box and the exact check.
- **Points on the axis.** The distance is not differentiable there. Real data seldom contain such points.
- **Equating local and global.** A local minimum can be reported as the cylindricity of the part only with a statement that it is an upper bound.
- **Scaling the tilt.** The tilt moves a point by its height times the angle. Without scaling the tilt box by the length of the part, the program favors tilts on long parts.

## Implementations

## History

Cylindricity was evaluated in early coordinate measuring machine software by least-squares cylinders, which overstate the minimum zone. Carr and Ferreira, in 1995, wrote the minimum zone, minimum circumscribed and maximum inscribed cylinders as sequences of linear programs, after their linear programming treatment of flatness and straightness in part I of the same work. In computational geometry the same problem is the minimum width cylindrical shell, which Agarwal, Aronov and Sharir solved exactly in polynomial time in 2001.

## References
