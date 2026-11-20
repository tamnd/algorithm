---
tag: N9GXAG
kind: problem
slug: linear-boltzmann-transport-equation
name: Linear Boltzmann transport equation
aliases:
- neutron transport equation
area: scientific-computing/particle-transport
level: core
summary: The balance of particles in position, direction and energy under streaming, absorption, scattering and sources, for neutrons, photons and radiation.
prereqs: [advection-equation]
see_also: [analog-monte-carlo-transport, discrete-ordinates-method, source-iteration, diffusion-approximation-of-transport, k-eigenvalue-problem, neumann-series, rendering-equation, volumetric-path-tracing]
sources:
  - book: isbn:9780471092452
    title: E. E. Lewis and W. F. Miller, Jr., Computational Methods of Neutron Transport, Wiley, 1984
    locator: the opening chapter on the transport equation (its integro-differential and integral forms, boundary conditions and the eigenvalue problem) and the later chapters on discrete ordinates, spherical harmonics and Monte Carlo
  - book: isbn:9780486462936
    title: Jerome Spanier and Ely M. Gelbard, Monte Carlo Principles and Neutron Transport Problems, Dover edition, 2008
    locator: the chapters on the integral form of the transport equation and its Neumann series solution by random walks
  - book: isbn:9780849360749
    title: Iván Lux and László Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapters on the transport equation, its integral forms and the analog game
  - book: isbn:9783527407606
    title: Malvin H. Kalos and Paula A. Whitlock, Monte Carlo Methods, second edition, Wiley-VCH, 2008
    locator: Chapter 6, on the Monte Carlo solution of integral equations and of radiation transport
---

The linear Boltzmann transport equation is the balance law for a population of particles that fly in straight lines and interact only with a fixed background medium: neutrons in a reactor, gamma rays in a shield, photons in a star or in the atmosphere, light in fog. The unknown is the angular flux $\psi(r, \Omega, E, t)$, the number of particles per unit volume, solid angle and energy at position $r$, moving in direction $\Omega$ with energy $E$, times their speed $v$. The particles stream along $\Omega$, are removed by collisions at the rate $\Sigma_t$ per unit path, and reappear in other directions and energies by scattering, by fission or from an external source. The equation is linear because the particles are far fewer than the atoms of the medium, so they do not collide with each other and do not change the medium. The full Boltzmann equation of a gas, where molecules collide with molecules, is quadratic in the unknown; this page covers the linear case only. In steady state the equation is

$$\Omega \cdot \nabla \psi + \Sigma_t(r, E)\, \psi = \int_0^\infty \!\! \int_{4\pi} \Sigma_s(r, E' \to E, \Omega' \cdot \Omega)\, \psi(r, \Omega', E')\, d\Omega'\, dE' + q(r, \Omega, E),$$

with a boundary condition for the directions that enter the domain.

## In plain words

Picture a cloud of tiny balls that fly in straight lines through a material. Now and then a ball hits an atom. Then it may be swallowed, or it may bounce off in a new direction with a new speed. New balls also start from sources.

The transport equation keeps the books for this cloud. At each place, in each direction and at each speed, it says that the balls that arrive equal the balls that leave. Balls arrive because they fly in from upstream, because they bounce into this direction, or because a source makes them. Balls leave because they hit an atom.

The balls never hit each other, only the atoms. That makes the problem much simpler than the motion of a gas: twice the source gives twice the balls everywhere.

## Definition

**Data.** A domain $V$ in space with boundary $\partial V$ and outward normal $n$. The macroscopic total cross section $\Sigma_t(r, E) \ge 0$, in inverse length, so that $1/\Sigma_t$ is the mean free path. The scattering kernel $\Sigma_s(r, E' \to E, \Omega' \cdot \Omega) \ge 0$, which depends only on the cosine of the scattering angle in an isotropic medium. A source $q \ge 0$. In a multiplying medium, a fission term $\frac{\chi(E)}{4\pi}\int \nu\Sigma_f(r, E')\, \phi(r, E')\, dE'$ is added to the right side.

**Unknown.** The angular flux $\psi(r, \Omega, E)$. The scalar flux is $\phi(r, E) = \int_{4\pi} \psi\, d\Omega$. Reaction rates are integrals $\int \Sigma_x \phi$, which are what the methods of this area estimate.

