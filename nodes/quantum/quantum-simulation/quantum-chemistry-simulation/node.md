---
tag: 184NCZ
kind: problem
slug: quantum-chemistry-simulation
name: Quantum chemistry simulation
aliases:
- electronic structure simulation
- molecular simulation
area: quantum/quantum-simulation
level: advanced
summary: "Given the nuclei of a molecule, its electron count and an orbital basis, find the ground-state energy of the electronic Hamiltonian, usually to 1.6 millihartree, or simulate its dynamics."
prereqs: [second-quantization, hamiltonian-simulation, jordan-wigner-transformation]
see_also: [bravyi-kitaev-transformation, fermion-to-qubit-mapping, quantum-phase-estimation, eigenvalue-problem, ground-state-energy-estimation, variational-quantum-eigensolver, quantum-resource-estimation-factoring, molecular-dynamics]
sources:
  - paper: doi:10.1126/science.1113479
    title: Alán Aspuru-Guzik, Anthony D. Dutoi, Peter J. Love and Martin Head-Gordon, Simulated quantum computation of molecular energies, Science 309(5741), 2005, pages 1704 to 1707
    locator: phase estimation for the ground-state energy of molecules in a fixed basis, with the H2O and LiH examples and the qubit counts
  - paper: doi:10.1080/00268976.2011.552441
    title: James D. Whitfield, Jacob Biamonte and Alán Aspuru-Guzik, Simulation of electronic structure Hamiltonians using quantum computers, Molecular Physics 109(5), 2011, pages 735 to 750
    locator: the hydrogen molecule in the STO-3G basis, its integrals (Table 2) and its Jordan-Wigner qubit Hamiltonian
  - paper: doi:10.1073/pnas.1619152114
    title: Markus Reiher, Nathan Wiebe, Krysta M. Svore, Dave Wecker and Matthias Troyer, Elucidating reaction mechanisms on quantum computers, Proceedings of the National Academy of Sciences 114(29), 2017, pages 7555 to 7560
    locator: the resource estimates for the FeMoco active space of 54 electrons in 54 orbitals (T gate counts and logical qubits)
  - paper: doi:10.1103/RevModPhys.92.015003
    title: Sam McArdle, Suguru Endo, Alán Aspuru-Guzik, Simon C. Benjamin and Xiao Yuan, Quantum computational chemistry, Reviews of Modern Physics 92(1), 2020, article 015003
    locator: the electronic structure problem, basis sets, mappings, phase estimation and variational methods
  - book: isbn:9780486691862
    title: Attila Szabo and Neil S. Ostlund, Modern Quantum Chemistry, Dover, 1996
    locator: the chapters on the electronic Hamiltonian, Hartree-Fock and configuration interaction, with the minimal basis H2 model
---

*Quantum chemistry simulation* is the problem of computing the energies and the dynamics of the electrons of a molecule, with the nuclei held fixed. After a basis of $M$ spatial orbitals is chosen, the electronic Hamiltonian is a fermionic operator on $2M$ spin orbitals, written with the $a_p$ of [second quantization](/second-quantization/). The main task is its lowest eigenvalue in the sector with the right number of electrons, which decides bond energies, reaction barriers and the shape of molecules. The space of states grows like $\binom{2M}{N}$ for $N$ electrons, so exact classical methods stop at a few tens of orbitals. A quantum computer stores the state in $2M$ qubits after a [fermion-to-qubit mapping](/fermion-to-qubit-mapping/), and Aspuru-Guzik, Dutoi, Love and Head-Gordon (2005) proposed [quantum phase estimation](/quantum-phase-estimation/) on the resulting qubit Hamiltonian to find the energy.

## In plain words

Chemistry is decided by the electrons. Hold the atoms in place and ask for the lowest energy the electrons can have: that energy, as the atoms move, tells which molecules are stable and how reactions go. Each electron can sit in many orbitals, and electrons repel each other, so the possible arrangements multiply quickly. A quantum computer uses one qubit per orbital and spin, writes down the energy rule as a list of qubit operations, and measures the energy. The difficult part is to get it right to about one part in a thousand of a hartree, the size of chemical energy differences.

## Definition

**Input.**

