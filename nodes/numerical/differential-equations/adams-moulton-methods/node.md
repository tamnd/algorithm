---
tag: S41K1C
kind: algorithm
slug: adams-moulton-methods
name: Adams-Moulton methods
aliases:
- implicit Adams methods
- AM methods
area: numerical/differential-equations
level: core
summary: Implicit linear multistep methods that integrate the polynomial interpolating f at the new point and the last k points. The k-step method has order k + 1.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps", k: "the number of steps in the formula", d: "the dimension of y", m: "the number of Newton iterations per step"}
  time: {worst: "Θ(N (k d + m d^3))"}
  space: {extra: "Θ(k d + d^2)"}
  evaluations: {worst: "Θ(N m d)"}
properties: {deterministic: true, explicit: false, multistep: true, order: "k + 1", zero_stable: true, a_stable: "only for k = 0 and k = 1", self_starting: false}
history:
  year: 1926
  people: [Forest Ray Moulton, John Couch Adams]
  note: Adams already used implicit formulas of this type; Moulton (1926) made them practical as correctors in ballistics computations.
prereqs: [adams-bashforth-methods]
see_also: [adams-bashforth-moulton-method, linear-multistep-methods, backward-euler-method, trapezoidal-rule, backward-differentiation-formulas, zero-stability, a-stability, newton-method-for-systems]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section III.1 (implicit Adams methods, coefficients and error constants), Sections III.2 to III.4 (order, stability, convergence), Section III.3 (stability regions)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 2 (multistep methods; Adams-Moulton methods appear in the exercises and in Section 2.2) and Chapter 4 (stability of multistep methods)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 4 (linear multistep methods; Adams-Moulton methods)
  - book: "F. R. Moulton, New Methods in Exterior Ballistics, University of Chicago Press, 1926"
    locator: the implicit Adams formulas used as correctors
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section V.1 (stability of multistep methods for stiff problems; the Dahlquist barrier)
---

The Adams-Moulton methods are implicit [linear multistep methods](/linear-multistep-methods/) for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$. Like the [Adams-Bashforth methods](/adams-bashforth-methods/) they integrate an interpolating polynomial of $f$ over the next step, but the interpolation also uses the unknown value $f(t_{n+1}, y_{n+1})$. This gives order $k + 1$ from $k$ past values, error constants about ten times smaller, and much larger stability regions. The price is an equation for $y_{n+1}$ in each step. The one-step members are [backward Euler](/backward-euler-method/) and the trapezoidal rule. In practice the higher members are used as correctors in [predictor-corrector](/adams-bashforth-moulton-method/) pairs rather than solved exactly.

## In plain words

Like its explicit cousin, the method draws a smooth curve through the slopes it saw at recent points and adds up that curve over the next step. The difference is that it also wants the curve to pass through the slope at the point it is about to reach, which it does not know yet. So each step becomes a small puzzle: find the new value whose slope, put into the formula, gives back that same value. Solving the puzzle costs extra work in every step. In return, the curve is pinned at both ends of the step, so the answer is much more accurate and much less prone to errors that blow up.

## The problem

**Notation.** As on all differential-equations pages: $y' = f(t, y)$ on $[t_0, T]$, $y \in \mathbb{R}^d$, step $h$, $t_n = t_0 + nh$, $y_n \approx y(t_n)$, $f_n = f(t_n, y_n)$; $e_n = y(t_n) - y_n$; Lipschitz constant $L$; $z = h\lambda$; $\rho$ and $\sigma$ the polynomials of the multistep method.

The $k$-step Adams-Moulton method replaces $f$ in $y(t_{n+1}) = y(t_n) + \int_{t_n}^{t_{n+1}} f\,dt$ by the polynomial of degree $k$ that interpolates $f_{n+1}, f_n, \dots, f_{n-k+1}$:
$$y_{n+1} = y_n + h\Big(\beta^*_{-1} f(t_{n+1}, y_{n+1}) + \sum_{j=0}^{k-1}\beta^*_j f_{n-j}\Big), \qquad \beta^*_j = \int_0^1 \ell^*_j(s)\,ds,$$
with $\ell^*_j$ the Lagrange basis on the nodes $1, 0, -1, \dots, -(k-1)$. Then $\rho(\zeta) = \zeta^k - \zeta^{k-1}$ (for $k \ge 1$) and $\sigma$ has degree $k$.

| $k$ | $\beta^*_{-1}, \beta^*_0, \dots, \beta^*_{k-1}$ | order | error constant $\gamma^*_k$ | real stability interval |
|---|---|---|---|---|
| 0 | $1$ (backward Euler) | 1 | $-1/2$ | $(-\infty, 0]$ |
| 1 | $\tfrac12, \tfrac12$ (trapezoidal rule) | 2 | $-1/12$ | $(-\infty, 0]$ |
| 2 | $\tfrac{1}{12}(5, 8, -1)$ | 3 | $-1/24$ | $[-6, 0]$ |
| 3 | $\tfrac{1}{24}(9, 19, -5, 1)$ | 4 | $-19/720$ | $[-3, 0]$ |
| 4 | $\tfrac{1}{720}(251, 646, -264, 106, -19)$ | 5 | $-3/160$ | $[-90/49, 0]$ |

