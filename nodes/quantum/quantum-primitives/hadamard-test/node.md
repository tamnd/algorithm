---
tag: N1NJ1H
kind: technique
slug: hadamard-test
name: Hadamard test
area: quantum/quantum-primitives
level: intro
summary: "A circuit with one ancilla, two Hadamard gates and a controlled-U. The ancilla reads 0 with probability (1 + Re<psi|U|psi>)/2, so many runs estimate the real part. An added S-dagger gives Im."
prereqs: [phase-kickback, hadamard-gate, quantum-measurement]
see_also: [swap-test, quantum-phase-estimation, ancilla-qubits, unitary-operator, density-matrix, mixed-state, hoeffding-inequality, linear-combination-of-unitaries]
sources:
  - paper: doi:10.1098/rspa.1998.0164
    title: "Richard Cleve, Artur Ekert, Chiara Macchiavello and Michele Mosca, Quantum algorithms revisited, Proceedings of the Royal Society of London A 454(1969):339-354, 1998"
    locator: "the interferometer form of a quantum algorithm: a Hadamard gate, a controlled-U gate on an eigenvector and a Hadamard gate on one qubit, with outcome probabilities (1 ± cos φ)/2 (general locator)"
  - paper: doi:10.1103/PhysRevLett.81.5672
    title: "Emanuel Knill and Raymond Laflamme, Power of one bit of quantum information, Physical Review Letters 81(25):5672-5675, 1998"
    locator: "the one-clean-qubit model (DQC1): one pure qubit and a maximally mixed register give an estimate of the normalized trace of U (general locator)"
  - paper: doi:10.1007/s00453-008-9168-0
    title: "Dorit Aharonov, Vaughan Jones and Zeph Landau, A polynomial quantum algorithm for approximating the Jones polynomial, Algorithmica 55(3):395-421, 2009"
    locator: "the estimate of a matrix element of the unitary for a braid, by the Hadamard test (general locator)"
  - paper: arxiv:1907.09415
    title: Ronald de Wolf, Quantum Computing, lecture notes
    locator: "Section 16.6 and Figure 16.3 (the SWAP test: Hadamard, controlled SWAP, Hadamard, and outcome 1 with probability (1 - |<φ|ψ>|^2)/2)"
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: "Section 5.2 (phase estimation: a Hadamard gate on each control, controlled U^(2^j) on an eigenvector, and the readout of the phase)"
---

The *Hadamard test* is a circuit that estimates the real part of $\langle\psi|U|\psi\rangle$ for a [unitary](/unitary-operator/) $U$ and a [state](/quantum-state/) $|\psi\rangle$, with one [ancilla qubit](/ancilla-qubits/) and a controlled-$U$ gate. The ancilla goes through a [Hadamard gate](/hadamard-gate/), controls $U$, goes through a second Hadamard gate and is [measured](/quantum-measurement/): it reads $0$ with probability $\frac12(1 + \mathrm{Re}\langle\psi|U|\psi\rangle)$. One more gate $S^\dagger$ on the ancilla gives the imaginary part instead. It is [phase kickback](/phase-kickback/) for a state $|\psi\rangle$ that need not be an eigenvector of $U$.

## In plain words

You have a state and an operation, and you want a number that tells you how much the operation changes the state. You cannot get this number from the state directly.

The test sends one extra qubit into two paths at the same time. On one path the operation acts on the state, and on the other path nothing happens. Then the two paths are joined again and the extra qubit is measured. If the operation does not change the state, the paths agree and the qubit always reads 0. If the operation turns the state into its negative, the qubit always reads 1. Between these two cases the probability tells you the overlap. One run gives only one bit, so you repeat the test many times and count.

## When it applies

- You can prepare $|\psi\rangle$ again for each run, or you are given many copies of it.
- You can apply controlled-$U$, that is $|0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes U$ with the ancilla first, and not only $U$ itself.
- You want a number of the form $\langle\psi|U|\psi\rangle$: an overlap of two states, the expectation of a unitary observable such as a [Pauli string](/pauli-string-decomposition/), a trace, or one bit of a phase.
- An additive error $\varepsilon$ is enough. The number of runs grows as $1/\varepsilon^2$.

## The template

