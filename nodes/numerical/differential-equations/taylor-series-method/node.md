---
tag: 9A499S
kind: algorithm
slug: taylor-series-method
name: Taylor series method for ODEs
aliases:
- Taylor method
- Taylor series integrator
- high-order Taylor method
area: numerical/differential-equations
level: advanced
summary: "Integrates y' = f(t, y) by computing the Taylor coefficients of the solution to order p with automatic differentiation in Taylor mode and summing the truncated series. Order p, any p."
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps", p: "the order", m: "the number of operations in the formula for f"}
  time: {worst: "Θ(N m p^3)"}
  space: {extra: "Θ(m p)"}
  evaluations: {worst: "N p"}
properties: {deterministic: true, implicit: false, one_step: true, order: "p, chosen freely", a_stable: false, symplectic: false}
history:
  year: 1960
  people: [Leonhard Euler, A. Gibbons, Ramon E. Moore, George F. Corliss, Àngel Jorba]
  note: Euler (1768) proposed the expansion of the solution in a Taylor series. Gibbons (1960) and Moore (1966) computed the coefficients automatically by recurrences, the start of Taylor-mode automatic differentiation; Corliss and Chang (1982) and Jorba and Zou (2005) built general solvers.
prereqs: [ode-initial-value-problem, euler-method, order-of-accuracy]
see_also: [runge-kutta-methods, picard-lindelof-theorem, stability-region, local-truncation-error, global-error, bulirsch-stoer-method, pade-approximation]
sources:
  - paper: "George F. Corliss and Y. F. Chang, Solving ordinary differential equations using Taylor series, ACM Transactions on Mathematical Software 8 (1982) 114-144"
    locator: recurrences for Taylor coefficients, step size and order selection; doi:10.1145/355993.355995
  - paper: "Àngel Jorba and Maorong Zou, A software package for the numerical integration of ODEs by means of high-order Taylor methods, Experimental Mathematics 14 (2005) 99-117"
    locator: Sections 2 and 3 (automatic differentiation rules, cost, step size and order control); doi:10.1080/10586458.2005.10128904
  - book: isbn:9780898716597
    title: Andreas Griewank and Andrea Walther, Evaluating Derivatives, Principles and Techniques of Algorithmic Differentiation, second edition, SIAM, 2008
    locator: Chapter 13 (Taylor and tensor coefficients; propagation rules and their cost)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section I.8 (existence theory using Taylor series), Section II.3 (convergence of one-step methods)
  - paper: "A. Gibbons, A program for the automatic integration of differential equations using the method of Taylor series, The Computer Journal 3 (1960) 108-111"
    locator: automatic computation of Taylor coefficients by recurrences
---

The Taylor series method solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, by expanding the solution at each grid point in its Taylor series to order $p$ and summing the truncated series: $y_{n+1} = \sum_{k=0}^{p} y_{[k]} h^k$ with $y_{[k]} = y^{(k)}(t_n)/k!$. The derivatives are not derived by hand: automatic differentiation in Taylor mode computes them from the formula for $f$ by simple recurrences. The order $p$ can be any integer, 20 or 30 is common, so very high accuracy is cheap for smooth nonstiff problems. With $p = 1$ it is the [Euler method](/euler-method/).

## In plain words

If you know where a moving point is, how fast it moves, how its speed changes, how that change changes, and so on, you can predict where it will be a little later with a polynomial. The differential equation gives the speed directly from the position. Differentiating the equation again and again gives all the higher rates of change.

Doing that by hand is tedious and error-prone, but a computer can do it mechanically: it treats every number in the formula as a short polynomial and applies the rules of polynomial arithmetic. One pass gives the next coefficient. After enough passes, the polynomial is very accurate over a fairly long step, so very few steps are needed.

## The problem

Given $f$ as a formula built from $t$, $y$, constants, $+$, $-$, $\times$, $/$, integer powers and elementary functions such as $\exp$, $\sin$ and $\cos$, start values $t_0$, $y_0$, an end time $T \ge t_0$, a step size $h > 0$ and an order $p \ge 1$, compute $y_N \approx y(T)$. We assume the solution exists on $[t_0, T]$ and stays where $f$ is defined; then $f$ and $y$ are analytic. The cost is the number of evaluations of $f$ on truncated power series, $p$ per step, each costing $O(m p^2)$ arithmetic for a formula with $m$ operations in the simple version implemented here.

