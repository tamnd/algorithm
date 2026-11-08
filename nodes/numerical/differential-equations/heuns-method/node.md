---
tag: G2M62V
kind: algorithm
slug: heuns-method
name: Heun's method
aliases:
- improved Euler method
- explicit trapezoidal method
- explicit trapezoidal rule
area: numerical/differential-equations
level: intro
summary: "Predict with an Euler step, then average the slopes at both ends: y_(n+1) = y_n + (h/2)(k_1 + k_2). Two evaluations of f per step, order 2, stability function 1 + z + z^2/2."
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps, ⌈(T - t_0)/h⌉", d: "the dimension of y", C: "the cost of one evaluation of f"}
  time: {worst: "Θ(N (C + d))"}
  space: {extra: "Θ(d)"}
  evaluations: {worst: "2N"}
properties: {deterministic: true, implicit: false, one_step: true, order: "2", a_stable: false, l_stable: false, symplectic: false}
history:
  year: 1900
  people: [Karl Heun, Carl Runge]
  note: Heun published two-stage and three-stage methods of this kind in 1900, after Runge's paper of 1895 on methods that sample the slope at several points.
prereqs: [euler-method, ode-initial-value-problem, local-truncation-error]
see_also: [explicit-midpoint-method, runge-kutta-methods, butcher-tableau, classical-runge-kutta-4, trapezoidal-rule, crank-nicolson-method, global-error, order-of-accuracy]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.1 (the first Runge-Kutta methods of Runge, Heun and Kutta) and Section II.3 (convergence of one-step methods)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 2 (numerical differential equation methods, Runge-Kutta methods of low order) and Chapter 3 (Runge-Kutta methods)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 5 (two-stage Runge-Kutta methods, truncation errors) and Chapter 7 (absolute stability regions)
  - paper: "Karl Heun, Neue Methoden zur approximativen Integration der Differentialgleichungen einer unabhängigen Veränderlichen, Zeitschrift für Mathematik und Physik 45 (1900) 23-38"
---

Heun's method solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, with steps of the form $k_1 = f(t_n, y_n)$, $k_2 = f(t_n + h, y_n + h k_1)$, $y_{n+1} = y_n + \frac{h}{2}(k_1 + k_2)$. It predicts the end of the step with [Euler's method](/euler-method/) and then uses the average of the slopes at both ends, as the [trapezoidal rule](/trapezoidal-rule/) does. It costs two evaluations of $f$ per step and has order $p = 2$ when $f$ is Lipschitz in $y$ and the solution is $C^3$. It is the two-stage explicit [Runge-Kutta method](/runge-kutta-methods/) with stability function $R(z) = 1 + z + z^2/2$.

## In plain words

Euler's method looks at the direction of the path at the start of a step and moves in a straight line. On a curved path this always misses in the same direction. Heun's method makes the Euler move only as a trial. It then asks for the direction at the trial point, at the end of the step. The real move uses the average of the two directions: the one at the start and the one at the end.

The two errors partly cancel. When the steps are made half as long, the total error becomes about four times smaller, not two times as with Euler's method. The price is two questions to the equation per step instead of one.

## The problem

Given $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$, a start value $y_0$, an end time $T \ge t_0$ and a step size $h > 0$, compute an approximation $y_N$ of $y(T)$, where $y$ solves $y' = f(t, y)$, $y(t_0) = y_0$. We assume that $f$ is continuous and Lipschitz in $y$ with constant $L$. The cost is the number of evaluations of $f$.

## The algorithm

```pseudo id=main
HEUN(f, t0, y0, T, h)
L1  N ← ⌈(T − t0)/h − δ⌉                    ▷ δ: a relative slack of 10^-9 against rounding, 0 in exact arithmetic
L2  t ← t0, y ← y0
L3  for n ← 0 to N − 1 do
L4      t_next ← T if n = N − 1 else t0 + (n + 1) h
L5      k ← t_next − t                       ▷ the actual step, h except possibly the last
L6      k1 ← f(t, y)                         ▷ slope at the start
L7      k2 ← f(t_next, y + k k1)              ▷ slope at the Euler prediction
L8      y ← y + (k/2)(k1 + k2)
L9      t ← t_next
L10 return (t, y)
```

Lines L1 and L4 build the grid as in Euler's method: grid points are computed by a product, the last step ends exactly at $T$, a step $h > T - t_0$ gives one step of length $T - t_0$, and $T = t_0$ gives no step at all. Line L7 is the predictor and line L8 the corrector. As a Runge-Kutta method with $s = 2$ stages its [Butcher tableau](/butcher-tableau/) is

$$c = \begin{pmatrix} 0 \\ 1 \end{pmatrix}, \qquad A = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}, \qquad b = \begin{pmatrix} 1/2 & 1/2 \end{pmatrix}.$$

