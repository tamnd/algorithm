---
tag: AS8516
kind: problem
slug: primes-in-range
name: Listing primes in an interval
aliases:
- primes in [L, R]
- primes in a range
- interval prime listing
area: number-theory/sieves
level: core
summary: Given L <= R, list all primes p with L <= p <= R. The segmented sieve does it in O((R - L + 1) log log R + R^(1/2)) word operations, with memory for the primes up to R^(1/2) and one block.
model: word-ram
complexity:
  vars: {L: the lower end, R: the upper end, Δ: the length R - L + 1}
  time: {worst: "O(Δ log log R + R^(1/2))"}
  space: {extra: "O(R^(1/2) + Δ)"}
prereqs: [primes-up-to-n]
see_also: [segmented-sieve, primes-up-to-n, sieve-of-eratosthenes, prime-counting-function, miller-rabin, deterministic-miller-rabin-bases, prime-gaps, trial-division]
sources:
  - paper: doi:10.1007/BF01932283
    title: Carter Bays and Richard H. Hudson, The segmented sieve of Eratosthenes and primes in arithmetic progressions to 10^12, BIT 17(2), 1977
    locator: pages 121 to 127 (the segmented sieve and its use on intervals up to 10^12)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.2, Sieving (sieving an interval with the primes up to the square root of its upper end)
  - paper: doi:10.1112/S0025579300004708
    title: H. L. Montgomery and R. C. Vaughan, The large sieve, Mathematika 20(2), 1973
    locator: pages 119 to 134 (the Brun-Titchmarsh bound pi(x + y) - pi(x) <= 2y / log y)
---

Listing the primes in an interval is the problem of writing out every [prime](/prime-number/) $p$ with $L \le p \le R$, for integers $L \le R$. It extends [listing primes up to n](/primes-up-to-n/) to intervals far from 0, where a table that starts at 0 would be too large. The [segmented sieve](/segmented-sieve/) solves it with $O(\Delta \log \log R + \sqrt R)$ word operations, where $\Delta = R - L + 1$, because every composite in the interval has a prime factor at most $\sqrt R$. Short intervals near huge numbers are also handled by a [primality test](/primality-testing/) on each candidate.

## In plain words

You get two numbers, a start and an end, and must list the primes between them. The start may be huge, say a billion, while the gap between the two is small.

A plain sieve would have to cross out everything from two up to the end, which wastes time and memory. But to tell whether a number is prime, you only need to know whether a prime up to its square root divides it. So it is enough to find the small primes first, and then cross out their multiples inside the window alone.

## Definition

**Input.** Integers $L$ and $R$ with $L \le R$.

**Output.** The increasing list of all primes $p$ with $L \le p \le R$. Values below 2 contain no prime, so the answer for $[L, R]$ equals the answer for $[\max(L, 2), R]$, and it is empty if $R < 2$.

**Cost model.** The [word RAM](/word-ram/) with words of $\Theta(\log R)$ binary digits: arithmetic, comparisons and array access on numbers up to $R$ cost one step. Memory is counted in words or flags. Two lengths matter: $\Delta = R - L + 1$, and $\sqrt R$.

## Variants

- **Counting.** Return $\pi(R) - \pi(L - 1)$ only. For a long interval, two calls to a [prime-counting](/prime-counting-function/) method are faster than sieving.
- **Many short intervals.** Answer many queries with the same base list of primes up to $\sqrt{R_{\max}}$.
- **Factor tables of an interval.** Return the smallest prime factor of each $m$ in $[L, R]$, or the values of a multiplicative function; the same sieve does this.
- **Primes in a progression.** List the primes $p \equiv a \pmod q$ in the interval, as Bays and Hudson did up to $10^{12}$.

## Examples

| $[L, R]$ | output |
|---|---|
| $[0, 10]$ | 2, 3, 5, 7 |
| $[1, 1]$ | empty |
| $[2, 2]$ | 2 |
| $[24, 28]$ | empty |
| $[100, 130]$ | 101, 103, 107, 109, 113, 127 |
| $[114, 126]$ | empty, inside the gap between 113 and 127 |
| $[10^9, 10^9 + 100]$ | $10^9 + 7$, $+9$, $+21$, $+33$, $+87$, $+93$, $+97$ |

For $[10^9, 10^9 + 100]$ the base primes are those up to $\lfloor \sqrt{10^9 + 100} \rfloor = 31622$, and the interval has 101 numbers, of which 7 are prime.

## Known algorithms

| algorithm | time (word operations) | memory |
|---|---|---|
| [trial division](/trial-division/) of each number | $O(\Delta \sqrt R)$ | $O(1)$ besides the output |
| [deterministic Miller-Rabin](/deterministic-miller-rabin-bases/) on each number | $O(\Delta \log R)$ multiplications modulo numbers up to $R$ | $O(1)$ besides the output |
| full [sieve of Eratosthenes](/sieve-of-eratosthenes/) up to $R$ | $O(R \log \log R)$ | $O(R)$ |
| [segmented sieve](/segmented-sieve/) | $O(\Delta \log \log R + \sqrt R)$ | $O(\sqrt R + \Delta)$, or $O(\sqrt R)$ with blocks |

The Miller-Rabin bound is proved for the ranges where a fixed set of bases is known to be correct, for example $R < 3.3 \cdot 10^{24}$ with the first thirteen primes as bases; for general $R$ it relies on the generalized Riemann hypothesis, or one uses a randomized test. The segmented sieve bound is proved: the term $\sqrt R$ covers the base sieve, the term $\Delta \log \log R$ covers the marking, by Mertens' theorem on $\sum 1/p$. If $\Delta$ is much smaller than $\sqrt R$, the base sieve dominates, and testing each number is faster.

## Bounds

The output can have up to about $\Delta / \ln \Delta$ numbers: Montgomery and Vaughan proved $\pi(x + y) - \pi(x) \le 2y / \ln y$ for all $x \ge 1$ and $y > 1$, a form of the Brun-Titchmarsh theorem, so a short interval never holds many more primes than the start of the number line does. The marking cost $\Delta \log \log R$ of the segmented sieve exceeds this output size by a factor of about $\log \Delta \cdot \log \log R$, and the wheels behind the sublinear sieves of Pritchard and of Atkin and Bernstein reduce it further. A lower bound beyond the size of the output is not known.

## Reductions

- **From listing up to $n$.** The case $L = 2$, $R = n$ is [listing primes up to n](/primes-up-to-n/).
- **To listing up to $\sqrt R$.** The segmented sieve needs the primes up to $\sqrt R$ first, a call to the problem with bound $\sqrt R$.
- **To primality testing.** Each $m$ in the interval can be tested on its own, which is the better choice when $\Delta$ is tiny.

## Applications

- Searching for [prime gaps](/prime-gaps/) and checking conjectures such as Goldbach's far from 0.
- Finding the next prime after a large number, or the $n$-th prime after a [prime count](/prime-counting-function/) has located it.
- The segmented sieve is the standard way to list primes up to large $n$ with small memory.

## References
