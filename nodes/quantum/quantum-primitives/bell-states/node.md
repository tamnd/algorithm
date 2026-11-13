---
tag: 7ZRWP7
kind: definition
slug: bell-states
name: Bell states
aliases:
- EPR pairs
- maximally entangled two-qubit states
area: quantum/quantum-primitives
level: intro
summary: "The four Bell states (|00> ± |11>)/√2 and (|01> ± |10>)/√2 form an orthonormal basis of two qubits. A Hadamard and a CNOT make them from |00>, |01>, |10>, |11>."
prereqs: [entanglement, hadamard-gate, cnot-gate]
see_also: [quantum-teleportation, superdense-coding, chsh-inequality, pauli-gates, entanglement-entropy, stabilizer-formalism]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.3.6 (Example, Bell states), Section 1.3.7 (quantum teleportation) and Section 2.3 (superdense coding)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.5 (quantum teleportation) and Chapter 17 (entanglement and non-locality)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 6.3.1 (teleportation and dense coding)
  - paper: doi:10.1103/PhysRevLett.68.3259
    title: Samuel L. Braunstein, A. Mann and M. Revzen, Maximal violation of Bell inequalities for mixed states, Physical Review Letters 68, 1992, pages 3259 to 3261
    locator: the four states used as a basis
  - paper: doi:10.1103/PhysRevA.59.3295
    title: N. Lütkenhaus, J. Calsamiglia and K.-A. Suominen, Bell measurements for teleportation, Physical Review A 59, 1999, pages 3295 to 3300
    locator: the limit of Bell measurements with linear optics
---

The *Bell states* are the four two-qubit states $|\Phi^\pm\rangle = (|00\rangle \pm |11\rangle)/\sqrt{2}$ and $|\Psi^\pm\rangle = (|01\rangle \pm |10\rangle)/\sqrt{2}$. They form an orthonormal basis of $\mathbb{C}^2 \otimes \mathbb{C}^2$, the *Bell basis*, and each of them is maximally [entangled](/entanglement/): each qubit alone is in the maximally mixed state $I/2$. A [Hadamard gate](/hadamard-gate/) followed by a [CNOT](/cnot-gate/) maps the four computational basis states to the four Bell states, and the reverse circuit is a *Bell measurement*. They are the shared resource of [quantum teleportation](/quantum-teleportation/) and [superdense coding](/superdense-coding/), and the states of most Bell tests.

## Definition

The pages of this area number the qubits so that the left symbol of $|q_1 q_0\rangle$ is qubit $1$ and the right symbol is qubit $0$, and $|q_1 q_0\rangle$ is the basis vector with index $2q_1 + q_0$ ([quantum state](/quantum-state/)). For bits $x, y \in \{0, 1\}$, write $\bar{y} = 1 - y$. The Bell state with label $xy$ is

$$|\beta_{xy}\rangle = \frac{|0\,y\rangle + (-1)^x\, |1\,\bar{y}\rangle}{\sqrt{2}}.$$

The four states and their usual names are:

| label $xy$ | name | vector |
|---|---|---|
| $00$ | $\lvert\Phi^+\rangle$ | $(\lvert 00\rangle + \lvert 11\rangle)/\sqrt{2}$ |
| $01$ | $\lvert\Psi^+\rangle$ | $(\lvert 01\rangle + \lvert 10\rangle)/\sqrt{2}$ |
| $10$ | $\lvert\Phi^-\rangle$ | $(\lvert 00\rangle - \lvert 11\rangle)/\sqrt{2}$ |
| $11$ | $\lvert\Psi^-\rangle$ | $(\lvert 01\rangle - \lvert 10\rangle)/\sqrt{2}$ |

The bit $y$ says whether the two qubits agree ($\Phi$, $y = 0$) or differ ($\Psi$, $y = 1$) in the computational basis, and $x$ is the sign between the two terms. $|\Psi^-\rangle$ is the *singlet*. The four states are also called *EPR pairs*, after Einstein, Podolsky and Rosen; some authors keep that name for $|\Phi^+\rangle$ or for $|\Psi^-\rangle$ only.

### The circuit

Apply $H$ to qubit $1$, then a CNOT with control qubit $1$ and target qubit $0$:

$$|\beta_{xy}\rangle = \mathrm{CNOT}_{1 \to 0}\, (H \otimes I)\, |x\,y\rangle.$$

Indeed $H$ maps $|x\rangle$ to $(|0\rangle + (-1)^x|1\rangle)/\sqrt{2}$, so the state after it is $(|0\,y\rangle + (-1)^x |1\,y\rangle)/\sqrt{2}$, and the CNOT flips qubit $0$ in the second term only. Both gates are unitary and self-inverse, so the circuit in reverse order, $(H \otimes I)\,\mathrm{CNOT}_{1 \to 0}$, maps $|\beta_{xy}\rangle$ back to $|x\,y\rangle$. A measurement of both qubits after it in the computational basis returns $x$ on qubit $1$ and $y$ on qubit $0$. This is the *Bell measurement*, the projective measurement $\{|\beta_{xy}\rangle\langle\beta_{xy}|\}$.

