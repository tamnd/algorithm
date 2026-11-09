---
tag: X3M1JR
kind: concept
slug: integer-partition-function
name: Partition function p(n)
aliases:
- Number of partitions p(n)
- Partition numbers
area: combinatorics/generating-partitions-and-trees
level: core
summary: The function p(n) counts the integer partitions of n; it grows like exp(pi sqrt(2n/3)) divided by 4n sqrt(3).
prereqs: [integer-partitions, generating-functions]
see_also: [integer-partition-counting, euler-pentagonal-recurrence, euler-pentagonal-number-theorem, hardy-ramanujan-theorem, rademacher-formula, euler-partition-theorem, integer-partition-generation, coin-change-counting]
sources:
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 1 (generating functions and the pentagonal number theorem), Chapter 5, The Hardy-Ramanujan-Rademacher expansion of p(n), pages 68 to 87, and Chapter 10, Congruence properties of partition functions
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.4, Generating all partitions (the generating function, Euler's recurrence and the asymptotic formula for p(n))
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 14, Partitions (the generating function, Euler's pentagonal number theorem and the recurrence with the sum of divisors)
  - paper: doi:10.1112/S1461157012001088
    title: Fredrik Johansson, Efficient implementation of the Hardy-Ramanujan-Rademacher formula, LMS Journal of Computation and Mathematics 15 (2012), 341-359
    locator: the whole paper (the computation of a single p(n) from the Rademacher series, with error control)
---

The partition function $p(n)$ is the number of [integer partitions](/integer-partitions/) of $n$, the ways to write $n$ as a sum of positive integers when the order does not matter. It starts $1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42$ for $n = 0, \ldots, 10$, and it grows faster than every polynomial but slower than every exponential $c^n$ with $c > 1$: by the [Hardy-Ramanujan theorem](/hardy-ramanujan-theorem/), $p(n) \sim \frac{1}{4n\sqrt 3} e^{\pi\sqrt{2n/3}}$. It is the length of every list of all partitions, and it has a simple [generating function](/generating-functions/), fast recurrences and an exact formula.

## In plain words

Count the ways to split a pile of identical coins into smaller piles, where only the sizes of the piles matter. For a pile of four there are five ways: one pile of four, three and one, two and two, two and one and one, and four single coins. This count, as a function of the size of the pile, is the partition function.

The counts grow fast. For a pile of one hundred there are about two hundred million ways. Still, they grow far slower than the number of ordered splits, which doubles each time the pile grows by one coin. A program can compute the count for a large pile quickly, without listing the splits.

## The idea

**Definition.** For an integer $n \ge 0$, $p(n)$ is the number of sequences $\lambda_1 \ge \cdots \ge \lambda_\ell \ge 1$ with sum $n$. So $p(0) = 1$, for the empty partition, and we set $p(n) = 0$ for $n < 0$.

**The generating function.** As [formal power series](/generating-functions/),

$$\sum_{n \ge 0} p(n)\, x^n = \prod_{k \ge 1} \frac{1}{1 - x^k}.$$

*Proof.* Expand each factor as $\sum_{m_k \ge 0} x^{k m_k}$. A term of the product picks one exponent $m_k$ for each $k$, with only finitely many nonzero, and gives $x^{\sum_k k m_k}$. The choices with $\sum_k k m_k = n$ are the multiplicity forms $1^{m_1} 2^{m_2} \cdots$ of the partitions of $n$, one for each partition. $\square$

**The table of the largest part.** Let $p(n, k)$ be the number of partitions of $n$ with each part at most $k$. Then $p(0, k) = 1$, $p(n, 0) = 0$ for $n \ge 1$, and

$$p(n, k) = p(n, k - 1) + p(n - k, k) \qquad (n, k \ge 1),$$

with $p(n - k, k) = 0$ when $n < k$. The first term counts the partitions with no part $k$, and the second removes one part $k$ from the others. This gives $p(0), \ldots, p(n)$ in $O(n^2)$ additions, and it is the same table as [coin change counting](/coin-change-counting/) with coins $1, \ldots, n$.

**Euler's recurrence.** By the [pentagonal number theorem](/euler-pentagonal-number-theorem/), $\prod_{k \ge 1} (1 - x^k) = \sum_{j \in \mathbb{Z}} (-1)^j x^{j(3j-1)/2}$. Multiplying this series by the generating function of $p$ gives $1$, so for $n \ge 1$

$$p(n) = \sum_{j \ge 1} (-1)^{j+1} \Big( p\big(n - \tfrac{j(3j-1)}{2}\big) + p\big(n - \tfrac{j(3j+1)}{2}\big) \Big).$$

Only $O(\sqrt n)$ terms are nonzero, since the pentagonal numbers $j(3j \mp 1)/2$ grow as $3j^2/2$. So $p(0), \ldots, p(n)$ take $O(n^{3/2})$ additions of big integers. See the [pentagonal recurrence](/euler-pentagonal-recurrence/).

**The divisor recurrence.** Let $\sigma(k)$ be the sum of the divisors of $k$. For $n \ge 1$,

$$n\, p(n) = \sum_{k=1}^{n} \sigma(k)\, p(n - k).$$

*Proof.* Let $P(x) = \prod_k (1 - x^k)^{-1}$. Then $x P'(x)/P(x) = \sum_k \frac{k x^k}{1 - x^k} = \sum_k \sum_{m \ge 1} k x^{km} = \sum_{N \ge 1} \sigma(N) x^N$. So $x P'(x) = P(x) \sum_N \sigma(N) x^N$, and the coefficient of $x^n$ on both sides gives the identity. $\square$

**Size and growth.** The bounds $e^{2\sqrt n - 4}/n \le p(n) < e^{\pi\sqrt{2n/3}}$ hold for all $n \ge 1$, with elementary proofs on the page of the [Hardy-Ramanujan theorem](/hardy-ramanujan-theorem/). So $\log p(n) = \Theta(\sqrt n)$, and $p(n)$ has $\Theta(\sqrt n)$ bits; the asymptotic formula gives about $\pi \sqrt{2n/3} / \ln 2 - \log_2 n$ bits. [Rademacher's formula](/rademacher-formula/) gives $p(n)$ exactly as a convergent series.

**Cost of computing it.** Let $M(b)$ be the time to multiply two $b$-bit integers.

- All of $p(0), \ldots, p(n)$ exactly: Euler's recurrence takes $O(n^{3/2})$ additions of $O(\sqrt n)$-bit numbers, so $O(n^2)$ bit operations.
- All of $p(0), \ldots, p(n)$ modulo a prime $m$: the same recurrence takes $O(n^{3/2})$ word operations. [Power series inversion](/power-series-inversion/) of the pentagonal series, with [FFT multiplication](/fft-polynomial-multiplication/) over a suitable prime, takes $O(n \log n)$ operations.
- One value $p(n)$ exactly: Johansson (2012) evaluates the Rademacher series with enough terms and enough precision, in time close to linear in the $\Theta(\sqrt n)$ bits of the result.

## Examples

**First values.** For $n = 0, \ldots, 20$, $p(n)$ is

$$1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627.$$

**Euler's recurrence at $n = 10$.** The pentagonal numbers up to $10$ are $1, 2, 5, 7$, with signs $+, +, -, -$. So $p(10) = p(9) + p(8) - p(5) - p(3) = 30 + 22 - 7 - 3 = 42$. For all $n \le 1000$ the recurrence uses $33475$ terms in total, against about $500000$ steps of the $p(n, k)$ table.

**Larger values.** $p(100) = 190569292$, $p(200) = 3972999029388$, and

$$p(1000) = 24061467864032622473692149727991,$$

a number of $32$ decimal digits and $105$ bits. The Hardy-Ramanujan formula gives $p(100) \approx 1.993 \times 10^8$, which is $4.6\%$ too large, and $p(1000) \approx 2.440 \times 10^{31}$, which is $1.4\%$ too large.

**Ramanujan's congruences.** For all $k \ge 0$,

$$p(5k + 4) \equiv 0 \pmod 5, \qquad p(7k + 5) \equiv 0 \pmod 7, \qquad p(11k + 6) \equiv 0 \pmod{11}.$$

For example $p(4) = 5$, $p(9) = 30$, $p(5) = 7$, $p(12) = 77$, $p(6) = 11$ and $p(17) = 297 = 27 \cdot 11$. Andrews proves these and related results in Chapter 10.

**Non-example.** The number of ordered sums, the [compositions](/integer-compositions/), is $2^{n-1}$ for $n \ge 1$, which is $16$ for $n = 5$ against $p(5) = 7$. The order of the parts makes the difference.

## Where it is used

- **Generation.** $p(n)$ is the number of steps of every generator of all partitions, such as [Algorithm P](/integer-partition-generation/), and it tells you before the run whether a full list is feasible.
- **Ranking and random partitions.** The tables $p(n, k)$ give the rank and unrank maps of partitions in reverse lexicographic order, and so a uniform random partition from a random integer below $p(n)$.
- **Counting with restrictions.** The product form adapts to parts in a set $S$, distinct parts, or bounded multiplicities, as in [Euler's partition theorem](/euler-partition-theorem/) and in [coin change counting](/coin-change-counting/).
- **Cycle types and conjugacy classes.** $p(n)$ is the number of conjugacy classes of the [symmetric group](/symmetric-group/) $S_n$, and the number of abelian groups of order $q^n$ for a prime $q$.
- **Asymptotic analysis.** $p(n)$ is the standard example of the saddle point method and of the circle method, which lead to the [Hardy-Ramanujan theorem](/hardy-ramanujan-theorem/) and to [Rademacher's formula](/rademacher-formula/).

## References
