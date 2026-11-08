---
tag: Q8KN04
kind: algorithm
slug: dormand-prince-method
name: Dormand-Prince method
aliases:
- DOPRI5
- RK5(4)7FM
- Dormand-Prince 5(4) pair
- ode45 method
area: numerical/differential-equations
level: core
summary: "Explicit embedded Runge-Kutta pair of orders 5 and 4 with 7 stages and the FSAL property: 6 evaluations of f per step, the order-5 result is kept and the difference gives the error estimate."
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of attempted steps", d: "the dimension of y", C: "the cost of one evaluation of f"}
  time: {worst: "Θ(N (C + d))"}
  space: {extra: "Θ(d)"}
  evaluations: {worst: "6 N + 2"}
properties: {deterministic: true, implicit: false, one_step: true, order: "5 (embedded order 4)", adaptive: true, fsal: true, a_stable: false}
history:
  year: 1980
  people: [John R. Dormand, Peter J. Prince]
  note: Dormand and Prince published the pair in 1980, choosing the coefficients to make the error of the fifth-order formula small, so that the fifth-order result is propagated.
prereqs: [embedded-runge-kutta-pairs, butcher-order-conditions, adaptive-step-size-control]
see_also: [runge-kutta-fehlberg-method, cash-karp-method, bogacki-shampine-method, classical-runge-kutta-4, dense-output, stiff-ode-problem, global-error, butcher-tableau]
sources:
  - paper: doi:10.1016/0771-050X(80)90013-3
    title: J. R. Dormand and P. J. Prince, A family of embedded Runge-Kutta formulae, Journal of Computational and Applied Mathematics 6(1) (1980) 19-26
    locator: the coefficients of RK5(4)7M and the design criteria
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.2 (order conditions and Butcher's theorem), Section II.4 (error estimation, step size control and the starting step size), Section II.5 (explicit Runge-Kutta methods of higher order, the Dormand-Prince pair), Section II.6 (dense output); Appendix (the code DOPRI5)
  - paper: doi:10.1137/S1064827594276424
    title: Lawrence F. Shampine and Mark W. Reichelt, The MATLAB ODE suite, SIAM Journal on Scientific Computing 18(1) (1997) 1-22
    locator: the choice of the Dormand-Prince pair for ode45
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 3 (Runge-Kutta methods; order conditions and embedded methods)
  - paper: doi:10.1017/S1446788700027932
    title: J. C. Butcher, Coefficients for the study of Runge-Kutta integration processes, Journal of the Australian Mathematical Society 3 (1963) 185-201
    locator: the order conditions indexed by rooted trees
---

The Dormand-Prince method is an explicit [embedded Runge-Kutta pair](/embedded-runge-kutta-pairs/) for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$. Seven stages give two results of orders 5 and 4. The method keeps the order-5 result, uses the difference of the two as an estimate of the local error, and changes the step size $h$ from step to step so that the estimate stays below a tolerance. The last stage is evaluated at the new point, so it is the first stage of the next step (FSAL), and a step costs 6 evaluations of $f$. It is the method of MATLAB's `ode45`, of SciPy's default `RK45`, and of Hairer's code DOPRI5.

## In plain words

A fixed step size is either too small where the solution is smooth, which wastes work, or too large where it changes fast, which loses accuracy. This method chooses the step as it goes. In each step it computes the next value twice, once with a very accurate formula and once with a slightly less accurate one, both made from the same slope evaluations. The two answers differ by about the error of the weaker one. If that difference is small enough, the step is kept and the next step can be longer. If not, the step is thrown away and tried again with a shorter length. The last slope of a step is also the first slope of the next, so it is not computed twice.

## The problem

Given $f$, $t_0$, $y_0 \in \mathbb{R}^d$, an end time $T \ge t_0$, an absolute tolerance $\mathrm{Atol} > 0$ and a relative tolerance $\mathrm{Rtol} \ge 0$, compute an approximation of $y(T)$, keeping the estimated local error of each step at most 1 in the scaled norm

$$\mathrm{err} = \sqrt{\frac1d\sum_{i=1}^{d}\left(\frac{\mathrm{est}_i}{\mathrm{Atol} + \mathrm{Rtol}\max(|y_{n,i}|, |y_{n+1,i}|)}\right)^2}.$$

Here $f$ is continuous and Lipschitz in $y$ (so the solution is unique), and smooth ($C^5$ or more) for the orders to show.

## The algorithm

The coefficients form the [Butcher tableau](/butcher-tableau/) below. The row of $b$ is also the last row of $A$.

| $c_i$ | $a_{i1}$ | $a_{i2}$ | $a_{i3}$ | $a_{i4}$ | $a_{i5}$ | $a_{i6}$ |
|---|---|---|---|---|---|---|
| 0 | | | | | | |
| 1/5 | 1/5 | | | | | |
| 3/10 | 3/40 | 9/40 | | | | |
| 4/5 | 44/45 | -56/15 | 32/9 | | | |
| 8/9 | 19372/6561 | -25360/2187 | 64448/6561 | -212/729 | | |
| 1 | 9017/3168 | -355/33 | 46732/5247 | 49/176 | -5103/18656 | |
| 1 | 35/384 | 0 | 500/1113 | 125/192 | -2187/6784 | 11/84 |

The weights are $b = (\tfrac{35}{384}, 0, \tfrac{500}{1113}, \tfrac{125}{192}, -\tfrac{2187}{6784}, \tfrac{11}{84}, 0)$ (order 5) and $\hat b = (\tfrac{5179}{57600}, 0, \tfrac{7571}{16695}, \tfrac{393}{640}, -\tfrac{92097}{339200}, \tfrac{187}{2100}, \tfrac{1}{40})$ (order 4).

```pseudo id=main
DOPRI5(f, t0, y0, T, Atol, Rtol, h)
L1  t ← t0, y ← y0, k1 ← f(t, y), facmax ← 5              ▷ h: given, or from the starting rule
L2  while t < T do
L3      if t + h ≥ T then h ← T − t                        ▷ the last step ends at T
L4      for i ← 2 to 6 do k_i ← f(t + c_i h, y + h Σ_{j<i} a_ij k_j);  y_new ← y + h Σ_{j≤6} b_j k_j
L5      k7 ← f(t + h, y_new)                                ▷ FSAL: the first stage of the next step
L6      err ← scaled RMS norm of est = h Σ_j (b_j − b̂_j) k_j
L7      if err ≤ 1 then t ← t + h, y ← y_new, k1 ← k7, facmax ← 5     ▷ accept
L8      else facmax ← 1                                     ▷ reject, retry from the same t
L9      h ← h · min(facmax, max(0.2, 0.9 err^(−1/5)))
L10 return (t, y)
```

Line L4 builds the stages and the order-5 result. Line L6 never forms the order-4 result; it uses the weights $b - \hat b$ directly. The exponent $1/5$ in line L9 comes from $\mathrm{err} \approx K h^5$, the local error of the order-4 formula: the step $h\,\mathrm{err}^{-1/5}$ would give $\mathrm{err} = 1$, and the safety factor $0.9$ aims a little lower. The factor is kept in $[0.2, 5]$, and after a rejection the step may not grow ($\mathrm{facmax} = 1$). When no $h$ is given, the starting rule of HNW I, Section II.4 compares $\|y_0\|$, $\|f(t_0, y_0)\|$ and a difference estimate of $\|y''\|$ and costs one extra evaluation. A real code also stops with an error when $h$ falls below a small multiple of the rounding unit times $|t|$.

## Example

Take $y' = -2ty^2$, $y(0) = 1$, exact solution $1/(1 + t^2)$, $T = 1$, $\mathrm{Atol} = \mathrm{Rtol} = 10^{-6}$ and the first trial step $h = 0.1$.

| attempt | $t$ | $h$ | err | result | $y_{n+1}$ | error of $y_{n+1}$ |
|---|---|---|---|---|---|---|
| 1 | 0 | 0.1 | 0.0043 | accept | 0.99009901 | $-3.8 \cdot 10^{-10}$ |
| 2 | 0.1 | 0.267276 | 1.7169 | reject | | |
| 3 | 0.1 | 0.215901 | 0.4920 | accept | 0.90926183 | $6.9 \cdot 10^{-8}$ |
| 4 | 0.315901 | 0.223922 | 2.0525 | reject | | |
| 5 | 0.315901 | 0.174535 | 0.5415 | accept | 0.80610838 | $8.2 \cdot 10^{-8}$ |
| 6 | 0.490436 | 0.177583 | 0.4245 | accept | 0.69144368 | $9.9 \cdot 10^{-8}$ |
| 7 | 0.668019 | 0.189697 | 0.0602 | accept | 0.57614434 | $2.5 \cdot 10^{-8}$ |
| 8 | 0.857716 | 0.142284 | 0.0740 | accept | 0.50000001 | $-1.3 \cdot 10^{-8}$ |

After attempt 1 the error estimate is tiny, so the step grows by the factor $0.9 \cdot 0.0043^{-1/5} \approx 2.67$, to $0.267276$. That step fails ($\mathrm{err} = 1.72$), and the retry uses $0.267276 \cdot 0.9 \cdot 1.7169^{-1/5} = 0.215901$. The last step is cut to land on $T = 1$. The run makes 6 accepted and 2 rejected steps and $1 + 8 \cdot 6 = 49$ evaluations of $f$.

Other tolerances on the same problem, all with first step $0.1$: $10^{-4}$ gives 3 steps, 19 evaluations and error $1.3 \cdot 10^{-6}$; $10^{-8}$ gives 15 attempts, 91 evaluations and error $3.1 \cdot 10^{-9}$; $10^{-10}$ gives 32 attempts, 193 evaluations and error $3.8 \cdot 10^{-11}$.

With constant steps and no control, the order-5 result has errors at $T = 1$ for $h = 0.2, 0.1, 0.05, 0.025, 0.0125$ of $1.80 \cdot 10^{-7}$, $4.71 \cdot 10^{-9}$, $1.29 \cdot 10^{-10}$, $3.71 \cdot 10^{-12}$, $1.11 \cdot 10^{-13}$: observed orders $5.26$, $5.19$, $5.12$, $5.07$. The order-4 result alone gives observed orders $4.74$, $4.42$, $4.22$, $4.11$.

## Correctness

The loop computes a sequence of accepted steps, each of which is one step of the order-5 Runge-Kutta method. By Butcher's theorem a Runge-Kutta method has order $p$ iff its elementary weights satisfy $\Phi(\tau) = 1/\gamma(\tau)$ for every rooted tree with at most $p$ vertices ([Butcher order conditions](/butcher-order-conditions/)). The weights $b$ satisfy all 17 conditions up to order 5 and $\hat b$ all 8 up to order 4, which exact rational arithmetic confirms, and both fail at the next order. So, for $f \in C^6$, the estimate $h\sum(b_j - \hat b_j)k_j$ equals the local error of the order-4 formula up to $O(h^6)$. The last row of $A$ equals $b$, so $k_7 = f(t + h, y_{n+1})$ is the first stage of the next step. The controller ends: after a rejection $h$ shrinks by a factor at most $0.9$, a small enough $h$ is always accepted, and steps stay above a positive bound, so finitely many steps reach $T$, and the last one is cut to land on it.

What the method guarantees is the local estimate, not the [global error](/global-error/). That the global error is roughly proportional to the tolerance is observed on smooth problems and holds asymptotically under hypotheses on the controller. With constant steps the method converges with order 5 by the general theorem for one-step methods. The full proof is below.

## Complexity

Each attempted step makes 6 evaluations of $f$ (stages 2 to 7) and $O(s d) = O(d)$ further arithmetic for the stage sums, so $N$ attempts cost $6N$ evaluations, plus 1 for the first slope and 1 for the starting rule: $6N + 2$. The time is $\Theta(N(C + d))$ in the [real RAM](/real-ram/) model, and the extra space is $\Theta(d)$ for the 7 stage vectors. The number of steps is not known in advance. For a smooth nonstiff problem it behaves like $\mathrm{tol}^{-1/5}$ as the tolerance tends to 0, which is why the method is efficient at moderate accuracy. On a [stiff problem](/stiff-ode-problem/) it behaves like $|\lambda|(T - t_0)/3.3$, independent of the tolerance (see Pitfalls).

## Properties

- **Orders 5 and 4, local extrapolation.** The propagated value has order 5, and the error estimate belongs to the order-4 formula. So the estimate is pessimistic for the value that is kept.
- **FSAL.** Seven stages, but six new evaluations per step.
- **Stability function.** $R(z) = 1 + z + \tfrac{z^2}{2} + \tfrac{z^3}{6} + \tfrac{z^4}{24} + \tfrac{z^5}{120} + \tfrac{z^6}{600}$. The real stability interval is about $[-3.3066, 0]$.
- **Small error constants.** Dormand and Prince chose the free parameters to make the order-6 error terms of the order-5 formula small. This is the reason the order-5 value, not the order-4 value, is propagated.
- **Dense output.** A continuous extension of order 4 uses the same 7 stages, so the solution can be evaluated between grid points at no extra cost in evaluations ([dense output](/dense-output/)).

## Variants and improvements

- **[Runge-Kutta-Fehlberg](/runge-kutta-fehlberg-method/) 4(5).** The earlier pair of 1969, which propagates the order-4 value; 6 evaluations per step, no FSAL.
- **[Cash-Karp](/cash-karp-method/).** Another 5(4) pair with 6 stages.
- **[Bogacki-Shampine](/bogacki-shampine-method/) 3(2).** A smaller FSAL pair for loose tolerances (MATLAB's `ode23`).
- **DOP853.** Dormand and Prince's 8(5,3) pair for tight tolerances.
- **Tsitouras 5(4).** A later pair with similar cost and smaller error coefficients under weaker simplifying assumptions.
- **PI step control.** Using the last two error estimates in line L9 (Gustafsson's controller) smooths the step sequence when stability limits the step.

## When to use it

Use the Dormand-Prince pair as the default for nonstiff problems at tolerances from about $10^{-3}$ to $10^{-8}$. At tighter tolerances a higher order (DOP853, extrapolation, or Adams methods with variable order) needs fewer evaluations. If the step sizes stay small for no visible reason and the run makes many rejections, the problem is probably stiff: switch to an implicit method such as [Radau IIA](/radau-iia-methods/) or the [BDF methods](/backward-differentiation-formulas/).

## Pitfalls

- **Comparing err with the tolerance instead of 1.** The tolerances enter the scale in line L6. Testing $\mathrm{err} \le \mathrm{Rtol}$ in line L7 applies the tolerance twice.
- **Using $h$ again after a rejection without the cap.** If line L8 does not set $\mathrm{facmax} = 1$, a rejected step can be followed by a larger one, and the code can oscillate between rejections.
- **Discarding k7.** Computing $f(t + h, y)$ again at the start of the next step costs 7 evaluations per step instead of 6. Line L7 keeps it as $k_1$; after a rejection the old $k_1$ is still valid because $t$ and $y$ did not change.
- **Expecting the tolerance as the global error.** The tolerance bounds a local estimate. On $y' = -2ty^2$ with tolerance $10^{-6}$ the final error is $1.3 \cdot 10^{-8}$, and on unstable problems it can be much larger than the tolerance.
- **Stiffness.** On $y' = -1000(y - \cos t) - \sin t$, $y(0) = 1$, $T = 1$ (solution $\cos t$), the code needs about 300 accepted steps (1928 evaluations) for both $\mathrm{tol} = 10^{-2}$ and $10^{-3}$, because $h|\lambda|$ must stay inside the interval $[-3.3, 0]$. A smaller tolerance does not change the count much, since stability, not accuracy, limits $h$.

## Implementations

## History

Fehlberg (1969) introduced pairs with a cheap error estimate in which the lower-order result is propagated. Dormand and Prince (1980) derived a family of 5(4) pairs with the FSAL property and with the free coefficients chosen to minimize the error of the fifth-order formula, so that the fifth-order value can be propagated. Hairer and Wanner's code DOPRI5, and later MATLAB's `ode45` (Shampine and Reichelt 1997), made it the default explicit integrator in scientific software.

## References
