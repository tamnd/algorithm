---
tag: 1RRERC
kind: definition
slug: density-matrix
name: Density matrix
aliases:
- density operator
- statistical operator
area: quantum/quantum-primitives
level: core
summary: "A Hermitian, positive semidefinite matrix of trace 1. It describes every state of a quantum system, pure or mixed, and gives each measurement probability as Tr(P rho)."
prereqs: [quantum-state, qubit, born-rule, positive-definite-matrix]
see_also: [mixed-state, partial-trace, bloch-sphere, quantum-measurement, quantum-channel, von-neumann-entropy, trace-distance, fidelity]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.4 (The density operator), Sections 2.4.1 and 2.4.2 (ensembles, the general properties and Theorem 2.6, unitary freedom in the ensemble)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Chapter 2, Section 2.1 (registers and states, density operators as the states of a register)
  - url: http://eudml.org/doc/59230
    title: "John von Neumann, Wahrscheinlichkeitstheoretischer Aufbau der Quantenmechanik, Nachrichten von der Gesellschaft der Wissenschaften zu Göttingen, Mathematisch-Physikalische Klasse, 1927"
    locator: pp. 245 to 272 (the statistical operator of an ensemble)
  - paper: doi:10.1007/BF01343064
    title: Lev Landau, Das Dämpfungsproblem in der Wellenmechanik, Zeitschrift für Physik 45, 1927
    locator: pp. 430 to 441
---

A density matrix is a [Hermitian](/spectral-theorem/), [positive semidefinite](/positive-definite-matrix/) matrix with trace 1. It is the general description of the state of a quantum system. A [state vector](/quantum-state/) $|\psi\rangle$ describes only a *pure* state, which corresponds to the density matrix $|\psi\rangle\langle\psi|$. A density matrix also describes a system that is in state $|\psi_i\rangle$ with probability $p_i$, and a part of a larger system (see [partial trace](/partial-trace/)). The [Born rule](/born-rule/), unitary evolution and [quantum channels](/quantum-channel/) all act on it directly. The states that are not pure, and the many ensembles that give one density matrix, are the topic of the page [mixed state](/mixed-state/).

## Definition

Let $\mathcal{H} = \mathbb{C}^d$ be the state space of a system. A **density matrix** (or density operator) on $\mathcal{H}$ is a $d \times d$ complex matrix $\rho$ with three properties:

1. $\rho$ is Hermitian: $\rho^\dagger = \rho$.
2. $\rho$ is positive semidefinite: $\langle v | \rho | v \rangle \ge 0$ for every $v \in \mathbb{C}^d$. For a Hermitian matrix this holds exactly when every [eigenvalue](/eigenvalue/) is $\ge 0$.
3. $\operatorname{Tr} \rho = 1$.

By the [spectral theorem](/spectral-theorem/), $\rho = \sum_{k=1}^{d} \lambda_k |e_k\rangle\langle e_k|$ with an orthonormal basis $|e_k\rangle$, $\lambda_k \ge 0$ and $\sum_k \lambda_k = 1$. So the eigenvalues of a density matrix form a [probability distribution](/probability-distribution/). The set of density matrices on $\mathbb{C}^d$ is convex, and it has $d^2 - 1$ real parameters: a Hermitian matrix has $d^2$, and the trace condition removes one.

### Ensembles

An **ensemble** is a list of pairs $\{(p_i, |\psi_i\rangle)\}_{i=1}^{m}$ of probabilities $p_i \ge 0$ with $\sum_i p_i = 1$ and unit vectors $|\psi_i\rangle$. It means: the system is in state $|\psi_i\rangle$ with probability $p_i$. Its density matrix is

$$\rho = \sum_{i=1}^{m} p_i \, |\psi_i\rangle\langle\psi_i|.$$

**Claim.** A matrix $\rho$ is the density matrix of some ensemble if and only if it has the three properties above.

