---
tag: PV1NH2
kind: concept
slug: syndrome
name: Syndrome
aliases:
- error syndrome
- syndrome of a received word
area: compression-and-coding/error-correcting-codes
level: core
summary: The vector s = H r^T of a received word r for a linear code with parity-check matrix H. It is zero on codewords and depends only on the error.
prereqs: [parity-check-matrix]
see_also: [syndrome-decoding, standard-array, hamming-code, bch-code, error-detection, niederreiter-cryptosystem, slepian-wolf-theorem, steane-code]
sources:
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 3, Section 3.2 (syndrome and error detection) and Section 3.5 (the syndrome and the cosets of the standard array)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (the syndrome, cosets and coset leaders)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 2 (syndromes and the decoding of linear codes)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 1 (syndrome decoding of the (7,4) Hamming code)
---

The syndrome of a received word $r$ for a [linear code](/linear-code/) with [parity-check matrix](/parity-check-matrix/) $H$ is the vector $s = H r^T$. It lists the results of the parity checks. It is zero exactly when $r$ is a codeword, and it does not depend on which codeword was sent, only on the error. So a decoder can work with $n - k$ symbols instead of $n$, and with the error pattern instead of the codeword.

## In plain words

A code adds check symbols to a message, and each check says that some weighted sum of symbols must be zero. When a word arrives, the receiver computes every check. The list of results is the syndrome.

If no check fails, the word is a valid codeword. If some checks fail, the pattern of failed checks is a fingerprint of the error. The fingerprint is the same whatever message was sent, so the receiver can prepare a table of fingerprints in advance and look up the most likely error. For the Hamming code the fingerprint of a single error even spells out its position.

The fingerprint cannot tell apart two errors that differ by a valid codeword. Those errors look the same to every check.

## The idea

**Notation.** $C$ is an $[n, k, d]_q$ linear code over $\mathrm{GF}(q)$ with generator matrix $G$ ($c = m G$) and parity-check matrix $H$ of size $(n - k) \times n$ ($H c^T = 0$). Vectors are rows. The channel adds an error vector: $r = c + e$. On a binary channel, $e$ marks the flipped bits.

The **syndrome** of $r$ is

$$s = H r^T \in \mathrm{GF}(q)^{n-k}.$$

**It depends only on the error.** $H r^T = H c^T + H e^T = 0 + H e^T$. So the receiver, who does not know $c$, knows $H e^T$.

**It detects errors.** $s = 0$ if and only if $r \in C$. A nonzero syndrome means that an error occurred. A zero syndrome means that either no error occurred or the error is itself a nonzero codeword. So the undetected errors are exactly the nonzero codewords, and every error of weight $1$ to $d - 1$ is detected.

**It is a sum of columns.** If $h_j$ is column $j$ of $H$, then $s = \sum_j e_j h_j$. One error of value $a$ at position $j$ gives $s = a\, h_j$. When the columns of $H$ are nonzero and no column is a multiple of another, each single error has its own syndrome. That is the design of the [Hamming code](/hamming-code/).

**It names a coset.** Two words have the same syndrome if and only if their difference is a codeword, that is, if they lie in the same coset $r + C$. Because $H$ has rank $n - k$, every vector of $\mathrm{GF}(q)^{n-k}$ is a syndrome. So the $q^n$ words split into $q^{n-k}$ cosets of $q^k$ words each, one coset for each syndrome. A decoder that sees $s$ knows that $e$ is one of the $q^k$ words of its coset. On a [binary symmetric channel](/binary-symmetric-channel/) with $p < 1/2$, the most likely of these is one of least weight, the *coset leader*. Storing one leader per syndrome is [syndrome decoding](/syndrome-decoding/), and the table of all cosets is the [standard array](/standard-array/).

**Which $H$.** The syndrome depends on the choice of $H$: with $H' = A H$ for an invertible $A$, the syndrome becomes $A s$. The coset, and so the set of possible errors, does not change.

