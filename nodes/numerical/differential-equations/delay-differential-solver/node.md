---
tag: J3P31B
kind: algorithm
slug: delay-differential-solver
name: Delay differential equation solvers
aliases:
- DDE solvers
- Runge-Kutta method for delay equations
- method of steps with dense output
area: numerical/differential-equations
level: research
summary: "Runge-Kutta steps for y'(t) = f(t, y(t), y(t - τ)) that read delayed values from a Hermite interpolant of the computed past and put derivative breakpoints on the grid. Order 4 with RK4."
solves: [delay-differential-equations]
model: real-ram
complexity:
  vars: {N: "the number of steps, at most (T - t_0)/H + K with H = min(h, τ_1, ..., τ_m)", K: "the number of breakpoints in (t_0, T], at most C(m + 4, 4)", m: "the number of delays", d: "the dimension of y", C: "the cost of one evaluation of f"}
  time: {worst: "Θ(N (C + m d + m log N))"}
  space: {extra: "Θ(N d)"}
  evaluations: {worst: "4 N + 1"}
properties: {deterministic: true, implicit: false, one_step: true, order: "4", dense_output: true, adaptive: false}
history:
  year: 1981
  people: [Hans Joachim Oberle, Hans Josef Pesch]
  note: The method of steps reduces a DDE to a chain of ODEs; Oberle and Pesch (1981) paired Runge-Kutta steps with Hermite interpolation of the past, and Neves (1975), Bellen and Zennaro (1980s) and Shampine and Thompson (dde23, 2001) made discontinuity tracking and continuous extensions the standard design.
prereqs: [delay-differential-equations, classical-runge-kutta-4, dense-output]
see_also: [hermite-interpolation, cubic-hermite-spline, bogacki-shampine-method, radau-iia-methods, global-error, gronwall-inequality, binary-search, stiff-ode-problem]
sources:
  - book: isbn:9780198506546
    title: Alfredo Bellen and Marino Zennaro, Numerical Methods for Delay Differential Equations, Oxford University Press, 2003
    locator: Chapter 2 (the method of steps and the propagation of discontinuities), Chapters 4 to 6 (continuous Runge-Kutta methods, convergence and order with an interpolant of uniform order q), Chapter 7 (the overlapping case, steps longer than the delay)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.17 (numerical solution of delay equations with dense output; discontinuities), Section II.6 (dense output and Hermite interpolation), Section II.3 (local and global error of Runge-Kutta methods)
  - paper: doi:10.1016/S0168-9274(00)00055-6
    title: L. F. Shampine and S. Thompson, Solving DDEs in MATLAB, Applied Numerical Mathematics 37 (2001) 441-458
    locator: the dde23 code; Bogacki-Shampine 3(2) pair, cubic Hermite history, discontinuity tracking for constant delays, steps longer than the delay
---

A delay differential equation solver integrates $y'(t) = f\big(t, y(t), y(t - \tau_1), \ldots, y(t - \tau_m)\big)$ from a given past $y = \varphi$ on $[t_0 - \tau, t_0]$. The version on this page uses the [classical Runge-Kutta method](/classical-runge-kutta-4/) and takes each delayed value either from $\varphi$ or from a cubic [Hermite interpolant](/hermite-interpolation/) of the steps already computed, the [dense output](/dense-output/) of the solution. It keeps two rules: no step is longer than the smallest delay, so every delayed value lies in the computed past and the method stays explicit, and the grid contains the points $t_0 + n_1\tau_1 + \cdots + n_m\tau_m$ where derivatives of the solution may jump. With both rules it keeps the order 4 it has on ODEs; without the second it drops to order 2 or less.

## In plain words

A delay equation says how fast something changes now in terms of what it was some time ago, like a population whose growth depends on last year's numbers. A solver walks forward in small steps, as for an ordinary equation. Whenever the rule asks for an old value, the solver looks it up in its own record of the past, drawing a smooth curve through the points it has already computed. Two cautions keep this accurate. Each step must be short enough that the old values it needs are already in the record. And the true solution has small kinks at fixed times (one delay after the start, two delays after, and so on), so the solver lands its steps exactly on those times instead of stepping over them.

## The problem

Given $f : [t_0, T] \times \mathbb{R}^d \times (\mathbb{R}^d)^m \to \mathbb{R}^d$, constant delays $\tau_1, \ldots, \tau_m > 0$ with $\tau = \max_j\tau_j$, and a history $\varphi : [t_0 - \tau, t_0] \to \mathbb{R}^d$, approximate the solution of the [delay differential equation](/delay-differential-equations/)

$$y'(t) = f\big(t, y(t), y(t - \tau_1), \ldots, y(t - \tau_m)\big) \quad (t_0 < t \le T), \qquad y(t) = \varphi(t) \quad (t_0 - \tau \le t \le t_0),$$

