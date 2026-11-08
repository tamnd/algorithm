---
tag: K94YNY
kind: algorithm
slug: upwind-scheme
name: Upwind scheme
aliases:
- upwind differencing
- first-order upwind
- Courant-Isaacson-Rees scheme
- donor cell scheme
area: numerical/differential-equations
level: core
summary: "Difference in the direction the information flows: for u_t + a u_x = 0, use the neighbour on the side the wind comes from. Monotone and stable for |ν| <= 1, first order, diffusive."
solves: [advection-equation, burgers-equation]
model: real-ram
complexity:
  vars: {m: "the number of cells", N: "the number of time steps, ⌈T/Δt⌉", C: "the cost of one evaluation of the flux f (nonlinear case)"}
  time: {worst: "Θ(N m (C + 1))"}
  space: {extra: "Θ(m)"}
  evaluations: {worst: "N m"}
properties: {deterministic: true, explicit: true, conservative: true, order: "1", monotone: "for |ν| <= 1", stable_for: "0 <= ν <= 1 (a >= 0)", tvd: true}
history:
  year: 1952
  people: [Richard Courant, Eugene Isaacson, Mina Rees]
  note: Courant, Isaacson and Rees (1952) solved hyperbolic systems with one-sided differences taken along the direction of the characteristics, the scheme now called upwind.
prereqs: [advection-equation, courant-friedrichs-lewy-condition, finite-differences]
see_also: [lax-friedrichs-scheme, lax-wendroff-method, godunov-method, von-neumann-stability-analysis, total-variation-diminishing, burgers-equation, flux-limiter-methods, method-of-characteristics]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 4.10 (the upwind method for advection), Section 4.12 (the CFL condition), Chapter 8 (convergence, accuracy and stability), Chapter 12 (nonlinear scalar conservation laws, monotone methods, the Lax-Wendroff theorem)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 10 (advection equations and hyperbolic systems; upwind methods, von Neumann analysis, modified equations)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 1 (one-way wave equation, forward-time backward-space scheme, CFL condition), Chapter 2 (von Neumann analysis)
  - book: isbn:9780521607933
    title: K. W. Morton and D. F. Mayers, Numerical Solution of Partial Differential Equations, second edition, Cambridge University Press, 2005
    locator: Chapter 4 (hyperbolic equations in one space dimension; the upwind scheme, its error analysis and the maximum principle)
  - paper: "Richard Courant, Eugene Isaacson and Mina Rees, On the solution of nonlinear hyperbolic differential equations by finite differences, Communications on Pure and Applied Mathematics 5 (1952) 243-255"
    locator: one-sided differences along characteristics
  - paper: "Michael G. Crandall and Andrew Majda, Monotone difference approximations for scalar conservation laws, Mathematics of Computation 34 (1980) 1-21"
    locator: convergence of monotone conservative schemes to the entropy solution
---

The upwind scheme solves the [advection equation](/advection-equation/) $u_t + a u_x = 0$ by replacing $u_x$ with a one-sided difference taken on the side the flow comes from. For $a > 0$ that is the backward difference, giving $U_j^{n+1} = U_j^n - \nu(U_j^n - U_{j-1}^n)$ with Courant number $\nu = a\Delta t/\Delta x$. For $0 \le \nu \le 1$ the new value is a weighted average of old values, which makes the scheme stable, monotone and free of oscillations. The price is first-order accuracy and strong smearing of fronts. In conservation form it extends to nonlinear laws such as [Burgers' equation](/burgers-equation/) and is the starting point of [Godunov's method](/godunov-method/).

## In plain words

Smoke carried by the wind at a steady speed only depends on what was upwind of it a moment ago. So to update a cell, look at the cell the wind is blowing from, not the one it is blowing to. The new amount of smoke in a cell is a blend of what it had and what its upwind neighbour had, with more of the neighbour when the wind is fast or the time step long.

A blend never makes a new maximum or minimum, so the method cannot invent wiggles. But blending also mixes neighbours a little every step, so sharp edges get blurred over time. If the time step is so long that the smoke would travel past the neighbour, the blend needs a negative weight and the numbers blow up. Taking the neighbour on the wrong side blows up too.

## The problem

Given the speed $a$, initial cell values $U_j^0$ on $m$ cells of width $\Delta x$, a time step $\Delta t$ and an end time $T \ge 0$, compute $U_j^N \approx u(x_j, T)$, where $u(x, t) = u_0(x - at)$ is the exact solution. Boundary conditions are periodic or transmissive (ghost cells copy the edge value). The error is measured in the max norm over the grid. The nonlinear version takes a flux $f$ and solves $u_t + f(u)_x = 0$, with cost measured in evaluations of $f$.

