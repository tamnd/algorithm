---
tag: ZW0DHJ
kind: algorithm
slug: segmented-sieve
name: Segmented sieve
aliases:
- segmented sieve of Eratosthenes
- windowed sieve
area: number-theory/sieves
level: core
summary: List the primes in [L, R] by sieving one block at a time with the primes up to R^(1/2). It takes O((R - L + 1) log log R + R^(1/2)) word operations and O(R^(1/2) + B) memory for blocks of length B.
solves: [primes-in-range, primes-up-to-n]
model: word-ram
complexity:
  vars: {L: the lower end, R: the upper end, Δ: the length R - L + 1, B: the block length}
  time: {worst: "O(Δ log log R + (Δ / B + 1) R^(1/2) / log R + R^(1/2) log log R)"}
  space: {extra: "O(R^(1/2) / log R + B)"}
properties: {deterministic: true, recursive: false}
prereqs: [sieve-of-eratosthenes]
see_also: [sieve-of-eratosthenes, primes-in-range, primes-up-to-n, linear-sieve, prime-gaps, external-memory-model, wheel-factorization, sieve-of-atkin]
sources:
  - paper: doi:10.1007/BF01932283
    title: Carter Bays and Richard H. Hudson, The segmented sieve of Eratosthenes and primes in arithmetic progressions to 10^12, BIT 17(2), 1977
    locator: pages 121 to 127 (the segmented sieve, its blocks, and the computation of the primes up to 10^12)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.2, Sieving (the segmented form of the sieve of Eratosthenes)
  - url: https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html
    title: Sieve of Eratosthenes, cp-algorithms
    locator: Sections Segmented Sieve and Find primes in range
  - paper: doi:10.1090/S0025-5718-2013-02787-1
    title: Tomás Oliveira e Silva, Siegfried Herzog and Silvio Pardi, Empirical verification of the even Goldbach conjecture and computation of prime gaps up to 4 x 10^18, Mathematics of Computation 83(288), 2014
    locator: pages 2033 to 2060 (the segmented sieve with buckets for the large base primes)
---

The segmented sieve lists the primes in an interval $[L, R]$ by first finding the base primes up to $\sqrt R$ with the [sieve of Eratosthenes](/sieve-of-eratosthenes/), and then sieving the interval one block of length $B$ at a time: in each block it clears the multiples of each base prime $p$, starting at the first one that is at least $\max(p^2, \text{block start})$. It solves [listing primes in an interval](/primes-in-range/) with $O(\Delta \log \log R + \sqrt R)$ word operations for $\Delta = R - L + 1$, and with $B \approx \sqrt R$ it needs only $O(\sqrt R)$ memory. With $L = 2$ it is the standard way to list the [primes up to n](/primes-up-to-n/) when a full table does not fit in the cache or in memory.

## In plain words

The plain sieve needs a cell for every number up to the bound. For a big bound that is too much memory, and jumping around a huge table is slow.

The segmented sieve cuts the range into windows that fit in fast memory. It first finds the small primes, those up to the square root of the end of the range, with a plain sieve. Then, for one window at a time, it crosses out the multiples of the small primes that fall inside the window. Whatever is left in a window is prime. Then it reuses the same memory for the next window.

## The problem

The input is a pair of integers $L \le R$, and a block length $B \ge 1$ that affects only the speed. The output is the increasing list of primes $p$ with $L \le p \le R$: the problem of [listing primes in an interval](/primes-in-range/). The cost model is the [word RAM](/word-ram/) with words of $\Theta(\log R)$ binary digits: arithmetic, comparisons and array access on numbers up to $R$ cost one step. Memory is counted in words and flags; the output is not counted.

## The algorithm

The block $[lo, hi]$ is held in a table $S[0 \ldots hi - lo]$, where $S[j]$ stands for $lo + j$.

```pseudo id=main
SEGMENTED-SIEVE(L, R, B)                   ▷ returns the primes p with L ≤ p ≤ R
L1  L ← max(L, 2); if L > R then return the empty list
L2  base ← SIEVE(⌊√R⌋)                     ▷ the primes up to √R, by the sieve of Eratosthenes
L3  out ← empty list, lo ← L
L4  while lo ≤ R do
L5      hi ← min(lo + B − 1, R)
L6      S[0 .. hi − lo] ← true
L7      for each p in base with p · p ≤ hi do
L8          s ← max(p · p, ⌈lo / p⌉ · p)   ▷ the first multiple of p in the block that is at least p²
L9          for m ← s, s + p, s + 2p, … while m ≤ hi do S[m − lo] ← false
L10     append lo + j to out for each j with S[j] = true
L11     lo ← hi + 1
L12 return out
```

Line L8 starts at $p^2$ for the same reason as the plain sieve: a smaller multiple $kp$ with $k < p$ has a smaller prime factor. Starting at $p^2$ also keeps the base prime $p$ itself from being cleared when it lies in the block. In the usual implementation, line L8 is replaced by keeping, for each base prime, the next multiple left over from the previous block, which saves the division.

## Example

Take $L = 100$, $R = 130$ and $B = 16$. The base primes are those up to $\lfloor \sqrt{130} \rfloor = 11$: 2, 3, 5, 7, 11.

| block | $p$ | start $s$ | cleared |
|---|---|---|---|
| $[100, 115]$ | 2 | 100 | 100, 102, ..., 114 |
| | 3 | 102 | 102, 105, 108, 111, 114 |
| | 5 | 100 | 100, 105, 110, 115 |
| | 7 | 105 | 105, 112 |
| | 11 | | skipped, since $121 > 115$ |
| $[116, 130]$ | 2 | 116 | 116, 118, ..., 130 |
| | 3 | 117 | 117, 120, 123, 126, 129 |
| | 5 | 120 | 120, 125, 130 |
| | 7 | 119 | 119, 126 |
| | 11 | 121 | 121 |

