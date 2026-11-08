---
tag: ANY3EP
kind: algorithm
slug: lattice-boltzmann-method
name: Lattice Boltzmann method
aliases:
- LBM
- lattice BGK method
- D2Q9 lattice Boltzmann
area: numerical/differential-equations
level: research
summary: "Evolve particle populations f_i on a lattice: relax each node toward a local equilibrium (BGK, time tau), then stream to the neighbours. Recovers Navier-Stokes with nu = (tau - 1/2)/3 at low Mach."
solves: [navier-stokes-equations, heat-equation]
model: real-ram
complexity:
  vars: {M: "the number of lattice nodes", S: "the number of time steps", Q: "the number of lattice velocities, 9 for D2Q9"}
  time: {worst: "Θ(S Q M)"}
  space: {extra: "Θ(Q M)"}
properties: {deterministic: true, explicit: true, local_collision: true, conserves_mass_exactly: true, conserves_momentum_exactly: true, order_in_space: "2", weakly_compressible: true}
history:
  year: 1992
  people: [Yue-Hong Qian, Dominique d'Humières, Pierre Lallemand]
  note: "Grew out of lattice gas automata (Frisch, Hasslacher and Pomeau, 1986) through McNamara and Zanetti's Boltzmann version (1988); the single relaxation time (BGK) form on D2Q9 is due to Qian, d'Humières and Lallemand (1992) and to Chen, Chen and Matthaeus (1992)."
prereqs: [navier-stokes-equations, heat-equation, finite-difference-method]
see_also: [smoothed-particle-hydrodynamics, cellular-automaton, finite-volume-method, ftcs-method, lax-equivalence-theorem, boundary-conditions, method-of-characteristics, operator-splitting]
sources:
  - book: isbn:9783319446479
    title: "Timm Krüger, Halim Kusumaatmaja, Alexandr Kuzmin, Orest Shardt, Goncalo Silva and Erlend Magnus Viggen, The Lattice Boltzmann Method: Principles and Practice, Springer, 2017"
    locator: "Chapter 3 (the lattice Boltzmann equation, D2Q9 weights and equilibrium), Chapter 4 (Chapman-Enskog analysis), Chapter 5 (bounce-back and the Poiseuille slip) and Chapter 6 (forcing)"
  - paper: doi:10.1209/0295-5075/17/6/001
    title: "Y. H. Qian, D. d'Humières and P. Lallemand, Lattice BGK models for Navier-Stokes equation, Europhysics Letters 17 (1992) 479-484"
  - paper: doi:10.1103/PhysRevLett.61.2332
    title: "Guy R. McNamara and Gianluigi Zanetti, Use of the Boltzmann equation to simulate lattice-gas automata, Physical Review Letters 61 (1988) 2332-2335"
  - paper: doi:10.1103/PhysRevE.65.046308
    title: "Zhaoli Guo, Chuguang Zheng and Baochang Shi, Discrete lattice effects on the forcing term in the lattice Boltzmann method, Physical Review E 65 (2002) 046308"
  - paper: doi:10.1146/annurev.fluid.30.1.329
    title: "Shiyi Chen and Gary D. Doolen, Lattice Boltzmann method for fluid flows, Annual Review of Fluid Mechanics 30 (1998) 329-364"
  - paper: "Xiaoyi He, Qisu Zou, Li-Shi Luo and Micah Dembo, Analytic solutions of simple flows and analysis of nonslip boundary conditions for the lattice Boltzmann BGK model, Journal of Statistical Physics 87 (1997) 115-136"
---

The lattice Boltzmann method computes a fluid flow by evolving, at every node of a regular lattice, a small set of particle populations $f_i(x, t)$, one for each lattice velocity $c_i$, instead of the velocity and pressure themselves. One time step has two parts. **Collision** relaxes the populations at each node toward an equilibrium $f_i^{\mathrm{eq}}(\rho, u)$ built from the local density $\rho = \sum_i f_i$ and momentum $\rho u = \sum_i c_if_i$:

$$f_i^\ast = f_i - \frac1\tau\bigl(f_i - f_i^{\mathrm{eq}}\bigr) \qquad \text{(BGK)}.$$

**Streaming** moves each $f_i^\ast$ to the neighbour $x + c_i$. Both are local and explicit. In lattice units ($\Delta x = \Delta t = 1$, sound speed $c_s^2 = \frac13$) the density and velocity obey, at low Mach number $\mathrm{Ma} = |u|/c_s$, the [Navier-Stokes equations](/navier-stokes-equations/) with pressure $p = \rho/3$ and kinematic viscosity $\nu = (\tau - \frac12)/3$, up to errors $O(\Delta x^2)$ and $O(\mathrm{Ma}^2)$. With a one-dimensional lattice and a velocity-free equilibrium the same scheme solves the [heat equation](/heat-equation/).

## In plain words

Instead of tracking the speed and pressure of a fluid directly, the method imagines crowds of particles sitting on the points of a grid. At each point there are a few groups of particles, each moving in one fixed direction: stay, left, right, up, down, or diagonally.

Every tick, two things happen. First the groups at a point exchange particles so that they drift toward a balanced mix that matches the local amount and average motion of the fluid. Then every group hops one grid point along its direction. Counting the particles at a point gives the fluid density, and their net direction gives its velocity. How quickly the groups rebalance sets how syrupy the fluid is. Because both steps only look at one point and its neighbours, the method is simple and parallelises very well.

## The problem

Given a periodic or channel domain of $n_x \times n_y$ nodes, a relaxation time $\tau > \frac12$, an initial density and velocity field, an optional constant body force $g$, and a number of steps $S$, compute the populations after $S$ steps and the fields $\rho$ and $u$ they define. The target is the incompressible Navier-Stokes solution with viscosity $\nu = (\tau - \frac12)/3$ in lattice units, approximated at low Mach number. Errors are measured in the max norm over nodes, relative to the velocity amplitude. Cost is counted in node updates: one collision and $Q$ moves per node and step.

## The algorithm

D2Q9 has the rest velocity, the four axis velocities and the four diagonals, with weights $w_0 = \frac49$, $w_{1..4} = \frac19$, $w_{5..8} = \frac1{36}$, and

$$f_i^{\mathrm{eq}}(\rho, u) = w_i\rho\Bigl(1 + 3\,c_i\cdot u + \tfrac92(c_i\cdot u)^2 - \tfrac32|u|^2\Bigr).$$

```pseudo id=main
LBM-D2Q9(n_x, n_y, τ, S, init, g, walls)
L1  for each node x: (ρ, u) ← init(x); f_i(x) ← f_i^eq(ρ, u) for i = 0..8
L2  repeat S times
L3      for each node x: ρ ← Σ f_i,  u ← (Σ c_i f_i + g/2)/ρ
L4          f*_i ← f_i − (f_i − f_i^eq(ρ, u))/τ + (1 − 1/(2τ)) w_i [3(c_i − u) + 9(c_i·u) c_i]·g
L5      for each node x and each i: f_i(x + c_i) ← f*_i(x)       ▷ periodic in x and, without walls, in y
L6          if x + c_i lies beyond a wall then f_ī(x) ← f*_i(x)  ▷ halfway bounce-back, ī = −i
L7  return ρ, u at every node (with the g/2 shift)
```

The force term in line L4 is Guo's scheme; with $g = 0$ it vanishes. Walls sit halfway between the last row of nodes and the next one, at $y = -\frac12$ and $y = n_y - \frac12$, and a population that would leave through a wall comes back to its node with reversed velocity. The implementation also contains D1Q3 for diffusion: velocities $0, \pm1$, weights $\frac23, \frac16, \frac16$, equilibrium $w_i\rho$, diffusivity $D = (\tau - \frac12)/3$.

## Example

**By hand: D1Q3 with $\tau = 1$.** With $\tau = 1$ collision replaces $f_i$ by $w_i\rho$, and streaming then gives $\rho_j^{n+1} = \frac23\rho_j^n + \frac16(\rho_{j-1}^n + \rho_{j+1}^n)$: exactly the [FTCS scheme](/ftcs-method/) for $u_t = Du_{xx}$ with $\mu = D\Delta t/\Delta x^2 = \frac16$. A unit mass at the centre of five nodes becomes $(0, \frac16, \frac23, \frac16, 0)$ and then $(\frac1{36}, \frac29, \frac12, \frac29, \frac1{36})$. With $\tau = 2$ the first step is the same (the start is an equilibrium), but the second gives $(\frac7{72}, \frac19, \frac7{12}, \frac19, \frac7{72})$, because the populations that are not fully relaxed keep moving: more mass reaches distance 2.

**By hand: one D2Q9 equilibrium.** For $\rho = 1$, $u = (0.1, 0)$: $f_0^{\mathrm{eq}} = \frac49(1 - 0.015) = 0.43778$, $f_1^{\mathrm{eq}} = \frac19(1 + 0.3 + 0.045 - 0.015) = 0.14778$, $f_3^{\mathrm{eq}} = \frac19 \cdot 0.73 = 0.08111$, $f_2^{\mathrm{eq}} = f_4^{\mathrm{eq}} = 0.10944$, $f_5^{\mathrm{eq}} = f_8^{\mathrm{eq}} = 0.03694$, $f_6^{\mathrm{eq}} = f_7^{\mathrm{eq}} = 0.02028$. They sum to 1, and $\sum c_{ix}f_i^{\mathrm{eq}} = 0.06667 + 2 \cdot 0.01667 = 0.1$.

**Taylor-Green vortex.** $u = -u_0\cos kx\sin ky$, $v = u_0\sin kx\cos ky$ on an $N \times N$ periodic lattice, $k = 2\pi/N$, decays like $e^{-2\nu k^2t}$. With $\tau = 0.8$ ($\nu = 0.1$), diffusive scaling $u_0 = 0.16/N$ and $S = N^2/8$ steps (the same physical time), the relative max error of $u$ was:

| $N$ | 8 | 16 | 32 | 64 |
|---|---|---|---|---|
| relative error | 8.65e-2 | 2.12e-2 | 5.39e-3 | 1.49e-3 |
| observed order | | 2.03 | 1.97 | 1.86 |
| fitted $\nu$ / $(\tau - \frac12)/3$ | 1.092 | 1.022 | 1.005 | 1.001 |

The fitted viscosity converges to $(\tau - \frac12)/3$, the observed order is close to 2, and the slight drop at $N = 64$ is consistent with the initial layer from starting at equilibrium (observed, not analysed).

**Poiseuille flow.** A channel of $n_y = 16$ nodes, one node wide and periodic in $x$, driven by $g = 10^{-6}$, run to steady state ($6n_y^2/\nu$ steps). The exact profile with walls at $y = -\frac12$ and $n_y - \frac12$ is $u(y) = \frac{g}{2\nu}(y + \frac12)(n_y - \frac12 - y)$. The computed profile is that parabola plus a constant slip $s$:

| $\tau$ | 0.6 | 0.8 | 0.9330 | 1.0 | 1.5 |
|---|---|---|---|---|---|
| slip $s/g$ | −3.55 | −0.65 | 0.0000 | 0.25 | 1.6 |
| relative max error | 3.7e-3 | 2.0e-3 | 3.6e-11 | 1.3e-3 | 1.7e-2 |

The measured slips fit $s = g\bigl(2(\tau - \frac12) - \frac3{8(\tau - \frac12)}\bigr)$, which vanishes at $\tau = \frac12 + \frac{\sqrt3}4 \approx 0.9330$, where the scheme reproduces the parabola to rounding. The slip comes from the bounce-back wall, whose effective position depends on $\tau$ (He, Zou, Luo and Dembo analyse this; here it is observed).

**D1Q3 diffusion orders.** A sine mode on $N$ nodes with $S = N^2/16$ steps: for $\tau = 0.8$ the errors $4.0 \cdot 10^{-3}, 1.0 \cdot 10^{-3}, 2.5 \cdot 10^{-4}, 6.3 \cdot 10^{-5}$ for $N = 16$ to 128 show order 2. For $\tau = 1$ they are $6.1 \cdot 10^{-6}, 3.8 \cdot 10^{-7}, 2.3 \cdot 10^{-8}, 1.5 \cdot 10^{-9}$, order 4: this is FTCS with $\mu = \frac16$, the special Courant number where the leading truncation error cancels.

**Instability.** A perturbed double shear layer on $16 \times 16$ nodes for 300 steps stays bounded at $\tau = 0.6$ for speeds up to $0.4$, but at $\tau = 0.505$ it blows up for $u_0 = 0.4$, and at $\tau = 0.501$ already for $u_0 = 0.2$. Small viscosity combined with large lattice speed is the stability limit of BGK, the analogue of a CFL condition (observed).

## Correctness

Proved in the correctness file: the D2Q9 weights satisfy the lattice isotropy identities up to fourth order, so the equilibrium has density $\rho$, momentum $\rho u$ and momentum flux $\rho c_s^2I + \rho uu$ exactly; collision therefore conserves mass and momentum at every node, the force term adds exactly $g$ to the momentum of each node per step, and streaming (periodic or with bounce-back) conserves total mass, so these hold to the last bit in exact arithmetic. For D1Q3 with $\tau = 1$ the scheme is FTCS with $\mu = \frac16$, which is stable and consistent of order 4 for the heat equation, so it converges by the [Lax equivalence theorem](/lax-equivalence-theorem/).

The macroscopic limit for general $\tau$ is cited. The Chapman-Enskog expansion (Krüger et al., Chapter 4) shows that $\rho$ and $u$ satisfy the continuity equation and the Navier-Stokes momentum equation with $p = \rho/3$ and $\nu = (\tau - \frac12)/3$, with errors $O(\Delta x^2)$ under diffusive scaling plus an $O(u^3)$ error in the viscous stress, which is why the equations are recovered only at low Mach number. The $-\frac12$ in $\nu$ is the second-order correction that the streaming step contributes, which makes the scheme second order rather than first. The second-order convergence in the tables is observed.

## Complexity

Each step does, per node, $Q$ equilibrium evaluations and $Q$ collisions in $\Theta(Q)$ arithmetic, and moves $Q$ numbers: $\Theta(SQM)$ time for $M$ nodes and $S$ steps in the [real RAM](/real-ram/) model, with $\Theta(QM)$ memory (two population arrays here; one array with in-place streaming in tuned codes). There are no linear solves and no global communication: the pressure, which needs a Poisson solve in incompressible solvers, comes from the density through $p = \rho/3$. The price is the time step: in diffusive scaling $\Delta t \propto \Delta x^2$, so reaching a fixed physical time on a grid with $N$ nodes per direction takes $\Theta(N^2)$ steps and $\Theta(N^4)$ node updates in 2D. The method is memory-bandwidth bound on modern hardware.

## Properties

- **Exact conservation** of mass and momentum (without forces and walls) in exact arithmetic; rounding is the only source of drift in floating point.
- **Second order** in space under diffusive scaling, with $\nu = (\tau - \frac12)/3$.
- **Weakly compressible.** The density fluctuates with $\delta\rho/\rho = O(\mathrm{Ma}^2)$; incompressibility holds only asymptotically.
- **Local and explicit**, hence easy to parallelise and to apply in complex geometries with bounce-back.
- **Stability.** Requires $\tau > \frac12$ and low lattice speeds; BGK becomes unstable as $\tau \to \frac12$ (high Reynolds number) unless the speed is reduced. There is no simple stability bound for nonlinear flows.
- **Boundary errors.** With BGK collision the effective wall position of halfway bounce-back shifts with $\tau$, which appears as the $\tau$-dependent slip in the Poiseuille table.

## Variants and improvements

- **Lattices.** D1Q3, D2Q9, D3Q15, D3Q19 and D3Q27; larger stencils for thermal and high-Mach flows.
- **MRT and TRT collisions.** Multiple relaxation times (d'Humières, 1992) and the two-relaxation-time scheme relax moments at different rates, which improves stability and makes bounce-back walls independent of viscosity.
- **Entropic and regularised LBM** for stability near $\tau = \frac12$.
- **Boundary schemes.** Zou-He velocity and pressure boundaries, interpolated bounce-back for curved walls, immersed boundaries.
- **Forcing schemes.** Guo's scheme (used here) removes the discrete lattice artefacts of naive forcing; Shan-Chen and free-energy models add interparticle forces for multiphase flows.
- **Advection-diffusion LBM** for scalar transport, the D1Q3 diffusion case being the simplest instance.

## When to use it

Use the lattice Boltzmann method for low-Mach flows in complicated geometries such as porous media, blood flow and microfluidics, and for multiphase and multicomponent flows, where its locality and simple boundaries pay off and GPU implementations run at very high node rates. Prefer a classical Navier-Stokes solver (finite volume, finite element, spectral) for high Reynolds numbers with adaptive meshes, compressible flows, steady problems where implicit solvers converge quickly, or when strict incompressibility is needed.

## Pitfalls

- **$\tau$ too close to $\frac12$.** Low viscosity in lattice units with sizeable velocities blows up, as in the shear layer experiment; refine the lattice or use MRT or entropic collisions.
- **Lattice speeds too large.** Keep $|u| \lesssim 0.1$ in lattice units; the equilibrium is only a second-order expansion in $u$ and becomes negative for large speeds.
- **Units.** All quantities are in lattice units; physical viscosity, speed and time must be converted with $\Delta x$ and $\Delta t$, and choosing them fixes $\tau$.
- **Starting from equilibrium.** Initialising $f_i = f_i^{\mathrm{eq}}$ omits the non-equilibrium part and creates an initial layer and pressure waves.
- **Forcing without the half shift.** Using $u = \sum c_if_i/\rho$ instead of adding $g/2$ gives a first-order error in force-driven flows.
- **Wall position.** With halfway bounce-back the wall is between nodes, at a position that depends on $\tau$; comparing with a solution whose walls are on the nodes shows a spurious first-order error.

## Implementations

## History

Lattice gas automata, in which Boolean particles hop and collide on a hexagonal lattice, were shown by Frisch, Hasslacher and Pomeau in 1986 to produce Navier-Stokes dynamics on average. McNamara and Zanetti replaced the Boolean particles by their averages in 1988, removing the statistical noise; Higuera and Jiménez linearised the collision operator in 1989. The single relaxation time BGK collision on D2Q9 and D3Q19, with the equilibrium used here, was introduced in 1992 by Qian, d'Humières and Lallemand and independently by Chen, Chen and Matthaeus. Later work connected the method to a discretisation of the discrete-velocity Boltzmann equation and developed boundary, forcing (Guo, Zheng and Shi, 2002), MRT and entropic schemes.

## References
