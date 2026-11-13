---
tag: 3K5NPE
kind: problem
slug: quantum-field-theory-simulation
name: Quantum field theory simulation
aliases:
- lattice gauge theory simulation
area: quantum/quantum-simulation
level: research
summary: "Given a quantum field theory, such as phi^4 theory or a lattice gauge theory, put it on a spatial lattice with a truncated field at each site and compute its real-time dynamics to a set error."
prereqs: [quantum-many-body-simulation, hamiltonian-simulation]
see_also: [quantum-scattering-simulation, jordan-wigner-transformation, second-quantization, lieb-robinson-bound, analog-quantum-simulation, bqp, discrete-fourier-transform, monte-carlo-integration]
sources:
  - paper: doi:10.1126/science.1217069
    title: Stephen P. Jordan, Keith S. M. Lee and John Preskill, Quantum algorithms for quantum field theories, Science 336(6085), 2012, pages 1130 to 1133
    locator: the lattice phi^4 theory on qubits, the truncation of the field at each site, and the gate counts polynomial in the energy, the number of particles and 1/ε
  - paper: doi:10.26421/QIC14.11-12-8
    title: Stephen P. Jordan, Keith S. M. Lee and John Preskill, Quantum computation of scattering in scalar quantum field theories, Quantum Information and Computation 14(11-12), 2014, pages 1014 to 1080 (arXiv:1112.4833)
    locator: the full analysis for the scalar theory, with the errors of the lattice spacing, the field truncation and the state preparation
  - paper: doi:10.1103/PhysRevD.11.395
    title: John Kogut and Leonard Susskind, Hamiltonian formulation of Wilson's lattice gauge theories, Physical Review D 11(2), 1975, pages 395 to 408
    locator: the Hamiltonian of a lattice gauge theory with link operators, electric and magnetic terms, Gauss's law and staggered fermions
  - paper: doi:10.1038/nature18318
    title: Esteban A. Martinez, Christine A. Muschik, Philipp Schindler, Daniel Nigg, Alexander Erhard, Markus Heyl, Philipp Hauke, Marcello Dalmonte, Thomas Monz, Peter Zoller and Rainer Blatt, Real-time dynamics of lattice gauge theories with a few-qubit quantum computer, Nature 534(7608), 2016, pages 516 to 519
    locator: the Schwinger model on 4 trapped-ion qubits, with the gauge field removed by Gauss's law, and the measured creation of particle-antiparticle pairs
  - paper: doi:10.1103/PhysRevLett.94.170201
    title: Matthias Troyer and Uwe-Jens Wiese, Computational complexity and fundamental limitations to fermionic quantum Monte Carlo simulations, Physical Review Letters 94(17), 2005, article 170201
    locator: the sign problem of quantum Monte Carlo and its NP-hardness for a class of models
  - paper: doi:10.22331/q-2018-01-08-44
    title: Stephen P. Jordan, Hari Krovi, Keith S. M. Lee and John Preskill, BQP-completeness of scattering in scalar quantum field theory, Quantum 2, 2018, article 44
    locator: the BQP-completeness of the vacuum-to-vacuum amplitude with spacetime-dependent sources in a massive scalar theory in 1 + 1 dimensions
---

*Quantum field theory simulation* is the problem of computing the behaviour of a quantum field theory, the theory of particle physics, on a quantum computer. A field has a degree of freedom at every point of space, so the first step is to put it on a spatial lattice with spacing $a$ and $L$ sites in each direction. The second step is to truncate the infinite range of the field at each site to $2^{n_b}$ values or states, which then fit into $n_b$ qubits. The result is a [quantum many-body simulation](/quantum-many-body-simulation/) with a local Hamiltonian, and the answer of the field theory is its limit as $a \to 0$ and $L \to \infty$. Classical lattice methods sample the theory in imaginary time and handle static properties well, but real-time dynamics, such as scattering, is out of their reach. Jordan, Lee and Preskill (2012) gave the first full quantum algorithm with a proof of polynomial cost, for $\phi^4$ theory.

## In plain words

