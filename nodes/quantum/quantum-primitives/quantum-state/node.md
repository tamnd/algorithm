---
tag: WTP45P
kind: definition
slug: quantum-state
name: Quantum state
aliases:
- state vector
- ket
area: quantum/quantum-primitives
level: intro
summary: "A pure quantum state is a unit vector in a complex Hilbert space, up to a global phase. On n qubits it is a vector of 2^n amplitudes, and qubit 0 is the least significant bit."
prereqs: [qubit]
see_also: [tensor-product, density-matrix, mixed-state, entanglement, born-rule, unitary-operator, quantum-superposition, row-major-order]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.2.1 (multiple qubits), Section 2.1 (linear algebra and Dirac notation), Section 2.2.1 (the state space postulate) and Section 2.2.8 (composite systems)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.2.1 (superposition), Section 1.3 (qubits and quantum memory) and Appendix A.10 (Dirac notation)
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 2 (linear algebra and the Dirac notation) and Chapter 3 (qubits and the framework of quantum mechanics)
  - paper: doi:10.1017/S0305004100021162
    title: P. A. M. Dirac, A new notation for quantum mechanics, Mathematical Proceedings of the Cambridge Philosophical Society 35(3), 1939, pages 416 to 418
    locator: the bra and ket notation
---

A *pure quantum state* of a system is a unit vector in the complex Hilbert space of the system, where two vectors that differ by a factor $e^{i\gamma}$ are the same state. For $n$ [qubits](/qubit/) the space is $(\mathbb{C}^2)^{\otimes n} \cong \mathbb{C}^{2^n}$, so a state is a list of $2^n$ complex amplitudes, one for each $n$-bit string. This page also fixes the qubit order that all quantum pages of this encyclopedia use: qubit $j$ is bit $j$ of the basis index, so qubit $0$ is the least significant bit and the rightmost symbol of a ket. A pure state is also called a *state vector*; general states, which include probabilistic mixtures, are [density matrices](/density-matrix/).

## Definition

**Hilbert space.** In quantum computing a *Hilbert space* is a finite-dimensional complex vector space $\mathcal{H} \cong \mathbb{C}^d$ with the inner product $\langle u|v\rangle = \sum_k \overline{u_k} v_k$, which is linear in the second argument and conjugate-linear in the first. The norm is $\lVert v \rVert = \sqrt{\langle v|v\rangle}$. Infinite-dimensional spaces appear in physics, for example for the position of a particle, but they are not needed here.

**Dirac notation.** A vector $v \in \mathcal{H}$ is written as a *ket* $|v\rangle$, a column. The *bra* $\langle v|$ is the conjugate transpose of $|v\rangle$, a row. The product of a bra and a ket is the inner product $\langle u|v\rangle$, a number. The product of a ket and a bra is the *outer product* $|u\rangle\langle v|$, a $d \times d$ matrix with $(|u\rangle\langle v|)\,|w\rangle = \langle v|w\rangle\,|u\rangle$. For a matrix $A$, the number $\langle u|A|v\rangle$ is $\langle u|(A|v\rangle)$.

**Pure state.** A pure state of a system with Hilbert space $\mathcal{H}$ is a vector $|\psi\rangle \in \mathcal{H}$ with $\langle\psi|\psi\rangle = 1$. Two unit vectors $|\psi\rangle$ and $|\phi\rangle$ are the same state when $|\phi\rangle = e^{i\gamma}|\psi\rangle$ for a real $\gamma$, which holds if and only if $|\langle\phi|\psi\rangle| = 1$. No measurement and no evolution can detect a global phase: the [qubit](/qubit/) page gives the argument. Given an orthonormal basis $|e_0\rangle, \dots, |e_{d-1}\rangle$, the state is $|\psi\rangle = \sum_k \alpha_k |e_k\rangle$ with $\alpha_k = \langle e_k|\psi\rangle$ and $\sum_k |\alpha_k|^2 = 1$. The numbers $\alpha_k$ are the *amplitudes* in that basis. A pure state of $\mathbb{C}^d$ has $2d - 2$ real parameters: $2d$ real numbers, less one for the norm and one for the global phase.

