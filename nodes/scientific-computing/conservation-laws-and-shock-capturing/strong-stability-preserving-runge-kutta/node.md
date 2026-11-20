---
tag: 4YEW5E
kind: algorithm
slug: strong-stability-preserving-runge-kutta
name: Strong stability preserving Runge-Kutta methods
aliases:
- SSP Runge-Kutta methods
- TVD Runge-Kutta methods
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: Explicit Runge-Kutta methods that are convex combinations of forward Euler steps, so they keep the TVD or positivity property under a scaled CFL limit.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {s: "the number of stages", K: "the number of time steps", M: "the number of unknowns of the semidiscrete system"}
  time: {worst: "O(K s^2 M)"}
  space: {extra: "O(s M)"}
  evaluations: {worst: "K s"}
properties: {deterministic: true, explicit: true, ssp_coefficient: "1 for SSPRK(2,2) and SSPRK(3,3), 6 for SSPRK(10,4)", max_order_with_positive_ssp_coefficient: "4"}
history:
  year: 1988
  people: [C.-W. Shu, S. Osher, S. Gottlieb, E. Tadmor, D. I. Ketcheson]
  note: Shu and Osher (1988) wrote Runge-Kutta steps as convex combinations of forward Euler steps and gave the third-order TVD method. Gottlieb, Shu and Tadmor (2001) named the class strong stability preserving.
prereqs: [runge-kutta-methods, euler-method, method-of-lines, total-variation-diminishing]
see_also: [classical-runge-kutta-4, stability-region, courant-friedrichs-lewy-condition, weno-scheme, muscl-scheme, positivity-preserving-limiter, runge-kutta-discontinuous-galerkin, godunov-order-barrier]
sources:
  - paper: doi:10.1016/0021-9991(88)90177-5
    title: Chi-Wang Shu and Stanley Osher, Efficient implementation of essentially non-oscillatory shock-capturing schemes, Journal of Computational Physics 77(2) (1988) 439-471
    locator: the Shu-Osher form and the third-order TVD Runge-Kutta method
  - paper: doi:10.1090/S0025-5718-98-00913-2
    title: Sigal Gottlieb and Chi-Wang Shu, Total variation diminishing Runge-Kutta schemes, Mathematics of Computation 67(221) (1998) 73-85
    locator: optimal second- and third-order methods, no four-stage fourth-order method with a positive SSP coefficient, the example of a non-TVD second-order method
  - paper: "Sigal Gottlieb, Chi-Wang Shu and Eitan Tadmor, Strong stability-preserving high-order time discretization methods, SIAM Review 43(1) (2001) 89-112"
    locator: survey, the name strong stability preserving
  - paper: "Steven J. Ruuth and Raymond J. Spiteri, Two barriers on strong-stability-preserving time discretization methods, Journal of Scientific Computing 17 (2002) 211-220"
    locator: no explicit SSP Runge-Kutta method of order five with a positive SSP coefficient
  - paper: doi:10.1137/07070485X
    title: David I. Ketcheson, Highly efficient strong stability-preserving Runge-Kutta methods with low-storage implementations, SIAM Journal on Scientific Computing 30(4) (2008) 2113-2136
    locator: the ten-stage fourth-order method SSPRK(10,4) with SSP coefficient 6 and its low-storage form
  - book: isbn:9789814289269
    title: Sigal Gottlieb, David Ketcheson and Chi-Wang Shu, Strong Stability Preserving Runge-Kutta and Multistep Time Discretizations, World Scientific, 2011
    locator: the SSP coefficient, optimal explicit methods, order barriers
---

Strong stability preserving (SSP) Runge-Kutta methods are explicit [Runge-Kutta methods](/runge-kutta-methods/) for the system $u' = L(u)$ that a spatial discretization of a conservation law gives by the [method of lines](/method-of-lines/). Each stage is a convex combination of [forward Euler](/euler-method/) steps. So if forward Euler keeps a convex property for $\Delta t \le \Delta t_{FE}$, such as a [TVD](/total-variation-diminishing/) bound, a maximum principle or positive density, the SSP method keeps it for $\Delta t \le C\,\Delta t_{FE}$, where $C$ is the SSP coefficient of the method. The SSP methods reach higher order in time without losing the nonlinear stability that a limiter gives the space discretization. The classical [fourth-order method](/classical-runge-kutta-4/) is not SSP: its coefficient is 0.

## In plain words

A shock-capturing scheme is often built so that one simple time step, the forward Euler step, never creates new wiggles if the step is small enough. But that simple step is only first order accurate in time. A higher-order Runge-Kutta method mixes several evaluations, and some mixtures do create wiggles even when each simple step would not. SSP methods use only mixtures with positive weights that add up to one. Each stage is then an average of simple steps. An average of results that have no new wiggles has no new wiggles either. The price is a smaller allowed step for some methods, and a limit on the order.

## The problem

