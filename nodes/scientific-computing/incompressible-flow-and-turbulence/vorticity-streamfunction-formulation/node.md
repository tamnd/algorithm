---
tag: 8HPSC5
kind: technique
slug: vorticity-streamfunction-formulation
name: Vorticity-streamfunction formulation
aliases:
- streamfunction-vorticity method
area: scientific-computing/incompressible-flow-and-turbulence
level: intro
summary: "Solves 2D incompressible flow for vorticity and streamfunction, which makes the velocity divergence free by construction and removes the pressure."
model: real-ram
prereqs: [navier-stokes-equations, poisson-equation, finite-difference-method, successive-over-relaxation]
see_also: [chorin-projection-method, artificial-compressibility-method, marker-and-cell-method, helmholtz-hodge-decomposition, vortex-particle-method, spectral-methods, multigrid-method, vorticity-confinement]
sources:
  - paper: doi:10.1098/rspa.1933.0146
    title: Alexander Thom, The flow past circular cylinders at low speeds, Proceedings of the Royal Society of London A 141(845) (1933) 651-669
    locator: the early hand computation of viscous flow in streamfunction and vorticity, to which the wall vorticity formula is usually credited
  - paper: doi:10.1016/0021-9991(82)90058-4
    title: U. Ghia, K. N. Ghia and C. T. Shin, High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method, Journal of Computational Physics 48(3) (1982) 387-411
    locator: the lid-driven cavity benchmark in streamfunction and vorticity; Table I (u on the vertical center line) and the primary vortex values for Re = 100
  - book: isbn:9783319996912
    title: Joel H. Ferziger, Milovan Perić and Robert L. Street, Computational Methods for Fluid Dynamics, 4th edition, Springer, 2020
    locator: the streamfunction-vorticity approach among the methods for incompressible flow
---

The vorticity-streamfunction formulation replaces the velocity and the pressure of a two-dimensional incompressible flow by two scalars: the streamfunction $\psi$, whose derivatives give the velocity, and the vorticity $\omega$, the local rate of rotation. Any velocity computed from a streamfunction is divergence free, so the incompressibility constraint is satisfied by construction, and taking the curl of the momentum equation removes the pressure. What remains is a transport equation for $\omega$ and a Poisson equation for $\psi$. The price is that the method is natural only in two dimensions, and that the wall has two conditions on $\psi$ and none on $\omega$, so the wall vorticity must come from a formula such as Thom's.

## In plain words

In a flat flow you can describe the motion by a height map of the streamfunction: the fluid always moves along the lines of equal height, faster where the lines are close together. Fluid that moves along such lines can never pile up or leave a gap, so the hardest condition of the problem holds for free. The second quantity, the spin of each small fluid parcel, is carried along by the flow and spreads out by friction. At every step the method moves the spin forward, then rebuilds the height map from the spin, and so gets the new velocity. The pressure is never needed. At a wall the spin is not known in advance; it is computed from how the height map bends next to the wall.

## When it applies

- **Two-dimensional incompressible flow.** In 2D the vorticity is a scalar and a single streamfunction exists on a simply connected domain. In 3D the streamfunction becomes a vector potential with three components and harder boundary conditions, and the method loses most of its advantage.
- **Simple geometry.** Squares, channels and polar or body-fitted grids around a cylinder, where the Poisson equation for $\psi$ is cheap to solve with [SOR](/successive-over-relaxation/), [multigrid](/multigrid-method/) or a fast transform.
- **When the pressure is not needed** inside the iteration. It can be recovered afterwards from a Poisson equation.
- **Teaching and benchmarks.** The lid-driven cavity of Ghia, Ghia and Shin (1982), computed in this formulation, is still a standard benchmark for incompressible solvers.

## The template

