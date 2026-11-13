---
tag: YX77AF
kind: definition
slug: qubit
name: Qubit
aliases:
- quantum bit
area: quantum/quantum-primitives
level: intro
summary: "A qubit is a quantum system whose state space is C^2. A pure state is a unit vector a|0> + b|1>, and two vectors that differ by a global phase are the same state."
prereqs: [dot-product, probability-distribution]
see_also: [quantum-state, bloch-sphere, born-rule, density-matrix, mixed-state, entanglement, no-cloning-theorem, probabilistic-turing-machine]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.2 (quantum bits, the Bloch sphere picture and multiple qubits), Section 2.2.1 (the state space postulate), Section 2.2.7 (global and relative phase) and Chapter 12 (the Holevo bound)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 1, Sections 1.2.1 (superposition), 1.2.2 (measurement) and 1.3 (qubits and quantum memory)
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 3 (qubits and the framework of quantum mechanics)
  - paper: doi:10.1103/PhysRevA.51.2738
    title: Benjamin Schumacher, Quantum coding, Physical Review A 51(4), 1995, pages 2738 to 2747
    locator: the abstract and the acknowledgments (the word qubit, coined in conversation with W. K. Wootters)
---

A *qubit*, or quantum bit, is a quantum system whose state space is the complex vector space $\mathbb{C}^2$. A pure state of a qubit is a unit vector $a|0\rangle + b|1\rangle$ with $|a|^2 + |b|^2 = 1$, and two vectors that differ only by a factor $e^{i\gamma}$ are the same state. A measurement in the basis $|0\rangle, |1\rangle$ gives $0$ with probability $|a|^2$ and $1$ with probability $|b|^2$, by the [Born rule](/born-rule/). The qubit is to quantum information what the bit is to classical information: $n$ qubits together have a $2^n$-dimensional [state space](/quantum-state/).

## Definition

The space $\mathbb{C}^2$ has the inner product $\langle u | v \rangle = \overline{u_0} v_0 + \overline{u_1} v_1$, which is conjugate-linear in the first argument. In Dirac notation a column vector is a *ket* $|v\rangle$, its conjugate transpose is a *bra* $\langle v|$, and $\langle u | v \rangle$ is the product of the two. The *computational basis* is

$$|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \qquad |1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}.$$

**Pure state.** A pure state of a qubit is given by a vector

$$|\psi\rangle = a|0\rangle + b|1\rangle = \begin{pmatrix} a \\ b \end{pmatrix}, \qquad a, b \in \mathbb{C}, \qquad |a|^2 + |b|^2 = 1.$$

The numbers $a$ and $b$ are the *amplitudes* of $|0\rangle$ and $|1\rangle$. When both are nonzero, the state is a [superposition](/quantum-superposition/) of $|0\rangle$ and $|1\rangle$.

**Global phase.** For each real $\gamma$, the vectors $|\psi\rangle$ and $e^{i\gamma}|\psi\rangle$ describe the same physical state. The reason is that no experiment can tell them apart. Each measurement probability has the form $\langle\psi|P|\psi\rangle$ for a projector $P$ ([quantum measurement](/quantum-measurement/)), and $\langle e^{i\gamma}\psi|P|e^{i\gamma}\psi\rangle = \overline{e^{i\gamma}} e^{i\gamma} \langle\psi|P|\psi\rangle = \langle\psi|P|\psi\rangle$. Each evolution is a linear map $U$, and $U(e^{i\gamma}|\psi\rangle) = e^{i\gamma}(U|\psi\rangle)$, so the factor stays a global factor forever. A state of a qubit is thus a *ray* $\{e^{i\gamma}|\psi\rangle\}$, a point of the complex projective line. Two unit vectors $|u\rangle, |v\rangle$ are the same state if and only if $|\langle u|v\rangle| = 1$, by the equality case of the Cauchy-Schwarz inequality.

**Relative phase.** Write $a = |a| e^{i\alpha}$ and $b = |b| e^{i\beta}$ with $a, b \neq 0$. The *relative phase* $\beta - \alpha$ (modulo $2\pi$) does not change under a global phase, and it is observable. After the global phase $e^{-i\alpha}$ is removed, each state is

$$|\psi\rangle = \cos\tfrac{\theta}{2}\,|0\rangle + e^{i\varphi} \sin\tfrac{\theta}{2}\,|1\rangle, \qquad 0 \le \theta \le \pi, \quad 0 \le \varphi < 2\pi,$$

