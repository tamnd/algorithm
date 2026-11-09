---
tag: ACW188
kind: definition
slug: young-tableau
name: Young tableau
aliases:
- Standard Young tableau
- SYT
- Semistandard Young tableau
- Young tableaux
area: combinatorics/generating-partitions-and-trees
level: core
summary: A filling of the Ferrers diagram of a partition with positive integers that increase along rows and down columns; it is standard when the entries are exactly 1 to n, each used once.
prereqs: [ferrers-diagram, integer-partitions]
see_also: [standard-young-tableaux, youngs-lattice, hook-length-formula, counting-standard-young-tableaux, generating-involutions, longest-increasing-subsequence, conjugate-partition, catalan-numbers]
sources:
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Section 7.10, The combinatorial definition of Schur functions (semistandard and standard tableaux), and Corollary 7.21.6 (the hook length formula)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition, Addison-Wesley, 1998
    locator: Section 5.1.4, Tableaux and involutions
  - book: isbn:9780387950679
    title: Bruce E. Sagan, The Symmetric Group, second edition, Springer, 2001
    locator: Chapter 2 (Young tableaux and Specht modules) and Chapter 3 (the Robinson-Schensted algorithm and the hook formula)
  - book: isbn:9780521567244
    title: William Fulton, Young Tableaux, Cambridge University Press, 1997
    locator: Chapter 1, Bumping and sliding (definitions of tableaux and the row bumping algorithm)
  - paper: doi:10.4153/CJM-1954-030-1
    title: J. S. Frame, G. de B. Robinson and R. M. Thrall, The hook graphs of the symmetric group, Canadian Journal of Mathematics 6 (1954), 316-324
    locator: the hook length formula for the number of standard tableaux of a shape
---

A Young tableau of shape $\lambda$ is a filling of the [Ferrers diagram](/ferrers-diagram/) of the partition $\lambda$ with positive integers, so that the entries increase along each row and down each column. It is standard when the entries are exactly $1, \ldots, n$, each used once, and semistandard when rows only weakly increase and repeated entries are allowed. The number $f^\lambda$ of standard tableaux of shape $\lambda$ is given by the hook length formula, and the squares of these numbers sum to $n!$, which makes tableaux the standard way to index permutations, involutions and the irreducible representations of the symmetric group.

## Definition

**Notation.** $\lambda = (\lambda_1 \ge \cdots \ge \lambda_\ell \ge 1)$ is a [partition](/integer-partitions/) of $n = |\lambda|$. Its diagram is $D(\lambda) = \{(i, j) : 1 \le i \le \ell,\ 1 \le j \le \lambda_i\}$, drawn in English notation: row $1$ at the top, rows left-justified. The cell $(i, j)$ is in row $i$ and column $j$. $\lambda'$ is the [conjugate partition](/conjugate-partition/).

**Standard Young tableau.** A standard Young tableau (SYT) of shape $\lambda$ is a bijection $T : D(\lambda) \to [n]$ such that

- $T(i, j) < T(i, j + 1)$ whenever both cells are in $D(\lambda)$ (rows increase), and
- $T(i, j) < T(i + 1, j)$ whenever both cells are in $D(\lambda)$ (columns increase).

We write $f^\lambda$ for the number of SYT of shape $\lambda$, and $\mathrm{SYT}(\lambda)$ for their set.

**Semistandard Young tableau.** A semistandard Young tableau (SSYT) of shape $\lambda$ is a map $T : D(\lambda) \to \{1, 2, \ldots\}$ with $T(i, j) \le T(i, j + 1)$ along rows and $T(i, j) < T(i + 1, j)$ down columns. Its content is $\mu = (\mu_1, \mu_2, \ldots)$, where $\mu_k$ is the number of entries equal to $k$. An SSYT with content $(1, 1, \ldots, 1)$ is an SYT. Some authors use "Young tableau" for the SSYT and some for the SYT; this page states which one it means each time.

**Three equal views of an SYT.** For a shape $\lambda \vdash n$ the following sets are in bijection.