The first block keeps 101, 103, 107, 109 and 113, and the second keeps 127. The prime 11 is needed only in the second block, to clear $121 = 11^2$, which no smaller prime divides.

## Correctness

A number $m \ge 2$ in a block is cleared only by line L9, as a multiple $m \ge p^2$ of a prime $p$, so $m$ is composite. Conversely, a composite $m \le R$ has a least prime factor $q \le \sqrt m \le \sqrt R$, so $q$ is a base prime, and $m \ge q^2$. In the block that holds $m$, the test $q^2 \le hi$ passes since $q^2 \le m \le hi$, the start $s$ of line L8 is at most $m$, because $m$ is a multiple of $q$ that is at least both $q^2$ and $lo$, and $m - s$ is a multiple of $q$. So line L9 clears $m$. The blocks cover $[L, R]$ without overlap, in increasing order. The full proof is below.

## Complexity

**Base sieve.** Line L2 takes $O(\sqrt R \log \log R)$ steps and keeps $\pi(\sqrt R) = O(\sqrt R / \log R)$ words.

**Marking.** In a block of length $\ell \le B$, the base prime $p$ costs at most $\ell / p + 1$ steps in lines L8 and L9. Over all blocks the terms $\ell / p$ sum to $\Delta / p$, and by Mertens' theorem $\sum_{p \le \sqrt R} 1/p = \ln \ln R + O(1)$. The terms $+1$ sum to at most $\pi(\sqrt R)$ per block, and there are $\lceil \Delta / B \rceil$ blocks.

**Total.** $O(\Delta \log \log R + (\Delta / B + 1) \sqrt R / \log R + \sqrt R \log \log R)$ word operations, and $O(\sqrt R / \log R + B)$ words and flags of memory. With $B \ge \sqrt R / \log R$ the middle term is absorbed, and the time is $O(\Delta \log \log R + \sqrt R \log \log R)$. All of these bounds are proved and use no conjecture.

For listing the primes up to $n$ ($L = 2$, $R = n$) with $B = \Theta(\sqrt n)$, this is $O(n \log \log n)$ time, the same as the plain sieve, with $O(\sqrt n)$ memory in place of $\Theta(n)$.

## Properties

- **Small memory.** Only the base primes and one block are kept.
- **Cache friendly.** With the block in the cache, the scattered writes of each round stay fast. This, not the operation count, is why the segmented sieve is faster in practice for large $n$.
- **Parallel.** The blocks are independent once the base primes are known, so they can be sieved on different processors.
- **Works far from 0.** The cost depends on $\Delta$ and $\sqrt R$, not on $R$ itself.

## Variants and improvements

- **Carry the next multiple.** Store for each base prime the first multiple beyond the current block, and continue from there. This removes the division of line L8.
- **Odd numbers or a wheel.** Keep flags only for odd numbers, or for numbers coprime to $2 \cdot 3 \cdot 5 \cdot 7$, as in [wheel factorization](/wheel-factorization/). This saves a constant factor in time and memory.
- **Bucket sieve for large primes.** When $\sqrt R$ is much larger than $B$, most base primes hit a block at most once. Keeping them in buckets by the block of their next multiple avoids the $+1$ cost per prime and block; Oliveira e Silva, Herzog and Pardi used this bucket method in their check of the Goldbach conjecture and their computation of prime gaps up to $4 \cdot 10^{18}$.
- **Other outputs.** Divide out the base primes from the numbers of the block to get the smallest prime factors, or the values of a [multiplicative function](/multiplicative-functions-up-to-n/), for each number in $[L, R]$.
- **Other sieves.** The [sieve of Atkin](/sieve-of-atkin/) and the [linear sieve](/linear-sieve/) have segmented forms too.

## When to use it

Use it to list the primes in an interval $[L, R]$ with $R$ up to about $10^{18}$ and a length $\Delta$ of at least $\sqrt R$ or so; for a very short interval near a huge number, test each candidate with [Miller-Rabin](/miller-rabin/). Use it with $L = 2$ instead of the plain sieve whenever $n$ is beyond a few million and speed matters, or when $n$ is so large that a table up to $n$ does not fit in memory.

## Pitfalls

- **Clearing a base prime.** Starting at $\lceil lo / p \rceil \cdot p$ without the $\max$ with $p^2$ clears $p$ itself when $p$ lies in the block, which happens for small $L$.
- **0 and 1.** If $L \le 1$, the cells for 0 and 1 are never cleared by the sieve. Raise $L$ to 2, as line L1 does.
- **The integer square root.** Compute $\lfloor \sqrt R \rfloor$ exactly in integers; a floating point square root can be off by one for large $R$, which can drop a base prime $p$ with $p^2 = R$, such as $R = 49$ with $p = 7$.
- **Overflow.** Near the top of the word range, $p \cdot p$, $lo + B - 1$ and $m + p$ can overflow. Use wider types or compare by subtraction.
- **Block length.** A block much larger than the cache loses the main advantage; a block much shorter than $\sqrt R / \log R$ makes the per-prime cost dominate.

## Implementations

## History

Segmented sieving was in use on computers by the 1970s. Carter Bays and Richard Hudson described the segmented sieve of Eratosthenes in 1977 and used it to tabulate primes in arithmetic progressions up to $10^{12}$. Later computations of prime gaps and of the Goldbach conjecture, up to $4 \cdot 10^{18}$, used refined segmented sieves.

## References
