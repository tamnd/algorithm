---
tag: CCCZ0N
kind: problem
slug: modular-square-root
name: Modular square root
aliases:
- square roots modulo a prime
- square root modulo n
area: number-theory/modular-arithmetic
level: advanced
summary: Given a and n, find x with x^2 ≡ a (mod n), or decide that none exists; easy modulo a prime, and as hard as factoring modulo a composite with unknown factors.
prereqs: [quadratic-residue, legendre-symbol]
see_also: [tonelli-shanks, cipolla-algorithm, euler-criterion, hensel-lifting, chinese-remainder-theorem, rabin-cryptosystem, quadratic-residuosity-problem, nontrivial-square-root-of-one]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 3.5, Square roots modulo n (Algorithms 3.34, 3.36, 3.37 and 3.39 for a prime; Definition 3.43, Algorithm 3.44 and Fact 3.46 for a composite), and Section 2.4.3, Fact 2.140 and Example 2.141
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Springer GTM 138
    locator: Section 1.5, Computing Square Roots Modulo p
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 2.3.2, Square roots
  - paper: "Michael O. Rabin, Digitalized signatures and public-key functions as intractable as factorization, Technical Report MIT/LCS/TR-212, MIT Laboratory for Computer Science, 1979"
    locator: the proof that extracting square roots modulo n is as hard as factoring n
---

