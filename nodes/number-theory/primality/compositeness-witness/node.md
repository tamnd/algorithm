---
tag: W6Z2BR
kind: concept
slug: compositeness-witness
name: Compositeness witness
aliases:
- witness of compositeness
area: number-theory/primality
level: core
summary: A base that proves a number is composite when a test fails on it.
prereqs: [prime-number, fermat-little-theorem, modular-exponentiation]
see_also: [miller-rabin, fermat-primality-test, solovay-strassen, strong-liar, nontrivial-square-root-of-one, deterministic-miller-rabin-bases, certificate, one-sided-error]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.8, Primality testing (the procedure WITNESS and the bound on the number of witnesses)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.5, Probable primes and witnesses (including Section 3.5.1, The least witness for n)
  - paper: doi:10.1016/0022-314X(80)90084-0
    title: Michael O. Rabin, Probabilistic algorithm for testing primality, Journal of Number Theory 12 (1980)
    locator: pages 128 to 138 (at most a quarter of the bases are not witnesses)
  - paper: doi:10.1090/S0025-5718-1990-1023756-8
    title: Eric Bach, Explicit bounds for primality testing and related problems, Mathematics of Computation 55 (1990)
    locator: pages 355 to 380 (under GRH, the least witness is below 2 (ln n)^2)
---

A compositeness witness for an integer $n$ is a value, usually a base $a$, on which a primality condition that every [prime](/prime-number/) satisfies fails for $n$. Once a witness is known, anyone can check in polynomial time that $n$ is composite, often without learning any factor. The probabilistic tests, [Fermat](/fermat-primality-test/), [Solovay-Strassen](/solovay-strassen/) and [Miller-Rabin](/miller-rabin/), work by sampling bases and hoping to hit a witness; their error bounds are lower bounds on how many witnesses each composite has.

## In plain words

Primes obey certain rules that can be checked quickly with a helper number. If a number breaks one of these rules for some helper, the number cannot be prime. The helper is then a witness: it is proof, which anyone can check again, that the number is composite.

A witness does not have to show how the number splits into factors. It only shows that some split exists. For the good tests, most helpers are witnesses for every composite number, so a few random helpers find one with high probability. The helpers that fail to expose a composite number are called liars.

## The idea

Fix a predicate $P(n, a)$ that can be computed fast and that holds for every prime $n$ and every base $a$ in a range $B(n)$. A **witness** for $n$ is an $a \in B(n)$ with $P(n, a)$ false; by the property of $P$, $n$ is then composite. A base $a$ for which $P(n, a)$ holds although $n$ is composite is a **liar** for $n$. The common predicates, for odd $n \ge 3$ and $1 \le a \le n - 1$:

| witness type | $P(n, a)$ (true for each prime $n$) | share of witnesses for each odd composite |
|---|---|---|
| divisor witness | $\gcd(a, n) = 1$ | $1 - \varphi(n)/(n-1)$, can be tiny |
| Fermat witness | $a^{n-1} \equiv 1 \pmod n$ | at least $1/2$ unless $n$ is a [Carmichael number](/carmichael-number/) |
| Euler witness | $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \not\equiv 0 \pmod n$, with the [Jacobi symbol](/jacobi-symbol/) | at least $1/2$ |
| strong (Miller) witness | $n - 1 = 2^s d$, $d$ odd: $a^d \equiv 1$, or $a^{2^j d} \equiv -1$ for some $0 \le j < s$ | at least $3/4$ |

The first column moves from weak to strong: each strong liar is an Euler liar ([Euler-Jacobi pseudoprime](/euler-jacobi-pseudoprime/) base), and each Euler liar is a Fermat liar ([Fermat pseudoprime](/fermat-pseudoprime/) base). A strong witness either breaks the Fermat condition or shows a [nontrivial square root of 1](/nontrivial-square-root-of-one/) modulo $n$. The bound $3/4$ is the [Miller-Rabin error bound](/miller-rabin-error-bound/) of Rabin and Monier; the strong liars are the [strong liars](/strong-liar/).

