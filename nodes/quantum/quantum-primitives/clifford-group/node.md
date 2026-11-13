---
tag: 5V9XE0
kind: definition
slug: clifford-group
name: Clifford group
aliases:
- Clifford gates
area: quantum/quantum-primitives
level: advanced
summary: "The unitaries that map Pauli strings to Pauli strings under conjugation. H, S and CNOT generate it up to phase; modulo phase it has 24 elements on one qubit and 11520 on two."
prereqs: [pauli-gates, hadamard-gate, phase-and-t-gates, cnot-gate]
see_also: [stabilizer-formalism, gottesman-knill-theorem, universal-gate-set, solovay-kitaev-theorem, quantum-error-correction, steane-code, toffoli-gate, bell-states]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 10.5.1 (the Pauli group and stabilizers) and Section 10.5.2 (unitary gates and the stabilizer formalism, the normalizer of the Pauli group and its generation by H, S and CNOT)
  - url: https://arxiv.org/abs/quant-ph/9705052
    title: Daniel Gottesman, Stabilizer Codes and Quantum Error Correction, PhD thesis, California Institute of Technology, 1997, arXiv:quant-ph/9705052
    locator: Chapter 5, section Transformations of the Stabilizer (the normalizer of the Pauli group and its generators), and Chapter 3, section Alternate Languages for Stabilizers (the binary form)
  - url: https://arxiv.org/abs/quant-ph/9807006
    title: Daniel Gottesman, The Heisenberg representation of quantum computers, Group22, Proceedings of the XXII International Colloquium on Group Theoretical Methods in Physics, International Press, 1999, pages 32 to 43, arXiv:quant-ph/9807006
    locator: the action of H, S (called P there) and CNOT on Pauli operators
  - paper: doi:10.1109/18.681315
    title: A. Robert Calderbank, Eric M. Rains, Peter W. Shor and Neil J. A. Sloane, Quantum error correction via codes over GF(4), IEEE Transactions on Information Theory 44(4), 1998, pages 1369 to 1387
    locator: the binary symplectic description of the Pauli group and of its normalizer
  - paper: doi:10.1103/PhysRevA.70.052328
    title: Scott Aaronson and Daniel Gottesman, Improved simulation of stabilizer circuits, Physical Review A 70, 2004, article 052328, arXiv:quant-ph/0406196
    locator: the canonical form of a Clifford circuit with O(n^2/log n) gates
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 20.2 (Clifford circuits) and Section 20.4 (T gates and magic states)
  - paper: doi:10.1038/46503
    title: Daniel Gottesman and Isaac L. Chuang, Demonstrating the viability of universal quantum computation using teleportation and single-qubit operations, Nature 402, 1999, pages 390 to 393
    locator: the Clifford hierarchy
---

The *Clifford group* on $n$ [qubits](/qubit/) is the set of [unitary operators](/unitary-operator/) $U$ that map every [Pauli string](/pauli-gates/) to a Pauli string, up to a phase, under conjugation $P \mapsto UPU^\dagger$. The [Hadamard gate](/hadamard-gate/) $H$, the [phase gate](/phase-and-t-gates/) $S$ and the [CNOT gate](/cnot-gate/) generate it, up to a global phase. Modulo phases it is a finite group: 24 elements on one qubit, 11520 on two. Clifford circuits make entangled states and are the gates of most [error-correcting codes](/quantum-error-correction/), but a classical computer simulates them efficiently ([Gottesman-Knill theorem](/gottesman-knill-theorem/)). One more gate outside the group, such as $T$, makes a [universal gate set](/universal-gate-set/).

## Definition

**The Pauli group.** Let $\mathcal{P}_n$ be the group of the $4 \cdot 4^n$ operators $i^k P_{n-1} \otimes \cdots \otimes P_0$ with $k \in \{0, 1, 2, 3\}$ and each $P_j \in \{I, X, Y, Z\}$ ([Pauli gates](/pauli-gates/)). A Pauli string is written as a word such as $XIZ$; its rightmost letter acts on qubit $0$, the convention of [quantum state](/quantum-state/).

**The Clifford group.** The $n$-qubit Clifford group is the normalizer of $\mathcal{P}_n$ in the unitary group:

$$\mathcal{C}_n = \{\, U \in \mathrm{U}(2^n) : U P U^\dagger \in \mathcal{P}_n \text{ for every } P \in \mathcal{P}_n \,\}.$$

A *Clifford gate* or *Clifford circuit* is an element of $\mathcal{C}_n$. The group contains every global phase $e^{i\gamma} I$, so it is infinite. A global phase cannot be observed, so one usually counts the quotient $\mathcal{C}_n / \mathrm{U}(1)$, which is finite.

