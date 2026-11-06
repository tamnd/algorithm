---
tag: S8AEFR
kind: concept
slug: nontrivial-square-root-of-one
name: Nontrivial square root of 1 modulo n
area: number-theory/primality
level: core
summary: A residue x other than 1 and n-1 with x squared congruent to 1 modulo n, whose existence proves n composite.
prereqs: [congruence, chinese-remainder-theorem, euclidean-algorithm]
see_also: [miller-rabin, compositeness-witness, strong-pseudoprime, carmichael-function, congruence-of-squares, factoring-to-order-finding, rabin-cryptosystem, modular-square-root]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.6, Powers of an element (nontrivial square roots of 1), and Section 31.8, Primality testing (the procedure WITNESS)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Chapter 10, Probabilistic primality testing (the Miller-Rabin test)
  - paper: doi:10.1016/0022-314X(80)90084-0
    title: Michael O. Rabin, Probabilistic algorithm for testing primality, Journal of Number Theory 12 (1980)
    locator: pages 128 to 138
---

A nontrivial square root of 1 modulo $n$ is an integer $x$ with $x^2 \equiv 1 \pmod n$ but $x \not\equiv 1$ and $x \not\equiv -1 \pmod n$. Modulo a [prime](/prime-number/) there is no such $x$, so finding one proves that $n$ is composite. More than that, it gives a factor of $n$ at once, as $\gcd(x - 1, n)$. This is the fact behind the [Miller-Rabin test](/miller-rabin/), and it also links factoring to taking square roots and to finding orders.

## In plain words

Modulo a prime, the only numbers whose square is one are one and minus one, just as for ordinary numbers. Modulo a composite number there can be other such numbers. So if a test meets a number, other than one and minus one, whose square is one, it knows that the modulus is not prime.

Such a number does more than prove the modulus composite. It splits the modulus: the common factor of the modulus and the number minus one is a proper divisor. So a method that finds these extra square roots is also a method that factors.

## The idea

Let $n \ge 2$. The **square roots of 1 modulo $n$** are the residues $x$ with $x^2 \equiv 1 \pmod n$. The residues $1$ and $n - 1$ are always square roots of 1; they are the *trivial* ones. Any other square root of 1 is **nontrivial**.

**Modulo a prime there are none.** If $p$ is prime and $x^2 \equiv 1 \pmod p$, then $p \mid (x - 1)(x + 1)$, so $p \mid x - 1$ or $p \mid x + 1$, that is, $x \equiv \pm 1 \pmod p$. The same holds modulo an odd prime power $p^e$: $p$ cannot divide both $x - 1$ and $x + 1$, whose difference is 2, so $p^e$ divides one of them.

