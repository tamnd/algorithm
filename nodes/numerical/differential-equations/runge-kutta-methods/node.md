---
tag: EV2XHR
kind: algorithm
slug: runge-kutta-methods
name: Runge-Kutta methods
aliases:
- RK methods
- explicit Runge-Kutta methods
- s-stage Runge-Kutta method
area: numerical/differential-equations
level: core
summary: "One-step methods for y' = f(t, y) that combine s evaluations of f per step, given by a Butcher tableau (A, b, c). Order p needs the tree conditions; global error O(h^p) for f Lipschitz."
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps, ⌈(T - t_0)/h⌉", s: "the number of stages", d: "the dimension of y", C: "the cost of one evaluation of f"}
  time: {worst: "Θ(N s (C + s d))"}
  space: {extra: "Θ(s d)"}
  evaluations: {worst: "N s"}
properties: {deterministic: true, implicit: false, one_step: true, order: "set by the tableau (p <= s for explicit methods)", a_stable: false, symplectic: false}
history:
  year: 1895
  people: [Carl Runge, Karl Heun, Wilhelm Kutta, John C. Butcher]
  note: Runge (1895) and Heun (1900) proposed methods with several evaluations of f per step, and Kutta (1901) derived the order conditions up to order 4 and the classical fourth-order method. Butcher (1963) gave the general order theory with rooted trees.
prereqs: [ode-initial-value-problem, euler-method, butcher-tableau, local-truncation-error]
see_also: [classical-runge-kutta-4, butcher-order-conditions, embedded-runge-kutta-pairs, runge-kutta-fehlberg-method, implicit-runge-kutta-methods, stability-region, global-error, linear-multistep-methods]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.1 (the first Runge-Kutta methods), Section II.2 (order conditions and Butcher trees), Section II.3 (error estimation and convergence of one-step methods), Section II.5 (explicit methods of higher order and the order barriers)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 3 (Runge-Kutta methods, trees and order conditions, explicit methods of orders 2 to 8)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 3 (Runge-Kutta methods, explicit and implicit), Chapter 4 (stability functions and A-stability)
  - paper: "Carl Runge, Über die numerische Auflösung von Differentialgleichungen, Mathematische Annalen 46 (1895) 167-178"
    locator: the first methods with several evaluations of f per step
  - paper: "Wilhelm Kutta, Beitrag zur näherungsweisen Integration totaler Differentialgleichungen, Zeitschrift für Mathematik und Physik 46 (1901) 435-453"
    locator: the order conditions up to order 4 and the classical fourth-order method
  - paper: "John C. Butcher, Coefficients for the study of Runge-Kutta integration processes, Journal of the Australian Mathematical Society 3 (1963) 185-201"
    locator: the rooted-tree form of the order conditions
---

A Runge-Kutta method solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, by one-step updates that each combine $s$ evaluations of $f$, called stages. The coefficients form a [Butcher tableau](/butcher-tableau/) $(A, b, c)$. With the right coefficients the [global error](/global-error/) is $O(h^p)$ for an order $p$ much higher than the order 1 of the [Euler method](/euler-method/), at a cost of $s$ evaluations of $f$ per step. Explicit methods, the subject of this page, are the standard tool for nonstiff problems; the [implicit Runge-Kutta methods](/implicit-runge-kutta-methods/) are for stiff ones.

## In plain words

The Euler method looks at the slope once, at the start of a step, and follows it in a straight line. A Runge-Kutta method takes a few trial steps inside the same step. It looks at the slope at the start, makes a short trial move, looks at the slope there, makes another trial move with that slope, and so on. At the end it moves from the start point with a weighted average of all the slopes it saw.

The weights and the positions of the trial moves are chosen so that the errors of the trial slopes cancel each other. With four well chosen slopes per step, halving the step size makes the error about sixteen times smaller, while for Euler it only halves. So a few more evaluations of the equation per step save a very large number of steps.

## The problem

