---
tag: G5ZPZ8
kind: definition
slug: reed-solomon-code
name: Reed-Solomon code
aliases:
- RS code
area: compression-and-coding/error-correcting-codes
level: core
summary: The code of the values of all polynomials of degree below k at n distinct points of GF(q). It is an [n, k, n - k + 1] code, so it meets the Singleton bound.
history:
  year: 1960
  people: [Irving S. Reed, Gustave Solomon]
  note: Reed and Solomon defined the codes in 1960 as the values of a message polynomial at all points of a finite field.
prereqs: [linear-code, minimum-distance, singleton-bound, polynomial-evaluation]
see_also: [reed-solomon-decoding, bch-code, cyclic-code, berlekamp-welch, guruswami-sudan, burst-errors, interleaving, concatenated-codes]
sources:
  - paper: doi:10.1137/0108018
    title: I. S. Reed and G. Solomon, Polynomial codes over certain finite fields, Journal of the Society for Industrial and Applied Mathematics 8(2), 1960
    locator: pp. 300 to 304 (the code as the values of a polynomial of bounded degree, and its minimum distance)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 10 (Reed-Solomon codes as BCH codes, extended and generalized forms) and Chapter 11 (MDS codes and their weight distribution)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 5 (generalized Reed-Solomon codes, the parity-check matrix and the MDS property)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 7 (nonbinary BCH codes and Reed-Solomon codes)
  - url: https://ccsds.org/Pubs/131x0b5.pdf
    title: CCSDS 131.0-B-5, TM Synchronization and Channel Coding, Recommended Standard, September 2023
    locator: Section 4.3 (parameters J = 8 and E = 16 or 8, field generator 4.3.3, code generator 4.3.4, interleaving depth 4.3.5), Annex F (dual basis transformation, Table F-1) and Annex G (coefficients of g(x))
  - paper: "ISO/IEC 18004:2006, Information technology, Automatic identification and data capture techniques, QR Code 2005 bar code symbology specification"
    title: ISO/IEC 18004:2006, Information technology, Automatic identification and data capture techniques, QR Code 2005 bar code symbology specification
    locator: Section 6.5.2 (generating the error correction codewords), Annex A (error correction generator polynomials) and Annex I.2 (encoding a QR Code symbol)
  - url: https://www.thonky.com/qr-code-tutorial/error-correction-coding
    title: Thonky.com, QR Code Tutorial, Error Correction Coding
    locator: The HELLO WORLD 1-M example (16 data codewords, 10 error correction codewords) and the generator for 10 codewords
---

A Reed-Solomon code is the set of value vectors $(f(a_1), \ldots, f(a_n))$ of all polynomials $f$ of degree less than $k$ at $n$ fixed distinct points of a finite field $\mathrm{GF}(q)$. A nonzero polynomial of degree less than $k$ has fewer than $k$ roots, so two codewords differ in at least $n - k + 1$ places, and the code meets the [Singleton bound](/singleton-bound/) with equality: it is a maximum distance separable (MDS) code. With $n = q - 1$ and the powers of a primitive element as points, the same code is a [cyclic](/cyclic-code/) [BCH code](/bch-code/) with generator $\prod (x - \alpha^i)$. Reed-Solomon codes protect deep space links (CCSDS), QR codes, optical discs, storage arrays and many other systems, usually over $\mathrm{GF}(256)$, so that one symbol is one byte.

## Definition

**Notation.** A code is $[n, k, d]_q$ with rate $R = k/n$. Vectors are rows, $c = m G$ and $H c^T = 0$. A decoder corrects $t$ errors and $e$ erasures. A word $(c_0, \ldots, c_{n-1})$ is also the polynomial $c(x) = \sum_i c_i x^i$.

**Evaluation view (Reed and Solomon, 1960).** Let $a_1, \ldots, a_n$ be distinct elements of $\mathrm{GF}(q)$, so $n \le q$, and let $1 \le k \le n$. The Reed-Solomon code is

$$\mathrm{RS}_q[n, k] = \bigl\{ \bigl(f(a_1), f(a_2), \ldots, f(a_n)\bigr) : f \in \mathrm{GF}(q)[x],\ \deg f < k \bigr\}.$$

The message is the coefficient vector $(f_0, \ldots, f_{k-1})$, and the generator matrix is the $k \times n$ Vandermonde matrix with entries $G_{j,i} = a_i^{\,j}$. A *generalized* Reed-Solomon code multiplies position $i$ by a fixed nonzero $v_i$.

**Theorem (MDS).** $\mathrm{RS}_q[n, k]$ is a linear $[n, k, n - k + 1]_q$ code.

*Proof.* The map $f \mapsto (f(a_1), \ldots, f(a_n))$ is linear. Let $f \ne 0$ with $\deg f < k$. A nonzero polynomial of degree at most $k - 1$ has at most $k - 1$ roots in a field, so at most $k - 1$ of the values are zero, and the codeword has weight at least $n - k + 1 \ge 1$. So the map is injective, the dimension is $k$, and $d \ge n - k + 1$. The [Singleton bound](/singleton-bound/) $d \le n - k + 1$ holds for every linear code, so $d = n - k + 1$. $\square$