**Boundary conditions.** Vacuum: $\psi(r, \Omega, E) = 0$ for $r \in \partial V$ and $\Omega \cdot n < 0$, so nothing enters. Reflecting: the incoming flux equals the outgoing flux in the mirror direction. An incoming flux can also be prescribed.

**Time dependence.** The time-dependent equation adds $\frac{1}{v}\frac{\partial \psi}{\partial t}$ on the left and needs an initial condition.

**The integral form.** Integrating along the characteristic line through $r$ in direction $\Omega$ gives

$$\psi(r, \Omega, E) = \int_0^{R(r, -\Omega)} e^{-\tau(r, r - s\Omega, E)}\, S(r - s\Omega, \Omega, E)\, ds + \text{boundary term},$$

where $S$ is the right side of the equation (scattering plus source), $R$ is the distance to the boundary in direction $-\Omega$, and $\tau(r, r', E) = \int_0^{|r - r'|} \Sigma_t$ along the segment is the optical depth. With isotropic scattering and an isotropic source in a domain with vacuum boundary, the scalar flux alone satisfies

$$\phi(r) = \int_V \frac{e^{-\tau(r, r')}}{4\pi |r - r'|^2}\, \big(\Sigma_s(r')\phi(r') + q(r')\big)\, dr',$$

an integral equation of the second kind. This form is what Monte Carlo methods sample: $e^{-\tau}$ is the probability of flying from $r'$ to $r$ without collision, and $1/(4\pi|r - r'|^2)$ is the spreading over the sphere.

**The slab.** In a slab $0 \le x \le L$ with isotropic scattering and one energy, let $\mu$ be the cosine of the angle with the $x$ axis and $\psi(x, \mu)$ the flux integrated over the azimuth. The convention of this area is $\phi(x) = \int_{-1}^{1} \psi(x, \mu)\, d\mu$, and then

$$\mu \frac{\partial \psi}{\partial x} + \Sigma_t \psi = \frac{\Sigma_s}{2}\phi + \frac{Q}{2},$$

where $Q$ is the isotropic source per unit length.

## Variants

- **One-speed or grey problems.** One energy, the model problem of most analysis.
- **Multigroup problems.** The energy range is cut into groups with constant cross sections, as in the [multigroup approximation](/multigroup-approximation/).
- **Fixed-source problems.** A given source and a subcritical medium, for shielding and detectors.
- **Eigenvalue problems.** No external source and a fission term divided by $k$; the [k-eigenvalue problem](/k-eigenvalue-problem/) asks for the largest $k$ and its eigenfunction.
- **Time-dependent problems.** Pulsed sources, reactor kinetics, and thermal radiation, where the medium emits as a function of its temperature and the equation is coupled to a nonlinear energy equation, as in [implicit Monte Carlo](/implicit-monte-carlo/).
- **Charged particles.** Electrons and ions have very many small-angle collisions; the transport equation still holds, but it is solved with the [condensed history method](/condensed-history-method/).
- **The adjoint equation.** Directions are reversed and the source is a detector response; its solution is the importance function of the [adjoint method](/adjoint-importance-function/).

## Examples

**A beam through an absorber.** A beam enters a slab with $\Sigma_s = 0$ and $\Sigma_t L = 2$, normal to the face. The equation is $d\psi/dx = -\Sigma_t \psi$, so the transmitted fraction is $e^{-2} = 0.135335$. This is a theorem and the test of [free-flight sampling](/free-flight-sampling/).

**An infinite uniform medium.** With a uniform isotropic source $Q$ per unit volume and no space dependence, $\nabla\psi = 0$ and the equation integrates over directions to $\Sigma_t \phi = \Sigma_s \phi + Q$, so $\phi = Q/\Sigma_a$ with $\Sigma_a = \Sigma_t - \Sigma_s$. A particle has a mean of $1/(1 - c)$ collisions with $c = \Sigma_s/\Sigma_t$, which is 2 for $c = 0.5$: the collision density is $\Sigma_t \phi = Q/(1 - c)$. These values are theorems and the checks of the [collision estimator](/collision-estimator/) and of [analog Monte Carlo transport](/analog-monte-carlo-transport/).

**A point source in an absorber.** An isotropic point source emitting one particle per second in an infinite medium with $\Sigma_s = 0$ gives $\phi(r) = e^{-\Sigma_t r}/(4\pi r^2)$, the kernel of the integral form. With scattering, this is the uncollided part of the flux.

**A slab with scattering.** For the slab of the first example, with $\Sigma_t L = 2$, a normal beam and $c = 0.5$, the analog Monte Carlo page measures a transmission of $0.1887$, a reflection of $0.1139$ and an absorption of $0.6973$ (a measurement). Of the transmission, the part $e^{-2} = 0.1353$ is exact: it is the uncollided beam, which does not depend on $c$. The rest comes from particles that scattered at least once.

## Known algorithms

- **Monte Carlo.** Simulate particle histories: [free-flight sampling](/free-flight-sampling/), [analog Monte Carlo transport](/analog-monte-carlo-transport/), and the [collision](/collision-estimator/) and [track-length](/track-length-estimator/) estimators, with variance reduction such as [implicit capture](/implicit-capture/). No discretization of space, direction or energy is needed.
- **Discrete ordinates.** The [discrete ordinates method](/discrete-ordinates-method/) solves the equation on a set of directions with quadrature weights, by [transport sweeps](/transport-sweep/) inside [source iteration](/source-iteration/), often with [diffusion synthetic acceleration](/diffusion-synthetic-acceleration/).
- **Spherical harmonics.** The [spherical harmonics method](/spherical-harmonics-method/) expands $\psi$ in direction by Legendre or spherical harmonic functions.
- **Characteristics.** The [method of characteristics](/method-of-characteristics-transport/) integrates the integral form along tracks through a mesh.
- **Diffusion.** The [diffusion approximation](/diffusion-approximation-of-transport/) replaces the equation by a second-order equation for $\phi$, accurate where scattering dominates and the flux is nearly isotropic.

## Bounds

**Source iteration converges in a subcritical problem.** With no fission, $c = \Sigma_s/\Sigma_t \le c_{\max} < 1$ everywhere, the map that takes a scattering source to the next one has norm at most $c_{\max}$ in the norm of total collision rate, because each collision makes at most $c_{\max}$ particles on average. So the [Neumann series](/neumann-series/) of collision generations converges, and the error after $n$ steps is at most $c_{\max}^n$ times the initial error. This is a theorem. In a bounded domain with vacuum boundary and $\Sigma_t$ bounded, the series also converges for $c = 1$, because each generation loses a positive fraction by leakage, but the rate can be very slow in a thick domain, which is the reason for acceleration methods.

**Dimension.** The steady problem lives in a phase space of three space variables, two direction variables and one energy variable. A deterministic grid with $N_x$ cells, $N_\Omega$ directions and $N_g$ groups has $N_x N_\Omega N_g$ unknowns per sweep. Monte Carlo has a statistical error of order $N^{-1/2}$ in the number of histories, by the [central limit theorem](/central-limit-theorem/), whatever the dimension; the constant depends on the problem and can be very large for deep penetration.

## Reductions

- **To an integral equation.** The integral form above is a Fredholm equation of the second kind, and its Neumann series is the sum over collision generations. Random walks sample this series, as in [Monte Carlo integration](/monte-carlo-integration/).
- **To diffusion.** In a thick, scattering medium an asymptotic expansion in the ratio of mean free path to the size of the domain reduces the equation to a diffusion equation for $\phi$.
- **The rendering equation.** The [rendering equation](/rendering-equation/) is the same balance for light between surfaces with no medium; with a medium, [volumetric path tracing](/volumetric-path-tracing/) solves this equation.
- **From the eigenvalue problem.** The k-eigenvalue problem is solved by [power iteration](/power-iteration/) on fission generations, each step a fixed-source problem.

## Applications

Nuclear reactor design and safety, where the flux gives the power and the multiplication factor. Radiation shielding for reactors, accelerators and spacecraft. Medical physics: dose in radiotherapy and imaging, with photons and electrons. Radiative transfer in stellar atmospheres, in the Earth's atmosphere and in combustion. Detector design, oil well logging and neutron activation analysis. Rendering of fog, smoke, skin and clouds in computer graphics.

## References
