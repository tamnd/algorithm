---
tag: YFZYCG
kind: concept
slug: stabilizer-formalism
name: Stabilizer formalism
aliases:
- stabilizer states
area: quantum/quantum-primitives
level: advanced
summary: "Describe a state or a code by the abelian group of Pauli strings that fixes it: n - k generators on n qubits in place of 2^n amplitudes. The language of most quantum codes."
prereqs: [clifford-group, pauli-gates]
see_also: [gottesman-knill-theorem, quantum-error-correction, shor-code, steane-code, bell-states, syndrome, parity-check-matrix, linear-system-modulo-2]
sources:
  - url: https://arxiv.org/abs/quant-ph/9705052
    title: Daniel Gottesman, Stabilizer Codes and Quantum Error Correction, PhD thesis, California Institute of Technology, 1997, arXiv:quant-ph/9705052
    locator: Chapter 3 (stabilizer coding, with the section on alternate languages for the binary form), Chapter 4 (encoding and decoding stabilizer codes) and Chapter 8 (examples, among them the five-qubit code and CSS codes)
  - paper: doi:10.1103/PhysRevA.54.1862
    title: Daniel Gottesman, Class of quantum error-correcting codes saturating the quantum Hamming bound, Physical Review A 54, 1996, pages 1862 to 1868
    locator: the first paper with stabilizer codes
  - paper: doi:10.1109/18.681315
    title: A. Robert Calderbank, Eric M. Rains, Peter W. Shor and Neil J. A. Sloane, Quantum error correction via codes over GF(4), IEEE Transactions on Information Theory 44(4), 1998, pages 1369 to 1387
    locator: additive codes over GF(4) and the binary symplectic form
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 10.5 (stabilizer codes), with 10.5.1 (the stabilizer formalism), 10.5.3 (measurement) and 10.5.6 (examples, among them the five-qubit code)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 20.1 (stabilizer states) and Chapter 21 (error correction)
  - paper: doi:10.1103/PhysRevLett.77.198
    title: Raymond Laflamme, Cesar Miquel, Juan Pablo Paz and Wojciech H. Zurek, Perfect quantum error correcting code, Physical Review Letters 77, 1996, pages 198 to 201
    locator: the five-qubit code
  - paper: doi:10.1103/PhysRevA.54.3824
    title: Charles H. Bennett, David P. DiVincenzo, John A. Smolin and William K. Wootters, Mixed-state entanglement and quantum error correction, Physical Review A 54, 1996, pages 3824 to 3851
    locator: the five-qubit code, found at the same time
---

The *stabilizer formalism* describes a quantum state, or a whole subspace, by the set of [Pauli strings](/pauli-gates/) that leave it unchanged. On $n$ qubits such a set is an abelian group that is given by at most $n$ generators, so a list of $n$ strings of $n$ letters replaces $2^n$ complex amplitudes. [Clifford gates](/clifford-group/) map these groups to groups of the same kind, and Pauli measurements change them by simple rules, which gives the [Gottesman-Knill theorem](/gottesman-knill-theorem/). Almost every [quantum error-correcting code](/quantum-error-correction/) in use, from the [Shor code](/shor-code/) and the [Steane code](/steane-code/) to the surface code, is a stabilizer code.

## In plain words

Some quantum states are fully described by a few yes-or-no checks. Each check is a row of letters I, X, Y or Z, one for each qubit, and the state is the only one that passes all the checks. A Bell pair, for example, is the only two-qubit state that passes the checks "XX" and "ZZ". If you keep only the checks, you can follow what simple gates do, and you can describe a code: the code is the set of states that pass a shorter list of checks. An error makes some checks fail, and the pattern of failed checks tells you which error happened, without looking at the encoded data.

## The idea

**Stabilizer groups.** Let $\mathcal{P}_n$ be the $n$-qubit Pauli group, the operators $i^k P_{n-1} \otimes \cdots \otimes P_0$ with $P_j \in \{I, X, Y, Z\}$ (rightmost letter on qubit $0$, as on [quantum state](/quantum-state/)). A *stabilizer group* is a subgroup $\mathcal{S} \subseteq \mathcal{P}_n$ that is abelian and does not contain $-I$. Its elements are then Hermitian, $\pm$ a Pauli string. The group has $2^m$ elements and $m$ independent generators $g_1, \ldots, g_m$, with $m \le n$.

