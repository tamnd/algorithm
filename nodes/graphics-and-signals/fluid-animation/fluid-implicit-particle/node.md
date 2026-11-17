---
tag: QNPJRR
kind: algorithm
slug: fluid-implicit-particle
name: Fluid-implicit-particle method
aliases:
- FLIP
area: graphics-and-signals/fluid-animation
level: core
summary: Like particle-in-cell, but add only the change of the grid velocity to each particle, which reduces the dissipation of PIC and adds noise.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of particles", c: "the number of grid cells", k: "the number of conjugate gradient iterations of the projection"}
  time: {transfers: "O(n + c)", step: "O(n + k c)"}
  space: {extra: "O(n + c)"}
properties: {deterministic: true, exact: false, conserves_linear_momentum: true, conserves_angular_momentum: false, dissipative: false}
history:
  year: 1986
  people: [Jeremiah U. Brackbill, Hans M. Ruppel, Yongning Zhu, Robert Bridson]
  note: Brackbill and Ruppel introduced FLIP in 1986 for fluid flows in two dimensions; Zhu and Bridson brought it to the animation of liquids and sand in 2005.
prereqs: [particle-in-cell, mac-grid]
see_also: [affine-particle-in-cell, material-point-method, stable-fluids, particle-level-set, particle-fluid-surfacing, smoothed-particle-hydrodynamics, fluid-simulation-for-animation]
sources:
  - paper: doi:10.1016/0021-9991(86)90211-1
    title: J. U. Brackbill and H. M. Ruppel, FLIP. A method for adaptively zoned, particle-in-cell calculations of fluid flows in two dimensions, Journal of Computational Physics 65(2), 314-343, 1986
    locator: the whole paper (the update of the particle velocity by the change of the grid velocity)
  - paper: doi:10.1145/1073204.1073298
    title: Yongning Zhu and Robert Bridson, Animating sand as a fluid, ACM Transactions on Graphics 24(3), 965-972, 2005
    locator: the section on PIC and FLIP
  - book: "Robert Bridson, Fluid Simulation for Computer Graphics, 2nd edition, CRC Press, 2015"
    title: Fluid Simulation for Computer Graphics
    locator: the chapter on particle methods
---

The fluid-implicit-particle method (FLIP) is the [particle-in-cell](/particle-in-cell/) method with a different grid to particle transfer.
A PIC particle takes the new grid velocity, which is an average and loses energy.
A FLIP particle keeps its own velocity and adds only the change of the grid velocity over the step.
So small swirls that the grid cannot hold stay on the particles, and the dissipation is much smaller.
The cost is noise: the particle velocities drift away from the smooth grid field, because nothing pulls them back.
In practice the update is a blend of FLIP and a small part of PIC.

## In plain words

The water is a cloud of particles over a grid of boxes, as in PIC.
The particles give their speeds to the grid, and the grid adds gravity and makes sure that the water does not squeeze.
In PIC, each particle then forgets its speed and takes the average speed of the grid near it.
In FLIP, each particle keeps its speed and adds only what the grid changed.
So a particle does not lose its small motions in each step, and swirls last much longer.
But the particles can now get speeds that differ a little from their neighbors, which shows as noise.
A small part of PIC in the mix calms the noise.

## The problem

The input and the output are those of [PIC](/particle-in-cell/): $n$ particles with masses $m_p$, positions $x_p$ and velocities $(u_p, v_p)$, a [MAC grid](/mac-grid/) of cells of size $\Delta x$ with fixed walls, the density $\rho$, gravity $g = -9.81$ m/s² on the $y$ axis, the step $\Delta t$, and the blend weight $\alpha \in [0, 1]$.
This is one method for [fluid simulation for animation](/fluid-simulation-for-animation/).
The weights $w_{fp}$ are the bilinear weights of PIC.

## The algorithm

```pseudo id=main
FLIP-STEP(x, u, v, Δt, α)
L1  for each cell: FLUID if it holds a particle, else AIR (walls stay SOLID)
L2  for each face f: m_f ← Σₚ w_fp mₚ; u_f ← Σₚ w_fp mₚ uₚ / m_f (0 if m_f = 0), the same for v
L3  u_old ← u, v_old ← v (the grid velocity of line L2)
L4  for each v face f with m_f > 0: v_f ← v_f + Δt g
L5  project the grid velocity (pressure solve on the FLUID cells)
L6  for each particle p: uₚ ← α (uₚ + Σ_f w_fp (u_f - u_old,f)) + (1 - α) Σ_f w_fp u_f, the same for v
L7  for each particle p: move xₚ through the grid velocity for Δt, keep it Δx/2 from the walls
```

Lines L1, L2, L4, L5 and L7 are the lines of PIC.
Line L3 saves the grid velocity right after the transfer, before the forces and the projection.
Line L6 is the only real change.
Its first term is the FLIP update: the old particle velocity plus the change of the grid velocity, interpolated to the particle.
Its second term is the PIC update.
With $\alpha = 1$ the update is pure FLIP, and with $\alpha = 0$ it is PIC.
The code uses $\alpha = 0.95$; values from 0.95 to 0.99 are common in graphics, and the value is a tuning choice.

