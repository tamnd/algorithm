---
tag: ZA2F6K
kind: concept
slug: eulerian-and-lagrangian-viewpoints
name: Eulerian and Lagrangian viewpoints
aliases:
- Eulerian versus Lagrangian
area: graphics-and-signals/fluid-animation
level: intro
summary: "Describe a fluid by values at fixed points of space, or by values carried with the moving fluid; grids follow the first view, particles the second, and the material derivative links them."
prereqs: [advection-equation]
see_also: [fluid-simulation-for-animation, mac-grid, marker-and-cell-method, method-of-characteristics, stable-fluids, smoothed-particle-hydrodynamics, particle-in-cell, material-point-method]
sources:
  - book: isbn:9781482232837
    title: "Robert Bridson, Fluid Simulation for Computer Graphics, second edition, CRC Press, 2015"
    locator: the chapter The Equations of Fluids (the Lagrangian and Eulerian viewpoints and the material derivative) and the chapter Advection Algorithms
  - book: isbn:9780521663960
    title: "G. K. Batchelor, An Introduction to Fluid Dynamics, Cambridge University Press, 1967 (paperback 2000)"
    locator: chapter 2, the kinematics of the flow field (the two descriptions and the rate of change following a material element)
  - paper: doi:10.1063/1.1761178
    title: "Francis H. Harlow and J. Eddie Welch, Numerical calculation of time-dependent viscous incompressible flow of fluid with free surface, The Physics of Fluids 8(12), 2182-2189, 1965"
    locator: the marker and cell method, an Eulerian grid with Lagrangian marker particles
  - paper: doi:10.1146/annurev.aa.30.090192.002551
    title: "J. J. Monaghan, Smoothed particle hydrodynamics, Annual Review of Astronomy and Astrophysics 30, 543-574, 1992"
    locator: a fully Lagrangian method, the equations written with the derivative that follows the particle
  - paper: doi:10.1145/311535.311548
    title: "Jos Stam, Stable fluids, Proceedings of SIGGRAPH 1999, 121-128"
    locator: the advection step that stores values on a grid and traces each grid point back along the flow
---

A fluid can be described in two ways. In the Eulerian view, you stand at fixed points of space and record what passes: the velocity, the temperature or the density at each point and time, as fields $q(\mathbf x, t)$. In the Lagrangian view, you ride on the bits of fluid and record what each one carries: its position, its velocity and its temperature, as functions of time for each bit. Both views describe the same flow. The material derivative $D/Dt = \partial/\partial t + \mathbf u \cdot \nabla$ converts between them: it is the rate of change seen by a bit of fluid, written with Eulerian fields. In simulation, the Eulerian view leads to grids, the Lagrangian view leads to particles, and many methods for animation mix the two, because each view makes a different part of the work easy.

## In plain words

Think of a river. You can stand on a bridge and measure how fast the water passes under one spot. That is the Eulerian view: the spot stays, the water moves through it.

Or you can drop a cork in the water and follow it, writing down where it goes and how fast. That is the Lagrangian view: you move with the water.

The two give different answers to the question "how fast does the temperature change?". On the bridge, the temperature may stay the same all day, while the cork drifts from cold water into warm water and feels it heat up. The material derivative adds the change at the spot to the change from moving. A computer keeps fluid either on a fixed grid, like many bridges, or on moving particles, like many corks.

## The idea

**Two descriptions.** An Eulerian field gives a quantity $q(\mathbf x, t)$ at each point $\mathbf x$ of space and each time $t$. A Lagrangian description labels each bit of fluid, for example by its position $\mathbf a$ at time 0, and follows its path $\mathbf X(\mathbf a, t)$, with

$$\frac{\partial \mathbf X}{\partial t}(\mathbf a, t) = \mathbf u(\mathbf X(\mathbf a, t), t), \qquad \mathbf X(\mathbf a, 0) = \mathbf a.$$

The quantity that the bit $\mathbf a$ carries is $Q(\mathbf a, t) = q(\mathbf X(\mathbf a, t), t)$.

**The material derivative.** The chain rule gives the rate of change that the bit sees:

$$\frac{\partial Q}{\partial t}(\mathbf a, t) = \frac{\partial q}{\partial t} + \frac{\partial \mathbf X}{\partial t} \cdot \nabla q = \Big(\frac{\partial q}{\partial t} + \mathbf u \cdot \nabla q\Big)(\mathbf X(\mathbf a, t), t).$$

The operator in the bracket is the material derivative,

$$\frac{Dq}{Dt} = \frac{\partial q}{\partial t} + \mathbf u \cdot \nabla q.$$

The first term is the change at a fixed point. The second is the change that comes from moving through a field that differs from place to place. For a vector, $D\mathbf u / Dt = \partial \mathbf u / \partial t + (\mathbf u \cdot \nabla)\, \mathbf u$ is the acceleration of a bit of fluid. The momentum equation of the [Navier-Stokes equations](/navier-stokes-equations/) is Newton's law for a bit of fluid, $\rho\, D\mathbf u / Dt = -\nabla p + \mu \nabla^2 \mathbf u + \mathbf f$.

