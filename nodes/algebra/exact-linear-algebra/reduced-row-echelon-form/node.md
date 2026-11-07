---
tag: 5WHH45
kind: definition
slug: reduced-row-echelon-form
name: Reduced row echelon form
aliases: [RREF, row-reduced echelon form, reduced echelon form]
area: algebra/exact-linear-algebra
level: intro
summary: Echelon form with each pivot equal to 1 and zero above and below it.
prereqs: [echelon-form, pivot]
see_also: [gauss-jordan-elimination, gaussian-elimination, rank, nullspace, hermite-normal-form, cramers-rule, hadamard-bound]
sources:
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition, Prentice Hall, 1971
    locator: Section 1.4, Row-Reduced Echelon Matrices (the definition and the reduction of every matrix), and Section 2.5, Computations Concerning Subspaces (each subspace of the space of row vectors is the row space of exactly one row-reduced echelon matrix)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer
    locator: Section 2.3.1, Kernel and image (elimination to a reduced form, and the kernel and image read from it)
  - paper: "Arne Storjohann, Algorithms for Matrix Canonical Forms, PhD thesis, ETH Zurich, 2000"
    locator: Chapter 2, echelon forms over fields (the reduced echelon form with a transforming matrix in O(n m r^(ω-2)) field operations)
---

A matrix is in *reduced row echelon form* (RREF) when it is in [echelon form](/echelon-form/), each [pivot](/pivot/) is $1$, and each pivot is the only nonzero entry of its column. Each matrix over a field is row equivalent to exactly one matrix in reduced row echelon form, so the RREF is a canonical form for the row space. [Gauss-Jordan elimination](/gauss-jordan-elimination/) computes it, and the [rank](/rank/), a basis of the row space and a basis of the [nullspace](/nullspace/) can all be read from it.

## Definition

**Notation.** $K$ is a field and $E$ is an $m \times n$ matrix over $K$. The *leading entry* of a nonzero row is its first nonzero entry.

$E$ is in **reduced row echelon form** when the four conditions below hold.

1. Each zero row is below each nonzero row.
2. If rows $i$ and $i+1$ are nonzero, the leading entry of row $i+1$ is in a column to the right of the leading entry of row $i$.
3. Each leading entry is $1$.
4. Each column that holds a leading entry has zeros in all its other places.

Conditions 1 and 2 define a row echelon form. The leading entries are the *pivots*; if there are $r$ nonzero rows with pivots in columns $p_1 < \cdots < p_r$, then $E$ restricted to the columns $p_1, \ldots, p_r$ and the rows $1, \ldots, r$ is the identity matrix $I_r$. Two $m \times n$ matrices $A$ and $B$ are *row equivalent* when $B = P A$ for an invertible $m \times m$ matrix $P$; this holds exactly when each can be turned into the other by row swaps, row scalings by nonzero constants, and additions of a multiple of one row to another.

**Theorem (existence and uniqueness).** For each $m \times n$ matrix $A$ over $K$ there is exactly one matrix $E$ in reduced row echelon form that is row equivalent to $A$. It is written $\operatorname{rref}(A)$.

*Existence.* Gauss-Jordan elimination: for each column from left to right, if the rows not yet used have a nonzero entry in it, swap one of them up, scale it to make the entry $1$, and subtract multiples of it from all other rows to clear the column. Each operation is invertible, and the result satisfies conditions 1 to 4.

*Uniqueness.* Let $E$ and $E'$ be in reduced row echelon form and row equivalent to $A$, so $E' = Q E$ with $Q$ invertible. Multiplication by $Q$ keeps each linear relation among the columns, so column $j$ of $E$ is a combination of columns $1, \ldots, j-1$ of $E$ if and only if the same holds in $E'$. In a reduced echelon form, column $j$ is a pivot column exactly when it is not such a combination. So $E$ and $E'$ have the same pivot columns $p_1 < \cdots < p_r$, and the same number $r$ of nonzero rows. Both have the same row space, since $Q$ is invertible. A vector $v = \sum_i c_i E_i$ of this row space has entry $c_i$ in column $p_i$, by condition 4. So the nonzero rows $E_i$ and $E'_i$ are both the unique vector of the row space with entry $1$ in column $p_i$ and $0$ in the other pivot columns, and $E_i = E'_i$. $\square$

