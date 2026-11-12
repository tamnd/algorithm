---
tag: ADQX34
kind: definition
slug: linear-code
name: Linear code
aliases:
- linear block code
area: compression-and-coding/error-correcting-codes
level: core
summary: A block code that is a k dimensional subspace of GF(q)^n. Its minimum distance is the least weight of a nonzero codeword.
prereqs: [hamming-distance, hamming-weight, linear-independence]
see_also: [generator-matrix, parity-check-matrix, systematic-code, dual-code, syndrome-decoding, minimum-distance, cyclic-code, code-based-cryptography]
sources:
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (linear codes, generator and parity check matrices, the minimum weight of a linear code, equivalent codes)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 3, Section 3.1 (introduction to linear block codes) and Section 3.3 (the minimum distance of a block code)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 2 (linear codes)
  - book: isbn:9780521782807
    title: W. Cary Huffman and Vera Pless, Fundamentals of Error-Correcting Codes, Cambridge University Press, 2003
    locator: Chapter 1 (basic concepts of linear codes)
  - paper: doi:10.1002/j.1538-7305.1956.tb02379.x
    title: David Slepian, A class of binary signaling alphabets, Bell System Technical Journal 35(1), 1956, pages 203 to 234
    locator: The group alphabets, binary codes that are closed under addition modulo 2
---

A linear code is a block code whose codewords form a linear subspace of the vector space $\mathrm{GF}(q)^n$. A code of dimension $k$ has $q^k$ codewords, so $k$ basis vectors describe it, and its minimum distance is the least [Hamming weight](/hamming-weight/) of a nonzero codeword. Almost all codes in practice are linear: the [Hamming code](/hamming-code/), [Reed-Solomon codes](/reed-solomon-code/), BCH codes, [LDPC codes](/ldpc-code/) and polar codes.

## Definition

**Notation.** $\mathrm{GF}(q)$ is the finite field with $q$ elements, where $q$ is a prime power. A word of length $n$ is a vector of $\mathrm{GF}(q)^n$, and we write vectors as rows. $\mathrm{wt}(x)$ is the number of nonzero entries of $x$, and $d(x, y)$ is the [Hamming distance](/hamming-distance/).

A **linear code** of length $n$ and dimension $k$ over $\mathrm{GF}(q)$ is a subspace $C \subseteq \mathrm{GF}(q)^n$ with $\dim C = k$. That is, $C$ is not empty, and $a x + b y \in C$ for all $x, y \in C$ and all $a, b \in \mathrm{GF}(q)$. Its elements are *codewords*. Its **minimum distance** is

$$d = \min \{\, d(x, y) : x, y \in C,\ x \ne y \,\},$$

defined when $k \ge 1$. We call $C$ an $[n, k, d]_q$ code, or an $[n, k]_q$ code when $d$ is not known. Its rate is $R = k/n$, and it corrects $t = \lfloor (d - 1)/2 \rfloor$ errors with a nearest codeword decoder. When $q = 2$ the index is often omitted.

**Basic facts.**

1. **Size.** $|C| = q^k$. A basis $g_1, \ldots, g_k$ of $C$ gives each codeword as $m_1 g_1 + \cdots + m_k g_k$ for exactly one message $m \in \mathrm{GF}(q)^k$, because the $g_i$ are [linearly independent](/linear-independence/). The $k \times n$ matrix $G$ with rows $g_i$ is a [generator matrix](/generator-matrix/), and the encoder is $c = m G$.
2. **Minimum distance is minimum weight.** For a linear code, $d = \min \{\, \mathrm{wt}(c) : c \in C,\ c \ne 0 \,\}$. *Proof.* For $x \ne y$ in $C$, $d(x, y) = \mathrm{wt}(x - y)$ and $x - y$ is a nonzero codeword, so $d \ge$ the minimum weight. A nonzero $c \in C$ has $\mathrm{wt}(c) = d(c, 0)$ and $0 \in C$, so the minimum weight is $\ge d$. $\blacksquare$ This cuts the work from $\binom{q^k}{2}$ pairs to $q^k - 1$ words. Computing $d$ is still hard in general: see the [minimum distance problem](/minimum-distance-problem/).
3. **Translation invariance.** For each codeword $c$, the map $x \mapsto x + c$ sends $C$ onto $C$ and keeps all distances. So every codeword sees the same set of distances to the other codewords, and the probability of a decoding error on a symmetric channel does not depend on the codeword sent. A test with the all zero codeword is enough.
4. **Kernel description.** Each subspace of dimension $k$ is the set of solutions of $n - k$ independent linear equations. In matrix form, $C = \{\, c : H c^T = 0 \,\}$ for an $(n - k) \times n$ [parity-check matrix](/parity-check-matrix/) $H$ of rank $n - k$. The rows of $H$ span the [dual code](/dual-code/).
5. **Binary codes.** Over $\mathrm{GF}(2)$ the only scalars are 0 and 1, so a nonempty binary code is linear if and only if it is closed under addition modulo 2. Slepian called such codes group alphabets in 1956, and the name group code is still used.

