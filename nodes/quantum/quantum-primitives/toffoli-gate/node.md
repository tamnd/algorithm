---
tag: 8SZNQR
kind: definition
slug: toffoli-gate
name: Toffoli gate
aliases:
- CCNOT
- controlled-controlled-NOT
- CCX gate
area: quantum/quantum-primitives
level: intro
summary: "The three-bit gate (a, b, c) -> (a, b, c xor ab). It is universal for classical reversible computation, and with the Hadamard gate it is universal for quantum computation."
prereqs: [cnot-gate, quantum-gate]
see_also: [reversible-computation, ancilla-qubits, uncomputation, universal-gate-set, clifford-group, phase-and-t-gates, boolean-circuit, solovay-kitaev-theorem]
sources:
  - paper: doi:10.1007/3-540-10003-2_104
    title: "Tommaso Toffoli, Reversible computing, ICALP 1980, Lecture Notes in Computer Science 85, Springer, 1980, pp. 632-644"
    locator: the controlled-controlled-NOT gate and its universality for reversible computation with constant inputs
  - paper: doi:10.1007/BF01857727
    title: "Edward Fredkin and Tommaso Toffoli, Conservative logic, International Journal of Theoretical Physics 21(3-4):219-253, 1982"
    locator: the Fredkin gate (controlled swap), a second universal reversible gate
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: "Section 1.4.1 (the Toffoli gate as a classical reversible gate), Section 3.2.5 (energy and reversible computation), Section 4.3 (Figure 4.9, the Toffoli gate from Hadamard, phase, CNOT and pi/8 gates, and Exercise 4.24)"
  - paper: doi:10.1103/PhysRevA.52.3457
    title: "Adriano Barenco, Charles H. Bennett, Richard Cleve, David P. DiVincenzo, Norman Margolus, Peter Shor, Tycho Sleator, John A. Smolin and Harald Weinfurter, Elementary gates for quantum computation, Physical Review A 52(5):3457-3467, 1995"
    locator: "Lemma 6.1 (a doubly controlled U from five two-qubit gates)"
  - paper: arxiv:0803.2316
    title: "Vivek V. Shende and Igor L. Markov, On the CNOT-cost of TOFFOLI gates, Quantum Information and Computation 9(5-6):461-486, 2009"
    locator: six CNOT gates are necessary for the Toffoli gate
  - paper: arxiv:1308.4134
    title: David Gosset, Vadym Kliuchnikov, Michele Mosca and Vincent Russo, An algorithm for the T-count, 2013
    locator: every Clifford plus T circuit for the Toffoli gate has at least 7 T gates
  - paper: doi:10.1109/TCAD.2003.811448
    title: "Vivek V. Shende, Aditya K. Prasad, Igor L. Markov and John P. Hayes, Synthesis of reversible logic circuits, IEEE Transactions on Computer-Aided Design 22(6):710-722, 2003"
    locator: every even permutation is a circuit of NOT, CNOT and Toffoli gates with no extra lines
  - paper: arxiv:quant-ph/0205115
    title: "Yaoyun Shi, Both Toffoli and controlled-NOT need little help to do universal quantum computing, Quantum Information and Computation 3:84-92, 2003"
    locator: Toffoli plus any real one-qubit gate that changes the computational basis is universal
  - paper: arxiv:quant-ph/0301040
    title: Dorit Aharonov, A simple proof that Toffoli and Hadamard are quantum universal, 2003
    locator: a short proof of the Toffoli and Hadamard universality from Kitaev's gate set
---

The Toffoli gate is the three-bit gate that flips its third bit when its first two bits are both 1: $(a, b, c) \mapsto (a, b, c \oplus ab)$. Tommaso Toffoli introduced it in 1980 as a universal gate for [reversible computation](/reversible-computation/): with [ancilla](/ancilla-qubits/) bits set to constants, Toffoli gates compute every Boolean function. As a [quantum gate](/quantum-gate/) it is the doubly controlled version of the Pauli X gate, the [CNOT gate](/cnot-gate/) with one more control. It is how a quantum circuit runs classical logic, for example inside an [oracle](/quantum-oracle/).

## Definition

The Toffoli gate acts on three qubits, two *controls* $a, b$ and one *target* $c$. On the computational basis it is

$$\mathrm{CCX}\,|a\rangle|b\rangle|c\rangle = |a\rangle|b\rangle|c \oplus ab\rangle, \qquad a, b, c \in \{0, 1\},$$

and it extends to all states by linearity. Here $ab$ is the AND of $a$ and $b$, and $\oplus$ is addition mod 2. In the basis order $|000\rangle, |001\rangle, \ldots, |111\rangle$ its matrix is the $8 \times 8$ permutation matrix

$$\mathrm{CCX} = I_6 \oplus X = \begin{pmatrix} I_6 & 0 \\ 0 & X \end{pmatrix}, \qquad X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}.$$

