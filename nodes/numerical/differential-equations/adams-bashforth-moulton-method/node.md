---
tag: VJTC0J
kind: algorithm
slug: adams-bashforth-moulton-method
name: Adams-Bashforth-Moulton predictor-corrector
aliases:
- PECE method
- predictor-corrector methods
- ABM method
- Adams predictor-corrector
area: numerical/differential-equations
level: core
summary: An explicit Adams-Bashforth predictor, one evaluation of f, an Adams-Moulton corrector and a second evaluation (PECE). Order k for two evaluations per step, with Milne's error estimate.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps", k: "the order", d: "the dimension of y", m: "the number of corrections per step"}
  time: {worst: "Θ(N k d m)"}
  space: {extra: "Θ(k d)"}
  evaluations: {worst: "N (m + 1) + 4 k"}
properties: {deterministic: true, explicit: true, multistep: true, order: "k", zero_stable: true, a_stable: false, error_estimate: "Milne's device"}
history:
  year: 1926
  people: [Forest Ray Moulton, William Edmund Milne]
  note: Moulton (1926) used an Adams-Bashforth predictor with an Adams-Moulton corrector for ballistics; Milne (1926) proposed estimating the error from the difference of predictor and corrector.
prereqs: [adams-bashforth-methods, adams-moulton-methods]
see_also: [linear-multistep-methods, adaptive-step-size-control, embedded-runge-kutta-pairs, local-truncation-error, absolute-stability, zero-stability, classical-runge-kutta-4, backward-differentiation-formulas]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section III.1 (predictor-corrector methods, PECE and PEC modes), Section III.3 (stability regions of predictor-corrector schemes), Section III.7 (Milne's device and step size control in Adams codes)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 5, Section 5.4 (predictor-corrector methods, Milne's estimate)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 4 (linear multistep methods; predictor-corrector Adams methods)
  - book: "F. R. Moulton, New Methods in Exterior Ballistics, University of Chicago Press, 1926"
    locator: the predictor-corrector use of the Adams formulas
  - paper: "W. E. Milne, Numerical integration of ordinary differential equations, American Mathematical Monthly 33 (1926) 455-460"
    locator: the estimate of the error from the difference between predicted and corrected values
---