at $T$ and, through the dense output, at every $t \in [t_0, T]$. The derivative at $t_0$ is the right derivative $y'(t_0^+) = f(t_0, \varphi(t_0), \varphi(t_0 - \tau_1), \ldots)$, which in general differs from $\varphi'(t_0)$. The user gives a maximal step $h$.

## The algorithm

```pseudo id=main
DDE-RK4(f, φ, (τ_1, ..., τ_m), t0, T, h)
L1  B ← {t0} ∪ {t0 + n_1 τ_1 + ... + n_m τ_m < T : n_j ≥ 0, 1 ≤ Σ n_j ≤ 4} ∪ {T}, sorted as b_0 < ... < b_K
L2  H ← min(h, τ_1, ..., τ_m)                       ▷ steps never exceed a delay
L3  y ← φ(t0); F ← f(t0, y, Z(t0)); store (t0, y, F)
L4  for i ← 1 to K do
L5      n ← max(1, ⌈(b_i − b_(i−1))/H − δ⌉); k ← (b_i − b_(i−1))/n     ▷ δ = 10^-9 against rounding
L6      for r ← 1 to n do                             ▷ step from t = b_(i−1) + (r − 1)k to t + k
L7          z ← Z(t + k/2); K1 ← F; K2 ← f(t + k/2, y + (k/2)K1, z); K3 ← f(t + k/2, y + (k/2)K2, z)
L8          z' ← Z(t + k); K4 ← f(t + k, y + k K3, z')
L9          y ← y + (k/6)(K1 + 2K2 + 2K3 + K4)
L10         F ← f(t + k, y, z'); store (t + k, y, F)
L11 Z(s) = (Y(s − τ_1), ..., Y(s − τ_m)), where Y(u) = φ(u) if u ≤ t0, else the cubic Hermite
        interpolant of the stored (t_l, y_l, F_l), (t_(l+1), y_(l+1), F_(l+1)) with t_l < u ≤ t_(l+1)
L12 return y and the dense solution Y
```

Line L1 lists the breakpoints. A jump in $y'$ at $t_0$ (from $\varphi'(t_0) \ne y'(t_0^+)$) reappears, smoothed by one order, wherever the right side reads $y$ at a jump: a point reached from $t_0$ by $k$ delays can carry a jump in $y^{(k+1)}$. Points reached by up to 4 delays carry the jumps in $y', \ldots, y^{(5)}$, which are the ones that would spoil an order 4 method. Line L5 splits each interval between breakpoints into equal steps of length at most $H$, so the last step lands exactly on $b_i$ and no step straddles a breakpoint. Line L11 is a [binary search](/binary-search/) in the stored times followed by the Hermite formula with $\theta = (u - t_l)/k_l$:

$$Y(u) = (2\theta^3 - 3\theta^2 + 1)y_l + (\theta^3 - 2\theta^2 + \theta)k_lF_l + (3\theta^2 - 2\theta^3)y_{l+1} + (\theta^3 - \theta^2)k_lF_{l+1}.$$

Since $k \le H \le \tau_j$, every delayed time $s - \tau_j$ at lines L7, L8 and L10 is at most $t$, the start of the current step, so $Z$ only reads finished steps. The slope $F$ stored at line L10 is the derivative at the new point, which serves both as the Hermite slope and as $K_1$ of the next step, so a step costs four evaluations of $f$.

## Example

**By hand.** Take $y'(t) = -y(t - 1)$ with $\varphi = 1$ on $[-1, 0]$, $h = \tfrac12$, $T = 4$. The breakpoints are $0, 1, 2, 3, 4$, each interval gets two steps, and the exact solution, by the method of steps, is $y(t) = \sum_{k=0}^{n}(-1)^k(t - k + 1)^k/k!$ on $[n - 1, n]$.

- Step $[0, \tfrac12]$: all delayed times lie in $[-1, -\tfrac12]$, where $\varphi = 1$, so $K_1 = \cdots = K_4 = -1$ and $y(\tfrac12) = \tfrac12$.
- Step $[1, \tfrac32]$: $K_1 = F = -y(0) = -1$; at $t = \tfrac54$ the delayed time $\tfrac14$ lies in the first step, whose Hermite cubic through $(0, 1)$ and $(\tfrac12, \tfrac12)$ with slopes $-1, -1$ gives $Y(\tfrac14) = \tfrac34$, so $K_2 = K_3 = -\tfrac34$; $K_4 = -Y(\tfrac12) = -\tfrac12$. Then $y(\tfrac32) = 0 + \tfrac1{12}(-1 - \tfrac32 - \tfrac32 - \tfrac12) = -\tfrac38$.

