---
tag: FZZC89
kind: algorithm
slug: artificial-compressibility-method
name: Artificial compressibility method
aliases:
- pseudo-compressibility method
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Replaces incompressibility by a pressure equation with an artificial sound speed and marches in pseudo-time to a divergence-free steady state."
solves: [navier-stokes-equations]
model: real-ram
complexity:
  vars: {M: "the number of grid cells", I: "the number of pseudo-time iterations"}
  time: {worst: "Θ(I M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, explicit: true, steady_state: true, needs_poisson_solve: false, divergence_free_at_convergence: true}
history:
  year: 1967
  people: [Alexandre J. Chorin]
  note: Chorin (1967) added an artificial time derivative of the pressure to the continuity equation, which makes the steady incompressible equations a hyperbolic-parabolic system that can be marched explicitly to the steady state.
prereqs: [navier-stokes-equations, finite-difference-method, courant-friedrichs-lewy-condition, mac-grid]
see_also: [chorin-projection-method, simple-algorithm, marker-and-cell-method, von-neumann-stability-analysis, lattice-boltzmann-method, smoothed-particle-hydrodynamics, fixed-point-iteration, helmholtz-hodge-decomposition]
sources:
  - paper: doi:10.1016/0021-9991(67)90037-X
    title: Alexandre J. Chorin, A numerical method for solving incompressible viscous flow problems, Journal of Computational Physics 2(1) (1967) 12-26
    locator: the artificial compressibility equations and the explicit iteration to the steady state
  - book: isbn:9783319996912
    title: Joel H. Ferziger, Milovan Peric and Robert L. Street, Computational Methods for Fluid Dynamics, fourth edition, Springer, 2020
    locator: Chapter 7 (other methods for the pressure-velocity coupling, artificial compressibility)
  - paper: doi:10.1090/S0025-5718-1968-0242392-2
    title: Alexandre J. Chorin, Numerical solution of the Navier-Stokes equations, Mathematics of Computation 22(104) (1968) 745-762
    locator: the projection method that Chorin proposed next for time-accurate flow
---

The artificial compressibility method finds steady incompressible flow without solving a pressure Poisson equation. It adds a fake time derivative of the pressure to the continuity equation, $p_\tau + c^2\nabla\cdot\mathbf{u} = 0$, with an artificial sound speed $c$. The resulting system behaves like a slightly compressible fluid: pressure waves carry the information that the constraint $\nabla\cdot\mathbf{u} = 0$ is violated, and viscosity damps them. The method marches this system in pseudo time $\tau$ with simple explicit steps until nothing changes. At that steady state the time derivatives are zero, so the velocity is divergence free and the momentum equation holds, for any choice of $c$. Each step is cheap and local, which made the method attractive for early computers and later for compressible-flow codes reused for incompressible flow. Intermediate pseudo-time states have no physical meaning.

## In plain words

Real water cannot be squeezed, and that rule is hard to enforce directly, because every part of the flow must agree at once. This method relaxes the rule. It pretends the water can be squeezed a little, so that pushing water into a region raises its pressure, and the higher pressure then pushes the water out again. These pressure pulses move like sound and fade because of friction. The method lets the flow settle step by step, each step looking only at neighbors. When the flow stops changing, every region has exactly as much water leaving as entering, so the pretend squeezing is gone and the answer is the true steady flow. How fast it settles depends on the chosen fake sound speed.

## The problem

Find a steady solution of the incompressible [Navier-Stokes equations](/navier-stokes-equations/)

$$(\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu\Delta\mathbf{u} + \mathbf{f}, \qquad \nabla\cdot\mathbf{u} = 0,$$

with $p$ the pressure divided by the density and $\nu$ the kinematic viscosity. Artificial compressibility replaces it by the pseudo-time system

$$\mathbf{u}_\tau + (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu\Delta\mathbf{u} + \mathbf{f}, \qquad p_\tau + c^2\nabla\cdot\mathbf{u} = 0,$$

and looks for its steady state. This page discretizes it on the periodic [MAC grid](/mac-grid/) with $M$ cells: central differences for advection, the 5-point Laplacian for viscosity, $D$ the divergence at the cell centers and $G$ the gradient at the faces. The cost is counted in real arithmetic operations and in pseudo-time iterations $I$.

## The algorithm

```pseudo id=main
ARTIFICIAL-COMPRESSIBILITY(u, v, p, Δτ, c, ν, f, tol)
L1  repeat
L2      R ← -(u·∇)u + ν Δ_h u - G p + f              ▷ momentum residual at the faces
L3      (u, v) ← (u, v) + Δτ R
L4      p ← p - Δτ c² D(u, v)                         ▷ uses the new velocity
L5  until max|R| ≤ tol and max|D(u, v)| ≤ tol
L6  return (u, v, p)
```

Line L4 uses the velocity just computed in line L3. This makes the pressure-velocity part of the iteration a symplectic Euler step for the pseudo-acoustic waves, which allows a larger step than a fully explicit update. The step $\Delta\tau$ is chosen from the sharp condition proved on this page for the linear Stokes problem, $\Delta\tau^2c^2\mu_{\max} + 2\Delta\tau\nu\mu_{\max} < 4$ with $\mu_{\max} = 4/\Delta x^2 + 4/\Delta y^2$, times a safety factor $0.8$, and from the rule of thumb $\Delta\tau \le 2\nu/|\mathbf{u}|_{\max}^2$ for central advection. The safety factor and $c$ are choices.

For time-accurate flow, dual time stepping puts the whole pseudo-time iteration inside each physical time step: the physical time derivative becomes a source term, and the iteration converges to an implicit time step.

## Example

**One step by hand.** Take a periodic row of 4 cells with $\Delta x = 1$, $\nu = 0$, zero start, force $(1, 0, 0, 0)$ on the $u$ faces, $\Delta\tau = \tfrac12$ and $c = 1$. Line L3 gives $u = (\tfrac12, 0, 0, 0)$. The divergence is $Du = (-\tfrac12, 0, 0, \tfrac12)$: face 0 is the left face of cell 0 and the right face of cell 3, and $u > 0$ there carries fluid from cell 3 into cell 0. Line L4 gives $p = -\tfrac12 \cdot Du = (\tfrac14, 0, 0, -\tfrac14)$: pressure rises where fluid gathers (cell 0) and falls where it leaves (cell 3). In the next step this pressure difference pushes back on face 0. The test file checks these numbers in exact rational arithmetic.

**Forced steady Taylor-Green vortex.** On $[0, 2\pi]^2$ the field $u = -\cos x \sin y$, $v = \sin x \cos y$, $p = -\tfrac14(\cos 2x + \cos 2y)$ is a steady solution with the force $\mathbf{f} = 2\nu\mathbf{u}$, which balances viscous decay. With $\nu = 0.5$, $c = 1$, a zero start and a stopping tolerance of $10^{-10}$:

| cells | $\Delta\tau$ | iterations | velocity error | order | pressure error |
|---|---|---|---|---|---|
| $8 \times 8$ | 0.198 | 137 | 4.899e-2 | | 1.993e-2 |
| $12 \times 12$ | 0.0977 | 296 | 2.237e-2 | 1.93 | 1.168e-2 |
| $16 \times 16$ | 0.0576 | 514 | 1.270e-2 | 1.97 | 7.189e-3 |

The velocity converges at second order; the pressure error ratios are still below that on these coarse grids. On the $8 \times 8$ grid the number of iterations to reach $10^{-11}$ depends on $c$: 1151 for $c = 0.25$, 313 for $c = 0.5$, 151 for $c = 1$, 160 for $c = 1.5$, 183 for $c = 2$ and 290 for $c = 4$, and the converged fields agree to $10^{-9}$. These are measurements from the implementation on this page. The best $c$ here is of the order of the flow speed, in line with the usual rule of thumb.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). A fixed point of the iteration has zero momentum residual and zero discrete divergence, and conversely, so the limit, when the iteration converges, solves the discrete steady incompressible equations for every $c > 0$ and every $\Delta\tau$; the stopping test checks both residuals directly. For the linear Stokes problem on the periodic MAC grid, the proof splits the error into a divergence-free part, which decays by viscosity alone, and gradient modes, each coupled to one pressure mode by a 2 by 2 matrix with determinant $1 - \Delta\tau\nu\mu$ and trace $2 - \Delta\tau\nu\mu - \Delta\tau^2c^2\mu$. The Jury conditions give convergence exactly when $\Delta\tau^2c^2\mu + 2\Delta\tau\nu\mu < 4$ for every eigenvalue $\mu$ of $-DG$. The tests confirm that the bound is sharp on the checkerboard mode. Convergence for the nonlinear problem is not guaranteed; it is observed here.

## Complexity

One iteration costs $\Theta(M)$ operations and $\Theta(M)$ memory, with no linear solve. The number of iterations is the cost driver. With $\Delta\tau \sim \Delta x^2/\nu$ from the viscous part of the step limit, the slowest smooth modes decay at a rate of order $\nu$ per unit pseudo time, so $I = O(\Delta x^{-2}\log(1/\text{tol}))$ and the total cost on a square grid is $O(M^2\log(1/\text{tol}))$. The measured counts above grow by about 2.2 and 1.7 from grid to grid, close to the $\Delta x^{-2}$ growth. Implicit pseudo-time stepping, local time steps, preconditioning and multigrid reduce the count in practice.

## Properties

- The steady state does not depend on $c$ or $\Delta\tau$; only the path to it does.
- No Poisson equation and no global solve: every step is local, so the method is easy to parallelize.
- The pseudo-time system is hyperbolic-parabolic, so methods for compressible flow (upwind fluxes, Riemann solvers, implicit schemes) can be reused.
- Intermediate iterates are not divergence free and have no physical meaning.
- The steady discrete equations are the same as those of the MAC method, so the result has the same second order spatial accuracy.

## Variants and improvements

- **Dual time stepping** for unsteady flow: a pseudo-time iteration inside each physical step.
- **Implicit and preconditioned pseudo time:** implicit schemes and low-Mach preconditioning, which make the pseudo-acoustic and convective speeds comparable, cut the iteration count.
- **Upwind and characteristic schemes** for the pseudo-compressible system, used in collocated finite volume codes.
- **[Projection methods](/chorin-projection-method/)** solve a Poisson equation instead and enforce $\nabla\cdot\mathbf{u} = 0$ at every step; Chorin proposed them a year later for time-accurate flow.
- **Weakly compressible methods** such as [lattice Boltzmann](/lattice-boltzmann-method/) and weakly compressible [SPH](/smoothed-particle-hydrodynamics/) also replace incompressibility by a stiff equation of state, but with a physical time and a small Mach number instead of a pseudo-time iteration.

## When to use it

Use artificial compressibility for steady incompressible flow when a compressible-flow code or an explicit, local, easily parallel scheme is available and a Poisson solver is not. With dual time stepping it also serves unsteady flow. If a fast Poisson solver is at hand and time accuracy matters, the [projection method](/chorin-projection-method/) is usually cheaper. For steady flow with implicit momentum equations, [SIMPLE](/simple-algorithm/) is the common alternative.

## Pitfalls

- **The artificial sound speed is a choice.** Too small a $c$ makes the pressure respond slowly and the iteration crawl; too large a $c$ makes the system stiff and forces a small $\Delta\tau$. A rule of thumb takes $c$ of the order of the flow speed; it is not a guarantee.
- **Separate step limits are not enough.** The viscous and acoustic limits interact: the condition is $\Delta\tau^2c^2\mu + 2\Delta\tau\nu\mu < 4$, not two independent conditions. On the $8 \times 8$ grid above, a step at 0.8 of each separate limit diverges for $c = 1.5$.
- **Stopping on the change between iterates** instead of the residuals can stop early when the iteration is slow. Check $\max|D\mathbf{u}|$ and the momentum residual.
- **Unsteady flow without dual time stepping.** Plain pseudo time is not physical time; transients computed with it are wrong.
- **Periodic and closed domains** fix the pressure only up to a constant and the mean velocity only by the start; give the start the right mean flow.

## Implementations

## History

Chorin (1967) introduced the method in the first volume of the Journal of Computational Physics, as a way to compute steady viscous incompressible flow by explicit marching. A year later Chorin (1968) proposed the projection method for time-accurate flow. Artificial compressibility returned in the 1980s in upwind and implicit form in collocated finite volume codes, often with dual time stepping for unsteady problems.

## References
