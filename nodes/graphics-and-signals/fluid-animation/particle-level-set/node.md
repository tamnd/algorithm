---
tag: S6VHF6
kind: algorithm
slug: particle-level-set
name: Particle level set method
aliases:
- hybrid particle level set
area: graphics-and-signals/fluid-animation
level: advanced
summary: "Move a liquid surface as a level set and fix its loss of volume with marker particles on both sides. A particle that crosses the surface by more than its radius rebuilds it nearby."
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of grid nodes", p: "the number of particles", c: "the number of points where the interface crosses a grid edge"}
  time: {advect: "Θ(n + p)", correct: "Θ(n + p)", reinitialize: "O(n c)", step: "O(n c + p)"}
  space: {extra: "Θ(n + p)"}
properties: {deterministic: false, exact: false, conservative: false}
history:
  year: 2002
  people: [Douglas Enright, Ronald Fedkiw, Joel Ferziger, Ian Mitchell]
  note: Enright, Fedkiw, Ferziger and Mitchell put marker particles on both sides of a level set interface and used the particles that escape to rebuild the level set where it had lost detail.
prereqs: [level-set-method, signed-distance-function, bilinear-interpolation]
see_also: [fluid-simulation-for-animation, fast-marching-method, volume-of-fluid-method, marker-and-cell-method, weno-scheme, runge-kutta-methods, particle-fluid-surfacing, marching-cubes]
sources:
  - paper: doi:10.1006/jcph.2002.7166
    title: "Douglas Enright, Ronald Fedkiw, Joel Ferziger and Ian Mitchell, A hybrid particle level set method for improved interface capturing, Journal of Computational Physics 183(1), 83-116, 2002"
    locator: "section 2.2 (marker particles, equations 5 to 7), section 2.3 (seeding and attraction, equations 8 and 9; escape and correction, equations 10 to 13; reinitialization and the order of the steps; reseeding), section 3.1 (Zalesak's disk, tables 1 and 2)"
  - paper: doi:10.1145/566654.566645
    title: "Douglas Enright, Stephen Marschner and Ronald Fedkiw, Animation and rendering of complex water surfaces, ACM Transactions on Graphics 21(3), 736-744, 2002 (SIGGRAPH 2002)"
    locator: the use of the particle level set for water in animation
  - paper: doi:10.1016/j.compstruc.2004.04.024
    title: "Douglas Enright, Frank Losasso and Ronald Fedkiw, A fast and accurate semi-Lagrangian particle level set method, Computers and Structures 83, 479-490, 2005"
    locator: the semi-Lagrangian version
  - paper: doi:10.1016/0021-9991(88)90002-2
    title: "Stanley Osher and James A. Sethian, Fronts propagating with curvature-dependent speed: algorithms based on Hamilton-Jacobi formulations, Journal of Computational Physics 79(1), 12-49, 1988"
    locator: the level set method
  - paper: doi:10.1016/0021-9991(79)90051-2
    title: "Steven T. Zalesak, Fully multidimensional flux-corrected transport algorithms for fluids, Journal of Computational Physics 31, 335-362, 1979"
    locator: the slotted disk test
---

The particle level set method of Enright, Fedkiw, Ferziger and Mitchell (2002) tracks a moving interface, such as the surface of water, with two tools at once. A [level set](/level-set-method/) $\varphi$ on a grid gives the surface as the set $\varphi = 0$. It handles changes of topology with no extra work, but each step smooths it a little, so thin parts and sharp corners lose volume and vanish. Marker particles carried by the flow keep their shape well, but they give no surface by themselves. The method puts particles on both sides of the surface, near it. When a particle is found on the wrong side of the level set by more than its radius, it has "escaped": the level set has lost something there. The particle then rebuilds $\varphi$ in its grid cell with the help of the small circle around it. The level set stays in charge of the surface, and the particles only repair it.

## In plain words

Think of a puddle drawn on graph paper. Each grid point knows how far it is from the edge of the puddle, and on which side. When the water moves, these numbers are moved too, but each move blurs them a little. After many moves, thin parts of the puddle disappear.

