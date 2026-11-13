---
tag: 2Q9G14
kind: problem
slug: ground-state-preparation
name: Ground state preparation
aliases:
- ground state synthesis
- ground state preparation problem
area: quantum/quantum-simulation
level: advanced
summary: Prepare a state close to the lowest-energy eigenstate of a Hamiltonian. With a gap Delta and a guiding state of overlap gamma, about 1/(gamma Delta) uses of H are enough and necessary.
prereqs: [ground-state-energy-estimation, hamiltonian-simulation, fidelity]
see_also: [quantum-imaginary-time-evolution, variational-quantum-eigensolver, variational-method, quantum-phase-estimation, amplitude-amplification, gibbs-state-preparation, quantum-eigenvalue-transformation, quantum-chemistry-simulation]
sources:
  - paper: doi:10.22331/q-2020-12-14-372
    title: "Lin Lin and Yu Tong, Near-optimal ground state preparation, Quantum 4:372, 2020, arXiv:2002.12508"
    locator: the preparation algorithm with a known bound between E_0 and E_1, its cost with logarithmic dependence on the error, and the lower bounds from search and approximate counting
  - paper: doi:10.1103/PhysRevLett.102.130503
    title: "David Poulin and Pawel Wocjan, Preparing ground states of quantum many-body systems on a quantum computer, Physical Review Letters 102:130503, 2009, arXiv:0809.2705"
    locator: ground state preparation by phase estimation and amplitude amplification, with a quadratic speedup over exhaustive search in the dimension
  - url: https://arxiv.org/abs/1712.03193
    title: "Yimin Ge, Jordi Tura and J. Ignacio Cirac, Faster ground state preparation and high-precision ground energy estimation with fewer qubits, arXiv:1712.03193, 2017"
    locator: preparation with a run time that depends on the error exponentially better than phase estimation, and with fewer ancilla qubits
  - url: https://arxiv.org/abs/quant-ph/0001106
    title: "Edward Farhi, Jeffrey Goldstone, Sam Gutmann and Michael Sipser, Quantum computation by adiabatic evolution, arXiv:quant-ph/0001106, 2000"
    locator: the proposal to reach the ground state of a problem Hamiltonian by slow interpolation from a simple Hamiltonian
  - paper: doi:10.1063/1.2798382
    title: "Sabine Jansen, Mary-Beth Ruskai and Ruedi Seiler, Bounds for the adiabatic approximation with applications to quantum computation, Journal of Mathematical Physics 48:102111, 2007, arXiv:quant-ph/0603175"
    locator: the rigorous adiabatic theorem with explicit dependence on the gap, including the terms in the inverse cube of the gap
  - paper: doi:10.1103/RevModPhys.90.015002
    title: "Tameem Albash and Daniel A. Lidar, Adiabatic quantum computation, Reviews of Modern Physics 90:015002, 2018"
    locator: the section on adiabatic theorems, which states the Jansen-Ruskai-Seiler bound and explains how the usual condition on the inverse square of the gap differs from it
  - url: https://arxiv.org/abs/quant-ph/0405098
    title: "Dorit Aharonov, Wim van Dam, Julia Kempe, Zeph Landau, Seth Lloyd and Oded Regev, Adiabatic quantum computation is equivalent to standard quantum computation, SIAM Journal on Computing 37(1):166-194, 2007, arXiv:quant-ph/0405098"
    locator: the polynomial equivalence of the adiabatic model and the circuit model
---

Ground state preparation asks for a quantum state close to a ground state $|\psi_0\rangle$ of a Hamiltonian $H$, the eigenvector of its smallest eigenvalue $E_0$. The output is a state on qubits, not a number, so the problem is the state version of [ground state energy estimation](/ground-state-energy-estimation/), and it is at least as hard: with a prepared ground state, phase estimation gives $E_0$. For local Hamiltonians it is therefore QMA-hard in general. Two promises make it tractable. If the *spectral gap* $\Delta = E_1 - E_0$ is not too small and a *guiding state* with overlap $\gamma$ with the ground state can be prepared, about $1/(\gamma\Delta)$ uses of $H$ and $1/\gamma$ uses of the guiding state are enough and necessary, up to logarithmic factors (Lin and Tong 2020). If $H$ is connected to a simple Hamiltonian by a path along which the gap stays open, slow adiabatic evolution along the path works. The prepared state is the input to measurements of observables, correlation functions and dynamics.

## In plain words

The lowest-energy state of a molecule or a magnet carries the information about its chemistry and its phases. A quantum computer can store such a state, which a classical computer usually cannot, but it has to make it first. The task is to build a state that is almost exactly the lowest-energy state, starting from a simple state. This is easy when you can start from a state that already resembles the target and when the lowest energy is well separated from the next one. The cost grows as the starting state gets worse and as the separation gets smaller. Without such help the task is believed to be hard even for quantum computers.

## Definition

