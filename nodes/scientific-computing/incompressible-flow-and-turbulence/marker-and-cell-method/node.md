---
tag: B1FT13
kind: algorithm
slug: marker-and-cell-method
name: Marker-and-cell method
aliases:
- MAC method
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Solves incompressible flow on a staggered grid, with pressures at cell centers and velocities on faces, and tracks the free surface with marker particles."
solves: [navier-stokes-equations]
model: real-ram
complexity:
  vars: {M: "the number of grid cells", N: "the number of time steps", K: "the pressure solver iterations per step", P: "the number of marker particles"}
  time: {worst: "Θ(N (M K + P))"}
  space: {extra: "Θ(M + P)"}
properties: {deterministic: true, explicit: true, staggered: true, divergence_free: true, order_space: "2 for smooth confined flow", order_time: "1"}
history:
  year: 1965
  people: [Francis H. Harlow, J. Eddie Welch]
  note: Harlow and Welch (1965) put pressure at cell centers and velocity components on cell faces, solved a Poisson equation for the pressure at each step, and moved marker particles to show where the fluid is.
prereqs: [navier-stokes-equations, mac-grid, poisson-equation, chorin-projection-method]
see_also: [mac-grid, chorin-projection-method, stable-fluids, helmholtz-hodge-decomposition, volume-of-fluid-method, level-set-method, rhie-chow-interpolation, simple-algorithm]
sources:
  - paper: doi:10.1063/1.1761178
    title: Francis H. Harlow and J. Eddie Welch, Numerical calculation of time-dependent viscous incompressible flow of fluid with free surface, Physics of Fluids 8(12) (1965) 2182-2189
    locator: the staggered grid, the pressure Poisson equation, marker particles and the free surface conditions
  - book: isbn:9783319996912
    title: Joel H. Ferziger, Milovan Peric and Robert L. Street, Computational Methods for Fluid Dynamics, fourth edition, Springer, 2020
    locator: Chapter 7 (staggered grids, the pressure equation and fractional step methods)
  - book: isbn:9780070487406
    title: Suhas V. Patankar, Numerical Heat Transfer and Fluid Flow, Hemisphere, 1980
    locator: Section 6.3 (the staggered grid and why it removes the checkerboard pressure)
  - paper: doi:10.1090/S0025-5718-1968-0242392-2
    title: Alexandre J. Chorin, Numerical solution of the Navier-Stokes equations, Mathematics of Computation 22(104) (1968) 745-762
    locator: the projection step in the form used by later MAC codes
---

The marker-and-cell (MAC) method computes time-dependent incompressible flow on a staggered grid. Pressure lives at cell centers, and each velocity component lives on the cell faces normal to it. Each time step updates the velocity from advection, viscosity and gravity, then solves a [Poisson equation](/poisson-equation/) for the pressure that makes the new velocity divergence free in every cell. Massless marker particles move with the flow; the cells that hold markers are the fluid, and the empty cells are air, which lets the method follow a free surface. Graphics readers know the grid as the [MAC grid](/mac-grid/) and the step as the pressure projection of [stable fluids](/stable-fluids/). The MAC method as a CFD scheme adds central, consistent differences for advection and viscosity, a time step set by accuracy and stability limits, and wall conditions for each velocity component, so that the error falls at a measured second order rate in space.

## In plain words

Divide the box into square cells. Keep one pressure value in the middle of each cell. Keep the flow through each wall between two cells as one number on that wall. Then the amount that leaves a cell is easy to count: add up the four walls. Each step has three moves. First, let the flow carry itself along and feel friction and gravity. Second, find the pressures that make each cell lose exactly as much as it gains, and push the flow with them. Third, move a cloud of tiny tracer dots with the flow. The dots show where the water is, so cells with dots are wet and cells without dots are dry. Because pressures and wall flows sit at different places, the pressures cannot form a hidden zigzag pattern that the flow does not feel.

## The problem