**The code space.** The *stabilizer code* of $\mathcal{S}$ is the joint $+1$ eigenspace

$$V_{\mathcal{S}} = \{\, |\psi\rangle : g|\psi\rangle = |\psi\rangle \text{ for all } g \in \mathcal{S} \,\}, \qquad \Pi_{\mathcal{S}} = \prod_{i=1}^{m} \frac{I + g_i}{2} = \frac{1}{2^m}\sum_{g \in \mathcal{S}} g.$$

Each $g \ne I$ in $\mathcal{S}$ is traceless, so $\operatorname{tr} \Pi_{\mathcal{S}} = 2^n / 2^m$ and $\dim V_{\mathcal{S}} = 2^{n-m}$. With $m = n - k$ generators the code holds $k$ logical qubits. If $-I$ were in $\mathcal{S}$ the space would be $\{0\}$; this is why the condition is needed. With $m = n$ the space is one-dimensional, and its state is a *stabilizer state*. The number of stabilizer states on $n$ qubits is $2^n \prod_{j=1}^{n}(2^j + 1)$, which is 6, 60 and 1080 for $n = 1, 2, 3$.

**Binary form.** Write a Pauli string up to sign as $X^{a} Z^{b}$ with $a, b \in \mathrm{GF}(2)^n$ (see [Clifford group](/clifford-group/)). Two strings commute exactly when the symplectic product $a \cdot b' + b \cdot a'$ is $0$ mod 2. So $m$ generators are an $m \times 2n$ binary matrix $[A \mid B]$ with $AB^{\mathsf T} + BA^{\mathsf T} = 0$, and independence is the rank of this matrix over $\mathrm{GF}(2)$. Products, independence and membership tests are [Gaussian elimination modulo 2](/linear-system-modulo-2/). This is the quantum version of a [parity-check matrix](/parity-check-matrix/).

**Gates and measurements.** If $|\psi\rangle \in V_{\mathcal{S}}$ and $U$ is a unitary, then $U|\psi\rangle$ is fixed by $U g U^\dagger$ for each $g \in \mathcal{S}$. For a Clifford $U$ the new group is again a stabilizer group, so a state is updated by conjugating its $m$ generators. Measuring a Pauli string $P$ either gives a fixed outcome, when $\pm P \in \mathcal{S}$, or two outcomes with probability $1/2$ each, when $P$ anticommutes with some generator; in the second case one generator is replaced by $\pm P$. The [Gottesman-Knill theorem](/gottesman-knill-theorem/) proves these rules.

**Errors, syndromes and logical operators.** Let $E$ be a Pauli string. For each generator, $E$ either commutes or anticommutes with it, so $g_i E |\psi\rangle = \pm E |\psi\rangle$. Measuring $g_1, \ldots, g_m$ on $E|\psi\rangle$ gives a list of $m$ signs, the *syndrome* of $E$, and it does not disturb the encoded state. It is the analogue of the classical [syndrome](/syndrome/) $H e$. The Pauli strings that commute with all of $\mathcal{S}$ form its *normalizer* $N(\mathcal{S})$. An element of $N(\mathcal{S}) \setminus \mathcal{S}$ has syndrome $0$ but changes the encoded state; it is a *logical operator*. The *distance* $d$ is the smallest weight of a logical operator, and the code is called $[[n, k, d]]$. A set of errors $\{E_a\}$ is correctable when every product $E_a^\dagger E_b$ is either in $\mathcal{S}$ (the two errors act the same on the code, and the code is *degenerate*) or outside $N(\mathcal{S})$ (the syndromes differ). This is the [Knill-Laflamme condition](/quantum-error-correction/) for Pauli errors. A code of distance $d$ corrects all errors on up to $\lfloor (d-1)/2 \rfloor$ qubits.

**CSS codes.** If every generator is a pure $X$-string or a pure $Z$-string, the code is a CSS code (Calderbank, Shor and Steane). Then the $X$ part comes from one classical [linear code](/linear-code/) and the $Z$ part from another, and the commutation condition says that one code contains the [dual](/dual-code/) of the other. The [Steane code](/steane-code/) uses the [Hamming code](/hamming-code/) for both.

## Examples

