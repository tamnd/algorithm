---
tag: N6Z3N3
kind: algorithm
slug: particle-in-cell
name: Particle-in-cell method
aliases:
- PIC method
area: graphics-and-signals/fluid-animation
level: core
summary: Carry velocity on particles, transfer it to a grid for forces and pressure projection, and interpolate the grid velocity back to the particles.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of particles", c: "the number of grid cells", k: "the number of conjugate gradient iterations of the projection"}
  time: {transfers: "O(n + c)", step: "O(n + k c)"}
  space: {extra: "O(n + c)"}
properties: {deterministic: true, exact: false, conserves_linear_momentum: true, conserves_angular_momentum: false, dissipative: true}
history:
  year: 1964
  people: [Francis H. Harlow, Yongning Zhu, Robert Bridson]
  note: Harlow developed PIC at Los Alamos in the 1950s and early 1960s; Zhu and Bridson brought PIC and FLIP to the animation of liquids and sand in 2005.
prereqs: [mac-grid, bilinear-interpolation]
see_also: [fluid-implicit-particle, affine-particle-in-cell, stable-fluids, material-point-method, plasma-particle-in-cell, marker-and-cell-method, particle-fluid-surfacing, fluid-simulation-for-animation]
sources:
  - paper: doi:10.1090/psapm/015/9942
    title: Francis H. Harlow, The particle-in-cell method for numerical solution of problems in fluid dynamics, Proceedings of Symposia in Applied Mathematics 15, 269-288, 1963
    locator: the whole paper
  - book: "Francis H. Harlow, The particle-in-cell computing method for fluid dynamics, Methods in Computational Physics 3, Academic Press, 1964"
    title: The particle-in-cell computing method for fluid dynamics
    locator: the whole chapter
  - paper: doi:10.1145/1073204.1073298
    title: Yongning Zhu and Robert Bridson, Animating sand as a fluid, ACM Transactions on Graphics 24(3), 965-972, 2005
    locator: the section on PIC and FLIP for liquids (the transfers and the particle labels of the cells)
  - book: "Robert Bridson, Fluid Simulation for Computer Graphics, 2nd edition, CRC Press, 2015"
    title: Fluid Simulation for Computer Graphics
    locator: the chapter on particle methods
---

The particle-in-cell method (PIC) simulates a liquid with particles and a grid together.
The particles carry the positions and the velocities, so the liquid moves without the smoothing of a grid advection.
The grid is a [MAC grid](/mac-grid/), where gravity and the pressure projection are simple.
In each step the particle velocities go to the grid, the grid velocity is made divergence free, and the new grid velocity comes back to the particles.
Each transfer is an average, so PIC loses kinetic energy in each step, and fast swirls slow down.
[FLIP](/fluid-implicit-particle/) and [APIC](/affine-particle-in-cell/) change the transfers to lose less.

## In plain words

The water is a cloud of small particles, and each particle knows its speed.
A grid of boxes covers the water.
In each step, each edge of the grid takes an average of the speeds of the near particles.
On the grid it is easy to add gravity and to make sure that no box takes in more water than it lets out.
Then each particle gets a new speed, which is an average of the near grid edges.
At last the particles move with the grid flow.
The two averages smooth the speeds, so a swirl in the water slowly stops, even when nothing in the water should stop it.

## The problem

The input is a set of $n$ particles with masses $m_p$, positions $x_p$ and velocities $(u_p, v_p)$, a MAC grid of $n_x$ by $n_y$ cells of size $\Delta x$ with fixed walls, the density $\rho$, gravity $g = -9.81$ m/s² on the $y$ axis and the step $\Delta t$.
The output is the state after one step.
This is one method for [fluid simulation for animation](/fluid-simulation-for-animation/).
On the MAC grid, $u$ is stored at the centers of the vertical faces and $v$ at the centers of the horizontal faces.
The weight $w_{fp}$ of face $f$ at particle $p$ is the [bilinear](/bilinear-interpolation/) weight of the four nearest samples of the same component, so $w_{fp} \ge 0$ and $\sum_f w_{fp} = 1$.

## The algorithm

```pseudo id=main
PIC-STEP(x, u, v, Δt)
L1  for each cell: FLUID if it holds a particle, else AIR (walls stay SOLID)
L2  for each face f: m_f ← Σₚ w_fp mₚ; u_f ← Σₚ w_fp mₚ uₚ / m_f (0 if m_f = 0), the same for v
L3  for each v face f with m_f > 0: v_f ← v_f + Δt g
L4  project the grid velocity (pressure solve on the FLUID cells)
L5  for each particle p: uₚ ← Σ_f w_fp u_f, vₚ ← Σ_f w_fp v_f
L6  for each particle p: move xₚ through the grid velocity for Δt, keep it Δx/2 from the walls
```

Line L1 marks the liquid: a cell with at least one particle is FLUID, and the pressure is 0 in the AIR cells.
Line L2 is the particle to grid transfer (P2G), a mass-weighted average of the particle velocities near each face.
Line L3 adds gravity on the faces that carry liquid.
Line L4 is the projection of the MAC grid page: a conjugate gradient solve for the pressure, then the pressure gradient is subtracted, so the discrete divergence of every FLUID cell is 0.
Line L5 is the grid to particle transfer (G2P), with the same weights as line L2.
Line L6 moves each particle with a midpoint (RK2) step in the projected grid velocity.
The clamp to half a cell from the walls keeps the bilinear weights unclamped, which matters for the angular momentum claim below.
The code puts four particles in each cell at the start, with a small random shift.

## Example