**Notation.** The velocity is $u = \partial\psi/\partial y$, $v = -\partial\psi/\partial x$; the vorticity is $\omega = \partial v/\partial x - \partial u/\partial y$; $\nu$ is the kinematic viscosity. Then $\nabla\cdot\mathbf{u} = \psi_{yx} - \psi_{xy} = 0$, and the curl of the [Navier-Stokes equations](/navier-stokes-equations/) gives

$$\omega_t + u\,\omega_x + v\,\omega_y = \nu\Delta\omega, \qquad \Delta\psi = -\omega.$$

On a wall at rest $\psi$ is constant (no flow through the wall) and $\partial\psi/\partial n$ is given (no slip). Both conditions are on $\psi$, and $\omega$ has none. **Thom's formula** supplies it: with $\psi_w = 0$ on the wall, $\psi_{w+1}$ at the first node inside, a distance $h$ away, and the tangential wall speed $U_w$, a Taylor series and $\omega_w = -\partial^2\psi/\partial n^2$ on the wall give

$$\omega_w = -\frac{2\psi_{w+1}}{h^2} \mp \frac{2U_w}{h},$$

with the sign of the second term set by the direction of the wall motion. For the cavity lid at $y = 1$ moving with speed $U$ it is $\omega = -2\psi_{i,n-1}/h^2 - 2U/h$. The formula is first order in $h$ for $\omega_w$.

```pseudo id=main
CAVITY(n, Re, Δt, U, tol)
    repeat
L1      ω on the walls ← Thom's formula from ψ next to the walls
L2      r ← -u ω_x - v ω_y + ν Δ_h ω at the interior nodes, central differences, u and v from ψ
L3      ω ← ω + Δt r at the interior nodes
L4      a few SOR sweeps on Δ_h ψ = -ω, with ψ = 0 on the walls
L5      if max|r| < tol and the Poisson residual < tol then
L6          return (ψ, ω)
```

At a steady state the time step and the number of SOR sweeps drop out: both discrete equations hold to the tolerance, so the answer depends only on the grid. Cells of size $h = 1/n$ give $(n - 1)^2$ unknowns for each scalar, and one step costs $\Theta(n^2)$ times the number of sweeps. **Recovering the pressure.** The divergence of the momentum equation gives $\Delta p = 2(u_x v_y - u_y v_x)$, with a Neumann condition from the momentum equation at the wall; it is solved once at the end.

## Classic examples

**Thom's formula by hand.** Let $h = 0.1$, a lid speed $U = 1$, and $\psi = -0.05$ at the first node below the lid. Then $\omega_{\text{lid}} = -2(-0.05)/0.01 - 2(1)/0.1 = 10 - 20 = -10$. Check: $\psi = U(y - 1) + a(y - 1)^2$ has $\psi = 0$ and $\psi_y = U$ at $y = 1$, and $\psi = -0.1 + 0.01a = -0.05$ at $y = 0.9$ gives $a = 5$, so $\omega = -\psi_{yy} = -2a = -10$. The formula is exact for this quadratic profile; the test file checks this in exact fractions.

**The lid-driven cavity at Re = 100.** The unit square, the lid moving with $U = 1$, $\nu = 0.01$. The implementation on this page, run to steady state (tolerance $10^{-5}$), against Ghia, Ghia and Shin (1982), who used a finer grid:

| cells | $\Delta t$ | steps | $u(0.5, 0.5)$ | error | $\psi_{\min}$ | error |
|---|---|---|---|---|---|---|
| $16 \times 16$ | 0.02 | 1089 | $-0.17576$ | 0.0300 | $-0.090978$ | 0.0124 |
| $32 \times 32$ | 0.01 | 2183 | $-0.20099$ | 0.0048 | $-0.100381$ | 0.0030 |
| $64 \times 64$ | 0.004 | 5354 | $-0.20719$ | 0.0014 | $-0.102723$ | 0.0007 |
| Ghia et al. | | | $-0.20581$ | | $-0.103423$ | |

