---
tag: 4QMRZ8
kind: algorithm
slug: adams-bashforth-methods
name: Adams-Bashforth methods
aliases:
- explicit Adams methods
- AB methods
area: numerical/differential-equations
level: core
summary: Explicit linear multistep methods that integrate the polynomial interpolating f at the last k points. The k-step method has order k and costs one evaluation of f per step.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps", k: "the number of steps in the formula", d: "the dimension of y"}
  time: {worst: "Θ(N k d)"}
  space: {extra: "Θ(k d)"}
  evaluations: {worst: "N + 4 k"}
properties: {deterministic: true, explicit: true, multistep: true, order: "k", zero_stable: true, a_stable: false, self_starting: false}
history:
  year: 1883
  people: [John Couch Adams, Francis Bashforth]
  note: Adams devised the method to integrate the equation of a capillary drop; it appeared in the 1883 book of Bashforth and Adams.
prereqs: [ode-initial-value-problem, polynomial-interpolation, euler-method]
see_also: [adams-moulton-methods, adams-bashforth-moulton-method, linear-multistep-methods, zero-stability, dahlquist-equivalence-theorem, backward-differentiation-formulas, classical-runge-kutta-4, absolute-stability]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section III.1 (explicit Adams methods, their coefficients and error constants), Sections III.2 to III.4 (order, stability and convergence of multistep methods), Section III.5 (variable step size)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 2, Section 2.1 (the Adams method) and Section 2.2 (order and convergence of multistep methods)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 4 (linear multistep methods; Adams methods, consistency, stability and convergence)
  - book: "F. Bashforth and J. C. Adams, An Attempt to Test the Theories of Capillary Action by Comparing the Theoretical and Measured Forms of Drops of Fluid, with an Explanation of the Method of Integration Employed, Cambridge University Press, 1883"
    locator: the explanation of the method of integration, by Adams
  - paper: "G. Dahlquist, Convergence and stability in the numerical integration of ordinary differential equations, Mathematica Scandinavica 4 (1956) 33-53"
    locator: convergence of linear multistep methods, consistency plus zero-stability
---

The Adams-Bashforth methods are explicit [linear multistep methods](/linear-multistep-methods/) for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$. The $k$-step method stores the last $k$ values of $f$, fits the polynomial of degree $k - 1$ through them, and integrates that polynomial over the next step. It has order $k$ and costs only one new evaluation of $f$ per step, whatever $k$ is, which made it the workhorse of hand computation and, in variable-order form, of non-stiff codes. In return it needs $k - 1$ starting values from another method, and its [stability region](/absolute-stability/) shrinks quickly as $k$ grows.

## In plain words

The method remembers the slopes it saw at the last few points. It draws the simplest smooth curve through those slopes and pretends the slope will keep following that curve during the next step. Adding up the predicted slope over the step gives the change in the solution. Because the old slopes are already known, each step needs only one new slope, at the point just reached. Using more old slopes makes the curve a better guess, so the method gets more accurate. But a guess that reaches further into the past also reacts more wildly to errors, so with many remembered slopes the step must be kept small, or the errors start to grow.

## The problem

**Notation.** As on all differential-equations pages: $y' = f(t, y)$ on $[t_0, T]$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$; step $h$, grid $t_n = t_0 + nh$, $y_n \approx y(t_n)$, $f_n = f(t_n, y_n)$; global error $e_n = y(t_n) - y_n$; order $p$; Lipschitz constant $L$; test equation $y' = \lambda y$ with $z = h\lambda$. A linear multistep method $\sum_{i=0}^k \alpha_i y_{n+i} = h\sum_{i=0}^k \beta_i f_{n+i}$ has the polynomials $\rho(\zeta) = \sum \alpha_i\zeta^i$ and $\sigma(\zeta) = \sum \beta_i\zeta^i$.

Integrating the ODE over one step gives $y(t_{n+1}) = y(t_n) + \int_{t_n}^{t_{n+1}} f(t, y(t))\,dt$. The $k$-step Adams-Bashforth method replaces the integrand by the [interpolating polynomial](/polynomial-interpolation/) $P$ of degree $k - 1$ with $P(t_{n-j}) = f_{n-j}$ for $j = 0, \dots, k - 1$:
$$y_{n+1} = y_n + h\sum_{j=0}^{k-1} \beta_{k,j}\, f_{n-j}, \qquad \beta_{k,j} = \int_0^1 \ell_j(s)\,ds,$$
where $\ell_j$ is the Lagrange basis polynomial on the nodes $0, -1, \dots, -(k-1)$ (time measured from $t_n$ in units of $h$). So $\rho(\zeta) = \zeta^k - \zeta^{k-1}$ and $\sigma(\zeta) = \sum_j \beta_{k,j}\zeta^{k-1-j}$. The weights are:

