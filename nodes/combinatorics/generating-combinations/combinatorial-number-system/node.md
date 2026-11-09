---
tag: GBWB9K
kind: concept
slug: combinatorial-number-system
name: Combinatorial number system
aliases:
- combinadic
- combinatorial numbering
- combinatorial number system of degree k
- binomial representation of an integer
area: combinatorics/generating-combinations
level: core
summary: Writes each integer uniquely as a sum of binomial coefficients, giving a bijection between integers and k-subsets.
prereqs: [binomial-coefficient, colexicographic-order]
see_also: [colexicographic-order, combinatorial-ranking-and-unranking, k-subset-enumeration, hockey-stick-identity, enumerative-coding, rrr-bitvector, pascal-triangle-dp, big-integer]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3, Generating all combinations (Theorem L, after D. H. Lehmer, and the combinatorial number system of degree t, with a reference to E. Pascal, 1887)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 2, Section 2.3, k-element subsets (co-lex rank and unrank)
---

The combinatorial number system of degree $k$ writes each integer $N \ge 0$ in exactly one way as
$$N = \binom{c_k}{k} + \binom{c_{k-1}}{k-1} + \cdots + \binom{c_1}{1}, \qquad c_k > c_{k-1} > \cdots > c_1 \ge 0.$$
The digits $c_k, \ldots, c_1$ form a $k$-subset of $\{0, 1, 2, \ldots\}$, and $N$ is the position of that subset in [colexicographic order](/colexicographic-order/). So the system is a bijection between the integers $N \ge 0$ and the $k$-subsets, with no bound $n$ on the elements. A greedy method computes the digits, and the sum computes $N$ back.

## In plain words

In base ten, each number has one list of digits. Here each number has one list of $k$ different numbers instead. You find them greedily. Take the largest $c$ such that "$c$ choose $k$" is at most your number. Subtract that, and go on with $k - 1$ and the rest.

The list you get is a set of $k$ numbers. If you list all sets of $k$ numbers in colex order, this set is at the position of your number. So one number can stand for one choice of $k$ items, and the other way round. Programs use this to store a choice as one integer, or to pick the choice with a given index.

## The idea

**The theorem.** Fix $k \ge 1$. For each integer $N \ge 0$ there is exactly one sequence $c_k > \cdots > c_1 \ge 0$ with $N = \sum_{i=1}^{k} \binom{c_i}{i}$. The convention $\binom{c}{i} = 0$ for $c < i$ is needed: low digits can be smaller than their index.

**A key bound.** If $c_k = c$, the largest possible sum is reached by $c, c - 1, \ldots, c - k + 1$:
$$\binom{c}{k} + \binom{c-1}{k-1} + \cdots + \binom{c-k+1}{1} = \binom{c+1}{k} - 1.$$
This is the [hockey stick identity](/hockey-stick-identity/). So each sum with top digit $c$ lies in the range $\binom{c}{k} \le N < \binom{c+1}{k}$.

**Existence, by the greedy method.** Choose $c_k$ as the largest $c$ with $\binom{c}{k} \le N$. Then $N < \binom{c_k + 1}{k}$, so the rest $N' = N - \binom{c_k}{k}$ is less than $\binom{c_k + 1}{k} - \binom{c_k}{k} = \binom{c_k}{k-1}$. Write $N'$ with $k - 1$ digits by the same method. Its top digit $c_{k-1}$ satisfies $\binom{c_{k-1}}{k-1} \le N' < \binom{c_k}{k-1}$, so $c_{k-1} < c_k$. For $k = 1$ the method gives $c_1 = N$.

**Uniqueness.** By the key bound, the top digit of any representation is the unique $c$ with $\binom{c}{k} \le N < \binom{c+1}{k}$. So any representation has the greedy top digit, and by induction on $k$ the same holds for the other digits.

**The link to colex order.** The number of $k$-subsets of $\{0, 1, 2, \ldots\}$ that come before $\{c_k > \cdots > c_1\}$ in colex order is $\sum_i \binom{c_i}{i}$. The sets with a smaller top element are the $k$-subsets of $\{0, \ldots, c_k - 1\}$, and there are $\binom{c_k}{k}$ of them. The sets with the same top element and a smaller rest are counted in the same way, one level down. Knuth gives this as Theorem L in Section 7.2.1.3, after an observation of D. H. Lehmer (1964). Knuth credits the number system itself to E. Pascal (1887).

