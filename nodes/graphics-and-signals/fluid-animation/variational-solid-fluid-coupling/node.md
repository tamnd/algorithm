---
tag: T5ZPKE
kind: algorithm
slug: variational-solid-fluid-coupling
name: Variational solid-fluid coupling
aliases:
- variational pressure projection
area: graphics-and-signals/fluid-animation
level: advanced
summary: "Find the pressure that minimizes the kinetic energy of fluid and solids, with face weights for cells that a solid cuts. Walls need not follow the grid, and rigid bodies couple in one solve."
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of grid cells", k: "the number of conjugate gradient iterations", m: "the number of faces that the body covers"}
  time: {weights: "Θ(n)", matvec: "Θ(n + m)", project: "O((n + m) k)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, exact: false}
history:
  year: 2007
  people: [Christopher Batty, Florence Bertails, Robert Bridson]
  note: Batty, Bertails and Bridson wrote the pressure projection as a minimization of kinetic energy and used it for solids that do not follow the grid and for two-way rigid body coupling.
prereqs: [mac-grid, stable-fluids, conjugate-gradient-method, level-set-method]
see_also: [fluid-simulation-for-animation, foster-metaxas-fluids, chorin-projection-method, helmholtz-hodge-decomposition, rigid-body-simulation-problem, immersed-boundary-method, linear-complementarity-problem, quadratic-programming]
sources:
  - paper: doi:10.1145/1276377.1276502
    title: "Christopher Batty, Florence Bertails and Robert Bridson, A fast variational framework for accurate solid-fluid coupling, ACM Transactions on Graphics 26(3), article 100, 2007 (SIGGRAPH 2007)"
    locator: "section 2 (equations 1 to 3, the energy), section 2.1 (equations 4 to 7, the weights and the pressure system), section 3 (equations 8 to 13, rigid bodies; time integration and results), section 4 (equations 14 and 15, wall separation)"
  - paper: "Mark Carlson, Peter J. Mucha and Greg Turk, Rigid fluid: animating the interplay between rigid bodies and fluid, ACM Transactions on Graphics 23(3), 377-384, 2004 (SIGGRAPH 2004)"
    title: "Carlson, Mucha and Turk, Rigid fluid"
    locator: the earlier coupling that treats the body as fluid and then makes it rigid
---

Variational solid-fluid coupling, from Batty, Bertails and Bridson (2007), changes how the pressure step of a grid fluid sees solids. The usual "voxelized" solve marks each cell as solid or fluid, so a slanted or curved wall becomes a staircase. The variational method instead writes the pressure step as a minimization of kinetic energy. Each velocity sample on a [MAC grid](/mac-grid/) is weighted by the part of its face that is open to the fluid. The minimum is a sparse, symmetric positive semidefinite linear system that has the same shape as the usual one. So the same solver works, and walls at any angle need no special stencils. A rigid body adds its own kinetic energy to the sum. The fluid and the body then get their new velocities from one solve, with no iteration between two solvers.

## In plain words

The pressure step makes the water flow so that no cell gains or loses water. Among all the ways to do that, it picks the one with the least change of motion energy.

The new method counts the energy honestly in cells that a wall cuts. A cell face that is half in the wall counts half. So the water can slide along a sloped wall instead of hitting steps.

A floating box is part of the same count. Its mass and speed go into the energy, so the pressure that moves the water also pushes the box. Heavy boxes sink, light boxes rise, and a box as heavy as water stays still.

## The problem

The input is a velocity field $\mathbf u^*$ after advection and forces, the walls, and the rigid bodies with their velocities $V^*$ (here $V = (v_x, v_y, \omega)$ in 2D). Find a pressure $p$ such that the new fluid velocity $\mathbf u = \mathbf u^* - (\Delta t / \rho) \nabla p$ has zero divergence, the fluid neither enters nor leaves a solid, and each body gets the force and torque of the pressure on its surface. On the boundary this is $\mathbf u \cdot \hat n = \mathbf v_{solid} \cdot \hat n$, which is hard to discretize where the wall cuts a cell.

**The energy.** The paper's equation 3 is the kinetic energy of fluid and solids,

$$\mathrm{KE} = \iiint_{\text{fluid}} \tfrac12 \rho |\mathbf u|^2 + \tfrac12 V^\mathsf{T} M_S V,$$

and the pressure equation with its boundary condition is the condition for the minimum over $p$. So we can discretize the energy, which is easy, and get the boundary condition for free.

## The algorithm

On a MAC grid, each face $f$ has a fluid weight $w_f$: the part of the face outside every solid (the paper's figure 3 uses the part of the control volume of the face; it names the face area as a simpler estimate, which the code uses). Let $b_f$ be the part inside the body. $(G p)_f$ is the pressure difference across $f$ divided by $\Delta x$, $G^\mathsf{T}$ is minus the divergence, and $R_f V$ is the normal component of the rigid velocity at $f$. The discrete energy is $\tfrac12 \rho \Delta x^2 \sum_f w_f u_f^2 + \tfrac12 V^\mathsf{T} M V$, with $M = \rho_s \Delta x^2 R^\mathsf{T} B R$.

```pseudo id=main
VARIATIONAL-PROJECT(u*, V*, walls, body, Δt)
L1  for each face f: s_f and b_f <- the parts of f in the walls and in the body; w_f <- 1 - s_f - b_f
L2  the unknowns are the cells that are not AIR or SOLID and have a face with w_f > 0
L3  r <- Gᵀ (W u* + B R V*)
L4  A <- (Δt/ρ) Gᵀ W G + (Δt/ρ_s) Gᵀ B R (Rᵀ B R)⁻¹ Rᵀ B G
L5  solve A p = r by conjugate gradients, with p = 0 in AIR cells
L6  u_f <- u*_f - (Δt/ρ) (G p)_f on every face with w_f > 0
L7  V <- V* - (Δt/ρ_s) (Rᵀ B R)⁻¹ Rᵀ B G p
```

**Weights (L1).** With a level set for each solid, the part of a face inside the solid comes from the values at the two ends of the face, by linear interpolation. The paper lists three estimates of the fluid mass of a velocity sample: the exact fluid volume of its control volume, $\Delta x$ times the fluid area of its face (which gives a method related to finite volumes), and $\Delta x^2$ times the fluid part of the segment between the two pressure samples. The voxelized solve is the case where every weight is 0 or 1.

**Pressure (L3 to L5).** Without a body, setting the derivative of the energy to zero gives the paper's equation 6, $(\Delta t / \rho^2) G^\mathsf{T} M_F G p = (1 / \rho) G^\mathsf{T} M_F \tilde{\mathbf u}$, with the fluid masses $M_F$. In 2D, its equation 7 is a 5-point stencil whose coefficients are the face weights. The right side is minus the divergence of the mixed velocity $W \mathbf u^* + B R V^*$. The body adds $\Delta t\, J^\mathsf{T} M_S^{-1} J$ to the matrix, where $J$ maps the pressure to the net force and torque on the body (its equations 8 to 12, written as volume integrals of $\nabla p$). This term has rank 3 in 2D and rank 6 in 3D, and the code applies it without forming it.

**Scripted solids.** A solid whose motion is given has an infinite mass. Then $M_S^{-1} = 0$: the term leaves the matrix, and only its velocity stays on the right side.

**Cells inside the body.** A cell whose four faces are all inside the body has a zero column in $J$, because the contributions of opposite faces cancel. Its pressure does not matter, and the code leaves it out.

## Example

**A face cut by a wall.** Let the wall level set be $-1$ at one end of a face and $3$ at the other. The wall crosses the face at a quarter of its length, so $s_f = 0.25$ and $w_f = 0.75$. In the energy, the velocity sample counts with three quarters of the mass of a full face; in the 5-point stencil, the coefficient of this neighbor is 0.75 instead of 1.

**Still water in a round bowl.** On a 24 by 24 grid of the unit square, take water inside a circle of radius 0.46 up to the height 0.75, gravity $g = 9.81$ m/s² and $\Delta t = 0.01$ s. After gravity and one projection, every face velocity is below $10^{-13}$ m/s, and the pressure equals $\rho g$ times the depth to $10^{-9}$ Pa. Conjugate gradients take 94 iterations on 344 unknowns. This holds for any shape of the container (Theorem 3 of the proof).

**Flow along a tilted channel.** A straight channel of width 0.24 crosses a 24 by 16 grid at 10 or 20 degrees, open at both ends. A uniform flow of speed 1 along the channel is already divergence free and tangent to the walls, so the projection should not change it. The variational solve keeps it to $10^{-15}$. The voxelized solve of [`macgrid`](/mac-grid/) changes it:

| angle | variational flux | voxelized flux |
|---|---|---|
| 10° | 0.2400 | 0.2239 |
| 20° | 0.2400 | 0.2186 |

The paper's figure 2 shows the same effect on a vortex in a rotated box.

**A sinking and a rising disk.** Put a disk of radius 0.1 at $(0.5, 0.45)$ in the bowl, and take one step from rest. A cylinder in unbounded still fluid starts with the acceleration $g (\rho_s - \rho) / (\rho_s + \rho)$: the fluid that must move with it acts as an added mass equal to the fluid it displaces. The coupled solve finds this added mass without a model for it:

| $\rho_s / \rho$ | measured $a / g$ | unbounded fluid |
|---|---|---|
| 2 | -0.3316 | -0.3333 |
| 1 | 0 (to $10^{-15}$) | 0 |
| 0.5 | 0.3299 | 0.3333 |
| 0.1 | 0.8066 | 0.8182 |

The walls of the bowl add a little to the added mass, so the measured values are slightly smaller. The light disk with $\rho_s = 0.1 \rho$ is stable; the paper notes that the method of Carlson et al. (2004) cannot handle bodies lighter than about 0.45 times the fluid density.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **Lines L3 to L5 minimize the energy.** The gradient of the discrete energy is zero exactly when $A p = r$, and then the mixed velocity of fluid and body has zero divergence in every unknown cell.
2. **The matrix.** $A$ is symmetric positive semidefinite. Constant vectors are in its null space when no AIR cell is present; with an AIR cell next to each group of fluid cells, $A$ is positive definite. So the system is not positive definite in every case; the paper calls it "symmetric positive semi-definite".
3. **No energy is added.** The projection never increases the kinetic energy of fluid and body.
4. **Hydrostatic rest.** Still water in a container of any shape stays still, with $p = \rho g$ times the depth, and a body with the density of the fluid stays at rest if its mass matrix comes from the same face weights.
5. **Binary weights.** With weights 0 and 1 from the cell labels, the method is the usual voxelized solve.
6. **Straight walls.** A uniform flow along straight walls is kept exactly.

The method is a discretization. The face area estimate of the mass is exact for the flux through straight walls (item 6) and only approximates a curved wall. The paper calls its results accurate on coarse grids, which means without the stair-step artifacts, not a proved order of convergence.

## Complexity

Let $n$ be the number of cells and $m$ the number of faces that the body covers. The weights cost $\Theta(n)$ level set evaluations. One product with $A$ costs $\Theta(n)$ for the fluid part and $\Theta(m)$ for the body part, since $J$ is a sum over the covered faces followed by a 3 by 3 solve. With $k$ iterations of conjugate gradients, the projection costs $O((n + m) k)$; the paper uses a modified incomplete Cholesky preconditioner, which applies because the fluid part is still a symmetric M-matrix. The paper notes that its general sparse storage of the body term is wasteful and that its low rank could be used. The space is $\Theta(n)$.

## Properties

- **Same stencil.** The fluid part is the 5-point (7-point in 3D) stencil with face weights, so existing solvers and preconditioners work.
- **Sub-grid detail.** A gap narrower than a cell still has weights above zero, so fluid can flow through it; the paper shows a box that nearly blocks a channel, with gaps of half a cell.
- **One solve for two-way coupling.** Fluid and body velocities come out of one linear system. There is no iteration between a fluid solver and a body solver.
- **Not conservative of energy.** The projection removes the part of the energy that violates the constraint; it never adds energy.

## Variants and improvements

- **Wall separation.** The paper's section 4 replaces $\mathbf u \cdot \hat n = \mathbf v_{solid} \cdot \hat n$ with $\mathbf u \cdot \hat n \ge \mathbf v_{solid} \cdot \hat n$ and $p \ge 0$ on the walls (its equation 15). The minimization becomes a [quadratic program](/quadratic-programming/), and fluid can leave a ceiling or a wall instead of sticking. The paper solves the equivalent [linear complementarity problem](/linear-complementarity-problem/) with the PATH solver, on small problems.
- **Free surface.** The paper uses the ghost fluid boundary condition of Gibou et al. (2002) for $p = 0$ at a free surface. The code here sets $p = 0$ at the centers of AIR cells.
- **Deformable solids.** Any solid whose kinetic energy is a quadratic form in its velocities fits the framework; the paper does rigid bodies and expects deformable ones to follow.
- **Thin solids.** A shell has no interior that the grid samples, so the method as written does not apply to it. The paper suggests ghost pressures on the two sides as future work.

## When to use it

Use it when solids do not follow the grid: curved containers, rotated boxes, moving paddles and floating bodies on a coarse grid. Use it for two-way rigid body coupling where the bodies can be much lighter or heavier than the fluid. If every wall follows the grid, the voxelized solve gives the same result (Theorem 4 of the proof).

## Pitfalls

- **A closed container.** Without AIR, the matrix is singular. The right side is compatible only if the solids do not change the volume of the fluid; a scripted piston that pushes into a closed box makes the system inconsistent, and the paper then removes the null space part of the right side.
- **Inconsistent masses.** The body's mass matrix must come from the same volumes as $J$. Otherwise a body with the density of the fluid drifts; the paper notes that this matters most for hydrostatic rest.
- **Faces with zero weight.** A face with $w_f = 0$ has no fluid velocity. For advection, extrapolate the tangential velocity into the solid, as the paper does.
- **Tiny weights.** A cell whose faces all have weights near zero has a small diagonal entry, which makes the matrix worse conditioned and slows the solver.
- **Thin bodies.** A body thinner than a cell has no interior cells, and pressure leaks across it.

## Implementations

## History

Foster and Metaxas (1996) brought the MAC grid to graphics with voxelized solids. Foster and Fedkiw (2001) let the fluid slip along walls by setting the velocity after the solve, and Houston et al. (2003) and Rasmussen et al. (2004) extended this. These methods still used the voxelized solve with its stair-step artifacts, and the paper notes that they fail for still water in a container with oblique walls. For coupling, Takahashi et al. (2002) and Guendelman et al. (2005) alternated between fluid and body solves; Carlson et al. (2004) treated bodies as fluid and then made them rigid; Klingner et al. (2006) and Chentanez et al. (2006) coupled fluids with solids on tetrahedral meshes. In 2007, Batty, Bertails and Bridson wrote the pressure solve as a kinetic energy minimization on a regular grid. They reported a paddle in smoke on an $80 \times 40 \times 60$ grid at 3 seconds per frame, about 20 times faster than the tetrahedral mesh method of Klingner et al. on a comparable example.

## References
