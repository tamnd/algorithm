---
tag: FA09JN
kind: algorithm
slug: bulirsch-stoer-method
name: Bulirsch-Stoer method
aliases:
- Gragg-Bulirsch-Stoer method
- GBS extrapolation
- extrapolated midpoint method
area: numerical/differential-equations
level: advanced
summary: An extrapolation method for ODEs. It repeats one big step with Gragg's modified midpoint rule for several substep counts and extrapolates the results to step size zero in powers of h^2.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of accepted steps", R: "the number of rejected steps", k: "the number of extrapolation stages", d: "the dimension of y"}
  time: {worst: "Θ((N + R) k^2 d)"}
  space: {extra: "Θ(k^2 d)"}
  evaluations: {worst: "(k^2 + 1) (N + R)"}
properties: {deterministic: true, explicit: true, one_step: true, order: "2k", error_estimate: true, a_stable: false}
history:
  year: 1966
  people: [William B. Gragg, Roland Bulirsch, Josef Stoer]
  note: Gragg (1965) proved that the modified midpoint rule has an error expansion in even powers of h. Bulirsch and Stoer (1966) combined it with rational extrapolation into a practical adaptive method.
prereqs: [richardson-extrapolation, explicit-midpoint-method]
see_also: [runge-kutta-methods, dormand-prince-method, cash-karp-method, adaptive-step-size-control, symplectic-integrators, stiff-ode-problem, polynomial-interpolation, local-truncation-error]
sources:
  - paper: doi:10.1007/BF02165234
    title: "R. Bulirsch and J. Stoer, Numerical treatment of ordinary differential equations by extrapolation methods, Numerische Mathematik 8 (1966) 1-13"
    locator: the extrapolation algorithm with the midpoint rule, rational extrapolation and the step number sequence
  - paper: "W. B. Gragg, On extrapolation algorithms for ordinary initial value problems, SIAM Journal on Numerical Analysis, Series B, 2 (1965) 384-403"
    locator: the asymptotic expansion in even powers of h for the modified midpoint rule
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.8 (asymptotic expansion of the global error) and Section II.9 (extrapolation methods, the GBS method, order and step size control)
  - paper: "P. Deuflhard, Order and stepsize control in extrapolation methods, Numerische Mathematik 41 (1983) 399-422"
    locator: the step number sequence 2, 4, 6, 8, ... and the joint control of order and step size
---

The Bulirsch-Stoer method, also called Gragg-Bulirsch-Stoer or GBS, solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$ by [Richardson extrapolation](/richardson-extrapolation/). One big step of size $H$ is computed several times with Gragg's modified midpoint rule, using $n_1 < n_2 < \dots < n_k$ substeps. The modified midpoint rule is the [explicit midpoint method](/explicit-midpoint-method/) started by one Euler step. Gragg showed that its error has an expansion in even powers of the substep $h = H/n$ when $n$ is even. Extrapolating the $k$ results to $h = 0$ in powers of $h^2$ removes one more term of this expansion with every extra run. The final value has order $2k$, and the second best value gives an error estimate for free. Varying $k$ as well as $H$ turns the method into a variable-order solver that is very efficient for smooth problems at tight tolerances.

## In plain words

To cross a stretch of time, the method makes the same trip several times, first with 2 small steps, then 4, then 6, and so on. Each trip uses a simple rule that is only moderately accurate, but its error changes in a very regular way as the steps get smaller. Knowing this pattern, the method looks at how the answers change from trip to trip and predicts the answer an infinitely fine trip would give. The prediction from the last few trips is very accurate. The difference between the best and the second best prediction shows how much to trust it, and this decides whether the next stretch should be longer or shorter.

## The problem

**Notation.** As on all differential-equations pages: $y' = f(t, y)$ on $[t_0, T]$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$; $y_n \approx y(t_n)$; global error $e_n = y(t_n) - y_n$; order $p$; Lipschitz constant $L$; test equation $y' = \lambda y$ with $z = h\lambda$ and $R(z)$. Here $H$ is the big step and $h = H/n$ a substep.

