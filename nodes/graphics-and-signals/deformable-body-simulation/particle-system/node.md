---
tag: 8JJ5P6
kind: model
slug: particle-system
name: Particle system
aliases:
- Reeves particle system
area: graphics-and-signals/deformable-body-simulation
level: intro
summary: Model fuzzy phenomena such as fire, smoke and sparks as many point particles that are emitted with random attributes, moved by forces and removed when their lifetime ends.
prereqs: [symplectic-euler-method]
see_also: [mass-spring-system, social-force-model, boids, smoothed-particle-hydrodynamics, molecular-dynamics, alpha-blending, position-based-dynamics, cloth-simulation]
sources:
  - paper: doi:10.1145/357318.357320
    title: "William T. Reeves, Particle systems: a technique for modeling a class of fuzzy objects, ACM Transactions on Graphics 2(2), 91-108, 1983 (also Computer Graphics 17(3), SIGGRAPH 83, 359-376)"
    locator: "Section 2 (the five steps of a frame), Section 2.1 (the number of new particles), Section 2.2 (the attributes and the generation shape), Section 2.3 (dynamics) and Section 2.4 (extinction)"
  - paper: doi:10.1145/97879.97923
    title: "Karl Sims, Particle animation and rendering using data parallel computation, Proceedings of SIGGRAPH 90, 405-413, 1990"
    locator: the whole paper (particle operations written as data parallel functions over all particles, general locator)
---

A particle system models a fuzzy object, such as fire, smoke, sparks or spray, as a large set of point particles that are born, move and die. William Reeves introduced it in 1983 for the fire in the Genesis Demo sequence of the film Star Trek II. The model fixes the state of a particle and the rules of emission, update and death, and leaves the forces and the rendering to the user. It differs from the [social force model](/social-force-model/), where the particles are pedestrians that push on each other, and from the [mass-spring system](/mass-spring-system/), where springs join the particles: in Reeves's model the particles do not interact at all.

## The machine

The state at frame $f$ is a set $P_f$ of particles. A particle carries a position $\mathbf x$ (in m), a velocity $\mathbf v$ (in m/s), a size, a color, a transparency, a shape and a remaining lifetime $\ell$, which is a whole number of frames. A system also has an origin, an orientation and a generation shape: a sphere of radius $r$, a circle of radius $r$ or a rectangle of length $l$ and width $w$. Every random attribute is a mean plus a random part:

$$a = \bar a + \mathrm{Rand}() \cdot \Delta a,$$

where $\mathrm{Rand}()$ is uniform in $[-1, 1]$, $\bar a$ is the mean and $\Delta a$ is what Reeves calls the variance (it is the half width of the range, not a statistical variance). Each frame does five steps (Reeves, Section 2):

1. **Emission.** The number of new particles is $N_f = \bar N_f + \mathrm{Rand}() \cdot \Delta N$ with $\bar N_f = N_0 + \delta N \, (f - f_0)$, a mean that changes linearly from the first frame $f_0$ of the system. A second form scales the count by the screen area of the system, so a small object on the screen gets few particles.
2. **Attributes.** Each new particle gets a random position inside the generation shape. A sphere sends particles outward from its center; a circle or a rectangle sends them up, tilted by at most an ejection angle. The speed is $\bar s + \mathrm{Rand}() \cdot \Delta s$. Color, transparency, size and lifetime use the same rule.
3. **Death.** A particle with $\ell = 0$ is removed. Optional rules also remove a particle whose intensity falls below a threshold, or one that has moved too far from the origin in a given direction.
4. **Update.** Each remaining particle moves by its velocity, its velocity changes by a constant acceleration $\mathbf a$ (for example gravity $(0, -9.81, 0)$ m/s$^2$), its color, transparency and size change at fixed rates, and $\ell$ decreases by 1.
5. **Rendering.** Each living particle is drawn, in Reeves's renderer as a point light source added to the frame buffer.

Reeves adds the velocity to the position once per frame and does not state the order of the two updates. This page and its code use [symplectic Euler](/symplectic-euler-method/), velocity first, with a frame time $\Delta t$:

$$\mathbf v \leftarrow \mathbf v + \Delta t \, \mathbf a, \qquad \mathbf x \leftarrow \mathbf x + \Delta t \, \mathbf v.$$

One frame, without the rendering, is then:

```pseudo id=main
PARTICLE-SYSTEM-FRAME(P, f, dt)
L1  mean <- N0 + dN (f - f0)
L2  n <- round(mean + Rand() VarN)        ▷ Rand() is uniform in [-1, 1]
L3  repeat n times: add to P a particle with a position in the generation shape, speed MeanSpeed + Rand() VarSpeed and lifetime MeanLife + Rand() VarLife
L4  remove from P each particle with lifetime 0 or outside the region of interest
L5  for each particle in P: v <- v + dt a
L6      x <- x + dt v
L7      lifetime <- lifetime - 1
```

The standing assumptions are that particles do not act on each other and do not intersect the other objects of the scene (Reeves composites those objects in a separate pass), and that each particle is drawn as a point light source, so the light of the particles adds up and no particle hides another. The code with this page is 2D, with $\mathbf x = (x, y)$, $y$ up, and a segment as the generation shape.

## What it counts

The model gives the positions and the appearance of all living particles at each frame, and so an image of the fuzzy object. The quantities that the designer controls are statistical: the mean rate of birth, the spread of speeds and directions, and the mean lifetime. The model makes no claim about the physics of fire or smoke. It is a procedural model: the parameters are tuned until the result looks right, and each one is a tuning, not a measured property of a material.

The cost of a frame is $\Theta(n)$ for $n$ living particles, because every step treats each particle once and no step looks at pairs. Memory is $\Theta(n)$.

## Relation to other models

The particle system is the simplest of the particle models in graphics. The others add an interaction:

- A [mass-spring system](/mass-spring-system/) joins particles with springs, so the forces depend on pairs of positions. Cloth and soft bodies use it.
- [Smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/) gives each particle a density and a pressure from its neighbors, so the particles behave as a fluid.
- [Boids](/boids/) and the [social force model](/social-force-model/) give each particle steering rules or forces from its neighbors, for flocks and crowds.
- [Molecular dynamics](/molecular-dynamics/) moves atoms under pair potentials, with the same update loop but with physical forces and units.
- [Position-based dynamics](/position-based-dynamics/) moves particles and then projects them onto constraints.

Each of these keeps the particle state of Reeves and replaces step 4 by a solver with pair forces or constraints. The birth and death rules are what stay specific to particle systems for effects.

## Known results in the model

1. **No forces, straight lines (proved).** With $\mathbf a = 0$, the update gives $\mathbf x_n = \mathbf x_0 + n \Delta t \, \mathbf v_0$ exactly, in exact arithmetic. The test checks this to $10^{-12}$ in floating point.
2. **Free fall (proved, closed form).** A particle dropped from rest under gravity $g$ with symplectic Euler has $y_n = -g \Delta t^2 \, n (n + 1) / 2$ after $n$ frames, and with explicit Euler (position first) $y_n = -g \Delta t^2 \, n (n - 1) / 2$. The exact value is $-g t^2 / 2$ with $t = n \Delta t$. For $\Delta t = 0.1$ s and $n = 10$, symplectic Euler gives $-5.3955$ m, explicit Euler gives $-4.4145$ m, and the exact value is $-4.905$ m. Both errors are $g \Delta t \, t / 2$, so both methods are first order. The test checks the three numbers.
3. **Lifetime in frames (proved, for the update order above).** A particle born with lifetime $L$ is moved and drawn in exactly $L$ frames. With $m$ births per frame and no variance, the count after frame $f$ (counted from 0) is $m \min(f + 1, L)$. The test checks this.
4. **Mean number of particles (proved).** If every frame has the same mean birth count $\bar N$ and the lifetimes are independent with mean $\bar L$, and no other rule kills particles, the expected number of living particles in the steady state is $\bar N \bar L$, by linearity of expectation over the birth frames. This is Little's law for the particle population.
5. **Range of the birth count (proved).** With rounding to the nearest integer, $N_f$ lies in $[\bar N_f - \Delta N - 1/2, \bar N_f + \Delta N + 1/2]$, and its mean is $\bar N_f$ up to the rounding. The test checks the range and measures the mean over 400 frames with a fixed seed.
6. **Parallel cost (observed).** Because no step looks at pairs, every step is a map over the particles. Sims (1990) wrote the operations as data parallel functions and ran the update and the rendering on a data parallel computer; his timings are measurements on that machine.

## References
