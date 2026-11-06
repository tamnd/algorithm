---
tag: E7NA3A
kind: algorithm
slug: mobius-sieve
name: Möbius sieve
aliases:
- mu sieve
- Mobius sieve
- linear sieve for the Mobius function
area: number-theory/sieves
level: core
summary: Compute the Möbius function mu(m) for all m up to n in Θ(n) time with the linear sieve. Each composite m = p i with p = lp(m) gets mu(m) = 0 if p divides i, and -mu(i) otherwise.
solves: [multiplicative-functions-up-to-n]
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [mobius-function, linear-sieve]
see_also: [mobius-function, linear-sieve, multiplicative-functions-up-to-n, euler-phi-sieve, mobius-inversion-formula, counting-coprime-pairs, divisor-count-sieve, dirichlet-convolution]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 2 (the Möbius function, the sum of mu(d) over the divisors of n, and Möbius inversion)
  - paper: doi:10.1145/359657.359660
    title: David Gries and Jayadev Misra, A linear sieve algorithm for finding prime numbers, Communications of the ACM 21(12), 1978
    locator: pages 999 to 1003 (the linear sieve on which the computation rests)
  - url: https://cp-algorithms.com/algebra/prime-sieve-linear.html
    title: Linear Sieve, cp-algorithms
    locator: Sections Algorithm and Correctness proof (the array lp and the unique form m = lp(m) times i)
---

The Möbius sieve computes the [Möbius function](/mobius-function/) $\mu(m)$ for every $m \le n$ in $\Theta(n)$ word operations. It runs the [linear sieve](/linear-sieve/), which reaches each composite $m$ exactly once as $m = p \cdot i$ with $p$ the least prime factor of $m$, and sets $\mu(m) = 0$ when $p$ also divides $i$ and $\mu(m) = -\mu(i)$ otherwise. It is the standard first step of programs that use [Möbius inversion](/mobius-inversion-formula/), such as counting coprime pairs or squarefree numbers, and it is one case of [multiplicative functions up to n](/multiplicative-functions-up-to-n/).

## In plain words

The Möbius function gives each number one of three values. A number with a repeated prime factor, such as twelve, gets zero. A product of distinct primes gets one if the number of primes is even and minus one if it is odd: six gets one, thirty gets minus one, and one itself gets one.

The sieve works through the numbers in order and builds each one from a smaller number times its smallest prime. If that prime already divides the smaller number, the product has a square factor and gets zero. If not, the product has one more distinct prime than the smaller number, so its value is the smaller number's value with the sign flipped.

## The problem

The input is an integer $n \ge 0$. The output is the array $\mu[1 \ldots n]$ with

$$\mu(m) = \begin{cases} 1 & m = 1, \\ (-1)^r & m = p_1 p_2 \cdots p_r \text{ with distinct primes } p_i, \\ 0 & p^2 \mid m \text{ for some prime } p. \end{cases}$$

This is the [multiplicative function](/multiplicative-function/) case $f = \mu$ of [multiplicative functions up to n](/multiplicative-functions-up-to-n/). The cost model is the [word RAM](/word-ram/): arithmetic, comparisons and array access on numbers up to $n$ cost one step. Memory is counted in words.

## The algorithm

```pseudo id=main
MOBIUS-SIEVE(n)                            ▷ returns μ[0 .. n], with μ[0] = 0
L1  μ[0 .. n] ← 0, lp[0 .. n] ← 0, primes ← empty list, and μ[1] ← 1 if n ≥ 1
L2  for i ← 2 to n do
L3      if lp[i] = 0 then lp[i] ← i, append i to primes, μ[i] ← −1
L4      for each p in primes, in increasing order, do
L5          if p > lp[i] or p · i > n then break
L6          lp[p · i] ← p
L7          if p = lp[i] then μ[p · i] ← 0          ▷ p² divides p · i
L8          else μ[p · i] ← −μ[i]                   ▷ p does not divide i
L9  return μ
```

Lines L1 to L6 are the [linear sieve](/linear-sieve/). In line L7, $p = \mathrm{lp}(i)$ means that $p \mid i$, so $p^2 \mid p i$. In line L8, $p < \mathrm{lp}(i)$, so $p \nmid i$, and $\mu(p i) = \mu(p) \mu(i) = -\mu(i)$ because $\mu$ is multiplicative.

## Example

Take $n = 12$. The column "writes" lists each composite $p \cdot i$ set in the round of $i$, with the value it gets.

