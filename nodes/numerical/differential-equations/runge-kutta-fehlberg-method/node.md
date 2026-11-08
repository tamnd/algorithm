---
tag: 37PW24
kind: algorithm
slug: runge-kutta-fehlberg-method
name: Runge-Kutta-Fehlberg method
aliases:
- RKF45
- Fehlberg 4(5) method
- Runge-Kutta-Fehlberg 4(5)
area: numerical/differential-equations
level: core
summary: "An embedded explicit Runge-Kutta pair of orders 4 and 5 with 6 stages. The difference of the two results estimates the local error and drives the choice of the step size."
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {A: "the number of accepted steps", R: "the number of rejected steps", d: "the dimension of y", C: "the cost of one evaluation of f"}
  time: {worst: "Θ((A + R) (C + d))"}
  space: {extra: "Θ(d)"}
  evaluations: {worst: "6 (A + R)"}
properties: {deterministic: true, implicit: false, one_step: true, order: "4 (with a fifth-order error estimator)", adaptive: true, a_stable: false, symplectic: false}
history:
  year: 1969
  people: [Erwin Fehlberg]
  note: Fehlberg published the 4(5) pair in a NASA technical report in 1969, as one of a series of embedded formulas with step size control.
prereqs: [runge-kutta-methods, embedded-runge-kutta-pairs, local-truncation-error]
see_also: [dormand-prince-method, cash-karp-method, bogacki-shampine-method, adaptive-step-size-control, classical-runge-kutta-4, stiff-ode-problem, global-error, dense-output]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.4 (practical error estimation and step size selection, embedded formulas, the Fehlberg pair), Section II.5 (explicit methods of higher order, Dormand-Prince and local extrapolation)
  - book: isbn:9780131653320
    title: George E. Forsythe, Michael A. Malcolm and Cleve B. Moler, Computer Methods for Mathematical Computations, Prentice-Hall, 1977
    locator: Chapter 6 (ordinary differential equations and the RKF45 code)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 3 (embedded Runge-Kutta methods and step size control)
  - paper: "Erwin Fehlberg, Low-order classical Runge-Kutta formulas with stepsize control and their application to some heat transfer problems, NASA Technical Report R-315, 1969"
    locator: the 4(5) pair and its coefficients
---

The Runge-Kutta-Fehlberg method (RKF45) is an [embedded pair](/embedded-runge-kutta-pairs/) of explicit [Runge-Kutta methods](/runge-kutta-methods/): six evaluations of $f$ per step give one result of order 4 and one of order 5. The difference of the two results estimates the [local error](/local-truncation-error/) of the fourth-order result, and the code accepts or rejects the step and chooses the next step size from this estimate. It solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$ to a user tolerance without a step size from the user. It was the first widely used method of this kind; the [Dormand-Prince pair](/dormand-prince-method/) has since replaced it in most libraries.

## In plain words

A fixed step size is a guess. Too large, and the answer is wrong; too small, and the program wastes time. RKF45 measures its own error as it goes. In each step it computes two answers from the same six slopes: a good one and a better one. The two answers differ by about the error of the good one. If that difference is larger than the user allows, the step is thrown away and tried again with a shorter step. If it is smaller, the step is kept, and the next step is made longer or shorter so that its error should be just under the limit. So the method takes long steps where the solution is smooth and short steps where it changes fast.

## The problem

Given $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$, $y_0$, $T \ge t_0$ and tolerances $\mathrm{rtol}, \mathrm{atol} \ge 0$ (not both $0$), compute $y_N \approx y(T)$ with each accepted local error estimate below the tolerance. We assume that $f$ is continuous and Lipschitz in $y$, and $C^5$ for the asymptotic statements. The cost is the number of evaluations of $f$, $6$ per trial step.

## The algorithm

The Fehlberg tableau, with $b$ the fourth-order and $\hat b$ the fifth-order weights:

$$\begin{array}{c|cccccc} 0 & & & & & & \\ \frac14 & \frac14 & & & & & \\ \frac38 & \frac3{32} & \frac9{32} & & & & \\ \frac{12}{13} & \frac{1932}{2197} & -\frac{7200}{2197} & \frac{7296}{2197} & & & \\ 1 & \frac{439}{216} & -8 & \frac{3680}{513} & -\frac{845}{4104} & & \\ \frac12 & -\frac8{27} & 2 & -\frac{3544}{2565} & \frac{1859}{4104} & -\frac{11}{40} & \\ \hline b & \frac{25}{216} & 0 & \frac{1408}{2565} & \frac{2197}{4104} & -\frac15 & 0 \\ \hat b & \frac{16}{135} & 0 & \frac{6656}{12825} & \frac{28561}{56430} & -\frac9{50} & \frac2{55} \end{array}$$

