---
tag: TMRF7Z
kind: problem
slug: quantum-many-body-simulation
name: Quantum many-body simulation
aliases:
- spin model simulation
area: quantum/quantum-simulation
level: advanced
summary: "Given a local Hamiltonian on a lattice of spins or fermions, such as the Heisenberg, transverse-field Ising or Hubbard model, estimate observables of its dynamics or its low-energy states."
prereqs: [hamiltonian-simulation, pauli-string-decomposition]
see_also: [lieb-robinson-bound, jordan-wigner-transformation, ising-model, eigenvalue-problem, ground-state-energy-estimation, gibbs-state-preparation, quantum-field-theory-simulation, open-quantum-system-simulation]
sources:
  - paper: doi:10.1137/18M1231511
    title: Jeongwan Haah, Matthew B. Hastings, Robin Kothari and Guang Hao Low, Quantum algorithm for simulating real time evolution of lattice Hamiltonians, SIAM Journal on Computing 52(6), 2023 (FOCS 2018, arXiv:1801.03922)
    locator: the main theorem, O(nT polylog(nT/ε)) gates for a lattice Hamiltonian on n sites, and the matching lower bound up to polylogarithmic factors
  - paper: doi:10.1073/pnas.1801723115
    title: Andrew M. Childs, Dmitri Maslov, Yunseong Nam, Neil J. Ross and Yuan Su, Toward the first quantum simulation with quantum speedup, Proceedings of the National Academy of Sciences 115(38), 2018, pages 9456 to 9461
    locator: the Heisenberg chain with a random field as a benchmark, and the gate counts of product formulas, Taylor series and quantum signal processing
  - paper: doi:10.1103/PhysRevLett.94.170201
    title: Matthias Troyer and Uwe-Jens Wiese, Computational complexity and fundamental limitations to fermionic quantum Monte Carlo simulations, Physical Review Letters 94(17), 2005, article 170201
    locator: the NP-hardness of the sign problem of quantum Monte Carlo for a class of spin glass models
  - paper: doi:10.1007/BF01645779
    title: Elliott H. Lieb and Derek W. Robinson, The finite group velocity of quantum spin systems, Communications in Mathematical Physics 28(3), 1972, pages 251 to 257
    locator: the finite velocity of propagation for local spin Hamiltonians
  - paper: doi:10.1007/BF01331938
    title: "Pascual Jordan and Eugene Wigner, Über das Paulische Äquivalenzverbot, Zeitschrift für Physik 47(9), 1928, pages 631 to 651"
    locator: the map between fermions and spins in one dimension
---

*Quantum many-body simulation* is the problem of computing the properties of many interacting quantum particles on a lattice: spins, or fermions such as electrons in a solid. The input is a local Hamiltonian, a sum of terms that each act on a few neighbouring sites. The state space has dimension $d^n$ for $n$ sites with $d$ states each, so a classical computer that stores the state runs out of memory near $n = 50$ for spins. A quantum computer stores the state in $n$ qubits (or $2n$ for spin-$\frac12$ fermions), and [Hamiltonian simulation](/hamiltonian-simulation/) gives the time evolution in a number of gates that grows polynomially. The standard models are the Heisenberg model, the transverse-field [Ising model](/ising-model/) and the Hubbard model. This was the first use of a quantum computer that Feynman proposed, and the lattice models are still the main candidates for a first useful quantum simulation.

## In plain words

A magnet is a grid of tiny spins, and each spin feels only its neighbours. The rule for one pair is simple. But the state of the whole grid is a superposition of all the ways the spins can point, and the number of ways doubles with each spin. Fifty spins already have more than $10^{15}$ ways. A quantum computer uses one qubit per spin and lets the qubits play the grid directly. The questions are the usual ones: how does the grid change after a sudden change, which arrangement has the lowest energy, and what does the grid look like at a temperature.

## Definition

**Input.**

- A lattice: a graph $\Lambda$ with $n$ sites, usually a chain, a square lattice or a cubic lattice, with open or periodic boundaries.
- A local Hilbert space $\mathbb C^d$ at each site: $d = 2$ for spin $\frac12$, or $d = 4$ for a site with a spin-up and a spin-down fermionic mode.
- A local Hamiltonian $H = \sum_X h_X$, where each term $h_X$ acts on a set $X$ of sites of diameter at most $r$ in the graph, and $\|h_X\| \le J$. The number of terms is $O(n)$.
- A task, with an error $\epsilon$:
  - *dynamics*: an initial state $|\psi_0\rangle$ that is easy to prepare (often a product state), a time $t$ and a local observable $O$; output $\langle\psi_0|e^{iHt}Oe^{-iHt}|\psi_0\rangle \pm \epsilon\|O\|$;
  - *energies*: the ground energy $E_0$ or a low part of the spectrum, $\pm\epsilon$;
  - *thermal properties*: $\mathrm{Tr}(Oe^{-\beta H})/\mathrm{Tr}(e^{-\beta H}) \pm \epsilon\|O\|$ at inverse temperature $\beta$.