Given $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$, a start value $y_0$, an end time $T \ge t_0$ and a step size $h > 0$, compute $y_N \approx y(T)$. We assume that $f$ is continuous and Lipschitz in $y$ with constant $L$, so the solution exists and is unique ([Picard-Lindelöf theorem](/picard-lindelof-theorem/)), and that $f$ is $C^p$ when we claim order $p$. The cost is the number of evaluations of $f$.

## The algorithm

An $s$-stage explicit method has a strictly lower triangular $A = (a_{ij})$, weights $b = (b_i)$ and nodes $c_i = \sum_j a_{ij}$:

$$\begin{array}{c|c} c & A \\ \hline & b^T \end{array} \qquad \text{for example RK4:} \qquad \begin{array}{c|cccc} 0 & & & & \\ \frac12 & \frac12 & & & \\ \frac12 & 0 & \frac12 & & \\ 1 & 0 & 0 & 1 & \\ \hline & \frac16 & \frac13 & \frac13 & \frac16 \end{array}$$

```pseudo id=main
RK-STEP(f, t, y, h, A, b, c)                 ▷ one step of an explicit method
L1  for i ← 1 to s do
L2      Y_i ← y + h Σ_{j<i} a_ij k_j          ▷ the stage value
L3      k_i ← f(t + c_i h, Y_i)               ▷ the stage slope
L4  return y + h Σ_{i=1..s} b_i k_i

RUNGE-KUTTA(f, t0, y0, T, h, A, b, c)
L5  N ← ⌈(T − t0)/h − δ⌉                       ▷ δ: a relative slack of 10^-9 against rounding
L6  t ← t0, y ← y0
L7  for n ← 0 to N − 1 do
L8      t_next ← T if n = N − 1 else t0 + (n + 1) h
L9      y ← RK-STEP(f, t, y, t_next − t, A, b, c)
L10     t ← t_next
L11 return (t, y)
```

Lines L1 to L3 compute the stages in order. Each stage uses only the slopes before it, which is what "explicit" means. Line L4 forms the step with the weights $b_i$. Lines L5 to L11 are the same driver as for the Euler method: the grid is $t_n = t_0 + nh$, the last step ends exactly at $T$, $T = t_0$ gives zero steps, and $h > T - t_0$ gives one short step.

**Order conditions.** The method has order $p$ when its local error is $O(h^{p+1})$ for each smooth $f$. With $c_i = \sum_j a_{ij}$, the conditions up to order 4 are (HNW I, Section II.2):

| order | conditions | count |
|---|---|---|
| 1 | $\sum b_i = 1$ | 1 |
| 2 | $\sum b_i c_i = \frac12$ | 1 |
| 3 | $\sum b_i c_i^2 = \frac13$, $\sum b_i a_{ij} c_j = \frac16$ | 2 |
| 4 | $\sum b_i c_i^3 = \frac14$, $\sum b_i c_i a_{ij} c_j = \frac18$, $\sum b_i a_{ij} c_j^2 = \frac1{12}$, $\sum b_i a_{ij} a_{jk} c_k = \frac1{24}$ | 4 |

In general there is one condition for each rooted tree with at most $p$ vertices: 1, 2, 4, 8, 17, 37, 85 and 200 conditions for $p = 1, \ldots, 8$. The full theory is on the page [Butcher order conditions](/butcher-order-conditions/).

## Example

Take $y' = -2ty^2$, $y(0) = 1$, with the solution $y = 1/(1 + t^2)$, and RK4 with $h = 0.2$. The first step has $k_1 = f(0, 1) = 0$, $k_2 = f(0.1, 1) = -0.2$, $k_3 = f(0.1, 0.98) = -0.19208$, $k_4 = f(0.2, 0.961584) = -0.369858$, and $y_1 = 1 + \frac{0.2}{6}(k_1 + 2k_2 + 2k_3 + k_4) = 0.961533$.

