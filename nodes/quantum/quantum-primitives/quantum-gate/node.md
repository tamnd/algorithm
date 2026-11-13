---
tag: H2C1T8
kind: definition
slug: quantum-gate
name: Quantum gate
aliases:
- quantum logic gate
area: quantum/quantum-primitives
level: intro
summary: "A quantum gate is a unitary matrix on a few qubits, applied to chosen qubits of a register. Circuits are sequences of gates, and the matrix of A then B is the product BA."
prereqs: [unitary-operator, tensor-product]
see_also: [quantum-circuit-model, universal-gate-set, solovay-kitaev-theorem, boolean-circuit, pauli-gates, hadamard-gate, cnot-gate, toffoli-gate]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.3.1 (single qubit gates), Section 1.3.2 (multiple qubit gates), Section 4.2 (single qubit operations), Section 4.3 (controlled operations) and Section 4.5 (universal quantum gates)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.4 (elementary gates) and Section 2.2 (universality of various sets of elementary gates)
  - paper: doi:10.1098/rspa.1989.0099
    title: David Deutsch, Quantum computational networks, Proceedings of the Royal Society of London A 425, 1989, pages 73 to 90
    locator: the definition of quantum gates and networks
  - paper: doi:10.1103/PhysRevA.52.3457
    title: Adriano Barenco, Charles H. Bennett, Richard Cleve, David P. DiVincenzo, Norman Margolus, Peter Shor, Tycho Sleator, John A. Smolin and Harald Weinfurter, Elementary gates for quantum computation, Physical Review A 52(5), 1995, pages 3457 to 3467
    locator: one-qubit gates and CNOT are universal; constructions of controlled gates
---

A *quantum gate* is a [unitary](/unitary-operator/) operation on a small number of qubits, usually one, two or three. A gate on $k$ qubits is a $2^k \times 2^k$ unitary matrix, and it acts on $k$ chosen qubits of an $n$-qubit register while the other qubits are left alone. A *quantum circuit* is a sequence of gates, and its matrix is the product of the gate matrices in reverse order. Gates are the quantum analogue of the logic gates of a [Boolean circuit](/boolean-circuit/), but they are always reversible, and they act on amplitudes, not on bits.

## Definition

**Gate.** A *$k$-qubit gate* is a unitary matrix $G \in U(2^k)$. Its rows and columns are indexed by $k$-bit strings in the [qubit order](/quantum-state/) of this encyclopedia: the local qubit $i$ of the gate is bit $i$ of the index, so the local qubit $0$ is the rightmost symbol of a ket. Two matrices $G$ and $e^{i\gamma}G$ act in the same way on states and are often treated as the same gate.

**Applying a gate to chosen qubits.** Let $q_0, \dots, q_{k-1}$ be distinct qubits of an $n$-qubit register. *$G$ on the qubits $(q_0, \dots, q_{k-1})$* is the $2^n \times 2^n$ unitary that puts the local qubit $i$ of $G$ on the register qubit $q_i$ and acts as the identity on the other $n - k$ qubits. On a basis state $|x\rangle$ it acts as

$$|x\rangle \mapsto \sum_{y} G_{\,y,\,x|_q}\, |x \text{ with the bits } q_0, \dots, q_{k-1} \text{ replaced by } y\rangle,$$

where $x|_q = \sum_i x_{q_i} 2^i$ is the $k$-bit string that $x$ has on the gate qubits. For one qubit $j$ this is the matrix $I^{\otimes(n-1-j)} \otimes G \otimes I^{\otimes j}$ of the [tensor product](/tensor-product/) page. For adjacent qubits in decreasing order, $G$ on $(j, j+1, \dots, j+k-1)$ is $I^{\otimes(n-j-k)} \otimes G \otimes I^{\otimes j}$. For other qubit lists it is that matrix conjugated by a permutation of the qubits.

**Circuit.** A *circuit* on $n$ qubits is a finite sequence of gates $G_1, \dots, G_m$, each with its list of qubits. It maps the state $|\psi\rangle$ to $U_m \cdots U_2 U_1 |\psi\rangle$, where $U_t$ is the $2^n \times 2^n$ matrix of the gate $G_t$ on its qubits. So the gate that acts first is the rightmost factor of the product. A circuit diagram is read from left to right in time, but the matrix product is written from right to left. The *size* of the circuit is $m$. Its *depth* is the number of layers when each gate goes in the first layer after the last earlier gate that shares a qubit with it.

**Properties.**

- Gates on disjoint sets of qubits commute, and their product is the tensor product of the gates. So the order of gates within one layer does not matter.
- Gates on a common qubit need not commute: $HZ \ne ZH$.
- The inverse of the circuit $G_1, \dots, G_m$ is the circuit $G_m^\dagger, \dots, G_1^\dagger$, the gates in reverse order with each replaced by its adjoint.
- A gate is linear, so it acts on a [superposition](/quantum-superposition/) of inputs term by term. It is not a function on bit strings in general: $H$ maps the basis state $|0\rangle$ to a superposition.