### Basic properties

**Orthonormal basis.** The circuit is unitary and the vectors $|x\,y\rangle$ are an orthonormal basis, so the four Bell states are an orthonormal basis too: $\langle\beta_{xy}|\beta_{x'y'}\rangle = [xy = x'y']$ and $\sum_{xy} |\beta_{xy}\rangle\langle\beta_{xy}| = I$. In the other direction,

$$|00\rangle = \tfrac{1}{\sqrt{2}}(|\Phi^+\rangle + |\Phi^-\rangle), \quad |11\rangle = \tfrac{1}{\sqrt{2}}(|\Phi^+\rangle - |\Phi^-\rangle), \quad |01\rangle = \tfrac{1}{\sqrt{2}}(|\Psi^+\rangle + |\Psi^-\rangle), \quad |10\rangle = \tfrac{1}{\sqrt{2}}(|\Psi^+\rangle - |\Psi^-\rangle).$$

**Maximal entanglement.** The coefficient matrix of $|\beta_{xy}\rangle$ has the two singular values $1/\sqrt{2}$, so its Schmidt coefficients are $1/\sqrt{2}, 1/\sqrt{2}$ and its [entanglement entropy](/entanglement-entropy/) is $1$ bit, the maximum for two qubits. Each reduced state ([partial trace](/partial-trace/)) is $I/2$. For a pure state the test of the [entanglement](/entanglement/) page gives $c_{00}c_{11} - c_{01}c_{10} = \pm\tfrac{1}{2}$.

**Local Paulis move between them.** With the [Pauli gates](/pauli-gates/) acting on qubit $1$ only,

$$|\beta_{xy}\rangle = (Z^x X^y \otimes I)\,|\Phi^+\rangle.$$

So one party can turn a shared $|\Phi^+\rangle$ into any of the four Bell states without touching the other qubit. This is the encoding step of [superdense coding](/superdense-coding/) and, read backwards, the correction step of [teleportation](/quantum-teleportation/).

**Stabilizers.** The operators $Z \otimes Z$ and $X \otimes X$ commute, and $|\beta_{xy}\rangle$ is their joint eigenvector with the eigenvalues $(-1)^y$ and $(-1)^x$. Since $(X \otimes X)(Z \otimes Z) = (XZ) \otimes (XZ) = -\,Y \otimes Y$, the eigenvalue of $Y \otimes Y$ is $-(-1)^{x+y}$:

| state | $Z \otimes Z$ | $X \otimes X$ | $Y \otimes Y$ |
|---|---|---|---|
| $\lvert\Phi^+\rangle$ | $+1$ | $+1$ | $-1$ |
| $\lvert\Phi^-\rangle$ | $+1$ | $-1$ | $+1$ |
| $\lvert\Psi^+\rangle$ | $-1$ | $+1$ | $+1$ |
| $\lvert\Psi^-\rangle$ | $-1$ | $-1$ | $-1$ |

In the [stabilizer formalism](/stabilizer-formalism/), $|\Phi^+\rangle$ is the state with the stabilizer group generated by $XX$ and $ZZ$.

**The transpose trick.** For every $2 \times 2$ matrix $A$,

$$(A \otimes I)\,|\Phi^+\rangle = (I \otimes A^{\mathsf{T}})\,|\Phi^+\rangle.$$

Both sides equal $\tfrac{1}{\sqrt{2}} \sum_{i,j} A_{ij} |i\,j\rangle$. An operation on one half of $|\Phi^+\rangle$ can thus be moved to the other half.

**The singlet is invariant.** For every $2 \times 2$ unitary $U$, $(U \otimes U)\,|\Psi^-\rangle = \det(U)\,|\Psi^-\rangle$. The vector $|\Psi^-\rangle$ spans the antisymmetric subspace of $\mathbb{C}^2 \otimes \mathbb{C}^2$, which has dimension $1$, and $U \otimes U$ acts on it as multiplication by $\det U$. So the two halves of a singlet give opposite results for every measurement axis, as long as both sides use the same axis.

**Every maximally entangled state is local.** A two-qubit pure state with Schmidt coefficients $1/\sqrt{2}, 1/\sqrt{2}$ has the form $(I \otimes V)\,|\Phi^+\rangle$ for a unitary $V$. The coefficient matrix of $(I \otimes V)|\Phi^+\rangle$ is $V^{\mathsf{T}}/\sqrt{2}$, and a $2 \times 2$ matrix with both singular values $1/\sqrt{2}$ is $1/\sqrt{2}$ times a unitary. So the alias "maximally entangled two-qubit states" names the Bell states up to a local unitary on one qubit.

## Examples and non-examples

