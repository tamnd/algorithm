---
tag: ZMQXGG
kind: definition
slug: fermat-prime
name: Fermat prime
aliases:
- Fermat number prime
area: number-theory/primality
level: core
summary: A prime of the form F_k = 2^(2^k) + 1. Only F_0 to F_4 (3, 5, 17, 257, 65537) are known to be prime, and F_5 to F_32 are known to be composite.
prereqs: [prime-number, multiplicative-order, quadratic-residue]
see_also: [pepin-test, mersenne-prime, fermat-pseudoprime, proth-prime, number-theoretic-transform, schonhage-strassen-multiplication, rsa-cryptosystem, prime-number]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 1.3.2, Fermat numbers, and Section 4.1.1, The Lucas theorem and Pepin test
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 2, The sequence of primes (Fermat's numbers and their pairwise coprimality)
  - url: https://en.wikipedia.org/wiki/Fermat_number
    title: Fermat number, Wikipedia
    locator: sections Primality and Factorization (the status of F_5 to F_32, Euler's factor 641 of F_5, Lucas's form of the factors, the Gauss-Wantzel theorem)
---

A Fermat prime is a [prime](/prime-number/) of the form $F_k = 2^{2^k} + 1$. Fermat believed that all the numbers $F_k$ are prime, but only $F_0, \ldots, F_4$, that is $3, 5, 17, 257, 65537$, are known to be, and Euler found the factor 641 of $F_5$ in 1732. [Pépin's test](/pepin-test/) decides whether $F_k$ is prime with $2^k - 1$ squarings modulo $F_k$. Fermat primes give the regular polygons that can be drawn with ruler and compass, and $65537$ is the most common RSA public exponent.

## Definition

For an integer $k \ge 0$, the **Fermat number** $F_k$ is

$$F_k = 2^{2^k} + 1.$$

A **Fermat prime** is a Fermat number that is prime.

**Only powers of two in the exponent.** If $2^m + 1$ is prime and $m \ge 1$, then $m$ is a power of 2. Indeed, if $m = 2^k q$ with $q > 1$ odd, put $x = 2^{2^k}$. Then $x + 1$ divides $x^q + 1$, because $x \equiv -1$ gives $x^q + 1 \equiv (-1)^q + 1 = 0 \pmod{x + 1}$, and $1 < x + 1 < x^q + 1 = 2^m + 1$. So the Fermat numbers are the only candidates for primes of the form $2^m + 1$.

**The form of the factors.** Let $k \ge 2$ and let $q$ be a prime factor of $F_k$. Then $q \equiv 1 \pmod{2^{k+2}}$, so $q = j \cdot 2^{k+2} + 1$ for some $j \ge 1$ (Euler proved $2^{k+1} \mid q - 1$, and Lucas the sharper form).

*Proof.* From $2^{2^k} \equiv -1 \pmod q$ we get $2^{2^{k+1}} \equiv 1$, so the [multiplicative order](/multiplicative-order/) of 2 modulo $q$ divides $2^{k+1}$ but not $2^k$, so it is $2^{k+1}$. By [Fermat's little theorem](/fermat-little-theorem/), $2^{k+1} \mid q - 1$. As $k \ge 2$, $8 \mid q - 1$, so 2 is a [quadratic residue](/quadratic-residue/) modulo $q$, and [Euler's criterion](/euler-criterion/) gives $2^{(q-1)/2} \equiv 1$. So the order $2^{k+1}$ divides $(q - 1)/2$, and $2^{k+2} \mid q - 1$. $\square$

**Fermat numbers are pairwise coprime.** For each $k \ge 1$, $F_0 F_1 \cdots F_{k-1} = F_k - 2$, by induction: $(F_k - 2) F_k = (2^{2^k} - 1)(2^{2^k} + 1) = 2^{2^{k+1}} - 1 = F_{k+1} - 2$. So a common divisor of $F_j$ and $F_k$ with $j < k$ divides 2, and as both are odd it is 1. Since each $F_k$ has a prime factor of its own, this gives a proof, due to Pólya, that there are infinitely many primes.

## Examples and non-examples

**Examples.** The known Fermat primes are

$$F_0 = 3, \quad F_1 = 5, \quad F_2 = 17, \quad F_3 = 257, \quad F_4 = 65537.$$

The prime $65537 = 2^{16} + 1$ is the usual RSA public exponent $e$: encryption with it costs 16 squarings and one multiplication, and it is large enough to avoid the attacks on the exponent $e = 3$ with unpadded messages. The primes $257$ and $65537$ are also moduli for [number-theoretic transforms](/number-theoretic-transform/), where 2 is a root of unity of order $2^{k+1}$ modulo $F_k$, so multiplication by its powers is a shift.

**Non-examples.**

- $F_5 = 2^{32} + 1 = 4294967297 = 641 \cdot 6700417$. Here $641 = 5 \cdot 2^7 + 1$ and $6700417 = 52347 \cdot 2^7 + 1$, both of the form $j \cdot 2^{k+2} + 1$ with $k = 5$.
- $F_6 = 274177 \cdot 67280421310721$, with $274177 = 1071 \cdot 2^8 + 1$.
- $F_5$ to $F_{32}$ are all known to be composite. $F_{20}$ and $F_{24}$ are proved composite by Pépin's test, but no factor of either is known. $F_{33}$ is the smallest Fermat number whose status is unknown.
- $2^6 + 1 = 65 = 5 \cdot 13$: an exponent that is not a power of two gives a composite number.
- Each composite Fermat number is a [Fermat pseudoprime](/fermat-pseudoprime/) to the base 2, so the Fermat test with base 2 cannot find them; Pépin's test uses the base 3.

**Constructible polygons.** By the Gauss-Wantzel theorem, a regular polygon with $m$ sides can be drawn with ruler and compass if and only if $m = 2^a p_1 \cdots p_r$ with $p_1, \ldots, p_r$ distinct Fermat primes. Gauss drew the 17-gon in 1796. With the five known Fermat primes there are 31 odd values of $m > 1$ of this kind, the largest being $3 \cdot 5 \cdot 17 \cdot 257 \cdot 65537 = 2^{32} - 1$.

**What is open.** It is not known whether $F_k$ is composite for every $k \ge 5$, or whether there are infinitely many composite Fermat numbers. A heuristic count, with the chance that $F_k$ is prime about $1/\ln F_k \approx 1/(2^k \ln 2)$, predicts only finitely many Fermat primes.

## Related definitions

- [Pépin's test](/pepin-test/): for $k \ge 1$, $F_k$ is prime if and only if $3^{(F_k - 1)/2} \equiv -1 \pmod{F_k}$.
- [Mersenne prime](/mersenne-prime/): primes $2^p - 1$, the other classic family, with the [Lucas-Lehmer test](/lucas-lehmer-test/).
- [Proth prime](/proth-prime/): primes $j \cdot 2^m + 1$ with $j < 2^m$; Fermat numbers are the case $j = 1$, and the prime factors of $F_k$ have the same shape $j \cdot 2^m + 1$, though not always with $j < 2^m$.
- [Fermat pseudoprime](/fermat-pseudoprime/): the name comes from Fermat's little theorem, not from Fermat numbers.

## References
