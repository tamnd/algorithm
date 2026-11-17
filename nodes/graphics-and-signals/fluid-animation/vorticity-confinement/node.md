---
tag: 8A418J
kind: technique
slug: vorticity-confinement
name: Vorticity confinement
aliases:
- vorticity confinement force
area: graphics-and-signals/fluid-animation
level: core
summary: "Add a force at right angles to the gradient of the vorticity magnitude, which spins up the small swirls that numerical dissipation removes from smoke on a coarse grid."
prereqs: [stable-fluids, mac-grid]
see_also: [fluid-simulation-for-animation, boussinesq-buoyancy, fire-simulation, bfecc, unconditionally-stable-maccormack, position-based-fluids, vortex-particle-method, navier-stokes-equations]
sources:
  - paper: doi:10.1145/383259.383260
    title: "Ronald Fedkiw, Jos Stam and Henrik Wann Jensen, Visual simulation of smoke, Proceedings of SIGGRAPH 2001, 15-22"
    locator: "section 3 (equations 9 to 11: the vorticity, the vectors N and the force), section 4 (forces at the voxel centers, added with the time step before the advection and the pressure solve), section 1.2 (stable while the force stays below a threshold)"
  - paper: doi:10.1063/1.868164
    title: "John Steinhoff and David Underhill, Modification of the Euler equations for vorticity confinement: application to the computation of interacting vortex rings, Physics of Fluids 6(8), 2738-2744, 1994"
    locator: the original confinement term in computational fluid dynamics, without the grid spacing factor
  - paper: doi:10.1145/1073204.1073282
    title: "Andrew Selle, Nick Rasmussen and Ronald Fedkiw, A vortex particle method for smoke, water and explosions, ACM Transactions on Graphics 24(3), 910-914, 2005"
    locator: vorticity carried on particles and given back to the grid by a confinement-like force
  - paper: doi:10.1145/2461912.2461984
    title: "Miles Macklin and Matthias Müller, Position based fluids, ACM Transactions on Graphics 32(4), 2013"
    locator: vorticity confinement on particles to give back the energy that the position solver removes
---

Vorticity confinement is a force that a grid fluid solver adds to its velocity to keep small swirls alive. Stable solvers for animation, such as [stable fluids](/stable-fluids/), use semi-Lagrangian advection, which averages the velocity at each step. On a coarse grid this averaging damps the rotation of the flow much faster than the real viscosity of air would. The force finds the places where the vorticity $\omega = \nabla \times \mathbf u$ is concentrated and pushes the fluid around them, so the swirls become stronger and stay small. Steinhoff and Underhill (1994) built the method for vortices around helicopter rotors. Fedkiw, Stam and Jensen (2001) brought it to smoke in graphics, with a factor $\Delta x$ so that the force goes to zero as the grid is refined. The force adds energy. It is a tuning tool, and its strength $\varepsilon$ is chosen by eye.

## In plain words

A swirl in smoke is like a small paddle wheel that turns the air around it. The usual stable solver smears the velocity a little at each step, so the paddle wheels slow down and the smoke looks thick and dull.

Vorticity confinement looks at how fast the air turns at each cell. It finds the direction toward the cells that turn faster, which is the direction to the center of a swirl. Then it pushes the air at right angles to that direction, in the sense that the swirl already turns. The push makes the swirl turn faster and keeps it tight. The push is weak where the air turns slowly and zero where every cell turns at the same rate. You set one number for its strength. If it is too large, the smoke gains energy and the flow can become noisy.

## When it applies

- The solver dissipates rotation more than the physics would, mostly by the interpolation in semi-Lagrangian advection on a coarse grid.
- The goal is the look of the flow, not a measured flow. The force changes the equations by a term that goes to zero only as $\Delta x \to 0$.
- The flow is a gas, such as smoke or the hot products of [fire](/fire-simulation/), with swirls of a few cells across. Most uses add the force to an incompressible solver before the pressure projection, which then removes any part of the force that is a gradient.
- The velocity is known on a grid, or can be estimated at particles, so that the curl and the gradient of its magnitude can be computed.

## The template

Fedkiw, Stam and Jensen give the force by three equations (their equations 9 to 11):

$$\omega = \nabla \times \mathbf u, \qquad \mathbf N = \frac{\boldsymbol\eta}{|\boldsymbol\eta|}, \quad \boldsymbol\eta = \nabla |\omega|, \qquad \mathbf f_{conf} = \varepsilon\, \Delta x\, (\mathbf N \times \omega).$$

The paper writes $h$ for the grid spacing $\Delta x$. In 2D, $\omega$ is a scalar, the $z$ part $\partial v / \partial x - \partial u / \partial y$ of the curl, and $\mathbf N \times \omega \hat{\mathbf z} = (N_y\, \omega,\ -N_x\, \omega)$. Each step of the solver does the following.

