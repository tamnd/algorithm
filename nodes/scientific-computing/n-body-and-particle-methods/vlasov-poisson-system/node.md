---
tag: BE006M
kind: problem
slug: vlasov-poisson-system
name: Vlasov-Poisson system
aliases:
- Vlasov-Poisson equations
area: scientific-computing/n-body-and-particle-methods
level: core
summary: The kinetic equations of a collisionless plasma or star system, a phase-space density advected by the field that it creates through Poisson's equation.
model: real-ram
prereqs: [poisson-equation, advection-equation]
see_also: [plasma-particle-in-cell, particle-mesh-method, method-of-characteristics, operator-splitting, gravitational-n-body-problem, boris-pusher, hamiltonian-systems, cloud-in-cell-assignment]
sources:
  - book: isbn:9780750310253
    title: Charles K. Birdsall and A. Bruce Langdon, Plasma Physics via Computer Simulation, Taylor and Francis, 2004 (reprint of the IOP edition of 1991)
    locator: Part 1 (the electrostatic program ES1)
  - paper: "Lev D. Landau, On the vibrations of the electronic plasma, Journal of Physics USSR 10, 1946, 25-34"
    locator: the damping of plasma waves without collisions
  - paper: doi:10.1016/0021-9991(76)90053-X
    title: Chio-Zong Cheng and Georg Knorr, The integration of the Vlasov equation in configuration space, Journal of Computational Physics 22(3), 1976, 330-351
    locator: the splitting of the Vlasov equation into shifts in x and in v and their solution by interpolation
  - paper: doi:10.1007/BF01232273
    title: Pierre-Louis Lions and Benoit Perthame, Propagation of moments and regularity for the 3-dimensional Vlasov-Poisson system, Inventiones Mathematicae 105, 1991, 415-430
    locator: the propagation of velocity moments and global smooth solutions in 3D
  - paper: doi:10.1016/0022-0396(92)90033-J
    title: Klaus Pfaffelmoser, Global classical solutions of the Vlasov-Poisson system in three dimensions for general initial data, Journal of Differential Equations 95(2), 1992, 281-303
    locator: global classical solutions in 3D for smooth data of compact support
  - paper: doi:10.1063/1.1706638
    title: John Dawson, One-dimensional plasma model, The Physics of Fluids 5(4), 1962, 445-459
    locator: the measurement of Landau damping in a charge sheet simulation
---

The Vlasov-Poisson system describes a gas of charged particles, or of stars, so thin that collisions between them do not matter. Its unknown is the phase space density $f(\mathbf{x}, \mathbf{v}, t)$, the number of particles per unit volume of position and velocity. The density is carried along the particle orbits, and the orbits are bent by a field that the density itself creates through Poisson's equation. The computational problem is to find $f$ at later times from $f$ at $t = 0$. The two main families of methods are particle methods, such as [particle-in-cell plasma simulation](/plasma-particle-in-cell/), and grid methods in phase space, such as the semi-Lagrangian splitting of Cheng and Knorr. Linear Landau damping, the decay of a small wave without collisions, is the standard test for both.

## In plain words

Think of a cloud of electrons in a box. Instead of tracking each electron, we keep a map that says how many electrons are at each place with each speed. Every electron moves in a straight line at its own speed, and the electric field bends its path. The field, in turn, comes from where the electrons are.

So the map moves itself: the electrons make the field, and the field moves the electrons. The problem is to start from a given map and find the map at a later time. A small ripple in such a cloud dies away even though the electrons never collide. Electrons that ride with the wave take energy from it. This effect, found by Landau, is the usual first test of a program for this problem.

## Definition

The domain is $\Omega \times \mathbb{R}^d$, where $\Omega$ is the periodic box $[0, L)^d$ (or all of $\mathbb{R}^d$) and $d \in \{1, 2, 3\}$. For electrons with a fixed uniform ion background in normalized units ($\epsilon_0 = 1$, charge $-1$, mass 1, times in units of $1/\omega_p$, lengths in units of the Debye length $\lambda_D$), the system is

$$\partial_t f + \mathbf{v} \cdot \nabla_{\mathbf{x}} f - \mathbf{E} \cdot \nabla_{\mathbf{v}} f = 0, \qquad \mathbf{E} = -\nabla \phi, \qquad -\Delta \phi = \rho = 1 - \int f \, d\mathbf{v}.$$

