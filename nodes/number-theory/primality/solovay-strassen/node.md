---
tag: 4S0832
kind: algorithm
slug: solovay-strassen
name: Solovay-Strassen primality test
aliases:
- Solovay-Strassen test
- Euler-Jacobi test
area: number-theory/primality
level: core
summary: Randomized test that compares a^((n-1)/2) mod n with the Jacobi symbol (a/n) for random bases a. A mismatch proves n composite, and each round catches each odd composite with probability at least 1/2.
solves: [primality-testing]
model: multitape-turing-machine
complexity:
  vars: {n: the number tested, k: the number of rounds}
  time: {worst: O(k (log n)^3), best: O(1)}
  space: {extra: O(log n)}
properties: {deterministic: false, recursive: false, certifying: false}
history:
  year: 1977
  people: [Robert Solovay, Volker Strassen]
  note: Published in SIAM Journal on Computing in 1977 (submitted in 1974), with an erratum in 1978. It was the first efficient probabilistic primality test with an error bound for every input.
prereqs: [jacobi-symbol, euler-criterion, modular-exponentiation, fermat-primality-test]
see_also: [euler-jacobi-pseudoprime, miller-rabin, fermat-primality-test, compositeness-witness, strong-liar, probable-prime, one-sided-error, monte-carlo-algorithm]
sources:
  - paper: doi:10.1137/0206006
    title: Robert Solovay and Volker Strassen, A fast Monte-Carlo test for primality, SIAM Journal on Computing 6 (1977)
    locator: pages 84 to 85; erratum in SIAM Journal on Computing 7 (1978), page 118, doi:10.1137/0207009
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Section 4.2.2 (Fact 4.14, Definition 4.15, Example 4.16, Fact 4.17, Algorithm 4.18, Fact 4.19) and Section 4.2.4 (Fact 4.30, Example 4.31, Fact 4.32, Note 4.33)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 12.3 (computing the Jacobi symbol), Exercise 12.6, and Section 10.5 (notes)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Chapter 3, Exercises 3.21 to 3.23
---

