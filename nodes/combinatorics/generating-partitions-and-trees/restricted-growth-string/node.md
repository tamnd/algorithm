---
tag: 26XAZW
kind: definition
slug: restricted-growth-string
name: Restricted growth string
aliases:
- RGS
- Canonical set partition code
- Restricted growth function
area: combinatorics/generating-partitions-and-trees
level: core
summary: A sequence a_1 ... a_n with a_1 = 0 and each a_i at most 1 + max(a_1, ..., a_(i-1)); these strings are in bijection with the set partitions of {1, ..., n}.
prereqs: [set-partitions]
see_also: [set-partition-generation, stirling-numbers, bell-numbers, partition-lattice, ranking-unranking, catalan-numbers, lexicographic-order]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.5, Generating all set partitions (restricted growth strings and their lexicographic order)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 3, Section 3.2, Set partitions, Bell and Stirling numbers (restricted growth functions, with ranking and unranking)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.9, The twelvefold way (set partitions and Stirling numbers of the second kind)
---

A restricted growth string (RGS) of length $n$ is a sequence $a_1 a_2 \ldots a_n$ of non-negative integers with $a_1 = 0$ in which each entry is at most one more than the largest entry before it. It is the standard code for a [set partition](/set-partitions/) of $[n] = \{1, \ldots, n\}$: $a_i$ is the number of the block of $i$, when the blocks are numbered $0, 1, 2, \ldots$ in the order of their smallest elements. The code turns the problem of listing set partitions into the problem of listing strings, which [Algorithm H](/set-partition-generation/) solves in lexicographic order.

## Definition

**Notation.** $n \ge 0$, $[n] = \{1, \ldots, n\}$, and $k$ is a number of blocks.

**Restricted growth string.** A sequence $a = a_1 \ldots a_n$ of integers is an RGS when

$$a_1 = 0 \quad\text{and}\quad 0 \le a_i \le 1 + \max(a_1, \ldots, a_{i-1}) \quad (2 \le i \le n).$$

For $n = 0$ the empty string is the one RGS. Some books shift all values by $1$, so that $a_1 = 1$ and the values are block numbers from $1$.

**Bijection with set partitions.** For a partition $\pi$ of $[n]$, order its blocks by their smallest elements as $B_0, B_1, \ldots, B_{k-1}$, and let $a_i = j$ when $i \in B_j$. Call this string $r(\pi)$.

*Claim.* $r$ is a bijection from the partitions of $[n]$ onto the RGS of length $n$, and $\pi$ has $k$ blocks exactly when $\max_i a_i = k - 1$.

*Proof.*

1. *$r(\pi)$ is an RGS.* Element $1$ is the smallest of all, so it lies in $B_0$, and $a_1 = 0$. Let $i \ge 2$ with $a_i = j \ge 1$. The smallest elements $m_0 < m_1 < \cdots < m_j$ of $B_0, \ldots, B_j$ are at most $i$, and $m_{j-1} < m_j \le i$, so the position $m_{j-1} < i$ has value $j - 1$. So $j \le 1 + \max(a_1, \ldots, a_{i-1})$.
2. *The inverse.* For an RGS $a$, let $B_j = \{i : a_i = j\}$ for $j = 0, \ldots, \max_i a_i$. Each value from $0$ to the maximum appears, because the values grow by at most $1$ over the running maximum. So the $B_j$ are nonempty, disjoint and cover $[n]$, and the first time $j$ appears is before the first time $j + 1$ appears, so the numbering is by smallest elements. This gives $r^{-1}(a)$.
3. The two maps are inverse to each other, and the number of blocks is the number of values, $1 + \max_i a_i$. $\square$

So the number of RGS of length $n$ is the Bell number $B_n$, and the number with maximum $k - 1$ is the [Stirling number](/stirling-numbers/) $S(n, k)$.

**Running maximum.** Write $b_i = 1 + \max(a_1, \ldots, a_{i-1})$ for $i \ge 2$, the number of blocks among $1, \ldots, i - 1$. The condition is $0 \le a_i \le b_i$: element $i$ joins one of the $b_i$ blocks so far, or it opens block number $b_i$.

**Completions and rank.** Let $T(r, b)$ be the number of ways to complete a prefix that uses $b$ blocks with $r$ more entries. Then $T(0, b) = 1$ and $T(r, b) = b\, T(r - 1, b) + T(r - 1, b + 1)$, by the choice of the next entry, and $T(r, 1) = B_{r+1}$. In lexicographic order, starting from $0$, the rank of an RGS is

