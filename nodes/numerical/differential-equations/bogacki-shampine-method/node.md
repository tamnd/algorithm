---
tag: 34RG05
kind: algorithm
slug: bogacki-shampine-method
name: Bogacki-Shampine method
aliases:
- BS23
- ode23
- Bogacki-Shampine 3(2) pair
area: numerical/differential-equations
level: core
summary: An embedded explicit Runge-Kutta pair of orders 3 and 2 with the FSAL property. Each accepted step costs three new evaluations of f and gives an error estimate for adaptive step control.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of accepted steps", R: "the number of rejected steps", d: "the dimension of y"}
  time: {worst: "Θ((N + R) d)"}
  space: {extra: "Θ(d)"}
  evaluations: {worst: "1 + 3 (N + R)"}
properties: {deterministic: true, explicit: true, one_step: true, order: "3", embedded_order: "2", stages: "4", fsal: true, a_stable: false, error_estimate: true}
history:
  year: 1989
  people: [Przemyslaw Bogacki, Lawrence F. Shampine]
  note: Bogacki and Shampine published the pair in 1989. It became the method of the MATLAB solver ode23 described by Shampine and Reichelt in 1997.
prereqs: [butcher-tableau, adaptive-step-size-control]
see_also: [embedded-runge-kutta-pairs, dormand-prince-method, runge-kutta-fehlberg-method, cash-karp-method, classical-runge-kutta-4, butcher-order-conditions, absolute-stability, dense-output]
sources:
  - paper: doi:10.1016/0893-9659(89)90079-7
    title: "P. Bogacki and L. F. Shampine, A 3(2) pair of Runge-Kutta formulas, Applied Mathematics Letters 2 (1989) 321-325"
    locator: the tableau, the FSAL construction and the choice of the free parameters
  - paper: doi:10.1137/S1064827594276424
    title: "L. F. Shampine and M. W. Reichelt, The MATLAB ODE Suite, SIAM Journal on Scientific Computing 18 (1997) 1-22"
    locator: Section 2 (the explicit solvers ode23 and ode45)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.4 (error estimation and step size control, the starting step size) and Section II.5 (embedded formulas and FSAL)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 3, Section 33 (embedded methods and error estimation)
---

The Bogacki-Shampine method, often called BS23 or by the name of the MATLAB solver ode23, is an [embedded Runge-Kutta pair](/embedded-runge-kutta-pairs/) for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$. From one set of four stages it forms a solution of order 3, which is kept, and a solution of order 2, which is used only to estimate the local error. The fourth stage is $f$ at the new solution, so it is also the first stage of the next step. This property is called FSAL, first same as last. An accepted step therefore costs three new evaluations of $f$. The error estimate drives [adaptive step size control](/adaptive-step-size-control/). The method suits non-stiff problems at modest accuracy, roughly tolerances from $10^{-2}$ to $10^{-6}$.

## In plain words

Each step computes the new value in two ways from the same slope samples. One way is accurate, the other is a little rougher. Their difference tells the solver how large the error of the rough answer is, and so gives an upper guide for the error of the step. If the difference is small enough compared with what the user asked for, the step is accepted and the accurate value is kept. If not, the step is thrown away and tried again with a smaller step. In both cases the size of the difference also suggests the next step size: larger when things are calm, smaller when they change fast. The last slope sample of a step is taken at the new point, so the next step reuses it for free.

## The problem

**Notation.** As on all differential-equations pages: $y' = f(t, y)$ on $[t_0, T]$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$; step $h$; $y_n \approx y(t_n)$; global error $e_n = y(t_n) - y_n$; order $p$; Lipschitz constant $L$; test equation $y' = \lambda y$ with $z = h\lambda$ and stability function $R(z)$. Here the grid is not uniform: $t_{n+1} = t_n + h_n$, and the step sizes $h_n$ are chosen by the method.