**Witnesses are certificates.** Checking a Fermat, Euler or strong witness costs one [modular exponentiation](/modular-exponentiation/), $O((\log n)^3)$ bit operations with schoolbook multiplication. So a witness is a short [certificate](/certificate/) of compositeness, like a factor, which puts compositeness in [NP](/np/). A factor reveals more, but finding one is much harder: $2^{1277} - 1$ has the Fermat witness 3, while no factor of it is known.

**Many witnesses give a fast randomized test.** If every odd composite has at least a fraction $c$ of witnesses in $B(n)$, then $k$ independent random bases all miss with probability at most $(1 - c)^k$, and a prime is never rejected. This is a [Monte Carlo](/monte-carlo-algorithm/) algorithm with [one-sided error](/one-sided-error/), and it puts compositeness in [RP](/rp/) and primality in [co-RP](/co-rp/).

**The least witness.** Instead of sampling, a deterministic test may try the bases $2, 3, 4, \ldots$ in order until it finds a witness, and stop at a bound. Under the generalized Riemann hypothesis (GRH), Bach (1990) proved that each odd composite $n$ has a strong witness below $2 (\ln n)^2$, which gives Miller's deterministic test; the bound is conditional on GRH. Without GRH no polynomial bound on the least witness is known. For $n$ below fixed limits, finite sets of bases are known to contain a witness for every composite, by exhaustive search; see [deterministic Miller-Rabin bases](/deterministic-miller-rabin-bases/).

## Examples

- **$n = 341 = 11 \cdot 31$.** The base 2 is a Fermat liar: $2^{340} \equiv 1$. It is a strong witness: $340 = 2^2 \cdot 85$, and $2^{85} \equiv 32$, $32^2 \equiv 1 \pmod{341}$, so $32$ is a nontrivial square root of 1. The base 3 is a Fermat witness: $3^{340} \equiv 56$. Of the bases $1, \ldots, 340$, 240 are Fermat witnesses and 290 are strong witnesses.
- **$n = 561 = 3 \cdot 11 \cdot 17$**, a Carmichael number. Its only Fermat witnesses are the 240 bases sharing a factor with it, while 550 of the 560 bases are strong witnesses; 2 is one of them.
- **$n = 2047 = 23 \cdot 89$.** The base 2 is a strong liar, and 2047 is the smallest odd composite for which 2 is not a strong witness. The base 3 is a strong witness. Below $1373653$, each odd composite has a strong witness in $\{2, 3\}$.
- **$n = 9$.** The strong liars are $1$ and $8$, so $6$ of the $8$ bases are witnesses, exactly $3/4$. So the share $3/4$ is reached, and the bound on strong liars as a share of $\varphi(n)$ needs $n > 9$.
- **Large $n$.** $3^{M - 1} \not\equiv 1 \pmod M$ for $M = 2^{1277} - 1$, so 3 is a Fermat witness, a certificate of compositeness of a 385-digit number with no known factor.

## Where it is used

- **Randomized primality tests.** [Fermat](/fermat-primality-test/), [Solovay-Strassen](/solovay-strassen/) and [Miller-Rabin](/miller-rabin/) sample random bases; the share of witnesses gives the error per round. In [random prime generation](/random-prime-generation/) for RSA, most composite candidates are rejected by the first base.
- **Deterministic tests for bounded inputs.** Fixed witness sets such as $\{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37\}$ decide primality for all $n < 2^{64}$; see [deterministic Miller-Rabin bases](/deterministic-miller-rabin-bases/) and [Baillie-PSW](/baillie-psw/).
- **Complexity theory.** Compositeness has short certificates (witnesses or factors), and primality has [Pratt certificates](/pratt-certificate/), so primality is in $\mathrm{NP} \cap \mathrm{co\text{-}NP}$. The density of witnesses gave the early membership in [co-RP](/co-rp/), years before the [AKS test](/aks-primality-test/) put primality in [P](/p/).
- **Factoring.** A strong witness that exposes a nontrivial square root $x$ of 1 also gives the factor $\gcd(x - 1, n)$. Fermat and Euler witnesses alone do not give a factor.

## References
