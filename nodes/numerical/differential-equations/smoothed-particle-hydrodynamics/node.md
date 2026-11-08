---
tag: 9G16QJ
kind: algorithm
slug: smoothed-particle-hydrodynamics
name: Smoothed particle hydrodynamics
aliases:
- SPH
- smoothed particle hydrodynamics method
area: numerical/differential-equations
level: research
summary: "Meshless Lagrangian method: fluid particles carry mass, and density and forces come from kernel-weighted sums over neighbours, with pairwise symmetric terms that conserve momentum and energy."
solves: [riemann-problem]
model: real-ram
complexity:
  vars: {n: "the number of particles", k: "the average number of neighbours of a particle", N: "the number of time steps, ⌈T/Δt⌉"}
  time: {worst: "Θ((N + 1)(n log n + n k))"}
  space: {extra: "Θ(n k)"}
  evaluations: {worst: "(N + 1) n k"}
properties: {deterministic: true, explicit: true, lagrangian: true, meshless: true, conserves: "mass and momentum exactly, energy in the semi-discrete system", order: "2 for the kernel estimate; observed L1 order 0.6 to 0.7 with shocks", galilean_invariant: true}
history:
  year: 1977
  people: [Leon B. Lucy, Robert A. Gingold, Joseph J. Monaghan]
  note: Lucy (1977) and Gingold and Monaghan (1977) introduced SPH independently to model nonspherical stars; Monaghan's later papers gave the symmetric conservative form and the artificial viscosity used today.
prereqs: [verlet-integration, riemann-problem, fixed-radius-near-neighbors]
see_also: [lattice-boltzmann-method, finite-volume-method, godunov-method, weno-scheme, navier-stokes-equations, symplectic-integrators, molecular-dynamics, method-of-characteristics]
sources:
  - paper: "Leon B. Lucy, A numerical approach to the testing of the fission hypothesis, The Astronomical Journal 82 (1977) 1013-1024"
    locator: the first SPH computation; doi:10.1086/112164
  - paper: "Robert A. Gingold and Joseph J. Monaghan, Smoothed particle hydrodynamics, theory and application to non-spherical stars, Monthly Notices of the Royal Astronomical Society 181 (1977) 375-389"
    locator: the kernel estimate and the name; doi:10.1093/mnras/181.3.375
  - paper: "Joseph J. Monaghan, Smoothed particle hydrodynamics, Annual Review of Astronomy and Astrophysics 30 (1992) 543-574"
    locator: the symmetric momentum and energy equations, the cubic spline kernel, the artificial viscosity with α and β, time stepping; doi:10.1146/annurev.aa.30.090192.002551
  - paper: "Joseph J. Monaghan, Smoothed particle hydrodynamics, Reports on Progress in Physics 68 (2005) 1703-1759"
    locator: derivation from a Lagrangian, conservation, variable smoothing lengths, applications; doi:10.1088/0034-4885/68/8/R01
  - paper: "Daniel J. Price, Smoothed particle hydrodynamics and magnetohydrodynamics, Journal of Computational Physics 231 (2012) 759-794"
    locator: a tutorial review including the Sod test, artificial dissipation switches and conservation; doi:10.1016/j.jcp.2010.12.011
  - paper: "Gary A. Sod, A survey of several finite difference methods for systems of nonlinear hyperbolic conservation laws, Journal of Computational Physics 27 (1978) 1-31"
    locator: the shock tube test problem; doi:10.1016/0021-9991(78)90023-2
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 4 (the exact Riemann solver for the Euler equations, used for the reference solution)
  - paper: "J. W. Swegle, D. L. Hicks and S. W. Attaway, Smoothed particle hydrodynamics stability analysis, Journal of Computational Physics 116 (1995) 123-134"
    locator: the tensile instability; doi:10.1006/jcph.1995.1010
---

