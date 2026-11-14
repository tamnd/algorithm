---
tag: FYQ408
kind: concept
slug: universal-gate-set
name: Universal gate set
aliases:
- universal quantum gates
area: quantum/quantum-primitives
level: core
summary: "A set of gates whose circuits can approximate every unitary on any number of qubits to any accuracy. CNOT with all one-qubit gates is exact; H, T and CNOT is a finite universal set."
prereqs: [quantum-gate, cnot-gate, phase-and-t-gates]
see_also: [solovay-kitaev-theorem, clifford-group, gottesman-knill-theorem, toffoli-gate, hadamard-gate, quantum-circuit-model, bqp, reversible-computation]
sources:
  - paper: doi:10.1103/PhysRevA.52.3457
    title: Adriano Barenco, Charles H. Bennett, Richard Cleve, David P. DiVincenzo, Norman Margolus, Peter Shor, Tycho Sleator, John A. Smolin and Harald Weinfurter, Elementary gates for quantum computation, Physical Review A 52, 1995, pages 3457 to 3467
    locator: CNOT and one-qubit gates are universal, with the constructions of controlled and multiply controlled gates
  - paper: doi:10.1103/PhysRevA.51.1015
    title: David P. DiVincenzo, Two-bit gates are universal for quantum computation, Physical Review A 51, 1995, pages 1015 to 1022
    locator: universality of two-qubit gates
  - paper: doi:10.1103/PhysRevLett.75.346
    title: Seth Lloyd, Almost any quantum logic gate is universal, Physical Review Letters 75, 1995, pages 346 to 349
    locator: almost every two-qubit gate is universal
  - paper: doi:10.1098/rspa.1995.0065
    title: David Deutsch, Adriano Barenco and Artur Ekert, Universality in quantum computation, Proceedings of the Royal Society of London A 449, 1995, pages 669 to 677
    locator: almost every two-qubit gate is universal
  - paper: doi:10.1016/S0020-0190(00)00084-3
    title: P. Oscar Boykin, Tal Mor, Matthew Pulver, Vwani Roychowdhury and Farrokh Vatan, A new universal and fault-tolerant quantum basis, Information Processing Letters 75(3), 2000, pages 101 to 107
    locator: H, the pi/8 gate T and CNOT form a universal basis, with the irrational rotation angle
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 4.5 (universal quantum gates), with 4.5.1 (two-level unitaries), 4.5.2 (one-qubit and CNOT gates), 4.5.3 (a discrete set) and 4.5.4 (most unitaries are hard)
  - url: https://arxiv.org/abs/quant-ph/0205115
    title: Yaoyun Shi, Both Toffoli and controlled-NOT need little help to do universal quantum computation, arXiv:quant-ph/0205115
    locator: the abstract and main theorems, Toffoli or CNOT with one real one-qubit gate
  - url: https://arxiv.org/abs/quant-ph/0301040
    title: Dorit Aharonov, A simple proof that Toffoli and Hadamard are quantum universal, arXiv:quant-ph/0301040, 2003
    locator: the short proof and the meaning of computational universality
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 2 (the circuit model), the part on universal sets of elementary gates
---

A *universal gate set* is a set of [quantum gates](/quantum-gate/) such that circuits built from them can approximate every [unitary](/unitary-operator/) on any number of qubits to any accuracy. CNOT together with all one-qubit gates is universal even exactly (Barenco et al. 1995). A finite set can only approximate, and the standard finite set is Hadamard, $T$ and CNOT ("Clifford plus $T$"). The [Solovay-Kitaev theorem](/solovay-kitaev-theorem/) shows that the approximation is cheap, so the choice of a universal set changes gate counts by at most a polylogarithmic factor.

## In plain words

A classical computer needs only one kind of logic gate, such as NAND, to build every function. A quantum computer has infinitely many possible gates, so no finite list can build all of them exactly. The best you can ask is to get as close as you like. A universal gate set does that: with enough of its gates in a row, you can come as near to any target operation as you want. The surprise is how small the set can be. One two-qubit gate and two one-qubit gates are enough, and the number of gates you need grows only slowly with the accuracy. Some sets look powerful but are not universal: the Clifford gates make large entangled states, but a classical computer can follow them easily.

## The idea