**Proof.** If $\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$, then $\rho^\dagger = \rho$ because each term is Hermitian and each $p_i$ is real. For every $v$, $\langle v|\rho|v\rangle = \sum_i p_i |\langle v|\psi_i\rangle|^2 \ge 0$. And $\operatorname{Tr}\rho = \sum_i p_i \langle\psi_i|\psi_i\rangle = \sum_i p_i = 1$. Conversely, if $\rho$ has the three properties, its spectral decomposition $\sum_k \lambda_k |e_k\rangle\langle e_k|$ is an ensemble, because $\lambda_k \ge 0$ and $\sum_k \lambda_k = \operatorname{Tr}\rho = 1$. $\square$

Many ensembles give the same density matrix. Two ensembles give the same $\rho$ exactly when they are related by a unitary matrix (Hughston, Jozsa and Wootters 1993; Nielsen and Chuang, Theorem 2.6). The statement and its proof are on [mixed state](/mixed-state/).

### What the density matrix predicts

All predictions of quantum mechanics depend on the ensemble only through $\rho$:

- **Measurement.** For a [projective measurement](/quantum-measurement/) with projectors $P_m$ that sum to $I$, outcome $m$ has probability $p(m) = \operatorname{Tr}(P_m \rho)$. After outcome $m$ the state is $P_m \rho P_m / p(m)$. For a POVM with elements $E_m$, $p(m) = \operatorname{Tr}(E_m \rho)$.
- **Expectation.** A Hermitian observable $A$ has mean value $\langle A \rangle = \operatorname{Tr}(\rho A)$.
- **Evolution.** A [unitary](/unitary-operator/) $U$ maps $\rho$ to $U \rho U^\dagger$. A general physical process is a [quantum channel](/quantum-channel/) $\rho \mapsto \sum_k K_k \rho K_k^\dagger$.
- **Composite systems.** Independent systems in states $\rho_A$ and $\rho_B$ have the joint state $\rho_A \otimes \rho_B$ on the [tensor product](/tensor-product/). The state of one part of a joint state $\rho_{AB}$ is the [partial trace](/partial-trace/) $\rho_A = \operatorname{Tr}_B \rho_{AB}$.

Each rule is linear in $\rho$. For an ensemble it gives the average over the ensemble: for example $\operatorname{Tr}(P_m \rho) = \sum_i p_i \langle\psi_i|P_m|\psi_i\rangle$, which is the probability of $m$ when the state is $|\psi_i\rangle$ with probability $p_i$. So two ensembles with the same $\rho$ cannot be told apart by any experiment.

### Pure and mixed

$\rho$ is **pure** if $\rho = |\psi\rangle\langle\psi|$ for a unit vector $|\psi\rangle$, and **mixed** otherwise. The **purity** is $\operatorname{Tr}(\rho^2) = \sum_k \lambda_k^2$.

**Claim.** $1/d \le \operatorname{Tr}(\rho^2) \le 1$, and $\operatorname{Tr}(\rho^2) = 1$ if and only if $\rho$ is pure.

**Proof.** Since $0 \le \lambda_k \le 1$, $\sum_k \lambda_k^2 \le \sum_k \lambda_k = 1$, with equality exactly when each $\lambda_k$ is 0 or 1. The eigenvalues sum to 1, so equality holds exactly when one eigenvalue is 1 and the others are 0, that is, when $\rho = |e_1\rangle\langle e_1|$ is pure. For the lower bound, the Cauchy-Schwarz inequality gives $1 = (\sum_k \lambda_k)^2 \le d \sum_k \lambda_k^2$. $\square$

The lower bound $1/d$ holds only for the **maximally mixed state** $I/d$. A global phase does not change a pure density matrix: $(e^{i\theta}|\psi\rangle)(e^{i\theta}|\psi\rangle)^\dagger = |\psi\rangle\langle\psi|$. So the density matrix removes the one part of a state vector that no experiment can see.