**Bell states.** $(|00\rangle + |11\rangle)/\sqrt 2$ has generators $XX$ and $ZZ$. The other three [Bell states](/bell-states/) have $\pm XX$, $\pm ZZ$ with the other sign choices; $-XX, -ZZ$ gives the singlet $(|01\rangle - |10\rangle)/\sqrt 2$. Since $XX \cdot ZZ = -YY$, the list $XX, ZZ, -YY$ is not independent: its third element is already in the group. The list $XX, ZZ, YY$ is worse: $XX \cdot ZZ \cdot YY = -I$, so no nonzero state is fixed by all three.

**GHZ state.** $(|000\rangle + |111\rangle)/\sqrt 2$ has generators $XXX$, $ZZI$, $IZZ$. Three generators of three letters replace eight amplitudes; for $n$ qubits, $n$ generators replace $2^n$ amplitudes.

**The three-qubit bit-flip code.** Generators $ZZI$ and $IZZ$, so $n = 3$, $m = 2$, $k = 1$, and the code space is spanned by $|000\rangle$ and $|111\rangle$. An $X$ error on qubit $0$, $1$ or $2$ gives the syndromes $(+, -)$, $(-, -)$, $(-, +)$ for $(ZZI, IZZ)$. The logical operators are $XXX$ and $ZII$, so $d = 1$: a single $Z$ error is a logical error. This is the quantum form of the [repetition code](/repetition-code/), and it protects only against $X$ errors.

**The five-qubit code.** The four generators $XZZXI$, $IXZZX$, $XIXZZ$, $ZXIXZ$ (cyclic shifts) give a $[[5, 1, 3]]$ code (Laflamme, Miquel, Paz and Zurek; Bennett, DiVincenzo, Smolin and Wootters). The 15 single-qubit Pauli errors and the identity have the 16 different syndromes in $\{+,-\}^4$, so the code meets the quantum [Hamming bound](/hamming-bound/) $2^{n-k} \ge 1 + 3n$ with equality, the quantum analogue of a perfect code.

**Shor and Steane.** The [Shor code](/shor-code/) is $[[9, 1, 3]]$ with 8 generators, six of type $ZZ$ and two of weight six of type $X$; it is degenerate. The [Steane code](/steane-code/) is $[[7, 1, 3]]$ with 6 generators, three $X$-type and three $Z$-type from the Hamming parity-check matrix.

### Implementation

The file `impl/python/stabilizer_formalism.py` builds the projector $\prod_i (I + g_i)/2$ as a dense matrix for small $n$, reads off code dimensions and stabilizer states, multiplies signed Pauli strings, tests the stabilizer-group conditions and computes syndromes. The tests check the Bell, singlet and GHZ states against their amplitudes, that the lists $XX, ZZ, -YY$ (dependent) and $XX, ZZ, YY$ (with $-I$ in the group) are rejected, that the bit-flip code and the five-qubit code have dimension 2, that the five-qubit code has 16 different syndromes, and that a breadth-first search from $|0\cdots0\rangle$ under $H$, $S$ and CNOT finds 6, 60 and 1080 stabilizer states modulo phase.

## Where it is used

- **Quantum error correction.** Encoders, syndrome circuits and decoders of stabilizer codes are described and built in this language: the [Shor code](/shor-code/), the [Steane code](/steane-code/), the five-qubit code, the surface code and the quantum LDPC codes. Decoding a stabilizer code is a classical problem on the binary syndrome, close to [syndrome decoding](/syndrome-decoding/) of a classical linear code.
- **Fault tolerance.** Fault-tolerant gadgets and the [quantum threshold theorem](/quantum-threshold-theorem/) use stabilizer codes, transversal Clifford gates and stabilizer-state ancillas.
- **Classical simulation.** Stabilizer states are the states of the [Gottesman-Knill theorem](/gottesman-knill-theorem/), and simulators of this kind run error-correction circuits with millions of gates.
- **Entanglement and communication.** [Bell states](/bell-states/), GHZ states and graph states are stabilizer states; [teleportation](/quantum-teleportation/) and [superdense coding](/superdense-coding/) are stabilizer protocols.
- **Measurement-based computation.** Cluster states are stabilizer states; with single-qubit measurements in non-Pauli bases they give universal computation.

Pitfalls: the generators of a group are not unique, so two different lists can describe the same state; a stabilizer group must not contain $-I$; and the formalism describes only Clifford dynamics exactly. A $T$ gate maps a stabilizer state to a state that is not a stabilizer state.

## References
