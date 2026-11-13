---
tag: MXZFJW
kind: definition
slug: shor-code
name: Shor code
aliases:
- nine-qubit code
area: quantum/quantum-primitives
level: advanced
summary: "The [[9, 1, 3]] code of Shor (1995), the first quantum error-correcting code: a phase-flip code of three bit-flip codes, which corrects any error on one of its nine qubits."
prereqs: [quantum-error-correction]
see_also: [steane-code, stabilizer-formalism, repetition-code, concatenated-codes, quantum-threshold-theorem, hadamard-gate, cnot-gate, syndrome-decoding]
sources:
  - paper: doi:10.1103/PhysRevA.52.R2493
    title: Peter W. Shor, Scheme for reducing decoherence in quantum computer memory, Physical Review A 52, 1995, pages R2493 to R2496
    locator: the whole paper (the nine-qubit code)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 10.1 (the three-qubit bit-flip and phase-flip codes), Section 10.2 (the Shor code) and Section 10.5.6 (the Shor code as a stabilizer code)
  - url: https://arxiv.org/abs/quant-ph/9705052
    title: Daniel Gottesman, Stabilizer Codes and Quantum Error Correction, PhD thesis, California Institute of Technology, 1997, arXiv:quant-ph/9705052
    locator: Chapter 3, section The Nine-Qubit Code Revisited
  - paper: doi:10.1103/PhysRevA.55.900
    title: Emanuel Knill and Raymond Laflamme, Theory of quantum error-correcting codes, Physical Review A 55, 1997, pages 900 to 911
    locator: the error-correction conditions, which the code meets as a degenerate code
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 21, Section 21.4 (quantum error-correcting codes)
---

The *Shor code* is the nine-qubit quantum code that Peter Shor published in 1995, the first code to protect a qubit against an arbitrary error on any one of its physical qubits. It encodes one logical qubit in nine qubits by putting a three-qubit phase-flip code on top of three three-qubit bit-flip codes, a quantum form of the [repetition code](/repetition-code/) used twice. In the language of the [stabilizer formalism](/stabilizer-formalism/) it is a $[[9, 1, 3]]$ code with eight check operators. It is *degenerate*: different errors can have the same effect on the code, which no classical code shows. Seven qubits are enough with the [Steane code](/steane-code/), and five with the five-qubit code.

## Definition

Number the qubits $0$ to $8$ and group them in three blocks $\{0, 1, 2\}$, $\{3, 4, 5\}$ and $\{6, 7, 8\}$. Qubit $0$ is the rightmost symbol in a ket and the least significant bit, as on [quantum state](/quantum-state/).

**Codewords.** The Shor code is the two-dimensional subspace spanned by

$$|0_L\rangle = \frac{(|000\rangle + |111\rangle)(|000\rangle + |111\rangle)(|000\rangle + |111\rangle)}{2\sqrt 2}, \qquad |1_L\rangle = \frac{(|000\rangle - |111\rangle)(|000\rangle - |111\rangle)(|000\rangle - |111\rangle)}{2\sqrt 2}.$$

A logical qubit $\alpha|0\rangle + \beta|1\rangle$ is stored as $\alpha|0_L\rangle + \beta|1_L\rangle$.

**Construction.** First encode with the phase-flip code, $|0\rangle \mapsto |{+}{+}{+}\rangle$ and $|1\rangle \mapsto |{-}{-}{-}\rangle$, then encode each of the three qubits with the bit-flip code, $|0\rangle \mapsto |000\rangle$ and $|1\rangle \mapsto |111\rangle$ (see [quantum error correction](/quantum-error-correction/) for both). This is a two-level [concatenated code](/concatenated-codes/). As a circuit, with the data on qubit $0$: [CNOT](/cnot-gate/) from $0$ to $3$ and from $0$ to $6$, then a [Hadamard gate](/hadamard-gate/) on qubits $0$, $3$ and $6$, then CNOT from each of $0$, $3$, $6$ to the two other qubits of its block.

**Stabilizer.** The code is the joint $+1$ eigenspace of eight commuting Pauli strings:

| generators | meaning |
|---|---|
| $Z_0 Z_1$, $Z_1 Z_2$, $Z_3 Z_4$, $Z_4 Z_5$, $Z_6 Z_7$, $Z_7 Z_8$ | the qubits of each block agree (bit-flip checks) |
| $X_0 X_1 X_2 X_3 X_4 X_5$, $X_3 X_4 X_5 X_6 X_7 X_8$ | the signs of neighbouring blocks agree (phase-flip checks) |

Here $X_0X_1X_2$ acts on block $0$ as $+1$ on $|000\rangle + |111\rangle$ and $-1$ on $|000\rangle - |111\rangle$, so the weight-six checks compare the signs of two blocks. There are $9 - 1 = 8$ generators, so the code has dimension $2^{9-8} = 2$. The logical operators are $\bar X = Z_0 Z_3 Z_6$, which swaps $|0_L\rangle$ and $|1_L\rangle$, and $\bar Z = X_0 X_1 \cdots X_8$, which fixes $|0_L\rangle$ and negates $|1_L\rangle$. The smallest weight of a logical operator is $3$, so the distance is $d = 3$ and the code corrects $t = 1$ error.

**Decoding.** Measure the eight generators to get eight syndrome bits.

- In each block, the two bits of the $Z$ checks name the qubit with an $X$ error: $(1, 0)$, $(1, 1)$ and $(0, 1)$ for the first, middle and last qubit of the block, as for the [repetition code](/repetition-code/). Apply $X$ to that qubit.
- The two bits of the $X$ checks name the block with a $Z$ error: $(1, 0)$ for block $0$, $(1, 1)$ for block $1$, $(0, 1)$ for block $2$. Apply $Z$ to any one qubit of that block.
- A $Y$ error sets both kinds of bits and gets both corrections.

