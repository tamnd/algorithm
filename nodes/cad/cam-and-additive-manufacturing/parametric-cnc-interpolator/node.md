---
tag: QFCNX0
kind: algorithm
slug: parametric-cnc-interpolator
name: Parametric curve interpolator for CNC
aliases:
- NURBS interpolator
- real-time parametric interpolation
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Computes the next curve parameter each servo period by a Taylor expansion in arc length, so the tool follows a spline at the planned feed, after Shpitalni, Koren and Lo.
model: real-ram
complexity:
  vars: {n: number of interpolation periods, p: degree of the curve}
  time: {worst: "O(n p^2)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, recursive: false}
history:
  year: 1994
  people: [Moshe Shpitalni, Yoram Koren, C. C. Lo]
  note: Shpitalni, Koren and Lo gave real-time interpolators that take the curve itself from CAD instead of many short lines, with the parameter step from a Taylor expansion.
prereqs: [arc-length-parametrization, nurbs, cutter-location-data]
see_also: [pythagorean-hodograph-curve, feedrate-scheduling, time-scaling, b-spline, trapezoidal-velocity-profile, toolpath-planning]
sources:
  - paper: doi:10.1016/0010-4485(94)90097-3
    title: M. Shpitalni, Y. Koren and C. C. Lo, Realtime curve interpolators, Computer-Aided Design 26(11), 832-838, 1994
    locator: the interpolation of parametric curves in real time, with the parameter step from the first and second derivatives of the curve
  - paper: doi:10.1016/0167-8396(95)00047-X
    title: Rida T. Farouki and Sagar Shah, Real-time CNC interpolators for Pythagorean-hodograph curves, Computer Aided Geometric Design 13(7), 583-600, 1996
    locator: the exact arc length of PH curves and the interpolator that solves the polynomial arc length equation in each period
  - paper: doi:10.1016/S0010-4485(01)00082-3
    title: Syh-Shiuh Yeh and Pau-Lo Hsu, Adaptive-feedrate interpolation for parametric curves with a confined chord error, Computer-Aided Design 34(3), 229-237, 2002
    locator: the feed limit from the chord error and its use in the Taylor interpolator
---

A parametric curve interpolator is the part of a CNC controller that turns a curved toolpath into the positions that the drives must reach at each tick of the servo clock. The path is a spline, such as a [NURBS](/nurbs/) curve $C(u)$, and the [feed schedule](/feedrate-scheduling/) says how fast the tool must move. In each period $\tau$ the tool must advance the arc length $L = V\tau$ along the curve. The difficulty is that the parameter $u$ is not the arc length, so a fixed step in $u$ gives an uneven speed, and the exact parameter for a given arc length needs the inverse of an integral. The interpolator of Shpitalni, Koren and Lo uses a Taylor expansion of $u$ as a function of arc length instead. The second-order step is
$$
\Delta u = \frac{L}{|C'|} - \frac{L^2\, (C' \cdot C'')}{2|C'|^4},
$$
and the arc length that it really covers differs from $L$ by $O(L^3)$, a relative feed error of order $(V\tau)^2$. For a [Pythagorean hodograph curve](/pythagorean-hodograph-curve/) the arc length is a polynomial, so the step can be checked, or computed, exactly.

## In plain words

A machine controller wakes up many times a second, and each time it must say where the tool should be next. On a straight line this is easy. On a smooth curve the curve is drawn by a number $u$ that runs from start to end, but equal steps of $u$ do not give equal steps along the curve. The tool would speed up and slow down.

The interpolator asks how fast the curve moves when $u$ changes, and divides the wanted distance by that speed. This first guess is a little off where the curve speeds up or slows down, so a second term corrects for that change. With the correction, the error of each step is tiny, and halving the step makes the error eight times smaller.

## The problem

Given a regular parametric curve $C(u)$, $u \in [u_0, u_1]$, with the derivatives $C'$ and $C''$, a feed $V$ and a period $\tau$, find parameters $u_0 < u_1' < u_2' < \dots$ such that the arc length from each to the next is $L = V\tau$, as closely as possible, with a fixed and small amount of work per period. The arc length $s(u) = \int |C'|$ has no closed form for most splines, so the exact answer, the inverse of $s$ at $s(u_k) + L$, is too slow to compute by quadrature and root finding in each period of a millisecond or less. This is the inverse problem of [arc length parametrization](/arc-length-parametrization/), solved approximately and in real time.

## The algorithm

```pseudo id=main
PARAMETRIC-INTERPOLATOR(C', C'', u_start, u_end, V, τ)
L1  L ← V τ                                     ▷ the arc length per period
L2  u ← u_start;  params ← [u]
L3  while u < u_end
L4      d₁ ← C'(u);  d₂ ← C''(u);  σ ← |d₁|
L5      Δu ← L/σ − L² (d₁ · d₂) / (2 σ⁴)          ▷ Taylor expansion of u(s) to second order
L6      u ← min(u + Δu, u_end)
L7      append u to params                       ▷ the drives move to C(u)
L8  return params
```

Line L5 is the Taylor polynomial of degree 2 of $u(s + L) - u(s)$. The derivatives of the inverse of $s(u)$ are $du/ds = 1/|C'|$ and $d^2u/ds^2 = -(C' \cdot C'')/|C'|^4$. The first-order interpolator drops the second term. In a real controller $V$ changes from period to period, as the feed schedule says, and $L$ is computed in each pass.

