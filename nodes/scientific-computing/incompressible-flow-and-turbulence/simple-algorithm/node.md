---
tag: 61PTZG
kind: algorithm
slug: simple-algorithm
name: SIMPLE algorithm
aliases:
- semi-implicit method for pressure-linked equations
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Couples pressure and velocity by guessing a pressure, solving momentum, then correcting both from a pressure correction equation, until converged."
solves: [navier-stokes-equations]
model: real-ram
complexity:
  vars: {M: "the number of grid cells", I: "the number of outer iterations", K: "the number of conjugate gradient iterations per pressure correction"}
  time: {worst: "Θ(I M K)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, iterative: true, steady_state: true, needs_poisson_solve: true, mass_conserving_iterates: true}
history:
  year: 1972
  people: [Suhas V. Patankar, D. Brian Spalding]
  note: Patankar and Spalding (1972) introduced the pressure correction procedure for three-dimensional parabolic flows, and Patankar's 1980 textbook made SIMPLE and its variant SIMPLER the standard method of finite volume codes.
prereqs: [navier-stokes-equations, mac-grid, finite-volume-method, gauss-seidel-method, poisson-equation]
see_also: [piso-algorithm, rhie-chow-interpolation, artificial-compressibility-method, chorin-projection-method, marker-and-cell-method, conjugate-gradient-method, successive-over-relaxation, fixed-point-iteration]
sources:
  - paper: doi:10.1016/0017-9310(72)90054-3
    title: S. V. Patankar and D. B. Spalding, A calculation procedure for heat, mass and momentum transfer in three-dimensional parabolic flows, International Journal of Heat and Mass Transfer 15(10) (1972) 1787-1806
    locator: the pressure correction procedure
  - book: isbn:9780070487406
    title: Suhas V. Patankar, Numerical Heat Transfer and Fluid Flow, Hemisphere and McGraw-Hill, 1980
    locator: Sections 6.3 to 6.8 (staggered grid, momentum equations, pressure and velocity corrections, the pressure correction equation, SIMPLE, SIMPLER)
  - book: isbn:9783319996912
    title: Joel H. Ferziger, Milovan Peric and Robert L. Street, Computational Methods for Fluid Dynamics, fourth edition, Springer, 2020
    locator: Chapter 7 (pressure correction methods for steady flow)
  - paper: doi:10.1016/0021-9991(86)90099-9
    title: R. I. Issa, Solution of the implicitly discretised fluid flow equations by operator-splitting, Journal of Computational Physics 62(1) (1986) 40-65
    locator: PISO, the non-iterative relative of SIMPLE for unsteady flow
---

SIMPLE, the Semi-Implicit Method for Pressure-Linked Equations, is the classic iteration for steady incompressible flow in finite volume codes. The difficulty is that incompressible flow has no equation for the pressure: the pressure is whatever field makes the velocity divergence free. SIMPLE guesses a pressure, solves the momentum equations with it, and then asks how the pressure must change so that the new velocity conserves mass. An approximate answer to that question is a Poisson-like equation for a pressure correction $p'$. The velocity takes the full correction, so it conserves mass after every iteration, and the pressure takes only a fraction of $p'$. The iteration repeats until the momentum equations hold too. At convergence the answer does not depend on the approximations made in the correction or on the under-relaxation factors.

## In plain words

Think of a network of pipes where the pump pressures are unknown. Guess the pressures and compute how the fluid would move with them. The result leaks: some junctions receive more fluid than they send out. For each junction, work out how much the pressure must go up or down to stop the leak, if each pipe reacts only to the pressures at its two ends. Correct the flows fully, so that nothing leaks now, but correct the pressures only part of the way, because the estimate of how pipes react was rough. Then compute the flows again with the new pressures and repeat. When nothing changes any more, the flows and the pressures fit each other exactly.

## The problem

Find a steady solution of the incompressible [Navier-Stokes equations](/navier-stokes-equations/)

$$(\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu\Delta\mathbf{u} + \mathbf{f}, \qquad \nabla\cdot\mathbf{u} = 0,$$

with $p$ the pressure divided by the density and $\nu$ the kinematic viscosity. This page uses the staggered [MAC grid](/mac-grid/) with $M$ cells, periodic in $x$, and in $y$ either periodic or closed by no-slip walls. Central differences for advection and viscosity give, at each velocity face, the discrete momentum equation

$$a_P u_P - \sum_{nb} a_{nb}u_{nb} = f_P - (Gp)_P,$$

with coefficients that depend on the velocity, and $D\mathbf{u} = 0$ at each cell, where $D$ is the divergence and $G$ the pressure gradient. Finite volume codes have the same structure with fluxes through cell faces. The cost is counted in real arithmetic operations.

## The algorithm

```pseudo id=main
SIMPLE(u, p, ν, f, α_u, α_p, s, tol)
L1  repeat
L2      compute a_P, a_nb from the current u                       ▷ Picard linearization
L3      u* ← s Gauss-Seidel sweeps on (a_P/α_u) u* - Σ a_nb u*_nb = f - G p + (1 - α_u)(a_P/α_u) u
L4      d ← α_u / a_P                                              ▷ on every velocity face
L5      solve -D(d G p') = -D u* for p'                            ▷ pressure correction equation
L6      p ← p + α_p p'
L7      u ← u* - d G p'
L8  until the momentum residual and |D u| are at most tol
L9  return (u, p)
```

Line L3 solves the momentum equations only roughly, with the old pressure and with momentum under-relaxation $\alpha_u$, which adds weight to the diagonal and pulls $\mathbf{u}^*$ toward the previous iterate. The corrected velocity should satisfy $a_P u'_P = \sum a_{nb}u'_{nb} - (Gp')_P$ for the corrections $u' = \mathbf{u} - \mathbf{u}^*$. SIMPLE drops the neighbor sum, which gives $u' = -d\,Gp'$ in line L7. Requiring $D\mathbf{u} = 0$ then gives the correction equation of line L5. Its matrix is $-D\operatorname{diag}(d)G$, a 5-point Poisson matrix with face weights $d$; a wall face has no correction, which is the Neumann condition for $p'$. This page solves it with [conjugate gradients](/conjugate-gradient-method/). Line L6 under-relaxes the pressure, because the dropped neighbor sum makes $p'$ too large. The values $\alpha_u = 0.7$, $\alpha_p = 0.3$ and $s = 3$ in the implementation are rules of thumb.

## Example

**Channel flow by hand.** Take a channel of height 1 with walls at $y = 0$ and $y = 1$, a constant force $G$ along $x$, and $n$ cells in $y$ with $\Delta y = 1/n$. The exact solution is $u = \tfrac{G}{2\nu}y(1-y)$, $v = 0$, $p$ constant. The discrete $u$ equation is $-\nu(u_{j+1} - 2u_j + u_{j-1})/\Delta y^2 = G$ with the ghost value $u_{-1} = -u_0$ for no slip, and the same at the top. A second difference is exact on a parabola, so $u_j = q(y_j) + c$ with $q(y) = \tfrac{G}{2\nu}y(1-y)$ satisfies the interior equations for any constant $c$. The ghost condition $q(-\Delta y/2) + c = -(q(\Delta y/2) + c)$ gives $c = -\tfrac12(q(\Delta y/2) + q(-\Delta y/2)) = \tfrac{G\Delta y^2}{8\nu}$. So the discrete solution overshoots the exact one by exactly $G\Delta y^2/(8\nu)$ at every face, second order in $\Delta y$. With $G = 1$ and $\nu = 0.5$ the shift is $1/64$ for $n = 4$ and $1/256$ for $n = 8$. SIMPLE reaches it from a zero start in 70, 155 and 568 iterations for $n = 4, 8, 16$ (tolerance $10^{-9}$). The count grows roughly with $n^2$ here, because three Gauss-Seidel sweeps per iteration spread viscous effects slowly across the channel.

**Under-relaxation.** A second test uses a channel on $[0, 2) \times [0, 1]$ with $8 \times 8$ cells, $\nu = 0.5$, and a force chosen so that a given smooth field, divergence free on the grid, is the exact discrete solution. SIMPLE recovers that field to $2 \times 10^{-11}$ from a zero start, with $\max|D\mathbf{u}| < 10^{-12}$ after every iteration. The number of iterations to a residual of $10^{-10}$:

| $\alpha_u$ | $\alpha_p$ | sweeps $s$ | iterations |
|---|---|---|---|
| 0.7 | 0.1 | 3 | 297 |
| 0.7 | 0.3 | 3 | 153 |
| 0.7 | 0.5 | 3 | 156 |
| 0.7 | 0.7 | 3 | 157 |
| 0.7 | 1.0 | 3 | diverges |
| 0.8 | 0.2 | 3 | 155 |
| 0.5 | 0.5 | 3 | 288 |
| 0.5 | 1.0 | 3 | 292 |
| 0.7 | 0.3 | 1 | 301 |
| 0.7 | 0.3 | 10 | 111 |

The runs with $(\alpha_u, \alpha_p) = (0.7, 0.3)$, $(0.8, 0.2)$ and $(0.5, 0.5)$ were compared with the given field and agree with it to $2 \times 10^{-11}$. With $\alpha_u = 0.7$ and $\alpha_p = 1$ the residual is 24 after 5 iterations and $8 \times 10^4$ after 25. These are measurements from the implementation on this page, not general results.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Summation by parts gives $G^T = -D$ on the staggered grid, so the correction matrix $-D\operatorname{diag}(d)G = G^T\operatorname{diag}(d)G$ is symmetric positive semidefinite, with the constants as its null space and the zero-sum vectors as its range. The right side $-D\mathbf{u}^*$ always sums to zero, so the correction equation is solvable, and the corrected velocity has $D\mathbf{u} = 0$ exactly, at every iteration and for every under-relaxation factor. The second theorem shows that the fixed points of SIMPLE are exactly the solutions of the discrete steady equations, for every $\alpha_u$, $\alpha_p$ and number of sweeps, provided that Gauss-Seidel converges on the relaxed momentum system. So the approximation in the velocity correction affects only the path, not the answer. Convergence itself is not proved; SIMPLE has no general convergence theorem.

## Complexity

One iteration assembles the coefficients and does $s$ Gauss-Seidel sweeps in $\Theta(M)$ operations, and solves the correction equation with $K$ conjugate gradient iterations of $\Theta(M)$ each. With $I$ outer iterations the total is $\Theta(I M K)$ for constant $s$, and the memory is $\Theta(M)$. Both $I$ and $K$ grow with the grid: $K$ grows like the square root of the condition number of the Poisson matrix, about $\sqrt{M}$ on a square grid, and $I$ grew like $n^2$ in the channel example. A [multigrid](/multigrid-method/) solver for the correction equation makes $K$ independent of the grid. Production codes also stop the inner solves early, since only the converged outer iterate matters.

## Properties

- Every iterate conserves mass on the discrete grid (Theorem 1 of the proof); only the momentum residual is not yet zero.
- The converged answer does not depend on $\alpha_u$, $\alpha_p$ or the inner solvers.
- The momentum equations are implicit, so SIMPLE has no time step limit of the CFL kind; under-relaxation plays the role of a pseudo time step.
- The pressure correction equation is the expensive part; it is a Poisson problem with variable coefficients $d$.
- On the staggered grid there is no checkerboard pressure mode. On a collocated grid SIMPLE needs [Rhie-Chow interpolation](/rhie-chow-interpolation/).

## Variants and improvements

- **SIMPLER** (Patankar 1980, Section 6.8) solves a separate pressure equation from the momentum coefficients and uses $p'$ only to correct the velocity, so the pressure needs no under-relaxation.
- **SIMPLEC** keeps part of the neighbor sum in the velocity correction, with $d = 1/(a_P - \sum a_{nb})$ in place of $1/a_P$, which allows $\alpha_p$ near 1.
- **[PISO](/piso-algorithm/)** (Issa 1986) applies two or more corrections per time step for unsteady flow, without outer iterations.
- **Coupled solvers** solve the momentum and continuity equations together with a block preconditioner, at a higher cost per iteration and with far fewer iterations.
- **Collocated grids** store all unknowns at cell centers and use [Rhie-Chow interpolation](/rhie-chow-interpolation/) for the face velocities in the continuity equation.

## When to use it

Use SIMPLE or one of its variants for steady incompressible flow with implicit momentum equations, especially in finite volume codes on unstructured or body-fitted grids, where it is widely used. For unsteady flow with small time steps, [PISO](/piso-algorithm/) or a [projection method](/chorin-projection-method/) avoids the outer iterations. For a simple explicit steady solver without a Poisson solve, [artificial compressibility](/artificial-compressibility-method/) is an alternative.

## Pitfalls

- **Too much pressure correction diverges.** The dropped neighbor sum makes $p'$ too large, and $\alpha_p = 1$ with $\alpha_u = 0.7$ diverged in the example. A common rule of thumb is $\alpha_p \approx 1 - \alpha_u$ for SIMPLE.
- **Too little under-relaxation is slow.** Small $\alpha_u$ or $\alpha_p$ converges, but the count roughly doubles from $\alpha_u = 0.7$ to $0.5$ in the example.
- **Stopping on the change between iterates.** Heavy under-relaxation makes successive iterates close long before they converge. Stop on the residual of the full discrete equations, as line L8 does.
- **Periodic boxes leave the mean velocity free.** With no walls, the steady equations do not fix the mean flow. The tests start a forced Taylor-Green vortex with two different mean velocities and get two different converged states, both with a residual below $10^{-10}$. Prescribe the mean velocity, or a mass flow rate in a periodic channel.
- **The pressure is fixed only up to a constant** when no boundary prescribes it. The correction equation is singular; keep its right side at zero sum and fix the constant afterwards.
- **Central advection at cell Péclet numbers above 2** loses diagonal dominance, and Gauss-Seidel on the momentum equations may stop converging. Production codes use upwind or deferred-correction schemes for advection.

## Implementations

## History

Patankar and Spalding (1972) introduced the pressure correction procedure in a paper on three-dimensional parabolic flows. Patankar's 1980 textbook gave the method on the staggered grid in its now standard form, with the discussion of the pressure correction equation, its boundary conditions and the relative nature of the pressure, and introduced SIMPLER. Collocated versions became possible with the interpolation of Rhie and Chow (1983), and Issa (1986) derived PISO for unsteady flow.

## References
