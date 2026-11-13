---
tag: BBMCQ5
kind: concept
slug: quantum-error-correction
name: Quantum error correction
aliases:
- QEC
- quantum error-correcting codes
area: quantum/quantum-primitives
level: advanced
summary: "Encode k logical qubits in n physical qubits so that measuring a syndrome finds and undoes errors without reading the data. Correcting X and Z errors corrects every error."
prereqs: [pauli-gates, quantum-measurement, quantum-channel, kraus-operators]
see_also: [stabilizer-formalism, shor-code, steane-code, quantum-threshold-theorem, no-cloning-theorem, repetition-code, syndrome-decoding, hamming-bound]
sources:
  - paper: doi:10.1103/PhysRevA.52.R2493
    title: Peter W. Shor, Scheme for reducing decoherence in quantum computer memory, Physical Review A 52, 1995, pages R2493 to R2496
    locator: the first quantum error-correcting code
  - paper: doi:10.1103/PhysRevA.55.900
    title: Emanuel Knill and Raymond Laflamme, Theory of quantum error-correcting codes, Physical Review A 55, 1997, pages 900 to 911
    locator: the error-correction conditions and the quantum Singleton bound
  - paper: doi:10.1103/PhysRevLett.77.793
    title: Andrew M. Steane, Error correcting codes in quantum theory, Physical Review Letters 77, 1996, pages 793 to 797
    locator: the seven-qubit code
  - paper: doi:10.1103/PhysRevA.54.1098
    title: A. Robert Calderbank and Peter W. Shor, Good quantum error-correcting codes exist, Physical Review A 54, 1996, pages 1098 to 1105
    locator: CSS codes and their rate
  - paper: doi:10.1103/PhysRevA.54.3824
    title: Charles H. Bennett, David P. DiVincenzo, John A. Smolin and William K. Wootters, Mixed-state entanglement and quantum error correction, Physical Review A 54, 1996, pages 3824 to 3851
    locator: the error-correction conditions found independently, and the five-qubit code
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 10, with Section 10.1 (the three-qubit codes), Section 10.2 (the Shor code), Section 10.3 and Theorem 10.1 (the error-correction conditions), Section 10.3.1 (discretization of the errors) and Section 10.5 (stabilizer codes)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 21 (error-correction and fault-tolerance), Section 21.4 (quantum error-correcting codes)
  - url: https://arxiv.org/abs/quant-ph/9705052
    title: Daniel Gottesman, Stabilizer Codes and Quantum Error Correction, PhD thesis, California Institute of Technology, 1997, arXiv:quant-ph/9705052
    locator: Chapter 2 (basics of quantum error correction) and Chapter 3 (stabilizer coding)
  - paper: doi:10.1063/1.1499754
    title: Eric Dennis, Alexei Kitaev, Andrew Landahl and John Preskill, Topological quantum memory, Journal of Mathematical Physics 43, 2002, pages 4452 to 4505
    locator: the surface code as a quantum memory
  - paper: doi:10.1038/s41586-024-08449-y
    title: Google Quantum AI and collaborators, Quantum error correction below the surface code threshold, Nature 638, 2025, pages 920 to 926, arXiv:2408.13687
    locator: the abstract (distance 7 surface code, error suppression factor 2.14 per distance step)
---

*Quantum error correction* protects quantum information by encoding $k$ logical [qubits](/qubit/) in a subspace of $n$ physical qubits, chosen so that the likely errors move the subspace to distinguishable places. A measurement of a *syndrome* then tells which error happened without telling anything about the encoded state, and a gate undoes the error. The two difficulties of the quantum case, that unknown states cannot be copied ([no-cloning theorem](/no-cloning-theorem/)) and that errors form a continuum, are solved by the syndrome measurement and by the *discretization* of errors: a code that corrects the Pauli errors $X$, $Y$ and $Z$ on a qubit corrects every error on that qubit. The Knill-Laflamme conditions say exactly which sets of errors a code can correct.

## In plain words

A classical bit can be protected by copying it three times and taking a majority vote. Qubits cannot be copied, and looking at a qubit changes it. The trick is to spread one qubit over several qubits in an entangled way, and then to ask only questions of the form "do these two qubits agree?". The answers do not reveal the stored value, so asking them does no harm. But if a qubit was disturbed, the answers show which one, and you can undo it. A small random tilt of a qubit is also fixed: asking the question forces it to become either "no error" or "one full flip", and both can be handled.

## The idea

**Codes and errors.** A *quantum code* is a subspace $C$ of the $2^n$-dimensional space of $n$ qubits, with an orthonormal basis $|0_L\rangle, \ldots$ of $2^k$ codewords. Noise is a [quantum channel](/quantum-channel/) $\mathcal{E}(\rho) = \sum_a E_a \rho E_a^\dagger$ with [Kraus operators](/kraus-operators/) $E_a$. The code *corrects* $\mathcal{E}$ when some channel $\mathcal{R}$, the *recovery*, gives $\mathcal{R}(\mathcal{E}(\rho)) = \rho$ for every [density matrix](/density-matrix/) $\rho$ supported on $C$.