The pure states are the extreme points of the convex set of density matrices. If $|\psi\rangle\langle\psi| = p\sigma + (1-p)\tau$ with $0 < p < 1$, then for each $|\phi\rangle$ orthogonal to $|\psi\rangle$, $0 = p\langle\phi|\sigma|\phi\rangle + (1-p)\langle\phi|\tau|\phi\rangle$, so both terms are 0. A positive semidefinite matrix with $\langle\phi|\sigma|\phi\rangle = 0$ on the orthogonal complement of $|\psi\rangle$ is a multiple of $|\psi\rangle\langle\psi|$, and the trace makes it equal. So $\sigma = \tau = |\psi\rangle\langle\psi|$. A mixed state, with two or more nonzero eigenvalues, is a nontrivial mixture of its eigenvectors.

### One qubit

Every $2 \times 2$ density matrix has the form

$$\rho = \frac{1}{2}\left(I + r_x X + r_y Y + r_z Z\right) = \frac{1}{2}\begin{pmatrix} 1 + r_z & r_x - i r_y \\ r_x + i r_y & 1 - r_z \end{pmatrix}, \qquad |\vec r| \le 1,$$

with the [Pauli matrices](/pauli-gates/) $X, Y, Z$ and the real **Bloch vector** $\vec r = (\operatorname{Tr}\rho X, \operatorname{Tr}\rho Y, \operatorname{Tr}\rho Z)$. The matrices $I, X, Y, Z$ are a basis of the Hermitian $2 \times 2$ matrices over the reals, and $\operatorname{Tr} X = \operatorname{Tr} Y = \operatorname{Tr} Z = 0$, so the trace condition fixes the coefficient of $I$. The eigenvalues are $(1 \pm |\vec r|)/2$, so $\rho \ge 0$ exactly when $|\vec r| \le 1$. The purity is $(1 + |\vec r|^2)/2$. So pure states lie on the surface of the [Bloch sphere](/bloch-sphere/), mixed states inside it, and $I/2$ at the center.

### Qubit order

On $n$ qubits, $\rho$ is a $2^n \times 2^n$ matrix. These pages and their code number the qubits so that qubit 0 is the least significant bit of a basis index. So the space is (qubit $n-1$) $\otimes \cdots \otimes$ (qubit 0), and the matrix of $A \otimes B$ is the [Kronecker product](/kronecker-product/) with $A$ on the high-order part. Nielsen and Chuang write qubit 1 on the left as the most significant one; the matrices are then the same up to a permutation of the basis.

## Examples and non-examples

**A mixture of two non-orthogonal states.** Prepare $|0\rangle$ or $|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$, each with probability $1/2$. Then

$$\rho = \frac{1}{2}\begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} + \frac{1}{2}\begin{pmatrix} 1/2 & 1/2 \\ 1/2 & 1/2 \end{pmatrix} = \begin{pmatrix} 3/4 & 1/4 \\ 1/4 & 1/4 \end{pmatrix}.$$

Its trace is 1 and its determinant is $3/16 - 1/16 = 1/8$. The eigenvalues solve $\lambda^2 - \lambda + 1/8 = 0$, so they are $(2 \pm \sqrt 2)/4 \approx 0.8536$ and $0.1464$, which are $\cos^2(\pi/8)$ and $\sin^2(\pi/8)$. Both are positive, so $\rho$ is a density matrix. The purity is $9/16 + 1/16 + 1/16 + 1/16 = 3/4 < 1$, so $\rho$ is mixed. The Bloch vector is $(1/2, 0, 1/2)$, and indeed $(1 + 1/2)/2 = 3/4$. A measurement in the basis $|0\rangle, |1\rangle$ gives 0 with probability $\langle 0|\rho|0\rangle = 3/4$, and the average over the ensemble agrees: $\frac12 \cdot 1 + \frac12 \cdot \frac12 = 3/4$. The spectral decomposition is a second ensemble for the same $\rho$: the two orthogonal eigenvectors with probabilities $0.8536$ and $0.1464$.