Smoothed particle hydrodynamics (SPH) solves the equations of fluid dynamics without a mesh. The fluid is represented by particles that move with the flow and carry mass, velocity and internal energy. Any field is estimated at a point by a weighted sum over nearby particles, with a smooth bell-shaped kernel $W(r, h)$ of width $h$ as the weight; the density is $\rho_i = \sum_j m_jW(x_i - x_j, h)$, and pressure forces come from the kernel gradient. Written in a pairwise symmetric form, the forces conserve momentum exactly and energy in the semi-discrete system, and an artificial viscosity captures shocks. SPH was created for astrophysics and is widely used for free surfaces, splashing, fragmentation and large deformations, where a mesh would tangle.

## In plain words

Think of the fluid as a crowd of small blobs, each with a fixed amount of stuff. Where blobs crowd together the fluid is dense; where they spread out it is thin. To find the density at a blob, add up the masses of the blobs around it, counting close ones more and far ones less, and ignoring any beyond a fixed reach.

High pressure pushes blobs apart. Each pair of nearby blobs pushes on each other with equal and opposite forces, so the total momentum of the crowd never changes, and the work done by the push goes into or out of the blobs' heat, so total energy is kept too. When blobs rush head-on into each other, as in a shock, an extra friction term between approaching pairs turns their motion into heat instead of letting them pass through each other.

## The problem

Given $n$ particles with masses $m_i > 0$, positions $x_i$, velocities $v_i$, specific internal energies $e_i \ge 0$ and smoothing lengths $h_i > 0$, an ideal gas law $P = (\gamma - 1)\rho e$, a time step $\Delta t$ and an end time $T \ge 0$, approximate the solution at time $T$ of the one-dimensional Euler equations
$$\rho_t + (\rho v)_x = 0, \qquad (\rho v)_t + (\rho v^2 + P)_x = 0, \qquad E_t + ((E + P)v)_x = 0,$$
in Lagrangian form: $\dot x = v$, $\dot v = -P_x/\rho$, $\dot e = -(P/\rho)v_x$. Errors are measured in the $L^1$ norm of the density over a test region, against the exact solution of the [Riemann problem](/riemann-problem/). Cost is counted in pair interactions, one kernel and gradient evaluation per pair of neighbours.

## The algorithm

```pseudo id=main
SPH(x, v, m, e, h, T, Δt, γ, η)              ▷ η ≈ 1.2: smoothing length factor
L1  N ← ⌈T/Δt − δ⌉, t ← 0                      ▷ δ: relative slack 10^-9
L2  (a, ė) ← FORCES(x, v, e, h)
L3  for s ← 0 to N − 1 do τ ← step length; v½ ← v + (τ/2) a; e ← e + (τ/2) ė
L4      x ← x + τ v½; h_i ← η m_i / ρ_i
L5      (a, ė) ← FORCES(x, v½ + (τ/2) a, e, h)        ▷ predicted velocities for the viscosity
L6      v ← v½ + (τ/2) a; e ← e + (τ/2) ė; t ← t + τ
    FORCES(x, v, e, h):
L7      pairs ← all i < j with |x_i − x_j| < 2 max(h_i, h_j)     ▷ sort, then binary search
L8      ρ_i ← Σ_j m_j W_ij (self term included); P_i ← (γ − 1) ρ_i e_i; c_i ← √(γ P_i / ρ_i)
L9      for each pair: A ← P_i/ρ_i² + P_j/ρ_j² + Π_ij; a_i −= m_j A ∂_iW_ij; a_j += m_i A ∂_iW_ij;
            ė_i += (m_j/2) A (v_i − v_j) ∂_iW_ij; ė_j += (m_i/2) A (v_i − v_j) ∂_iW_ij
L10     return (a, ė)
```

