---
tag: FXCWEJ
kind: problem
slug: euler-equations-of-gas-dynamics
name: Euler equations of gas dynamics
aliases:
- compressible Euler equations
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: The conservation laws of mass, momentum and energy of an inviscid compressible gas, closed by an equation of state.
model: real-ram
prereqs: [hyperbolic-conservation-law, rankine-hugoniot-conditions]
see_also: [exact-riemann-solver, riemann-problem, godunov-method, roe-solver, hllc-riemann-solver, navier-stokes-equations, shallow-water-equations, lax-entropy-condition]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 14.3 (the Euler equations), Section 14.4 (polytropic ideal gas), Section 14.5 (entropy), Sections 14.8 to 14.13 (the Riemann problem for the Euler equations), Section 15.1 (Godunov's method), Section 15.3 (approximate Riemann solvers)
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Section 1.1 (the Euler equations), Section 3.1 (the one dimensional Euler equations; 3.1.3 elementary waves), Section 3.3 (conservative and non-conservative formulations), Chapter 4 (the exact Riemann solver)
  - paper: doi:10.1016/0021-9991(78)90023-2
    title: G. A. Sod, A survey of several finite difference methods for systems of nonlinear hyperbolic conservation laws, Journal of Computational Physics 27 (1978) 1-31
    locator: the shock tube test problem
  - paper: doi:10.1002/cpa.21537
    title: E. Chiodaroli, C. De Lellis and O. Kreml, Global ill-posedness of the isentropic system of gas dynamics, Communications on Pure and Applied Mathematics 68 (2015) 1157-1190
    locator: infinitely many admissible weak solutions in two space dimensions
---

The Euler equations of gas dynamics are the conservation laws of mass, momentum and energy for a compressible gas with no viscosity and no heat conduction. With an equation of state, usually the ideal gas law, they form a [hyperbolic conservation law](/hyperbolic-conservation-law/) with three wave speeds $u - c$, $u$ and $u + c$ in one space dimension. The problem is to compute their solution from given initial and boundary data, including shocks and contact discontinuities. They are the standard test system for shock capturing methods: the [exact Riemann solver](/exact-riemann-solver/) solves them for two constant states, the [Godunov method](/godunov-method/) builds a scheme on that solution, and the Sod shock tube is the first test of nearly every code. They are the limit of the [Navier-Stokes equations](/navier-stokes-equations/) when viscosity and heat conduction go to zero. They should not be confused with the incompressible Euler equations, where the density is constant and there is no sound speed.

## In plain words

A gas has a density, a velocity and an energy at every point. The Euler equations say three things. Mass is not created. Momentum changes only by the pressure push of the gas around it. Energy changes only by the work the pressure does. A rule that gives the pressure from the density and the energy closes the system.

Disturbances in the gas travel as sound waves, which move at the speed of sound relative to the gas, and as contact surfaces, which move with the gas. Strong sound waves steepen into shocks, which are thin layers where the pressure and the density jump.

## Definition

**Unknowns.** The density $\rho$, the velocity $u$, the pressure $p$, and the total energy per unit volume $E = \rho e + \frac12\rho u^2$, with $e$ the specific internal energy.

**One space dimension.** With $U = (\rho, \rho u, E)$,

$$U_t + F(U)_x = 0, \qquad F(U) = \begin{pmatrix} \rho u \\ \rho u^2 + p \\ u(E + p) \end{pmatrix}.$$

**Equation of state.** For a polytropic ideal gas with ratio of specific heats $\gamma > 1$, $p = (\gamma - 1)\rho e$, so

$$E = \frac{p}{\gamma - 1} + \frac12\rho u^2, \qquad c = \sqrt{\gamma p/\rho}.$$

For air, $\gamma = 1.4$. The specific entropy is $S = c_v\log(p/\rho^\gamma)$ up to a constant.

**Characteristic structure.** Where $\rho > 0$ and $p > 0$, the Jacobian $F'(U)$ has the eigenvalues $\lambda_1 = u - c$, $\lambda_2 = u$, $\lambda_3 = u + c$ with right eigenvectors

$$r_1 = \begin{pmatrix} 1 \\ u - c \\ H - uc \end{pmatrix}, \quad r_2 = \begin{pmatrix} 1 \\ u \\ \frac12u^2 \end{pmatrix}, \quad r_3 = \begin{pmatrix} 1 \\ u + c \\ H + uc \end{pmatrix},$$

where $H = (E + p)/\rho$ is the specific enthalpy. The system is strictly hyperbolic. Fields 1 and 3 are genuinely nonlinear: they give shocks and rarefactions. Field 2 is linearly degenerate: it gives contact discontinuities, across which $u$ and $p$ are continuous and $\rho$ jumps (LeVeque 2002, Sections 14.3 to 14.8).

**Several dimensions.** With velocity $\mathbf u \in \mathbb{R}^d$, $U = (\rho, \rho\mathbf u, E)$ and

$$\rho_t + \nabla\cdot(\rho\mathbf u) = 0, \quad (\rho\mathbf u)_t + \nabla\cdot(\rho\mathbf u \otimes \mathbf u + pI) = 0, \quad E_t + \nabla\cdot\big((E + p)\mathbf u\big) = 0.$$

In direction $n$ the speeds are $\mathbf u\cdot n \pm c$ and $\mathbf u\cdot n$, the last with multiplicity $d$.

**The computational problem.** Given $\gamma$, initial data $U_0$ with $\rho_0 > 0$, $p_0 > 0$, boundary conditions and a final time $T$, compute the admissible weak solution: a [weak solution](/weak-solution-of-conservation-law/) whose shocks satisfy the [Rankine-Hugoniot conditions](/rankine-hugoniot-conditions/) and the [Lax entropy condition](/lax-entropy-condition/), which here means that the physical entropy $S$ increases across every shock.

## Variants

- **Other equations of state.** Stiffened gas $p = (\gamma - 1)\rho e - \gamma p_\infty$ for liquids, van der Waals gases, and tabulated equations of state. They change $c$ and the Riemann solution, but not the conservation form.
- **Isentropic and isothermal Euler.** If $p = \kappa\rho^\gamma$ is imposed, the energy equation is dropped and the system has two equations. It has the same form as the [shallow water equations](/shallow-water-equations/), which are isentropic Euler with $\gamma = 2$ and $\kappa = g/2$.
- **Primitive variables.** $W = (\rho, u, p)$ with $W_t + A(W)W_x = 0$. This form is equivalent only for smooth solutions; a scheme for it does not give the right shocks (Toro 2009, Section 3.3).
- **With source terms.** Gravity, chemical reactions (reactive Euler), and the quasi one dimensional nozzle equations with a variable area.
- **Relativistic and magnetohydrodynamic extensions.** More equations and more waves, with the same structure of a hyperbolic system.

## Examples

**The Sod shock tube.** $\gamma = 1.4$, $(\rho, u, p) = (1, 0, 1)$ for $x < 0$ and $(0.125, 0, 0.1)$ for $x > 0$ (Sod 1978). The [exact Riemann solver](/exact-riemann-solver/) gives the star state $p_* = 0.30313$, $u_* = 0.92745$, with $\rho_{*L} = 0.42632$ to the left of the contact and $\rho_{*R} = 0.26557$ to the right. The waves are:

- a left rarefaction from $x/t = -c_L = -1.18322$ to $x/t = u_* - c_{*L} = -0.07027$, where $c_{*L} = \sqrt{1.4 \cdot 0.30313/0.42632} = 0.99772$;
- a contact at $x/t = u_* = 0.92745$;
- a right shock at $x/t = 1.75216$.

The entropy check: $p/\rho^\gamma$ is $1.0$ on the left and in the rarefaction, $1.93990$ just right of the contact, and $1.83792$ in the undisturbed right state. So it is constant through the rarefaction, jumps at the contact, and increases from $1.83792$ to $1.93990$ across the shock. These values come from the reference code of the exact Riemann solver page; they are a measurement to five digits. The page on the [Rankine-Hugoniot conditions](/rankine-hugoniot-conditions/) checks the three jump conditions at this shock.

**A contact alone.** $\rho_L = 1$, $\rho_R = 0.5$, $u = 0.3$ and $p = 1$ everywhere. The exact solution is the jump in $\rho$ moving at speed $0.3$. Any consistent conservative scheme with a positive diffusion smears this jump, and the smearing grows with time, because a contact is not self steepening.

**Vacuum generation.** Two gases moving apart fast enough leave a vacuum between them. For the Sod sound speeds, this happens when $u_R - u_L \ge \frac{2}{\gamma - 1}(c_L + c_R) = 11.20758$ (Toro 2009, Chapter 4).

## Known algorithms

- **Godunov type finite volume methods.** The [Godunov method](/godunov-method/) with the [exact Riemann solver](/exact-riemann-solver/), or with approximate solvers: the [Roe solver](/roe-solver/), [HLL](/hll-riemann-solver/), [HLLC](/hllc-riemann-solver/) and the [Rusanov flux](/rusanov-flux/). High order versions use [MUSCL](/muscl-scheme/), the [piecewise parabolic method](/piecewise-parabolic-method/) or [WENO](/weno-scheme/) reconstruction with [SSP Runge-Kutta](/strong-stability-preserving-runge-kutta/) time steps.
- **Flux vector splitting and AUSM.** [Flux vector splitting](/flux-vector-splitting/) (Steger-Warming, van Leer) and the [AUSM scheme](/ausm-scheme/) split the flux by the sign of the wave speeds without a Riemann solver.
- **Central schemes.** [Lax-Friedrichs](/lax-friedrichs-scheme/), [Nessyahu-Tadmor](/nessyahu-tadmor-scheme/) and [Kurganov-Tadmor](/kurganov-tadmor-scheme/) need only the maximum wave speed.
- **Classical second order schemes with artificial viscosity.** The [Lax-Wendroff method](/lax-wendroff-method/) and the [MacCormack method](/maccormack-method/). They oscillate at shocks unless viscosity is added.
- **Discontinuous Galerkin methods.** [Discontinuous Galerkin](/discontinuous-galerkin-method/) and [RKDG](/runge-kutta-discontinuous-galerkin/) methods use the same numerical fluxes at element faces.
- **Supporting techniques.** [Positivity preserving limiters](/positivity-preserving-limiter/) keep $\rho$ and $p$ positive, [entropy stable schemes](/entropy-stable-scheme/) give a discrete entropy inequality, [adaptive mesh refinement](/adaptive-mesh-refinement/) puts cells at the shocks, and the [ghost fluid method](/ghost-fluid-method/) treats interfaces between two materials.

## Bounds

- **Cost of an explicit scheme.** On a grid of $M$ cells, one step of a Godunov type scheme costs $O(M)$ operations, with a constant set by the Riemann solver. The time step is bounded by the [CFL condition](/courant-friedrichs-lewy-condition/) $\Delta t \le \nu\Delta x/\max_j(|u_j| + c_j)$ with $\nu \le 1$, so reaching time $T$ takes $O(T\max(|u| + c)/\Delta x)$ steps. In one dimension the total is $O(M^2)$ for a fixed $T$; in $d$ dimensions with $M$ cells it is $O(M^{1 + 1/d})$.
- **Accuracy at shocks.** For a solution with shocks, the $L^1$ error of a scheme of any formal order is at best $O(\Delta x)$, and at contacts first order schemes give $O(\Delta x^{1/2})$ errors because the smearing spreads over $O(\sqrt{t\Delta x})$. This is the rule of thumb in the literature and is what measurements show; the rates for systems are not proved in general.
- **Well posedness (theorem).** In one dimension, for data with small total variation near a state with $\rho, p > 0$, an admissible weak solution exists for all time (Glimm 1965). In two dimensions, Chiodaroli, De Lellis and Kreml (2015) proved that the isentropic system has Lipschitz initial data with infinitely many admissible weak solutions. So the entropy condition alone does not give uniqueness in several dimensions.
- **Riemann problem (theorem).** For an ideal gas, the one dimensional Riemann problem has a unique solution of the shock, rarefaction and contact type for every pair of states, and it contains a vacuum exactly when $u_R - u_L \ge \frac{2}{\gamma - 1}(c_L + c_R)$ (Toro 2009, Chapter 4).
- **Positivity.** A scheme can produce $\rho < 0$ or $p < 0$ even from positive data. Measurement: the MacCormack method without added viscosity on the Sod problem with $\Delta t/\Delta x = 0.2$ gives negative pressure within ten steps, see the [MacCormack method](/maccormack-method/).

## Reductions

- **To Riemann problems.** A Godunov type scheme reduces each step to one [Riemann problem](/riemann-problem/) per cell face. The exact solver reduces each Riemann problem to one scalar equation for $p_*$.
- **To linear acoustics.** Linearization about a constant state $(\rho_0, u_0, p_0)$ gives the acoustics system with speeds $u_0 \pm c_0$ and $u_0$, which is the [wave equation](/wave-equation/) for small pressure perturbations.
- **From Navier-Stokes.** The compressible [Navier-Stokes equations](/navier-stokes-equations/) reduce to the Euler equations when viscosity and heat conduction are dropped. The vanishing viscosity limit is how the entropy condition is justified.
- **To shallow water.** The isentropic system with $\gamma = 2$ has the same mathematical form as the [shallow water equations](/shallow-water-equations/), with $\rho$ in the place of $h$.

## Applications

- Aerodynamics of transonic and supersonic flight: wings, inlets, nozzles, where the boundary layer is thin and the shocks are the main feature.
- Astrophysics: supernova blast waves, accretion flows, jets and the gas in galaxy simulations.
- Detonations and explosions, with reactive source terms.
- Inertial confinement fusion and high speed impact.
- A standard test bed for numerical methods for hyperbolic systems: the Sod, Lax, Shu-Osher and Woodward-Colella blast wave problems.

## References