Take an 8 by 8 grid with $\Delta x = 1/8$ m, 256 particles at random positions at least half a cell from the walls, unit masses, and the rigid rotation $u = -(y - 1/2)$, $v = x - 1/2$ in 1/s.
Do lines L2 and L5 only, with no gravity and no projection, again and again at the same positions.
The rigid rotation is a linear field, so an exact method would keep it.
The table gives the kinetic energy and the angular momentum as fractions of their start values.

| round trips | grid energy after L2 | particle energy after L5 | particle angular momentum after L5 |
|---|---|---|---|
| 1 | 0.9657 | 0.9340 | 0.9647 |
| 2 | 0.9042 | 0.8758 | 0.9321 |
| 5 | 0.7503 | 0.7279 | 0.8444 |
| 10 | 0.5560 | 0.5397 | 0.7201 |

Each transfer is an average, so each one loses energy, and after 10 round trips almost half of the energy is gone.
Line L2 keeps the angular momentum exactly (the grid value after line L2 equals the particle value before it), and line L5 loses it.
A uniform flow, in contrast, goes through both transfers with no change.

## Correctness

PIC is an approximation of the Euler equations of a liquid, and its error is not bounded here.
The tests check these facts, and the [proof](proofs/correctness.md) gives the arguments:

- **The weights.** Each weight is at least 0 and the four weights of a particle add up to 1, so line L5 is the bilinear sample of the MAC grid page.
- **Linear momentum.** Lines L2 and L5 keep $\sum m u$ and $\sum m v$, also near the walls.
- **Energy.** Line L2 does not increase the kinetic energy, and line L5 does not increase it either. The loss is strict unless the velocities near each face are equal.
- **Angular momentum.** If no particle is closer than $\Delta x/2$ to a wall, line L2 keeps the angular momentum exactly. Line L5 does not keep it in general.
- **Constant flows.** A uniform velocity goes through lines L2 and L5 unchanged.
- **Projection.** After line L4, the discrete divergence of the FLUID cells is 0, to the tolerance of the solver.

The tests also run a small dam break and check that the divergence stays near 0 and that the particles stay in the box.

## Complexity

Lines L1, L2, L3, L5 and L6 cost $O(n + c)$ time for $n$ particles and $c$ cells, because each particle touches four faces of each component.
Line L4 costs $O(k c)$ for $k$ conjugate gradient iterations, and $k$ grows with the size of the grid.
The memory is $O(n + c)$.
In the dam break of the tests, a 12 by 12 grid with 96 particles takes 60 steps of 5 ms in about 0.1 s of Python time (a measurement).

## Properties

- **Dissipation.** Each transfer is an average and loses energy (proved for the transfers). The loss acts like a viscosity that depends on the grid size, and it damps small swirls.
- **Linear momentum.** The transfers keep it (proved).
- **Angular momentum.** P2G keeps it under the hypothesis above, and G2P loses it (proved for P2G, shown by the example for G2P).
- **Stability.** The new particle velocities are averages of the grid values, so PIC is stable for steps where FLIP is noisy.
- **No mass loss in advection.** The particles carry the liquid, so the volume does not leak away as in a level set advected on a grid. The particle density can still drift.

## Variants and improvements

- **FLIP.** [FLIP](/fluid-implicit-particle/) adds the change of the grid velocity to the particle velocity, which removes most of the dissipation and adds noise. A blend of PIC and FLIP is common.
- **APIC.** [APIC](/affine-particle-in-cell/) stores a velocity gradient on each particle and makes line L5 keep the angular momentum and linear fields.
- **Wider kernels.** Quadratic or cubic B-spline weights in place of bilinear ones give smoother transfers at a higher cost.
- **Velocity extrapolation.** Copying the velocity of the liquid faces into the near AIR faces after line L4 gives better values to line L6 at the free surface.
- **MPM.** The [material point method](/material-point-method/) uses the same transfers for solids and also carries a deformation on each particle.
- **Plasma PIC.** In plasma physics, [particle-in-cell](/plasma-particle-in-cell/) moves charged particles in electric and magnetic fields that are solved on a grid. The transfers are of the same kind, but the forces are different.

## When to use it

Use PIC as the base of a particle and grid liquid, or when stability matters more than detail, for example for sand, mud or very viscous liquids.
For splashing water, blend it with [FLIP](/fluid-implicit-particle/) or use [APIC](/affine-particle-in-cell/).
For smoke on a fixed grid, [stable fluids](/stable-fluids/) is simpler.

## Pitfalls

- **Holes in the liquid.** Line L1 makes each empty cell AIR. With too few particles per cell, cells inside the liquid become AIR and get the pressure 0. Use about four particles per cell in 2D.
- **Division by the face mass.** Line L2 must divide by the sum of the mass weights, not by the number of particles. A face with no mass gets no velocity and must not be used as liquid.
- **Gravity on empty faces.** Line L3 changes only the faces with mass. Gravity on all faces gives a falling velocity in the air, which line L6 then reads at the surface.
- **Different weights.** Line L5 must use the same weights as line L2. With different weights the momentum and energy claims fail.
- **The free surface in line L6.** The midpoint of line L6 can read a face with no mass, which has the velocity 0 and slows the surface. Extrapolate the velocity, or use the velocity of line L5 for the move.
- **Particles at the walls.** Without the clamp of line L6, particles leave the box or sit on the wall, where the weights clamp and the angular momentum claim fails.

## Implementations

## History

Harlow and his group at Los Alamos developed the particle-in-cell method in the 1950s and early 1960s, for compressible flows with large deformations, and described it in papers of 1963 and 1964.
Brackbill and Ruppel (1986) made FLIP, which keeps the full velocity on the particles.
Zhu and Bridson (2005) brought PIC and FLIP to computer graphics, with a MAC grid and a pressure projection, for liquids and sand.
Jiang, Schroeder, Selle, Teran and Stomakhin (2015) added APIC.

## References
