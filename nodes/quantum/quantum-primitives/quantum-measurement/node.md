---
tag: GQ7MFN
kind: concept
slug: quantum-measurement
name: Quantum measurement
aliases:
- projective measurement
- wavefunction collapse
area: quantum/quantum-primitives
level: intro
summary: "A quantum measurement returns an outcome m with the Born probability and replaces the state by P_m|psi>/sqrt(p_m). POVMs are the general case, and each is projective on a larger space."
prereqs: [born-rule]
see_also: [density-matrix, quantum-channel, kraus-operators, state-discrimination-problem, quantum-state-tomography, ancilla-qubits, no-cloning-theorem, gram-schmidt-process]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.2.3 (the measurement postulate), Section 2.2.5 (projective measurements), Section 2.2.6 (POVM measurements) and Section 4.4 (measurement in the circuit model)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.2.2 (measurement)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 2.3 (measurements), with Naimark's theorem in Section 2.3.2
  - book: isbn:9780691178561
    title: John von Neumann, Mathematical Foundations of Quantum Mechanics, new edition, translated by Robert T. Beyer, edited by Nicholas A. Wheeler, Princeton University Press, 2018
    locator: Chapter VI, The measuring process
  - paper: doi:10.1002/andp.19504430510
    title: Gerhart Lüders, Über die Zustandsänderung durch den Meßprozeß, Annalen der Physik (6) 8, 1951, pages 322 to 328
    locator: the state change P_m psi / norm for a measurement with degenerate outcomes
---

A *quantum measurement* is the only way to get classical information out of a quantum system. A *projective measurement* is a set of orthogonal projectors $P_m$ that sum to the identity. On the state $|\psi\rangle$ it gives the outcome $m$ with probability $p_m = \langle\psi|P_m|\psi\rangle$, the [Born rule](/born-rule/), and the state after it is $P_m|\psi\rangle/\sqrt{p_m}$. A measurement is not a [unitary](/unitary-operator/) operation: it is random, it is not reversible, and in general it destroys the superposition that it measures. The general case, a POVM, is a projective measurement on a larger space, by Naimark's theorem.

## In plain words

To learn something about a qubit, you must measure it. A measurement asks one question with a fixed set of possible answers, and it returns one answer at random, with chances that the state sets. The act of measuring also changes the state: after the answer, the system is in the state that matches that answer. So if you ask the same question again at once, you get the same answer again. Most of the information in a state is lost in this step and cannot be recovered. A measurement cannot be undone, and no series of measurements on one copy shows the full state. Some useful questions have more answers than the number of states that the system can hold with no overlap. They are possible too, by joining an extra system to the first one and asking an ordinary question about the pair.

## The idea

**Projective measurements.** A projective measurement on a Hilbert space $\mathcal{H}$ is a list of matrices $P_1, \dots, P_k$ with

$$P_m^\dagger = P_m, \qquad P_m P_{m'} = \delta_{m m'} P_m, \qquad \sum_m P_m = I.$$

Each $P_m$ is the orthogonal projector onto a subspace $V_m$, and $\mathcal{H}$ is the orthogonal direct sum of the $V_m$. On the unit vector $|\psi\rangle$:

1. the outcome is $m$ with probability $p_m = \langle\psi|P_m|\psi\rangle = \lVert P_m\psi \rVert^2$;
2. if the outcome is $m$, the state after the measurement is $|\psi_m\rangle = P_m|\psi\rangle / \sqrt{p_m}$.

Rule 2 is the projection postulate of von Neumann, in the form Lüders gave for subspaces of dimension more than one. It keeps the part of $|\psi\rangle$ inside $V_m$, with its amplitude ratios and relative phases, and removes the rest. A measurement *in a basis* $|e_k\rangle$ is the case $P_k = |e_k\rangle\langle e_k|$; the state after the outcome $k$ is $|e_k\rangle$, up to a global phase. Measuring some qubits of a register in the computational basis is the case $P_y = \sum_{x\,:\,x_S = y}|x\rangle\langle x|$, where $x_S$ is the restriction of the bit string $x$ to the measured set $S$.

**An observable.** A Hermitian matrix $A$ with the spectral decomposition $A = \sum_m a_m P_m$ ([spectral theorem](/spectral-theorem/)) names the projective measurement $\{P_m\}$ with the outcome values $a_m$. The mean outcome is $\langle\psi|A|\psi\rangle$. The Pauli $Z$ is the measurement in the computational basis with the values $+1$ and $-1$.

**Repeatability.** Since $P_m P_m = P_m$, the state $|\psi_m\rangle$ gives outcome $m$ again with probability $1$. A second measurement with the same projectors adds no information.

**Not unitary, not linear.** A measurement maps pure states to a random pure state. When the outcome is not recorded, the state after it is the [density matrix](/density-matrix/) $\sum_m P_m |\psi\rangle\langle\psi| P_m$, which is mixed in general: $|+\rangle$ measured in the computational basis becomes $I/2$. No unitary maps a pure state to a mixed one. A measurement of the two-outcome kind also cannot be reversed: $|0\rangle$ and $|+\rangle$ both give $|0\rangle$ after the outcome $0$. In the circuit model a measurement is a separate step, usually at the end. The principle of deferred measurement says that a measurement in the middle of a circuit, whose outcome controls later gates, can be moved to the end, with the classical control replaced by quantum controlled gates.

