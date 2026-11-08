---
tag: P0J8GY
kind: algorithm
slug: euler-method
name: Euler's method
aliases:
- forward Euler method
- explicit Euler method
- Euler polygon method
area: numerical/differential-equations
level: intro
summary: "The explicit step y_(n+1) = y_n + h f(t_n, y_n). One evaluation of f per step, global error O(h) for f Lipschitz in y, stability function 1 + z, so stiff problems need tiny steps."
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps, ⌈(T - t_0)/h⌉", d: "the dimension of y", C: "the cost of one evaluation of f"}
  time: {worst: "Θ(N (C + d))"}
  space: {extra: "Θ(d)"}
  evaluations: {worst: "N"}
properties: {deterministic: true, implicit: false, one_step: true, order: "1", a_stable: false, l_stable: false, symplectic: false}
history:
  year: 1768
  people: [Leonhard Euler, Augustin-Louis Cauchy, Rudolf Lipschitz]
  note: Euler described the method in Institutiones calculi integralis (1768). Cauchy proved that the polygons converge in his lectures of the 1820s, and Lipschitz (1868) replaced Cauchy's assumption of a bounded derivative by the Lipschitz condition.
prereqs: [ode-initial-value-problem, lipschitz-condition, local-truncation-error]
see_also: [backward-euler-method, explicit-midpoint-method, heuns-method, global-error, dahlquist-test-equation, stiff-ode-problem, symplectic-euler-method, euler-maruyama-method]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section I.7 (existence theory, Cauchy's convergence proof for Euler polygons), Section II.1 (Euler's method as the first Runge-Kutta method), Section II.3 (convergence of one-step methods)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 1, Section 1.2 (Euler's method and its convergence proof)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 2, Section 20 (the Euler method) and Section 21 (analysis of the Euler method)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 5 (basic methods and truncation errors), Chapter 6 (convergence of one-step methods), Chapter 7 (absolute stability of forward Euler)
---

Euler's method solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, by following the tangent for one step of length $h$: $y_{n+1} = y_n + h f(t_n, y_n)$ on the grid $t_n = t_0 + n h$. It costs one evaluation of $f$ per step. When $f$ is [Lipschitz](/lipschitz-condition/) in $y$ and the solution is $C^2$, the [global error](/global-error/) at a fixed time is $O(h)$, so the method has order $p = 1$. Its stability function on the [test equation](/dahlquist-test-equation/) is $R(z) = 1 + z$, which makes it useless on [stiff problems](/stiff-ode-problem/) unless the step is very small.

## In plain words

You know where you are now and, from the equation, which way you are moving and how fast. Euler's method assumes that this speed and direction stay the same for a short time. It moves in a straight line for one short step, then looks at the equation again at the new point, and repeats. The result is a chain of straight segments that follows the true curve.

Each segment starts in the right direction but bends away from the curve a little. The errors of all the segments add up. If you halve the length of the segments, you make twice as many, but each error becomes four times smaller, so the total error at the end becomes about half as large.

## The problem

Given $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$, a start value $y_0$, an end time $T \ge t_0$ and a step size $h > 0$, compute an approximation $y_N$ of $y(T)$, where $y$ solves $y' = f(t, y)$, $y(t_0) = y_0$. We assume that $f$ is continuous and Lipschitz in $y$ with constant $L$, so that the solution exists and is unique ([Picard-Lindelöf theorem](/picard-lindelof-theorem/)). The cost is the number of evaluations of $f$.

## The algorithm

```pseudo id=main
EULER(f, t0, y0, T, h)
L1  N ← ⌈(T − t0)/h − δ⌉                    ▷ δ: a relative slack of 10^-9 against rounding, 0 in exact arithmetic
L2  t ← t0, y ← y0
L3  for n ← 0 to N − 1 do
L4      t_next ← T if n = N − 1 else t0 + (n + 1) h
L5      y ← y + (t_next − t) f(t, y)
L6      t ← t_next
L7  return (t, y)
```

Line L1 counts the steps. Line L4 computes the next grid point by a product, not by adding $h$ again and again, so rounding does not move the grid. The last step ends exactly at $T$: it is shorter than $h$ when $T - t_0$ is not a multiple of $h$, and it is the only step when $h > T - t_0$. If $T = t_0$, then $N = 0$ and the method returns $y_0$ with no evaluation of $f$. Line L5 is the Euler step. For a vector $y$ it updates all $d$ components with the same slope evaluation.

## Example

Take $y' = -2 t y^2$, $y(0) = 1$, whose solution is $y(t) = 1/(1 + t^2)$, and $h = 0.2$ up to $T = 1$.

| $n$ | $t_n$ | $y_n$ | $y(t_n)$ | $e_n = y(t_n) - y_n$ |
|---|---|---|---|---|
| 0 | 0.0 | 1.000000 | 1.000000 | 0.000000 |
| 1 | 0.2 | 1.000000 | 0.961538 | -0.038462 |
| 2 | 0.4 | 0.920000 | 0.862069 | -0.057931 |
| 3 | 0.6 | 0.784576 | 0.735294 | -0.049282 |
| 4 | 0.8 | 0.636842 | 0.609756 | -0.027086 |
| 5 | 1.0 | 0.507060 | 0.500000 | -0.007060 |

The first step uses the slope $f(0, 1) = 0$, so $y_1 = y_0$. The second step uses $f(0.2, 1) = -0.4$, so $y_2 = 1 - 0.2 \cdot 0.4 = 0.92$. The error first grows and then falls again: the local truncation error $\frac12 h^2 y''(t_n)$ changes sign at $t = 1/\sqrt{3}$, where $y'' = (6t^2 - 2)/(1 + t^2)^3$ changes sign.

When $h$ is halved, the error at $T = 1$ is about halved. For $h = 0.1, 0.05, 0.025, 0.0125, 0.00625$ the errors $|e_N|$ are $3.642 \cdot 10^{-3}$, $1.805 \cdot 10^{-3}$, $8.949 \cdot 10^{-4}$, $4.451 \cdot 10^{-4}$, $2.219 \cdot 10^{-4}$. The observed orders $\log_2(|e^{(h)}| / |e^{(h/2)}|)$ are $1.012$, $1.013$, $1.008$, $1.004$, which tend to $p = 1$.

On the stiff test problem $y' = -50 y$, $y(0) = 1$, $T = 1$, the exact value is $e^{-50} \approx 1.9 \cdot 10^{-22}$. With $h = 0.05$, $z = h\lambda = -2.5$ and $y_{20} = (1 - 2.5)^{20} \approx 3325$. With $h = 0.04$, $z = -2$ and $|y_{25}| = 1$: the method is exactly on the stability limit. With $h = 0.025$, $y_{40} = (-0.25)^{40} \approx 8.3 \cdot 10^{-25}$, which is small, as it should be.

## Correctness

The loop computes the Euler polygon: after iteration $n$, $t = t_{n+1}$ and $y = y_{n+1}$ (induction on $n$). The method converges with order 1:

$$\|y(t_n) - y_n\| \le \frac{h M_2}{2L}\left(e^{L(t_n - t_0)} - 1\right), \qquad M_2 = \max_{[t_0, T]} \|y''\|,$$

when $f$ is continuous and Lipschitz in $y$ with constant $L > 0$, and the solution $y$ is $C^2$ (true when $f$ is $C^1$). The proof bounds the [local truncation error](/local-truncation-error/) of one step by $\frac12 h^2 M_2$ with Taylor's formula, shows that the error is multiplied by at most $1 + hL \le e^{hL}$ in each step, and sums the geometric series. This is a proved, non-asymptotic bound. The full proof, which also allows a shorter last step and adds rounding errors, is below.

The bound is usually far too large: the factor $e^{L(t - t_0)}$ grows even when the solutions of the problem contract. A sharper statement is asymptotic: when $f$ is smooth, $e_n = h\, E(t_n) + O(h^2)$, where $E$ solves the linear problem $E' = f_y(t, y(t)) E + \frac12 y''(t)$, $E(t_0) = 0$ (HNW I, Section II.8). This explains why halving $h$ halves the error in the table above.

## Complexity

Line L5 runs $N = \lceil (T - t_0)/h \rceil$ times. Each run makes one evaluation of $f$, at cost $C$, and $d$ multiplications and $d$ additions. So the time is $\Theta(N (C + d))$ in the [real RAM](/real-ram/) model, and the number of evaluations of $f$ is exactly $N$. The method stores $t$, $y$ and one slope, so the extra space is $\Theta(d)$. To reach an error $\varepsilon$ at a fixed $T$ the method needs $h \approx \varepsilon / C$, so $N = \Theta(1/\varepsilon)$ evaluations. A method of order $p$ needs only $\Theta(\varepsilon^{-1/p})$ steps, which is why Euler's method is rarely used for accurate work.

## Properties

- **Order 1.** The local truncation error is $\frac12 h^2 y''(t_n) + O(h^3)$, and the global error is $O(h)$.
- **Stability function $R(z) = 1 + z$.** On $y' = \lambda y$ the method gives $y_n = (1 + h\lambda)^n y_0$. The [region of absolute stability](/stability-region/) is the disk $|1 + z| \le 1$ of radius 1 about $-1$. For real $\lambda < 0$ the condition is $h \le 2/|\lambda|$. The method is not [A-stable](/a-stability/).
- **Explicit.** Each step is one evaluation of $f$ and no equation to solve.
- **Not symplectic, energy grows.** On the harmonic oscillator $y_1' = y_2$, $y_2' = -y_1$, each step multiplies $y_1^2 + y_2^2$ by exactly $1 + h^2$, so the orbit spirals outward.
- **It is the first member of several families.** It is the one-stage explicit [Runge-Kutta method](/runge-kutta-methods/) and the [linear multistep method](/linear-multistep-methods/) with $\rho(\zeta) = \zeta - 1$, $\sigma(\zeta) = 1$, and the first of the [Adams-Bashforth methods](/adams-bashforth-methods/).

## Variants and improvements

- **[Backward Euler method](/backward-euler-method/).** Use the slope at the new point. Same order, but $R(z) = 1/(1 - z)$ is A-stable, at the price of solving an equation in each step.
- **Two-stage methods.** The [explicit midpoint method](/explicit-midpoint-method/) and [Heun's method](/heuns-method/) evaluate $f$ twice per step and reach order 2.
- **[Richardson extrapolation](/richardson-extrapolation/).** Since $e_n = h E(t_n) + O(h^2)$, the combination $2 y^{(h/2)} - y^{(h)}$ has error $O(h^2)$. Repeating this idea gives the [Bulirsch-Stoer method](/bulirsch-stoer-method/).
- **[Symplectic Euler method](/symplectic-euler-method/).** For Hamiltonian systems, update the momentum with the old position and the position with the new momentum. The energy then stays bounded.
- **[Euler-Maruyama method](/euler-maruyama-method/).** The same step with a Brownian increment added solves stochastic differential equations.

## When to use it

Use Euler's method to teach, to build a first prototype, and inside methods that need a cheap predictor. It is also a reasonable choice when $f$ itself is noisy or only Lipschitz, so that higher order brings nothing. For accurate solutions of smooth nonstiff problems, use a higher-order method with error control, such as the [Dormand-Prince method](/dormand-prince-method/). For stiff problems, use an implicit method such as [backward Euler](/backward-euler-method/) or the [backward differentiation formulas](/backward-differentiation-formulas/).

## Pitfalls

- **Stepping by repeated addition.** Writing `t ← t + h` in line L6 lets rounding move the grid: after ten steps of $h = 0.1$ the time is $0.9999999999999999$, and a loop `while t < T` takes an eleventh tiny step. Compute $t_0 + (n+1)h$ as in line L4 and end the last step at $T$.
- **An explicit step on a stiff problem.** With $h > 2/|\lambda|$ for a large negative eigenvalue $\lambda$ of $f_y$, the numbers grow like $|1 + h\lambda|^n$ even though the true solution decays. The fix is a smaller $h$ or an implicit method, not a higher-order explicit one.
- **Too small a step.** Rounding adds an error of about $\varepsilon$ per step, so the total error behaves like $h M_2/2 + \varepsilon/h$ times a constant. Below $h \approx \sqrt{2\varepsilon/M_2}$ the error grows again. In double precision this limit is near $h = 10^{-8}$ for $M_2 \approx 1$.
- **Trusting the error bound to choose $h$.** The bound with $e^{L(T - t_0)}$ can be larger than the real error by many orders of magnitude. Estimate the error by a second computation with $h/2$, or use an [embedded pair](/embedded-runge-kutta-pairs/).

## Implementations

## History

Euler described the method in 1768, in the first volume of Institutiones calculi integralis, as a way to approximate the solution of a differential equation by a polygon. Cauchy proved, in his lectures at the École Polytechnique in the 1820s, that the Euler polygons converge to a solution when $f$ and its derivative are continuous, which gave both an existence theorem and a convergence proof. Lipschitz replaced the bounded derivative by the condition that now bears his name in 1868 (HNW I, Section I.7).

## References