Solve the incompressible [Navier-Stokes equations](/navier-stokes-equations/) $\mathbf{u}_t + (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu\Delta\mathbf{u} + \mathbf{g}$, $\nabla\cdot\mathbf{u} = 0$ in a rectangular box, with $p$ the pressure divided by the density and $\nu$ the kinematic viscosity, up to a time $T$. At the walls the normal velocity is zero. The tangential velocity is either free (free slip, zero shear) or set (no slip, with a moving lid as a special case). The cost is counted in real arithmetic operations and pressure solver iterations on $M = n_x n_y$ cells.

The grid places $p_{i,j}$ at the cell center $((i + \tfrac12)\Delta x, (j + \tfrac12)\Delta y)$, $u_{i,j}$ at $(i\Delta x, (j + \tfrac12)\Delta y)$ for $i = 0, \dots, n_x$, and $v_{i,j}$ at $((i + \tfrac12)\Delta x, j\Delta y)$ for $j = 0, \dots, n_y$. The wall faces hold the normal velocity, which is zero. $D$ is the divergence at the centers, $G$ the gradient at the interior faces, and $A = -DG$.

## The algorithm

```pseudo id=main
MAC(u, v, markers, Δt, ν, g, N)
L1  for n ← 0 to N - 1 do
L2      fill the ghost values from the wall conditions, and form -(u·∇)u + ν Δ_h u
L3      (u*, v*) ← (u, v) + Δt (-(u·∇)u + ν Δ_h u + g)      ▷ interior faces only
L4      solve A p = -D(u*, v*) / Δt                        ▷ ∂p/∂n = 0 at the walls
L5      (u, v) ← (u*, v*) - Δt G p                         ▷ interior faces only
L6      move every marker with the interpolated velocity
L7      flag the cells that hold a marker as fluid
L8  return (u, v, p, markers, fluid cells)
```

The tangential velocity at a wall enters only through ghost values outside the box. For free slip the ghost is a mirror copy of the first interior value. For no slip with wall speed $U$ it is $2U$ minus the interior value, so that the average on the wall is $U$. The wall faces are never changed, and $G$ is zero there, which gives the pressure equation the homogeneous Neumann condition. The advection term uses central differences with the other component averaged from its four nearest faces. Markers move by a midpoint step with bilinear interpolation of each component.

The implementation on this page handles confined flow, where all cells are fluid. For a free surface, Harlow and Welch (1965) set the pressure in surface cells from the normal stress condition, set the velocities on faces between fluid and empty cells so that the surface cells are divergence free, and leave empty cells out of the pressure solve.

## Example

**Why the staggering matters, by hand.** Take the checkerboard pressure $p_{i,j} = (-1)^{i+j}$ on a $4 \times 4$ grid with $\Delta x = \tfrac14$. A collocated central gradient $(p_{i+1,j} - p_{i-1,j})/(2\Delta x)$ is zero at every interior point, because both neighbors have the same sign. A solver that uses it cannot see or remove this pressure. The MAC gradient $(p_{i,j} - p_{i-1,j})/\Delta x$ is $\pm 8$ on every interior face, so the checkerboard is not in the null space. On the MAC grid, $-DG$ is exactly the 5-point Neumann matrix, and the only pressures it ignores are the constants. For a $3 \times 2$ grid with $\Delta x = 1$, $\Delta y = \tfrac12$ the corner cell's row is $(1 + 4, -1, -4)$ for itself, its east neighbor and its north neighbor; the test file checks every column of this matrix in exact rational arithmetic.

**Free-slip Taylor-Green vortex.** In the box $[0, \pi]^2$ the field $u = \sin x \cos y\, e^{-2\nu t}$, $v = -\cos x \sin y\, e^{-2\nu t}$, $p = \tfrac14(\cos 2x + \cos 2y)\, e^{-4\nu t}$ is an exact solution with zero normal velocity and zero shear at the walls. With $\nu = 0.1$, $T = 0.2$ and $\Delta t \approx 0.4\,\Delta x^2$, the maximum errors at $T$ (pressure with the mean removed) are:

| cells | steps | velocity error | order | pressure error | order |
|---|---|---|---|---|---|
| $8 \times 8$ | 3 | 2.349e-4 | | 7.184e-3 | |
| $16 \times 16$ | 13 | 6.414e-5 | 1.87 | 1.736e-3 | 2.05 |
| $32 \times 32$ | 52 | 1.607e-5 | 2.00 | 4.441e-4 | 1.97 |

The divergence after each step is below $10^{-13}$. In the same vortex, frozen in time on a $16 \times 16$ grid, four markers moved for 100 midpoint steps of $\Delta t = 0.05$ keep the stream function $\sin x \sin y$ constant to $1.9 \times 10^{-4}$, so they stay on their streamlines. In a no-slip cavity of $8 \times 8$ cells with the lid moving at speed 1 and $\nu = 0.01$, 60 steps of $\Delta t = 0.01$ give the start of the primary vortex: the top row moves right with the lid and the fluid below it returns to the left. These are measurements from the implementation on this page.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). For velocity fields with zero normal velocity on the walls, summation by parts gives $\langle\mathbf{u}, Gp\rangle = -(D\mathbf{u}, p)$. So $A = -DG$ is the symmetric Neumann 5-point matrix, its null space is the constants, and the right side of the pressure equation has zero sum because nothing flows through the walls. The pressure equation then has a solution, the new velocity has zero divergence in every cell, and it is the orthogonal projection of the predicted velocity onto the divergence-free fields, so the projection never adds kinetic energy. The same lemma shows that only constant pressures have zero MAC gradient, so there is no checkerboard mode. The proof also shows that marker interpolation is exact for linear fields. The second order spatial accuracy is a measurement, not a theorem proved here.

