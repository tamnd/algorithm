---
tag: 1KQDQK
kind: algorithm
slug: cash-karp-method
name: Cash-Karp method
aliases:
- Cash-Karp Runge-Kutta
- Cash-Karp 5(4) pair
- RKCK
area: numerical/differential-equations
level: advanced
summary: An embedded explicit Runge-Kutta pair of orders 5 and 4 with six stages. The difference of the two solutions estimates the local error for adaptive step size control.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of accepted steps", R: "the number of rejected steps", d: "the dimension of y"}
  time: {worst: "Θ((N + R) d)"}
  space: {extra: "Θ(d)"}
  evaluations: {worst: "1 + 6 (N + R)"}
properties: {deterministic: true, explicit: true, one_step: true, order: "5", embedded_order: "4", stages: "6", fsal: false, a_stable: false, error_estimate: true}
history:
  year: 1990
  people: [Jeff R. Cash, Alan H. Karp]
  note: Cash and Karp published the pair in 1990, inside a variable-order scheme for problems with rapidly varying right-hand sides. Numerical Recipes made it widely known.
prereqs: [butcher-tableau, adaptive-step-size-control]
see_also: [embedded-runge-kutta-pairs, runge-kutta-fehlberg-method, dormand-prince-method, bogacki-shampine-method, classical-runge-kutta-4, butcher-order-conditions, absolute-stability, runge-kutta-methods]
sources:
  - paper: doi:10.1145/79505.79507
    title: "J. R. Cash and A. H. Karp, A variable order Runge-Kutta method for initial value problems with rapidly varying right-hand sides, ACM Transactions on Mathematical Software 16 (1990) 201-222"
    locator: the six-stage tableau with embedded solutions of orders 1 to 5 and the strategy for choosing the order
  - book: isbn:9780521431088
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes in C, second edition, Cambridge University Press, 1992
    locator: Section 16.2 (adaptive step size control for Runge-Kutta, the Cash-Karp coefficients)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.4 (error estimation and step size control) and Section II.5 (embedded formulas of order 5)
---

The Cash-Karp method is an [embedded Runge-Kutta pair](/embedded-runge-kutta-pairs/) for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$. From six evaluations of $f$ it forms a solution of order 5, which is kept, and a solution of order 4. Their difference is an estimate of the local error, which drives [adaptive step size control](/adaptive-step-size-control/). The pair is a close relative of [Runge-Kutta-Fehlberg 4(5)](/runge-kutta-fehlberg-method/). Its stages were chosen so that solutions of orders 1, 2 and 3 can also be read off the early stages, which the original paper uses to cope with right-hand sides that change rapidly. Numerical Recipes made the pair popular. Modern codes mostly prefer [Dormand-Prince 5(4)](/dormand-prince-method/), which has the FSAL property and smaller error constants.

## In plain words

The method samples the slope six times inside each step, at fixed fractions of the step. It combines these samples in two different ways. One gives a very accurate new value, the other a slightly less accurate one. The gap between the two shows roughly how large the error is. If the gap is small enough compared with the tolerance, the step is kept and the next one may be longer. If it is too large, the step is repeated with a shorter length. Because the accuracy improves with the fifth power of the step length, small changes in the step give large changes in the error, so the method can reach many digits cheaply on smooth problems.

## The problem

**Notation.** As on all differential-equations pages: $y' = f(t, y)$ on $[t_0, T]$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$; step $h$; $y_n \approx y(t_n)$; global error $e_n = y(t_n) - y_n$; order $p$; Lipschitz constant $L$; test equation $y' = \lambda y$ with $z = h\lambda$ and $R(z)$. The step sizes $h_n$ vary and are chosen by the method.

The input is $f$, $t_0$, $y_0$, $T \ge t_0$, $\mathrm{rtol}$ and $\mathrm{atol}$. The output is the accepted points $(t_n, y_n)$, ending exactly at $T$. The [Butcher tableau](/butcher-tableau/) is
$$\begin{array}{c|cccccc} 0 & & & & & & \\ \tfrac15 & \tfrac15 & & & & & \\ \tfrac{3}{10} & \tfrac{3}{40} & \tfrac{9}{40} & & & & \\ \tfrac35 & \tfrac{3}{10} & -\tfrac{9}{10} & \tfrac65 & & & \\ 1 & -\tfrac{11}{54} & \tfrac52 & -\tfrac{70}{27} & \tfrac{35}{27} & & \\ \tfrac78 & \tfrac{1631}{55296} & \tfrac{175}{512} & \tfrac{575}{13824} & \tfrac{44275}{110592} & \tfrac{253}{4096} & \\ \hline b & \tfrac{37}{378} & 0 & \tfrac{250}{621} & \tfrac{125}{594} & 0 & \tfrac{512}{1771} \\ \hat b & \tfrac{2825}{27648} & 0 & \tfrac{18575}{48384} & \tfrac{13525}{55296} & \tfrac{277}{14336} & \tfrac14 \end{array}$$
The estimate is $\mathrm{est} = y_{n+1} - \hat y_{n+1} = h\sum_j(b_j - \hat b_j)k_j$, and a step is accepted when $\mathrm{err} = \max_i|\mathrm{est}_i|/(\mathrm{atol} + \mathrm{rtol}\cdot\max(|y_{n,i}|, |y_{n+1,i}|)) \le 1$.

