---
tag: 390KSX
kind: definition
slug: bell-numbers
name: Bell numbers
aliases:
- Bell's numbers
- exponential numbers
area: combinatorics/counting-algorithms
level: core
summary: Total number of set partitions of an n-element set.
prereqs: [stirling-numbers-second-kind, binomial-coefficient]
see_also: [stirling-numbers-second-kind, counting-set-partitions, set-partitions, set-partition-generation, restricted-growth-string, exponential-generating-functions, partition-lattice, integer-partition-counting]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.5, Generating all set partitions (the Bell numbers, their triangle and their asymptotics)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.9, The twelvefold way (the Bell number B(n))
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 6.1, Stirling Numbers, and Section 7.6, Exponential Generating Functions
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter II, Section II.3, Surjections, set partitions, and words
---

The Bell number $B_n$ is the number of ways to split a set of $n$ elements into nonempty blocks, with no order on the blocks. It is the sum of the [Stirling numbers of the second kind](/stirling-numbers-second-kind/) $S(n, k)$ over all $k$, and the number of equivalence relations on an $n$-set. The sequence starts $1, 1, 2, 5, 15, 52, 203, 877$. It grows faster than any exponential $c^n$ but slower than $n!$, so a program that lists all [set partitions](/set-partitions/) works only for small $n$.

## Definition

**Notation.** $n \ge 0$ is the size of the ground set $[n] = \{1, \ldots, n\}$, $k$ is the number of blocks, and $S(n, k)$ is the Stirling number of the second kind.

A set partition of $[n]$ is a set of nonempty, pairwise disjoint subsets of $[n]$, the blocks, whose union is $[n]$. The Bell number is

$$B_n = \bigl|\{\pi : \pi \text{ is a set partition of } [n]\}\bigr| = \sum_{k=0}^{n} S(n, k).$$

The empty set has one partition, the one with no blocks, so $B_0 = 1$. A set partition is the same thing as an equivalence relation, whose classes are the blocks, so $B_n$ also counts the equivalence relations on $[n]$.

**Recurrence.** For $n \ge 0$,

$$B_{n+1} = \sum_{k=0}^{n} \binom{n}{k} B_k.$$

*Proof.* Split the partitions of $[n+1]$ by the block $X$ that holds $n + 1$. Let $j = |X| - 1$ be the number of other elements of $X$. There are $\binom{n}{j}$ choices of these elements, and the other $n - j$ elements form any partition of a set of size $n - j$, in $B_{n-j}$ ways. So $B_{n+1} = \sum_j \binom{n}{j} B_{n-j}$, and $\binom{n}{j} = \binom{n}{n-j}$ gives the form above. $\square$

**Exponential generating function.** $\sum_{n \ge 0} B_n \frac{z^n}{n!} = \exp(e^z - 1)$. A partition is a set of blocks, and a block is a nonempty set with the [exponential generating function](/exponential-generating-functions/) $e^z - 1$, so this is the exponential formula.

**Dobinski's formula.** For $n \ge 0$,

$$B_n = \frac{1}{e} \sum_{m=0}^{\infty} \frac{m^n}{m!}.$$

*Proof.* By the conversion $m^n = \sum_k S(n, k)\, m^{\underline k}$ and $m^{\underline k}/m! = 1/(m-k)!$ for $m \ge k$ (and $0$ for $m < k$), $\sum_m \frac{m^n}{m!} = \sum_k S(n, k) \sum_{m \ge k} \frac{1}{(m-k)!} = e \sum_k S(n, k) = e\, B_n$. All terms are non-negative, so the order of summation can change. $\square$ In probability terms, $B_n$ is the $n$th moment of a Poisson random variable with mean 1.

**Bounds.** For $n \ge 1$, $2^{n-1} \le B_n \le n!$. *Proof.* Lower bound: the partitions with at most two blocks, where the block of the element 1 is any set that contains 1, already number $2^{n-1}$. Upper bound: write each block as a cycle in increasing order. This maps each partition to a different permutation of $[n]$, so $B_n \le n!$. $\square$ Both bounds are far from the truth for large $n$: $\ln B_n = n \ln n - n \ln \ln n - n + o(n)$, a result of de Bruijn's saddle point analysis, so $B_n$ grows like $(n / \ln n)^n$ up to an exponential factor (Knuth, Section 7.2.1.5).

