---
tag: 8ERT4C
kind: problem
slug: fluid-simulation-for-animation
name: Fluid simulation for animation
aliases:
- fluid animation
area: graphics-and-signals/fluid-animation
level: core
summary: "Produce plausible, controllable motion of smoke, fire and liquids from a domain, sources and boundaries, stable at the large time steps of animation, rather than accurate motion."
prereqs: [navier-stokes-equations, poisson-equation]
see_also: [eulerian-and-lagrangian-viewpoints, stable-fluids, mac-grid, finite-volume-method, smoothed-particle-hydrodynamics, fluid-implicit-particle, rigid-body-simulation-problem, particle-system]
sources:
  - book: isbn:9781482232837
    title: "Robert Bridson, Fluid Simulation for Computer Graphics, second edition, CRC Press, 2015"
    locator: "the chapters The Equations of Fluids and Overview of Numerical Simulation (the equations, the splitting into advection, forces and projection, and the time step), and the later chapters on smoke, water and fire"
  - paper: doi:10.1006/gmip.1996.0039
    title: "Nick Foster and Dimitri Metaxas, Realistic animation of liquids, Graphical Models and Image Processing 58(5), 471-483, 1996"
    locator: the first full 3D Navier-Stokes liquids in graphics, with explicit steps limited by the CFL condition
  - paper: doi:10.1145/311535.311548
    title: "Jos Stam, Stable fluids, Proceedings of SIGGRAPH 1999, 121-128"
    locator: the goal of stability at any time step, and the semi-Lagrangian advection with a pressure projection
  - paper: doi:10.1145/383259.383260
    title: "Ronald Fedkiw, Jos Stam and Henrik Wann Jensen, Visual simulation of smoke, Proceedings of SIGGRAPH 2001, 15-22"
    locator: the introduction and the section on vorticity confinement (a coarse grid with the lost swirls added back)
  - paper: doi:10.1145/566654.566645
    title: "Douglas Enright, Stephen Marschner and Ronald Fedkiw, Animation and rendering of complex water surfaces, ACM Transactions on Graphics 21(3), 736-744, 2002 (SIGGRAPH 2002)"
    locator: liquids with a free surface tracked by the particle level set method
  - paper: doi:10.1063/1.1761178
    title: "Francis H. Harlow and J. Eddie Welch, Numerical calculation of time-dependent viscous incompressible flow of fluid with free surface, The Physics of Fluids 8(12), 2182-2189, 1965"
    locator: the staggered grid and the marker particles that most grid solvers for animation still use
---

Fluid simulation for animation is the problem of making smoke, fire, water and other fluids move on screen. The input is a scene: a domain, the solids in it, the sources of fluid, smoke or heat, and forces such as gravity. The output is the state of the fluid at each frame, which a renderer turns into images. The motion should follow the [Navier-Stokes equations](/navier-stokes-equations/) closely enough to look like a fluid. But the goals differ from those of computational fluid dynamics in science and engineering. A solver for animation must stay stable at the large time steps that a frame rate allows, must run on grids that are coarse for the detail on screen, and must let an artist steer the result. It is not judged by its error against the true flow. This page defines the problem, lists the methods for it, and gives the costs that limit them.

## In plain words

A film needs smoke that curls, water that splashes and fire that flickers. Drawing them by hand is slow, so the computer computes them from the laws of fluids.

The computer cuts space into small cells, or fills the fluid with many particles. Each step it moves the fluid along its own velocity, adds forces such as gravity, and then fixes the velocity so that the fluid does not squeeze into a smaller volume.

An engineer who designs a wing wants the right numbers. An animator wants a result that looks right, does not blow up, and can be changed. So the methods for animation accept large errors in exchange for speed, stability and control. They also add back by hand some of the detail that the coarse grid loses.

## Definition

**Input.**

- A domain $\Omega \subset \mathbb R^d$ with $d = 2$ or $3$, and the solids in it, each with a given motion or with a mass that the fluid can push.
- For smoke and fire, the fluid fills $\Omega$. For a liquid, the initial liquid region $F(0) \subset \Omega$; the rest is air, which is usually left out of the solve.
- The initial velocity $\mathbf u_0$ on the fluid, and fields that the fluid carries, such as a smoke density $s$ and a temperature $T$.
- Sources: regions where fluid, smoke or heat enter with a given velocity, and external forces $\mathbf f$ such as gravity, [buoyancy](/boussinesq-buoyancy/) or forces that an artist adds.
- The density $\rho$, the viscosity $\mu$ (often 0 for gases), the frame times $t_1 < t_2 < \dots$ and a budget of computing time per frame.

**Output.** At each frame time $t_k$, the velocity $\mathbf u(\cdot, t_k)$, the carried fields, and for a liquid the region $F(t_k)$, given by a surface that a renderer can draw.

