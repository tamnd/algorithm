---
tag: TC4WH0
kind: definition
slug: cnot-gate
name: CNOT gate
aliases:
- controlled-NOT
- controlled-X
area: quantum/quantum-primitives
level: intro
summary: "The CNOT gate maps |a, b> to |a, a XOR b>: it flips the target qubit when the control qubit is 1. With H on the control it maps |00> to a Bell state."
prereqs: [tensor-product, quantum-gate, pauli-gates]
see_also: [bell-states, entanglement, toffoli-gate, reversible-computation, universal-gate-set, clifford-group, no-cloning-theorem, quantum-teleportation]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.3.2 (multiple qubit gates), Section 1.3.6 (Bell states), Section 4.3 (controlled operations) and Section 4.5 (universal quantum gates)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.4 (elementary gates, the CNOT gate) and Section 1.5 (quantum teleportation)
  - paper: doi:10.1103/PhysRevA.52.3457
    title: Adriano Barenco, Charles H. Bennett, Richard Cleve, David P. DiVincenzo, Norman Margolus, Peter Shor, Tycho Sleator, John A. Smolin and Harald Weinfurter, Elementary gates for quantum computation, Physical Review A 52, 1995, pages 3457 to 3467
    locator: CNOT and one-qubit gates are universal
---

The *CNOT gate* (controlled-NOT) is the two-qubit gate that applies $X$ to a *target* qubit when a *control* qubit is $1$ and does nothing when it is $0$. On basis states it maps $|a, b\rangle$ to $|a, a \oplus b\rangle$, so it computes the XOR of the two bits into the target, reversibly. On superpositions it acts linearly, and with a Hadamard gate on the control it maps the product state $|00\rangle$ to the entangled Bell state $(|00\rangle + |11\rangle)/\sqrt 2$. CNOT together with all one-qubit gates is universal.

## Definition

The **CNOT gate** with control qubit $c$ and target qubit $t \ne c$ is the [quantum gate](/quantum-gate/) that maps each basis state $|a\rangle_c|b\rangle_t$ to $|a\rangle_c|a \oplus b\rangle_t$ and leaves every other qubit unchanged; $\oplus$ is addition modulo $2$. On two qubits, with the control written first,

$$\text{CNOT}|a, b\rangle = |a, a \oplus b\rangle, \qquad \text{CNOT} = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes X = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}.$$

**Qubit order.** The matrix is in the basis $|00\rangle, |01\rangle, |10\rangle, |11\rangle$, with $|a, b\rangle = |a\rangle \otimes |b\rangle$ at the index $2a + b$. In the convention of [quantum state](/quantum-state/) and [tensor product](/tensor-product/), the left symbol is qubit $1$ and the right symbol is qubit $0$, so this matrix has the control on qubit $1$ and the target on qubit $0$. The CNOT with the control on qubit $0$ and the target on qubit $1$ is a different matrix (see below). In an $n$-qubit register, the CNOT from qubit $c$ to qubit $t$ maps $|x\rangle$ to $|x \oplus x_c 2^t\rangle$, where $x_c$ is bit $c$ of $x$.

**Properties.**

1. CNOT is a permutation matrix, so it is [unitary](/unitary-operator/). It is also Hermitian, so $\text{CNOT}^2 = I$: it is its own inverse.
2. It is the controlled version of the [Pauli gate](/pauli-gates/) $X$, which is why it is also called controlled-$X$. In circuit diagrams the control is a dot and the target is $\oplus$.
3. Conjugation maps Pauli strings to Pauli strings (control letter first):

| $P$ | $XI$ | $IX$ | $ZI$ | $IZ$ | $YI$ | $IY$ |
|---|---|---|---|---|---|---|
| $\text{CNOT}\,P\,\text{CNOT}$ | $XX$ | $IX$ | $ZI$ | $ZZ$ | $YX$ | $ZY$ |

An $X$ on the control spreads to the target, and a $Z$ on the target spreads to the control. So CNOT is in the [Clifford group](/clifford-group/).

**Universality.** Every unitary on $n$ qubits is a product of CNOT gates and one-qubit gates (Barenco et al. 1995). With $H$ and $T$ as the one-qubit gates, these circuits approximate every unitary ([universal gate set](/universal-gate-set/)). One-qubit gates alone cannot entangle qubits, so a universal set needs at least one gate such as CNOT that acts on two qubits.

## Examples and non-examples

**The Bell circuit.** $H$ on the control and then CNOT maps $|a, b\rangle$ to the [Bell state](/bell-states/) $\beta_{ab}$:

$$|00\rangle \xrightarrow{H \otimes I} \tfrac{1}{\sqrt 2}(|00\rangle + |10\rangle) \xrightarrow{\text{CNOT}} \tfrac{1}{\sqrt 2}(|00\rangle + |11\rangle) = \beta_{00},$$

