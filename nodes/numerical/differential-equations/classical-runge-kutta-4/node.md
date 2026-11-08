---
tag: 349F36
kind: algorithm
slug: classical-runge-kutta-4
name: Classical Runge-Kutta method (RK4)
aliases:
- RK4
- fourth-order Runge-Kutta
- the Runge-Kutta method
area: numerical/differential-equations
level: core
summary: The explicit four-stage Runge-Kutta method of order 4 published by Kutta in 1901. Four evaluations of f per step give a global error O(h^4) for smooth problems.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps", d: "the dimension of y"}
  time: {worst: "Θ(N d)"}
  space: {extra: "Θ(d)"}
  evaluations: {worst: "4 N"}
properties: {deterministic: true, explicit: true, one_step: true, order: "4", stages: "4", a_stable: false, symplectic: false, error_estimate: false}
history:
  year: 1901
  people: [Carl Runge, Karl Heun, Martin Wilhelm Kutta]
  note: Runge (1895) and Heun (1900) built the first methods of this type. Kutta (1901) derived the order conditions up to order 4 and gave this method.
prereqs: [butcher-tableau, euler-method]
see_also: [runge-kutta-methods, butcher-order-conditions, absolute-stability, adaptive-step-size-control, embedded-runge-kutta-pairs, dormand-prince-method, heuns-method, simpsons-rule]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.1 (the first Runge-Kutta methods, Kutta's methods of order 4), Section II.2 (order conditions), Section II.3 (error estimation and convergence of one-step methods)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 3, Section 31 (order conditions) and Section 32 (low order explicit methods, methods of order 4)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 3, Section 3.2 (explicit Runge-Kutta schemes)
  - paper: "W. Kutta, Beitrag zur näherungsweisen Integration totaler Differentialgleichungen, Zeitschrift für Mathematik und Physik 46 (1901) 435-453"
    locator: the four-stage method of order 4 and the 3/8 rule
  - paper: "C. Runge, Über die numerische Auflösung von Differentialgleichungen, Mathematische Annalen 46 (1895) 167-178"
    locator: the first methods of Runge-Kutta type
---

The classical Runge-Kutta method, RK4, advances the solution of the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$ by evaluating $f$ four times per step, at the start, twice at the midpoint and once at the end, and averaging the four slopes with weights $1/6, 1/3, 1/3, 1/6$. It is an explicit [Runge-Kutta method](/runge-kutta-methods/) of order 4: for a smooth problem its global error is $O(h^4)$, so halving the step divides the error by about 16. For a fixed step size it is the most widely taught and used one-step method, but it has no error estimate and a bounded [stability region](/absolute-stability/), so adaptive codes use [embedded pairs](/embedded-runge-kutta-pairs/) instead and stiff problems need implicit methods.

## In plain words

To move one step forward, the method takes four looks at the slope. It looks at the start. It uses that slope to walk half a step and looks again. It uses the second slope to walk half a step from the start once more and takes a third look. It uses the third slope to walk a full step and takes a fourth look. Then it moves from the start along a weighted average of the four slopes, counting the two middle ones twice. This is the same weighting that Simpson's rule uses for an area. The averaging cancels the errors of the single slopes so well that the error of each step is tiny, and a smaller step makes it shrink very fast.

## The problem

**Notation.** As on all differential-equations pages: $y' = f(t, y)$ on $[t_0, T]$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$; step $h$, grid $t_n = t_0 + nh$, $y_n \approx y(t_n)$; global error $e_n = y(t_n) - y_n$; order $p$; Lipschitz constant $L$; test equation $y' = \lambda y$ with $z = h\lambda$ and stability function $R(z)$.

The input is $f$, $t_0$, $y_0$, $T \ge t_0$ and $h > 0$. The output is the list of pairs $(t_n, y_n)$ with $t_N = T$; the last step is shortened when $T - t_0$ is not a multiple of $h$. The [Butcher tableau](/butcher-tableau/) is
$$\begin{array}{c|cccc} 0 & & & & \\ \tfrac12 & \tfrac12 & & & \\ \tfrac12 & 0 & \tfrac12 & & \\ 1 & 0 & 0 & 1 & \\ \hline & \tfrac16 & \tfrac13 & \tfrac13 & \tfrac16 \end{array}$$

## The algorithm

```pseudo id=main
RK4(f, t0, y0, T, h)
L1  t ← t0, y ← y0, n ← 0, output (t, y)
L2  while t < T do
L3      n ← n + 1, t′ ← min(t0 + n·h, T), η ← t′ − t     ▷ η = h except maybe in the last step
L4      k1 ← f(t, y)
L5      k2 ← f(t + η/2, y + (η/2)·k1)
L6      k3 ← f(t + η/2, y + (η/2)·k2)
L7      k4 ← f(t + η, y + η·k3)
L8      y ← y + (η/6)·(k1 + 2·k2 + 2·k3 + k4)
L9      t ← t′, output (t, y)
```

Line L3 computes the grid point from $t_0$ and $n$ so that rounding does not move the grid, and clips the last step to end at $T$. Lines L4 to L7 are the four stages; each one uses only the previous stage, so the method needs only a few vectors of memory. If $f$ does not depend on $y$, lines L4 to L8 are [Simpson's rule](/simpsons-rule/) for $\int_t^{t+\eta} f(s)\,ds$.

## Example

**One step on $y' = y$.** With $y_0 = 1$ and $h = 0.1$: $k_1 = 1$, $k_2 = 1.05$, $k_3 = 1 + 0.05 \cdot 1.05 = 1.0525$, $k_4 = 1 + 0.1 \cdot 1.0525 = 1.10525$, and
$$y_1 = 1 + \tfrac{0.1}{6}(1 + 2.1 + 2.105 + 1.10525) = 1.1051708333,$$
while $e^{0.1} = 1.1051709181$. The error, $8.5 \cdot 10^{-8}$, is close to the next Taylor term $h^5/120 = 8.3 \cdot 10^{-8}$, since on this problem $y_1 = R(h) = 1 + h + h^2/2 + h^3/6 + h^4/24$.

**A nonlinear problem.** $y' = -2ty^2$, $y(0) = 1$, exact solution $y = 1/(1 + t^2)$. With $h = 0.5$, the first step has $k_1 = 0$, $k_2 = -0.5$, $k_3 = -0.3828125$, $k_4 = -0.6538239$ and gives $y_1 = 0.7983793$ (exact $0.8$). The second step gives $y_2 = 0.4997015$ (exact $0.5$). On $[0, 2]$ the error at $t = 2$ is:

| $h$ | error at $t = 2$ | $\log_2$ of the ratio |
|---|---|---|
| 0.2 | $1.0954 \cdot 10^{-5}$ | |
| 0.1 | $6.5412 \cdot 10^{-7}$ | 4.066 |
| 0.05 | $3.9711 \cdot 10^{-8}$ | 4.042 |
| 0.025 | $2.4430 \cdot 10^{-9}$ | 4.023 |
| 0.0125 | $1.5144 \cdot 10^{-10}$ | 4.012 |

The observed order tends to 4.

## Correctness

The proofs are in `proofs/correctness.md`. In summary:

1. **Order 4.** The tableau satisfies the eight [Butcher order conditions](/butcher-order-conditions/) for the rooted trees with at most four vertices, and fails the condition $\sum_i b_ic_i^4 = 1/5$ of order 5 (it gives $5/24$). By the order condition theorem, if $f$ is $C^4$ near the solution, the local error of one step is $O(h^5)$, and not $O(h^6)$ in general. This is an asymptotic statement with a constant that depends on derivatives of $f$.
2. **Lipschitz increment.** If $f$ is $L$-Lipschitz in $y$, the increment function $\Phi$ with $y_{n+1} = y_n + h\Phi(t_n, y_n, h)$ is Lipschitz with constant $\Lambda = L(1 + hL/2 + (hL)^2/6 + (hL)^3/24)$.
3. **Convergence.** If also $\|\tau_{n+1}\| \le Ch^5$ for all steps, then $\|e_n\| \le Ch^4(e^{\Lambda(t_n - t_0)} - 1)/\Lambda$. So the global error is $O(h^4)$, proved for this hypothesis.

## Complexity

The cost model counts evaluations of $f$. Each step costs exactly 4 evaluations, so $N = \lceil (T - t_0)/h \rceil$ steps cost $4N$ evaluations, plus $\Theta(d)$ arithmetic per stage for the vector updates. The memory is a few vectors of length $d$. To reach a global error $\varepsilon$ on a smooth problem, $h \sim \varepsilon^{1/4}$, so the work grows like $\varepsilon^{-1/4}$; explicit Euler needs work like $\varepsilon^{-1}$ for the same goal.

## Properties

- **Explicit, order 4, four stages.** Butcher proved that an explicit method of order $p \ge 5$ needs more than $p$ stages, so order 4 with 4 stages is the last case where the number of stages equals the order.
- **Stability function.** $R(z) = 1 + z + z^2/2 + z^3/6 + z^4/24$, the same for every 4-stage method of order 4. The stability region contains the real interval $[-2.7853, 0]$ and the imaginary interval $[-2\sqrt2, 2\sqrt2]i$. It is bounded, so the method is not [A-stable](/a-stability/).
- **Not symplectic, not energy-preserving.** On $y_1' = y_2$, $y_2' = -y_1$, each step multiplies $y_1^2 + y_2^2$ by $|R(ih)|^2 = 1 - h^6/72 + h^8/576$, which is $0.99979$ for $h = 0.5$. The energy decays slowly but steadily over long runs.
- **No built-in error estimate.** Step doubling (one step of $2h$ against two of $h$) gives an estimate, but costs $11$ evaluations for every two steps instead of $8$; embedded pairs get an estimate more cheaply.

## Variants and improvements

- **Kutta's 3/8 rule.** Another 4-stage order-4 method, with $b = (1/8, 3/8, 3/8, 1/8)$ and nodes $0, 1/3, 2/3, 1$. Its error constants are slightly smaller.
- **Low-storage versions.** Williamson and other 2-register forms reorganize the stages so that only two vectors of length $d$ are stored, which matters in large PDE simulations.
- **Embedded pairs.** [Runge-Kutta-Fehlberg](/runge-kutta-fehlberg-method/), [Cash-Karp](/cash-karp-method/) and [Dormand-Prince](/dormand-prince-method/) add stages so that a solution of order 4 and one of order 5 come from the same evaluations, which allows [adaptive step size control](/adaptive-step-size-control/).
- **Implicit order 4.** The 2-stage [Gauss method](/gauss-legendre-runge-kutta/) has order 4, is A-stable and symplectic, at the price of a nonlinear system per step.

## When to use it

Use RK4 for non-stiff problems with a fixed step: teaching, games and physics simulations with a fixed frame rate, the time step of a [method of lines](/method-of-lines/) code where a CFL bound fixes $\Delta t$ anyway, and as a reliable reference for testing other methods. For a requested accuracy with unknown solution behaviour, use an adaptive embedded pair. For stiff problems use [BDF](/backward-differentiation-formulas/) or [Radau IIA](/radau-iia-methods/). For long Hamiltonian runs use a [symplectic integrator](/symplectic-integrators/).

## Pitfalls

- **Stiffness.** On $y' = -1000y$ with $h = 0.01$, $z = -10$ lies far outside the stability region and the solution explodes to more than $10^{100}$ by $t = 1$; with $h = 0.002$ ($z = -2$) it decays as it should.
- **Wrong time arguments.** Stages 2 and 3 are evaluated at $t + h/2$ and stage 4 at $t + h$. Using $t$ for all stages keeps order 4 only on autonomous problems.
- **A drifting grid.** Repeated $t \leftarrow t + h$ gives a last time of $0.9999999999999999$ after ten steps of $0.1$, and a tiny extra step. Compute $t_n = t_0 + nh$.
- **Non-smooth $f$.** Order 4 needs $f \in C^4$. Across a jump of $f$ or of a derivative, the observed order drops unless a step ends exactly at the jump.
- **Order is asymptotic.** For large $h$, the error need not fall by 16 when $h$ halves; check the observed order in the range of steps you use.

## Implementations

## History

Runge (1895) proposed to improve the Euler method by evaluating the slope at intermediate points, in analogy with quadrature rules. Heun (1900) gave methods of order up to 3. Kutta (1901) wrote down the conditions for order 4, found the classical method and the 3/8 rule, and studied order 5. Hairer, Nørsett and Wanner describe this history in Section II.1. Butcher's 1963 theory of rooted trees later gave the order conditions for every order in closed form.

## References
