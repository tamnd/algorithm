---
tag: FSB95K
kind: definition
slug: rank
name: Rank
aliases: [matrix rank, column rank, row rank]
area: algebra/exact-linear-algebra
level: intro
summary: Dimension of the column space of a matrix.
prereqs: [linear-independence]
see_also: [rank-nullity-theorem, nullspace, echelon-form, pivot, determinant, rank-computation, tensor-rank]
sources:
  - book: isbn:9783319110790
    title: Sheldon Axler, Linear Algebra Done Right, third edition, Springer, 2015
    locator: Section 3.B, Null Spaces and Ranges, and Section 3.F, Duality (column rank equals row rank)
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition, Prentice Hall, 1971
    locator: Section 3.1, Linear Transformations (rank and the rank theorem), and Section 3.7, The Transpose of a Linear Transformation (row rank equals column rank)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 0.4, Rank (rank by minors, rank of products and the full rank factorization)
---

The *rank* of an $m \times n$ matrix $A$ over a field $K$ is the dimension of its column space, the subspace of $K^m$ spanned by its columns. It is also the largest number of [linearly independent](/linear-independence/) columns, the largest number of independent rows, the number of [pivots](/pivot/) of an [echelon form](/echelon-form/) of $A$, and the size of the largest square submatrix with a nonzero [determinant](/determinant/). For a matrix over $\mathbb{Z}$ the rank is taken over $\mathbb{Q}$, and the rank of its image modulo a prime $p$ can be smaller.

## Definition

**Notation.** $K$ is a field, $R$ is an integral domain with field of fractions $K$, and $A$ is an $m \times n$ matrix over $K$ with columns $a_1, \ldots, a_n \in K^m$. A *minor of order $s$* of $A$ is the determinant of the $s \times s$ submatrix in some $s$ rows and $s$ columns.

The column space of $A$ is

$$\operatorname{col}(A) = \{ A x : x \in K^n \} = \{ x_1 a_1 + \cdots + x_n a_n : x_i \in K \},$$

a subspace of $K^m$. The **rank** of $A$ is

$$\operatorname{rank}(A) = \dim \operatorname{col}(A).$$

The matrix has **full rank** when $\operatorname{rank}(A) = \min(m, n)$, full column rank when the rank is $n$, and full row rank when it is $m$. For a matrix over an integral domain $R$, the rank is the rank over $K$. The following facts hold for every $m \times n$ matrix over $K$, including the cases $m = 0$ or $n = 0$, where the rank is $0$.

**Fact 1 (independent columns).** $\operatorname{rank}(A)$ is the largest number of linearly independent columns of $A$. *Proof.* Take a set of columns that is independent and that stays independent with no other column added. Each other column is then a combination of the chosen ones, so the chosen columns span $\operatorname{col}(A)$ and form a basis. Every independent set of columns lies in $\operatorname{col}(A)$, so it has at most $\dim \operatorname{col}(A)$ members. $\square$

**Fact 2 (bounds).** $0 \le \operatorname{rank}(A) \le \min(m, n)$, since $\operatorname{col}(A) \subseteq K^m$ and it is spanned by $n$ vectors.

**Fact 3 (row rank equals column rank).** $\operatorname{rank}(A^T) = \operatorname{rank}(A)$. *Proof.* Let $r = \operatorname{rank}(A)$ and let $b_1, \ldots, b_r$ be a basis of $\operatorname{col}(A)$. Write $a_j = \sum_k c_{kj} b_k$. With $B = (b_1, \ldots, b_r)$ of size $m \times r$ and $C = (c_{kj})$ of size $r \times n$, this is $A = B C$. Row $i$ of $A$ is $\sum_k B_{ik} \cdot (\text{row } k \text{ of } C)$, so the $r$ rows of $C$ span the row space of $A$, and $\operatorname{rank}(A^T) \le r$. The same argument on $A^T$ gives the other inequality. $\square$ The factorization $A = B C$ with inner size $r$ is a *full rank factorization*, and no factorization with a smaller inner size exists.

**Fact 4 (products).** $\operatorname{rank}(A B) \le \min(\operatorname{rank}(A), \operatorname{rank}(B))$, and $\operatorname{rank}(P A Q) = \operatorname{rank}(A)$ for invertible $P$ and $Q$. *Proof.* Each column of $AB$ is $A$ times a column of $B$, so $\operatorname{col}(AB) \subseteq \operatorname{col}(A)$. By Fact 3, $\operatorname{rank}(AB) = \operatorname{rank}(B^T A^T) \le \operatorname{rank}(B^T) = \operatorname{rank}(B)$. For invertible $P$, $\operatorname{rank}(PA) \le \operatorname{rank}(A) = \operatorname{rank}(P^{-1} P A) \le \operatorname{rank}(PA)$, and the same holds on the right. $\square$

**Fact 5 (echelon form).** Row operations multiply $A$ by an invertible matrix on the left, so by Fact 4 they keep the rank. In an echelon form $E$ with nonzero rows $E_1, \ldots, E_k$ and pivot columns $p_1 < \cdots < p_k$, the nonzero rows are independent: in $c_1 E_1 + \cdots + c_k E_k = 0$, column $p_1$ is nonzero only in $E_1$, so $c_1 = 0$, then column $p_2$ gives $c_2 = 0$, and so on. They span the row space, so $\operatorname{rank}(A) = \operatorname{rank}(E) = k$, the number of pivots. This is how [Gaussian elimination](/gaussian-elimination/) computes the rank.

