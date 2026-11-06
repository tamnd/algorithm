---
tag: XRA6WF
kind: definition
slug: proth-prime
name: Proth prime
aliases:
- Proth number
area: number-theory/primality
level: core
summary: A prime of the form k·2^m + 1 with odd k and k < 2^m. Proth's theorem proves such a number prime with one modular exponentiation.
prereqs: [prime-number, euler-criterion, pocklington-primality-test]
see_also: [proth-test, fermat-prime, pepin-test, mersenne-prime, pocklington-primality-test, primality-proving, quadratic-residue, sophie-germain-prime]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 4.1.2 (Theorem 4.1.3 and Corollary 4.1.4), Exercise 4.10 (Proth's theorem), Exercise 1.83 (Sierpinski numbers) and Section 9.2.3 (Algorithm 9.2.14, fast reduction modulo Proth numbers)
  - paper: "F. Proth, Theoremes sur les nombres premiers, Comptes Rendus de l'Academie des Sciences de Paris 87 (1878)"
    title: Theoremes sur les nombres premiers
    locator: page 926
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 12.1 (Legendre symbol and Euler's criterion) and Section 12.3 (computing the Jacobi symbol)
---

A Proth number is an integer $N = k \cdot 2^m + 1$ with $k$ odd, $m \ge 1$ and $k < 2^m$, and a Proth prime is a Proth number that is [prime](/prime-number/). The condition $k < 2^m$ says that the power of 2 in $N - 1$ is larger than $\sqrt N$. That makes the factorization of $N - 1$ known for free, and so Proth's theorem proves a Proth prime prime with one [modular exponentiation](/modular-exponentiation/), in the same way as the [Pepin test](/pepin-test/) for [Fermat numbers](/fermat-prime/).

## Definition

Each odd integer $N \ge 3$ has exactly one representation $N - 1 = k \cdot 2^m$ with $k$ odd and $m \ge 1$: $m$ is the exponent of the largest power of 2 that divides $N - 1$, and $k = (N - 1)/2^m$. So the following definition does not depend on a choice.

An odd integer $N \ge 3$ is a **Proth number** if, with $N - 1 = k \cdot 2^m$ and $k$ odd,

$$k < 2^m.$$

Equivalently, $N - 1 < 4^m$, since $k < 2^m \iff k \cdot 2^m < 2^{2m}$. A **Proth prime** is a Proth number that is prime.

**Proth's theorem** (Proth 1878; Crandall and Pomerance, Exercise 4.10). Let $N$ be a Proth number. Then $N$ is prime if and only if there is an integer $a$ with

$$a^{(N-1)/2} \equiv -1 \pmod N.$$

*Proof.* If $N$ is prime, take for $a$ a quadratic non-residue modulo $N$; one exists because exactly half of the nonzero residues modulo an odd prime are non-residues. [Euler's criterion](/euler-criterion/) gives $a^{(N-1)/2} \equiv -1$. Conversely, suppose $a^{(N-1)/2} \equiv -1 \pmod N$ and let $p$ be a prime factor of $N$. Then $a^{N-1} \equiv 1$ and $a^{(N-1)/2} \not\equiv 1 \pmod p$, because $-1 \not\equiv 1 \pmod p$ for odd $p$. So the [multiplicative order](/multiplicative-order/) of $a$ modulo $p$ divides $N - 1 = k \cdot 2^m$ but not $(N-1)/2 = k \cdot 2^{m-1}$, and so $2^m$ divides it. The order divides $p - 1$, so $2^m \mid p - 1$ and $p > 2^m$. From $k < 2^m$, $N = k \cdot 2^m + 1 \le (2^m - 1) 2^m + 1 < 2^{2m}$, so $p > 2^m > \sqrt N$. Each prime factor of $N$ is larger than $\sqrt N$. A composite $N$ has a prime factor at most $\sqrt N$, so $N$ is prime. $\square$

This is the case $F = 2^m$ of [Pocklington's theorem](/pocklington-primality-test/) (Crandall and Pomerance, Theorem 4.1.3 and Corollary 4.1.4). The [Proth test](/proth-test/) turns it into an algorithm: it finds a non-residue $a$ with the [Jacobi symbol](/jacobi-symbol/) and checks the congruence.

**Cost model.** For $N$ of bit length $n$, the check costs one modular exponentiation, $O(n)$ multiplications of $n$-bit numbers, which is $O(n^3)$ bit operations with schoolbook multiplication. For $N = k \cdot 2^m + 1$ with a one-word $k$, reduction modulo $N$ needs only shifts, a small multiplication and additions (Crandall and Pomerance, Algorithm 9.2.14), so each step is cheaper than a general reduction.

## Examples and non-examples

**Examples.**

- The Proth numbers below 200 are $3, 5, 9, 13, 17, 25, 33, 41, 49, 57, 65, 81, 97, 113, 129, 145, 161, 177, 193$. The primes among them are $3, 5, 13, 17, 41, 97, 113, 193$.
- $13 = 3 \cdot 2^2 + 1$ with $3 < 4$. The base $a = 2$ is a non-residue modulo 13, and $2^6 = 64 \equiv -1 \pmod{13}$, which proves 13 prime.
- Each Fermat number $F_j = 2^{2^j} + 1$ is a Proth number with $k = 1$. So the Fermat primes $3, 5, 17, 257, 65537$ are Proth primes.
- $3 \cdot 2^m + 1$ is a Proth prime for $m = 2, 5, 6, 8, 12, 18, 30, 36, 41, 66, 189, 201, 209, 276, 353, 408, 438, 534$, and for no other $m$ with $2 \le m < 700$. The largest of these, $3 \cdot 2^{534} + 1$, has 162 decimal digits.
- There are 450 Proth numbers below $10^5$, and 99 of them are prime. Below $10^6$ there are 249 Proth primes, against 78498 primes in all.

**Non-examples.**

- $7 = 3 \cdot 2^1 + 1$ is prime but not a Proth number, since $3 > 2$. The same holds for $11 = 5 \cdot 2 + 1$, $19 = 9 \cdot 2 + 1$, $23 = 11 \cdot 2 + 1$ and $37 = 9 \cdot 2^2 + 1$.
- $9 = 1 \cdot 2^3 + 1$, $25 = 3 \cdot 2^3 + 1$ and $65 = 1 \cdot 2^6 + 1$ are Proth numbers but composite. For $N = 25$, no $a$ gives $a^{12} \equiv -1 \pmod{25}$.
- Even numbers and $1$ are not Proth numbers.
- Proth numbers are sparse. If $N \le x$, then $k < 2^m$ and $k \cdot 2^m < x$ give $k < \sqrt x$; for each odd $k$ the values of $m$ are at most $\log_2 x$, so there are $O(\sqrt x \log x)$ Proth numbers up to $x$. Most primes are therefore not Proth primes.
- A Sierpinski number is an odd $k$ such that $k \cdot 2^m + 1$ is composite for every $m \ge 1$, so it gives no Proth prime. Sierpinski proved that there are infinitely many, and $78557$ is one (Crandall and Pomerance, Exercise 1.83).

## Related definitions

- **[Proth test](/proth-test/).** The algorithm that proves or disproves the primality of a Proth number with Proth's theorem.
- **[Fermat prime](/fermat-prime/).** The case $k = 1$, $m = 2^j$. The [Pepin test](/pepin-test/) is the Proth test with the fixed base $3$.
- **[Pocklington's test](/pocklington-primality-test/).** The general form: a factored part $F$ of $N - 1$ with $F > \sqrt N$ is enough. Proth numbers are the case where $F$ is a power of 2.
- **[Mersenne prime](/mersenne-prime/).** Primes $2^p - 1$, where $N + 1$ is a power of 2; the [Lucas-Lehmer test](/lucas-lehmer-test/) proves them with Lucas sequences.
- **[Primality proving](/primality-proving/).** Proth primes are among the few large primes that can be proved prime at the cost of one probable prime test.

## References