The input is $f$, $t_0$, $y_0$, $T \ge t_0$, a relative tolerance $\mathrm{rtol}$ and an absolute tolerance $\mathrm{atol}$. The output is the list of accepted points $(t_n, y_n)$, ending exactly at $T$. The [Butcher tableau](/butcher-tableau/) is
$$\begin{array}{c|cccc} 0 & & & & \\ \tfrac12 & \tfrac12 & & & \\ \tfrac34 & 0 & \tfrac34 & & \\ 1 & \tfrac29 & \tfrac13 & \tfrac49 & \\ \hline b & \tfrac29 & \tfrac13 & \tfrac49 & 0 \\ \hat b & \tfrac{7}{24} & \tfrac14 & \tfrac13 & \tfrac18 \end{array}$$
The last row of $A$ equals $b$, which is what makes FSAL work. A step is accepted when
$$\mathrm{err} = \max_i \frac{|\mathrm{est}_i|}{\mathrm{atol} + \mathrm{rtol}\cdot\max(|y_{n,i}|, |y_{n+1,i}|)} \le 1, \qquad \mathrm{est} = y_{n+1} - \hat y_{n+1} = h\sum_{j=1}^4(b_j - \hat b_j)k_j.$$

## The algorithm

```pseudo id=main
BS23(f, t0, y0, T, rtol, atol)
L1  t ← t0, y ← y0, k1 ← f(t, y), choose a starting h
L2  while t < T do
L3      if t + h ≥ T then h ← T − t                    ▷ the last step ends at T
L4      k2 ← f(t + h/2, y + (h/2)·k1)
L5      k3 ← f(t + 3h/4, y + (3h/4)·k2)
L6      y′ ← y + h·(2/9·k1 + 1/3·k2 + 4/9·k3)
L7      k4 ← f(t + h, y′), est ← h·(−5/72·k1 + 1/12·k2 + 1/9·k3 − 1/8·k4)
L8      err ← max_i |est_i| / (atol + rtol·max(|y_i|, |y′_i|))
L9      if err ≤ 1 then t ← t + h, y ← y′, k1 ← k4         ▷ accept; FSAL
L10     h ← h·min(5, max(0.2, 0.9·err^(−1/3)))            ▷ factor at most 1 after a rejection
L11 return the accepted points
```

Line L7 computes the estimate directly from the weights $b - \hat b = (-5/72, 1/12, 1/9, -1/8)$, so $\hat y$ is never formed. Line L10 uses the exponent $1/3$ because the estimate behaves like $Ch^3$: it is the local error of the order-2 solution. The factor 0.9 is a safety factor, and the bounds 0.2 and 5 stop the step from changing too abruptly. The starting step in the implementation is $0.01\,\|y_0\|/\|f(t_0, y_0)\|$ in the scaled norm, a simplified form of the rule in Hairer, Nørsett and Wanner, Section II.4.

## Example

**One step by hand.** Take $y' = -2ty^2$, $y(0) = 1$, exact solution $y = 1/(1 + t^2)$, and $h = 0.5$. Then $k_1 = 0$, $k_2 = f(0.25, 1) = -0.5$, $k_3 = f(0.375, 0.8125) = -0.4951172$, and
$$y_1 = 1 + 0.5\,\big(\tfrac13(-0.5) + \tfrac49(-0.4951172)\big) = 0.806640625,$$
against the exact $0.8$. Next $k_4 = f(0.5, 0.806640625) = -0.6506691$, and the estimate is $\mathrm{est} = -0.0076730$. With $\mathrm{rtol} = \mathrm{atol} = 10^{-3}$ the scale is $2 \cdot 10^{-3}$, so $\mathrm{err} = 3.84$. The step is rejected and retried with $h = 0.5 \cdot 0.9 \cdot 3.84^{-1/3} = 0.2875$. That step is accepted, with $y = 0.9239868$ at $t = 0.2875$ (error $3.1 \cdot 10^{-4}$). The whole run to $T = 2$ from $h_0 = 0.5$ takes 6 accepted and 2 rejected steps, and $1 + 3 \cdot 8 = 25$ evaluations.

**Fixed steps, observed order.** Without step control, on the same problem, the error at $t = 2$ is:

| $h$ | error at $t = 2$ | $\log_2$ of the ratio |
|---|---|---|
| 0.2 | $1.7886 \cdot 10^{-4}$ | |
| 0.1 | $2.0271 \cdot 10^{-5}$ | 3.14 |
| 0.05 | $2.4082 \cdot 10^{-6}$ | 3.07 |
| 0.025 | $2.9335 \cdot 10^{-7}$ | 3.04 |
| 0.0125 | $3.6194 \cdot 10^{-8}$ | 3.02 |

**Adaptive runs.** With $\mathrm{rtol} = \mathrm{atol} = \mathrm{tol}$ and the automatic starting step, on $[0, 2]$:

| tol | accepted | rejected | evaluations | max error on the grid |
|---|---|---|---|---|
| $10^{-3}$ | 14 | 1 | 46 | $6.19 \cdot 10^{-3}$ |
| $10^{-4}$ | 19 | 3 | 67 | $5.64 \cdot 10^{-4}$ |
| $10^{-5}$ | 31 | 3 | 103 | $6.40 \cdot 10^{-5}$ |
| $10^{-6}$ | 58 | 5 | 190 | $5.22 \cdot 10^{-6}$ |
| $10^{-7}$ | 116 | 5 | 364 | $5.86 \cdot 10^{-7}$ |

In this run the global error is about 6 times the tolerance, and the number of steps grows by about $10^{1/3} \approx 2.15$ per decade of tolerance. These are observations on one problem. The method controls the local error per step and gives no guarantee on the global error. Every row satisfies evaluations $= 1 + 3\,(\text{accepted} + \text{rejected})$, which is the FSAL count.

## Correctness

The proofs are in `proofs/correctness.md`. In summary:

1. **Orders.** With exact fractions, $b$ satisfies the four [order conditions](/butcher-order-conditions/) for trees with at most 3 vertices. It fails two of the four conditions of order 4: $\sum b_ic_i^3 = 11/48 \ne 1/4$ and $\sum b_ia_{ij}a_{jk}c_k = 0 \ne 1/24$. So $y_{n+1}$ has order exactly 3. The weights $\hat b$ satisfy the conditions of order 2 and fail $\sum\hat b_ic_i^2 = 3/8 \ne 1/3$, so $\hat y_{n+1}$ has order exactly 2.
2. **The estimate.** If $f$ is $C^3$, then $\mathrm{est} = \hat\tau_{n+1} + O(h^4)$, where $\hat\tau_{n+1} = O(h^3)$ is the local error of the order-2 solution. This is asymptotic. Since the kept solution has local error $O(h^4)$, the test $\mathrm{err} \le 1$ asks, for small $h$, that a bound for the local error of the kept solution be below the tolerance.
3. **Termination and the final point.** Each pass of the loop either accepts a step and advances $t$, or rejects it and multiplies $h$ by at most $0.9 \cdot \mathrm{err}^{-1/3} < 0.9$. For $f$ with bounded derivatives the estimate tends to 0 as $h \to 0$, so a step is accepted after finitely many rejections, unless the step size underflows. The clipping in L3 makes the last accepted point equal $T$. The implementation also stops after a maximum number of attempts.
4. **Convergence as tol tends to 0.** For fixed step sequences the pair converges with order 3, by the usual one-step argument for an increment that is Lipschitz in $y$. For the adaptive method, results that relate the global error to the tolerance hold only under extra assumptions on the controller. They are cited, not proved, here.

## Complexity

The cost model counts evaluations of $f$. The first stage costs one evaluation. Every attempted step, accepted or rejected, costs three more: $k_2$, $k_3$ and $k_4$. A rejected step keeps $k_1$, because $t$ and $y$ do not change. The total is $1 + 3\,(N + R)$, where $N$ is the number of accepted steps and $R$ the number of rejected steps. The arithmetic is $\Theta(d)$ per stage, and the memory is a few vectors of length $d$. No Jacobians and no linear solves are needed. On a smooth problem the step size is about $(\mathrm{tol}/C)^{1/3}$, so the work grows like $\mathrm{tol}^{-1/3}$. That is why higher-order pairs such as [Dormand-Prince](/dormand-prince-method/) are cheaper at tight tolerances.

