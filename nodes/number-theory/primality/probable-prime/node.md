---
tag: J565VK
kind: definition
slug: probable-prime
name: Probable prime
aliases:
- PRP
- probable prime test result
area: number-theory/primality
level: intro
summary: An integer that passes a test which every prime passes, so that it is prime or a pseudoprime for that test.
prereqs: [prime-number, fermat-little-theorem, modular-exponentiation]
see_also: [pseudoprime, fermat-pseudoprime, strong-pseudoprime, euler-jacobi-pseudoprime, miller-rabin, primality-certificate, random-prime-generation, carmichael-number]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.4.1 (probable prime base a, Algorithm 3.4.3), Section 3.5 (strong probable prime, Algorithm 3.5.2, industrial-grade primes, Algorithm 3.5.7) and Section 3.6 (Algorithm 3.6.9, Lucas probable prime test)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Definitions 4.5 and 4.34, Fact 4.30, Section 4.4.1 (Algorithm 4.44, Fact 4.48, Note 4.49) and Note 4.64
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 10.3, Generating random primes using the Miller-Rabin test
  - paper: doi:10.1090/S0025-5718-1993-1189518-9
    title: Ivan Damgard, Peter Landrock and Carl Pomerance, Average case error estimates for the strong probable prime test, Mathematics of Computation 61 (1993)
    locator: pages 177 to 194
---

A probable prime is an integer that passes a test which every [prime](/prime-number/) passes. The test gives no proof: a probable prime is either a prime or a composite that fools the test, and such a composite is a [pseudoprime](/pseudoprime/) for that test. The common tests are the [Fermat test](/fermat-primality-test/), the Euler test of [Solovay and Strassen](/solovay-strassen/), the strong test of [Miller and Rabin](/miller-rabin/) and the Lucas test, each with a *base* or a pair of parameters. "Probable prime" names the outcome of a test, so it always goes with the test and the base that were used.

## Definition

Let $T$ be a test that takes an integer $n$ and a parameter $a$ and either accepts or rejects, and suppose that $T$ accepts each prime $n$ for each allowed parameter. An integer $n$ is a **probable prime for $T$ with parameter $a$** if $T$ accepts $(n, a)$. A composite probable prime is a **pseudoprime** for $T$ with parameter $a$. A rejection proves that $n$ is composite; an acceptance proves nothing.

The four standard cases follow. In each, $n$ and $a$ are integers with $1 < a < n - 1$, so $n \ge 4$.

