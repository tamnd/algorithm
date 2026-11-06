---
tag: F0W4PP
kind: algorithm
slug: sieve-of-eratosthenes
name: Sieve of Eratosthenes
aliases:
- Eratosthenes sieve
- Eratosthenes' sieve
area: number-theory/sieves
level: intro
summary: List all primes up to n. Keep a table of flags, and for each prime p with p^2 at most n clear the flags of p^2, p^2 + p, p^2 + 2p, and so on. It takes Θ(n log log n) word operations and n + 1 flags.
solves: [primes-up-to-n]
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Θ(n log log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [prime-number, harmonic-series, loop-invariant]
see_also: [primes-up-to-n, linear-sieve, segmented-sieve, sieve-of-sundaram, sieve-of-atkin, smallest-prime-factor-table, wheel-factorization, trial-division]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.2, Sieving (the sieve of Eratosthenes in pseudocode and its running time)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition, Oxford University Press, 2008
    locator: Chapter 1 (the sequence of primes and the sieve of Eratosthenes) and Theorem 427 (Mertens, the sum of 1/p over primes p up to x is log log x + B + o(1))
  - paper: doi:10.1017/S0956796808007004
    title: Melissa E. O'Neill, The Genuine Sieve of Eratosthenes, Journal of Functional Programming 19(1), 2009
    locator: Sections 1 to 3 (the faithful sieve, the unfaithful sieve that is trial division, and their costs)
  - paper: doi:10.1016/0167-6423(87)90024-4
    title: Paul Pritchard, Linear prime-number sieves, a family tree, Science of Computer Programming 9(1), 1987
    locator: pages 17 to 35 (the sieve of Eratosthenes as the root of the family, and its refinements)
---

The sieve of Eratosthenes lists all primes up to $n$ by crossing out multiples: for each [prime](/prime-number/) $p$ with $p^2 \le n$, it clears the flags of $p^2, p^2 + p, p^2 + 2p, \ldots$ in a table of $n + 1$ flags, and the numbers whose flags stay set are the primes. It solves [listing primes up to n](/primes-up-to-n/) with $\Theta(n \log \log n)$ word operations. It is the oldest known algorithm of number theory and still a fast way to make a table of small primes.

## In plain words

Write down the numbers from two up to the bound. The first number, two, is prime. Cross out every larger multiple of two. The next number that is not crossed out is three, and it is prime, so cross out its multiples. Go on like this: each time, the next number that is still standing is a prime, and you cross out its multiples.

You can stop early. Once the square of the next prime is past the bound, every number still standing is prime. You can also start each round at the square of the prime, since the smaller multiples were crossed out in earlier rounds.

## The problem

The input is an integer $n \ge 0$. The output is the increasing list of all primes $p \le n$. This is [listing primes up to n](/primes-up-to-n/). The cost model is the [word RAM](/word-ram/): an addition, a comparison, a multiplication or an array access on numbers up to $n$ costs one step. Memory is counted in flags of one binary digit each, or in words.

## The algorithm

The table $P[0 \ldots n]$ holds one flag per number. At the end, $P[m]$ is true exactly when $m$ is prime.

```pseudo id=main
SIEVE(n)                                   ▷ returns the primes p ≤ n
L1  if n < 2 then return the empty list
L2  P[0 .. n] ← true, then P[0] ← false and P[1] ← false
L3  p ← 2
L4  while p · p ≤ n do
L5      if P[p] then                       ▷ p is prime
L6          for m ← p · p, p · p + p, p · p + 2p, … while m ≤ n do
L7              P[m] ← false               ▷ m is a multiple of p
L8      p ← p + 1
L9  return the list of all m with 2 ≤ m ≤ n and P[m] = true
```

The loop of line L6 starts at $p^2$. A smaller multiple $kp$ with $2 \le k < p$ has a prime factor $q \le k < p$, so an earlier round already cleared it. The loop of line L4 stops at $\sqrt n$, because a composite $m \le n$ has a prime factor $q \le \sqrt m \le \sqrt n$.

## Example

Take $n = 30$. The primes $p$ with $p^2 \le 30$ are 2, 3 and 5.

| $p$ | the loop of line L6 writes | cells that were still true |
|---|---|---|
| 2 | 4, 6, 8, ..., 30 (14 cells) | 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30 |
| 3 | 9, 12, 15, ..., 30 (8 cells) | 9, 15, 21, 27 |
| 5 | 25, 30 (2 cells) | 25 |

At $p = 4$, line L5 finds $P[4]$ false and skips. At $p = 6$, the test $36 \le 30$ of line L4 fails. The loop wrote 24 cells and cleared the 19 composites from 4 to 30. Line L9 returns 2, 3, 5, 7, 11, 13, 17, 19, 23, 29.

## Correctness

The proof is a [loop invariant](/loop-invariant/) of line L4: when line L4 tests $p$, a number $m$ with $2 \le m \le n$ has $P[m]$ false exactly when $m$ is composite and its smallest prime factor is less than $p$. A prime is never cleared, because each cleared $m$ is $p \cdot k$ with $k \ge p \ge 2$. A composite $m$ with smallest prime factor $q$ is $q \cdot k$ with $k \ge q$, so the round of $q$ clears it. When the loop stops, $p^2 > n$, and each composite $m \le n$ has its smallest prime factor at most $\sqrt n < p$. So the flags that stay true are exactly the primes. The full proof is below.

## Complexity

The work is the number of writes of line L7. The round of the prime $p$ writes $\lfloor n/p \rfloor - p + 1$ cells, so the total is

$$W(n) = \sum_{p \le \sqrt n} \left( \left\lfloor \frac{n}{p} \right\rfloor - p + 1 \right).$$

Mertens' theorem gives $\sum_{p \le x} 1/p = \ln \ln x + B + o(1)$ with $B \approx 0.2615$, and it is proved without any conjecture (Hardy and Wright, Theorem 427). Since $\sum_{p \le \sqrt n} p \le n$, this gives

$$W(n) = n \ln \ln \sqrt n + O(n) = n \ln \ln n + O(n).$$

So the sieve takes $\Theta(n \log \log n)$ steps: the upper and the lower bound are both proved. Lines L4, L5 and L8 run about $\sqrt n$ times, and line L9 scans $n$ cells.

- **Time.** $\Theta(n \log \log n)$ word operations, in every case, since the work depends only on $n$.
- **Memory.** $n + 1$ flags, which is $\Theta(n)$. With one binary digit per flag this is about $n/8$ bytes, and storing only the odd numbers halves it. The output list has $\pi(n) \sim n / \ln n$ numbers.

| $n$ | writes of line L7 | $n \ln \ln n$ | $\pi(n)$ |
|---|---|---|---|
| $10^4$ | 16981 | 22203 | 1229 |
| $10^6$ | 2122048 | 2625792 | 78498 |
| $10^7$ | 22850051 | 27799426 | 664579 |

The factor $\ln \ln n$ grows very slowly: it is below 3 for all $n < 5 \cdot 10^8$, so in practice the sieve runs in about linear time.

## Properties

- **Additive.** The marking loop needs only additions and comparisons: $m$ grows by $p$, and $p^2$ can be kept up to date by adding $2p + 1$.
- **No division.** The sieve never divides, which is what makes it faster than [trial division](/trial-division/) on each number.
- **Scattered writes.** The round of $p$ jumps through the table in steps of $p$. When the table is larger than the cache, these jumps are slow, which the [segmented sieve](/segmented-sieve/) fixes.
- **Writes some cells many times.** A composite $m$ is written once for each prime $p$ with $p^2 \le m$ and $p \mid m$. The [linear sieve](/linear-sieve/) writes each composite once.

## Variants and improvements

- **Odd numbers only.** Keep flags for odd $m$ only and sieve with odd $p$, stepping by $2p$. This halves the time and the memory.
- **Wheel.** Keep flags only for $m$ coprime to $2 \cdot 3 \cdot 5$ or a larger primorial. This is the sieve form of [wheel factorization](/wheel-factorization/), and with a wheel that grows with $n$ it reaches $O(n / \log \log n)$ operations (Pritchard).
- **Packed flags.** Store the table as a [bit vector](/bit-vector/), eight flags per byte.
- **Segmented sieve.** Sieve $[2, n]$ in blocks that fit in the cache, with the primes up to $\sqrt n$. This is the [segmented sieve](/segmented-sieve/), with $O(\sqrt n)$ memory.
- **Factor tables.** Store a prime factor instead of a flag to get the [smallest prime factor table](/smallest-prime-factor-table/).
- **Linear sieve.** Clear each composite exactly once, for $\Theta(n)$ time. This is the [linear sieve](/linear-sieve/).
- **Incremental sieve.** Produce the primes without a bound by keeping, for each prime found so far, its next multiple in a priority queue. O'Neill describes this form.

## When to use it

Use it when you need all primes up to a bound of up to about $10^8$ to $10^9$ and the table fits in memory. For larger bounds, or when the table does not fit in the cache, use the [segmented sieve](/segmented-sieve/). When you also need the smallest prime factor of each number, use the [linear sieve](/linear-sieve/) or a factor table. To test one large number, use a [primality test](/primality-testing/).

## Pitfalls

- **Off by one.** The table needs $n + 1$ cells, so that $P[n]$ exists. Clear $P[0]$ and $P[1]$ by hand.
- **Overflow of $p \cdot p$.** In fixed-width arithmetic the test $p \cdot p \le n$ can overflow when $n$ is near the largest integer. Test $p \le n / p$ instead.
- **The unfaithful sieve.** A program that keeps a list and removes from it every number divisible by $p$, by testing each number with a division, is trial division in disguise. O'Neill shows that this common functional program is much slower than the true sieve, which steps from one multiple to the next.
- **Flags as words.** A table of full integers uses eight times the memory of a byte table and up to 64 times that of a packed table, and the extra memory traffic slows the sieve.

## Implementations

## History

Eratosthenes of Cyrene, who lived in the third century BC, is credited with the method. His own writing on it is lost; the oldest surviving description is in the *Introduction to Arithmetic* of Nicomachus of Gerasa, from about 100 AD. Pritchard's survey of 1987 traces the later sieves, including the linear ones, back to this method.

## References