In exact rational arithmetic the whole run gives

| $t$ | 1/2 | 1 | 3/2 | 2 | 5/2 | 3 | 7/2 | 4 |
|---|---|---|---|---|---|---|---|---|
| $y_n$ | 1/2 | 0 | $-3/8$ | $-1/2$ | $-19/48$ | $-1/6$ | 25/384 | 5/24 |

which is the exact solution at every grid point: on $[n - 1, n]$ the solution is a polynomial of degree $n$, the Hermite cubic reproduces it exactly while $n \le 3$, and RK4 integrates a right side of degree $\le 3$ in $t$ exactly. The run takes 8 steps, 33 evaluations of $f$ and 17 history lookups.

**Order 4 with breakpoints.** On $[0, 10]$ (float arithmetic), the maximum error over $t \in \{0, \tfrac18, \ldots, 10\}$ of the dense output is

| $h$ | 1/4 | 1/8 | 1/16 | 1/32 | 1/64 |
|---|---|---|---|---|---|
| max error | $1.101 \times 10^{-5}$ | $4.239 \times 10^{-7}$ | $2.649 \times 10^{-8}$ | $1.656 \times 10^{-9}$ | $1.035 \times 10^{-10}$ |
| ratio | | 26.0 | 16.0 | 16.0 | 16.0 |

**Order 2 without them.** On $[0, 3]$ with steps $h = 2/(2m + 1)$, so that the breakpoint $t = 1$ falls in the middle of a step, a uniform grid that ignores the breakpoints gives maximum errors $4.320 \times 10^{-4}, 1.017 \times 10^{-4}, 1.584 \times 10^{-5}, 3.622 \times 10^{-6}, 8.993 \times 10^{-7}$ for $m = 5, 11, 23, 47, 95$: observed orders 1.96, 2.60, 2.10, 1.99. The jump of $y''$ at $t = 1$ costs a local error $O(h^2)$ in one step, and that error stays in the solution. The tracked grid is exact up to rounding on this interval ($\le 2 \times 10^{-15}$).

**A delayed logistic equation.** For Hutchinson's equation $y' = r\,y(t)\big(1 - y(t - 1)\big)$, $\varphi = \tfrac12$, $h = 0.05$, the equilibrium $y = 1$ is asymptotically stable for $r < \pi/2$. Over $t \in [60, 80]$ the computed solution varies by less than $10^{-8}$ for $r = 1$, by $6.5 \times 10^{-3}$ for $r = 1.4$ (slow decay), and oscillates between 0.33 and 1.94 for $r = 1.7$ and between 0.07 and 2.90 for $r = 2$: a delay alone turns a stable equilibrium into a limit cycle.

## Correctness

The algorithm is the method of steps with classical Runge-Kutta steps and a cubic Hermite history. The proof file shows three things.

1. **Explicitness.** Every delayed time used at lines L7, L8 and L10 is at most the start of the current step, so $Z$ is well defined when it is called.
2. **Piecewise smoothness.** If $f \in C^4$ and $\varphi \in C^4[t_0 - \tau, t_0]$, the exact solution is $C^5$ on each closed interval between consecutive breakpoints of line L1 (with one-sided derivatives at the ends), by induction on the number of delays needed to reach a point.
3. **Convergence of order 4 (proved).** If moreover $f$ is Lipschitz in $y$ and in the delayed arguments, then $\max_n\|y(t_n) - y_n\| \le CH^4$ and $\sup_{t_0 \le t \le T}\|y(t) - Y(t)\| \le CH^4$ for $H$ small enough. The proof bounds the Hermite error through the basis bounds $|h_{10}|, |h_{11}| \le \tfrac4{27}$ and the interpolation remainder $k^4\max\|y^{(4)}\|/384$, bounds the RK4 local error by $O(k^5)$ on each smooth interval, and closes with a discrete [Gronwall](/gronwall-inequality/) argument.

This is the special case of the general result that a Runge-Kutta method of order $p$ with a continuous extension of uniform order $q$ converges with order $\min(p, q + 1)$ on a grid that contains the breakpoints (Bellen and Zennaro 2003, Chapters 4 to 6); here $p = 4$ and $q = 3$.

## Complexity

The number of steps is $N = \sum_i\lceil(b_i - b_{i-1})/H\rceil \le (T - t_0)/H + K$. Each step evaluates $f$ four times (line L10 doubles as the next $K_1$), plus one evaluation at line L3: $4N + 1$ evaluations. Each step makes $2m$ history lookups, each a binary search over the stored times ($O(\log N)$) and a Hermite combination ($O(d)$), and $O(d)$ vector arithmetic per stage, so the time is $\Theta(N(C + md + m\log N))$ in the [real RAM](/real-ram/) model, plus the work of listing breakpoints at line L1 ($K \le \binom{m+4}{4} - 1$ of them). Lookups could be made $O(1)$ by a moving pointer, because the delayed times increase with $t$.