**Definition.** Fix a set $G$ of gates, each acting on one or two qubits. A circuit over $G$ applies gates of $G$ to any qubits in any order. The set $G$ is *universal* if for every $n$, every unitary $U$ on $n$ qubits and every $\varepsilon > 0$ there is a circuit $C$ over $G$, maybe with [ancilla qubits](/ancilla-qubits/) returned to $|0\rangle$, such that $\lVert U - e^{i\phi} C \rVert \le \varepsilon$ for some global phase $\phi$. It is *exactly universal* if $\varepsilon = 0$ is possible. Global phase is ignored, because no measurement sees it. Errors of separate gates add at most linearly: if each of $m$ gates is within $\varepsilon/m$ of its target, the circuit is within $\varepsilon$.

**Step 1: two-level unitaries.** A *two-level* unitary acts as a $2 \times 2$ unitary on two basis states and as the identity on all others. Every $d \times d$ unitary is a product of at most $d(d-1)/2$ two-level unitaries: multiply by two-level rotations that make the entries of the first column zero one by one, then go on with the next column, exactly as in a QR factorization by Givens rotations.

**Step 2: two-level unitaries from controlled gates.** A two-level unitary on basis states $|s\rangle$ and $|t\rangle$ is made by a Gray code walk from $s$ to $t$: multiply controlled $X$ gates swap $|s\rangle$ along the walk until it differs from $|t\rangle$ in one bit, then a multiply controlled one-qubit gate acts on that bit, and the walk is undone. With the multiply controlled gates of Step 3 this gives $O(n^2)$ gates per two-level unitary on $n$ qubits, and $O(n^2 4^n)$ gates for any unitary.

**Step 3: controlled gates from CNOT and one-qubit gates.** Every one-qubit unitary is $U = e^{i\alpha} R_z(\beta) R_y(\gamma) R_z(\delta)$. With $A = R_z(\beta) R_y(\gamma/2)$, $B = R_y(-\gamma/2) R_z(-(\delta + \beta)/2)$ and $C = R_z((\delta - \beta)/2)$ one has $ABC = I$ and $U = e^{i\alpha} AXBXC$. So the controlled-$U$ is $C$ on the target, a [CNOT](/cnot-gate/), $B$, a CNOT, $A$, and a phase $\mathrm{diag}(1, e^{i\alpha})$ on the control. When the control is $0$ the target sees $ABC = I$; when it is $1$ it sees $AXBXC$. Multiply controlled gates follow from controlled gates and the [Toffoli gate](/toffoli-gate/), and the Toffoli gate itself is six CNOTs and nine one-qubit gates. Steps 1 to 3 together prove that CNOT and all one-qubit gates are exactly universal.

**Step 4: a finite set.** Only the one-qubit gates are still infinite. The gate $T H T H$ is a rotation of the [Bloch sphere](/bloch-sphere/) by an angle $\theta$ with $\cos(\theta/2) = \cos^2(\pi/8)$, and $\theta$ is not a rational multiple of $\pi$. So its powers never repeat, and they come arbitrarily near every rotation about the same axis $\vec n$. Conjugating by $H$ gives the rotation by $\theta$ about a second axis $\vec m$, not parallel to $\vec n$, and every one-qubit gate is, up to phase, a finite product of rotations about $\vec n$ and $\vec m$ in turn. So $\{H, T\}$ generates a dense subgroup of the one-qubit gates, and $\{H, T, \mathrm{CNOT}\}$ is universal (Boykin et al.).

**Step 5: the cost.** The powers of $THTH$ alone need about $1/\varepsilon$ gates. The [Solovay-Kitaev theorem](/solovay-kitaev-theorem/) does much better: $O(\log^c(1/\varepsilon))$ gates for any finite universal set that is closed under inverses. The total cost of compiling a circuit of $m$ arbitrary gates is $O(m \log^c(m/\varepsilon))$ gates.

**Most unitaries are still expensive.** The steps above use $O(n^2 4^n)$ gates for a general $n$-qubit unitary. This cannot be improved much: a counting argument shows that most $n$-qubit unitaries need a number of gates exponential in $n$, even to accuracy a constant. Universality says that everything can be built, not that everything can be built cheaply. The interesting quantum algorithms are the unitaries with short circuits.

Pitfalls: approximate universality is about one fixed accuracy at a time, so a finite set never gives $U$ exactly; the Solovay-Kitaev bound needs a set that is closed under inverses, which holds for $H$ and $T$ because $H^{-1} = H$ and $T^7 = T^\dagger$; and a set can make every classical reversible function and large entanglement and still not be universal.

## Examples

**CNOT and all one-qubit gates.** Exactly universal, by Steps 1 to 3 (Barenco et al.). This is the usual "elementary gate" set for counting gates in theory.