**Cost.** Computing $N$ from the digits takes $k$ binomial coefficients, so $O(k)$ arithmetic operations with a table of [Pascal's triangle](/pascal-triangle-dp/). Computing the digits from $N$ by a downward scan, from a bound $n > c_k$ down to $0$, takes $O(n)$ arithmetic operations: the scan for $c_k$ starts at $n - 1$, and the scan for each later digit starts where the last one stopped. With a binary search for each digit it takes $O(k \log n)$ operations. The numbers are as large as $\binom{n}{k}$, so for large $n$ they need [big integers](/big-integer/). For example $\binom{100}{50}$ has $97$ bits.

**Information content.** The $k$-subsets of $\{0, \ldots, n-1\}$ have the numbers $0, \ldots, \binom{n}{k} - 1$. So the system stores such a subset in $\lceil \log_2 \binom{n}{k} \rceil$ bits, the least possible number. This is the basis of [enumerative coding](/enumerative-coding/).

## Examples

**$N = 72$, $k = 3$.** The binomials $\binom{c}{3}$ are $\ldots, 35, 56, 84$ for $c = 7, 8, 9$. So $c_3 = 8$ and the rest is $72 - 56 = 16$. Then $\binom{6}{2} = 15 \le 16 < 21 = \binom{7}{2}$, so $c_2 = 6$ and the rest is $1$. Then $c_1 = 1$. So
$$72 = \binom{8}{3} + \binom{6}{2} + \binom{1}{1} = 56 + 15 + 1.$$
The set $\{8, 6, 1\}$ is at position $72$ in the colex list of $3$-subsets.

**$N = 19$, $k = 3$.** $19 = \binom{5}{3} + \binom{4}{2} + \binom{3}{1} = 10 + 6 + 3$, so the digits are $5, 4, 3$. This is the last $3$-subset of $\{0, \ldots, 5\}$: by the key bound, $\binom{6}{3} - 1 = 19$.

**$N = 1000000$, $k = 4$.** The digits are $71, 56, 36, 15$:
$$\binom{71}{4} + \binom{56}{3} + \binom{36}{2} + \binom{15}{1} = 971635 + 27720 + 630 + 15 = 1000000.$$

**The first ten numbers for $k = 3$.**

| $N$ | digits $c_3 c_2 c_1$ | $N$ | digits $c_3 c_2 c_1$ |
| --- | --- | --- | --- |
| 0 | $2, 1, 0$ | 5 | $4, 2, 0$ |
| 1 | $3, 1, 0$ | 6 | $4, 2, 1$ |
| 2 | $3, 2, 0$ | 7 | $4, 3, 0$ |
| 3 | $3, 2, 1$ | 8 | $4, 3, 1$ |
| 4 | $4, 1, 0$ | 9 | $4, 3, 2$ |

This is the colex list of the $3$-subsets of $\{0, \ldots, 4\}$.

## Where it is used

- **Ranking and unranking.** The system is the standard rank and unrank for $k$-subsets in colex order. Lexicographic rank follows by the mirror map $a \mapsto n - 1 - a$. See [ranking and unranking combinations](/combinatorial-ranking-and-unranking/).
- **Compact storage.** A program stores a poker hand, a $5$-subset of $52$ cards, as one integer below $\binom{52}{5} = 2598960$, and uses it as an index into a table.
- **Succinct bit vectors.** The [RRR bit vector](/rrr-bitvector/) stores each block of $b$ bits as its weight and the index of the block among the blocks of that weight. See also [enumerative coding](/enumerative-coding/).
- **Random and parallel generation.** Unrank a uniform random integer below $\binom{n}{k}$ to get a uniform random $k$-subset. Unrank the start of each range to split a [k-subset enumeration](/k-subset-enumeration/) among processors.
- **Extremal set theory.** The Kruskal-Katona theorem states the least size of a shadow with this representation of the number of sets, see [colexicographic order](/colexicographic-order/).

## References
