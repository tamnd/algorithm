---
tag: 5K31VD
kind: technique
slug: dense-output
name: Dense output
aliases:
- continuous extension
- interpolant
- continuous Runge-Kutta method
- dense output formula
area: numerical/differential-equations
level: advanced
summary: "Give the numerical solution at any time inside a step, not only at grid points, from data the step already computed: u(t_n + θh) = y_n + h Σ b_i(θ) k_i. Used for output, event location and delays."
prereqs: [runge-kutta-methods, butcher-order-conditions, hermite-interpolation]
see_also: [dormand-prince-method, embedded-runge-kutta-pairs, delay-differential-solver, collocation-method, bogacki-shampine-method, adaptive-step-size-control, delay-differential-equations, adams-bashforth-methods]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.6 (dense output, discontinuities, derivatives; continuous Runge-Kutta methods, Hermite interpolation, the dense output of DOPRI5), Section II.17 (use in delay equations)
  - paper: doi:10.1137/0722060
    title: L. F. Shampine, Interpolation for Runge-Kutta methods, SIAM Journal on Numerical Analysis 22(5) (1985) 1014-1027
    locator: interpolants built from the stages of a step, their order and cost
  - paper: doi:10.1137/0720036
    title: M. K. Horn, Fourth- and fifth-order, scaled Runge-Kutta algorithms for treating dense output, SIAM Journal on Numerical Analysis 20(3) (1983) 558-568
    locator: Runge-Kutta formulas with weights depending on the output point
  - book: isbn:9780198506546
    title: Alfredo Bellen and Marino Zennaro, Numerical Methods for Delay Differential Equations, Oxford University Press, 2003
    locator: Chapter 5 (continuous extensions of Runge-Kutta methods, uniform order)
---

Dense output is a way for a step-by-step ODE solver to return the numerical solution at any time inside a step, not only at the grid points $t_n$. After a step from $t_n$ to $t_{n+1} = t_n + h$, the solver builds a function $u(t_n + \theta h)$, $\theta \in [0, 1]$, from data it has already computed: the stages of a Runge-Kutta step, or the end values and slopes. A good dense output costs few or no extra evaluations of $f$, has an order close to that of the method, and lets the step size be chosen for accuracy alone instead of being cut to hit output times. It is needed for plotting, for locating events, and for [delay equations](/delay-differential-equations/), whose right-hand side needs the solution at past off-grid times.

## In plain words

A solver moves in jumps. With large jumps it is efficient, but the user may want the answer at many times in between, or may need to know exactly when something happens, such as a ball touching the ground. Shortening the jumps to land on each of those times would waste work. Instead, after each jump, the solver draws a smooth curve through what it already knows about that jump: where it started, where it ended, and how fast it was moving at both ends and in between. Reading values off this curve is almost free. If the curve is built well, it is about as accurate as the jumps themselves, so nothing is lost.

## When it applies

- A one-step or multistep method is used with steps much longer than the spacing of the requested output times, or with automatic step size control.
- The solution must be evaluated at times not known in advance: event location (roots of $g(t, y(t))$), stopping conditions, delays $y(t - \tau)$.
- The method keeps enough information per step: the stages $k_i$ for Runge-Kutta methods, past values for multistep methods, or $y$ and $f$ at both ends of the step.
- The cost model counts evaluations of $f$: an interpolant that needs extra stages is charged for them, and an interpolant built from existing stages is free.

## The template

**Notation.** IVP $y' = f(t, y)$, $y \in \mathbb{R}^d$; a step from $(t_n, y_n)$ with step $h$ and Butcher tableau $(A, b, c)$ with $s$ stages gives $k_i = f(t_n + c_ih, y_n + h\sum_j a_{ij}k_j)$ and $y_{n+1} = y_n + h\sum_i b_ik_i$; $f_n = f(t_n, y_n)$. A **continuous extension** is a set of polynomials $b_i(\theta)$ with $b_i(0) = 0$ and $b_i(1) = b_i$, and the dense output is

