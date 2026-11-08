---
tag: 5JF65E
kind: problem
slug: navier-stokes-equations
name: Navier-Stokes equations
aliases:
- incompressible Navier-Stokes
- Navier-Stokes problem
area: numerical/differential-equations
level: research
summary: "Find velocity u and pressure p with u_t + (u . grad) u + grad p = nu Laplace u + f and div u = 0, from initial and boundary data. The equations of viscous flow; 3D global regularity is open."
prereqs: [heat-equation, burgers-equation, poisson-equation]
see_also: [lattice-boltzmann-method, smoothed-particle-hydrodynamics, finite-volume-method, finite-element-method, spectral-methods, operator-splitting, method-of-lines, boundary-conditions]
sources:
  - paper: doi:10.1090/S0025-5718-1968-0242392-2
    title: "Alexandre Joel Chorin, Numerical solution of the Navier-Stokes equations, Mathematics of Computation 22 (1968) 745-762"
  - paper: doi:10.1063/1.1761178
    title: "Francis H. Harlow and J. Eddie Welch, Numerical calculation of time-dependent viscous incompressible flow of fluid with free surface, Physics of Fluids 8 (1965) 2182-2189"
  - book: isbn:9780821827376
    title: "Roger Temam, Navier-Stokes Equations: Theory and Numerical Analysis, AMS Chelsea, 2001"
    locator: "Chapter I (the stationary Stokes problem and the inf-sup condition), Chapter III (existence of weak solutions, uniqueness in two dimensions, the projection method)"
  - paper: doi:10.1016/j.cma.2005.10.010
    title: "J. L. Guermond, P. Minev and Jie Shen, An overview of projection methods for incompressible flows, Computer Methods in Applied Mechanics and Engineering 195 (2006) 6011-6045"
  - paper: doi:10.1007/BF02547354
    title: "Jean Leray, Sur le mouvement d'un liquide visqueux emplissant l'espace, Acta Mathematica 63 (1934) 193-248"
  - paper: "Charles L. Fefferman, Existence and smoothness of the Navier-Stokes equation, in The Millennium Prize Problems, Clay Mathematics Institute and American Mathematical Society, 2006, 57-67"
---

The incompressible Navier-Stokes equations describe a viscous fluid of constant density $\rho$. Given a domain $\Omega \subset \mathbb{R}^d$ ($d = 2$ or $3$), a kinematic viscosity $\nu > 0$, a body force $f$ and an initial velocity $u_0$ with $\nabla\cdot u_0 = 0$, the problem asks for a velocity field $u(x, t)$ and a pressure $p(x, t)$ with

$$\partial_tu + (u\cdot\nabla)u + \frac1\rho\nabla p = \nu\Delta u + f, \qquad \nabla\cdot u = 0,$$

$u(\cdot, 0) = u_0$, and [boundary conditions](/boundary-conditions/) such as no-slip $u = 0$ on walls or periodicity. The first equation is Newton's law for a fluid parcel; the second says the flow neither compresses nor expands. The pressure has no evolution equation of its own: it is the Lagrange multiplier that keeps $u$ divergence free, and it is determined by a [Poisson equation](/poisson-equation/). The equations combine the nonlinear transport of the [Burgers equation](/burgers-equation/) with the diffusion of the [heat equation](/heat-equation/); the ratio of the two effects is the Reynolds number $\mathrm{Re} = UL/\nu$ for a velocity scale $U$ and length scale $L$.

## In plain words

These are the equations behind the motion of water, air and blood, whenever the fluid is not squeezed noticeably. They say two things. Each small piece of fluid speeds up or slows down because pressure differences push it, friction with its neighbours drags it, and outside forces such as gravity act on it. And no fluid is created or destroyed anywhere: what flows into a region flows out again.

When friction is strong, as for honey or very slow flows, the motion is smooth and predictable. When friction is weak compared with the speed, as for wind around a building, the flow breaks into eddies of many sizes, called turbulence, and computing it in full detail becomes enormously expensive. Whether smooth solutions in three dimensions can suddenly break down is one of the famous unsolved problems of mathematics.

## Definition

**Input.** A domain $\Omega$ (bounded with a Lipschitz boundary, or a periodic box $[0, L]^d$), $\nu > 0$, $\rho > 0$, a time horizon $T$, a force $f$, a divergence-free initial velocity $u_0$ satisfying the boundary condition, and boundary data.

**Output.** $u : \Omega \times [0, T] \to \mathbb{R}^d$ and $p : \Omega \times [0, T] \to \mathbb{R}$ (unique up to an additive function of $t$) satisfying the equations above. A *classical* solution is smooth; a *Leray-Hopf weak solution* satisfies the equations in the sense of distributions, lies in $L^\infty(0, T; L^2) \cap L^2(0, T; H^1)$, and obeys the energy inequality.