The Solovay-Strassen test decides whether an odd integer $n$ is probably [prime](/prime-number/) by checking [Euler's criterion](/euler-criterion/) $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$ for random bases $a$, where $\left(\frac{a}{n}\right)$ is the [Jacobi symbol](/jacobi-symbol/). Every prime passes, and for every odd composite at least half of the bases fail, so $k$ rounds err with probability less than $2^{-k}$ on every input. It was the first test with such a bound, and it removed the weak point of the [Fermat test](/fermat-primality-test/), the [Carmichael numbers](/carmichael-number/). The [Miller-Rabin test](/miller-rabin/) has since replaced it in practice, because it costs the same and is never weaker.

## In plain words

For a prime number, two different calculations about a base always give the same answer. One is a remainder after raising the base to a large power. The other is a sign, plus or minus one, that a fast method like Euclid's algorithm computes. So pick a random base and do both calculations. If the answers differ, the number is certainly not prime. If they agree, the number may be prime, so try more random bases.

Unlike the simpler Fermat test, this test has no bad family of composite numbers. For every composite number at least half of the bases expose it, so each extra round at least halves the chance of a wrong answer, whatever number you test.

## The problem

The input is an integer $n \ge 0$ and a number of rounds $k \ge 1$. The output is false, which means "$n$ is not prime", or true, which means "$n$ is probably prime". This is a [Monte Carlo](/monte-carlo-algorithm/) solution of [primality testing](/primality-testing/) with [one-sided error](/one-sided-error/): false is always right, and every prime gets true.

**Cost model.** The integers are of arbitrary precision. Let $\ell = \lfloor \lg n \rfloor + 1$ be the bit length of $n$. Costs are bit operations, as on a [multitape Turing machine](/multitape-turing-machine/), with schoolbook multiplication unless stated. For $n$ below $2^w$ on a [word RAM](/word-ram/), where a product modulo $n$ costs $O(1)$, the bounds are given too.

## The algorithm

For odd $n \ge 3$ and an integer $a$, the base $a$ is an *Euler witness* for $n$ if $\left(\frac{a}{n}\right) = 0$ or $a^{(n-1)/2} \not\equiv \left(\frac{a}{n}\right) \pmod n$. For an odd composite $n$, a base with $\gcd(a, n) = 1$ that is not a witness is an *Euler liar*, and $n$ is then an [Euler-Jacobi pseudoprime](/euler-jacobi-pseudoprime/) to the base $a$ (HAC Definition 4.15).

```pseudo id=main
SOLOVAY-STRASSEN(n, k)                     ▷ true means "probably prime"
L1  if n < 4 then return n ≥ 2              ▷ 0 and 1 are not prime; 2 and 3 are prime
L2  if n is even then return false
L3  for i ← 1 to k do
L4      a ← a uniform random integer in [2, n − 2]
L5      j ← JACOBI(a, n)                    ▷ j ∈ {−1, 0, 1}
L6      if j = 0 then return false          ▷ gcd(a, n) > 1
L7      if a^((n−1)/2) mod n ≠ j mod n then return false
L8  return true
```

Lines L1 and L2 leave only odd $n \ge 5$ for the loop, so the range of line L4 is not empty. Line L5 computes the Jacobi symbol with the Euclid-like loop of Shoup (Section 12.3): reduce $a$ modulo $n$, remove factors of 2 from $a$ and flip the sign for each one when $n \equiv \pm 3 \pmod 8$, then swap $a$ and $n$ and flip the sign when both are $\equiv 3 \pmod 4$ (quadratic reciprocity). The loop ends with $a = 0$, and the result is the sign if $n = 1$ and $0$ otherwise. Line L6 rejects a base that shares a factor with $n$. Line L7 computes the power by [binary exponentiation](/binary-exponentiation/) and compares it with $j$ read as a residue, so $j = -1$ means $n - 1$.

## Example

Test the [Carmichael number](/carmichael-number/) $n = 561 = 3 \cdot 11 \cdot 17$, which passes the Fermat test for every base coprime to it. Here $(n-1)/2 = 280$.

The Jacobi symbol $\left(\frac{13}{561}\right)$ by the loop of line L5:

| step | $a$ | $n$ | action | sign |
|---|---|---|---|---|
| 1 | $13$ | $561$ | $a$ is odd; $13 \equiv 1 \pmod 4$, no flip; swap | $+1$ |
| 2 | $561 \bmod 13 = 2$ | $13$ | one factor 2 and $13 \equiv 5 \pmod 8$: flip; $a = 1$; swap | $-1$ |
| 3 | $13 \bmod 1 = 0$ | $1$ | stop with $n = 1$ | $-1$ |

So $\left(\frac{13}{561}\right) = -1$. Three rounds with the bases 2, 7 and 13:

| base $a$ | $\left(\frac{a}{561}\right)$ | $a^{280} \bmod 561$ | line L7 | verdict |
|---|---|---|---|---|
| 2 | $1$ | $1$ | $1 = 1$ | liar, the round passes |
| 7 | $1$ | $67$ | $67 \ne 1$ | witness, return false |
| 13 | $-1$ | $1$ | $1 \ne 560$ | witness, return false |

The base 13 is a Fermat liar ($13^{560} \equiv 1$) but an Euler witness: the power is $+1$ where a prime would give $-1$. Of the 320 units modulo 561, exactly 80 are Euler liars. So one round with a base from $[2, 559]$ misses with probability $78/558 \approx 0.14$, and the Fermat test misses with probability $318/558 \approx 0.57$.

For the HAC example $n = 65 = 5 \cdot 13$ (Example 4.31), the Euler liars are $1, 8, 14, 18, 47, 51, 57, 64$, out of 16 Fermat liars and 48 units.

## Correctness

The answer false is always right. Lines L1 and L2 are right by inspection. For an odd prime $n$ and $2 \le a \le n - 2$, $\gcd(a, n) = 1$, so the Jacobi symbol equals the Legendre symbol and is not 0, and Euler's criterion gives $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right)$. So lines L6 and L7 never return for a prime, and every prime gets true.

For an odd composite $n$, the Euler liars form a subgroup $E(n)$ of the [group of units](/multiplicative-group-modulo-n/) $\mathbb{Z}_n^*$, because both sides of the congruence are multiplicative in $a$. The subgroup is proper. If $p^2 \mid n$ for a prime $p$, the unit $a = 1 + n/p$ has order $p$, and a liar $a$ would satisfy $a^{n-1} \equiv 1$, so $p \mid n - 1$, which is false. If $n$ is squarefree, write $n = pm$ with $p$ prime and $m > 1$, and take $a$ with $a \equiv s \pmod p$ for a non-residue $s$ and $a \equiv 1 \pmod m$, by the [Chinese remainder theorem](/chinese-remainder-theorem/); then $\left(\frac{a}{n}\right) = -1$ while $a^{(n-1)/2} \equiv 1 \pmod m$, so $a^{(n-1)/2} \not\equiv -1 \pmod n$. By [Lagrange's theorem](/lagranges-theorem-group-theory/), $|E(n)| \le \varphi(n)/2$, and since $1$ and $n - 1$ are liars, a round with a base from $[2, n-2]$ passes with probability at most $(\varphi(n)/2 - 2)/(n - 3) < 1/2$. The full proof is in the proofs.

## Complexity

**One round.** Line L5 costs $O(\ell^2)$ bit operations: the Jacobi loop is analysed like [Euclid's algorithm](/euclidean-algorithm/), in time $O(\operatorname{len}(a) \operatorname{len}(n))$ (Shoup, Section 12.3). Line L7 is one [modular exponentiation](/modular-exponentiation/) with an exponent of $\ell - 1$ bits, so $O(\ell)$ products modulo $n$ and $O(\ell^3)$ bit operations with schoolbook arithmetic, or $O(\ell \, M(\ell))$ with a multiplication algorithm of cost $M(\ell)$. The exponentiation dominates.

**All rounds.** The worst case runs all $k$ rounds, for $O(k (\log n)^3)$ bit operations; this happens for every prime. The best case is $O(1)$ for $n < 4$ or even $n$. Each round draws $O(\log n)$ random bits. On the word RAM with $n < 2^w$, a round costs $O(\log n)$ steps and the test $O(k \log n)$.

**Space.** The base, the running power and the Jacobi loop need $O(\log n)$ bits.

**Error.** The error is one-sided: only an odd composite $n$ can get a wrong answer, and the wrong answer is true. For each odd composite $n$ the probability of true is $q^k$ with $q = (|E(n)| - 2)/(n - 3) < 1/2$. The bound holds for every input; it does not depend on the input distribution or on any conjecture. The constant $1/2$ cannot be improved in general: for $n = 1729 = 7 \cdot 13 \cdot 19$, exactly 648 of the 1296 units are Euler liars.

## Properties

- **Monte Carlo with one-sided error.** The answer false comes with a proof, the witness $a$; the answer true does not.
- **Never weaker than Fermat, never stronger than Miller-Rabin.** For odd $n$ and each base $a$, a strong liar is an Euler liar and an Euler liar is a Fermat liar (HAC Fact 4.30). So a base that exposes $n$ in this test also exposes it in the strong test of [Miller-Rabin](/miller-rabin/). For $n \equiv 3 \pmod 4$ the Euler liars and the [strong liars](/strong-liar/) are the same set (HAC Fact 4.32).
- **Uniform error bound.** At most $\varphi(n)/2$ liars for every odd composite $n$ (HAC Fact 4.17), against $\varphi(n)/4$ for Miller-Rabin. Below $10^5$ there are 36 odd composites that pass the base 2, against 78 for the Fermat test and 16 for the strong test.
- **Witnesses are short proofs.** A witness can be checked by anyone with one Jacobi symbol and one exponentiation.

## Variants and improvements

- **Fixed bases.** Test a fixed list of bases instead of random ones. The result is deterministic but, without a bound on the least witness, carries no guarantee for an adversarial $n$.
- **Deterministic under GRH.** Bach showed, under a generalization of the Riemann hypothesis, that every proper subgroup of $\mathbb{Z}_n^*$ misses some $a \le 2(\ln n)^2$ (Shoup, Section 10.5). Testing all bases up to that bound gives a deterministic polynomial test whose correctness depends on that hypothesis.
- **[Miller-Rabin](/miller-rabin/).** The strong test uses the sequence $a^d, a^{2d}, \ldots, a^{2^s d}$ with $n - 1 = 2^s d$. It needs no Jacobi symbol, has error at most $1/4$ per round, and each of its witnesses is also an Euler witness. HAC Note 4.33 recommends it over Solovay-Strassen for these reasons.
- **Lucas and Frobenius tests.** These replace powers of $a$ by Lucas sequences; combined with a strong test base 2 they give [Baillie-PSW](/baillie-psw/).

## When to use it

In new code, use [Miller-Rabin](/miller-rabin/) instead: it costs the same per round, needs no Jacobi symbol, and has the smaller error bound. Solovay-Strassen is still a clean example of a randomized algorithm whose error bound comes from a proper subgroup, and its proof needs less work than the bound $1/4$ for Miller-Rabin. When a proof of primality is needed, use a proving method such as [ECPP](/ecpp/) or the [AKS test](/aks-primality-test/).

## Pitfalls

- **Skipping the zero test.** If line L6 is left out, a base with $\gcd(a, n) > 1$ can pass: for $n = 9$ and $a = 3$, $3^4 = 81 \equiv 0$ and $\left(\frac{3}{9}\right) = 0$, so the two sides agree. Reject $j = 0$ first.
- **Comparing $-1$ with a residue.** The power is in $[0, n-1]$ and the symbol is $-1$, $0$ or $1$. Compare with $j \bmod n$, so that $-1$ becomes $n - 1$.
- **Legendre rules for a composite modulus.** The Jacobi symbol $\left(\frac{a}{n}\right) = 1$ does not mean that $a$ is a square modulo a composite $n$, and Euler's criterion does not hold for composite $n$. That failure is what the test detects; do not compute the symbol by a power.
- **Even modulus in the Jacobi loop.** The Jacobi symbol is defined only for odd positive $n$. Line L2 must run before line L5.
- **Bases 1 and n − 1.** Both always pass for odd $n$: $(-1)^{(n-1)/2} = \left(\frac{-1}{n}\right)$. Draw from $[2, n-2]$.
- **Recursion depth.** A recursive Jacobi function on numbers of thousands of bits recurses $O(\log n)$ times; a loop is safer and as fast.

## Implementations

## History

Solovay and Strassen published the test in 1977 in the SIAM Journal on Computing, under the title "A fast Monte-Carlo test for primality", and an erratum followed in 1978. Shoup (Section 10.5) notes that their paper was submitted in 1974 and calls it the first efficient probabilistic primality test. Crandall and Pomerance (Exercise 3.22) credit the proper subgroup property of the Euler liars to Lehmer as well as to Solovay and Strassen. The strong test of Miller (1976) and Rabin (1980) gives a smaller error per round, and the Handbook of Applied Cryptography (Note 4.33) recommends it over Solovay-Strassen.

## References
