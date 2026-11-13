---
tag: M3YVJN
kind: definition
slug: unitary-operator
name: Unitary operator
aliases:
- unitary matrix
- unitarity
area: quantum/quantum-primitives
level: intro
summary: "A unitary operator U satisfies U^dagger U = I. It keeps inner products, its eigenvalues have modulus 1, and every closed quantum evolution and every quantum gate is unitary."
prereqs: [quantum-state, eigenvalue]
see_also: [spectral-theorem, quantum-gate, bloch-sphere, hamiltonian-simulation, qr-decomposition, householder-reflections, orthogonal-transform, reversible-computation]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.1.6 (adjoints, Hermitian and unitary operators), Section 2.2.2 (the evolution postulate) and Section 4.2 (single qubit operations, Theorem 4.1 on the Z-Y decomposition)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.2.3 (unitary evolution) and Appendix A.4 (unitary matrices)
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 2 (linear algebra, unitary operators) and Chapter 3 (time evolution)
---

A *unitary operator* on a complex Hilbert space is a linear map $U$ with $U^\dagger U = I$, where $U^\dagger$ is the conjugate transpose. In finite dimension this is the same as $UU^\dagger = I$, so $U$ is invertible with $U^{-1} = U^\dagger$. Unitary matrices are exactly the linear maps that keep inner products, so they map unit vectors to unit vectors and orthonormal bases to orthonormal bases. In quantum mechanics a closed system evolves by a unitary operator, and in quantum computing every [gate](/quantum-gate/) is one.

## Definition

Let $\mathcal{H} = \mathbb{C}^d$ with the inner product $\langle u|v\rangle = \sum_k \overline{u_k}v_k$. The *adjoint* $U^\dagger$ of a $d \times d$ matrix $U$ is its conjugate transpose, $(U^\dagger)_{ij} = \overline{U_{ji}}$, which is the unique matrix with $\langle u|Uv\rangle = \langle U^\dagger u|v\rangle$ for all $u$ and $v$. A matrix $U$ is **unitary** if

$$U^\dagger U = I.$$

The unitary $d \times d$ matrices form a group under multiplication, the unitary group $U(d)$. The real unitary matrices are the orthogonal matrices, the group $O(d)$.

**Equivalent conditions.** For a $d \times d$ complex matrix $U$, these are equivalent:

1. $U^\dagger U = I$.
2. $UU^\dagger = I$. (A one-sided inverse of a square matrix is a two-sided inverse.)
3. The columns of $U$ form an orthonormal basis of $\mathbb{C}^d$. The same holds for the rows.
4. $U$ keeps inner products: $\langle Uu|Uv\rangle = \langle u|v\rangle$ for all $u, v$.
5. $U$ keeps norms: $\lVert Uv\rVert = \lVert v\rVert$ for all $v$. (Condition 4 follows from 5 by the polarization identity.)

**Spectrum.** If $U|v\rangle = \lambda|v\rangle$ with $v \ne 0$, then $\lVert v\rVert = \lVert Uv\rVert = |\lambda|\,\lVert v\rVert$, so every [eigenvalue](/eigenvalue/) has $|\lambda| = 1$, $\lambda = e^{i\theta}$. A unitary matrix is normal ($U^\dagger U = UU^\dagger$), so by the [spectral theorem](/spectral-theorem/) it has an orthonormal basis of eigenvectors: $U = \sum_k e^{i\theta_k}|v_k\rangle\langle v_k|$. Eigenvectors for different eigenvalues are orthogonal. The determinant is the product of the eigenvalues, so $|\det U| = 1$. The matrices with $\det U = 1$ form the special unitary group $SU(d)$, and $U(d) = \{e^{i\gamma}V : V \in SU(d)\}$.

**Unitaries and Hermitian matrices.** For a Hermitian matrix $H$ ($H^\dagger = H$) and a real $t$, the matrix exponential $e^{-iHt} = \sum_k (-iHt)^k/k!$ is unitary. Conversely every unitary matrix is $e^{-iH}$ for a Hermitian $H$: in the eigenbasis of $U$, take $H = -\sum_k \theta_k |v_k\rangle\langle v_k|$.

**Evolution postulate.** The state of a closed quantum system at time $t_2$ is $|\psi(t_2)\rangle = U|\psi(t_1)\rangle$ for a unitary $U$ that depends only on $t_1$ and $t_2$. For a system with the Hamiltonian $H$, constant in time, $U = e^{-iH(t_2 - t_1)/\hbar}$, the solution of the Schrödinger equation. In quantum computing the units are chosen with $\hbar = 1$, and the gates are given directly as unitary matrices.

**Consequences.** A unitary map is linear, invertible and keeps inner products, so:

- it keeps the [Born rule](/born-rule/) probabilities summing to $1$;
- it maps orthogonal states, which can be told apart with certainty, to orthogonal states;
- it cannot map two different states to one, so it cannot erase information. Classical irreversible operations such as AND must be embedded in [reversible computation](/reversible-computation/) before they can run on a quantum computer.

## Examples and non-examples

