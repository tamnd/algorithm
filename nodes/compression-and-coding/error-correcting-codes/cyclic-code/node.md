---
tag: Z6M51W
kind: definition
slug: cyclic-code
name: Cyclic code
aliases:
- cyclic linear code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: A linear code closed under cyclic shifts. It is an ideal of GF(q)[x]/(x^n - 1), so one generator polynomial g(x) that divides x^n - 1 defines it.
history:
  year: 1957
  people: [Eugene Prange, W. Wesley Peterson]
  note: Prange introduced cyclic codes in Air Force Cambridge Research Center reports in 1957 and 1958. Peterson and Brown (1961) gave the shift-register encoder and the error detection properties.
prereqs: [linear-code, generator-matrix, parity-check-matrix, polynomial-ring, polynomial-division]
see_also: [bch-code, reed-solomon-code, hamming-code, golay-code, cyclic-redundancy-check, gf2-polynomial-arithmetic, burst-errors, syndrome]
sources:
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 7 (cyclic codes as ideals, the generator and check polynomials, the zeros of a code, and the factors of x^n - 1)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 5 (cyclic codes, systematic encoding by division, the division circuit, syndrome computation and burst error detection)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 8 (cyclic codes, the generator and check polynomials, and the roots of a cyclic code)
  - paper: doi:10.1109/JRPROC.1961.287814
    title: W. W. Peterson and D. T. Brown, Cyclic codes for error detection, Proceedings of the IRE 49(1), 1961
    locator: pp. 228 to 235 (the shift-register encoder and the burst errors that a cyclic code detects)
  - paper: "E. Prange, Cyclic error-correcting codes in two symbols, Air Force Cambridge Research Center, report AFCRC-TN-57-103, 1957"
    title: Cyclic error-correcting codes in two symbols
    locator: The first definition of cyclic codes (a technical report; locator to check)
  - url: https://reveng.sourceforge.io/crc-catalogue/all.htm
    title: Greg Cook, Catalogue of parametrised CRC algorithms
    locator: Entries CRC-8/SMBUS (check 0xF4) and CRC-16/XMODEM (check 0x31C3), used in the tests
---

A cyclic code is a [linear code](/linear-code/) $C \subseteq \mathrm{GF}(q)^n$ in which each cyclic shift of a codeword is again a codeword. If we read a word as a polynomial, a cyclic code is exactly an ideal of the ring $\mathrm{GF}(q)[x]/(x^n - 1)$. So one polynomial, the generator polynomial $g(x)$, which divides $x^n - 1$, defines the whole code, and a short [shift register](/linear-feedback-shift-register/) encodes it. [Hamming codes](/hamming-code/), [Golay codes](/golay-code/), [BCH codes](/bch-code/) and [Reed-Solomon codes](/reed-solomon-code/) are cyclic, and a [CRC](/cyclic-redundancy-check/) is a shortened cyclic code that is used only to detect errors.

## Definition

**Notation.** A code is $[n, k, d]_q$: length $n$, dimension $k$, minimum distance $d$, over the field $\mathrm{GF}(q)$. Vectors are rows. The word $c = (c_0, c_1, \ldots, c_{n-1})$ is identified with the polynomial $c(x) = c_0 + c_1 x + \cdots + c_{n-1} x^{n-1}$ in $R_n = \mathrm{GF}(q)[x]/(x^n - 1)$. The [polynomial ring](/polynomial-ring/) $\mathrm{GF}(q)[x]$ is the ring of all polynomials with coefficients in $\mathrm{GF}(q)$.

**Cyclic code.** A linear code $C$ of length $n$ over $\mathrm{GF}(q)$ is *cyclic* when for each $(c_0, \ldots, c_{n-1}) \in C$ the shift $(c_{n-1}, c_0, \ldots, c_{n-2})$ is also in $C$.

In polynomial form the shift is $x\,c(x) \bmod (x^n - 1)$, because $x^n = 1$ in $R_n$. A linear code that is closed under multiplication by $x$ is closed under multiplication by each $a(x) \in R_n$. So:

> A subset $C \subseteq R_n$ is a cyclic code if and only if it is an ideal of $R_n$.

**Generator polynomial.** Let $C \ne \{0\}$ be a cyclic code, and let $g(x)$ be a monic polynomial of least degree $r$ in $C$. Then:

1. $g(x)$ is unique, and $g(x)$ divides $x^n - 1$ in $\mathrm{GF}(q)[x]$.
2. $C = \{\, m(x)\,g(x) : \deg m < n - r \,\}$, and each codeword has exactly one such $m(x)$. So $k = n - r$.
3. Conversely, each monic divisor $g(x)$ of $x^n - 1$ generates a cyclic code of dimension $n - \deg g$.

