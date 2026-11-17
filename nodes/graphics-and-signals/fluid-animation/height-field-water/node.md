---
tag: CH9SFZ
kind: algorithm
slug: height-field-water
name: Height field water
aliases:
- Kass-Miller water
area: graphics-and-signals/fluid-animation
level: core
summary: Simulate a water surface as a height grid evolving by a linearized shallow water wave equation with implicit steps, cheap enough for real time.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {c: "the number of grid cells (n_x times n_y)"}
  time: {step: "O(c)"}
  space: {extra: "O(c)"}
properties: {deterministic: true, exact: false, conserves_volume: true, unconditionally_stable: true, overhanging_surfaces: false}
history:
  year: 1990
  people: [Michael Kass, Gavin Miller]
  note: Kass and Miller presented the method at SIGGRAPH 90, with implicit steps of a linearized shallow water equation and tridiagonal solves along the rows and the columns.
prereqs: [wave-equation, thomas-algorithm, finite-difference-method]
see_also: [shallow-water-equations, gerstner-waves, fft-ocean-synthesis, backward-euler-method, stable-fluids, fluid-simulation-for-animation]
sources:
  - paper: doi:10.1145/97880.97884
    title: Michael Kass and Gavin Miller, Rapid, stable fluid dynamics for computer graphics, ACM SIGGRAPH Computer Graphics 24(4), 49-57, 1990
    locator: the whole paper (the linearized shallow water equation, the implicit step and the tridiagonal solves)
  - book: "Robert Bridson, Fluid Simulation for Computer Graphics, 2nd edition, CRC Press, 2015"
    title: Fluid Simulation for Computer Graphics
    locator: the chapter on shallow water
---

Height field water stores the water surface as one height per cell of a 2D grid, so the water is a sheet with no overhangs and no splashes.
The heights move by a linearized form of the [shallow water equations](/shallow-water-equations/), a [wave equation](/wave-equation/) whose wave speed is $(g d)^{1/2}$ for the water depth $d$.
Kass and Miller (1990) made it fast and stable with implicit steps: each step is one tridiagonal solve along each row and one along each column.
The step size is then limited by the accuracy that the animation needs, not by stability, and the volume of the water is kept exactly.
The method suits ponds, rivers and wakes in real time.

## In plain words

The water is a grid of columns, and each column has a height.
Where a column is higher than its neighbors, water flows out of it, and where it is lower, water flows in.
So a bump in the surface spreads out as waves, and in deep water the waves run faster.
Each step works out the new heights of a whole row of columns at once, and then of a whole column of the grid at once.
Doing it all at once in this way keeps the method calm even with long steps, and no water is lost or made.

## The problem

The input is a grid of $n_x$ by $n_y$ cells of size $\Delta x$, the water heights $h$ at the current step and $h^-$ at the last step, the depth $d$ of each cell, gravity $g = 9.81$ m/s², the step $\Delta t$ and a damping $\tau \in [0, 1]$.
The output is the height field at the next step.
The equation is

$$\frac{\partial^2 h}{\partial t^2} = \nabla\cdot(g\,d\,\nabla h),$$

with no flow through the border of the grid.
It comes from the shallow water equations when the waves are small, the velocity is small, and the depth $d = h - b$ above the ground $b$ is taken as known in each step.
This is one method for [fluid simulation for animation](/fluid-simulation-for-animation/).

## The algorithm

```pseudo id=main
HEIGHT-FIELD-STEP(h, h⁻, d, Δt)
L1  for each cell k: r_k ← h_k + (1 - τ)(h_k - h⁻_k)
L2  s ← g Δt² / (2 Δx²); for each pair of neighbor cells k, l: e_kl ← s (d_k + d_l), or 0 if d_k = 0 or d_l = 0
L3  for each row: solve z_k + Σ_l e_kl (z_k - z_l) = r_k over the x neighbors l, by the Thomas algorithm
L4  for each column: solve h'_k + Σ_l e_kl (h'_k - h'_l) = z_k over the y neighbors l, by the Thomas algorithm
L5  return h', h
```

Line L1 extrapolates the motion of the last step, $h + (h - h^-)$, with a damping $\tau$ that removes a part of the velocity.
Line L2 computes the coupling of each pair of neighbors, the [finite difference](/finite-difference-method/) form of $g\,d$ on the face between them.
A dry cell, with $d = 0$, has no coupling; this rule of the code keeps the water out of dry cells.
Lines L3 and L4 are the implicit part.
Together they solve $(I + A_x)(I + A_y)h' = r$, where $A_x$ and $A_y$ are the 1D operators of the two directions, and this is a split form of the implicit step $(I + A_x + A_y)h' = r$.
Each line of the grid is a tridiagonal system, and the [Thomas algorithm](/thomas-algorithm/) solves it in linear time.
The matrices are strictly diagonally dominant, so the Thomas algorithm needs no pivoting.
In a full run, the depth comes from $d = \max(h - b, 0)$ before each step.
This follows the idea of Kass and Miller; the code is not claimed to repeat their exact equations.

## Example

