---
tag: 4DDRB0
kind: algorithm
slug: stable-fluids
name: Stable fluids
aliases:
- Stam stable fluids
area: graphics-and-signals/fluid-animation
level: core
summary: Advance a grid fluid by semi-Lagrangian advection, implicit diffusion and pressure projection. It is stable for any time step, but first order and dissipative, so stable is not accurate.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {g: "the number of grid cells", k: "the number of conjugate gradient iterations of a solve"}
  time: {advect: "Θ(g)", diffuse: "O(g k)", project: "O(g k)", step: "O(g k)"}
  space: {extra: "Θ(g)"}
properties: {deterministic: true, exact: false, unconditionally_stable: true, conservative: false}
history:
  year: 1999
  people: [Jos Stam]
  note: Stam combined semi-Lagrangian advection, implicit diffusion and a pressure projection into a solver with no limit on the time step, at SIGGRAPH 1999.
prereqs: [mac-grid, navier-stokes-equations, method-of-characteristics, backward-euler-method]
see_also: [bfecc, unconditionally-stable-maccormack, vorticity-confinement, boussinesq-buoyancy, chorin-projection-method, helmholtz-hodge-decomposition, foster-metaxas-fluids, fluid-implicit-particle]
sources:
  - paper: doi:10.1145/311535.311548
    title: "Jos Stam, Stable fluids, Proceedings of SIGGRAPH 99, 121-128, 1999"
    locator: "the solver (add force, advect, diffuse, project), the stability argument, and the FFT solve on a periodic domain"
  - paper: doi:10.1145/383259.383260
    title: "Ronald Fedkiw, Jos Stam and Henrik Wann Jensen, Visual simulation of smoke, SIGGRAPH 2001, 15-22"
    locator: Section 4, the semi-Lagrangian solver on the staggered grid
  - book: isbn:9781482232837
    title: "Robert Bridson, Fluid Simulation for Computer Graphics, second edition, CRC Press, 2015"
    locator: the chapters Advection Algorithms and Making Fluids Incompressible
---

Stable fluids is the grid fluid solver of Jos Stam (1999). Each time step adds the forces, moves the velocity along itself by semi-Lagrangian advection, diffuses it by an implicit step, and projects it onto the divergence-free fields. None of the four parts has a limit on the time step, so the solver does not blow up at any $\Delta t$. That made interactive fluids possible and made the method the base of most grid solvers for smoke and fire in animation. The price is accuracy: the advection is first order and smooths the flow, so a stable step is not an accurate step.

## In plain words

Each frame, the solver does four things to the velocity on a grid.

First it adds the pushes, such as gravity or a fan. Then it moves the flow along itself. For each grid point it asks where the fluid there came from, walks back along the flow, and reads the old value at that spot by mixing the four nearest grid values. A mix of old values can never be larger than the largest old value, so nothing can grow without limit, whatever the step size.

Next it spreads the velocity a little to model friction inside the fluid. It solves for the spread state at the end of the step, which also cannot grow.

Last it removes the part of the flow that would squeeze or stretch the fluid, so the fluid keeps its volume. Smoke and other quantities then ride along on the new flow.

## The problem

Given a velocity field $\mathbf u$ on a grid, a density $\rho$, a viscosity $\nu$, a force field $\mathbf f$ and a time step $\Delta t$, compute the velocity at the next step for the incompressible [Navier-Stokes equations](/navier-stokes-equations/)

$$\frac{\partial \mathbf u}{\partial t} = -(\mathbf u \cdot \nabla)\mathbf u - \frac{1}{\rho}\nabla p + \nu \nabla^2 \mathbf u + \mathbf f, \qquad \nabla \cdot \mathbf u = 0,$$

and move the passive scalars $s$ (smoke density, temperature) by $\partial s / \partial t = -\mathbf u \cdot \nabla s + \kappa \nabla^2 s - a_s s$. The goal of [fluid simulation for animation](/fluid-simulation-for-animation/) is plausible motion at the step that the frame rate or the artist sets, without a limit from the grid. The output must stay bounded and divergence free for any $\Delta t$.

## The algorithm