*Proof.* For $c \in C$, divide in $\mathrm{GF}(q)[x]$: $c = a g + s$ with $\deg s < r$. The product $a g$ reduced modulo $x^n - 1$ is in $C$ because $C$ is an ideal, so $s = c - a g$ is in $C$. A nonzero $s$ would contradict the minimality of $r$, so $s = 0$ and $c = a g$. Since $\deg c < n$, $\deg a < n - r$, and $a$ is unique because $\mathrm{GF}(q)[x]$ has no zero divisors. If two monic polynomials of degree $r$ were in $C$, their difference would be a nonzero element of $C$ of degree less than $r$, so $g$ is unique. Divide $x^n - 1 = a g + s$ with $\deg s < r$. In $R_n$, $s \equiv -a g$, which is in $C$, so $s = 0$. For part 3, the set of products $m g$ with $\deg m < n - \deg g$ is closed under addition, and $x\,m g \bmod (x^n - 1) = x m g - m_{k-1}(x^n - 1)$ is again a multiple of $g$ of degree less than $n$, because $g$ divides $x^n - 1$. $\square$

The rows $g(x), x g(x), \ldots, x^{k-1} g(x)$ form a [generator matrix](/generator-matrix/). It is a band matrix: each row is the row above, shifted one place.

**Check polynomial.** Let $h(x) = (x^n - 1)/g(x)$, of degree $k$. Then $c(x) \in C$ if and only if $c(x)\,h(x) \equiv 0 \pmod{x^n - 1}$. The coefficient of $x^{j}$ in $c h$, for $k \le j \le n - 1$, is $\sum_{i} c_i h_{j-i} = 0$, so the $n - k$ shifts of the reciprocal $h^*(x) = x^k h(1/x)$ are the rows of a [parity-check matrix](/parity-check-matrix/). The code generated by $h^*(x)/h(0)$ is the [dual code](/dual-code/) of $C$, so the dual of a cyclic code is cyclic.

**Systematic encoding by division.** With $r = n - k$, the encoder of the message $m(x)$ of degree less than $k$ is

$$c(x) = x^{r} m(x) - \bigl(x^{r} m(x) \bmod g(x)\bigr).$$

The word $c$ is a multiple of $g$, its top $k$ positions hold the message, and its low $r$ positions hold the check symbols. The remainder comes from an $r$-stage division register that takes one message symbol per clock, from the highest power down. This is the same register that computes a [CRC](/cyclic-redundancy-check/), and over $\mathrm{GF}(2)$ the arithmetic is the one of [GF(2) polynomial arithmetic](/gf2-polynomial-arithmetic/). The [syndrome](/syndrome/) of a received word $v$ is $s(x) = v(x) \bmod g(x)$. It is zero exactly for codewords, and $s$ depends only on the error pattern $e = v - c$.

**Zeros of the code.** Assume $\gcd(n, q) = 1$, and let $\beta$ be a primitive $n$-th root of unity in an extension field $\mathrm{GF}(q^m)$, with $n \mid q^m - 1$. Then $x^n - 1 = \prod_{j=0}^{n-1}(x - \beta^j)$ has $n$ distinct roots. The *zeros* of $C$ are the roots of $g$: a set $Z \subseteq \{0, \ldots, n-1\}$ of exponents with $g(x) = \prod_{j \in Z}(x - \beta^j)$, and

$$C = \{\, c(x) \in R_n : c(\beta^j) = 0 \text{ for each } j \in Z \,\}.$$

The set $Z$ is closed under multiplication by $q$ modulo $n$, because $g$ has its coefficients in $\mathrm{GF}(q)$. So $Z$ is a union of cyclotomic cosets, and the number of cyclic codes of length $n$ over $\mathrm{GF}(q)$ is $2^s$, where $s$ is the number of irreducible factors of $x^n - 1$ over $\mathrm{GF}(q)$.

**The BCH bound.** If $Z$ contains $\delta - 1$ consecutive exponents $b, b+1, \ldots, b + \delta - 2$ (modulo $n$), then $d \ge \delta$. The proof, a Vandermonde determinant argument, is on the [BCH code](/bch-code/) page.

**Burst detection.** If $g(0) \ne 0$ and $\deg g = n - k$, each burst of length at most $n - k$ has a nonzero syndrome. Such a burst is $e(x) = x^i b(x)$ with $b(0) \ne 0$ and $\deg b < n - k$. The polynomial $g$ is coprime to $x$, so $g \mid x^i b$ would force $g \mid b$, which is not possible for a nonzero $b$ of smaller degree. This holds also for burst patterns that wrap around the end of the word, because a cyclic shift maps a codeword to a codeword.

## Examples and non-examples

**All binary cyclic codes of length 7.** Over $\mathrm{GF}(2)$, $x^7 - 1 = (x + 1)(x^3 + x + 1)(x^3 + x^2 + 1)$, with three irreducible factors, so there are $2^3 = 8$ cyclic codes of length 7. Take $\alpha$ a root of $x^3 + x + 1$ in $\mathrm{GF}(8)$, so $\beta = \alpha$ and $n = 7$.

