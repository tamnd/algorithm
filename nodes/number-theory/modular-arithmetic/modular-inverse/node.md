---
tag: 3KEZYN
kind: problem
slug: modular-inverse
name: Modular inverse
aliases:
- multiplicative inverse mod n
area: number-theory/modular-arithmetic
level: intro
summary: Find x with a·x ≡ 1 (mod n), which exists exactly when gcd(a, n) = 1.
prereqs: [congruence, greatest-common-divisor, bezouts-identity]
see_also: [extended-euclidean-algorithm, batch-modular-inverse, fermat-little-theorem, linear-congruence, chinese-remainder-theorem, multiplicative-group-modulo-n, montgomery-multiplication, coprime-integers]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.3, Modular arithmetic, and Section 31.4, Solving modular linear equations (the inverse as the case b = 1 of a modular linear equation)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.3 (Definition 2.115 and Fact 2.117, an inverse exists if and only if gcd(a, n) = 1), Algorithm 2.142, and Note 14.64 (inverses by the binary extended gcd)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 2.1.1, Greatest common divisor and inverse
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 2.5, Modular division and inversion (and 2.5.1, Several inversions at once)
---

The modular inverse problem asks, for an integer $a$ and a modulus $n \ge 1$, for an integer $x$ with $ax \equiv 1 \pmod n$, or for a proof that none exists. An inverse exists exactly when $a$ and $n$ are [coprime](/coprime-integers/), and then it is unique modulo $n$. The [extended Euclidean algorithm](/extended-euclidean-algorithm/) finds it in $O(\log n)$ division steps, as a coefficient of [Bézout's identity](/bezouts-identity/). Inverses are how division is done with [congruences](/congruence/): they appear in RSA key generation, the [Chinese remainder theorem](/chinese-remainder-theorem/), binomial coefficients modulo a prime and [Montgomery multiplication](/montgomery-multiplication/).

## In plain words

In clock arithmetic you can add, subtract and multiply, but you cannot always divide. Dividing by a number means multiplying by its inverse: a second number that, multiplied by the first, gives one on the clock. On a clock with eleven hours, three times four is twelve, which is one, so four is the inverse of three. On a clock with nine hours, six has no inverse: every multiple of six lands on zero, three or six, never on one. The rule is that an inverse exists exactly when the number and the clock size share no common factor. The usual way to find it is a small extension of Euclid's method for the greatest common divisor.

## Definition

**Input.** An integer $a$ and an integer $n \ge 1$.

**Output.** The integer $x$ with $0 \le x < n$ and $ax \equiv 1 \pmod n$, written $a^{-1} \bmod n$, if it exists; otherwise the answer "no inverse", often with $g = \gcd(a, n)$ as the certificate.

**Theorem (existence and uniqueness).** An integer $x$ with $ax \equiv 1 \pmod n$ exists if and only if $\gcd(a, n) = 1$. If it exists, the set of all such integers is one residue class modulo $n$.

*Proof.* If $ax \equiv 1 \pmod n$, then $ax - 1 = ny$ for an integer $y$, so $ax - ny = 1$. Each common divisor of $a$ and $n$ divides the left side, hence divides $1$, so $\gcd(a, n) = 1$. Conversely, if $\gcd(a, n) = 1$, Bézout's identity gives integers $x, y$ with $ax + ny = 1$, and then $ax \equiv 1 \pmod n$. For uniqueness, let $ax \equiv 1$ and $ax' \equiv 1 \pmod n$. Then $x \equiv x(ax') = (xa)x' \equiv x' \pmod n$. And each $x'' \equiv x$ is again an inverse, so the solutions form exactly one class. $\square$

**Residues and the modulus.** Residues are the integers $0, \ldots, n - 1$. For $n = 1$ there is one residue, $0$, and $0 \equiv 1 \pmod 1$, so every $a$ has the inverse $0$. For $n \ge 2$, the residues with an inverse are the units modulo $n$; there are $\varphi(n)$ of them ([Euler's totient](/euler-totient/)), and they form the [multiplicative group modulo n](/multiplicative-group-modulo-n/).

**Cost models.** For a modulus below $2^w$ on the [word RAM](/word-ram/), each division with remainder of word-sized integers costs one unit. For a modulus of $k$ binary digits in arbitrary precision, cost is in bit operations, with $M(k)$ the cost of multiplying two $k$-digit integers.

## Variants

- **Modular division.** Find $x$ with $ax \equiv b \pmod n$. If $\gcd(a, n) = 1$ the answer is $x = a^{-1}b \bmod n$. The general case is a [linear congruence](/linear-congruence/), which may have no solution or several.
- **Prime modulus.** For a prime $p$, each $a \not\equiv 0$ is invertible, and $a^{-1} \equiv a^{p-2} \pmod p$ by [Fermat's little theorem](/fermat-little-theorem/).
- **Power-of-two modulus.** For $n = 2^k$, exactly the odd $a$ are invertible. If $ax \equiv 1 \pmod{2^j}$, then $x' = x(2 - ax)$ satisfies $1 - ax' = (1 - ax)^2$, so $ax' \equiv 1 \pmod{2^{2j}}$. This Newton (or [Hensel](/hensel-lifting/)) step doubles the number of correct low digits. Since $a \cdot a \equiv 1 \pmod 8$ for each odd $a$, the start $x = a$ is correct to 3 digits, and 5 steps give an inverse modulo $2^{64}$. [Montgomery multiplication](/montgomery-multiplication/) uses this to find $-n^{-1} \bmod 2^w$.
- **Many inverses, one modulus.** The [batch modular inverse](/batch-modular-inverse/) (Montgomery's trick) inverts $m$ residues with one inversion and $3(m - 1)$ multiplications.
- **All inverses modulo a prime.** For a prime $p$, the inverses of $1, \ldots, m$ for $m < p$ follow from $\mathrm{inv}[1] = 1$ and $\mathrm{inv}[i] = -\lfloor p/i \rfloor \cdot \mathrm{inv}[p \bmod i] \bmod p$, in $O(m)$ word operations. Proof: write $p = qi + r$ with $q = \lfloor p/i \rfloor$ and $0 < r < i$ (here $r \ne 0$ because $1 < i < p$ and $p$ is prime). Then $qi + r \equiv 0$, and multiplying by $i^{-1} r^{-1}$ gives $q r^{-1} + i^{-1} \equiv 0 \pmod p$.
- **Other rings.** Inverses modulo a polynomial over a finite field, for example in $\mathrm{GF}(2^8)$ for AES, use the same theory with the [polynomial extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/).

## Examples

| $a$ | $n$ | $\gcd(a, n)$ | $a^{-1} \bmod n$ | check |
| --- | --- | --- | --- | --- |
| 3 | 11 | 1 | 4 | $3 \cdot 4 = 12 = 11 + 1$ |
| 10 | 17 | 1 | 12 | $10 \cdot 12 = 120 = 7 \cdot 17 + 1$ |
| 17 | 3120 | 1 | 2753 | $17 \cdot 2753 = 46801 = 15 \cdot 3120 + 1$ |
| 6 | 9 | 3 | none | the multiples of 6 modulo 9 are 0, 6, 3 |
| 7 | 1 | 1 | 0 | every integer is $\equiv 1 \pmod 1$ |
| 3 | $2^{64}$ | 1 | $\mathtt{0xAAAAAAAAAAAAAAAB}$ | $3 \cdot \mathtt{0xAA\ldots AB} = 2 \cdot 2^{64} + 1$ |
| $2^{64} - 1$ | $2^{64}$ | 1 | $2^{64} - 1$ | $(-1)(-1) = 1$ |

The pair $(17, 3120)$ is the textbook RSA example with primes $53$ and $61$: $3120 = 52 \cdot 60$, and $2753$ is the private exponent. The extended Euclidean algorithm gives $17 \cdot (-367) + 3120 \cdot 2 = 1$, and $-367 + 3120 = 2753$.

Modulo $p = 11$, the linear-time rule gives the inverses of $1, \ldots, 10$ as $1, 6, 4, 3, 9, 2, 8, 7, 5, 10$. For example, $\mathrm{inv}[7] = -\lfloor 11/7 \rfloor \cdot \mathrm{inv}[4] = -3 \equiv 8$, and $7 \cdot 8 = 56 = 5 \cdot 11 + 1$.

## Known algorithms

- [Extended Euclidean algorithm](/extended-euclidean-algorithm/): returns $g = \gcd(a, n)$ and $x$ with $ax \equiv g \pmod n$; the inverse is $x \bmod n$ when $g = 1$. $O(\log n)$ steps on the word RAM, $O(k^2)$ bit operations.
- [Binary GCD](/binary-gcd/), extended: shifts and subtractions only, common for an odd modulus in hardware (Handbook of Applied Cryptography, Algorithm 14.61). $O(k^2)$ bit operations.
- [Fermat's little theorem](/fermat-little-theorem/) for a prime modulus: one [modular exponentiation](/modular-exponentiation/) $a^{p-2} \bmod p$, with $O(k)$ multiplications, so $O(k \cdot M(k))$ bit operations. It is easy to make constant time.
- [Euler's theorem](/euler-theorem/) for any modulus with known [totient](/euler-totient/): $a^{-1} \equiv a^{\varphi(n) - 1} \pmod n$ when $\gcd(a, n) = 1$.
- [Half-GCD](/half-gcd/): the extended gcd, and so the inverse, in $O(M(k) \log k)$ bit operations.
- [Batch modular inverse](/batch-modular-inverse/): $m$ inverses for the cost of one inverse and $3(m - 1)$ products.

## Bounds

**Word-sized modulus.** The extended Euclidean algorithm uses at most about $\log_\varphi n + 2$ division steps by [Lamé's theorem](/lames-theorem/), where $\varphi$ is the golden ratio, so $O(\log n)$ time in the worst case and $O(1)$ words of space.

**Arbitrary precision.** The quadratic methods take $O(k^2)$ bit operations for a $k$-digit modulus, and the half-GCD takes $O(M(k) \log k)$. The inverse modulo $2^k$ by Newton steps costs $O(M(k))$, because the precision doubles at each step and the costs form a geometric series. Any algorithm must read its input, so $\Omega(k)$ is a lower bound; no higher general lower bound is known.

**Exponentiation versus Euclid.** For a prime modulus of $k$ digits, both methods take $\Theta(k)$ steps in the worst case. A Euclidean step is a division whose cost shrinks with the quotient, and the steps sum to $O(k^2)$ bit operations, while each step of the exponentiation is a full product modulo $p$, for $O(k \cdot M(k))$ in total. So the Euclidean method is faster, and the exponentiation is used when its fixed sequence of operations, which is easy to make constant time, matters more.

## Reductions

- **From the gcd.** Deciding whether an inverse exists is deciding whether $\gcd(a, n) = 1$. Computing the inverse is the extended gcd with the second coefficient dropped.
- **To linear congruences.** Every solvable [linear congruence](/linear-congruence/) $ax \equiv b \pmod n$ with $d = \gcd(a, n)$ reduces to one inverse: $x \equiv (b/d)(a/d)^{-1} \pmod{n/d}$. See the [modular linear equation solver](/modular-linear-equation-solver/).
- **Chinese remainder theorem.** Combining $x \equiv r_1 \pmod{n_1}$ and $x \equiv r_2 \pmod{n_2}$ for coprime moduli needs $n_1^{-1} \bmod n_2$, as in [Garner's algorithm](/garner-algorithm/).
- **Batch to single.** Many inverses modulo the same $n$ reduce to one inverse and multiplications, by the batch method.

## Applications

- **RSA key generation.** The private exponent is $d = e^{-1} \bmod \varphi(N)$ or $e^{-1} \bmod \lambda(N)$ in the [RSA cryptosystem](/rsa-cryptosystem/).
- **Combinatorics modulo a prime.** $\binom{m}{k} \bmod p = m! \, (k!)^{-1} ((m - k)!)^{-1} \bmod p$ for $m < p$, with factorials and inverse factorials precomputed in a table.
- **Montgomery arithmetic.** The constant $-n^{-1} \bmod 2^w$ of [Montgomery multiplication](/montgomery-multiplication/), and the conversion factor $R^{-1} \bmod n$.
- **Elliptic curves.** Adding two points in affine coordinates needs one inverse modulo $p$; projective coordinates avoid it at the cost of more multiplications.
- **Rational numbers modulo $n$.** A fraction $u/v$ with $\gcd(v, n) = 1$ maps to $uv^{-1} \bmod n$, the basis of exact linear algebra by [modular methods](/modular-methods/).

## References