**Input.** A Hamiltonian $H$ on $n$ qubits, as a sum of local terms or through a [block encoding](/block-encoding/) $U_H$ of $H/\alpha$ with $\alpha \ge \|H\|$, an error $\varepsilon \in (0, 1)$ and an error probability $\delta$. In the guided form, also a circuit $U_I$ with $U_I|0^n\rangle = |\phi\rangle$ and $|\langle\phi|\psi_0\rangle| \ge \gamma$.

**Promise.** The ground energy is nondegenerate with gap $E_1 - E_0 \ge \Delta$. Some forms also give a number $\mu$ with $E_0 \le \mu - \Delta/2$ and $\mu + \Delta/2 \le E_1$.

**Output.** A state $\rho$ with [fidelity](/fidelity/) $\langle\psi_0|\rho|\psi_0\rangle \ge 1 - \varepsilon$, together with a flag that reports success; the flag is set with probability at least $1 - \delta$. With a degenerate ground space, replace $|\psi_0\rangle\langle\psi_0|$ by the projection $\Pi_0$ onto it.

**Cost.** In the oracle form, the number of uses of $U_H$ and of $U_I$; with time evolution, the total evolution time. In the local form, the number of gates.

**Energy and state.** A state with energy error $\eta = \mathrm{Tr}(\rho H) - E_0$ has weight at most $\eta/\Delta$ outside the ground space, so a low energy implies a good state only when the gap is known; see the [variational method](/variational-method/).

## Variants

- **Adiabatic form.** Given a path $H(s)$ for $s \in [0, 1]$ with $H(1) = H$, a ground state of $H(0)$ that is easy to prepare, and a lower bound $g$ on the gap of $H(s)$ along the path. The cost is the total time $T$ of the evolution under $H(s)$ with $s = t/T$.
- **Known or unknown energy.** With the number $\mu$ above, a filter that keeps the energies below $\mu$ suffices. Without it, an estimate of $E_0$ to precision of order $\Delta$ is needed first.
- **Symmetry sectors.** Prepare the lowest state with a given particle number, spin or momentum. This is the usual task in chemistry, where the number of electrons is fixed.
- **Low-energy states.** Prepare any state with energy at most $E_0 + \eta$, without a gap promise. The [Gibbs state](/gibbs-state-preparation/) at inverse temperature $\beta$ has energy at most $E_0 + O(n/\beta)$.
- **Classical descriptions.** Output a classical description of the ground state, such as a matrix product state, instead of a quantum state.
- **Excited states.** Prepare the eigenstate of $E_1$, or of the eigenvalue nearest a given energy.

## Examples

- **A Bell state.** $H = -X_1X_0 - Z_1Z_0$ has the ground state $(|00\rangle + |11\rangle)/\sqrt2$ with $E_0 = -2$, and the other three Bell states have energies $0$, $0$ and $2$, so $\Delta = 2$. The product state $|00\rangle$ is a guiding state with $\gamma^2 = 1/2$, and projecting it onto the ground space succeeds with probability $1/2$.
- **A transverse-field Ising chain.** On three qubits, $H = -Z_2Z_1 - Z_1Z_0 - X_2 - X_1 - X_0 - 0.3Z_2$ has $E_0 \approx -3.56025$ and gap about $0.991$. The product state $|{+}{+}{+}\rangle$ has squared overlap about $0.828$ with the ground state and energy $-3$. By the gap bound its weight outside the ground state is at most $0.56/0.991 \approx 0.57$; the true weight is $0.172$. The values come from exact diagonalization.
- **An adiabatic path on one qubit.** $H(s) = -(1 - s)X - sZ$ has eigenvalues $\pm\sqrt{(1 - s)^2 + s^2}$, so the gap $g(s) = 2\sqrt{(1 - s)^2 + s^2}$ is smallest at $s = 1/2$, where it is $\sqrt2$. The path starts at the ground state $|+\rangle$ of $-X$ and ends at the ground state $|0\rangle$ of $-Z$.
- **Search as preparation.** For a marked item $w$ among $N$, $H = -|w\rangle\langle w|$ has ground state $|w\rangle$ and gap $1$. The uniform superposition has $\gamma = 1/\sqrt N$, so preparing $|w\rangle$ is unstructured search.

## Known algorithms

