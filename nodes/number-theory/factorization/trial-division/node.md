---
tag: 1TKFVE
kind: algorithm
slug: trial-division
name: Trial division
aliases:
- trial division factorization
- trial division primality test
area: number-theory/factorization
level: intro
summary: Divide N by 2, 3, 5, 7, 9, ... while the square of the divisor is at most the unfactored part. It finds the full factorization with O(N^(1/2)) divisions in the worst case.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, P: the second largest prime factor of N with multiplicity, Q: the largest prime factor of N}
  time: {worst: O(N^(1/2)), best: Θ(log N)}
  space: {extra: O(1)}
  divisions: {worst: "O(max(P, Q^(1/2)) + log N)"}
  bit_operations: {worst: O(N^(1/2) n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [divisibility, prime-number, fundamental-theorem-of-arithmetic]
see_also: [wheel-factorization, sieve-of-eratosthenes, smallest-prime-factor-table, pollard-rho, smooth-number, integer-factorization, primality-testing, enumerating-divisors]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.1, Trial division, pages 117 to 121 (Algorithm 3.1.1; Section 3.1.4, Theoretical considerations, with the average costs)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.5.4, Factoring into primes (Algorithm A, factoring by division, and the analysis of its running time)
  - paper: "Donald E. Knuth and Luis Trabb Pardo, Analysis of a simple factorization algorithm, Theoretical Computer Science 3(3), 1976"
    locator: pages 321 to 348 (the distribution of the largest and second largest prime factors, and the running time of trial division)
---

Trial division factors a positive integer $N$ by dividing it by $2, 3, 5, 7, 9, \dots$ in turn, and it stops when the square of the divisor is larger than the part of $N$ that is not yet factored. It solves [integer factorization](/integer-factorization/) exactly and needs no theory beyond [divisibility](/divisibility/). Its cost is $O(N^{1/2})$ divisions in the worst case, which is exponential in the number of digits of $N$. So it is the method of choice only for small numbers, and the first step of every other factoring program, which removes the small [prime](/prime-number/) factors before a faster method starts.

## In plain words

Try to divide the number by two. As long as it divides, write down a two and replace the number by the quotient. Then do the same with three, then five, then seven, and so on through the odd numbers.

When a divisor works, it is always a prime. All smaller primes are already removed from the number, so a composite divisor such as nine cannot divide what is left.

You can stop early. If the next divisor, multiplied by itself, is larger than what is left, then what is left has no smaller factor, so it is one or a prime. Write it down, and you are done.

## The problem

**Input.** An integer $N \ge 1$.

**Output.** The list of primes $p_1 \le \cdots \le p_k$ with $p_1 \cdots p_k = N$ (the empty list for $N = 1$). This is [integer factorization](/integer-factorization/).

**Cost model.** On the [word RAM](/word-ram/), with $N$ less than $2^w$ for the word size $w$ (for example $N < 2^{64}$), one division costs $O(1)$, and the time is the number of divisions. For an arbitrary-precision $N$ with $n$ binary digits, a division of a number of at most $n$ digits by a divisor $d \le N^{1/2}$ costs $O(n \log d) = O(n^2)$ bit operations with schoolbook division.

## The algorithm

$F$ is the output list. $m$ is the part of $N$ that is not yet factored, and $d$ is the current trial divisor.

```pseudo id=main
TRIAL-DIVISION(N)                          ▷ N ≥ 1; returns the prime factors of N in order
L1  F ← empty list, m ← N, d ← 2
L2  while d · d ≤ m do
L3      while m mod d = 0 do
L4          append d to F, m ← m / d
L5      if d = 2 then d ← 3 else d ← d + 2
L6  if m > 1 then append m to F
L7  return F
```

The trial divisors are $2$ and then the odd numbers. Line L3 removes each power of $d$, so the same prime is appended as many times as it divides $N$. The test of line L2 uses the current $m$, not $N$: each found factor makes $m$ smaller and so ends the loop sooner. After the loop, $m$ is $1$ or a prime, and line L6 appends it.

## Example

Factor $N = 9100$.

| $d$ | $m$ before | $d^2 \le m$? | divisions that go | $m$ after | $F$ |
|---|---|---|---|---|---|
| 2 | 9100 | yes | 2, 2 | 2275 | 2, 2 |
| 3 | 2275 | yes | none | 2275 | 2, 2 |
| 5 | 2275 | yes | 5, 5 | 91 | 2, 2, 5, 5 |
| 7 | 91 | yes | 7 | 13 | 2, 2, 5, 5, 7 |
| 9 | 13 | no ($81 > 13$) | | 13 | 2, 2, 5, 5, 7 |

The loop stops at $d = 9$ because $81 > 13$. Line L6 appends $13$, and the result is $9100 = 2^2 \cdot 5^2 \cdot 7 \cdot 13$. The method tried only four divisors, while $\sqrt{9100} \approx 95$; the early stop of line L2 saved the rest.

## Correctness

The proof uses a [loop invariant](/loop-invariant/) of line L2: $N = (\prod F) \cdot m$, each entry of $F$ is a prime at most $d$ in non-decreasing order, and $m$ has no prime factor less than $d$. When $d$ divides $m$ at line L3, each prime factor of $d$ divides $m$ and so is at least $d$, so $d$ is prime. When the loop stops, $d^2 > m$; a composite $m$ would have a prime factor at most $\sqrt{m} < d$, so $m$ is $1$ or a prime, and line L6 completes the factorization. The loop ends because $d$ grows by at least $1$ in each pass while $m$ never grows. The full proof is below.

## Complexity

**Where the loop stops.** Let $Q$ be the largest prime factor of $N$ and $P$ the second largest, counted with multiplicity ($P = 1$ when $N$ is $1$ or a prime). While $d \le P$, the number $m$ still contains $P$ and $Q$, so $m \ge PQ \ge d^2$ and the loop goes on. When $d > P$, every factor except $Q$ is removed, so $m = Q$, and the loop stops at the first $d$ with $d^2 > Q$. So the last trial divisor is about $\max(P, \sqrt{Q})$, and the number of trial divisors is about half of that.

- **Worst case.** $N$ prime, or $N = 2q$ with $q$ prime. Then about $\frac12 \sqrt{N}$ trial divisors are tried. The time is $O(N^{1/2})$ on the word RAM and $O(N^{1/2} n^2)$ bit operations for an arbitrary-precision $N$.
- **Best case.** $N = 2^k$. Line L3 divides $k = \lg N$ times, then $d = 3$ fails the test of line L2. The time is $\Theta(\log N)$.
- **The number of divisions** is the number of trial divisors plus the number of successful divisions, at most $\lg N$. This gives the bound $O(\max(P, Q^{1/2}) + \log N)$ of the front matter.
- **Extra space** is $O(1)$ words besides the output, or $O(n)$ bits for an arbitrary-precision $N$.

**Typical numbers.** The worst case is common enough to dominate the average: Crandall and Pomerance (Section 3.1.4) note that the average cost over composite $N$ is still close to $N^{1/2}$. If one discards the 50% hardest numbers, the average of the rest is about $N^{c}$ with $c = 1/(2\sqrt{e}) \approx 0.303$. Knuth and Trabb Pardo give the distributions of $P$ and $Q$ that control these averages; the probability that $Q \le N^{1/u}$ tends to the [Dickman function](/dickman-function/) $\rho(u)$.

## Properties

- **Deterministic and exact.** The output is the full factorization, with a proof: each factor is prime by the invariant.
- **A primality test.** For a prime $N$ the output is $[N]$. This proves primality, at the cost of $\Theta(N^{1/2})$ divisions.
- **Finds small factors first.** A prime factor $p$ is found after about $p/2$ trial divisors, whatever the size of $N$.
- **Partial factorization.** Stopped at a bound $B$, the algorithm gives the factorization of the largest [$B$-smooth](/smooth-number/) divisor of $N$.

## Variants and improvements

- **Primes only.** Divide only by primes from a [sieve of Eratosthenes](/sieve-of-eratosthenes/). This needs about $2\sqrt{N}/\ln N$ divisions instead of $\frac12 \sqrt{N}$, at the cost of a table of the primes up to $\sqrt{N}$.
- **[Wheel factorization](/wheel-factorization/).** Skip the multiples of $2, 3, 5$ with a fixed pattern of steps. The wheel modulo $30$ tries $8$ of each $30$ numbers instead of $15$.
- **Bounded trial division.** Stop at a bound $B$ and return the rest $m$. With a fast [primality test](/primality-testing/) on $m$, a program then calls [Pollard's rho](/pollard-rho/) or another method only when $m$ is composite.
- **A table of smallest prime factors.** For many queries $N \le X$, a [smallest prime factor table](/smallest-prime-factor-table/) of size $X$ gives each factorization in $O(\log N)$ time.
- **Batch division.** To find the small factors of many numbers at once, take one gcd with the product of all the small primes, or use a product tree and a remainder tree (see [batch gcd](/batch-gcd/)).

## When to use it

Use trial division for $N$ up to about $10^{12}$, where $10^6$ divisions are cheap. Use it as the first stage before any other method: the cost to remove all prime factors below $10^4$ is small, and the faster methods do badly on small factors (Fermat's method) or need $N$ to be free of them (the sieve methods). For larger $N$ with large factors, switch to [Pollard's rho](/pollard-rho/), [SQUFOF](/shanks-squfof/) or the [elliptic curve method](/elliptic-curve-factorization/). To test primality, use [Miller-Rabin](/miller-rabin/), which is much faster than trial division.

## Pitfalls

- **The test against the original number.** A loop `while d * d ≤ N` instead of line L2 is still correct, but it does not stop early, and it takes $\Theta(N^{1/2})$ steps even for $N = 2^{40}$. Compare with the current $m$.
- **A floating-point square root.** A bound `d ≤ sqrt(m)` with a double has rounding errors for $m > 2^{53}$ and can stop one step too early. Keep the exact test $d \cdot d \le m$ of line L2, or use an [integer square root](/integer-square-root/).
- **Overflow of $d \cdot d$.** In 64-bit arithmetic with $m$ close to $2^{64}$, $d \cdot d$ can overflow. Write the test as $d \le m / d$ (integer division).
- **A single test instead of a loop.** Line L3 must be a loop. With `if m mod d = 0` the factor $2$ of $N = 12$ is found only once, the loop ends at $d = 3$ with $m = 6$, and the output is $[2, 6]$.
- **The last factor.** Without line L6 the largest prime factor is lost when it is larger than $\sqrt{N}$: for $N = 26$ the loop ends with $m = 13$.

## Implementations

## History

Trial division is the oldest factoring method, and the textbooks give it first: it is Algorithm A of Knuth's Section 4.5.4 and Algorithm 3.1.1 of Crandall and Pomerance. Knuth and Trabb Pardo analyzed its running time in 1976 through the distribution of the largest prime factors of a random integer, which is governed by the Dickman function.

## References