**Equivalence.** Two codes are *permutation equivalent* when a fixed permutation of the $n$ positions maps one onto the other. Over $\mathrm{GF}(q)$ with $q > 2$ one also allows a nonzero scale factor at each position (monomial equivalence). Equivalent codes have the same $n$, $k$, $d$ and weight distribution, so most results are stated up to equivalence. Every linear code is equivalent to a [systematic code](/systematic-code/), one whose first $k$ positions carry the message.

## Examples and non-examples

**Examples.**

- **Repetition code.** $\{00 \cdots 0, 11 \cdots 1\}$ is an $[n, 1, n]_2$ code. See [repetition code](/repetition-code/).
- **Single parity check code.** The even weight words of length $n$ form an $[n, n - 1, 2]_2$ code. It is the dual of the repetition code, and it detects each single error. A [parity bit](/parity-bit/) makes a word of this code.
- **Hamming code.** The binary $[7, 4, 3]$ [Hamming code](/hamming-code/) has the generator matrix with rows $1000110$, $0100011$, $0010111$, $0001101$. Its 16 codewords have the weights $0$ (once), $3$ (7 times), $4$ (7 times) and $7$ (once), so $d = 3$ and it corrects $t = 1$ error.
- **A small code.** $C = \{0000, 1100, 0011, 1111\}$ is a $[4, 2, 2]_2$ code with basis $1100, 0011$. It is closed under addition, and its least nonzero weight is 2.
- **A ternary code.** Over $\mathrm{GF}(3)$ the rows $1011$ and $0112$ span the tetracode, a $[4, 2, 3]_3$ code with 9 codewords. All 8 nonzero codewords have weight 3.
- **Reed-Solomon codes.** The evaluations of the polynomials of degree less than $k$ at $n$ distinct points of $\mathrm{GF}(q)$ form an $[n, k, n - k + 1]_q$ code. The set is closed under linear combinations because the polynomials of degree less than $k$ are.
- **How many codes.** The number of $k$ dimensional subspaces of $\mathrm{GF}(q)^n$ is the Gaussian binomial coefficient. For $n = 7$, $k = 4$ and $q = 2$ it is $\frac{(2^7 - 1)(2^6 - 1)(2^5 - 1)}{(2^3 - 1)(2^2 - 1)(2 - 1)} = 11811$. Thirty of these are Hamming codes: the 5040 permutations of the positions give each Hamming code 168 times.

**Non-examples.**

- **No zero word.** $\{111\}$ and $\{001, 110\}$ are not linear, because a subspace holds $0$.
- **Not closed.** $\{000, 110, 011\}$ is not linear: $110 + 011 = 101$ is not in it.
- **Wrong size.** A linear code over $\mathrm{GF}(q)$ has a power of $q$ codewords. A binary code with 3 or 12 codewords is not linear.
- **Good nonlinear codes.** The Nordstrom-Robinson code has length 16, 256 codewords and minimum distance 6. Every binary linear code of length 16 and dimension 8 has $d \le 5$. So for some parameters the best codes are not linear, and a page that says "code" without "linear" may mean such a code.
- **Additive but not linear.** Over $\mathrm{GF}(4) = \{0, 1, \omega, \omega^2\}$, a code closed under addition need not be closed under multiplication by $\omega$. It is linear over $\mathrm{GF}(2)$ only. The facts above hold with $\mathrm{GF}(2)$ as the field of scalars, not with $\mathrm{GF}(4)$.
- **A CRC is linear but used for detection.** The codewords of a [cyclic redundancy check](/cyclic-redundancy-check/) form a linear code (a shortened [cyclic code](/cyclic-code/)), but a CRC receiver only checks the remainder. It does not correct errors.

## Related definitions

- [Generator matrix](/generator-matrix/) and [parity-check matrix](/parity-check-matrix/): the two matrix descriptions, $C = \{ m G \}$ and $C = \{ c : H c^T = 0 \}$.
- [Systematic code](/systematic-code/): a generator matrix of the form $[I_k \mid P]$, so that the message is a part of the codeword.
- [Dual code](/dual-code/): $C^\perp$, the words orthogonal to all of $C$, of dimension $n - k$.
- [Minimum distance](/minimum-distance/): the parameter $d$. For a linear code it is the least number of linearly dependent columns of $H$.
- [Syndrome](/syndrome/) and [syndrome decoding](/syndrome-decoding/): decoding that uses the linear structure through $s = H r^T$.
- [Cyclic code](/cyclic-code/): a linear code that is also closed under cyclic shifts.
- [MacWilliams identity](/macwilliams-identity/): the weight distribution of $C^\perp$ from that of $C$.
- [Code-based cryptography](/code-based-cryptography/): public key systems built on random-looking linear codes.

## References