## Example

Take the PH cubic $C(t) = (t - t^3/3,\ t^2)$. Its speed is $|C'| = 1 + t^2$ and its arc length is $s(t) = t + t^3/3$. Here $C' \cdot C'' = 2t(1 + t^2)$, so line L5 gives
$$
\Delta u = \frac{L}{1 + t^2} - \frac{L^2\, t}{(1 + t^2)^3}.
$$
With $L = 0.1$ and the start $t = 1$, the first steps are:

| $k$ | $u_k$ | first-order $\Delta u$ | second-order $\Delta u$ | first-order error $\Delta S - L$ | second-order error $\Delta S - L$ |
|---|---|---|---|---|---|
| 0 | 1.000000 | 0.050000 | 0.048750 | $+2.54 \times 10^{-3}$ | $-8.48 \times 10^{-5}$ |
| 1 | 1.048750 | 0.047622 | 0.046489 | $+2.41 \times 10^{-3}$ | $-7.83 \times 10^{-5}$ |
| 2 | 1.095239 | 0.045464 | 0.044435 | $+2.30 \times 10^{-3}$ | $-7.21 \times 10^{-5}$ |
| 3 | 1.139674 | 0.043500 | 0.042562 | $+2.18 \times 10^{-3}$ | $-6.63 \times 10^{-5}$ |

The errors are measured with the exact arc length. At $t = 1$ the first-order error is $L^2/4 + L^3/24$ exactly, and the second-order error is close to $-L^3/12 = -8.33 \times 10^{-5}$. Over the whole curve from $t = 0$ to $t = 2$, the largest relative errors per step are:

| $L$ | first order, PH cubic | second order, PH cubic | first order, parabola | second order, parabola |
|---|---|---|---|---|
| 0.02 | $6.55 \times 10^{-3}$ | $1.33 \times 10^{-4}$ | $7.78 \times 10^{-3}$ | $2.67 \times 10^{-4}$ |
| 0.01 | $3.26 \times 10^{-3}$ | $3.33 \times 10^{-5}$ | $3.87 \times 10^{-3}$ | $6.67 \times 10^{-5}$ |
| 0.005 | $1.63 \times 10^{-3}$ | $8.33 \times 10^{-6}$ | $1.93 \times 10^{-3}$ | $1.67 \times 10^{-5}$ |

Halving $L$ halves the first-order error and divides the second-order error by four, as the theorem says. On the parabola $(t, t^2)$, which is not a PH curve, the reference is the closed form $s(t) = \tfrac12 t\sqrt{1 + 4t^2} + \tfrac14 \operatorname{asinh}(2t)$.

## Correctness

**Theorem.** Let $C$ be three times continuously differentiable and regular. Then each step of the second-order interpolator covers an arc length $\Delta S$ with
$$
|\Delta S - L| \le \frac{M_1 M_3}{6} L^3,
$$
where $M_1$ bounds $|C'|$ and $M_3$ bounds $|d^3u/ds^3|$. So the relative feedrate error is $O((V\tau)^2)$. The first-order step has $|\Delta S - L| \le \tfrac12 M_1 M_2 L^2$, a relative error $O(V\tau)$.

