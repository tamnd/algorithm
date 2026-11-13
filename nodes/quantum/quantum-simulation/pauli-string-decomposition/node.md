---
tag: SAG9RR
kind: definition
slug: pauli-string-decomposition
name: Pauli string decomposition
aliases:
- Pauli decomposition
- Pauli expansion
area: quantum/quantum-simulation
level: advanced
summary: "Write a 2^n x 2^n matrix as a sum of the 4^n tensor products of I, X, Y, Z with coefficients c_P = Tr(P M)/2^n. The coefficients are real exactly when the matrix is Hermitian."
prereqs: [pauli-gates, tensor-product]
see_also: [hamiltonian-simulation, kronecker-product, fast-walsh-hadamard-transform, clifford-group, jordan-wigner-transformation, linear-combination-of-unitaries, qdrift, trotter-suzuki-product-formulas]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.1.3 (the Pauli matrices) and Section 10.5.1 (the Pauli group in the stabilizer formalism)
  - paper: arxiv:quant-ph/9705052
    title: Daniel Gottesman, Stabilizer Codes and Quantum Error Correction, PhD thesis, California Institute of Technology, 1997
    locator: the chapter on the stabilizer formalism, the Pauli group and the commutation of Pauli operators
  - paper: doi:10.1103/PhysRevLett.123.070503
    title: Earl Campbell, Random compiler for fast Hamiltonian simulation, Physical Review Letters 123(7), 2019, article 070503 (arXiv:1811.08017)
    locator: the Hamiltonian as a weighted sum of Pauli terms and the coefficient sum lambda
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 9 (Hamiltonian simulation), Hamiltonians written as sums of Pauli terms
---

A Pauli string decomposition writes a $2^n \times 2^n$ matrix $M$ as a linear combination of the $4^n$ Pauli strings on $n$ qubits, $M = \sum_P c_P P$, with $c_P = \mathrm{Tr}(PM)/2^n$. Every matrix has exactly one such decomposition, because the Pauli strings form an orthogonal basis of the space of matrices. The coefficients are real exactly when $M$ is Hermitian. In quantum simulation this is the standard input format of a Hamiltonian, the Pauli list access model of [Hamiltonian simulation](/hamiltonian-simulation/): physical Hamiltonians have few terms, product formulas exponentiate one term at a time, and the coefficient sum $\lambda = \sum_P |c_P|$ sets the cost of [qDRIFT](/qdrift/) and of [linear combination of unitaries](/linear-combination-of-unitaries/) methods.

## Definition

**Pauli matrices.** The four $2 \times 2$ matrices are
$$I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$
(see [Pauli gates](/pauli-gates/)). They are Hermitian and unitary, they square to $I$, and $\mathrm{Tr}(\sigma_a \sigma_b) = 2\,\delta_{ab}$ for $\sigma_a, \sigma_b \in \{I, X, Y, Z\}$.

**Pauli strings.** An $n$-qubit Pauli string is a [tensor product](/tensor-product/) $P = \sigma_{n-1} \otimes \cdots \otimes \sigma_1 \otimes \sigma_0$ with each $\sigma_q \in \{I, X, Y, Z\}$, written as a word of $n$ letters, for example $XIZ$. The encyclopedia puts qubit 0 at the right end of a ket (see [quantum state](/quantum-state/)), so the last letter of the word acts on qubit 0 and the first letter on qubit $n-1$; the word is then also the order of the factors in the [Kronecker product](/kronecker-product/) of the matrices. The *weight* of $P$ is the number of letters that are not $I$.

