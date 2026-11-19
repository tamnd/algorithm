---
tag: GHR7QP
kind: technique
slug: chapman-enskog-expansion
name: Chapman-Enskog expansion
aliases:
- Chapman-Enskog analysis
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: A multiscale expansion in the Knudsen number that derives the Navier-Stokes equations and their viscosity from a kinetic equation such as lattice Boltzmann.
prereqs: [lattice-boltzmann-method, bgk-collision-operator, navier-stokes-equations]
see_also: [multiple-relaxation-time-lattice-boltzmann, bounce-back-boundary-condition, heat-equation, euler-equations-of-gas-dynamics, consistency, local-truncation-error, direct-simulation-monte-carlo]
sources:
  - book: isbn:9780521408448
    title: "Sydney Chapman and T. G. Cowling, The Mathematical Theory of Non-uniform Gases, 3rd edition, Cambridge University Press, 1970"
    locator: "the chapters on the solution of the Boltzmann equation by successive approximation (the Chapman-Enskog method) and on viscosity and conduction"
  - book: isbn:9783319446479
    title: "Timm Krüger, Halim Kusumaatmaja, Alexandr Kuzmin, Orest Shardt, Goncalo Silva and Erlend Magnus Viggen, The Lattice Boltzmann Method: Principles and Practice, Springer, 2017"
    locator: "Chapter 4 (analysis of the lattice Boltzmann equation, the Chapman-Enskog analysis)"
  - paper: doi:10.1209/0295-5075/17/6/001
    title: "Y. H. Qian, D. d'Humières and P. Lallemand, Lattice BGK models for Navier-Stokes equation, Europhysics Letters 17 (1992) 479-484"
  - paper: doi:10.1103/PhysRevA.45.R5339
    title: "Hudong Chen, Shiyi Chen and William H. Matthaeus, Recovery of the Navier-Stokes equations using a lattice-gas Boltzmann method, Physical Review A 45 (1992) R5339-R5342"
  - paper: doi:10.1103/PhysRevE.61.6546
    title: "Pierre Lallemand and Li-Shi Luo, Theory of the lattice Boltzmann method: Dispersion, dissipation, isotropy, Galilean invariance, and stability, Physical Review E 61 (2000) 6546-6562"
---

The Chapman-Enskog expansion derives the equations of fluid flow from a kinetic equation. It expands the particle distribution around the local equilibrium in powers of the Knudsen number $\epsilon$, the ratio of the mean free path to the length of the flow, and expands the time derivative in the same way. The first order gives the Euler equations, and the second order gives the Navier-Stokes equations with a viscosity expressed in the collision time. Chapman and Enskog built it for the Boltzmann equation of a dilute gas. In lattice Boltzmann work it is the standard way to show that the scheme is consistent with Navier-Stokes and to find $\nu = c_s^2(\tau - \frac12)$ for the [BGK collision](/bgk-collision-operator/). It is a formal asymptotic expansion: it shows what equations the scheme approximates, but it is not a convergence proof.

## In plain words

A gas is made of particles that collide very often. Between collisions the particles carry mass and momentum from place to place. If collisions are frequent compared with the time it takes the flow to change, the particle velocities at each point are almost in balance, and only a small correction is left. The Chapman-Enskog method writes the distribution as the balanced state plus small corrections, sorted by how small they are. The balanced state alone gives inviscid flow. The first correction gives viscosity, because it describes how much the velocities lag behind the flow. Applied to a lattice Boltzmann scheme, the same steps tell you which equations the scheme solves and with which viscosity.

## When it applies

- A kinetic equation $\partial_t f + \xi \cdot \nabla f = \Omega(f)$ or a lattice Boltzmann scheme, whose collision $\Omega$ has an equilibrium $f^{\mathrm{eq}}$ that depends on the local conserved moments only (density, momentum and, for thermal models, energy).
- The Knudsen number is small: the flow varies on length scales much larger than the mean free path, and on time scales much longer than the collision time. For lattice Boltzmann this means smooth flow on many lattice nodes.
- The Mach number is small, for lattice equilibria that are second order in $u$: the expansion then also shows the $O(u^3)$ error terms that break Galilean invariance.
- It does not apply to strongly rarefied flow (Knudsen number of order 1 or more), to shock interiors, or to the first steps after a start far from equilibrium.

## The template

```pseudo id=main
CHAPMAN-ENSKOG(kinetic equation, f^eq, conserved moments φ)
L1  Taylor-expand the update in Δt (lattice schemes only): D_i f_i + (Δt/2) D_i^2 f_i + ... = Ω_i / Δt, with D_i = ∂_t + c_i · ∇
L2  write f = f^(0) + ε f^(1) + ε^2 f^(2) + ..., with f^(0) = f^eq
L3  solvability: Σ φ f^(k) = 0 for every k ≥ 1, so the conserved moments come from f^(0) only
L4  write ∇ = ε ∇^(1) and ∂_t = ε ∂_t^(1) + ε^2 ∂_t^(2)
L5  order ε: take moments with φ to get the Euler-level equations for ∂_t^(1); solve for f^(1) in terms of f^(0)
L6  order ε^2: take moments with φ to get the ∂_t^(2) equations; the momentum flux of f^(1) gives the viscous stress
L7  recombine ∂_t = ε ∂_t^(1) + ε^2 ∂_t^(2) into one macroscopic equation, and read off the transport coefficients
```