The step splits the equation into four parts and solves each part by a method that is stable on its own. The order is the one of Stam's paper: force, advect, diffuse, project. This page uses the [MAC grid](/mac-grid/) layout, with $u$ on the vertical faces, $v$ on the horizontal faces and $p$ and the scalars at the cell centers, as Fedkiw, Stam and Jensen (2001) did for smoke. Stam's 1999 paper stored all components at the cell centers and solved the projection with the [fast Fourier transform](/fast-fourier-transform/) on a periodic domain, or with a fast Poisson solver for fixed walls.

```pseudo id=main
STABLE-FLUIDS-STEP(u, v, s, dt)
L1  add dt f(x) to the velocity at each face center x
L2  for each sample point x of u, v: x_b <- x - dt U(x - (dt/2) U(x))    ▷ RK2 backtrace
L3      new value at x <- bilinear sample of the old field at x_b, clamped to the grid
L4  for each of u and v: solve (I + alpha L) w = (advected field), alpha = nu dt / dx^2
L5  set the normal velocity to 0 on each face with a SOLID side
L6  build A p = b on the FLUID cells, b = -(rho dx / dt) (net outflow of the cell)
L7  solve A p = b by conjugate gradients; on a closed region remove the mean of b, then of p
L8  on each open face: u <- u - dt / (rho dx) (pressure difference across the face)
L9  for each scalar s: advect by L2 and L3, diffuse with kappa by L4, then s <- s / (1 + dt a_s)
```

**Forces (L1).** This is one forward Euler step of $\partial \mathbf u / \partial t = \mathbf f$. With a bounded force it adds at most $\Delta t \max |\mathbf f|$ to each face. [Buoyancy](/boussinesq-buoyancy/) and [vorticity confinement](/vorticity-confinement/) enter here.

**Advection (L2, L3).** The term $-(\mathbf u \cdot \nabla)\mathbf u$ says that velocity is carried along by the flow. Along a path $\mathbf x(t)$ with $d\mathbf x / dt = \mathbf u$, the value stays the same, which is the [method of characteristics](/method-of-characteristics/). So the new value at a sample point is the old value at the point that reaches it after $\Delta t$. Line L2 finds that point by one midpoint step backward in time; line L3 reads the old field there by bilinear interpolation. Each component uses its own sample points and offsets. The old velocity moves itself: all backtraces use the field from before the advection. This is the semi-Lagrangian method: the grid stays fixed (Eulerian), and each value is found by a Lagrangian trace.

**Diffusion (L4).** This is one [backward Euler](/backward-euler-method/) step of the [heat equation](/heat-equation/) $\partial w / \partial t = \nu \nabla^2 w$ for each component, with the 5-point graph Laplacian $L$ of the array. The matrix $I + \alpha L$ is symmetric positive definite, and conjugate gradients solve it. Smoke usually uses $\nu = 0$ and skips the step, because the advection already smooths more than the physical viscosity of air.

**Projection (L5 to L8).** Line L5 closes the walls. Lines L6 and L7 solve the pressure [Poisson equation](/poisson-equation/), and line L8 subtracts the pressure gradient, so every FLUID cell has zero net outflow. This is the [Chorin projection](/chorin-projection-method/), and the field that results is the divergence-free part of the [Helmholtz-Hodge decomposition](/helmholtz-hodge-decomposition/) of the discrete field. The MAC grid page derives the matrix; the slug file writes it out again.

**Scalars (L9).** A scalar moves with the new velocity by the same advection, diffuses with the coefficient $\kappa$, and fades by $s / (1 + \Delta t\, a_s)$, which is backward Euler for $ds/dt = -a_s s$ as in Stam's paper.

## Example

**One advection step by hand.** Take a row of five cells with $\Delta x = 1$ m, a constant velocity $u = 1$ m/s and $\Delta t = 1.5$ s, so the CFL number is $1.5$. The scalar is $s = (0, 0, 1, 0, 0)$. Positions below are in cell index units. The foot of cell $a$ is $1.5$ cells to the left, halfway between cells $a - 2$ and $a - 1$, so the new value is $\frac12 s_{a-2} + \frac12 s_{a-1}$:

| cell | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| before | 0 | 0 | 1 | 0 | 0 |
| foot of the backtrace | -1.5 (clamped to 0) | -0.5 (clamped to 0) | 0.5 | 1.5 | 2.5 |
| after | 0 | 0 | 0 | 0.5 | 0.5 |

