---
tag: RN20CX
kind: problem
slug: set-partitions
name: Set partitions
aliases:
- Enumerating set partitions
- Partitions of a set
- Generating all equivalence relations
area: combinatorics/generating-partitions-and-trees
level: intro
summary: Enumerate all ways to split the set {1, ..., n} into nonempty disjoint blocks; there are B_n of them, the Bell number.
complexity:
  vars: {n: the size of the set, N: "the number of set partitions, the Bell number B_n"}
  time: {worst: Ω(N)}
prereqs: [combinatorial-generation]
see_also: [set-partition-generation, restricted-growth-string, stirling-numbers, bell-numbers, partition-lattice, counting-set-partitions, integer-partitions, stirling-numbers-second-kind]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.5, Generating all set partitions (restricted growth strings, Algorithm H, Gray codes and the Bell numbers)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapter 11, Next equivalence relation on n letters (NEXEQU), and Chapter 12, Random equivalence relation on n letters (RANEQU)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 3, Section 3.2, Set partitions, Bell and Stirling numbers (generation, ranking and unranking of restricted growth functions)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.9, The twelvefold way (set partitions, Stirling numbers of the second kind and Bell numbers)
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter II, Labelled structures and exponential generating functions (set partitions and the generating function exp(e^z - 1))
---

The set partition problem asks for a list of all partitions of the set $[n] = \{1, \ldots, n\}$ into nonempty, disjoint blocks whose union is $[n]$. The number of them is the Bell number $B_n$: $B_4 = 15$, $B_{10} = 115975$ and $B_{20} = 51724158235372$. Each method needs $\Omega(B_n)$ time, and [Algorithm H](/set-partition-generation/), which lists the [restricted growth strings](/restricted-growth-string/), meets this bound with constant amortized time for each partition. The same objects are the equivalence relations on $[n]$.

## In plain words

You have a group of different people and you want to split them into teams. The teams have no names and no order, and every team has at least one person. The task is to list every possible way to form the teams, each one time.

A good way to write a split is to walk through the people in a fixed order and give each one a team number. The first person always gets team zero, and each later person either joins a team that already exists or opens the next new team. Each split has exactly one such list of numbers, so a program can list the number lists instead of the splits.

## Definition

**Notation.** $n \ge 0$, $[n] = \{1, \ldots, n\}$ with $[0] = \emptyset$, $k$ is a number of blocks, and $C(n, k) = \binom{n}{k}$.

**Set partition.** A partition of a finite set $X$ is a set $\pi = \{B_1, \ldots, B_k\}$ of nonempty, pairwise disjoint subsets of $X$, the blocks, with $B_1 \cup \cdots \cup B_k = X$. The order of the blocks does not matter, and the empty set has one partition, with no blocks.

**Problem.** Given $n$, output each partition of $[n]$ exactly once.

**Counts.** Let $S(n, k)$ be the number of partitions of $[n]$ into exactly $k$ blocks, the [Stirling number](/stirling-numbers/) of the second kind, and let $B_n = \sum_{k} S(n, k)$ be the Bell number. Then $B_0 = 1$ and

$$B_{n+1} = \sum_{j=0}^{n} C(n, j)\, B_j \qquad (n \ge 0).$$

*Proof.* In a partition of $[n + 1]$, the block of $n + 1$ is $\{n + 1\} \cup T$ for a set $T \subseteq [n]$. If $|T| = n - j$, there are $C(n, n - j) = C(n, j)$ choices of $T$, and the other blocks form a partition of the $j$ elements left, in $B_j$ ways. $\square$

**Growth.** $2^{n-1} \le B_n \le n!$ for $n \ge 1$, and $B_n$ grows faster than $c^n$ for each constant $c$.

- *Lower bound.* For $i \ge 1$, each partition of $[i]$ gives two partitions of $[i + 1]$: one with the new block $\{i + 1\}$ and one with $i + 1$ added to the block of $1$. These are all different, so $B_{i+1} \ge 2 B_i$.
- *Upper bound.* Write each block as a cycle with its elements in increasing order. Different partitions give different [permutations](/permutation/), so $B_n \le n!$.
- *Faster than exponential.* $k!\, S(n, k)$ counts the maps from $[n]$ onto $[k]$. At most $k (k-1)^n$ maps from $[n]$ to $[k]$ miss a value, so $B_n \ge S(n, k) \ge (k^n - k (k-1)^n)/k!$, which is about $k^n / k!$ for a fixed $k$ and large $n$.

**Generating function.** $\sum_{n \ge 0} B_n \frac{x^n}{n!} = \exp(e^x - 1)$, because a set partition is a set of nonempty blocks, and the [exponential generating function](/exponential-generating-functions/) of one nonempty block is $e^x - 1$ (Flajolet and Sedgewick, Chapter II).

## Variants

- **Exactly $k$ blocks.** List the $S(n, k)$ partitions with $k$ blocks.
- **Block sizes.** Blocks of size at most $b$, or of sizes in a set; with all sizes $2$ these are the perfect matchings of $[n]$.
- **Non-crossing partitions.** No $a < b < c < d$ with $a, c$ in one block and $b, d$ in another. There are $C_n$ of them, the [Catalan number](/catalan-numbers/).
- **Order.** Lexicographic order of the restricted growth strings, or a Gray code in which one element changes block at each step.
- **Counting, ranking and sampling.** Count $B_n$ or $S(n, k)$, rank or unrank a partition in a fixed order, or draw a uniform random partition, without the list. See [counting set partitions](/counting-set-partitions/).
- **Multisets.** Partitions of a multiset, such as $\{1, 1, 2, 3\}$. With all elements equal these are the [integer partitions](/integer-partitions/).