## Example

Take $y' = -2 t y^2$, $y(0) = 1$, with the solution $y(t) = 1/(1 + t^2)$, and $h = 0.2$ up to $T = 1$.

| $n$ | $t_n$ | $y_n$ | $y(t_n)$ | $e_n = y(t_n) - y_n$ |
|---|---|---|---|---|
| 0 | 0.0 | 1.000000 | 1.000000 | 0.000000 |
| 1 | 0.2 | 0.960000 | 0.961538 | 0.001538 |
| 2 | 0.4 | 0.860298 | 0.862069 | 0.001771 |
| 3 | 0.6 | 0.735043 | 0.735294 | 0.000252 |
| 4 | 0.8 | 0.611572 | 0.609756 | -0.001816 |
| 5 | 1.0 | 0.503338 | 0.500000 | -0.003338 |

In the first step $k_1 = f(0, 1) = 0$, so the prediction is $1$, and $k_2 = f(0.2, 1) = -0.4$. Then $y_1 = 1 + 0.1 \cdot (0 - 0.4) = 0.96$. In the second step $k_1 = -2 \cdot 0.2 \cdot 0.96^2 = -0.36864$, the prediction is $0.96 - 0.2 \cdot 0.36864 = 0.886272$, $k_2 = -0.8 \cdot 0.886272^2 = -0.628383$, and $y_2 = 0.96 + 0.1\,(k_1 + k_2) = 0.860298$. The final error $0.0033$ is half the error $0.0071$ of Euler's method with the same $h$, at twice the cost. The advantage of order 2 shows when $h$ gets smaller.

For $h = 0.1, 0.05, 0.025, 0.0125, 0.00625, 0.003125$ the errors $|e_N|$ at $T = 1$ are $9.186 \cdot 10^{-4}$, $2.363 \cdot 10^{-4}$, $5.976 \cdot 10^{-5}$, $1.502 \cdot 10^{-5}$, $3.763 \cdot 10^{-6}$, $9.420 \cdot 10^{-7}$. The observed orders $\log_2(|e^{(h)}| / |e^{(h/2)}|)$ are $1.959$, $1.984$, $1.993$, $1.996$, $1.998$, which tend to $p = 2$. With $h = 0.003125$ Heun's method uses 640 evaluations of $f$ for an error of $9.4 \cdot 10^{-7}$. Euler's method needs about 38000 evaluations for the same error, about 60 times as many.

On the stiff problem $y' = -50 y$, $y(0) = 1$, $T = 1$: with $h = 0.05$, $z = -2.5$, $R(z) = 1.625$ and $y_{20} = 1.625^{20} \approx 16484$. With $h = 1/24$ (just above the limit), $z = -2.083$ and $y_{24} = 7.37$. With $h = 0.04$, $z = -2$ and $R(z) = 1$ exactly. With $h = 1/26$ (just below), $y_{26} = 0.136$. With $h = 0.025$, $y_{40} = 0.53125^{40} \approx 1.03 \cdot 10^{-11}$. The exact value is $e^{-50} \approx 1.9 \cdot 10^{-22}$.

## Correctness

The loop computes $y_{n+1} = \Phi_{h_n}(t_n, y_n)$ with the step map above, by induction on $n$. The method converges with order 2. If $f$ is continuous and Lipschitz in $y$ with constant $L > 0$ and the solution is $C^3$, then

$$\|y(t_n) - y_n\| \le C h^2\, \frac{e^{\Lambda (t_n - t_0)} - 1}{\Lambda}, \qquad C = \frac{M_3}{12} + \frac{L M_2}{4}, \quad \Lambda = L\Bigl(1 + \frac{hL}{2}\Bigr),$$

