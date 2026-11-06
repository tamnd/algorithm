---
tag: H7W80V
kind: definition
slug: mersenne-prime
name: Mersenne prime
aliases:
- Mersenne number
area: number-theory/primality
level: intro
summary: A prime of the form 2^p - 1. The exponent p must itself be prime, and the Lucas-Lehmer test decides primality of these numbers fast, so the largest known primes are Mersenne primes.
prereqs: [prime-number, divisibility, multiplicative-order]
see_also: [lucas-lehmer-test, fermat-prime, fermat-pseudoprime, mersenne-twister, quadratic-residue, prime-number]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 1.3.1, Mersenne primes, and Section 4.2.1, The Lucas-Lehmer test
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.4, Factoring into primes (the Lucas-Lehmer test for 2^p - 1 and the table of Mersenne primes)
  - url: https://www.mersenne.org/primes/?press=M136279841
    title: Great Internet Mersenne Prime Search, 2^136279841-1 is Prime!
    locator: the press release of the 52nd known Mersenne prime, found on 12 October 2024
  - url: https://en.wikipedia.org/wiki/Mersenne_prime
    title: Mersenne prime, Wikipedia
    locator: sections History and List of known Mersenne primes (Mersenne's list of 1644, Cole's factorization of 2^67 - 1, Robinson's computer search of 1952)
---

A Mersenne prime is a [prime](/prime-number/) of the form $M_p = 2^p - 1$. The exponent $p$ must be prime, but a prime exponent is not enough: $2^{11} - 1 = 2047 = 23 \cdot 89$. The [Lucas-Lehmer test](/lucas-lehmer-test/) decides whether $M_p$ is prime with $p - 2$ squarings modulo $M_p$, much faster than any test for a general number of the same size, and for this reason the largest known primes are almost always Mersenne primes. In 2026, 52 Mersenne primes are known; the largest is $2^{136279841} - 1$, found in October 2024.

## Definition

For an integer $n \ge 1$, the **Mersenne number** $M_n$ is

$$M_n = 2^n - 1.$$

A **Mersenne prime** is a Mersenne number that is prime. Some authors keep the name Mersenne number for $M_p$ with $p$ prime only, because only these can be prime.

**The exponent is prime.** If $M_n$ is prime, then $n$ is prime. Indeed $M_1 = 1$ is not prime, and if $n = ab$ with $1 < a < n$, then

$$2^{ab} - 1 = (2^a - 1)\left(1 + 2^a + 2^{2a} + \cdots + 2^{(b-1)a}\right),$$

and $1 < 2^a - 1 < 2^n - 1$, so $2^a - 1$ is a proper factor of $M_n$.

**The form of the factors.** Let $p$ be an odd prime and $q$ a prime factor of $M_p$. Then $q \equiv 1 \pmod{2p}$ and $q \equiv \pm 1 \pmod 8$.

*Proof.* From $2^p \equiv 1 \pmod q$ and $2 \not\equiv 1$, the [multiplicative order](/multiplicative-order/) of 2 modulo $q$ divides $p$ and is not 1, so it is $p$. By [Fermat's little theorem](/fermat-little-theorem/), $2^{q-1} \equiv 1$, so $p \mid q - 1$. As $q$ is odd, $2p \mid q - 1$. Next, $2 \equiv 2 \cdot 2^p = (2^{(p+1)/2})^2 \pmod q$, so 2 is a [quadratic residue](/quadratic-residue/) modulo $q$. By the second supplement to [quadratic reciprocity](/quadratic-reciprocity/), this holds only for $q \equiv \pm 1 \pmod 8$. $\square$

So a search for factors of $M_p$ needs to try only $q = 2kp + 1$ with $q \equiv \pm 1 \pmod 8$. For $p = 11$: $23 = 2 \cdot 11 + 1$ and $89 = 8 \cdot 11 + 1$, with $23 \equiv 7$ and $89 \equiv 1 \pmod 8$.

**A factor rule of Euler.** If $p \equiv 3 \pmod 4$, $p > 3$, and $q = 2p + 1$ is prime, then $q \mid M_p$, so $M_p$ is composite. Here $q \equiv 7 \pmod 8$, so 2 is a quadratic residue modulo $q$, and [Euler's criterion](/euler-criterion/) gives $2^{(q-1)/2} = 2^p \equiv 1 \pmod q$. Since $q < M_p$ for $p > 3$, the factor is proper. The cases $p = 11, 23, 83, 131, 179, 191, 239, 251$ come from this rule.

## Examples and non-examples

| $p$ | $M_p$ | prime? | factorization |
|---|---|---|---|
| 2 | 3 | yes | |
| 3 | 7 | yes | |
| 5 | 31 | yes | |
| 7 | 127 | yes | |
| 11 | 2047 | no | $23 \cdot 89$ |
| 13 | 8191 | yes | |
| 17 | 131071 | yes | |
| 19 | 524287 | yes | |
| 23 | 8388607 | no | $47 \cdot 178481$ |
| 29 | 536870911 | no | $233 \cdot 1103 \cdot 2089$ |
| 31 | 2147483647 | yes | |
| 37 | 137438953471 | no | $223 \cdot 616318177$ |

**Examples.** The Mersenne primes $M_p$ have the exponents $p = 2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, \ldots$ The prime $M_{31} = 2147483647$ is the largest signed 32-bit integer. The prime $M_{61}$ is a common modulus for hashing, because reduction modulo $2^{61} - 1$ needs only a shift, a mask and an addition. The prime $M_{19937}$ gives the period of the [Mersenne Twister](/mersenne-twister/) generator. The largest known, $M_{136279841}$, has $41024320$ decimal digits.

**Non-examples.**

- $M_4 = 15 = 3 \cdot 5$ and $M_8 = 255 = 3 \cdot 5 \cdot 17$: a composite exponent gives a composite number.
- $M_{11} = 2047$: a prime exponent does not guarantee a prime. 2047 is also the smallest [strong pseudoprime](/strong-pseudoprime/) to the base 2, and each composite $M_p$ with $p$ prime is a [Fermat pseudoprime](/fermat-pseudoprime/) to the base 2.
- $M_{67} = 193707721 \cdot 761838257287$: Mersenne listed $p = 67$ as giving a prime, and Cole found this factorization in 1903.
- $2^{1277} - 1$ is composite by the Lucas-Lehmer test, but no factor of it is known. A primality test can prove a number composite without finding a factor.

**Even perfect numbers.** A positive integer is *perfect* when it equals the sum of its divisors below itself, such as $6 = 1 + 2 + 3$ and $28$. By the Euclid-Euler theorem, the even perfect numbers are exactly the numbers $2^{p-1}(2^p - 1)$ with $2^p - 1$ prime. So each Mersenne prime gives one even perfect number: $3 \to 6$, $7 \to 28$, $31 \to 496$, $127 \to 8128$.

**What is open.** It is not known whether there are infinitely many Mersenne primes. A heuristic argument, known as the Lenstra-Pomerance-Wagstaff conjecture, predicts about $(e^\gamma / \ln 2) \ln x$ Mersenne primes $M_p$ with $p \le x$, where $\gamma$ is Euler's constant, and so infinitely many.

## Related definitions

- [Lucas-Lehmer test](/lucas-lehmer-test/): the deterministic test for $M_p$, with $s_0 = 4$, $s_{i+1} = s_i^2 - 2$, and $M_p$ prime exactly when $s_{p-2} \equiv 0 \pmod{M_p}$ for odd $p$.
- [Fermat prime](/fermat-prime/): the other classic special form, $2^{2^k} + 1$, with its own test, [Pépin's test](/pepin-test/).
- [Fermat pseudoprime](/fermat-pseudoprime/): each composite $M_p$ with prime $p$ is one, to the base 2.
- [Prime number](/prime-number/) and [primality testing](/primality-testing/): the general setting.

## References
