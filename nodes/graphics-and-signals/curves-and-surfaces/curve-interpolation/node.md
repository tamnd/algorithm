---
tag: 6MKG7Q
kind: problem
slug: curve-interpolation
name: Curve interpolation
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: Find a parametric curve of a given kind that passes through a given sequence of points. A parameter value must be chosen for each point, and that choice changes the shape.
model: real-ram
complexity:
  vars: {m: "the number of data points, minus one", d: "the dimension, with the degree fixed"}
  time: {worst: Θ(m d)}
prereqs: [parametric-curve, hermite-spline]
see_also: [natural-cubic-spline, catmull-rom-spline, kochanek-bartels-spline, b-spline-fitting, schoenberg-whitney-theorem, interpolation-problem, cubic-spline-interpolation, four-point-scheme]
sources:
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 9.2, Global Interpolation (Section 9.2.1, Global Curve Interpolation to Point Data, page 364, and Section 9.2.3, Cubic Spline Curve Interpolation), and Section 9.3, Local Interpolation
  - paper: doi:10.1016/0010-4485(89)90003-1
    title: E. T. Y. Lee, Choosing nodes in parametric curve interpolation, Computer-Aided Design 21(6), 363-370 (1989)
    locator: the uniform, chord-length and centripetal parameters, and the exponent family
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 9, Constructing Spline Curves (spline interpolation of points, end conditions and parametrization)
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XIII, Spline interpolation (the Schoenberg-Whitney theorem and the banded totally positive system)
---

Curve interpolation is the problem of finding a [parametric curve](/parametric-curve/) that passes through given points $Q_0, \dots, Q_m$ in the plane or in space, in that order. The answer depends on two choices that the data do not fix: the kind of curve (one polynomial, a $C^1$ or $C^2$ cubic spline, a B-spline of degree $p$) and the parameter value $t_k$ at which the curve reaches $Q_k$. Once both are fixed, the problem is linear: it splits into $d$ function interpolation problems, one per coordinate, with the same matrix. The parameter choice is the step specific to curves. The same points with uniform, chord-length or centripetal parameters give visibly different curves. The function case, with given abscissas $x_k$ and values $y_k$, is the [interpolation problem](/interpolation-problem/) of numerical analysis.

## In plain words

You click a few points on the screen and you want a smooth curve through all of them, in the order you clicked. There are many such curves. To pick one, you first decide what kind of curve you allow, for example pieces of cubics joined smoothly. Then you decide at what "time" the curve reaches each point.

The time matters. If the points are far apart in one place and close together in another, but the curve must reach each one after the same time, it rushes over the long gaps and crawls over the short ones. A curve made of cubics that moves like that swings wide and can make loops. If the time between two points grows with their distance, the curve stays calmer.

## Definition

**Input.**

- Points $Q_0, \dots, Q_m \in \mathbb{R}^d$, with $Q_k \ne Q_{k+1}$.
- A space $S$ of curves, for example cubic splines with given knots, or B-spline curves of degree $p$ with $m + 1$ control points.
- Optionally, derivative data (tangent vectors at some points) and end conditions.

**Output.** Parameters $t_0 < t_1 < \dots < t_m$ and a curve $C \in S$ with

$$C(t_k) = Q_k, \qquad k = 0, \dots, m,$$

and the derivative conditions if they are given.

**Parameter rules.** The parameters are usually set by a rule of the form $t_0 = 0$ and

$$t_{k+1} - t_k = \lVert Q_{k+1} - Q_k \rVert^{e},$$

often normalized to $[0, 1]$. The exponent $e = 0$ gives *uniform* parameters, $e = 1$ *chord-length* parameters, and $e = 1/2$ *centripetal* parameters (Lee 1989). Lee proposed the centripetal rule by analogy with the centripetal force on a point that moves along the curve. For the [Catmull-Rom spline](/catmull-rom-spline/) the centripetal rule is proved to avoid cusps and self-intersections inside a segment.

**The linear system.** If $S$ has a basis $\phi_0, \dots, \phi_m$, write $C = \sum_i \phi_i P_i$ with unknown coefficients $P_i \in \mathbb{R}^d$. The conditions are $\sum_i \phi_i(t_k) P_i = Q_k$, a square system $\Phi \mathbf{P} = \mathbf{Q}$ with $\Phi_{ki} = \phi_i(t_k)$, the same for each coordinate. For B-splines of degree $p$ the [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/) says that $\Phi$ is nonsingular if and only if $\phi_k(t_k) \ne 0$ for every $k$, so a unique solution exists exactly then. $\Phi$ is banded with at most $p + 1$ nonzeros per row.

## Variants