## The algorithm

```pseudo id=main
TAYLOR(f, t0, y0, T, h, p)
L1  N ← ⌈(T − t0)/h − δ⌉; t ← t0, y ← y0      ▷ δ: relative slack 10^-9 against rounding
    for n ← 0 to N − 1 do                      ▷ step τ = h, or T − t for the last step
L2      Y_[0] ← y
L3      for k ← 0 to p − 1 do
L4          F ← f(t + s, Y_[0] + Y_[1] s + ... + Y_[k] s^k) in series arithmetic mod s^(k+1)
L5          Y_[k+1] ← F_[k] / (k + 1)          ▷ coefficient k of F
L6      y ← Y_[0] + τ(Y_[1] + τ(Y_[2] + ... + τ Y_[p]))    ▷ Horner's rule
L7      t ← t + τ
    return (t, y)
```

Series arithmetic on truncated power series uses the Cauchy product for $\times$, a recurrence for $/$, and recurrences such as $k e_{[k]} = \sum_{j=1}^k j x_{[j]} e_{[k-j]}$ for $e = \exp x$ and the coupled pair for $\sin$ and $\cos$. Coefficient $k$ of each result depends only on coefficients up to $k$ of the arguments, which is why line L5 is exact.

## Example

Take $y' = -2ty^2$, $y(0) = 1$, with solution $y = 1/(1 + t^2)$. At $t = 0$ the recurrences give the coefficients $1, 0, -1, 0, 1, 0, -1, \ldots$, the series of $1/(1 + t^2)$. With $p = 4$ and $h = 0.2$, the first step is $y_1 = 1 - 0.2^2 + 0.2^4 = 0.9616$, against $y(0.2) = 0.961538$. Continuing, $y_5 = 0.500087$ at $t = 1$.

Max errors at $t = 1$ for $h = 0.2, 0.1, 0.05, 0.025$ (observed):

| $p$ | $h = 0.2$ | $0.1$ | $0.05$ | $0.025$ | last observed order |
|---|---|---|---|---|---|
| 1 | 7.06e-3 | 3.64e-3 | 1.81e-3 | 8.95e-4 | 1.01 |
| 2 | 7.71e-3 | 1.71e-3 | 4.05e-4 | 9.85e-5 | 2.04 |
| 3 | 4.52e-4 | 5.57e-5 | 6.84e-6 | 8.47e-7 | 3.01 |
| 4 | 8.75e-5 | 4.70e-6 | 2.75e-7 | 1.67e-8 | 4.04 |
| 6 | 5.61e-7 | 1.33e-8 | 2.36e-10 | 3.89e-12 | 5.93 |

For the harmonic oscillator $y_1' = y_2$, $y_2' = -y_1$ with $p = 20$ and $h = 1$, ten steps reach $t = 10$ with error $1.1 \times 10^{-16}$.

## Correctness

**Theorem (proved).** Let $f$ be built from the supported operations and let the solution stay in a compact set where $f$ is defined. Then line L5 computes the exact Taylor coefficients $y_{[k]}$ of the solution through $(t_n, y_n)$, the local error is $y_{[p+1]}(\xi)h^{p+1}$ per component, and the global error is $O(h^p)$ on $[t_0, T]$.

The proof shows that each series operation is causal: coefficient $k$ of the result depends only on coefficients $0$ to $k$ of the arguments. Comparing coefficients in $y'(t + s) = f(t + s, y(t + s))$ then gives $y_{[k+1]}$ by induction, and convergence follows from the Lipschitz argument for one-step methods. On $y' = \lambda y$ the method gives $R(z) = \sum_{k=0}^p z^k/k!$, so its [stability region](/stability-region/) is bounded, the same as explicit Runge-Kutta methods of order $p \le 4$.

## Complexity