**Universal sets.** A set of gates is *universal* if circuits of its gates can approximate every unitary on any number of qubits to any accuracy. The one-qubit gates together with CNOT are universal exactly: every unitary on $n$ qubits is a circuit of them (Barenco and others, 1995), and the construction of Nielsen and Chuang, Section 4.5, uses $O(n^2 4^n)$ gates. The finite set $\{H, T, \mathrm{CNOT}\}$ is universal approximately, and the [Solovay-Kitaev theorem](/solovay-kitaev-theorem/) says that a one-qubit gate needs only $O(\log^c(1/\varepsilon))$ gates of the set for accuracy $\varepsilon$ ([universal gate set](/universal-gate-set/)). A counting argument shows that most unitaries on $n$ qubits need a number of gates exponential in $n$.

## Examples and non-examples

**One-qubit gates.** The [Pauli gates](/pauli-gates/) $X$, $Y$, $Z$, the [Hadamard gate](/hadamard-gate/) $H$, the [phase and T gates](/phase-and-t-gates/) $S$ and $T$, and the rotations $R_x(\theta)$, $R_y(\theta)$, $R_z(\theta)$. On the [Bloch sphere](/bloch-sphere/) each is a rotation.

**Two-qubit gates.** The [CNOT gate](/cnot-gate/), with the matrix

$$\mathrm{CNOT} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$$

in the basis $|00\rangle, |01\rangle, |10\rangle, |11\rangle$. Its control is the local qubit $1$ (the left symbol) and its target is the local qubit $0$. So "CNOT on $(t, c)$", with the target $t$ in place $0$ and the control $c$ in place $1$, flips qubit $t$ when qubit $c$ is $1$. Other two-qubit gates are the controlled-$Z$ $\mathrm{diag}(1, 1, 1, -1)$, which is symmetric in its two qubits, and SWAP.

**Three-qubit gates.** The [Toffoli gate](/toffoli-gate/) flips its target when both controls are $1$. It is universal for classical reversible computation.

**The matrix order of a circuit.** The circuit "$H$, then $S$" on one qubit has the matrix $SH = \tfrac{1}{\sqrt 2}\begin{pmatrix} 1 & 1 \\ i & -i \end{pmatrix}$. It maps $|0\rangle$ to $(|0\rangle + i|1\rangle)/\sqrt 2$. The other order gives $HS = \tfrac{1}{\sqrt 2}\begin{pmatrix} 1 & i \\ 1 & -i \end{pmatrix}$, which maps $|0\rangle$ to $|+\rangle$.

**Non-example: AND.** The map $(a, b) \mapsto a \wedge b$ has two input bits and one output bit and is not injective, so no unitary carries it out. Its reversible form is the Toffoli gate $|a, b, c\rangle \mapsto |a, b, c \oplus (a \wedge b)\rangle$ with $c = 0$ ([reversible computation](/reversible-computation/)).

**Non-example: measurement and reset.** A [measurement](/quantum-measurement/) is not unitary, and a reset of a qubit to $|0\rangle$ maps all states of the qubit to one state. Circuit diagrams draw them as boxes, but they are not gates in the sense of this page.

**Non-example: copying.** No gate maps $|\psi\rangle|0\rangle$ to $|\psi\rangle|\psi\rangle$ for every $|\psi\rangle$ ([no-cloning theorem](/no-cloning-theorem/)). CNOT copies the basis states $|0\rangle$ and $|1\rangle$, but it maps $|+\rangle|0\rangle$ to a Bell state.

### Common errors

- Multiplying the gate matrices in the order of the diagram. The first gate is the rightmost factor.
- Mixing qubit orders between a gate and a register. With the convention here, $G$ on $(q_0, q_1)$ puts the right symbol of the gate's kets on $q_0$. A library that numbers qubits from the left uses the reverse.
- Building the $2^n \times 2^n$ matrix to apply a gate. A simulator applies a $k$-qubit gate to each of the $2^{n-k}$ groups of $2^k$ amplitudes that agree outside the gate qubits, in $O(4^k 2^{n-k})$ arithmetic operations.

### Implementation

The file `impl/python/quantum_gate.py` applies a $2^k \times 2^k$ unitary to a list of qubits as defined above, runs a circuit given as a list of gates with their qubit lists, builds the circuit matrix column by column, and computes the inverse circuit and the depth. It rejects matrices that are not unitary. The tests compare one-qubit gates with the simulator routine on 1 to 4 qubits, compare CNOT and Toffoli on permuted qubit lists with the simulator's controlled gate, check that "$H$, then $S$" has the matrix $SH$, that gates on disjoint qubits commute, and that a circuit followed by its inverse is the identity.

## Related definitions

- [Quantum circuit model](/quantum-circuit-model/): circuits with inputs, gates and measurements as a model of computation.
- [Universal gate set](/universal-gate-set/) and [Solovay-Kitaev theorem](/solovay-kitaev-theorem/): which finite gate sets suffice and at what cost.
- [Boolean circuit](/boolean-circuit/): the classical model with AND, OR and NOT, where gates need not be reversible.
- [Unitary operator](/unitary-operator/): the matrices that gates are.
- [Clifford group](/clifford-group/): the gates generated by $H$, $S$ and CNOT, which map Pauli products to Pauli products and can be simulated efficiently.

### History

Deutsch defined quantum computational networks of gates in 1989 and gave a universal three-qubit gate. Barenco and eight coauthors showed in 1995 that one-qubit gates and CNOT are universal, and gave the standard constructions of multiply controlled gates from them.

## References