**Making $|\Phi^+\rangle$.** From $|00\rangle$, the Hadamard on qubit $1$ gives $(|00\rangle + |10\rangle)/\sqrt{2}$. The CNOT leaves $|00\rangle$ alone and maps $|10\rangle$ to $|11\rangle$, so the result is $(|00\rangle + |11\rangle)/\sqrt{2}$.

**Making the singlet.** From $|11\rangle$, the Hadamard gives $(|01\rangle - |11\rangle)/\sqrt{2}$, and the CNOT maps it to $(|01\rangle - |10\rangle)/\sqrt{2} = |\Psi^-\rangle$.

**Perfect correlation in two bases.** Measure both halves of $|\Phi^+\rangle$ in the computational basis: the results are $00$ or $11$, each with probability $\tfrac{1}{2}$. Measure both in the basis $|\pm\rangle$: since $|\Phi^+\rangle = (|{+}{+}\rangle + |{-}{-}\rangle)/\sqrt{2}$, the results again agree. The eigenvalues $ZZ = XX = +1$ in the table say the same thing. A classical mixture of $|00\rangle$ and $|11\rangle$ agrees in the first basis and gives independent results in the second.

**A product state in the Bell basis.** $|00\rangle$ is not a Bell state; it is the superposition $(|\Phi^+\rangle + |\Phi^-\rangle)/\sqrt{2}$, so a Bell measurement on it returns $\Phi^+$ or $\Phi^-$ with probability $\tfrac{1}{2}$ each.

**Non-example: maximally entangled, but not one of the four.** $\tfrac{1}{2}(|00\rangle + |01\rangle + |10\rangle - |11\rangle) = (I \otimes H)\,|\Phi^+\rangle$ is maximally entangled. It is not a Bell state: its expansion in the Bell basis is $(|\Phi^-\rangle + |\Psi^+\rangle)/\sqrt{2}$.

**Non-example: three qubits.** The GHZ state $(|000\rangle + |111\rangle)/\sqrt{2}$ looks like $|\Phi^+\rangle$ with one more qubit, but it is not a two-qubit state. Two of its qubits alone are in the separable mixed state $\tfrac{1}{2}(|00\rangle\langle 00| + |11\rangle\langle 11|)$, not in $|\Phi^+\rangle$.

**Non-example: a Bell measurement with linear optics.** With photons, beam splitters and photon counters alone, a Bell measurement that never fails is impossible; such a setup can only tell some of the four states apart (Lütkenhaus, Calsamiglia and Suominen 1999). The circuit above needs a two-qubit gate.

### Common errors

- Swapping the roles of the two bits of the label. On this page the label $xy$ gives $x$ as the sign and $y$ as the parity, and the circuit reads $x$ from qubit $1$. Other texts write the label in the other order or put the Hadamard on the other qubit, which permutes the names.
- Writing $(Z^x X^y \otimes I)$ with the Paulis in the other order. $X Z = -Z X$, so $X^y Z^x$ gives the same state up to the global phase $(-1)^{xy}$, which is harmless here but matters inside a larger circuit with control qubits.
- Expecting a Bell state to send a signal. Each qubit alone is $I/2$ whatever the other side does ([no-communication theorem](/no-communication-theorem/)).

### Implementation

The folder `impl/python` builds the four Bell states by the circuit and by the closed form, with exact amplitudes of the form $a + b\sqrt{2}$ with rational $a$ and $b$. The tests check with exact arithmetic that the circuit gives the closed form, that the four states are orthonormal and sum to the identity, that each reduced state is exactly $I/2$, and that $Z^x X^y$ on qubit $1$ maps $|\Phi^+\rangle$ to $|\beta_{xy}\rangle$. In floating point they check the table of Pauli correlations, the Bell measurement circuit, the transpose trick for random complex matrices and the invariance of the singlet under random unitaries $U \otimes U$.

## Related definitions

- [Entanglement](/entanglement/): the property that the Bell states have in the largest amount for two qubits.
- [CNOT gate](/cnot-gate/) and [Hadamard gate](/hadamard-gate/): the two gates of the Bell circuit.
- [Pauli gates](/pauli-gates/): the local operations that permute the Bell basis.
- [Quantum teleportation](/quantum-teleportation/) and [superdense coding](/superdense-coding/): the two protocols that use one shared Bell state.
- [CHSH inequality](/chsh-inequality/) and [Bell's theorem](/bell-theorem/): the Bell states give the largest quantum violation of the CHSH inequality, $2\sqrt{2}$.
- [Entanglement entropy](/entanglement-entropy/): the measure that is $1$ for every Bell state.

### History

Einstein, Podolsky and Rosen (1935) used an entangled state of position and momentum. Bohm (1951) rewrote their argument with two spins in the singlet state, and Bell (1964) used that form for his inequality. The states carry Bell's name. The four of them as a basis, the Bell basis, appear in Braunstein, Mann and Revzen (1992), and the Bell measurement is the key step of teleportation (Bennett and others, 1993).

## References