For a self-gravitating system with $G = 1$, the force term is $-\nabla \phi \cdot \nabla_{\mathbf{v}} f$ with $\Delta \phi = 4\pi \int f \, d\mathbf{v}$ (on a periodic box, minus its mean); the sign makes like masses attract.

- **Input:** the initial density $f_0(\mathbf{x}, \mathbf{v}) \ge 0$ with finite mass and kinetic energy, the box, and a final time $T$.
- **Output:** $f(\cdot, \cdot, t)$ for $t \in [0, T]$, or functionals of it such as the field energy $W(t) = \tfrac{1}{2} \int |\mathbf{E}|^2 \, d\mathbf{x}$, to a stated accuracy.

Along a characteristic, $d\mathbf{x}/dt = \mathbf{v}$ and $d\mathbf{v}/dt = -\mathbf{E}(\mathbf{x}, t)$, the density $f$ is constant. So $f(\mathbf{x}, \mathbf{v}, t) = f_0(\mathbf{X}_0, \mathbf{V}_0)$, where $(\mathbf{X}_0, \mathbf{V}_0)$ is the start of the characteristic through $(\mathbf{x}, \mathbf{v})$ at time $t$. The flow preserves phase space volume, and the system conserves the total mass, momentum and energy $\tfrac{1}{2} \iint |\mathbf{v}|^2 f + W$, and every integral $\iint G(f)$, for example the $L^p$ norms and the maximum of $f$.

## Variants

- **1D1V.** One space and one velocity dimension, the usual test case; it has the same structure in 2 dimensions of phase space.
- **Vlasov-Maxwell.** The field obeys Maxwell's equations, with the magnetic force $\mathbf{v} \times \mathbf{B}$, for magnetized or relativistic plasmas.
- **Several species.** Electrons and ions each have a density; with mobile ions, ion acoustic waves appear.
- **Gravitational Vlasov-Poisson** (the collisionless Boltzmann equation of stellar dynamics), for galaxies and for dark matter in cosmology.
- **Linearized Vlasov-Poisson.** Around a homogeneous equilibrium $f_0(\mathbf{v})$, which gives the dispersion relation of plasma waves.
- **With collisions.** A Fokker-Planck or Landau collision term on the right gives a collisional kinetic model.

## Examples

**Linear Landau damping.** Take $d = 1$, $f_0(x, v) = (1 + \alpha \cos kx) \, e^{-v^2/2} / \sqrt{2\pi}$ with small $\alpha$, on $[0, 2\pi/k)$. The field behaves like $e^{-\mathrm{i}\omega t}$ with complex $\omega = \omega_r + \mathrm{i}\gamma$, where $\omega$ is the root, with the largest imaginary part, of

$$1 + \frac{1}{k^2} \bigl(1 + \zeta Z(\zeta)\bigr) = 0, \qquad \zeta = \frac{\omega}{\sqrt{2}\, k},$$

and $Z$ is the plasma dispersion function, the analytic continuation of $\pi^{-1/2} \int e^{-s^2} / (s - \zeta) \, ds$ from the upper half plane. Solving this equation numerically gives:

| $k$ | $\omega_r$ | $\gamma$ |
|---|---|---|
| 0.3 | 1.1598 | -0.0126 |
| 0.4 | 1.2851 | -0.0661 |
| 0.5 | 1.4157 | -0.1534 |

So for $k = 0.5$ the field energy oscillates at $2\omega_r$ and its envelope decays as $e^{2\gamma t} = e^{-0.3067 t}$. The weak damping formula $\gamma \approx -\sqrt{\pi/8} \, k^{-3} e^{-1/(2k^2) - 3/2}$ gives $-0.151$ at $k = 0.5$, and the Bohm-Gross relation $\omega_r^2 \approx 1 + 3k^2$ gives $1.323$; both are approximations for small $k$ (heuristics, not bounds).

A measurement with the code of the [plasma particle-in-cell](/plasma-particle-in-cell/) page ($N = 100\,000$ particles, $M = 32$ grid points, $h = 0.1$, $\alpha = 0.01$, a quiet start) gives a decay rate of 0.147 and a frequency of about 1.42 for the amplitude of the mode $k = 0.5$, fitted for $t$ from 2.5 to 18.

**Two-stream instability.** Two cold or warm beams with opposite velocities $\pm v_0$ have growing modes for a band of $k$, and $f$ forms vortices in phase space as the instability saturates.