```pseudo id=main
HADAMARD-TEST(U, |ψ⟩, part, n)
L1  prepare the ancilla in |0⟩ next to |ψ⟩
L2  apply H to the ancilla
L3  if part = Im: apply S† to the ancilla     ▷ hole: the part to estimate
L4  apply controlled-U, the ancilla controls  ▷ hole: a circuit for controlled-U, global phase included
L5  apply H to the ancilla
L6  measure the ancilla; repeat n times; return (n₀ - n₁)/n  ▷ hole: the number of runs n
```

**Why it works.** Write $z = \langle\psi|U|\psi\rangle$. After L2 the state is $\frac{1}{\sqrt2}(|0\rangle|\psi\rangle + |1\rangle|\psi\rangle)$, and after L4 it is $\frac{1}{\sqrt2}(|0\rangle|\psi\rangle + |1\rangle U|\psi\rangle)$. After L5 it is

$$\tfrac12\,|0\rangle\bigl(|\psi\rangle + U|\psi\rangle\bigr) + \tfrac12\,|1\rangle\bigl(|\psi\rangle - U|\psi\rangle\bigr).$$

So $P(0) = \frac14\,\| |\psi\rangle + U|\psi\rangle \|^2 = \frac14(2 + z + \bar z) = \frac12(1 + \mathrm{Re}\,z)$ and $P(1) = \frac12(1 - \mathrm{Re}\,z)$. The difference is $P(0) - P(1) = \mathrm{Re}\,z$. With L3, the $|1\rangle$ part of the ancilla gets the factor $-i$, so the circuit is the test for $-iU$, and $\mathrm{Re}(-iz) = \mathrm{Im}\,z$.

