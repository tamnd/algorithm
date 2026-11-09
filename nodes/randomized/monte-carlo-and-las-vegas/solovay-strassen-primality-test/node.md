---
tag: XD7T81
kind: algorithm
slug: solovay-strassen-primality-test
name: Solovay-Strassen primality test
aliases:
- Euler-Jacobi test
- Solovay-Strassen test
area: randomized/monte-carlo-and-las-vegas
level: advanced
summary: Tests n by checking Euler's criterion a^((n-1)/2) = (a/n) mod n for random bases, with the Jacobi symbol; a random base catches a composite with probability at least 1/2.
solves: [primality-testing]
model: word-ram
complexity:
  vars: {n: the integer to test, k: the number of rounds}
  time: {worst: O(k log^3 n)}
  space: {extra: O(log n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1977
  people: [Robert Solovay, Volker Strassen]
  note: Solovay and Strassen published the test in the SIAM Journal on Computing in 1977, the first randomized primality test with a proved error bound.
prereqs: [jacobi-symbol, euler-criterion, modular-exponentiation, one-sided-error]
see_also: [miller-rabin-primality-test, jacobi-symbol, euler-criterion, euler-jacobi-pseudoprime, fermat-primality-test, carmichael-number, quadratic-reciprocity, error-amplification]
sources:
  - paper: doi:10.1137/0206006
    title: Robert Solovay and Volker Strassen, A fast Monte-Carlo test for primality, SIAM Journal on Computing 6(1), 1977
    locator: pages 84 to 85 (the test, and the proof that at most half of the bases are liars)
  - paper: doi:10.1016/0304-3975(80)90007-9
    title: Louis Monier, Evaluation and comparison of two efficient probabilistic primality testing algorithms, Theoretical Computer Science 12(1), 1980
    locator: pages 97 to 108 (the number of Euler liars, and the comparison with the strong test)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 2.3 (the Jacobi symbol and its computation by reciprocity) and Section 3.5 (Euler pseudoprimes and their relation to strong pseudoprimes)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 14, Number theoretic algorithms (the Solovay-Strassen test)
  - paper: doi:10.1090/S0025-5718-1990-1023756-8
    title: Eric Bach, Explicit bounds for primality testing and related problems, Mathematics of Computation 55(191), 1990
    locator: pages 355 to 380 (under the extended Riemann hypothesis, a witness in the sense of Solovay and Strassen below 2 (ln n)^2)
---

The Solovay-Strassen test decides whether an odd integer $n$ is prime by checking [Euler's criterion](/euler-criterion/) for random bases $a$: for a prime $n$, $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$, where $\left(\frac{a}{n}\right)$ is the [Jacobi symbol](/jacobi-symbol/). The Jacobi symbol can be computed fast without factoring $n$, by [quadratic reciprocity](/quadratic-reciprocity/). For an odd composite $n$, the bases that satisfy the criterion form a proper subgroup of the units, so at most half of the bases are liars. The test is a [Monte Carlo algorithm](/monte-carlo-algorithm/) with [one-sided error](/one-sided-error/): COMPOSITE is always right, and PROBABLY PRIME is wrong with probability at most $2^{-k}$ after $k$ rounds. The [Miller-Rabin test](/miller-rabin-primality-test/) is stronger: every strong liar is an Euler liar, and its error per round is at most $1/4$.

## In plain words

For a prime $n$, raising a base to the power $(n-1)/2$ gives $1$ or $n - 1$, and which one it gives is decided by a simple rule: whether the base is a perfect square modulo $n$. That rule can be computed by a quick method much like the method for the greatest common divisor, even when the factors of $n$ are unknown.

The test picks a random base, computes the power and the rule, and compares. A prime always agrees. A composite number disagrees for at least half of the bases, because the agreeing bases form a closed family that cannot fill the whole group. So each round at least halves the chance that a composite slips through.

## The problem

Given an integer $n \ge 1$, decide whether $n$ is prime. See [primality testing](/primality-testing/). The input size is $\log_2 n$ bits.

Notation on this page: $e = (n-1)/2$; $\left(\frac{a}{n}\right)$ is the Jacobi symbol; $\varphi$ is [Euler's totient](/euler-totient/); $\Pr$ is over the bases. A base $a$ is an **Euler liar** for an odd composite $n$ if $\left(\frac{a}{n}\right) \ne 0$ and $a^{e} \equiv \left(\frac{a}{n}\right) \pmod n$, and a witness otherwise. A composite $n$ that passes for a base $a$ is an [Euler-Jacobi pseudoprime](/euler-jacobi-pseudoprime/) to base $a$. Randomness model: each base is uniform on $\{2, \dots, n - 2\}$, drawn by rejection from uniform random bits.

## The algorithm

```pseudo id=main
SOLOVAY-STRASSEN(n, k)
L1  if n ∈ {2, 3} then return PRIME;  if n < 2 or n even then return COMPOSITE
L2  for i ← 1 to k do
L3      a ← uniform integer in {2, ..., n − 2}
L4      j ← JACOBI(a, n)
L5      if j = 0 then return COMPOSITE            ▷ gcd(a, n) > 1
L6      if a^((n−1)/2) mod n ≠ j mod n then return COMPOSITE
L7  return PROBABLY PRIME                         ▷ wrong with probability at most 2^-k

JACOBI(a, n)                                      ▷ n odd and positive
L8  a ← a mod n;  t ← 1
L9  while a ≠ 0 do
L10     while a is even do a ← a / 2; if n mod 8 ∈ {3, 5} then t ← −t
L11     swap a and n
L12     if a mod 4 = 3 and n mod 4 = 3 then t ← −t      ▷ quadratic reciprocity
L13     a ← a mod n
L14 return t if n = 1, else 0
```

Line L5 matters: for $n = 9$ and $a = 3$, $3^4 = 81 \equiv 0 \pmod 9$ and $\left(\frac{3}{9}\right) = 0$, so the two sides of line L6 agree, and only line L5 rejects. In line L6, $j \bmod n$ turns $-1$ into $n - 1$.

## Example

**A Carmichael number.** $n = 561 = 3 \cdot 11 \cdot 17$, so $e = 280$. The [Fermat test](/fermat-primality-test/) passes for every base coprime to 561.

| $a$ | $\left(\frac{a}{561}\right)$ (line L4) | $a^{280} \bmod 561$ | line L6 |
| --- | --- | --- | --- |
| 2 | 1 | 1 | pass, 2 is an Euler liar |
| 5 | 1 | 67 | COMPOSITE |
| 7 | 1 | 67 | COMPOSITE |

JACOBI$(5, 561)$: $5$ is odd; swap to $(561, 5)$; $5 \equiv 1 \pmod 4$, so no sign change; $561 \bmod 5 = 1$; swap to $(5, 1)$; $5 \bmod 1 = 0$; $n = 1$, so the result is $t = 1$. Here $67^2 \equiv 1$, so $67$ is a nontrivial square root of 1 and a Miller-Rabin round with base 5 also finds it. 561 has 80 Euler liars among its 320 units, so a random base from $\{2, \dots, 559\}$ fools one round with probability $78/558 \approx 0.14$; for Miller-Rabin the rate is $8/558$.

**A liar of a product of two primes.** $n = 221 = 13 \cdot 17$, $e = 110$. For $a = 174$ and $a = 47$, the symbol is $-1$ and the power is $220 \equiv -1$, so both are Euler liars.

**A prime.** $n = 97$, $a = 5$: $\left(\frac{5}{97}\right) = -1$ and $5^{48} \equiv 96 \equiv -1$, as Euler's criterion requires.

**A composite with symbol 1.** $n = 1001 = 7 \cdot 11 \cdot 13$, $a = 2$: $\left(\frac{2}{1001}\right) = 1$ but $2^{500} \equiv 529$, so line L6 returns COMPOSITE.

## Correctness

Line L14 returns the Jacobi symbol: the loop keeps $t \cdot \left(\frac{a}{n}\right)$ equal to the symbol of the input, using the rule for $\left(\frac{2}{n}\right)$ in line L10 and reciprocity in line L12, and it ends like the Euclidean algorithm. For a prime $n$ the Jacobi symbol is the [Legendre symbol](/legendre-symbol/), and Euler's criterion says that every base passes, so COMPOSITE is always right. For an odd composite $n$, the Euler liars are units and are closed under products, so they form a subgroup of $\mathbb{Z}_n^*$. It is proper: if $p^2 \mid n$, the unit $1 + n/p$ has order $p$, which does not divide $n - 1$; if $n = pm$ is squarefree, a unit that is a non-residue modulo $p$ and 1 modulo $m$ has symbol $-1$ but power 1 modulo $m$. By [Lagrange's theorem](/lagranges-theorem-group-theory/) at most $\varphi(n)/2$ bases are liars. The [full proof](proofs/correctness.md) gives the details and shows that the bound is reached.

## Complexity

- **Time.** The exponentiation of line L6 costs $O(\log n)$ multiplications modulo $n$, so $O(\log^3 n)$ bit operations with schoolbook multiplication. JACOBI costs $O(\log n)$ passes like the Euclidean algorithm, $O(\log^2 n)$ bit operations in total. $k$ rounds cost $O(k \log^3 n)$.
- **Rounds for a target error.** Error $\delta$ needs $k = \lceil \log_2(1/\delta) \rceil$ rounds by the worst-case bound: 20 for $10^{-6}$ and 64 for $2^{-64}$, twice as many as Miller-Rabin. See [error amplification](/error-amplification/).
- **Space.** $O(\log n)$ bits.

## Properties

- **One-sided error.** COMPOSITE is always right, and the base $a$ is a witness that anyone can check.
- **Error at most 1/2, and this is reached.** The Carmichael numbers 1729 and 2465 have exactly $\varphi(n)/2$ Euler liars: 648 of 1296 and 896 of 1792. No odd composite below 1500 reaches $\varphi(n)/2$.
- **Weaker than Miller-Rabin.** Every strong liar is an Euler liar (proved on the [Miller-Rabin page](/miller-rabin-primality-test/)), so a Miller-Rabin round with the same base catches at least the same composites. The inclusion can be strict: $n = 45$ has 2 strong liars and 4 Euler liars; 561 has 10 and 80. For $n \equiv 3 \pmod 4$ the two sets are equal.
- **No bad inputs.** Unlike the Fermat test, the bound holds for every odd composite. The Carmichael numbers below 10000 have a quarter or a half of their units as Euler liars: 80 of 320 for 561, 540 of 2160 for 2821, 1782 of 7128 for 8911.
- **A proper subgroup argument.** The proof needs only that the liars form a proper subgroup, so it is the simplest proof of a constant error bound for a primality test.

## Variants and improvements

- **Deterministic under the extended Riemann hypothesis.** The liars form a proper subgroup of $\mathbb{Z}_n^*$, and under the hypothesis every proper subgroup misses some number below $2(\ln n)^2$ (Bach 1990). So testing all bases up to this bound is a deterministic test, correct if the hypothesis holds.
- **The strong test.** Miller-Rabin replaces the comparison with the Jacobi symbol by the sequence $a^d, a^{2d}, \dots$; it is simpler, faster and has error at most $1/4$. In practice it has replaced Solovay-Strassen.
- **Euler test without the Jacobi symbol.** Checking only $a^{e} \equiv \pm 1$ is weaker: every Euler liar passes it, and so do bases whose power has the wrong sign.

## When to use it

- To teach randomized primality testing: the proof of the bound $1/2$ is short and complete.
- When a library already has a fast Jacobi symbol and the code must be short.
- In practice, prefer [Miller-Rabin](/miller-rabin-primality-test/): it is at least as strong for each base, has a better bound, and needs no Jacobi symbol.

## Pitfalls

- **Comparing $-1$ with $n - 1$.** The symbol is $-1$ and the power is $n - 1$. Reduce the symbol modulo $n$ before the comparison of line L6.
- **Skipping the test $j = 0$.** For $n = 9$ and $a = 3$ both sides are 0, and a check with only line L6 would pass a composite.
- **Using the Legendre formula for composite $n$.** $a^{(n-1)/2} \bmod n$ is not the Jacobi symbol when $n$ is composite; the whole test is the comparison of the two.
- **Even $n$.** The Jacobi symbol is defined only for odd $n$. Line L1 handles even $n$.
- **Counting rounds as for Miller-Rabin.** With the bound $1/2$, twice as many rounds are needed for the same error.

## Implementations

## History

Robert Solovay and Volker Strassen published the test in 1977, as "a fast Monte-Carlo test for primality". It was the first primality test with a proved bound on its error for every input, and it showed that the composite numbers are in RP, so the primes are in [co-RP](/co-rp/). With Rabin's test of 1980 it made randomized algorithms widely known, and it was an early example used to argue for randomness in computation. Monier (1980) and Rabin (1980) showed that the strong test of Miller is better. Agrawal, Kayal and Saxena gave a deterministic polynomial-time test in 2002.

## References