- Nuclear charges $Z_A$ and positions $R_A$ (the Born-Oppenheimer approximation treats the nuclei as fixed).
- The number $N$ of electrons, and often the total spin.
- A basis of $M$ real spatial orbitals $\phi_p$, made orthonormal, for example the minimal STO-3G basis. Each gives two spin orbitals, indexed here by $2p + s$ with $s = 0$ for spin up and $1$ for spin down.
- The one- and two-electron integrals, computed classically:
$$h_{pq} = \int \phi_p(r)\Big(-\tfrac12\nabla^2 - \sum_A \frac{Z_A}{|r - R_A|}\Big)\phi_q(r)\,dr, \qquad (pq|rs) = \iint \frac{\phi_p(r_1)\phi_q(r_1)\phi_r(r_2)\phi_s(r_2)}{|r_1 - r_2|}\,dr_1 dr_2.$$
- An error $\epsilon$. The usual target is *chemical accuracy*, 1 kcal/mol, about $1.6 \times 10^{-3}$ hartree.

**The Hamiltonian.** With $p, q, r, s$ running over spatial orbitals and $\sigma, \tau$ over spins,
$$H = \sum_{pq,\sigma} h_{pq}\, a_{p\sigma}^\dagger a_{q\sigma} + \frac12\sum_{pqrs,\sigma\tau} (pq|rs)\, a_{p\sigma}^\dagger a_{r\tau}^\dagger a_{s\tau} a_{q\sigma} + E_{\text{nuc}}, \qquad E_{\text{nuc}} = \sum_{A<B}\frac{Z_AZ_B}{|R_A - R_B|}.$$

**Output.** An estimate of the lowest eigenvalue $E_0$ of $H$ in the sector with $N$ electrons (and the chosen spin), within $\epsilon$, with probability at least $\frac23$. Its error relative to the exact energy of the molecule has two parts: the error of the basis, which this problem does not include, and $\epsilon$.

## Variants

- **Excited states.** Other eigenvalues of $H$ in the sector, for spectra and photochemistry.
- **Dynamics.** Evolve an electronic state under $H$ for a time $t$, for example after the removal of an electron.
- **Potential energy surfaces.** $E_0$ as a function of the nuclear positions, for reaction paths and forces. Classical [molecular dynamics](/molecular-dynamics/) moves the nuclei on such a surface.
- **Active spaces.** Treat a few orbitals near the Fermi level exactly and the rest by a mean field. Large calculations, such as the FeMoco estimate below, solve this smaller problem.
- **First quantization.** Keep the electrons as particles with positions on a grid instead of occupation numbers. It uses about $N\log_2(\text{grid size})$ qubits, which pays when the basis is very large.

## Examples

**The hydrogen molecule, minimal basis.** At $R = 1.401$ bohr, the STO-3G basis gives two spatial orbitals, the bonding $g$ and the antibonding $u$, so 4 spin orbitals and 4 qubits. The integrals, from Whitfield, Biamonte and Aspuru-Guzik (2011), in hartree:

| $h_{gg}$ | $h_{uu}$ | $(gg \vert gg)$ | $(uu \vert uu)$ | $(gg \vert uu)$ | $(gu \vert ug)$ | $E_{\text{nuc}} = 1/R$ |
|---|---|---|---|---|---|---|
| $-1.252477$ | $-0.475934$ | $0.674493$ | $0.697397$ | $0.663472$ | $0.181287$ | $0.713776$ |

The [Jordan-Wigner transformation](/jordan-wigner-transformation/) gives 15 Pauli strings on 4 qubits (written with qubit 3 first): the identity with $-0.098834$, $IIIZ = IIZI = 0.171201$, $IZII = ZIII = -0.222797$, $IIZZ = 0.168623$, $ZZII = 0.174349$, $IZIZ = ZIZI = 0.120546$, $IZZI = ZIIZ = 0.165868$, and $XXYY = YYXX = -0.045322$, $XYYX = YXXY = 0.045322$. The [Bravyi-Kitaev transformation](/bravyi-kitaev-transformation/) also gives 15 strings. The exact energies, from the $16 \times 16$ matrix, against closed forms:

| quantity | closed form | electronic | total |
|---|---|---|---|
| Hartree-Fock, $g^2$ | $2h_{gg} + (gg \vert gg)$ | $-1.830461$ | $-1.116685$ |
| ground state, $N = 2$ singlet | lowest root of the $2\times 2$ problem below | $-1.851046$ | $-1.137270$ |
| triplet $gu$ | $h_{gg} + h_{uu} + (gg \vert uu) - (gu \vert ug)$ | $-1.246226$ | |
| $N = 1$ | $h_{gg}$ and $h_{uu}$ | $-1.252477$, $-0.475934$ | |
| $N = 3$ and $N = 4$ | | $-1.160738$, $-0.361291$; $0.206382$ | |