**Output.** The estimate. On a quantum computer the output is random, and the estimate must be right with probability at least $\frac23$.

**Fermions.** For fermionic models the Hamiltonian is written with the $a_j$ of [second quantization](/second-quantization/), and a [fermion-to-qubit mapping](/fermion-to-qubit-mapping/) turns it into a qubit Hamiltonian. The map preserves the spectrum but not locality: a hop between neighbours in two dimensions can become a Pauli string of length $O(\sqrt n)$ under the [Jordan-Wigner transformation](/jordan-wigner-transformation/).

**The three standard models.** With $\vec S = \frac12(X, Y, Z)$ and the Pauli strings of the [Pauli string decomposition](/pauli-string-decomposition/) page:

| model | Hamiltonian | Pauli form of one bond or site |
|---|---|---|
| Heisenberg | $J\sum_{\langle xy\rangle} \vec S_x\cdot\vec S_y$ | $\frac J4(X_xX_y + Y_xY_y + Z_xZ_y)$, norm $\frac34 J$ |
| transverse-field Ising | $-J\sum_{\langle xy\rangle} Z_xZ_y - g\sum_x X_x$ | $-JZ_xZ_y$ and $-gX_x$ |
| Hubbard | $-t\sum_{\langle xy\rangle, s}(a_{xs}^\dagger a_{ys} + a_{ys}^\dagger a_{xs}) + U\sum_x \hat n_{x\uparrow}\hat n_{x\downarrow}$ | hops of weight 2 or more, $\frac U4(I - Z)(I - Z)$ on site $x$ |

## Variants

- **Dynamics against static properties.** Dynamics after a quench is the task for which a quantum computer has a clear polynomial algorithm. Ground energies and thermal states are hard in general (see Bounds) and need extra structure, such as a trial state with good overlap.
- **Spins, fermions and bosons.** Spin models map to qubits directly. Fermions need a mapping. Bosons have unbounded local spaces and must be cut off at a maximum occupation, which breaks the bound $\|h_X\| \le J$ unless the cutoff is controlled.
- **Dimension and range.** One-dimensional models with a gap are often easy classically (by tensor network methods, which have no page here). Two- and three-dimensional models, and models with long-range interactions $1/r^\alpha$, are where classical methods struggle.
- **Disorder.** A random field $h_x Z_x$ added to the Heisenberg chain models many-body localization. Childs, Maslov, Nam, Ross and Su (2018) used this chain as their benchmark.
- **Time-dependent Hamiltonians and open systems.** A driven lattice has $H(t)$, and a lattice coupled to an environment follows a Lindblad equation; see [open quantum system simulation](/open-quantum-system-simulation/).

## Examples

All values below come from exact diagonalization of the qubit matrices, against closed forms, with $J = 1$.

- **Two spins.** $\vec S_0\cdot\vec S_1$ has eigenvalues $-\frac34$ (the singlet) and $\frac14$ three times (the triplet), since $\vec S_0\cdot\vec S_1 = \frac12(S_{\text{tot}}^2 - \frac32)$.
- **Heisenberg rings.** On a ring of 4 spins, the lowest eigenvalues are $-2$ and then $-1$ three times. On a ring of 6 spins, $E_0 = -\frac12(2 + \sqrt{13}) = -2.8027756$.
- **Transverse-field Ising rings.** The [Jordan-Wigner transformation](/jordan-wigner-transformation/) makes the model quadratic in fermions, and on a ring of $n$ sites
$$E_0 = -\sum_{m=1}^{n}\sqrt{J^2 + g^2 - 2Jg\cos k_m}, \qquad k_m = \frac{\pi(2m - 1)}{n}.$$
  For $n = 4$ and $g = 1$ this is $-5.226252$. For $n = 6$ it is $-6.384695$, $-7.727407$ and $-12.769389$ at $g = 0.5, 1, 2$. Exact diagonalization gives the same values. On two open sites, $E_0 = -\sqrt{J^2 + 4g^2}$.
- **The Hubbard dimer.** Two sites, one spin-up and one spin-down electron, hopping $t$ and interaction $U$. The 4 states of the sector have energies
$$\tfrac12\big(U - \sqrt{U^2 + 16t^2}\big),\quad 0,\quad U,\quad \tfrac12\big(U + \sqrt{U^2 + 16t^2}\big).$$
  The qubit Hamiltonian on 4 qubits, with mode $2x + s$ for site $x$ and spin $s$, gives exactly these. For $U = 8$ and $t = 1$, $E_0 = -0.472136$. At large $U$ it tends to $-4t^2/U = -0.5$: each site holds one electron, and the spins feel a Heisenberg coupling $J = 4t^2/U$.
