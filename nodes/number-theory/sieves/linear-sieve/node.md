---
tag: 0C3CNA
kind: algorithm
slug: linear-sieve
name: Linear sieve
aliases:
- Euler's sieve
- sieve of Euler
- Gries-Misra sieve
area: number-theory/sieves
level: core
summary: List the primes up to n and the least prime factor lp(m) of every m up to n in Θ(n) time. Each composite m is written once, as p times i with p = lp(m) and p at most lp(i).
solves: [primes-up-to-n, smallest-prime-factor-table]
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [sieve-of-eratosthenes, smallest-prime-factor-table]
see_also: [sieve-of-eratosthenes, smallest-prime-factor-table, primes-up-to-n, multiplicative-functions-up-to-n, mobius-sieve, euler-phi-sieve, segmented-sieve, sieve-of-atkin]
sources:
  - paper: doi:10.1145/359657.359660
    title: David Gries and Jayadev Misra, A linear sieve algorithm for finding prime numbers, Communications of the ACM 21(12), 1978
    locator: pages 999 to 1003 (the algorithm, its invariants, and the proof that each composite is removed once)
  - paper: doi:10.1016/0167-6423(87)90024-4
    title: Paul Pritchard, Linear prime-number sieves, a family tree, Science of Computer Programming 9(1), 1987
    locator: pages 17 to 35 (the linear sieves derived from the sieve of Eratosthenes, and their relations)
  - url: https://cp-algorithms.com/algebra/prime-sieve-linear.html
    title: Linear Sieve, cp-algorithms
    locator: Sections Algorithm, Correctness proof and Runtime and memory
---

The linear sieve computes the list of primes up to $n$ and, for each $m \le n$, its least prime factor $\mathrm{lp}(m)$, with $\Theta(n)$ word operations. It writes each composite $m$ exactly once, as $m = p \cdot i$ where $p = \mathrm{lp}(m)$, while the loop is at $i = m/p$; this unique form is what removes the factor $\log \log n$ of the [sieve of Eratosthenes](/sieve-of-eratosthenes/). It solves both [listing primes up to n](/primes-up-to-n/) and the [smallest prime factor table](/smallest-prime-factor-table/), and with small changes it computes any [multiplicative function](/multiplicative-function/) up to $n$ in linear time.

## In plain words

The sieve of Eratosthenes crosses out some numbers many times: thirty is crossed out by two, by three and by five. The linear sieve crosses out each number only once, by its smallest prime.

It goes through the numbers in order. Each number, prime or not, is used as a multiplier: it is multiplied by the primes found so far, from the smallest up. It stops at the first prime that divides the multiplier. A larger prime would no longer be the smallest prime factor of the product, and that product will be reached later from another multiplier.

Every number then gets its smallest prime factor written exactly once, and a number with nothing written when the loop reaches it is prime.

## The problem

The input is an integer $n \ge 0$. The output is the increasing list of primes $p \le n$ and the array $\mathrm{lp}[0 \ldots n]$ with $\mathrm{lp}[m]$ the least prime factor of $m$ for $2 \le m \le n$, and $\mathrm{lp}[0] = \mathrm{lp}[1] = 0$. The cost model is the [word RAM](/word-ram/): arithmetic, comparisons and array access on numbers up to $n$ cost one step. Memory is counted in words.

## The algorithm

```pseudo id=main
LINEAR-SIEVE(n)                            ▷ returns lp[0 .. n] and the primes up to n
L1  lp[0 .. n] ← 0, primes ← empty list
L2  for i ← 2 to n do
L3      if lp[i] = 0 then                  ▷ nothing wrote i, so i is prime
L4          lp[i] ← i, append i to primes
L5      for each p in primes, in increasing order, do
L6          if p > lp[i] or p · i > n then break
L7          lp[p · i] ← p                  ▷ p is the least prime factor of p · i
L8  return lp, primes
```

The test $p > \mathrm{lp}[i]$ of line L6 is the heart of the method. While $p \le \mathrm{lp}(i)$, the prime $p$ is at most every prime factor of $i$, so $p$ is the least prime factor of $p \cdot i$. Once $p$ passes $\mathrm{lp}(i)$, the product $p \cdot i$ has the smaller factor $\mathrm{lp}(i)$, and it is left for the multiplier $p \cdot i / \mathrm{lp}(i)$.

## Example

Take $n = 20$. The column "writes" lists the products $p \cdot i$ that line L7 sets in the round of $i$.

| $i$ | $\mathrm{lp}[i]$ | prime? | writes |
|---|---|---|---|
| 2 | 2 | yes | 4 |
| 3 | 3 | yes | 6, 9 |
| 4 | 2 | no | 8 |
| 5 | 5 | yes | 10, 15 |
| 6 | 2 | no | 12 |
| 7 | 7 | yes | 14 |
| 8 | 2 | no | 16 |
| 9 | 3 | no | 18 |
| 10 | 2 | no | 20 |
| 11 to 20 | | 11, 13, 17, 19 | none, since $2i > 20$ |

At $i = 9$ the loop writes $2 \cdot 9 = 18$ and $3 \cdot 9 = 27$ would exceed 20; at $i = 4$ it writes 8 and stops at $p = 3 > \mathrm{lp}(4) = 2$, so 12 is not written as $3 \cdot 4$ but later as $2 \cdot 6$. The eleven composites from 4 to 20 are each written once. The result is the primes 2, 3, 5, 7, 11, 13, 17, 19 and $\mathrm{lp}[2 \ldots 20] = 2, 3, 2, 5, 2, 7, 2, 3, 2, 11, 2, 13, 2, 3, 2, 17, 2, 19, 2$.