**Numerical problem.** On a grid with spacing $\Delta x$ and step $\Delta t$, compute $U^n \approx u(\cdot, t_n)$ and $P^n \approx p(\cdot, t_n)$ with a discrete divergence $\nabla_h\cdot U^n$ that is zero (or $O(\Delta x^q)$), and errors measured in a discrete $L^2$ or max norm of the velocity. Costs are counted in work per step (a linear solve for the pressure in most methods) times the number of steps, which is set by stability, accuracy and the need to resolve the smallest eddies.

## Variants

- **Compressible Navier-Stokes.** Density and energy become unknowns, with an equation of state; the pressure is no longer a constraint force. Used for high-speed aerodynamics.
- **Stokes equations.** Drop $(u\cdot\nabla)u$, the limit $\mathrm{Re} \to 0$: linear, a saddle point problem.
- **Euler equations.** $\nu = 0$: inviscid flow, no boundary layers, possible loss of regularity.
- **Oseen equations.** Linearise the convection around a known field $w$: $(w\cdot\nabla)u$.
- **Boussinesq approximation.** Add a temperature equation and buoyancy, for natural convection and atmosphere and ocean models.
- **Vorticity form in 2D.** With $\omega = \partial_xv - \partial_yu$ and a stream function $\psi$, $\partial_t\omega + u\cdot\nabla\omega = \nu\Delta\omega$, $\Delta\psi = -\omega$, which removes the pressure.
- **Stationary problem.** Drop $\partial_tu$; for small data the steady solution is unique, for large $\mathrm{Re}$ it may be unstable or non-unique.

## Examples

**Exact solutions.** These are the standard tests for codes.

- *Plane Poiseuille flow* between walls at $y = 0$ and $y = H$ driven by a constant force $g$: $u = \frac{g}{2\nu}y(H - y)$, $v = 0$. The [lattice Boltzmann](/lattice-boltzmann-method/) page reproduces it, with a viscosity-dependent wall slip.
- *Taylor-Green vortex* in $[0, 2\pi]^2$, periodic: $u = \sin x\cos y\,e^{-2\nu t}$, $v = -\cos x\sin y\,e^{-2\nu t}$, $p = \frac\rho4(\cos2x + \cos2y)e^{-4\nu t}$. Here $(u\cdot\nabla)u = \frac12(\sin2x, \sin2y)e^{-4\nu t}$ is exactly balanced by $-\nabla p/\rho$, and what remains is the heat equation for each velocity component.
- *Kovasznay flow*, a steady 2D solution behind a grid: $u = 1 - e^{\lambda x}\cos2\pi y$, $v = \frac{\lambda}{2\pi}e^{\lambda x}\sin2\pi y$, $p/\rho = \frac12(1 - e^{2\lambda x})$ with $\lambda = \frac{\mathrm{Re}}2 - \sqrt{\frac{\mathrm{Re}^2}4 + 4\pi^2}$ and $\nu = 1/\mathrm{Re}$.

**A projection method on the Taylor-Green vortex.** Chorin's method with forward Euler in time and second-order central differences, $\nu = 0.1$, $T = 1$, $\Delta t \approx 0.1\Delta x^2$; the pressure step projects onto the kernel of the discrete divergence exactly, using the discrete Fourier transform on the periodic grid. Max error of $u$ at $T$ (observed):

| $N$ (nodes per direction) | 8 | 16 | 32 |
|---|---|---|---|
| steps | 17 | 65 | 260 |
| max error | 7.40e-3 | 1.85e-3 | 4.63e-4 |
| observed order | | 2.00 | 2.00 |
| max discrete divergence | 1.6e-15 | 6.8e-15 | 1.8e-14 |

The discrete divergence is zero to rounding, and the error is second order in $\Delta x$ because $\Delta t \propto \Delta x^2$ makes the first-order time error $O(\Delta x^2)$ too. With the larger step $\Delta t = \Delta x^2$ the errors were $3.6 \cdot 10^{-4}, 2.3 \cdot 10^{-4}, 1.0 \cdot 10^{-4}$: smaller but irregular, because time and space errors partly cancel. An apparent order measured in that regime would be misleading.

**Lid-driven cavity.** A unit square with no-slip walls and the top wall sliding at speed 1. There is no closed-form solution; tabulated reference velocities on the centrelines (Ghia, Ghia and Shin, 1982) for $\mathrm{Re}$ from 100 to 10000 serve as the benchmark.

## Known algorithms

| Method | Idea | Per-step cost | Notes |
|---|---|---|---|
| Projection (Chorin 1968, Temam 1969) | advance velocity ignoring incompressibility, then project onto divergence-free fields | one Poisson solve | splitting error at walls; incremental and rotational versions improve it (Guermond, Minev and Shen) |
| MAC staggered grid (Harlow and Welch 1965) | pressures at cell centres, velocities on faces | one Poisson solve | no spurious pressure modes; conserves mass exactly per cell |
| SIMPLE and PISO | iterative pressure correction for steady and transient flows | several linear solves | the workhorse of finite volume CFD codes |
| Mixed [finite elements](/finite-element-method/) | velocity and pressure spaces satisfying the inf-sup (LBB) condition, such as Taylor-Hood | saddle point solve | unstable pairs (equal order) give checkerboard pressures unless stabilised |
| [Spectral](/spectral-methods/) and pseudo-spectral | Fourier or Chebyshev expansions, pressure by exact projection | FFTs, $\Theta(M\log M)$ | the standard for DNS in simple geometries |
| [Lattice Boltzmann](/lattice-boltzmann-method/) | kinetic populations relaxing to equilibrium | local, no linear solve | weakly compressible, explicit |
| Vortex methods and [SPH](/smoothed-particle-hydrodynamics/) | Lagrangian particles carrying vorticity or mass | particle interactions | grid-free; free surfaces |