## Properties

- **Explicit, 4 stages, 3 new evaluations per step.** Without FSAL, a 3-stage order-3 method plus a separate estimate would need at least 4 evaluations per step.
- **Local extrapolation.** The method continues with the order-3 solution, while the estimate is the error of the order-2 solution. For small $h$ the estimate is therefore pessimistic for the value kept.
- **Stability function.** Every explicit 3-stage method of order 3 has $R(z) = 1 + z + z^2/2 + z^3/6$. The 4th stage of BS23 does not enter $y_{n+1}$ (its weight is $b_4 = 0$). The real stability interval is $[-2.5127, 0]$, and since $|R(iy)|^2 = 1 - y^4/12 + y^6/36$, the imaginary interval is $[-\sqrt3, \sqrt3]i$. The method is not [A-stable](/a-stability/).
- **Interpolant.** The stages give a free cubic Hermite interpolant on each step, using $y_n$, $y_{n+1}$, $k_1$ and $k_4$. This is a [dense output](/dense-output/) of order 3.

## Variants and improvements

- **Higher-order pairs.** [Dormand-Prince 5(4)](/dormand-prince-method/) (ode45) also uses FSAL and is the default for tighter tolerances. [Runge-Kutta-Fehlberg 4(5)](/runge-kutta-fehlberg-method/) and [Cash-Karp](/cash-karp-method/) are other well-known pairs.
- **Controllers.** The elementary controller of line L10 can be replaced by a PI controller, which uses the last two error estimates and gives smoother step sequences. See [adaptive step size control](/adaptive-step-size-control/).
- **Error per unit step.** Some codes divide the estimate by $h$, which changes the exponent in L10 to $1/2$.
- **Norm.** ode23 uses a max norm of the scaled error as above. Other codes use a root mean square norm, which is smoother but can hide a large error in one component.

## When to use it

Use BS23 for non-stiff problems when a few digits are enough. Typical cases are rough tolerances, plotting, problems with only moderate smoothness and early experiments, where its low cost per step and robustness pay off. For tolerances below about $10^{-6}$, a fifth-order pair needs far fewer steps. For stiff problems use an implicit method such as [BDF](/backward-differentiation-formulas/) or a Rosenbrock method (ode23s in MATLAB).

## Pitfalls

- **Stiffness.** On $y' = -1000(y - \cos t) - \sin t$, $y(0) = 1$, over $[0, 1]$ the solution is just $\cos t$. Yet BS23 takes about 400 steps, both with $\mathrm{rtol} = 10^{-3}$ (397 accepted, 4 rejected) and with $\mathrm{rtol} = 10^{-6}$ (394 accepted, 133 rejected). The step size is held near $2.51/1000$ by the stability interval, not by accuracy. A step count that does not fall when the tolerance is loosened is the typical sign of stiffness.
- **Zero or tiny tolerances.** With $\mathrm{atol} = 0$ and a solution component that passes through 0, the scale becomes 0 and the test can never pass. Keep $\mathrm{atol} > 0$ for such components.
- **Global error.** The tolerance bounds the local error estimate of each step, not the error at $T$. Check the result by solving again at a tighter tolerance.
- **Mixing the two solutions.** Keeping $\hat y$ instead of $y$ is a valid method of order 2, but it wastes accuracy. Using the exponent $1/4$ in L10 (the order of the kept solution plus 1) makes the controller react too weakly.
- **Event times and output points.** Shortening the last step to reach $T$ is fine, but for many output times use the interpolant rather than forcing steps to hit each one.

## Implementations

## History

Fehlberg in the 1960s introduced embedded pairs in which the two solutions share all stages. Dormand and Prince (1980) used the FSAL idea and proposed advancing with the higher-order solution. Bogacki and Shampine (1989) built this 3(2) pair in that style. They chose the free parameters to make the order-3 solution accurate and the estimate reliable. Shampine and Reichelt made it the method of ode23 in the MATLAB ODE Suite (1997), and it is also the default low-order explicit method in several other libraries.

## References