Given $L : \mathbb{R}^M \to \mathbb{R}^M$, a convex functional $\|\cdot\|$ (a norm, the total variation, or the indicator of a convex set), and a step $\Delta t_{FE}$ such that $\|u + \Delta t\,L(u)\| \le \|u\|$ for all $0 \le \Delta t \le \Delta t_{FE}$, find an explicit time stepping method of order $p > 1$ that keeps $\|u^{n+1}\| \le \|u^n\|$ for a step $\Delta t \le C\,\Delta t_{FE}$ with $C$ as large as possible.

## The algorithm

A method with $s$ stages is given in Shu-Osher form by lower triangular tables $\alpha_{ik}$ and $\beta_{ik}$ with $\sum_k\alpha_{ik} = 1$.

```pseudo id=main
SSP-RK-STEP(u, Δt, L, α, β)
L1  y_0 ← u
L2  for i ← 1 to s do
L3      y_i ← Σ over k < i of (α_ik y_k + Δt β_ik L(y_k))      ▷ each L(y_k) is computed once
L4  return y_s
SSP-COEFFICIENT(α, β)
L5  if some α_ik < 0 or β_ik < 0 then return 0
L6  return the minimum of α_ik/β_ik over all β_ik > 0
```

The methods on this page, with $L_k = L(y_k)$:

- **SSPRK(2,2)** ($C = 1$): $y_1 = u + \Delta t L_0$, $u^{n+1} = \frac12u + \frac12(y_1 + \Delta t L_1)$. This is Heun's method.
- **SSPRK(3,3)** ($C = 1$, Shu and Osher 1988): $y_1 = u + \Delta t L_0$, $y_2 = \frac34u + \frac14(y_1 + \Delta t L_1)$, $u^{n+1} = \frac13u + \frac23(y_2 + \Delta t L_2)$.
- **SSPRK(10,4)** ($C = 6$, Ketcheson 2008): $y_i = y_{i-1} + \frac{\Delta t}{6}L_{i-1}$ for $i = 1, \dots, 4$; $y_5 = \frac35u + \frac25(y_4 + \frac{\Delta t}{6}L_4)$; $y_i = y_{i-1} + \frac{\Delta t}{6}L_{i-1}$ for $i = 6, \dots, 9$; $u^{n+1} = \frac1{25}u + \frac9{25}(y_4 + \frac{\Delta t}{6}L_4) + \frac35(y_9 + \frac{\Delta t}{6}L_9)$.

The effective coefficient $C/s$ compares methods with different numbers of stages at equal cost: it is $\frac12$ for SSPRK(2,2), $\frac13$ for SSPRK(3,3) and $0.6$ for SSPRK(10,4).

## Example

**One step by hand.** Take upwind advection $L(u)_j = -(u_j - u_{j-1})$ with $\Delta x = 1$ on 4 periodic points. Forward Euler is TVD and keeps the values in $[0, 1]$ for $\Delta t \le 1$. With SSPRK(2,2), $\Delta t = \frac12$ and $u = (1, 0, 0, 0)$, the first stage is $y_1 = (\frac12, \frac12, 0, 0)$. The forward Euler step from $y_1$ is $(\frac14, \frac12, \frac14, 0)$, and the average with $u$ gives

$$u^{n+1} = \tfrac12(1, 0, 0, 0) + \tfrac12\big(\tfrac14, \tfrac12, \tfrac14, 0\big) = \big(\tfrac58, \tfrac14, \tfrac18, 0\big).$$

The values stay in $[0, 1]$, the sum stays 1, and the total variation falls from 2 to $\frac54$.

**Observed orders** (measurement, with the code on this page). Error at $t = 1$ for $u' = -u^2$, $u(0) = 1$, exact $u(1) = \frac12$:

| method | $\Delta t = 0.1$ | $0.05$ | $0.025$ | last ratio |
|---|---|---|---|---|
| forward Euler | 1.829e-2 | 8.895e-3 | 4.389e-3 | 2.03 |
| SSPRK(2,2) | 6.712e-4 | 1.621e-4 | 3.979e-5 | 4.07 |
| SSPRK(3,3) | 3.497e-5 | 4.137e-6 | 5.026e-7 | 8.23 |
| SSPRK(10,4) | 3.321e-8 | 2.096e-9 | 1.315e-10 | 15.94 |