## The algorithm

```pseudo id=main
UPWIND(U^0, a, Δx, Δt, T, bc)
L1  N ← ⌈T/Δt − δ⌉                         ▷ δ: relative slack 10^-9 against rounding
L2  U ← U^0, t ← 0
L3  for n ← 0 to N − 1 do
L4      t_next ← T if n = N − 1 else (n + 1)Δt
L5      ν ← a (t_next − t)/Δx               ▷ the Courant number of this step
L6      add ghost values U_{−1}, U_m from bc ▷ periodic: wrap; transmissive: copy
L7      if a ≥ 0 then U_j ← U_j − ν (U_j − U_{j−1}) for all j     ▷ from the old values
L8      else U_j ← U_j − ν (U_{j+1} − U_j) for all j
L9      t ← t_next
L10 return U
```

Lines L7 and L8 pick the neighbour on the side the wind comes from. Both are the single formula $U_j \leftarrow U_j - \nu^+(U_j - U_{j-1}) - \nu^-(U_{j+1} - U_j)$ with $\nu^+ = \max(\nu, 0)$ and $\nu^- = \min(\nu, 0)$. As with the time-stepping pages, $T = 0$ gives zero steps and a $\Delta t$ beyond $T$ gives one short step.

**Conservation form.** For $u_t + f(u)_x = 0$, write $U_j^{n+1} = U_j^n - \frac{\Delta t}{\Delta x}(F_{j+1/2} - F_{j-1/2})$ with the upwind flux $F_{j+1/2} = f(U_j)$ if the jump speed $s_{j+1/2} = (f(U_{j+1}) - f(U_j))/(U_{j+1} - U_j)$ is $\ge 0$, and $f(U_{j+1})$ otherwise (the Murman-Roe choice). For $f(u) = au$ this is lines L7 and L8. The implementation provides both forms.

## Example

Take $a = 1$, $m = 100$ cells on the periodic interval $[0, 1)$, and the box $u_0 = 1$ on $[0.25, 0.5)$, else 0. After one full period $T = 1$ the exact solution is the box again. The observed max value and $L^1$ error are:

| $\nu$ | 0.2 | 0.5 | 0.8 | 1.0 |
|---|---|---|---|---|
| $\max_j U_j$ | 0.838 | 0.923 | 0.995 | 1.000 |
| $L^1$ error | 0.142 | 0.113 | 0.071 | 0 (up to rounding) |

All values stay in $[0, 1]$, and the sum of the cell values is unchanged. The smaller $\nu$, the more smearing, as the numerical diffusion $\frac{a\Delta x}{2}(1 - \nu)$ predicts. At $\nu = 1$ the scheme shifts the data by exactly one cell per step.

For the smooth wave $u_0 = \sin 2\pi x$ with $\nu = 0.5$ and $T = 1$, the max-norm errors for $m = 50, 100, 200, 400$ are $0.1792$, $0.0940$, $0.0481$, $0.0244$, observed order $0.93$, $0.97$, $0.98$, tending to 1.

## Correctness

**Theorem (proved).** Let $a \ge 0$, $0 \le \nu \le 1$, and let $u_0 \in C^2$ be periodic with $M = \max|u_0''|$. Then $\max_j |u(x_j, t_n) - U_j^n| \le t_n \frac{a\Delta x}{2}(1 + \nu) M$. If $\nu > 1$ the scheme is unstable: the mode $(-1)^j$ grows by the factor $|1 - 2\nu| > 1$ per step.

The proof writes line L7 as the convex combination $(1 - \nu)U_j + \nu U_{j-1}$, which gives the maximum principle, monotonicity, conservation and the TVD property at once, and adds up the [local truncation errors](/local-truncation-error/) $O(\Delta x)$. In Fourier terms the amplification factor is $g(\theta) = 1 - \nu(1 - e^{-i\theta})$ with $|g|^2 = 1 - 2\nu(1 - \nu)(1 - \cos\theta)$, the [von Neumann](/von-neumann-stability-analysis/) form of the same limit. The limit $\nu \le 1$ coincides with the [CFL condition](/courant-friedrichs-lewy-condition/), so here the CFL condition is both necessary and sufficient. For nonlinear laws with $f' \ge 0$, the conservative scheme is monotone when $\frac{\Delta t}{\Delta x}\max f' \le 1$, and monotone conservative schemes converge to the entropy solution (Crandall and Majda 1980, cited, not proved).