## Examples

**$n = 3$.** The $B_3 = 5$ partitions are $\{1, 2, 3\}$; $\{1, 2\}, \{3\}$; $\{1, 3\}, \{2\}$; $\{1\}, \{2, 3\}$; and $\{1\}, \{2\}, \{3\}$. By number of blocks this is $S(3, 1) = 1$, $S(3, 2) = 3$ and $S(3, 3) = 1$.

**$n = 4$.** There are $15$ partitions: $1$ with one block, $7$ with two, $6$ with three and $1$ with four. The seven with two blocks are $\{1,2,3\}\{4\}$, $\{1,2,4\}\{3\}$, $\{1,3,4\}\{2\}$, $\{2,3,4\}\{1\}$, $\{1,2\}\{3,4\}$, $\{1,3\}\{2,4\}$ and $\{1,4\}\{2,3\}$, which is $2^{3} - 1$. The partition $\{1, 4\}, \{2, 3\}$ has restricted growth string $0110$.

**Bell numbers.** For $n = 0, \ldots, 12$, $B_n$ is

$$1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975, 678570, 4213597.$$

The recurrence gives $B_5 = 1 \cdot 1 + 4 \cdot 1 + 6 \cdot 2 + 4 \cdot 5 + 1 \cdot 15 = 52$.

**Non-examples.** $\{\{1, 2\}, \{2, 3\}\}$ is not a partition of $[3]$, because the blocks overlap. $\{\{1, 2\}, \emptyset, \{3\}\}$ is not one either, because a block is empty. $\{\{1\}, \{3\}\}$ is a partition of $\{1, 3\}$ but not of $[3]$, because $2$ is in no block.

## Known algorithms

| method | order | time for each partition | notes |
| --- | --- | --- | --- |
| [Algorithm H](/set-partition-generation/) | lexicographic order of the RGS | $O(1)$ amortized, CAT | the standard choice |
| Insertion of $n$ | recursive, by blocks | $O(1)$ amortized | add $n$ to each block or as a new block |
| Gray codes for RGS | one entry changes | see Knuth | Knuth, Section 7.2.1.5 |
| NEXEQU (Nijenhuis and Wilf) | their order | see Chapter 11 | a successor routine for equivalence relations |
| Unrank with counts of completions | any rank | $O(n)$ big integer steps | random access, uniform sampling |

All of these change the current partition in place. Copying each partition out costs $\Theta(n)$, so a full list of copies costs $\Theta(n B_n)$.

## Bounds

- **Output.** Each method visits $N = B_n$ partitions, so it needs $\Omega(B_n)$ time. Algorithm H meets this bound, since the scans of all steps add up to $\sum_{i=1}^{n-1} B_i < B_n$.
- **Copies.** Writing each partition in full, as $n$ labels or as $n$ elements in blocks, costs $\Theta(n B_n)$ in total.
- **Counting.** The triangle of $S(n, k)$ gives $B_0, \ldots, B_n$ in $O(n^2)$ big integer additions. The numbers are exact big integers: since $2^{n-1} \le B_n \le n!$, $B_n$ has between $n - 1$ and $O(n \log n)$ bits.

## Reductions

- **Restricted growth strings.** The partitions of $[n]$ are in bijection with the [restricted growth strings](/restricted-growth-string/) of length $n$, so the problem is to list those strings.
- **Equivalence relations.** A partition of $[n]$ is the set of classes of exactly one equivalence relation on $[n]$.
- **Surjections.** The maps from $[n]$ onto $[k]$ are the partitions into $k$ blocks with the blocks numbered, so there are $k!\, S(n, k)$ of them. A list of partitions with $k$ blocks and a list of the $k!$ [permutations](/next-permutation/) give all surjections.
- **Integer partitions.** The block sizes of a set partition of $[n]$, sorted, form an [integer partition](/integer-partitions/) of $n$, its type. For a fixed type with $m_j$ blocks of size $j$, there are $n! / \prod_j (j!)^{m_j} m_j!$ set partitions.
- **Factorizations.** A squarefree integer with $n$ prime factors has $B_n$ factorizations into factors greater than $1$, ignoring order, one for each partition of its prime factors.

## Applications

- **Search without symmetry.** In graph coloring, bin packing with identical bins and clustering, the names of the colors, bins or clusters do not matter. A search over restricted growth strings visits each grouping once instead of $k!$ times.
- **Rhyme schemes.** The rhyme schemes of a poem with $n$ lines, such as $abab$ or $aabb$, are the restricted growth strings of length $n$ written with letters.
- **Probability and statistics.** The moment-cumulant formulas sum over the set partitions of $[n]$, with signs from the Möbius function of the [partition lattice](/partition-lattice/).
- **Testing.** Exhaustive tests of union-find structures and of equivalence checks run over all partitions of a small set.

## References