**Cost.** Computing $s$ takes $(n - k) n$ multiplications and additions in $\mathrm{GF}(q)$, or one addition per nonzero entry of $H$ when $H$ is sparse, as for [LDPC codes](/ldpc-code/). With $H = [-P^T \mid I_{n-k}]$, it is the received check symbols minus the check symbols that the received message part would have: $s^T = r_{\mathrm{chk}} - r_{\mathrm{msg}} P$.

## Examples

**Hamming code, one error.** Take the $[7, 4, 3]$ Hamming code with

$$H = \begin{pmatrix} 1&0&1&1&1&0&0 \\ 1&1&1&0&0&1&0 \\ 0&1&1&1&0&0&1 \end{pmatrix},$$

whose columns are $110, 011, 111, 101, 100, 010, 001$. The codeword $c = 1011100$ is sent, and bit 5 flips, so $r = 1011000$. Then $s = h_1 + h_3 + h_4 = 110 + 111 + 101 = 100$, which is column 5. The decoder flips bit 5 and gets $c$ back.

**Hamming code, two errors.** If bits 1 and 2 flip instead, $s = h_1 + h_2 = 110 + 011 = 101$, which is column 4. The syndrome of this double error equals the syndrome of a single error at position 4. A decoder for one error flips bit 4 and outputs a wrong codeword with three bit errors. The syndrome cannot tell the two patterns apart, because $1101000$ (errors at 1, 2 and 4) is a codeword.

**A code with ties.** For the $[6, 3, 3]$ code with $H$ rows $011100$, $101010$, $110001$, the seven nonzero syndromes are: the six columns, one for each single error, and $111$. The syndrome $111$ is the sum of three different pairs of columns ($h_1 + h_4$, $h_2 + h_5$, $h_3 + h_6$), so it has three error patterns of weight 2 and no pattern of weight 1. A decoder must choose one of the three.

**Error detection.** For the even weight code with $H = (1\ 1\ \cdots\ 1)$, the syndrome is the sum of all bits modulo 2, which is a [parity bit](/parity-bit/) check. It detects every odd number of flips and no even number.

**Polynomial form.** For a [cyclic code](/cyclic-code/) with generator polynomial $g(x)$, the remainder $r(x) \bmod g(x)$ plays the role of the syndrome: it is zero exactly on codewords and depends only on $e(x)$. A [cyclic redundancy check](/cyclic-redundancy-check/) receiver computes this remainder and only tests it for zero.

## Where it is used

- **Syndrome decoding.** [Syndrome decoding](/syndrome-decoding/) maps each syndrome to a stored error pattern, a table of $q^{n-k}$ entries.
- **Algebraic decoders.** The decoders of [BCH](/bch-code/) and [Reed-Solomon codes](/reed-solomon-code/) start from the power sum syndromes $S_j = r(\alpha^j)$, which are the entries of $H r^T$ for a parity-check matrix in Vandermonde form. Berlekamp-Massey then finds the error locator from them.
- **Error detection.** Memory with an error-correcting code (SECDED, built on the extended Hamming code) computes a syndrome on each read. A zero syndrome means the read is clean.
- **Iterative decoding.** [Belief propagation](/belief-propagation-decoding/) on an LDPC code stops when the syndrome of the current hard decision is zero.
- **Code-based cryptography.** In the [Niederreiter cryptosystem](/niederreiter-cryptosystem/) the ciphertext is the syndrome $H e^T$ of a secret low weight $e$. Finding $e$ from $s$ for a random-looking $H$ is the [syndrome decoding problem](/syndrome-decoding-problem/).
- **Distributed compression.** For [Slepian-Wolf](/slepian-wolf-theorem/) coding of a source with side information at the decoder, the encoder sends only the syndrome of the source block, $n - k$ symbols, and the decoder finds the word of that coset nearest to its side information.
- **Quantum error correction.** A [stabilizer](/stabilizer-formalism/) code measures syndromes without measuring the encoded data. The [Steane code](/steane-code/) uses the parity-check matrix of the $[7, 4, 3]$ Hamming code for both kinds of quantum error.

## References