| $k$ | $\beta_{k,0}, \dots, \beta_{k,k-1}$ | order | error constant $\gamma_k$ |
|---|---|---|---|
| 1 | $1$ (explicit Euler) | 1 | $1/2$ |
| 2 | $\tfrac{3}{2}, -\tfrac{1}{2}$ | 2 | $5/12$ |
| 3 | $\tfrac{1}{12}(23, -16, 5)$ | 3 | $3/8$ |
| 4 | $\tfrac{1}{24}(55, -59, 37, -9)$ | 4 | $251/720$ |
| 5 | $\tfrac{1}{720}(1901, -2774, 2616, -1274, 251)$ | 5 | $95/288$ |

## The algorithm

```pseudo id=main
ADAMS-BASHFORTH(f, t0, y0, T, h, k)
L1  N ← ⌈(T − t0)/h⌉; if N = 0 return (t0, y0); h ← (T − t0)/N
L2  β_j ← ∫₀¹ ℓ_j(s) ds for j = 0, …, k − 1    ▷ exact, from the nodes 0, −1, …, −(k−1)
L3  y_0 ← y0, f_0 ← f(t0, y_0)
L4  for n = 0 to min(k − 1, N) − 1 do             ▷ starting values
L5      y_{n+1} ← one RK4 step from (t_n, y_n); f_{n+1} ← f(t_{n+1}, y_{n+1})
L6  for n = k − 1 to N − 1 do
L7      y_{n+1} ← y_n + h · Σ_{j=0}^{k−1} β_j f_{n−j}
L8      f_{n+1} ← f(t_{n+1}, y_{n+1})              ▷ the only new evaluation
L9  return (t_n, y_n) for n = 0, …, N
```

Line L1 shrinks the step so that $N$ equal steps end exactly at $T$; a multistep formula with constant coefficients needs an equally spaced grid, so the last step cannot simply be cut short. Lines L4 and L5 compute $y_1, \dots, y_{k-1}$ with the [classical Runge-Kutta method](/classical-runge-kutta-4/), whose local error $O(h^5)$ is small enough for $k \le 5$. Only the last $k$ values of $f$ are kept.

## Example

Take $y' = -2ty^2$, $y(0) = 1$, exact solution $y = 1/(1 + t^2)$, with $k = 2$ and $h = 0.1$. The starting step gives $y_1 = 0.9900989$ (exact $0.9900990$), and $f_0 = 0$, $f_1 = -2 \cdot 0.1 \cdot y_1^2 = -0.1960592$. Then
$$y_2 = y_1 + 0.1\big(\tfrac32 f_1 - \tfrac12 f_0\big) = 0.9900989 - 0.0294089 = 0.9606900,$$
against the exact $0.9615385$; the error $8.5 \cdot 10^{-4}$ is of the size $\gamma_2 h^3 |y'''|$, with $|y'''| \approx 2$ near $t = 0.1$, as the next section predicts.

On $[0, 2]$, the maximum error over the grid for several $k$ (observed, from the implementation) is:

| $h$ | $k = 1$ | $k = 2$ | $k = 3$ | $k = 4$ | $k = 5$ |
|---|---|---|---|---|---|
| 0.1 | $2.63 \cdot 10^{-2}$ | $5.75 \cdot 10^{-3}$ | $7.91 \cdot 10^{-4}$ | $6.49 \cdot 10^{-4}$ | $2.39 \cdot 10^{-4}$ |
| 0.05 | $1.25 \cdot 10^{-2}$ | $1.47 \cdot 10^{-3}$ | $1.42 \cdot 10^{-4}$ | $4.96 \cdot 10^{-5}$ | $6.38 \cdot 10^{-6}$ |
| 0.025 | $6.13 \cdot 10^{-3}$ | $3.72 \cdot 10^{-4}$ | $2.07 \cdot 10^{-5}$ | $3.31 \cdot 10^{-6}$ | $1.93 \cdot 10^{-7}$ |
| 0.0125 | $3.03 \cdot 10^{-3}$ | $9.34 \cdot 10^{-5}$ | $2.79 \cdot 10^{-6}$ | $2.11 \cdot 10^{-7}$ | $7.67 \cdot 10^{-9}$ |
| 0.00625 | $1.50 \cdot 10^{-3}$ | $2.34 \cdot 10^{-5}$ | $3.61 \cdot 10^{-7}$ | $1.33 \cdot 10^{-8}$ | $2.66 \cdot 10^{-10}$ |

The last ratios are $2^{1.01}, 2^{2.00}, 2^{2.95}, 2^{3.99}$ and $2^{4.85}$: order $k$, reached only for small $h$ when $k$ is large.

## Correctness

The proofs are in `proofs/correctness.md`. In summary:

1. **Local truncation error.** If $y \in C^{k+1}$, then $\tau_{n+1} = y(t_{n+1}) - y(t_n) - h\sum_j\beta_{k,j}y'(t_{n-j})$ satisfies $\|\tau_{n+1}\| \le \gamma_k M_{k+1}h^{k+1}$ with $M_{k+1} = \max\|y^{(k+1)}\|$ and $\gamma_k = \int_0^1 \binom{s + k - 1}{k}ds$. For scalar $y$, $\tau_{n+1} = \gamma_k h^{k+1}y^{(k+1)}(\xi)$ exactly, so the order is exactly $k$. The weights and constants are checked exactly with fractions in the tests.
2. **Zero-stability.** $\rho(\zeta) = \zeta^{k-1}(\zeta - 1)$ has the simple root 1 and the root 0, so the method is [zero-stable](/zero-stability/) for every $k$.
3. **Convergence.** If $f$ is $L$-Lipschitz in $y$, $B = \sum_j|\beta_{k,j}|$, and the starting errors satisfy $\max_{m<k}\|e_m\| \le \delta$, then $\|e_n\| \le e^{LB(t_n - t_0)}\delta + \gamma_kM_{k+1}h^k(e^{LB(t_n - t_0)} - 1)/(LB)$. With RK4 starting values, $\delta = O(h^5)$, so the implementation has order $\min(k, 5)$, proved under these hypotheses.

## Complexity

The cost model counts evaluations of $f$. After the start each step costs one evaluation. In the implementation the start costs $1 + 5(k - 1)$ evaluations and the last step needs none, so the total is $N + 4(k - 1)$ for $N \ge k - 1$. The arithmetic is $\Theta(kd)$ per step and the memory is $k$ vectors of $f$ values. For the same order, RK4 needs 4 evaluations per step; AB4 needs 1, but its smaller stability region often forces a smaller step.

## Properties

- **Explicit, order $k$, error constant $\gamma_k$** as in the table. The constants decrease slowly, from $1/2$ to about $0.3$.
- **Stability.** The intersection of the region of [absolute stability](/absolute-stability/) with the negative real axis is $[-2, 0]$ for $k = 1$, $[-1, 0]$ for $k = 2$, $[-6/11, 0]$ for $k = 3$, $[-3/10, 0]$ for $k = 4$ and $[-90/551, 0] \approx [-0.163, 0]$ for $k = 5$ (computed with a root finder). The regions are bounded, so no Adams-Bashforth method is A-stable; they are unsuited to [stiff problems](/stiff-ode-problem/).
- **Strongly stable.** All roots of $\rho$ other than 1 are 0, so parasitic solutions are damped at once when $h\lambda$ is small.
- **Not self-starting.** The first $k - 1$ values must come from elsewhere, and their errors enter the global error with a factor bounded by $e^{LB(T - t_0)}$.

## Variants and improvements

- **[Adams-Moulton methods](/adams-moulton-methods/).** The implicit counterpart: the interpolation includes the unknown $f_{n+1}$, giving order $k + 1$ from $k$ steps and smaller error constants.
- **[Predictor-corrector](/adams-bashforth-moulton-method/).** An Adams-Bashforth predictor followed by an Adams-Moulton corrector (PECE) gives a method that is still explicit, more stable and has a free error estimate.
- **Variable step size and order.** Writing the interpolant with divided differences (Krogh) or in Nordsieck form allows the step and the order to change from step to step. This is how DE/STEP (Shampine and Gordon), LSODE in Adams mode and MATLAB's ode113 work.
- **Starting by order increase.** Variable-order codes start with $k = 1$ and a very small step, raising $k$ as values accumulate, so no separate starting method is needed.

## When to use it

Adams-Bashforth methods suit non-stiff problems where $f$ is expensive, such as orbit computations and $N$-body problems with smooth forces, because accuracy is cheap in evaluations of $f$. They are also used as time steppers for the nonlinear terms of PDE codes (AB2 and AB3, often paired with an implicit method for the linear terms). For a fixed step and moderate accuracy RK4 is simpler. For stiff problems use [BDF](/backward-differentiation-formulas/).

## Pitfalls

- **Bad starting values.** Starting AB4 with explicit Euler steps limits the global order to 2, because the starting errors are $O(h^2)$ and are propagated, not damped.
- **Changing the step.** The weights hold only for equal spacing. Changing $h$ and reusing old values as if they were equally spaced makes the method inconsistent; resample by interpolation or use variable-step weights.
- **Stiffness.** On $y' = -1000(y - \cos t)$ with $h = 0.01$, AB2 has $z = -10$, far outside $[-1, 0]$, and the solution explodes; with $h = 0.0005$ ($z = -0.5$) it is accurate.
- **Large $k$ does not always pay.** With $h = 0.1$ in the table above AB4 is barely better than AB3, because the stability and the error constants, not only the order, govern the error at moderate $h$.

## Implementations

## History

J. C. Adams designed the method around 1855 and published it in the 1883 book by Francis Bashforth and Adams on the shapes of drops of fluid, where it integrated the capillary equation. F. R. Moulton added the implicit corrector in 1926 for ballistics. Dahlquist (1956) proved that consistency and zero-stability together are equivalent to convergence for all linear multistep methods, which covers the Adams methods. Hairer, Nørsett and Wanner tell this history in Section III.1.

## References
