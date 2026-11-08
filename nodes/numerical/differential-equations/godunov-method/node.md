---
tag: H99E04
kind: algorithm
slug: godunov-method
name: Godunov's method
aliases:
- Godunov scheme
- Godunov's scheme
- Godunov upwind method
area: numerical/differential-equations
level: advanced
summary: "Finite volume scheme whose flux at each cell face is f of the exact Riemann solution there. First order, conservative, monotone under CFL 1, and entropy satisfying at transonic rarefactions."
solves: [burgers-equation, advection-equation]
model: real-ram
complexity:
  vars: {m: "the number of cells", N: "the number of time steps, ⌈T/Δt⌉"}
  time: {worst: "Θ(N m)"}
  space: {extra: "Θ(m)"}
  evaluations: {worst: "N (m + 1)"}
properties: {deterministic: true, explicit: true, conservative: true, monotone: true, order: "1", entropy_satisfying: true}
history:
  year: 1959
  people: [S. K. Godunov]
  note: Godunov (1959) proposed replacing the solution by cell averages and evolving them with exact Riemann solutions for gas dynamics, and proved that linear schemes preserving monotonicity are at most first order accurate.
prereqs: [finite-volume-method, riemann-problem]
see_also: [burgers-equation, upwind-scheme, lax-friedrichs-scheme, flux-limiter-methods, total-variation-diminishing, courant-friedrichs-lewy-condition, weno-scheme, lax-wendroff-method]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 4 (REA algorithm, Godunov's method for advection), Chapter 11 (Riemann problem for a convex scalar flux, Rankine-Hugoniot and entropy conditions), Chapter 12 (Godunov's method for nonlinear scalar problems, transonic rarefactions, entropy fixes, monotone methods)
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 5 (Godunov's method for scalar conservation laws), Chapter 6 (Godunov's method for nonlinear systems), Chapter 4 (exact Riemann solver for the Euler equations)
  - paper: doi:10.1137/1025002
    title: Amiram Harten, Peter D. Lax and Bram van Leer, On upstream differencing and Godunov-type schemes for hyperbolic conservation laws, SIAM Review 25(1) (1983) 35-61
    locator: Godunov-type schemes, the integral form of the Godunov flux, the HLL approximate Riemann solver
  - paper: doi:10.1090/S0025-5718-1980-0551288-3
    title: Michael G. Crandall and Andrew Majda, Monotone difference approximations for scalar conservation laws, Mathematics of Computation 34(149) (1980) 1-21
    locator: convergence of conservative monotone schemes to the entropy solution
  - paper: doi:10.1016/0021-9991(79)90145-1
    title: Bram van Leer, Towards the ultimate conservative difference scheme V, a second-order sequel to Godunov's method, Journal of Computational Physics 32(1) (1979) 101-136
    locator: MUSCL, piecewise linear reconstruction with limited slopes on top of the Godunov flux
---

Godunov's method is the [finite volume method](/finite-volume-method/) for a conservation law $u_t + f(u)_x = 0$ in which the numerical flux at each cell face comes from the exact solution of a local [Riemann problem](/riemann-problem/). It treats the cell averages as a piecewise constant function, solves exactly the Riemann problem formed by the two constant states at each face, takes the flux of that solution on the face, and updates the averages: $u_i^{n+1} = u_i^n - \frac{\Delta t}{\Delta x}\big(f(u^*_{i+1/2}) - f(u^*_{i-1/2})\big)$, where $u^*_{i+1/2}$ is the Riemann solution's value at the face. Under the CFL condition this equals evolving the piecewise constant data exactly for one step and averaging again. The scheme is first order, conservative and monotone. Because the Riemann solutions satisfy the entropy condition, it computes the physically correct solution, including the transonic rarefactions that simpler upwind fluxes get wrong. Godunov-type schemes are the basis of modern shock-capturing methods.

## In plain words

Imagine a row of compartments, each holding a uniform amount of something that flows, such as cars on a road. At each wall between two compartments, the two different uniform states meet, and for that simple situation, two constant states meeting at a wall, the exact behaviour is known: a sharp front such as a traffic jam forms, or the cars spread out smoothly. The method works out, at every wall, what that exact behaviour would send through the wall, then updates each compartment by what came in minus what went out. Then it forgets the detailed shape again and keeps only one average per compartment. Using the exact local answer makes the method choose the physically right behaviour, so a spreading flow is never mistaken for a jam.

## The problem