**The entries as quotients of minors.** Let $A$ have rank $r$, let $p_1 < \cdots < p_r$ be the pivot columns of $\operatorname{rref}(A)$, and suppose first that $r = m$. Let $B$ be the $m \times m$ submatrix of $A$ in the pivot columns. Then $\operatorname{rref}(A) = P A$ with $P B = I$, so $P = B^{-1}$ and, by [Cramer's rule](/cramers-rule/),

$$\operatorname{rref}(A)_{ij} = \frac{\det B_{i \leftarrow j}}{\det B},$$

where $B_{i \leftarrow j}$ is $B$ with its column $i$ replaced by column $j$ of $A$. For $r < m$ the same formula holds with $B$ the $r \times r$ submatrix in the pivot columns and in $r$ independent rows of $A$, applied to those rows. So for an integer matrix with entries of absolute value less than $2^b$, each entry of $\operatorname{rref}(A)$ is a quotient of two integers of absolute value at most $r^{r/2} 2^{r b}$ by the [Hadamard bound](/hadamard-bound/), with the common denominator $\det B$. This is the size bound behind exact and fraction-free computation of the form.

**Cost.** Gauss-Jordan elimination computes $\operatorname{rref}(A)$ of an $m \times n$ matrix of rank $r$ with $O(m n r)$ field operations. With fast matrix multiplication the bound is $O(m n r^{\omega - 2})$ field operations (Storjohann, Chapter 2), where $\omega$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/). Over $\mathbb{Q}$, the formula above bounds the output, and the computation can be done modulo primes and lifted, or fraction-free with the [Bareiss algorithm](/bareiss-algorithm/) followed by one exact division by $\det B$ per entry.

## Examples and non-examples

**A reduction with a free column.** For

$$A = \begin{pmatrix} 1 & 2 & 1 & 4 \\ 2 & 4 & 0 & 2 \\ 3 & 6 & 1 & 6 \end{pmatrix}$$

subtract $2$ and $3$ times row $1$ from rows $2$ and $3$; both become $(0, 0, -2, -6)$. Column $2$ has no pivot. Scale row $2$ by $-\tfrac12$ to get $(0, 0, 1, 3)$, subtract it from row $1$, and add $2$ times it to row $3$. The result is

$$\operatorname{rref}(A) = \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & 0 & 1 & 3 \\ 0 & 0 & 0 & 0 \end{pmatrix},$$

with pivot columns $1$ and $3$, rank $2$, and the nullspace basis $(-2, 1, 0, 0)^T$, $(-1, 0, -3, 1)^T$ from the free columns $2$ and $4$.

**Same pivot columns, different forms.** The matrix with rows $(2, 4, 1, 3)$, $(1, 2, 3, 4)$, $(3, 6, 4, 7)$ has the reduced form with rows $(1, 2, 0, 1)$, $(0, 0, 1, 1)$, $(0, 0, 0, 0)$. It has the same pivot columns as the example above, but a different form, so the two matrices have different row spaces.

**Denominators from a minor.** For $A$ with rows $(2, 1, 3)$ and $(1, 3, 2)$, the pivot columns are $1$ and $2$, $B = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$ and $\det B = 5$. The reduced form has rows $(1, 0, \tfrac75)$ and $(0, 1, \tfrac15)$; the numerators $7$ and $1$ are $\det \begin{pmatrix} 3 & 1 \\ 2 & 3 \end{pmatrix}$ and $\det \begin{pmatrix} 2 & 3 \\ 1 & 2 \end{pmatrix}$, as the formula says.

**Shapes.** The identity $I_n$, a zero matrix and the $0 \times n$ matrix are in reduced row echelon form. The RREF of an invertible $n \times n$ matrix is $I_n$, and the RREF of $(A \mid I_n)$ is $(I_n \mid A^{-1})$; this is how Gauss-Jordan elimination inverts a matrix.

**Non-example: echelon but not reduced.** $\begin{pmatrix} 2 & 1 \\ 0 & 3 \end{pmatrix}$ is in echelon form, but its pivots are not $1$. $\begin{pmatrix} 1 & 5 \\ 0 & 1 \end{pmatrix}$ has pivots $1$, but the entry $5$ is above a pivot. Both have RREF $I_2$.

**Non-example: a zero row in the middle.** The matrix with rows $(1, 0)$, $(0, 0)$, $(0, 1)$ breaks condition 1.

**Non-example: integer matrices.** Over $\mathbb{Z}$ the scaling of condition 3 needs a division, so there is no integer RREF in general. The analog over $\mathbb{Z}$ is the [Hermite normal form](/hermite-normal-form/), which allows only unimodular row operations and asks for reduced entries above each pivot instead of zeros.

## Related definitions

- [Echelon form](/echelon-form/): conditions 1 and 2 only; it is not unique.
- [Pivot](/pivot/): a leading entry; the pivot columns of the RREF are the column rank profile of $A$.
- [Gauss-Jordan elimination](/gauss-jordan-elimination/): the algorithm that computes the RREF.
- [Rank](/rank/): the number of nonzero rows of the RREF.
- [Nullspace](/nullspace/): a basis is read from the free columns of the RREF.
- [Hermite normal form](/hermite-normal-form/): the canonical form under unimodular row operations over $\mathbb{Z}$.
- [Cramer's rule](/cramers-rule/) and the [Hadamard bound](/hadamard-bound/): they bound the size of the entries of the RREF of an integer matrix.

## References