**A nontrivial root gives a factor.** Let $x^2 \equiv 1 \pmod n$ with $x \not\equiv \pm 1$. Then $n \mid (x - 1)(x + 1)$, but $n \nmid x - 1$ and $n \nmid x + 1$. Put $g = \gcd(x - 1, n)$. If $g = n$, then $n \mid x - 1$, which is false. If $g = 1$, then $n \mid x + 1$ by [Euclid's lemma](/euclids-lemma/), which is also false. So $1 < g < n$, and $g$ is a proper factor of $n$, found with one run of the [Euclidean algorithm](/euclidean-algorithm/). The cofactor is $\gcd(x + 1, n)$ when $n$ is odd and squarefree; in general it is $n/g$.

**How many square roots of 1 there are.** By the [Chinese remainder theorem](/chinese-remainder-theorem/), $x$ is a square root of 1 modulo $n$ exactly when it is one modulo each prime power in $n$, and the counts multiply. Modulo an odd prime power there are 2. Modulo $2$ there is 1, modulo $4$ there are 2, and modulo $2^e$ with $e \ge 3$ there are 4, namely $\pm 1$ and $2^{e-1} \pm 1$. So an odd $n$ with $r$ distinct prime factors has exactly $2^r$ square roots of 1, and $2^r - 2$ of them are nontrivial. Each odd $n$ that is not a prime power has some.

**How tests find one.** A test cannot search all residues, but it can produce candidates by repeated squaring. Write $n - 1 = 2^s d$ with $d$ odd, pick a base $a$, and compute $a^d, a^{2d}, \ldots, a^{2^s d} = a^{n-1}$, each the square of the one before. If $n$ is prime, the last term is 1 by [Fermat's little theorem](/fermat-little-theorem/), and the term just before the first 1 can only be $-1$. If the sequence reaches 1 from a term other than $\pm 1$, that term is a nontrivial square root of 1. This is the *strong probable prime* condition of [Miller-Rabin](/miller-rabin/), and the base is then a [compositeness witness](/compositeness-witness/).

## Examples

- Modulo $15 = 3 \cdot 5$ the square roots of 1 are $1, 4, 11, 14$. The root $4$ is nontrivial: $4^2 = 16 \equiv 1$. Then $\gcd(3, 15) = 3$ and $\gcd(5, 15) = 5$ give the factors.
- Modulo $8$ every odd residue is a square root of 1: $1, 3, 5, 7$. This is the case $2^e$ with $e \ge 3$, and $n = 8$ is a prime power with nontrivial roots.
- Modulo $9 = 3^2$ only $1$ and $8$ are square roots of 1, as for any odd prime power. So the factor trick cannot split a prime power, and Miller-Rabin catches odd prime powers by other means: they fail the Fermat condition for most bases.
- **The Carmichael number 561.** $561 = 3 \cdot 11 \cdot 17$ has $2^3 = 8$ square roots of 1: $1, 67, 188, 254, 307, 373, 494, 560$. With the base 2, $560 = 2^4 \cdot 35$, and the sequence $2^{35}, 2^{70}, 2^{140}, 2^{280}, 2^{560}$ modulo 561 is $263, 166, 67, 1, 1$. The term before the first 1 is $67$, a nontrivial square root of 1. So 561 is composite, although $2^{560} \equiv 1 \pmod{561}$ passes the Fermat test, and $\gcd(66, 561) = 33$, $\gcd(68, 561) = 17$ are factors.

## Where it is used

- **[Miller-Rabin](/miller-rabin/).** The test is built on the absence of nontrivial roots modulo a prime. The count of square roots, $2^r$, is also the core of the [Miller-Rabin error bound](/miller-rabin-error-bound/): for a composite, at most a quarter of the bases avoid producing a nontrivial root or a Fermat failure.
- **Factoring from a multiple of the order.** If $m$ is a known multiple of the [Carmichael function](/carmichael-function/) $\lambda(n)$, such as $ed - 1$ for an [RSA](/rsa-cryptosystem/) key pair, then repeated squaring of $a^{m/2^t}$ for a random $a$ finds a nontrivial square root of 1 with probability at least $1/2$ for odd $n$ that is not a prime power. So the RSA private exponent reveals the factors of the modulus.
- **[Shor's algorithm](/shor-algorithm/) and [order finding](/order-finding/).** If the order $r$ of $a$ modulo $n$ is even and $a^{r/2} \not\equiv -1$, then $a^{r/2}$ is a nontrivial square root of 1, and $\gcd(a^{r/2} - 1, n)$ is a factor. This is the [reduction from factoring to order finding](/factoring-to-order-finding/).
- **[Congruence of squares](/congruence-of-squares/).** The [quadratic sieve](/quadratic-sieve/) and [Dixon's method](/dixon-random-squares/) find $x^2 \equiv y^2 \pmod n$ with $x \not\equiv \pm y$; for $y$ coprime to $n$, $x y^{-1}$ is a nontrivial square root of 1, and $\gcd(x - y, n)$ is a factor.
- **[Rabin cryptosystem](/rabin-cryptosystem/).** A square modulo $n = pq$ has four square roots, which differ by the factors of the square roots of 1. An algorithm that returns square roots modulo $n$ can therefore be used to factor $n$, so breaking the system is as hard as factoring.

## References
