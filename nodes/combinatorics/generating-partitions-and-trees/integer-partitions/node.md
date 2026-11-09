---
tag: 8NAFRY
kind: problem
slug: integer-partitions
name: Integer partitions
aliases:
- Partitions of an integer
- Enumerating partitions
- Generating all partitions of n
area: combinatorics/generating-partitions-and-trees
level: intro
summary: Enumerate all ways to write a positive integer n as an unordered sum of positive integers.
complexity:
  vars: {n: the integer that is partitioned, N: "the number of partitions, p(n)"}
  time: {worst: Ω(N)}
prereqs: [combinatorial-generation]
see_also: [integer-partition-generation, integer-partition-function, integer-partition-counting, ferrers-diagram, conjugate-partition, euler-partition-theorem, integer-compositions, set-partitions]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.4, Generating all partitions (Algorithm P, Algorithm H for partitions into m parts, Gray codes, the counts p(n) and their asymptotics)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapter 9, Next partition of integer n (NEXPAR), and Chapter 10, Random partition of an integer n (RANPAR)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 3, Section 3.1, Integer partitions (generation, ranking and unranking)
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 1, The elementary theory of partitions, pages 1 to 15
---

The integer partition problem asks for a list of all partitions of $n$: the ways to write $n$ as a sum of positive integers when the order of the terms does not matter. There are $p(n)$ of them, where $p$ is the [partition function](/integer-partition-function/), so $p(5) = 7$ and $p(100) = 190569292$. Each method needs $\Omega(p(n))$ time, and [Knuth's Algorithm P](/integer-partition-generation/) meets this bound with constant amortized time for each partition.

## In plain words

You have a pile of identical coins and you want to split it into smaller piles. Only the sizes of the piles matter, not their order, so a pile of three next to a pile of two is the same split as a pile of two next to a pile of three. The task is to list every possible split once.

The usual trick is to write each split with the piles sorted from largest to smallest. Then two splits are equal only when their sorted lists are equal, and a program can walk through the sorted lists in dictionary order. The number of splits grows fast, but much slower than the number of subsets of the coins.

## Definition

**Notation.** In this page $n \ge 0$ is the integer that is partitioned, $\ell$ is the number of parts, and $N = p(n)$ is the number of partitions.

A *partition* of $n$ is a sequence $\lambda = (\lambda_1, \ldots, \lambda_\ell)$ of integers with $\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_\ell \ge 1$ and $\lambda_1 + \cdots + \lambda_\ell = n$. The $\lambda_i$ are the *parts*. We write $\lambda \vdash n$. The empty sequence is the one partition of $0$, so $p(0) = 1$. Two other forms are common:

- the *multiplicity form* $1^{m_1} 2^{m_2} \cdots n^{m_n}$, where $m_j \ge 0$ is the number of parts equal to $j$ and $\sum_j j\, m_j = n$;
- the [Ferrers diagram](/ferrers-diagram/), with $\lambda_i$ cells in row $i$.

Sorting the parts makes a partition the same thing as a multiset of positive integers with sum $n$. So the partitions of $n$ are in bijection with the solutions $(m_1, \ldots, m_n) \in \mathbb{Z}_{\ge 0}^n$ of $\sum_j j\, m_j = n$.

**Input.** An integer $n \ge 0$.

**Output.** A sequence $\lambda^{(0)}, \ldots, \lambda^{(N-1)}$ in which each partition of $n$ appears exactly once.

**Cost model.** The generator keeps one partition in an array and changes it in place. A visit of the array is free. If the program copies each partition, a copy costs $\Theta(\ell)$ more, and the total output size is $\sum_{\lambda \vdash n} \ell(\lambda)$, which is computed below.

## Variants

- **Fixed order.** Reverse lexicographic order, from $(n)$ down to $(1^n)$, is the order of [Algorithm P](/integer-partition-generation/). Lexicographic order runs from $(1^n)$ up to $(n)$.
- **Exactly $k$ parts, or at most $k$ parts.** Knuth's Algorithm H, after an idea of Hindenburg, lists the partitions into exactly $k$ parts in colexicographic order of the parts.
- **Bounded parts.** Each part at most $k$. By the transpose of the [Ferrers diagram](/ferrers-diagram/) this is the same as at most $k$ parts, see [conjugate partition](/conjugate-partition/).
- **Distinct parts, or odd parts.** Only partitions with no repeated part, or with only odd parts. [Euler's partition theorem](/euler-partition-theorem/) says the two lists have the same length.
- **Parts from a given set.** Only parts from a set $S$, for example coin values. Counting these is [coin change counting](/coin-change-counting/).
- **Counting only.** Compute $p(n)$ without a list, see [integer partition counting](/integer-partition-counting/) and the [pentagonal recurrence](/euler-pentagonal-recurrence/).
- **Rank and unrank.** Map each partition to its position in a fixed order and back.
- **One random partition.** Choose a partition of $n$ with probability $1/p(n)$.
- **Minimal change.** Each step moves one unit from one part to another part.

## Examples

**$n = 5$.** In reverse lexicographic order the $p(5) = 7$ partitions are

$$5,\quad 41,\quad 32,\quad 311,\quad 221,\quad 2111,\quad 11111.$$

In multiplicity form they are $5^1$, $1^1 4^1$, $2^1 3^1$, $1^2 3^1$, $1^1 2^2$, $1^3 2^1$ and $1^5$. Of the seven, $3$ have distinct parts ($5$, $41$, $32$) and $3$ have only odd parts ($5$, $311$, $11111$).

**The first values.** For $n = 0, 1, \ldots, 10$,

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $p(n)$ | 1 | 1 | 2 | 3 | 5 | 7 | 11 | 15 | 22 | 30 | 42 |
| parts in total | 0 | 1 | 3 | 6 | 12 | 20 | 35 | 54 | 86 | 128 | 192 |

**Sizes.** $p(20) = 627$, $p(50) = 204226$, $p(100) = 190569292$ and $p(200) = 3972999029388$. A list of all partitions of $100$ fits in a few seconds of a compiled program. A list for $n = 200$ does not.

## Known algorithms

| algorithm | order | time for each partition | page |
| --- | --- | --- | --- |
| Algorithm P (reverse lexicographic successor) | reverse lexicographic | $O(1)$ amortized | [integer partition generation](/integer-partition-generation/) |
| recursion on the largest part | reverse lexicographic | $O(1)$ amortized with care | this page, below |
| Algorithm H (Hindenburg) | exactly $k$ parts, colexicographic | $O(1)$ amortized | Knuth, Section 7.2.1.4 |
| NEXPAR (multiplicity form) | a fixed successor order | $O(1)$ amortized | Nijenhuis and Wilf, Chapter 9 |
| unrank each rank | any ranked order | $O(n)$ big integer operations, after an $O(n^2)$ table | Kreher and Stinson, Section 3.1 |

**Recursion on the largest part.** Let $P(n, k)$ be the set of partitions of $n$ with each part at most $k$. Then $P(0, k) = \{()\}$, and for $n \ge 1$, $P(n, k)$ is the disjoint union over $j = \min(n, k), \ldots, 1$ of the sets $\{(j) \cdot \mu : \mu \in P(n - j, j)\}$. A program that recurses on this rule, with the parts in an array, lists $P(n, n)$ in reverse lexicographic order. The same rule gives the count $|P(n, k)| = \sum_{j=1}^{\min(n,k)} |P(n - j, j)|$.

**Random generation.** Nijenhuis and Wilf's RANPAR picks a uniform random partition of $n$ from a table of the counts $p(0), \ldots, p(n)$. Unranking a uniform random integer in $[0, p(n))$ does the same job.

## Bounds

- **Lower bound.** There are $p(n)$ outputs, so each algorithm takes $\Omega(p(n))$ time, and $\Omega(p(n))$ changes in the in-place model.
- **Upper bound.** Algorithm P takes $\Theta(p(n))$ time in total, so $O(1)$ amortized time for each partition, with the partition kept in place. The worst delay of Algorithm P is $\Theta(n)$, at the step from $(3, 1^{n-3})$ to $(2^{\lfloor n/2 \rfloor}, 1^{n \bmod 2})$.
- **Growth.** By the [Hardy-Ramanujan theorem](/hardy-ramanujan-theorem/), $p(n) \sim \frac{1}{4n\sqrt 3} e^{\pi \sqrt{2n/3}}$. So $\log p(n) = \Theta(\sqrt n)$. The list is far shorter than the $2^{n-1}$ [compositions](/integer-compositions/).
- **Written output.** If each partition is copied in full, the time is $\Theta(\sum_{\lambda \vdash n} \ell(\lambda))$. This sum is $\sum_{k=1}^{n} d(k)\, p(n - k)$, where $d(k)$ is the number of divisors of $k$. *Proof.* The partitions with at least $t$ parts equal to $j$ are in bijection with the partitions of $n - tj$: remove $t$ copies of $j$. So the number of parts equal to $j$, summed over all $\lambda \vdash n$, is $\sum_{t \ge 1} p(n - tj)$. Summing over $j$ counts each pair $(j, t)$ with $jt = k$ once for each $k \le n$, which gives $d(k)$ terms $p(n - k)$. $\square$ For $n = 50$ the sum is $2805218$, about $13.7$ parts for each partition on average.

## Reductions

- **To multisets and coin change.** A partition of $n$ is a multiset of positive integers with sum $n$. Partitions with parts in a set $S$ are the ways to pay $n$ with coins of values in $S$, see [coin change counting](/coin-change-counting/).
- **Conjugation.** The transpose of the [Ferrers diagram](/ferrers-diagram/) is a bijection from partitions with at most $k$ parts to partitions with parts at most $k$. A generator for one family gives the other at $O(\lambda_1)$ cost for each object. See [conjugate partition](/conjugate-partition/).
- **From compositions.** Sorting the parts of a [composition](/integer-compositions/) gives a partition. A filter over all $2^{n-1}$ compositions lists the partitions, but it takes exponentially more time than $p(n)$.
- **To cycle types.** The cycle type of a [permutation](/permutation/) of $[n]$ is a partition of $n$. Two permutations are conjugate in the [symmetric group](/symmetric-group/) if and only if they have the same cycle type, so the partitions of $n$ index the conjugacy classes of $S_n$. See [permutation cycle decomposition](/permutation-cycle-decomposition/).
- **To set partitions.** The block sizes of a [set partition](/set-partitions/) of $[n]$, sorted, form a partition of $n$.

## Applications

- **Brute force over cycle types.** A program that sums a function over the permutations of $[n]$ that depends only on the cycle type can sum over the $p(n)$ partitions instead of the $n!$ permutations, with the weight $n!/\prod_j (j^{m_j} m_j!)$ for the type $1^{m_1} 2^{m_2} \cdots$. This is the core of [Pólya enumeration](/polya-enumeration-theorem/).
- **Representation theory.** The irreducible representations of $S_n$ are indexed by the partitions of $n$, and their dimensions are the numbers of [standard Young tableaux](/standard-young-tableaux/).
- **Algebra.** The abelian groups of order $q^n$, for a prime $q$, are in bijection with the partitions of $n$, by the structure theorem of finite abelian groups.
- **Test data.** Lists of partitions give all ways to split a load of $n$ units among identical machines, or all histograms with total $n$.

## References