The input is $f$, $t_0$, $y_0$, $T \ge t_0$, $\mathrm{rtol}$, $\mathrm{atol}$ and the number of stages $k \ge 2$. The output is the accepted points, ending exactly at $T$. The modified midpoint rule with $n$ substeps from $(t, y)$ is
$$z_0 = y, \quad z_1 = y + hf(t, y), \quad z_{m+1} = z_{m-1} + 2hf(t + mh, z_m) \quad (m = 1, \dots, n - 1),$$
and $T_{j,1} = z_{n_j}$. The implementation uses $n_j = 2j$ and polynomial extrapolation (the Aitken-Neville scheme)
$$T_{j,l} = T_{j,l-1} + \frac{T_{j,l-1} - T_{j-1,l-1}}{(n_j/n_{j-l+1})^2 - 1}, \qquad l = 2, \dots, j.$$
The step is accepted when the scaled max norm of $\mathrm{est} = T_{k,k} - T_{k,k-1}$ is at most 1.

## The algorithm

```pseudo id=main
GBS(f, t0, y0, T, rtol, atol, k)
L1  t ← t0, y ← y0, H ← starting step
L2  while t < T do
L3      if t + H ≥ T then H ← T − t                          ▷ the last step ends at T
L4      for j ← 1 to k do T_{j,1} ← modified midpoint from (t, y) over H with n_j = 2j substeps
L5          for l ← 2 to j do T_{j,l} ← T_{j,l−1} + (T_{j,l−1} − T_{j−1,l−1}) / ((n_j / n_{j−l+1})² − 1)
L6      err ← max_i |T_{k,k,i} − T_{k,k−1,i}| / (atol + rtol·max(|y_i|, |T_{k,k,i}|))
L7      if err ≤ 1 then t ← t + H, y ← T_{k,k}                     ▷ accept
L8      H ← H·min(4, max(0.2, 0.9·err^(−1/(2k−1))))               ▷ factor at most 1 after a rejection
L9  return the accepted points
```

All runs in L4 share $f(t, y)$, so the run with $n_j$ substeps costs $n_j - 1$ new evaluations. With $n_j = 2j$ an attempt costs $1 + \sum_{j=1}^k(2j - 1) = k^2 + 1$ evaluations, which is 17 for the default $k = 4$ (order 8). The estimate $T_{k,k} - T_{k,k-1}$ is the local error of the order $2k - 2$ value, which behaves like $CH^{2k-1}$. That is the reason for the exponent in L8.

## Example

**One step by hand.** Take $y' = y$, $y(0) = 1$, $H = 1$ and $k = 2$. With $n = 2$, $h = 0.5$: $z_1 = 1.5$, $z_2 = 1 + 2 \cdot 0.5 \cdot 1.5 = 2.5$. With $n = 4$, $h = 0.25$: $z_1 = 1.25$, $z_2 = 1.625$, $z_3 = 2.0625$, $z_4 = 2.65625$. Extrapolation gives
$$T_{2,2} = 2.65625 + \frac{2.65625 - 2.5}{(4/2)^2 - 1} = 2.708333 = \tfrac{65}{24},$$
against $e = 2.718282$. The estimate is $T_{2,2} - T_{2,1} = 5/96 = 0.052$. Here $65/24 = 1 + 1 + \tfrac12 + \tfrac16 + \tfrac1{24}$. On $y' = \lambda y$, $T_{k,k}$ is exactly the Taylor polynomial of $e^z$ of degree $2k$, which the tests check for $k = 2, 3, 4$. With $k = 4$ the same step gives $2.7182788$, an error of $3.1 \cdot 10^{-6}$.

**Fixed steps, observed order.** On $y' = -2ty^2$, $y(0) = 1$, exact solution $1/(1 + t^2)$, with $N$ equal big steps on $[0, 2]$, the error at $t = 2$ is:

| $N$ | $k = 1$ | $k = 2$ | $k = 3$ | $k = 4$ |
|---|---|---|---|---|
| 4 | $1.05 \cdot 10^{-2}$ | $5.21 \cdot 10^{-4}$ | $4.60 \cdot 10^{-6}$ | $2.94 \cdot 10^{-7}$ |
| 8 | $2.62 \cdot 10^{-3}$ | $2.65 \cdot 10^{-5}$ | $1.02 \cdot 10^{-7}$ | $5.31 \cdot 10^{-10}$ |
| 16 | $5.84 \cdot 10^{-4}$ | $1.49 \cdot 10^{-6}$ | $1.47 \cdot 10^{-9}$ | $1.75 \cdot 10^{-12}$ |
| 32 | $1.37 \cdot 10^{-4}$ | $8.79 \cdot 10^{-8}$ | $2.17 \cdot 10^{-11}$ | $6.27 \cdot 10^{-15}$ |
| last $\log_2$ ratio | 2.09 | 4.08 | 6.08 | 8.12 |

**Adaptive runs.** With $k = 4$ and $\mathrm{rtol} = \mathrm{atol} = \mathrm{tol}$ on the same problem:

| tol | accepted | rejected | evaluations | max error |
|---|---|---|---|---|
| $10^{-4}$ | 4 | 0 | 68 | $2.40 \cdot 10^{-5}$ |
| $10^{-6}$ | 5 | 0 | 85 | $3.05 \cdot 10^{-7}$ |
| $10^{-8}$ | 9 | 0 | 153 | $1.03 \cdot 10^{-9}$ |
| $10^{-10}$ | 16 | 2 | 306 | $7.65 \cdot 10^{-12}$ |
| $10^{-12}$ | 30 | 5 | 595 | $2.74 \cdot 10^{-14}$ |

At $10^{-12}$ this is fewer evaluations than the [Cash-Karp pair](/cash-karp-method/) needs on the same problem (793), and the error is smaller than the tolerance. At loose tolerances the big steps are wasted, because the first big step is already more accurate than needed.

## Correctness

The proofs are in `proofs/correctness.md`. In summary:

1. **Gragg's expansion.** If $f$ is smooth, the modified midpoint value after an even number $n$ of substeps satisfies $z_n = y(t + H) + \sum_{i=1}^{m}c_i(H)h^{2i} + O(h^{2m+2})$, with coefficients that are the same for all even $n$. This is Gragg's theorem. It is cited, and the proof file gives the reason for the even powers: the midpoint rule is symmetric.
2. **Extrapolation.** The Aitken-Neville scheme computes the value at $h^2 = 0$ of the polynomial in $h^2$ of degree $j - 1$ through the points $(h_i^2, T_{i,1})$. Hence $T_{j,j}$ removes the terms $h^2, \dots, h^{2j-2}$, and $T_{k,k} = y(t + H) + O(H^{2k+1})$. This part is proved. The tests check exactness on polynomials in $h^2$ with fractions.
3. **Order $2k$.** Combining 1 and 2, the local error of $T_{k,k}$ is $O(H^{2k+1})$, so the global error with fixed $H$ is $O(H^{2k})$. The table confirms orders 2, 4, 6 and 8.
4. **Estimate and termination.** $T_{k,k} - T_{k,k-1} = O(H^{2k-1})$ is asymptotically the local error of $T_{k,k-1}$. A rejected step shrinks $H$ by a factor below 0.9, so with $\mathrm{atol} > 0$ every step is eventually accepted. The last point is $T$ because of L3.

## Complexity

The cost model counts evaluations of $f$. Each attempt costs $k^2 + 1$ evaluations with $n_j = 2j$. The implementation recomputes $f(t, y)$ after a rejection, although it could keep it. The arithmetic is $\Theta(k^2d)$ per attempt for the midpoint runs and the extrapolation table, and the memory is $\Theta(k^2d)$ for the table (it can be reduced to $\Theta(kd)$). No Jacobians and no linear solves are needed. For a fixed $k$, the work to reach a tolerance $\mathrm{tol}$ grows like $\mathrm{tol}^{-1/(2k)}$. Variable-order codes choose $k$ to minimize the work per unit step, and for tight tolerances they choose large $k$.