**Laws in both views.** A quantity that each bit keeps satisfies $Dq/Dt = 0$. In Eulerian form this is the [advection equation](/advection-equation/) $\partial q / \partial t + \mathbf u \cdot \nabla q = 0$, and in Lagrangian form it says only that $Q(\mathbf a, t)$ does not change. Conservation of mass reads $D\rho / Dt + \rho\, \nabla \cdot \mathbf u = 0$. So a flow in which each bit keeps its density is exactly a flow with $\nabla \cdot \mathbf u = 0$, the incompressible flows of most animation solvers.

**From views to methods.** Each view makes some steps easy and others hard.

- *Eulerian grids.* Neighbors are fixed, so differences, the pressure [Poisson equation](/poisson-equation/) and boundary conditions on walls are simple. Advection is hard: the term $\mathbf u \cdot \nabla q$ moves values across a fixed grid, an explicit scheme must respect the [CFL condition](/courant-friedrichs-lewy-condition/), and interpolation smooths the values at each step. A free surface is not on the grid and needs a [level set](/level-set-method/) or another marker.
- *Lagrangian particles.* Advection is trivial: move each particle with its velocity, and $Dq/Dt = 0$ holds exactly. The mass is where the particles are, and a free surface comes for free. But particles have no fixed neighbors, so each step must find them, and incompressibility and pressure are harder to impose.
- *Hybrids.* Particles carry the fluid, and a grid solves for the pressure. This uses each view for what it does well, at the cost of transfers between them, which can smooth or add noise.
- *Semi-Lagrangian advection.* Values stay on a grid, but each grid point is traced back along the flow for one step by the [method of characteristics](/method-of-characteristics/), and the value at the start point is interpolated. The step is Lagrangian in thought and Eulerian in storage.

## Examples

**A steady field and a warming particle.** Let air move along $x$ at $u = 2$ m/s through the steady temperature field $T(x) = 300 + 5x$ (K, with $x$ in m). At every fixed point, $\partial T / \partial t = 0$: a thermometer on a post reads a constant. A bit of air that starts at $x_0$ is at $x_0 + 2t$, and its temperature is $300 + 5 (x_0 + 2t)$, so it warms at $10$ K/s. The material derivative gives the same: $DT/Dt = 0 + 2 \cdot 5 = 10$ K/s.

**A carried pattern.** Let $T(x, t) = f(x - ut)$ for any profile $f$ and constant $u$. At a fixed point, $\partial T / \partial t = -u f'$, which is not zero. Along a bit of fluid, $x - ut$ is constant, so the bit keeps its temperature. Check: $DT/Dt = -u f' + u f' = 0$. The pattern moves; nothing in it changes.

**A steady flow that accelerates.** Let $u(x) = k x$ with $k = 1\ \mathrm{s}^{-1}$, which does not depend on time. At each fixed point, $\partial u / \partial t = 0$. But a bit of fluid at $x_0$ follows $x(t) = x_0 e^{k t}$, and its acceleration is $k^2 x_0 e^{k t} = k^2 x$. The material derivative gives $Du/Dt = 0 + u\, \partial u / \partial x = k x \cdot k = k^2 x$. At $x = 3$ m, both give $3$ m/s². A steady Eulerian field does not mean that the fluid is not accelerating.

**One semi-Lagrangian step by hand.** On a 1D grid with spacing 1, let $T = (0, 0, 10, 0, 0)$ at the points $0, \dots, 4$, with $u = 0.5$ and $\Delta t = 1$. Each point $x_i$ traces back to $x_i - 0.5$ and takes the linear interpolation there, which is the mean of $T_{i-1}$ and $T_i$. The result is $(0, 0, 5, 5, 0)$. A particle carrying the value 10 would still carry 10, now at $x = 2.5$. The sum is the same, 10, but the peak has dropped by half. This smoothing at every step is the numerical dissipation of grid advection, which [BFECC](/bfecc/) and [vorticity confinement](/vorticity-confinement/) try to reduce or hide.

## Where it is used

- **Grid (Eulerian) methods.** [Stable fluids](/stable-fluids/) and the [Foster-Metaxas method](/foster-metaxas-fluids/) store the velocity on the [MAC grid](/mac-grid/). The [level set method](/level-set-method/) and the [volume of fluid method](/volume-of-fluid-method/) track a liquid surface with Eulerian fields. [Height field water](/height-field-water/) and the [shallow water equations](/shallow-water-equations/) are Eulerian in two dimensions. In scientific computing, the [finite volume method](/finite-volume-method/) is the usual Eulerian discretization.
- **Particle (Lagrangian) methods.** [Smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/), [weakly compressible SPH](/weakly-compressible-sph/), [position based fluids](/position-based-fluids/) and the [vortex particle method](/vortex-particle-method/) carry the fluid on particles.
- **Hybrid methods.** The [marker and cell method](/marker-and-cell-method/) moves marker particles through an Eulerian grid to tell fluid from air. The [particle in cell method](/particle-in-cell/), [FLIP](/fluid-implicit-particle/), [APIC](/affine-particle-in-cell/) and the [material point method](/material-point-method/) carry the state on particles and solve on a grid. The [particle level set method](/particle-level-set/) uses particles to correct an Eulerian level set.
- **Semi-Lagrangian advection.** [Stable fluids](/stable-fluids/), [BFECC](/bfecc/) and the [unconditionally stable MacCormack method](/unconditionally-stable-maccormack/) trace grid points back along the flow.
- **The problem.** [Fluid simulation for animation](/fluid-simulation-for-animation/) lists the methods in both views and what they cost.

## References