The proof is in the proof file. Line L5 is the Taylor polynomial of $u(s_k + L) - u(s_k)$, so the parameter misses the exact one by the remainder $\tfrac16 L^3 u'''(\xi)$, and the arc length misses $L$ by at most $M_1$ times that. The orders are sharp: $(\Delta S - L)/L^3$ tends to $-|C'| u'''/6$, which for the PH cubic is $(1 - 5t^2)/(3(1 + t^2)^4)$. The tests check this limit, and the exact errors $L^3/3$ at $t = 0$ and $L^2/4 + L^3/24$ at $t = 1$, in rational arithmetic. They check the orders and the bound on the parabola against the exact arc length, and they compare the parameters with a reference that inverts the exact arc length by bisection.

## Complexity

Each period evaluates $C'$ and $C''$ once and does $O(1)$ more arithmetic. For a NURBS curve of degree $p$ the derivatives cost $O(p^2)$ with the de Boor recurrences, so $n$ periods take $O(n p^2)$ time and $O(1)$ extra space. The work per period is fixed, which is what a real-time controller needs. The exact method, quadrature and Newton steps on $s(u)$, has no fixed bound on its work.

## Properties

- **Second order.** The relative feed error per step is $O((V\tau)^2)$, against $O(V\tau)$ for the first-order step.
- **Fixed work per period.** Two derivative evaluations and a few operations.
- **Accumulating error.** The step errors add up. After $n$ steps the position along the curve can drift by $n$ times the step bound, which is of order $L^2$ times the path length.
- **No chord control.** The tool moves along chords between the computed points, and the chord is shorter than the arc by about $\kappa^2 L^3/24$, so a separate feed limit is needed on tight curves.
- **Exact on PH curves when solved exactly.** For a PH curve, $s(u)$ is a polynomial, and a few Newton steps on it give the exact parameter.

## Variants and improvements

- **First-order interpolator.** $\Delta u = L/|C'|$ only. It is simpler and has the relative error $O(V\tau)$.
- **Higher order and predictor-corrector.** More Taylor terms, or one Newton correction on an approximate arc length, reduce the feed error further.
- **PH curve interpolators.** Farouki and Shah used the polynomial arc length of [PH curves](/pythagorean-hodograph-curve/) to solve $s(u) = s(u_k) + L$ by Newton steps, with no truncation error in the feed.
- **Adaptive feed with a chord limit.** Yeh and Hsu lower $V$ where the chord error $\rho - \sqrt{\rho^2 - L^2/4}$ on the circle of curvature would exceed a tolerance. This is one of the speed limits of [feedrate scheduling](/feedrate-scheduling/).
- **Feed correction polynomials.** Some interpolators fit a polynomial to $u(s)$ before the run, from the exact arc length, and evaluate it in real time.

## When to use it

Use a parametric interpolator when the CAM system can send splines to the controller, as in high-speed milling of molds, dies and aircraft parts. It replaces many short lines, which give a jerky motion and large programs, by a smooth curve followed at the planned feed. The second-order step is the usual choice. Use the exact PH method when the path is a PH curve.

## Pitfalls

- **Singular points.** Where $C' = 0$, the step is not defined. Splines with repeated control points or cusps must be repaired before interpolation.
- **Long periods on tight curves.** If $L$ is not small compared with the radius of curvature and the scale on which $|C'|$ changes, the second term can be larger than the first, and the step can even be negative. The implementation stops with an error then.
- **Drift.** The small step errors add up over a long path. Controllers that must end exactly at a point correct the last steps.
- **The feed is along the chords.** The interpolator controls the arc length of each step, but the drives follow straight chords. Both errors are of order $L^2$ relative to $L$.
- **Feed changes.** The expansion assumes a constant $V$ in the period. With acceleration, a term in $\dot V$ is added, or $V$ is taken at the middle of the period.

## Implementations

## History

Early CNC controllers could only follow lines and circular arcs, and CAM systems broke curves into many short lines. Shpitalni, Koren and Lo (1994) showed how a controller can follow a parametric curve directly, with the parameter step in each period from the first and second derivatives of the curve. Farouki and Shah (1996) gave interpolators for Pythagorean hodograph curves, whose arc length is a polynomial, and Yeh and Hsu (2002) added a feed limit from the chord error. Commercial controllers added NURBS interpolation in the late 1990s and the 2000s.

## References