## Complexity

One step costs $\Theta(M)$ for the momentum update, the divergence and the gradient, $O(1)$ per marker, and one Poisson solve. CG needs $O(n_x)$ iterations on general data for a fixed tolerance, so a step costs $O(M^{3/2})$ on a square grid with CG and $O(M)$ with [multigrid](/multigrid-method/). Memory is $\Theta(M + P)$. The explicit step must satisfy the viscous limit $\Delta t \le 1/\big(2\nu(\Delta x^{-2} + \Delta y^{-2})\big)$ and the advective limits. The number of markers per cell is a choice.

## Properties

- Exact discrete mass conservation in every cell, up to the solver tolerance.
- No spurious pressure modes: the null space of $-DG$ is the constants.
- Second order in space for smooth confined flow on a uniform grid (measured above), first order in time with forward Euler.
- The projection is orthogonal in the discrete $L^2$ inner product and never increases the kinetic energy.
- The markers carry no mass and do not affect the flow; they only mark fluid cells.

## Variants and improvements

- **SMAC (simplified MAC)** by Amsden and Harlow (1970) solves for a pressure correction, which is the [projection method](/chorin-projection-method/) form used today.
- **Implicit diffusion** and second order time stepping (Adams-Bashforth, Crank-Nicolson) on the same grid.
- **Surface tracking.** [Volume of fluid](/volume-of-fluid-method/) and [level set](/level-set-method/) methods replaced markers for the free surface in most codes, because they give the surface position and the curvature more cleanly.
- **Particle methods on the MAC grid.** PIC and FLIP keep markers that carry velocity; this is the graphics branch that grew out of MAC.
- **Staggered grids in finite volume codes.** [SIMPLE](/simple-algorithm/) and its relatives use the same staggering for steady flow; collocated codes replace it with [Rhie-Chow interpolation](/rhie-chow-interpolation/).
- **Graphics.** Foster and Metaxas (1996) used the MAC method for animating liquids, and Stam (1999) made the step unconditionally stable with semi-Lagrangian advection.

## When to use it

Use the MAC method for incompressible flow on rectangular or nearly rectangular domains, in particular with a free surface: sloshing, dam breaks, splashing in animation, and flows driven by moving walls such as the lid-driven cavity. It is a good base for teaching and for codes where exact cell mass conservation matters. On complex geometry, unstructured finite volume or finite element methods fit the walls better, or an [immersed boundary method](/immersed-boundary-method/) brings the geometry onto the MAC grid.

## Pitfalls

- **Index offsets.** On a staggered grid $u_{i,j}$, $v_{i,j}$ and $p_{i,j}$ sit at three different points. Most bugs are half-cell offsets in the averages of the advection term or in the interpolation of markers; test interpolation on linear fields.
- **The no-slip ghost value** is a linear extrapolation. The viscous term next to the wall is then only first order accurate locally; the global error is usually still second order, but wall shear stress needs care.
- **The singular pressure matrix.** In a closed box the pressure is fixed only up to a constant. Keep the right side of the pressure equation at zero sum and fix the constant.
- **Marker gaps.** Markers spread out in stretching flow and leave fluid cells with no markers, which are then flagged as empty by mistake. Add markers or use a surface tracking method.
- **Free surface boundary conditions** need consistent velocities on faces next to empty cells; mistakes there show up as mass loss.
- **Explicit time step limits** are hard limits. Central advection with forward Euler needs enough viscosity; at high Reynolds number use upwind or higher order time stepping.

## Implementations

## History

Harlow and Welch (1965) published the MAC method in Physics of Fluids for time-dependent viscous incompressible flow with a free surface, with the staggered grid, a Poisson equation for the pressure at each step and marker particles. Chorin (1968) gave the projection form of the pressure step, and Amsden and Harlow (1970) simplified the method as SMAC. Patankar (1980) made the staggered grid standard in steady finite volume solvers. Foster and Metaxas (1996) brought the method into computer graphics, where the grid is now called the MAC grid.

## References