1. Compute the vorticity $\omega$ at each cell center. On a [MAC grid](/mac-grid/), average the face velocities to the centers, and take central differences.
2. Compute $\boldsymbol\eta = \nabla |\omega|$ at each cell center by central differences of $|\omega|$.
3. Normalize: $\mathbf N = \boldsymbol\eta / (|\boldsymbol\eta| + \delta)$, with a small $\delta > 0$.
4. Compute the force $\mathbf f = \varepsilon\, \Delta x\, (\mathbf N \times \omega)$ at each cell center.
5. Add $\Delta t\, \mathbf f$ to the velocity, at each face the mean of the two cells beside it. Then advect and project as usual.

```pseudo id=main
VORTICITY-CONFINEMENT(u, ε, Δx, Δt)
L1  for each cell c: ω_c ← curl of u at c, by central differences
L2  for each cell c: η_c ← gradient of |ω| at c
L3  N_c ← η_c / (|η_c| + δ)
L4  f_c ← ε Δx (N_c × ω_c)
L5  for each face: u ← u + Δt (mean of f over the two cells of the face)
```

**Why the direction is right.** Near the center of a swirl, $|\omega|$ has a peak, so $\mathbf N$ points toward the center. The cross product $\mathbf N \times \omega$ is at right angles to $\mathbf N$, and it turns in the sense of $\omega$. So the force is tangent to circles around the center, in the direction of the flow there. It is not along the gradient of $|\omega|$, but at right angles to it.

**Why the size is right.** Where $|\boldsymbol\eta| \gg \delta$, $|\mathbf N| = 1$ and $|\mathbf f| = \varepsilon\, \Delta x\, |\omega|$. The force is large where the rotation is large, and it is zero where $\omega = 0$. The factor $\Delta x$ makes the force go to zero as the grid is refined, which is the paper's reason to call the method consistent with the Euler equations.

**Units.** $\Delta x\, |\omega|$ has the units of a velocity. For $\mathbf f$ to be a force per unit mass, $\varepsilon$ must have the units $1/\mathrm{s}$. The paper says only that $\varepsilon > 0$ controls the amount of detail.

**Order in the step.** The paper multiplies each force by the time step and adds it to the velocity, then advects, then solves for the pressure. The pressure projection removes the part of $\mathbf f$ that is a gradient. Around a swirl, $\mathbf f$ goes along the flow, so it has a positive circulation around the center, and a gradient field has none. That part stays.

**Cost.** Each of lines L1 to L5 visits every cell or face once with a constant number of neighbors, so the force costs $\Theta(n)$ time and $\Theta(n)$ extra space on a grid of $n$ cells. This is small next to the pressure solve.

## Classic examples

**A hand computation.** Let $\Delta x = 0.1$ m, $\varepsilon = 2\ \mathrm{s}^{-1}$, and at one cell let $\omega = 3\ \mathrm{s}^{-1}$ (counterclockwise) with $\mathbf N = (-1, 0)$: the center of the swirl is to the left. Then $\mathbf N \times \omega = (N_y \omega, -N_x \omega) = (0, 3)$ and $\mathbf f = 2 \cdot 0.1 \cdot (0, 3) = (0, 0.6)\ \mathrm{m/s^2}$. A counterclockwise swirl moves upward on its right side, so the force goes with the flow. With $\Delta t = 0.05$ s, the vertical velocity at that cell grows by $0.03$ m/s.

**Solid body rotation.** For $\mathbf u = (-(y - 1/2),\ x - 1/2)$, $\omega = 2$ at every cell, and central differences give it to rounding error. So $\boldsymbol\eta = 0$ and the force is zero. A flow that turns as one rigid body has no concentrated swirl, so the method leaves it alone. The tests check $|\omega - 2| < 10^{-12}$ and $|\mathbf f| < 10^{-9}$ on a $20 \times 20$ grid.

**A Gaussian vortex on a coarse grid.** The test file puts a vortex with a Gaussian profile, $\sigma = 0.12$, on a $20 \times 20$ grid of the unit square with walls, and runs 10 steps of $\Delta t = 0.05$ with semi-Lagrangian advection and projection. The kinetic energy at the end, as a fraction of the start, was

| $\varepsilon$ ($\mathrm{s}^{-1}$) | 0 | 1 | 3 |
|---|---|---|---|
| energy kept | 0.650 | 0.792 | 1.150 |

Without the force, the solver loses a third of the energy in 10 steps. With $\varepsilon = 1$ it loses a fifth. With $\varepsilon = 3$ the flow ends with more energy than it started with. These are measurements of this code, not general bounds.