### The Knill-Laflamme conditions

**Theorem (Knill and Laflamme 1997; Bennett, DiVincenzo, Smolin and Wootters 1996).** Let $P$ be the projector onto $C$. A recovery for the errors $\{E_a\}$ exists if and only if

$$P E_a^\dagger E_b P = c_{ab} P \quad\text{for all } a, b,$$

for some Hermitian matrix $(c_{ab})$, that is $\langle i_L| E_a^\dagger E_b |j_L\rangle = c_{ab}\,\delta_{ij}$ for all codewords. Two errors must not map different codewords to overlapping states ($i \ne j$ gives $0$), and every codeword must be changed by the errors in the same way ($c_{ab}$ does not depend on $i$), so the error reveals nothing about which codeword is present.

*Proof sketch* (Nielsen and Chuang, Theorem 10.1). Diagonalize $c = u\,d\,u^\dagger$ and pass to the Kraus operators $F_k = \sum_a u_{ak} E_a$, which describe the same channel. Then $P F_k^\dagger F_l P = d_{kl} P$ with $d$ diagonal. By polar decomposition $F_k P = \sqrt{d_{kk}}\, U_k P$ for a unitary $U_k$, so $F_k$ maps $C$ onto the space $U_k C$, and these spaces are orthogonal for different $k$. The recovery measures which space $P_k = U_k P U_k^\dagger$ the state is in and applies $U_k^\dagger$. Conversely, if a recovery with Kraus operators $R_l$ exists, then $R_l E_a P = \lambda_{la} P$ for scalars $\lambda_{la}$, and summing $P E_a^\dagger R_l^\dagger R_l E_b P$ over $l$ gives the condition with $c_{ab} = \sum_l \overline{\lambda_{la}} \lambda_{lb}$. $\blacksquare$

The code is *nondegenerate* for $\{E_a\}$ when the matrix $c$ is nonsingular, so that the errors move the code to linearly independent places. It is *degenerate* when $c$ is singular: then a nonzero combination of the errors acts on the code as $0$, and two different errors act the same on the code. The [Shor code](/shor-code/) is degenerate: $Z$ on two qubits of the same block does nothing to the codewords.

**Discretization.** The condition is linear in the errors: if it holds for $\{E_a\}$, it holds for every set of linear combinations of the $E_a$, with the same recovery. The four matrices $I, X, Y, Z$ span all $2 \times 2$ matrices. So a code that corrects $X$, $Y$ and $Z$ on every single qubit corrects every error on one qubit, unitary or not, small or large. The syndrome measurement projects a small rotation $\cos\theta\, I - i \sin\theta\, X_q$ onto "no error" with probability $\cos^2\theta$ or "$X_q$" with probability $\sin^2\theta$, and each case is then fixed exactly.

**Stabilizer codes and syndromes.** Most codes are [stabilizer codes](/stabilizer-formalism/): $C$ is the joint $+1$ eigenspace of $n - k$ commuting Pauli strings $g_1, \ldots, g_{n-k}$. A Pauli error $E$ commutes or anticommutes with each $g_i$, so measuring the $g_i$ on $E|\psi\rangle$ gives a fixed list of $n - k$ signs, the syndrome, and leaves $E|\psi\rangle$ unchanged. The decoder looks up the most likely error with that syndrome and applies it again. This is [syndrome decoding](/syndrome-decoding/) of a classical [linear code](/linear-code/) in a new form, with a binary $(n - k) \times 2n$ check matrix in place of a [parity-check matrix](/parity-check-matrix/). For Pauli errors the Knill-Laflamme condition says: for all pairs of correctable errors, $E_a^\dagger E_b$ is in the stabilizer group or anticommutes with some $g_i$.

**Parameters and bounds.** A code is $[[n, k, d]]$ when it encodes $k$ qubits in $n$ and every Pauli error of weight less than $d$ is detected; it then corrects $t = \lfloor (d-1)/2 \rfloor$ errors. Two bounds:

- the *quantum Singleton bound* $n - k \ge 2(d - 1)$ (Knill and Laflamme), so a code that corrects one error on one qubit needs $n \ge 5$;
- the *quantum Hamming bound* $2^{n-k} \ge \sum_{j=0}^{t} \binom{n}{j} 3^j$ for nondegenerate codes, the quantum form of the classical [Hamming bound](/hamming-bound/); with $k = 1$, $t = 1$ it also gives $n \ge 5$, and the five-qubit code meets it with equality, since $2^4 = 1 + 3 \cdot 5$.

Calderbank and Shor showed that good codes exist: CSS codes with rate $k/n \ge 1 - 2 H_2(2t/n)$ that correct $t$ errors, where $H_2$ is the binary entropy, so a constant fraction of errors can be corrected at a constant rate.

