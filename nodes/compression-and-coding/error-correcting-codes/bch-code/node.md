---
tag: RQPH9G
kind: definition
slug: bch-code
name: BCH code
aliases:
- Bose-Chaudhuri-Hocquenghem code
- binary BCH code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: A cyclic code whose generator has delta - 1 consecutive powers of a root of unity as zeros. The BCH bound then gives minimum distance at least delta.
history:
  year: 1959
  people: [Alexis Hocquenghem, Raj Chandra Bose, Dijen K. Ray-Chaudhuri]
  note: Hocquenghem described the codes in 1959. Bose and Ray-Chaudhuri found the binary codes on their own in 1960.
prereqs: [cyclic-code, minimum-distance]
see_also: [reed-solomon-code, hamming-code, peterson-gorenstein-zierler, berlekamp-massey, reed-solomon-decoding, goppa-code, chien-search, singleton-bound]
sources:
  - paper: "A. Hocquenghem, Codes correcteurs d'erreurs, Chiffres 2, 1959"
    title: Codes correcteurs d'erreurs
    locator: pp. 147 to 156 (the codes defined by consecutive roots)
  - paper: doi:10.1016/S0019-9958(60)90287-4
    title: R. C. Bose and D. K. Ray-Chaudhuri, On a class of error correcting binary group codes, Information and Control 3(1), 1960
    locator: pp. 68 to 79 (binary codes that correct t errors with at most m t check bits)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 6 (binary BCH codes, the minimal polynomials and the BCH bound) and Appendix C (generator polynomials of the binary primitive BCH codes in octal; to check against the printed table)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 7 (the BCH bound) and Chapter 9 (BCH codes, their dimension and true minimum distance)
---

A BCH code is a [cyclic code](/cyclic-code/) whose generator polynomial has $\delta - 1$ consecutive powers $\beta^b, \beta^{b+1}, \ldots, \beta^{b+\delta-2}$ of a root of unity $\beta$ as zeros. The *BCH bound* then says that its [minimum distance](/minimum-distance/) is at least the designed distance $\delta$, so the code corrects $t = \lfloor (\delta - 1)/2 \rfloor$ errors. A binary BCH code of length $2^m - 1$ that corrects $t$ errors needs at most $m t$ check bits. The [Reed-Solomon codes](/reed-solomon-code/) are the BCH codes with $m = 1$, and the [Hamming codes](/hamming-code/) are the binary BCH codes with $\delta = 3$.

## Definition

**Notation.** A code is $[n, k, d]_q$ with rate $R = k/n$. A word $(c_0, \ldots, c_{n-1})$ is the polynomial $c(x) = \sum c_i x^i$, as on the [cyclic code](/cyclic-code/) page.

**Setting.** Fix a prime power $q$ and a length $n$ with $\gcd(n, q) = 1$. Let $m$ be the least integer with $n \mid q^m - 1$, and let $\beta \in \mathrm{GF}(q^m)$ have order exactly $n$. For an integer $i$, let $M_i(x)$ be the minimal polynomial of $\beta^i$ over $\mathrm{GF}(q)$: the monic polynomial of least degree with coefficients in $\mathrm{GF}(q)$ that has $\beta^i$ as a root. Its roots are $\beta^j$ for $j$ in the *cyclotomic coset* $C_i = \{ i, iq, iq^2, \ldots \} \bmod n$, so $\deg M_i = |C_i| \le m$.

**BCH code.** For integers $b \ge 0$ and $2 \le \delta \le n$, the BCH code of length $n$ and designed distance $\delta$ is the cyclic code with generator polynomial

$$g(x) = \operatorname{lcm}\bigl( M_b(x), M_{b+1}(x), \ldots, M_{b+\delta-2}(x) \bigr).$$

Equivalently, $C = \{\, c(x) : c(\beta^i) = 0 \text{ for } i = b, \ldots, b + \delta - 2 \,\}$. The code is *narrow sense* when $b = 1$, and *primitive* when $n = q^m - 1$, so that $\beta$ is a primitive element of $\mathrm{GF}(q^m)$.

**Parity-check matrix over the extension field.** The code is the set of words over $\mathrm{GF}(q)$ in the kernel of the $(\delta - 1) \times n$ matrix