$$\operatorname{rank}(a) = \sum_{i=2}^{n} a_i\, T(n - i, b_i).$$

*Proof.* The strings before $a$ are those that first differ from $a$ at some $i \ge 2$ with a smaller value $v < a_i$ there. Since $v < a_i \le b_i$, the value $v$ does not open a new block, so each such $v$ leaves $T(n - i, b_i)$ completions, and there are $a_i$ values $v$. $\square$

With the table of $T$, ranking and unranking take $O(n)$ big integer operations.

## Examples and non-examples

**$n = 3$.** The five RGS are $000, 001, 010, 011, 012$, for the partitions $\{1,2,3\}$, $\{1,2\}\{3\}$, $\{1,3\}\{2\}$, $\{1\}\{2,3\}$ and $\{1\}\{2\}\{3\}$.

**$n = 4$.** The $15$ RGS in lexicographic order, with their partitions:

| rank | RGS | partition | rank | RGS | partition |
| --- | --- | --- | --- | --- | --- |
| $0$ | $0000$ | $\{1,2,3,4\}$ | $8$ | $0110$ | $\{1,4\}\{2,3\}$ |
| $1$ | $0001$ | $\{1,2,3\}\{4\}$ | $9$ | $0111$ | $\{1\}\{2,3,4\}$ |
| $2$ | $0010$ | $\{1,2,4\}\{3\}$ | $10$ | $0112$ | $\{1\}\{2,3\}\{4\}$ |
| $3$ | $0011$ | $\{1,2\}\{3,4\}$ | $11$ | $0120$ | $\{1,4\}\{2\}\{3\}$ |
| $4$ | $0012$ | $\{1,2\}\{3\}\{4\}$ | $12$ | $0121$ | $\{1\}\{2,4\}\{3\}$ |
| $5$ | $0100$ | $\{1,3,4\}\{2\}$ | $13$ | $0122$ | $\{1\}\{2\}\{3,4\}$ |
| $6$ | $0101$ | $\{1,3\}\{2,4\}$ | $14$ | $0123$ | $\{1\}\{2\}\{3\}\{4\}$ |
| $7$ | $0102$ | $\{1,3\}\{2\}\{4\}$ | | | |

For $0110$ the formula gives rank $1 \cdot T(2, 1) + 1 \cdot T(1, 2) + 0 = 5 + 3 = 8$, since $T(2, 1) = B_3 = 5$ and $T(1, 2) = 3$.

**From a partition.** For $\{2, 5\}, \{1, 3\}, \{4\}$, the blocks in order of smallest elements are $\{1, 3\}, \{2, 5\}, \{4\}$, so the RGS is $01021$.

**Non-examples.**

- $1000$ is not an RGS, because $a_1 \ne 0$. It names the same partition as $0111$ with the block numbers swapped; the RGS is the unique numbering by smallest elements.
- $0021$ is not an RGS, because $a_3 = 2$ but $1 + \max(0, 0) = 1$.
- $0120$ is an RGS, while $0220$ is not. Every value up to the maximum must appear before a larger one.

## Related definitions

- [Set partitions](/set-partitions/): the objects that RGS encode, counted by the Bell numbers.
- [Set partition generation](/set-partition-generation/): Algorithm H lists the RGS in lexicographic order in constant amortized time.
- [Stirling numbers](/stirling-numbers/): $S(n, k)$ counts the RGS with maximum $k - 1$, and the recurrence $T(r, b)$ is a refinement of their recurrence.
- [Bell numbers](/bell-numbers/): $B_n$ counts the RGS of length $n$.
- [Partition lattice](/partition-lattice/): the refinement order on set partitions, which is not the lexicographic order of the RGS.
- [Catalan numbers](/catalan-numbers/): the sequences with $a_1 = 0$ and $0 \le a_i \le a_{i-1} + 1$, a stronger growth limit, are counted by $C_n$; for $n = 4$ there are $14$ of them against $B_4 = 15$ RGS, since $0102$ is an RGS but $a_4 = 2 > a_3 + 1$.
- [Ranking and unranking](/ranking-unranking/): the table $T(r, b)$ gives the rank and unrank maps.

## References
