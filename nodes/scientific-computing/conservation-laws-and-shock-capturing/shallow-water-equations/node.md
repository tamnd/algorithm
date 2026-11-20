---
tag: FKDZS0
kind: problem
slug: shallow-water-equations
name: Shallow water equations
aliases:
- Saint-Venant equations
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: Hyperbolic equations for the depth and depth-averaged velocity of a thin fluid layer under gravity, used for rivers, tsunamis and atmospheres.
model: real-ram
prereqs: [hyperbolic-conservation-law]
see_also: [height-field-water, well-balanced-scheme, euler-equations-of-gas-dynamics, riemann-problem, exact-riemann-solver, positivity-preserving-limiter, godunov-method, fluid-simulation-for-animation]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 13.1 (the shallow water equations), Section 13.2 (the dam break problem), Section 13.3 (characteristic structure), Section 13.7 (Hugoniot loci), Section 13.8 (rarefaction waves), Section 13.9 (solving the dam break problem), Section 13.10 (the general Riemann solver), Chapter 17 (source terms and balance laws)
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Section 1.6.9 (the shallow water equations)
  - paper: doi:10.1137/S1064827503431090
    title: E. Audusse, F. Bouchut, M.-O. Bristeau, R. Klein and B. Perthame, A fast and stable well-balanced scheme with hydrostatic reconstruction for shallow water flows, SIAM Journal on Scientific Computing 25(6) (2004) 2050-2065
    locator: the hydrostatic reconstruction, preservation of the lake at rest and of nonnegative depth
  - paper: "A. Ritter, Die Fortpflanzung der Wasserwellen, Zeitschrift des Vereines Deutscher Ingenieure 36(33) (1892) 947-954"
    locator: the dam break solution over a dry bed
  - paper: "A. J. C. Barré de Saint-Venant, Théorie du mouvement non permanent des eaux, avec application aux crues des rivières et à l'introduction des marées dans leurs lits, Comptes Rendus de l'Académie des Sciences 73 (1871)"
    locator: the one dimensional equations for unsteady open channel flow
---

The shallow water equations describe a layer of water, or any fluid, that is thin compared with the length of its waves, by two fields on a flat grid: the depth $h$ and the velocity $u$ averaged over the depth. Here $h$ is the water depth, not a mesh size; the mesh size is $\Delta x$. Gravity drives the flow, and waves move at the speed $\sqrt{gh}$ relative to the water. Graphics programs use the same picture as a height field: [height field water](/height-field-water/) evolves a grid of water heights with a linearized wave equation that is cheap and stable. The accurate method adds the nonlinear equations in conservation form, solved with a finite volume scheme that conserves the water volume and the momentum exactly, so that bores, hydraulic jumps, dam breaks and wet and dry fronts move at the correct speed. Mathematically the equations are a two component [hyperbolic conservation law](/hyperbolic-conservation-law/), the same system as the isentropic [Euler equations](/euler-equations-of-gas-dynamics/) with $\gamma = 2$.

## In plain words

Think of a river or a flood seen from above. At each point you keep only two numbers: how deep the water is and how fast it flows. Water is never created or lost, so the depth at a place changes only when water flows in or out. The flow speeds up where the water surface slopes down, because gravity pushes the water downhill.

Small waves travel at a speed that grows with the depth, so waves are faster in deep water. A wave that is high enough catches up with the water in front of it and steepens into a bore: a moving step in the water surface, like a breaking front.

## Definition

**One space dimension.** With depth $h \ge 0$, velocity $u$, discharge $hu$, gravity $g$ and bottom height $B(x)$,

$$h_t + (hu)_x = 0, \qquad (hu)_t + \Big(hu^2 + \frac12gh^2\Big)_x = -ghB_x.$$

With a flat bottom the right side is zero and the system is a conservation law $U_t + F(U)_x = 0$ with $U = (h, hu)$.

**Two space dimensions.** With velocity $(u, v)$,

$$h_t + (hu)_x + (hv)_y = 0,$$
$$(hu)_t + \Big(hu^2 + \frac12gh^2\Big)_x + (huv)_y = -ghB_x,$$
$$(hv)_t + (huv)_x + \Big(hv^2 + \frac12gh^2\Big)_y = -ghB_y.$$

**Assumptions.** The pressure is hydrostatic, the horizontal velocity does not depend on the height inside the layer, and the wavelength is long compared with the depth. Friction, viscosity and the Coriolis force are left out, but they can be added as source terms.