Given a convex flux $f \in C^1(\mathbb{R})$ (so $f'$ is nondecreasing), initial data $u_0$ on $[a, b]$, boundary conditions and a final time $T$, approximate the entropy solution of $u_t + f(u)_x = 0$ in the discrete $L^1$ norm, using $m$ cells of width $\Delta x$. The Riemann problem with data $u_L$ for $x < 0$ and $u_R$ for $x > 0$ has a self-similar entropy solution $u(x, t) = w(x/t)$ (LeVeque 2002, Chapter 11):

- if $u_L > u_R$, a shock moving at the Rankine-Hugoniot speed $\sigma = \frac{f(u_L) - f(u_R)}{u_L - u_R}$;
- if $u_L \le u_R$, a rarefaction fan, $w(\xi) = u_L$ for $\xi \le f'(u_L)$, $w(\xi) = u_R$ for $\xi \ge f'(u_R)$, and $w(\xi) = (f')^{-1}(\xi)$ in between.

The face state is $u^* = w(0)$. The cost is counted in Riemann solves, one per face per step.

## The algorithm

For a convex flux the face state has a closed form, with $u_s$ the sonic point where $f'(u_s) = 0$:

$$u^*(u_L, u_R) = \begin{cases} u_L & u_L > u_R,\ \sigma \ge 0, \\ u_R & u_L > u_R,\ \sigma < 0, \\ u_L & u_L \le u_R,\ f'(u_L) \ge 0, \\ u_R & u_L \le u_R,\ f'(u_R) \le 0, \\ u_s & u_L < u_s < u_R \ \text{(transonic rarefaction).} \end{cases}$$

Equivalently (Osher's formula), $f(u^*) = \min_{u_L \le u \le u_R} f(u)$ if $u_L \le u_R$ and $\max_{u_R \le u \le u_L} f(u)$ if $u_L > u_R$; the tests use this second form as an independent check.

```pseudo id=main
GODUNOV(u, Δx, Δt, T, f)
L1  for n ← 0 to ⌈T/Δt⌉ − 1 do                  ▷ the last step is shortened to end at T
L2      add ghost cells u_0, u_(m+1) from the boundary conditions
L3      for i ← 0 to m do u*_(i+1/2) ← RIEMANN-FACE-STATE(u_i, u_(i+1))
L4          F_(i+1/2) ← f(u*_(i+1/2))
L5      for i ← 1 to m do u_i ← u_i − (Δt/Δx)(F_(i+1/2) − F_(i−1/2))
L6  return u
```

The time step must satisfy the CFL condition $\frac{\Delta t}{\Delta x}\max|f'(u)| \le 1$. For linear advection $f(u) = au$ the face state is the upwind value and Godunov's method is the [upwind scheme](/upwind-scheme/). For systems such as the Euler equations, the Riemann problem has several waves and is solved exactly by iteration or approximately (Roe, HLL, HLLC).

## Example

**A transonic rarefaction, exactly.** For [Burgers' equation](/burgers-equation/) $f(u) = u^2/2$ with $u_s = 0$, take cells $(-1, -1, 1, 1)$, $\Delta x = 1$, $\Delta t = \tfrac12$ (Courant number $\tfrac12$) and transmissive boundaries. At the middle face $u_L = -1 < 0 < 1 = u_R$, so the fan is centred on the face and $u^* = 0$, with flux $0$. The outer faces have flux $f(\pm1) = \tfrac12$.

| step | $u_1$ | $u_2$ | $u_3$ | $u_4$ |
|---|---|---|---|---|
| 0 | $-1$ | $-1$ | $1$ | $1$ |
| 1 | $-1$ | $-3/4$ | $3/4$ | $1$ |
| 2 | $-57/64$ | $-39/64$ | $39/64$ | $57/64$ |

The fan opens, as it should. The Roe flux $\tfrac12(f(u_L) + f(u_R)) - \tfrac12|\hat a|(u_R - u_L)$ with $\hat a = (u_L + u_R)/2 = 0$ gives $\tfrac12$ at the middle face too, so with it nothing moves: it keeps a stationary expansion shock, a weak solution that violates the entropy condition. On 200 cells over $[-1, 1]$ at $t = 0.5$, the Roe scheme's $L^1$ error stays exactly $0.5$, while Godunov's is $0.022$.

**A shock.** Data $(1, 1, 0, 0)$, same grid: the shock has speed $\sigma = \tfrac12 > 0$, so the face takes $u_L$. After two steps the averages are $(1, 1, \tfrac{31}{64}, \tfrac{1}{64})$, and the total grew by exactly the inflow $\Delta t \cdot f(1)$ per step.

**Convergence** on $[-1, 1]$ at $t = 0.5$, Courant number $0.8$, $L^1$ error against exact cell averages:

| $m$ | rarefaction $(-1, 1)$ | ratio | shock $(1, 0)$ |
|---|---|---|---|
| 50 | 5.848e-2 | | 7.86e-3 |
| 100 | 3.658e-2 | 1.60 | 1.67e-3 |
| 200 | 2.221e-2 | 1.65 | 3.89e-3 |
| 400 | 1.314e-2 | 1.69 | 1.76e-3 |
| 800 | 7.614e-3 | 1.73 | 8.81e-4 |

At the shock the error stays below $0.4\Delta x$, $O(\Delta x)$ with fluctuations that depend on where the shock sits relative to the cell faces at the final time: the scheme resolves it over one or two cells. Near the corners of the rarefaction the rate is below 1 (ratios 1.6 to 1.73), as is usual for first-order schemes with discontinuous initial data.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that the face state formula gives $f(u^*) = $ Osher's min/max expression, that the Godunov flux is nondecreasing in $u_L$ and nonincreasing in $u_R$, and that under the CFL condition the scheme is monotone: each new value is a nondecreasing function of the three old values it depends on. Monotonicity gives the discrete maximum principle; together with Harten's incremental form it also gives the TVD property, and conservation holds exactly. Convergence to the entropy solution is cited: conservative monotone schemes with a consistent flux converge to the entropy solution as $\Delta x \to 0$ with fixed Courant number (Crandall and Majda 1980), with $L^1$ error $O(\Delta x^{1/2})$ for data of bounded variation (Kuznetsov).

## Complexity

One step does $m + 1$ Riemann solves, each $O(1)$ for a scalar convex flux, and $O(m)$ further arithmetic, so $N$ steps cost $\Theta(Nm)$ time and $N(m + 1)$ Riemann solves, with $\Theta(m)$ memory. With the CFL condition, $N = \Theta(m)$ for a fixed final time. For systems, an exact Riemann solve needs an iterative root finder per face (Toro 2009, Chapter 4), which is why approximate solvers are common.

## Properties

- **Conservative**, so shocks move at the Rankine-Hugoniot speed.
- **Monotone** under $\frac{\Delta t}{\Delta x}\max|f'| \le 1$, hence maximum principle and TVD.
- **Entropy satisfying**: transonic rarefactions are resolved without an entropy fix.
- **First order.** By Godunov's theorem, a linear scheme that maps monotone data to monotone data is at most first order accurate, so higher order needs nonlinear (limited) reconstructions.
- **Least viscous E-scheme.** Every E-flux satisfies $F \le F_{\text{God}}$ when $u_L \le u_R$ and $F \ge F_{\text{God}}$ when $u_L > u_R$, so Godunov's flux adds the least numerical viscosity in that class (Osher's characterization).
- **REA interpretation**: reconstruct (piecewise constant), evolve (exactly), average.

## Variants and improvements

- **MUSCL (van Leer 1979).** Reconstruct a linear function in each cell with a limited slope, evaluate the Riemann problem at the face values, and use a two-stage time step: second order away from extrema, TVD. See [flux limiter methods](/flux-limiter-methods/).
- **Approximate Riemann solvers.** Roe's linearization (with an entropy fix at sonic points), HLL and HLLC (Harten, Lax and van Leer 1983; Toro 2009), Osher's solver.
- **Engquist-Osher flux.** $F = f(\max(u_L, u_s)) + f(\min(u_R, u_s)) - f(u_s)$: monotone and smoother than Godunov's.
- **Higher order Godunov-type schemes.** WENO reconstruction with Runge-Kutta time stepping, discontinuous Galerkin with Riemann fluxes, ADER.
- **Multidimensional problems.** Dimension-by-dimension fluxes on Cartesian grids, or face-by-face fluxes on unstructured meshes, possibly with corner-transport upwinding.

## When to use it

Use Godunov's method, or more often a Godunov-type scheme with an approximate Riemann solver, for hyperbolic conservation laws with shocks: compressible gas dynamics, shallow water, magnetohydrodynamics, traffic flow. The first-order version is the building block and the robust fallback near strong shocks; production codes add reconstruction to reach second order. For smooth linear problems, [Lax-Wendroff](/lax-wendroff-method/) or spectral methods are more accurate per cell.

## Pitfalls

- **Missing the sonic case.** Using $u^* = u_L$ when $f'(u_L) \ge 0$, else $u_R$, without the transonic branch gives the Roe-like expansion shock of the example.
- **Wrong shock direction test.** The side is chosen by the sign of the shock speed $\sigma$, not by the sign of $f'(u_L)$ or $f'(u_R)$ alone.
- **Nonconvex fluxes.** The formula above assumes convex $f$; for nonconvex fluxes (Buckley-Leverett) the Riemann solution contains compound waves, and Osher's min/max formula still gives the Godunov flux.
- **CFL above 1.** Waves from neighbouring faces then reach other faces within one step, the face states are no longer constant in time and the scheme becomes unstable.
- **Expecting high accuracy.** First-order smearing of contact discontinuities grows like $\sqrt{t\,\Delta x}$; use high-resolution extensions.
- **Exact solvers for systems everywhere.** They are expensive and can fail near vacuum; robust approximate solvers (HLL) are often better.

## Implementations

## History

Godunov (1959) introduced the method for gas dynamics in Matematicheskii Sbornik 47(89), 271-306, using exact solutions of local Riemann problems between cell averages, and in the same paper proved that monotonicity-preserving linear schemes are at most first order accurate. Van Leer (1979) made the method second order with MUSCL, and Harten, Lax and van Leer (1983) set out the theory of Godunov-type schemes and approximate Riemann solvers. Crandall and Majda (1980) proved convergence of monotone schemes to the entropy solution.

## References