$$H = \begin{pmatrix} 1 & \beta^{b} & \beta^{2b} & \cdots & \beta^{(n-1)b} \\ 1 & \beta^{b+1} & \beta^{2(b+1)} & \cdots & \beta^{(n-1)(b+1)} \\ \vdots & & & & \vdots \\ 1 & \beta^{b+\delta-2} & \beta^{2(b+\delta-2)} & \cdots & \beta^{(n-1)(b+\delta-2)} \end{pmatrix}, \qquad H c^T = 0.$$

The entries of $H c^T$ are the syndromes $S_i = c(\beta^i)$ that the [Peterson-Gorenstein-Zierler](/peterson-gorenstein-zierler/) and [Berlekamp-Massey](/berlekamp-massey/) decoders use.

**Theorem (BCH bound).** Each nonzero codeword has weight at least $\delta$. So $d \ge \delta$. This holds for each cyclic code whose zeros include $\delta - 1$ consecutive powers of an element of order $n$.

*Proof.* Let $c \ne 0$ be a codeword of weight $w$, with nonzero entries at the positions $p_1 < \cdots < p_w$. Assume $w \le \delta - 1$. Put $X_l = \beta^{p_l}$. The equations $c(\beta^i) = 0$ for $i = b, \ldots, b + w - 1$ are a subset of the defining equations, and they read

$$\sum_{l=1}^{w} c_{p_l} X_l^{\,i} = 0, \qquad i = b, \ldots, b + w - 1.$$

The matrix of this system has entries $X_l^{\,b+j}$ for $0 \le j < w$. Its determinant is $\prod_l X_l^{\,b}$ times the Vandermonde determinant $\prod_{l < l'} (X_{l'} - X_l)$. Each $X_l$ is nonzero, and the $X_l$ are distinct because the $p_l$ are distinct modulo $n$ and $\beta$ has order $n$. So the matrix is invertible, and all $c_{p_l}$ are zero. This contradicts the choice of the positions. $\square$

**Dimension.** The zeros of $g$ form the union $Z$ of the cosets $C_b, \ldots, C_{b+\delta-2}$, and $k = n - |Z| \ge n - m(\delta - 1)$. For a binary narrow-sense code with $\delta = 2t + 1$, the coset of an even $i$ is the coset of $i/2$, so only the $t$ odd indices $1, 3, \ldots, 2t - 1$ add factors, and

$$n - k \le m t.$$

This is the bound of Bose and Ray-Chaudhuri. For $q > 2$ no such halving happens in general, and the bound is $n - k \le m(\delta - 1)$. The true minimum distance can exceed $\delta$, and the largest $\delta'$ that gives the same $g$ is the *Bose distance*.

**Decoding.** A BCH code with $d \ge 2t + 1$ corrects each pattern of at most $t$ errors by the syndrome pipeline of [Reed-Solomon decoding](/reed-solomon-decoding/): syndromes, an error locator by [Berlekamp-Massey](/berlekamp-massey/) or [Peterson-Gorenstein-Zierler](/peterson-gorenstein-zierler/), roots by [Chien search](/chien-search/), and for $q > 2$ the error values by the [Forney algorithm](/forney-algorithm/). For a binary code each error value is 1, so the last step is not needed.

**Asymptotic behavior.** For a fixed relative distance $\delta / n > 0$, the rate of the primitive binary BCH codes tends to 0 as $n$ grows (MacWilliams and Sloane, Chapter 9). They are good codes for short and moderate lengths and small $t$, not an asymptotically good family.

## Examples and non-examples

**Length 15.** Let $\alpha$ be a root of $x^4 + x + 1$, a primitive element of $\mathrm{GF}(16)$, and $\beta = \alpha$. The cosets modulo 15 under doubling and their minimal polynomials are:

| coset | minimal polynomial |
|---|---|
| $C_1 = \{1, 2, 4, 8\}$ | $x^4 + x + 1$ |
| $C_3 = \{3, 6, 12, 9\}$ | $x^4 + x^3 + x^2 + x + 1$ |
| $C_5 = \{5, 10\}$ | $x^2 + x + 1$ |
| $C_7 = \{7, 14, 13, 11\}$ | $x^4 + x^3 + 1$ |

The narrow-sense primitive binary BCH codes of length 15 are:

| $\delta$ | $g(x)$ | octal | $[n, k, d]$ |
|---|---|---|---|
| 3 | $M_1 = x^4 + x + 1$ | 23 | $[15, 11, 3]$, a Hamming code |
| 5 | $M_1 M_3 = x^8 + x^7 + x^6 + x^4 + 1$ | 721 | $[15, 7, 5]$ |
| 7 | $M_1 M_3 M_5 = x^{10} + x^8 + x^5 + x^4 + x^2 + x + 1$ | 2467 | $[15, 5, 7]$ |