**Gates on one qubit.** The [Pauli matrices](/pauli-gates/) $X$, $Y$, $Z$, the [Hadamard gate](/hadamard-gate/) $H = \tfrac{1}{\sqrt 2}\begin{pmatrix} 1 & 1 \\ 1 & -1\end{pmatrix}$ and the [phase gates](/phase-and-t-gates/) $S = \mathrm{diag}(1, i)$ and $T = \mathrm{diag}(1, e^{i\pi/4})$ are unitary. $X$ has the eigenvalues $1$ and $-1$ with the eigenvectors $|+\rangle$ and $|-\rangle$. $T$ has the eigenvalues $1$ and $e^{i\pi/4}$.

**Rotations.** $R_z(\theta) = e^{-i\theta Z/2} = \mathrm{diag}(e^{-i\theta/2}, e^{i\theta/2})$ and $R_y(\theta) = e^{-i\theta Y/2} = \begin{pmatrix} \cos\frac{\theta}{2} & -\sin\frac{\theta}{2} \\ \sin\frac{\theta}{2} & \cos\frac{\theta}{2}\end{pmatrix}$ are unitary, with determinant $1$. On the [Bloch sphere](/bloch-sphere/) they are rotations by $\theta$ about the $z$ and $y$ axes.

**The Z-Y decomposition.** Every $2 \times 2$ unitary is

$$U = e^{i\alpha} R_z(\beta) R_y(\gamma) R_z(\delta)$$

for real $\alpha, \beta, \gamma, \delta$ (Nielsen and Chuang, Theorem 4.1). To find them, take $\alpha = \tfrac{1}{2}\arg\det U$. Then $e^{-i\alpha}U = \begin{pmatrix} a & -\bar b \\ b & \bar a\end{pmatrix}$ with $|a|^2 + |b|^2 = 1$, and $\gamma = 2\arctan(|b|/|a|)$, $\beta = \arg b - \arg a$, $\delta = -\arg a - \arg b$. When $a = 0$ or $b = 0$ one of $\beta, \delta$ is free.

**Permutation matrices.** A permutation of the basis states, such as the [CNOT gate](/cnot-gate/) $|a, b\rangle \mapsto |a, a \oplus b\rangle$ or the Toffoli gate, is a real unitary matrix. These are the classical reversible gates.

**Matrices from numerical linear algebra.** [Householder reflections](/householder-reflections/) $I - 2|v\rangle\langle v|$ for a unit $v$ and [Givens rotations](/givens-rotations/) are unitary. The [QR decomposition](/qr-decomposition/) writes a matrix as a unitary times an upper triangular matrix, and the DFT matrix divided by $\sqrt{d}$ is unitary ([quantum Fourier transform](/quantum-fourier-transform/)).

**Non-example: an invertible matrix that is not unitary.** $\begin{pmatrix} 1 & 1 \\ 0 & 1\end{pmatrix}$ is invertible with determinant $1$, but it maps the unit vector $|1\rangle$ to $|0\rangle + |1\rangle$, of norm $\sqrt 2$.

**Non-example: a projector.** $|0\rangle\langle 0| = \mathrm{diag}(1, 0)$ is Hermitian but not unitary: it maps $|1\rangle$ to $0$. A [quantum measurement](/quantum-measurement/) is described by projectors and is not a unitary operation.

**Non-example: $2I$.** It keeps orthogonality but scales the norm by $2$. Only the scalars $e^{i\gamma}I$ are unitary, and they are global phases.

### Common errors

- Writing $U^T$ for $U^{-1}$. The inverse is the conjugate transpose $U^\dagger$; the transpose is enough only for real matrices.
- Testing only $U^\dagger U = I$ for a non-square matrix. A $D \times d$ matrix $V$ with $D > d$ and $V^\dagger V = I$ is an *isometry*, not a unitary; it is the kind of map that adds [ancilla qubits](/ancilla-qubits/).
- Comparing gates exactly. $U$ and $e^{i\gamma}U$ are the same gate as an operation on states, although they are different matrices; and in floating point a test of $U^\dagger U = I$ needs a tolerance.

### Implementation

The file `impl/python/unitary_operator.py` has the $2 \times 2$ eigenvalues from the characteristic polynomial, the closed form $e^{i(cI + r\,\hat n\cdot\vec\sigma)} = e^{ic}(\cos r\,I + i\sin r\,\hat n\cdot\vec\sigma)$, the Z-Y decomposition and a random unitary by Gram-Schmidt on complex Gaussian columns. The tests check that the eigenvalues and the determinant of 200 random unitaries have modulus $1$, that inner products are kept in dimensions $2$, $4$ and $8$, that the closed-form exponential agrees with 40 terms of the Taylor series, and that the Z-Y decomposition gives back each of 106 matrices, with fixed seeds.

## Related definitions

- [Quantum gate](/quantum-gate/): a unitary on a small number of qubits, used as a building block.
- [Spectral theorem](/spectral-theorem/): the eigenbasis of a normal matrix, which gives $U = e^{-iH}$.
- [Hamiltonian simulation](/hamiltonian-simulation/): the task of building the unitary $e^{-iHt}$ from gates.
- [Quantum channel](/quantum-channel/): the general evolution of an open system, which contains the unitary maps $\rho \mapsto U\rho U^\dagger$ as a special case.
- [Orthogonal transform](/orthogonal-transform/): the real case, used in signal compression.

## References