A field is like a sheet of springs that fills space: at each point there is a value that can wiggle, and neighbouring points pull on each other. Waves on the sheet are the particles. A computer cannot hold infinitely many points, so it keeps a grid of them, and it cannot hold an arbitrary value at a point, so it keeps a finite list of values. With qubits for each grid point, the quantum computer runs the wiggling forward in time. Then the grid is made finer, and the results must settle to an answer that does not depend on the grid.

## Definition

**Input.**

- A field theory, given by a lattice Hamiltonian. The scalar $\phi^4$ theory in $d$ spatial dimensions has the field $\phi_x$ and its conjugate momentum $\pi_x$ at each site $x$, with $[\phi_x, \pi_y] = i\delta_{xy}/a^d$, and
$$H = \sum_x a^d\Big[\frac12\pi_x^2 + \frac12(\nabla_a\phi)_x^2 + \frac12 m_0^2\phi_x^2 + \frac{\lambda_0}{4!}\phi_x^4\Big],$$
  where $\nabla_a$ is the difference over one lattice step divided by $a$.
- The physical parameters: a mass $m$ and a coupling $\lambda$, which fix the bare $m_0$ and $\lambda_0$ at each $a$ by renormalization.
- An initial state, a time $t$, an observable, and an error $\epsilon$ on the result.

**Output.** An estimate of the observable after time $t$, in the continuum theory, within $\epsilon$, with probability at least $\frac23$. The error has four parts, and each must be below a fraction of $\epsilon$:

| error | source | control |
|---|---|---|
| lattice spacing | $a > 0$ | let $a \to 0$ with the bare parameters renormalized |
| volume | $L$ sites | larger than the region the particles reach in time $t$ |
| field truncation | $2^{n_b}$ values per site | $n_b$ grows like $\log(1/\epsilon)$ for low-energy states |
| simulation | $e^{-iHt}$ only approximated | [Hamiltonian simulation](/hamiltonian-simulation/) to error $\epsilon$ |

**Lattice gauge theories.** In the Hamiltonian form of Kogut and Susskind (1975), the gauge field lives on the links of the lattice as a group element $U_\ell$ with an electric field $E_\ell$. The Hamiltonian has an electric term $\frac{g^2}{2}\sum_\ell E_\ell^2$, a magnetic term $-\frac{1}{g^2}\sum_p \mathrm{Re}\,\mathrm{Tr}\,U_p$ over the plaquettes $p$, and a term for the matter. Physical states obey Gauss's law at every site. Fermionic matter uses staggered fermions on the sites, with the [Jordan-Wigner transformation](/jordan-wigner-transformation/) or another mapping to qubits. The link spaces are infinite and must be truncated, for example to $|E_\ell| \le E_{\max}$.

## Variants

- **Scalar, fermionic and gauge theories.** $\phi^4$ theory is the simplest interacting case. Fermion fields need a mapping from [second quantization](/second-quantization/) to qubits. Gauge theories add links and constraints, with the groups U(1) for electrodynamics and SU(3) for quantum chromodynamics.
- **Dimension.** The Schwinger model (electrodynamics in 1 spatial dimension) is the standard first target. Three spatial dimensions are the physical case.
- **Tasks.** Real-time evolution after a quench; [scattering](/quantum-scattering-simulation/) of particles; states at finite density or temperature; the spectrum of the lattice Hamiltonian.
- **Digital and analog.** A gate-based computer runs a product formula for the lattice Hamiltonian. An [analog quantum simulation](/analog-quantum-simulation/) builds a device, such as cold atoms in an optical lattice, whose own Hamiltonian is close to the lattice field theory.

## Examples

- **The free scalar field.** For $\lambda_0 = 0$ in one dimension with periodic boundary, the Hamiltonian is a set of coupled oscillators, and the [discrete Fourier transform](/discrete-fourier-transform/) decouples them. The normal modes have the lattice dispersion
$$\omega_k^2 = m_0^2 + \frac{4}{a^2}\sin^2\frac{ka}{2}, \qquad k = \frac{2\pi j}{La},$$
  which tends to the relativistic $\omega_k^2 = m^2 + k^2$ as $a \to 0$ for fixed $k$. The ground energy is $\frac12\sum_k\omega_k$. These closed forms are the check for any simulation of the free field.