The stored history takes $\Theta(Nd)$ space. Only the part newer than $t - \tau$ is ever read again, so a solver that does not need dense output afterwards can discard older steps and keep $\Theta((\tau/H + 1)d)$.

## Properties

- **Order 4** for smooth $f$ and $\varphi$ with breakpoints on the grid; order 2 or less when jumps of $y''$ fall inside steps.
- **Explicit**, with the step limited by the smallest delay; a step that is longer than a delay would need the current step's own interpolant and an iteration.
- **Continuous output.** The Hermite interpolant is a $C^1$ approximation of order 4 on the whole interval, used both internally and as the answer.
- **Exact for low-degree pieces.** If the solution is a polynomial of degree $\le 3$ on each grid interval, the method reproduces it exactly.
- **Inherits RK4's stability region.** For $y' = \lambda y + \mu y(t - \tau)$ with $\operatorname{Re}\lambda \ll 0$ the step must satisfy roughly $|h\lambda| \le 2.78$, as for the ODE; explicit DDE methods are not suitable for stiff delay problems.
- **Fixed step.** The version here has no error control; production codes adapt the step with an embedded pair.

## Variants and improvements

- **Adaptive pairs.** MATLAB's dde23 uses the [Bogacki-Shampine](/bogacki-shampine-method/) 3(2) pair with its cubic Hermite interpolant and the same breakpoint tracking for constant delays (Shampine and Thompson 2001); codes based on Dormand-Prince pairs use their dense output.
- **Steps longer than the delay.** When $\tau$ is much shorter than the natural step, the delayed times fall inside the current step. The stage values then depend on the step's own continuous extension, and the step is computed by fixed-point iteration (Bellen and Zennaro 2003, Chapter 7).
- **State-dependent delays.** For $\tau = \tau(t, y)$ the breakpoints are not known in advance; they are located during the integration as roots of $t - \tau(t, y(t)) = \xi$ for earlier breakpoints $\xi$, and the delayed time can move forward and backward.
- **Stiff DDEs.** Implicit collocation methods such as [Radau IIA](/radau-iia-methods/) with their collocation polynomial as the continuous extension (the RADAR5 code of Guglielmi and Hairer) handle stiff problems and neutral equations.
- **Natural continuous extensions.** Instead of Hermite cubics, a Runge-Kutta method can use its own continuous extension built from the stages, which needs no extra evaluation and can reach uniform order $p$ (Zennaro 1986).

## When to use it

Use a method of this kind for nonstiff DDEs with constant or slowly varying delays, such as population models, control loops with transport lags and epidemic models. Prefer an adaptive code (dde23, DelayDiffEq.jl, RADAR5) in practice; the fixed-step version is the right size for understanding and for testing. For stiff problems use implicit collocation. For questions about stability of equilibria (as in the logistic example) compute the roots of the characteristic equation instead of simulating.

## Pitfalls

- **Stepping over breakpoints.** A jump in $y''$ or $y'''$ inside a step silently reduces the order to 2 or 3; the error control of an adaptive code notices only by rejecting steps there. Put the breakpoints on the grid.
- **Using $\varphi'(t_0)$ as the first slope.** The derivative at $t_0$ for the step after it is $f(t_0, \ldots)$, not the derivative of the history.
- **Low-order interpolation.** Linear interpolation of the history ($q = 1$) limits any method to order 2.
- **Steps longer than the delay without iteration.** Extrapolating the current step's interpolant past its end loses accuracy and can break stability; cap the step at the smallest delay, or iterate.
- **Closely spaced breakpoints.** Several incommensurate delays create many nearby breakpoints and very short steps; merge points that differ by rounding only.
- **Vanishing delays.** If a state-dependent delay tends to 0, the equation approaches an ODE with a singular perturbation of the past, and fixed-delay codes misbehave.

## Implementations

## History

The method of steps, which solves a DDE with constant delay one interval of length $\tau$ at a time as an ODE, is classical and was the basis of Bellman and Cooke's 1963 treatment. Numerical methods built on it with interpolation of the stored past appeared in the 1970s, including Neves' discontinuity tracking (1975). Oberle and Pesch (1981) combined Runge-Kutta steps with Hermite interpolation. In the 1980s Bellen, Zennaro and others developed the theory of continuous Runge-Kutta methods for DDEs and proved the order $\min(p, q + 1)$ result, collected in Bellen and Zennaro's 2003 book. Shampine and Thompson's dde23 (2001) brought an adaptive solver of this design into MATLAB.

## References
