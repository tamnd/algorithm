---
tag: MYD986
kind: algorithm
slug: chorin-projection-method
name: Chorin projection method
aliases:
- Chorin-Temam projection method
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Advances the velocity without pressure, then solves a pressure Poisson equation and subtracts its gradient so the velocity is divergence free. First order in time."
solves: [navier-stokes-equations]
model: real-ram
complexity:
  vars: {M: "the number of grid cells", N: "the number of time steps", K: "the pressure solver iterations per step"}
  time: {worst: "Θ(N M K)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, explicit: true, order_time: "1", order_space: "2 on the MAC grid for smooth flow", divergence_free: true}
history:
  year: 1968
  people: [Alexandre J. Chorin, Roger Temam]
  note: Chorin (1968) split each time step into a velocity update without pressure and a projection onto divergence-free fields; Temam (1969) proved convergence of the same fractional step method independently.
prereqs: [helmholtz-hodge-decomposition, navier-stokes-equations, poisson-equation, mac-grid]
see_also: [marker-and-cell-method, stable-fluids, operator-splitting, piso-algorithm, artificial-compressibility-method, conjugate-gradient-method, multigrid-method, immersed-boundary-method]
sources:
  - paper: doi:10.1090/S0025-5718-1968-0242392-2
    title: Alexandre J. Chorin, Numerical solution of the Navier-Stokes equations, Mathematics of Computation 22(104) (1968) 745-762
    locator: the fractional step method, velocity update without pressure followed by projection
  - paper: doi:10.1007/BF00247696
    title: "Roger Temam, Sur l'approximation de la solution des equations de Navier-Stokes par la methode des pas fractionnaires (II), Archive for Rational Mechanics and Analysis 33 (1969) 377-385"
    locator: convergence of the fractional step (projection) method
  - paper: doi:10.1016/j.cma.2005.10.010
    title: J. L. Guermond, P. Minev and Jie Shen, An overview of projection methods for incompressible flows, Computer Methods in Applied Mechanics and Engineering 195(44-47) (2006) 6011-6045
    locator: pressure-correction schemes, the non-incremental and incremental forms, the artificial pressure boundary condition and its error
  - book: isbn:9783319996912
    title: Joel H. Ferziger, Milovan Peric and Robert L. Street, Computational Methods for Fluid Dynamics, fourth edition, Springer, 2020
    locator: Chapter 7 (solution of the Navier-Stokes equations, fractional step methods)
  - paper: doi:10.1063/1.1761178
    title: Francis H. Harlow and J. Eddie Welch, Numerical calculation of time-dependent viscous incompressible flow of fluid with free surface, Physics of Fluids 8(12) (1965) 2182-2189
    locator: the staggered grid that the projection uses here
---

Chorin's projection method advances incompressible flow in time in two parts per step. First it updates the velocity with advection, viscosity and body forces but without pressure. This intermediate velocity is not divergence free. Then it solves a [Poisson equation](/poisson-equation/) for the pressure and subtracts the pressure gradient, which removes exactly the part of the velocity that is not divergence free. The second part is the discrete [Helmholtz-Hodge decomposition](/helmholtz-hodge-decomposition/): it is an orthogonal projection onto divergence-free fields. Graphics readers know this step from [stable fluids](/stable-fluids/), which uses the same projection on the same [MAC grid](/mac-grid/). What the CFD form adds is a consistent advection term and a time step chosen for accuracy, so that the error falls at a known rate when the grid and the step are refined. The basic method is first order in time.

## In plain words

Water cannot be squeezed. If you push it into a region, the same amount must leave that region at once. The method moves the fluid forward in two moves. In the first move it lets the fluid carry itself along, slow down by friction and feel gravity, as if squeezing were allowed. After this move, some cells have more fluid coming in than going out. In the second move it finds the pressure that pushes the fluid out of the crowded cells and into the empty ones, just enough that each cell has the same inflow and outflow again. Finding this pressure means solving one large set of linked equations, one equation per cell. Then it applies the push. The second move changes only the part of the flow that broke the rule and leaves the rest alone.

## The problem

Solve the incompressible [Navier-Stokes equations](/navier-stokes-equations/)

$$\mathbf{u}_t + (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu\Delta\mathbf{u} + \mathbf{f}, \qquad \nabla\cdot\mathbf{u} = 0,$$

for the velocity $\mathbf{u} = (u, v)$ and the pressure $p$ up to a time $T$, from a divergence-free initial velocity. Here $p$ is the pressure divided by the constant density and $\nu$ is the kinematic viscosity. The pressure has no evolution equation. It is the Lagrange multiplier of the constraint $\nabla\cdot\mathbf{u} = 0$, and it is fixed only up to a constant.

This page uses a periodic box with $M = n_x n_y$ cells on a staggered [MAC grid](/mac-grid/): $p$ at cell centers, $u$ on the left face and $v$ on the bottom face of each cell. $D$ is the discrete divergence at the centers and $G$ the discrete gradient at the faces, both by central differences over one cell. On this grid $A = -DG$ is the 5-point matrix of minus the Laplacian. The cost is counted in arithmetic operations on reals and in iterations of the pressure solver.

## The algorithm

```pseudo id=main
CHORIN-PROJECTION(u, v, Δt, ν, f, N)
L1  for n ← 0 to N - 1 do
L2      (u*, v*) ← (u, v) + Δt (-(u·∇)u + ν Δ_h u + f)    ▷ no pressure term
L3      b ← -D(u*, v*) / Δt
L4      solve A p = b                                      ▷ A = -D G, the 5-point matrix
L5      (u, v) ← (u*, v*) - Δt G p
L6  return (u, v, p)
```

Line L2 is one forward Euler step of the momentum equation without $\nabla p$. The implementation computes the advection term in advective form with central differences, averaging $v$ to the $u$ faces and $u$ to the $v$ faces, and the viscous term with the 5-point Laplacian on each velocity component. Lines L3 to L5 project: $D$ of the new velocity is $D\mathbf{u}^* - \Delta t\, DGp = D\mathbf{u}^* + \Delta t\, Ap = 0$. The periodic matrix $A$ is singular, with the constants as null space, and $b$ has zero sum, so $p$ exists and is unique up to a constant. The implementation solves line L4 by [conjugate gradient](/conjugate-gradient-method/), warm started from the previous pressure. A [multigrid](/multigrid-method/) solver or, on a periodic box, a [fast Fourier transform](/fast-fourier-transform/) solve can replace it.

With walls, the normal velocity on a wall face is set to the wall value and is not changed by the projection, and the pressure equation gets the homogeneous Neumann condition $\partial p/\partial n = 0$ at the wall. The [marker and cell method](/marker-and-cell-method/) page works out this case.

## Example

**A projection by hand.** Take a periodic row of 4 cells with $\Delta x = 1$, $\Delta t = 1$, $v^* = 0$, and $u^* = (1, 0, 0, 0)$ on the 4 faces, so face 0 carries one unit of flow into cell 0 from cell 3. The divergence is $D u^* = (-1, 0, 0, 1)$, so $b = (1, 0, 0, -1)$. The matrix $A$ is the periodic second difference with rows $(2, -1, 0, -1)$ and its shifts. The solution with zero mean is $p = (\tfrac38, \tfrac18, -\tfrac18, -\tfrac38)$; for example row 0 gives $2 \cdot \tfrac38 - \tfrac18 + \tfrac38 = 1$. The face gradients are $Gp = (p_0 - p_3, p_1 - p_0, p_2 - p_1, p_3 - p_2) = (\tfrac34, -\tfrac14, -\tfrac14, -\tfrac14)$, and

$$u = u^* - Gp = (\tfrac14, \tfrac14, \tfrac14, \tfrac14).$$

In one periodic dimension a divergence-free field is a constant, and the projection keeps the mean flow $\tfrac14$ and removes the rest, which is a gradient. The test file checks these numbers.

**Taylor-Green vortex.** On the periodic square $[0, 2\pi]^2$ the field $u = -\cos x \sin y\, e^{-2\nu t}$, $v = \sin x \cos y\, e^{-2\nu t}$, $p = -\tfrac14(\cos 2x + \cos 2y)\, e^{-4\nu t}$ is an exact solution with $\mathbf{f} = 0$. With $\nu = 0.1$, $T = 0.5$ and $\Delta t \approx 0.4\,\Delta x^2$ (so that the first order time error also scales like $\Delta x^2$), the maximum velocity error at $T$ is:

| $N \times N$ cells | steps | $\Delta t$ | max error | observed order |
|---|---|---|---|---|
| $8 \times 8$ | 2 | 0.25 | 2.266e-3 | |
| $16 \times 16$ | 8 | 0.0625 | 5.898e-4 | 1.94 |
| $32 \times 32$ | 32 | 0.015625 | 1.489e-4 | 1.99 |

The discrete divergence after every projection is about $10^{-14}$. For the order in time, fix the $16 \times 16$ grid, set $T = 1$, and compare runs with 10, 20, 40 and 80 steps. The differences between successive runs are 7.99e-4, 3.96e-4 and 1.97e-4, an observed order of 1.01, as expected for a first order method. These are measurements from the implementation on this page.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). On the periodic MAC grid, summation by parts gives $G^T = -D$, so $A = -DG$ is symmetric positive semidefinite with the constants as its null space, and every divergence $D\mathbf{u}^*$ has zero sum. So the pressure equation has a solution, the new velocity has zero discrete divergence, and it is the orthogonal projection of $\mathbf{u}^*$ onto the discretely divergence-free fields. From this, one Chorin step is exactly one forward Euler step for the projected system $\mathbf{u}' = P_h F_h(\mathbf{u})$, which is the method-of-lines form of the discrete Navier-Stokes equations. This gives first order convergence in time on a fixed periodic grid (a theorem, with $F_h$ Lipschitz on bounded sets). The spatial order 2 is a measurement on this page. For the continuous problem, Temam (1969) proved convergence of the fractional step method.

## Complexity

One step costs $\Theta(M)$ operations for lines L2, L3 and L5, plus the pressure solve. CG on the 5-point matrix has condition number $O(\Delta x^{-2})$, so it needs $O(n_x)$ iterations for a fixed tolerance on general data, and one step costs $O(M^{3/2})$ on a square grid. Multigrid solves it in $O(M)$ and an FFT in $O(M\log M)$. Memory is $\Theta(M)$. On the Taylor-Green vortex, whose data lie in a few eigenvectors, warm-started CG needed 2.0, 4.1 and 8.9 iterations per step on the three grids above (a measurement).

The explicit update limits the time step. The viscous term needs $\Delta t \le 1/\big(2\nu(\Delta x^{-2} + \Delta y^{-2})\big)$, and central advection with forward Euler needs the viscous term to damp it, about $\Delta t \le 2\nu/|\mathbf{u}|_{\max}^2$, together with the advective [CFL condition](/courant-friedrichs-lewy-condition/). With $\Delta t \sim \Delta x^2/\nu$, a run to time $T$ takes $N = \Theta(T\nu/\Delta x^2)$ steps. Implicit diffusion removes the viscous limit at the price of one more linear solve per velocity component per step.

## Properties

- Exact discrete incompressibility: $D\mathbf{u}^{n+1} = 0$ up to the pressure solver tolerance, at every step.
- The projection is orthogonal, so it never increases the discrete kinetic energy: $\|\mathbf{u}^{n+1}\| \le \|\mathbf{u}^*\|$.
- First order in time, both for the velocity and for the pressure on a periodic domain. Second order in space on the MAC grid for smooth flow (measured here).
- The pressure is not a state variable. It is recomputed at each step and needs no initial value.
- One elliptic solve per step, with a constant matrix, so a factorization or a multigrid hierarchy is set up once.

## Variants and improvements

- **Incremental pressure correction.** Keep the old pressure gradient in the predictor, $\mathbf{u}^* = \dots - \Delta t\,Gp^n$, and solve for the increment $p^{n+1} - p^n$. This is the form used with second order time stepping (Goda 1979, van Kan 1986). In its rotational form the pressure error near walls drops (Guermond, Minev and Shen 2006).
- **Implicit diffusion.** Treat $\nu\Delta\mathbf{u}$ by [backward Euler](/backward-euler-method/) or [Crank-Nicolson](/crank-nicolson-method/), so the time step is limited only by advection.
- **Stable fluids.** Semi-Lagrangian advection makes the step stable for any $\Delta t$, at the cost of strong numerical dissipation; see [stable fluids](/stable-fluids/).
- **[PISO](/piso-algorithm/).** Several pressure corrections per step with an implicit momentum equation; the first corrector is close to a projection.
- **Velocity correction schemes** swap the roles: the viscous term is corrected after the pressure step.
- **Approximate projections** on collocated or adaptive grids give a field that is only approximately divergence free, in exchange for simpler data structures.

## When to use it

Use the projection method for time-accurate incompressible flow when one Poisson solve per step is affordable: direct simulation of transitional and turbulent flow, flows in boxes and channels, and as the fluid solver inside the [immersed boundary method](/immersed-boundary-method/). On periodic domains with an FFT pressure solve, it is hard to beat. For steady flow, where time accuracy does not matter, [SIMPLE](/simple-algorithm/) or [artificial compressibility](/artificial-compressibility-method/) go to the steady state with larger effective steps.

## Pitfalls

- **Collocated grids.** If $p$ and $\mathbf{u}$ sit at the same points and $D$ and $G$ are wide central differences, $DG$ has a checkerboard null space and the pressure oscillates. Use a staggered grid, or add [Rhie-Chow interpolation](/rhie-chow-interpolation/).
- **The artificial pressure boundary condition.** With walls and implicit viscosity, $\mathbf{u}^*$ satisfies the wall condition but the projection changes its tangential part, and the pressure gets $\partial p/\partial n = 0$, which the true pressure does not satisfy. This splitting error creates a numerical boundary layer. For the basic non-incremental scheme the velocity is first order in $L^2$ but the pressure only of order $\Delta t^{1/2}$; the incremental form recovers first order (Guermond, Minev and Shen 2006).
- **The singular pressure matrix.** On a periodic domain or with only Neumann walls, fix the constant (zero mean, or one value) and keep $b$ in the range of $A$, or CG drifts.
- **Too loose a pressure tolerance** leaves a divergence that accumulates over many steps. Measure $\max|D\mathbf{u}|$ after the projection, not only the solver residual.
- **The time step.** The explicit viscous and advective limits above are hard limits; central advection with forward Euler is unstable without viscosity.
- **Initial data** that are not divergence free are projected in the first step. That is harmless, but the first pressure then has no physical meaning.

## Implementations

## History

Chorin (1968) proposed the method in Mathematics of Computation. Temam (1969) analyzed the same idea, which he called the method of fractional steps, and proved its convergence. The method builds on the staggered grid of Harlow and Welch (1965). Incremental forms (Goda 1979, van Kan 1986) and the analysis of the splitting error near walls followed; Guermond, Minev and Shen (2006) survey the family. Stam's stable fluids (1999) brought the same projection into computer graphics.

## References
