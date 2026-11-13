---
tag: QGYZM1
kind: definition
slug: steane-code
name: Steane code
aliases:
- seven-qubit code
area: quantum/quantum-primitives
level: advanced
summary: "The [[7, 1, 3]] CSS code of Steane (1996), built from the [7, 4, 3] Hamming code for both X and Z checks. It corrects any one-qubit error and has transversal H, S and CNOT."
prereqs: [quantum-error-correction, stabilizer-formalism, hamming-code]
see_also: [shor-code, clifford-group, quantum-threshold-theorem, dual-code, simplex-code, parity-check-matrix, syndrome-decoding, gottesman-knill-theorem]
sources:
  - paper: doi:10.1103/PhysRevLett.77.793
    title: Andrew M. Steane, Error correcting codes in quantum theory, Physical Review Letters 77, 1996, pages 793 to 797
    locator: the seven-qubit code from the Hamming code
  - paper: doi:10.1098/rspa.1996.0136
    title: Andrew M. Steane, Multiple-particle interference and quantum error correction, Proceedings of the Royal Society of London A 452, 1996, pages 2551 to 2577
    locator: the general construction of codes from a classical code that contains its dual
  - paper: doi:10.1103/PhysRevA.54.1098
    title: A. Robert Calderbank and Peter W. Shor, Good quantum error-correcting codes exist, Physical Review A 54, 1996, pages 1098 to 1105
    locator: the CSS construction and its rate
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 10.4.2 (Calderbank-Shor-Steane codes and the Steane code), Section 10.5.6 (the Steane code as a stabilizer code) and Section 10.6 (fault-tolerant operations on the Steane code)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 21, Section 21.4 (quantum error-correcting codes) and Section 21.5 (fault-tolerance)
  - paper: doi:10.1103/PhysRevLett.102.110502
    title: Bryan Eastin and Emanuel Knill, Restrictions on transversal encoded quantum gate sets, Physical Review Letters 102, 2009, article 110502
    locator: no code that detects all one-qubit errors has a universal set of transversal gates
---

The *Steane code* is a seven-qubit quantum code, found by Andrew Steane in 1996, that encodes one logical [qubit](/qubit/) and corrects an arbitrary error on any one of the seven qubits. It is the CSS code of the classical [Hamming code](/hamming-code/) $[7, 4, 3]$: the same parity checks are used once with $Z$ to find bit flips and once with $X$ to find phase flips. As a [stabilizer code](/stabilizer-formalism/) it is $[[7, 1, 3]]$, with six check operators of weight four. It is smaller than the nine-qubit [Shor code](/shor-code/), and the logical Clifford gates $H$, $S$ and CNOT are applied qubit by qubit (transversally), which made it the standard example of fault-tolerant computation.

## Definition

**The classical code.** Let $H$ be the parity-check matrix of the $[7, 4, 3]$ Hamming code in Hamming's layout, with column $j$ the binary form of $j$ and the top row the most significant bit, as on [Hamming code](/hamming-code/):

$$H = \begin{pmatrix} 0&0&0&1&1&1&1 \\ 0&1&1&0&0&1&1 \\ 1&0&1&0&1&0&1 \end{pmatrix}.$$

Position $j \in \{1, \ldots, 7\}$ is qubit $j - 1$. The rows of $H$ span the [dual code](/dual-code/) $C^\perp$, the $[7, 3, 4]$ [simplex code](/simplex-code/); its 8 words have weights $0$ and $4$. The Hamming code $C$ contains $C^\perp$, and $C \setminus C^\perp$ is one coset, $C^\perp + 1111111$, whose words have weights $3$ and $7$.

**Codewords.** The Steane code is spanned by

$$|0_L\rangle = \frac{1}{\sqrt 8} \sum_{c \in C^\perp} |c\rangle, \qquad |1_L\rangle = \frac{1}{\sqrt 8} \sum_{c \in C^\perp} |c \oplus 1111111\rangle.$$

