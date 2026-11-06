---
tag: KWQ8J3
kind: algorithm
slug: lucy-hedgehog-prime-counting
name: Lucy_Hedgehog prime counting
aliases:
- Lucy's prime counting
- Lucy sieve
- Lucy_Hedgehog algorithm
area: number-theory/sieves
level: advanced
summary: Computes pi(x) by running the sieve of Eratosthenes on the counts S(v) for the values v = floor(x/k) only. It takes O(x^(3/4) / log x) time and O(x^(1/2)) memory.
solves: [prime-counting-function]
model: word-ram
complexity:
  vars: {x: the input, r: the integer square root of x}
  time: {worst: "O(x^(3/4) / log x)"}
  space: {extra: "O(x^(1/2))"}
properties: {deterministic: true, recursive: false}
prereqs: [prime-counting-function, sieve-of-eratosthenes]
see_also: [meissel-lehmer-algorithm, prime-counting-function, legendre-phi-function, sieve-of-eratosthenes, fenwick-tree, multiplicative-functions-up-to-n, primes-up-to-n]
sources:
  - url: https://gbroxey.github.io/blog/2023/04/09/lucy-fenwick.html
    title: Griffin Macris, Lucy's Algorithm + Fenwick Trees, griff's math blog, 2023
    locator: Sections The Lucy_Hedgehog Algorithm (Square Root Trick, Algorithm (Lucy), Runtime Analysis) and Sums of Primes, Primes Squared
  - url: https://projecteuler.net/problem=10
    title: Project Euler, Problem 10, Summation of primes
    locator: the forum thread of the problem, where the user Lucy_Hedgehog posted the method for the sum of the primes
  - paper: doi:10.1090/S0025-5718-96-00674-6
    title: M. Deléglise and J. Rivat, Computing pi(x), the Meissel, Lehmer, Lagarias, Miller, Odlyzko method, Mathematics of Computation 65(213), 1996
    locator: Section 1 (the history of combinatorial prime counting, for comparison)
---

The Lucy_Hedgehog method computes the [prime-counting function](/prime-counting-function/) $\pi(x)$ by running the [sieve of Eratosthenes](/sieve-of-eratosthenes/) on counts instead of on numbers. It keeps, for each of the about $2\sqrt x$ distinct values $v = \lfloor x/k \rfloor$, the number $S(v)$ of integers in $[2, v]$ not yet crossed out, and for each prime $p \le \sqrt x$ it updates all $S(v)$ with $v \ge p^2$ by the rule $S(v) \leftarrow S(v) - (S(\lfloor v/p \rfloor) - S(p - 1))$. At the end, $S(x) = \pi(x)$. It takes $O(x^{3/4} / \log x)$ word operations and $O(\sqrt x)$ memory, and the same few lines compute the sum of the primes up to $x$ or other sums over primes.

## In plain words

Suppose you ran the sieve of Eratosthenes up to a huge bound but only cared about how many numbers survive, not which ones. You do not need every count: when a prime crosses out its multiples, the number of survivors up to some bound drops by an amount that depends only on how many survivors there were up to a smaller bound, that bound divided by the prime.

The bounds that ever come up are the results of dividing the big bound by whole numbers, and there are only about twice its square root of them. So the method keeps one counter per such bound, and for each small prime it updates the counters from the largest bound down. The counter for the big bound ends as the number of primes.

## The problem

The input is an integer $x$. The output is $\pi(x)$, the number of primes $p \le x$. The cost model is the [word RAM](/word-ram/) with words of $\Theta(\log x)$ binary digits: arithmetic, comparisons and array access on numbers up to $x$ cost one step. Memory is counted in words.

Let $r = \lfloor \sqrt x \rfloor$ and $V = \{ \lfloor x/k \rfloor : 1 \le k \le x \}$. For $m \ge 2$, $\mathrm{lpf}(m)$ is the least prime factor of $m$.

## The algorithm

For $q \ge 1$ and $v \ge 0$ let

$$S_q(v) = \#\{ 2 \le n \le v : n \text{ is prime or } \mathrm{lpf}(n) > q \},$$

the number of survivors in $[2, v]$ after the sieve has used the primes up to $q$. Then $S_1(v) = v - 1$, and $S_r(x) = \pi(x)$, since every composite $n \le x$ has $\mathrm{lpf}(n) \le \sqrt x$. The algorithm moves from $S_{p-1}$ to $S_p$ for $p = 2, 3, \ldots, r$, keeping only the values on $V$.

