---
tag: 3RCYBF
kind: model
slug: lennard-jones-potential
name: Lennard-Jones potential
aliases:
- 12-6 potential
- LJ potential
area: scientific-computing/molecular-simulation
level: intro
summary: "The pair potential 4 epsilon ((sigma/r)^12 - (sigma/r)^6), with steep repulsion and van der Waals attraction. It is the standard model of simple liquids such as argon."
model: real-ram
history:
  year: 1924
  people: [John Edward Lennard-Jones, Fritz London, Aneesur Rahman, Loup Verlet]
  note: Jones fitted inverse-power potentials to gas data in 1924, London derived the r^-6 dispersion energy in 1930, and Lennard-Jones used the 12-6 form in 1931. Rahman and Verlet made it the model fluid of molecular dynamics.
prereqs: [interatomic-potential]
see_also: [interatomic-potential, molecular-dynamics, periodic-boundary-conditions, molecular-mechanics-force-field, embedded-atom-method, radial-distribution-function, ewald-summation, verlet-neighbor-list]
sources:
  - paper: doi:10.1098/rspa.1924.0082
    title: J. E. Jones, On the determination of molecular fields. II. From the equation of state of a gas, Proceedings of the Royal Society of London A 106(738), 1924, 463-477
    locator: the fit of an inverse-power repulsion and attraction to the second virial coefficient of argon
  - paper: doi:10.1088/0959-5309/43/5/301
    title: J. E. Lennard-Jones, Cohesion, Proceedings of the Physical Society 43(5), 1931, 461-482
    locator: the pair potential with an r^-12 repulsion and the r^-6 attraction of London
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 1.3 (model systems and interaction potentials, with the argon parameters of Table 1.1), Section 1.6.3 (potential truncation) and Section 2.8 (long-range corrections)
  - paper: doi:10.1063/1.462271
    title: Berend Smit, Phase diagrams of Lennard-Jones fluids, Journal of Chemical Physics 96(11), 1992, 8639-8640
    locator: the critical temperature of the full and of the truncated and shifted potential
  - paper: doi:10.1039/C9CP05445F
    title: Xipeng Wang, Simon Ramirez-Hinestrosa, Jure Dobnikar and Daan Frenkel, The Lennard-Jones potential, when (not) to use it, Physical Chemistry Chemical Physics 22, 2020
    locator: the effect of the cutoff and the shift on the computed properties, and the truncated form they propose
  - paper: doi:10.1103/PhysRev.136.A405
    title: Aneesur Rahman, Correlations in the motion of atoms in liquid argon, Physical Review 136(2A), 1964, A405-A411
    locator: the first molecular dynamics of a Lennard-Jones liquid, for argon
  - paper: doi:10.1103/PhysRev.159.98
    title: Loup Verlet, Computer "experiments" on classical fluids. I. Thermodynamical properties of Lennard-Jones molecules, Physical Review 159(1), 1967, 98-103
    locator: the equation of state of the Lennard-Jones fluid from molecular dynamics
  - paper: "National Institute of Standards and Technology, Lennard-Jones Fluid Properties, NIST Standard Reference Simulation Website"
    locator: the critical point of the full Lennard-Jones fluid from simulation
---

The Lennard-Jones potential is the pair potential $\phi(r) = 4\epsilon\left((\sigma/r)^{12} - (\sigma/r)^6\right)$ between two atoms at distance $r$, where $\epsilon$ is the depth of the well and $\sigma$ is the distance at which $\phi = 0$. The $r^{-6}$ term is the London dispersion attraction, and the $r^{-12}$ term is a steep repulsion chosen for convenience, not derived. It is one model inside the general idea of an [interatomic potential](/interatomic-potential/): the energy is a sum over pairs, which makes it the simplest model in use, the standard test fluid of [molecular dynamics](/molecular-dynamics/), and the nonbonded term of a [molecular mechanics force field](/molecular-mechanics-force-field/). It is a good model for noble gases such as argon and a poor one for metals, where the [embedded atom method](/embedded-atom-method/) adds the many-body terms that pairs miss.

## The machine

**Unknowns.** The positions $r_1, \ldots, r_N$ of $N$ atoms, with $r_{ij} = r_i - r_j$ and $r_{ij} = |r_{ij}|$.

**Functional form.** The potential energy is a sum over pairs:
$$U = \sum_{i<j} \phi(r_{ij}), \qquad \phi(r) = 4\epsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right].$$
The force on atom $i$ is $F_i = -\nabla_i U = \sum_{j \ne i} f(r_{ij})\, r_{ij} / r_{ij}$, with the scalar pair force
$$f(r) = -\phi'(r) = \frac{24\epsilon}{r}\left[2\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right],$$
positive when the pair repels. By Newton's third law, the pair adds $+f\, r_{ij}/r_{ij}$ to $F_i$ and the opposite to $F_j$.

**Parameters.** Two per pair of species, both fitted, not derived:

- $\epsilon$, the well depth, an energy.
- $\sigma$, the distance where $\phi = 0$, a length.