**A Clifford is fixed by its action on 2n Paulis.** Let $U, V \in \mathcal{C}_n$ with $U X_j U^\dagger = V X_j V^\dagger$ and $U Z_j U^\dagger = V Z_j V^\dagger$ for each qubit $j$. Then $W = V^\dagger U$ commutes with every $X_j$ and $Z_j$. These generate all Pauli strings, and the Pauli strings span all $2^n \times 2^n$ matrices, so $W$ commutes with every matrix. So $W$ is a multiple of $I$, and $U = e^{i\gamma} V$. The list of the $2n$ images $U X_j U^\dagger$, $U Z_j U^\dagger$ is the *tableau* of $U$. It fixes $U$ up to a global phase.

**Binary form.** Each Pauli operator is $i^k X^{x} Z^{z}$, short for $i^k \bigotimes_j X^{x_j} Z^{z_j}$, with $x, z \in \mathrm{GF}(2)^n$. Since $XZ = -iY$, a $Y$ at position $j$ has $x_j = z_j = 1$ and adds $1$ to $k$. Two Pauli operators with vectors $(x, z)$ and $(x', z')$ commute if and only if the symplectic product

$$\omega\big((x, z), (x', z')\big) = x \cdot z' + z \cdot x' \bmod 2$$

is $0$. Conjugation keeps products and commutation, so a Clifford $U$ acts on the vectors $(x, z)$ by a linear map $M_U$ over $\mathrm{GF}(2)$ with $\omega(M_U a, M_U b) = \omega(a, b)$, a *symplectic* matrix, and on the phases by a sign for each of the $2n$ images. Every symplectic matrix and every choice of the $2n$ signs occurs. This gives the order

$$\left|\mathcal{C}_n / \mathrm{U}(1)\right| = 4^n \cdot |\mathrm{Sp}(2n, 2)| = 2^{n^2 + 2n} \prod_{j=1}^{n} (4^j - 1),$$

where the factor $4^n$ counts the sign choices that the Pauli strings themselves make, and $|\mathrm{Sp}(2n, 2)| = 2^{n^2}\prod_{j=1}^n (4^j - 1)$. For $n = 1, 2, 3$ this is 24, 11520 and 92897280.

**The generators.** $H$, $S$ and CNOT are in $\mathcal{C}_n$, and they generate $\mathcal{C}_n$ up to global phases: every element is, up to phase, a circuit of $O(n^2)$ such gates (Nielsen and Chuang, Section 10.5.2; Aaronson and Gottesman give a canonical form with $O(n^2/\log n)$ gates). On the basis $X$, $Z$ of each qubit they act as follows.

| gate | $X \mapsto$ | $Z \mapsto$ | $Y \mapsto$ |
|---|---|---|---|
| $H$ | $Z$ | $X$ | $-Y$ |
| $S$ | $Y$ | $Z$ | $-X$ |
| CNOT, control $c$, target $t$ | $X_c \mapsto X_c X_t$, $X_t \mapsto X_t$ | $Z_c \mapsto Z_c$, $Z_t \mapsto Z_c Z_t$ | $Y_c \mapsto Y_c X_t$, $Y_t \mapsto Z_c Y_t$ |

In the binary form the rules are: $H$ on qubit $q$ swaps $x_q$ and $z_q$ and adds $2 x_q z_q$ to $k$; $S$ on qubit $q$ sets $z_q \leftarrow z_q \oplus x_q$ and adds $x_q$ to $k$; CNOT sets $x_t \leftarrow x_t \oplus x_c$ and $z_c \leftarrow z_c \oplus z_t$ and does not change $k$. Each rule costs $O(1)$ word operations, which is the basis of fast stabilizer simulation.

## Examples and non-examples

**One qubit.** A one-qubit Clifford maps $X$ to one of the six operators $\pm X, \pm Y, \pm Z$, and $Z$ to one of the four that anticommute with the image of $X$. So $|\mathcal{C}_1/\mathrm{U}(1)| = 6 \cdot 4 = 24$, the formula with $n = 1$. These are the 24 rotations of a cube whose face centres are the six Pauli eigenstates on the [Bloch sphere](/bloch-sphere/). As shortest words in $H$ and $S$, the 24 elements have lengths 0 to 6, with 1, 2, 3, 5, 5, 5 and 3 elements of each length. With the phases kept, the matrices generated by $H$ and $S$ form a group of 192 elements, eight phases $e^{i\pi k/4}$ for each of the 24.

**Two qubits.** A breadth-first search over the tableaux from the six generators $H$ and $S$ on each qubit and CNOT in both directions finds 11520 elements, the formula with $n = 2$. The longest shortest circuit has 11 gates.