The Adams-Bashforth-Moulton method combines an explicit [Adams-Bashforth](/adams-bashforth-methods/) formula and an implicit [Adams-Moulton](/adams-moulton-methods/) formula of the same order $k$. In each step it **P**redicts $y_{n+1}$ with the explicit formula, **E**valuates $f$ there, **C**orrects with the implicit formula using that value in place of the unknown $f_{n+1}$, and **E**valuates again (PECE). The result is an explicit method for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$ of order $k$ that costs two evaluations of $f$ per step, has the small error constant of the corrector and a larger stability region than the predictor, and gives an estimate of its own local error for free from the gap between corrector and predictor (Milne's device). In variable-step, variable-order form it is the method of the classical non-stiff codes.

## In plain words

The method makes a quick guess of the next value by extrapolating the recent slopes, as the explicit Adams method does. It then looks at the slope at that guessed point. With this slope it redoes the step using the more accurate implicit formula, which normally needs the slope at the unknown new point; the guess stands in for it. The guess and the improved value usually agree closely. When they do not, something is wrong with the step, and the size of the disagreement says how large the error of the improved value is. So the method gets an accurate step, a warning signal and a way to choose the next step size, for only two slope evaluations.

## The problem

**Notation.** As on all differential-equations pages: $y' = f(t, y)$ on $[t_0, T]$, $y \in \mathbb{R}^d$, step $h$, $t_n = t_0 + nh$, $y_n \approx y(t_n)$, $f_n = f(t_n, y_n)$; global error $e_n = y(t_n) - y_n$; order $p$; $z = h\lambda$.

For order $k$ the predictor is the $k$-step Adams-Bashforth formula with weights $\beta_j$ and error constant $\gamma_k$, and the corrector is the $(k-1)$-step Adams-Moulton formula with weights $\beta^*_j$ and error constant $\gamma^*_{k-1}$, both of order $k$:
$$y^P_{n+1} = y_n + h\sum_{j=0}^{k-1}\beta_jf_{n-j}, \qquad y_{n+1} = y_n + h\Big(\beta^*_{-1}f(t_{n+1}, y^P_{n+1}) + \sum_{j=0}^{k-2}\beta^*_jf_{n-j}\Big).$$
Since $y(t_{n+1}) - y^P_{n+1} \approx \gamma_kh^{k+1}y^{(k+1)}$ and $y(t_{n+1}) - y_{n+1} \approx \gamma^*_{k-1}h^{k+1}y^{(k+1)}$, **Milne's estimate** of the local error of the corrected value is
$$\mathrm{est}_{n+1} = \frac{\gamma^*_{k-1}}{\gamma_k - \gamma^*_{k-1}}\,(y_{n+1} - y^P_{n+1}).$$
For $k = 4$ the factor is $(-19/720)/(270/720) = -19/270$; for $k = 2$ it is $-1/6$.

## The algorithm

```pseudo id=main
ABM-PECE(f, t0, y0, T, h, k, m = 1)
L1  N ← ⌈(T − t0)/h⌉; if N = 0 return (t0, y0); h ← (T − t0)/N
L2  β_j (AB, k steps), β*_j (AM, k − 1 steps), M ← γ*/(γ − γ*), all exact
L3  y_0 ← y0, f_0 ← f(t0, y_0)
L4  for n = 0 to min(k − 1, N) − 1 do                 ▷ starting values
L5      y_{n+1} ← one RK4 step from (t_n, y_n); f_{n+1} ← f(t_{n+1}, y_{n+1})
L6  for n = k − 1 to N − 1 do
L7      P: y^P ← y_n + h Σ_{j=0}^{k−1} β_j f_{n−j}
L8      E: φ ← f(t_{n+1}, y^P)
L9      C: y^C ← y_n + h (β*_{−1} φ + Σ_{j=0}^{k−2} β*_j f_{n−j})      ▷ L9 and L10 are repeated m times
L10     E: φ ← f(t_{n+1}, y^C)
L11     y_{n+1} ← y^C, f_{n+1} ← φ, est_{n+1} ← |M| · ‖y^C − y^P‖∞
L12 return (t_n, y_n, est_n) for n = 0, …, N
```

With $m = 1$ this is PECE; with $m > 1$ it is P(EC)$^m$E, and as $m \to \infty$ (for $h|\beta^*_{-1}|L < 1$) it tends to the fully implicit Adams-Moulton step. The step is shrunk in L1 so that the uniform grid ends at $T$.

## Example

Take $y' = -2ty^2$, $y(0) = 1$, exact $y = 1/(1 + t^2)$, $k = 4$, $h = 0.1$. RK4 gives $y_1, y_2, y_3$. At step 4 the predictor gives $y^P_4 = 0.8623886$ and the corrector $y_4 = 0.8620271$; the exact value is $0.8620690$. Milne's estimate is $\tfrac{19}{270}|y_4 - y^P_4| = \tfrac{19}{270} \cdot 3.61 \cdot 10^{-4} = 2.54 \cdot 10^{-5}$, while the actual error is $4.18 \cdot 10^{-5}$. The estimate has the right size, and it improves as $h$ shrinks. From exact past values at $t = 1$ the ratio of estimate to true local error is $0.58, 0.73, 0.85, 0.92$ for $h = 0.1, 0.05, 0.025, 0.0125$.

The maximum error over $[0, 2]$ (observed):

| $h$ | $k = 2$ | $k = 3$ | $k = 4$ | $k = 5$ |
|---|---|---|---|---|
| 0.1 | $1.69 \cdot 10^{-3}$ | $1.69 \cdot 10^{-4}$ | $8.24 \cdot 10^{-5}$ | $3.05 \cdot 10^{-5}$ |
| 0.05 | $3.58 \cdot 10^{-4}$ | $1.52 \cdot 10^{-5}$ | $4.87 \cdot 10^{-6}$ | $6.35 \cdot 10^{-7}$ |
| 0.025 | $8.21 \cdot 10^{-5}$ | $2.25 \cdot 10^{-6}$ | $2.86 \cdot 10^{-7}$ | $1.33 \cdot 10^{-8}$ |
| 0.0125 | $1.96 \cdot 10^{-5}$ | $3.05 \cdot 10^{-7}$ | $1.71 \cdot 10^{-8}$ | $4.23 \cdot 10^{-10}$ |
| 0.00625 | $4.80 \cdot 10^{-6}$ | $3.98 \cdot 10^{-8}$ | $1.04 \cdot 10^{-9}$ | $1.49 \cdot 10^{-11}$ |

Compared with AB4 alone (error $1.33 \cdot 10^{-8}$ at $h = 0.00625$, on the Adams-Bashforth page), PECE of order 4 is about 13 times more accurate for twice the evaluations.

## Correctness

The proofs are in `proofs/correctness.md`. In summary:

1. **PECE is an explicit one-step map on the history.** Its local error is $\tau^{PECE}_{n+1} = \tau^*_{n+1} + h\beta^*_{-1}\big(f(t_{n+1}, y(t_{n+1})) - f(t_{n+1}, \tilde y^P)\big)$, where $\tau^*$ is the local error of the corrector and $\tilde y^P$ the predictor from exact data. If $f$ is $L$-Lipschitz and $y \in C^{k+1}$, then $\|\tau^{PECE}_{n+1}\| \le (|\gamma^*_{k-1}| + h|\beta^*_{-1}|L\gamma_k)M_{k+1}h^{k+1}$. So the order is $k$, and the leading error term is that of the corrector alone.
2. **Convergence.** The error recursion is $\|e_{n+1}\| \le (1 + hLB(1 + h|\beta^*_{-1}|L))\max_{m \le n}\|e_m\| + \|\tau^{PECE}_{n+1}\|$ with $B$ the sum of the absolute weights. As for Adams-Bashforth this gives $\|e_n\| = O(\delta + h^k)$ on bounded intervals, a proved bound; $\delta$ is the starting error, $O(h^5)$ with RK4.
3. **Milne's estimate.** If $f \in C^{k+1}$, $y^C - y^P = (\gamma_k - \gamma^*_{k-1})h^{k+1}y^{(k+1)}(t_n) + O(h^{k+2})$ for exact data, so the estimate equals the local error up to $O(h^{k+2})$. This is an asymptotic statement; the numbers above show it at moderate $h$.

## Complexity

The cost model counts evaluations of $f$. P(EC)$^m$E costs $m + 1$ evaluations per step and no linear algebra. With RK4 starting values the implementation costs $1 + 5(k - 1) + (m + 1)(N - k + 1)$ evaluations, at most $N(m + 1) + 4k$. The memory is the last $k$ values of $f$. A fully implicit Adams-Moulton step would instead need a Jacobian and a linear solve of size $d$ in each Newton iteration.

## Properties

- **Order $k$ with the corrector's error constant.** For $k = 4$, $|\gamma^*_3| = 19/720 \approx 0.026$ against $\gamma_4 = 251/720 \approx 0.35$ for AB4.
- **Stability.** The PECE scheme has its own stability polynomial, $\zeta^k - \zeta^{k-1} - z\big(\beta^*_{-1}(\zeta^{k-1} + z\sigma_{AB}(\zeta)) + \sum_{j \ge 0}\beta^*_j\zeta^{k-1-j}\big)$. Its real stability intervals, found with a root finder, are $[-2, 0]$, $[-1.729, 0]$, $[-1.285, 0]$ and $[-0.947, 0]$ for $k = 2, 3, 4, 5$, about four times those of Adams-Bashforth for $k = 4$ but much smaller than those of the implicit corrector. The region is bounded, so PECE is not suitable for stiff problems.
- **Zero-stable.** For $h = 0$ the scheme reduces to $\rho(\zeta) = \zeta^{k-1}(\zeta - 1)$.
- **A built-in error estimate**, used to accept or reject steps and to choose the next $h$ and $k$.

## Variants and improvements

- **PEC and PECE modes.** PEC skips the final evaluation and reuses $f(y^P)$ in the history; it saves one evaluation per step but has smaller stability regions. P(EC)$^m$E iterates the corrector.
- **Local extrapolation.** Adding Milne's estimate to $y^C$ gives a value of order $k + 1$, at the cost of losing the estimate for that value; many codes do this.
- **Corrector of higher order.** Pairing AB$k$ with AM of $k$ steps (order $k + 1$) also works; then the difference estimates the predictor's error.
- **Variable step and order.** Shampine and Gordon's DE/STEP, Krogh's DVDQ, LSODE in Adams mode and MATLAB's ode113 use modified divided differences or Nordsieck vectors to change $h$ and $k$ each step.
- **Milne's and Hamming's methods.** Older predictor-corrector pairs built from Milne's (Simpson) formulas, now mostly of historical interest because Milne's corrector is only weakly stable.

## When to use it

Use ABM for smooth non-stiff problems where evaluations of $f$ dominate the cost and high accuracy is wanted, such as orbit and trajectory computations, $N$-body problems and smooth control systems. In a variable-step code it typically needs fewer evaluations than Runge-Kutta pairs at tight tolerances. Prefer [embedded Runge-Kutta pairs](/embedded-runge-kutta-pairs/) when the solution has frequent discontinuities (restarts are cheap for one-step methods) and BDF for stiff problems.

## Pitfalls

- **Treating PECE as the implicit method.** PECE inherits the accuracy of the corrector but not its stability. On $y' = -1000(y - \cos t)$ with $h = 0.01$, PECE of order 4 explodes, as the tests show; with $h = 0.0005$ it is accurate.
- **Iterating the corrector to convergence on stiff problems.** The fixed-point iteration converges only if $h|\beta^*_{-1}|L < 1$, the same restriction again.
- **Trusting the estimate at large $h$.** Milne's estimate is asymptotic; in the example at $h = 0.1$ it is 40 percent too small.
- **Restarting after a discontinuity.** A jump in $f$ invalidates the history; the code must restart with the starting procedure, which costs extra evaluations.

## Implementations

## History

F. R. Moulton combined the explicit and implicit Adams formulas as predictor and corrector for the ballistics computations of the First World War and published them in 1926. In the same year W. E. Milne published his predictor-corrector method and the idea of estimating the error from the difference of the two values. The automatic variable-order Adams codes of Krogh, of Shampine and Gordon (1975) and of Hindmarsh's LSODE made the PECE scheme the standard non-stiff multistep integrator. Hairer, Nørsett and Wanner give the history in Sections III.1 and III.7.

## References