So we also drop many small beads near the edge, some in the water and some in the air. The beads move with the water and do not blur. If a water bead ends up in the air side of the drawing, by more than its own size, the drawing is wrong there. The bead then pulls the edge back out around itself. Air beads do the same on the other side.

## The problem

Given a velocity field $\mathbf u$ and an interface as the zero set of $\varphi$, move the interface with the flow: $\varphi_t + \mathbf u \cdot \nabla \varphi = 0$. In a fluid solver, $\mathbf u$ is the fluid velocity, and $\varphi < 0$ marks the liquid. Grid methods for this equation are smooth by design. Where the interface is thinner than a few cells, or has corners, they lose part of the shape, and in a liquid this is a loss of volume. The paper calls this the "excessive regularization" of a level set method. We want a level set that keeps the detail that the flow carries, while it keeps the simple grid operations of a level set.

This page uses $\varphi < 0$ for the liquid and $\varphi > 0$ for the air. The paper uses $\varphi > 0$ for one region and $\varphi \le 0$ for the other. Only the signs matter: positive particles live where $\varphi > 0$ and negative ones where $\varphi < 0$.

## The algorithm

Each particle $p$ has a position $\mathbf x_p$, a sign $s_p = \pm 1$ and a radius $r_p$ between $r_{min} = 0.1 \Delta x$ and $r_{max} = 0.5 \Delta x$ (the paper's equations 6 and 7). Its own small level set is $\varphi_p(\mathbf x) = s_p (r_p - |\mathbf x - \mathbf x_p|)$ (equation 10). $\varphi(\mathbf x_p)$ is interpolated from the grid.

**Seeding.** Put particles of both signs at random in the cells near the interface (the paper takes cells with a corner where $|\varphi| < 3 \Delta x$, and 16 particles of each sign per cell in 2D). Give each particle a goal value $\varphi_{goal} = s_p\, U[b_{min}, b_{max}]$, with $b_{min} = r_{min}$ and $b_{max} = 3 \Delta x$. Move it along the normal $\mathbf N = \nabla \varphi / |\nabla \varphi|$ by $\mathbf x_p \leftarrow \mathbf x_p + \lambda (\varphi_{goal} - \varphi(\mathbf x_p)) \mathbf N$ (equation 8), with $\lambda = 1$, halved while the point leaves the domain. Accept the point when it is in the band $s_p \varphi \in [b_{min}, b_{max}]$; else move with $\lambda / 2$ and try again. Delete the particle after 15 tries. Then set $r_p$ as in line L7 (equation 9).

**One step.**

```pseudo id=main
PLS-STEP(φ, particles, u, Δt)
L1  move φ with u over Δt on the grid, and move each particle x_p with u over Δt
L2  E <- the particles with s_p φ(x_p) < 0 and |φ(x_p)| > r_p (the escaped particles)
L3  φ+ <- max(φ, φ_p) over the positive particles of E, and φ- <- min(φ, φ_p) over the negative ones, at the corners of each particle's cell
L4  at each node, φ <- φ+ if |φ+| <= |φ-|, else φ-
L5  reinitialize φ to a signed distance
L6  repeat lines L2 to L4 with the new φ
L7  r_p <- min(max(s_p φ(x_p), r_min), r_max) for each particle
```

Lines L2 to L4 run once after line L1 and once more after line L5, because reinitialization can also move the interface (the paper's section 2.3.4). During line L5, the particles do not move. Line L7 lets a particle shrink as the interface comes close, so that small and slow drift does not count as an escape. Escaped particles are not deleted: they mark detail that the grid cannot hold now, and they may help again later.

**Reseeding.** Stretching flows leave parts of the interface with few particles. Every few steps, or when the interface length changes much, the paper adds particles to cells near the interface that have too few, deletes non-escaped particles far from it, and keeps the particles nearest to the interface in cells that have too many. The code of this page seeds once and does not reseed.

**The parts of the paper.** The paper moves $\varphi$ with a fifth order Hamilton-Jacobi [WENO scheme](/weno-scheme/) and the particles with third order TVD [Runge-Kutta](/runge-kutta-methods/), and reinitializes by the PDE $\varphi_\tau + \operatorname{sgn}(\varphi_0)(|\nabla \varphi| - 1) = 0$. The code here uses simpler parts for a small test: it moves $\varphi$ by semi-Lagrangian sampling, which is a form of the [method of characteristics](/method-of-characteristics/), as in the 2005 paper of Enright, Losasso and Fedkiw; it moves particles by the exact flow of a rotation; and it reinitializes by a brute force search for the nearest crossing point.

## Example

**One escaped particle, by hand.** Let $\varphi = y - 1/2$ on a $32 \times 32$ grid, so the liquid is below $y = 1/2$. A negative particle with $r_p = 0.3 \Delta x$ sits at a height $0.4 \Delta x$ above the surface. Then $\varphi(\mathbf x_p) = 0.4 \Delta x > r_p$, and the particle has escaped. The node of its cell just above it is at distance $0.1 \Delta x$, so $\varphi_p = -(0.3 - 0.1)\Delta x = -0.2 \Delta x$ there, and $\varphi = 0.5 \Delta x$. Line L3 gives $\varphi^- = -0.2 \Delta x$ and $\varphi^+ = 0.5 \Delta x$. Line L4 takes $-0.2 \Delta x$, so this node moves into the liquid. The other three corners keep their values. If the same particle were only $0.2 \Delta x$ above the surface, it would not count as escaped, and nothing would change.

**Zalesak's disk, measured.** Zalesak's slotted disk (1979) is the standard test for this kind of loss. The paper uses a disk of radius 15 at $(50, 75)$ in a $100 \times 100$ domain, with a slot of width 5 and length 25 cut from the bottom, turned once about the center of the domain. On the unit square, this is a disk of radius 0.15 at $(0.5, 0.75)$, with the area 0.0582. The code turns it once on a $32 \times 32$ grid, so the slot is 1.6 cells wide, with 400 particles from seed 3. Areas are counted on $200 \times 200$ sample points:

| Steps per turn | Level set only: area (loss) | Particle level set: area (loss) | Area of wrong sign, level set only | Area of wrong sign, particles |
|---|---|---|---|---|
| 32 | 0.0458 (21.3%) | 0.0549 (5.6%) | 0.0324 | 0.0222 |
| 64 | 0.0273 (53.1%) | 0.0536 (8.0%) | 0.0481 | 0.0242 |
| 128 | 0 (100%) | 0.0529 (9.1%) | 0.0582 | 0.0246 |

Without particles, each step blurs $\varphi$ once more, so more steps lose more, and at 128 steps the disk is gone. With particles, the loss stays near 10 percent, and most of the remaining error is the slot, which the grid cannot hold at this size. For four other seeds at 64 steps, the area with particles was between 0.052 and 0.057.

The paper's table 2 reports, for one turn with the particle level set, a loss of 14.9% on a $50 \times 50$ grid, 0.31% on $100 \times 100$ and 0.20% on $200 \times 200$. Its level set alone (table 1) loses the whole disk on the $50 \times 50$ grid. These numbers come from a fifth order scheme and 16 particles per cell, so they are not directly comparable with the small test here.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Seeded particles have not escaped.** After seeding, every particle has $s_p \varphi(\mathbf x_p) \ge r_p$, so the correction changes nothing until the flow moves things.
2. **The escape test.** If $\varphi$ is a signed distance near $\mathbf x_p$, a particle has escaped exactly when its whole circle is on the wrong side.
3. **Local and one-sided.** Lines L3 and L4 change only the corners of the cells of escaped particles. Positive particles can only raise $\varphi$, negative ones can only lower it, and where both meet the value closer to zero wins.
4. **One particle.** For a single escaped negative particle, a positive corner at distance $d$ becomes negative exactly when $d < r_p$ and $r_p - d \le \varphi$.

These are statements about one correction. The method does not conserve volume exactly: the paper's own tables show small losses and gains. Particles also cannot restore detail where no particle is left, which is why reseeding matters.

## Complexity

Let $n$ be the number of grid nodes and $p$ the number of particles. Line L1 costs $\Theta(n)$ for the grid and $\Theta(p)$ for the particles. Lines L2 to L4 cost $\Theta(p)$ for the tests and four nodes per escaped particle. The code copies $\varphi$ twice, so it costs $\Theta(n + p)$. Line L7 costs $\Theta(p)$. Reinitialization by fast marching costs $O(n \log n)$, and a PDE solver costs $O(n)$ per iteration; both can be limited to a band near the interface. The brute force search of the code costs $O(n c)$, where $c$ is the number of crossing points. So one step of the code costs $O(n c + p)$. Space is $\Theta(n + p)$.

The particles live only in a band of about 3 cells on each side, so $p$ grows with the area of the interface in 3D, not with the volume. The paper notes that only escaped particles in poorly resolved regions need the square roots of line L3.

## Properties

- **The level set decides.** The surface is always the zero set of $\varphi$. Particles never define it directly; they only correct $\varphi$.
- **Both signs are needed.** Positive particles repair the corners that the liquid rounds off from outside, and negative particles repair those it rounds off from inside. In the paper's figure 14, the two kinds of particles repair different corners of the slot.
- **Topology is free.** Merging and splitting come from the level set, as in a plain level set method, and particles need no links to each other.
- **Not exactly conservative.** It reduces the loss of volume but does not remove it. A [volume of fluid](/volume-of-fluid-method/) method conserves volume to rounding error, but places it less sharply.
- **Random.** Seeding is random. The code takes a seeded random generator, so a run can be repeated.

## Variants and improvements

- **Semi-Lagrangian particle level set.** Enright, Losasso and Fedkiw (2005) move $\varphi$ with a semi-Lagrangian step and use the particles to recover the accuracy that the simpler step loses.
- **Water in animation.** Enright, Marschner and Fedkiw (2002) used the method for water surfaces, with a "thickened" front tracking technique and a velocity extrapolation that moves the surface smoothly.
- **Other escape thresholds.** The paper uses "out by more than the radius", and notes that any nonzero multiple of the radius would do.

## When to use it

Use it to track a liquid surface on a grid in a [fluid simulation](/fluid-simulation-for-animation/) when thin sheets, drops and sharp features must survive many steps. For smooth, well resolved surfaces, a plain level set with a good scheme may be enough. For particle based fluids such as [FLIP](/fluid-implicit-particle/), the fluid particles themselves can define the surface; see [particle fluid surfacing](/particle-fluid-surfacing/). When exact volume matters more than sharp shape, a volume of fluid method fits better.

## Pitfalls

- **Escape threshold too small.** If any crossing of the interface counts, rounding and interpolation errors trigger repairs all the time. The paper requires the particle to be out by more than its radius.
- **$\varphi$ not a signed distance.** The escape test and the formula $\varphi_p$ compare distances with values of $\varphi$. If $\varphi$ is steep or flat, they disagree. Reinitialize every step.
- **Moving particles in line L5.** Reinitialization should not move the interface, so the particles must stay fixed while it runs.
- **Deleting escaped particles.** They mark lost detail; delete only non-escaped particles far from the interface.
- **Too much reseeding.** New particles are attracted to the current $\varphi$, which may already be wrong. The paper warns that where the geometry is poorly resolved, reseeding may make the interface worse.
- **Inaccurate particle motion.** The repair is only as good as the particle paths. The paper uses trilinear interpolation of the velocity and third order TVD Runge-Kutta for them.

## Implementations

## History

Marker particles go back to the [marker-and-cell method](/marker-and-cell-method/) of 1965, which filled the liquid with particles. Osher and Sethian (1988) introduced the level set method, and it became the common way to capture interfaces with changes of topology. Its loss of volume in thin and sharp regions was a known weakness. In 2002, Enright, Fedkiw, Ferziger and Mitchell combined the two: particles only near the interface, on both sides, and used only where the level set fails. They showed the gain on Zalesak's disk, on a vortex that stretches a disk into a thin filament, on a deformation field, and on 3D tests. In the same year, Enright, Marschner and Fedkiw brought the method to water in computer graphics. Enright, Losasso and Fedkiw (2005) made a faster semi-Lagrangian version.

## References