**Relation.** The output should approximately satisfy the incompressible Navier-Stokes equations on the fluid region,

$$\frac{\partial \mathbf u}{\partial t} + (\mathbf u \cdot \nabla)\, \mathbf u = -\frac{1}{\rho} \nabla p + \frac{\mu}{\rho} \nabla^2 \mathbf u + \mathbf f, \qquad \nabla \cdot \mathbf u = 0,$$

with $\partial q / \partial t + \mathbf u \cdot \nabla q = 0$ for each carried field $q$, the condition $\mathbf u \cdot \mathbf n = \mathbf u_{solid} \cdot \mathbf n$ on solid walls, and for a liquid $p = 0$ on the free surface, which moves with the fluid. The equations are in the [Eulerian view](/eulerian-and-lagrangian-viewpoints/); particle methods use the same equations in the Lagrangian view.

The requirements are not an error bound. A method should:

1. stay bounded for any time step that the user picks, at least as large as one frame, such as $1/24$ s, and often larger than the [CFL condition](/courant-friedrichs-lewy-condition/) of explicit schemes allows;
2. keep the fluid incompressible to a tolerance, so that a liquid keeps its volume;
3. be controllable, by parameters with a visible effect and by forces or targets;
4. give plausible motion, with the swirls and splashes that a viewer expects.

**Cost model.** The cost is the time per frame, counted as arithmetic operations on a grid of $n$ cells or a set of $n$ particles, and the memory. Each step costs at least $\Theta(n)$ to touch every cell or particle. The number of steps per frame depends on the time step that stability or accuracy allows.

**Against computational fluid dynamics.** A [finite volume](/finite-volume-method/) code in engineering solves the same equations, but its goal is a converged and validated answer. It refines the grid until the result stops changing, conserves mass and momentum exactly through the fluxes between cells, chooses the time step for accuracy, and compares with experiments. A solver for animation runs on a fixed coarse grid, takes the largest step that stays stable, uses advection schemes such as semi-Lagrangian tracing that are stable but neither conservative nor accurate, and then adds detail back with terms such as [vorticity confinement](/vorticity-confinement/) that change the equations. The smoke solver of Fedkiw, Stam and Jensen (2001) is built on this trade: it accepts a coarse grid and adds vorticity confinement to restore the small swirls that the grid loses.

## Variants

- **Smoke and gases.** The fluid fills the domain; the visible part is a carried density. Buoyancy drives the flow. The main methods are [stable fluids](/stable-fluids/) and its successors.
- **Liquids with a free surface.** The fluid region changes, and the method must track the surface between water and air, keep its volume and draw it. Tools are the [level set method](/level-set-method/), the [particle level set method](/particle-level-set/), the [volume of fluid method](/volume-of-fluid-method/) and particles.
- **Fire and explosions.** A reaction front, heat and expansion. See [fire simulation](/fire-simulation/).
- **Coupling with solids.** Solids that move the fluid and are moved by it, as in [variational solid-fluid coupling](/variational-solid-fluid-coupling/).
- **Large water surfaces.** Oceans and ponds where only the surface matters: [height field water](/height-field-water/), the [shallow water equations](/shallow-water-equations/) and [FFT ocean synthesis](/fft-ocean-synthesis/) replace the full 3D problem by a 2D one.
- **Real time against offline.** Games fix the time per frame and accept small grids. Film work fixes the look and accepts hours per frame.

## Examples

**A projection by hand.** Take two fluid cells side by side in a closed box, with $\Delta x = 1$ m, $\rho = 1$ kg/m³ and $\Delta t = 1$ s. The faces on the outer walls have $u = 0$, and the face between the cells has $u = 1$ m/s. The left cell has the divergence $+1$ and the right cell $-1$: fluid leaves the first and piles up in the second. The pressure equation $(\Delta t / (\rho \Delta x^2)) (p_0 - p_1) = -1$ for the left cell gives $p_1 - p_0 = 1$ Pa. The update $u \leftarrow u - (\Delta t / (\rho \Delta x)) (p_1 - p_0) = 1 - 1 = 0$. In a closed box of two cells in a row, the fluid has nowhere to go, and the [Chorin projection](/chorin-projection-method/) stops it.

**How many steps per frame.** Smoke moves at up to 3 m/s on a grid with $\Delta x = 0.05$ m, and the frame lasts $1/24$ s. In one frame the fluid crosses $3 \cdot (1/24) / 0.05 = 2.5$ cells. An explicit [upwind scheme](/upwind-scheme/) needs a CFL number of at most 1, so it needs 3 steps per frame. Semi-Lagrangian advection stays stable with 1 step, at the price of more smoothing.