## Complexity

Each step does $\Theta(m)$ arithmetic, and the nonlinear form evaluates $f$ once per cell, so $N$ steps cost $\Theta(N m (C + 1))$ with $N m$ flux evaluations. The new values need a second array, or a sweep against the wind direction, so the extra space is $\Theta(m)$ or $\Theta(1)$. To reach a fixed time with $\nu$ fixed, $N = \Theta(m)$, so the total is $\Theta(m^2)$ in one dimension, and an error $\varepsilon$ needs $m = \Theta(1/\varepsilon)$.

## Properties

- **Order.** First order in space and time; the error is $O(\Delta x)$ at fixed $\nu$.
- **Stability.** Stable in the max norm and in $\ell^2$ exactly for $0 \le \nu \le 1$ ($a \ge 0$), or $-1 \le \nu \le 0$ ($a < 0$).
- **Monotone, TVD and positivity preserving** for $|\nu| \le 1$. By Godunov's theorem, a linear monotone scheme cannot be better than first order, so upwind is optimal among linear monotone schemes in that sense.
- **Conservative** in the flux form; the sum $\sum_j U_j \Delta x$ only changes by boundary fluxes.
- **Numerical diffusion.** The modified equation is $u_t + a u_x = \frac{a\Delta x}{2}(1 - \nu) u_{xx}$.
- **Exact at $\nu = 1$**, where it shifts the grid values by one cell.

## Variants and improvements

- **Second-order upwind (Beam-Warming)** uses two upwind neighbours; it is second order but oscillates near jumps.
- **[Lax-Wendroff](/lax-wendroff-method/)** is centered and second order; [flux limiters](/flux-limiter-methods/) switch between it and upwind to stay [TVD](/total-variation-diminishing/).
- **[Godunov's method](/godunov-method/)** replaces the Roe flux by the exact Riemann solution, which handles sign changes of $f'$ correctly.
- **Flux vector splitting** (Steger-Warming, van Leer) splits the flux of a system into right- and left-moving parts and upwinds each.
- **Higher order** reconstructions such as MUSCL and WENO keep the upwind idea with more cells.
- **[Lax-Friedrichs](/lax-friedrichs-scheme/)** needs no wind direction but is more diffusive.

## When to use it

Use upwind when robustness matters more than accuracy: as a first scheme for an advection problem, inside a [finite volume method](/finite-volume-method/) as the low-order fallback of a limiter, for positive quantities such as densities that must stay nonnegative, and for the [eikonal equation](/eikonal-equation/) and other Hamilton-Jacobi problems. For smooth solutions where accuracy per cell matters, prefer a second-order or spectral method.

## Pitfalls

- **Courant number just above 1.** With $\nu = 1.01$ on the box example the max value is 2.65 after $T = 1$, 1540 after $T = 5$ and $1.7 \times 10^7$ after $T = 10$ (observed). With $\nu = 0.99$ it stays in $[0, 1]$.
- **The wrong side.** Downwind differencing $U_j - \nu(U_{j+1} - U_j)$ with $a > 0$ has $|g(\theta)| > 1$ for every $\theta \ne 0$, whatever $\Delta t$.
- **Non-conservative form.** For Burgers' equation, $U_j - \lambda U_j(U_j - U_{j-1})$ looks like upwind for $u u_x$, but for the jump from 1 to 0 it never moves the shock, while the true speed is $\frac12$. The conservative scheme puts the shock within a few cells of the right place.
- **Sonic points.** Where $f'$ changes sign, the Roe flux keeps the stationary jump from $-1$ to $1$ in Burgers' equation forever, though the entropy solution is a rarefaction fan. An entropy fix or Godunov's flux is needed.
- **Accuracy.** A front is spread over about $\sqrt{a\Delta x(1 - \nu)T}$ after time $T$, which needs very fine grids to keep sharp.

## Implementations

## History

Courant, Isaacson and Rees (1952) computed hyperbolic systems with one-sided differences chosen along the characteristic directions, which is the upwind idea. Godunov (1959) interpreted upwind as the solution of local Riemann problems and proved that linear monotone schemes are at most first order. Crandall and Majda (1980) proved convergence of monotone conservative schemes to the entropy solution (LeVeque 2002, Chapters 4 and 12).

## References