Line L4 is an evaluation of $f$ on series of length $k + 1$. A product of two such series costs $\Theta(k^2)$ when all coefficients are recomputed, as in this implementation, so one step costs $\Theta(m p^3)$ and $N$ steps $\Theta(N m p^3)$, with $N p$ series evaluations of $f$. Production codes store all intermediate series and compute only the new coefficient $k$ of each operation, in $\Theta(k)$, which gives $\Theta(m p^2)$ per step (Jorba and Zou 2005; Griewank and Walther 2008, Chapter 13). Space is $\Theta(m p)$ for the intermediate series. With $p$ growing like $\log(1/\text{tol})$ and the step adapted to the radius of convergence, the work to reach tolerance tol grows only polynomially in the number of digits.

## Properties

- **Order** $p$ for any $p \ge 1$; explicit, one-step.
- **Exact derivatives**: no difference quotients, so no cancellation from numerical differentiation.
- **Stability function** $R(z) = \sum_{k \le p} z^k/k!$, the truncated exponential. Its real stability interval grows roughly linearly with $p$ (for example $[-2, 0]$ for $p = 1, 2$, $[-2.513, 0]$ for $p = 3$ and $[-2.785, 0]$ for $p = 4$), but the region is always bounded; not A-stable.
- **Error estimates for free**: the size of the last coefficients estimates the truncation error and the radius of convergence, which drives step size and order control.
- **Dense output**: the Taylor polynomial gives the solution anywhere inside the step.
- **Validated integration**: with interval arithmetic and a bound on the remainder, the method yields rigorous enclosures of the solution (Moore).

## Variants and improvements

- **Variable order and step**: choose $p \approx -\frac12 \ln(\text{tol})$ and $h$ from the decay of the last coefficients, as in the codes of Jorba and Zou.
- **Interval Taylor methods** (Moore; Lohner's method) enclose the solution rigorously and are a standard tool of computer-assisted proofs in dynamical systems.
- **Implicit Taylor methods** and Taylor-Padé methods replace the polynomial by a [Padé approximant](/pade-approximation/) to get A-stable schemes for stiff problems.
- **Multivariate Taylor (jet transport)** propagates sets of initial conditions as polynomials.
- **Runge-Kutta methods** reach the same order without derivatives of $f$, at the cost of $s \ge p$ evaluations per step and order conditions that explode with $p$.

## When to use it

Use the Taylor method for smooth nonstiff problems where very high accuracy is needed, such as celestial mechanics, the computation of periodic orbits and invariant manifolds, and computer-assisted proofs, and where $f$ is given as an explicit formula. It is less convenient when $f$ is a black box (for example a simulation or table lookup), when the problem is stiff, or when low accuracy suffices, where a Runge-Kutta method of order 4 or 5 is simpler.

## Pitfalls

- **Stiff problems.** On $y' = -100y$ with $p = 4$, $h = 0.025$ ($z = -2.5$) decays, while $h = 0.03$ ($z = -3$) grows past $10^6$ by $t = 2$ (observed), because the real stability limit is $-2.785$.
- **Steps beyond the radius of convergence.** For $y' = y^2$, $y(0) = 1$, the coefficients are all 1 and the series diverges for $h \ge 1$; a step near a singularity of the solution needs $h$ well below the radius of convergence.
- **Black-box functions.** Calls to library routines without series rules (for example `abs`, table lookups, `if` statements on $y$) break the recurrences or make $f$ non-analytic.
- **Rounding for large $p$.** Large coefficients of alternating sign can cancel; summing by Horner's rule from the highest term and keeping $h$ inside the radius of convergence keeps this under control.

## Implementations

## History

Euler (1768) suggested expanding the solution in its Taylor series. The approach was impractical by hand beyond low orders until Gibbons (1960) and Moore (1966) showed that the coefficients can be computed automatically by recurrences on the formula for $f$, which is Taylor-mode automatic differentiation. Barton, Willers and Zahar, Corliss and Chang (1982) and later Jorba and Zou (2005) built general Taylor solvers, and interval versions became a standard tool of computer-assisted proofs.

## References
