---
tag: GWSB3B
kind: problem
slug: erasure-decoding
name: Erasure decoding
aliases:
- erasure recovery
- erasure filling
area: compression-and-coding/error-correcting-codes
level: core
summary: "Fill in the lost symbols of a codeword when the decoder knows where they are. For a linear code it is a linear system: it succeeds if and only if the erased columns of H are independent."
prereqs: [linear-code, parity-check-matrix, gaussian-elimination]
see_also: [erasure-codes, binary-erasure-channel, maximum-likelihood-decoding, peeling-decoding, reed-solomon-decoding, rank, xor-gaussian-elimination, nearest-codeword-problem]
sources:
  - book: isbn:9780521852296
    title: Tom Richardson and Rüdiger Urbanke, Modern Coding Theory, Cambridge University Press, 2008
    locator: Chapter 3 (the binary erasure channel, maximum a posteriori decoding as the solution of a linear system, stopping sets and the peeling decoder)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (erasures and the correction of d - 1 erasures) and Chapter 11 (MDS codes and the recovery from any k symbols)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 7.1.5 (the binary erasure channel and its capacity 1 - ε)
  - paper: doi:10.1109/TIT.1978.1055873
    title: Elwyn R. Berlekamp, Robert J. McEliece and Henk C. A. van Tilborg, On the inherent intractability of certain coding problems, IEEE Transactions on Information Theory 24(3), 1978
    locator: The NP-completeness of maximum likelihood decoding of linear codes on the binary symmetric channel, the contrast with erasures
---

## In plain words

A message was encoded with extra symbols and sent or stored. Some symbols were lost, and the receiver knows which ones: the places are marked as empty. The task is to fill in the empty places with the values they had. All the other symbols are correct.

For the codes used in practice, each rule of the code says that some weighted sum of symbols is zero. Each rule with an empty place in it is an equation, and the empty places are the unknowns. So the task is to solve a set of equations. It has one answer when the equations pin down every unknown. If they do not, several codewords fit what was received, and no decoder can tell which one was sent.

## Definition

**Notation.** $\mathcal{C}$ is a [linear code](/linear-code/) $[n, k, d]_q$ over the field $\mathrm{GF}(q)$, with rate $R = k/n$. Vectors are rows. $G$ is a $k \times n$ [generator matrix](/generator-matrix/), so codewords are $c = mG$, and $H$ is an $(n - k) \times n$ [parity-check matrix](/parity-check-matrix/), so $H c^T = 0$ exactly for the codewords. For a set $E$ of positions, $H_E$ is the submatrix of the columns of $H$ in $E$ and $c_E$ is the restriction of $c$ to $E$.

**Channel.** On the $q$-ary erasure channel each symbol arrives intact or is replaced by the erasure mark $?$, independently with probability $\varepsilon$. For $q = 2$ this is the [binary erasure channel](/binary-erasure-channel/) BEC($\varepsilon$). The channel makes no errors, so the decoder works with hard decisions only, and the erasures are known.

**Input.** The code (given by $H$ or $G$), and a word $y \in (\mathrm{GF}(q) \cup \{?\})^n$ that comes from a codeword $c$ by erasing the positions in a set $E$, $|E| = e$. Let $S = \{0, \ldots, n-1\} \setminus E$.

**Output.** The codeword $c$ if it is the only codeword that agrees with $y$ on $S$. Otherwise a report that the pattern is not decodable (or, in the *list* form, the set of all codewords that agree with $y$).

**Theorem.** The codewords that agree with $y$ on $S$ are exactly the vectors with $c_S = y_S$ and

$$H_E\, c_E^T = -H_S\, y_S^T.$$

So they form a coset of the null space of $H_E$, and their number is $q^{\,e - \operatorname{rank}(H_E)}$. The erasure pattern is decodable, for each sent codeword, if and only if the $e$ columns of $H$ in $E$ are linearly independent. Equivalently, the columns of $G$ in $S$ have rank $k$.