```pseudo id=main
LUCY(x)                                    ▷ returns π(x)
L1  if x < 2 then return 0
L2  r ← ⌊√x⌋; V ← the distinct values ⌊x / k⌋ for k ≥ 1
L3  S[v] ← v − 1 for each v in V
L4  for p ← 2 to r do
L5      if S[p] = S[p − 1] then continue     ▷ p is composite
L6      c ← S[p − 1]                         ▷ c = π(p − 1)
L7      for each v in V with v ≥ p², in decreasing order do
L8          S[v] ← S[v] − (S[⌊v / p⌋] − c)   ▷ remove the composites with least prime factor p
L9  return S[x]
```

**Storage.** $V$ has at most $2r$ elements: the values $1, 2, \ldots, r$, which all lie in $V$, and the values $\lfloor x/k \rfloor$ for $1 \le k \le r$. A value $v \le r$ is kept at index $v$ of an array `small`, and $v = \lfloor x/k \rfloor > r$ at index $k$ of an array `large`, so $\lfloor v/p \rfloor = \lfloor x/(kp) \rfloor$ is at `large[kp]` when $kp \le r$ and at `small[x // (kp)]` otherwise. Both arrays need $r + 1$ words.

**The order.** Line L8 reads $S[\lfloor v/p \rfloor]$ for a smaller value, which must still hold $S_{p-1}$; going through $V$ in decreasing order guarantees that.

## Example

Take $x = 30$, so $r = 5$ and $V = \{30, 15, 10, 7, 6, 5, 4, 3, 2, 1\}$.

| $v$ | 30 | 15 | 10 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|
| $S_1(v) = v - 1$ | 29 | 14 | 9 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
| after $p = 2$ | 15 | 8 | 5 | 4 | 3 | 3 | 2 | 2 | 1 | 0 |
| after $p = 3$ | 11 | 6 | 4 | 4 | 3 | 3 | 2 | 2 | 1 | 0 |
| after $p = 5$ | 10 | 6 | 4 | 4 | 3 | 3 | 2 | 2 | 1 | 0 |

For $p = 2$, $c = S(1) = 0$, and for instance $S(30) \leftarrow 29 - (S(15) - 0) = 29 - 14 = 15$, the count of 2 and the 14 odd numbers from 3 to 29. For $p = 3$, $c = S(2) = 1$, and only $v \ge 9$ change: $S(30) \leftarrow 15 - (S(10) - 1) = 15 - 4 = 11$, which removes 9, 15, 21 and 27. For $p = 4$, $S(4) = S(3) = 2$, so 4 is skipped. For $p = 5$, $c = S(4) = 2$, and only $v = 30$ changes: $S(30) \leftarrow 11 - (S(6) - 2) = 10$, removing 25. So $\pi(30) = 10$.

## Correctness

The invariant is that before round $p$ of line L4, $S[v] = S_{p-1}(v)$ for every $v \in V$. A composite $n$ with $\mathrm{lpf}(n) = p$ is $n = pk$ with $p \le k$ and $\mathrm{lpf}(k) \ge p$, so there are none up to $v < p^2$, and for $v \ge p^2$ their number is $\#\{ 2 \le k \le \lfloor v/p \rfloor : \mathrm{lpf}(k) \ge p \} = S_{p-1}(\lfloor v/p \rfloor) - \pi(p - 1)$: the survivors up to $\lfloor v/p \rfloor$, minus the primes below $p$, which survive but have a smaller least prime factor. Since $S_{p-1}(p - 1) = \pi(p - 1)$, line L8 turns $S_{p-1}$ into $S_p$. Line L5 is right because $S_{p-1}(p) - S_{p-1}(p - 1)$ is 1 exactly when $p$ is prime. All the arguments stay in $V$, since $\lfloor \lfloor x/k \rfloor / p \rfloor = \lfloor x/(kp) \rfloor$. The full proof is below.

## Complexity

**Rounds.** Line L4 runs $r - 1$ times, and line L5 costs $O(1)$ each time, so $O(\sqrt x)$ in all.

**Small primes.** For a prime $p \le x^{1/4}$, line L7 visits at most $|V| \le 2\sqrt x$ values. There are $\pi(x^{1/4}) = O(x^{1/4} / \log x)$ such primes, which gives $O(x^{3/4} / \log x)$.

