---
tag: 0EN12C
kind: problem
slug: integer-partition-counting
name: Counting integer partitions
aliases:
- partition function p(n)
- computing p(n)
- number of partitions of n
area: combinatorics/counting-algorithms
level: core
summary: Computing the number of ways to write n as an unordered sum of positive integers.
prereqs: [integer-partitions, generating-functions]
see_also: [integer-partition-function, euler-pentagonal-recurrence, euler-pentagonal-number-theorem, hardy-ramanujan-asymptotics, rademacher-formula, coin-change-counting, integer-partition-generation, conjugate-partition]
sources:
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 1, The elementary theory of partitions (generating functions and the pentagonal number theorem)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.4, Generating all partitions (the generating function, Euler's recurrence and the asymptotics of p(n))
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 14, Partitions (the recurrence with the sum of divisors)
  - paper: doi:10.1112/S1461157012001088
    title: Fredrik Johansson, Efficient implementation of the Hardy-Ramanujan-Rademacher formula, LMS Journal of Computation and Mathematics 15 (2012), 341-359
    locator: the whole paper (one value of p(n) from the Rademacher series in softly optimal time)
---

Counting integer partitions asks for $p(n)$, the number of ways to write $n$ as a sum of positive integers when the order of the summands does not matter. The answer has only $\Theta(\sqrt n)$ digits, so it can be computed for huge $n$, and the best method depends on whether one value, a whole prefix, or a residue is wanted. The main tools are a [coin change](/coin-change-counting/) style table, [Euler's pentagonal recurrence](/euler-pentagonal-recurrence/), power series inversion, and the [Rademacher series](/rademacher-formula/).

## In plain words

You have a pile of identical coins and want to split it into smaller piles. Only the sizes of the piles matter, not their order. A pile of 4 coins can be split in 5 ways: 4, 3 and 1, 2 and 2, 2 and 1 and 1, or four single coins. The task is to compute this number of ways for a given pile size. A pile of 100 already has about 190 million splits, so a program must count them without listing them.

## Definition

**Notation.** $n \ge 0$ is an integer. A partition of $n$ is a sequence $\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_\ell \ge 1$ of integers with $\lambda_1 + \cdots + \lambda_\ell = n$, and the $\lambda_i$ are its parts. $p(n)$ is the number of partitions of $n$, with $p(0) = 1$ and $p(n) = 0$ for $n < 0$. $C(n, k)$ is a binomial coefficient.

**Input:** an integer $n \ge 0$, and in some variants a bound $k$ or a modulus $m$.

**Output:** $p(n)$ as an exact integer, or $p(n) \bmod m$, or the whole prefix $p(0), \ldots, p(n)$.

The [generating function](/generating-functions/) is

$$\sum_{n \ge 0} p(n)\, x^n = \prod_{k \ge 1} \frac{1}{1 - x^k},$$

because a partition picks, for each $k \ge 1$, how many parts equal $k$, and the factor $1/(1 - x^k) = 1 + x^k + x^{2k} + \cdots$ records that choice.

## Variants

- **Parts at most $k$.** $p_k(n)$, the number of partitions of $n$ with all parts at most $k$, satisfies $p_k(n) = p_{k-1}(n) + p_k(n - k)$: either no part equals $k$, or removing one part $k$ leaves a partition of $n - k$ with parts at most $k$. By the [conjugate partition](/conjugate-partition/), $p_k(n)$ also counts partitions of $n$ into at most $k$ parts.
- **Exactly $k$ parts.** $p(n, k)$ satisfies $p(n, k) = p(n-1, k-1) + p(n-k, k)$: either a part equals 1 and is removed, or every part is at least 2 and each part loses 1. The triangle starts $1$; $1, 1$; $1, 1, 1$; $1, 2, 1, 1$; $1, 2, 2, 1, 1$ (OEIS A008284).
- **Distinct parts.** $q(n)$, with generating function $\prod_k (1 + x^k)$, starts $1, 1, 1, 2, 2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 22, 27$ (OEIS A000009). It equals the number of partitions into odd parts, since $\prod_k (1 + x^k) = \prod_k \frac{1 - x^{2k}}{1 - x^k} = \prod_{k \text{ odd}} \frac{1}{1 - x^k}$. This is [Euler's partition theorem](/euler-partition-theorem/).
- **Parts from a set.** If the parts must come from a set $S$, the problem is [coin change counting](/coin-change-counting/).
- **Residues.** Compute $p(n) \bmod m$, for example to study congruences such as Ramanujan's $p(5j + 4) \equiv 0 \pmod 5$.

## Examples

**Example 1.** The partitions of 5 are $5$, $4+1$, $3+2$, $3+1+1$, $2+2+1$, $2+1+1+1$ and $1+1+1+1+1$, so $p(5) = 7$.

**Example 2.** For $n = 0$ to $15$, $p(n)$ is $1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176$ (OEIS A000041).

**Example 3.** $p(100) = 190569292$, $p(200) = 3972999029388$, and $p(1000) = 24061467864032622473692149727991$, a number with 32 digits and 105 bits.

**Example 4: Ramanujan's congruence.** $p(4) = 5$, $p(9) = 30$, $p(14) = 135$ and $p(19) = 490$ are all multiples of 5.

## Known algorithms

**Table over the largest part.** Start with $p_0(m) = [m = 0]$, and for $k = 1, \ldots, n$ update $p_k(m) = p_{k-1}(m) + p_k(m - k)$ in place for $m = k, \ldots, n$. This is the coin change loop with every coin $1, \ldots, n$. It uses $O(n^2)$ additions and $O(n)$ memory, and it gives the whole prefix. The numbers have $O(\sqrt n)$ bits, so the exact bit cost is $O(n^{5/2})$.

**Euler's pentagonal recurrence.** By the [pentagonal number theorem](/euler-pentagonal-number-theorem/),

$$p(n) = \sum_{j \ne 0} (-1)^{j+1}\, p\bigl(n - j(3j - 1)/2\bigr),$$

a sum over the positive and negative $j$ with $j(3j - 1)/2 \le n$. There are about $1.6 \sqrt n$ such terms, so the whole prefix costs $O(n^{3/2})$ additions and $O(n^2)$ bit operations in exact arithmetic. This is the standard method for exact prefixes. See [Euler's pentagonal recurrence](/euler-pentagonal-recurrence/).

**The divisor recurrence.** With $\sigma(k)$ the sum of the divisors of $k$,

$$n\, p(n) = \sum_{k=1}^{n} \sigma(k)\, p(n - k).$$

*Proof.* Take the logarithmic derivative of the product: $x P'(x) / P(x) = \sum_k \frac{k x^k}{1 - x^k} = \sum_{m \ge 1} \sigma(m)\, x^m$. Multiply by $P(x)$ and compare the coefficients of $x^n$. $\square$ It costs $O(n^2)$ operations and needs a division by $n$, so it is slower than the pentagonal recurrence. It is a useful cross-check.

**Power series inversion.** The product $\prod_k (1 - x^k)$ is sparse by the pentagonal number theorem: it is $\sum_j (-1)^j x^{j(3j-1)/2}$. Modulo a prime that suits the [number-theoretic transform](/number-theoretic-transform/), [power series inversion](/power-series-inversion/) of this sparse series gives $p(0), \ldots, p(n) \bmod m$ in $O(n \log n)$ operations.

**The Rademacher series.** For one exact value of a large $n$, the [Rademacher formula](/rademacher-formula/) expresses $p(n)$ as a fast convergent series. Johansson showed how to evaluate it with controlled error so that $p(n)$ comes out in $O(n^{1/2 + o(1)})$ bit operations, which is close to the size of the output.

**Brute force.** [Integer partition generation](/integer-partition-generation/) lists all partitions in $O(1)$ amortized time each, so counting by listing costs $\Theta(p(n))$, which is exponential in $\sqrt n$. Use it only as a test oracle.

## Bounds

- **Output size.** $\ln p(n) \sim \pi \sqrt{2n/3}$, so $p(n)$ has about $3.7 \sqrt n$ bits. Any exact algorithm must spend $\Omega(\sqrt n)$ time to write the answer, and the Rademacher method meets this bound up to the $n^{o(1)}$ factor. The proof of the leading term is on the [Hardy-Ramanujan asymptotics](/hardy-ramanujan-asymptotics/) page.
- **Elementary bounds.** $p(n) \le e^{\pi \sqrt{2n/3}}$ for every $n \ge 1$, and $p(n) \ge 2^{\lfloor \sqrt n \rfloor - 1}$ for $n \ge 1$. For the lower bound, let $s = \lfloor \sqrt n \rfloor$. The parts $2, \ldots, s$ have sum below $s(s+1)/2 \le n$, so each of the $2^{s-1}$ subsets of them, filled up to $n$ with ones, is a partition of $n$, and different subsets give different partitions.
- **Prefix.** The prefix $p(0), \ldots, p(n)$ has $\Theta(n^{3/2})$ bits in total, so the $O(n^2)$ bit cost of the pentagonal recurrence is within a factor $\sqrt n$ of the output size.

## Reductions

- Counting partitions with parts in $\{1, \ldots, n\}$ is the coin change counting problem with these $n$ coin values, so any coin change algorithm counts partitions.
- $p(n)$ is the number of conjugacy classes of the symmetric group $S_n$, since two permutations are conjugate exactly when they have the same cycle type, and cycle types are partitions of $n$.
- $p(n)$ is the number of Ferrers diagrams with $n$ cells, and the number of multisets of positive integers with sum $n$.
- The number of abelian groups of order $q^n$, for a prime $q$, up to isomorphism, is $p(n)$, by the structure theorem for finite abelian groups.

## Applications

- **Representation theory.** The irreducible representations of $S_n$ are indexed by the partitions of $n$, so $p(n)$ is the size of the character table of $S_n$.
- **Test generation.** Counting partitions gives the exact size of an exhaustive test space before a program lists it, and the counts give a check for partition generators.
- **Statistical mechanics.** The number of states of a quantum system of identical bosons with total energy $n$ in equally spaced levels is a partition count, and the Hardy-Ramanujan asymptotics give its entropy.
- **Number theory.** Computations of $p(n) \bmod m$ for many $n$ test and discover partition congruences.

## References