It swaps $|110\rangle$ and $|111\rangle$ and fixes the other six basis states. In operator form, $\mathrm{CCX} = (I - |11\rangle\langle 11|) \otimes I + |11\rangle\langle 11| \otimes X$, where the first factor is the two controls (see [tensor product](/tensor-product/)).

On the implementation pages of this group, qubit 0 is the least significant bit of a basis index, and the ket $|q_2 q_1 q_0\rangle$ is the binary numeral of the index. This is the convention of the [quantum state](/quantum-state/) page. With the controls on qubits 2 and 1 and the target on qubit 0, the index of $|a\,b\,c\rangle$ is $4a + 2b + c$, and the gate swaps the indices 6 and 7.

**Basic properties.** Each one follows from the matrix.

- *Reversible and self-inverse.* Applying the gate twice adds $ab$ twice to $c$, so $\mathrm{CCX}^2 = I$. A permutation matrix is real and orthogonal, so the gate is [unitary](/unitary-operator/) and Hermitian.
- *Symmetric controls.* Swapping $a$ and $b$ does not change $c \oplus ab$.
- *Doubly controlled Z.* Conjugating the target by the [Hadamard gate](/hadamard-gate/) gives $\mathrm{CCZ} = (I \otimes I \otimes H)\,\mathrm{CCX}\,(I \otimes I \otimes H) = \mathrm{diag}(1, 1, 1, 1, 1, 1, 1, -1)$, because $HXH = Z$. The CCZ gate is symmetric in all three qubits.
- *Not Clifford.* $\mathrm{CCX}\,(X \otimes I \otimes I)\,\mathrm{CCX} = (X \otimes I \otimes I)\,\mathrm{CNOT}_{b \to c}$. The right side is not a Pauli operator up to a phase, so the gate does not map Pauli operators to Pauli operators, and it is outside the [Clifford group](/clifford-group/). Proof of the identity: on $|a, b, c\rangle$ the left side gives $|a \oplus 1, b, c \oplus ab \oplus (a \oplus 1)b\rangle = |a \oplus 1, b, c \oplus b\rangle$.

### Classical universality

With some inputs fixed to constants, one Toffoli gate gives the gates of a [Boolean circuit](/boolean-circuit/):

| gate | inputs $(a, b, c)$ | output | the result is on |
|---|---|---|---|
| AND | $(a, b, 0)$ | $(a, b, ab)$ | the target |
| NAND | $(a, b, 1)$ | $(a, b, 1 \oplus ab)$ | the target |
| NOT | $(1, 1, c)$ | $(1, 1, 1 \oplus c)$ | the target |
| FANOUT (copy) | $(a, 1, 0)$ | $(a, 1, a)$ | the first and the third bit |

NAND and FANOUT together compute every Boolean function. So for each $f : \{0,1\}^n \to \{0,1\}^m$ computed by a circuit of $s$ NAND and FANOUT gates there is a circuit of $s$ Toffoli gates and $s$ constant ancilla bits that maps $(x, \text{constants})$ to $(x, f(x), g(x))$, where $g(x)$ is the leftover *garbage*. The [uncomputation](/uncomputation/) page shows how to clear $g(x)$.

**No ancilla, and parity.** On $n$ wires a gate is a permutation of the $2^n$ bit strings. A Toffoli gate on $n$ wires swaps two strings for each value of the $n - 3$ other wires, so it is a product of $2^{n-3}$ disjoint transpositions. In the same way, a CNOT gate is $2^{n-2}$ transpositions and a NOT gate is $2^{n-1}$. For $n \ge 4$ each count is even, so each circuit of these gates on $n \ge 4$ wires computes an even permutation. Shende, Prasad, Markov and Hayes (2003) proved the converse: every even permutation of $\{0,1\}^n$ is a circuit of NOT, CNOT and Toffoli gates with no extra wires. An odd permutation $p$ needs one ancilla: $p \otimes \mathrm{id}$ on $n + 1$ wires is $p$ applied twice, once for each value of the ancilla, so it is even. On exactly 3 wires the Toffoli gate is one transposition, which is odd.

### Quantum universality

The Toffoli gate has only real entries and maps basis states to basis states, so alone it cannot make a superposition. Add the Hadamard gate, and the set $\{\mathrm{CCX}, H\}$ is universal for quantum computation in the computational sense (Shi 2003; a short proof by Aharonov 2003). The two gates generate only real matrices. A circuit over them simulates any quantum circuit with a polynomial overhead, because real amplitudes suffice when one extra qubit holds the real and imaginary parts. Shi proved more: the Toffoli gate with any real one-qubit gate that does not preserve the computational basis is universal. See [universal gate set](/universal-gate-set/).

### Decompositions

**Clifford plus T.** The Toffoli gate is an exact circuit of 6 CNOT gates, 7 gates T or $T^\dagger$, and 2 Hadamard gates on the target (Nielsen and Chuang, Figure 4.9, draw a version with one phase gate $S$). With controls $a, b$ and target $c$, in time order:

```
H(c)
CNOT(b,c)  Tdg(c)  CNOT(a,c)  T(c)
CNOT(b,c)  Tdg(c)  CNOT(a,c)  T(b)  T(c)
H(c)
CNOT(a,b)  T(a)  Tdg(b)  CNOT(a,b)
```

Here $T = \mathrm{diag}(1, e^{i\pi/4})$ (see [phase and T gates](/phase-and-t-gates/)). The circuit equals CCX exactly, with no global phase. Both counts are optimal. Shende and Markov (2009) proved that six CNOT gates are necessary, even with any one-qubit gates. Gosset, Kliuchnikov, Mosca and Russo (2013) proved that each Clifford plus T circuit for the Toffoli gate on three qubits has at least 7 T gates.

**Two-qubit gates.** Let $V = \frac{1}{2}\begin{pmatrix} 1+i & 1-i \\ 1-i & 1+i \end{pmatrix}$, so $V^2 = X$. Then (Barenco et al. 1995, Lemma 6.1)

$$\mathrm{CCX} = C_a V_c \cdot \mathrm{CNOT}_{a \to b} \cdot C_b V^\dagger_c \cdot \mathrm{CNOT}_{a \to b} \cdot C_b V_c,$$

where $C_q W_c$ applies $W$ to $c$ when $q$ is 1, and the rightmost factor acts first. Proof: after the two CNOT gates the middle gate sees $a \oplus b$. The target gets $V^{b}$, then $V^{-(a \oplus b)}$, then $V^{a}$. The exponent $a + b - (a \oplus b)$ is $2ab$, so the target gets $V^{2ab} = X^{ab}$. The two CNOT gates restore $b$.

## Examples and non-examples

**Truth table.** The gate changes only the last two rows:

| $a\,b\,c$ | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|---|---|---|---|---|---|---|---|---|
| output | 000 | 001 | 010 | 011 | 100 | 101 | 111 | 110 |

**A half adder.** Start with $(a, b, 0)$. A Toffoli gate with target the third bit gives $(a, b, ab)$, and then a CNOT from $a$ to $b$ gives $(a, a \oplus b, ab)$. The middle bit is the sum bit and the last bit is the carry. For $a = b = 1$ the result is $(1, 0, 1)$: $1 + 1 = 10$ in binary. Chains of such blocks give reversible versions of the [ripple-carry adder](/ripple-carry-adder/).

**On a superposition.** Apply CCX to $\frac{1}{\sqrt 2}(|0\rangle + |1\rangle) \otimes |1\rangle \otimes |0\rangle$. By linearity the result is $\frac{1}{\sqrt 2}(|010\rangle + |111\rangle)$. The first and the last qubit are now entangled: the state is not a product of one-qubit states.

**On an eigenvector of X.** Put the target in $|-\rangle = \frac{1}{\sqrt 2}(|0\rangle - |1\rangle)$. Since $X|-\rangle = -|-\rangle$, the gate maps $|a\rangle|b\rangle|-\rangle$ to $(-1)^{ab}|a\rangle|b\rangle|-\rangle$. The target does not change, and the controls get the phase of a controlled Z. This is [phase kickback](/phase-kickback/).

**Non-example: the AND gate.** The map $(a, b) \mapsto ab$ is not reversible: three inputs give the output 0. No unitary computes it in place. The Toffoli gate keeps $a$ and $b$, and so it is a bijection.

**Non-example: CNOT and NOT alone.** A circuit of CNOT and NOT gates computes an affine map $x \mapsto Mx \oplus v$ over $\mathrm{GF}(2)$, because each of the two gates is affine and a composition of affine maps is affine. AND is not affine, so these gates cannot compute it, with any number of ancillas. The Toffoli gate is the step from linear to universal logic.

**Non-example: Toffoli without H.** A circuit of Toffoli, CNOT and NOT gates maps each basis state to one basis state. Its output on a basis input is always a basis state, so it cannot give any interference. It is a classical reversible circuit that runs on qubits.

## Related definitions

- [CNOT gate](/cnot-gate/): the gate with one control. The Toffoli gate is the case $k = 2$ of the gate with $k$ controls, $C^k X$. The [ancilla qubits](/ancilla-qubits/) page builds $C^k X$ from Toffoli gates with $k - 2$ ancillas.
- The Fredkin gate, or controlled swap: it swaps $b$ and $c$ when $a = 1$. It conserves the number of ones, and it is also universal for reversible computation (Fredkin and Toffoli 1982). It is the gate of the [swap test](/swap-test/).
- [Reversible computation](/reversible-computation/): the model of circuits of bijective gates. [Uncomputation](/uncomputation/) clears the garbage that Toffoli circuits leave.
- [Universal gate set](/universal-gate-set/) and the [Solovay-Kitaev theorem](/solovay-kitaev-theorem/): Clifford plus T is universal, and the Toffoli gate is a standard non-Clifford gate in it.
- [Quantum oracle](/quantum-oracle/): the bit oracle $|x\rangle|y\rangle \mapsto |x\rangle|y \oplus f(x)\rangle$ is built from a Toffoli circuit for $f$.

## References