- **Probable prime base $a$** (Fermat). $a^{n-1} \equiv 1 \pmod n$. Each prime $n$ satisfies this by [Fermat's little theorem](/fermat-little-theorem/), because $1 < a < n - 1$ forces $n \nmid a$. A composite that satisfies it is a [Fermat pseudoprime](/fermat-pseudoprime/) base $a$.
- **Euler probable prime base $a$**. $n$ is odd, $\gcd(a, n) = 1$ and $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$, where $\left(\frac{a}{n}\right)$ is the [Jacobi symbol](/jacobi-symbol/). Each odd prime satisfies this by [Euler's criterion](/euler-criterion/). A composite that satisfies it is an [Euler-Jacobi pseudoprime](/euler-jacobi-pseudoprime/) base $a$.
- **Strong probable prime base $a$**. $n$ is odd, $n - 1 = 2^s t$ with $t$ odd, and either $a^t \equiv 1 \pmod n$ or $a^{2^i t} \equiv -1 \pmod n$ for some $i$ with $0 \le i \le s - 1$. Each odd prime satisfies this, because in $\mathbb{Z}_n$ the only square roots of $1$ are $\pm 1$. A composite that satisfies it is a [strong pseudoprime](/strong-pseudoprime/) base $a$.
- **Lucas probable prime with parameters $(a, b)$**. The test of Crandall and Pomerance (Algorithm 3.6.9) replaces the powers of $a$ by the terms of a Lucas sequence attached to the polynomial $x^2 - ax + b$, whose discriminant $\Delta = a^2 - 4b$ is not a square, and it needs $\gcd(n, 2b\Delta) = 1$.

The bound $1 < a < n - 1$ removes two trivial bases. With $a = 1$ every $n$ passes. With $a = n - 1$ the Fermat congruence reads $(-1)^{n-1} \equiv 1$, which every odd $n$ satisfies.

**Strength order.** For odd $n$ and $\gcd(a, n) = 1$: a strong probable prime base $a$ is an Euler probable prime base $a$, and an Euler probable prime base $a$ is a probable prime base $a$ (HAC Fact 4.30). The second step follows by squaring both sides, because $\left(\frac{a}{n}\right)^2 = 1$. So each refinement accepts the same primes and fewer composites.

**Probable prime as an outcome.** The Handbook of Applied Cryptography calls an integer a probable prime when it "is believed to be prime on the basis of a probabilistic primality test" (Definition 4.5). Henri Cohen's phrase "industrial-grade prime" (Crandall and Pomerance, Section 3.5) names a number that passed several strong tests with random bases. The error is one-sided: a prime is never rejected, and the only possible mistake is to accept a composite.

## Examples and non-examples

**Examples.**

- $341 = 11 \cdot 31$ is a probable prime base 2, since $2^{340} \equiv 1 \pmod{341}$. It is the smallest composite with this property.
- $91 = 7 \cdot 13$ is a probable prime base 3 ($3^{90} \equiv 1 \pmod{91}$) and a strong probable prime base 10: $90 = 2 \cdot 45$ and $10^{45} \equiv 90 \equiv -1 \pmod{91}$.
- $561 = 3 \cdot 11 \cdot 17$ is a probable prime base $a$ for each $a$ coprime to it, because it is a [Carmichael number](/carmichael-number/). It is also an Euler probable prime base 2: $2^{280} \equiv 1$ and $\left(\frac{2}{561}\right) = 1$.
- $2047 = 23 \cdot 89$ is the smallest strong pseudoprime base 2.
- $2^{67} - 1 = 193707721 \cdot 761838257287$ is a strong probable prime base 2. Each composite Mersenne number $2^p - 1$ with $p$ prime is one.
- Among the odd integers $n$ with $5 \le n < 10^5$, there are $9590$ primes, and the composites that pass base 2 are $78$ for the Fermat test, $36$ for the Euler test and $16$ for the strong test. The 16 strong ones start $2047, 3277, 4033, 4681, 8321$. None of these 16 is also a strong probable prime to both bases 3 and 5.
- A random probable prime is almost always prime. For a random odd $k$-bit integer that passes $t$ strong tests with random bases, Damgard, Landrock and Pomerance bound the chance that it is composite; for example the bound for $k = 512$ and $t = 6$ is at most $2^{-88}$ (HAC Fact 4.48), and $t = 3$ rounds bring 1000-bit candidates below $2^{-80}$ (HAC Note 4.49). Shoup (Section 10.3) gives similar bounds for one round.

**Non-examples.**

- $341$ is not a probable prime base 3: $3^{340} \equiv 56 \pmod{341}$. That one computation proves $341$ composite without a factor.
- $341$ is not a strong probable prime base 2: $340 = 2^2 \cdot 85$, $2^{85} \equiv 32$ and $2^{170} \equiv 1 \pmod{341}$, so $32$ is a [nontrivial square root of one](/nontrivial-square-root-of-one/) modulo $341$.
- $561$ is not a strong probable prime base 2: $560 = 2^4 \cdot 35$ and the chain $2^{35}, 2^{70}, 2^{140}, 2^{280}$ is $263, 166, 67, 1$ modulo $561$, with no $-1 \equiv 560$.
- $2^{67} - 1$ is not a strong probable prime base 3, and also not a probable prime base 3.
- A probable prime is not a proven prime. A proof needs a [primality certificate](/primality-certificate/) or a deterministic test; see [primality proving](/primality-proving/).

## Related definitions

- **[Pseudoprime](/pseudoprime/).** A composite probable prime for a given test and base. The variants are [Fermat pseudoprimes](/fermat-pseudoprime/), [Euler-Jacobi pseudoprimes](/euler-jacobi-pseudoprime/) and [strong pseudoprimes](/strong-pseudoprime/).
- **[Compositeness witness](/compositeness-witness/) and [strong liar](/strong-liar/).** For a composite $n$, a base that the test rejects is a witness, and a base that it accepts is a liar. $n$ is a probable prime base $a$ exactly when $a$ is a liar for $n$.
- **[Carmichael number](/carmichael-number/).** A composite that is a probable prime base $a$ for each $a$ coprime to it. No composite is a strong probable prime for all its bases, and this makes the [Miller-Rabin test](/miller-rabin/) a good test.
- **[Baillie-PSW](/baillie-psw/).** A strong test base 2 followed by a Lucas test. A number that passes both is a "BPSW probable prime".
- **Provable prime.** A number "determined to be prime on the basis of a primality proving algorithm" (HAC Definition 4.34), for example from [Pocklington's test](/pocklington-primality-test/), a [Pratt certificate](/pratt-certificate/) or [ECPP](/ecpp/). HAC Note 4.64 compares provable and probable primes for cryptographic use.
- **[Random prime generation](/random-prime-generation/).** Its usual output is a probable prime.

## References
