---
tag: VC43JA
kind: concept
slug: primality-certificate
name: Primality certificate
aliases:
- certificate of primality
area: number-theory/primality
level: advanced
summary: Extra data that lets anyone check quickly and with no error that n is prime, such as a base and the factors of n - 1, or a chain of elliptic curves. Finding it can be hard; checking it is easy.
prereqs: [prime-number, primality-testing, certificate]
see_also: [pratt-certificate, pocklington-primality-test, proth-test, ecpp, primality-proving, compositeness-witness, np, co-np]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 4.1.3 (Theorems 4.1.8 and 4.1.9 and the remarks after them), Section 7.6 (Theorem 7.6.1, Algorithm 7.6.2 and its example) and Section 7.6.2 (Algorithm 7.6.3 and the example for 2^89 - 1)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Section 4.3 (Definition 4.34, Sections 4.3.2 to 4.3.4) and the chapter notes on Section 4.3
  - paper: doi:10.1137/0204018
    title: Vaughan R. Pratt, Every prime has a succinct certificate, SIAM Journal on Computing 4 (1975)
    locator: pages 214 to 220
---

A primality certificate for an integer $n$ is a piece of data that lets a fast, deterministic checker confirm that $n$ is [prime](/prime-number/) with no chance of error. The checker must accept only primes, and every prime must have some certificate that it accepts. Finding a certificate can take much more work than checking it, as with every [certificate](/certificate/) in the sense of the class [NP](/np/). The main kinds come from the factorization of $n - 1$ ([Pratt](/pratt-certificate/), [Pocklington](/pocklington-primality-test/), [Proth](/proth-test/)) and from elliptic curves ([ECPP](/ecpp/)).

## In plain words

Saying "this number is prime" is easy; making others believe it is the hard part. A certificate is a short note that comes with the claim and makes the check easy. A checker follows a fixed recipe on the number and the note, does a modest amount of arithmetic, and either accepts or rejects. A good recipe never accepts a number that is not prime. The note may have taken weeks of computing to find, but anyone can check it in seconds. For a number that is not prime, a factor is the obvious note: one division shows it. For a prime the notes are less obvious, and the main ones use a special base number, the factors of the number just below, or a chain of elliptic curves.

## The idea

**Definition.** A *primality certificate system* is a checker $V$ that takes $n$ and a string $c$ and runs in time polynomial in $\log n$, such that:

- *soundness:* if $V(n, c)$ accepts for some $c$, then $n$ is prime;
- *completeness:* for every prime $n$, some $c$ of length polynomial in $\log n$ makes $V(n, c)$ accept.

A certificate for $n$ is any $c$ that $V$ accepts. Soundness must hold with certainty, not with high probability: a passed [probable prime](/probable-prime/) test is evidence, not a certificate (HAC Definition 4.34 calls a number proved prime in this way a provable prime).

**Certificates of compositeness.** The other direction is easier. A proper factor $d$ of $n$ is checked by one division. A [compositeness witness](/compositeness-witness/) also works, with no factor: a base $a$ with $a^{n-1} \not\equiv 1 \pmod n$, or a strong witness of the [Miller-Rabin test](/miller-rabin/), proves $n$ composite by one power. So the composites are in NP, and the primes are in [co-NP](/co-np/).

**From $n - 1$.** Lucas's theorem says that $n$ is prime if some $a$ has $a^{n-1} \equiv 1$ and $a^{(n-1)/q} \not\equiv 1 \pmod n$ for each prime $q \mid n - 1$. The base $a$ and the factorization of $n - 1$ are a certificate, provided the primes $q$ are also proved. The [Pratt certificate](/pratt-certificate/) proves each $q$ the same way, recursively. It has fewer than $\lg n$ entries and is checked with fewer than $2 \lg^2 n$ modular products (Crandall and Pomerance, Theorem 4.1.9). This showed that every prime has a short certificate, so the primes are in NP as well as in co-NP (Pratt 1975; HAC, chapter notes on Section 4.3).

**From part of $n - 1$.** [Pocklington's theorem](/pocklington-primality-test/) needs only a factored part $F > \sqrt n$ of $n - 1$ and one base for each prime of $F$. For [Proth numbers](/proth-prime/) $k \cdot 2^m + 1$ with $k < 2^m$, the part $F = 2^m$ is free and the certificate is a single base $a$ with $a^{(n-1)/2} \equiv -1$; see [Proth's test](/proth-test/).