| $i$ | $\mu[i]$ | writes |
|---|---|---|
| 2 | $-1$ (prime) | $\mu[4] = 0$ |
| 3 | $-1$ (prime) | $\mu[6] = 1$, $\mu[9] = 0$ |
| 4 | 0 | $\mu[8] = 0$ |
| 5 | $-1$ (prime) | $\mu[10] = 1$ |
| 6 | 1 | $\mu[12] = 0$ |
| 7 to 12 | | none, since $2i > 12$ |

At $i = 3$, the prime $p = 2$ is less than $\mathrm{lp}(3) = 3$, so line L8 gives $\mu[6] = -\mu[3] = 1$; the prime $p = 3 = \mathrm{lp}(3)$ goes to line L7 and gives $\mu[9] = 0$. The result is $\mu[1 \ldots 12] = 1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0$.

## Correctness

The proof of the [linear sieve](/linear-sieve/) shows that each composite $m \le n$ is written exactly once, in the round of $i = m / \mathrm{lp}(m)$ with $p = \mathrm{lp}(m)$, and that $\mathrm{lp}[i]$ is final by then. Since $i < m$, the value $\mu[i]$ is also final by then, by induction on $m$. If $p = \mathrm{lp}(i)$, then $p^2 \mid m$, so $\mu(m) = 0$. If $p < \mathrm{lp}(i)$, then $\gcd(p, i) = 1$ and $\mu(m) = \mu(p) \mu(i) = -\mu(i)$. Primes get $-1$ in line L3, and $\mu(1) = 1$ in line L1. The full proof is below.

## Complexity

Lines L1 to L6 cost $\Theta(n)$, as in the linear sieve: line L6 runs once per composite, and each round of line L4 ends after at most one extra test. Lines L7 and L8 add $O(1)$ to each run of line L6. So the time is $\Theta(n)$ word operations, a proved bound with no conjecture involved. The memory is $n + 1$ words for $\mathrm{lp}$, $n + 1$ small values for $\mu$, and $\pi(n)$ words for the primes.

## Properties

- **Linear time.** Each composite is touched once.
- **Exact integer arithmetic.** The values are $-1$, $0$ and $1$, so one byte per entry is enough.
- **Gives more for free.** The arrays $\mathrm{lp}$ and the prime list are the [smallest prime factor table](/smallest-prime-factor-table/) and the [primes up to n](/primes-up-to-n/).
- **No division.** Line L7 tests $p = \mathrm{lp}[i]$ with a lookup, not with a remainder.

## Variants and improvements

- **Eratosthenes style.** Start with $\mu[m] = 1$. For each prime $p$, multiply $\mu[m]$ by $-1$ at each multiple of $p$, then set $\mu[m] = 0$ at each multiple of $p^2$. This takes $\Theta(n \log \log n)$ time with a table of flags for the primes; it is the same pattern as the [Euler totient sieve](/euler-phi-sieve/).
- **From the divisor sum.** Use $\sum_{d \mid m} \mu(d) = [m = 1]$: set $\mu[1] = 1$, and for $i = 1, 2, \ldots$ subtract $\mu[i]$ from $\mu[j]$ at each multiple $j \ge 2i$. This needs no primes and takes $\Theta(n \log n)$ time, like the [divisor count sieve](/divisor-count-sieve/).
- **Without the table $\mathrm{lp}$.** Keep only a flag per number and test $p \mid i$ by a remainder; break right after the write when $p \mid i$.
- **Mertens function.** Prefix sums of the table give $M(x) = \sum_{m \le x} \mu(m)$ for all $x \le n$. For a single large $x$, methods based on $\sum_{d \le x} M(x/d) = 1$ take about $x^{2/3}$ steps, using the sieve for the small values.

## When to use it

Use it whenever a program needs $\mu$ at all points up to $n$: to apply [Möbius inversion](/mobius-inversion-formula/), to count [coprime pairs](/counting-coprime-pairs/) as $\sum_{d \le n} \mu(d) \lfloor n/d \rfloor^2$, or to count squarefree numbers as $\sum_{d \le \sqrt n} \mu(d) \lfloor n/d^2 \rfloor$. If the program also needs other multiplicative functions, compute them in the same pass.

## Pitfalls

- **$\mu(1) = 1$.** The value at 1 must be set by hand; the sieve never reaches it.
- **The sign for primes.** A prime gets $-1$, not $1$.
- **The test in line L7.** Testing $p \mid i$ is right; testing whether $p^2 \le i$ or any other size condition is wrong.
- **Eratosthenes style with composites.** In the variant above, the round of a composite number must be skipped; otherwise the sign flips too often.

## Implementations

## History

Möbius introduced the function in 1832, together with the inversion formula that bears his name. The linear sieve that computes it is that of Gries and Misra (1978), with the update of line L7 and L8; this use of the linear sieve for multiplicative functions is common in programming contest references.

## References
