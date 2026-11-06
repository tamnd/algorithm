---
tag: 1P82VA
kind: algorithm
slug: euler-phi-sieve
name: Euler totient sieve
aliases:
- totient sieve
- phi sieve
- Euler phi sieve
area: number-theory/sieves
level: intro
summary: Compute phi(m) for all m up to n. Start with phi[m] = m, and for each prime p subtract phi[m]/p from every multiple m of p. It takes Θ(n log log n) word operations and n + 1 words.
solves: [totient-values-up-to-n]
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Θ(n log log n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [euler-totient, sieve-of-eratosthenes]
see_also: [totient-values-up-to-n, linear-sieve, sieve-of-eratosthenes, multiplicative-functions-up-to-n, mobius-sieve, divisor-count-sieve, counting-coprime-pairs]
sources:
  - url: https://cp-algorithms.com/algebra/phi-function.html
    title: Euler's totient function, cp-algorithms
    locator: Section Euler totient function from 1 to n in O(n log log n)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition, Oxford University Press, 2008
    locator: Section 5.5 (the product formula for phi(m)) and Theorem 427 (Mertens, the sum of 1/p over primes p up to x)
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 2 (the product formula for the totient)
---

The Euler totient sieve computes [Euler's totient](/euler-totient/) $\varphi(m)$ for every $m \le n$ at once. It starts with $\varphi[m] = m$, and for each prime $p$ it replaces $\varphi[m]$ by $\varphi[m] - \varphi[m]/p$ at every multiple $m$ of $p$, which applies the factor $1 - 1/p$ of the product formula. It solves [totient values up to n](/totient-values-up-to-n/) in $\Theta(n \log \log n)$ word operations with only the output array, and it finds the primes along the way, as the [sieve of Eratosthenes](/sieve-of-eratosthenes/) does.

## In plain words

The number of values below a number that share no factor with it can be found by starting from the number itself and taking away a share for each prime that divides it. For the prime two, take away half. For the prime three, take away a third of what is left, and so on.

The sieve does this for all numbers at once. Each entry starts as its own number. For each prime, go through all its multiples and take away the right share from each. An entry that is still equal to its own number when you reach it has no smaller prime factor, so it is a prime.

## The problem

The input is an integer $n \ge 0$. The output is the array $\varphi[1 \ldots n]$ of [totient values up to n](/totient-values-up-to-n/), where

$$\varphi(m) = m \prod_{p \mid m} \left( 1 - \frac{1}{p} \right).$$

The cost model is the [word RAM](/word-ram/): arithmetic, including integer division, comparisons and array access on numbers up to $n$ cost one step. The array has $n + 1$ words and is the output; the extra memory is $O(1)$ words.

## The algorithm

```pseudo id=main
PHI-SIEVE(n)                               ▷ returns φ[0 .. n], with φ[0] = 0
L1  for m ← 0 to n do φ[m] ← m
L2  for p ← 2 to n do
L3      if φ[p] = p then                   ▷ no smaller prime divides p, so p is prime
L4          for m ← p, 2p, 3p, … while m ≤ n do
L5              φ[m] ← φ[m] − φ[m] / p     ▷ the division is exact
L6  return φ
```

Line L5 multiplies $\varphi[m]$ by $1 - 1/p$ without fractions. The division is exact: at that moment $\varphi[m] = m \prod_q (1 - 1/q)$ over the primes $q < p$ that divide $m$, and $p$ divides this number, since it divides $m$ and none of the $q$. The loop of line L2 must run up to $n$, not $\sqrt n$, because a prime $p > \sqrt n$ still divides its multiples up to $n$.

## Example

Take $n = 12$. The rows show the array $\varphi[1 \ldots 12]$ after the round of each prime.

| after | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| line L1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| $p = 2$ | 1 | 1 | 3 | 2 | 5 | 3 | 7 | 4 | 9 | 5 | 11 | 6 |
| $p = 3$ | 1 | 1 | 2 | 2 | 5 | 2 | 7 | 4 | 6 | 5 | 11 | 4 |
| $p = 5$ | 1 | 1 | 2 | 2 | 4 | 2 | 7 | 4 | 6 | 4 | 11 | 4 |
| $p = 7$ | 1 | 1 | 2 | 2 | 4 | 2 | 6 | 4 | 6 | 4 | 11 | 4 |
| $p = 11$ | 1 | 1 | 2 | 2 | 4 | 2 | 6 | 4 | 6 | 4 | 10 | 4 |

At $p = 4$, line L3 finds $\varphi[4] = 2 \ne 4$ and skips; the same happens at 6, 8, 9, 10 and 12. For $m = 12$, the round of 2 gives $12 - 6 = 6$ and the round of 3 gives $6 - 2 = 4$.

## Correctness

The proof is an invariant of the loop of line L2: when the loop reaches $p$, each entry is $\varphi[m] = m \prod_q (1 - 1/q)$, with the product over the primes $q < p$ that divide $m$. This value is an integer, and line L5 keeps the invariant because its division is exact. The test of line L3 is right: if $p$ is prime, no prime $q < p$ divides it, so $\varphi[p] = p$; if $p$ is composite, some prime $q < p$ divides it, and $\varphi[p] \le p (1 - 1/q) < p$. When the loop ends, every prime factor of each $m \le n$ is at most $n$, so the product is complete. The full proof is below.

## Complexity

Line L5 runs $\lfloor n/p \rfloor$ times for each prime $p \le n$, so the number of updates is

$$U(n) = \sum_{p \le n} \left\lfloor \frac{n}{p} \right\rfloor = n \ln \ln n + O(n),$$

by Mertens' theorem $\sum_{p \le x} 1/p = \ln \ln x + B + o(1)$, which is proved without any conjecture (Hardy and Wright, Theorem 427). Lines L1 to L3 cost $O(n)$. So the time is $\Theta(n \log \log n)$ word operations, a proved bound. Each update needs one division.

| $n$ | updates of line L5 | $n \ln \ln n$ |
|---|---|---|
| $10^4$ | 24300 | 22203 |
| $10^6$ | 2853708 | 2625792 |

The memory is the output array of $n + 1$ words and $O(1)$ more words. No flag table is needed, because the test $\varphi[p] = p$ plays its role.

## Properties

- **In place.** The output array is the only table.
- **Finds the primes.** The values $p$ that pass line L3 are the primes up to $n$, in increasing order.
- **Uses division.** Each update divides by $p$. The [linear sieve](/linear-sieve/) needs only multiplications.
- **Writes each entry once per prime factor.** The entry $m$ changes $\omega(m)$ times, where $\omega(m)$ is the number of distinct prime factors.

## Variants and improvements

- **Linear sieve.** Set each composite once, as $\varphi(p i) = p \varphi(i)$ when $p \mid i$ and $(p - 1) \varphi(i)$ otherwise, with $p$ the least prime factor. This takes $\Theta(n)$ time but needs a list of primes. See the [linear sieve](/linear-sieve/).
- **From a factor table.** With the [smallest prime factor table](/smallest-prime-factor-table/), compute $\varphi(m)$ from $\varphi(m / p)$ in one step, in increasing order of $m$.
- **Segmented.** For $m$ in $[L, R]$, keep two arrays, the value and the unfactored part, and sieve with the primes up to $\sqrt R$; a remaining part larger than 1 is a prime factor. This is the [segmented sieve](/segmented-sieve/) pattern.
- **Other functions.** The same loop with another update rule gives the [Möbius sieve](/mobius-sieve/), and with all $d$ in place of the primes gives the [divisor count sieve](/divisor-count-sieve/).

## When to use it

Use it when you need all totients up to about $10^7$ or $10^8$ and want the simplest code. The [linear sieve](/linear-sieve/) is faster for large $n$ and also gives a factor table, but it needs more memory. For a single $\varphi(m)$, factor $m$ instead. For the sum $\sum_{m \le n} \varphi(m)$ alone, a sublinear method is better; see [totient values up to n](/totient-values-up-to-n/).

## Pitfalls

- **Floating point.** Computing $\varphi[m] \cdot (1 - 1/p)$ in floating point gives rounding errors for large $m$. Use the exact integer form $\varphi[m] - \varphi[m]/p$.
- **Multiplying first.** The form $\varphi[m] \cdot (p - 1) / p$ is exact too, but $\varphi[m] \cdot (p - 1)$ can overflow a fixed-width word. Divide first.
- **Stopping at $\sqrt n$.** The outer loop must reach $n$; with a stop at $\sqrt n$, large prime factors are never applied, so $\varphi[p]$ stays $p$ for primes $p > \sqrt n$.
- **The start of the inner loop.** Start at $m = p$, not at $p^2$ as in the sieve of Eratosthenes; $p$ itself and its small multiples also need the factor.

## Implementations

## History

Euler introduced the totient in 1763, in his proof of the generalization of Fermat's little theorem now called [Euler's theorem](/euler-theorem/). The product formula follows from the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/) and inclusion and exclusion. The sieve itself is folklore: it is the [sieve of Eratosthenes](/sieve-of-eratosthenes/) with a value in place of a flag, and it appears in programming texts and contest references such as cp-algorithms.

## References