The kernel is the cubic spline $W(r, h) = \frac{2}{3h}\big(1 - \frac{3}{2}q^2 + \frac{3}{4}q^3\big)$ for $q = |r|/h < 1$, $\frac{2}{3h}\cdot\frac{1}{4}(2 - q)^3$ for $1 \le q < 2$, and 0 beyond; $W_{ij}$ averages the kernels with $h_i$ and $h_j$. The Monaghan artificial viscosity is $\Pi_{ij} = (-\alpha\bar c_{ij}\mu_{ij} + \beta\mu_{ij}^2)/\bar\rho_{ij}$ with $\mu_{ij} = \bar h_{ij}v_{ij}x_{ij}/(x_{ij}^2 + 0.01\bar h_{ij}^2)$ for approaching pairs ($v_{ij}x_{ij} < 0$) and 0 otherwise, with $\alpha = 1$, $\beta = 2$ and bars for pair averages. Lines L3 to L6 are kick-drift-kick leapfrog, the [velocity Verlet](/verlet-integration/) scheme. As with the other time-stepping pages, $T = 0$ gives zero steps and a $\Delta t$ beyond $T$ gives one short step.

## Example

**Sod shock tube.** Left state $(\rho, v, P) = (1, 0, 1)$ on $[-0.75, 0)$, right state $(0.125, 0, 0.1)$ on $(0, 0.75]$, $\gamma = 1.4$, $T = 0.2$. Equal-mass particles are spaced 8 times wider on the right, so the density ratio comes from the spacing, and $h_i = 1.2$ times the local spacing. The time step is $\Delta t = 0.3\,h_{\min}/1.2$. The exact solution has a rarefaction, a contact at $x = 0.185$ and a shock at $x = 0.350$, with plateau densities 0.4263 and 0.2656 and velocity 0.9275. Observed, with the $L^1$ density error over $[-0.4, 0.4]$ (away from the free ends):

| left particles | total $n$ | steps | pair interactions | $L^1$ error | relative energy error |
|---|---|---|---|---|---|
| 80 | 90 | 72 | 14 550 | 0.0150 | 3.7e-5 |
| 160 | 180 | 143 | 55 055 | 0.0100 | 1.8e-5 |
| 320 | 360 | 285 | 213 859 | 0.0062 | 8.0e-6 |

With 360 particles the mean densities on the two plateaus are 0.4268 and 0.2636, and the velocity between rarefaction and shock is $0.937$ on average with a maximum of $0.954$, a 3% overshoot. Total momentum stays at zero to $10^{-16}$. The $L^1$ order is about 0.6 to 0.7, typical for a solution with a shock and a contact.

## Correctness

**Theorem (proved in the proof file).** (1) The cubic spline kernel has integral 1, zero first and third moments and second moment $h^2/3$, so the kernel estimate of a smooth field has error $\frac{h^2}{6}A'' + O(h^4)$. (2) Total mass and momentum are conserved exactly by the fully discrete scheme, because every pair contributes equal and opposite momentum changes; total energy $\sum m_i(\frac{1}{2}v_i^2 + e_i)$ is conserved exactly by the semi-discrete system. (3) The scheme is Galilean invariant. (4) The artificial viscosity only acts on approaching pairs and only turns kinetic energy into internal energy.

What is *not* proved: the particle sums are not exact quadratures for irregular particles, so SPH is not even zeroth-order consistent in general (a regular lattice with $h = 1.2\Delta p$ gives $\sum_k W\Delta p = 1.0018$), and the convergence to the Euler equations is observed rather than proved here. Leapfrog does not conserve the energy of a dissipative system exactly; the errors in the table are observed.

## Complexity

A force evaluation sorts the positions ($O(n\log n)$), finds neighbours by binary search, and does constant work per pair, so with $k$ neighbours per particle it costs $\Theta(n\log n + nk)$ time and $\Theta(nk)$ space for the pair list. The scheme makes $N + 1$ force evaluations, giving $\Theta((N + 1)(n\log n + nk))$ time and $(N + 1)nk$ pair interactions up to a constant ($nk/2$ pairs, each visited twice). In one dimension $k \approx 4\eta$; in three dimensions a typical $k$ is 30 to 60 and a cell list or tree replaces sorting. The time step is limited by $\Delta t \le C h/(c + |v|)$, so $N = \Theta(T/h)$ when $h$ is refined.