*Proof.* $Hc^T = H_E c_E^T + H_S c_S^T$, so the first claim is the definition of a codeword. The system has the solution $c_E$ of the sent codeword, so its solutions form $c_E + \ker H_E$, of size $q^{\dim \ker H_E} = q^{e - \operatorname{rank} H_E}$. This is one exactly when $\operatorname{rank} H_E = e$. For the last claim, the codewords that vanish on $S$ are the vectors $mG$ with $m G_S = 0$, and also the vectors supported on $E$ in $\ker H$. The first set has $q^{k - \operatorname{rank} G_S}$ elements and the second $q^{e - \operatorname{rank} H_E}$, so the two ranks are full together. $\blacksquare$

**Maximum likelihood.** On the erasure channel, every codeword that agrees with $y$ on $S$ has the same likelihood $(1 - \varepsilon)^{n - e} \varepsilon^{e}$, and every other codeword has likelihood zero. So [maximum likelihood decoding](/maximum-likelihood-decoding/) is erasure decoding: it succeeds with certainty when the solution is unique, and otherwise it guesses among $q^{e - \operatorname{rank} H_E}$ equal candidates.

## Variants

- **Errors and erasures.** Some symbols are erased and up to $t$ others are wrong. A code with minimum distance $d$ handles every case with $2t + e < d$. For [Reed-Solomon codes](/reed-solomon-decoding/) the decoders take an erasure locator polynomial as an extra input.
- **Symbol erasures with bit-level codes.** A packet or a disk block is one symbol of many bytes. The same linear combination is applied to every byte, so one elimination serves all bytes.
- **Incremental decoding.** Symbols arrive one at a time and the decoder stops as soon as the system is solvable. This is the setting of [fountain codes](/fountain-codes/).
- **Iterative decoding.** Solve only equations with one unknown, again and again. This is the [peeling decoder](/peeling-decoding/). It is fast but fails on stopping sets even when the full system is solvable.
- **Burst erasures.** The erased positions form one run, as on a scratched disc. Cyclic codes and interleaving handle these with simple decoders.

## Examples

**Hamming code.** Let $H$ be the $3 \times 7$ binary matrix whose column $j$ is the binary form of $j + 1$, with the least significant bit in the top row. This is the [Hamming code](/hamming-code/) $[7, 4, 3]_2$. Take $c = (1, 1, 1, 0, 0, 0, 0)$ and erase positions 0, 3 and 5:

$$y = (?, 1, 1, ?, 0, ?, 0).$$

The known part gives $H_S y_S^T$ = column 1 + column 2 = binary $2 \oplus 3 = 1$. The erased columns are the binary forms of 1, 4 and 6, and $c_0 \cdot 1 \oplus c_3 \cdot 4 \oplus c_5 \cdot 6 = 1$ forces $c_0 = 1$, $c_3 = c_5 = 0$. Now erase positions 0, 1 and 2 instead. Their columns are 1, 2 and 3, and $1 \oplus 2 \oplus 3 = 0$, so they are dependent: both $c$ and the zero word fit, and no decoder can choose. Over all patterns, the Hamming code corrects all $\binom{7}{2} = 21$ patterns of 2 erasures, 28 of the 35 patterns of 3 erasures (it fails on the 7 supports of weight-3 codewords), and no pattern of 4 or more, because $H_E$ has only 3 rows.

**Reed-Solomon codes.** A Reed-Solomon code is MDS, so each $n - k$ columns of $H$ are independent and every pattern of up to $n - k$ erasures is decodable. The tests check all $\binom{8}{4} = 70$ patterns of 4 erasures for an $[8, 4, 5]_{13}$ code, and that each pattern of 5 erasures fails. For these codes erasure decoding is [polynomial interpolation](/polynomial-interpolation/) through the $k$ or more points that are left.

**Random codes.** For a random binary $r \times e$ matrix $H_E$, the probability that it has rank $e$ is

$$\prod_{i=0}^{e-1} \bigl(1 - 2^{\,i - r}\bigr) \ \ge\ 1 - 2^{\,e - r}.$$

With $r = n - k = 10$ checks and $e = 8$ erasures this is about $0.771$. So a random linear code fails with probability about $2^{-(n - k - e)}$, which is small once the number of checks exceeds the number of erasures by a margin.

## Known algorithms