**Characteristic structure.** For $h > 0$ the eigenvalues of $F'(U)$ are $\lambda_{1,2} = u \mp \sqrt{gh}$, with eigenvectors $r_{1,2} = (1, u \mp \sqrt{gh})$. The system is strictly hyperbolic for $h > 0$, and both fields are genuinely nonlinear. The Riemann invariants are $u + 2\sqrt{gh}$ and $u - 2\sqrt{gh}$. The ratio $|u|/\sqrt{gh}$ is the Froude number: the flow is subcritical below 1 and supercritical above 1 (LeVeque 2002, Sections 13.1 and 13.3).

**The computational problem.** Given $g$, $B$, initial data $h_0 \ge 0$ and $u_0$, boundary conditions and a final time $T$, compute the entropy solution. Its jumps (bores) satisfy the [Rankine-Hugoniot conditions](/rankine-hugoniot-conditions/), and the total energy $\eta = \frac12hu^2 + \frac12gh^2$ decreases across them. The depth must stay nonnegative, and states with $h = 0$ (dry land) must be allowed.

## Variants

- **Flat or variable bottom.** With $B$ not constant the system is a balance law. The steady state of a lake at rest, $u = 0$ and $h + B$ constant, has a flux gradient that balances the source exactly. A scheme that keeps this state exactly is called [well balanced](/well-balanced-scheme/).
- **Linearized shallow water.** About a state with depth $H$ and $u = 0$, small perturbations satisfy $\eta_t + Hu_x = 0$, $u_t + g\eta_x = 0$, so $\eta_{tt} = gH\eta_{xx}$: the [wave equation](/wave-equation/) with speed $\sqrt{gH}$. This is the model behind [height field water](/height-field-water/). It has no bores and no wet and dry fronts.
- **Rotating shallow water.** The Coriolis terms $fhv$ and $-fhu$ are added to the right sides of the $hu$ and $hv$ equations. It is a standard model of the atmosphere and the ocean.
- **Multilayer and dispersive models.** Several layers of different density, and Boussinesq or Serre-Green-Naghdi equations, which add dispersion for shorter waves.
- **Friction.** Manning or Chezy friction terms for rivers and floods.

## Examples

**Dam break over a wet bed.** $g = 1$, $h_L = 2$, $h_R = 1$, $u_L = u_R = 0$. The middle state solves

$$2\big(\sqrt{gh_L} - \sqrt{gh_*}\big) = (h_* - h_R)\sqrt{\frac{g(h_* + h_R)}{2h_*h_R}},$$

where the left side is the rarefaction branch and the right side is the shock branch of the wave relations. The solution is $h_* = 1.45384$, $u_* = 0.41692$. Hand check: $2(\sqrt{1.45384} - \sqrt2) = 2(1.20575 - 1.41421) = -0.41692$, so $u_* = 0.41692$ from the left; and $0.45384\sqrt{2.45384/(2 \cdot 1.45384)} = 0.41692$ from the right. The waves are a left rarefaction from $x/t = -\sqrt2 = -1.41421$ to $x/t = u_* - \sqrt{h_*} = -0.78883$, and a right bore with speed $s = h_*u_*/(h_* - h_R) = 1.33557$ (LeVeque 2002, Sections 13.2 and 13.9). The bore loses energy: $-s(\eta_R - \eta_*) + (\psi_R - \psi_*) = -0.02147$ per unit time, with the energy flux $\psi = (\frac12hu^2 + gh^2)u$. This is computed from the five digit values above.

**Dam break over a dry bed (Ritter 1892).** $h = h_0$ for $x < 0$ and $h = 0$ for $x > 0$, at rest. The solution is a single rarefaction:

$$h = \frac{\big(2\sqrt{gh_0} - x/t\big)^2}{9g}, \qquad u = \frac23\Big(\frac xt + \sqrt{gh_0}\Big), \qquad -\sqrt{gh_0} \le \frac xt \le 2\sqrt{gh_0}.$$

With $g = 1$ and $h_0 = 1$: the back of the wave moves left at speed 1, the wet and dry front moves right at speed 2, and at the dam site $x = 0$ the depth is $\frac49 = 0.44444$ and the velocity is $\frac23$. At $x/t = 1$, $h = \frac19$ and $u = \frac43$. Check: $u + 2\sqrt{gh} = 2$ at every point, the value of the Riemann invariant in the still water. The front moves twice as fast as small waves in the still water, which a linear height field model cannot show.