Take a 1D channel of 10 m with 400 cells ($\Delta x = 0.025$ m), depth 1 m, no damping, and a Gaussian bump of height 0.01 m and width 0.2 m in the middle, at rest.
The bump splits into two waves that run to the left and to the right.
The exact speed is $(g d)^{1/2} = 3.13209$ m/s.
After 1 s, the table gives the measured distance of the right crest from the start and its height.
Each of the two waves of the exact linear equation would have the height 0.005 m.

| $\Delta t$ (s) | Courant number $c\Delta t/\Delta x$ | crest distance (m) | crest height (m) |
|---|---|---|---|
| 0.002 | 0.25 | 3.11 | 0.00355 |
| 0.005 | 0.63 | 3.11 | 0.00269 |
| 0.01 | 1.25 | 3.11 | 0.00206 |
| 0.02 | 2.5 | 3.06 | 0.00153 |
| 0.05 | 6.3 | 2.99 | 0.00101 |

The crest position is read to the nearest cell, 0.025 m.
The step stays stable far above a Courant number of 1, where an explicit scheme would blow up.
The price is damping and a slower wave at large steps: the implicit step removes energy from the short waves, so the crest gets lower and wider.

## Correctness

The scheme approximates the wave equation, and its error depends on $\Delta t$ and $\Delta x$; this page does not bound it.
The tests check these facts, and the [proof](proofs/correctness.md) gives the arguments:

- **Thomas.** The tridiagonal solves equal Gaussian elimination, checked in exact rational arithmetic.
- **Volume.** Each of lines L3 and L4 keeps the sum of the heights, for any depths and any $\tau$. So if $h$ and $h^-$ have the same volume, all later steps have it too. The test checks this exactly with fractions.
- **Energy.** For a constant depth and $\tau = 0$, the discrete energy $|h' - h|^2 + \frac12(\langle Mh', h'\rangle + \langle Mh, h\rangle)$ with $M = A_x + A_y + A_x A_y$ does not increase, for any $\Delta t$. So the step is stable for any step size.
- **Rest.** A flat lake, also with islands of dry ground, stays flat.

The wave speed of the example is a measurement, close to $(g d)^{1/2}$ for small steps.

## Complexity

Each row solve and each column solve is linear in its length, so a step costs $O(n_x n_y)$ time, about a constant number of passes over the grid.
The memory is $O(n_x n_y)$.
There is no iteration and no tolerance, so the cost per step is fixed, which suits real time.

## Properties

- **Unconditional stability.** The energy does not grow for any $\Delta t$ (proved for a constant depth). For a depth that varies, the split operators do not commute, and the energy proof does not apply.
- **Exact volume.** Each solve keeps the sum of the heights (proved).
- **Damping.** The implicit step damps the waves, more at large steps and for short waves (measured).
- **Wave speed.** Waves run faster in deep water and slower in shallow water, so waves bend toward a beach and slow down there. This is a property of the equation.
- **Height field.** The surface is a function of the position, so there are no breaking waves, overhangs or splashes.

## Variants and improvements

- **Full shallow water.** A solver of the [shallow water equations](/shallow-water-equations/) with velocities on a staggered grid adds the flow of the water, not only the waves.
- **Explicit steps.** An explicit step is simpler and damps the waves less, but it is stable only when $c\Delta t/\Delta x$ is below a limit of order 1.
- **No splitting.** Solving $(I + A_x + A_y)h' = r$ with [conjugate gradients](/conjugate-gradient-method/) removes the splitting error at a higher cost.
- **Ocean waves.** For deep open water, [Gerstner waves](/gerstner-waves/) or [FFT ocean synthesis](/fft-ocean-synthesis/) give waves with no simulation; a height field adds the local response to objects.
- **Coupling to particles.** Splashes from a particle system on top of the height field give the motion that a height field cannot hold.

## When to use it

Use height field water for ponds, pools, rivers and wakes, where the surface has no overhangs and the cost must be small and fixed.
For breaking waves and splashes, use a 3D solver such as [FLIP](/fluid-implicit-particle/) or [SPH](/smoothed-particle-hydrodynamics/).
For deep ocean waves seen from far away, use [FFT ocean synthesis](/fft-ocean-synthesis/).

## Pitfalls

- **No damping and long runs.** With $\tau = 0$ in line L1, only the implicit damping removes energy, and small waves can run for a long time. A small $\tau$ gives calm water.
- **Water flowing into dry cells.** Without the rule of line L2 for dry cells, a dry cell next to water gets a coupling, and the heights of its ground pull water into it or out of it. The code sets the coupling to 0, which also stops water from flooding dry land.
- **Negative depth.** With large waves on a shallow bed, $h - b$ can become negative. The depth must be clamped at 0 before line L2.
- **Wrong boundary rows.** At the border, line L3 has only one neighbor. Using a coupling to a cell outside the grid adds or removes water.
- **One pass only.** Only line L3, without line L4, gives waves along the rows only.

## Implementations

## History

Kass and Miller (1990) presented this method at SIGGRAPH 90.
They linearized the shallow water equations, took implicit steps for stability, and split the 2D solve into tridiagonal solves along the rows and the columns.
They also let the depth change with the water and the ground, so that waves slow down near a beach.
Height fields of this kind are still a common choice for water surfaces in games.

## References
