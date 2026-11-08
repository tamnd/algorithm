---
tag: RYE9V7
kind: algorithm
slug: ftcs-method
name: Forward-time centered-space scheme
aliases:
- FTCS
- explicit finite difference scheme for heat
- explicit heat scheme
area: numerical/differential-equations
level: intro
summary: "Explicit scheme u_j^(n+1) = u_j^n + r (u_(j+1)^n - 2 u_j^n + u_(j-1)^n) for u_t = κ u_xx, r = κ Δt/Δx^2. Error O(Δt + Δx^2), stable iff r ≤ 1/2."
solves: [heat-equation]
model: real-ram
complexity:
  vars: {J: "the number of space intervals, 1/Δx", N: "the number of time steps, T/Δt"}
  time: {worst: "Θ(N J)", stable: "Θ(J^3)"}
  space: {extra: "Θ(J)"}
properties: {deterministic: true, implicit: false, order: "1 in time, 2 in space", conditionally_stable: true, maximum_principle: "for r ≤ 1/2"}
history:
  year: 1928
  people: [Richard Courant, Kurt Friedrichs, Hans Lewy]
  note: Courant, Friedrichs and Lewy (1928) showed that difference schemes converge only under conditions on the ratio of the mesh widths; for this explicit heat scheme the condition is r ≤ 1/2.
prereqs: [heat-equation, finite-difference-method, euler-method]
see_also: [crank-nicolson-method, von-neumann-stability-analysis, method-of-lines, lax-equivalence-theorem, courant-friedrichs-lewy-condition, backward-euler-method, adi-method, upwind-scheme]
sources:
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 9 (diffusion equations and parabolic problems; truncation error, the method of lines, stiffness, convergence and von Neumann analysis of the explicit scheme)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 16 (the diffusion equation; the Euler method with the Courant number μ = Δt/Δx^2 and its stability)
  - book: isbn:9780521607933
    title: K. W. Morton and D. F. Mayers, Numerical Solution of Partial Differential Equations, second edition, Cambridge University Press, 2005
    locator: Chapter 2 (parabolic equations in one space variable; the explicit scheme, its truncation error, the maximum principle and convergence)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 6 (parabolic partial differential equations; the forward-time central-space scheme and its stability)
  - paper: doi:10.1007/BF01448839
    title: Richard Courant, Kurt Friedrichs and Hans Lewy, Über die partiellen Differenzengleichungen der mathematischen Physik, Mathematische Annalen 100 (1928) 32-74
    locator: the conditions on the mesh ratio for convergence of difference schemes
---

The forward-time centered-space scheme (FTCS) solves the [heat equation](/heat-equation/) $u_t = \kappa u_{xx}$ by replacing $u_t$ with a forward difference in time and $u_{xx}$ with the centered second difference in space:

$$U^{n+1}_j = U^n_j + r\left(U^n_{j+1} - 2U^n_j + U^n_{j-1}\right), \qquad r = \frac{\kappa\,\Delta t}{\Delta x^2}.$$

Each step is explicit and costs $O(J)$ operations on a grid of $J$ intervals. The scheme is consistent with error $O(\Delta t + \Delta x^2)$, and it is stable, in the maximum norm and in the $\ell^2$ norm, exactly when $r \le \tfrac12$. That limit forces $\Delta t \le \Delta x^2/(2\kappa)$, which makes fine grids expensive.

## In plain words

Picture a metal rod cut into many small pieces, each with its own temperature. Heat flows from a hot piece to its cooler neighbours. In one short tick of time, each piece moves its temperature toward the average of its two neighbours, by an amount that depends on the length of the tick. FTCS does exactly this, piece by piece, tick by tick, using only the temperatures of the last tick.

If the tick is too long compared with the size of a piece, a piece overshoots: it becomes colder than its cold neighbours, then the next tick it becomes hotter than before. These swings grow without end. The scheme only works when the tick is at most half of the square of the piece size, divided by the heat speed.

## The problem

The input is the initial profile $u_0$ on $[0, 1]$, the diffusion coefficient $\kappa > 0$, boundary values $g_L(t) = u(0, t)$ and $g_R(t) = u(1, t)$, the grid $x_j = j\Delta x$ with $\Delta x = 1/J$, the time step $\Delta t$ and the number of steps $N$. The output is the grid function $U^N_j \approx u(x_j, N\Delta t)$, where $u$ solves $u_t = \kappa u_{xx}$ with these data. Errors are measured in the maximum norm $\max_j |u(x_j, t^n) - U^n_j|$.

## The algorithm