**Jeans instability.** In the gravitational case, a uniform Maxwellian of density $\rho_0$ and velocity spread $\sigma$ is unstable to waves longer than the Jeans length $\sigma \sqrt{\pi / (G \rho_0)}$.

## Known algorithms

- **Particle-in-cell.** Sample $f_0$ by $N$ macroparticles, compute the field with a [particle-mesh](/particle-mesh-method/) step on $M$ grid points, and move the particles along the characteristics. Cost $\Theta(N + M)$ per step in 1D with a Gauss solve, or $\Theta(N + M \log M)$ with an FFT. The error has a statistical part of size about $N_c^{-1/2}$ for $N_c$ particles per cell (a heuristic). See [plasma particle-in-cell](/plasma-particle-in-cell/).
- **Semi-Lagrangian splitting (Cheng and Knorr 1976).** Store $f$ on a phase space grid. A half step of $\partial_t f + v \partial_x f = 0$ is a shift in $x$ by $v h/2$ for each $v$; a full step of $\partial_t f - E \partial_v f = 0$ is a shift in $v$ by $-E h$ for each $x$; then another half shift in $x$. Each shift is done by interpolation (Fourier or splines), so the step has no CFL limit. This is [operator splitting](/operator-splitting/) of Strang type, second order in $h$. The cost is $\Theta(M_x M_v)$ per step in 1D1V with spline interpolation, more with Fourier interpolation.
- **Eulerian grid methods.** Finite volume or finite difference schemes for the [advection equation](/advection-equation/) in phase space, with conservative and positivity-preserving variants.
- **Spectral methods.** Fourier in $x$ and Fourier or Hermite in $v$.
- **N-body methods.** For the gravitational case, the characteristics are followed by N-body codes with softened forces ([gravitational N-body problem](/gravitational-n-body-problem/)), with particle-mesh, tree or P3M forces.

## Bounds

- **Existence.** In 3D, smooth initial data of compact support have a unique global classical solution (Pfaffelmoser 1992). Lions and Perthame (1991) showed, by a different method, that velocity moments of high enough order stay finite, which gives global smooth solutions for data with such moments. These are theorems on the continuous problem.
- **Grid cost.** A phase space grid has $M_x^d M_v^d$ points, which is $M^6$ in 3D with $M$ points per axis. This is the main reason for using particles in 3D.
- **Filamentation.** Free streaming turns a perturbation $\cos(kx)$ of $f$ into $\cos(k(x - vt))$, whose scale in $v$ is $2\pi / (k t)$. A velocity grid of spacing $\Delta v$ resolves it only for $t < 2\pi / (k \Delta v)$, and on a uniform velocity grid the initial perturbation returns at the recurrence time $T_R = 2\pi / (k \Delta v)$ (a theorem for the free streaming part). For $k = 0.5$ and $\Delta v = 0.1$, $T_R \approx 126$.
- **Particle noise.** For PIC, the statistical error of a grid quantity falls as $N_c^{-1/2}$; halving the noise costs 4 times the particles (a heuristic from the central limit theorem).
- **Nonlinear Landau damping.** Mouhot and Villani (2011) proved that small perturbations of stable homogeneous equilibria in the periodic box damp in the nonlinear problem, for analytic or Gevrey data.

## Reductions

- **To ordinary differential equations.** By the method of characteristics, $f$ is known once the characteristics are known, so the problem reduces to the motion of particles in the self-consistent field; PIC is a Monte Carlo version of this reduction. See [method of characteristics](/method-of-characteristics/).
- **To advection equations.** Splitting reduces one step to constant coefficient [advection](/advection-equation/) in $x$ and in $v$.
- **From the N-body problem.** The Vlasov-Poisson system is the mean field limit of $N$ particles with forces scaled by $1/N$ as $N \to \infty$; this is a theorem for smooth interaction kernels, and the Coulomb and Newton kernels need softening or more delicate arguments.
- **To fluid models.** Taking velocity moments gives the continuity and momentum equations, and a closure for the pressure gives a fluid model; the closure loses Landau damping.

## Applications

Plasma physics: waves and instabilities in fusion plasmas, the solar wind and the magnetosphere, beam physics and laser-plasma interaction. Astrophysics: the dynamics of galaxies and star clusters on time scales shorter than the relaxation time, and the growth of structure in cold dark matter cosmology. Landau damping and the two-stream instability serve as standard tests of new kinetic codes.

## References
