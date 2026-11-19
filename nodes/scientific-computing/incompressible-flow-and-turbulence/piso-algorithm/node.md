---
tag: 8SFP8G
kind: algorithm
slug: piso-algorithm
name: PISO algorithm
aliases:
- pressure-implicit with splitting of operators
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: "A non-iterative pressure-velocity coupling for transient flow with one predictor and two corrector steps in each time step."
solves: [navier-stokes-equations]
model: real-ram
complexity:
  vars: {M: "the number of grid cells", N: "the number of time steps", K: "the number of conjugate gradient iterations per pressure solve"}
  time: {worst: "Θ(N M K)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, implicit: true, time_accurate: true, needs_poisson_solve: true, divergence_free_after_each_corrector: true, outer_iterations: false}
history:
  year: 1986
  people: [Raad I. Issa]
  note: Issa (1986) split the implicitly discretized flow equations into a momentum predictor and a fixed sequence of pressure correctors in each time step, without outer iterations, and analyzed the splitting error.
prereqs: [navier-stokes-equations, mac-grid, backward-euler-method, simple-algorithm, poisson-equation]
see_also: [simple-algorithm, chorin-projection-method, rhie-chow-interpolation, operator-splitting, artificial-compressibility-method, conjugate-gradient-method, courant-friedrichs-lewy-condition, fixed-point-iteration]
sources:
  - paper: doi:10.1016/0021-9991(86)90099-9
    title: R. I. Issa, Solution of the implicitly discretised fluid flow equations by operator-splitting, Journal of Computational Physics 62(1) (1986) 40-65
    locator: the predictor and corrector steps and the analysis of the splitting error
  - book: isbn:9783319996912
    title: Joel H. Ferziger, Milovan Peric and Robert L. Street, Computational Methods for Fluid Dynamics, fourth edition, Springer, 2020
    locator: Chapter 7 (pressure correction methods, PISO)
  - book: isbn:9780070487406
    title: Suhas V. Patankar, Numerical Heat Transfer and Fluid Flow, Hemisphere and McGraw-Hill, 1980
    locator: Sections 6.5 to 6.7 (the pressure and velocity corrections of SIMPLE that PISO repeats)
---

PISO, Pressure-Implicit with Splitting of Operators, computes one implicit time step of incompressible flow without outer iterations. The implicit step couples the velocity and the pressure in one large system. [SIMPLE](/simple-algorithm/) would iterate on that system with under-relaxation until it converges. PISO instead does one momentum predictor with the old pressure and then a fixed number of pressure corrections, usually two. Each corrector solves a Poisson equation for the pressure and leaves a divergence-free velocity. The second corrector repairs the neighbor terms that the first one ignored. When the time step is small, the remaining difference from the fully coupled step shrinks with a high power of the time step and is smaller than the error of the time discretization itself, so the extra iterations of SIMPLE buy nothing.

## In plain words

Each time step must find a new flow and a new pressure that fit together. The careful way is to adjust both again and again until they agree. PISO notices that over a short time step the flow changes only a little, so a few well-chosen adjustments are enough. First it moves the fluid using the old pressure. Then it fixes the pressure so that no cell gains or loses fluid, assuming each face reacts only to its own two cells. Then it does the same fix once more, now counting the push from the neighboring faces too. After these two fixes the answer is so close to the careful one that more work would not improve the result.

## The problem

Advance the incompressible [Navier-Stokes equations](/navier-stokes-equations/)

$$\mathbf{u}_t + (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu\Delta\mathbf{u} + \mathbf{f}, \qquad \nabla\cdot\mathbf{u} = 0,$$

with $p$ the pressure divided by the density and $\nu$ the kinematic viscosity, by $N$ steps of the [backward Euler method](/backward-euler-method/). This page uses the periodic [MAC grid](/mac-grid/) with $M$ cells and central differences, with the advecting velocity frozen at the old time level. One step then asks for the solution of the coupled linear system

$$a_P\mathbf{u} - \sum_{nb} a_{nb}\mathbf{u}_{nb} = \frac{\mathbf{u}^n}{\Delta t} + \mathbf{f} - Gp, \qquad D\mathbf{u} = 0,$$

with $a_P = 1/\Delta t + 2\nu/\Delta x^2 + 2\nu/\Delta y^2$, $D$ the divergence and $G$ the gradient. The cost is counted in real arithmetic operations.

## The algorithm

```pseudo id=main
PISO-STEP(u^n, p^n, ν, Δt, f, m)
L1  compute a_P, a_nb from u^n;  b ← u^n/Δt + f
L2  u* ← solve a_P u* - Σ a_nb u*_nb = b - G p^n                ▷ momentum predictor
L3  for k ← 1 to m                                               ▷ m = 2 in standard PISO
L4      h ← (b + Σ a_nb u^(k-1)_nb) / a_P                        ▷ u^(0) = u*
L5      solve -D G p = -a_P D h for p                            ▷ pressure equation
L6      u^(k) ← h - G p / a_P                                    ▷ divergence free
L7  return (u^(m), p)
```

Line L2 solves the momentum equations with the old pressure; this page uses Gauss-Seidel sweeps to a tolerance of $10^{-13}$. Line L4 uses the neighbor values of the latest velocity, so the $k$-th corrector differs from the first only through the neighbor sum. The first corrector is the SIMPLE correction $\mathbf{u}^{(1)} = \mathbf{u}^* - G(p - p^n)/a_P$, written for the full pressure instead of the increment $p' = p - p^n$. Finite volume codes write line L4 with face fluxes, and on general grids $a_P$ varies, so line L5 has variable coefficients $1/a_P$. Here $a_P$ is constant and line L5 is the periodic 5-point Poisson equation, solved with [conjugate gradients](/conjugate-gradient-method/).

## Example

**The first corrector by hand.** In line L2, $a_P\mathbf{u}^* = \mathbf{b} + N\mathbf{u}^* - Gp^n$, where $N$ holds the $a_{nb}$. So line L4 for $k = 1$ gives $\mathbf{h} = \mathbf{u}^* + Gp^n/a_P$, and line L6 gives $\mathbf{u}^{(1)} = \mathbf{u}^* - G(p - p^n)/a_P$: the old pressure gradient is taken out and the new one put in, with the face weight $1/a_P$. Nothing in this step accounts for $N(\mathbf{u}^{(1)} - \mathbf{u}^*)$, the change in the neighbor terms. The second corrector puts that change into $\mathbf{h}$ and projects again.

**Taylor-Green vortex.** On $[0, 2\pi]^2$ the field $u = \sin x\cos y\,F$, $v = -\cos x\sin y\,F$, $p = \tfrac14(\cos 2x + \cos 2y)F^2$ with $F = e^{-2\nu t}$ solves the equations with $\mathbf{f} = 0$. With $\nu = 0.1$ on $8 \times 8$ cells, start from a pressure consistent with the scheme (one coupled step first), and compare one PISO step with $m$ correctors against the coupled step:

| $\Delta t$ | $m = 1$ | $m = 2$ | $m = 3$ |
|---|---|---|---|
| 0.1 | 8.336e-5 | 3.575e-6 | 1.546e-7 |
| 0.05 | 1.107e-5 | 2.447e-7 | 5.457e-9 |
| 0.025 | 1.425e-6 | 1.600e-8 | 1.814e-10 |

The observed orders are about 2.9, 3.9 and 4.9, in line with the bound $O(\Delta t^{m+2})$ proved for a consistent pressure. Over many steps to $T = 0.4$ with $m = 2$, the differences between runs with $\Delta t = 0.1, 0.05, 0.025, 0.0125$ are 3.196e-4, 1.553e-4 and 7.716e-5, which is first order in time (orders 1.04 and 1.01), the order of backward Euler. On $16 \times 16$ cells the orders are 1.18 and 1.06 with $m = 2$, and 0.99 and 0.99 with $m = 40$, which is the coupled step. These are measurements from the implementation on this page.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Because $G^T = -D$ on the MAC grid, each corrector is the orthogonal projection of $\mathbf{h}$ onto the divergence-free fields, so every corrector ends with $D\mathbf{u} = 0$ exactly, whatever the predictor. Repeating the corrector is a fixed-point iteration $\mathbf{w} \mapsto P((\mathbf{b} + N\mathbf{w})/a_P)$. The neighbor matrix has norm at most $S = 2\nu/\Delta x^2 + 2\nu/\Delta y^2 + U/\Delta x + V/\Delta y$, so when the Courant number $C = \Delta t(U/\Delta x + V/\Delta y)$ is below 1 the map is a contraction with factor $q = S/a_P \le \Delta t\,S$, the coupled step has a unique solution, and $m$ correctors miss it by at most $q^m\Delta t\|G(p - p^n)\|/(1 - C)$. On a fixed grid this is $O(\Delta t^{m+1})$, and $O(\Delta t^{m+2})$ when the old pressure is consistent. Two correctors thus stay below the $O(\Delta t^2)$ local error of backward Euler. The step always ends after a fixed amount of work.

## Complexity

The predictor costs $\Theta(M)$ per Gauss-Seidel sweep, and the number of sweeps for a fixed tolerance is bounded when $C$ is bounded away from 1, because the momentum matrix is then strictly diagonally dominant. Each corrector costs $\Theta(M)$ plus one Poisson solve of $K$ conjugate gradient iterations of $\Theta(M)$ each. With a fixed number $m$ of correctors one step costs $\Theta(M K)$ and $N$ steps cost $\Theta(N M K)$, with $\Theta(M)$ memory. $K$ grows like $\sqrt{M}$ on a square grid; [multigrid](/multigrid-method/) or a fast Poisson solver removes that factor. Compared with SIMPLE applied to each time step, PISO replaces an outer iteration of unknown length by a fixed number of solves.

## Properties

- Non-iterative: a fixed number of linear solves per time step, so the cost of a step is known in advance.
- Every corrector leaves a discretely divergence-free velocity.
- No under-relaxation is needed: the time step plays the role that under-relaxation plays in SIMPLE.
- Time accurate to the order of the underlying implicit scheme when $\Delta t$ is small enough that the splitting error is smaller than the time error.
- For large time steps the splitting error grows, and PISO no longer approximates the implicit step well.

## Variants and improvements

- **More correctors.** Each extra corrector multiplies the splitting error by at most $q$ (by about 0.08 in the test case, where $q = 0.53$); three or more are used for stiff cases.
- **PIMPLE**, the name used in OpenFOAM, wraps PISO correctors in a few SIMPLE-like outer iterations per time step, which allows larger time steps.
- **Non-orthogonal correctors.** On skewed grids, extra solves of the pressure equation inside each corrector treat the non-orthogonal part of the Laplacian explicitly.
- **Collocated grids** use [Rhie-Chow interpolation](/rhie-chow-interpolation/) for the face velocities in line L5.
- **Projection methods.** A [projection method](/chorin-projection-method/) with an incremental pressure is closely related: one predictor and one projection per step, with the splitting error analyzed in terms of the pressure update.

## When to use it

Use PISO for unsteady incompressible flow with an implicit momentum equation and time steps at Courant numbers around 1 or below, where time accuracy matters and SIMPLE iterations per step would be wasted. For steady flow, use [SIMPLE](/simple-algorithm/). For large time steps, use outer iterations (PIMPLE) or a fully coupled solver.

## Pitfalls

- **Large Courant numbers.** The contraction bound needs $C < 1$. Above that the splitting error is no longer small, the result drifts from the implicit step, and the method may become unstable, although on a $16 \times 16$ Taylor-Green case the correctors still converged for $C = 5$ to 20, only slowly.
- **Inconsistent pressure at the start.** If $p^n$ does not fit the scheme, as with an exact pressure sampled on a coarse grid, the first step loses one order: on $16 \times 16$ cells the measured one-corrector error fell like $\Delta t^2$ instead of $\Delta t^3$.
- **Inner solves that are too loose.** The proof assumes the pressure equation is solved exactly; a pressure solve stopped early leaves a divergence error of the size of its residual.
- **Frozen advection coefficients.** PISO linearizes advection at the old velocity. This is part of the first-order time error; a second order scheme needs a different predictor and more care.

## Implementations

## History

Issa (1986) introduced PISO as a way to solve the implicitly discretized flow equations by operator splitting, with one predictor and a sequence of correctors in each time step, and analyzed the splitting error. It grew out of the pressure correction idea of SIMPLE (Patankar and Spalding 1972, and Patankar 1980), applied without outer iterations. PISO became one of the standard transient solvers of finite volume codes.

## References
