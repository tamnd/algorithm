---
tag: DX1XMN
kind: concept
slug: gf2-polynomial-arithmetic
name: Polynomial arithmetic over GF(2)
aliases:
- binary polynomial arithmetic
- carry-less polynomial arithmetic
- arithmetic in GF(2)[x]
area: compression-and-coding/checksums
level: intro
summary: "Arithmetic on polynomials with bit coefficients, stored as bit vectors: addition is XOR, multiplication is carry-less, and division is long division by shift and XOR."
prereqs: [polynomial-long-division]
see_also: [cyclic-redundancy-check, irreducible-polynomial, rabin-irreducibility-test, linear-feedback-shift-register, clmul-crc-folding, gcm-mode, cyclic-code, necklace]
sources:
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 2, Sections 2.3 (binary field arithmetic) and 2.4 (construction of the Galois field GF(2^m))
  - book: isbn:9780521392310
    title: Rudolf Lidl and Harald Niederreiter, Finite Fields, second edition, Cambridge University Press, 1997
    locator: Chapter 3 (order of polynomials and primitive polynomials, irreducible polynomials, and the number of monic irreducible polynomials of a given degree)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6 (polynomial arithmetic, division of polynomials) and Section 4.6.2 (factorization of polynomials modulo p)
  - paper: doi:10.1137/0209024
    title: Michael O. Rabin, Probabilistic algorithms in finite fields, SIAM Journal on Computing 9(2), 1980
    locator: pp. 273 to 280 (the irreducibility test by x^(q^n) mod f and gcd conditions)
  - url: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf
    title: NIST, FIPS 197, Advanced Encryption Standard (AES), 2001
    locator: Section 4.2, Multiplication (the example {57} times {83} equals {c1} modulo x^8 + x^4 + x^3 + x + 1)
---

Polynomial arithmetic over GF(2) is arithmetic on [polynomials](/polynomial/) whose coefficients are the bits 0 and 1, with $1 + 1 = 0$. A polynomial is stored as a bit vector, bit $i$ being the coefficient of $x^i$. Then addition is XOR, multiplication is a carry-less multiply (shift and XOR), and division is [long division](/polynomial-long-division/) with XOR in place of subtraction. This arithmetic is the base of the [cyclic redundancy check](/cyclic-redundancy-check/), of [linear feedback shift registers](/linear-feedback-shift-register/), and of the finite fields $\mathrm{GF}(2^m)$ that AES, GHASH, BCH codes and Reed-Solomon codes use.

## In plain words

Write a number in binary, but read each bit as a coefficient of a power of an unknown, not as a power of two. Now change one rule: when two ones meet, there is no carry. One plus one is zero, so adding two such values is the same as XOR of their bits, and subtracting is the same as adding.

Multiplication is the schoolbook method with shifts, but the partial rows are combined with XOR, so no carry ever moves left. Division is long division: line up the divisor under the top bit of the dividend, XOR it away, and go on until what is left is shorter than the divisor. What is left is the remainder. A CRC is such a remainder, and a hardware circuit makes it with only a shift register and a few XOR gates.

## The idea

**Notation.** $\mathrm{GF}(2) = \{0, 1\}$ with addition and multiplication modulo 2. $\mathrm{GF}(2)[x]$ is the ring of polynomials $a(x) = \sum_i a_i x^i$ with $a_i \in \mathrm{GF}(2)$. We store $a(x)$ as the integer $\sum_i a_i 2^i$, so `0b1011` is $x^3 + x + 1$. We write $\deg a$ for the degree, with $\deg 0 = -1$ in the code. Below, $n$ is the degree of the operands.

### Addition

The coefficient of $x^i$ in $a + b$ is $a_i + b_i \bmod 2 = a_i \oplus b_i$. So $a + b$ is the bitwise XOR of the two words, and $a - b = a + b$ because $-1 = 1$ in $\mathrm{GF}(2)$. Each polynomial is its own negative: $a + a = 0$. This is the reason why a CRC check over a message with its own remainder gives zero.

### Carry-less multiplication

The product is $c_k = \sum_{i + j = k} a_i b_j \bmod 2$. The schoolbook method computes it as $a \cdot b = \bigoplus_{j : b_j = 1} (a \ll j)$: one shifted copy of $a$ for each 1 bit of $b$, combined with XOR. There is no carry, so the bits of the product do not interact. This is the operation of the PCLMULQDQ instruction on x86 and PMULL on ARM, which multiply two 64-bit operands into a 128-bit product. The product of degrees $n$ and $m$ has degree exactly $n + m$, because $\mathrm{GF}(2)[x]$ has no zero divisors.

### Division with remainder