**The Bell circuit.** Apply $H$ to qubit $1$, then CNOT with control $1$ and target $0$. Track the generators of the stabilizer of $|00\rangle$: $Z_1 \mapsto X_1 \mapsto X_1 X_0$ and $Z_0 \mapsto Z_0 \mapsto Z_1 Z_0$. So the output is the state fixed by $XX$ and $ZZ$, which is the [Bell state](/bell-states/) $(|00\rangle + |11\rangle)/\sqrt 2$. This is the [stabilizer formalism](/stabilizer-formalism/) in one line.

**A sign that matters.** CNOT with control $1$ and target $0$ maps $XZ$ to $(X_1X_0)(Z_1Z_0) = (XZ) \otimes (XZ) = (-iY) \otimes (-iY) = -YY$. A simulator that drops the phase $k$ gets the sign wrong.

**Other Clifford gates.** The controlled-$Z$ gate is $(I \otimes H)\,\mathrm{CNOT}\,(I \otimes H)$, and SWAP is three CNOT gates, so both are Clifford. Every Pauli string is Clifford: it maps each Pauli string $Q$ to $\pm Q$.

**Non-example: the T gate.** $T X T^\dagger = (X + Y)/\sqrt 2$, which is not a Pauli string times a phase, so $T \notin \mathcal{C}_1$. $T$ still maps $Z$ to $Z$. Since $T^2 = S$, $T$ is a "square root" of a Clifford gate; such gates make the third level of the *Clifford hierarchy* of Gottesman and Chuang, where level 1 is the Pauli group, level 2 the Clifford group, and level $k+1$ the unitaries that map Paulis into level $k$.

**Non-example: the Toffoli gate.** The [Toffoli gate](/toffoli-gate/) maps $X$ on a control to $X$ on that control times a CNOT, which is not a Pauli string. It is in level 3 of the hierarchy, like $T$.

**Non-example: a group that is too small.** Clifford circuits are not universal. The group $\mathcal{C}_n/\mathrm{U}(1)$ is finite, so its elements cannot approximate the continuum of unitaries. Adding $T$ gives a dense set ([universal gate set](/universal-gate-set/)).

### Common errors

- Conjugating the wrong way. The tableau records $U P U^\dagger$, the image of $P$ when $U$ acts on the state. $U^\dagger P U$ is the image under $U^{-1}$; for $S$ the two differ ($S X S^\dagger = Y$, $S^\dagger X S = -Y$).
- Dropping signs and the phase $k$. The images must be tracked with their signs; the symplectic matrix alone fixes $U$ only up to a Pauli string.
- Confusing it with the Clifford algebra of physics. The name is the same, the object is not: here it is a finite group (modulo phase) of unitaries.
- Thinking that "easy to simulate" means "no entanglement". Clifford circuits make Bell states and GHZ states; the [Gottesman-Knill theorem](/gottesman-knill-theorem/) simulates them anyway.

### Implementation

The file `impl/python/clifford_group.py` stores a Pauli operator as $(k, x, z)$ with $x, z$ as integer bit masks and applies the three rules above exactly. It computes tableaux and the commutation test, and it enumerates $\mathcal{C}_n/\mathrm{U}(1)$ by a breadth-first search over tableaux. The tests compare each rule with the matrix product $U P U^\dagger$ for every gate and all 64 Pauli strings on three qubits, compare 25 random circuits with matrices (seed 6061), check that 40 random four-qubit circuits keep the commutation relations (seed 6062), count 24 and 11520 elements, count 192 matrices generated by $H$ and $S$ with phases, and check that $T$ is not Clifford.

## Related definitions

- [Pauli gates](/pauli-gates/): the group that the Clifford group normalizes.
- [Stabilizer formalism](/stabilizer-formalism/): states and codes described by Pauli groups; Clifford gates map stabilizer states to stabilizer states.
- [Gottesman-Knill theorem](/gottesman-knill-theorem/): the binary rules above give a polynomial-time classical simulation of Clifford circuits.
- [Universal gate set](/universal-gate-set/) and [Solovay-Kitaev theorem](/solovay-kitaev-theorem/): Clifford gates plus $T$ are universal, and the Clifford plus T set is the standard target of gate synthesis.
- [Quantum error correction](/quantum-error-correction/) and [Steane code](/steane-code/): the Steane code applies every Clifford gate transversally, and the [threshold theorem](/quantum-threshold-theorem/) uses Clifford gates as the inexpensive part of a fault-tolerant gate set.
- [Phase and T gates](/phase-and-t-gates/): $S$ is Clifford and $T$ is not.

### History

Gottesman described the normalizer of the Pauli group and its action on Pauli operators in his 1997 thesis on stabilizer codes, and the binary symplectic form appears in the work of Calderbank, Rains, Shor and Sloane (1998). Gottesman's 1998 lecture on the Heisenberg representation used the action of $H$, $S$ and CNOT on Pauli operators to simulate these circuits. Gottesman and Chuang defined the Clifford hierarchy in 1999. Aaronson and Gottesman gave the canonical form and the fast simulator in 2004.

## References