The $Z$ correction does not need to hit the qubit that had the error: $Z_a$ and $Z_b$ in the same block differ by $Z_a Z_b$, which is in the stabilizer and acts as the identity on the code. By the discretization of errors, correcting $X$, $Y$ and $Z$ on each qubit corrects every one-qubit error, unitary or not.

## Examples and non-examples

**A bit flip.** The error $X_4$ on $\alpha|0_L\rangle + \beta|1_L\rangle$ makes block $1$ hold $|010\rangle \pm |101\rangle$. The checks $Z_3Z_4$ and $Z_4Z_5$ both give $-1$, the others $+1$: syndrome $(1, 1)$ in block $1$, so apply $X_4$.

**A phase flip.** The error $Z_7$ changes the sign of $|111\rangle$ in block $2$, which turns $|000\rangle + |111\rangle$ into $|000\rangle - |111\rangle$ there and back. Only $X_3 \cdots X_8$ gives $-1$: syndrome $(0, 1)$, block $2$. The decoder applies $Z_6$, and $Z_6 Z_7$ is a stabilizer, so the state is restored exactly.

**A small rotation.** The error $e^{-i\theta Y_2} = \cos\theta\, I - i\sin\theta\, Y_2$ is a superposition of "no error" and "$Y_2$". The syndrome measurement gives "no error" with probability $\cos^2\theta$ and the syndrome of $Y_2$ with probability $\sin^2\theta$, and in both cases the decoder returns the exact encoded state.

**Degeneracy.** The 28 errors $I$ and $X_q, Y_q, Z_q$ have only 22 different syndromes: in each block, $Z_a$, $Z_b$ and $Z_c$ share one. For a nondegenerate code with 8 checks and these 28 errors, 28 distinct syndromes would be needed. In the Knill-Laflamme matrix $c_{ab} = \langle 0_L|E_a^\dagger E_b|0_L\rangle$ the entry for $Z_0$ and $Z_1$ is $1$, not $0$, so $c$ is not diagonal.

**Non-example: two errors in one block.** The error $X_0 X_1$ gives the syndrome of $X_2$, the decoder applies $X_2$, and the result is $X_0X_1X_2$, a logical $\bar Z$ (it is $X$ on one block, which acts as a sign change on $|1_L\rangle$ there). Two $X$ errors in different blocks are corrected; two $Z$ errors in different blocks are not.

**Non-example: one block alone.** A single block $\alpha|000\rangle + \beta|111\rangle$ is the bit-flip code. It corrects one $X$ but no $Z$: $Z$ on any of its qubits is a logical operator.

### Common errors

- Correcting $Z$ errors on the exact qubit. It is not needed and cannot be done: the syndrome does not name the qubit inside a block, and it does not have to.
- Saying the code "copies" the qubit nine times. $\alpha|0_L\rangle + \beta|1_L\rangle$ is an entangled state, not $(\alpha|0\rangle + \beta|1\rangle)^{\otimes 9}$, which the [no-cloning theorem](/no-cloning-theorem/) forbids making.
- Measuring the qubits to compare them. The syndrome is a parity, measured with an ancilla and CNOT gates; measuring single qubits would destroy the superposition.
- Reading $[[9, 1, 3]]$ as a classical $[9, 1, 3]$ code. Double brackets mean $9$ qubits, $1$ logical qubit and distance $3$ against all Pauli errors.

### Implementation

The file `impl/python/shor_code.py` builds the codewords from the definition and with the encoding circuit, lists the eight generators and the logical operators, computes syndromes and the decoder above, and corrects an arbitrary error on one qubit by projecting onto each possible syndrome. The tests check, on random and basis encoded states (seeds 9091 and 9092): the circuit gives the codewords; the generators fix the code and commute; $\bar X$ and $\bar Z$ act as stated; all 27 single-qubit Pauli errors and the identity are corrected, with the syndrome read from the state; 28 errors give 22 syndromes; random non-unitary one-qubit errors are corrected in every branch; the Knill-Laflamme conditions hold for all 28 errors with 18 nonzero off-diagonal entries of $c$; no Pauli string of weight at most 2 (352 of them) is an undetected logical error, by [Gaussian elimination over GF(2)](/bitset-gaussian-elimination/); and two $X$ errors in one block give a logical error.

## Related definitions

- [Quantum error correction](/quantum-error-correction/): the Knill-Laflamme conditions and the discretization of errors, which the Shor code was the first to use.
- [Steane code](/steane-code/): a $[[7, 1, 3]]$ CSS code, smaller and with transversal Clifford gates. The Shor code is also a CSS code, built from the repetition code and its dual.
- [Stabilizer formalism](/stabilizer-formalism/): the eight generators and the logical operators above.
- [Repetition code](/repetition-code/) and [concatenated codes](/concatenated-codes/): the classical pieces of the construction.
- [Quantum threshold theorem](/quantum-threshold-theorem/): concatenating a code with itself many times is one route to the threshold; the Bacon-Shor subsystem code is a later form of the Shor code.

### History

Shor's 1995 paper "Scheme for reducing decoherence in quantum computer memory" gave the nine-qubit code and showed that quantum information can be protected, at a time when many doubted it because measurement disturbs a state and errors form a continuum. Steane found the seven-qubit code in 1996, Calderbank, Shor and Steane gave the general CSS construction, and Gottesman's stabilizer formalism (1996 to 1997) described the Shor code by the eight generators above.

## References
