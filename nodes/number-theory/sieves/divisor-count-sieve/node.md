---
tag: VFD6YZ
kind: algorithm
slug: divisor-count-sieve
name: Divisor-count sieve
aliases:
- harmonic sieve
- divisor sieve
- divisor count sieve
area: number-theory/sieves
level: intro
summary: Compute the number of divisors d(m) for all m up to n by adding 1 at every multiple of each e from 1 to n. It takes Θ(n log n) word operations, and adding e instead of 1 gives sigma(m).
solves: [divisor-function-up-to-n]
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Θ(n log n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [divisor-function, harmonic-series]
see_also: [divisor-function-up-to-n, euler-phi-sieve, linear-sieve, sieve-of-eratosthenes, divisor-summatory-function, dirichlet-convolution, multiplicative-functions-up-to-n, enumerating-divisors]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 3 (the average order of d(n), with the sum of floor(x/n) and Dirichlet's divisor theorem)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition, Oxford University Press, 2008
    locator: Section 18.2 (the average order of d(n))
  - url: https://cp-algorithms.com/algebra/divisors.html
    title: Number of divisors / sum of divisors, cp-algorithms
    locator: Sections Number of divisors and Sum of divisors
---

The divisor-count sieve computes the number of divisors $d(m)$ of every $m \le n$ by visiting, for each $e$ from 1 to $n$, all multiples $e, 2e, 3e, \ldots$ up to $n$ and adding 1 to each. Every divisor $e$ of $m$ is then counted exactly once at $m$. The total work is $\sum_{e \le n} \lfloor n/e \rfloor \approx n \ln n$, a [harmonic series](/harmonic-series/) sum, which gives the name harmonic sieve. Adding $e$ or $e^k$ in place of 1 gives the [divisor function](/divisor-function/) $\sigma$ or $\sigma_k$, so it solves [divisor function values up to n](/divisor-function-up-to-n/).

## In plain words

Instead of asking each number for its divisors, let each possible divisor visit the numbers it divides. One visits every number. Two visits every even number. Three visits every third number, and so on. Each visit adds one to a tally.

When all visitors are done, each tally shows how many numbers visited it, which is how many divisors it has. If a visitor adds its own value instead of one, the tallies become the sums of the divisors.

The work is small: the visitor with a big value makes few stops.

## The problem

The input is an integer $n \ge 0$. The output is the array $d[1 \ldots n]$ with $d(m)$ the number of positive divisors of $m$; this is [divisor function values up to n](/divisor-function-up-to-n/) with order $k = 0$. The cost model is the [word RAM](/word-ram/): arithmetic, comparisons and array access on numbers up to $n$ cost one step. The array is the output; the extra memory is $O(1)$ words.

## The algorithm

```pseudo id=main
DIVISOR-COUNT-SIEVE(n)                     ▷ returns d[0 .. n], with d[0] = 0
L1  d[0 .. n] ← 0
L2  for e ← 1 to n do
L3      for m ← e, 2e, 3e, … while m ≤ n do
L4          d[m] ← d[m] + 1                ▷ e divides m
L5  return d
```

For the sum of divisors, line L4 adds $e$ instead of 1; for $\sigma_k$ it adds $e^k$. Index 0 is never written, since $m \ge e \ge 1$.

## Example

Take $n = 12$. The rows list the multiples that each $e$ visits.

| $e$ | multiples visited |
|---|---|
| 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 |
| 2 | 2, 4, 6, 8, 10, 12 |
| 3 | 3, 6, 9, 12 |
| 4 | 4, 8, 12 |
| 5 | 5, 10 |
| 6 | 6, 12 |
| 7 to 12 | the number itself |

The result is $d[1 \ldots 12] = 1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6$. The entry 12 is visited by 1, 2, 3, 4, 6 and 12, so $d(12) = 6$. Line L4 runs $12 + 6 + 4 + 3 + 2 + 2 + 6 = 35$ times, which equals $d(1) + \cdots + d(12)$.

## Correctness

For $1 \le m \le n$, line L4 adds 1 to $d[m]$ once for each $e \le n$ such that $m$ is a multiple of $e$, that is, once for each divisor $e$ of $m$ with $e \le n$. Every divisor of $m$ is at most $m \le n$, so all divisors are counted, and none twice, since the loop of line L3 visits each multiple of $e$ once. The full proof is below.

## Complexity

The number of runs of line L4 is

$$D(n) = \sum_{e=1}^{n} \left\lfloor \frac{n}{e} \right\rfloor = \sum_{m=1}^{n} d(m).$$

Since $n/e - 1 < \lfloor n/e \rfloor \le n/e$, this gives $n H_n - n < D(n) \le n H_n$, where $H_n = \sum_{e \le n} 1/e$ satisfies $\ln n < H_n \le \ln n + 1$. So $D(n) = n \ln n + O(n)$, and the time is $\Theta(n \log n)$ word operations. Both bounds are proved; Dirichlet's sharper form is $D(n) = n \ln n + (2\gamma - 1) n + O(\sqrt n)$.

| $n$ | runs of line L4 | $n \ln n$ |
|---|---|---|
| 12 | 35 | 30 |
| $10^4$ | 93668 | 92103 |
| $10^6$ | 13970034 | 13815511 |

The memory is the output array of $n + 1$ words. For $\sigma$, each entry needs up to two words, since $\sigma(m) \le m^2$.

## Properties

- **No division and no multiplication.** The inner loop only adds. The variant for $\sigma$ adds $e$.
- **Works for any Dirichlet convolution.** Line L4 with $d[e \cdot f] \mathrel{+}= g(e) h(f)$ computes the [Dirichlet convolution](/dirichlet-convolution/) $g * h$ up to $n$ in the same $\Theta(n \log n)$ time; $d = 1 * 1$ and $\sigma = \mathrm{id} * 1$.
- **Needs no primes.** Unlike the [Euler totient sieve](/euler-phi-sieve/), it does not find or use the primes.
- **Sequential writes for small $e$.** The rounds with small $e$ sweep the array almost in order, and they do most of the work.

## Variants and improvements

- **Pairs of divisors.** For $e \le \sqrt n$, visit only the multiples $m = e f$ with $f \ge e$, and add 2 (or 1 when $f = e$). Each divisor pair $\{e, m/e\}$ is then counted in one visit. This halves the work to about $\frac12 n \ln n$.
- **Divisor lists.** Append $e$ to a list at $m$ instead of adding 1. The lists come out sorted, and they hold all $D(n)$ divisors, which is optimal for this output.
- **Linear time.** The [linear sieve](/linear-sieve/), which also records the exponent of the least prime factor, computes $d$ and $\sigma$ in $\Theta(n)$. See [multiplicative functions up to n](/multiplicative-functions-up-to-n/).
- **Prime rounds only.** Using the formula $d(m) = \prod (a_i + 1)$, a sieve over the prime powers $p^a$ alone takes $O(n \log \log n)$ steps.

## When to use it

Use it for $n$ up to about $10^7$ when you want the shortest correct code, or when you need the full lists of divisors. For larger $n$ or in a hot loop, the linear sieve saves the factor $\ln n$. For the sum $\sum_{m \le n} d(m)$ alone, use the [divisor summatory function](/divisor-summatory-function/) method, which takes $O(\sqrt n)$ time.

## Pitfalls

- **Overflow of $\sigma$.** The values of $\sigma(m)$ reach about $m \ln \ln m$ times a constant, and $\sigma_k$ grows like $m^k$. Use a type wide enough for the largest value.
- **Lists of divisors and memory.** The lists hold about $n \ln n$ numbers in total, which is 14 times $n$ at $n = 10^6$. Store counts unless the lists are needed.
- **Starting at $2e$.** Starting the inner loop at $2e$ leaves out the divisor $m$ itself, which gives $d(m) - 1$.

## Implementations

## History

The cost of this sieve is Dirichlet's divisor sum: Dirichlet showed in 1849 that $\sum_{m \le n} d(m) = n \ln n + (2\gamma - 1) n + O(\sqrt n)$, by the method now called the [Dirichlet hyperbola method](/dirichlet-hyperbola-method/). The sieve itself, adding at the multiples of each number, is folklore, and it is a common first exercise in loops over multiples.

## References