and $\beta_{01} = (|01\rangle + |10\rangle)/\sqrt 2$, $\beta_{10} = (|00\rangle - |11\rangle)/\sqrt 2$, $\beta_{11} = (|01\rangle - |10\rangle)/\sqrt 2$. The four Bell states are orthonormal and none is a product state: a two-qubit state $\sum a_{jk}|jk\rangle$ is a product exactly when $a_{00}a_{11} = a_{01}a_{10}$, and here one side is $\pm\tfrac12$ and the other is $0$. So CNOT creates [entanglement](/entanglement/) from a product input. The reverse circuit, CNOT then $H$ on the control, is the measurement in the Bell basis of [quantum teleportation](/quantum-teleportation/) and [superdense coding](/superdense-coding/).

**Non-example: CNOT does not copy.** $\text{CNOT}(|+\rangle|0\rangle) = \beta_{00}$, not $|+\rangle|+\rangle = \tfrac12(|00\rangle + |01\rangle + |10\rangle + |11\rangle)$. CNOT copies the basis states, $|a\rangle|0\rangle \mapsto |a\rangle|a\rangle$, and so it is the classical fan-out of a reversible circuit. But it is linear, so on $\alpha|0\rangle + \beta|1\rangle$ it gives $\alpha|00\rangle + \beta|11\rangle$, which equals $(\alpha|0\rangle + \beta|1\rangle)^{\otimes 2}$ only when $\alpha\beta = 0$. This is the [no-cloning theorem](/no-cloning-theorem/) for this gate.

**The target can change the control.** In the basis $|\pm\rangle$ the roles change: $\text{CNOT}|+\rangle|+\rangle = |+\rangle|+\rangle$ and $\text{CNOT}|+\rangle|-\rangle = |-\rangle|-\rangle$. The target $|-\rangle$ is the eigenvector of $X$ with eigenvalue $-1$, so the gate multiplies $|1\rangle|-\rangle$ by $-1$, and that phase goes to the control. This is [phase kickback](/phase-kickback/). The same fact in matrix form is

$$(H \otimes H)\,\text{CNOT}\,(H \otimes H) = \text{CNOT with the control on qubit } 0 = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \end{pmatrix}.$$

**SWAP from three CNOTs.** CNOT from qubit $1$ to $0$, then from $0$ to $1$, then from $1$ to $0$ again, exchanges the two qubits. On basis states this is the exchange of two bits with three XORs: $b \leftarrow a \oplus b$, $a \leftarrow a \oplus b$, $b \leftarrow a \oplus b$.

**Classical circuits.** On basis states, CNOT is the reversible XOR gate: it maps $(a, b)$ to $(a, a \oplus b)$ and keeps $a$, so no information is lost. With the [Toffoli gate](/toffoli-gate/), which computes $c \oplus ab$, it simulates any [Boolean circuit](/boolean-circuit/) reversibly ([reversible computation](/reversible-computation/)). A [probabilistic Turing machine](/probabilistic-turing-machine/) that applies XOR to a random bit gets $00$ or $11$ with probability $\tfrac12$ each. That mixture and $\beta_{00}$ give the same results in the computational basis, but not in the basis $|\pm\rangle$: there the two qubits of the mixture give independent results, and the two qubits of $\beta_{00} = (|{+}{+}\rangle + |{-}{-}\rangle)/\sqrt 2$ always give equal results.

### Common errors

- Reading the matrix with the wrong qubit as control. The matrix above has the control on the left symbol, as in N&C, and that is qubit $1$ in the convention of these pages. A CNOT given by qubit numbers as "control $0$, target $1$" has the reversed matrix, because qubit $0$ is the right symbol. Software that puts qubit $0$ on the left gives the opposite result. Check the order before copying a matrix.
- Thinking that the control never changes. In the computational basis the control bit is unchanged, but in other bases the phase kickback above changes the control state.
- Expecting CNOT to clone a superposition. It copies only basis states.

### Implementation

The file `impl/python/cnot_gate.py` has the $4 \times 4$ matrix, the basis permutation $x \mapsto x \oplus x_c 2^t$ for a CNOT in an $n$-qubit register, the gate applied to a state, the Bell circuit and the product test $a_{00}a_{11} = a_{01}a_{10}$. The tests check unitarity, $\text{CNOT}^2 = I$, $\text{CNOT} = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes X$, the truth table, the matrix against the simulator, the permutation for 20 random pairs of qubits in a 5-qubit register with seed 23, the four Bell states and that they are orthonormal and not products, SWAP from three CNOTs, the reversal by $H \otimes H$, the Pauli table above, that $\text{CNOT}(|+\rangle|0\rangle) \ne |+\rangle|+\rangle$, the failure to copy 10 real states with seed 29, and the phase kickback on $|+\rangle|-\rangle$.

## Related definitions

- [Bell states](/bell-states/) and [entanglement](/entanglement/): the states that the Bell circuit makes.
- [Toffoli gate](/toffoli-gate/): the doubly controlled $X$, universal for reversible classical computation.
- [Reversible computation](/reversible-computation/) and [Boolean circuit](/boolean-circuit/): CNOT is the reversible XOR.
- [Universal gate set](/universal-gate-set/): CNOT with one-qubit gates.
- [Clifford group](/clifford-group/) and [stabilizer formalism](/stabilizer-formalism/): CNOT, $H$ and $S$ generate the Clifford group.
- [Kronecker product](/kronecker-product/): the matrix $|0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes X$ is a sum of two Kronecker products.

## References
