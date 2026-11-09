---
tag: H4RVSK
kind: definition
slug: ferrers-diagram
name: Ferrers diagram
aliases:
- Young diagram
- Ferrers graph
- Ferrers board
area: combinatorics/generating-partitions-and-trees
level: intro
summary: A left-justified array of boxes whose row lengths form a partition; it gives a visual model of partitions.
prereqs: [integer-partitions]
see_also: [conjugate-partition, durfee-square, young-tableau, youngs-lattice, euler-partition-theorem, hook-length-formula, integer-partition-function]
sources:
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 1, The elementary theory of partitions, pages 1 to 15 (graphical representation of partitions and conjugation)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.4, Generating all partitions (Ferrers diagrams, conjugate partitions and the Durfee square)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.8, Partition identities (the Ferrers diagram and the conjugate of a partition)
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Chapter 7, Symmetric functions (Young diagrams, hooks and the hook length formula, Corollary 7.21.6)
---

A Ferrers diagram is the picture of an [integer partition](/integer-partitions/) $\lambda = (\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_\ell)$: row $i$ holds $\lambda_i$ boxes (or dots), and all rows start at the same left edge. The map from a partition to its diagram is a bijection, so a statement about partitions can be proved by a cut, a flip or a slide of the diagram. The [conjugate partition](/conjugate-partition/), the [Durfee square](/durfee-square/), the hooks of the [hook length formula](/hook-length-formula/) and the shapes of [Young tableaux](/young-tableau/) are all read off this picture.

## Definition

**Notation.** In this page $n \ge 0$ is the integer that is partitioned, and $\ell$ is the number of parts. A *partition* of $n$ is a finite sequence of integers $\lambda = (\lambda_1, \ldots, \lambda_\ell)$ with $\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_\ell \ge 1$ and $|\lambda| = \lambda_1 + \cdots + \lambda_\ell = n$. The length is $\ell(\lambda) = \ell$. The empty sequence is the only partition of $0$. It is convenient to set $\lambda_i = 0$ for $i > \ell$.

**Ferrers diagram.** The Ferrers diagram of $\lambda$ is the finite set of cells

$$D(\lambda) = \{(i, j) \in \mathbb{Z}^2 : 1 \le i \le \ell(\lambda),\ 1 \le j \le \lambda_i\}.$$

Cell $(i, j)$ is in row $i$ and column $j$. It has $|D(\lambda)| = n$ cells. A drawing puts a box (Young's picture) or a dot (Ferrers's picture) at each cell.

**Conventions.** This page uses the English convention: row $1$ is on top, and rows go down. The French convention puts row $1$ at the bottom, so the picture is the English one turned upside down. The Russian convention turns the French picture by $45$ degrees. All three draw the same set $D(\lambda)$.

**Characterization.** A finite set $D \subset \mathbb{Z}_{>0}^2$ is the Ferrers diagram of a partition if and only if it is closed toward the corner: for each $(i, j) \in D$ and each $1 \le i' \le i$, $1 \le j' \le j$, the cell $(i', j')$ is also in $D$.