For argon, Allen and Tildesley list $\epsilon / k_B = 119.8$ K and $\sigma = 0.341$ nm in their Table 1.1, from fits to gas-phase data; the values $\sigma = 0.3405$ nm and $\epsilon / k_B = 120$ K are also in use. The exponent 6 is derived: it is the leading term of the dispersion energy between two atoms in quantum mechanics. The exponent 12 is a choice. It is the square of the $r^{-6}$ term, which made it cheap to compute and gives closed forms; the true Pauli repulsion decays more like an exponential.

**Reduced units.** Measure lengths in $\sigma$, energies in $\epsilon$ and masses in the atomic mass $m$. Then time is in $\tau = \sigma\sqrt{m/\epsilon}$, temperature is $T^* = k_B T / \epsilon$, density is $\rho^* = N\sigma^3/V$, and pressure is $P^* = P\sigma^3/\epsilon$. For argon with $\sigma = 0.3405$ nm, $\epsilon / k_B = 119.8$ K and $m = 39.948$ u, $\tau = 2.156 \times 10^{-12}$ s. A typical time step $h = 0.005 \tau$ is then about 11 fs.

**Cutoff.** In a simulation the sum is cut at $r_c$, often $2.5\sigma$, and the page or code must say how:

- **Truncated:** $\phi_t(r) = \phi(r)$ for $r < r_c$ and 0 beyond. The energy jumps by $\phi(r_c)$ at $r_c$.
- **Truncated and shifted:** $\phi_{ts}(r) = \phi(r) - \phi(r_c)$ for $r < r_c$. The energy is continuous; the force is unchanged inside $r_c$ and jumps to 0 at $r_c$.
- **Shifted-force:** $\phi_{sf}(r) = \phi(r) - \phi(r_c) - (r - r_c)\phi'(r_c)$ for $r < r_c$. Energy and force are both continuous, but the force is changed everywhere inside $r_c$.
- **Tail correction:** with the truncated form, add the part of the energy and the pressure beyond $r_c$, under the assumption that the [radial distribution function](/radial-distribution-function/) is 1 there:
$$\frac{U_{tail}}{N} = \frac{8}{3}\pi\rho\epsilon\sigma^3\left[\frac{1}{3}\left(\frac{\sigma}{r_c}\right)^9 - \left(\frac{\sigma}{r_c}\right)^3\right], \qquad P_{tail} = \frac{16}{3}\pi\rho^2\epsilon\sigma^3\left[\frac{2}{3}\left(\frac{\sigma}{r_c}\right)^9 - \left(\frac{\sigma}{r_c}\right)^3\right].$$

The four choices define four different models, with different phase diagrams.

**Standing assumptions.** The atoms are spherical and have no charge, the energy is pairwise additive, and the two parameters do not depend on the density or the temperature. In a periodic box, the cutoff satisfies $r_c \le L/2$ (see [periodic boundary conditions](/periodic-boundary-conditions/)).

```pseudo id=main
LJ-ENERGY-FORCES(r_1..r_N, ε, σ, r_c, variant)
L1  U ← 0; F_i ← 0 for each atom i
L2  for each pair i < j:
L3      r ← |r_ij| (the minimum image in a periodic box); if r ≥ r_c then skip the pair
L4      x ← (σ / r)^6
L5      u ← 4ε (x^2 - x); f ← 24ε (2x^2 - x) / r
L6      shifted: u ← u - φ(r_c).  shifted-force: u ← u - φ(r_c) + (r - r_c) f(r_c); f ← f - f(r_c)
L7      U ← U + u; F_i ← F_i + f r_ij / r; F_j ← F_j - f r_ij / r
L8  return U, F
```

Line L4 computes one power and line L5 reuses it, so a pair costs no square root beyond $r$ itself; codes that test $r^2 < r_c^2$ avoid even that one. The cost is one evaluation per pair within the cutoff, $N(N-1)/2$ pair tests with the direct loop in the real RAM, and $O(N)$ at fixed density with a [linked-cell list](/linked-cell-list/) or a [Verlet neighbor list](/verlet-neighbor-list/).

## What it counts

The model gives a potential energy $U$ and the forces $F_i$ for every configuration, and through them, by simulation, every equilibrium and transport property of the model fluid or solid.

- **Energy and forces** for [molecular dynamics](/molecular-dynamics/) and Monte Carlo.
- **Pressure** by the virial: $P = \rho k_B T + \frac{1}{3V}\sum_{i<j} r_{ij} f(r_{ij})$, plus $P_{tail}$ for the truncated form.
- **Structure,** such as the [radial distribution function](/radial-distribution-function/), and from it the energy and pressure as integrals over $g(r)$.
- **Phase behavior:** the gas, liquid and solid phases, the critical point and the triple point of the model.

By the law of corresponding states, all these results depend on $\epsilon$, $\sigma$ and $m$ only through the reduced units. One simulation at $(T^*, \rho^*)$ serves every substance that the model fits, once the units are converted. This is a property of the model, exact for any two-parameter pair potential of the form $\epsilon\, g(r/\sigma)$; whether real argon and krypton follow it is a question of measurement.