1. The SYT of shape $\lambda$.
2. The chains $\varnothing = \lambda^{(0)} \subset \lambda^{(1)} \subset \cdots \subset \lambda^{(n)} = \lambda$ of partitions with $|\lambda^{(k)}| = k$, which are the saturated chains from $\varnothing$ to $\lambda$ in [Young's lattice](/youngs-lattice/).
3. The ballot sequences (lattice words) $r_1 \ldots r_n$ with $\lambda_i$ letters equal to $i$, such that every prefix has at least as many letters $i$ as letters $i + 1$, for each $i$.

*Proof.* Given $T$, let $\lambda^{(k)}$ be the set of cells with entries at most $k$, and let $r_k$ be the row of the entry $k$. The set $\lambda^{(k)}$ is the diagram of a partition exactly when it is closed to the left and upward, which is what the row and column conditions say for each $k$. Adding the cell of $k$ in row $r_k$ keeps a partition shape exactly when row $r_k$ is shorter than row $r_k - 1$ before the step, which is the ballot condition. Each view determines $T$, since the cell of $k$ is the one cell of $\lambda^{(k)} \setminus \lambda^{(k-1)}$, the last cell of row $r_k$. $\square$

**Corners.** A corner of $\lambda$ is a cell $(i, \lambda_i)$ with $\lambda_{i+1} < \lambda_i$. In an SYT, the entry $n$ is in a corner, and removing it leaves an SYT of the smaller shape. So

$$f^\varnothing = 1, \qquad f^\lambda = \sum_{\text{corners } c} f^{\lambda \setminus c}.$$

**Hook length formula.** The hook of a cell $u = (i, j)$ is the cell, the cells to its right in row $i$ and the cells below it in column $j$. Its length is $h(u) = \lambda_i - j + \lambda'_j - i + 1$. Frame, Robinson and Thrall proved

$$f^\lambda = \frac{n!}{\prod_{u \in D(\lambda)} h(u)}.$$

See the [hook length formula](/hook-length-formula/) for proofs, and [counting standard Young tableaux](/counting-standard-young-tableaux/) for algorithms.

**Sums over shapes.** By the Robinson-Schensted correspondence, the permutations of $[n]$ are in bijection with the pairs $(P, Q)$ of SYT of the same shape, and $P = Q$ exactly for the involutions. So

$$\sum_{\lambda \vdash n} (f^\lambda)^2 = n!, \qquad \sum_{\lambda \vdash n} f^\lambda = \#\{\text{involutions of } [n]\}.$$

The first row length $\lambda_1$ of the common shape is the length of a [longest increasing subsequence](/longest-increasing-subsequence/) of the permutation (Schensted). Knuth Section 5.1.4 gives the proofs.

**Transpose.** Reflecting an SYT of shape $\lambda$ in its main diagonal gives an SYT of shape $\lambda'$, so $f^{\lambda'} = f^\lambda$.

## Examples and non-examples

**All SYT for $n = 3$.** Shape $(3)$: $123$. Shape $(1, 1, 1)$: one column $1, 2, 3$. Shape $(2, 1)$: two tableaux,

$$\begin{array}{cc} 1 & 2 \\ 3 & \end{array} \qquad \begin{array}{cc} 1 & 3 \\ 2 & \end{array}$$

with ballot sequences $112$ and $121$. So $f^{(3)} + f^{(2,1)} + f^{(1,1,1)} = 4$, the number of involutions of $[3]$, and $1 + 4 + 1 = 6 = 3!$.

**Shape $(3, 2)$.** The five SYT, by rows, are $135/24$, $125/34$, $134/25$, $124/35$ and $123/45$. The hook lengths are $4, 3, 1$ in row $1$ and $2, 1$ in row $2$, so $f^{(3,2)} = 120 / 24 = 5$.

**Shape $(4, 3, 1)$.** The hook lengths are

$$\begin{array}{cccc} 6 & 4 & 3 & 1 \\ 4 & 2 & 1 & \\ 1 & & & \end{array}$$

with product $576$, so $f^{(4,3,1)} = 8! / 576 = 40320 / 576 = 70$.

**Counts for $n = 5$.** $f^\lambda$ for $\lambda = (5), (4,1), (3,2), (3,1,1), (2,2,1), (2,1,1,1), (1^5)$ is $1, 4, 5, 6, 5, 4, 1$. The sum is $26$, the number of involutions of $[5]$, and the sum of squares is $1 + 16 + 25 + 36 + 25 + 16 + 1 = 120 = 5!$.

**Two rows of equal length.** $f^{(k,k)}$ is the Catalan number $C(2k, k)/(k + 1)$: the ballot sequence of an SYT of shape $(k, k)$ is a [Dyck word](/dyck-word/) with $1$ for an up step and $2$ for a down step. For $k = 1, \ldots, 7$ the values are $1, 2, 5, 14, 42, 132, 429$.

**A semistandard tableau.** The filling $112/23$ of shape $(3, 2)$ is an SSYT with content $(2, 2, 1)$: rows $1 \le 1 \le 2$ and $2 \le 3$ weakly increase, and columns $1 < 2$, $1 < 3$ strictly increase. It is not standard, since $1$ and $2$ repeat. The number of SSYT of shape $(2, 1)$ with entries in $\{1, 2, 3\}$ is $8$.

**Non-example: a column fails.** The filling $14/23$ of shape $(2, 2)$ has increasing rows $1 < 4$ and $2 < 3$, but column $2$ reads $4$ over $3$, so it is not an SYT. The two SYT of shape $(2, 2)$ are $12/34$ and $13/24$.

**Non-example: not a partition shape.** A filling of the cells $\{(1, 1), (2, 1), (2, 2)\}$, with a longer second row, is not a Young tableau, since the cells do not form a Ferrers diagram. Fillings of a difference $\lambda / \mu$ of two diagrams are called skew tableaux.

## Related definitions

- [Ferrers diagram](/ferrers-diagram/), [integer partitions](/integer-partitions/) and the [conjugate partition](/conjugate-partition/) give the shapes.
- [Young's lattice](/youngs-lattice/): an SYT of shape $\lambda$ is a saturated chain from $\varnothing$ to $\lambda$.
- [Standard Young tableaux enumeration](/standard-young-tableaux/) is the problem of listing all SYT of a shape or of a size.
- The [hook length formula](/hook-length-formula/) and [counting standard Young tableaux](/counting-standard-young-tableaux/) give $f^\lambda$.
- [Generating involutions](/generating-involutions/) lists the objects that are in bijection with all SYT of size $n$.
- The [Catalan numbers](/catalan-numbers/) and the [ballot theorem](/ballot-theorem/) count the two-row case.
- The Robinson-Schensted correspondence links tableaux to the [longest increasing subsequence](/longest-increasing-subsequence/) and to [patience sorting](/patience-sorting/).

## References