- *Global or local.* A global method (natural spline, B-spline interpolation) solves one system, and each point affects the whole curve. A local method ([Catmull-Rom](/catmull-rom-spline/), [Kochanek-Bartels](/kochanek-bartels-spline/), Piegl and Tiller's local interpolation in Section 9.3) builds each segment from a few neighbouring points, with no system and with lower smoothness ($C^1$ or $G^1$).
- *With derivatives.* Tangents given at the points give the [Hermite spline](/hermite-spline/), a local problem with an explicit answer. This is curve [Hermite interpolation](/hermite-interpolation/).
- *End conditions.* For cubic splines: natural ($C'' = 0$), clamped (given end tangents), not-a-knot, or periodic for closed curves.
- *Closed curves.* $Q_m = Q_0$ with periodic conditions; the matrix becomes cyclic banded.
- *Shape preserving.* Ask the curve to keep the convexity or the monotone direction of the data polygon. Cubic splines with fixed parameters do not do this in general.
- *Subdivision.* Interpolatory subdivision, such as the [four-point scheme](/four-point-scheme/), inserts new points between old ones at each step and defines the curve as the limit.
- *Approximation instead of interpolation.* For noisy or dense data the curve should pass near the points, not through them: see [B-spline fitting](/b-spline-fitting/).

## Examples

**Three parameter rules for the same points.** Take $Q_0 = (0, 0)$, $Q_1 = (3, 4)$, $Q_2 = (4, 4)$, $Q_3 = (4, 0)$, with chord lengths 5, 1 and 4. The normalized parameters are:

| rule | $t_0$ | $t_1$ | $t_2$ | $t_3$ |
|---|---|---|---|---|
| uniform ($e = 0$) | 0 | 0.3333 | 0.6667 | 1 |
| centripetal ($e = 1/2$) | 0 | 0.4271 | 0.6180 | 1 |
| chord length ($e = 1$) | 0 | 0.5 | 0.6 | 1 |

The [natural cubic spline](/natural-cubic-spline/) through the points with each rule, sampled at 20001 parameter values, gives:

| rule | largest $y$ | largest $x$ | length |
|---|---|---|---|
| uniform | 4.600 | 4.051 | 10.672 |
| centripetal | 4.197 | 4.250 | 10.191 |
| chord length | 4.057 | 4.642 | 10.610 |

The data polygon has $y \le 4$, $x \le 4$ and length 10. Uniform parameters give the short edge from $Q_1$ to $Q_2$ as much time as the long ones, and the curve bulges $0.6$ above it. Chord-length parameters give that edge little time, and the curve swings $0.64$ out past the corner at $Q_2$. The centripetal curve lies between the two and is the shortest.

**A unique B-spline interpolant.** For cubic B-splines with $m + 1$ control points, Piegl and Tiller take clamped knots and place each inner knot at the average of $p$ consecutive parameters, $u_{j+p} = \frac1p \sum_{i=j}^{j+p-1} t_i$ for $j = 1, \dots, m - p$. With this choice every condition $\phi_k(t_k) \ne 0$ of the Schoenberg-Whitney theorem holds, so the interpolant exists and is unique, and the banded system can be solved by Gaussian elimination without pivoting (Section 9.2.1).

**Not solvable.** For degree 1 B-splines on the knots $(0, 0, \tfrac12, 1, 1)$ and the parameters $0, \tfrac18, \tfrac14$, the last basis function is zero at all three parameters. The condition fails, and no curve of the space passes through three general points at those parameters.

## Known algorithms

| method | smoothness | system | cost for $m + 1$ points |
|---|---|---|---|
| [Hermite spline](/hermite-spline/) with given tangents | $C^1$ | none | $O(md)$ |
| [Catmull-Rom spline](/catmull-rom-spline/) | $C^1$ | none | $O(md)$ |
| [Kochanek-Bartels spline](/kochanek-bartels-spline/) | $C^1$, or $C^0$ by choice | none | $O(md)$ |
| [Natural cubic spline](/natural-cubic-spline/) | $C^2$ | tridiagonal, by the [Thomas algorithm](/thomas-algorithm/) | $O(md)$ |
| B-spline interpolation of degree $p$ (Piegl and Tiller 9.2.1) | $C^{p-1}$ | band $p$ | $O(mp^2 + mpd)$ |
| one polynomial of degree $m$ ([Lagrange interpolation](/lagrange-interpolation/)) | $C^\infty$ | dense, or barycentric | $O(m^2 d)$ |

A single polynomial of high degree through many points oscillates near the ends, as in the [Runge phenomenon](/runge-phenomenon/), so curve design uses splines.

## Bounds

In the real RAM model, any method must read the $(m + 1)d$ input coordinates and, for an explicit answer, write $\Theta(md)$ output coefficients, so $\Omega(md)$ time is needed. The spline methods of the table reach $O(md)$ for a fixed degree, which is optimal. The bound counts arithmetic operations. In floating point the global methods also need a well conditioned matrix: the natural spline matrix is strictly diagonally dominant, and the B-spline collocation matrix is totally positive, which keeps elimination without pivoting stable. There is no size bound on the overshoot of a cubic interpolant in terms of the data alone: with uniform parameters and one very short edge between long edges, the curve can loop.

## Reductions

- *To function interpolation.* With the parameters fixed, each coordinate $x_j(t)$ is a function interpolation problem with nodes $t_k$ and values $(Q_k)_j$, all with the same matrix, so curve interpolation is $d$ instances of the [interpolation problem](/interpolation-problem/) with one factorization. For cubic splines in one variable, see [cubic spline interpolation](/cubic-spline-interpolation/).
- *From function interpolation.* Interpolating a function $y = f(x)$ at increasing $x_k$ is the curve problem in the plane with $Q_k = (x_k, y_k)$ and the parameters $t_k = x_k$. For a spline space that contains the linear functions the $x$ coordinate is then reproduced exactly, $x(t) = t$.
- *To least squares.* Interpolation is the case of [B-spline fitting](/b-spline-fitting/) with as many control points as data points, when the Schoenberg-Whitney condition holds: the minimum of the sum of squares is then zero.

## Applications

- CAD: a curve through measured or designed points, then used to build surfaces by lofting or sweeping (see [sweep surface](/sweep-surface/)).
- Animation: a path through key positions of an object or a camera, usually with a local method and a reparametrization by [arc length](/arc-length-parametrization/) for constant speed.
- Drawing programs and fonts: a smooth stroke through sampled pen positions.
- Robotics and machining: a smooth tool path through way points, often with a $C^2$ spline so that the acceleration is continuous.

## References