so the pure states of a qubit form a two-parameter family. The pair $(\theta, \varphi)$ is a point of the [Bloch sphere](/bloch-sphere/). The angle $\varphi$ is the relative phase, and it is undefined at the poles $\theta = 0$ and $\theta = \pi$.

**Mixed state.** A qubit can also be in a *mixed state*, a probabilistic mixture of pure states. It is described by a $2 \times 2$ [density matrix](/density-matrix/), and the [mixed-state](/mixed-state/) page covers it. On this page "state" means a pure state.

**Measurement in the computational basis.** A measurement of $|\psi\rangle = a|0\rangle + b|1\rangle$ in the basis $|0\rangle, |1\rangle$ gives the outcome $0$ with probability $|a|^2$ and leaves the qubit in $|0\rangle$, or gives $1$ with probability $|b|^2$ and leaves it in $|1\rangle$. A measurement in another orthonormal basis $|e_0\rangle, |e_1\rangle$ gives $k$ with probability $|\langle e_k|\psi\rangle|^2$.

### A bit, a random bit and a qubit

| | bit | random bit | qubit |
|---|---|---|---|
| state | $0$ or $1$ | $(p_0, p_1)$, real, $p_k \ge 0$ | $(a, b)$, complex |
| constraint | none | $p_0 + p_1 = 1$ | $\lvert a\rvert^2 + \lvert b\rvert^2 = 1$ |
| reversible steps | identity, NOT | permutations | all unitary $2 \times 2$ matrices |
| general steps | four maps of $\{0, 1\}$ | stochastic matrices | quantum channels |
| read out | the value | one sample of $(p_0, p_1)$ | one sample of $(\lvert a\rvert^2, \lvert b\rvert^2)$ |

The random bit is the state of one cell of a [probabilistic Turing machine](/probabilistic-turing-machine/). Its probabilities are nonnegative, so contributions to an outcome can only add. Amplitudes are complex, so two contributions to the same outcome can cancel. This cancellation, [quantum interference](/quantum-interference/), is what a quantum algorithm uses. A qubit has a continuum of pure states, but a measurement returns one bit. By the Holevo bound, $n$ qubits sent to a receiver who shares no entanglement with the sender carry at most $n$ bits of classical information that the receiver can extract. With shared entanglement, [superdense coding](/superdense-coding/) sends two bits with one qubit.

### Physical systems

Any quantum system with two distinguishable levels can serve as a qubit: the spin of an electron or a nucleus (up or down along an axis), the polarization of a photon (horizontal or vertical), two energy levels of an atom or an ion, or two charge or flux states of a superconducting circuit. The definition above does not depend on the system.

## Examples and non-examples

**A worked state.** Let $|\psi\rangle = \tfrac{3}{5}|0\rangle + \tfrac{4i}{5}|1\rangle$. It is a unit vector, since $\tfrac{9}{25} + \tfrac{16}{25} = 1$. In the computational basis the outcome $0$ has probability $\tfrac{9}{25}$ and the outcome $1$ has probability $\tfrac{16}{25}$. In the basis $|\pm\rangle = (|0\rangle \pm |1\rangle)/\sqrt{2}$ the amplitudes are $\langle \pm|\psi\rangle = (\tfrac{3}{5} \pm \tfrac{4i}{5})/\sqrt{2}$, so each outcome has probability $\tfrac{1}{2}$. In the basis $|\pm i\rangle = (|0\rangle \pm i|1\rangle)/\sqrt{2}$ the amplitudes are $(\tfrac{3}{5} \pm \tfrac{4}{5})/\sqrt{2}$, so the outcome $+i$ has probability $\tfrac{49}{50}$ and the outcome $-i$ has probability $\tfrac{1}{50}$. The relative phase is $\pi/2$, the phase of $i$.

**A global phase.** The vectors $-|\psi\rangle$, $i|\psi\rangle$ and $e^{i\pi/3}|\psi\rangle$ are the same state as $|\psi\rangle$. In the same way $e^{i\pi/3}|1\rangle$ is the state $|1\rangle$.