The error weights are $\hat b - b = \left(\frac1{360}, 0, -\frac{128}{4275}, -\frac{2197}{75240}, \frac1{50}, \frac2{55}\right)$.

```pseudo id=main
RKF45(f, t0, y0, T, rtol, atol, h0)
L1  t ← t0, y ← y0, h ← h0
L2  while t < T do
L3      if h ≥ T − t then h ← T − t, last ← true else last ← false
L4      for i ← 1 to 6 do k_i ← f(t + c_i h, y + h Σ_{j<i} a_ij k_j)
L5      y4 ← y + h Σ b_i k_i,   est ← h Σ (b̂_i − b_i) k_i
L6      err ← sqrt( (1/d) Σ_m ( est_m / (atol + rtol · max(|y_m|, |y4_m|)) )^2 )
L7      if err ≤ 1 then t ← (T if last else t + h), y ← y4        ▷ accept
L8      h ← h · min(5, max(0.2, 0.9 · err^(−1/5)))                  ▷ new trial step
L9  return (t, y)
```

Line L3 shortens the last step so that it ends at $T$; an initial $h_0$ larger than $T - t_0$ gives one step. Line L4 is a Runge-Kutta step with 6 stages. Line L5 forms the fourth-order result and the estimate. Line L6 measures the estimate in a root mean square norm scaled by a mixed absolute and relative tolerance, so $\mathrm{err} \le 1$ means "within tolerance". Line L8 uses $\mathrm{err} \approx C h^5$: the step $h\,\mathrm{err}^{-1/5}$ would give $\mathrm{err} = 1$, and the safety factor $0.9$ and the limits $0.2$ and $5$ keep the change of $h$ moderate. A rejected step changes only $h$. The implementation also stops with an error when $h$ falls below $10^{-14}\max(1, |t|)$ or the number of trials passes a limit.

## Example

Take $y' = -2ty^2$, $y(0) = 1$, with the solution $y = 1/(1 + t^2)$, on $[0, 1]$ with $\mathrm{rtol} = \mathrm{atol} = 10^{-6}$ and $h_0 = 0.5$:

| trial | $t$ | $h$ | err | result | $y_4$ |
|---|---|---|---|---|---|
| 1 | 0.0000 | 0.5000 | 52.70 | reject | |
| 2 | 0.0000 | 0.2036 | 0.012 | accept | 0.96018306 |
| 3 | 0.2036 | 0.4410 | 127.8 | reject | |
| 4 | 0.2036 | 0.1505 | 0.335 | accept | 0.88859015 |
| 5 | 0.3541 | 0.1685 | 0.668 | accept | 0.78546844 |
| 6 | 0.5226 | 0.1644 | 0.274 | accept | 0.67932535 |
| 7 | 0.6871 | 0.1918 | 0.217 | accept | 0.56421535 |
| 8 | 0.8788 | 0.1212 | 0.072 | accept | 0.50000073 |

The first trial is too long, so $h$ shrinks by $0.9 \cdot 52.70^{-1/5} = 0.407$. After the first accepted step the error is very small, so $h$ grows by $0.9 \cdot 0.012^{-1/5} = 2.17$, too much, and the third trial fails. The last trial is shortened to end at $1$. The final error is $7.3 \cdot 10^{-7}$ after 48 evaluations of $f$.

**Tolerance and work.** With $\mathrm{rtol} = \mathrm{atol} = \mathrm{tol}$ and the default first step $0.01$:

| tol | accepted | rejected | evaluations | error at $T = 1$ |
|---|---|---|---|---|
| $10^{-3}$ | 5 | 1 | 36 | $1.29 \cdot 10^{-3}$ |
| $10^{-5}$ | 6 | 1 | 42 | $9.52 \cdot 10^{-6}$ |
| $10^{-7}$ | 11 | 4 | 90 | $4.76 \cdot 10^{-8}$ |
| $10^{-9}$ | 22 | 3 | 150 | $1.91 \cdot 10^{-11}$ |

The error follows the tolerance, but it is not bounded by it: at $10^{-3}$ the error is larger than the tolerance.

**A stiff problem.** The problem $y' = -1000(y - \cos t) - \sin t$, $y(0) = 1$, has the smooth solution $y = \cos t$. The fourth-order formula has the stability polynomial $R(z) = 1 + z + \frac{z^2}{2} + \frac{z^3}{6} + \frac{z^4}{24} + \frac{z^5}{104}$, stable on the real interval $[-3.02, 0]$. So $h \le 0.00302$, and the run on $[0, 1]$ needs about 330 steps whatever the tolerance: 328 accepted steps for $\mathrm{tol} = 10^{-3}$ and 319 for $10^{-6}$ (with 151 rejections). Only at $10^{-9}$ does accuracy, not stability, set the step (1056 steps).

## Correctness

