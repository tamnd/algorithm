---
tag: XZ33DG
kind: problem
slug: smallest-prime-factor-table
name: Smallest prime factor table
aliases:
- spf table
- factor table
- least prime factor table
area: number-theory/sieves
level: intro
summary: Given n, compute the smallest prime factor of every m from 2 to n. The table takes Θ(n) time to build with the linear sieve, and then factors any m up to n in O(log m) steps.
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
prereqs: [prime-number, fundamental-theorem-of-arithmetic]
see_also: [linear-sieve, sieve-of-eratosthenes, primes-up-to-n, multiplicative-functions-up-to-n, trial-division, integer-factorization, enumerating-divisors]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.2, Sieving (sieving to build a factor table, and to find complete factorizations)
  - paper: doi:10.1145/359657.359660
    title: David Gries and Jayadev Misra, A linear sieve algorithm for finding prime numbers, Communications of the ACM 21(12), 1978
    locator: pages 999 to 1003 (the linear sieve, which also yields the least prime factor of each number)
  - url: https://cp-algorithms.com/algebra/prime-sieve-linear.html
    title: Linear Sieve, cp-algorithms
    locator: Sections Algorithm and Correctness proof (the array lp of least prime factors)
---

The smallest prime factor table up to $n$ is the array $\mathrm{spf}[2 \ldots n]$ in which $\mathrm{spf}[m]$ is the least [prime](/prime-number/) that divides $m$. It is the standard tool for factoring many small numbers: with the table, any $m \le n$ factors in $O(\log m)$ steps, by dividing by $\mathrm{spf}[m]$ until 1 is left. The [linear sieve](/linear-sieve/) builds it in $\Theta(n)$ word operations, which matches the size of the output, and a variant of the [sieve of Eratosthenes](/sieve-of-eratosthenes/) builds it in $O(n \log \log n)$.

## In plain words

For each number from two up to the bound, store the smallest prime that divides it. For a prime, that is the number itself. For an even number, it is two. For fifteen, it is three.

The table pays off when you must break many numbers into primes. To factor a number, look up its smallest prime, divide by it, and look up the smallest prime of what is left. Each step at least halves the number, so it takes only a few steps.

The cost is memory: one stored number for each number up to the bound.

## Definition

**Input.** An integer $n \ge 0$.

**Output.** An array $\mathrm{spf}[0 \ldots n]$ with $\mathrm{spf}[m] = \min\{p \text{ prime} : p \mid m\}$ for $2 \le m \le n$. The entries for $m = 0$ and $m = 1$ hold a fixed marker, often 0, since 1 has no prime factor and every prime divides 0.

**Cost model.** The [word RAM](/word-ram/) with words of $\Theta(\log n)$ binary digits: arithmetic, comparisons and array access on numbers up to $n$ cost one step. The table itself is $n + 1$ words.

**Basic facts.** $\mathrm{spf}[m] = m$ exactly when $m$ is prime. If $m$ is composite, $\mathrm{spf}[m]^2 \le m$. And $\mathrm{spf}[m] \le \mathrm{spf}[m / \mathrm{spf}[m]]$ for composite $m$, since every prime factor of $m / \mathrm{spf}[m]$ divides $m$.

## Variants

- **Largest prime factor.** Store the largest prime factor instead. A sieve that writes $p$ into all multiples of $p$, for $p$ in increasing order, leaves the largest one.
- **Full factorization table.** Store the complete factorization of each $m$. This takes $\Theta(n \log \log n)$ words, the sum of the number of distinct prime factors.
- **Odd numbers only.** Store $\mathrm{spf}$ for odd $m$ only, and handle the factors 2 with a shift. This halves the memory. Wheels with 3 and 5 save more.
- **Factor table of an interval.** Compute the smallest prime factor of each $m$ in $[L, R]$, with the [segmented sieve](/segmented-sieve/) and the primes up to $\sqrt R$.

## Examples

| $m$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\mathrm{spf}[m]$ | 2 | 3 | 2 | 5 | 2 | 7 | 2 | 3 | 2 | 11 | 2 | 13 | 2 | 3 | 2 | 17 | 2 | 19 | 2 |

**Factoring with the table.** Take $m = 360$. The lookups give $\mathrm{spf}[360] = 2$, then $\mathrm{spf}[180] = 2$, $\mathrm{spf}[90] = 2$, $\mathrm{spf}[45] = 3$, $\mathrm{spf}[15] = 3$ and $\mathrm{spf}[5] = 5$, which leaves 1. So $360 = 2^3 \cdot 3^2 \cdot 5$, found with six lookups and six divisions.

**Non-example.** The array of all divisors, with $\mathrm{spf}[15] = 15$, is not the table: 15 is not prime. Neither is the array of the largest prime factors, with 5 at 15.

## Known algorithms

| algorithm | time (word operations) | memory |
|---|---|---|
| [trial division](/trial-division/) of each $m$ up to $\mathrm{spf}(m)$ | $O(n^{3/2} / \log n)$ | $O(1)$ words besides the table |
| [sieve of Eratosthenes](/sieve-of-eratosthenes/), writing $p$ into each unset multiple | $\Theta(n \log \log n)$ | $n + 1$ words |
| [linear sieve](/linear-sieve/) | $\Theta(n)$ | $n + 1$ words, plus the prime list |

In the Eratosthenes version, the round of the prime $p$ writes $p$ into each multiple $m \ge p^2$ whose entry is still empty. The rounds run in increasing $p$, so the first prime to reach $m$ is the smallest. The linear sieve sets each composite once, as $m = p \cdot i$ with $p = \mathrm{spf}[m] \le \mathrm{spf}[i]$. The trial division bound uses that a composite $m$ has $\mathrm{spf}(m) \le \sqrt m$, and that a prime costs $\sqrt m$ divisions; the primes dominate, with $\sum_{p \le n} \sqrt p = O(n^{3/2} / \log n)$.

## Bounds

The output has $n - 1$ entries, so every algorithm takes $\Omega(n)$ steps. The [linear sieve](/linear-sieve/) takes $O(n)$ steps. So the problem takes $\Theta(n)$ time on the word RAM. This bound is proved, and it depends on no conjecture.

## Reductions

- **Factoring.** With the table, $m \le n$ factors into primes in $\Omega(m) + 1 \le \log_2 m + 1$ lookups and divisions, where $\Omega(m)$ is the number of prime factors counted with multiplicity.
- **Primes.** The [primes up to n](/primes-up-to-n/) are the $m$ with $\mathrm{spf}[m] = m$, found in one pass.
- **Multiplicative functions.** From the table, $f(m)$ for a [multiplicative function](/multiplicative-function/) follows from $f$ at the smaller number $m / \mathrm{spf}[m]^e$, where $\mathrm{spf}[m]^e$ is the full power of the smallest prime in $m$. This gives [multiplicative functions up to n](/multiplicative-functions-up-to-n/) in $O(n)$ more steps, once the exponent is stored too.
- **Divisors.** The factorization leads to [enumerating the divisors](/enumerating-divisors/) of $m$.

## Applications

- Factoring many numbers up to $10^7$ or so, for example all values $m \le n$ in a loop, or many queries.
- Computing arithmetic functions such as $\varphi$, $\mu$ and $\sigma$ at all points up to $n$.
- Finding all numbers up to $n$ that are smooth, that is, whose largest prime factor is small.
- Before computers, printed factor tables served the same purpose. D. N. Lehmer published a table of the least factors of the numbers up to ten million in 1909.

## References
