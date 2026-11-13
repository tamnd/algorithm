---
tag: T3KB06
kind: model
slug: digital-quantum-simulation
name: Digital quantum simulation
aliases:
- gate-based quantum simulation
area: quantum/quantum-simulation
level: intro
summary: Simulate a quantum system on a gate-based quantum computer by compiling e^(-iHt) into a circuit. The cost is gates, depth, qubits and queries for a stated error.
prereqs: [feynman-quantum-simulation, quantum-circuit-model]
see_also: [analog-quantum-simulation, hamiltonian-simulation, trotter-suzuki-product-formulas, pauli-string-decomposition, cnot-gate, solovay-kitaev-theorem, jordan-wigner-transformation, quantum-threshold-theorem]
sources:
  - paper: doi:10.1126/science.273.5278.1073
    title: Seth Lloyd, Universal quantum simulators, Science 273(5278), 1996, pages 1073 to 1078
    locator: the simulation of local Hamiltonians by sequences of local gates and its gate count
  - paper: doi:10.1126/science.1208001
    title: B. P. Lanyon and others, Universal digital quantum simulation with trapped ions, Science 334(6052), 2011, pages 57 to 61 (arXiv:1109.1512)
    locator: the digital simulation of spin models with up to 6 qubits and up to 100 gates
  - paper: doi:10.1103/RevModPhys.86.153
    title: I. M. Georgescu, S. Ashhab and F. Nori, Quantum simulation, Reviews of Modern Physics 86(1), 2014, pages 153 to 185
    locator: the section on digital quantum simulation and its comparison with analog simulation
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 4.7 (simulation of quantum systems)
---

Digital quantum simulation is the model in which a quantum computer simulates a quantum system by running a circuit of discrete gates. The time evolution $e^{-iHt}$ of the target is compiled into a sequence of one- and two-qubit gates of the [quantum circuit model](/quantum-circuit-model/), with a stated error $\epsilon$. Lloyd (1996) showed that every local Hamiltonian can be simulated in this way with a polynomial number of gates (the [universal quantum simulator](/universal-quantum-simulator/) theorem). The model differs from [analog quantum simulation](/analog-quantum-simulation/), where the device evolves under its own Hamiltonian: a digital simulator is universal and can use [quantum error correction](/quantum-error-correction/), but it pays for the approximation of $e^{-iHt}$ with gates. The task that the circuit solves is [Hamiltonian simulation](/hamiltonian-simulation/).

## The machine

A digital simulator is a quantum computer in the circuit model. A simulation has five steps.

1. **Encode the target in qubits.** Spin-1/2 systems map to qubits one to one. Fermions need a [fermion-to-qubit mapping](/fermion-to-qubit-mapping/), for example the [Jordan-Wigner transformation](/jordan-wigner-transformation/). Bosons and fields need a cutoff on the number of particles per mode.
2. **Write the Hamiltonian in a form the circuit can use.** The usual form is a [Pauli string decomposition](/pauli-string-decomposition/) $H = \sum_{j=1}^{L} c_j P_j$, with real $c_j$ and $n$-qubit Pauli strings $P_j$. Other forms are a sparse matrix given by an oracle, or a block encoding.
3. **Choose a simulation algorithm.** It gives a circuit $V$ of simple unitaries with $\|V - e^{-iHt}\| \le \epsilon$. The [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/), [higher-order Trotter-Suzuki formulas](/higher-order-trotter-suzuki/) and [qDRIFT](/qdrift/) use exponentials of single terms. [Linear combination of unitaries](/linear-combination-of-unitaries/), [truncated Taylor series simulation](/truncated-taylor-series-simulation/) and [qubitization](/qubitization/) use ancilla qubits and queries to a [block encoding](/block-encoding/).
4. **Compile each simple unitary into gates.** The exponential of one Pauli string is the basic block; see below.
5. **Prepare, run, measure.** Prepare an initial state, run the circuit, measure. Repeat to estimate expected values, or feed the circuit into [quantum phase estimation](/quantum-phase-estimation/) to estimate energies.

**The exponential of a Pauli string.** Let $P$ act as $X$, $Y$ or $Z$ on $w$ qubits and as $I$ on the rest. Then $e^{-i\theta P}$ is:

- a basis change on each of the $w$ qubits: $H$ (the Hadamard gate) where $P$ has $X$, since $HXH = Z$, and $HS^\dagger$ where $P$ has $Y$, since $(HS^\dagger) Y (HS^\dagger)^\dagger = HXH = Z$;
- a ladder of $w - 1$ [CNOT gates](/cnot-gate/) that writes the parity of the $w$ qubits into the last one;
- the rotation $R_z(2\theta) = e^{-i\theta Z}$ on that qubit;
- the same ladder in reverse order, and the inverse basis changes.

This uses $2(w-1)$ CNOT gates and one rotation. The ladder works because $Z \otimes \cdots \otimes Z$ has the eigenvalue $(-1)^{x_1 \oplus \cdots \oplus x_w}$ on the basis state $|x_1 \ldots x_w\rangle$, so the phase depends only on the parity.