**POVMs.** A *positive operator-valued measure* is a list of Hermitian positive semidefinite matrices $E_1, \dots, E_k$ with $\sum_m E_m = I$. The outcome $m$ has the probability $\langle\psi|E_m|\psi\rangle$, or $\operatorname{tr}(E_m\rho)$ for a density matrix. The $E_m$ need not be projectors and need not commute, and $k$ can be larger than $\dim\mathcal{H}$. A projective measurement is the case where every $E_m$ is a projector. The state after a POVM outcome is not fixed by the $E_m$ alone. It is $M_m|\psi\rangle/\sqrt{p_m}$ for matrices $M_m$ with $M_m^\dagger M_m = E_m$, the [Kraus operators](/kraus-operators/) of the measurement.

**Naimark's theorem.** Every POVM is a projective measurement on a larger space. For a POVM of rank-one elements $E_k = |e_k\rangle\langle e_k|$ on $\mathbb{C}^d$, the matrix $V$ with

$$V|\psi\rangle = \sum_{k} \langle e_k|\psi\rangle\, |k\rangle$$

maps $\mathbb{C}^d$ into $\mathbb{C}^K$ and satisfies $V^\dagger V = \sum_k |e_k\rangle\langle e_k| = I$, so it is an isometry. Extend it to a unitary $U$ on $\mathbb{C}^K$ by the [Gram-Schmidt process](/gram-schmidt-process/), apply $U$ to $|\psi\rangle$ padded with zeros (on qubits: the system together with [ancilla qubits](/ancilla-qubits/) in $|0\rangle$), and measure in the standard basis. The outcome $k$ then has the probability $|\langle e_k|\psi\rangle|^2 = \langle\psi|E_k|\psi\rangle$. A general POVM element $E_m$ is a sum of rank-one terms, and the same construction with the square roots $\sqrt{E_m}$ works for it.

## Examples

**A qubit in the computational basis.** $\tfrac{3}{5}|0\rangle + \tfrac{4i}{5}|1\rangle$ gives $0$ with probability $\tfrac{9}{25}$ and then is $|0\rangle$, or gives $1$ with probability $\tfrac{16}{25}$ and then is $|1\rangle$ up to the phase $i$.

**One qubit of a Bell state.** In $(|00\rangle + |11\rangle)/\sqrt{2}$, measure qubit $0$ with $P_b = I \otimes |b\rangle\langle b|$. Each outcome $b$ has probability $\tfrac{1}{2}$, and the state after it is $|bb\rangle$. A later measurement of qubit $1$ then gives $b$ with certainty. The outcomes are perfectly correlated, but each alone is a fair coin, so the pair cannot send a message ([Bell states](/bell-states/), [no-cloning theorem](/no-cloning-theorem/)).

**A two-outcome measurement on two qubits.** The parity measurement $P_{\text{even}} = |00\rangle\langle 00| + |11\rangle\langle 11|$, $P_{\text{odd}} = I - P_{\text{even}}$ asks whether the two bits are equal and nothing else. On $\alpha|00\rangle + \beta|11\rangle$ it gives "even" with certainty and does not change the state. This kind of measurement, with projectors of rank more than one, is how [quantum error correction](/quantum-error-correction/) reads an error syndrome without reading the data.

**The trine POVM.** Let $|\psi_k\rangle = \cos(2\pi k/3)|0\rangle + \sin(2\pi k/3)|1\rangle$ for $k = 0, 1, 2$: three real states at $120^\circ$ on a great circle of the [Bloch sphere](/bloch-sphere/). The matrices $E_k = \tfrac{2}{3}|\psi_k\rangle\langle\psi_k|$ sum to $I$ and form a POVM with three outcomes on a two-dimensional space. They are not projectors: $E_k^2 = \tfrac{2}{3}E_k$. On $|0\rangle$ the outcome probabilities are $\tfrac{2}{3}, \tfrac{1}{6}, \tfrac{1}{6}$. A Naimark unitary on two qubits, the system on qubit $0$ and an ancilla on qubit $1$, gives the same three probabilities, and the fourth outcome has probability $0$.

**Unambiguous discrimination.** The states $|0\rangle$ and $|+\rangle$ are not orthogonal, so no measurement tells them apart with certainty. A three-outcome POVM can answer "it was $|0\rangle$", "it was $|+\rangle$" or "do not know", and never be wrong ([state discrimination](/state-discrimination-problem/)).

### Implementation

The file `impl/python/quantum_measurement.py` tests whether a list of matrices is a projective measurement, computes the outcome probabilities and the state after an outcome, samples a measurement with a seeded generator, builds the trine POVM, and builds a Naimark unitary for a rank-one POVM by Gram-Schmidt completion. The tests check repeatability, the Bell state correlations over 200 seeded runs, that an unrecorded measurement of $|+\rangle$ gives the mixed state with $\operatorname{tr}\rho^2 = \tfrac{1}{2}$, the exact trine probabilities, and that the Naimark unitary reproduces the POVM probabilities on 30 random states and in 20000 seeded samples within $0.02$.

## Where it is used

- The last step of almost every quantum algorithm, which reads the answer as a bit string from a measurement in the computational basis.
- Mid-circuit measurements and classical control: [quantum teleportation](/quantum-teleportation/) and error correction measure some qubits and choose later gates by the outcomes.
- [Quantum state tomography](/quantum-state-tomography/), which estimates a state from the statistics of measurements in several bases, and [state discrimination](/state-discrimination-problem/), which chooses the measurement that best tells given states apart.
- Measurement-based quantum computing, where a sequence of one-qubit measurements on an entangled resource state carries out a computation.

### Common errors

- Treating measurement as a gate. It has no unitary matrix, and a simulator that applies it must sample an outcome and renormalize.
- Forgetting the state change. After a measurement of qubit $0$ of a register, the other qubits are in the state that matches the outcome, not in their state before.
- Reading a POVM element as a projector. $E_m$ fixes only the probabilities; the state after the outcome needs a choice of $M_m$.

## References