| $n$ | $t_n$ | $y_n$ | $y(t_n)$ | $e_n$ |
|---|---|---|---|---|
| 0 | 0.0 | 1.00000000 | 1.00000000 | 0 |
| 1 | 0.2 | 0.96153275 | 0.96153846 | $5.71 \cdot 10^{-6}$ |
| 2 | 0.4 | 0.86205242 | 0.86206897 | $1.65 \cdot 10^{-5}$ |
| 3 | 0.6 | 0.73527834 | 0.73529412 | $1.58 \cdot 10^{-5}$ |
| 4 | 0.8 | 0.60975183 | 0.60975610 | $4.26 \cdot 10^{-6}$ |
| 5 | 1.0 | 0.50000720 | 0.50000000 | $-7.20 \cdot 10^{-6}$ |

With 20 evaluations of $f$ the error at $T = 1$ is $7.2 \cdot 10^{-6}$. Euler's method with the same 20 evaluations ($h = 0.05$) has the error $1.8 \cdot 10^{-3}$.

**Observed orders.** For $h = 0.1, 0.05, 0.025, 0.0125, 0.00625$ the errors at $T = 1$ are:

| method | $s$ | errors | observed orders |
|---|---|---|---|
| Euler | 1 | $3.64 \cdot 10^{-3}$ ... $2.22 \cdot 10^{-4}$ | 1.012, 1.012, 1.008, 1.004 |
| Heun | 2 | $9.19 \cdot 10^{-4}$ ... $3.76 \cdot 10^{-6}$ | 1.959, 1.984, 1.993, 1.996 |
| Kutta's third order | 3 | $1.57 \cdot 10^{-5}$ ... $2.98 \cdot 10^{-9}$ | 3.188, 3.099, 3.051, 3.026 |
| RK4 | 4 | $6.02 \cdot 10^{-7}$ ... $1.05 \cdot 10^{-11}$ | 3.879, 3.954, 3.980, 3.991 |

**A stiff failure.** On $y' = -10y$, $y(0) = 1$, $T = 10$, RK4 is stable when $-2.785 \le h\lambda \le 0$ on the real axis. With $h = 0.27$ ($z = -2.7$) the result is $7.6 \cdot 10^{-3}$, which is small, though still far above the exact $e^{-100}$. With $h = 0.3$ ($z = -3$) it is $1.37 \cdot 10^{4}$.

## Correctness

The loop computes $y_{n+1} = y_n + h_n\Phi(t_n, y_n, h_n)$ with the increment function $\Phi = \sum_i b_i k_i$. If $f$ is Lipschitz with constant $L$, then $\Phi$ is Lipschitz in $y$ with $\Lambda = L\beta(1 + hL\alpha)^{s-1}$, where $\alpha = \max_i\sum_j|a_{ij}|$ and $\beta = \sum_i|b_i|$. If each local error is at most $C h_n^{p+1}$, which holds when $f \in C^p$ and the order conditions up to order $p$ hold, then

$$\|y(t_n) - y_n\| \le \frac{C h^p}{\Lambda}\left(e^{\Lambda(t_n - t_0)} - 1\right).$$

This is a proved, non-asymptotic bound. The proof is the same induction as for the Euler method, with $\Lambda$ in place of $L$. The full proof, with the derivation of the conditions for order 1 and 2, is below. The order conditions for $p \ge 3$ are Butcher's theorem, which we quote with its locator.

## Complexity

Each step evaluates $f$ exactly $s$ times (lines L1 to L3) and forms $s + 1$ linear combinations of up to $s$ vectors of length $d$. So the time is $\Theta(N s (C + s d))$ for $N = \lceil (T - t_0)/h \rceil$ steps, and the evaluations number $Ns$. The extra space is $\Theta(s d)$ for the $s$ slopes. A method of order $p$ reaches an error $\varepsilon$ with $N = \Theta(\varepsilon^{-1/p})$ steps on a fixed interval, so for small $\varepsilon$ higher order pays off even with more stages.

**Order barriers.** An explicit method with $s$ stages has order at most $s$, and for $p \ge 5$ more stages are needed: order 5 needs 6 stages, order 6 needs 7, order 7 needs 9 and order 8 needs 11 (Butcher; HNW I, Section II.5). This is why RK4 is so popular: it is the highest order that costs only one evaluation per order.