**A relative phase.** The states $|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$ and $|-\rangle = (|0\rangle - |1\rangle)/\sqrt{2}$ have the same probabilities $\tfrac{1}{2}, \tfrac{1}{2}$ in the computational basis. They are still different states, and even orthogonal: $\langle + | - \rangle = 0$. In the basis $|+\rangle, |-\rangle$ the first one gives $+$ with probability $1$ and the second one gives $-$ with probability $1$. A [Hadamard gate](/hadamard-gate/) followed by a measurement in the computational basis does this measurement.

**Non-example: a probability vector.** The vector $(\tfrac{1}{2}, \tfrac{1}{2})$ has entries that sum to $1$, but its length is $1/\sqrt{2}$. It is a probability distribution, not a qubit state. The normalization of a qubit is in the 2-norm, not in the 1-norm.

**Non-example: a coin.** A qubit that is $|0\rangle$ with probability $\tfrac{1}{2}$ and $|1\rangle$ with probability $\tfrac{1}{2}$ is not the state $|+\rangle$. It is the mixed state with density matrix $I/2$. In the basis $|+\rangle, |-\rangle$ the coin gives each outcome with probability $\tfrac{1}{2}$, while $|+\rangle$ gives $+$ with certainty. No unit vector in $\mathbb{C}^2$ describes the coin.

**Non-example: more levels.** A system with three distinguishable levels has the state space $\mathbb{C}^3$. It is a *qutrit*, not a qubit. Two qubits together have the state space $\mathbb{C}^2 \otimes \mathbb{C}^2 \cong \mathbb{C}^4$ ([tensor product](/tensor-product/)), and most of its states are not pairs of qubit states ([entanglement](/entanglement/)).

### Common errors

- Reading an amplitude as a probability. The probability is $|a|^2$, not $a$, and an amplitude can be negative or complex.
- Treating $|\psi\rangle$ and $-|\psi\rangle$ as different states. They are equal. But $|0\rangle + |1\rangle$ and $|0\rangle - |1\rangle$ are different, because the sign is a relative phase.
- Saying that a qubit stores two complex numbers of information. The amplitudes are not readable: one measurement returns one bit and destroys the superposition, and an unknown state cannot be copied ([no-cloning theorem](/no-cloning-theorem/)).
- Saying that a qubit "is 0 and 1 at the same time". A superposition is one definite state, a vector. In another basis the same state can be a basis vector: $|+\rangle$ is a basis vector of the basis $|+\rangle, |-\rangle$.

### Implementation

The file `impl/python/qubit.py` represents a qubit as a list of two Python complex numbers. It builds the states $|0\rangle, |1\rangle, |\pm\rangle, |\pm i\rangle$, computes the probabilities $|\langle e_k|\psi\rangle|^2$ in a given basis, applies a global phase, tests two vectors for equality up to a global phase with $|\langle u|v\rangle| = 1$, and samples measurement outcomes with a `random.Random` object. The tests compute the worked example above exactly, show for 48 pairs of a state and a phase that a global phase changes no probability in the three bases, and compare 20000 samples (seed 2024) of the worked state with $\tfrac{9}{25}$ within $0.02$, a bound that fails with probability below $2 \times 10^{-6}$ by the Hoeffding inequality.

## Related definitions

- [Quantum state](/quantum-state/): the state of $n$ qubits, a unit vector in $(\mathbb{C}^2)^{\otimes n}$, and the qubit order convention used by all pages of this area.
- [Bloch sphere](/bloch-sphere/): the pure states of one qubit as points of the unit sphere, with the angles $\theta$ and $\varphi$ above.
- [Born rule](/born-rule/) and [quantum measurement](/quantum-measurement/): the probabilities $|a|^2, |b|^2$ and the state after a measurement.
- [Quantum superposition](/quantum-superposition/): a state with more than one nonzero amplitude in a given basis.
- [Density matrix](/density-matrix/) and [mixed state](/mixed-state/): the general state of a qubit, including probabilistic mixtures.
- [Tensor product](/tensor-product/): how the state spaces of several qubits combine.
- [Quantum gate](/quantum-gate/), [Pauli gates](/pauli-gates/) and [Hadamard gate](/hadamard-gate/): the unitary maps that act on qubits.

### History

Schumacher introduced the word *qubit* in his 1995 paper on quantum coding, where he credits a conversation with W. K. Wootters. The paper uses it for a two-level quantum system as the unit of quantum information, and shows that the von Neumann entropy of a source counts the qubits needed to encode it.

## References
