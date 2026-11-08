---
tag: 80XDHS
kind: algorithm
slug: finite-volume-method
name: Finite volume method
aliases:
- FVM
- conservative finite volume scheme
- flux-differencing scheme
area: numerical/differential-equations
level: advanced
summary: "Store cell averages and update each by the difference of numerical fluxes through its faces: u_i -= (Δt/Δx)(F_(i+1/2) - F_(i-1/2)). Conservative by construction; the flux choice sets accuracy."
solves: [advection-equation, burgers-equation]
model: real-ram
complexity:
  vars: {m: "the number of cells", N: "the number of time steps, ⌈T/Δt⌉"}
  time: {worst: "Θ(N m)"}
  space: {extra: "Θ(m)"}
  evaluations: {worst: "N (m + 1)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "1", tvd_under_cfl: true}
history:
  year: 1959
  people: [S. K. Godunov, Peter Lax, Burton Wendroff]
  note: Lax and Wendroff (1960) showed that convergent conservative schemes converge to weak solutions; Godunov (1959) built the flux from Riemann problems, and finite volume formulations on general meshes spread through computational fluid dynamics in the 1970s.
prereqs: [advection-equation, courant-friedrichs-lewy-condition, upwind-scheme]
see_also: [godunov-method, riemann-problem, lax-friedrichs-scheme, flux-limiter-methods, total-variation-diminishing, burgers-equation, finite-element-method, finite-difference-method]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 4 (finite volume methods, numerical flux, conservation, CFL condition), Chapter 6 (high-resolution methods, TVD and Harten's theorem), Chapter 12 (nonlinear scalar conservation laws, Lax-Wendroff theorem, entropy, monotone methods)
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 5 (conservative methods for scalar conservation laws, Rusanov and Lax-Friedrichs fluxes), Chapter 13 (TVD methods)
  - paper: doi:10.1002/cpa.3160130205
    title: Peter Lax and Burton Wendroff, Systems of conservation laws, Communications on Pure and Applied Mathematics 13(2) (1960) 217-237
    locator: conservation form; a convergent conservative consistent scheme converges to a weak solution
  - paper: doi:10.1016/0021-9991(83)90136-5
    title: Ami Harten, High resolution schemes for hyperbolic conservation laws, Journal of Computational Physics 49(3) (1983) 357-393
    locator: the incremental form and the sufficient condition for total variation diminishing schemes
  - paper: doi:10.1016/S1570-8659(00)07005-8
    title: Robert Eymard, Thierry Gallouët and Raphaèle Herbin, Finite volume methods, in Handbook of Numerical Analysis VII, North-Holland, 2000, 713-1018
    locator: finite volume schemes on general meshes for elliptic, parabolic and hyperbolic problems
---

The finite volume method discretizes a conservation law $u_t + \nabla \cdot f(u) = 0$ by dividing the domain into cells and tracking the average of $u$ over each cell. Integrating the law over a cell shows that the average changes only through the fluxes across the cell faces, so the method updates each average by the net numerical flux through its faces. A flux leaving one cell enters its neighbour, so the total of $u$ is conserved exactly, and with a suitable numerical flux, shocks move at the right speed. In one dimension with cell width $\Delta x$ and time step $\Delta t$ the scheme is $u_i^{n+1} = u_i^n - \frac{\Delta t}{\Delta x}\big(F(u_i^n, u_{i+1}^n) - F(u_{i-1}^n, u_i^n)\big)$, where the two-point numerical flux $F$ approximates $f(u)$ at the face. [Upwind](/upwind-scheme/), [Lax-Friedrichs](/lax-friedrichs-scheme/) and [Godunov](/godunov-method/) schemes are finite volume methods with different fluxes.

## In plain words

Think of a long pipe cut into equal compartments, each holding some amount of a substance. Over a short time the amount in a compartment changes only by what flows in through its left wall minus what flows out through its right wall. The method estimates the flow through each wall from the contents of the two compartments on either side, then updates every compartment by its inflow minus its outflow. What one compartment loses, the next gains, so nothing is created or destroyed, even when the substance piles up into a sharp front. The quality of the result depends on how well the wall flows are estimated, and on keeping the time step short enough that nothing passes more than one compartment in one step.

## The problem

Given a flux $f : \mathbb{R} \to \mathbb{R}$, initial data $u_0$ on $[a, b]$, boundary conditions, and a final time $T$, approximate the entropy solution $u(x, t)$ of the scalar conservation law $u_t + f(u)_x = 0$. Divide $[a, b]$ into $m$ cells $C_i = [x_{i-1/2}, x_{i+1/2}]$ of width $\Delta x$ and approximate the cell averages $\bar u_i(t) = \frac{1}{\Delta x}\int_{C_i}u(x, t)\,dx$, which satisfy exactly

$$\frac{d}{dt}\bar u_i(t) = -\frac{1}{\Delta x}\Big(f\big(u(x_{i+1/2}, t)\big) - f\big(u(x_{i-1/2}, t)\big)\Big).$$

The scheme replaces the unknown face values by a numerical flux $F(u_L, u_R)$ that is consistent, $F(v, v) = f(v)$, and Lipschitz. Errors are measured in the discrete $L^1$ norm $\Delta x\sum_i|u_i - \bar u_i|$, the natural norm for conservation laws. The cost is counted in numerical flux evaluations, $m + 1$ per step.

## The algorithm

```pseudo id=main
FINITE-VOLUME(u, Δx, Δt, T, F, bc)
L1  for n ← 0 to ⌈T/Δt⌉ − 1 do                 ▷ the last step is shortened to end at T
L2      add ghost cells u_0, u_(m+1) from bc   ▷ periodic: copies of u_m, u_1; transmissive: of u_1, u_m
L3      for i ← 0 to m do F_(i+1/2) ← F(u_i, u_(i+1))
L4      for i ← 1 to m do u_i ← u_i − (Δt/Δx)(F_(i+1/2) − F_(i−1/2))
L5  return u
```

Two classical fluxes:

- **Upwind** for linear advection $f(u) = au$: $F(u_L, u_R) = au_L$ if $a \ge 0$, else $au_R$. This is the exact flux of the Riemann problem.
- **Rusanov** (local Lax-Friedrichs) for general $f$: $F(u_L, u_R) = \tfrac12\big(f(u_L) + f(u_R)\big) - \tfrac12 s(u_R - u_L)$, with $s = \max(|f'(u_L)|, |f'(u_R)|)$, the average flux plus just enough numerical diffusion.

Stability requires the CFL condition $\nu = \frac{\Delta t}{\Delta x}\max|f'(u)| \le 1$: information may not cross more than one cell per step. In several dimensions, the cells are arbitrary polygons or polyhedra and the update sums $|e|\,F(u_K, u_L; n_e)$ over the faces $e$ of cell $K$, divided by its volume, with $n_e$ the unit normal.

## Example

**Advection, exact arithmetic.** Five periodic cells, $\Delta x = 1$, $a = 1$, $\Delta t = \tfrac12$ (Courant number $\nu = \tfrac12$), initial averages $(0, 0, 1, 0, 0)$. The upwind flux through the right face of cell $i$ is $u_i$, so $u_i \leftarrow u_i - \tfrac12(u_i - u_{i-1})$:

| step | $u_1$ | $u_2$ | $u_3$ | $u_4$ | $u_5$ | total |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1/2 | 1/2 | 0 | 1 |
| 2 | 0 | 0 | 1/4 | 1/2 | 1/4 | 1 |

The exact solution has moved the block one cell to the right; the scheme has the right centre of mass ($u$-weighted mean position $4$, one cell right of $3$) but smears the block, which is the numerical diffusion of a first-order method. At $\nu = 1$ the update is $u_i \leftarrow u_{i-1}$, an exact shift.

**A Burgers shock.** For $f(u) = u^2/2$ with the Rusanov flux, transmissive boundaries, $\Delta x = 1$, $\Delta t = \tfrac12$ and data $(1, 1, 0, 0)$, one step gives $(1, \tfrac78, \tfrac38, 0)$. The fluxes at the four inner faces are $\tfrac12, \tfrac12, \tfrac34, 0$ (the flux between $1$ and $0$ is $\tfrac14 + \tfrac12 = \tfrac34$), and the total increases by exactly $\Delta t(F_{\text{in}} - F_{\text{out}}) = \tfrac12(\tfrac12 - 0) = \tfrac14$, the amount that entered through the left end.

**Convergence.** Advecting $\sin 2\pi x$ once around the periodic unit interval with the upwind flux at $\nu = 0.5$:

| $m$ | $L^1$ error of cell averages | ratio |
|---|---|---|
| 50 | 1.141e-1 | |
| 100 | 5.984e-2 | 1.91 |
| 200 | 3.065e-2 | 1.95 |
| 400 | 1.552e-2 | 1.98 |

First order, as expected for smooth data. For discontinuous data, first-order schemes converge in $L^1$ at rate $O(\Delta x)$ across self-sharpening shocks, but only at rate $O(\Delta x^{1/2})$ across a discontinuity that is merely advected, which is also the worst case for monotone schemes.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It proves three things. Conservation: with periodic boundaries $\sum_iu_i$ is constant, and with other boundaries it changes exactly by $\Delta t$ times the inflow minus the outflow at the two ends; the tests check this exactly with fractions. Total variation: if the flux can be written in Harten's incremental form with nonnegative coefficients summing to at most 1 at each face, the total variation does not increase; this holds under the CFL condition for the upwind flux and for the Rusanov flux with convex or concave $f$, which rules out growing oscillations. Maximum principle: under the CFL condition for the upwind flux, and under $\nu \le \tfrac12$ for the Rusanov flux, new values lie between the old neighbouring values (the tests observe it for Rusanov up to $\nu = 1$). The convergence statements are cited: by the Lax-Wendroff theorem (Lax and Wendroff 1960), if a conservative consistent scheme converges boundedly in $L^1_{\text{loc}}$ as $\Delta x, \Delta t \to 0$, the limit is a weak solution; monotone schemes converge to the entropy solution, with $L^1$ error $O(\Delta x^{1/2})$ for BV data (Kuznetsov's estimate; LeVeque 2002, Chapter 12).

## Complexity

Each step evaluates $m + 1$ numerical fluxes and does $O(m)$ arithmetic, so a run of $N = \lceil T/\Delta t\rceil$ steps costs $\Theta(Nm)$ time and $N(m + 1)$ flux evaluations, with $\Theta(m)$ memory for the averages and fluxes. The CFL condition forces $\Delta t \le \Delta x/\max|f'|$, so reaching a fixed time $T$ takes $N = \Theta(m)$ steps and $\Theta(m^2)$ work in 1D; in $d$ dimensions with $m$ cells per direction, $\Theta(m^{d+1})$.

## Properties

- **Conservative.** Exactly, in exact arithmetic, for any flux and any cell geometry; this is what makes shock speeds correct.
- **Explicit**, one flux evaluation per face per step.
- **First order** with two-point fluxes; second order needs reconstruction and [flux limiters](/flux-limiter-methods/) to stay non-oscillatory.
- **Total variation diminishing** under the CFL condition for the upwind and Rusanov fluxes (Rusanov with convex or concave $f$).
- **Works on unstructured meshes** of arbitrary polygons or polyhedra, unlike classical finite differences.

## Variants and improvements

- **Godunov's method.** The flux of the exact Riemann solution at each face; the least diffusive monotone first-order flux.
- **Approximate Riemann solvers.** Roe, HLL and HLLC fluxes for systems such as the Euler equations (Toro 2009).
- **MUSCL and high-resolution schemes.** Reconstruct linear functions in each cell with limited slopes, then apply the flux to the reconstructed face values; second order away from extrema while staying TVD (see [total variation diminishing](/total-variation-diminishing/)).
- **WENO and ENO reconstructions** for higher order (see [WENO](/weno-scheme/)).
- **Method of lines.** Treat the flux differences as an ODE right-hand side and integrate with a strong-stability-preserving Runge-Kutta method.
- **Finite volumes for elliptic problems.** The two-point flux approximation on admissible (orthogonal) meshes gives cell-centred schemes for diffusion; on general meshes multipoint flux approximations are needed (Eymard, Gallouët and Herbin 2000).

## When to use it

Use finite volumes for conservation laws whose solutions develop shocks or contact discontinuities: gas dynamics, shallow water, traffic flow, multiphase transport in porous media, and many other problems in computational fluid dynamics. Conservation at the discrete level is the decisive property there. For smooth elliptic problems, [finite elements](/finite-element-method/) give higher order more easily, and for smooth problems on simple domains [finite differences](/finite-difference-method/) are simpler.

## Pitfalls

- **Nonconservative updates.** Writing Burgers' equation as $u_t + uu_x = 0$ and differencing that form produces shocks with the wrong speed even as $\Delta x \to 0$.
- **Violating the CFL condition.** Above $\nu = 1$ the upwind scheme amplifies high frequencies; in the tests a random state grows past $10^3$ within 400 steps at $\nu = 1.05$, while at $\nu = 0.99$ it stays bounded by its initial maximum.
- **Entropy-violating fluxes.** Fluxes that do not add diffusion at sonic points (plain Roe linearization) can keep stationary expansion shocks; add an entropy fix.
- **Too much numerical diffusion.** First-order fluxes smear contacts over many cells; use high-resolution reconstruction.
- **Boundary conditions through ghost cells.** Ghost cell values must encode the physics (inflow, outflow, wall); transmissive copies are only a crude outflow condition.
- **Evaluating initial data at cell centres.** For second-order accuracy initialize with true cell averages, not point values.

## Implementations

## History

Conservation form became central with Lax (1954) and Lax and Wendroff (1960), who proved that limits of convergent conservative schemes are weak solutions, so they capture shocks correctly. Godunov (1959) built the flux from exact solutions of local Riemann problems. The cell-centred finite volume viewpoint on irregular meshes was developed for aerodynamics in the 1970s by McDonald, MacCormack and Paullay, and Jameson among others, and high-resolution TVD methods followed with van Leer (1979) and Harten (1983).

## References
