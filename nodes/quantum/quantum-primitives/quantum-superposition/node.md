---
tag: F1S9BZ
kind: concept
slug: quantum-superposition
name: Quantum superposition
area: quantum/quantum-primitives
level: intro
summary: "A quantum superposition is a state with two or more nonzero amplitudes in a chosen basis. Amplitudes are complex and can cancel; probabilities of classical randomness cannot."
prereqs: [quantum-state]
see_also: [quantum-interference, quantum-parallelism, hadamard-gate, born-rule, mixed-state, entanglement, deutsch-jozsa-algorithm, probabilistic-turing-machine]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.2 (quantum bits) and Section 1.4.2 (quantum parallelism)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.2.1 (superposition) and Section 1.2.2 (measurement)
  - book: isbn:9780198520115
    title: P. A. M. Dirac, The Principles of Quantum Mechanics, 4th edition, Oxford University Press, 1958
    locator: Chapter I, The principle of superposition
---

A *quantum superposition* is a quantum state that is a sum of two or more basis states with nonzero complex amplitudes, $|\psi\rangle = \sum_x \alpha_x |x\rangle$. The word names a property of a state relative to a basis, not a kind of state: $|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$ is a superposition in the computational basis and a basis state of the Hadamard basis. What sets a superposition apart from a random choice is that amplitudes are complex numbers, so contributions to one outcome can cancel, while probabilities of a random choice only add.

## In plain words

A classical bit is zero or one. A qubit can be in a state that mixes both answers, each with a weight. The weights are not chances. They are numbers that can be positive, negative or complex, and the chance of an answer comes from the size of its weight only when the qubit is measured. Then the qubit gives one answer, and the mix is gone. Because weights can be negative, two routes to the same answer can cancel each other, and that answer then never occurs. A coin that is flipped at random cannot do this: chances never cancel. Quantum algorithms use this. They arrange the weights so that the routes to wrong answers cancel and the routes to right answers add up. A superposition is not a hidden list of answers that a computer can read out one by one.

## The idea

Take an orthonormal basis $|e_0\rangle, \dots, |e_{d-1}\rangle$ of the state space, usually the computational basis $|x\rangle$ of $n$ qubits. Every pure state is a linear combination

$$|\psi\rangle = \sum_k \alpha_k |e_k\rangle, \qquad \alpha_k = \langle e_k|\psi\rangle, \qquad \sum_k |\alpha_k|^2 = 1.$$

The state is a *superposition* of the basis states $|e_k\rangle$ with $\alpha_k \ne 0$. It is a superposition in that basis when at least two $\alpha_k$ are nonzero. The *superposition principle* says that every such unit vector is a possible state, so the state space is a vector space and not only the set of basis states.

**Superposition depends on the basis.** Every state is a basis state of some orthonormal basis, so "is a superposition" has no meaning without a basis. In quantum computing the default basis is the computational basis, the one in which the hardware measures.

**Superposition is not a mixture.** The [mixed state](/mixed-state/) "$|0\rangle$ with probability $\tfrac{1}{2}$, $|1\rangle$ with probability $\tfrac{1}{2}$" and the superposition $|+\rangle$ give the same statistics in the computational basis. They differ in other bases: the [Hadamard gate](/hadamard-gate/) maps $|+\rangle$ to $|0\rangle$, so a measurement after $H$ gives $0$ every time, but it leaves the mixture uniform. In the same way $|+\rangle$ and $|-\rangle = (|0\rangle - |1\rangle)/\sqrt{2}$ have the same weights $|\alpha_k|^2$ and are orthogonal states. The relative phase is part of the superposition.

**Amplitudes interfere.** Apply $H$ twice to $|0\rangle$. After the first $H$ the state is $\tfrac{1}{\sqrt 2}|0\rangle + \tfrac{1}{\sqrt 2}|1\rangle$. The second $H$ sends each term to $|0\rangle$ and $|1\rangle$ again, and the amplitude of an outcome is the sum over the two paths:

$$\langle 1|H H|0\rangle = \tfrac{1}{\sqrt 2} \cdot \tfrac{1}{\sqrt 2} + \tfrac{1}{\sqrt 2} \cdot \bigl(-\tfrac{1}{\sqrt 2}\bigr) = 0, \qquad \langle 0|H H|0\rangle = \tfrac{1}{2} + \tfrac{1}{2} = 1.$$

A classical bit that is set to a fair random value, and then set to a fair random value again, is uniform after both steps. Its two paths to the value $1$ have probabilities $\tfrac{1}{4}$ and $\tfrac{1}{4}$, and they add to $\tfrac{1}{2}$. A [probabilistic Turing machine](/probabilistic-turing-machine/) evolves a vector of probabilities by stochastic matrices, whose entries are nonnegative. A quantum computer evolves a vector of amplitudes by unitary matrices, whose entries can have any phase. This is the difference that [quantum interference](/quantum-interference/) exploits.

**Measurement gives one outcome.** A measurement in the basis $|e_k\rangle$ returns $k$ with probability $|\alpha_k|^2$ ([Born rule](/born-rule/)) and leaves the state $|e_k\rangle$. One run of a circuit on the uniform superposition of $2^n$ inputs returns one sample, not $2^n$ answers. An algorithm must make the wanted answer likely before the measurement.

## Examples

**The uniform superposition.** The [Hadamard gate](/hadamard-gate/) on each of $n$ qubits maps $|0 \cdots 0\rangle$ to $2^{-n/2} \sum_{x=0}^{2^n - 1} |x\rangle$, with all $2^n$ amplitudes equal. It is the first step of the [Deutsch-Jozsa algorithm](/deutsch-jozsa-algorithm/), of [Simon's algorithm](/simon-algorithm/) and of [Grover search](/grover-search/). It is a product state, so it is a superposition without [entanglement](/entanglement/).

**A Bell state.** $(|00\rangle + |11\rangle)/\sqrt{2}$ is a superposition of two basis states and is entangled ([Bell states](/bell-states/)). Superposition is a property of one state in one basis; entanglement is a property of a state with respect to a split into parts.

**One state, two bases.** $|0\rangle = (|+\rangle + |-\rangle)/\sqrt{2}$, so the basis state $|0\rangle$ is a superposition in the Hadamard basis.

**A cat state.** The GHZ state $(|0 \cdots 0\rangle + |1 \cdots 1\rangle)/\sqrt{2}$ on $n$ qubits has two nonzero amplitudes. A measurement gives all zeros or all ones, each with probability $\tfrac{1}{2}$.

**Not this superposition.** The [superposition](/superposition/) rule of automated theorem proving is an inference rule for equational logic. It has no relation to the quantum concept.

### Implementation

The file `impl/python/quantum_superposition.py` computes the amplitudes of a state in a given basis, tests whether a state is a superposition in that basis, and builds the uniform superposition with $H$ on each qubit. It compares the two-step examples above exactly: the classical case with fractions, which give $\tfrac{1}{2}$ for every path count, and the quantum case with integer path sums, where the two paths of $H H$ to $|1\rangle$ sum to $0$. A sampling test with a fixed seed measures the uniform superposition on 3 qubits 16000 times and checks that every frequency is within $0.02$ of $\tfrac{1}{8}$.

## Where it is used

- Every quantum algorithm: the state between the first gate and the final measurement is in general a superposition of many basis states, and the gates change the amplitudes so that they interfere.
- [Quantum parallelism](/quantum-parallelism/): an oracle applied to a superposition of inputs gives a superposition of input and output pairs. A measurement returns one pair only, so the gain needs interference.
- [Superdense coding](/superdense-coding/) and [quantum teleportation](/quantum-teleportation/): both start from a superposition shared between two parties.
- [Quantum state tomography](/quantum-state-tomography/): measurements in several bases are needed because one basis does not see the relative phases of a superposition.

### History

Dirac made the superposition principle the first principle of his textbook in 1930, with the example of the polarization of a photon. Schrödinger's cat example of 1935 described a superposition of macroscopically different states.

## References