The same argument shows that any $k$ positions of a codeword determine it, by [Lagrange interpolation](/polynomial-interpolation/). This is why a Reed-Solomon code corrects any $e \le n - k$ erasures, and any $t$ errors and $e$ erasures with $2t + e \le n - k$.

**Cyclic view (BCH view).** Let $n = q - 1$, let $\alpha$ be a primitive element of $\mathrm{GF}(q)$, and fix an integer $b$. The cyclic code with generator polynomial

$$g(x) = \prod_{i=b}^{b+n-k-1} (x - \alpha^i)$$

is a BCH code with designed distance $\delta = n - k + 1$ and $m = 1$, so each cyclotomic coset has one element and $\deg g = n - k$. Its codewords are the $c(x)$ with $c(\alpha^i) = 0$ for $i = b, \ldots, b + n - k - 1$.

**The two views agree.** Take $b = 1$ and the points $a_i = \alpha^i$ for $i = 0, \ldots, n-1$. For $f(x) = \sum_{l<k} f_l x^l$ and $c_i = f(\alpha^i)$,

$$c(\alpha^j) = \sum_{i=0}^{n-1} f(\alpha^i)\,\alpha^{ij} = \sum_{l=0}^{k-1} f_l \sum_{i=0}^{n-1} \bigl(\alpha^{l+j}\bigr)^i.$$

The inner sum is $n \cdot 1 = -1 \ne 0$ in $\mathrm{GF}(q)$ when $l + j \equiv 0 \pmod n$, and $0$ otherwise, because it is a geometric series of an $n$-th root of unity other than 1. For $1 \le j \le n - k$ and $0 \le l \le k - 1$ we have $1 \le l + j \le n - 1$, so each $c(\alpha^j)$ is zero. Both codes have dimension $k$, so they are equal. For another $b$, the same computation shows that the cyclic code is the generalized Reed-Solomon code with multipliers $v_i = \alpha^{i(1-b)}$.

**Systematic encoding.** In the cyclic view the encoder is the division of the [cyclic code](/cyclic-code/) page: $c(x) = x^{n-k} m(x) - (x^{n-k} m(x) \bmod g(x))$. The $n - k$ check symbols come from a division register with $n - k$ stages of one symbol each.

**Shortened and extended codes.** Fix the top $s$ message symbols to zero and do not send them: the result is a *shortened* $[n - s, k - s, n - k + 1]$ code, still MDS, with the same encoder and decoder. With the point 0 added, $n = q$, and with a point at infinity (the coefficient $f_{k-1}$), $n = q + 1$. These are the extended codes, also MDS.

**Weight distribution.** An MDS code has a fixed weight distribution. For $d \le w \le n$, the number of codewords of weight $w$ is

$$A_w = \binom{n}{w} \sum_{j=0}^{w-d} (-1)^j \binom{w}{j} \bigl(q^{\,w-d+1-j} - 1\bigr),$$

and $A_d = \binom{n}{d}(q - 1)$ (MacWilliams and Sloane, Chapter 11).

**Bursts.** Over $\mathrm{GF}(2^m)$, each symbol is $m$ bits. A burst of $b$ consecutive bit errors touches at most $\lceil (b - 1)/m \rceil + 1$ symbols. So a code that corrects $t$ symbols corrects every burst of up to $m(t - 1) + 1$ bits. [Interleaving](/interleaving/) of $I$ codewords, symbol by symbol, multiplies the correctable burst length by $I$.

## Examples and non-examples

**A small code.** Over $\mathrm{GF}(8)$ with $\alpha$ a root of $x^3 + x + 1$, take $n = 7$, $k = 3$ and $b = 1$. Then $d = 5$, $t = 2$, and

$$g(x) = (x - \alpha)(x - \alpha^2)(x - \alpha^3)(x - \alpha^4) = x^4 + \alpha^3 x^3 + x^2 + \alpha x + \alpha^3.$$

The message $m(x) = 1 + \alpha x + \alpha^2 x^2$ has the systematic codeword $c = (\alpha^3, \alpha^4, \alpha^5, \alpha^6, 1, \alpha, \alpha^2)$: check symbols in positions 0 to 3, the message in positions 4 to 6. In the evaluation view the same message, as $f(x) = 1 + \alpha x + \alpha^2 x^2$ at $1, \alpha, \ldots, \alpha^6$, gives $(\alpha^5, \alpha^3, \alpha^5, \alpha^6, \alpha^6, \alpha^3, 1)$, another codeword of the same code. The 512 codewords have the weights $A_0 = 1$, $A_5 = 147$, $A_6 = 147$ and $A_7 = 217$, which is the MDS formula above. Shortened by one symbol, the code is a $[6, 2, 5]_8$ code.