**From elliptic curves.** The Goldwasser-Kilian theorem (Crandall and Pomerance, Theorem 7.6.1) replaces the group of units modulo $n$ by an elliptic curve $E$ over $\mathbb{Z}_n$. If a point $P$ has $[m]P = O$ and $[m/q]P \ne O$ for a prime $q \mid m$ with $q > (n^{1/4} + 1)^2$, then $n$ is prime. By Hasse's bound each prime factor $p$ of $n$ then has $p > \sqrt n$. The certificate gives the curve, the point, $m$ and $q$, and then a certificate for the smaller prime $q$, in a chain that ends with a prime small enough for trial division. Since the curve can be changed until its order factors well, this works for primes of no special form; this is [ECPP](/ecpp/). HAC Section 4.3.4 notes that Atkin's version produces a short certificate that can be checked efficiently.

**Short and very short proofs.** Pomerance (1987) showed that every prime has a proof with only $O(\log p)$ modular products, using Theorem 7.6.1. As Crandall and Pomerance remark after Theorem 4.1.9, such a proof exists in principle, but finding it is the hard part.

**Tests without certificates.** Some proofs of primality leave nothing short to check. The Jacobi sum test decides primality in time $(\ln n)^{O(\ln \ln \ln n)}$ but produces no certificate that can be checked faster than running the test again (HAC Section 4.3.3). The [AKS test](/aks-primality-test/) is deterministic and polynomial, so its "certificate" is empty and the checker is the test itself, which is much slower than checking a Pratt or ECPP certificate.

## Examples

**A Pratt certificate for 1279** (Crandall and Pomerance, Section 4.1.3). The entries $(p, a, p - 1)$ are $(3, 2, 2)$, $(5, 2, 2^2)$, $(7, 3, 2 \cdot 3)$, $(71, 7, 2 \cdot 5 \cdot 7)$ and $(1279, 3, 2 \cdot 3^2 \cdot 71)$. For the last entry the checker confirms $3^{639} \equiv -1$, $3^{213} \equiv 775 \not\equiv -1$ and $3^{9} \equiv 498 \not\equiv -1 \pmod{1279}$. The whole check takes 48 modular products.

**A Pocklington certificate for 1000003.** Here $n - 1 = 6 \cdot 166667$ with $166667$ prime and $166667 > \sqrt n$. The base $2$ gives $2^{n-1} \equiv 1$ and $\gcd(2^6 - 1, n) = \gcd(63, 1000003) = 1$. So the certificate is $(F = 166667, a = 2)$ plus a certificate for $166667$.

**A Proth certificate for 97.** $97 = 3 \cdot 2^5 + 1$ with $3 < 32$, and the base $5$ gives $5^{48} \equiv 96 \equiv -1 \pmod{97}$. The single number $5$ is the certificate.

**The backbone of an ECPP certificate for $2^{89} - 1$** (Crandall and Pomerance, Section 7.6.2). With discriminant $D = -3$ and $u^2 + 3 v^2 = 4p$, a curve has order $p + 1 + u = 2^2 \cdot 3^2 \cdot 5^2 \cdot 7 \cdot 848173 \cdot p_2$ with $p_2 = 115836285129447871$. One more step with $D = -3$ gives the order $p_2 + 1 + u_2 = 2^2 \cdot 3 \cdot 7 \cdot 37 \cdot 65707 \cdot p_3$ with $p_3 = 567220573$, which trial division proves prime. The full certificate adds the curve coefficients and the points. The identities $u^2 + 3v^2 = 4p$ and the two factorizations check by direct computation, and each $q$ exceeds $(n^{1/4} + 1)^2$ for its $n$.

**Compositeness certificates.** For $561 = 3 \cdot 11 \cdot 17$, the factor $3$. For $341 = 11 \cdot 31$, the base $3$, since $3^{340} \equiv 56 \not\equiv 1 \pmod{341}$, although the base 2 gives $2^{340} \equiv 1$.

**Not a certificate.** That $n$ passes 50 rounds of Miller-Rabin bounds the chance of error by $4^{-50}$ but proves nothing; a checker that accepts it is not sound.

## Where it is used

- **Complexity theory.** Pratt certificates put the primes in NP and in co-NP together, long before AKS put them in [P](/p/) (HAC, chapter notes on Section 4.3).
- **Records and tables of primes.** A large prime found by one group can be checked by others from its certificate, with far less work than finding it; ECPP certificates serve this role for primes of no special form.
- **Cryptography.** Provable primes for keys and group parameters come with a certificate, often built together with the prime, as in Maurer's method, which uses Pocklington's theorem at each step; see [random prime generation](/random-prime-generation/).
- **Checked software and formal proofs.** A small, trusted checker can confirm a certificate produced by large, untrusted software, so the trust rests only on the checker.
- **Recursive proofs.** Certificates for the primes $q$ inside a Pocklington or ECPP step are themselves certificates, so proofs compose into chains and trees.

## References