**What correction does not do.** A code does not stop errors from happening; it only removes them after the fact, and the syndrome circuits make new errors. If errors arrive faster than they are removed, or the correction circuits spread one fault to many qubits, encoding makes things worse. Fault-tolerant design and the [quantum threshold theorem](/quantum-threshold-theorem/) deal with this. A code also corrects only the errors it was designed for: two $X$ errors on the bit-flip code below become a logical error.

## Examples

**The three-qubit bit-flip code.** $|0_L\rangle = |000\rangle$, $|1_L\rangle = |111\rangle$, the quantum form of the [repetition code](/repetition-code/) and the [binary symmetric channel](/binary-symmetric-channel/) model. The syndrome is the two parities $Z_2 Z_1$ and $Z_1 Z_0$ ("do qubits 2 and 1 agree? do qubits 1 and 0 agree?"):

| error | $Z_2Z_1$ | $Z_1Z_0$ | correction |
|---|---|---|---|
| none | $+1$ | $+1$ | none |
| $X_0$ | $+1$ | $-1$ | $X_0$ |
| $X_1$ | $-1$ | $-1$ | $X_1$ |
| $X_2$ | $-1$ | $+1$ | $X_2$ |

For $\alpha|000\rangle + \beta|111\rangle$ with an $X_1$ error, the state is $\alpha|010\rangle + \beta|101\rangle$, and both parities are $-1$ on both terms, so the measurement does not disturb $\alpha$ and $\beta$. The set $\{I, X_0, X_1, X_2\}$ meets the Knill-Laflamme condition with $c = I$. A phase error $Z_0$ does not: $\langle 0_L|Z_0|0_L\rangle = 1$ but $\langle 1_L|Z_0|1_L\rangle = -1$, so $Z_0$ acts on the code as a logical $Z$.

**The three-qubit phase-flip code.** $|0_L\rangle = |{+}{+}{+}\rangle$, $|1_L\rangle = |{-}{-}{-}\rangle$ with the checks $X_2X_1$ and $X_1X_0$. It is the bit-flip code in the [Hadamard](/hadamard-gate/) basis and corrects one $Z$ error but no $X$ error.

**The Shor code.** Putting the phase-flip code outside and the bit-flip code inside gives the [Shor code](/shor-code/) $[[9, 1, 3]]$, the first code that corrects every one-qubit error.

**The Steane code.** The [Steane code](/steane-code/) $[[7, 1, 3]]$ uses the [Hamming code](/hamming-code/) $[7, 4, 3]$ for both the $X$ and the $Z$ checks; it is the smallest CSS code that corrects every one-qubit error.

**The five-qubit code.** The $[[5, 1, 3]]$ code with checks $XZZXI$ and its cyclic shifts is the smallest code that corrects every one-qubit error (see [stabilizer formalism](/stabilizer-formalism/)).

**The surface code.** Qubits on a square grid with checks on each face of four neighbouring qubits, $[[d^2, 1, d]]$ in the rotated form. Its checks are local, and its threshold under circuit noise is about $1\%$ (see [quantum threshold theorem](/quantum-threshold-theorem/)). In 2024 the Google Quantum AI group ran a distance-7 surface code in which each increase of the distance by 2 lowered the logical error per cycle by a factor of $2.14$.

### Implementation

The file `impl/python/quantum_error_correction.py` tests the Knill-Laflamme condition on a code basis and a list of errors, measures a stabilizer syndrome on a state vector with all its outcomes and probabilities, and applies a lookup-table correction. The tests (seeds 8081 to 8085) check: the bit-flip code meets the condition for $\{I, X_0, X_1, X_2\}$ with $c = I$ and fails it once $Z_0$ and $I$ are both in the set; the phase-flip code is the reverse; every single $X$ error is corrected and two $X$ errors give a logical $X$; random rotations $e^{-i\theta X_q}$ and random non-unitary Kraus operators $aI + bX_q$ are corrected in every syndrome branch; random linear combinations of correctable errors meet the condition; the syndrome probabilities do not depend on the encoded state; and the quantum Hamming bound first allows $n = 5$.

## Where it is used

- **Fault-tolerant quantum computers.** Every proposal for large-scale quantum computing encodes its qubits in a code, today usually the surface code or a quantum LDPC code, and runs the [threshold theorem](/quantum-threshold-theorem/) construction. Resource estimates for [Shor's algorithm](/shor-algorithm/) are mostly the cost of error correction.
- **Quantum memories and communication.** Codes protect stored qubits and qubits sent over noisy [quantum channels](/quantum-channel/); the same conditions describe entanglement distillation.
- **Classical simulation of error correction.** Stabilizer codes under Pauli noise are Clifford circuits, so the [Gottesman-Knill theorem](/gottesman-knill-theorem/) lets classical computers simulate them on many qubits to find thresholds and test decoders.
- **Theory.** The same ideas appear in the study of topological phases, in holography and in approximate codes.

Pitfalls: syndrome measurement replaces classical copying; correction needs fresh ancilla qubits, because entropy must leave the system; and a decoder must be fast enough to keep up with the error rate.

## References