- **Qubits for one site.** A truncated field value $\phi_x$ with $n_b$ qubits takes $2^{n_b}$ values on a grid in $[-\phi_{\max}, \phi_{\max}]$. The operator $\pi_x$ is diagonal after a Fourier transform on the same qubits, so $e^{-i\delta\pi_x^2/2}$ is a [quantum Fourier transform](/quantum-fourier-transform/), a diagonal phase and its inverse. Jordan, Lee and Preskill show that $n_b = O(\log(1/\epsilon))$ qubits per site suffice for the states that matter at low energy.
- **The Schwinger model on 4 qubits.** In 1 spatial dimension, Gauss's law fixes the electric field on each link as the total charge to its left. The gauge field can then be removed, and its energy $\frac{g^2a}{2}\sum_n E_n^2$ becomes a long-range interaction between the charges, a sum of $Z_iZ_j$ terms after the Jordan-Wigner transformation. Martinez et al. (2016) ran this spin model on 4 trapped-ion qubits and measured the creation of particle-antiparticle pairs from the vacuum after a quench.

## Known algorithms

The algorithms are described on the cited papers and on the pages of their parts.

| method | cost | note |
|---|---|---|
| lattice Monte Carlo in imaginary time, classical | polynomial for static properties without a sign problem | fails for real time and for finite density |
| Jordan, Lee and Preskill, $\phi^4$ theory | $(1/\epsilon)^{1.5}$, $(1/\epsilon)^{2.376}$ and $(1/\epsilon)^{3.564}$ gates for $d = 1, 2, 3$ at weak coupling | adiabatic preparation of wave packets, [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/), measurement |
| Jordan, Lee and Preskill, fermionic theories | polynomial | arXiv:1404.7115, the Gross-Neveu model |
| product formulas for the Kogut-Susskind Hamiltonian | polynomial in the lattice size and the link truncation | the cost depends on the gauge group and the truncation |
| analog simulators | not counted in gates | no general error correction |

## Bounds

- **BQP-hard.** Jordan, Krovi, Lee and Preskill (2018) proved that estimating the vacuum-to-vacuum transition amplitude of a massive scalar theory in 1 spatial dimension, driven by classical sources that vary in space and time, is BQP-complete, even at weak coupling. So no efficient classical algorithm is expected; see [quantum scattering simulation](/quantum-scattering-simulation/) and [BQP](/bqp/).
- **The sign problem.** Real-time evolution and finite density give complex weights in the path integral. Troyer and Wiese (2005) proved that the sign problem of quantum Monte Carlo is NP-hard for a class of models, which explains why no general classical fix is expected.
- **Locality.** A lattice field theory with truncated fields has bounded local terms, so the [Lieb-Robinson bound](/lieb-robinson-bound/) gives a light cone. Without the truncation the terms are unbounded and the bound needs more care.
- **Size.** In $d$ dimensions with $L$ sites per direction, the register has $L^d n_b$ qubits, and the number of terms is $O(L^d)$.

## Reductions

- **To many-body simulation.** After the lattice and the truncation, the problem is a [quantum many-body simulation](/quantum-many-body-simulation/) of a local Hamiltonian.
- **Fermion fields to qubits.** Staggered fermions are modes in [second quantization](/second-quantization/), mapped to qubits by the [Jordan-Wigner transformation](/jordan-wigner-transformation/).
- **One-dimensional gauge theories to spin models.** Gauss's law removes the gauge field and leaves long-range spin interactions.
- **To scattering.** Scattering amplitudes are one task of this problem; see [quantum scattering simulation](/quantum-scattering-simulation/).

## Applications

- **Quantum chromodynamics in real time.** The dynamics of quarks and gluons after a collision, which lattice Monte Carlo cannot compute.
- **Matter at high density.** The interiors of neutron stars, where the sign problem blocks classical methods.
- **String breaking and pair creation.** In the Schwinger model and its relatives, as a test of quantum hardware.
- **Tests of the theory.** Scattering in $\phi^4$ theory as a benchmark where perturbation theory gives the answer at weak coupling.

## References