- **[Gaussian elimination](/gaussian-elimination/).** Compute the syndrome $s = -H_S y_S^T$ in $O((n - k)\, n)$ field operations and solve $H_E c_E^T = s$ in $O((n - k)\, e^2)$. Over $\mathrm{GF}(2)$, [XOR Gaussian elimination](/xor-gaussian-elimination/) on machine words divides the cost by the word length. This is the maximum likelihood decoder for each linear code.
- **Solve with the generator.** Find $k$ independent columns among those in $S$ and invert the $k \times k$ submatrix of $G$. For a systematic code with few erased data symbols, only those need solving.
- **Interpolation for Reed-Solomon codes.** [Lagrange interpolation](/lagrange-interpolation/) through $k$ known points in $O(k^2)$ operations, or $O(n \log^2 n)$ with fast polynomial arithmetic.
- **Closed forms.** RAID 6 rebuilds two lost blocks with a fixed formula per pair of positions (see [erasure codes](/erasure-codes/)).
- **Peeling.** On sparse codes such as [LDPC codes](/ldpc-code/) and [LT codes](/lt-codes/), the [peeling decoder](/peeling-decoding/) runs in time linear in the number of edges of the [Tanner graph](/tanner-graph/). It decodes exactly when the erased set contains no stopping set.
- **Inactivation decoding.** Peel until stuck, declare a few unknowns as *inactive*, keep peeling, then solve a small dense system for the inactive unknowns. This is maximum likelihood with a cost close to peeling. RaptorQ (RFC 6330) uses it.

## Bounds

- **Counting.** $H_E$ has $n - k$ rows, so $e \le n - k$ is necessary for unique decoding. Every pattern with $e \le d - 1$ is decodable, and some pattern with $e = d$ is not (the support of a codeword of weight $d$). MDS codes reach $e = n - k$ for every pattern.
- **Capacity.** The capacity of the $q$-ary erasure channel is $1 - \varepsilon$ symbols per use (Cover and Thomas, Section 7.1.5 for $q = 2$). Codes of rate $R > 1 - \varepsilon$ fail with probability tending to 1, because $e$ exceeds $n - k$ with high probability. Random linear codes of each rate $R < 1 - \varepsilon$ succeed with probability tending to 1, by the bound above.
- **Time.** For a general linear code the problem is as hard as solving a linear system (see Reductions), so $O(n^{\omega})$ with fast matrix multiplication is the best known general bound. Structured codes do better: Reed-Solomon codes in $O(n \log^2 n)$, and sparse codes in $O(n)$ when peeling works.

## Reductions

- **Erasure decoding is a linear system.** The theorem above reduces it to solving $H_E x^T = s$, so any solver for [linear systems over a finite field](/linear-system-modulo-2/) decodes erasures.
- **A linear system is erasure decoding.** Given a system $A x^T = b^T$ over $\mathrm{GF}(q)$ with $e$ unknowns, let $H = [\, A \mid -b^T \,]$, take the code $\ker H$ of length $e + 1$, and erase the first $e$ positions of the word $(?, \ldots, ?, 1)$. The completions are exactly the solutions $x$. So the two problems have the same complexity up to the cost of writing the input.
- **Contrast with errors.** Maximum likelihood decoding of a linear code on the binary symmetric channel is NP-hard (Berlekamp, McEliece and van Tilborg 1978), and so is the [nearest codeword problem](/nearest-codeword-problem/). With erasures, where the positions of the damage are known, the problem drops to polynomial time.

## Applications

- Rebuilding failed disks in RAID and in distributed storage systems that use [erasure codes](/erasure-codes/).
- Recovering lost packets with packet-level forward error correction and [fountain codes](/fountain-codes/).
- The inner step of decoders for concatenated and product codes, where a failed inner decoding becomes an erasure for the outer code.
- The analysis of codes on the binary erasure channel, where exact thresholds of [LDPC codes](/ldpc-code/) and [polar codes](/polar-code/) are known.

## References

- Tom Richardson and Rüdiger Urbanke, Modern Coding Theory, Cambridge University Press, 2008, Chapter 3.
- F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977.
- Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006.
- E. R. Berlekamp, R. J. McEliece and H. C. A. van Tilborg, "On the inherent intractability of certain coding problems", IEEE Transactions on Information Theory 24(3), 1978.