**A second-order method that is not SSP** (measurement). Gottlieb and Shu (1998) give the second-order method $u^{(1)} = u - 20\Delta t\,L(u)$, $u^{n+1} = u + \Delta t\big(\frac{41}{40}L(u) - \frac1{40}L(u^{(1)})\big)$, which has a negative coefficient. Take [Burgers' equation](/burgers-equation/) on 40 periodic cells with $\Delta x = 1$, a MUSCL space discretization with minmod slopes and the Godunov flux, the data $u = 1$ on cells 0 to 19 and $u = -0.5$ on cells 20 to 39, and $\Delta t = 0.3$. In 26 steps the total variation of that method rises from 3 to 3.1398, and the maximum rises to 1.0699. SSPRK(2,2) with the same $L$ and the same step keeps the total variation at 3 and the values in $[-0.5, 1]$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: if all $\alpha_{ik}$ and $\beta_{ik}$ are nonnegative and $C > 0$, each stage is $y_i = \sum_k\alpha_{ik}\big(y_k + (\beta_{ik}/\alpha_{ik})\Delta t\,L(y_k)\big)$, a convex combination of forward Euler steps of size at most $\Delta t/C$. Convexity and induction over the stages give $\|u^{n+1}\| \le \|u^n\|$ for $\Delta t \le C\,\Delta t_{FE}$. The proof also checks the coefficients and the orders of SSPRK(2,2) and SSPRK(3,3) from the Butcher conditions, and shows that $C \le s$ for every explicit method with $s$ stages. The order of SSPRK(10,4) is cited and measured.

## Complexity

Theorem: one step evaluates $L$ once per stage, $s$ times, and forms the stage sums in $O(s^2M)$ operations in the general form. For the methods above most $\alpha_{ik}$ are zero, and the sums cost $O(sM)$. The general form stores all stages, $O(sM)$ memory. Many SSP methods, SSPRK(10,4) among them, have low-storage forms with two or three registers of size $M$ (Ketcheson 2008). In practice the cost of $L$ dominates.

## Properties

- **Convex combination of forward Euler steps**, so any convex bound of forward Euler is kept: TVD, maximum principle, positivity, an entropy inequality of a fully discrete form.
- **Sufficient, not necessary.** $\Delta t \le C\,\Delta t_{FE}$ is a guarantee. For a given $L$ a larger step may still keep the bound.
- **Order barriers** (theorems, cited). No four-stage fourth-order explicit method has $C > 0$ (Gottlieb and Shu 1998), and no explicit method of order five or more has $C > 0$ (Ruuth and Spiteri 2002).
- **$C \le s$** for explicit methods with $s$ stages, so the effective coefficient is at most 1.
- **Optimal methods.** SSPRK(2,2) and SSPRK(3,3) have the largest $C$ among methods with as many stages as their order (Gottlieb and Shu 1998).

## Variants and improvements

- **More stages.** SSPRK(s,2) with $C = s - 1$ and SSPRK(s,3) methods with larger effective coefficients, and SSPRK(10,4) for order four.
- **Low-storage forms.** Only two or three arrays of size $M$, important for large 3D runs.
- **Multistep and multistep multistage SSP methods**, and implicit SSP methods. Implicit SSP methods also have bounded $C$, so they do not allow arbitrarily large steps.
- **Downwind operators.** Methods with negative $\beta$ need a second operator $\tilde L$ that is stable backward in time. They avoid some of the order barriers, at the cost of a second operator.
- **With limiters.** [WENO](/weno-scheme/), [MUSCL](/muscl-scheme/) and the [Runge-Kutta discontinuous Galerkin method](/runge-kutta-discontinuous-galerkin/) use SSP time stepping, and a [positivity-preserving limiter](/positivity-preserving-limiter/) relies on it.

## When to use it

Use an SSP method whenever the space discretization is proved TVD, monotone or positive only for forward Euler: limited finite volume schemes, WENO, DG with a limiter. SSPRK(3,3) is the usual default. SSPRK(10,4) gives order four with a larger stable step per evaluation. For smooth problems without limiters, where no nonlinear bound is needed, a method with a large [stability region](/stability-region/), such as classical RK4, can be more efficient.

## Pitfalls

- **A non-SSP method with a TVD space discretization.** The bound can fail, as in the example. Classical RK4 and many embedded pairs have $C = 0$.
- **The wrong step limit.** The guarantee is $\Delta t \le C\,\Delta t_{FE}$, where $\Delta t_{FE}$ is the forward Euler limit of the space discretization, for example $\frac12$ of the CFL limit for MUSCL with minmod. It is not the linear stability limit.
- **Boundary conditions inside the stages.** Apply the boundary conditions at each stage time, or the order drops near the boundary.
- **Time-dependent sources.** Evaluate $L(t, u)$ at the stage times $t_n + c_i\Delta t$, not at $t_n$.
- **The effective coefficient.** Compare methods by $C/s$, not by $C$: SSPRK(10,4) allows a step six times larger but costs ten evaluations.

## Implementations

## History

Shu and Osher (1988) wrote explicit Runge-Kutta methods as convex combinations of forward Euler steps and gave the third-order TVD method that is now SSPRK(3,3). Gottlieb and Shu (1998) found the optimal second- and third-order methods and proved that no four-stage fourth-order method has a positive coefficient. Gottlieb, Shu and Tadmor (2001) introduced the name strong stability preserving. Ruuth and Spiteri (2002) proved the order barrier for explicit methods, and Ketcheson (2008) gave efficient low-storage methods such as SSPRK(10,4). The book by Gottlieb, Ketcheson and Shu (2011) collects the theory.

## References
