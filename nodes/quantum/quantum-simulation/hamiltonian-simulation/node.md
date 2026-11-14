---
tag: 615P36
kind: problem
slug: hamiltonian-simulation
name: Hamiltonian simulation
aliases:
- quantum time evolution
- quantum dynamics simulation
area: quantum/quantum-simulation
level: core
summary: Given a Hamiltonian H in a stated access model, a time t and an error e, build a quantum circuit V with ||V - e^(-iHt)|| <= e in the spectral norm.
prereqs: [unitary-operator, quantum-circuit-model, matrix-norms]
see_also: [trotter-suzuki-product-formulas, qdrift, sparse-hamiltonian-simulation, block-encoding, optimal-hamiltonian-simulation, no-fast-forwarding-theorem, time-dependent-hamiltonian-simulation, phase-estimation-problem]
sources:
  - paper: doi:10.1126/science.273.5278.1073
    title: Seth Lloyd, Universal quantum simulators, Science 273(5278), 1996, pages 1073 to 1078
    locator: the problem for local Hamiltonians and the first algorithm with a proof
  - paper: doi:10.1007/s00220-006-0150-x
    title: Dominic W. Berry, Graeme Ahokas, Richard Cleve and Barry C. Sanders, Efficient quantum algorithms for simulating sparse Hamiltonians, Communications in Mathematical Physics 270(2), 2007, pages 359 to 371 (arXiv:quant-ph/0508139)
    locator: the definition of the problem for sums of terms and for sparse Hamiltonians, and the lower bound linear in t (no fast-forwarding)
  - paper: doi:10.1103/PhysRevLett.118.010501
    title: Guang Hao Low and Isaac L. Chuang, Optimal Hamiltonian simulation by quantum signal processing, Physical Review Letters 118(1), 2017, article 010501 (arXiv:1606.02685)
    locator: the main theorem on sparse Hamiltonian simulation and its comparison with the lower bounds
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 9 (Hamiltonian simulation), the statement of the problem and its access models
  - url: https://www.cs.umd.edu/~amchilds/qa/
    title: Andrew M. Childs, Lecture Notes on Quantum Algorithms, University of Maryland
    locator: Part V (quantum simulation), the chapter Simulating Hamiltonian dynamics
---