**Stabilizer.** For each row $h$ of $H$ take $X^{h}$ (an $X$ on each qubit where $h$ has a 1) and $Z^{h}$:

| row of $H$ (positions) | qubits | $X$ check | $Z$ check |
|---|---|---|---|
| 4, 5, 6, 7 | 3, 4, 5, 6 | $X_3X_4X_5X_6$ | $Z_3Z_4Z_5Z_6$ |
| 2, 3, 6, 7 | 1, 2, 5, 6 | $X_1X_2X_5X_6$ | $Z_1Z_2Z_5Z_6$ |
| 1, 3, 5, 7 | 0, 2, 4, 6 | $X_0X_2X_4X_6$ | $Z_0Z_2Z_4Z_6$ |

An $X$ check and a $Z$ check overlap on an even number of qubits, because two rows of $H$ are orthogonal over $\mathrm{GF}(2)$, so all six commute. With $7 - 1 = 6$ generators the code has dimension 2. The $Z$ checks are $+1$ on every $|c\rangle$ with $c \in C$, and the $X$ checks permute the terms of the sums inside $C^\perp$ and its coset, so both codewords are fixed. The logical operators are $\bar X = X^{\otimes 7}$ and $\bar Z = Z^{\otimes 7}$, or any of their products with checks; $X_0X_1X_2$ (positions 1, 2, 3, a weight-3 Hamming codeword) is a logical $\bar X$ of the smallest weight, so the distance is $d = 3$.

**Decoding.** Measure the six checks.

- The three $Z$ checks see $X$ errors. An $X$ on position $j$ flips exactly the checks whose row has a 1 in column $j$, so the three bits, read as a binary number with the top row first, are $j$ itself, exactly as in classical [syndrome decoding](/syndrome-decoding/) of the Hamming code. Apply $X$ to position $j$.
- The three $X$ checks see $Z$ errors in the same way, and give the position of the $Z$ error.
- A $Y$ error gives the same position in both halves, and gets both corrections.

The 21 one-qubit Pauli errors and the identity have 22 different syndromes, so the code is nondegenerate for them. By the discretization of errors (see [quantum error correction](/quantum-error-correction/)) the code corrects every error on one qubit.

**CSS codes in general.** Given classical linear codes $C_2 \subset C_1$ of length $n$, the CSS code $\mathrm{CSS}(C_1, C_2)$ has $Z$ checks from a parity-check matrix of $C_1$ and $X$ checks from a parity-check matrix of $C_2^\perp$, and encodes $\dim C_1 - \dim C_2$ qubits. It corrects $t$ errors when $C_1$ and $C_2^\perp$ both correct $t$ errors. The Steane code is $\mathrm{CSS}(C, C^\perp)$ with $C$ the Hamming code: $4 - 3 = 1$ logical qubit.

## Examples and non-examples

**One bit flip.** $X$ on qubit $4$ (position $5 = 101_2$) flips the checks of rows 1 and 3, which contain position 5: the $Z$ syndrome is $(1, 0, 1)$, the number 5. The $X$ syndrome is $(0, 0, 0)$. The decoder applies $X_4$.

**One $Y$ error.** $Y$ on qubit $2$ (position $3 = 011_2$) gives $(0, 1, 1)$ in both halves, and the decoder applies $X_2$ and $Z_2$, which is $Y_2$ up to a phase.

**Transversal Hadamard.** $H^{\otimes 7}$ maps $|0_L\rangle$ to $(|0_L\rangle + |1_L\rangle)/\sqrt 2$ and $|1_L\rangle$ to $(|0_L\rangle - |1_L\rangle)/\sqrt 2$, a logical [Hadamard](/hadamard-gate/). The reason is that the $X$ and $Z$ checks come from the same matrix, so $H^{\otimes 7}$ exchanges them and maps the code to itself.

**Transversal phase gate.** $S^{\otimes 7}$ multiplies $|c\rangle$ by $i^{|c|}$. On $|0_L\rangle$ the weights are $0$ and $4$, so the factor is $1$; on $|1_L\rangle$ they are $3$ and $7$, so the factor is $-i$. So $S^{\otimes 7}$ is the logical $S^\dagger$, and $(S^\dagger)^{\otimes 7}$ is the logical $S$.