with $M_k = \max \|y^{(k)}\|$ on $[t_0, T]$. The proof bounds the [local truncation error](/local-truncation-error/) by $C h^3$: one part is the error $-\frac{h^3}{12} y'''$ of the trapezoidal rule applied to $y'$, and the other comes from using the Euler prediction instead of $y(t_n + h)$ in $k_2$, which costs $\frac{h}{2} L \cdot \frac{h^2}{2} M_2$. The step map has the Lipschitz constant $1 + h\Lambda$, and the errors are summed as for Euler's method. This is a proved, non-asymptotic bound; the full proof is below.

In terms of the [Butcher order conditions](/butcher-order-conditions/), $\sum_i b_i = 1$ and $\sum_i b_i c_i = \frac12$ hold, so the order is at least 2. The order-3 conditions $\sum_i b_i c_i^2 = \frac13$ and $\sum_{i,j} b_i a_{ij} c_j = \frac16$ fail (the left sides are $\frac12$ and $0$), so the order is exactly 2.

## Complexity

The loop runs $N = \lceil (T - t_0)/h \rceil$ times. Each run makes two evaluations of $f$ and $O(d)$ further operations. So the time is $\Theta(N (C + d))$ in the [real RAM](/real-ram/) model, the number of evaluations is exactly $2N$, and the extra space is $\Theta(d)$ for $y$, $k_1$, $k_2$ and the prediction. To reach an error $\varepsilon$ at fixed $T$ the method needs $N = \Theta(\varepsilon^{-1/2})$ steps on a smooth problem with a nonzero error constant, against $\Theta(\varepsilon^{-1})$ for Euler's method. This is asymptotic in $\varepsilon \to 0$.

## Properties

- **Order 2.** The local error is $O(h^3)$ and the global error $O(h^2)$, under the hypotheses above.
- **Stability function $R(z) = 1 + z + z^2/2$.** This is the Taylor polynomial of $e^z$ of degree 2, as for each explicit two-stage method of order 2. On the real axis $|R(z)| \le 1$ exactly for $-2 \le z \le 0$, so the step limit for real $\lambda < 0$ is $h \le 2/|\lambda|$, the same as for Euler's method. The [stability region](/stability-region/) is bounded, so the method is not [A-stable](/a-stability/).
- **Energy drift.** On the harmonic oscillator $y_1' = y_2$, $y_2' = -y_1$, one step multiplies $y_1^2 + y_2^2$ by $|R(ih)|^2 = 1 + h^4/4$. The drift is much slower than the factor $1 + h^2$ of Euler's method, but it does not stop: the method is not [symplectic](/symplectic-integrators/).
- **On quadrature problems.** When $f$ does not depend on $y$, the step is the [trapezoidal rule](/trapezoidal-rule/) on $[t_n, t_{n+1}]$.
- **A built-in error estimate.** The difference of the Euler prediction and the Heun value, $\frac{h}{2}(k_2 - k_1)$, is an estimate of the local error of the Euler step. This gives the embedded pair of orders 1 and 2 used for [adaptive step size control](/adaptive-step-size-control/) at low accuracy.

## Variants and improvements

- **[Explicit midpoint method](/explicit-midpoint-method/).** The other common two-stage method of order 2: $y_{n+1} = y_n + h f(t_n + h/2, y_n + \frac{h}{2} k_1)$. It has the same $R(z)$, and so the same linear stability.
- **The family of two-stage methods of order 2.** With $c_2 = \alpha \ne 0$, $a_{21} = \alpha$, $b_2 = 1/(2\alpha)$ and $b_1 = 1 - 1/(2\alpha)$, each choice of $\alpha$ gives order 2. Heun's method is $\alpha = 1$, the midpoint method is $\alpha = 1/2$, and Ralston's method $\alpha = 2/3$ minimizes a bound on the error constant.
- **The implicit trapezoidal rule.** Use $y_{n+1}$ itself instead of the prediction in $k_2$. The result is A-stable but needs a solve in each step; on the heat equation it is the [Crank-Nicolson method](/crank-nicolson-method/).
- **Predictor-corrector.** Iterating line L8 to convergence gives the implicit trapezoidal rule, and a fixed number of corrections gives a family of explicit methods. The [Adams-Bashforth-Moulton method](/adams-bashforth-moulton-method/) uses the same idea with multistep formulas.
- **Heun's third-order method.** Heun's paper of 1900 also gives a three-stage method of order 3.

## When to use it

Use Heun's method when a simple explicit method with order 2 is enough, for example in a first implementation, in real-time simulations with a fixed step, and as the predictor in a step size control at low accuracy. For accurate solutions of smooth problems, use a method of order 4 or 5 with error control, such as [classical RK4](/classical-runge-kutta-4/) or the [Dormand-Prince method](/dormand-prince-method/). For stiff problems, use an implicit method.

## Pitfalls

- **The name.** "Improved Euler method" means Heun's method in some books and the explicit midpoint method in others, and "Heun's method" sometimes means Heun's three-stage method of order 3. State the formula.
- **Evaluating $f$ at the wrong time in the predictor.** Line L7 must use $t_n + h$ together with the predicted value. Using $t_n$ there keeps order 2 only when $f$ does not depend on $t$.
- **Stiff problems.** The order is higher than Euler's, but the stability interval is the same $[-2, 0]$. On a stiff problem a step larger than $2/|\lambda|$ makes the numbers grow like $|R(h\lambda)|^n$.
- **Too much trust in the order.** Order 2 needs a $C^3$ solution. If $f$ has a kink, for example $|y|$, the observed order near the kink can drop to 1.

## Implementations

## History

Runge published in 1895 the idea of sampling the slope at more than one point in a step, and Heun followed in 1900 with methods of order 2 and 3 of this kind, including the one on this page. Kutta then gave the general form and the fourth-order methods in 1901 (HNW I, Section II.1).

## References