Time stepping is usually by the [method of lines](/method-of-lines/) with implicit treatment of the viscous term and explicit treatment of convection (IMEX), or by [operator splitting](/operator-splitting/) between convection, diffusion and projection. Turbulent flows at high $\mathrm{Re}$ are rarely solved directly: large eddy simulation (LES) and Reynolds-averaged models (RANS) solve modified equations, which is modelling rather than numerical analysis.

## Bounds

**Energy (proved, for smooth solutions).** In a periodic box or with $u = 0$ on $\partial\Omega$, and $f = 0$,

$$\frac{d}{dt}\,\frac12\|u\|_{L^2}^2 = -\nu\|\nabla u\|_{L^2}^2.$$

*Proof.* Take the inner product of the momentum equation with $u$. The convection term gives $\int u\cdot(u\cdot\nabla)u = \int u\cdot\nabla\frac{|u|^2}2 = -\int(\nabla\cdot u)\frac{|u|^2}2 = 0$, and the pressure term $\int u\cdot\nabla p = -\int p\,\nabla\cdot u = 0$, both by integration by parts with no boundary terms. The viscous term gives $\nu\int u\cdot\Delta u = -\nu\|\nabla u\|^2$. $\square$ With the Poincaré inequality $\|\nabla u\|^2 \ge \lambda_1\|u\|^2$ (for zero-mean periodic fields in $[0, 2\pi]^d$, $\lambda_1 = 1$) this gives $\|u(t)\| \le e^{-\nu\lambda_1t}\|u_0\|$. The Taylor-Green vortex decays at the faster rate $2\nu$ because its wave vectors have $|k|^2 = 2$. Good discretisations inherit a discrete version of this identity, which is the main tool for proving their stability.

**Existence and regularity.** In 2D, for $u_0 \in L^2$ there is a unique global weak solution, and it is smooth for $t > 0$ (Leray for the plane, Ladyzhenskaya for bounded domains). In 3D Leray (1934) proved that global weak solutions satisfying the energy inequality exist; smooth solutions exist for a short time, or for all time when the data are small, but whether smooth data always give smooth solutions for all time, and whether weak solutions are unique, is open. It is one of the Clay Millennium Prize problems (Fefferman's problem statement).

**Resolution (heuristic).** Kolmogorov's 1941 theory puts the smallest eddies at $\eta \approx L\,\mathrm{Re}^{-3/4}$. A direct numerical simulation resolving them in 3D needs about $(L/\eta)^3 = \mathrm{Re}^{9/4}$ grid points and, with a time step limited by $\Delta x/U$, about $\mathrm{Re}^{3/4}$ steps over one large-eddy time, so about $\mathrm{Re}^3$ work. This is a scaling estimate, not a theorem; at $\mathrm{Re} = 10^6$ it is far beyond present computers.

**Time step restrictions.** Explicit convection needs a CFL condition $\Delta t \lesssim \Delta x/|u|$; explicit diffusion with central differences needs $\nu\Delta t/\Delta x^2 \le \frac1{2d}$. Both are why viscous terms are usually treated implicitly.

## Reductions

- **To a Poisson problem per step.** Taking the divergence of the momentum equation gives $\Delta p/\rho = -\nabla\cdot((u\cdot\nabla)u) + \nabla\cdot f$; projection methods reduce each time step to one Poisson solve, so fast Poisson solvers (FFT, multigrid) set the cost.
- **From Navier-Stokes to Burgers.** Dropping the pressure and the incompressibility in 1D leaves $u_t + uu_x = \nu u_{xx}$, the standard model for shock formation and viscous smoothing.
- **To Stokes and saddle point systems.** Linearising and dropping convection gives the Stokes problem, whose discretisation is a symmetric indefinite system; the inf-sup condition is the discrete well-posedness criterion.
- **From kinetic theory.** The Chapman-Enskog expansion of the Boltzmann equation gives Navier-Stokes at small Knudsen number; the lattice Boltzmann method uses this in reverse.
- **2D vorticity form.** In two dimensions the problem reduces to an advection-diffusion equation for the scalar vorticity coupled to a Poisson equation for the stream function.

## Applications

Aerodynamics of aircraft and cars, weather and climate models (with rotation and stratification), ocean circulation, blood flow in arteries and heart valves, combustion and chemical reactors, microfluidics and lab-on-a-chip devices, oil and groundwater flow (through Darcy and Brinkman limits), and computer graphics, where Stam's stable fluids method (a semi-Lagrangian projection method) animates smoke and water.

## References