```pseudo id=main
FTCS(U0[0..J], κ, Δx, Δt, N, gL, gR)
L1  r ← κ Δt / Δx²
L2  U ← U0
L3  for n ← 0 to N − 1 do
L4      for j ← 1 to J − 1 do V[j] ← U[j] + r (U[j+1] − 2 U[j] + U[j−1])
L5      V[0] ← gL(t^{n+1}), V[J] ← gR(t^{n+1})
L6      U ← V
L7  return U
```

Line L4 reads only old values and writes into a second array $V$, so every new value uses the same time level. Line L5 imposes the Dirichlet data. The scheme is the [method of lines](/method-of-lines/) with the centered second difference in space, followed by [Euler's method](/euler-method/) in time: the semi-discrete system is $U' = (\kappa/\Delta x^2) T U$, and Euler's step with step $\Delta t$ gives line L4.

## Example

Take $\kappa = 1$, $u_0(x) = \sin(\pi x)$, zero boundary values, $\Delta x = 0.2$ and $\Delta t = 0.01$, so $r = 0.25$. The exact solution is $u(x, t) = e^{-\pi^2 t}\sin(\pi x)$. By symmetry $U_3 = U_2$ and $U_4 = U_1$.

| $n$ | $U^n_1$ | $u(0.2, t^n)$ | $U^n_2$ | $u(0.4, t^n)$ |
|---|---|---|---|---|
| 0 | 0.587785 | 0.587785 | 0.951057 | 0.951057 |
| 1 | 0.531657 | 0.532544 | 0.860239 | 0.861674 |
| 2 | 0.480888 | 0.482495 | 0.778093 | 0.780693 |
| 3 | 0.434967 | 0.437149 | 0.703792 | 0.707322 |

The first step at $j = 1$ is $0.587785 + 0.25(0.951057 - 2 \cdot 0.587785 + 0) = 0.531657$. The grid sine is an eigenvector of the scheme: each step multiplies it by $g = 1 - 4r\sin^2(\pi\Delta x/2) = 0.904508$, while the exact factor is $e^{-\pi^2 \Delta t} = 0.906018$.

With $r = 0.25$ fixed and $T = 0.1$, the maximum errors for $J = 10, 20, 40, 80$ are $1.52 \cdot 10^{-3}$, $3.79 \cdot 10^{-4}$, $9.46 \cdot 10^{-5}$, $2.36 \cdot 10^{-5}$: observed order $2.00$ in $\Delta x$, since $\Delta t = r\Delta x^2$. With $r = 1/6$ the errors are $6.69 \cdot 10^{-6}$, $4.16 \cdot 10^{-7}$, $2.59 \cdot 10^{-8}$, $1.62 \cdot 10^{-9}$: order $4.0$.

Stability is sharp. With $J = 20$, the same data plus a perturbation $10^{-10}(-1)^j$, and $T = 0.5$: at $r = 0.5$ (400 steps) the maximum is $0.0070$, close to $e^{-\pi^2/2} = 0.0072$. At $r = 0.52$ (385 steps) the perturbation has grown to a maximum of $9.5$.

## Correctness

The loop computes the scheme exactly (induction on $n$). For convergence, insert the exact solution: by Taylor's formula the truncation error is

$$\tau^n_j = \tfrac12\Delta t\, u_{tt} - \tfrac{1}{12}\kappa\Delta x^2 u_{xxxx} + \text{higher terms} = \tfrac12\kappa\Delta x^2\left(r - \tfrac16\right)u_{xxxx} + O(\Delta t^2 + \Delta x^4),$$

where the second form uses $u_{tt} = \kappa^2 u_{xxxx}$. This is why $r = 1/6$ gives order 4 in the example. For $r \le \tfrac12$ the new value $rU_{j-1} + (1 - 2r)U_j + rU_{j+1}$ is a convex combination, so the error is not amplified in the maximum norm, and the errors of the steps add up:

$$\max_j |u(x_j, t^n) - U^n_j| \le t^n\left(\tfrac12\Delta t \max|u_{tt}| + \tfrac{1}{12}\kappa\Delta x^2\max|u_{xxxx}|\right),$$

when $u_{tt}$ and $u_{xxxx}$ are continuous on the closed domain. For $r > \tfrac12$, the grid mode $\sin(k\pi x_j)$ with $k = J-1$ has factor $g_{J-1} \to 1 - 4r < -1$ as $\Delta x \to 0$, so the scheme is unstable in $\ell^2$ (this is [von Neumann analysis](/von-neumann-stability-analysis/) made exact by the sine eigenvectors). By the [Lax equivalence theorem](/lax-equivalence-theorem/), consistency and stability together are equivalent to convergence. The full proof is below.

## Complexity

Line L4 does 4 additions and 2 multiplications at each of the $J - 1$ interior points, so one step costs $\Theta(J)$ and $N$ steps cost $\Theta(NJ)$ in the [real RAM](/real-ram/) model, with $\Theta(J)$ extra space for $V$. The stability limit makes $N$ grow fast: reaching a fixed time $T$ needs $N = T/\Delta t \ge 2\kappa T J^2$, so the total work is $\Theta(J^3)$. For an error $\varepsilon$ the method needs $\Delta x = \Theta(\varepsilon^{1/2})$, so the work is $\Theta(\varepsilon^{-3/2})$. An implicit scheme with a tridiagonal solve by the [Thomas algorithm](/thomas-algorithm/) also costs $\Theta(J)$ per step but allows $\Delta t$ of the size of $\Delta x$.

## Properties

- **Explicit, two time levels, three points.** Each new value needs three old values and nothing else.
- **Order 1 in time, 2 in space.** Order 2 in $\Delta x$ under $\Delta t = r\Delta x^2$, and order 4 in $\Delta x$ for the special ratio $r = 1/6$.
- **Conditionally stable.** Stable iff $r \le \tfrac12$, in both the maximum norm and the $\ell^2$ norm.
- **Discrete maximum principle for $r \le \tfrac12$.** The new interior values lie between the minimum and the maximum of the old values and the boundary values, as for the true heat equation.
- **Stiffness of the semi-discrete system.** The eigenvalues of $(\kappa/\Delta x^2)T$ lie in $[-4\kappa/\Delta x^2, 0]$, so Euler's real stability interval $[-2, 0]$ gives exactly $r \le \tfrac12$.

## Variants and improvements

- **[Crank-Nicolson method](/crank-nicolson-method/).** The trapezoidal rule in time. Unconditionally stable in $\ell^2$, order 2 in time, one tridiagonal solve per step.
- **Backward time, centered space.** [Backward Euler](/backward-euler-method/) in time. Unconditionally stable and keeps the maximum principle for all $r$.
- **The θ-method.** Mixes the two; it is stable in $\ell^2$ for all $r$ when $\theta \ge \tfrac12$, and for $r \le 1/(2(1 - 2\theta))$ when $\theta < \tfrac12$.
- **Several space dimensions.** In $d$ dimensions on a square grid the condition becomes $r \le 1/(2d)$. The [ADI method](/adi-method/) avoids the limit at the cost of tridiagonal solves.
- **Explicit super-time-stepping.** Runge-Kutta-Chebyshev methods use many cheap explicit stages to stretch the real stability interval to about twice the square of the number of stages.

## When to use it

Use FTCS for a first heat solver, as the baseline in a test, and when the time step must be small anyway, for example because the accuracy in time requires it or because the problem couples diffusion with fast explicit physics. When the grid is fine and the solution is smooth, the condition $\Delta t \le \Delta x^2/(2\kappa)$ wastes most of the work, and Crank-Nicolson or backward Euler with a tridiagonal solve is faster.

## Pitfalls

- **A ratio just above one half.** At $r = 0.52$ the scheme looks fine for many steps, because only the highest grid mode grows, from round-off size. Check $r \le \tfrac12$ before line L3, not by eye.
- **Updating in place.** Writing the new value into $U[j]$ in line L4 makes $U[j-1]$ already new when $U[j]$ is computed. The result is a different method (a Gauss-Seidel-like sweep) with a different error. Write into $V$, then swap in line L6.
- **Using FTCS for advection.** The same centered differencing applied to $u_t + a u_x = 0$ is unstable for every $\Delta t > 0$: the amplification factor is $1 - i\nu\sin\theta$ with $|g|^2 = 1 + \nu^2\sin^2\theta > 1$, where $\nu = a\Delta t/\Delta x$ is the Courant number. Use an [upwind scheme](/upwind-scheme/) or [Lax-Wendroff](/lax-wendroff-method/) there.
- **Refining space but not time.** Halving $\Delta x$ with the same $\Delta t$ multiplies $r$ by 4 and can cross the limit. Keep $r$ fixed when refining.

## Implementations

## History

Courant, Friedrichs and Lewy (1928) showed that the solutions of difference equations converge to the solution of the differential equation only when the ratio of the mesh widths satisfies a condition. For the explicit heat scheme this is the condition $r \le \tfrac12$ on $\kappa\Delta t/\Delta x^2$. The Fourier method of stability analysis that gives the sharp limit is due to von Neumann and became standard after the Second World War (LeVeque, Chapter 9; Strikwerda, Chapter 2).

## References