The error in $\psi_{\min}$ falls by a factor of about 4 each time $h$ is halved, which is second order, although Thom's formula alone is first order. On the $64 \times 64$ grid the minimum of $u$ on the center line is $-0.21151$ at $y = 0.4531$, against $-0.21090$ at the same height in Ghia's Table I, and the center of the primary vortex is at the node $(0.6094, 0.7344)$. These are measurements.

**Divergence free by construction.** With central differences, the discrete velocity $u_{ij} = (\psi_{i,j+1} - \psi_{i,j-1})/(2h)$, $v_{ij} = -(\psi_{i+1,j} - \psi_{i-1,j})/(2h)$ has a central difference divergence that is exactly zero for every $\psi$, because the two difference operators commute. The test file checks this in exact fractions for a random $\psi$.

## Variations

- **Implicit time stepping.** ADI or fully implicit steps for the vorticity equation remove the explicit limit on $\Delta t$; a steady solver can also use Newton's method on the coupled discrete equations.
- **Streamfunction only.** Eliminating $\omega$ gives the fourth order equation $\partial_t\Delta\psi + \psi_y\Delta\psi_x - \psi_x\Delta\psi_y = \nu\Delta^2\psi$, with both wall conditions on $\psi$, which removes the need for a wall vorticity formula.
- **Other wall formulas.** Higher order one-sided formulas use more interior nodes, for example $\omega_w = (\psi_{w+2} - 8\psi_{w+1})/(2h^2)$ at a wall at rest, which is second order; they are more accurate but can be less stable.
- **Spectral methods.** In a periodic box $\psi$ follows from $\omega$ by a division in Fourier space, and the method is the standard one for 2D turbulence; see [spectral methods](/spectral-methods/).
- **Vortex methods.** [Vortex particle methods](/vortex-particle-method/) carry the vorticity on Lagrangian particles and recover the velocity by the Biot-Savart law instead of a Poisson solve on a grid.
- **3D vorticity-vector potential and vorticity-velocity methods** exist, but the boundary conditions are harder, and primitive variable methods such as the [projection method](/chorin-projection-method/) are more common in 3D.

## Pitfalls

- **Only 2D.** The scalar streamfunction does not exist in 3D, and the vector potential needs gauge and boundary conditions of its own.
- **Wall vorticity.** Thom's formula is the weak point: it is first order, it couples $\omega$ on the wall to $\psi$ inside, and an iteration that updates the two with large relaxation can diverge. Updating the wall values once per step, as here, is stable in practice.
- **Explicit time step.** The explicit central step needs $\Delta t$ below both the diffusion limit $h^2/(4\nu)$ and an advection limit of the order of $2\nu/|\mathbf{u}|^2$. On the $16 \times 16$ cavity at Re = 100, $\Delta t = 0.02$ converges and $\Delta t = 0.1$ overflows (measured).
- **Cell Reynolds number.** Central differences for the advection give wiggles when $|\mathbf{u}|h/\nu$ is much larger than 2; [upwind](/upwind-scheme/) differences remove them but add numerical viscosity.
- **Multiply connected domains.** Around an obstacle the value of $\psi$ on the obstacle is an unknown constant, fixed by the condition that the pressure is single valued.
- **The pressure is not free.** Forces on walls need the pressure, which needs a separate Poisson solve with a Neumann condition.

## Exercises

1. Show that $\nabla\cdot\mathbf{u} = 0$ for $u = \psi_y$, $v = -\psi_x$, and that the curl of the momentum equation gives the vorticity transport equation in 2D.
2. Derive Thom's formula from the Taylor series of $\psi$ normal to the wall, and show that its error is $O(h)$.
3. Show that the central difference divergence of the discrete velocity above is exactly zero.
4. On the unit cavity with $h = 1/2$ there is one interior node. Write the steady discrete equations and solve them for small Re.
5. Derive the pressure Poisson equation $\Delta p = 2(u_x v_y - u_y v_x)$ for a divergence free 2D velocity.

## References