| algorithm | model | cost | notes |
|---|---|---|---|
| projection by [phase estimation](/quantum-phase-estimation/) | $e^{-iH\tau}$, guided | about $1/\gamma^2$ repetitions, each of time of order $1/\Delta$ and polynomial in $1/\varepsilon$ | postselect on an energy below $\mu$ |
| the same with [amplitude amplification](/amplitude-amplification/) (Poulin and Wocjan 2009) | $e^{-iH\tau}$, guided | about $1/\gamma$ repetitions | $\sqrt N$ for a random start in dimension $N$ |
| Ge, Tura and Cirac (2017) | $e^{-iH\tau}$, guided | error dependence exponentially better than phase estimation | fewer ancilla qubits |
| Lin and Tong (2020), known $\mu$ | block encoding of $H/\alpha$ | $O((\alpha/(\gamma\Delta))\log(1/\varepsilon))$ uses of $U_H$, $O(1/\gamma)$ uses of $U_I$ | an eigenvalue filter by [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/) and amplitude amplification |
| Lin and Tong (2020), unknown $\mu$ | block encoding of $H/\alpha$ | $\tilde O((\alpha/(\gamma\Delta))\log(1/(\delta\varepsilon)))$ uses of $U_H$ | estimates $E_0$ first |
| adiabatic state preparation (Farhi et al. 2000) | time-dependent $H(s)$ | total time polynomial in $1/g$, $\|\partial_sH\|$ and $1/\varepsilon$ | needs a path with an open gap |
| [quantum imaginary-time evolution](/quantum-imaginary-time-evolution/) | measured local terms | heuristic; the fitted operators grow with the correlation length | no guiding state needed |
| [VQE](/variational-quantum-eigensolver/) | parameterized circuits | heuristic | upper bounds on the energy only |

A path with an open gap and a guiding state are related: the adiabatic state at an intermediate point of the path can serve as a guiding state for a filter.

## Bounds

| form | model | complexity | source |
|---|---|---|---|
| local $H$, no guiding state | quantum polynomial time | QMA-hard | from [ground state energy estimation](/ground-state-energy-estimation/) |
| guided, oracle | uses of $U_I$ | $\Omega(1/\gamma)$ | search, Lin and Tong (2020) |
| guided, oracle | uses of $U_H$ | $\Omega(1/\Delta)$ in units of $\alpha$, for constant $\gamma$ | approximate counting, Lin and Tong (2020) |
| guided, oracle, known $\mu$ | uses of $U_H$ and $U_I$ | $O((\alpha/(\gamma\Delta))\log(1/\varepsilon))$ and $O(1/\gamma)$ | Lin and Tong (2020) |
| adiabatic | total time | polynomial in $1/g$, $\|\partial_sH\|$, $\|\partial_s^2H\|$ and $1/\varepsilon$ | Jansen, Ruskai and Seiler (2007) |

The upper and lower bounds in the oracle model match up to the factor $\alpha$ and logarithmic factors.

**The adiabatic condition.** The common statement is that the total time must satisfy $T \gg \max_s\|\partial_sH\|/g(s)^2$. This is a heuristic, not a theorem, and it fails for some Hamiltonians. The rigorous bound of Jansen, Ruskai and Seiler, as stated by Albash and Lidar, has an error at most $C/T$ times the sum of the boundary terms $\|\partial_sH\|/g^2$ at $s = 0$ and $s = 1$ and the integral over $s$ of $\|\partial_s^2H\|/g^2 + \|\partial_sH\|^2/g^3$, for a constant $C$. So the inverse cube of the gap enters, not only its inverse square. For the one-qubit path above, $\|\partial_sH\| = \|X - Z\| = \sqrt2$ and $\partial_s^2H = 0$.

**Adiabatic and circuit models.** Adiabatic evolution with local Hamiltonians and an inverse-polynomial gap is polynomially equivalent to the circuit model (Aharonov et al. 2007). So a ground state with such a path is preparable in polynomial time, and conversely the output of any polynomial-size circuit is, up to a clock register, the ground state of a local Hamiltonian with an inverse-polynomial gap.

## Reductions

- **Energy estimation from preparation.** A copy of the ground state and phase estimation of $e^{-iH\tau}$ give $E_0$ to precision $\varepsilon$ in total time $O(1/\varepsilon)$. So preparation is at least as hard as estimation.
- **Preparation from estimation.** An estimate of $E_0$ to precision of order $\Delta$ gives the number $\mu$, after which a filter that keeps energies below $\mu$ prepares the state.
- **Search to preparation.** The example $H = -|w\rangle\langle w|$ with the uniform guiding state shows that preparation needs $\Omega(1/\gamma)$ uses of $U_I$.
- **Circuits to ground states.** The history state of a circuit is the ground state of Kitaev's clock Hamiltonian, so a preparation method for such Hamiltonians can run any circuit.

## Applications

- **Chemistry and materials.** Measuring dipole moments, densities and correlation functions in the ground state of a molecule or a lattice model; see [quantum chemistry simulation](/quantum-chemistry-simulation/).
- **Initial states for dynamics.** Quenches and spectroscopy start from a ground state and evolve it under another Hamiltonian.
- **Energy estimation.** A good prepared state makes [ground state energy estimation](/ground-state-energy-estimation/) cheap, since the overlap is then close to $1$.
- **Optimization.** For a diagonal $H$, the ground state is an optimal bit string.
- **Quantum computation.** By the equivalence of the adiabatic and circuit models, preparing ground states of gapped local Hamiltonians is a universal model of computation.

## References