**Orthogonality.** For Pauli strings $P$ and $Q$,
$$\mathrm{Tr}(P Q) = 2^n \, \delta_{PQ}.$$
*Proof.* The trace of a tensor product is the product of the traces, so $\mathrm{Tr}(PQ) = \prod_q \mathrm{Tr}(\sigma_q \sigma'_q)$, and each factor is $2$ if the letters agree and $0$ if they differ. $\square$

So the $4^n$ strings are orthogonal for the inner product $\langle A, B\rangle = \mathrm{Tr}(A^\dagger B)$ (each $P$ is Hermitian). They are $4^n$ linearly independent elements of a space of dimension $4^n$, so they are a basis.

**The decomposition.** Every complex $2^n \times 2^n$ matrix $M$ has exactly one expansion
$$M = \sum_{P} c_P \, P, \qquad c_P = \frac{\mathrm{Tr}(P M)}{2^n},$$
where the sum is over all $4^n$ Pauli strings. The formula for $c_P$ follows by multiplying the expansion by $P$ and taking the trace.

**Properties.**

- *Hermitian means real.* $M$ is Hermitian if and only if every $c_P$ is real. If $M = M^\dagger$, then $\overline{\mathrm{Tr}(PM)} = \mathrm{Tr}((PM)^\dagger) = \mathrm{Tr}(MP) = \mathrm{Tr}(PM)$. Conversely, a real combination of Hermitian matrices is Hermitian.
- *Trace.* $c_{I\cdots I} = \mathrm{Tr}(M)/2^n$. The identity term only shifts the spectrum, and in $e^{-iHt}$ it is a global phase.
- *Parseval.* $\sum_P |c_P|^2 = \|M\|_F^2 / 2^n$, where $\|\cdot\|_F$ is the Frobenius norm, by orthogonality.
- *Norm bounds.* $\max_P |c_P| \le \|M\| \le \lambda$, with $\lambda = \sum_P |c_P|$ and $\|\cdot\|$ the spectral norm. The right side holds because each $\|P\| = 1$, and the left side because $|\mathrm{Tr}(PM)| \le 2^n \|PM\| = 2^n\|M\|$.
- *Commutation.* Two strings either commute or anticommute. They anticommute exactly when the number of positions where both letters are non-identity and different is odd, since two different non-identity one-qubit Pauli matrices anticommute. For anticommuting $P$ and $Q$, $\|[P, Q]\| = \|2PQ\| = 2$. These numbers give the commutator constants of the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/).

**Computing the coefficients.** Each Pauli string has exactly one nonzero entry in each row, so each trace $\mathrm{Tr}(PM)$ takes $O(2^n)$ operations, and all $4^n$ coefficients take $O(8^n)$ by the direct formula. A faster method takes $O(n\, 4^n)$. Write each string as $P = i^{|a \wedge b|} X^a Z^b$, where $a$ and $b$ are $n$-bit masks of the $X$ part and the $Z$ part, and $Y = iXZ$ supplies the phase. The nonzero entries of $X^a Z^b$ are at $(y \oplus a, y)$, with value $(-1)^{b \cdot y}$. So
$$\mathrm{Tr}(X^a Z^b M) = (-1)^{a \cdot b} \sum_{y} (-1)^{b \cdot y} M_{y \oplus a,\, y},$$
and for a fixed $a$ the sums for all $b$ are one [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) of the vector $y \mapsto M_{y \oplus a, y}$, which costs $O(n 2^n)$. There are $2^n$ masks $a$. The page's simulator uses this method and checks it against the direct traces and the round trip $\sum_P c_P P = M$ on random complex matrices of 1 to 3 qubits.

## Examples and non-examples

**A $2 \times 2$ Hermitian matrix.** For $M = \begin{pmatrix} a & b \\ \bar b & d \end{pmatrix}$ with real $a$ and $d$, the four traces give
$$c_I = \frac{a + d}{2}, \quad c_Z = \frac{a - d}{2}, \quad c_X = \mathrm{Re}\, b, \quad c_Y = -\mathrm{Im}\, b.$$
For $M = \begin{pmatrix} 2 & 1 - i \\ 1 + i & 0 \end{pmatrix}$ this is $M = I + X + Y + Z$. Check: $I + Z = \mathrm{diag}(2, 0)$ and $X + Y$ has $1 - i$ above the diagonal and $1 + i$ below it. Here $\lambda = 4$, while the eigenvalues of $M$ are $1 \pm \sqrt3$, so $\|M\| = 2.732$.