**States of n qubits.** The state space of $n$ qubits is the [tensor product](/tensor-product/) of $n$ copies of $\mathbb{C}^2$, of dimension $2^n$. Its *computational basis* has one vector $|x\rangle$ for each $x \in \{0, 1, \dots, 2^n - 1\}$, and a state is

$$|\psi\rangle = \sum_{x=0}^{2^n - 1} \alpha_x |x\rangle, \qquad \sum_x |\alpha_x|^2 = 1.$$

A computer stores it as an array of $2^n$ complex numbers, with $\alpha_x$ at position $x$. At 16 bytes for each complex number, 20 qubits take 16 MiB and 30 qubits take 16 GiB. This exponential size is why a classical simulation of a general $n$-qubit computation is expensive, and why [Feynman](/feynman-quantum-simulation/) proposed quantum computers.

### The qubit order convention

The quantum pages of this encyclopedia number the $n$ qubits $0, 1, \dots, n-1$. A basis state is written $|b_{n-1} \cdots b_1 b_0\rangle$, where $b_j \in \{0, 1\}$ is the value of qubit $j$. Then:

1. The string $b_{n-1} \cdots b_0$ is the binary numeral of $x = \sum_{j=0}^{n-1} b_j 2^j$, and $|b_{n-1} \cdots b_0\rangle$ and $|x\rangle$ are the same vector. Qubit $0$ is the least significant bit and the rightmost symbol. Qubit $n-1$ is the most significant bit and the leftmost symbol.
2. $|b_{n-1} \cdots b_0\rangle = |b_{n-1}\rangle \otimes \cdots \otimes |b_1\rangle \otimes |b_0\rangle$. Qubit $n-1$ is the leftmost tensor factor. With the [Kronecker product](/kronecker-product/), the left factor indexes the high-order bits, so the column vector of this product has its $1$ at position $x$.
3. A one-qubit gate $U$ on qubit $j$ is the matrix $I^{\otimes(n-1-j)} \otimes U \otimes I^{\otimes j}$, where $I$ is the $2 \times 2$ identity. In particular $U \otimes V$ applies $V$ to qubit $0$ and $U$ to qubit $1$.
4. Two registers written $|x\rangle|y\rangle$ or $|x, y\rangle$, with $y$ on $k$ qubits, form the basis state with index $x \cdot 2^k + y$. The first register holds the high-order qubits.
5. A two-qubit matrix in the basis order $|00\rangle, |01\rangle, |10\rangle, |11\rangle$ has its left symbol on the higher-numbered qubit. So the usual [CNOT](/cnot-gate/) matrix has its control on the left symbol.

Nielsen and Chuang number the qubits $1$ to $n$ from the left. Their qubit $k$ is qubit $n - k$ here. The kets, the matrices and the order of the tensor factors are the same in both conventions; only the numbers of the qubits differ. Some software packages use the convention of this page, and others use the left-to-right one; a page that compares results with such a package must say which order the package uses.

**Example.** On three qubits, $|110\rangle = |6\rangle$, with qubit $2$ and qubit $1$ equal to $1$ and qubit $0$ equal to $0$. The gate $X$ on qubit $0$ maps it to $|111\rangle = |7\rangle$, and $X$ on qubit $2$ maps it to $|010\rangle = |2\rangle$. In general $X$ on qubit $j$ maps $|x\rangle$ to $|x \oplus 2^j\rangle$.

### What the state determines

The state determines the probability of every measurement outcome, by the [Born rule](/born-rule/): a measurement in the computational basis gives $x$ with probability $|\alpha_x|^2$. A closed system evolves by a [unitary operator](/unitary-operator/), $|\psi\rangle \mapsto U|\psi\rangle$. The amplitudes themselves cannot be read out: each measurement returns one outcome and changes the state ([quantum measurement](/quantum-measurement/)).

## Examples and non-examples

**A two-qubit state with all four amplitudes.** The vector

$$|\psi\rangle = \tfrac{1}{2}|00\rangle + \tfrac{i}{2}|01\rangle - \tfrac{1}{2}|10\rangle - \tfrac{i}{2}|11\rangle$$