$$u(t_n + \theta h) = y_n + h\sum_{i=1}^{s^*}b_i(\theta)\,k_i, \qquad 0 \le \theta \le 1,$$

where $s^* \ge s$ allows extra stages. It has **uniform order** $q$ if $\|u(t_n + \theta h) - y^{(n)}(t_n + \theta h)\| = O(h^{q+1})$ uniformly in $\theta$, where $y^{(n)}$ is the exact solution through $(t_n, y_n)$. This holds when for each $\theta$ the weights $b_i(\theta)$ satisfy the [order conditions](/butcher-order-conditions/) up to order $q$ with the right-hand side $1/\gamma(\tau)$ replaced by $\theta^{\rho(\tau)}/\gamma(\tau)$, $\rho(\tau)$ the order of the tree $\tau$ (HNW I, Section II.6).

```pseudo id=main
DENSE-STEP(f, t_n, y_n, h, outputs, g)
L1  take one step: stages k_1..k_s, result y_(n+1); accept or reject it as usual
L2  if the step is rejected then return
L3  build the interpolant u(θ) on [0, 1] from y_n, k_1..k_s, y_(n+1)   ▷ hole: the interpolant
L4  for each requested time t* in (t_n, t_(n+1)] do
L5      θ ← (t* − t_n) / h
L6      emit (t*, u(θ))
L7  if g(t_n, y_n) and g(t_(n+1), y_(n+1)) differ in sign then
L8      find θ* in [0, 1] with g(t_n + θ* h, u(θ*)) = 0                   ▷ hole: root finder on a cheap function
L9      report the event at t_n + θ* h
L10 store (t_n, h, coefficients of u) if past values will be needed      ▷ for delay equations
```

The two holes are the interpolant (line L3) and the root finder (line L8). Line L8 calls only $u$, never $f$, so bisection or a secant method costs no evaluations of $f$. The global error of the dense output is the global error at $t_n$ propagated over a fraction of a step plus the local interpolation error, so a uniform order $q \ge p - 1$ gives output errors of order $\min(p, q + 1)$, the order of the method when $q = p - 1$.

## Classic examples

**Cubic Hermite interpolation.** From $y_n, y_{n+1}, f_n, f_{n+1}$:

$$u(\theta) = (1 - \theta)y_n + \theta y_{n+1} + \theta(\theta - 1)\big[(1 - 2\theta)(y_{n+1} - y_n) + (\theta - 1)hf_n + \theta hf_{n+1}\big]$$

(HNW I, Section II.6). It reproduces cubics exactly and has local error $O(h^4)$. For an FSAL method such as [Bogacki-Shampine](/bogacki-shampine-method/), $f_{n+1}$ is the first stage of the next step, so it is free; this is the dense output of `ode23` and of dde23. On $y' = -2ty^2$, $y(0) = 1$, solved to $t = 2$ with [classical RK4](/classical-runge-kutta-4/), the maximum errors at $\theta = \tfrac14, \tfrac12, \tfrac34$ in all steps are:

| $h$ | grid points | linear interpolation | cubic Hermite |
|---|---|---|---|
| 0.2 | $1.65 \cdot 10^{-5}$ | $9.33 \cdot 10^{-3}$ | $8.72 \cdot 10^{-5}$ |
| 0.1 | $9.68 \cdot 10^{-7}$ | $2.46 \cdot 10^{-3}$ | $6.03 \cdot 10^{-6}$ |
| 0.05 | $6.00 \cdot 10^{-8}$ | $6.22 \cdot 10^{-4}$ | $3.87 \cdot 10^{-7}$ |
| 0.025 | $3.73 \cdot 10^{-9}$ | $1.56 \cdot 10^{-4}$ | $2.44 \cdot 10^{-8}$ |

Linear interpolation is second order and ruins the fourth-order grid values; the Hermite cubic is fourth order (ratios 14.5, 15.6, 15.9), about 6 times less accurate than the grid values here.

**A continuous extension of RK4.** With $c = (0, \tfrac12, \tfrac12, 1)$ and the RK4 stages,