## Properties

- **Stability function.** On the test equation $y' = \lambda y$ a step gives $y_{n+1} = R(h\lambda) y_n$ with $R(z) = 1 + z\, b^T(I - zA)^{-1}\mathbf 1 = 1 + \sum_{k \ge 1} z^k\, b^T A^{k-1}\mathbf 1$. For an explicit method $A$ is nilpotent, so $R$ is a polynomial of degree at most $s$. For $p = s \le 4$ the order conditions force $R(z) = \sum_{k=0}^s z^k/k!$. The [stability region](/stability-region/) of a polynomial is bounded, so no explicit method is [A-stable](/a-stability/).
- **One-step and self-starting.** A step needs only $(t_n, y_n)$, so the step size can change at each step with no extra work. This is the base of [embedded pairs](/embedded-runge-kutta-pairs/) for step-size control.
- **Not symplectic.** On the harmonic oscillator, RK4 multiplies $y_1^2 + y_2^2$ by $|R(ih)|^2 = 1 - h^6/72 + h^8/576 < 1$ per step (for $h^2 < 8$), so the energy drifts slowly.
- **Exact on polynomials of degree at most $p$.** If $y$ is a polynomial of degree at most $p$ in $t$ and $f$ depends only on $t$, the method of order $p$ is a quadrature rule of order $p$ and gives $y$ exactly.

## Variants and improvements

- **Low-order members.** The [explicit midpoint method](/explicit-midpoint-method/) and [Heun's method](/heuns-method/) have order 2; [classical RK4](/classical-runge-kutta-4/) and the 3/8 rule have order 4.
- **Embedded pairs.** Two methods that share stages give an error estimate for free: [Runge-Kutta-Fehlberg](/runge-kutta-fehlberg-method/), [Cash-Karp](/cash-karp-method/), [Dormand-Prince](/dormand-prince-method/) and [Bogacki-Shampine](/bogacki-shampine-method/).
- **Implicit methods.** A full matrix $A$ gives [implicit Runge-Kutta methods](/implicit-runge-kutta-methods/), such as [Gauss-Legendre](/gauss-legendre-runge-kutta/) and [Radau IIA](/radau-iia-methods/), which can be A-stable and are used for stiff problems.
- **Linearly implicit methods.** [Rosenbrock methods](/rosenbrock-methods/) put the Jacobian into the stages and solve linear systems only.
- **Dense output.** Extra weights $b_i(\theta)$ give a [continuous approximation](/dense-output/) inside each step.

## When to use it

Use an explicit Runge-Kutta method for nonstiff problems of moderate accuracy, especially when $f$ is cheap, when the step size must change often, or when the solution has events or discontinuities that need restarts. Use it with an embedded error estimate in practice, not with a fixed $h$. For very expensive $f$ and smooth solutions, [linear multistep methods](/linear-multistep-methods/) use fewer evaluations. For stiff problems use an implicit method.

## Pitfalls

- **Inconsistent nodes.** If $c_i \ne \sum_j a_{ij}$, the method can have order $p$ on autonomous problems and a lower order on problems that depend on $t$.
- **Order reduction.** The order $p$ needs $f \in C^p$. With a kink in $f$, or with stiff components, the observed order is lower.
- **Explicit methods on stiff problems.** The step size is limited by stability, not accuracy: RK4 needs $h|\lambda| \le 2.785$ for real negative $\lambda$.
- **Judging a method by order alone.** Two methods of the same order can differ by a large factor in their error constants. The 3/8 rule and RK4 have the same order and the same $R(z)$, but different errors on nonlinear problems.

## Implementations

## History

Runge (1895) proposed methods that evaluate $f$ more than once per step, generalizing the midpoint and trapezoidal rules. Heun (1900) and Kutta (1901) continued the work, and Kutta derived the order conditions up to order 4, the classical fourth-order method and the 3/8 rule. Butcher (1963) organized the order conditions by rooted trees, which made the construction of methods of high order systematic (HNW I, Sections II.1 and II.2).

## References