**Superposition is not mixture.** The pure state $|+\rangle\langle+| = \frac12\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ and the mixture $I/2$ of $|0\rangle$ and $|1\rangle$ have the same diagonal. So a measurement in the basis $|0\rangle, |1\rangle$ gives 0 or 1 with probability $1/2$ for both. They differ in the off-diagonal entries, which are often called *coherences*. A measurement in the basis $|+\rangle, |-\rangle$ gives $+$ with probability 1 for the first and $1/2$ for the second.

**The maximally mixed state.** $I/d$ has all eigenvalues $1/d$ and purity $1/d$. The ensembles "each basis vector with probability $1/d$", for every orthonormal basis, all give $I/d$. For a qubit, the equal mixture of $|0\rangle$ and $|1\rangle$ and the equal mixture of $|+\rangle$ and $|-\rangle$ are the same state.

**A reduced state.** The Bell state $(|00\rangle + |11\rangle)/\sqrt 2$ is pure, but the state of each of its qubits is $I/2$. The computation is on [partial trace](/partial-trace/).

**Non-examples.**

- $\begin{pmatrix} 1/2 & 0.7 \\ 0.7 & 1/2 \end{pmatrix}$ is Hermitian with trace 1, but its eigenvalues are $1.2$ and $-0.2$. A diagonal with nonnegative entries does not make a matrix positive semidefinite.
- $\begin{pmatrix} 1/2 & 1/2 \\ 0 & 1/2 \end{pmatrix}$ has trace 1 and nonnegative eigenvalues ($1/2$ twice), but it is not Hermitian.
- The identity $I_2$ is positive and Hermitian, but its trace is 2. Divide by 2 to get a density matrix.
- The Bloch vector $(0.8, 0, 0.8)$ has length $1.13 > 1$, so $\frac12(I + 0.8X + 0.8Z)$ has a negative eigenvalue $(1 - 1.13)/2$.

### Common errors

- **Taking the ensemble as the state.** "The system is $|0\rangle$ or $|+\rangle$" and "the system is in the eigenbasis of $\rho$" are different stories with the same physics. Only $\rho$ has a physical meaning.
- **Mixing up a superposition and a mixture.** $(|0\rangle + |1\rangle)/\sqrt 2$ is pure; "0 or 1 with probability $1/2$" is $I/2$. Check the off-diagonal entries.
- **Checking positivity on the entries.** Positive entries do not imply a positive semidefinite matrix, and negative entries do not exclude it. Check the eigenvalues, with a tolerance in floating point.
- **Mixing the qubit orders.** A $4 \times 4$ matrix written with qubit 0 as the most significant bit is a different matrix from the same state written with qubit 0 as the least significant bit.

### Implementation

The Python code with this page builds $\rho$ from an ensemble, checks the three conditions (the smallest eigenvalue comes from a small Jacobi method in the shared helper), and computes purity, expectations, outcome probabilities, post-measurement states and Bloch vectors. Its tests compare each rule with the average over random ensembles, with fixed seeds and a tolerance of $10^{-9}$.

## Related definitions

- [Quantum state](/quantum-state/): a unit vector, for pure states only. A density matrix covers both pure and mixed states.
- [Mixed state](/mixed-state/): a density matrix that is not pure, and the ensembles that give it.
- [Partial trace](/partial-trace/): the state of one part of a composite system.
- [Quantum channel](/quantum-channel/) and [Kraus operators](/kraus-operators/): the maps from density matrices to density matrices that physics allows.
- [Trace distance](/trace-distance/) and [fidelity](/fidelity/): how close two density matrices are.
- [Von Neumann entropy](/von-neumann-entropy/): the [Shannon entropy](/shannon-entropy/) of the eigenvalues of $\rho$.
- [Quantum state tomography](/quantum-state-tomography/): estimating $\rho$ from measurements on many copies.
- [Bloch sphere](/bloch-sphere/): the picture of one-qubit density matrices as the unit ball.
- [Entanglement](/entanglement/): a pure joint state whose parts have mixed reduced density matrices.

### History

Von Neumann introduced the statistical operator of an ensemble in a 1927 paper in the Göttinger Nachrichten. Landau used a density matrix in the same year, in a paper on damping in wave mechanics.

## References
