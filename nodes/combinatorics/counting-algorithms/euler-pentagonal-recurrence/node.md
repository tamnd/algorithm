---
tag: SBKFAF
kind: algorithm
slug: euler-pentagonal-recurrence
name: Euler's pentagonal recurrence for partitions
aliases:
- pentagonal recurrence for p(n)
- Euler's recurrence for the partition function
- pentagonal number recurrence
area: combinatorics/counting-algorithms
level: advanced
summary: Computes p(n) in O(n^1.5) using a pentagonal-number recurrence.
solves: [integer-partition-counting]
model: word-ram
complexity:
  vars: {n: the largest index whose partition number is computed}
  time: {worst: Θ(n^(3/2)), best: Θ(n^(3/2))}
  space: {extra: Θ(n)}
  bit_operations: {worst: Θ(n^2)}
properties: {deterministic: true, recursive: false, exact: true, online: true}
history:
  year: 1750
  people: [Leonhard Euler, Percy Alexander MacMahon]
  note: Euler derived the recurrence from his pentagonal number theorem. MacMahon used it in 1918 to tabulate p(n) up to n = 200 for Hardy and Ramanujan.
prereqs: [euler-pentagonal-number-theorem, integer-partition-counting, loop-invariant]
see_also: [integer-partition-function, euler-pentagonal-number-theorem, hardy-ramanujan-asymptotics, rademacher-formula, coin-change-counting, power-series-inversion, tabulation]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.4, Generating all partitions (Euler's recurrence for p(n) from the pentagonal number theorem)
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 1, The elementary theory of partitions (the pentagonal number theorem and the recurrence for p(n))
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 14, Partitions (Euler's pentagonal-number theorem and the recurrence for p(n))
---

Euler's pentagonal recurrence computes the partition numbers $p(0), p(1), \ldots, p(n)$ from the identity $p(m) = p(m-1) + p(m-2) - p(m-5) - p(m-7) + p(m-12) + \cdots$, where the shifts are the generalized pentagonal numbers. Each $p(m)$ needs only about $1.6\sqrt m$ earlier values, so the whole prefix costs $\Theta(n^{3/2})$ additions, against $\Theta(n^2)$ for the [coin change](/coin-change-counting/) table. It works in exact integers or modulo any $M$, and it is the standard way to tabulate $p(n)$ for $n$ up to the hundreds of thousands.

## In plain words

To count the ways to split a pile of identical coins, the method builds a table of answers for piles of size 0, 1, 2 and so on. Each new answer is a short signed sum of answers already in the table. The rule looks back 1 and 2 places and adds them, then looks back 5 and 7 places and subtracts them, then 12 and 15 places and adds them, and so on with growing gaps. The gaps grow fast, so each new answer needs only a few earlier ones. That is why the table fills much faster than with the usual method that tries every pile size as a part.

## The problem

**Notation.** $n \ge 0$ is an integer, and $p(m)$ is the number of partitions of $m$, the ways to write $m$ as a sum of positive integers without regard to order. $p(0) = 1$ and $p(m) = 0$ for $m < 0$. For an integer $j$, $g_j = j(3j - 1)/2$, so $g_j$ for $j = 1, -1, 2, -2, 3, -3, \ldots$ runs $1, 2, 5, 7, 12, 15, \ldots$ and $g_{-j} = j(3j + 1)/2$.

The input is $n$, and optionally a modulus $M \ge 1$. The output is the list $p(0), \ldots, p(n)$, as exact integers, or as residues modulo $M$. This is the prefix form of [counting integer partitions](/integer-partition-counting/).

## The algorithm

The recurrence comes from the [pentagonal number theorem](/euler-pentagonal-number-theorem/): for $m \ge 1$,

$$p(m) = \sum_{j \ge 1} (-1)^{j+1} \bigl( p(m - g_j) + p(m - g_{-j}) \bigr).$$

```pseudo id=main
PENTAGONAL-PARTITIONS(n)                    ▷ returns P with P[m] = p(m) for 0 ≤ m ≤ n
L1  P[0] ← 1
L2  for m ← 1 to n
L3      s ← 0, j ← 1
L4      while j(3j − 1)/2 ≤ m do
L5          if j is odd then c ← +1 else c ← −1     ▷ the sign (−1)^(j+1)
L6          s ← s + c · P[m − j(3j − 1)/2]
L7          if j(3j + 1)/2 ≤ m then s ← s + c · P[m − j(3j + 1)/2]
L8          j ← j + 1
L9      P[m] ← s
L10 return P
```

For residues modulo $M$, reduce $s$ modulo $M$ at line L9, and start with $P[0] = 1 \bmod M$. The pentagonal numbers can also be stepped without multiplication: $g_{j+1} = g_j + 3j + 1$ and $g_{-j} = g_j + j$.

## Example

Compute up to $n = 12$. The rows show which earlier values each step uses.

| $m$ | terms | $p(m)$ |
|---|---|---|
| 1 | $p(0)$ | 1 |
| 2 | $p(1) + p(0)$ | 2 |
| 3 | $p(2) + p(1)$ | 3 |
| 4 | $p(3) + p(2)$ | 5 |
| 5 | $p(4) + p(3) - p(0)$ | 7 |
| 6 | $p(5) + p(4) - p(1)$ | 11 |
| 7 | $p(6) + p(5) - p(2) - p(0)$ | 15 |
| 8 | $p(7) + p(6) - p(3) - p(1)$ | 22 |
| 9 | $p(8) + p(7) - p(4) - p(2)$ | 30 |
| 10 | $p(9) + p(8) - p(5) - p(3)$ | 42 |
| 11 | $p(10) + p(9) - p(6) - p(4)$ | 56 |
| 12 | $p(11) + p(10) - p(7) - p(5) + p(0)$ | 77 |

For example, $p(12) = 56 + 42 - 15 - 7 + 1 = 77$. The values match OEIS A000041. For $m = 12$ the loop runs for $j = 1, 2, 3$: $g_3 = 12 \le 12$, but $g_{-3} = 15 > 12$, so line L7 skips the second term.

## Correctness

The pentagonal number theorem states $\prod_{k \ge 1} (1 - x^k) = \sum_j (-1)^j x^{g_j}$. The product of this series and $\sum_m p(m) x^m = \prod_k (1 - x^k)^{-1}$ is $1$, so the coefficient of $x^m$ for $m \ge 1$ gives $\sum_j (-1)^j p(m - g_j) = 0$. The $j = 0$ term is $p(m)$, which gives the recurrence above. The loop invariant of line L2 is that $P[0 \ldots m-1]$ holds $p(0), \ldots, p(m-1)$. The inner loop adds exactly the terms with $g_j \le m$ and $g_{-j} \le m$, which are the nonzero ones, since $g_1 < g_{-1} < g_2 < g_{-2} < \cdots$. The full proof is below.

## Complexity

For a fixed $m$, the loop of line L4 runs for the $j \ge 1$ with $j(3j - 1)/2 \le m$, about $\sqrt{2m/3}$ times, and does at most two additions each time. Summing over $m \le n$ gives at most $\frac{4}{3}\sqrt{2/3}\, n^{3/2} + O(n) \approx 1.09\, n^{3/2}$ additions. The count is the same for every input, so the best and the worst case are $\Theta(n^{3/2})$ operations. For $n = 1000$ the program does $33475$ additions.

- **Modulo $M$.** Each addition is one word operation, so the time is $\Theta(n^{3/2})$.
- **Exact integers.** $p(m) \le e^{\pi\sqrt{2m/3}}$, so $p(m)$ has at most $3.71\sqrt m$ bits, and an addition costs $O(\sqrt m)$ bit operations. The total is $\Theta(n^2)$ bit operations.
- **Space.** The table holds $n + 1$ numbers, which is $\Theta(n)$ words modulo $M$ or $\Theta(n^{3/2})$ bits exactly.

## Properties

- **Exact.** It uses only additions and subtractions of integers, with no division and no rounding.
- **Online.** The table can grow one entry at a time, so a program can extend a prefix it has already computed.
- **Intermediate sums.** After the first pair of terms, $s = p(m-1) + p(m-2)$, which can be larger than $p(m)$. In fixed-width arithmetic the running sum can therefore overflow slightly before $p(m)$ itself does.
- **Deterministic and not recursive.** The work does not depend on the values.

## Variants and improvements

- **Residues.** Computing modulo $M$ keeps every number in one word, and the time is $\Theta(n^{3/2})$ word operations. This is the form used to search for partition congruences.
- **Power series inversion.** The same identity says that $\sum_m p(m) x^m$ is the inverse of a sparse series. With [power series inversion](/power-series-inversion/) and the [number-theoretic transform](/number-theoretic-transform/), the prefix modulo a suitable prime costs $O(n \log n)$.
- **One value.** To get only $p(n)$ for a large $n$, the [Rademacher formula](/rademacher-formula/) is much faster, with time close to the $\Theta(\sqrt n)$ size of the answer.
- **Sum of divisors.** The same loop with the base term replaced by $m$ computes $\sigma(m)$, the sum of the divisors of $m$, by Euler's rule $\sigma(m) = \sigma(m-1) + \sigma(m-2) - \sigma(m-5) - \cdots$.
- **Restricted parts.** For parts from a set $S$, the pentagonal trick does not apply. Use the [coin change counting](/coin-change-counting/) table instead.

## When to use it

Use it to tabulate all of $p(0), \ldots, p(n)$ exactly, or modulo a number, for $n$ up to about $10^5$ exactly or $10^6$ modulo a word-size number. It is short and has no numerical error. For a single large $p(n)$, use the Rademacher series. For a prefix modulo an NTT prime of length in the millions, power series inversion is faster.

## Pitfalls

- **The sign pattern.** The signs go $+, +, -, -, +, +, \ldots$ in pairs: both terms for one $j$ share the sign $(-1)^{j+1}$. A program that alternates the sign at every term is wrong from $m = 2$ on.
- **The second term.** The loop must stop on $g_j > m$, not on $g_{-j} > m$, and line L7 must test $g_{-j}$ separately. Stopping on $g_{-j}$ skips the last term when $g_j \le m < g_{-j}$, as at $m = 12$.
- **Overflow.** $p(122)$ is the first value at least $2^{31}$, $p(406)$ the first at least $2^{63}$ and $p(417)$ the first at least $2^{64}$. Use big integers or a modulus beyond these points.
- **Negative residues.** Modulo $M$, the running sum can be negative in languages where the remainder keeps the sign of the dividend. Reduce to $[0, M)$ before storing.

## Implementations

## History

Euler found the pentagonal number theorem by computation in the 1740s and proved it around 1750, and the recurrence for $p(n)$ follows from it at once. In 1918 Percy MacMahon used the recurrence to compute $p(n)$ for all $n \le 200$. Hardy and Ramanujan compared their asymptotic series with his table and found that a few terms gave $p(200) = 3972999029388$ exactly.

## References