Hamiltonian simulation is the problem of building a quantum circuit that approximates the time evolution $e^{-iHt}$ of a quantum system with Hamiltonian $H$. The input is $H$ in a stated access model, a time $t$ and an error $\epsilon$; the output is a circuit $V$ with $\|V - e^{-iHt}\| \le \epsilon$ in the spectral norm. It is the central task of [digital quantum simulation](/digital-quantum-simulation/), the problem that [Feynman's quantum simulation idea](/feynman-quantum-simulation/) asks a quantum computer to solve, and a subroutine of many other quantum algorithms. The cost depends strongly on how $H$ is given. This page defines the problem; the algorithms are on their own pages, listed under Known algorithms.

## In plain words

A physical system changes with time by a fixed rule. The rule is its Hamiltonian, which says how much energy each state has and how the states mix. If you know the rule and the start state, the rule fixes the state at each later time.

The task is to make a quantum computer do the same change to its own qubits. You get a description of the rule, a time and an allowed error. You must give a sequence of gates that changes any start state in almost the same way as the real system would in that time. The questions are how many gates you need, and how this number grows with the time, the size of the system and the required precision.

## Definition

**Input.**

- A Hamiltonian $H$: a Hermitian $2^n \times 2^n$ matrix on $n$ qubits (see [unitary operator](/unitary-operator/) for the link between Hermitian $H$ and unitary $e^{-iHt}$), given in one of the access models below.
- A time $t > 0$.
- An error $\epsilon > 0$.

**Output.** A quantum circuit $V$ on the $n$ data qubits and possibly some ancilla qubits that start and end in $|0\rangle$, such that
$$\| V - e^{-iHt} \| \le \epsilon,$$
where $\|\cdot\|$ is the spectral norm (see [matrix norms](/matrix-norms/)) on the data qubits. Then for every input state $|\psi\rangle$, $\|V|\psi\rangle - e^{-iHt}|\psi\rangle\| \le \epsilon$, and every measurement on the two output states gives probability distributions within total variation distance $\epsilon$. A randomized algorithm outputs a random circuit; its average is a [quantum channel](/quantum-channel/) $\mathcal{E}$, and the error is then measured by the diamond norm distance between $\mathcal{E}$ and the map $\rho \mapsto e^{-iHt}\rho e^{iHt}$.

**Access models.** The problem is defined only when the access to $H$ is fixed:

| model | what is given | main parameters |
|---|---|---|
| local terms | $H = \sum_{j=1}^{L} H_j$, each $H_j$ acts on at most $k = O(1)$ qubits, as a $2^k \times 2^k$ matrix | $L$, $\Lambda = \max_j \|H_j\|$ |
| Pauli list | $H = \sum_{j=1}^{L} c_j P_j$ with real $c_j$ and Pauli strings $P_j$ (see [Pauli string decomposition](/pauli-string-decomposition/)) | $L$, $\lambda = \sum_j |c_j|$ |
| sparse oracle | each row has at most $d$ nonzero entries; one oracle gives the column index of the $\ell$-th nonzero entry of row $j$, another gives the value of an entry | $d$, $\|H\|_{\max} = \max_{jk} |H_{jk}|$, queries |
| block encoding | a unitary $U$ on $n + a$ qubits with $(\langle 0^a| \otimes I)\, U\, (|0^a\rangle \otimes I) = H/\alpha$ | $\alpha \ge \|H\|$, queries to $U$ |

The cost is a count of gates (for the first two models) or of queries to the oracle plus other gates (for the last two), as a function of $n$, $t$, $\epsilon$ and the parameters of the model.

**Two invariances.** Adding a multiple of the identity, $H + cI$, multiplies $e^{-iHt}$ by the global phase $e^{-ict}$, which no measurement sees; so the problem is often stated up to a global phase, or with $H$ shifted to make its norm small. Rescaling gives $e^{-i(sH)(t/s)} = e^{-iHt}$, so the cost can depend on $H$ and $t$ only through the products $\|H\| t$, $\Lambda t$, $\lambda t$ or $\alpha t$. These products are the dimensionless time of the simulation.

## Variants

- **State version.** Given a circuit that prepares $|\psi\rangle$, prepare a state within $\epsilon$ of $e^{-iHt}|\psi\rangle$. Algorithms for the unitary version solve it, and a few methods use the known initial state to do better.
- **Controlled evolution.** Build controlled-$e^{-iHt}$, as needed for [quantum phase estimation](/quantum-phase-estimation/) and the [phase estimation problem](/phase-estimation-problem/). Product formulas give it by controlling each rotation.
- **Sparse Hamiltonians.** The sparse oracle model has its own page, [sparse Hamiltonian simulation](/sparse-hamiltonian-simulation/).
- **Time-dependent Hamiltonians.** $H(t)$ changes in time, and the target is the time-ordered exponential; see [time-dependent Hamiltonian simulation](/time-dependent-hamiltonian-simulation/).
- **Open systems.** The target is a Lindblad evolution, a semigroup of channels; see [open quantum system simulation](/open-quantum-system-simulation/).
- **Imaginary time.** The target is $e^{-H\tau}$ up to normalization, which is not unitary; see [quantum imaginary time evolution](/quantum-imaginary-time-evolution/).
- **Hamiltonian given by copies of a state.** With $H = \rho$ a density matrix given by copies, the task is [density matrix exponentiation](/density-matrix-exponentiation/).
- **Fermions and bosons.** A fermionic Hamiltonian is first mapped to qubits by a [fermion-to-qubit mapping](/fermion-to-qubit-mapping/), for example the [Jordan-Wigner transformation](/jordan-wigner-transformation/).

## Examples

**One term.** For $H = X$ on one qubit, $X^2 = I$ gives
$$e^{-iXt} = \cos t \, I - i \sin t \, X,$$
which is the rotation $R_x(2t)$, a single gate. More generally, for a Pauli string $P$, $e^{-i\theta P} = \cos\theta\, I - i \sin\theta\, P$, and it costs $2(w-1)$ CNOT gates and one rotation for a string of weight $w$ (see [digital quantum simulation](/digital-quantum-simulation/)).

**Commuting terms.** For $H = \sum_{i=1}^{n-1} J_i Z_i Z_{i+1}$ all terms commute, so $e^{-iHt} = \prod_i e^{-iJ_i Z_i Z_{i+1} t}$ exactly, in any order, for every $t$. The terms on pairs $(1,2), (3,4), \ldots$ act on disjoint qubits, and so do the terms on $(2,3), (4,5), \ldots$, so the circuit has depth 2 in two-qubit exponentials, whatever $t$ is. Here the cost does not grow with $t$.

**Two terms that do not commute.** For $H = X + Z$ on one qubit, $H^2 = 2I$, so
$$e^{-i(X+Z)t} = \cos(\sqrt{2}\,t)\, I - i\, \frac{\sin(\sqrt{2}\,t)}{\sqrt{2}}\, (X + Z).$$
This is again one rotation, about the axis $(X + Z)/\sqrt{2}$. But the product $e^{-iZt} e^{-iXt}$ of the two term exponentials is not equal to it, since $[X, Z] = -2iY \ne 0$. For $t = 1$ the spectral norm of the difference is $0.799$. On many qubits no closed form exists, and the [Lie-Trotter product formula](/lie-trotter-product-formula/) is the basic tool to split such sums.

**An Ising chain.** The transverse-field Ising chain $H = \sum_{i=1}^{n-1} Z_i Z_{i+1} + h \sum_{i=1}^{n} X_i$ is a Pauli list with $L = 2n - 1$ terms and $\lambda = (n-1) + hn$. Its $ZZ$ terms and its $X$ terms do not commute. It is the standard test case of the simulation algorithms.

## Known algorithms

The algorithms are on their own pages. Their costs, each in its access model:

| algorithm | access | cost for time $t$ and error $\epsilon$ |
|---|---|---|
| [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/), first and second order | local terms or Pauli list | $O(t^2/\epsilon)$ and $O(t^{3/2}/\epsilon^{1/2})$ steps, constants from commutators |
| [higher-order Trotter-Suzuki](/higher-order-trotter-suzuki/), order $2k$ | local terms or Pauli list | $O(5^{2k} L (L \Lambda t)^{1+1/(2k)} / \epsilon^{1/(2k)})$ exponentials |
| [commutator scaling](/commutator-scaling/) bounds for the same formulas | local terms or Pauli list | $O(\tilde\alpha_{\mathrm{comm}}^{1/p}\, t^{1+1/p}/\epsilon^{1/p})$ steps for order $p$ |
| [qDRIFT](/qdrift/) | Pauli list | $O(\lambda^2 t^2/\epsilon)$ rotations, independent of $L$, diamond norm |
| [multi-product formulas](/multi-product-formulas/) | Pauli list | product formulas combined with an LCU |
| [truncated Taylor series simulation](/truncated-taylor-series-simulation/) | Pauli list or sparse | $O(\lambda t \log(\lambda t/\epsilon)/\log\log(\lambda t/\epsilon))$ queries |
| [qubitization](/qubitization/) and [quantum signal processing](/quantum-signal-processing/) | block encoding | $O(\alpha t + \log(1/\epsilon))$ queries |
| [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/) | sparse oracle | $O(t d \|H\|_{\max} + \log(1/\epsilon)/\log(e + \log(1/\epsilon)/(t d \|H\|_{\max})))$ queries |
| [interaction picture simulation](/interaction-picture-simulation/) | $H = A + B$ with a large, easy $A$ | cost driven by the norm of $B$ |

The first algorithm with a proof is Lloyd's (1996), with product formulas on local terms; it is the [universal quantum simulator](/universal-quantum-simulator/) theorem.

## Bounds

- **No fast forwarding.** In the sparse oracle model, no algorithm simulates every sparse Hamiltonian for time $t$ with $o(t)$ queries. Berry, Ahokas, Cleve and Sanders (2007) proved this by a reduction from the parity problem, whose query complexity is linear. See the [no-fast-forwarding theorem](/no-fast-forwarding-theorem/). Some classes of Hamiltonians are fast-forwardable, for example commuting sums of local terms (see Examples) and quadratic fermion Hamiltonians.
- **Error.** Low and Chuang (2017) gave a query count with the time and the error in separate terms, and showed that it matches the known lower bounds in both $t$ and $\epsilon$.
- **General dense Hamiltonians.** With no structure, the problem needs exponentially many gates. Every unitary is $e^{-iH}$ for a Hermitian $H$ with $\|H\| \le \pi$. The unitaries on $n$ qubits form a manifold of real dimension $4^n$, so an $\epsilon$-net needs at least $(c/\epsilon)^{4^n}$ points for a constant $c$. A circuit of $G$ gates from a fixed finite set of $g$ gates that act on at most 2 of the $n$ qubits is one of at most $(g n^2)^G$ circuits. So $G \ge 4^n \log(c/\epsilon)/\log(g n^2)$ for some unitaries. This is why the access models assume structure: locality, few terms, sparsity, or a block encoding.
- **Bounds in terms of the model.** Product formulas pay a power of $t$ greater than 1. The best methods with ancillas are linear in $t$ and additive in $\log(1/\epsilon)$, which is optimal in the query models.

## Reductions

- **From quantum circuits.** A circuit of $T$ gates can be encoded in a local Hamiltonian whose evolution, for a time polynomial in $T$, reproduces the output of the circuit (the clock construction that goes back to Feynman). So a classical polynomial-time method for Hamiltonian simulation of local Hamiltonians would simulate all of [BQP](/bqp/), and the decision form of the problem is BQP-complete.
- **From a Pauli list to a block encoding.** A Pauli list with $\lambda = \sum_j |c_j|$ gives a block encoding with $\alpha = \lambda$, by a state preparation of the weights and a controlled selection of the terms (see [linear combination of unitaries](/linear-combination-of-unitaries/) and [block encoding](/block-encoding/)). So the block encoding algorithms apply to Pauli lists.
- **From any Hermitian matrix to a Pauli list.** Every $2^n \times 2^n$ Hermitian matrix has a [Pauli string decomposition](/pauli-string-decomposition/), with up to $4^n$ terms.
- **To energy estimation.** Controlled-$e^{-iHt}$ with [quantum phase estimation](/quantum-phase-estimation/) estimates eigenvalues of $H$. This is the route to [ground state energy estimation](/ground-state-energy-estimation/).

## Applications

- [Quantum chemistry simulation](/quantum-chemistry-simulation/): energies and dynamics of molecules, with $H$ from second quantization.
- [Quantum many-body simulation](/quantum-many-body-simulation/): spin models and lattice models of electrons, and their dynamics after a sudden change.
- [Ground state energy estimation](/ground-state-energy-estimation/) and [Gibbs state preparation](/gibbs-state-preparation/), which call $e^{-iHt}$ as a subroutine.
- [Quantum scattering simulation](/quantum-scattering-simulation/) and [quantum field theory simulation](/quantum-field-theory-simulation/).
- Quantum algorithms for linear systems of equations, which use $e^{-iAt}$ for a matrix $A$ inside phase estimation.

## References