The singlet ground state mixes $g^2$ with $u^2$ only, through $(gu|ug)$. The $2 \times 2$ matrix is $\begin{pmatrix} -1.830461 & 0.181287 \\ 0.181287 & -0.254471\end{pmatrix}$ with $-0.254471 = 2h_{uu} + (uu|uu)$, and its lowest eigenvalue is $-1.851046$. The correlation energy is $-0.020585$ hartree, about 13 kcal/mol, 13 times chemical accuracy.

**FeMoco.** Reiher, Wiebe, Svore, Wecker and Troyer (2017) estimated the cost of the ground energy of an active space of the iron-molybdenum cofactor of nitrogenase, with 54 electrons in 54 spatial orbitals (108 qubits for the state). For one structure, phase estimation on a Trotter evolution needed about $1.1 \times 10^{15}$ T gates and 111 logical qubits in the serial version. These are estimates, not runs, and later work with other algorithms lowered them.

## Known algorithms

The algorithms are on their own pages or have none here.

| method | cost | note |
|---|---|---|
| Hartree-Fock, classical | $O(M^4)$ per iteration | mean field; misses the correlation energy |
| coupled cluster CCSD(T), classical | $O(M^7)$ | accurate near equilibrium, fails for strong correlation |
| full configuration interaction, classical | $\binom{2M}{N}$ dimension | the exact answer in the basis; Lanczos to about 20 orbitals |
| [quantum phase estimation](/quantum-phase-estimation/) on [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) | $O(1/\epsilon)$ evolution time, $O(M^4)$ terms per step | Aspuru-Guzik et al. 2005; Reiher et al. 2017 |
| phase estimation on [qubitization](/qubitization/) | $O(\lambda/\epsilon)$ queries to a [block encoding](/block-encoding/) | $\lambda$ is the 1-norm of the Pauli coefficients |
| variational quantum eigensolver | no guarantee | see the page in see also |

Phase estimation returns $E_0$ only with the probability $|\langle\psi_0|\text{trial}\rangle|^2$, so it needs a trial state, often the Hartree-Fock state, with a large overlap on the ground state.

## Bounds

- **The size of the space.** The $N$-electron sector of $2M$ spin orbitals has dimension $\binom{2M}{N}$. For $N = M = 54$ this is about $10^{31}$, far beyond classical storage.
- **The number of terms.** The Hamiltonian has $O(M^4)$ two-electron integrals, so $O(M^4)$ Pauli strings, each of weight up to $2M$ under Jordan-Wigner and $O(\log M)$ under Bravyi-Kitaev.
- **Phase estimation precision.** Reaching error $\epsilon$ takes total evolution time $\Omega(1/\epsilon)$, the Heisenberg limit of [phase estimation](/phase-estimation-problem/).
- **Hard in general.** The ground energy of a general local Hamiltonian is [QMA](/qma/)-complete, so no algorithm is expected to find $E_0$ for every input. The quantum methods rely on a good trial state.

## Reductions

- **To a qubit Hamiltonian.** The Hamiltonian becomes a Pauli list by a [fermion-to-qubit mapping](/fermion-to-qubit-mapping/): Jordan-Wigner or Bravyi-Kitaev.
- **To phase estimation.** With a block encoding or a product formula for $e^{-iHt}$, the energy is the [phase estimation problem](/phase-estimation-problem/) for the unitary $e^{-iHt}$ and the trial state.
- **To a classical eigenproblem.** In a small basis the problem is the [eigenvalue problem](/eigenvalue-problem/) for the symmetric matrix of $H$ in the $N$-electron sector, as in the $H_2$ example.
- **Symmetries remove qubits.** The number of electrons of each spin is conserved. In the parity encoding of the [fermion-to-qubit mapping](/fermion-to-qubit-mapping/) page such parities sit in single qubits, which can be fixed and removed.

## Applications

- **Catalysis.** The mechanism of nitrogen fixation by FeMoco motivated the estimate of Reiher et al.
- **Reaction energies and barriers.** Energy differences between structures, where errors above chemical accuracy change the predicted rates by large factors.
- **Strongly correlated molecules.** Transition metal complexes and bond breaking, where mean-field and coupled cluster methods fail.
- **Benchmarks of hardware.** Small molecules such as $H_2$ and LiH in minimal bases are standard tests for quantum computers.
- **Cost estimates.** Resource estimates for chemistry are compared with those for factoring in [resource estimation for factoring](/quantum-resource-estimation-factoring/).

## References