The modular square root problem asks, for integers $a$ and $n \ge 1$, for an $x$ with $x^2 \equiv a \pmod n$, or for the answer that $a$ has no square root. Modulo an odd prime $p$, a root exists exactly when $a$ is a [quadratic residue](/quadratic-residue/) or 0, and randomized algorithms such as [Tonelli-Shanks](/tonelli-shanks/) and [Cipolla's algorithm](/cipolla-algorithm/) find it with $O(\log p)$ to $O(\log^2 p)$ multiplications. Modulo a composite $n$ with known factorization, the roots modulo prime powers combine by the [Chinese remainder theorem](/chinese-remainder-theorem/). Without the factorization, finding square roots modulo $n$ is as hard as factoring $n$ (Rabin, 1979).

## In plain words

You are given a position on a clock and want a number whose square lands on it. On a clock with a prime number of positions, half of the nonzero positions have such a number and the other half do not. A quick test tells you which half a position is in. When the answer exists, there are exactly two numbers that work, and fast methods find them. On a clock whose size is a product of two large primes, there are usually four answers. If you know the two primes, you can solve the problem on each smaller clock and glue the answers. If you do not know them, nobody knows a fast method. Finding square roots there would let you find the primes.

## Definition

**Input.** An integer $a$ and a modulus $n \ge 1$.

**Output.** An $x \in \{0, \ldots, n - 1\}$ with $x^2 \equiv a \pmod n$, or "none" if no such $x$ exists.

**Number of roots.** For an odd prime $p$ and $a \not\equiv 0$, there are 0 or 2 roots, $\pm x$. For $n = p_1^{e_1} \cdots p_r^{e_r}$ with distinct odd primes and $\gcd(a, n) = 1$, a quadratic residue has exactly $2^r$ roots (HAC, Fact 2.140). Modulo $2^e$ with $e \ge 3$, an odd $a$ has 4 roots if $a \equiv 1 \pmod 8$ and none otherwise. When $\gcd(a, n) > 1$ the count can be larger: modulo 16, $x^2 \equiv 0$ has the four roots $0, 4, 8, 12$.

**Cost models.** For word-sized $n$, count multiplications modulo $n$. For a modulus of $k$ binary digits, count bit operations; one multiplication modulo $n$ costs $O(k^2)$ with schoolbook arithmetic.

## Variants

- **Prime modulus.** $n = p$ an odd prime. This is the core case; the other cases reduce to it.
- **Decision.** Decide whether a root exists. Modulo a prime, this is the [Legendre symbol](/legendre-symbol/), computed by [Euler's criterion](/euler-criterion/) or by quadratic reciprocity. Modulo $n = pq$ with unknown factors, it is the [quadratic residuosity problem](/quadratic-residuosity-problem/).
- **All roots.** List every root. With the factorization known, this is $2^r$ combinations of the roots modulo the prime powers.
- **Prime power modulus.** $n = p^e$. A root modulo $p$ with $p \nmid a$ lifts uniquely to a root modulo $p^e$ by [Hensel lifting](/hensel-lifting/).
- **Composite modulus with unknown factorization.** The case behind the [Rabin cryptosystem](/rabin-cryptosystem/).
- **Finite fields.** Square roots in $\mathbb{F}_q$ with $q = p^m$ odd use the same methods. In fields of characteristic 2, every element has exactly one root, $a^{2^{m-1}}$ (HAC, Fact 3.42).
- **General quadratic congruences.** $ax^2 + bx + c \equiv 0 \pmod p$ for odd $p \nmid a$ reduces to the square root of the discriminant $b^2 - 4ac$, by completing the square.

## Examples

| $a$ | $n$ | roots |
| --- | --- | --- |
| 2 | 7 | 3, 4 |
| 3 | 7 | none, since $3^3 \equiv -1 \pmod 7$ |
| 5 | 41 | 13, 28 |
| 12 | 13 | 5, 8, the square roots of $-1$ |
| 4 | 15 | 2, 7, 8, 13 |
| 121 | 315 | 11, 74, 101, 151, 164, 214, 241, 304 |
| 1 | 8 | 1, 3, 5, 7 |
| 17 | 32 | 7, 9, 23, 25 |
| 0 | 9 | 0, 3, 6 |

The example modulo 315 is HAC Example 2.141. Since $315 = 3^2 \cdot 5 \cdot 7$ has three distinct odd prime factors and $\gcd(121, 315) = 1$, there are $2^3 = 8$ roots. Modulo 15, the four roots of 4 are $\pm 2$ and $\pm 7$. Since $7 \not\equiv \pm 2$, the gcd $\gcd(7 - 2, 15) = 5$ is a factor of 15: this is how a square root algorithm modulo $n$ would factor $n$.

## Known algorithms

- **$p \equiv 3 \pmod 4$.** $x = a^{(p+1)/4} \bmod p$, one exponentiation (HAC, Algorithm 3.36).
- **$p \equiv 5 \pmod 8$.** Atkin's formula, one exponentiation and no nonresidue (HAC, Algorithm 3.37).
- **[Tonelli-Shanks](/tonelli-shanks/).** For any odd prime, with a quadratic nonresidue $z$: $O(\log p + s^2)$ multiplications where $2^s \parallel p - 1$, plus the search for $z$.
- **[Cipolla's algorithm](/cipolla-algorithm/).** Choose $t$ with $t^2 - a$ a nonresidue and compute a power in $\mathbb{F}_{p^2}$; $O(\log p)$ multiplications, expected $O(k^3)$ bit operations, independent of $s$ (HAC, Algorithm 3.39).
- **Factoring polynomials.** $x^2 - a$ factors over $\mathbb{F}_p$ with the [Cantor-Zassenhaus algorithm](/cantor-zassenhaus-algorithm/) or [Berlekamp's algorithm](/berlekamp-factorization/); Cipolla's method is a special case of this idea.
- **Prime powers and composites.** Lift roots modulo $p$ to $p^e$ with [Hensel lifting](/hensel-lifting/), then combine by the Chinese remainder theorem (HAC, Algorithm 3.44 for $n = pq$).
- **Schoof's deterministic algorithm.** For a fixed $a$, Schoof (1985) found square roots of $a$ modulo $p$ in deterministic time polynomial in $\log p$, by counting points on elliptic curves; the cost grows quickly with $|a|$.

## Bounds

**Prime modulus.** With randomness, square roots modulo $p$ take $O((\log p)^3)$ expected bit operations with schoolbook arithmetic, by Cipolla's algorithm (HAC, Fact 3.40), or $O((\log p)^4)$ for Tonelli-Shanks in the worst case over $s$ (HAC, Fact 3.35). The deterministic complexity is open: all general methods need a quadratic nonresidue, and no deterministic polynomial-time method to find one is known. Under the generalized Riemann hypothesis, the least nonresidue is below $2 (\ln p)^2$ (Bach, 1990), and Tonelli-Shanks with a sequential search is deterministic and polynomial.

**Composite modulus.** With the factorization of $n$, the cost is that of the prime cases plus the Chinese remainder theorem. Without it, finding square roots modulo $n$ is polynomial-time equivalent to factoring $n$ under randomized reductions (HAC, Fact 3.46). The best known methods factor $n$ first, in subexponential time.

**Lower bound.** Each method must read $a$ and $n$ and write $x$, so $\Omega(\log n)$ bit operations are needed. No better general lower bound is known.

## Reductions

- **From factoring, for composite $n$.** Pick a random $y$ coprime to $n$ and ask for a square root $x$ of $y^2 \bmod n$. If $n$ has at least two distinct odd prime factors, then with probability at least $1/2$, $x \not\equiv \pm y$, and $\gcd(x - y, n)$ is a proper factor of $n$ (Rabin, 1979).
- **To factoring.** With the factors known, solve modulo each prime power and combine with the Chinese remainder theorem.
- **To finding a nonresidue, modulo a prime.** Tonelli-Shanks needs only one nonresidue $z$ beyond deterministic arithmetic.
- **From finding a nonresidue.** Conversely, with a square root routine, start with $-1$ and take square roots repeatedly while they exist. If $p - 1 = q 2^s$ with $q$ odd and $s \ge 2$, after $s - 1$ steps this gives an element of order $2^s$, which is a nonresidue. So deterministic square roots modulo primes and deterministic nonresidue finding are equivalent.
- **To the discrete logarithm.** With a [primitive root](/primitive-root/) $g$, $a = g^i$ has the square root $g^{i/2}$ for even $i$. Tonelli-Shanks is this method restricted to the subgroup of order $2^s$.

## Applications

- **Public-key cryptography.** Decryption in the [Rabin cryptosystem](/rabin-cryptosystem/) computes square roots modulo $n = pq$ with the secret factors; its security is equivalent to factoring because of the reduction above.
- **Elliptic curves.** A point $(x, y)$ on $y^2 = x^3 + ax + b$ is stored as $x$ and one bit of $y$; recovering $y$ is a square root modulo the field prime. Hashing to a curve needs square roots too.
- **Integer factoring.** The quadratic sieve and the number field sieve find, for each prime $p$ of the factor base, the roots of $x^2 \equiv n \pmod p$ to know where to sieve.
- **Sums of two squares.** Cornacchia's algorithm writes a prime $p \equiv 1 \pmod 4$ as $x^2 + y^2$ from a square root of $-1$ modulo $p$, by a Euclid-like reduction.
- **Primality proving.** Elliptic curve primality proving computes square roots modulo the candidate to construct points on curves.
- **Identification schemes.** The Fiat-Shamir and Feige-Fiat-Shamir protocols prove knowledge of a square root modulo $n$ without revealing it.

## References