**CCSDS RS(255, 223).** CCSDS 131.0-B-5, Section 4.3, uses $J = 8$ bits per symbol, $n = 255$ and $E = 16$ (or $E = 8$). The field generator polynomial is $F(x) = x^8 + x^7 + x^2 + x + 1$, and with $F(\alpha) = 0$ the code generator is

$$g(x) = \prod_{j=128-E}^{127+E} \bigl(x - \alpha^{11 j}\bigr) = \sum_{i=0}^{2E} G_i x^i .$$

The element $\beta = \alpha^{11}$ is again primitive, and the roots $\beta^{112}, \ldots, \beta^{143}$ for $E = 16$ are placed symmetrically, so $g$ is self-reciprocal: $G_i = G_{2E-i}$. Annex G lists $G_0, \ldots, G_{16}$ as $\alpha^0, \alpha^{249}, \alpha^{59}, \alpha^{66}, \alpha^{4}, \alpha^{43}, \alpha^{126}, \alpha^{251}, \alpha^{97}, \alpha^{30}, \alpha^{3}, \alpha^{213}, \alpha^{50}, \alpha^{66}, \alpha^{170}, \alpha^{5}, \alpha^{24}$. The code is RS(255, 223) and corrects 16 symbol errors per codeword. The symbols on the link are in the Berlekamp dual basis, not in the polynomial basis of $\alpha$: Annex F gives the $8 \times 8$ bit matrices $T_{\alpha\ell}$ and $T_{\alpha\ell}^{-1}$ that convert a byte, and a conventional encoder sits between the two conversions. For example the conventional byte 01011001 ($\alpha^{152}$) is 11101000 in the dual basis. The interleaving depth is $I \in \{1, 2, 3, 4, 5, 8\}$ (Section 4.3.5), so a codeblock of $I$ codewords corrects any burst of up to $16 I$ consecutive symbols.

**QR codes.** ISO/IEC 18004 uses Reed-Solomon codes over $\mathrm{GF}(256)$ with the primitive polynomial $x^8 + x^4 + x^3 + x^2 + 1$ (0x11D), with $b = 0$: $g(x) = \prod_{i=0}^{r-1}(x - \alpha^i)$ for $r$ error correction codewords. For the version 1-M symbol, $n = 26$ and $k = 16$, a shortened $[26, 16, 11]$ code that can correct 5 codeword errors. The standard rates it at 4 errors, because it keeps 2 codewords as a reserve against misdecoding. The generator for $r = 10$ is

$$x^{10} + \alpha^{251} x^9 + \alpha^{67} x^8 + \alpha^{46} x^7 + \alpha^{61} x^6 + \alpha^{118} x^5 + \alpha^{70} x^4 + \alpha^{64} x^3 + \alpha^{94} x^2 + \alpha^{32} x + \alpha^{45}.$$

In the HELLO WORLD 1-M example of the Thonky QR code tutorial, the data codewords are 32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17 (first codeword = highest power), and the 10 error correction codewords are 196, 35, 39, 119, 235, 215, 231, 226, 93, 23. The two standards use different fields and different $b$, so their codes are not the same even at the same $n$ and $k$.

**Non-example: a binary code from the same idea.** Polynomials over $\mathrm{GF}(2)$ have only two points to be evaluated at, so $n \le 2$. Long binary codes come instead from the binary image of a Reed-Solomon code over $\mathrm{GF}(2^m)$, which is not MDS as a binary code, or from the subfield subcode, which is a binary [BCH code](/bch-code/).

**Non-example: repeated points.** If two of the points $a_i$ are equal, the two positions always hold the same value, and the distance argument fails. With the points $(1, 1, \alpha, \alpha^2)$ and $k = 2$, the polynomial $f(x) = x - 1$ is zero at both copies of 1, so its codeword has weight 2, less than $n - k + 1 = 3$. With distinct points the bound is exact.

## Related definitions

- [Singleton bound](/singleton-bound/): $d \le n - k + 1$ for each code; Reed-Solomon codes meet it.
- [BCH code](/bch-code/) and [cyclic code](/cyclic-code/): the cyclic view, the BCH bound and the systematic encoder.
- [Reed-Solomon decoding](/reed-solomon-decoding/): the syndrome pipeline with [Berlekamp-Massey](/berlekamp-massey/), [Chien search](/chien-search/) and the [Forney algorithm](/forney-algorithm/), or the [Berlekamp-Welch algorithm](/berlekamp-welch/) in the evaluation view.
- [List decoding](/list-decoding/) and the [Guruswami-Sudan algorithm](/guruswami-sudan/): decoding beyond half the minimum distance.
- [Reed-Muller code](/reed-muller-code/): the multivariate version of the evaluation view.
- [Concatenated codes](/concatenated-codes/), [interleaving](/interleaving/) and [burst errors](/burst-errors/): the classic use of a Reed-Solomon outer code.
- [Goppa code](/goppa-code/): an alternant code, as the binary BCH codes are, built from a generalized Reed-Solomon code.

## References
