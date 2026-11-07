---
tag: H1KMDM
kind: definition
slug: echelon-form
name: Echelon form
aliases:
- row echelon form
- staircase form
- REF
area: algebra/exact-linear-algebra
level: intro
summary: Matrix form in which the zero rows are at the bottom and the first nonzero entry of each row lies strictly right of the one above.
prereqs: [linear-independence]
see_also: [reduced-row-echelon-form, gaussian-elimination, gauss-jordan-elimination, rank, pivot, hermite-normal-form, lu-decomposition, nullspace]
sources:
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition
    locator: Chapter 1, Section 1.4, Row-reduced echelon matrices (definition, and the theorem that each matrix is row-equivalent to one such matrix)
  - book: isbn:9780980232714
    title: Gilbert Strang, Introduction to Linear Algebra, fourth edition
    locator: Chapter 3, Sections 3.2 and 3.3 (the echelon matrix U, the reduced form R, pivot columns and rank)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.3.1, Kernel and image (echelon forms used to compute the kernel and the image of a matrix)
  - paper: "Arne Storjohann, Algorithms for Matrix Canonical Forms, PhD thesis, ETH Zurich, 2000"
    locator: Chapter 2, Echelon forms over fields (the rank profile and the cost of computing an echelon transform)
---

A matrix is in *echelon form* when its zero rows are at the bottom and the first nonzero entry of each nonzero row lies strictly to the right of the first nonzero entry of the row above it. The nonzero rows then form a staircase, and the number of steps is the [rank](/rank/) of the matrix. [Gaussian elimination](/gaussian-elimination/) brings each matrix over a field to an echelon form by row operations, and the form is the starting point for solving linear systems, computing a [nullspace](/nullspace/) and reading off [linear independence](/linear-independence/) of the columns.

Notation on these pages: $K$ is a field and $R$ is an integral domain. $A$ is an $m \times n$ matrix with entries $a_{ij}$, rows $1, \dots, m$ and columns $1, \dots, n$. For a square matrix, $n$ is its size.

## Definition

Let $E$ be an $m \times n$ matrix over a field $K$, with $m, n \ge 0$. For a nonzero row $i$ of $E$, the *leading entry* is its first nonzero entry, and the *leading column* $\ell(i)$ is the column of that entry. $E$ is in **row echelon form** if there is an integer $r$ with $0 \le r \le \min(m, n)$ such that

1. rows $1, \dots, r$ are nonzero and rows $r+1, \dots, m$ are zero, and
2. $\ell(1) < \ell(2) < \cdots < \ell(r)$.

The leading entries are the *pivots* of $E$, and $\ell(1), \dots, \ell(r)$ are its *pivot columns*. Condition 2 says that each entry below a pivot, and each entry to the left of a pivot in the same row, is zero. Since the $r$ pivot columns are distinct, $r \le n$.

$E$ is in **reduced row echelon form** if, in addition, each pivot is $1$ and each pivot is the only nonzero entry of its column. This is the [reduced row echelon form](/reduced-row-echelon-form/).

A matrix $E$ is *an echelon form of* $A$ if $E = UA$ for some invertible $m \times m$ matrix $U$ over $K$. Since each invertible matrix is a product of elementary matrices, this is the same as saying that row swaps, multiplications of a row by a nonzero scalar and additions of a multiple of one row to another turn $A$ into $E$. *Column echelon form* is the transpose notion: $E^T$ is in row echelon form.

The same definition makes sense over an integral domain $R$, with $U$ invertible over $R$, that is, $\det U$ a unit of $R$. Over $\mathbb{Z}$ this means $\det U = \pm 1$, and the [Hermite normal form](/hermite-normal-form/) is the echelon form over $\mathbb{Z}$ made unique by conditions on the pivots and on the entries above them.

**Theorem.** Let $A$ be an $m \times n$ matrix over a field $K$.

- (a) $A$ has an echelon form.
- (b) Each echelon form $E$ of $A$ has the same number $r$ of nonzero rows and the same pivot columns. Column $j$ is a pivot column exactly when column $j$ of $A$ is not a linear combination of columns $1, \dots, j-1$ of $A$. In particular $r = \operatorname{rank} A$.
- (c) $A$ has exactly one reduced row echelon form.

*Proof of (a).* By induction on $n$. If $n = 0$ or $A$ is zero, $A$ is in echelon form with $r = 0$. Otherwise let $j$ be the first nonzero column of $A$ and let $a_{pj} \ne 0$. Swap rows $1$ and $p$, then subtract $a_{ij}/a_{1j}$ times row $1$ from each row $i > 1$. Now column $j$ is zero below row $1$ and columns $1, \dots, j-1$ are zero. By induction, row operations on rows $2, \dots, m$ bring the submatrix in rows $2, \dots, m$ and columns $j+1, \dots, n$ to echelon form. These operations do not change columns $1, \dots, j$, since those columns are zero in rows $2, \dots, m$. The result is in echelon form with $\ell(1) = j$. This is the method of [Gaussian elimination](/gaussian-elimination/).