## Properties

- **Lagrangian and meshless:** no advection error for the motion itself, free surfaces and vacuum boundaries come for free, and the resolution follows the mass.
- **Conservative:** mass, momentum and (semi-discretely) energy; angular momentum too in several dimensions with radial pair forces.
- **Galilean invariant** and, with time-reversible integrators and no viscosity, nearly energy-preserving over long times.
- **Low order and noisy:** second order for the continuous kernel estimate, but particle disorder adds a zeroth-order error.
- **Dissipative where needed:** the artificial viscosity spreads shocks over a few smoothing lengths.

## Variants and improvements

- **Variable smoothing lengths with grad-h terms** (Springel and Hernquist; Price) derive the equations from a Lagrangian so that energy and entropy are conserved exactly with $h_i$ tied to $\rho_i$.
- **Viscosity switches** (Morris-Monaghan, Cullen-Dehnen) reduce $\alpha$ away from shocks; **artificial conductivity** smooths the pressure blip at contacts.
- **Wendland kernels** avoid the pairing instability at large neighbour numbers.
- **Godunov SPH** replaces the artificial viscosity by Riemann solvers between particle pairs; **meshless finite mass and volume** methods combine particles with [finite volume](/finite-volume-method/) fluxes.
- **Weakly compressible and incompressible SPH** for liquids, with a stiff equation of state or a pressure Poisson equation.
- **Corrected kernels** (CSPH, MLS) restore first-order consistency at extra cost.

## When to use it

Use SPH for flows with free surfaces, violent splashing, fragmentation, impacts, and self-gravitating astrophysical gas, where mesh-based methods need complex interface tracking or remeshing. For flows on fixed domains where accuracy per degree of freedom matters, such as boundary layers or acoustics, grid methods like [finite volume](/finite-volume-method/) with [WENO](/weno-scheme/) reconstruction are more accurate.

## Pitfalls

- **Time step above the limit.** On the Sod problem, $\Delta t = C\,h_{\min}/1.2$ with $C = 0.3$ or $0.6$ is stable and $C = 1.0$ blows up; the limit involves the sound speed and the particle velocities, and particles escaping at free edges can move several times faster than the bulk flow.
- **Free boundaries are not walls.** A free edge expands into vacuum; the Sod numbers above measure the error only in $[-0.4, 0.4]$. Walls need ghost or boundary particles.
- **Tensile instability.** Under tension the standard equations make particles clump (Swegle, Hicks and Attaway 1995); artificial stress or other kernels are needed for solids.
- **Too few neighbours.** With $\eta$ well below 1 the sums become very noisy; with too many neighbours and the cubic spline, particles pair up.
- **Mixing instabilities.** Pressure discontinuities at contacts suppress Kelvin-Helmholtz rolls in standard SPH unless artificial conductivity or a pressure-based formulation is used.
- **Non-symmetric forms.** Writing the pressure force as $-\frac{1}{\rho_i}\sum_j m_j\frac{P_j}{\rho_j}\partial_iW$ looks consistent but breaks momentum conservation.

## Implementations

## History

Lucy (1977) and Gingold and Monaghan (1977) introduced SPH independently to study nonspherical stars, treating particles as samples of a probability density. Monaghan and Gingold (1983) added the artificial viscosity, and Monaghan's 1992 review fixed the standard symmetric form and the $\alpha$-$\beta$ viscosity. Later work derived SPH from a Lagrangian with variable smoothing lengths, identified the tensile instability (Swegle, Hicks and Attaway 1995), and extended the method to magnetohydrodynamics, solids and free-surface liquids (Monaghan 2005, Price 2012).

## References