## Example

Take an 8 by 8 grid of unit size, all filled with liquid (four particles per cell, unit masses), with no gravity.
The start velocity is the swirl $u = \sin(\pi x)\cos(\pi y)$, $v = -\cos(\pi x)\sin(\pi y)$, which has no divergence and no flow through the walls.
In an ideal liquid its kinetic energy would stay constant.
Run steps of 0.02 s.
The table gives the particle kinetic energy as a fraction of the start value (measured).

| steps | PIC ($\alpha = 0$) | blend ($\alpha = 0.95$) | FLIP ($\alpha = 1$) |
|---|---|---|---|
| 1 | 0.8916 | 0.9871 | 0.9924 |
| 5 | 0.5732 | 0.9470 | 0.9781 |
| 10 | 0.3378 | 0.9029 | 0.9676 |
| 20 | 0.1203 | 0.8267 | 0.9544 |
| 40 | 0.0152 | 0.7455 | 0.9521 |

PIC loses almost all of the swirl in 40 steps on this coarse grid.
FLIP keeps 95% of the energy.
The noise goes the other way: after 40 steps, the root mean square difference between the particle velocity and the grid velocity at the particle is 0.0005 m/s with PIC, 0.069 m/s with the blend and 0.159 m/s with FLIP, for a start speed of up to 1 m/s.

## Correctness

FLIP is an approximation of the Euler equations of a liquid, and its error is not bounded here.
The tests check these facts, and the [proof](proofs/correctness.md) gives the arguments:

- **No change, no update.** With $\alpha = 1$, if the grid velocity does not change between lines L3 and L6, line L6 leaves every particle velocity exactly as it was.
- **The PIC end.** With $\alpha = 0$, line L6 is the PIC transfer.
- **Linear momentum.** For every $\alpha$, the particle momentum after line L6 equals the grid momentum after line L5, with the face masses of line L2.
- **Energy.** FLIP has no energy bound like the one of PIC; with $\alpha = 1$ a transfer can add energy. The energy table above is a measurement.

The tests also run a small dam break and check that the divergence stays near 0 and that the particles stay in the box.

## Complexity

The cost is the cost of PIC, $O(n + c)$ for the transfers and $O(k c)$ for the projection, plus one copy of the grid velocity in line L3.
The memory is $O(n + c)$.

## Properties

- **Low dissipation.** FLIP does not average the particle velocities in each step, so it keeps much more energy than PIC (measured in the example).
- **Noise.** The particle velocities are not tied to the grid field, so they drift apart and the liquid looks noisy. The noise grows with $\alpha$ (measured).
- **Linear momentum.** The transfers keep it for every $\alpha$ (proved).
- **Angular momentum.** Line L6 does not keep it in general.
- **The null space.** The grid has about 2 velocity values per cell and the particles have 8 per cell. Particle velocity fields that give the same grid field are not seen by the grid, and FLIP never damps them. This is one source of the noise.

## Variants and improvements

- **PIC and FLIP blend.** The weight $\alpha$ of line L6 trades noise for dissipation.
- **APIC.** [APIC](/affine-particle-in-cell/) gives low dissipation with the stability of PIC, by a velocity gradient on each particle in place of the FLIP update.
- **Adaptive blends.** Some solvers make $\alpha$ depend on the position, for example less FLIP near the walls and the free surface.
- **MPM.** The [material point method](/material-point-method/) often uses a FLIP or APIC transfer for solids and sand.
- **Surfacing.** FLIP liquids need a surface for rendering; see [surface reconstruction from fluid particles](/particle-fluid-surfacing/).

## When to use it

Use FLIP, with a small part of PIC, for splashing liquids where swirls and thin sheets should last.
Use [PIC](/particle-in-cell/) for very viscous liquids and sand, where the dissipation does no harm.
If the noise is a problem, use [APIC](/affine-particle-in-cell/).

## Pitfalls

- **The wrong old velocity.** Line L3 must save the grid velocity after the transfer of line L2 and before line L4. Saving it after line L4 loses gravity in the FLIP term, and saving it before line L2 adds the whole velocity again.
- **Moved particles in line L6.** Line L6 must use the positions of line L2. A particle that moved before line L6 can read a face with no mass, which is 0 in the copy of line L3 and nonzero after line L5, and the FLIP term gets a false jump.
- **Pure FLIP.** With $\alpha = 1$ in line L6 the noise grows and can make the liquid unstable. Keep a small part of PIC.
- **A different velocity in line L7.** Line L7 moves the particles in the grid velocity. Moving them with the noisy particle velocity of line L6 puts the noise into the positions too.

## Implementations

## History

Brackbill and Ruppel (1986) introduced FLIP to remove the large numerical dissipation of the particle-in-cell method of Harlow.
Their particles carry all of the state, and the grid is only a work space for the update of each step.
Zhu and Bridson (2005) brought PIC and FLIP to computer graphics, with a MAC grid and a pressure projection.
Blends of FLIP with a small part of PIC are now widely used for liquids in visual effects.
Jiang, Schroeder, Selle, Teran and Stomakhin (2015) proposed [APIC](/affine-particle-in-cell/) as a stable alternative with low dissipation.

## References
