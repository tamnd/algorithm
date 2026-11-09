---
tag: 56BVQA
kind: definition
slug: conjugate-partition
name: Conjugate partition
aliases:
- Transpose partition
- Transposed partition
area: combinatorics/generating-partitions-and-trees
level: core
summary: The partition obtained by reflecting the Ferrers diagram, swapping rows and columns.
prereqs: [ferrers-diagram]
see_also: [integer-partitions, durfee-square, euler-partition-theorem, young-tableau, youngs-lattice, integer-partition-generation]
sources:
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 1, The elementary theory of partitions, pages 1 to 15 (conjugate partitions and their use in partition identities)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.8, Partition identities (the conjugate partition and self-conjugate partitions)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.4, Generating all partitions (Ferrers diagrams and conjugate partitions, and the exercises on computing a conjugate)
---

The conjugate of a [partition](/integer-partitions/) $\lambda$ is the partition $\lambda'$ whose [Ferrers diagram](/ferrers-diagram/) is the diagram of $\lambda$ reflected in its main diagonal, so the rows of one are the columns of the other. Part $j$ of $\lambda'$ is the number of parts of $\lambda$ that are at least $j$. Conjugation is a bijection from the partitions of $n$ to themselves, and it is its own inverse. It turns "at most $k$ parts" into "each part at most $k$", and it is the first tool for proofs of partition identities by pictures.

## Definition

**Notation.** A partition of $n \ge 0$ is $\lambda = (\lambda_1 \ge \cdots \ge \lambda_\ell \ge 1)$ with $|\lambda| = n$ and length $\ell(\lambda) = \ell$. We set $\lambda_i = 0$ for $i > \ell$. The empty partition $()$ has $\ell = 0$ and $\lambda_1 = 0$.

**Conjugate.** The conjugate of $\lambda$ is $\lambda' = (\lambda'_1, \ldots, \lambda'_{\lambda_1})$ with

$$\lambda'_j = |\{\, i : \lambda_i \ge j \,\}| \qquad (1 \le j \le \lambda_1).$$

Equivalently, $\lambda'_j$ is the length of column $j$ of the Ferrers diagram $D(\lambda)$, and