**Smoke.** Fedkiw, Stam and Jensen (2001) add the force to a solver in the style of [stable fluids](/stable-fluids/) on a [MAC grid](/mac-grid/), together with [buoyancy](/boussinesq-buoyancy/), and show the rolling motion that it keeps on grids that are coarse even for graphics.

**Fire.** The [fire method](/fire-simulation/) of Nguyen, Fedkiw and Jensen (2002) adds the same force, with separate values of $\varepsilon$ for the fuel and for the hot products.

## Variations

- **Steinhoff's original form.** Steinhoff and Underhill (1994) added a confinement term to the Euler equations for vortices around rotors. The 2001 paper describes it as similar to its equation 11 but without the factor $h$.
- **3D.** The equations are the same, with $\omega$ a vector. Then $\mathbf N \times \boldsymbol\omega$ needs all three components of $\omega$ at each cell.
- **On particles.** Particle methods estimate $\omega$ and $\boldsymbol\eta$ from sums over neighbors and apply the force to each particle. [Position based fluids](/position-based-fluids/) (Macklin and Müller 2013) do this to give back energy that the position solver removes.
- **Vortex particles.** Selle, Rasmussen and Fedkiw (2005) carry vorticity on particles, where advection does not damp it, and give it back to the grid by a force of the same kind. This keeps swirls that the grid alone has already lost. See the [vortex particle method](/vortex-particle-method/).
- **Less dissipative advection.** [BFECC](/bfecc/) and the [unconditionally stable MacCormack method](/unconditionally-stable-maccormack/) attack the cause by making advection more accurate. They can be used with or without confinement.

## Pitfalls

- **Dividing by a zero gradient.** Where $|\omega|$ is flat, $\boldsymbol\eta$ is rounding noise, and $\boldsymbol\eta / |\boldsymbol\eta|$ is a unit vector in a random direction. For solid body rotation with $\delta = 0$, the test file measures a force of exactly $\varepsilon\, \Delta x\, |\omega|$ at some cell, where the true force is zero. Add a small $\delta$, here $10^{-6} \max|\omega| / \Delta x$.
- **Too large a strength.** The force adds energy and nothing in it limits the growth. The paper says that the method is stable as long as the force stays below a certain threshold. The table above shows a run that gains 15% of its energy with $\varepsilon = 3$. Tune $\varepsilon$ on the grid and time step of the final shot.
- **It amplifies every peak.** The force spins up any local peak of $|\omega|$, of either sign. Around a Gaussian vortex there is a ring of opposite vorticity, and the test file finds that the force there points against the main flow. Noise in the velocity is also a set of small peaks.
- **It cannot make new detail.** The force strengthens rotation that the grid still holds. A swirl that the advection has already smoothed away does not come back. This is the motivation of the vortex particle variation above.
- **No claim of accuracy.** The term changes the equations. The result is a flow with more swirls, and the method does not claim that it is closer to the true flow.

## Exercises

1. Show that the force is zero for any flow whose vorticity is the same at every point. *Answer:* then $|\omega|$ is constant, $\boldsymbol\eta = \nabla|\omega| = 0$, and $\mathbf N = 0 / (0 + \delta) = 0$, so $\mathbf f = 0$.
2. Show that $\mathbf f \cdot \boldsymbol\eta = 0$, and that $|\mathbf f| = \varepsilon\, \Delta x\, |\omega|\, |\boldsymbol\eta| / (|\boldsymbol\eta| + \delta)$ in 2D. *Answer:* $\mathbf f$ is a multiple of $(N_y, -N_x)$, which is at right angles to $\mathbf N$ and so to $\boldsymbol\eta$, and $|(N_y \omega, -N_x \omega)| = |\mathbf N|\, |\omega|$.
3. At a cell with $\omega = -4\ \mathrm{s}^{-1}$ (clockwise), $\mathbf N = (0, 1)$, $\varepsilon = 0.5\ \mathrm{s}^{-1}$ and $\Delta x = 0.2$ m, find $\mathbf f$. *Answer:* $\mathbf N \times \omega = (1 \cdot (-4), -0 \cdot (-4)) = (-4, 0)$ and $\mathbf f = 0.5 \cdot 0.2 \cdot (-4, 0) = (-0.4, 0)\ \mathrm{m/s^2}$. The center is above the cell, and a clockwise swirl moves to the left below its center, so the force goes with the flow.
4. Why does the pressure projection not remove the force around a swirl? *Answer:* the projection removes exactly the gradient part. The force goes along the flow around the center, so its integral around a circle about the center is positive, while the integral of a gradient around a closed curve is zero.

## References
