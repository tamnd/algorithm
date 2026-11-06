---
tag: MAHY9R
kind: definition
slug: prime-number
name: Prime number
aliases:
- prime
- primes
area: number-theory/primality
level: intro
summary: An integer greater than 1 whose only positive divisors are 1 and itself.
prereqs: [divisibility, divisor]
see_also: [fundamental-theorem-of-arithmetic, euclids-lemma, primality-testing, prime-counting-function, prime-number-theorem, sieve-of-eratosthenes, coprime-integers, prime-gaps]
sources:
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 1, The series of primes (1), Sections 1.2 to 1.4, and Chapter 2, Section 2.1, First proof of Euclid's second theorem
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 1.1, Divisibility and primality, and Section 1.3, Some consequences of unique factorization
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.1, Elementary number-theory notions (prime and composite numbers)
---

A prime number is an integer $p \ge 2$ whose only positive [divisors](/divisor/) are $1$ and $p$. An integer $n \ge 2$ that is not prime is *composite*. The primes are the building blocks of the integers under multiplication: by the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/), each integer $n \ge 2$ is a product of primes in exactly one way, up to the order of the factors. There are infinitely many primes, and they thin out slowly, as the [prime number theorem](/prime-number-theorem/) describes.

## Definition

An integer $p$ is **prime** if $p \ge 2$ and, for all positive integers $d$,

$$d \mid p \implies d = 1 \text{ or } d = p.$$

An integer $n \ge 2$ is **composite** if it is not prime, that is, if $n = ab$ for some integers $a, b$ with $1 < a \le b < n$. The integers $0$ and $1$ are neither prime nor composite. Negative integers are not called prime numbers, although $-p$ behaves like $p$ in the ring $\mathbb{Z}$ (see below).

**The Euclid property.** For an integer $p \ge 2$, these two statements are equivalent:

1. $p$ is prime in the sense above (it has no divisor strictly between $1$ and $p$);
2. for all integers $a$ and $b$, if $p \mid ab$, then $p \mid a$ or $p \mid b$.

The step from 1 to 2 is [Euclid's lemma](/euclids-lemma/): if $p \nmid a$, then $\gcd(p, a) = 1$ because the only positive divisors of $p$ are $1$ and $p$, so [Bezout's identity](/bezouts-identity/) gives $1 = px + ay$, and $b = pbx + aby$ is a multiple of $p$. The step from 2 to 1: if $p = de$ with $1 < d < p$, then $1 < e < p$, and $p \mid de$ but $p$ divides neither $d$ nor $e$, since both are positive and smaller than $p$. In the language of rings, statement 1 says that $p$ is *irreducible* and statement 2 says that $p$ is a *prime element*. In $\mathbb{Z}$ the two notions agree, and the prime elements of $\mathbb{Z}$ are the numbers $\pm p$.

**A prime divisor always exists.** Each integer $n \ge 2$ has a prime divisor, and if $n$ is composite, it has one at most $\sqrt n$. *Proof.* Let $d$ be the smallest divisor of $n$ with $d > 1$; it exists because $n$ itself is such a divisor. If $d = ab$ with $1 < a < d$, then $a$ is a divisor of $n$ that is larger than 1 and smaller than $d$, which is impossible, so $d$ is prime. If $n$ is composite, write $n = d \cdot e$; then $e > 1$ is a divisor of $n$, so $e \ge d$ and $d^2 \le de = n$. $\square$ This fact is the basis of [trial division](/trial-division/) and of the [sieve of Eratosthenes](/sieve-of-eratosthenes/).

**There are infinitely many primes** (Euclid). *Proof.* Let $p_1, \ldots, p_k$ be any finite list of primes, and let $N = p_1 p_2 \cdots p_k + 1 \ge 2$. By the previous fact, $N$ has a prime divisor $q$. If $q = p_i$ for some $i$, then $q$ divides both $N$ and $N - 1 = p_1 \cdots p_k$, so $q \mid 1$, which is false. So $q$ is a prime that is not in the list, and no finite list holds all primes. $\square$

## Examples and non-examples

**Examples.**

- The primes below 100 are 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89 and 97. There are 25 of them.
- $2$ is the only even prime, because each even number above 2 has the divisor 2.
- $2^{31} - 1 = 2147483647$ is prime. It is a [Mersenne prime](/mersenne-prime/), and trial division by the odd numbers up to $46340$ finds no divisor.
- The numbers of primes up to $10^3$ and up to $10^6$ are $168$ and $78498$. The [prime-counting function](/prime-counting-function/) $\pi(x)$ gives these counts.

**Non-examples.**

- $1$ is not prime. With 1 as a prime, the factorization of an integer would not be unique ($6 = 2 \cdot 3 = 1 \cdot 2 \cdot 3$), and many theorems would need the words "except 1".
- $0$ is not prime: each integer divides $0$.
- $91 = 7 \cdot 13$ and $57 = 3 \cdot 19$ are composite, though they have no small factor that is easy to see.
- $561 = 3 \cdot 11 \cdot 17$ is composite, but it passes the [Fermat test](/fermat-primality-test/) for each base coprime to it. It is the smallest [Carmichael number](/carmichael-number/).
- Euclid's proof does not say that $p_1 \cdots p_k + 1$ is prime. For the first six primes, $2 \cdot 3 \cdot 5 \cdot 7 \cdot 11 \cdot 13 + 1 = 30031 = 59 \cdot 509$, which is composite, but its prime factors are new.
- Primality depends on the ring. The prime $5$ of $\mathbb{Z}$ factors as $(2 + i)(2 - i)$ in the Gaussian integers $\mathbb{Z}[i]$, so it is not a prime element there.

## Related definitions

- **Composite number.** An integer $n \ge 2$ that is not prime. A composite $n$ always has a prime factor at most $\sqrt n$.
- **[Coprime integers](/coprime-integers/).** Integers $a$ and $b$ with $\gcd(a, b) = 1$. A prime $p$ is coprime to each integer that it does not divide.
- **Prime factorization.** The unique way to write $n \ge 2$ as $p_1^{e_1} \cdots p_r^{e_r}$ with primes $p_1 < \cdots < p_r$ and exponents $e_i \ge 1$; see the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/). Finding it is [integer factorization](/integer-factorization/).
- **Primes of special form.** [Mersenne primes](/mersenne-prime/) $2^p - 1$, [Fermat primes](/fermat-prime/) $2^{2^k} + 1$, [Proth primes](/proth-prime/) $k \cdot 2^m + 1$, [Sophie Germain primes](/sophie-germain-prime/) $q$ with $2q + 1$ prime, and [safe primes](/safe-prime/) $2q + 1$ with $q$ prime.
- **[Probable prime](/probable-prime/) and [pseudoprime](/pseudoprime/).** A number that passes a probabilistic test, and a composite number that passes it.
- **Distribution.** The [prime-counting function](/prime-counting-function/), the [prime number theorem](/prime-number-theorem/) $\pi(x) \sim x / \ln x$, [Bertrand's postulate](/bertrands-postulate/) and the [prime gaps](/prime-gaps/).
- **Deciding primality.** The problem of [primality testing](/primality-testing/), and of [primality proving](/primality-proving/) with a certificate.

## References