| $g(x)$ | $[n, k, d]$ | zeros $Z$ | the code |
|---|---|---|---|
| $1$ | $[7, 7, 1]$ | none | all words |
| $1 + x$ | $[7, 6, 2]$ | $\{0\}$ | even weight words |
| $1 + x + x^3$ | $[7, 4, 3]$ | $\{1, 2, 4\}$ | a Hamming code |
| $1 + x^2 + x^3$ | $[7, 4, 3]$ | $\{3, 5, 6\}$ | a Hamming code |
| $1 + x + x^2 + x^4$ | $[7, 3, 4]$ | $\{0, 3, 5, 6\}$ | the even weight subcode of the second Hamming code, a simplex code |
| $1 + x^2 + x^3 + x^4$ | $[7, 3, 4]$ | $\{0, 1, 2, 4\}$ | a simplex code |
| $1 + x + \cdots + x^6$ | $[7, 1, 7]$ | $\{1, \ldots, 6\}$ | the repetition code |
| $x^7 - 1$ | $[7, 0]$ | all | $\{0\}$ |

For $g = 1 + x + x^3$, the zeros $\alpha, \alpha^2$ are consecutive, so the BCH bound gives $d \ge 3$, and $d = 3$ holds.

**Systematic encoding.** Take $g(x) = 1 + x + x^3$ and the message $m(x) = 1 + x^3$, so $k = 4$ and $r = 3$. Then $x^3 m(x) = x^3 + x^6$. Modulo $g$, $x^3 \equiv x + 1$ and $x^6 \equiv (x+1)^2 = x^2 + 1$, so the remainder is $x + x^2$. Over $\mathrm{GF}(2)$, minus is plus, and

$$c(x) = x + x^2 + x^3 + x^6, \qquad c = (0, 1, 1, \,1, 0, 0, 1).$$

The last four positions are the message $(1, 0, 0, 1)$. The non-systematic encoder gives $m(x) g(x) = 1 + x + x^4 + x^6$, a different codeword of the same code. The check polynomial is $h(x) = (x^7 - 1)/g(x) = 1 + x + x^2 + x^4$.

**A CRC is the same division.** With $g(x) = x^8 + x^2 + x + 1$ (the CRC-8/SMBUS generator, poly 0x07, no reflection, init 0) and the 72 bits of the ASCII string "123456789" as $m(x)$, highest bit as highest power, the systematic remainder is 0xF4. This is the check value of CRC-8/SMBUS in the CRC catalogue. The CRC code has a length far below the period of $g$, so it is a *shortened* cyclic code: the cyclic code of length $N$, the order of $g$, restricted to the words whose top $N - n$ positions are zero.

**Non-example: a permuted Hamming code.** The $[7, 4, 3]$ code with the systematic generator rows $1000110$, $0100101$, $0010011$, $0001111$ is a Hamming code with its positions in another order. It is linear, but it is not cyclic: some shift of a codeword is not a codeword. Equivalent codes need not both be cyclic.

**Non-example: a polynomial that does not divide $x^n - 1$.** The multiples $m(x)(1 + x + x^2)$ with $\deg m < 5$ form a linear $[7, 5]$ code, but $1 + x + x^2$ does not divide $x^7 - 1$. The shift of $x^4 + x^5 + x^6$ is $1 + x^5 + x^6$, which is not a multiple of $1 + x + x^2$ (at a root $\omega$ of $1 + x + x^2$, $\omega^3 = 1$ and $1 + \omega^5 + \omega^6 = \omega^2 \ne 0$). So the code is not cyclic. The same polynomial does generate cyclic codes of lengths 3, 6, 9 and every multiple of 3.

**Count for length 15.** Over $\mathrm{GF}(2)$, $x^{15} - 1$ has five irreducible factors, of degrees 1, 2, 4, 4 and 4, so there are $2^5 = 32$ binary cyclic codes of length 15.

## Related definitions

- [Linear code](/linear-code/), [generator matrix](/generator-matrix/), [parity-check matrix](/parity-check-matrix/) and [dual code](/dual-code/): a cyclic code is a linear code with a band generator matrix, and its dual is cyclic.
- [BCH code](/bch-code/): the cyclic code with a prescribed run of consecutive zeros, and the proof of the BCH bound.
- [Reed-Solomon code](/reed-solomon-code/): the cyclic code with $n = q - 1$ and $g(x) = \prod (x - \alpha^i)$ over $\mathrm{GF}(q)$ itself.
- [Hamming code](/hamming-code/) and [Golay code](/golay-code/): binary cyclic codes in a suitable order of the positions. Punctured [Reed-Muller codes](/reed-muller-code/) are cyclic too.
- [Cyclic redundancy check](/cyclic-redundancy-check/) and [CRC generator polynomial](/crc-generator-polynomial/): the checksum pages use the same division for detection only, with shortened lengths and with the init, reflection and xorout conventions of real CRCs. This page is about the code and its correction structure.
- [Syndrome](/syndrome/) and [burst errors](/burst-errors/): the remainder $v \bmod g$ is a syndrome, and it detects each burst of length at most $n - k$.
- [Linear feedback shift register](/linear-feedback-shift-register/): the encoder and the syndrome circuit of a cyclic code are shift registers with feedback taps from $g$.

## References