**Transversal CNOT.** CNOT from each qubit of one block to the same qubit of another block maps $|a_L\rangle|b_L\rangle$ to $|a_L\rangle|(a \oplus b)_L\rangle$, a logical [CNOT](/cnot-gate/). With $H$ and $S$ this gives the whole [Clifford group](/clifford-group/) transversally: one fault on one physical qubit stays on one qubit of each block, which the code can correct.

**Non-example: a transversal T.** $T^{\otimes 7}$ multiplies the terms of $|0_L\rangle$ by $e^{i\pi |c|/4} \in \{1, -1\}$, and $-1$ for weight 4 breaks the code space, so it is not a logical gate. No code that detects every one-qubit error has a universal set of transversal gates (Eastin and Knill); the logical $T$ is made from magic states instead.

**Non-example: two errors.** $X_0 X_1$ (positions 1 and 2) gives the syndrome $1 \oplus 2 = 3$, the decoder applies $X_2$, and $X_0X_1X_2$ is a logical $\bar X$. The code corrects one error, not two.

### Common errors

- Using $|0000000\rangle + |1111111\rangle$ as $|0_L\rangle$. That is a GHZ state, fixed by the $Z$ checks but not by the $X$ checks. The codeword is the sum over all 8 words of the simplex code.
- Mixing up which checks find which errors. $Z$ checks detect $X$ errors and $X$ checks detect $Z$ errors.
- Reading the syndrome bits in the wrong order. With the top row of $H$ as the most significant bit, the syndrome is the position; with another order it is a permutation of it. Positions count from 1, qubits from 0.
- Taking $S^{\otimes 7}$ for the logical $S$. It is the logical $S^\dagger$.

### Implementation

The file `impl/python/steane_code.py` builds $H$, the Hamming and simplex codes, the codewords and an encoding circuit (data on qubit 2, three Hadamard gates on the pivot qubits 0, 1, 3, and CNOT gates along the rows), the six checks, the decoder that reads each half of the syndrome as a position, and a branch-by-branch correction of an arbitrary error. The tests (seeds 1101 and 1102) check: the code sizes and weights; the encoder against the definition; that the checks fix the code and commute; all 21 single-qubit Pauli errors and the identity corrected, with the syndrome read from the state and 22 distinct syndromes; random non-unitary one-qubit errors corrected in every branch; the Knill-Laflamme conditions with $c = I$; that no Pauli string of weight 1 or 2 (211 strings in all, with the identity) has a zero syndrome, while a weight-3 logical operator does; and the transversal $H$, $S$ and CNOT on the logical basis.

## Related definitions

- [Hamming code](/hamming-code/), [simplex code](/simplex-code/) and [dual code](/dual-code/): the classical codes inside the construction, with the [parity-check matrix](/parity-check-matrix/) above.
- [Shor code](/shor-code/): the nine-qubit code, also CSS, but degenerate and without a transversal Hadamard.
- [Stabilizer formalism](/stabilizer-formalism/) and [quantum error correction](/quantum-error-correction/): the general language and the correction conditions.
- [Clifford group](/clifford-group/) and [Gottesman-Knill theorem](/gottesman-knill-theorem/): the transversal gates are Clifford, so a Steane-code computation with only these gates can be simulated classically.
- [Quantum threshold theorem](/quantum-threshold-theorem/): concatenated Steane codes are the classic route to the threshold.

### History

Steane published the seven-qubit code in Physical Review Letters in 1996 and the general construction from a classical code containing its dual in the Proceedings of the Royal Society the same year. Calderbank and Shor gave the same construction independently in 1996 and showed that such codes can have a constant rate, so the family is named CSS after the three authors. Shor's 1996 paper on fault-tolerant computation and later work by Gottesman, Preskill, Aliferis and others used the transversal gates of the Steane code to build fault-tolerant circuits.

## References