**The Bell triangle.** Put $a(0, 0) = 1$. For $n \ge 1$, put $a(n, 0) = a(n-1, n-1)$ and $a(n, k) = a(n, k-1) + a(n-1, k-1)$ for $1 \le k \le n$. Then $a(n, 0) = B_n$. *Proof.* We show $a(n, k) = \sum_{j=0}^{k} \binom{k}{j} B_{n-k+j}$ by induction on $n$, and on $k$ inside each row. The case $k = 0$ is $a(n, 0) = B_n$. It holds for $n = 0$. For $k \ge 1$, the rule gives $a(n, k) = \sum_j \binom{k-1}{j} B_{n-k+1+j} + \sum_j \binom{k-1}{j} B_{n-k+j}$, and [Pascal's rule](/pascal-triangle-dp/) merges the two sums into $\sum_j \binom{k}{j} B_{n-k+j}$. For the first entry of row $n + 1$, $a(n+1, 0) = a(n, n) = \sum_j \binom{n}{j} B_j = B_{n+1}$ by the recurrence. $\square$ The triangle computes $B_0, \ldots, B_n$ with $n(n+1)/2$ additions and no multiplication.

## Examples and non-examples

**Example 1.** $B_3 = 5$. The partitions of $\{1, 2, 3\}$ are $1|2|3$, $12|3$, $13|2$, $1|23$ and $123$. By blocks, this is $S(3, 1) + S(3, 2) + S(3, 3) = 1 + 3 + 1$.

**Example 2: the first values.** For $n = 0$ to $15$ the Bell numbers are

$$1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975, 678570, 4213597, 27644437, 190899322, 1382958545$$

(OEIS A000110). Further, $B_{20} = 51724158235372$, and $B_{100}$ has 116 decimal digits.

**Example 3: the Bell triangle.** Each row starts with the last entry of the row before, and each next entry is the sum of the entry to its left and the entry above that one (OEIS A011971).

| n | row |
|---|---|
| 0 | 1 |
| 1 | 1, 2 |
| 2 | 2, 3, 5 |
| 3 | 5, 7, 10, 15 |
| 4 | 15, 20, 27, 37, 52 |
| 5 | 52, 67, 87, 114, 151, 203 |

**Example 4: rhyme schemes.** A rhyme scheme of a poem with $n$ lines says which lines rhyme, such as $aabb$ or $abab$. It is a partition of the lines, so there are $B_4 = 15$ rhyme schemes for 4 lines. Written as [restricted growth strings](/restricted-growth-string/) with the letters in order of first use, they are the 15 strings $aaaa, aaab, \ldots, abcd$.

**Example 5: Dobinski's formula.** For $n = 5$, $\frac{1}{e} \sum_{m \ge 0} \frac{m^5}{m!} = 52.000\ldots$, which is $B_5$.

**Non-example 1: integer partitions.** The number of ways to split the integer $n$ into parts is $p(n)$, not $B_n$. The units of an integer are identical, so $p(4) = 5$ while $B_4 = 15$. See [counting integer partitions](/integer-partition-counting/).

**Non-example 2: ordered blocks.** If the order of the blocks matters, the count is the ordered Bell (Fubini) number $\sum_k k!\, S(n, k)$: $1, 1, 3, 13, 75, 541$. For $n = 2$ there are 3 ordered partitions ($12$, $1|2$, $2|1$) but $B_2 = 2$.

**Non-example 3: Bell polynomials.** The Bell polynomials $B_{n,k}(x_1, x_2, \ldots)$ of Faà di Bruno's formula are a different object. They reduce to $S(n, k)$ only when every $x_i = 1$.

## Related definitions

- [Stirling numbers of the second kind](/stirling-numbers-second-kind/) split $B_n$ by the number of blocks.
- [Counting set partitions](/counting-set-partitions/) is the problem of computing $B_n$ exactly or modulo a prime, with the algorithms and their costs.
- [Set partitions](/set-partitions/) and [set partition generation](/set-partition-generation/) list the $B_n$ partitions, often as [restricted growth strings](/restricted-growth-string/).
- The [partition lattice](/partition-lattice/) orders the $B_n$ partitions of $[n]$ by refinement.
- [Exponential generating functions](/exponential-generating-functions/) give $\exp(e^z - 1)$ through the exponential formula.

## References
