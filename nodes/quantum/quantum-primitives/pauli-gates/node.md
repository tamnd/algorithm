---
tag: KXAV0B
kind: definition
slug: pauli-gates
name: Pauli gates
aliases:
- X gate
- Y gate
- Z gate
- bit flip
- phase flip
area: quantum/quantum-primitives
level: intro
summary: "The Pauli gates X, Y and Z are the one-qubit gates of the Pauli matrices. They are Hermitian and unitary, square to I, anticommute in pairs, and satisfy XY = iZ."
prereqs: [quantum-gate]
see_also: [pauli-string-decomposition, clifford-group, stabilizer-formalism, bloch-sphere, quantum-error-correction, hadamard-gate, gottesman-knill-theorem, quantum-channel]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.3.1 (single qubit gates), Section 2.1.3 (the Pauli matrices), Section 4.2 (rotation operators) and Section 10.5.1 (the Pauli group)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.4 (elementary gates) and Appendix A.9 (Pauli matrices)
  - paper: doi:10.1007/BF01397326
    title: Wolfgang Pauli, Zur Quantenmechanik des magnetischen Elektrons, Zeitschrift für Physik 43, 1927, pages 601 to 623
    locator: the 2 x 2 spin matrices
---

The *Pauli gates* are the one-qubit gates given by the three Pauli matrices

$$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \qquad Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \qquad Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}.$$

$X$ exchanges $|0\rangle$ and $|1\rangle$, like a classical NOT. $Z$ multiplies $|1\rangle$ by $-1$ and so changes only the relative phase. $Y = iXZ$ does both. The three matrices are Hermitian and unitary, each squares to the identity, two different ones anticommute, and $XY = iZ$. Together with $I$ they form a basis of the $2 \times 2$ complex matrices, which is why every one-qubit operator and every one-qubit error can be written in terms of them.

## Definition

The **Pauli matrices** are $\sigma_0 = I$, $\sigma_1 = X$, $\sigma_2 = Y$ and $\sigma_3 = Z$ as above; physics texts also write $\sigma_x, \sigma_y, \sigma_z$. The **Pauli gates** are the [quantum gates](/quantum-gate/) $X$, $Y$ and $Z$ on one qubit. On the basis states, for $b \in \{0, 1\}$,

$$X|b\rangle = |1 - b\rangle, \qquad Z|b\rangle = (-1)^b|b\rangle, \qquad Y|b\rangle = i(-1)^b|1 - b\rangle.$$

**Algebraic properties.** For $P, Q \in \{X, Y, Z\}$:

1. $P^\dagger = P$ (Hermitian) and $P^\dagger P = I$ ([unitary](/unitary-operator/)). So $P^2 = I$ and $P^{-1} = P$.
2. $\operatorname{tr} P = 0$ and $\det P = -1$. The eigenvalues are $+1$ and $-1$.
3. For $P \ne Q$, $PQ = -QP$: two different Pauli matrices anticommute.
4. $XY = iZ$, $YZ = iX$ and $ZX = iY$; reversing the order changes the sign. So $XYZ = iI$. In one formula, $\sigma_j\sigma_k = \delta_{jk}I + i\sum_l \epsilon_{jkl}\sigma_l$ for $j, k, l \in \{1, 2, 3\}$, with the Levi-Civita symbol $\epsilon$.

**Eigenvectors.**

| matrix | eigenvalue $+1$ | eigenvalue $-1$ |
|---|---|---|
| $X$ | $\lvert +\rangle = (\lvert 0\rangle + \lvert 1\rangle)/\sqrt 2$ | $\lvert -\rangle = (\lvert 0\rangle - \lvert 1\rangle)/\sqrt 2$ |
| $Y$ | $\lvert {+i}\rangle = (\lvert 0\rangle + i\lvert 1\rangle)/\sqrt 2$ | $\lvert {-i}\rangle = (\lvert 0\rangle - i\lvert 1\rangle)/\sqrt 2$ |
| $Z$ | $\lvert 0\rangle$ | $\lvert 1\rangle$ |

These six states are the points $\pm x$, $\pm y$, $\pm z$ of the [Bloch sphere](/bloch-sphere/), and as measurements the three matrices are the measurements in the three bases.

**The Pauli basis.** The four matrices $I, X, Y, Z$ are orthogonal for the inner product $\langle A, B\rangle = \operatorname{tr}(A^\dagger B)$, with $\operatorname{tr}(P^\dagger Q) = 2\delta_{PQ}$. So every $2 \times 2$ complex matrix $M$ is

$$M = \sum_{P \in \{I, X, Y, Z\}} c_P\,P, \qquad c_P = \tfrac{1}{2}\operatorname{tr}(PM),$$

and $M$ is Hermitian exactly when all four $c_P$ are real. A one-qubit density matrix is $\tfrac{1}{2}(I + r_x X + r_y Y + r_z Z)$ with the Bloch vector $\vec r$.

**Rotations.** Since $P^2 = I$, $e^{-i\theta P/2} = \cos\tfrac{\theta}{2}I - i\sin\tfrac{\theta}{2}P$. These are the rotations $R_x(\theta)$, $R_y(\theta)$, $R_z(\theta)$ of the Bloch sphere about the three axes. In particular $P = iR_P(\pi)$: each Pauli gate is a half turn, up to a global phase.