has the amplitude list $(\tfrac{1}{2}, \tfrac{i}{2}, -\tfrac{1}{2}, -\tfrac{i}{2})$ at the positions $0, 1, 2, 3$, and $4 \cdot \tfrac{1}{4} = 1$. It is the product $|-\rangle \otimes |{+i}\rangle$ with $|-\rangle = (|0\rangle - |1\rangle)/\sqrt{2}$ on qubit $1$ and $|{+i}\rangle = (|0\rangle + i|1\rangle)/\sqrt{2}$ on qubit $0$, as the product of the two factors gives the four amplitudes above.

**An entangled state.** The GHZ state $(|000\rangle + |111\rangle)/\sqrt{2}$ has two nonzero amplitudes, at the positions $0$ and $7$. It is not a tensor product of three one-qubit states ([entanglement](/entanglement/)). Its overlap with $|000\rangle$ is $|\langle 000|\mathrm{GHZ}\rangle|^2 = \tfrac{1}{2}$.

**The uniform superposition.** The state $2^{-n/2} \sum_x |x\rangle$ has all $2^n$ amplitudes equal. The [Hadamard gate](/hadamard-gate/) on each qubit maps $|0 \cdots 0\rangle$ to it.

**Non-example: phases on each amplitude.** The vectors $(|00\rangle + |11\rangle)/\sqrt{2}$ and $(|00\rangle - |11\rangle)/\sqrt{2}$ differ only in the sign of one amplitude, but they are orthogonal, so they are different states. Only a common factor on all amplitudes is a global phase.

**Non-example: a mixture.** "The state $|00\rangle$ with probability $\tfrac{1}{2}$ and $|11\rangle$ with probability $\tfrac{1}{2}$" is not a unit vector. It is the [mixed state](/mixed-state/) with density matrix $\tfrac{1}{2}(|00\rangle\langle 00| + |11\rangle\langle 11|)$. It is not the state $(|00\rangle + |11\rangle)/\sqrt{2}$, which a measurement in the basis $|+\rangle, |-\rangle$ on each qubit tells apart. The alias "state vector" names pure states only.

**Non-example: the zero vector and unnormalized vectors.** The zero vector is not a state. A nonzero vector $v$ that is not a unit vector names the state $v / \lVert v \rVert$, but formulas such as the Born rule assume a unit vector.

### Common errors

- Mixing qubit orders. Code that puts qubit $0$ on the left reads $|110\rangle$ as qubit $0 = 1$, qubit $1 = 1$, qubit $2 = 0$. A circuit then gives a permuted output. Each page and each program must state its order, and this encyclopedia uses the order above.
- Reading "ket" as the state. A ket is a notation for a vector; the state is the ray of the vector.
- Treating the amplitudes as readable data. Estimating the probability $|\alpha_x|^2$ to error $\varepsilon$ needs about $1/\varepsilon^2$ measurements of fresh copies, and the phase of $\alpha_x$ needs other measurements ([quantum state tomography](/quantum-state-tomography/)).

### Implementation

The file `impl/python/quantum_state.py` stores a state as a list of $2^n$ complex numbers in the order above. It converts between an index and a label (`ket_label(3, 6)` is `"|110>"`), reads the value of qubit $j$ as bit $j$ of the index, builds a state from a table of labels and amplitudes, and tests two unit vectors for equality up to a global phase. Its tests check, for every basis state on 1 to 4 qubits and every qubit $j$, that the simulator gate $X$ on qubit $j$ maps $|x\rangle$ to $|x \oplus 2^j\rangle$.

## Related definitions

- [Qubit](/qubit/): the one-qubit case, with global and relative phase.
- [Tensor product](/tensor-product/): how the spaces of several systems combine, and product states.
- [Density matrix](/density-matrix/) and [mixed state](/mixed-state/): the general state $\rho$; a pure state is the density matrix $|\psi\rangle\langle\psi|$. One density matrix arises from many ensembles of pure states.
- [Entanglement](/entanglement/): a pure state of several systems that is not a tensor product.
- [Quantum superposition](/quantum-superposition/): a state with several nonzero amplitudes in a chosen basis.
- [Born rule](/born-rule/) and [unitary operator](/unitary-operator/): what a state predicts, and how it changes.

### History

Dirac introduced the bra and ket notation in 1939. The tensor product description of composite systems and the state space postulate are standard; Nielsen and Chuang state them as postulates 1 and 4 in Section 2.2.

## References