*Proof of (b).* Let $E = UA$ with $U$ invertible, and write $a_j$ and $e_j$ for column $j$ of $A$ and of $E$. Then $e_j = U a_j$, and for scalars $c_1, \dots, c_n$ we have $\sum_j c_j e_j = U \sum_j c_j a_j$. Since $U$ is invertible, $\sum_j c_j e_j = 0$ exactly when $\sum_j c_j a_j = 0$. So a column of $E$ is a combination of earlier columns of $E$ exactly when the same holds for $A$. In $E$, a pivot column $\ell(i)$ is not a combination of earlier columns, because the earlier columns are zero in rows $i, \dots, m$ while $e_{\ell(i)}$ has a nonzero entry in row $i$. A column $j$ that is not a pivot column lies between $\ell(k)$ and $\ell(k+1)$ for some $k$ (with $\ell(0) = 0$ and $\ell(r+1) = n+1$), so $e_j$ is zero below row $k$. The pivot columns $e_{\ell(1)}, \dots, e_{\ell(k)}$ restricted to rows $1, \dots, k$ form an upper triangular matrix with nonzero diagonal, which is invertible, so $e_j$ is a combination of them. This proves the characterization, which depends on $A$ only. The pivot columns are then the same for all echelon forms, and $r$ is their number. The pivot columns of $A$ form a basis of the column space of $A$, so $r = \operatorname{rank} A$.

*Proof of (c).* Existence: start from an echelon form, divide each nonzero row by its pivot, and for $i = r, r-1, \dots, 1$ subtract multiples of row $i$ from the rows above it to clear column $\ell(i)$. Each step keeps the echelon shape and the earlier zeros. Uniqueness: let $E$ and $E'$ be reduced echelon forms of $A$. By (b) they have the same pivot columns $\ell(1), \dots, \ell(r)$. Their nonzero rows span the same space, the row space of $A$, because $E = UA$ and $E' = U'A$ with $U$ and $U'$ invertible. Row $i$ of $E'$ is then $\sum_k c_k \cdot (\text{row } k \text{ of } E)$. Read this equation in column $\ell(k)$: row $k$ of $E$ has a $1$ there and the other rows of $E$ have $0$, so $c_k$ equals the entry of row $i$ of $E'$ in column $\ell(k)$, which is $1$ for $k = i$ and $0$ otherwise. So row $i$ of $E'$ equals row $i$ of $E$. $\blacksquare$

Part (b) says that the *set* of pivot columns, called the column rank profile of $A$, is an invariant. The echelon form itself is not unique, as the examples show.

## Examples and non-examples

Take, over $\mathbb{Q}$,

$$
A = \begin{pmatrix} 0 & 2 & 4 & 2 \\ 1 & 1 & 1 & 0 \\ 2 & 4 & 6 & 2 \end{pmatrix}.
$$

Swap rows $1$ and $2$, subtract $2$ times the new row $1$ from row $3$, then subtract row $2$ from row $3$. This gives

$$
E = \begin{pmatrix} 1 & 1 & 1 & 0 \\ 0 & 2 & 4 & 2 \\ 0 & 0 & 0 & 0 \end{pmatrix}, \qquad
E_{\text{red}} = \begin{pmatrix} 1 & 0 & -1 & -1 \\ 0 & 1 & 2 & 1 \\ 0 & 0 & 0 & 0 \end{pmatrix}.
$$

$E$ is in echelon form with $r = 2$ and pivot columns $1$ and $2$, so $\operatorname{rank} A = 2$. Row $3$ of $A$ is row $1$ plus $2$ times row $2$, which is why a zero row appears. $E_{\text{red}}$ is the reduced form: divide row $2$ of $E$ by $2$ and subtract it from row $1$.

- The matrix $\begin{pmatrix} 2 & 4 & 6 & 2 \\ 0 & 2 & 4 & 2 \\ 0 & 0 & 0 & 0 \end{pmatrix}$ is also an echelon form of the same $A$, since $(2, 4, 6, 2) = 2 \cdot (1, 1, 1, 0) + 2 \cdot (0, 1, 2, 1)$. It has the same pivot columns, as part (b) demands, but other entries. An echelon form is not unique; the reduced form is.
- Each upper triangular square matrix with nonzero diagonal is in echelon form with $r = n$, and each pivot lies on the diagonal.
- The zero $m \times n$ matrix is in echelon form with $r = 0$, and so is the $0 \times 0$ matrix.
- A $1 \times n$ matrix is always in echelon form.

Non-examples:

- $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ is not in echelon form: the leading column of row $2$ is left of that of row $1$. One row swap fixes it.
- $\begin{pmatrix} 1 & 2 \\ 0 & 0 \\ 0 & 3 \end{pmatrix}$ is not in echelon form: a zero row lies above a nonzero row.
- $\begin{pmatrix} 1 & 2 \\ 0 & 3 \end{pmatrix}$ is in echelon form but not in reduced form: the pivot $3$ is not $1$, and the entry $2$ above it is not $0$.
- $\begin{pmatrix} 1 & 1 \\ 0 & 1 \\ 0 & 1 \end{pmatrix}$ is not in echelon form: rows $2$ and $3$ have the same leading column.

## Related definitions

- [Reduced row echelon form](/reduced-row-echelon-form/): the unique echelon form with pivots $1$ and zeros above the pivots. [Gauss-Jordan elimination](/gauss-jordan-elimination/) computes it.
- [Pivot](/pivot/): a leading entry of an echelon form, and the entry by which elimination divides.
- [Rank](/rank/): the number $r$ of nonzero rows of any echelon form.
- [LU decomposition](/lu-decomposition/): when no row swap is needed, the elimination that gives $E$ also writes $A = LE$ with $L$ unit lower triangular.
- [Hermite normal form](/hermite-normal-form/) and [Smith normal form](/smith-normal-form/): canonical forms over $\mathbb{Z}$ and other principal ideal domains, where only unimodular row (and for Smith, column) operations are allowed.
- [Nullspace](/nullspace/): the columns that are not pivot columns are the free variables, and each gives one basis vector of the nullspace.

## References