For $b \neq 0$ there are unique $q, r$ with $a = q b + r$ and $\deg r < \deg b$. Long division finds them: while $\deg a \ge \deg b$, let $s = \deg a - \deg b$, set bit $s$ of $q$, and replace $a$ by $a \oplus (b \ll s)$. Each step clears the top bit of $a$, so the degree of $a$ falls by at least one, and the loop runs at most $\deg a - \deg b + 1$ times. We write $a \bmod b$ for $r$. The map $a \mapsto a \bmod b$ is linear over $\mathrm{GF}(2)$: $(a \oplus a') \bmod b = (a \bmod b) \oplus (a' \bmod b)$. Every CRC property starts from this linearity.

### Greatest common divisor and powers

The [Euclidean algorithm](/polynomial-euclidean-algorithm/) works without change: $\gcd(a, b) = \gcd(b, a \bmod b)$, and it stops at a zero remainder. Each step lowers the degree of the second argument, so it takes at most $\deg b + 1$ divisions. The power $a^e \bmod f$ comes from square and multiply with $O(\log e)$ multiplications modulo $f$. A CRC library uses it to compute $x^{8k} \bmod G$, for example in a CRC combine operation and in the folding constants of [CLMUL CRC folding](/clmul-crc-folding/).

### Irreducible and primitive polynomials

A polynomial $f$ of degree $d \ge 1$ is [irreducible](/irreducible-polynomial/) if it is not the product of two polynomials of degree at least 1. The polynomial $x^{2^d} - x$ is the product of all monic irreducible polynomials whose degree divides $d$, each one time (Lidl and Niederreiter, Chapter 3). Compare the degrees: $2^d = \sum_{k \mid d} k N(k)$, where $N(k)$ is the number of irreducible polynomials of degree $k$ over $\mathrm{GF}(2)$. [Möbius inversion](/mobius-function/) gives

$$N(d) = \frac{1}{d} \sum_{k \mid d} \mu\!\left(\frac{d}{k}\right) 2^k .$$

This is also the number of binary [Lyndon words](/lyndon-word/) of length $d$, the aperiodic [necklaces](/necklace/). So about one polynomial in $d$ of degree $d$ is irreducible.