The holes are the kinetic equation (its collision operator and, for a lattice, its velocity set and weights), the equilibrium $f^{\mathrm{eq}}$, and the list $\phi$ of conserved quantities (1 and $c$ for isothermal lattice Boltzmann).

Line L1 is the step that makes the lattice result differ from the continuous one: the second-order term $\frac{\Delta t}2 D_i^2 f_i$ is where the $-\frac12$ in $\tau - \frac12$ comes from. Line L2 is the expansion in the Knudsen number. Line L3 says that the corrections carry no mass or momentum; this fixes the expansion uniquely and makes the collision invariants come only from the equilibrium. Line L4 is the multiscale step: the fast convective time scale $t_1$ and the slow diffusive time scale $t_2$ are treated as independent. At order $\epsilon$ (line L5), the collision term gives $f^{(1)} = -\tau D_i^{(1)} f^{(0)}$, and the moments of $D_i^{(1)} f^{(0)}$ are the Euler equations. At order $\epsilon^2$ (line L6), the term $D_i^{(1)} f^{(1)}$ and the Taylor term combine into $(1 - \frac{\Delta t}{2\tau}) D_i^{(1)} f^{(1)}$; its moments give the viscous terms. Line L7 adds the two time scales back together.

The result is a formal asymptotic statement: if the scheme has a solution with the assumed smooth multiscale structure, that solution satisfies the macroscopic equations up to terms of order $\epsilon^2$. The expansion does not prove that such a solution exists or that the scheme converges.

## Classic examples

**D1Q3 diffusion, in full.** Velocities $c_i = 0, 1, -1$, weights $\frac23, \frac16, \frac16$, equilibrium $f_i^{\mathrm{eq}} = w_i\rho$, lattice units, BGK collision with time $\tau$. The only conserved quantity is $\rho = \sum f_i$. Line L1 gives $D_if_i + \frac12 D_i^2f_i = -\frac1\tau(f_i - w_i\rho)$ up to third-order terms. At order $\epsilon$:

$$D_i^{(1)} f_i^{(0)} = -\frac1\tau f_i^{(1)}, \qquad \text{so} \qquad f_i^{(1)} = -\tau(\partial_t^{(1)} + c_i \partial_x^{(1)}) w_i\rho.$$

Its zeroth moment gives $\partial_t^{(1)}\rho + \partial_x^{(1)}\sum_i c_iw_i\rho = \partial_t^{(1)}\rho = 0$, because $\sum c_iw_i = 0$: there is no convection. At order $\epsilon^2$:

$$\partial_t^{(2)} f_i^{(0)} + \Bigl(1 - \frac1{2\tau}\Bigr) D_i^{(1)} f_i^{(1)} = -\frac1\tau f_i^{(2)}.$$

The zeroth moment, with $\sum f_i^{(1)} = \sum f_i^{(2)} = 0$, is $\partial_t^{(2)}\rho + (1 - \frac1{2\tau})\partial_x^{(1)}\sum_i c_if_i^{(1)} = 0$. From the expression for $f^{(1)}$ and $\sum c_i^2w_i = \frac13$, $\sum_i c_if_i^{(1)} = -\frac\tau3\partial_x^{(1)}\rho$. So $\partial_t^{(2)}\rho = \frac13(\tau - \frac12)\partial_x^{(1)}\partial_x^{(1)}\rho$, and line L7 gives the [heat equation](/heat-equation/)

$$\partial_t\rho = D\,\partial_{xx}\rho, \qquad D = \frac13\Bigl(\tau - \frac12\Bigr).$$

Without the Taylor term of line L1 the result would be $D = \tau/3$. A run checks this: on a periodic lattice of $N$ nodes, start from $\rho = 1 + 0.01\sin(2\pi x/N)$ and measure the decay rate of the mode over the second half of $N^2/2$ steps.

| $\tau$ | predicted $D$ | measured, $N = 16$ | $N = 32$ | $N = 64$ |
|---|---|---|---|---|
| 0.6 | 0.033333 | 0.033747 | 0.033436 | 0.033359 |
| 1.0 | 0.166667 | 0.166659 | 0.166666 | 0.166667 |
| 2.0 | 0.5 | 0.438741 | 0.486406 | 0.496739 |

The relative difference falls by a factor of about 4 each time $N$ doubles, as it should: it is the next order of the expansion, of size $(k\tau)^2$ for wavenumber $k = 2\pi/N$. The value $\tau/3$ is ruled out at once: for $\tau = 2$ it would be $0.667$.

