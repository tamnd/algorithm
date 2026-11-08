---
tag: NNF3BE
kind: algorithm
slug: crank-nicolson-method
name: Crank-Nicolson method
aliases:
- trapezoidal scheme for the heat equation
- Crank-Nicolson scheme
area: numerical/differential-equations
level: core
summary: An implicit finite difference scheme for the heat equation that averages the space differences at the old and new time levels. It has second order in Δx and Δt and is stable in l2 for every Δt.
solves: [heat-equation]
model: real-ram
complexity:
  vars: {M: "the number of space intervals", N: "the number of time steps"}
  time: {worst: "Θ(N M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, implicit: true, order_space: "2", order_time: "2", unconditionally_stable_l2: true, maximum_principle: "only for r <= 1", l_stable: false}
history:
  year: 1947
  people: [John Crank, Phyllis Nicolson]
  note: Crank and Nicolson proposed the scheme in 1947 for heat conduction problems, as a stable replacement for the explicit scheme with its severe time step limit.
prereqs: [heat-equation, thomas-algorithm]
see_also: [trapezoidal-rule, backward-euler-method, method-of-lines, adi-method, a-stability, l-stability, von-neumann-stability-analysis, courant-friedrichs-lewy-condition]
sources:
  - paper: doi:10.1017/S0305004100023197
    title: "J. Crank and P. Nicolson, A practical method for numerical evaluation of solutions of partial differential equations of the heat-conduction type, Proceedings of the Cambridge Philosophical Society 43 (1947) 50-67"
    locator: the implicit scheme that averages the second differences at two time levels
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 9 (diffusion equations and parabolic problems, the Crank-Nicolson method, local truncation error, stability, the method of lines, stiffness and oscillations)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 16 (the diffusion equation, full discretization and stability by the eigenvalue and Fourier methods)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 6 (parabolic partial differential equations and the Crank-Nicolson scheme)
  - paper: "R. Rannacher, Finite element solution of diffusion problems with irregular data, Numerische Mathematik 43 (1984) 309-327"
    locator: starting with a few backward Euler steps to remove the oscillations of Crank-Nicolson for non-smooth data
---

The Crank-Nicolson method solves the [heat equation](/heat-equation/) $u_t = \kappa u_{xx}$ on a grid. It replaces $u_{xx}$ by the average of the second differences at the old and the new time level. Each time step is then one tridiagonal linear system, solved in $\Theta(M)$ operations by the [Thomas algorithm](/thomas-algorithm/). Seen through the [method of lines](/method-of-lines/), it is the [trapezoidal rule](/trapezoidal-rule/) applied to the system of ODEs for the grid values. The scheme has error $O(\Delta x^2 + \Delta t^2)$, and in the discrete $l^2$ norm it is stable for every ratio $r = \kappa\Delta t/\Delta x^2$. The explicit scheme needs $r \le 1/2$. The price of the large steps is that very rough modes are damped only weakly and change sign each step, so non-smooth data give slowly decaying oscillations when $r$ is large.

## In plain words

Picture a metal bar whose temperature is known at a row of points. Heat flows from warm points to colder neighbours, so each point moves toward the average of its neighbours. The simplest scheme uses only the old temperatures to compute this change. It must take very small time steps, or it blows up. Crank-Nicolson uses the average of the old temperatures and the unknown new ones. This links every new value to its neighbours. Finding them then means solving one chain of equations along the bar, which is cheap. In return the time step can be large and the results stay bounded. The answer is also accurate, because averaging the two time levels cancels most of the time error.

## The problem

**Notation.** The unknown is $u(x, t)$ for $0 \le x \le \ell$ and $0 \le t \le T$, with $u_t = \kappa u_{xx}$, $\kappa \ge 0$, initial data $u(x, 0) = u_0(x)$ and boundary values $u(0, t) = g_0(t)$, $u(\ell, t) = g_1(t)$. The grid is $x_j = j\Delta x$ with $\Delta x = \ell/M$, and $t_n = n\Delta t$. The grid values are $U^n_j \approx u(x_j, t_n)$, and $r = \kappa\Delta t/\Delta x^2$. Write $(\delta^2U)_j = U_{j-1} - 2U_j + U_{j+1}$. Errors and stability are measured in the discrete $l^2$ norm $\|U\|_{\Delta x} = (\Delta x\sum_j U_j^2)^{1/2}$ or in the max norm $\|U\|_\infty = \max_j|U_j|$, as stated in each claim. In the [method of lines](/method-of-lines/) view, $U' = (\kappa/\Delta x^2)\,\delta^2U$ is an ODE system $y' = f(t, y)$ whose eigenvalues lie in $[-4\kappa/\Delta x^2, 0]$.

The scheme is
$$\frac{U^{n+1}_j - U^n_j}{\Delta t} = \frac{\kappa}{2\Delta x^2}\big((\delta^2U^{n+1})_j + (\delta^2U^n)_j\big), \qquad j = 1, \dots, M - 1,$$
with $U^{n+1}_0 = g_0(t_{n+1})$ and $U^{n+1}_M = g_1(t_{n+1})$. In matrix form, $(I - \tfrac r2\delta^2)U^{n+1} = (I + \tfrac r2\delta^2)U^n$ plus boundary terms. The input is $u_0$, $\kappa$, $\ell$, $T$, $M$ and a requested $\Delta t$. The implementation takes $N = \lceil T/\Delta t\rceil$ equal steps of size $T/N$, so the last step lands on $T$ and $r$ stays the same for all steps.

## The algorithm

```pseudo id=main
CRANK-NICOLSON(u0, κ, ℓ, T, M, Δt, g0, g1)
L1  Δx ← ℓ/M, N ← ⌈T/Δt⌉, Δt ← T/N, r ← κΔt/Δx², U_j ← u0(x_j)
L2  for n ← 0 to N − 1 do
L3      for j ← 1 to M − 1 do d_j ← U_j + (r/2)·(U_{j−1} − 2U_j + U_{j+1})
L4      d_1 ← d_1 + (r/2)·g0(t_{n+1}), d_{M−1} ← d_{M−1} + (r/2)·g1(t_{n+1})
L5      solve −(r/2)·V_{j−1} + (1 + r)·V_j − (r/2)·V_{j+1} = d_j, j = 1..M−1, by the Thomas algorithm
L6      U ← (g0(t_{n+1}), V_1, …, V_{M−1}, g1(t_{n+1}))
L7  return U
```

Line L3 applies the explicit half of the step. Line L4 moves the known new boundary values to the right side. Line L5 is the implicit half. Its matrix is symmetric, strictly diagonally dominant ($1 + r > r$) and the same at every step, so the Thomas algorithm needs no pivoting. The implementation also offers the $\theta$-scheme. It weights $\delta^2U^{n+1}$ by $\theta$ and $\delta^2U^n$ by $1 - \theta$: $\theta = 1/2$ is Crank-Nicolson, $\theta = 1$ is [backward Euler](/backward-euler-method/) and $\theta = 0$ is the explicit FTCS scheme. It also offers zero-flux (Neumann) boundaries with ghost points $U_{-1} = U_1$, $U_{M+1} = U_{M-1}$.

## Example

**One step by hand.** Take $\kappa = \ell = 1$, $M = 4$ and $\Delta t = 1/16$, so $r = 1$, with $u_0 = \sin\pi x$ and $g_0 = g_1 = 0$. Write $a = \sin(\pi/4) = \sqrt2/2$, so $U^0 = (0, a, 1, a, 0)$. Line L3 gives $d_1 = a + \tfrac12(1 - 2a) = 0.5$, $d_2 = 1 + \tfrac12(2a - 2) = a$ and $d_3 = 0.5$. The system is $2V_1 - \tfrac12V_2 = 0.5$, $-\tfrac12V_1 + 2V_2 - \tfrac12V_3 = a$, $-\tfrac12V_2 + 2V_3 = 0.5$. By symmetry $V_1 = V_3 = p$ and $V_2 = q$, so $p = 0.25 + 0.25q$ and $2q - p = a$. That gives $q = (a + 0.25)/1.75 = 0.546918$ and $p = 0.386730$. The exact values are $e^{-\pi^2/16} = 0.539641$ and $0.381584$. The discrete mode $\sin(\pi x_j)$ is multiplied by exactly $g = (1 - 2s)/(1 + 2s)$ with $s = \sin^2(\pi\Delta x/2)$, which is $0.546918$ here.

**Convergence.** With $\kappa = 1$, $u_0 = \sin\pi x$, $T = 0.1$ and $\Delta t = \Delta x/10$, the max-norm error at $T$ is:

| $M$ | Crank-Nicolson | ratio $\log_2$ | backward Euler | ratio $\log_2$ |
|---|---|---|---|---|
| 10 | $2.7337 \cdot 10^{-3}$ | | $2.0320 \cdot 10^{-2}$ | |
| 20 | $6.8214 \cdot 10^{-4}$ | 2.003 | $9.6309 \cdot 10^{-3}$ | 1.077 |
| 40 | $1.7045 \cdot 10^{-4}$ | 2.001 | $4.6785 \cdot 10^{-3}$ | 1.042 |
| 80 | $4.2608 \cdot 10^{-5}$ | 2.000 | $2.3044 \cdot 10^{-3}$ | 1.022 |
| 160 | $1.0652 \cdot 10^{-5}$ | 2.000 | $1.1434 \cdot 10^{-3}$ | 1.011 |

Here $r = M/10$ grows from 1 to 16, and Crank-Nicolson still converges with order 2.

**Oscillation.** Put $U^0 = 1$ at the middle node of $M = 50$ intervals and 0 elsewhere, and take $\Delta t = 0.01$, so $r = 25$. The centre value after 1, 2, 3 and 4 steps is $-0.720$, $0.725$, $-0.591$, $0.599$. The exact solution is positive everywhere. Backward Euler with the same step stays positive, and Crank-Nicolson with $r = 1$ also stays in $[0, 1]$.

## Correctness

The proofs are in `proofs/correctness.md`. In summary:

1. **Truncation error.** If $u$ is smooth ($u_{ttt}$, $u_{xxtt}$ and $u_{xxxx}$ bounded), then inserting $u$ in the scheme leaves a residual $\tau = O(\Delta t^2 + \Delta x^2)$ in the max norm. The expansion is centred at $t_{n+1/2}$.
2. **Unconditional $l^2$ stability.** The step matrix $C = (I - \tfrac r2\delta^2)^{-1}(I + \tfrac r2\delta^2)$ is symmetric with eigenvalues $g_k = (1 - 2rs_k)/(1 + 2rs_k) \in (-1, 1)$, where $s_k = \sin^2(k\pi\Delta x/2)$. So $\|CU\|_{\Delta x} \le \|U\|_{\Delta x}$ for every $r > 0$. This is proved.
3. **Convergence.** With exact boundary values, $\|e^n\|_{\Delta x} \le \|e^0\|_{\Delta x} + t_n\sqrt\ell\,\max_m\|\tau^m\|_\infty$. The error is therefore $O(\Delta x^2 + \Delta t^2)$ in $l^2$, with no restriction on $r$. This is proved. Order 2 in the max norm is observed in the table.
4. **Maximum principle.** If $r \le 1$, then $\min(U^n, \text{boundary data}) \le U^{n+1}_j \le \max(U^n, \text{boundary data})$. For $r > 1$ this fails, as the oscillation example shows.
5. **Conservation.** With zero-flux boundaries, the trapezoidal total $\Delta x(\tfrac12U_0 + U_1 + \dots + U_{M-1} + \tfrac12U_M)$ is exactly constant in exact arithmetic.

## Complexity

Each step costs $\Theta(M)$ operations: $\Theta(M)$ for the right side and $\Theta(M)$ for the Thomas solve. There is one tridiagonal solve per step and no Jacobian, since the problem is linear. $N$ steps cost $\Theta(NM)$ time and $\Theta(M)$ memory. The matrix is the same for all steps, so its elimination factors can be computed once. For a target error $\varepsilon$, choosing $\Delta x \sim \Delta t \sim \varepsilon^{1/2}$ gives work $\Theta(\varepsilon^{-1})$. The explicit scheme needs $\Delta t \le \Delta x^2/(2\kappa)$ and work $\Theta(\varepsilon^{-3/2})$.

## Properties

- **Second order in both $\Delta x$ and $\Delta t$.** The scheme is centred at $t_{n+1/2}$.
- **A-stable but not L-stable.** On the ODE level the trapezoidal rule has $R(z) = (1 + z/2)/(1 - z/2)$, which is [A-stable](/a-stability/), but $R(z) \to -1$ as $z \to -\infty$, so it is not [L-stable](/l-stability/). The highest grid mode has $z = -4r$, so for large $r$ it is multiplied by nearly $-1$ in each step.
- **Unconditionally stable in $l^2$.** This holds in the norm $\|\cdot\|_{\Delta x}$. Stability in the max norm for every $r$ is a more delicate question and is not treated here.
- **Maximum principle only for $r \le 1$.** Backward Euler satisfies it for every $r$.
- **Exact for quadratics.** If $u = a + bx + cx^2 + 2c\kappa t$, the scheme reproduces $u$ exactly, because $\delta^2$ is exact on quadratics and the trapezoidal rule is exact on linear functions of $t$.

## Variants and improvements

- **The $\theta$-method.** $\theta = 1$ (backward Euler) is first order in time, L-stable and monotone. $\theta \ge 1/2$ gives $l^2$ stability for every $r$, and $\theta < 1/2$ needs $r \le 1/(2(1 - 2\theta))$.
- **Rannacher start-up.** Take two or four backward Euler steps (often with half the step size) before switching to Crank-Nicolson. This damps the rough modes of non-smooth data and keeps the order 2. It is standard in option pricing.
- **TR-BDF2 and L-stable second-order schemes.** These combine a trapezoidal stage with a BDF2 stage, so that $R(-\infty) = 0$.
- **More dimensions.** In 2D and 3D the implicit system is no longer tridiagonal. The [ADI method](/adi-method/) splits each step into one-dimensional tridiagonal solves.
- **Variable coefficients and nonlinear diffusion.** The same averaging applies to $u_t = (a(x)u_x)_x$. For a nonlinear $a(u)$ each step needs a Newton iteration or a linearization.

## When to use it

Use Crank-Nicolson for diffusion problems with smooth data when second order accuracy in time matters and $\Delta t$ should be far larger than the explicit limit $\Delta x^2/(2\kappa)$. Typical cases are the heat equation, the Black-Scholes equation after a change of variables, and the time step of a Schrödinger solver, where it also preserves the $l^2$ norm. For non-smooth initial data, use the Rannacher start or an L-stable scheme. When only monotone results are acceptable, use backward Euler or keep $r \le 1$.

## Pitfalls

- **Oscillations for rough data.** With $r = 25$ a single hot node produces a centre value that alternates in sign, as in the example. They decay only like $|g_{\max}|^n$, with $|g_{\max}|$ close to 1. Do not mistake them for physics.
- **Boundary values at the wrong time.** Using $g(t_n)$ on the left side instead of $g(t_{n+1})$ makes the boundary treatment first order and can spoil the global order.
- **Mismatched data.** If $u_0(0) \ne g_0(0)$, the solution has a corner at $t = 0$, and the order drops near the boundary for small $t$.
- **Varying the time step.** Changing $\Delta t$ changes $r$ and the matrix, which must then be set up again. The implementation keeps all steps equal, so a requested $\Delta t$ that does not divide $T$ is shortened slightly.
- **Explicit comparison.** FTCS ($\theta = 0$) with $r = 0.6$ amplifies the highest mode by $|1 - 4r\sin^2(\cdot)| \approx 1.4$ per step and blows up from rounding-level noise. With $r = 0.5$ it stays bounded. Crank-Nicolson is fine at both values.

## Implementations

## History

Crank and Nicolson (1947) introduced the scheme for problems of heat conduction type, where the explicit methods of the time either were unstable or needed very small steps. The analysis of stability by Fourier modes, due to von Neumann, came into wide use in the same years. It explains both the unconditional stability and the weak damping of rough modes. Rannacher (1984) analysed the start-up with backward Euler steps that is now standard for non-smooth data.

## References