**The SWAP gate.** $\mathrm{SWAP} = \tfrac12 (II + XX + YY + ZZ)$. So the Heisenberg coupling is $XX + YY + ZZ = 2\,\mathrm{SWAP} - II$, with eigenvalue $1$ on the three symmetric states and $-3$ on the singlet $(|01\rangle - |10\rangle)/\sqrt2$.

**The CNOT gate.** With qubit 1 (the first letter) as the control and qubit 0 as the target,
$$\mathrm{CNOT} = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes X = \tfrac12 (II + ZI + IX - ZX),$$
since $|0\rangle\langle 0| = (I + Z)/2$ and $|1\rangle\langle 1| = (I - Z)/2$. The coefficients are real because CNOT is Hermitian as well as unitary.

**A non-Hermitian matrix.** $|0\rangle\langle 1| = \begin{pmatrix} 0 & 1 \\ 0 & 0\end{pmatrix} = \tfrac12 (X + iY)$. The coefficient of $Y$ is imaginary, as it must be for a matrix that is not Hermitian. Fermion operators under the [Jordan-Wigner transformation](/jordan-wigner-transformation/) have this form, with a string of $Z$ letters in front.

**A projector with many terms.** $|0 \cdots 0\rangle\langle 0 \cdots 0| = ((I + Z)/2)^{\otimes n}$ has $2^n$ terms, all the strings made of $I$ and $Z$, each with coefficient $2^{-n}$. Its norm is 1 and $\lambda = 1$, but the number of terms is exponential. So a short description of a matrix does not mean a short Pauli list.

**A dense random matrix.** A random $8 \times 8$ Hermitian matrix with entries uniform in $[-1, 1]$ (real and imaginary parts, seed 4 in the simulator) has all 64 coefficients nonzero, $\lambda = 14.55$, $\|M\| = 3.29$ and $\max_P |c_P| = 0.565$. The coefficient sum $\lambda$ can be much larger than the norm, and this is the price that $\lambda$-based methods pay.

**Local Hamiltonians.** A Hamiltonian whose terms each act on at most $k$ qubits has only strings of weight at most $k$. On $n$ qubits there are $\sum_{w=0}^{k} \binom{n}{w} 3^w$ of them: 436 for $n = 10$ and $k = 2$, out of $4^{10} = 1\,048\,576$. The transverse-field Ising chain $\sum_i Z_i Z_{i+1} + h \sum_i X_i$ has $2n - 1$ terms.

**A non-example: a product of Pauli strings is not a sum.** $XX \cdot ZZ = (XZ) \otimes (XZ) = (-iY) \otimes (-iY) = -YY$ is one string with a phase, not a sum of strings. The set of strings with phases $\pm 1, \pm i$ is closed under products and forms the Pauli group; the decomposition is about sums.

## Related definitions

- **The Pauli group.** The strings with phases $\{\pm 1, \pm i\}$ form a group of order $4^{n+1}$ under matrix product. It is the base of the stabilizer formalism. The [Clifford group](/clifford-group/) is the set of unitaries that map Pauli strings to Pauli strings under conjugation, so it maps a Pauli decomposition to another one with the same coefficients up to signs and a permutation of the strings.
- **Locality and weight.** A $k$-local Hamiltonian is a sum of strings of weight at most $k$. The weight sets the gate cost of $e^{-i\theta P}$: $2(w-1)$ CNOT gates and one rotation (see [digital quantum simulation](/digital-quantum-simulation/)).
- **The coefficient sum.** $\lambda = \sum_P |c_P|$ is the normalization of the block encoding built by [linear combination of unitaries](/linear-combination-of-unitaries/), and the sampling scale of [qDRIFT](/qdrift/).
- **Walsh functions.** The diagonal strings, made of $I$ and $Z$ only, are the diagonal matrices of the characters $x \mapsto (-1)^{b \cdot x}$. So the Pauli decomposition of a diagonal matrix is its [Walsh-Hadamard transform](/walsh-hadamard-transform/), divided by $2^n$.
- **Fermion-to-qubit mappings.** A [fermion-to-qubit mapping](/fermion-to-qubit-mapping/) turns a fermionic Hamiltonian into a Pauli list. The weight of the strings depends on the mapping.

## References