## Properties

- **Explicit, order $2k$, arbitrary high order.** Higher order needs only one more midpoint run, not a new tableau.
- **Stability.** On the test equation, $R(z)$ is the Taylor polynomial of degree $2k$ of $e^z$ (for $n_j = 2j$). The real stability intervals are $[-2.785, 0]$ for $k = 2$, $[-3.554, 0]$ for $k = 3$ and $[-4.314, 0]$ for $k = 4$ (computed numerically, in units of $H$). Measured per evaluation of $f$, these regions are small, so the method is a poor choice for stiff problems.
- **Linear invariants.** Every value in the table is an affine combination of midpoint runs, each of which preserves linear invariants. So $T_{k,k}$ preserves them too.
- **Not symplectic.** The extrapolated value is not a symplectic map, even though the midpoint rule is symmetric.

## Variants and improvements

- **Order and step size control.** Deuflhard (1983) and the code ODEX of Hairer, Nørsett and Wanner change $k$ from step to step, estimating the work per unit step for neighbouring orders. This is the strength of extrapolation codes.
- **Rational extrapolation.** Bulirsch and Stoer used rational functions of $h^2$ and the sequence $2, 4, 6, 8, 12, 16, 24, \dots$. Later studies found polynomial extrapolation with $2, 4, 6, 8, \dots$ as good or better.
- **Gragg's smoothing step.** Replacing $z_n$ by $\tfrac14(z_{n-1} + 2z_n + z_{n+1})$ damps the weakly unstable oscillating component of the midpoint rule. It costs one more evaluation per run.
- **Linearly implicit extrapolation.** For stiff problems, extrapolating the linearly implicit Euler method (as in the codes SEULEX and SODEX) gives stable high-order methods. See [stiff ODE problems](/stiff-ode-problem/).
- **Second-order systems.** For $y'' = g(t, y)$, the Störmer rule has an expansion in $h^2$ as well, and extrapolating it directly is cheaper than rewriting the problem as a first-order system.

## When to use it

Use Bulirsch-Stoer for smooth non-stiff problems at tight tolerances, such as orbit computations, high-accuracy reference solutions and problems where $f$ is expensive and many digits are wanted. A variable-order code adapts well to changes in smoothness. Avoid it for loose tolerances, for problems with discontinuities in $f$ or its derivatives (the expansion fails across them), for stiff problems, and for long Hamiltonian runs where [symplectic integrators](/symplectic-integrators/) keep the energy bounded.

## Pitfalls

- **Mixed parity.** The coefficients of Gragg's expansion depend on whether $n$ is even or odd. Mixing even and odd $n_j$ makes the extrapolation lose the order, so use even $n_j$ only.
- **Stiffness.** On $y' = -1000(y - \cos t) - \sin t$ over $[0, 1]$, the $k = 4$ code needs 230 accepted and 47 rejected steps and about 4700 evaluations at $\mathrm{rtol} = 10^{-3}$. Cash-Karp needs about 1800. The big step is held near the stability bound $4.31/1000$, and each step costs 17 evaluations.
- **Non-smooth problems.** A kink in $f$ inside a big step breaks the asymptotic expansion. Extrapolation then makes the result worse, and the controller reacts with many rejections.
- **Error estimate at large $H$.** The estimate is asymptotic. For large $H$ the table may not have converged, and the estimate can be optimistic.
- **Rounding.** At order 8 and tolerances near $10^{-14}$, the differences in the extrapolation table lose digits. Do not ask for tolerances close to machine precision.

## Implementations

## History

Richardson (1927) introduced extrapolation to the limit. Romberg (1955) applied it repeatedly to the trapezoidal rule for integrals. Gragg (1964 thesis, 1965 paper) proved that the modified midpoint rule has an asymptotic error expansion in even powers of $h$, which makes it the natural base method for ODE extrapolation. Bulirsch and Stoer (1966) built the practical algorithm with rational extrapolation and step size control. Deuflhard (1983, 1985) and Hairer, Nørsett and Wanner developed the order control and the codes DIFEX and ODEX.

## References