**D2Q9 lattice BGK to Navier-Stokes.** The same steps with the conserved moments $\rho$ and $\rho u$ on the [lattice Boltzmann](/lattice-boltzmann-method/) D2Q9 lattice give, at order $\epsilon$, the Euler equations with pressure $p = c_s^2\rho$, and at order $\epsilon^2$ the viscous stress $\rho\nu(\nabla u + \nabla u^T)$ with $\nu = c_s^2(\tau - \frac12)$ in lattice units (Qian, d'Humières and Lallemand 1992; Chen, Chen and Matthaeus 1992). The analysis also shows the error terms: the third moment of the second-order equilibrium misses the term $\rho uuu$, which gives errors of order $u^3$ in the stress, so the result holds for small Mach number (Krüger et al. 2017, Chapter 4).

**The viscosity of MRT.** For the [multiple-relaxation-time method](/multiple-relaxation-time-lattice-boltzmann/) the same expansion, done in moment space, gives the shear viscosity $\nu = \frac13(\frac1{s_\nu} - \frac12)$ from the stress rate and a bulk viscosity from the energy rate, while the rates of the heat flux moments do not enter the Navier-Stokes level (Lallemand and Luo 2000). It shows that those rates are free at this order, which is what the wall tuning of [bounce-back](/bounce-back-boundary-condition/) uses.

**The continuous BGK gas.** For the Boltzmann equation with the continuous BGK operator, the expansion gives the compressible Navier-Stokes equations with dynamic viscosity $\mu = \tau p$ and a Prandtl number of 1. For the full Boltzmann collision integral, Chapman and Enskog obtained the viscosity and heat conductivity of a dilute gas from integral equations for $f^{(1)}$ (Chapman and Cowling 1970).

## Variations

- **Higher orders.** Order $\epsilon^3$ gives the Burnett equations. Bobylev (1982) showed that the Burnett equations are unstable for short waves, so the expansion is asymptotic and not convergent in general.
- **Diffusive scaling.** An expansion with $\Delta t \sim \Delta x^2$ (time scales as the square of space) and a small Mach number leads straight to the incompressible Navier-Stokes equations. It is an alternative to the two time scales of line L4.
- **Asymptotic analysis of the scheme.** Instead of expanding in $\epsilon$, expand the discrete scheme in $\Delta x$ with fixed $\tau$ (Junk and coworkers' asymptotic analysis). This gives the same leading equations, and also the initial and boundary layers that the Chapman-Enskog method does not see.
- **Hilbert expansion.** An expansion in $\epsilon$ without the multiscale time derivative. It needs the macroscopic fields to be expanded too, and gives the hierarchy of Euler and linearized equations.
- **Grad moment method.** Instead of an expansion, take a closure for a finite set of moments (13 moments in Grad's method). It is used for moderately rarefied gas.

## Pitfalls

- **Forgetting the Taylor term of line L1.** Doing the expansion of the continuous BGK equation and then reading off $\nu = c_s^2\tau$ for the lattice scheme gives the wrong viscosity; the lattice value is $c_s^2(\tau - \frac12)$. The D1Q3 table shows the difference.
- **Dropping the solvability condition of line L3.** Without $\sum\phi f^{(k)} = 0$ the split between $f^{(0)}$ and the corrections is not unique, and the moments of line L6 pick up spurious terms.
- **Reading the result as a convergence proof.** The expansion says which equation a smooth solution satisfies up to $O(\epsilon^2)$. Stability is a separate question, for example by the [von Neumann analysis](/von-neumann-stability-analysis/) of Lallemand and Luo; BGK with $\tau$ near $\frac12$ is consistent but often unstable.
- **Using the result outside its regime.** At large Knudsen number, inside shocks, or near walls on a coarse lattice, the higher-order terms are not small. The $\tau = 2$ column of the D1Q3 table shows a 12 percent error at $N = 16$.
- **Mixing the time scales.** $\partial_t^{(1)}$ and $\partial_t^{(2)}$ act on the same fields; after line L7 they must be added with their powers of $\epsilon$, not used as separate equations.

## Exercises

1. Repeat the D1Q3 calculation with the equilibrium $f_i^{\mathrm{eq}} = w_i\rho(1 + 3c_iU)$ for a constant velocity $U$, and show that the result is the advection-diffusion equation $\partial_t\rho + U\partial_x\rho = D\partial_{xx}\rho$ with $D = (\tau - \frac12)(\frac13 - U^2)$. The $U^2$ term is the D1Q3 version of the Galilean error.
2. Show that with the MRT collision and the rate $s_\nu$ on the stress moments, the D2Q9 calculation gives $\nu = \frac13(\frac1{s_\nu} - \frac12)$.
3. Check the second column of the table: for $\tau = 1$ the D1Q3 scheme is FTCS with $\mu = \frac16$, whose amplification factor $1 - \frac23\sin^2(k/2)$ gives an effective $D = -\ln(1 - \frac23\sin^2(k/2))/k^2$ that tends to $\frac16$ as $k \to 0$. Show that the $k^2$ term of this expansion vanishes, which is why the $\tau = 1$ column agrees so well.

## References