[Rabin's test](/rabin-irreducibility-test/) decides irreducibility with the same fact: $f$ of degree $d$ is irreducible if and only if $x^{2^d} \equiv x \pmod f$ and $\gcd(x^{2^{d/q}} - x \bmod f, f) = 1$ for each prime $q$ that divides $d$. It needs $d$ squarings modulo $f$ and one gcd for each prime factor of $d$.

If $f(0) = 1$, then $x$ is invertible modulo $f$, and the *order* of $f$ is the least $e \ge 1$ with $x^e \equiv 1 \pmod f$. It exists because the powers of $x$ modulo $f$ take at most $2^d - 1$ nonzero values, so two powers agree, and $x$ can be cancelled. An irreducible $f$ of degree $d$ is *primitive* if its order is $2^d - 1$, the largest possible value. There are $\varphi(2^d - 1)/d$ primitive polynomials of degree $d$, with $\varphi$ the Euler function. The order of the generator decides which 2-bit errors a CRC detects; see [CRC generator polynomial](/crc-generator-polynomial/). This "primitive" is the finite-field notion. It is not the primitive polynomial of [content](/primitive-polynomial/) 1 over the integers.

### The field GF(2^m)

If $f$ is irreducible of degree $m$, the remainders modulo $f$ form a field with $2^m$ elements, $\mathrm{GF}(2^m) = \mathrm{GF}(2)[x]/(f)$. An element is an $m$-bit word. Addition is XOR, and multiplication is a carry-less product followed by reduction modulo $f$. If $f$ is primitive, each nonzero element is a power of $x$, which gives log and antilog tables. If $f$ is not irreducible, the remainders still form a ring, but some nonzero elements have no inverse. CRC arithmetic happens in this ring: a CRC generator need not be irreducible.

### Cost

Let $n$ bound the degrees and let $w$ be the machine word size in bits.

| operation | bit operations | with $w$-bit words |
|---|---|---|
| addition | $n + 1$ XORs | $\lceil (n+1)/w \rceil$ word XORs |
| schoolbook product | $O(n^2)$ | $O(n^2/w)$ shifts and XORs, or $O((n/w)^2)$ carry-less word multiplies |
| long division of degree $n$ by degree $m$ | $O((n - m + 1) m)$ | $O((n - m + 1) m / w)$ |
| $a^e \bmod f$, $\deg f = n$ | $O(n^2 \log e)$ | $O((n^2/w) \log e)$ |

Karatsuba multiplication also works over $\mathrm{GF}(2)$, and it is easier than over the integers, because there are no carries to fix up.

## Examples

**Addition.** $(x^3 + x + 1) + (x^2 + x) = x^3 + x^2 + 1$, that is `0b1011 XOR 0b0110 = 0b1101`.

**Multiplication.** $(x^3 + x + 1)(x^2 + 1)$, that is `0b1011` times `0b101`. The bits of `0b101` are set at positions 0 and 2, so the product is `0b1011 XOR 0b101100 = 0b100111`, which is $x^5 + x^2 + x + 1$. The integer product $11 \times 5 = 55 = $ `0b110111` is different: in the integer product, the two $x^3$ terms make a carry, and here they cancel.

**Long division.** Divide $a = x^7 + x^6 + x^5 + x^2 + x$ (`0b11100110`) by $b = x^3 + x + 1$ (`0b1011`).

| step | $a$ before | shift $s$ | $b \ll s$ | $a$ after |
|---|---|---|---|---|
| 1 | `11100110` | 4 | `10110000` | `1010110` |
| 2 | `1010110` | 3 | `1011000` | `1110` |
| 3 | `1110` | 0 | `1011` | `101` |

The quotient has bits 4, 3 and 0, so $q = x^4 + x^3 + 1$ (`0b11001`), and the remainder is $r = x^2 + 1$ (`0b101`). A check: $q \cdot b + r = $ `0b11100110`.

**GCD.** Let $a = (x^3 + x + 1)(x^2 + x + 1) = x^5 + x^4 + 1$ (`0b110001`) and $b = (x^3 + x + 1)(x + 1) = x^4 + x^3 + x^2 + 1$ (`0b11101`). The Euclidean algorithm returns $\gcd(a, b) = x^3 + x + 1$ (`0b1011`).

**GF(8).** With $f = x^3 + x + 1$, the powers of $x$ modulo $f$ are

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $x^k \bmod f$ | `001` | `010` | `100` | `011` | `110` | `111` | `101` | `001` |

All 7 nonzero elements appear before the cycle closes, so $f$ is primitive. In contrast, $x^4 + x^3 + x^2 + x + 1$ is irreducible, but $x^5 \equiv 1$ modulo it, so its order is 5 and it is not primitive.

**GF(256) of AES.** AES uses $f = x^8 + x^4 + x^3 + x + 1$ (`0x11B`). The carry-less product of `0x57` and `0x83` is `0x2B79` $= x^{13} + x^{11} + x^9 + x^8 + x^6 + x^5 + x^4 + x^3 + 1$, and its remainder modulo $f$ is `0xC1`, the example of FIPS 197. This $f$ is irreducible but not primitive: $x$ has order 51, so AES tables use the element `0x03` as the generator.

**Counts of irreducible polynomials.** The formula for $N(d)$ gives these values, and both Rabin's test and trial division over all polynomials of degree $d$ give the same counts for $d \le 10$ in the code of this page.

| $d$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $N(d)$ | 2 | 1 | 2 | 3 | 6 | 9 | 18 | 30 | 56 | 99 |

## Where it is used

- **Error detection.** A [cyclic redundancy check](/cyclic-redundancy-check/) is the remainder of the message polynomial times $x^r$ modulo a [generator polynomial](/crc-generator-polynomial/). Its guarantees, such as burst detection, come from the division algorithm and the factors of the generator.
- **Fast CRC code.** The [table-driven CRC](/table-driven-crc/) precomputes $v(x) x^r \bmod G$ for each byte $v$. [Slicing-by-8](/slicing-by-8/) precomputes $v(x) x^{r + 8k} \bmod G$. [CLMUL folding](/clmul-crc-folding/) uses carry-less multiply instructions and Barrett reduction in $\mathrm{GF}(2)[x]$.
- **Shift registers.** A [linear feedback shift register](/linear-feedback-shift-register/) computes the powers of $x$ modulo its feedback polynomial. A primitive feedback polynomial of degree $d$ gives the maximal period $2^d - 1$.
- **Finite fields $\mathrm{GF}(2^m)$.** [AES](/advanced-encryption-standard/) uses $\mathrm{GF}(2^8)$. [GCM](/gcm-mode/) authenticates with GHASH, a polynomial evaluation in $\mathrm{GF}(2^{128})$, and fast GHASH code uses the same carry-less multiply as CRC folding. [BCH codes](/bch-code/) and [Reed-Solomon codes](/reed-solomon-code/) compute in $\mathrm{GF}(2^m)$, and every binary [cyclic code](/cyclic-code/) is an ideal in $\mathrm{GF}(2)[x]/(x^N - 1)$.

The general theory over any field is on the pages on [polynomial division](/polynomial-division/) and the [polynomial gcd](/polynomial-gcd/). This page is the special case with bit coefficients, where a polynomial fits in a machine word and each operation is a few shifts and XORs.

## References