Each accepted step is one step of an explicit Runge-Kutta method of order 4, so the computed values are those of a fourth-order method on the grid of accepted points. The weights $b$ satisfy the 8 order conditions up to order 4 and $\hat b$ satisfies all 17 conditions up to order 5, which the test file checks in exact rational arithmetic. For $f \in C^5$ the estimate is $\mathrm{est} = \ell_4 + O(h^6)$, where $\ell_4 = O(h^5)$ is the local error of the fourth-order result: the estimate is asymptotically exact. The loop terminates when $\mathrm{atol} > 0$ and $f$ is bounded: steps of length at most $h^* = \mathrm{atol}/(\sigma K)$ always pass, so $h$ never falls below $\min(h_0, 0.2h^*)$. The proofs are below.

The controller bounds local errors, not the global error. A proved bound on the global error in terms of the tolerance does not exist for this code; the relation in the table above is observed.

## Complexity

Each trial costs 6 evaluations of $f$ and $O(d)$ work for each of the 6 stages, so the time is $\Theta((A + R)(C + d))$ for $A$ accepted and $R$ rejected steps, and the evaluations number $6(A + R)$. The extra space is $\Theta(d)$ for the six slopes. On a smooth nonstiff problem the step is about $(\mathrm{tol}/C)^{1/5}$, so $A = \Theta(\mathrm{tol}^{-1/5})$ asymptotically; in the table above, each factor of 100 in the tolerance about doubles the number of steps ($100^{1/5} = 2.5$). On a stiff problem $A$ is $\Theta(|\lambda|(T - t_0))$ for the largest stiff eigenvalue $\lambda$, independent of the tolerance.

## Properties

- **Orders 4 and 5, six stages.** Six is the minimum number of stages for an explicit method of order 5. The fourth-order formula uses only five of them ($b_6 = 0$).
- **Fixed-step behaviour.** With a fixed step on the example, the fourth-order result has observed orders $5.28, 4.93, 4.64, 4.40$ for $h = 0.2, 0.1, \ldots, 0.0125$, which tend to 4 from above, and the estimate has observed orders close to 5.
- **No first-same-as-last.** The last stage is not $f$ at the new point, so each step needs all 6 evaluations. The Dormand-Prince pair saves one evaluation per accepted step this way.
- **Not suited to stiff problems.** The real stability interval is $[-3.02, 0]$.

## Variants and improvements

- **Local extrapolation.** Advance with the fifth-order result $y_5$ and use the same estimate. The error estimate is then pessimistic, but the result is more accurate.
- **[Dormand-Prince 5(4)](/dormand-prince-method/).** Coefficients chosen to make the fifth-order error small, local extrapolation, and the first-same-as-last property. It is the default in most libraries (HNW I, Section II.5).
- **[Cash-Karp](/cash-karp-method/)** and **[Bogacki-Shampine](/bogacki-shampine-method/).** Other embedded pairs, of orders 5(4) and 3(2).
- **Better controllers.** PI controllers use the last two error estimates and give smoother step sequences, especially near the stability limit ([adaptive step size control](/adaptive-step-size-control/)).
- **[Dense output](/dense-output/).** Interpolate inside the step to get values between the accepted points without more steps.

## When to use it

Use RKF45 or, better, Dormand-Prince for nonstiff problems where moderate accuracy (relative $10^{-3}$ to $10^{-8}$) is enough and the solution has regions of very different smoothness. If the number of steps stays large when you loosen the tolerance, the problem is stiff; switch to an implicit method such as [Radau IIA](/radau-iia-methods/) or the [backward differentiation formulas](/backward-differentiation-formulas/).

## Pitfalls

- **Reading the tolerance as a global error bound.** The tolerance controls each local error. The global error can be larger by the growth factor of the problem.
- **A pure relative tolerance near zero.** With $\mathrm{atol} = 0$ and a solution component that passes through 0, the scale factor becomes 0 and the step size collapses. Use a positive $\mathrm{atol}$.
- **Rounding the last step.** Advancing $t \leftarrow t + h$ on the last step can stop just short of $T$ and leave a tiny extra step. Set $t \leftarrow T$ exactly, as line L7 does.
- **Discontinuities in $f$.** At a jump the estimate stays large for all $h$ of the size of the jump region, and the code makes many rejections. Stop the integration at the known discontinuity and restart.

## Implementations

## History

Fehlberg, at NASA's Marshall Space Flight Center, published embedded Runge-Kutta formulas of several orders in NASA technical reports in 1968 and 1969, with the 4(5) pair in 1969. The RKF45 code of Shampine and Watts, printed in the book of Forsythe, Malcolm and Moler (1977), made the method a standard. Dormand and Prince (1980) later showed that a pair tuned for the fifth-order result with local extrapolation is more efficient (HNW I, Sections II.4 and II.5).

## References