**Pauli strings and the Pauli group.** A Pauli string on $n$ qubits is a tensor product $P_{n-1} \otimes \cdots \otimes P_1 \otimes P_0$ with each $P_j \in \{I, X, Y, Z\}$, written as a word such as $XIZ$ in which the rightmost letter acts on qubit $0$, as in a ket. The $4^n$ strings are an orthogonal basis of the $2^n \times 2^n$ matrices ([Pauli string decomposition](/pauli-string-decomposition/)). Two strings commute if the number of positions where both letters differ and neither is $I$ is even, and they anticommute otherwise. The strings with the phases $\pm 1, \pm i$ form the *Pauli group* $\mathcal{P}_n$, with $4 \cdot 4^n$ elements; on one qubit it has the 16 elements $\{\pm 1, \pm i\} \times \{I, X, Y, Z\}$.

## Examples and non-examples

**X is NOT.** $X$ on qubit $j$ of an $n$-qubit register maps $|x\rangle$ to $|x \oplus 2^j\rangle$, the basis state with bit $j$ inverted. On a superposition it acts term by term: $X(\alpha|0\rangle + \beta|1\rangle) = \beta|0\rangle + \alpha|1\rangle$.

**Z changes only the relative phase.** $Z|+\rangle = |-\rangle$ and $Z|-\rangle = |+\rangle$. A measurement in the computational basis gives the same probabilities before and after $Z$; a measurement in the basis $|\pm\rangle$ tells the two apart.

**Products.** $XZ = -iY$, so $XZ$ and $Y$ differ by a global phase and act in the same way on states. $ZXZ = -X$ is the anticommutation $ZX = -XZ$ multiplied on the right by $Z$.

**Two-qubit strings.** $X \otimes X$ and $Z \otimes Z$ commute, because they differ in two positions. $X \otimes I$ and $Z \otimes Z$ anticommute, because they differ, with both letters not $I$, in one position only. $XX$ and $ZZ$ are the stabilizers of the [Bell state](/bell-states/) $(|00\rangle + |11\rangle)/\sqrt 2$: each maps it to itself.

**Conjugation by Hadamard.** $HXH = Z$, $HZH = X$ and $HYH = -Y$ ([Hadamard gate](/hadamard-gate/)). Gates that map Pauli strings to Pauli strings under conjugation form the [Clifford group](/clifford-group/).

**Non-example: the Hadamard gate.** $H = (X + Z)/\sqrt 2$ is Hermitian and unitary and squares to $I$, but it is not a Pauli matrix and not in the Pauli group. It is a sum of two Pauli matrices.

**Non-example: $\sqrt{X}$.** The matrix $\tfrac{1}{2}\begin{pmatrix} 1 + i & 1 - i \\ 1 - i & 1 + i \end{pmatrix}$ squares to $X$. It is unitary but not Hermitian and is not in the Pauli group.

### Common errors

- The sign of $Y$. With $Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$, $Y|0\rangle = i|1\rangle$. Some texts use $iY = ZX$, a real matrix, and call it $Y$; check which one a source means.
- Reading a Pauli string from the wrong end. Here $XZ$ means $X$ on qubit $1$ and $Z$ on qubit $0$, the matrix $X \otimes Z$. It maps $|01\rangle$ to $-|11\rangle$.
- Treating $X$ and $Z$ as commuting. They anticommute, so $XZ = -ZX$; the phase matters when the product controls another gate.

### Implementation

The file `impl/python/pauli_gates.py` has the four matrices, the multiplication table with phases, the decomposition $c_P = \tfrac{1}{2}\operatorname{tr}(PM)$, the matrix of a Pauli string and the commutation rule for strings. The tests check that $X$, $Y$, $Z$ are Hermitian, unitary, square to $I$ and have trace $0$, that every product in the table equals the matrix product, the anticommutation of every pair, $XY = iZ$, $YZ = iX$, $ZX = iY$, the eigenvectors in the table above, the decomposition of 50 random matrices with a fixed seed, the commutation rule against the matrices for all 256 pairs of two-qubit strings, and that the one-qubit Pauli group has 16 elements and is closed.

## Related definitions

- [Pauli string decomposition](/pauli-string-decomposition/): writing an operator on $n$ qubits in the basis of Pauli strings.
- [Clifford group](/clifford-group/) and [stabilizer formalism](/stabilizer-formalism/): gates and states described by how they act on Pauli strings; the [Gottesman-Knill theorem](/gottesman-knill-theorem/) is about their efficient simulation.
- [Quantum error correction](/quantum-error-correction/): an error on one qubit is a combination of $I$, $X$, $Y$ and $Z$, so a code that corrects these three on each qubit corrects every one-qubit error.
- [Quantum channel](/quantum-channel/): the Pauli channels apply $X$, $Y$ or $Z$ at random.
- [Bloch sphere](/bloch-sphere/): the Pauli expectations are the coordinates of a state.

### History

Pauli introduced the three $2 \times 2$ matrices in 1927 to describe the spin of the electron.

## References