**A pool at rest.** Water 0.5 m deep in a tank, with $\rho = 1000$ kg/m³ and $g = 9.81$ m/s², must stay at rest. The projection must return the pressure $\rho g h$, which is $4905$ Pa at the bottom, and zero velocity. A solver that sets a resting pool in motion fails the simplest check.

## Known algorithms

- **Grids and projection.** The [marker and cell method](/marker-and-cell-method/) of Harlow and Welch (1965) introduced the staggered [MAC grid](/mac-grid/) and marker particles. [Foster and Metaxas](/foster-metaxas-fluids/) (1996) brought it to graphics, with explicit steps limited by the CFL condition. [Stable fluids](/stable-fluids/) (Stam 1999) made the step stable for any $\Delta t$ with semi-Lagrangian advection along the [method of characteristics](/method-of-characteristics/) and a pressure projection.
- **The projection.** The [Chorin projection method](/chorin-projection-method/) removes the gradient part of the velocity, by the [Helmholtz-Hodge decomposition](/helmholtz-hodge-decomposition/). It solves a [Poisson equation](/poisson-equation/) for the pressure, usually with the [conjugate gradient method](/conjugate-gradient-method/) and a preconditioner, or with the [multigrid method](/multigrid-method/).
- **Less dissipative advection.** [BFECC](/bfecc/), the [MacCormack method](/maccormack-method/) and the [unconditionally stable MacCormack method](/unconditionally-stable-maccormack/).
- **Detail and forces.** [Vorticity confinement](/vorticity-confinement/), [Boussinesq buoyancy](/boussinesq-buoyancy/) and the [vortex particle method](/vortex-particle-method/).
- **Free surfaces.** The [level set method](/level-set-method/) with redistancing by the [fast marching method](/fast-marching-method/), the [particle level set method](/particle-level-set/), the [ghost fluid method](/ghost-fluid-method/) for the pressure at the surface and at other jumps, and [marching cubes](/marching-cubes/) to extract a mesh for rendering.
- **Particles and hybrids.** [Smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/) with its variants [WCSPH](/weakly-compressible-sph/), [PCISPH](/pcisph/), [IISPH](/implicit-incompressible-sph/) and [DFSPH](/divergence-free-sph/), [position based fluids](/position-based-fluids/), and the hybrids [PIC](/particle-in-cell/), [FLIP](/fluid-implicit-particle/), [APIC](/affine-particle-in-cell/) and the [material point method](/material-point-method/). Particle surfaces are built by [particle fluid surfacing](/particle-fluid-surfacing/).
- **Special cases.** [Fire](/fire-simulation/), [solid-fluid coupling](/variational-solid-fluid-coupling/), [height field water](/height-field-water/) and [FFT oceans](/fft-ocean-synthesis/).

## Bounds

All bounds are in the RAM model with real arithmetic, for one time step on a grid of $n$ cells in $d$ dimensions, or $n$ particles.

- **Lower bound.** Every method reads and writes each cell or particle, so a step costs $\Omega(n)$.
- **Advection and forces.** Semi-Lagrangian advection and the force terms cost $\Theta(n)$ per step.
- **The pressure solve.** The 5-point (7-point in 3D) Poisson matrix has a condition number of order $n^{2/d}$. Unpreconditioned conjugate gradients then need $O(n^{1/d})$ iterations for a fixed reduction of the error, so a solve costs $O(n^{1 + 1/d})$. Multigrid solves the model Poisson problem to a fixed accuracy in $O(n)$, which meets the lower bound. In practice the projection is the most expensive part of a grid step.
- **Steps per frame.** An explicit scheme needs at least $u_{max} \Delta t_{frame} / \Delta x$ steps per frame for stability. Semi-Lagrangian advection needs one step for stability, but the error grows with the step.
- **Particles.** With a uniform grid for the neighbor search and a bounded number of neighbors per particle, a step of SPH costs $O(n)$ expected time, plus the cost of the pressure iterations.

There is no lower bound on plausibility: the requirements are visual, and no theorem measures them.

## Reductions

- **Incompressibility to a linear system.** The projection reduces to the Poisson equation for the pressure, a [sparse](/sparse-matrix/) symmetric positive semidefinite system, definite when some cell borders air.
- **Surface tracking to advection.** A free surface is the zero set of a level set, which is moved by the [advection equation](/advection-equation/) and kept a [signed distance function](/signed-distance-function/) by solving an Eikonal equation.
- **Rendering to isosurfaces.** Drawing a liquid reduces to extracting an isosurface, for example with [marching cubes](/marching-cubes/).

## Applications

Visual effects for film and television use offline solvers on large grids or particle sets for smoke, explosions, fire and water. Games and interactive tools use small grids, particles or height fields at a fixed time per frame. The same solvers drive the motion of other phenomena that act like fluids, such as clouds, sand with the material point method, and crowds of particles in [particle systems](/particle-system/).

## References