$$b_1(\theta) = \theta - \tfrac32\theta^2 + \tfrac23\theta^3, \quad b_2(\theta) = b_3(\theta) = \theta^2 - \tfrac23\theta^3, \quad b_4(\theta) = -\tfrac12\theta^2 + \tfrac23\theta^3.$$

In exact arithmetic $\sum_ib_i(\theta) = \theta$, $\sum_ib_i(\theta)c_i = \theta^2/2$, $\sum_ib_i(\theta)c_i^2 = \theta^3/3$ and $\sum_{i,j}b_i(\theta)a_{ij}c_j = \theta^3/6$, so it has uniform order 3 with no extra stage, and at $\theta = 1$ it gives $b = (\tfrac16, \tfrac13, \tfrac13, \tfrac16)$.

**[Dormand-Prince](/dormand-prince-method/) 5(4).** Shampine's interpolant uses the seven stages of an accepted step, including the FSAL stage, to give a continuous extension of uniform order 4 with no extra evaluation of $f$; this is the dense output of DOPRI5 and `ode45` (HNW I, Section II.6). Order 5 needs extra stages.

**[Collocation methods](/collocation-method/).** A collocation Runge-Kutta method is defined by a polynomial $u$ of degree $s$ that satisfies the ODE at the $s$ collocation points. That polynomial is a natural dense output of uniform order $s$, with no extra cost; this is what Radau IIA codes return.

**Multistep methods.** [Adams](/adams-bashforth-methods/) and BDF codes already represent the solution by an interpolation polynomial through past values; evaluating it at off-grid times is their dense output.

## Variations

- **Extra stages for higher uniform order.** Adding one to three stages raises the uniform order of an explicit pair to its discrete order; for Dormand-Prince 8(5,3) (DOP853) three extra stages give a dense output of order 7.
- **Derivative output.** Differentiating $u$ gives approximations of $y'$; for Hermite interpolation they agree with $f$ at both ends, so $u \in C^1$ across steps.
- **Continuity.** Any extension with $b_i(1) = b_i$ is continuous across steps; $C^1$ continuity needs $u'$ to match $f_{n+1}$ at $\theta = 1$, which Hermite interpolation gives and stage-based extensions in general do not.
- **Horn's scaled formulas** choose the weights per output point; Shampine's interpolants and the theory of continuous Runge-Kutta methods (Bellen and Zennaro 2003) describe the minimal number of stages for each uniform order.
- **Error control of the interpolant.** Codes for state-dependent delays control the defect $u' - f(t, u)$ of the dense output, not only the local error at the grid points.

## Pitfalls

- **Using linear interpolation between grid points.** It is second order whatever the method; the table shows it losing four digits against the grid values.
- **Evaluating outside $[0, 1]$.** Extrapolating the interpolant past $t_{n+1}$ is not covered by any error bound; for events, take the step first, then search.
- **Missing events.** A sign test at the step ends misses pairs of roots inside one step; codes check sign changes of the interpolated $g$ at several interior points or limit the step.
- **Dense output after a rejected step.** Only accepted steps define the interpolant; after a rejection the stages belong to a different $h$.
- **Interpolant order lower than needed.** For delay equations, the dense output enters the stages, so its uniform order limits the global order to $\min(p, q + 1)$.

## Exercises

1. Show that the Hermite cubic above satisfies $u(0) = y_n$, $u(1) = y_{n+1}$, $u'(0) = hf_n$ and $u'(1) = hf_{n+1}$ (derivatives with respect to $\theta$).
2. Check the four order conditions for the RK4 continuous extension in exact rational arithmetic, and show that no extension of RK4 without extra stages has uniform order 4.
3. For the explicit midpoint method, find $b_1(\theta), b_2(\theta)$ of degree 2 with uniform order 2, or show that none exists.
4. Locate the time when the solution of $y' = -2ty^2$, $y(0) = 1$, equals $\tfrac12$ by running RK4 with $h = 0.25$ and solving $u(\theta) = \tfrac12$ by bisection on the Hermite interpolant. Compare with the exact $t = 1$.

## References