**Large primes.** For a prime $p > x^{1/4}$, every $v \ge p^2 > \sqrt x$ in $V$ is $\lfloor x/k \rfloor$ with $k \le x / p^2$, so line L7 visits at most $x / p^2$ values. By Chebyshev's bound $\pi(t) = O(t / \log t)$ and partial summation, $\sum_{p > T} 1/p^2 = O(1/(T \log T))$, so these primes cost $O(x / (x^{1/4} \log x)) = O(x^{3/4} / \log x)$.

**Total.** $O(x^{3/4} / \log x)$ word operations and $O(\sqrt x)$ words of memory. These bounds are proved; they use no conjecture. If line L5 is dropped and every $p \le r$ is processed, the time becomes $O(x^{3/4})$, and the answer is still correct, as the update for a composite $p$ subtracts 0.

## Properties

- **Short.** The whole method is two arrays and three nested loops, with no sieve table up to $x$.
- **Sublinear.** About $x^{3/4} / \log x$ steps instead of the $x \log \log x$ of a full sieve, which makes $x$ around $10^{11}$ to $10^{12}$ practical in a compiled language.
- **All values at once.** At the end, $S[v] = \pi(v)$ for every $v \in V$, not just for $v = x$, which is what many sums over primes need.
- **Deterministic and iterative.** No randomness, no recursion, no floating point.

## Variants and improvements

- **Sums over primes.** Replace $v - 1$ by $\sum_{2 \le n \le v} f(n)$ and the update by $S(v) \leftarrow S(v) - f(p)\,(S(\lfloor v/p \rfloor) - S(p - 1))$ for a completely multiplicative $f$, such as $f(n) = n$ or $n^2$. With $f(n) = n$ this gives the sum of the primes up to $x$, the original purpose of the method; the implementation below includes it.
- **Primes in progressions.** Running it with $f$ a Dirichlet character, or on the classes modulo $m$, counts primes in arithmetic progressions.
- **Fenwick tree.** Sieving the small values $v \le y$ with an ordinary sieve and a [Fenwick tree](/fenwick-tree/), and using the update only for the large ones, gives about $O(x^{2/3} (\log x)^{1/3})$ time for a suitable split point $y$ near $x^{2/3}$, as in Macris's write-up.
- **Multiplicative functions.** The same values $\lfloor x/k \rfloor$ carry the Min_25 and Dirichlet hyperbola style methods for sums of a [multiplicative function](/multiplicative-functions-up-to-n/) up to $x$.
- **Faster prime counting.** The [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/) takes about $x^{2/3}$ time, and its Deléglise-Rivat form $O(x^{2/3} / \log^2 x)$.

## When to use it

Use it to compute $\pi(x)$, or a sum over the primes up to $x$, for $x$ from about $10^8$ to about $10^{12}$, when a short program matters more than the last factor of speed; it is the usual choice in programming contests and in Project Euler. For much larger $x$, use the [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/). For $x$ below about $10^8$, or to list the primes, a [sieve](/primes-up-to-n/) is simpler.

## Pitfalls

- **The order of the update.** Update $V$ from the largest value down. Going up reads values that are already updated for $p$ and subtracts too much.
- **Starting at $p^2$.** Skipping the condition $v \ge p^2$ breaks the count: for $v < p^2$ the term $S(\lfloor v/p \rfloor) - c$ is zero or negative, so a negative term would raise $S(v)$ above the true count.
- **Two cells for one value.** When $\lfloor x/r \rfloor = r$, the value $r$ is in both arrays. That is harmless, as both cells get the same updates, but code that assumes $|V|$ is exactly $2r$ or $2r - 1$ should not.
- **Overflow in the sums.** For the sum of primes, $v(v+1)/2$ overflows 64-bit words for $v$ above about $4 \cdot 10^9$. Use 128-bit integers or reduce modulo a number.
- **The integer square root.** Compute $r$ exactly in integers; a floating point square root can be off by one.

## Implementations

## History

The method is named after the Project Euler user Lucy_Hedgehog, who posted it in the forum thread of Problem 10 as a way to compute the sum of the primes below a bound, a task the problem sets for two million. It is a sieve of Eratosthenes run on the counts of the values $\lfloor x/k \rfloor$, an idea close to Legendre's formula for $\pi(x)$ and to the Meissel-Lehmer method, and it has since become a standard tool in competitive programming, with write-ups such as Macris's that add a Fenwick tree to speed it up.

## References