*Proof.* If $D = D(\lambda)$ and $(i, j) \in D$, take $i' \le i$ and $j' \le j$. Then $i' \le i \le \ell$ and $j' \le j \le \lambda_i \le \lambda_{i'}$, so $(i', j') \in D$. Conversely, let $D$ be finite and closed toward the corner. Let $\lambda_i$ be the number of cells of $D$ in row $i$. Row $i$ holds $(i, j)$ only if it holds $(i, 1), \ldots, (i, j)$, so row $i$ is exactly $\{(i, 1), \ldots, (i, \lambda_i)\}$. If $(i + 1, j) \in D$ then $(i, j) \in D$, so $\lambda_{i+1} \le \lambda_i$. The sequence of the nonzero $\lambda_i$ is therefore a partition, and $D$ is its diagram. The two maps are inverse to each other, so $\lambda \mapsto D(\lambda)$ is a bijection from the partitions of $n$ to the closed sets of $n$ cells. $\square$

**Parts of the picture.** For a cell $(i, j) \in D(\lambda)$, and with $\lambda'$ the [conjugate](/conjugate-partition/) of $\lambda$:

- the *arm* is $a(i, j) = \lambda_i - j$, the number of cells to its right;
- the *leg* is $l(i, j) = \lambda'_j - i$, the number of cells below it;
- the *hook length* is $h(i, j) = a(i, j) + l(i, j) + 1$;
- the cell is a *corner* (a removable cell) when $a(i, j) = l(i, j) = 0$, so $D(\lambda) \setminus \{(i, j)\}$ is again a Ferrers diagram;
- the [Durfee square](/durfee-square/) is the largest square $\{1, \ldots, d\}^2$ inside $D(\lambda)$.

**Containment and skew shapes.** For two partitions, $\mu \subseteq \lambda$ means $D(\mu) \subseteq D(\lambda)$, that is $\mu_i \le \lambda_i$ for each $i$. The set difference $D(\lambda) \setminus D(\mu)$ is the *skew diagram* $\lambda / \mu$. Containment is the order of [Young's lattice](/youngs-lattice/).

## Examples and non-examples

**A diagram.** The partition $\lambda = (4, 3, 1)$ of $8$ has this diagram (English convention):

```
□ □ □ □
□ □ □
□
```

Its columns have lengths $3, 2, 2, 1$, so its conjugate is $(3, 2, 2, 1)$. Its Durfee square has side $2$, because $\lambda_2 = 3 \ge 2$ but $\lambda_3 = 1 < 3$. Its corners are $(1, 4)$, $(2, 3)$ and $(3, 1)$. The hook lengths, row by row, are

```
6 4 3 1
4 2 1
1
```

Their product is $576$, and the hook length formula gives $8!/576 = 70$ standard Young tableaux of this shape.

**Proof by transpose.** Turning the diagram over its main diagonal swaps rows and columns. So the partitions of $n$ with at most $k$ parts are as many as the partitions of $n$ with each part at most $k$. For $n = 8$ and $k = 3$ there are $10$ of each, and $5$ partitions of $8$ have exactly $3$ parts, as many as have largest part $3$.

**Partitions of 4.** The five partitions $(4)$, $(3, 1)$, $(2, 2)$, $(2, 1, 1)$, $(1, 1, 1, 1)$ have five diagrams. The diagrams of $(4)$ and $(1, 1, 1, 1)$ are transposes of each other, and so are those of $(3, 1)$ and $(2, 1, 1)$. The square $(2, 2)$ is its own transpose.

**Non-examples.**

- The set with rows of lengths $2$ and $3$, in that order, is not a Ferrers diagram. The cell $(2, 3)$ is in the set but $(1, 3)$ is not, so the set is not closed toward the corner. Its row lengths form the [composition](/integer-compositions/) $(2, 3)$, which has no Ferrers diagram.
- The set $\{(1, 1), (1, 3)\}$ is not a Ferrers diagram: it has a gap in row $1$.
- A skew diagram such as $(4, 3, 1)/(2, 1)$ is not a Ferrers diagram, because it does not hold the cell $(1, 1)$.

## Related definitions

- [Integer partitions](/integer-partitions/): the objects that the diagrams draw. Their number is the [partition function](/integer-partition-function/) $p(n)$.
- [Conjugate partition](/conjugate-partition/): the partition of the transposed diagram.
- [Durfee square](/durfee-square/): the largest square in the diagram, the base of several partition identities.
- [Young tableau](/young-tableau/): a filling of the cells of a diagram with numbers that increase along rows and down columns.
- [Young's lattice](/youngs-lattice/): all diagrams, ordered by containment.
- [Hook length formula](/hook-length-formula/): the number of standard Young tableaux of shape $\lambda$ is $n!$ divided by the product of the hook lengths.
- [Euler's partition theorem](/euler-partition-theorem/): one of the classic identities that a picture of the diagram proves.

## References