The octal column writes the coefficients from the highest power down, in groups of three bits, as the tables of Lin and Costello do. For $\delta = 5$ the zeros are $C_1 \cup C_3$, which contain the run $\alpha^1, \ldots, \alpha^4$. The code has $n - k = 8 = m t$ check bits for $t = 2$. For $\delta = 7$, $n - k = 10 < 12 = m t$, because $C_5$ has only 2 elements.

**Designed distance below the true distance.** The designed distance $\delta = 6$ gives $\operatorname{lcm}(M_1, \ldots, M_5) = M_1 M_3 M_5$, the same generator as $\delta = 7$, so the code has $d = 7 > 6$. With $b = 0$ and $\delta = 5$, the zeros are $\{0\} \cup C_1 \cup C_3$, the generator is $(x + 1) M_1 M_3$, and the code is the $[15, 6, 6]$ even weight subcode of the $[15, 7, 5]$ code. Here $d = 6 > \delta = 5$.

**Length 31.** With $\alpha$ a root of $x^5 + x^2 + 1$, the narrow-sense codes for $\delta = 3, 5, 7, 11, 15$ have $k = 26, 21, 16, 11, 6$ and the octal generators 45, 3551, 107657, 5423325 and 313365047. The $[31, 16]$ code has $d = 7$ exactly.

**A non-primitive code that beats the bound.** The length $n = 17$ divides $2^8 - 1$, so $\beta = \alpha^{15}$ in $\mathrm{GF}(256)$ has order 17. The coset of 1 modulo 17 is $\{1, 2, 4, 8, 16, 15, 13, 9\}$, so $M_1$ has degree 8 and the code is a $[17, 9]$ code. Its longest run of consecutive zeros has length 2, so the BCH bound gives only $d \ge 3$, but the true minimum distance is 5. The BCH bound is a lower bound, not the exact value.

**Reed-Solomon codes.** With $n = q - 1$, $m = 1$ and $\beta = \alpha$ primitive in $\mathrm{GF}(q)$, each coset has one element, so $g(x) = \prod_{i=b}^{b+\delta-2}(x - \alpha^i)$ and $n - k = \delta - 1$. Then the [Singleton bound](/singleton-bound/) gives $d \le \delta$, so $d = \delta$ exactly. These are the [Reed-Solomon codes](/reed-solomon-code/).

**Non-example: zeros without a run.** Over $\mathrm{GF}(16)$, the cyclic code of length 15 with generator $M_3 = x^4 + x^3 + x^2 + x + 1$ has 4 check bits, as the Hamming code does, but its zeros $\{3, 6, 9, 12\}$ contain no two consecutive exponents. In fact $M_3$ divides $x^5 + 1$, so $x^5 + 1$ is a codeword and $d = 2$. A set of zeros of a given size gives a distance bound only when it holds a run. The run $3, 6, 9, 12$ with step 3 does not help here, because $\alpha^3$ has order 5, not 15.

## Related definitions

- [Cyclic code](/cyclic-code/): the class of codes, with the generator polynomial, the zeros and the systematic encoder.
- [Reed-Solomon code](/reed-solomon-code/): the BCH codes over $\mathrm{GF}(q)$ with $n = q - 1$. A binary BCH code is the subfield subcode of a Reed-Solomon code over $\mathrm{GF}(2^m)$: the codewords whose symbols all lie in $\mathrm{GF}(2)$.
- [Hamming code](/hamming-code/): the binary BCH code with $\delta = 3$.
- [Goppa code](/goppa-code/): a generalization by a rational function. A narrow-sense primitive BCH code of designed distance $\delta$ is the Goppa code with $g(x) = x^{\delta - 1}$ and the inverses of the nonzero field elements as its support (MacWilliams and Sloane, Chapter 12).
- [Minimum distance](/minimum-distance/) and [Singleton bound](/singleton-bound/): the BCH bound is a lower bound on $d$ for one code. The Singleton bound is an upper bound for all codes.
- Decoders: [Peterson-Gorenstein-Zierler](/peterson-gorenstein-zierler/), [Berlekamp-Massey](/berlekamp-massey/), [Chien search](/chien-search/), [Forney algorithm](/forney-algorithm/) and the whole [Reed-Solomon decoding](/reed-solomon-decoding/) pipeline.

## References