The intervals for $k \ge 2$ were computed with a root finder on $\rho(\zeta) - z\sigma(\zeta)$; the first two follow from [A-stability](/a-stability/).

## The algorithm

```pseudo id=main
ADAMS-MOULTON(f, t0, y0, T, h, k)
L1  N ← ⌈(T − t0)/h⌉; if N = 0 return (t0, y0); h ← (T − t0)/N
L2  β*_j ← ∫₀¹ ℓ*_j(s) ds for j = −1, 0, …, k − 1   ▷ nodes 1, 0, −1, …, −(k−1)
L3  y_0 ← y0, f_0 ← f(t0, y_0)
L4  for n = 0 to min(k − 1, N) − 1 do                 ▷ starting values
L5      y_{n+1} ← one RK4 step from (t_n, y_n); f_{n+1} ← f(t_{n+1}, y_{n+1})
L6  for n = max(k − 1, 0) to N − 1 do
L7      g ← y_n + h · Σ_{j=0}^{k−1} β*_j f_{n−j}       ▷ the known part
L8      x ← y_n + h f_n                                ▷ initial guess
L9      solve x = g + h β*_{−1} f(t_{n+1}, x) by Newton: (I − h β*_{−1} J) δ = g + h β*_{−1} f(t_{n+1}, x) − x, x ← x + δ
L10     y_{n+1} ← x, f_{n+1} ← f(t_{n+1}, y_{n+1})
L11 return (t_n, y_n) for n = 0, …, N
```

$J$ is the Jacobian $\partial f/\partial y$ at the current iterate, given by the caller or approximated by forward differences. Newton stops when the correction is below a relative tolerance of $10^{-12}$. As for Adams-Bashforth, the step is shrunk in L1 so that the uniform grid ends at $T$.

## Example

Take $y' = -2ty^2$, $y(0) = 1$, exact $y = 1/(1 + t^2)$, $k = 2$ and $h = 0.1$. The starting step gives $y_1 = 0.9900989$. Then $y_2$ solves
$$y_2 = y_1 + 0.1\Big(\tfrac{5}{12}(-0.4\,y_2^2) + \tfrac{8}{12}(-0.2\,y_1^2) - \tfrac{1}{12}\cdot 0\Big),$$
a quadratic equation, and Newton gives $y_2 = 0.9616165$ against the exact $0.9615385$. The error $7.8 \cdot 10^{-5}$ is about a tenth of the error $8.5 \cdot 10^{-4}$ of the explicit AB2 step with the same data, which has the same number of past values but order 2.

The maximum error over the grid on $[0, 2]$ (observed, from the implementation) is:

| $h$ | $k = 0$ | $k = 1$ | $k = 2$ | $k = 3$ | $k = 4$ |
|---|---|---|---|---|---|
| 0.1 | $2.18 \cdot 10^{-2}$ | $1.20 \cdot 10^{-3}$ | $1.13 \cdot 10^{-4}$ | $5.39 \cdot 10^{-5}$ | $1.33 \cdot 10^{-5}$ |
| 0.05 | $1.14 \cdot 10^{-2}$ | $3.00 \cdot 10^{-4}$ | $1.77 \cdot 10^{-5}$ | $3.91 \cdot 10^{-6}$ | $3.45 \cdot 10^{-7}$ |
| 0.025 | $5.84 \cdot 10^{-3}$ | $7.50 \cdot 10^{-5}$ | $2.42 \cdot 10^{-6}$ | $2.54 \cdot 10^{-7}$ | $1.18 \cdot 10^{-8}$ |
| 0.0125 | $2.96 \cdot 10^{-3}$ | $1.88 \cdot 10^{-5}$ | $3.17 \cdot 10^{-7}$ | $1.61 \cdot 10^{-8}$ | $4.50 \cdot 10^{-10}$ |
| 0.00625 | $1.49 \cdot 10^{-3}$ | $4.69 \cdot 10^{-6}$ | $4.06 \cdot 10^{-8}$ | $1.01 \cdot 10^{-9}$ | $1.54 \cdot 10^{-11}$ |

The observed orders at the last halving are $0.99, 2.00, 2.97, 3.99$ and $4.87$, that is $k + 1$.

## Correctness

The proofs are in `proofs/correctness.md`. In summary:

1. **Order $k + 1$.** If $y \in C^{k+2}$, the local truncation error is bounded by $|\gamma^*_k|M_{k+2}h^{k+2}$ with $\gamma^*_k = \int_0^1 \frac{(s - 1)s(s + 1)\cdots(s + k - 1)}{(k + 1)!}ds < 0$, and for scalar $y$ it equals $\gamma^*_kh^{k+2}y^{(k+2)}(\xi)$. The weights and the constants $C_0 = \dots = C_{k+1} = 0$, $C_{k+2} = \gamma^*_k$ are checked exactly with fractions in the tests.
2. **The step is well defined.** If $h|\beta^*_{-1}|L < 1$, the equation in L9 has exactly one solution (Banach fixed point theorem). On stiff problems, where $hL$ is large, existence needs other hypotheses, such as a one-sided Lipschitz condition for backward Euler and the trapezoidal rule.
3. **Convergence.** For $h|\beta^*_{-1}|L \le 1/2$ the global error satisfies $\|e_n\| \le e^{2LB^*(t_n - t_0)}(\delta + 2|\gamma^*_k|M_{k+2}h^{k+1}(t_n - t_0))$, where $B^* = \sum_{j \ge -1}|\beta^*_j|$ and $\delta$ bounds the starting errors. With RK4 starting values the implementation has order $\min(k + 1, 5)$.

## Complexity

The cost model counts evaluations of $f$, Jacobians and linear solves. Each step after the start costs $m$ Newton iterations, each with one evaluation of $f$, one Jacobian (or $d$ extra evaluations for the difference approximation) and one dense LU solve of size $d$, costing $\Theta(d^3)$, plus one final evaluation for $f_{n+1}$. For a linear $f$ Newton converges in one iteration, confirmed by a second one. In predictor-corrector use (no Newton, a fixed number of corrections) the cost drops to two evaluations per step; see [Adams-Bashforth-Moulton](/adams-bashforth-moulton-method/).

## Properties

- **Implicit, order $k + 1$, zero-stable.** $\rho(\zeta) = \zeta^{k-1}(\zeta - 1)$ satisfies the root condition with all spurious roots at 0.
- **Smaller error constants than Adams-Bashforth.** For the same order $p$, $|\gamma^*_{p-1}|$ is much smaller than $\gamma_p$ of Adams-Bashforth: $1/12$ against $5/12$ for $p = 2$, $19/720$ against $251/720$ for $p = 4$.
- **Stability.** Backward Euler and the trapezoidal rule are [A-stable](/a-stability/). For $k \ge 2$ the regions are bounded; the real intervals in the table are about ten times longer than those of Adams-Bashforth of the same order, but still finite, so these methods are not for stiff problems. By the [Dahlquist barrier](/dahlquist-barrier/), no member of order above 2 could be A-stable.
- **The trapezoidal rule preserves quadratic invariants of linear problems.** On $y_1' = y_2$, $y_2' = -y_1$, $|R(iy)| = 1$, so $y_1^2 + y_2^2$ is constant up to rounding, as the tests check over 200 steps.

## Variants and improvements

- **[Predictor-corrector (PECE)](/adams-bashforth-moulton-method/).** Predict $y_{n+1}$ with Adams-Bashforth, then apply the Adams-Moulton formula once or a fixed number of times. This avoids Newton and gives an error estimate by Milne's device.
- **Variable step size and order.** As for Adams-Bashforth, with divided differences or the Nordsieck form; Adams-Moulton correctors are the core of LSODE in non-stiff mode, VODE and ode113.
- **[Backward differentiation formulas](/backward-differentiation-formulas/).** Implicit methods built by differentiating, not integrating, an interpolant; they trade accuracy for stability on stiff problems.
- **The theta method.** Between backward Euler and the trapezoidal rule; A-stable for $\theta \ge 1/2$.

## When to use it

Use the low members, backward Euler and the trapezoidal rule, when stability matters: for mildly stiff problems and as the time step of [Crank-Nicolson](/crank-nicolson-method/). Use the higher members as correctors in Adams codes for smooth non-stiff problems with expensive $f$, such as celestial mechanics. For truly stiff problems of order above 2, use BDF or implicit Runge-Kutta methods.

## Pitfalls

- **Solving the equation by fixed-point iteration on a stiff problem.** Iterating $x \leftarrow g + h\beta^*_{-1}f(t_{n+1}, x)$ converges only if $h|\beta^*_{-1}|L < 1$, which is the stability restriction of an explicit method again. Stiff problems need Newton.
- **Expecting stiff stability from higher orders.** AM2 is stable on the real axis only up to $z = -6$. With $z = -6.5$ the computed solution of $y' = \lambda y$ grows without bound, as the tests show.
- **Trapezoidal rule on very stiff components.** $R(z) \to -1$ as $z \to -\infty$, so stiff components oscillate in sign and hardly decay. Use backward Euler or BDF2 when such components are present.
- **Starting values of too low an order.** As for Adams-Bashforth, they cap the global order.

## Implementations

## History

Adams used implicit interpolation formulas alongside the explicit ones in the 1850s. F. R. Moulton, working on ballistics tables in the First World War, published the systematic use of the implicit formula as a corrector to an explicit predictor in his 1926 book. Dahlquist's theory of 1956 and 1963 explained their convergence and showed the limit on their A-stability. Hairer, Nørsett and Wanner describe this history in Section III.1.

## References