- **The light cone.** For the Heisenberg chain on 5 sites, $\|[\tau_t(Z_0), Z_d]\|$ at $t = 0.25$ is $0.493$, $0.0324$, $3.1\times 10^{-3}$ and $1.1\times 10^{-4}$ for $d = 1, 2, 3, 4$, below the [Lieb-Robinson bound](/lieb-robinson-bound/).

## Known algorithms

The algorithms are on their own pages. For a lattice with $n$ sites, $O(n)$ terms and time $t$:

| method | cost | note |
|---|---|---|
| exact diagonalization, classical | $O(d^{3n})$ time and $O(d^{2n})$ memory | the [symmetric eigenproblem](/symmetric-eigenproblem/); fine to about 20 spins |
| [Lanczos algorithm](/lanczos-algorithm/), classical | $O(d^n)$ memory per vector | ground and low states to about 40 to 50 spins with symmetries |
| quantum Monte Carlo, classical | polynomial without a sign problem | fails for most fermion and frustrated models (Troyer and Wiese 2005) |
| [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) | $O(n\,t\,(nt/\epsilon)^{1/p})$ gates for order $p$, from [commutator scaling](/commutator-scaling/) | small constants on lattices |
| block decomposition from the [Lieb-Robinson bound](/lieb-robinson-bound/) | $O(nt\,\mathrm{polylog}(nt/\epsilon))$ gates | Haah, Hastings, Kothari and Low; optimal up to the polylog |
| [qubitization](/qubitization/) | $O(\lambda t + \log(1/\epsilon))$ queries, $\lambda = O(n)$ | block encoding of the Pauli list |
| [quantum phase estimation](/quantum-phase-estimation/) on $e^{-iHt}$ | $O(1/\epsilon)$ evolution time per run | energies, given a state with overlap on the eigenstate |

Childs, Maslov, Nam, Ross and Su (2018) compiled several of these for the Heisenberg chain with a random field on up to 100 sites. Product formulas, with error bounds measured on small instances, needed the fewest gates.

## Bounds

- **Dynamics is BQP-hard.** A quantum circuit can be written as the evolution of a time-independent local Hamiltonian, so estimating a local observable after polynomial time is as hard as any problem in [BQP](/bqp/). No efficient classical algorithm is expected.
- **Ground energies are QMA-hard.** Deciding whether $E_0$ of a 2-local Hamiltonian is below $a$ or above $b$, with $b - a \ge 1/\mathrm{poly}(n)$, is [QMA](/qma/)-complete. A quantum computer does not solve this in general either.
- **Locality limits speed.** By the [Lieb-Robinson bound](/lieb-robinson-bound/), information spreads at a finite velocity, so $\Omega(nt)$ gates are needed in the worst case and $O(nt\,\mathrm{polylog})$ suffice.
- **No fast-forwarding.** For general Hamiltonians, the time $t$ cannot be compressed to $o(t)$; see the [no-fast-forwarding theorem](/no-fast-forwarding-theorem/). Free models such as the transverse-field Ising chain are exceptions.
- **The sign problem.** Troyer and Wiese (2005) proved that removing the sign problem of quantum Monte Carlo for a class of models would solve an NP-hard problem.

## Reductions

- **Fermions to spins.** A fermionic lattice model reduces to a qubit model by a [fermion-to-qubit mapping](/fermion-to-qubit-mapping/), at a cost of the Pauli weight of the images.
- **Hubbard to Heisenberg.** At half filling and $U \gg t$, the low-energy part of the Hubbard model is the Heisenberg model with $J = 4t^2/U$, to second order in $t/U$.
- **Ising chain to free fermions.** The transverse-field Ising chain and the XX chain reduce by the [Jordan-Wigner transformation](/jordan-wigner-transformation/) to $n \times n$ matrix problems. These solved models serve as checks.
- **Quantum to classical.** The ground state of the transverse-field Ising model in $D$ dimensions maps to the classical [Ising model](/ising-model/) in $D + 1$ dimensions, whose Monte Carlo is free of signs.
- **Many-body to Hamiltonian simulation.** The dynamics task reduces to [Hamiltonian simulation](/hamiltonian-simulation/) with a Pauli list, plus state preparation and repeated measurement of $O$, with $O(1/\epsilon^2)$ repetitions.

## Applications

- **Magnetism.** Heisenberg and Ising models describe magnetic materials, their phases and their excitations.
- **Strongly correlated electrons.** The two-dimensional Hubbard model is a candidate model for high-temperature superconductivity, and its phase diagram is not settled by classical methods.
- **Thermalization and quenches.** Whether and how an isolated system reaches equilibrium after a sudden change is a dynamics question, natural for a quantum computer.
- **Benchmarks.** Small lattice models with known answers are standard tests for quantum hardware, and the light cone of the [Lieb-Robinson bound](/lieb-robinson-bound/) is a test of the error model.
- **Lattice field theory.** A lattice gauge theory is a many-body model with constraints; see [quantum field theory simulation](/quantum-field-theory-simulation/).

## References