## Relation to other models

- **Interatomic potentials in general.** The [interatomic potential](/interatomic-potential/) page gives the idea and the classes of models. Lennard-Jones is the simplest member of the class of pair potentials.
- **Other pair potentials.** The Mie potential replaces 12 and 6 by general exponents $n$ and $m$; the Buckingham potential uses an exponential repulsion; the Morse potential models a chemical bond. The Weeks-Chandler-Andersen potential keeps only the repulsive part, truncated and shifted at the minimum $2^{1/6}\sigma$. Hard spheres are the limit of a very steep repulsion.
- **Force fields.** A [molecular mechanics force field](/molecular-mechanics-force-field/) uses a Lennard-Jones term for each nonbonded pair of atoms, with mixed parameters such as the Lorentz-Berthelot rules $\sigma_{ij} = (\sigma_i + \sigma_j)/2$ and $\epsilon_{ij} = \sqrt{\epsilon_i \epsilon_j}$, and adds bonds, angles, dihedrals and charges.
- **Many-body models.** No pair potential can describe metals well: it gives the Cauchy relation $C_{12} = C_{44}$ between the elastic constants of a cubic crystal under zero stress, which metals break. The [embedded atom method](/embedded-atom-method/) adds an energy that depends on the local density. The [Behler-Parrinello potential](/behler-parrinello-potential/) fits a general many-body function to quantum data.
- **Charges.** Ions need a Coulomb term added to the Lennard-Jones term, which has no cutoff and needs [Ewald summation](/ewald-summation/).

## Known results in the model

The results below are of three kinds: exact properties of the function, computed values that the test file checks, and simulation results, which are measurements.

**Exact properties of the function.**

- $\phi(\sigma) = 0$, and the pair force there is $f(\sigma) = 24\epsilon/\sigma$.
- The minimum is at $r_m = 2^{1/6}\sigma = 1.122462\sigma$, with $\phi(r_m) = -\epsilon$. Set $\phi'(r) = 0$: $2(\sigma/r)^{12} = (\sigma/r)^6$, so $(\sigma/r)^6 = 1/2$, and then $\phi = 4\epsilon(1/4 - 1/2) = -\epsilon$.
- At the usual cutoff, $\phi(2.5\sigma) = -0.016317\epsilon$, about 1.6 percent of the well depth.

**Computed values (checked by the tests).**

| configuration | value |
|---|---|
| truncated at $r_c = 2.5$, at $r = 2$ | $\phi_t = -0.061523$ |
| truncated and shifted, at $r = 2$ | $\phi_{ts} = -0.045207$ |
| shifted-force, at $r = 2$ | $\phi_{sf} = -0.025707$ |
| 8 atoms on the corners of a cube of side $2^{1/6}\sigma$ (full potential) | $U = -15.1033\epsilon$ |
| tail correction at $\rho^* = 0.8$, $r_c = 2.5$ | $U_{tail}/N = -0.4283\epsilon$, $P^*_{tail} = -0.6844$ |
| static fcc lattice, sums $A_{12} = \sum (r_{nn}/r)^{12}$ and $A_6 = \sum (r_{nn}/r)^6$ over the lattice | $A_{12} = 12.13188$, $A_6 = 14.45392$ |
| fcc lattice at its minimum (full potential) | $r_{nn} = 1.09017\sigma$, $U/N = -8.6102\epsilon$ |

The cube can be checked by hand. It has 12 edges at $2^{1/6}$, each $-1$; 12 face diagonals at $2^{1/6}\sqrt 2$, each $4(1/64 - 1/8) = -0.234375$; and 4 body diagonals at $2^{1/6}\sqrt 3$, each $4(1/432 - 1/54) = -0.072702$. The sum is $-12 - 2.8125 - 0.290809 = -15.1033\epsilon$. For the lattice, the energy per atom at nearest-neighbor distance $a$ is $2\epsilon[A_{12}(\sigma/a)^{12} - A_6(\sigma/a)^6]$; its minimum is at $(a/\sigma)^6 = 2A_{12}/A_6$ with value $-\epsilon A_6^2/(2A_{12})$.

**Simulation results (measurements).**

- **The critical point depends on the cutoff.** For the full potential, simulations give $T_c^* \approx 1.31$ to $1.32$: Smit gives 1.316, and the NIST reference value is 1.3120. For the potential truncated and shifted at $r_c = 2.5\sigma$, Smit gives $T_c^* = 1.085$. The same name thus covers models whose critical temperatures differ by about 20 percent, which is why every result must state the cutoff and its treatment.
- **Properties differ between truncation schemes.** Wang, Ramirez-Hinestrosa, Dobnikar and Frenkel compare published results for different truncations and show that they are not interchangeable; they propose a truncated form that goes to zero smoothly at a short cutoff.
- **Argon.** Rahman's 1964 simulation of 864 atoms of liquid argon, and Verlet's 1967 equation of state, agreed with experiment for the structure and the thermodynamics to within a few percent, which made the Lennard-Jones fluid the model system of the field. This agreement is a measurement for argon, not a property of the model.

## References