## The algorithm

```pseudo id=main
CASH-KARP(f, t0, y0, T, rtol, atol)
L1  t ← t0, y ← y0, choose a starting h from |y0| and |f(t0, y0)|
L2  while t < T do
L3      if t + h ≥ T then h ← T − t                     ▷ the last step ends at T
L4      for i ← 1 to 6 do k_i ← f(t + c_i·h, y + h·Σ_{j<i} a_ij·k_j)
L5      y′ ← y + h·Σ_i b_i·k_i                            ▷ order 5
L6      est ← h·Σ_i (b_i − b̂_i)·k_i                       ▷ order-5 minus order-4 solution
L7      err ← max_i |est_i| / (atol + rtol·max(|y_i|, |y′_i|))
L8      if err ≤ 1 then t ← t + h, y ← y′                ▷ accept
L9      h ← h·min(5, max(0.2, 0.9·err^(−1/5)))             ▷ factor at most 1 after a rejection
L10 return the accepted points
```

The exponent $1/5$ in L9 comes from $\mathrm{est} \approx Ch^5$, the local error of the order-4 solution. The method advances with the order-5 solution (local extrapolation), as Numerical Recipes does. Line L1 costs one evaluation of $f$ when the starting step is not given. That value is not reused, because the pair is not FSAL.

## Example

**One step, and a warning.** On $y' = -2ty^2$, $y(0) = 1$, exact solution $y = 1/(1 + t^2)$, one step with $h = 0.5$ gives $y_1 = 0.80002545$ against the exact $0.8$, an error of $2.5 \cdot 10^{-5}$. The estimate is only $5.6 \cdot 10^{-7}$. The order-4 solution has error $2.49 \cdot 10^{-5}$, and the order-5 solution happens to have almost the same error. With $\mathrm{rtol} = \mathrm{atol} = 10^{-6}$ this step would be accepted ($\mathrm{err} = 0.28$). The estimate is only asymptotically correct, and $h = 0.5$ is far from the asymptotic range for this problem.

**Fixed steps, observed order.** Without step control, on the same problem, the error at $t = 2$ is:

| $h$ | error at $t = 2$ | $\log_2$ of the ratio |
|---|---|---|
| 0.2 | $1.0795 \cdot 10^{-7}$ | |
| 0.1 | $2.7958 \cdot 10^{-9}$ | 5.27 |
| 0.05 | $7.8569 \cdot 10^{-11}$ | 5.15 |
| 0.025 | $2.3195 \cdot 10^{-12}$ | 5.08 |
| 0.0125 | $7.0333 \cdot 10^{-14}$ | 5.04 |

**Adaptive runs.** With $\mathrm{rtol} = \mathrm{atol} = \mathrm{tol}$ and the automatic starting step, on $[0, 2]$:

| tol | accepted | rejected | evaluations | max error on the grid |
|---|---|---|---|---|
| $10^{-4}$ | 11 | 0 | 67 | $4.67 \cdot 10^{-4}$ |
| $10^{-6}$ | 16 | 2 | 109 | $4.33 \cdot 10^{-6}$ |
| $10^{-8}$ | 28 | 3 | 187 | $2.32 \cdot 10^{-8}$ |
| $10^{-10}$ | 56 | 4 | 361 | $2.58 \cdot 10^{-10}$ |
| $10^{-12}$ | 129 | 3 | 793 | $2.98 \cdot 10^{-12}$ |

Compared with the [Bogacki-Shampine pair](/bogacki-shampine-method/) on the same problem, Cash-Karp needs 109 evaluations at $10^{-6}$ where BS23 needs 190, and it reaches $10^{-12}$ with fewer than 800. The global error is a small multiple of the tolerance in these runs. That is an observation, not a guarantee.

## Correctness

The proofs are in `proofs/correctness.md`. In summary:

1. **Orders.** With exact fractions, $b$ satisfies all 17 [order conditions](/butcher-order-conditions/) for trees with at most 5 vertices, and fails all 20 of order 6. $\hat b$ satisfies the 8 conditions up to order 4 and fails all 9 of order 5. So, for $f$ of class $C^5$, the kept solution has local error $O(h^6)$ and the estimate behaves like $Ch^5$. These are asymptotic statements.
2. **Stability function.** $R(z) = 1 + z + \tfrac{z^2}{2} + \tfrac{z^3}{6} + \tfrac{z^4}{24} + \tfrac{z^5}{120} + \tfrac{z^6}{800}$, computed exactly as $1 + \sum_q z^{q}\,b^TA^{q-1}\mathbf 1$. The real stability interval is $[-3.7344, 0]$, found numerically.
3. **Convergence with fixed steps.** The increment is Lipschitz in $y$ when $f$ is, so the standard one-step argument gives global error $O(h^5)$. The table above shows it.
4. **Termination.** As for any embedded pair with the controller of L9, every rejection shrinks $h$ by a factor of at most $0.9$. Since $\mathrm{est} = O(h^5)$, a step is accepted after finitely many rejections when $\mathrm{atol} > 0$. Line L3 makes the last point equal $T$.

## Complexity

The cost model counts evaluations of $f$. Every attempted step costs 6 evaluations, accepted or not, and the automatic starting step costs one more. The total is $1 + 6(N + R)$. The arithmetic is $\Theta(d)$ per stage combination, so $\Theta(d)$ per stage and $\Theta((N + R)d)$ in total. The memory is the six stage vectors, $\Theta(d)$. No Jacobians and no linear solves are needed. On a smooth problem the step size is about $(\mathrm{tol}/C)^{1/5}$, so the work grows like $\mathrm{tol}^{-1/5}$. Dormand-Prince has 7 stages but FSAL, so it also costs 6 evaluations per step.

## Properties

- **Explicit, six stages, order 5.** Six is the smallest number of stages for an explicit method of order 5 (Butcher's barrier).
- **No FSAL.** The last stage is at $c_6 = 7/8$, not at the new point, so each step pays all six evaluations.
- **Embedded lower orders.** The weights $(-\tfrac32, \tfrac52)$ on $k_1, k_2$ give order 2, and $(\tfrac{19}{54}, 0, -\tfrac{10}{27}, \tfrac{55}{54})$ on $k_1, \dots, k_4$ give order 3. With $y + hk_1$ for order 1, the paper compares these solutions to decide early whether a step is going to fail.
- **Not A-stable.** The stability region is bounded. Its real interval, $[-3.7344, 0]$, is a little larger than that of RK4.

## Variants and improvements

- **Variable order.** Cash and Karp's own code compares the embedded solutions of orders 1 to 5 during the step. If the low-order solutions already disagree badly, it stops early and retries with a smaller step, which saves stages near sharp fronts.
- **Dormand-Prince 5(4).** A seven-stage FSAL pair with smaller error constants for the kept solution and a free interpolant of order 4. It is the usual default today, for example in ode45.
- **Runge-Kutta-Fehlberg 4(5).** The older six-stage pair, designed to advance with the order-4 solution.
- **PI control.** Replacing L9 by a PI controller gives smoother step sequences. See [adaptive step size control](/adaptive-step-size-control/).

## When to use it

Use Cash-Karp for smooth non-stiff problems at moderate to tight tolerances, from about $10^{-4}$ to $10^{-12}$, when a simple and well-tested 5(4) pair is enough. Examples include orbit integrations over moderate times and parameter studies. It is a reasonable alternative to Dormand-Prince when the code base already uses it. For loose tolerances a third-order pair is cheaper per step. For stiff problems use an implicit method.

## Pitfalls

- **The estimate can be far too small for large steps.** In the example, the estimate at $h = 0.5$ was 45 times smaller than the true error. Asymptotic estimates need steps in the asymptotic range. The controller usually gets there after a few steps, but a large $h_0$ can let one bad step through.
- **Stiffness.** On $y' = -1000(y - \cos t) - \sin t$ over $[0, 1]$ the method needs about 270 to 310 accepted steps. It took 271 accepted and 36 rejected steps for $\mathrm{rtol} = 10^{-3}$, and 312 for $\mathrm{rtol} = 10^{-6}$. The step size is set by the stability bound $3.73/1000$, not by the tolerance.
- **Zero scale.** Keep $\mathrm{atol} > 0$ for components that pass through 0.
- **Global error.** The tolerance controls the local error estimate per step. Check results by solving again with a smaller tolerance.
- **Copying coefficients.** The fractions have large denominators, and one wrong digit drops the order without any obvious symptom. Check the order conditions with exact arithmetic, as the tests do.

## Implementations

## History

Fehlberg's pairs of the 1960s showed how to obtain two solutions of different orders from the same stages. Dormand and Prince (1980) improved the error constants and advanced with the higher-order solution. Cash and Karp (1990) aimed at problems whose right-hand side varies rapidly, where a fixed high-order pair wastes work on failed steps. They designed six stages that carry solutions of every order from 1 to 5. Press, Teukolsky, Vetterling and Flannery adopted the order-5 and order-4 members as their standard adaptive Runge-Kutta routine in the second edition of Numerical Recipes (1992), which is how most users met the method.

## References