The exact solution moves the spike to the position $3.5$, between two cells. The grid cannot hold it there, so the spike splits into two halves. No value is larger than 1 and no value is negative, at any step size. The same mixing at every step is the numerical diffusion of the method.

**One diffusion step by hand.** Two cells with $w = (1, 0)$ and $\alpha = 1$. The system is $\begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix} w' = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$, so $w' = (\tfrac23, \tfrac13)$. The sum stays 1, the values stay in $[0, 1]$, and the sum of squares drops from 1 to $\tfrac59$. As $\alpha$ grows, $w'$ tends to $(\tfrac12, \tfrac12)$, never past it.

**First order, measured.** A Gaussian bump with $\sigma = 0.1$ m moves by $0.3125$ m with $u = 1$ m/s at the CFL number $2.5$ on grids of 8, 16 and 32 cells over 1 m. The largest errors are $0.154$, $0.0887$ and $0.0444$. The error halves when the grid spacing halves: the observed order between 16 and 32 cells is $1.00$. The proof page gives the bound $T u \Delta x \phi(1 - \phi) K / (2c) \approx 0.0488$ for 32 cells, where $\phi = 0.5$ is the fractional part of the CFL number and $K = 100$ bounds the second derivative.

**A large step, measured.** On a 16 by 16 box with $\Delta x = 1/16$ m, a random divergence-free velocity from `random.Random(11)` (largest face speed $1.08$ m/s) and a square of smoke, ten steps with $\Delta t = 0.29$ s, a CFL number of 5, run without trouble. After each step the largest divergence is below $10^{-8}$ (it is $2.9 \times 10^{-13}$ at the end). The kinetic energy drops at every step, from $0.150$ J to $0.0396$ J after one step and to $0.0021$ J after ten, per unit depth with $\rho = 1$. The smoke stays in $[0, 1]$, but its total grows from 16 to 16.84, because semi-Lagrangian advection does not conserve mass. The run is stable and also very wrong: an inviscid fluid in a closed box keeps its energy.

## Correctness

The claims are about the discrete step. They are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Advection.** Each new value is a convex combination of four old values, for any velocity and any $\Delta t$. A constant field stays the same, and the values stay between the old minimum and maximum.
2. **Diffusion.** The backward Euler step keeps the sum of the array, keeps the values between the old minimum and maximum, and does not increase the sum of squares, for any $\alpha \ge 0$.
3. **Projection.** After lines L5 to L8, every FLUID cell has zero divergence, and the kinetic energy has not increased. The projection is orthogonal in the inner product $\sum u^2 + \sum v^2$.
4. **One step.** With no force, the velocity after a step is bounded by a bound that depends on the old velocity and the number of faces, but not on $\Delta t$ or $\nu$. Each scalar stays inside its old range times $1 / (1 + \Delta t\, a_s)$.
5. **Order.** For a constant velocity and a smooth field, the advection error after a fixed time is $O(\Delta x)$ at a fixed CFL number. The leading error is a diffusion term. Away from a whole number of cells per step, the method is first order in space and time.

The tests check the advection, the interpolation and the projection of the slug file against the shared helper `macgrid.py` on the same input. They also check diffusion against a dense solve and its sum, bound and energy properties, the measured order, and the bounded run at a CFL number of 5.

## Complexity

Let $g$ be the number of cells. Lines L1 to L3, L5, L8 and the scalar advection cost $\Theta(g)$: each face or cell does a constant amount of work, and the backtrace and the sample cost $O(1)$ each. The extra space is $\Theta(g)$ for the new fields and the solver vectors.

The linear solves dominate. A conjugate gradient iteration costs $\Theta(g)$ on a 5-point matrix, so each solve costs $O(g k)$. For the pressure on an $N$ by $N$ grid, $k = O(N)$ for a fixed reduction of the error, because the condition number of $A$ grows as $N^2$; [multigrid](/multigrid-method/) brings the solve to $O(g)$. For the diffusion, the condition number of $I + \alpha L$ is at most $1 + 8\alpha$, so the solve is cheap when $\alpha$ is small and approaches the cost of a Poisson solve when $\alpha$ is large. Stam's periodic version replaces both solves by FFTs, which cost $O(g \log g)$.

## Properties