$$D(\lambda') = \{(j, i) : (i, j) \in D(\lambda)\}.$$

**Why the two forms agree.** Column $j$ of $D(\lambda)$ is the set of cells $(i, j)$ with $j \le \lambda_i$, so it has $\lambda'_j$ cells. Since $\lambda$ is non-increasing, these are the cells with $i = 1, \ldots, \lambda'_j$. So the transposed set is $\{(j, i) : 1 \le i \le \lambda'_j\}$, which is the diagram of $\lambda'$ by definition.

**Basic facts.** For each partition $\lambda$:

1. $\lambda'$ is a partition of $|\lambda|$. *Proof.* If $j < j'$ then each $i$ with $\lambda_i \ge j'$ also has $\lambda_i \ge j$, so $\lambda'_j \ge \lambda'_{j'}$. Each $\lambda'_j \ge 1$ for $j \le \lambda_1$, because $\lambda_1 \ge j$. The sum $\sum_j \lambda'_j$ counts the cells of $D(\lambda)$ by columns, so it is $|\lambda|$.
2. $\ell(\lambda') = \lambda_1$ and $\lambda'_1 = \ell(\lambda)$. *Proof.* The first holds by definition. For the second, every part is at least $1$, so $\lambda'_1 = \ell$.
3. $(\lambda')' = \lambda$. *Proof.* Transposing a set of cells twice gives the set back, and a Ferrers diagram fixes its partition.

So conjugation is an involution on the set of partitions of $n$. A partition with $\lambda' = \lambda$ is *self-conjugate*.

**In multiplicity form.** If $\lambda$ has distinct part sizes $v_1 > v_2 > \cdots > v_t$ with multiplicities $c_1, \ldots, c_t$, then $\lambda'$ has the part sizes $c_1 + \cdots + c_s$ with multiplicities $v_s - v_{s+1}$, for $s = 1, \ldots, t$, with $v_{t+1} = 0$. Each column of the diagram between $v_{s+1} + 1$ and $v_s$ has the same length $c_1 + \cdots + c_s$.

**Computation.** Given $\lambda$ as an array, $\lambda'$ takes $O(\lambda_1 + \ell)$ time: walk $j$ from $1$ to $\lambda_1$, and keep a pointer $i$ that moves down from $\ell$ while $\lambda_i < j$. The pointer moves at most $\ell$ times in total, and $\lambda'_j$ is its value. This is optimal up to a constant, since $\lambda'$ has $\lambda_1$ entries and $\lambda$ has $\ell$.

## Examples and non-examples

**A conjugate.** For $\lambda = (4, 3, 1)$,

```
□ □ □ □        □ □ □
□ □ □          □ □
□              □ □
               □
```

The left picture is $D(4, 3, 1)$ and the right one is its transpose, $D(3, 2, 2, 1)$. The parts of $\lambda$ that are at least $1, 2, 3, 4$ number $3, 2, 2, 1$. So $(4, 3, 1)' = (3, 2, 2, 1)$, and both have length and largest part swapped: $\ell = 3$, $\lambda_1 = 4$ against $\ell = 4$, $\lambda'_1 = 3$.

**Multiplicity form.** $\lambda = (5, 5, 3, 1) = 5^2\, 3^1\, 1^1$. The sizes $5, 3, 1$ have multiplicities $2, 1, 1$, so $\lambda'$ has parts $2$, $3$, $4$ with multiplicities $5 - 3 = 2$, $3 - 1 = 2$, $1 - 0 = 1$. That is $\lambda' = (4, 3, 3, 2, 2)$.

**At most $k$ parts.** Conjugation maps the partitions of $n$ with at most $k$ parts onto the partitions with largest part at most $k$, by fact 2. For $n = 8$ and $k = 3$ both sets have $10$ elements. So the count of partitions into at most $k$ parts is also the count of partitions into parts of size at most $k$, the [coin change count](/coin-change-counting/) with coins $1, \ldots, k$.

**Self-conjugate partitions.** The self-conjugate partitions of $8$ are $(4, 2, 1, 1)$ and $(3, 3, 2)$. For $n = 0, 1, \ldots, 15$ their numbers are

$$1, 1, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4.$$

These are also the numbers of partitions of $n$ into distinct odd parts. *Proof.* Let $\lambda = \lambda'$ have a [Durfee square](/durfee-square/) of side $d$. For $i = 1, \ldots, d$, the hook of cell $(i, i)$, made of the cell, its arm and its leg, has $(\lambda_i - i) + (\lambda'_i - i) + 1 = 2(\lambda_i - i) + 1$ cells, which is odd. These $d$ hooks cover the diagram without overlap, and their lengths strictly decrease, since $\lambda_i - i > \lambda_{i+1} - (i + 1)$. So they form a partition of $n$ into distinct odd parts. Conversely, nest $d$ distinct odd hooks $2h_1 + 1 > \cdots > 2h_d + 1$ on the diagonal, each with arm and leg $h_i$; the result is a self-conjugate diagram. The two maps are inverse. $\square$ For $(4, 2, 1, 1)$ the diagonal hooks have lengths $7, 1$, and for $(3, 3, 2)$ they are $5, 3$.

**Non-examples.**

- The reverse $(1, 3, 4)$ of $(4, 3, 1)$ is not its conjugate. It is not even a partition, since its parts increase.
- The complement of $D(\lambda)$ in a box is not the conjugate. In the $3 \times 4$ box, the complement of $D(4, 3, 1)$ has $4$ cells, so it cannot be the diagram of a partition of $8$.
- $(3, 2, 2, 1)$ is not self-conjugate: its conjugate is $(4, 3, 1)$.

## Related definitions

- [Ferrers diagram](/ferrers-diagram/): the picture that conjugation reflects.
- [Durfee square](/durfee-square/): the largest square in the diagram. A partition and its conjugate have the same Durfee square.
- [Euler's partition theorem](/euler-partition-theorem/): distinct parts against odd parts. The self-conjugate count above is a close relative.
- [Young tableau](/young-tableau/): transposing a standard Young tableau of shape $\lambda$ gives one of shape $\lambda'$, so both shapes have the same number of tableaux.
- [Young's lattice](/youngs-lattice/): conjugation is an automorphism of the containment order, since $\mu \subseteq \lambda$ if and only if $\mu' \subseteq \lambda'$.
- [Integer partition generation](/integer-partition-generation/): a generator for partitions with bounded length gives, through conjugates, the partitions with bounded parts.

## References