**The estimate.** Each run gives $+1$ for outcome $0$ and $-1$ for outcome $1$, and the mean of this value is $\mathrm{Re}\,z$. The values lie in an interval of length $2$, so [Hoeffding's inequality](/hoeffding-inequality/) gives $\Pr[|(n_0 - n_1)/n - \mathrm{Re}\,z| \ge \varepsilon] \le 2e^{-n\varepsilon^2/2}$. Thus $n \ge 2\ln(2/\delta)/\varepsilon^2$ runs give error at most $\varepsilon$ with probability at least $1 - \delta$. For $\varepsilon = 0.01$ and $\delta = 0.05$ this is $n = 73778$.

**Example: an eigenvector.** Let $U = X$ and $|\psi\rangle = |{+}\rangle$. Then $X|{+}\rangle = |{+}\rangle$, so $z = 1$ and the ancilla reads $0$ on every run. This is phase kickback with eigenvalue $1$.

**Example: no overlap.** Let $U = X$ and $|\psi\rangle = |0\rangle$. Then $\langle 0|X|0\rangle = 0$, and the ancilla reads $0$ and $1$ with probability $\frac12$ each.

**Example: an imaginary value.** Let $U = S = \mathrm{diag}(1, i)$ and $|\psi\rangle = |1\rangle$, so $z = i$. The real-part test gives $P(0) = \frac12$. The test with L3 gives $P(0) = \frac12(1 + 1) = 1$.

**Example: the T gate.** Let $U = T = \mathrm{diag}(1, e^{i\pi/4})$ and $|\psi\rangle = |1\rangle$. Then $\mathrm{Re}\,z = \cos(\pi/4) \approx 0.7071$ and $P(0) \approx 0.8536$.

## Classic examples

- **The swap test.** Let $U$ be the gate SWAP on two registers and $|\psi\rangle = |a\rangle|b\rangle$. Then $\langle a|\langle b|\,\mathrm{SWAP}\,|a\rangle|b\rangle = \langle a|b\rangle\langle b|a\rangle = |\langle a|b\rangle|^2$, which is real. So the [swap test](/swap-test/) is the Hadamard test for SWAP, and it reads $1$ with probability $\frac12(1 - |\langle a|b\rangle|^2)$.
- **Phase estimation.** If $|\psi\rangle$ is an eigenvector with $U|\psi\rangle = e^{i\varphi}|\psi\rangle$, the test gives $\cos\varphi$, and the test with L3 gives $\sin\varphi$. Together they give $\varphi$. [Quantum phase estimation](/quantum-phase-estimation/) applies this step with $U, U^2, U^4, \ldots$ on many ancillas at once and reads all of them with an inverse [quantum Fourier transform](/quantum-fourier-transform/).
- **The trace of a unitary.** Knill and Laflamme (1998) studied a model with one pure qubit and all other qubits maximally mixed, the one-clean-qubit model (DQC1). With the input $I/2^k$ on $k$ qubits the test gives $\frac{1}{2^k}\mathrm{Re}\,\mathrm{Tr}(U)$, because $\mathrm{Tr}(\rho U)$ replaces $\langle\psi|U|\psi\rangle$ for a [mixed state](/mixed-state/) $\rho$.
- **The Jones polynomial.** Aharonov, Jones and Landau (2009) write the value of the Jones polynomial at a root of unity as a matrix element $\langle\psi|U|\psi\rangle$ of a unitary built from the braid. The Hadamard test then gives an additive approximation in polynomial time.
- **Expectation values.** In [variational algorithms](/variational-quantum-eigensolver/) a Hamiltonian is a sum $\sum_k c_k P_k$ of Pauli strings. Each $P_k$ is unitary, so each $\langle\psi|P_k|\psi\rangle$ is one Hadamard test, and the energy is the weighted sum.

## Variations

- **An overlap of two prepared states.** If $|\phi\rangle = V|0\rangle$ and $|\chi\rangle = W|0\rangle$, the test for $U = V^\dagger W$ on $|0\rangle$ gives $\mathrm{Re}\langle 0|V^\dagger W|0\rangle = \mathrm{Re}\langle\phi|\chi\rangle$. With L3 it gives the imaginary part, so the two tests give the complex overlap, including its phase. The swap test gives only $|\langle\phi|\chi\rangle|^2$.
- **A mixed input.** The input can be a [density matrix](/density-matrix/) $\rho$, and the result is $\mathrm{Re}\,\mathrm{Tr}(\rho U)$. The maximally mixed state is the same as one half of a maximally entangled state on twice as many qubits, where $U$ acts only on that half.
- **A sum of unitaries.** For $A = \sum_k c_k U_k$, either run one test per term and add the results, or prepare the terms in one control register as in a [linear combination of unitaries](/linear-combination-of-unitaries/).
- **Fewer runs.** The number of runs grows as $1/\varepsilon^2$. [Amplitude amplification](/amplitude-amplification/) in the form of amplitude estimation reduces this to order $1/\varepsilon$ applications of the circuit, but it needs the circuit and its inverse, not only fresh copies of $|\psi\rangle$.

## Pitfalls

- **The global phase of $U$ changes the answer.** For $e^{i\alpha}U$ the test gives $\mathrm{Re}(e^{i\alpha}z)$. So the circuit for controlled-$U$ must have the correct phase, not only the correct $U$. This also shows that a black box for $U$ alone is not enough: $U$ and $e^{i\alpha}U$ act the same on every input, but their tests give different results.
- **One run gives one bit.** The test does not output $z$. It outputs a sample, and the error after $n$ runs is of order $1/\sqrt n$. For error $10^{-3}$ the number of runs is in the millions.
- **The input state is used up.** After the measurement the register holds $(|\psi\rangle \pm U|\psi\rangle)$, normalized, and not $|\psi\rangle$. Each run needs a new copy, unless $|\psi\rangle$ is an eigenvector of $U$.
- **Real part only.** The plain test gives $\mathrm{Re}\,z$, and $\mathrm{Re}\,z = 0$ does not mean $z = 0$, as the gate $S$ on $|1\rangle$ shows. For $|z|$ or the phase of $z$, run both tests.
- **The ancilla starts in $|0\rangle$.** If it starts in a mixed state the two paths interfere less, and the estimate is scaled down by a factor that the circuit cannot see.

## Exercises

1. Show directly from the state after L5 that $P(1) = \frac12(1 - \mathrm{Re}\langle\psi|U|\psi\rangle)$.
2. In L3, replace $S^\dagger$ by $S$. Which number does the test estimate now?
3. Show that the test for SWAP on $|a\rangle|b\rangle$ gives $|\langle a|b\rangle|^2$, and compute it for $|a\rangle = |0\rangle$ and $|b\rangle = |{+}\rangle$.
4. How many runs give error at most $0.1$ with probability at least $0.99$?
5. Let the system be the second half of $\frac{1}{\sqrt{2^k}}\sum_s |s\rangle|s\rangle$, with $U$ acting on the second half only. Show that the test gives $\frac{1}{2^k}\mathrm{Re}\,\mathrm{Tr}(U)$.
6. Let the ancilla start in the mixed state $(1 - p)|0\rangle\langle 0| + p|1\rangle\langle 1|$. Show that $P(0) - P(1) = (1 - 2p)\,\mathrm{Re}\langle\psi|U|\psi\rangle$.

## References