## Correctness

Every composite $m \le n$ has exactly one representation $m = p \cdot i$ with $p$ prime and $p \le \mathrm{lp}(i)$: the prime must be $p = \mathrm{lp}(m)$, and then $i = m/p$. Line L7 writes exactly the pairs of this form, because in the round of $i$ the loop runs through the primes $p \le \min(\mathrm{lp}(i), n/i)$, and these are all in the list by then. So each composite gets $\mathrm{lp}[m] = \mathrm{lp}(m)$ once, in the round of $i = m / \mathrm{lp}(m) < m$, which comes before the round of $m$. A prime is never written, so line L3 finds $\mathrm{lp}[i] = 0$ exactly for the primes. The full proof is below.

## Complexity

Each run of line L7 writes a different composite, so line L7 runs exactly $n - 1 - \pi(n)$ times in total. Each round of the loop of line L5 ends with at most one test of line L6 that breaks, plus one test for each write. So lines L5 to L7 cost $O(n)$ in total, and lines L2 to L4 cost $O(n)$. The time is $\Theta(n)$ word operations, a proved bound, and it does not depend on the distribution of the primes.

- **Memory.** The array $\mathrm{lp}$ has $n + 1$ words, and the list of primes has $\pi(n) \sim n / \ln n$ words.
- **Counts.** For $n = 10^6$, line L7 runs 921501 times, which is $10^6 - 1 - 78498$. The sieve of Eratosthenes writes 2122048 cells for the same $n$.

The linear bound counts operations, not time on a real machine. The array $\mathrm{lp}$ holds words, not flags, so it uses about 32 times the memory of a packed table, and the writes $p \cdot i$ jump through it. In practice a well-tuned [sieve of Eratosthenes](/sieve-of-eratosthenes/) with packed flags is often faster for listing primes alone.

## Properties

- **Each composite is written once.** This is the defining property, and the source of the bound.
- **Gives a factor table for free.** The array $\mathrm{lp}$ is the [smallest prime factor table](/smallest-prime-factor-table/).
- **Visits each $m$ with its cofactor.** When line L7 writes $m = p \cdot i$, the value at $i$ is already final. This lets the sieve compute $f(m)$ from $f(i)$ for a multiplicative $f$.
- **Uses multiplication.** Line L6 computes $p \cdot i$, unlike the additive sieve of Eratosthenes.

## Variants and improvements

- **Multiplicative functions.** In line L7, set $f(p i)$ from $f(i)$: if $p < \mathrm{lp}(i)$ then $f(p i) = f(p) f(i)$; if $p = \mathrm{lp}(i)$, use the stored power of $p$ in $i$. This gives $\varphi$, $\mu$, $d$ and $\sigma$ up to $n$ in $\Theta(n)$. See [multiplicative functions up to n](/multiplicative-functions-up-to-n/), the [Möbius sieve](/mobius-sieve/) and the [Euler totient sieve](/euler-phi-sieve/).
- **Flags only.** Store a flag per number and test $p \mid i$ instead of $p > \mathrm{lp}(i)$: break right after writing $p \cdot i$ with $p \mid i$. This is the common contest form; it needs a division or remainder per step.
- **Gries and Misra's form.** The original paper keeps the numbers that are not yet crossed out in a doubly linked list and removes $p^k q$ for each prime $p$ and each remaining $q$; it also takes $O(n)$ operations. Pritchard's survey derives the linear sieves, this one included, from the sieve of Eratosthenes.
- **Sublinear sieves.** With a wheel that grows with $n$, Pritchard's sieve and the sieve of Atkin and Bernstein take $O(n / \log \log n)$ operations; see the [sieve of Atkin](/sieve-of-atkin/).

## When to use it

Use it when you need the primes and a factor table, or the values of a multiplicative function, for all numbers up to about $10^7$ or $10^8$. If you need only the primes, a packed [sieve of Eratosthenes](/sieve-of-eratosthenes/) uses much less memory and is usually as fast. For an interval far from 0, use the [segmented sieve](/segmented-sieve/).

## Pitfalls

- **The order of the tests.** Line L6 must test $p > \mathrm{lp}[i]$ before writing. Writing first and testing $p = \mathrm{lp}[i]$ afterwards also works, but testing $p \ge \mathrm{lp}[i]$ before the write loses the products $\mathrm{lp}(i) \cdot i$, such as 4 and 9.
- **Overflow of $p \cdot i$.** In fixed-width arithmetic, $p \cdot i$ can overflow when $n$ is near the largest integer; test $p \le n / i$ instead.
- **Memory.** For $n = 10^8$, the array $\mathrm{lp}$ takes 400 MB with 32-bit words. Store $\mathrm{lp}$ only for odd numbers, or use a smaller type, when memory is tight.

## Implementations

## History

David Gries and Jayadev Misra published a linear sieve in 1978, with a proof from invariants. Paul Pritchard's survey of 1987 gives a family tree of the linear sieves and their relation to the sieve of Eratosthenes. The name "Euler's sieve" refers to Euler's proof of the product formula for the zeta function, in which each integer is removed exactly once, by its least prime factor. The array form with the test $p \le \mathrm{lp}(i)$ shown here is the one popular in programming contests.

## References