**Fact 6 (minors).** $\operatorname{rank}(A)$ is the largest $s$ such that $A$ has a nonzero minor of order $s$. *Proof.* Let $r = \operatorname{rank}(A)$. Take $r$ independent columns (Fact 1). The $m \times r$ matrix $C$ they form has rank $r$, so by Fact 3 it has $r$ independent rows, and these give an invertible $r \times r$ submatrix of $A$, with nonzero determinant. Conversely, if the submatrix $S$ in rows $I$ and columns $J$ has $\det S \neq 0$, then a relation $\sum_{j \in J} x_j a_j = 0$ restricted to the rows $I$ is $S x = 0$, so $x = 0$. The columns in $J$ are independent, and $|J| \le r$ by Fact 1. $\square$

**Fact 7 (rank modulo a prime).** Let $A$ be an integer matrix of rank $r$ over $\mathbb{Q}$ and let $\bar A$ be its image over $\mathbb{Z}/p\mathbb{Z}$. Then $\operatorname{rank}(\bar A) \le r$, with equality if and only if $p$ does not divide every minor of order $r$ of $A$. *Proof.* A minor of $\bar A$ is the image of the same minor of $A$. All minors of $A$ of order $r + 1$ are zero, so the same holds for $\bar A$, and Fact 6 over $\mathbb{Z}/p\mathbb{Z}$ gives $\operatorname{rank}(\bar A) \le r$; equality holds exactly when some minor of order $r$ has a nonzero image. $\square$ So a rank computed modulo one random large prime is a lower bound that is correct with high probability, which is the base of modular rank algorithms in [rank computation](/rank-computation/).

## Examples and non-examples

**Identity and zero.** $I_n$ has rank $n$, and the zero matrix of each size has rank $0$. The $0 \times 0$ matrix has rank $0$ and is invertible, with determinant $1$.

**Rank one.** $\begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$ has rank $1$: its second column is twice the first. Every matrix of rank $1$ is $u v^T$ for nonzero vectors $u$ and $v$, by Fact 3 with $r = 1$.

**Full row rank.** $\begin{pmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \end{pmatrix}$ has rank $2 = \min(2, 3)$, although its third column is the sum of the first two.

**A $3 \times 3$ matrix of rank 2.** The matrix with rows $(1, 2, 3)$, $(4, 5, 6)$, $(7, 8, 9)$ has determinant $0$ and the minor $\det \begin{pmatrix} 1 & 2 \\ 4 & 5 \end{pmatrix} = -3 \neq 0$, so its rank is $2$ by Fact 6.

**The field matters.** $A = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$ has $\det A = -2$. Over $\mathbb{Q}$ its rank is $2$. Over $\mathbb{Z}/2\mathbb{Z}$, $-1 = 1$, both columns are $(1, 1)^T$, and the rank is $1$. By Fact 7, $p = 2$ is the only prime where the rank drops, because the only minor of order $2$ is $-2$.

**Non-example: the number of nonzero entries.** $\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ has four nonzero entries and rank $1$.

**Non-example: the number of nonzero rows.** $\begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$ has two nonzero rows and two nonzero columns, but rank $1$. The count of nonzero rows gives the rank only after elimination to an echelon form.

**Non-example: rank is not additive under sums.** $\operatorname{rank}(A + B) \le \operatorname{rank}(A) + \operatorname{rank}(B)$, since $\operatorname{col}(A + B) \subseteq \operatorname{col}(A) + \operatorname{col}(B)$, but the inequality can be strict: $A = I_2$ and $B = -I_2$ have rank $2$ each, and $A + B = 0$ has rank $0$.

## Related definitions

- [Linear independence](/linear-independence/): Fact 1 says that the rank is the largest number of independent columns.
- [Nullspace](/nullspace/): its dimension is the nullity, and the [rank-nullity theorem](/rank-nullity-theorem/) says $\operatorname{rank}(A) + \dim \operatorname{null}(A) = n$.
- [Echelon form](/echelon-form/), [reduced row echelon form](/reduced-row-echelon-form/) and [pivot](/pivot/): the number of pivots is the rank (Fact 5).
- [Determinant](/determinant/): a square matrix has full rank exactly when its determinant is nonzero (Fact 6 with $s = n$).
- [Rank computation](/rank-computation/): the problem of computing the rank, over a field or over $\mathbb{Z}$, and its algorithms.
- [Smith normal form](/smith-normal-form/): over $\mathbb{Z}$ the rank is the number of nonzero diagonal entries of the Smith form, and the primes where Fact 7 gives a drop are the primes that divide the last nonzero one.
- [Tensor rank](/tensor-rank/): for a matrix it equals the rank, since a matrix of rank $r$ is a sum of $r$ matrices of rank $1$ (Fact 3) and a sum of $s$ matrices of rank $1$ has rank at most $s$; for tensors of order three or more it is a different notion.

## References
