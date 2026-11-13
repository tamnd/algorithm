---
tag: 0GVHJA
kind: definition
slug: hadamard-gate
name: Hadamard gate
aliases:
- H gate
area: quantum/quantum-primitives
level: intro
summary: "The Hadamard gate H = (X + Z)/sqrt 2 maps |0> and |1> to the equal superpositions |+> and |->. H on each of n qubits is the Walsh-Hadamard transform."
prereqs: [pauli-gates]
see_also: [walsh-hadamard-transform, fast-walsh-hadamard-transform, deutsch-jozsa-algorithm, quantum-fourier-transform, hadamard-code, fourier-analysis-of-boolean-functions, clifford-group, phase-and-t-gates]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.3.1 (single qubit gates), Section 1.4.2 (the Hadamard transform on n qubits), Section 1.4.4 (the Deutsch-Jozsa algorithm) and Section 4.2 (single qubit operations)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.4 (elementary gates) and Chapter 2 (the Hadamard transform on n qubits)
---

The *Hadamard gate* is the one-qubit gate

$$H = \frac{1}{\sqrt 2}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix} = \frac{X + Z}{\sqrt 2}.$$

It maps $|0\rangle$ to $|+\rangle = (|0\rangle + |1\rangle)/\sqrt 2$ and $|1\rangle$ to $|-\rangle = (|0\rangle - |1\rangle)/\sqrt 2$, so it changes between the computational basis and the basis of $X$. It is its own inverse. $H$ applied to each of $n$ qubits is the Walsh-Hadamard transform, and on $|0\cdots 0\rangle$ it gives the uniform superposition of all $2^n$ basis states, the first step of most quantum algorithms.

## Definition

The **Hadamard gate** is the [quantum gate](/quantum-gate/) on one qubit with the matrix $H$ above, in the basis $|0\rangle, |1\rangle$. On a basis state $|b\rangle$, $b \in \{0, 1\}$,

$$H|b\rangle = \frac{1}{\sqrt 2}\left(|0\rangle + (-1)^b|1\rangle\right) = \frac{1}{\sqrt 2}\sum_{c \in \{0,1\}} (-1)^{bc}|c\rangle.$$

**Properties.**

1. $H = (X + Z)/\sqrt 2$, with the [Pauli matrices](/pauli-gates/) $X$ and $Z$.
2. $H^\dagger = H$ and $H^2 = I$. So $H$ is Hermitian, [unitary](/unitary-operator/) and its own inverse. Its eigenvalues are $+1$ and $-1$, and $\det H = -1$.
3. Conjugation by $H$ exchanges $X$ and $Z$: $HXH = Z$, $HZH = X$ and $HYH = -Y$. So $H$ is in the [Clifford group](/clifford-group/).
4. On the [Bloch sphere](/bloch-sphere/), $H$ is the half turn about the axis $(\hat x + \hat z)/\sqrt 2$. As a matrix, $H = i\,e^{-i(\pi/2)\,\vec n \cdot \vec\sigma}$ with $\vec n = (1, 0, 1)/\sqrt 2$. It maps the Bloch vector $(x, y, z)$ to $(z, -y, x)$.

**The Hadamard transform on $n$ qubits.** Let $H^{\otimes n}$ be $H$ applied to each of $n$ qubits. For $x, y \in \{0, 1\}^n$ let $x \cdot y = \sum_j x_j y_j \bmod 2$, the parity of the bitwise AND. Then

$$H^{\otimes n}|x\rangle = \frac{1}{\sqrt{2^n}}\sum_{y \in \{0,1\}^n} (-1)^{x \cdot y}|y\rangle, \qquad \langle y|H^{\otimes n}|x\rangle = \frac{(-1)^{x \cdot y}}{\sqrt{2^n}}.$$

This $2^n \times 2^n$ matrix is the normalized [Walsh-Hadamard transform](/walsh-hadamard-transform/), the Fourier transform of the group $\mathbb{Z}_2^n$. In particular

$$H^{\otimes n}|0\cdots 0\rangle = \frac{1}{\sqrt{2^n}}\sum_{y \in \{0,1\}^n}|y\rangle.$$

The formula follows from the one-qubit formula, because $H^{\otimes n}|x_{n-1}\cdots x_0\rangle = \bigotimes_j H|x_j\rangle$ and the signs multiply to $(-1)^{\sum_j x_j y_j}$. The [tensor product](/tensor-product/) order does not change $H^{\otimes n}$, because every factor is the same, and $x \cdot y$ is symmetric in the bits. So this formula is the same with the qubit order convention of [quantum state](/quantum-state/) (qubit $0$ is the least significant bit) and with the reverse order.

**Cost.** As a circuit, $H^{\otimes n}$ is $n$ gates of depth $1$. As a classical computation on a vector of $2^n$ amplitudes, it takes $n 2^n$ additions and subtractions with the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/), one butterfly pass per qubit, and the same number of operations with $n$ calls of a one-qubit gate in a state-vector simulator.

## Examples and non-examples

**One qubit.** $H|0\rangle = |+\rangle$ and $H|1\rangle = |-\rangle$. A measurement of $|+\rangle$ or $|-\rangle$ in the computational basis gives $0$ or $1$ with probability $\tfrac12$ each, by the [Born rule](/born-rule/).

**Interference.** $H$ applied twice gives back $|0\rangle$:

$$H|+\rangle = \tfrac{1}{2}\left(|0\rangle + |1\rangle\right) + \tfrac{1}{2}\left(|0\rangle - |1\rangle\right) = |0\rangle.$$

The two paths to $|1\rangle$ have the amplitudes $+\tfrac12$ and $-\tfrac12$, and they cancel. Probabilities cannot cancel in this way. A fair coin flipped twice is still fair: the stochastic matrix $\tfrac12\begin{pmatrix}1 & 1 \\ 1 & 1\end{pmatrix}$ squares to itself. This is the simplest example of interference in a [quantum superposition](/quantum-superposition/), and the main difference between a quantum step and a random step of a [probabilistic Turing machine](/probabilistic-turing-machine/).

**Three qubits.** $H^{\otimes 3}|101\rangle = \tfrac{1}{2\sqrt 2}\sum_y (-1)^{y_2 + y_0}|y\rangle$. The sign of $|y\rangle$ is the parity of the bits of $y$ at the positions where $x = 101$ has a $1$. The amplitude of $|111\rangle$ is $+\tfrac{1}{2\sqrt 2}$ and the amplitude of $|100\rangle$ is $-\tfrac{1}{2\sqrt 2}$.

**Algorithms.** [Deutsch-Jozsa](/deutsch-jozsa-algorithm/), [Bernstein-Vazirani](/bernstein-vazirani-algorithm/) and [Simon's algorithm](/simon-algorithm/) apply $H^{\otimes n}$, then an oracle, then $H^{\otimes n}$ again, and measure. The second transform maps the phases $(-1)^{f(x)}$ to amplitudes that show a global property of $f$. [Grover search](/grover-search/) starts from $H^{\otimes n}|0\cdots 0\rangle$ and uses $H^{\otimes n}$ in its diffusion step.

**Hadamard and the Fourier transform.** On one qubit, $H$ is the [quantum Fourier transform](/quantum-fourier-transform/) of $\mathbb{Z}_2$. On $n$ qubits, $H^{\otimes n}$ is the Fourier transform of $\mathbb{Z}_2^n$, not of $\mathbb{Z}_{2^n}$. The quantum Fourier transform of $\mathbb{Z}_{2^n}$ needs controlled phase gates in addition to Hadamard gates.

**Non-example: $\sqrt{X}$.** $H$ also makes equal superpositions from the basis states, but it is not a square root of $X$: $H^2 = I$. A square root of $X$ is $HSH$, with $S = \operatorname{diag}(1, i)$ from [phase and T gates](/phase-and-t-gates/).

**Non-example: $H$ is not a classical gate.** No stochastic matrix $M$ maps the point distribution on $0$ to the uniform distribution and the uniform distribution back to the point distribution: if $Me_0 = u$, then $Mu = \tfrac12(Me_0 + Me_1)$ has at least weight $\tfrac14$ on $1$. $H$ has a negative entry, and it is the source of the interference above.

### Common errors

- Writing $H|1\rangle = |+\rangle$. The sign of the $|1\rangle$ term is $(-1)^b$, so $H|1\rangle = |-\rangle$.
- Forgetting the normalization. $\tfrac{1}{\sqrt{2^n}}$ belongs to $H^{\otimes n}$; the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) in its usual form omits it and multiplies the norm by $\sqrt{2^n}$.
- Taking $x \cdot y$ as an integer product. It is the inner product of bit strings modulo $2$.

### Implementation

The file `impl/python/hadamard_gate.py` has the matrix $H$, the transform $H^{\otimes n}$ as $n$ one-qubit gates in the simulator, the entry formula $(-1)^{x \cdot y}/\sqrt{2^n}$, and the fast Walsh-Hadamard transform with the normalization. The tests check $H = (X + Z)/\sqrt 2$, unitarity, $H^2 = I$, $HXH = Z$, $HZH = X$, $HYH = -Y$, the formula $H = i\,e^{-i(\pi/2)\vec n \cdot \vec\sigma}$, the matrix of $H^{\otimes n}$ against repeated Kronecker products for $n \le 5$, the uniform superposition for $n \le 8$, the Bloch map $(x, y, z) \mapsto (z, -y, x)$ on 100 random states with seed 7, and the fast transform against the gates on a random state of 10 qubits with seed 101.

## Related definitions

- [Walsh-Hadamard transform](/walsh-hadamard-transform/) and [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/): the classical transform with the matrix $\sqrt{2^n}\,H^{\otimes n}$.
- [Hadamard code](/hadamard-code/): the code whose codewords are the rows of the same $\pm 1$ matrix.
- [Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/): the coefficients of $(-1)^{f(x)}$ in the basis $(-1)^{x \cdot y}$.
- [Kronecker product](/kronecker-product/): $H^{\otimes n}$ is the $n$-fold Kronecker power of $H$.
- [Clifford group](/clifford-group/): $H$ and $S$ generate the one-qubit Clifford group up to phase.
- [Hadamard test](/hadamard-test/): a circuit with $H$ on a control qubit that estimates $\operatorname{Re}\langle\psi|U|\psi\rangle$.

### History

The gate is named after Jacques Hadamard, who in 1893 studied square matrices with entries $\pm 1$ and orthogonal rows. The tensor powers of $\begin{pmatrix}1 & 1 \\ 1 & -1\end{pmatrix}$ are an older example, given by Sylvester in 1867.

## References
