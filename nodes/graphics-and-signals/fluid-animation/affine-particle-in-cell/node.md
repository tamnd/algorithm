---
tag: AJQ8H2
kind: algorithm
slug: affine-particle-in-cell
name: Affine particle-in-cell
aliases:
- APIC
area: graphics-and-signals/fluid-animation
level: research
summary: Store an affine velocity matrix on each particle; under the hypotheses of the paper, the particle to grid and grid to particle transfers then conserve angular momentum.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of particles", c: "the number of grid cells", k: "the number of conjugate gradient iterations of the projection"}
  time: {transfers: "O(n + c)", step: "O(n + k c)"}
  space: {extra: "O(n + c)"}
properties: {deterministic: true, exact: false, conserves_linear_momentum: true, conserves_angular_momentum: true, keeps_affine_fields: true}
history:
  year: 2015
  people: [Chenfanfu Jiang, Craig Schroeder, Andrew Selle, Joseph Teran, Alexey Stomakhin]
  note: Jiang, Schroeder, Selle, Teran and Stomakhin presented APIC at SIGGRAPH 2015; Jiang, Schroeder and Teran gave the MAC grid version and the analysis in 2017.
prereqs: [particle-in-cell, mac-grid]
see_also: [fluid-implicit-particle, material-point-method, stable-fluids, bilinear-interpolation, particle-fluid-surfacing, fluid-simulation-for-animation]
sources:
  - paper: doi:10.1145/2766996
    title: Chenfanfu Jiang, Craig Schroeder, Andrew Selle, Joseph Teran and Alexey Stomakhin, The affine particle-in-cell method, ACM Transactions on Graphics 34(4), 2015
    locator: the transfers, the matrix D_p for the interpolation kernels and the conservation of angular momentum
  - paper: doi:10.1016/j.jcp.2017.02.050
    title: Chenfanfu Jiang, Craig Schroeder and Joseph Teran, An angular momentum conserving affine-particle-in-cell method, Journal of Computational Physics 338, 137-164, 2017
    locator: the whole paper (the analysis and the MAC grid transfers)
  - paper: doi:10.1145/1073204.1073298
    title: Yongning Zhu and Robert Bridson, Animating sand as a fluid, ACM Transactions on Graphics 24(3), 965-972, 2005
    locator: the section on PIC and FLIP (the base method)
---

The affine particle-in-cell method (APIC) is the [particle-in-cell](/particle-in-cell/) method with a richer particle.
Each particle carries its velocity and also the gradient of the velocity near it, so it carries a small affine velocity field.
The particle to grid transfer (P2G) spreads this affine field to the grid, and the grid to particle transfer (G2P) reads back both the velocity and the gradient.
So a linear flow, such as a rigid rotation, goes through both transfers with no loss, and the angular momentum is kept exactly.
APIC loses much less energy than PIC, and it has much less noise than [FLIP](/fluid-implicit-particle/).

## In plain words

The water is a cloud of particles over a grid of boxes, as in PIC.
In PIC, each particle only knows its own speed, so when the grid averages the speeds, a turning motion is smoothed away.
In APIC, each particle also knows how the speed changes around it: faster to the left, slower above, and so on.
When it gives its speed to the grid, each grid edge gets the speed that the particle expects at that edge, not only the speed at the particle.
When it reads back, the particle learns both the speed and how the speed changes.
So a turning motion goes to the grid and back with no loss.

## The problem

The input and the output are those of [PIC](/particle-in-cell/), with two more vectors on each particle: $c^u_p$, the gradient of the $x$ velocity, and $c^v_p$, the gradient of the $y$ velocity.
Together they are the rows of the affine matrix $C_p$ of the paper.
The grid is a [MAC grid](/mac-grid/) of cells of size $\Delta x$ with fixed walls, $\rho$ is the density, gravity is $g = -9.81$ m/s² on the $y$ axis and $\Delta t$ is the step.
This is one method for [fluid simulation for animation](/fluid-simulation-for-animation/).
The weight $w_{fp}$ is the [bilinear](/bilinear-interpolation/) weight of face $f$ at particle $p$, $\nabla w_{fp}$ is its gradient with respect to the particle position, and $x_f$ is the center of face $f$.