- **No step limit.** The [CFL condition](/courant-friedrichs-lewy-condition/) does not limit $\Delta t$, because the backtrace may cross many cells. Large steps lose accuracy, not stability. Many solvers still keep the CFL number at a few cells per step, as a rule of thumb for accuracy.
- **Dissipative.** Linear interpolation smooths the field at every step, with an effective viscosity of order $u\,\Delta x$. Smoke loses its small swirls, and the total kinetic energy decays even with $\nu = 0$. [Vorticity confinement](/vorticity-confinement/), [BFECC](/bfecc/) and the [unconditionally stable MacCormack method](/unconditionally-stable-maccormack/) are the usual repairs.
- **Not conservative.** The sum of an advected scalar is not kept. Smoke mass and liquid volume drift over time.
- **First order.** The splitting is first order in time, and the advection is first order at a fixed CFL number.
- **Simple and robust.** Every part is either a convex combination or a symmetric positive (semi)definite solve.

## Variants and improvements

- **Collocated grid with FFT.** Stam's original form, with all components at the cell centers and the diffusion and the projection done in Fourier space on a periodic domain, where both are diagonal.
- **A version for games.** Stam later published a short version for games (2003) that relaxes the linear systems with a fixed number of [Gauss-Seidel](/gauss-seidel-method/) sweeps. It is cheaper and less accurate than a converged solve.
- **Staggered grid.** The MAC layout of this page (Fedkiw, Stam and Jensen 2001), which avoids the checkerboard modes of the collocated projection.
- **Less dissipation.** Higher order interpolation (monotone cubic), [BFECC](/bfecc/), the [unconditionally stable MacCormack method](/unconditionally-stable-maccormack/), and particle methods such as [FLIP](/fluid-implicit-particle/) and [APIC](/affine-particle-in-cell/) that do not interpolate the velocity at every step.
- **Liquids.** Add a free surface tracked by a [level set](/level-set-method/) or particles, AIR cells with $p = 0$ and the [ghost fluid method](/ghost-fluid-method/) at the surface.
- **Better splitting.** Advection-reflection methods reflect the velocity at the half step instead of only projecting it. They lose less energy, at the cost of a second projection.

## When to use it

Use stable fluids for smoke, fire, dust and other gases in animation and games, where the step is set by the frame rate and the look matters more than the accuracy. It is also the base for liquid solvers and the grid stage of particle-grid hybrids. It is easy to write, easy to run on a GPU, and robust.

Do not use it where accuracy matters: in engineering flow, for drag or heat transfer, or where mass must be conserved. Use a conservative [finite volume method](/finite-volume-method/) with a step inside the CFL limit there. For thin liquid sheets, splashes and small features, the numerical diffusion is too strong; use particles.

## Pitfalls

- **Stable is not accurate.** A step at a CFL number of 5 runs, but it can lose most of the kinetic energy in a few steps, as the measured run shows. Pick $\Delta t$ for accuracy, not only for stability.
- **Advecting in place.** The backtraces must use the velocity from before the step. Writing the new values into the same arrays during the sweep mixes old and new values.
- **Half-cell offsets.** On a MAC grid, $u$, $v$ and the scalars have different sample points. Trace from the sample point of each component and sample with its offsets.
- **Boundaries.** A backtrace that leaves the domain must read a boundary value. Clamping returns the nearest sample, which is right for a wall and wrong for an inflow with a given value.
- **The order of the steps.** Advect with a divergence-free field. A force added after the projection is not projected and adds divergence to the next advection.
- **Diffusing walls.** The diffusion of this page treats the border of each array with a zero normal derivative. A no-slip wall needs zero velocity at the wall in the diffusion step, not only in the projection.
- **The singular pressure system.** A closed box has a free constant in $p$. Remove the mean of $b$ before conjugate gradients, or the solve stalls.

## Implementations

## History

Jos Stam presented stable fluids at SIGGRAPH 1999. Earlier animation solvers, such as the one of [Foster and Metaxas](/foster-metaxas-fluids/) (1996), were explicit and had to keep the step small. Stam made the advection semi-Lagrangian, a method known from weather prediction, made the diffusion implicit, and kept Chorin's projection. He showed that no part limits the step. In 2001, Fedkiw, Stam and Jensen moved the method to the staggered grid, added vorticity confinement, and used it for smoke. Later work kept the structure of the step and replaced the parts: higher order advection, particle velocities, and faster pressure solvers.

## References
