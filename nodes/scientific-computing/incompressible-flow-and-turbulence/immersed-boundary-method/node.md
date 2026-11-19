---
tag: J7JVKP
kind: algorithm
slug: immersed-boundary-method
name: Immersed boundary method
aliases:
- Peskin immersed boundary method
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: "Represents an elastic boundary by points that spread forces to a fixed grid through a smoothed delta function and move with the interpolated velocity."
solves: [navier-stokes-equations]
model: real-ram
complexity:
  vars: {M: "the number of grid cells", P: "the number of membrane points", N: "the number of time steps", K: "the number of conjugate gradient iterations per pressure solve"}
  time: {worst: "Θ(N (M K + P))"}
  space: {extra: "Θ(M + P)"}
properties: {deterministic: true, explicit: true, fixed_cartesian_grid: true, lagrangian_boundary: true, needs_poisson_solve: true, divergence_free_grid_velocity: true}
history:
  year: 1972
  people: [Charles S. Peskin]
  note: Peskin (1972) computed blood flow around heart valves by letting elastic boundary points exert force on a fixed Cartesian fluid grid through a smoothed delta function and move with the local fluid velocity.
prereqs: [navier-stokes-equations, chorin-projection-method, mac-grid]
see_also: [ghost-fluid-method, front-tracking-method, level-set-method, marker-and-cell-method, particle-in-cell, fluid-implicit-particle, smoothed-particle-hydrodynamics, chorin-projection-method]
sources:
  - paper: doi:10.1016/0021-9991(72)90065-4
    title: Charles S. Peskin, Flow patterns around heart valves, a numerical method, Journal of Computational Physics 10(2) (1972) 252-271
    locator: the original method for elastic boundaries in a fluid on a fixed grid
  - paper: doi:10.1017/S0962492902000077
    title: Charles S. Peskin, The immersed boundary method, Acta Numerica 11 (2002) 479-517
    locator: the continuous equations, the conditions on the discrete delta function and the four-point kernel
  - paper: doi:10.1146/annurev.fluid.37.061903.175743
    title: Rajat Mittal and Gianluca Iaccarino, Immersed boundary methods, Annual Review of Fluid Mechanics 37 (2005) 239-261
    locator: the survey of continuous forcing and discrete forcing variants
  - paper: doi:10.1090/S0025-5718-1968-0242392-2
    title: Alexandre J. Chorin, Numerical solution of the Navier-Stokes equations, Mathematics of Computation 22(104) (1968) 745-762
    locator: the projection method used for the fluid step
---

The immersed boundary method computes the flow of a fluid that contains a moving elastic structure, such as a heart valve, a cell membrane or a flexible fiber, on a fixed Cartesian grid that does not follow the structure. The structure is a set of points with their own coordinates. In every time step the points compute their elastic forces, spread those forces onto nearby grid cells through a smoothed delta function, the fluid solver advances the velocity with this body force, and the points then move with the fluid velocity interpolated back from the same delta function. No grid has to be fitted to the boundary or regenerated as it moves. The price is a boundary that is smeared over a few grid cells and an accuracy near the boundary that is usually only first order in the grid spacing.

## In plain words

Picture a rubber band floating in water on a sheet of graph paper. The band is drawn as a chain of beads, and the water is known only at the squares of the paper. When the band is stretched, each bead pulls on the water, and that pull is shared out among the squares near the bead, a little more to the nearest ones. The water then moves under these pulls while staying incompressible. Each bead then looks at the squares around it, takes a weighted average of their motion with the same weights, and moves by that amount. The beads and the squares always use the same weights, so the work the band does on the water is the same whether counted at the beads or at the squares.

## The problem

A closed elastic curve $\mathbf{X}(s, t)$ is immersed in a fluid that fills the periodic box. The fluid obeys the incompressible [Navier-Stokes equations](/navier-stokes-equations/) with a body force from the curve,

