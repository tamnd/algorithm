---
tag: AB3V76
kind: definition
slug: carmichael-number
name: Carmichael number
aliases:
- absolute Fermat pseudoprime
- Carmichael
area: number-theory/primality
level: core
summary: Composite n that is a Fermat pseudoprime to every base coprime to n; by Korselt's criterion, a squarefree n with p - 1 dividing n - 1 for each prime p dividing n.
prereqs: [fermat-pseudoprime, chinese-remainder-theorem, primitive-roots-existence]
see_also: [fermat-primality-test, fermat-pseudoprime, carmichael-function, miller-rabin, strong-pseudoprime, euler-jacobi-pseudoprime, solovay-strassen, compositeness-witness]
sources:
  - paper: doi:10.1090/S0002-9904-1910-01892-9
    title: R. D. Carmichael, Note on a new number theory function, Bulletin of the American Mathematical Society 16 (1910)
    locator: pages 232 to 238 (the example 561 = 3 · 11 · 17)
  - paper: doi:10.2307/2118576
    title: W. R. Alford, Andrew Granville and Carl Pomerance, There are infinitely many Carmichael numbers, Annals of Mathematics 139 (1994)
    locator: pages 703 to 722 (main theorem, C(x) > x^(2/7) for large x)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.4.2, Carmichael numbers (Korselt's criterion and the Chernick family)
  - url: https://oeis.org/A055553
    title: OEIS A055553, Number of Carmichael numbers less than 10^n
    locator: the data terms, from the computations of R. G. E. Pinch
  - url: https://arxiv.org/abs/math/0604376
    title: Richard G. E. Pinch, The Carmichael numbers up to 10^18
    locator: the table of counts
---

A Carmichael number is a composite integer $n$ that satisfies $a^{n-1} \equiv 1 \pmod n$ for every integer $a$ coprime to $n$. So it is a [Fermat pseudoprime](/fermat-pseudoprime/) to every base it could be tested against without a common factor, and the [Fermat primality test](/fermat-primality-test/) finds it composite only when a random base happens to share a factor with it. The smallest is $561 = 3 \cdot 11 \cdot 17$. Korselt's criterion turns the definition into a test on the prime factors, and Alford, Granville and Pomerance proved in 1994 that there are infinitely many.

## Definition

A **Carmichael number** is a composite integer $n \ge 2$ such that

$$a^{n-1} \equiv 1 \pmod n \quad \text{for every integer } a \text{ with } \gcd(a, n) = 1.$$

In terms of the [Carmichael function](/carmichael-function/) $\lambda(n)$, the exponent of the [group of units](/multiplicative-group-modulo-n/) $(\mathbb{Z}/n\mathbb{Z})^*$, the condition says $\lambda(n) \mid n - 1$.

**Korselt's criterion (1899).** A composite $n$ is a Carmichael number if and only if $n$ is squarefree and $p - 1 \mid n - 1$ for every prime $p \mid n$.

*Proof.* Suppose first that $n$ is squarefree and $p - 1 \mid n - 1$ for each prime $p \mid n$. Let $\gcd(a, n) = 1$. For each $p \mid n$, [Fermat's little theorem](/fermat-little-theorem/) gives $a^{p-1} \equiv 1 \pmod p$, so $a^{n-1} \equiv 1 \pmod p$. The primes $p$ are distinct and their product is $n$, so $a^{n-1} \equiv 1 \pmod n$.

Conversely, let $n$ be a Carmichael number. Then $n$ is odd: for an even $n \ge 4$, the base $a = n - 1$ is coprime to $n$ and $(n-1)^{n-1} \equiv (-1)^{n-1} = -1 \not\equiv 1 \pmod n$. Let $p$ be a prime with $p^e \parallel n$, $e \ge 1$. As $p$ is odd, $(\mathbb{Z}/p^e\mathbb{Z})^*$ is cyclic of order $p^{e-1}(p-1)$ ([existence of primitive roots](/primitive-roots-existence/)); let $g$ generate it. By the [Chinese remainder theorem](/chinese-remainder-theorem/) there is an $a$ with $a \equiv g \pmod{p^e}$ and $a \equiv 1 \pmod{n/p^e}$. This $a$ is coprime to $n$, so $a^{n-1} \equiv 1 \pmod{p^e}$, so the order $p^{e-1}(p-1)$ of $g$ divides $n - 1$. Since $p \mid n$, $p \nmid n - 1$, so $e = 1$, and $p - 1 \mid n - 1$. $\square$

**Basic properties.** Let $n$ be a Carmichael number.

- $n$ is odd, by the proof above.
- $n$ has at least three prime factors. If $n = pq$ with primes $p < q$, then $q - 1 \mid n - 1 = p(q - 1) + (p - 1)$, so $q - 1 \mid p - 1$, which is impossible as $0 < p - 1 < q - 1$.
- Each prime factor $p$ satisfies $p < \sqrt n$. Write $n = pm$. Then $n - 1 = (p - 1)m + (m - 1)$, so $p - 1 \mid m - 1$; as $m > 1$, $m \ge p$, and $m \ne p$ since $n$ is squarefree. So $p^2 < pm = n$.

## Examples and non-examples

**Examples.**

- $561 = 3 \cdot 11 \cdot 17$: $n - 1 = 560 = 2^4 \cdot 5 \cdot 7$, and $2$, $10$, $16$ all divide 560. It is the smallest Carmichael number.
- $1105 = 5 \cdot 13 \cdot 17$ ($4$, $12$, $16$ divide $1104$) and $1729 = 7 \cdot 13 \cdot 19$ ($6$, $12$, $18$ divide $1728$).
- The Carmichael numbers below $10^5$ are $561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973, 75361$. The first with four prime factors is $41041 = 7 \cdot 11 \cdot 13 \cdot 41$, and the first with five is $825265 = 5 \cdot 7 \cdot 17 \cdot 19 \cdot 73$.
- **Chernick's family (1939).** If $6k + 1$, $12k + 1$ and $18k + 1$ are all prime, then $n = (6k+1)(12k+1)(18k+1)$ is a Carmichael number. Indeed $n - 1 = 36k(36k^2 + 11k + 1)$, which is divisible by $6k$, $12k$ and $18k$. For $k = 1, 6, 35, 45$ this gives $1729$, $294409$, $56052361$ and $118901521$. It is not known whether the family is infinite.

**Non-examples.**

- $341 = 11 \cdot 31$ is a Fermat pseudoprime to the base 2 but not a Carmichael number: $30 \nmid 340$, and $3^{340} \equiv 56 \pmod{341}$.
- $15 = 3 \cdot 5$ has two prime factors, and $4 \nmid 14$.
- $45 = 3^2 \cdot 5$ is not squarefree. No number divisible by $p^2$ for a prime $p$ is a Carmichael number.
- A prime $p$ satisfies the congruence for every base coprime to it, but it is not a Carmichael number, which must be composite.

**How many there are.** The counts below $10^3, 10^4, \ldots, 10^7$ are $1, 7, 16, 43, 105$. Pinch counted $1401644$ below $10^{18}$ and $20138200$ below $10^{21}$. Alford, Granville and Pomerance (1994) proved that the count $C(x)$ below $x$ satisfies $C(x) > x^{2/7}$ for all large $x$, so there are infinitely many. Still they are much rarer than primes: there are about $2.1 \cdot 10^{19}$ primes below $10^{21}$.

**Why they matter for testing.** For a Carmichael number $n$ the only Fermat witnesses are bases sharing a factor with $n$, and their share among $[2, n - 2]$ is about $1 - \varphi(n)/n \le \sum_{p \mid n} 1/p$, which is tiny when all prime factors are large. So the Fermat test, repeated any number of times, can accept a Carmichael number with probability close to 1. The stronger tests do not have this gap:

| $n$ | units $\varphi(n)$ | Fermat liars | [Euler-Jacobi](/euler-jacobi-pseudoprime/) liars | [strong](/strong-pseudoprime/) liars |
|---|---|---|---|---|
| 561 | 320 | 320 | 80 | 10 |
| 1105 | 768 | 768 | 192 | 30 |
| 1729 | 1296 | 1296 | 648 | 162 |

Every composite has at most $\varphi(n)/2$ Euler-Jacobi liars, so [Solovay-Strassen](/solovay-strassen/) catches Carmichael numbers, and at most $\varphi(n)/4$ strong liars, so [Miller-Rabin](/miller-rabin/) catches them (see the [Miller-Rabin error bound](/miller-rabin-error-bound/)).
**History.** Václav Šimerka listed the first seven Carmichael numbers in 1885. Alwin Korselt gave the criterion in 1899 without an example. Robert Carmichael found 561 in 1910, and the numbers were named after him.

## Related definitions

- [Fermat pseudoprime](/fermat-pseudoprime/): composite with $a^{n-1} \equiv 1 \pmod n$ for one base $a$. A Carmichael number is one for all coprime bases at once.
- [Carmichael function](/carmichael-function/): $\lambda(n)$, the least $m$ with $a^m \equiv 1$ for all units; $n$ composite is a Carmichael number exactly when $\lambda(n) \mid n - 1$.
- [Euler-Jacobi pseudoprime](/euler-jacobi-pseudoprime/) and [strong pseudoprime](/strong-pseudoprime/): stronger notions. No composite is an Euler-Jacobi or strong pseudoprime to every base coprime to it, so there is no analogue of a Carmichael number for these tests.
- [Compositeness witness](/compositeness-witness/): a Carmichael number has no Fermat witness among the units, but it has many Miller-Rabin witnesses.

## References