**H, T and CNOT (Clifford plus T).** Universal, finite, and the standard set of fault-tolerant computing, because $H$ and CNOT are [Clifford gates](/clifford-group/) and the [T gate](/phase-and-t-gates/) can be made with magic states. Often $S = T^2$ is listed too. The Toffoli gate is exactly $2$ $H$ gates, $6$ CNOTs and $7$ $T$ or $T^\dagger$ gates.

**Almost any two-qubit gate.** A two-qubit gate chosen at random, with the freedom to apply it to any ordered pair of qubits, is universal with probability 1 (DiVincenzo; Lloyd; Deutsch, Barenco and Ekert, all 1995).

**Toffoli and Hadamard.** Universal in the *computational* sense (Shi 2003; Aharonov 2003): the gates have real entries, so they make only real amplitudes, but a complex amplitude $a + ib$ can be stored with one extra qubit, and every quantum computation can be simulated with polynomial overhead. More generally, Toffoli with any real one-qubit gate that does not preserve the computational basis is universal in this sense (Shi). So the step from classical [reversible computation](/reversible-computation/) to quantum computation is one gate.

**Non-example: the Clifford group.** $H$, $S$ and CNOT are not universal. The one-qubit Clifford group has only 24 elements modulo phase, so it approximates nothing else, and the [Gottesman-Knill theorem](/gottesman-knill-theorem/) simulates Clifford circuits classically. One $T$ gate makes the set universal.

**Non-example: classical gates.** Toffoli alone, or CNOT and $X$, only permute basis states. They make no superposition and are not universal.

**Non-example: one-qubit gates alone.** All one-qubit gates together are not universal: they make no entanglement, and a product state stays a product state.

**A check by hand.** With $R = T H T H$: up to phase, $T = \cos(\pi/8) I - i \sin(\pi/8) Z$ and $H T H = \cos(\pi/8) I - i \sin(\pi/8) X$. Their product has identity part $\cos^2(\pi/8) \approx 0.8536$, so $\cos(\theta/2) = \cos^2(\pi/8)$ and $\theta \approx 1.0961$, which is $\theta \approx 0.34889\pi$.

### Implementation

The file `impl/python/universal_gate_set.py` makes the constructive steps concrete: a two-level decomposition of any $d \times d$ unitary, the $Z$-$Y$-$Z$ form of a one-qubit gate, the controlled-$U$ from two CNOTs and the gates $A$, $B$ and $C$, the Toffoli circuit in $H$, $T$, $T^\dagger$ and CNOT, and the angle of $THTH$. The tests (seeds 4041 to 4043) check: the two-level decomposition of random unitaries of size 2, 3, 4 and 8, with at most $d(d-1)/2$ factors; the $Z$-$Y$-$Z$ form of $H$, $S$, $T$, $T^\dagger$ and 50 random gates; the controlled-$U$ circuit against the exact controlled gate for 20 random $U$ in both qubit orders; the Toffoli circuit against the Toffoli permutation, with the gate counts; that $\{H, S\}$ gives exactly 24 gates modulo phase while $\{H, T\}$ gives more than 500; and that $\cos(\theta/2) = \cos^2(\pi/8)$, no power $R^k$ with $k \le 2000$ is the identity, and the largest gap between the angles $k\theta \bmod 2\pi$ for $k \le 10^4$ is below $10^{-3}$. These are numerical checks; the irrationality of $\theta/\pi$ is a theorem, not something a finite test can prove.

## Where it is used

- **The circuit model.** The [quantum circuit model](/quantum-circuit-model/) counts gates from a universal set, and [BQP](/bqp/) is defined by uniform circuits over such a set. The Solovay-Kitaev theorem makes the class independent of the set.
- **Compilers.** A compiler turns the gates of an algorithm, such as the controlled rotations of the quantum Fourier transform, into the native gates of a machine or into Clifford plus $T$, with the [Solovay-Kitaev algorithm](/solovay-kitaev-theorem/) or with number-theoretic synthesis for $z$-rotations.
- **Fault tolerance.** Error-correcting codes such as the [Steane code](/steane-code/) give the Clifford gates transversally; the $T$ gate is made by magic state distillation. The universal set is chosen to match what the code can protect, and the [threshold theorem](/quantum-threshold-theorem/) is stated for such a set.
- **Hardness of simulation.** The line between Clifford circuits (easy) and Clifford plus $T$ (universal) is the basis of classical simulators whose cost is exponential only in the number of $T$ gates.

## References
