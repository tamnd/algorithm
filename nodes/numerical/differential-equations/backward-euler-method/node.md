---
tag: 8ARQ7F
kind: algorithm
slug: backward-euler-method
name: Backward Euler method
aliases:
- implicit Euler method
- BDF1
area: numerical/differential-equations
level: intro
summary: The implicit step y_(n+1) = y_n + h f(t_(n+1), y_(n+1)), solved by Newton's method. Order 1, stability function 1/(1 - z), A-stable and L-stable, so a basic method for stiff problems.
solves: [ode-initial-value-problem, stiff-ode-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps", d: "the dimension of y", k: "the number of Newton iterations in a step"}
  time: {worst: "O(N k d^3)"}
  space: {extra: "Θ(d^2)"}
  evaluations: {worst: "N k"}
properties: {deterministic: true, implicit: true, one_step: true, order: "1", a_stable: true, l_stable: true, symplectic: false}
history:
  year: 1952
  people: [Leonhard Euler, C. F. Curtiss, J. O. Hirschfelder]
  note: Euler described the explicit polygon method in 1768. Curtiss and Hirschfelder (1952) proposed the backward differentiation formulas for stiff equations; backward Euler is the member of order one.
prereqs: [euler-method, ode-initial-value-problem, newton-method-for-systems]
see_also: [a-stability, l-stability, stiff-ode-problem, backward-differentiation-formulas, crank-nicolson-method, radau-iia-methods, rosenbrock-methods, dahlquist-test-equation]
sources:
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.1 (stiff examples, implicit Euler), Section IV.3 (stability function, A-stability and L-stability), Section IV.12 (B-stability and contractivity)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 1, Section 1.4 (the theta method; theta = 0 in Iserles' convention gives backward Euler), Chapter 4, Section 4.2 (linear stability domain and A-stability)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 3, Section 3.4 (stiffness, backward Euler) and Section 3.5 (A-stability and stiff decay)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 7 (absolute stability) and Chapter 8 (stiff ordinary differential equations)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.1 (Euler's method of 1768 and the first Runge-Kutta methods)
  - paper: doi:10.1007/BF01963532
    title: Germund Dahlquist, A special stability problem for linear multistep methods, BIT 3 (1963) 27-43
    locator: the definition of A-stability
  - paper: doi:10.1073/pnas.38.3.235
    title: C. F. Curtiss and J. O. Hirschfelder, Integration of stiff equations, Proceedings of the National Academy of Sciences 38 (1952) 235-243
    locator: the backward difference formulas for stiff equations
---

The backward Euler method solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, with the step $y_{n+1} = y_n + h\, f(t_{n+1}, y_{n+1})$. The new value appears on both sides, so each step solves a system of equations, usually with [Newton's method](/newton-method-for-systems/). The method has order 1, the same as the explicit [Euler method](/euler-method/), but its stability function $R(z) = 1/(1-z)$ makes it [A-stable](/a-stability/) and [L-stable](/l-stability/). For this reason it is the simplest method that works on [stiff problems](/stiff-ode-problem/), where an explicit method needs a step that is far smaller than the accuracy needs.

## In plain words

The explicit Euler method looks at the slope at the start of a step and walks along it. Backward Euler uses the slope at the end of the step instead. It asks: which new point has the property that, if you walk back from it along its own slope, you land on the old point? That question is an equation, and the method solves it at each step. This costs more work than one slope evaluation. The reward is that the method does not explode when the problem has very fast decaying parts. For a quantity that decays to zero, each step of backward Euler also makes it smaller, for every step size. The explicit method only does this when the step is small.

## The problem

**Notation.** On the differential-equations pages, the problem is $y' = f(t, y)$ on $[t_0, T]$ with $y(t_0) = y_0$ and $y(t) \in \mathbb{R}^d$. The step size is $h > 0$, the grid is $t_n = t_0 + n h$, and $y_n$ is the approximation of $y(t_n)$. The global error is $e_n = y(t_n) - y_n$, $p$ is the order, $L$ is a Lipschitz constant of $f$ in $y$, and $\|\cdot\|$ is a vector norm. The test equation is $y' = \lambda y$ with $z = h\lambda$, and $R(z)$ is the stability function.

The input is $f$, $t_0$, $y_0$, the end time $T \ge t_0$ and a step $h > 0$. The Newton solver also uses the Jacobian $J(t, y) = \partial f / \partial y$, given by the caller or approximated by finite differences. The output is the list of pairs $(t_n, y_n)$, with $t_N = T$. If $T - t_0$ is not a multiple of $h$, the last step is shorter.

## The algorithm

```pseudo id=main
BACKWARD-EULER(f, J, t0, y0, T, h)
L1  t ← t0, y ← y0, n ← 0, output (t, y)
L2  while t < T do
L3      n ← n + 1
L4      t′ ← min(t0 + n·h, T)                  ▷ the last step can be shorter
L5      k ← t′ − t, Y ← y                       ▷ Newton starts at the old value
L6      repeat
L7          G ← Y − y − k·f(t′, Y)              ▷ the residual of the step equation
L8          solve (I − k·J(t′, Y)) Δ = −G
L9          Y ← Y + Δ
L10     until ‖Δ‖ ≤ tol · max(1, ‖Y‖)
L11     t ← t′, y ← Y, output (t, y)
```

Line L4 computes the grid point from $t_0$ and $n$, not by adding $h$ again and again, so rounding errors do not move the grid. Lines L6 to L10 are Newton's method for $G(Y) = Y - y_n - k f(t_{n+1}, Y) = 0$, whose Jacobian is $I - kJ$. When $f$ is linear in $y$, $G$ is affine and one Newton step gives the exact solution of the step equation. Production codes freeze $J$ for several steps and keep the LU factors of $I - kJ$ (simplified Newton), which saves most of the linear algebra.

## Example

Take $y' = -10y$, $y(0) = 1$, and $h = 0.25$, so $z = h\lambda = -2.5$. The step equation is $y_{n+1} = y_n - 2.5\, y_{n+1}$, so $y_{n+1} = y_n / 3.5$. The explicit Euler method gives $y_{n+1} = (1 + z) y_n = -1.5\, y_n$.

| $n$ | $t_n$ | backward Euler | explicit Euler | exact $e^{-10 t_n}$ |
|---|---|---|---|---|
| 0 | 0 | 1 | 1 | 1 |
| 1 | 0.25 | 0.285714 | -1.5 | 0.082085 |
| 2 | 0.5 | 0.081633 | 2.25 | 0.006738 |
| 3 | 0.75 | 0.023324 | -3.375 | 0.000553 |
| 4 | 1 | 0.006664 | 5.0625 | 0.000045 |

Both methods are poor at this step size, but backward Euler decays like the true solution and explicit Euler grows with an alternating sign.

A nonlinear case: $y' = -2ty^2$, $y(0) = 1$, whose solution is $y(t) = 1/(1+t^2)$. With $h = 0.5$, the first step solves $y_1 = 1 - 2(0.5)(0.5) y_1^2$, that is $0.5 y_1^2 + y_1 - 1 = 0$, so $y_1 = \sqrt{3} - 1 = 0.732051$ (exact $y(0.5) = 0.8$). The second step solves $y_2 = y_1 - y_2^2$, so $y_2 = (\sqrt{1 + 4y_1} - 1)/2 = 0.490985$ (exact $y(1) = 0.5$). Newton's method of lines L6 to L10, started at $Y = y_n$, stops after 5 iterations in each step, and the last correction is below $10^{-12}$.

## Correctness

The proofs are in `proofs/correctness.md`. They show four facts.

1. **The step is well defined.** If $f$ is Lipschitz in $y$ with constant $L$ and $hL < 1$, the step equation has exactly one solution (by the [Banach fixed-point theorem](/banach-fixed-point-theorem/)). If $f$ satisfies the one-sided condition $\langle f(t,u) - f(t,v), u - v\rangle \le \nu \|u - v\|_2^2$ and $h\nu < 1$, two solutions $y_n, z_n$ obey $\|y_{n+1} - z_{n+1}\|_2 \le \|y_n - z_n\|_2 / (1 - h\nu)$. For $\nu \le 0$ this holds for every $h > 0$, however large $L$ is.
2. **Local error.** If $y \in C^2$ and $M_2 = \max \|y''\|$, the [local truncation error](/local-truncation-error/) $\tau_{n+1} = y(t_{n+1}) - y(t_n) - h f(t_{n+1}, y(t_{n+1}))$ satisfies $\|\tau_{n+1}\| \le M_2 h^2/2$. The method is [consistent](/consistency/) of order 1.
3. **Convergence.** If $f$ is continuous, $L$-Lipschitz in $y$, $y \in C^2$, $e_0 = 0$, $hL \le 1/2$ and each step equation is solved exactly, then
$$\|e_n\| \le \frac{M_2 h}{2L}\left(e^{2L(t_n - t_0)} - 1\right).$$
4. **Stability.** On $y' = \lambda y$ the step is $y_{n+1} = R(z) y_n$ with $R(z) = 1/(1 - z)$. Then $|R(z)| \le 1$ for $\operatorname{Re} z \le 0$ and $R(z) \to 0$ as $|z| \to \infty$.

The bound in fact 3 is proved, not observed, but it is loose: for $y' = -y$ on $[0, 1]$ with $h = 0.1$ it gives $0.319$, while the true error is $0.0177$. The errors at $h = 0.1, 0.05, 0.025$ are $0.01766, 0.00901, 0.00455$, a ratio near 2 at each halving, as order 1 predicts.

## Complexity

The cost model counts evaluations of $f$, evaluations of $J$, and linear solves with the $d \times d$ matrix $I - hJ$. With $N = \lceil (T - t_0)/h \rceil$ steps and $k$ Newton iterations per step, the method on line L6 costs $Nk$ evaluations of $f$, $Nk$ Jacobians and $Nk$ dense solves of $\Theta(d^3)$ operations each. With a finite-difference Jacobian, each Jacobian costs $d$ more evaluations of $f$. Simplified Newton, which reuses one LU factorization over many iterations and steps, lowers this to about one $\Theta(d^3)$ factorization per Jacobian update plus $\Theta(d^2)$ per iteration. The extra memory is the $d \times d$ matrix.

The point of the method is the step count. For the stiff problem $y' = \lambda(y - \cos t)$ with $\lambda = -10^6$ on $[0, 1]$, explicit Euler needs $h < 2 \cdot 10^{-6}$, so more than $5 \cdot 10^5$ steps, before it is even stable. Backward Euler with $h = 0.1$ takes 10 steps and ends within $10^{-6}$ of the solution.

## Properties

- **Order 1.** The error constant is $-1/2$: $\tau_{n+1} = -\tfrac{h^2}{2} y''(t_{n+1}) + O(h^3)$.
- **A-stable and L-stable.** $|R(z)| \le 1$ on the closed left half-plane and $R(\infty) = 0$, so stiff components are damped in one step.
- **B-stable.** By fact 1 with $\nu = 0$, the method never increases the distance between two solutions of a dissipative problem.
- **Too much damping.** $|R(iy)| = 1/\sqrt{1 + y^2} < 1$ for $y \ne 0$. On the harmonic oscillator $y_1' = y_2$, $y_2' = -y_1$ each step multiplies the energy norm by $1/\sqrt{1 + h^2}$, so the orbit spirals into the origin. The method is not [symplectic](/symplectic-integrators/).
- **Member of two families.** It is the one-stage [Radau IIA method](/radau-iia-methods/) and the [backward differentiation formula](/backward-differentiation-formulas/) of order 1. Its [Butcher tableau](/butcher-tableau/) is $A = (1)$, $b = (1)$, $c = (1)$.

## Variants and improvements

- **Theta method.** $y_{n+1} = y_n + h[(1-\theta) f(t_n, y_n) + \theta f(t_{n+1}, y_{n+1})]$. Here $\theta = 1$ is backward Euler, $\theta = 0$ is explicit Euler, and $\theta = 1/2$ is the trapezoidal rule ([Crank-Nicolson](/crank-nicolson-method/) for the heat equation). Iserles writes the weights the other way round.
- **Linearly implicit Euler.** One Newton iteration per step with the Jacobian at $(t_n, y_n)$: $(I - hJ)\Delta = h f(t_n, y_n)$. This is the simplest [Rosenbrock method](/rosenbrock-methods/). It keeps the linear stability of backward Euler.
- **Higher order.** [BDF methods](/backward-differentiation-formulas/) of order 2 to 6 and [Radau IIA](/radau-iia-methods/) methods keep the strong damping with higher accuracy. Extrapolation of the linearly implicit Euler method is the base of the code SEULEX.
- **Error control.** The difference between a backward Euler step and an explicit Euler step estimates the local error, which allows [adaptive step size control](/adaptive-step-size-control/).

## When to use it

Use backward Euler for stiff problems where accuracy of a few digits is enough, as a robust first try, and as the time step of a [method of lines](/method-of-lines/) discretization of the [heat equation](/heat-equation/) when the solution must stay positive and free of oscillations. Use it to start BDF codes. For more accuracy on stiff problems use BDF or Radau IIA. On non-stiff problems an explicit method is cheaper. Do not use it for long runs of oscillating or Hamiltonian systems, where its damping is wrong.

## Pitfalls

- **Fixed-point iteration on a stiff problem.** The iteration $Y \leftarrow y_n + hf(t_{n+1}, Y)$ converges only when $hL < 1$, the same restriction that explicit methods have. Use Newton's method.
- **A Newton failure read as a solution.** Check the convergence test and reduce $h$ when it fails. Do not accept the last iterate after the iteration limit.
- **A Jacobian with the wrong sign or scale.** The matrix is $I - hJ$, not $I + hJ$ or $hJ - I$ with the residual of the other sign.
- **A drifting grid.** Adding $h$ to $t$ in a loop gives $t_{10} \ne 1$ for $h = 0.1$ in binary floating point. Compute $t_n = t_0 + nh$ and clip the last step.
- **A-stable is not accurate.** For $|z| \gg 1$ the method is stable but the transient is not resolved. In the example above, $y_1 = 0.2857$ while $e^{-2.5} = 0.0821$.

## Implementations

## History

Euler described the explicit polygon method in his Institutiones calculi integralis (1768). The implicit form arose as the first member of families of implicit methods. Curtiss and Hirschfelder (1952) named the difficulty of stiff equations and proposed the backward differentiation formulas for them, with backward Euler as the formula of order one. Dahlquist's 1963 paper on A-stability gave the framework in which its stability on the whole left half-plane is the central property. Hairer and Wanner, Section IV.3, use it as the first example of an L-stable method.

## References