**Hand example.** For $P = Z \otimes Z$, let the first qubit control a CNOT on the second. On $|a, b\rangle$ the CNOT gives $|a, a \oplus b\rangle$. Then $R_z(2\theta) = \mathrm{diag}(e^{-i\theta}, e^{i\theta})$ on the second qubit gives the phase $e^{-i\theta(-1)^{a \oplus b}}$, and the second CNOT restores $|a, b\rangle$. Since $(-1)^{a \oplus b}$ is the eigenvalue of $Z \otimes Z$ on $|a, b\rangle$, the circuit is exactly $e^{-i\theta Z \otimes Z}$. A product of the three $4 \times 4$ matrices for $\theta = 0.37$ agrees with $e^{-0.37 i Z\otimes Z}$ to the last floating point digit.

## What it counts

The cost of a digital simulation is a list of numbers, each for a stated error $\epsilon$ in the spectral norm (or, for random methods such as [qDRIFT](/qdrift/), in the diamond norm of the averaged channel):

- **Gates.** The number of one- and two-qubit gates from a stated gate set. For exact rotations the count is in CNOT gates and rotations. For a finite gate set such as Clifford plus T, each rotation is approximated by the [Solovay-Kitaev theorem](/solovay-kitaev-theorem/) or by a newer synthesis method, which multiplies the count by a factor polylog$(1/\epsilon)$. In fault-tolerant estimates the T count dominates.
- **Depth.** The number of layers of gates that act on disjoint qubits. Exponentials of terms on disjoint qubits run in parallel.
- **Qubits.** The $n$ data qubits, and the ancilla qubits apart. Product formulas need no ancillas. Methods with a block encoding need a few ancillas, which are returned clean.
- **Queries.** In the sparse oracle and block encoding access models the cost is the number of calls to the oracle, and the gates between calls are counted apart.

**The errors add.** For unitaries, $\|U_1 U_2 - V_1 V_2\| \le \|U_1 - V_1\| + \|U_2 - V_2\|$. So the total error is at most the sum of the algorithm error (for example the Trotter error), the synthesis error of all rotations and the error of the hardware. A common budget gives half of $\epsilon$ to the algorithm and splits the other half evenly over the $G$ rotations, so each rotation gets $\epsilon/(2G)$.

**A count from the bounds.** For the transverse-field Ising chain $H = \sum_{i=1}^{n-1} Z_i Z_{i+1} + \sum_{i=1}^{n} X_i$ with $n = 10$, $t = 1$ and $\epsilon = 10^{-3}$, the first order commutator bound of the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) is $(t^2/2r) \cdot 4(n-1)$. It asks for $r = 18\,000$ steps of 19 exponentials each: $342\,000$ rotations and $2 \cdot 9 \cdot 18\,000 = 324\,000$ CNOT gates. The second order formula and the [commutator scaling](/commutator-scaling/) bounds lower this count by orders of magnitude.

## Relation to other models

- **The circuit model.** A digital simulator is a [quantum circuit](/quantum-circuit-model/). Every polynomial-size circuit can be written as the evolution under a local Hamiltonian, and every local Hamiltonian evolution has a polynomial-size circuit. So simulation of local Hamiltonians is complete for [BQP](/bqp/) in its decision form.
- **Analog simulation.** An [analog simulator](/analog-quantum-simulation/) uses only its native Hamiltonians and has no Trotter error, but its control errors add up with time. A digital simulator can reach any target and, with [quantum error correction](/quantum-error-correction/) below the threshold of the [quantum threshold theorem](/quantum-threshold-theorem/), it can run for a time that grows with the code size, at a polylogarithmic overhead.
- **The query model.** When $H$ is given by an oracle for its nonzero entries, the cost is counted in the [quantum query model](/quantum-query-model/), as for other oracle algorithms.

## Known results in the model

- **Lloyd 1996.** A Hamiltonian $H = \sum_{j=1}^{L} H_j$ whose terms each act on $O(1)$ qubits can be simulated for time $t$ with error $\epsilon$ by $\mathrm{poly}(n, t, 1/\epsilon)$ gates (the [universal quantum simulator](/universal-quantum-simulator/) theorem).
- **Product formulas.** The first order formula needs $r = O(t^2/\epsilon)$ steps, the second order formula $O(t^{3/2}/\epsilon^{1/2})$, and a formula of order $2k$ needs $O(t^{1+1/(2k)}/\epsilon^{1/(2k)})$, with constants from nested commutators (see [commutator scaling](/commutator-scaling/)).
- **Methods beyond product formulas.** [Optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/) by [quantum signal processing](/quantum-signal-processing/) and [qubitization](/qubitization/) reaches a query cost additive in $t$ and $\log(1/\epsilon)$. The [no-fast-forwarding theorem](/no-fast-forwarding-theorem/) shows that a cost linear in $t$ is necessary in general.
- **Experiments.** Lanyon and others (2011) ran digital simulations of spin models on trapped ions, with up to 6 qubits and up to 100 gates, and saw the Trotter error and the gate errors that the theory predicts.

## References