**A lake at rest.** $B(x) = 0.5\sin x$, $h = 1 - B$, $u = 0$. The exact solution does not change. A scheme that discretizes $(\frac12gh^2)_x$ and $-ghB_x$ in different ways produces flow from nothing. A well balanced scheme, for example with the hydrostatic reconstruction of Audusse et al. (2004), keeps it exactly.

## Known algorithms

- **Godunov type finite volume methods.** The [Godunov method](/godunov-method/) with an [exact Riemann solver](/exact-riemann-solver/) for shallow water (one scalar equation for $h_*$), or with the [Roe solver](/roe-solver/), [HLL](/hll-riemann-solver/) or the [Rusanov flux](/rusanov-flux/). High order versions use [MUSCL](/muscl-scheme/) or [WENO](/weno-scheme/) reconstruction.
- **Well balanced schemes.** [Well balanced schemes](/well-balanced-scheme/) such as the hydrostatic reconstruction keep the lake at rest exactly with a variable bottom.
- **Positivity and wet and dry fronts.** [Positivity preserving limiters](/positivity-preserving-limiter/) and HLL type fluxes keep $h \ge 0$ at fronts.
- **Central schemes.** The [Kurganov-Tadmor scheme](/kurganov-tadmor-scheme/) and its well balanced versions need only the wave speeds.
- **Discontinuous Galerkin methods.** [Discontinuous Galerkin](/discontinuous-galerkin-method/) methods are used for coastal and tsunami models on unstructured meshes.
- **Adaptive meshes.** [Adaptive mesh refinement](/adaptive-mesh-refinement/) follows tsunami fronts across an ocean basin.
- **Graphics.** [Height field water](/height-field-water/) solves the linearized equations implicitly for real time animation. Semi-Lagrangian advection, also common in graphics, is stable for large steps, but it is not conservative in general, so the volume can drift.

## Bounds

- **Cost of an explicit scheme.** On $M$ cells one step costs $O(M)$ operations. The time step obeys the [CFL condition](/courant-friedrichs-lewy-condition/) $\Delta t \le \nu\Delta x/\max(|u| + \sqrt{gh})$ with $\nu \le 1$, so deep water forces small steps: for $h = 4000$ m and $g = 9.81$ m/s^2, $\sqrt{gh} = 198$ m/s.
- **Riemann problem (theorem).** For every pair of states with $h_L, h_R \ge 0$ the Riemann problem has a unique solution of shocks and rarefactions. A dry region forms in the middle exactly when $u_R - u_L \ge 2(\sqrt{gh_L} + \sqrt{gh_R})$. This follows from the two rarefaction branches $u_* = u_L + 2(\sqrt{gh_L} - \sqrt{gh_*})$ and $u_* = u_R - 2(\sqrt{gh_R} - \sqrt{gh_*})$, which cannot meet at any $h_* > 0$ under that condition (LeVeque 2002, Sections 13.8 to 13.10).
- **Energy (theorem).** For smooth solutions the energy $\eta = \frac12hu^2 + \frac12gh^2 + ghB$ is conserved. Across a bore it decreases. This is the entropy condition of the system.
- **Accuracy.** Near bores and fronts the $L^1$ error of any shock capturing scheme is at best first order; this is the usual measurement in the literature, not a proved rate for the system.

## Reductions

- **To the isentropic Euler equations.** With $\rho \to h$ and $p = \frac12gh^2$, the shallow water system is isentropic gas dynamics with $\gamma = 2$. Riemann solvers carry over.
- **To the wave equation.** Linearization about rest gives $\eta_{tt} = gH\eta_{xx}$, the model of [height field water](/height-field-water/).
- **From the incompressible Navier-Stokes equations.** Depth averaging of the free surface [Navier-Stokes equations](/navier-stokes-equations/) under the long wave assumption gives the shallow water equations.
- **To Riemann problems.** A Godunov type scheme reduces each step to one [Riemann problem](/riemann-problem/) per cell face.

## Applications

- Rivers, floods and dam break studies, with friction and real bottom data.
- Tsunami propagation across ocean basins and run up on coasts.
- Storm surges and tides.
- The atmosphere and the ocean as a rotating fluid layer, a standard test system for climate model dynamical cores.
- Water surfaces in games and films: [height field water](/height-field-water/) and the [fluid simulation for animation](/fluid-simulation-for-animation/) pipeline use the linear or the full equations.

## References