## The algorithm

```pseudo id=main
APIC-STEP(x, u, v, cᵘ, cᵛ, Δt)
L1  for each cell: FLUID if it holds a particle, else AIR (walls stay SOLID)
L2  for each u face f: m_f ← Σₚ w_fp mₚ; u_f ← Σₚ w_fp mₚ (uₚ + cᵘₚ·(x_f - xₚ)) / m_f, the same for v with cᵛ
L3  for each v face f with m_f > 0: v_f ← v_f + Δt g
L4  project the grid velocity (pressure solve on the FLUID cells)
L5  for each particle p: uₚ ← Σ_f w_fp u_f, cᵘₚ ← Σ_f u_f ∇w_fp, the same for v
L6  for each particle p: move xₚ through the grid velocity for Δt, keep it Δx/2 from the walls
```

Line L2 is the APIC P2G: each particle gives each face the value of its affine field at the face center.
With $c = 0$ it is the PIC transfer.
Line L5 is the APIC G2P.
The paper writes the gradient as $B_p D_p^{-1}$, with $B_p = \sum_f w_{fp} u_f (x_f - x_p)^T$ and $D_p = \sum_f w_{fp}(x_f - x_p)(x_f - x_p)^T$.
For bilinear weights, $D_p$ is diagonal with the entries $s(1-s)\Delta x^2$ and $t(1-t)\Delta x^2$, where $(s, t)$ is the position of the particle inside the stencil of the component, and $B_p D_p^{-1} = \sum_f u_f\nabla w_{fp}$.
The gradient form has no division and works also when $s$ or $t$ is 0.
Each component of the MAC grid has its own stencil, so $D_p$ differs for $u$ and $v$.
Lines L1, L3, L4 and L6 are the lines of PIC; line L6 keeps the particles in the range where no weight is clamped.

## Example

Take an 8 by 8 grid with $\Delta x = 1/8$ m, 256 particles at random positions at least half a cell from the walls, unit masses, and the rigid rotation $u = -(y - 1/2)$, $v = x - 1/2$ with $c^u = (0, -1)$ and $c^v = (1, 0)$.
Do lines L2 and L5 only, again and again at the same positions.
With PIC, the kinetic energy after 1, 2, 5 and 10 round trips is 0.9340, 0.8758, 0.7279 and 0.5397 of the start value (the example of the PIC page).
With APIC it is 1 to within rounding after every round trip, the gradients stay $(0, -1)$ and $(1, 0)$ to within $4\cdot 10^{-15}$, and the angular momentum changes by less than $10^{-15}$ of its value.

Now take the closed swirl of the [FLIP page](/fluid-implicit-particle/): the same box full of liquid with $u = \sin(\pi x)\cos(\pi y)$, $v = -\cos(\pi x)\sin(\pi y)$, no gravity and steps of 0.02 s.
APIC starts with the exact gradients of this field.
The table gives the measured particle energy as a fraction of the start value, and the root mean square difference between the particle velocity and the grid velocity at the particle after 40 steps, as a measure of noise.

| steps | PIC | FLIP ($\alpha = 0.95$) | FLIP ($\alpha = 1$) | APIC |
|---|---|---|---|---|
| 1 | 0.8916 | 0.9871 | 0.9924 | 0.9927 |
| 10 | 0.3378 | 0.9029 | 0.9676 | 0.9655 |
| 40 | 0.0152 | 0.7455 | 0.9521 | 0.9765 |
| noise after 40 steps (m/s) | 0.0005 | 0.069 | 0.159 | 0.028 |

APIC keeps about as much energy as pure FLIP on this flow, with less noise than the blend.
The energy of APIC is not monotone in the steps; it is not bounded by a proof here.

## Correctness

APIC is an approximation of the Euler equations of a liquid, and its error is not bounded here.
The claims below hold for bilinear weights, at the same particle positions in lines L2 and L5, and with no weight clamped, which holds if every particle is at least $\Delta x/2$ from the walls.
The angular momentum of the particles is $\sum_p m_p(x_p v_p - y_p u_p + c^v_{p,x} D^v_{p,xx} - c^u_{p,y} D^u_{p,yy})$: the angular momentum of the centers plus the one of the affine fields.
The angular momentum of the grid is $\sum_{v\text{ faces}} m_f x_f v_f - \sum_{u\text{ faces}} m_f y_f u_f$, with the face masses of line L2.
The tests check these facts, and the [proof](proofs/correctness.md) gives the arguments:

- **Angular momentum.** Line L2 keeps the angular momentum exactly, and line L5 keeps it exactly too.
- **Linear momentum.** Lines L2 and L5 keep $\sum m u$ and $\sum m v$.
- **Affine fields.** If every particle carries the same affine field, lines L2 and L5 give it back exactly, both the velocity and the gradient.
- **The gradient.** Line L5 gives $B_p D_p^{-1}$, with $D_p$ diagonal.

Gravity and the projection of line L4, through the walls, change the angular momentum; the claims are about the transfers only.
The tests also run a small dam break and check that the divergence stays near 0 and that the particles stay in the box.

## Complexity

The transfers cost $O(n + c)$ time, with four faces per component and particle, and a few more operations per face than PIC.
Line L4 costs $O(k c)$ for $k$ conjugate gradient iterations.
The memory is $O(n + c)$, with four more numbers per particle in 2D than PIC.

## Properties

- **Angular momentum.** Kept exactly by the transfers, under the hypotheses above (proved).
- **Linear fields.** Kept exactly by a round trip (proved), so rigid rotations and shears are not damped by the transfers.
- **Stability.** The particle state is read back from the grid in line L5, as in PIC, so APIC does not build up the free particle noise of FLIP.
- **Dissipation.** Lower than PIC, because only the part of the flow that is not affine near a particle is averaged away (measured in the example).
- **Energy.** This page gives no energy bound for APIC; the swirl table is a measurement.

## Variants and improvements

- **Other kernels.** With quadratic or cubic B-spline weights, $D_p$ is a constant times the identity, $\frac14\Delta x^2$ and $\frac13\Delta x^2$, and $C_p = B_p D_p^{-1}$ is cheap.
- **Collocated grids.** On a grid with all velocity components at the nodes, as in the [material point method](/material-point-method/), one matrix $D_p$ serves both components, and the transfers are the same in form.
- **Polynomial PIC.** Later work stores more polynomial terms on each particle, which keeps more of the flow at a higher cost.
- **FLIP blends.** Some solvers mix APIC with a small part of the FLIP update for more detail.

## When to use it

Use APIC for liquids where swirls should last and the noise of [FLIP](/fluid-implicit-particle/) is not acceptable, and in the [material point method](/material-point-method/) for solids, sand and snow.
Use [PIC](/particle-in-cell/) if the dissipation does no harm and the code must be as simple as possible.

## Pitfalls

- **One matrix for both components.** On a MAC grid, $u$ and $v$ have different stencils. Line L5 must compute $c^u$ from the $u$ faces and $c^v$ from the $v$ faces, each with its own weights.
- **Dividing by $D_p$.** For bilinear weights, $D_p$ is singular when a particle is on a grid line of a stencil. Use the gradient form of line L5, not $B_p D_p^{-1}$.
- **A missing term in line L2.** Line L2 must add $c_p\cdot(x_f - x_p)$ before the division by the face mass. Without it APIC is PIC, and the gradients of line L5 are lost in the next step.
- **Clamped weights.** If a particle is closer than $\Delta x/2$ to a wall, the weights clamp, the gradient of line L5 is wrong and the angular momentum is not kept. Line L6 keeps the particles away from this zone.
- **Angular momentum of the centers only.** The particle angular momentum includes the affine term. Measuring only $\sum m(x v - y u)$ gives a false loss.

## Implementations

## History

PIC (Harlow, from the 1950s) averages away the rotation of the flow near each particle, and FLIP (Brackbill and Ruppel 1986) keeps it but becomes noisy.
Jiang, Schroeder, Selle, Teran and Stomakhin (2015) gave each particle an affine velocity field, with transfers that keep linear and angular momentum.
Jiang, Schroeder and Teran (2017) gave the analysis in more detail, including a MAC grid version.
APIC and its extensions are now common in material point method solvers for graphics.

## References
