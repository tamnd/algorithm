---
tag: WJ3SQA
kind: algorithm
slug: explicit-midpoint-method
name: Midpoint method
aliases:
- modified Euler method
- RK2
- explicit midpoint rule
- Runge's midpoint method
area: numerical/differential-equations
level: intro
summary: "Take an Euler half step, then a full step with the slope at the midpoint. Two evaluations of f per step, order 2, stability function 1 + z + z^2/2."
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps, ⌈(T - t_0)/h⌉", d: "the dimension of y", C: "the cost of one evaluation of f"}
  time: {worst: "Θ(N (C + d))"}
  space: {extra: "Θ(d)"}
  evaluations: {worst: "2 N"}
properties: {deterministic: true, implicit: false, one_step: true, order: "2", a_stable: false, l_stable: false, symplectic: false}
history:
  year: 1895
  people: [Carl Runge]
  note: Runge proposed the method in 1895 as an extension of the midpoint quadrature rule to differential equations, the start of the Runge-Kutta methods.
prereqs: [euler-method, runge-kutta-methods, butcher-tableau]
see_also: [heuns-method, classical-runge-kutta-4, butcher-order-conditions, midpoint-rule, global-error, stability-region, verlet-integration, bulirsch-stoer-method]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.1 (Runge's midpoint method of 1895 and the first Runge-Kutta methods), Section II.2 (order conditions), Section II.3 (convergence of one-step methods)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 2, Section 23 (Runge-Kutta methods, the methods of order 2)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 3 (Runge-Kutta methods, explicit schemes of order 2)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 5 (two-stage Runge-Kutta methods and their truncation error), Chapter 7 (stability regions of Runge-Kutta methods)
  - paper: doi:10.1007/BF01446807
    title: Carl Runge, Über die numerische Auflösung von Differentialgleichungen, Mathematische Annalen 46 (1895) 167-178
    locator: the midpoint and trapezoidal extensions of quadrature rules
---

The explicit midpoint method solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, by taking an [Euler](/euler-method/) step of half length to estimate the solution at the middle of the step, and then a full step with the slope there:

$$k_1 = f(t_n, y_n), \qquad k_2 = f\left(t_n + \tfrac{h}{2},\; y_n + \tfrac{h}{2} k_1\right), \qquad y_{n+1} = y_n + h k_2.$$

It is the two-stage explicit [Runge-Kutta method](/runge-kutta-methods/) with [Butcher tableau](/butcher-tableau/) $c = (0, \tfrac12)$, $a_{21} = \tfrac12$, $b = (0, 1)$. It costs two evaluations of $f$ per step and has order $p = 2$: the [global error](/global-error/) is $O(h^2)$ when $f$ is $C^2$ with bounded second derivatives.

## In plain words

Euler's method uses the direction at the start of a step for the whole step. If the curve bends, that direction is wrong by the end of the step. The midpoint method first takes a trial half step in the start direction. It then asks the equation for the direction at that halfway point. That direction is a much better average of the directions along the whole step. The method throws away the trial half step and makes the full step from the start in the halfway direction.

This costs two looks at the equation per step instead of one. In return the error at the end shrinks four times when the step is halved, not two times.

## The problem

Given $f$, $t_0$, $y_0 \in \mathbb{R}^d$, an end time $T \ge t_0$ and a step size $h > 0$, approximate $y(T)$ for the solution of $y' = f(t, y)$, $y(t_0) = y_0$. Here $f$ is continuous and Lipschitz in $y$ with constant $L$ (so the solution is unique), and for order 2 we also need $f \in C^2$ with bounded second derivatives near the solution. The cost is the number of evaluations of $f$.

## The algorithm

```pseudo id=main
MIDPOINT(f, t0, y0, T, h)
L1  N ← ⌈(T − t0)/h − δ⌉                    ▷ δ: a relative slack of 10^-9, 0 in exact arithmetic
L2  t ← t0, y ← y0
L3  for n ← 0 to N − 1 do
L4      t_next ← T if n = N − 1 else t0 + (n + 1) h,  s ← t_next − t
L5      k1 ← f(t, y)
L6      k2 ← f(t + s/2, y + (s/2) k1)           ▷ the slope at the estimated midpoint
L7      y ← y + s k2
L8      t ← t_next
L9  return (t, y)
```

Lines L1, L2, L4 and L8 build the grid $t_n = t_0 + nh$ as in [Euler's method](/euler-method/): the last step is shortened to end at $T$, a step larger than the interval becomes one step to $T$, and $T = t_0$ gives $N = 0$ and no evaluation. Line L5 is the slope at the start. Line L6 evaluates $f$ at the end of an Euler half step. Line L7 discards that half step and moves the full step length from $y_n$ with the slope $k_2$.

When $f$ does not depend on $y$, the problem is the integral $\int_{t_0}^{T} f(t)\, dt$, and the method is the composite [midpoint rule](/midpoint-rule/) of quadrature.

## Example

Take $y' = -2 t y^2$, $y(0) = 1$, with solution $y(t) = 1/(1 + t^2)$, and $h = 0.2$ up to $T = 1$.

| $n$ | $t_n$ | $k_1$ | $k_2$ | $y_{n+1}$ | $y(t_{n+1})$ | $e_{n+1}$ |
|---|---|---|---|---|---|---|
| 0 | 0.0 | 0.000000 | -0.200000 | 0.960000 | 0.961538 | 0.001538 |
| 1 | 0.2 | -0.368640 | -0.511308 | 0.857738 | 0.862069 | 0.004331 |
| 2 | 0.4 | -0.588572 | -0.638211 | 0.730096 | 0.735294 | 0.005198 |
| 3 | 0.6 | -0.639648 | -0.621223 | 0.605852 | 0.609756 | 0.003905 |
| 4 | 0.8 | -0.587290 | -0.538818 | 0.498088 | 0.500000 | 0.001912 |

In the first step $k_1 = f(0, 1) = 0$, so the trial midpoint is $(0.1, 1)$ and $k_2 = -2 \cdot 0.1 \cdot 1 = -0.2$. The value $y_1 = 1 - 0.2 \cdot 0.2 = 0.96$ is much closer to $y(0.2) = 0.961538$ than the Euler value $1$. With the same 5 steps, the error at $T = 1$ is $1.9 \cdot 10^{-3}$, against $7.1 \cdot 10^{-3}$ for Euler's method, for twice the evaluations.

Halving $h$ shows order 2. For $h = 0.1, 0.05, 0.025, 0.0125, 0.00625$ the errors at $T = 1$ are $3.62 \cdot 10^{-4}$, $7.98 \cdot 10^{-5}$, $1.88 \cdot 10^{-5}$, $4.57 \cdot 10^{-6}$, $1.13 \cdot 10^{-6}$. The observed orders $\log_2$ of the ratios are $2.18$, $2.09$, $2.04$, $2.02$.

On $y' = -50y$ the step factor is $R(-50h)$. For $h = 0.05$, $R(-2.5) = 1.625$ and $y_{20} \approx 1.65 \cdot 10^4$. For $h = 0.04$, $R(-2) = 1$ exactly, the edge of stability. For $h = 0.025$, $R(-1.25) = 0.53125$ and the solution decays.

## Correctness

The loop computes $y_{n+1} = y_n + h_n \Phi(t_n, y_n, h_n)$ with the increment $\Phi(t, y, h) = f(t + h/2, y + (h/2) f(t, y))$, by induction on $n$. Convergence follows the pattern of all one-step methods. The increment is Lipschitz in $y$ with constant $\Lambda = L(1 + hL/2)$. When $f \in C^2$ with bounded second derivatives, a Taylor expansion of $\Phi$ in $h$ gives $h\Phi = h y' + \tfrac12 h^2 y'' + O(h^3)$, which matches the expansion of the exact solution, so the [local truncation error](/local-truncation-error/) is $O(h^3)$. The same [Gronwall](/gronwall-inequality/)-type induction as for Euler then gives the proved bound

$$\|y(t_n) - y_n\| \le \frac{K h^2}{\Lambda}\left(e^{\Lambda (t_n - t_0)} - 1\right).$$

The order is exactly 2: the order conditions of order 2, $\sum b_i = 1$ and $\sum b_i c_i = \tfrac12$, hold, but the two of order 3, $\sum b_i c_i^2 = \tfrac13$ and $\sum b_i a_{ij} c_j = \tfrac16$, give $\tfrac14$ and $0$ (see [Butcher order conditions](/butcher-order-conditions/)). The full proof is below.

## Complexity

Each of the $N$ steps makes two evaluations of $f$ (lines L5 and L6) and $O(d)$ arithmetic for the two vector updates. The time is $\Theta(N(C + d))$ in the [real RAM](/real-ram/) model and the count of evaluations is exactly $2N$. The extra space is $\Theta(d)$: $y$, $k_1$, $k_2$ and the trial point. For a target error $\varepsilon$ the method needs $N = \Theta(\varepsilon^{-1/2})$ steps on a smooth problem, against $\Theta(\varepsilon^{-1})$ for Euler, so it wins over Euler when $\varepsilon$ is small, although each step costs twice as much.

## Properties

- **Order 2, two stages.** Every explicit two-stage method of order 2 has $b_1 + b_2 = 1$ and $b_2 c_2 = \tfrac12$. The midpoint method is $c_2 = \tfrac12$; [Heun's method](/heuns-method/) is $c_2 = 1$.
- **Stability function $R(z) = 1 + z + \tfrac12 z^2$.** This is the same for all two-stage explicit methods of order 2. The real stability interval is $[-2, 0]$. The [stability region](/stability-region/) touches the imaginary axis only at $0$: $|R(iy)|^2 = 1 + y^4/4 > 1$ for $y \ne 0$.
- **Energy drift.** On the harmonic oscillator each step multiplies $y_1^2 + y_2^2$ by exactly $1 + h^4/4$. The drift is slower than for Euler ($1 + h^2$) but the orbit still spirals out.
- **Explicit.** No equation is solved. It is not A-stable, so it is not suited for [stiff problems](/stiff-ode-problem/).

## Variants and improvements

- **[Heun's method](/heuns-method/).** Average the slopes at both ends: $y_{n+1} = y_n + \tfrac{h}{2}(k_1 + f(t_n + h, y_n + h k_1))$. Same order, same stability function, different error constant.
- **Implicit midpoint rule.** $y_{n+1} = y_n + h f(t_n + h/2, (y_n + y_{n+1})/2)$. This is the one-stage [Gauss-Legendre method](/gauss-legendre-runge-kutta/): order 2, A-stable and symplectic.
- **Gragg's modified midpoint rule.** A two-step leapfrog recurrence with a smoothing final step; its error has an expansion in even powers of $h$, which the [Bulirsch-Stoer method](/bulirsch-stoer-method/) extrapolates.
- **Higher order.** More stages give the [classical Runge-Kutta method](/classical-runge-kutta-4/) of order 4 and the pairs used with step control, such as [Dormand-Prince](/dormand-prince-method/).

## When to use it

Use the midpoint method when an explicit method is required, the problem is not stiff, and moderate accuracy is enough, for example in a real-time simulation with a fixed time step. Against Euler it gives order 2 for twice the cost per step. For tight tolerances use an adaptive pair of order 4 or 5. For long simulations of Hamiltonian systems, use a [symplectic integrator](/symplectic-integrators/) such as the [Verlet method](/verlet-integration/), whose energy error stays bounded.

## Pitfalls

- **Confusing it with the two-step midpoint rule.** The leapfrog recurrence $y_{n+1} = y_{n-1} + 2h f(t_n, y_n)$ is a different method, a [linear multistep method](/linear-multistep-methods/), and it is weakly unstable on decaying problems. Line L7 starts from $y_n$, not from $y_{n-1}$.
- **Moving from the trial point.** Writing $y \leftarrow (y + (s/2)k_1) + s k_2$ in line L7, or keeping the half-step value, gives an inconsistent method. The full step starts from $y_n$.
- **The wrong time in line L6.** Evaluating $k_2$ at $t$ instead of $t + s/2$ drops the order to 1 when $f$ depends on $t$, and the error shows only on non-autonomous problems.
- **The name.** Some books call this method "modified Euler" and others use that name for Heun's method. Check the formula, not the name.

## Implementations

## History

Runge (1895) proposed the method as the analogue of the midpoint quadrature rule for differential equations, together with a trapezoid-like variant. Heun (1900) and Kutta (1901) extended the idea to more stages and higher order, and the family became the [Runge-Kutta methods](/runge-kutta-methods/) (HNW I, Section II.1).

## References