$$\mathbf{u}_t + (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu\Delta\mathbf{u} + \mathbf{f}, \qquad \nabla\cdot\mathbf{u} = 0, \qquad \mathbf{f}(\mathbf{x}) = \int \mathbf{F}(s)\,\delta(\mathbf{x} - \mathbf{X}(s))\,ds,$$

with $p$ the pressure divided by the density and $\nu$ the kinematic viscosity. The curve moves with the fluid, $\mathbf{X}_t = \mathbf{u}(\mathbf{X})$, and its force density comes from its elasticity; for springs of zero rest length with stiffness $\kappa$, $\mathbf{F} = \kappa\,\mathbf{X}_{ss}$. The discrete method uses the periodic [MAC grid](/mac-grid/) with $M$ cells of size $h$ and $P$ points $\mathbf{X}_l$ with parameter spacing $\Delta s$, and replaces $\delta$ by $\delta_h(\mathbf{x}) = \phi(x/h)\phi(y/h)/h^2$ with Peskin's four-point kernel $\phi$, whose support is 4 cells wide. The cost is counted in real arithmetic operations.

## The algorithm

```pseudo id=main
IB-STEP(u, X, κ, Δs, ν, Δt)
L1  F_l ← κ (X_{l+1} - 2 X_l + X_{l-1}) / Δs²              ▷ elastic force at each point
L2  f(x) ← Σ_l F_l δ_h(x - X_l) Δs                          ▷ spread to the grid
L3  u* ← u + Δt (-(u·∇)u + ν Δ_h u + f)                     ▷ explicit momentum step
L4  solve -D G q = -D u*;  u ← u* - G q;  p ← q / Δt         ▷ projection
L5  U_l ← Σ_x u(x) δ_h(x - X_l) h²                          ▷ interpolate to the points
L6  X_l ← X_l + Δt U_l
L7  return (u, p, X)
```

Lines L2 and L5 use the same weights $\phi\phi$ at the 16 grid points around each membrane point, separately for the $u$ and the $v$ lattice of the staggered grid. Line L4 is the projection of [Chorin's method](/chorin-projection-method/), solved here with conjugate gradients. Peskin's kernel $\phi$ is $(3 - 2|r| + \sqrt{1 + 4|r| - 4r^2})/8$ for $|r| \le 1$, $(5 - 2|r| - \sqrt{-7 + 12|r| - 4r^2})/8$ for $1 \le |r| \le 2$, and 0 beyond. It is the unique function with this support for which, at every position $r$, the weights sum to 1 separately over even and odd grid points (each half gets $1/2$), have zero first moment, and have squares summing to $3/8$. The first two conditions make the interpolation exact for linear fields and keep total force and torque; the last one makes the coupling between two points almost independent of where they sit relative to the grid.

## Example

**A static circle.** Put $P$ points on a circle of radius $R$. The discrete spring force is $\mathbf{F}_l = -\kappa\lambda(\mathbf{X}_l - \mathbf{c})$ with $\lambda = (2 - 2\cos\Delta s)/\Delta s^2$, normal to the circle and of equal size everywhere. This is a stretched band with tension $\kappa\lambda R$, so by the Laplace law the pressure inside exceeds the pressure outside by the tension divided by the radius, $\kappa\lambda$, and the fluid stays at rest. On the unit box with $R = 0.25$, $\kappa = 1$ and a point spacing of about $h/2$, the difference of the mean pressures inside and outside (cells more than $2h$ from the circle) after one spreading and one projection:

| grid | points | measured jump | $\kappa\lambda$ |
|---|---|---|---|
| $16 \times 16$ | 50 | 0.998556 | 0.998685 |
| $32 \times 32$ | 101 | 0.999665 | 0.999678 |
| $64 \times 64$ | 201 | 0.999925 | 0.999919 |

The pressure is flat inside to within $10^{-3}$. The jump is smeared over the support of $\delta_h$, about $2h$ on each side of the circle.

**A relaxing ellipse.** Start with 100 points on an ellipse with semi-axes 0.3 and 0.2 in fluid at rest, with $\kappa = 1$, $\nu = 0.1$, a $32 \times 32$ grid and $\Delta t = 0.002$. The tension pulls the ellipse toward a circle:

| time | width | height | relative area change |
|---|---|---|---|
| 0 | 0.6 | 0.4 | 0 |
| 0.1 | 0.5884 | 0.4064 | 3.05e-5 |
| 0.2 | 0.5686 | 0.4206 | 3.30e-5 |
| 0.3 | 0.5488 | 0.4367 | 2.88e-5 |
| 0.4 | 0.5320 | 0.4511 | 2.98e-5 |

The grid velocity has $\max|D\mathbf{u}| < 10^{-12}$ after every step (at most $7.2 \times 10^{-13}$). These are measurements from the implementation on this page.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It checks the four kernel conditions by direct algebra: on $0 \le r < 1$ the four nonzero weights are $t$, $\tfrac12 - t$, $\tfrac{1 + 2r}{4} - t$ and $\tfrac{1 - 2r}{4} + t$ with $t = (1 + 2r - \sqrt{1 + 4r - 4r^2})/8$, which gives the even and odd sums and the first moment at once, and the sum of squares is $3/8$ because $t$ is a root of $4t^2 - (1 + 2r)t + r^2/2 = 0$. Spreading is the adjoint of interpolation, so the power $\sum\mathbf{f}\cdot\mathbf{u}\,h^2$ on the grid equals $\sum\mathbf{F}_l\cdot\mathbf{U}_l\,\Delta s$ at the points. The moment conditions show that spreading keeps the total force and the torque. The projection makes every grid velocity exactly divergence free. The pressure jump of the static circle and the stability of the explicit step are measured, not proved.

## Complexity

The force, spreading and interpolation cost $\Theta(P)$ per step, with 16 grid points per point and component. The momentum step costs $\Theta(M)$ and the Poisson solve costs $K$ conjugate gradient iterations of $\Theta(M)$ each. So one step costs $\Theta(MK + P)$ and $N$ steps cost $\Theta(N(MK + P))$, with $\Theta(M + P)$ memory. With an FFT Poisson solver on the periodic box the step costs $\Theta(M\log M + P)$. The explicit spring force makes the method stiff: the stable $\Delta t$ falls as $\kappa$ grows and as $h$ shrinks, and this often dominates $N$.

## Properties

- The grid is fixed and Cartesian; the structure can move and deform freely without remeshing.
- Spreading and interpolation are adjoint, so energy is exchanged between structure and fluid without a numerical source in the coupling.
- Total force and torque pass unchanged from the points to the grid.
- The grid velocity is exactly divergence free; the interpolated velocity at the points is not, so enclosed areas can drift slowly.
- The interface is smeared over about four cells, and the velocity is usually first order accurate near it.

## Variants and improvements

- **Other kernels.** Peskin's three-point and six-point kernels, and kernels built from B-splines, trade support width against smoothness and grid invariance.
- **Implicit and semi-implicit time stepping** removes the severe step limit of stiff structures, at the cost of a coupled solve.
- **Direct forcing and discrete forcing** methods compute the force that makes the velocity at the boundary equal a prescribed value, for rigid bodies; Mittal and Iaccarino (2005) survey these.
- **The immersed interface method** puts the jump conditions into the finite difference stencils instead of smoothing them, which gives second order accuracy.
- **Adaptive and finite element versions** refine the grid near the structure or describe the structure with finite elements.
- **Related front methods:** [front tracking](/front-tracking-method/) also carries Lagrangian points on a fixed grid for multiphase flow, and the [ghost fluid method](/ghost-fluid-method/) and [level set method](/level-set-method/) treat interfaces in an Eulerian way.

## When to use it

Use the immersed boundary method when an elastic or moving structure interacts strongly with a viscous incompressible fluid and fitting a grid to the structure is hard: heart valves, swimming organisms, red blood cells, flexible fibers, insect flight. It suits low and moderate Reynolds numbers and problems where the coupling matters more than the sharpness of the boundary layer. For a rigid body at high Reynolds number, where the boundary layer must be resolved accurately, body-fitted grids, cut cells or sharp-interface direct forcing are usually better.

## Pitfalls

- **Stiffness and the explicit time step.** On a $16 \times 16$ grid with $\nu = 0.1$ and $\kappa = 1$, $\Delta t = 0.005$ and $0.01$ run smoothly, $\Delta t = 0.02$ already shows growth (maximum velocity 0.86 after 10 steps instead of about 0.1), and $\Delta t = 0.04$ blows up. Stiffer springs need smaller steps.
- **Points too far apart.** If neighboring points are more than about $h$ apart, fluid leaks between them. A common rule of thumb is a spacing of about $h/2$, which this page uses.
- **Area and volume drift.** The interpolated velocity is not exactly divergence free, so a closed membrane can slowly lose or gain area; here the drift stayed near $3 \times 10^{-5}$ of the area, but it grows with time and coarse grids.
- **Smeared boundaries.** The force and the pressure jump are spread over about four cells. Quantities at the boundary, such as wall shear stress, are only first order accurate.
- **Stencils that cross the box.** Spreading and interpolation must wrap around periodic edges, or be cut at walls with care; the moment conditions hold only for the full stencil.

## Implementations

## History

Peskin (1972) introduced the method to compute blood flow around heart valves, with the valve leaflets as elastic fibers on a fixed grid. Over the next decades Peskin, McQueen and others developed it into a three-dimensional model of the heart, and Peskin's 2002 review in Acta Numerica set out the continuous equations, the conditions on the discrete delta function and the four-point kernel. Many related methods for rigid and elastic bodies on Cartesian grids followed under the same name, surveyed by Mittal and Iaccarino (2005).

## References
