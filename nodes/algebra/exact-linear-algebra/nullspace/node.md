---
tag: 95C8TT
kind: definition
slug: nullspace
name: Nullspace
aliases: [kernel, null space, right kernel]
area: algebra/exact-linear-algebra
level: intro
summary: The set of vectors x with Ax = 0.
prereqs: [linear-independence]
see_also: [rank, rank-nullity-theorem, nullspace-computation, reduced-row-echelon-form, linear-diophantine-system, hermite-normal-form, linear-system-modulo-2]
sources:
  - book: isbn:9783319110790
    title: Sheldon Axler, Linear Algebra Done Right, third edition, Springer, 2015
    locator: Section 3.B, Null Spaces and Ranges (the null space of a linear map is a subspace, and injectivity is equivalent to a null space of zero)
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition, Prentice Hall, 1971
    locator: Section 3.1, Linear Transformations (null space, nullity and the rank theorem), and Section 1.4, Row-Reduced Echelon Matrices (the solutions of AX = 0 read from the reduced form)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer
    locator: Section 2.3.1, Kernel and image (the kernel over a field), and Section 2.4.3, Applications of the Hermite normal form (the kernel of an integer matrix as a Z-module)
---

The *nullspace* (or *kernel*) of an $m \times n$ matrix $A$ over a field $K$ is the set of all vectors $x \in K^n$ with $A x = 0$. It is a subspace of $K^n$, its dimension is the *nullity* of $A$, and by the [rank-nullity theorem](/rank-nullity-theorem/) the nullity is $n$ minus the [rank](/rank/). Over an integral domain such as $\mathbb{Z}$ the integer solutions form a module, not a vector space, and a basis over $\mathbb{Q}$ does not always give a basis of the integer solutions.

## Definition

**Notation.** $K$ is a field, $R$ an integral domain with field of fractions $K$, and $A$ an $m \times n$ matrix over $K$ (or over $R$). Vectors are columns.

**Over a field.** The nullspace of $A$ is

$$\operatorname{null}(A) = \{\, x \in K^n : A x = 0 \,\}.$$

It is a subspace of $K^n$: it contains $0$, and if $A x = 0$ and $A y = 0$ then $A(\lambda x + \mu y) = \lambda A x + \mu A y = 0$ for all $\lambda, \mu \in K$. Its dimension $\dim \operatorname{null}(A)$ is the **nullity** of $A$. When $A$ is the matrix of a linear map $f : K^n \to K^m$, the nullspace of $A$ is the kernel $\{ x : f(x) = 0 \}$ of $f$. The **left nullspace** is $\operatorname{null}(A^T) = \{ y \in K^m : y^T A = 0 \}$, the set of linear relations among the rows of $A$.

**A basis from the reduced form.** Let $E$ be the [reduced row echelon form](/reduced-row-echelon-form/) of $A$, with pivot columns $p_1 < \cdots < p_r$ and free columns $F = \{1, \ldots, n\} \setminus \{p_1, \ldots, p_r\}$. Row operations are invertible, so $\operatorname{null}(A) = \operatorname{null}(E)$. For each free column $j \in F$ define $u_j \in K^n$ by

$$(u_j)_j = 1, \qquad (u_j)_{j'} = 0 \text{ for } j' \in F \setminus \{j\}, \qquad (u_j)_{p_i} = -E_{i j} \text{ for } i = 1, \ldots, r.$$

Row $i$ of $E u_j$ is $(u_j)_{p_i} + E_{ij} = 0$, so $u_j \in \operatorname{null}(A)$. The $u_j$ are independent, because on the coordinates in $F$ they are the standard vectors. They span: for $x \in \operatorname{null}(A)$, the vector $x - \sum_{j \in F} x_j u_j$ is in the nullspace and is zero on $F$, and row $i$ of $E$ then forces its coordinate $p_i$ to be zero. So $\{u_j : j \in F\}$ is a basis, and the nullity is $|F| = n - r$.

**Over an integral domain.** For $A$ over $R$, the set $\operatorname{null}_R(A) = \{ x \in R^n : A x = 0 \}$ is an $R$-submodule of $R^n$, and $\operatorname{null}_R(A) = R^n \cap \operatorname{null}_K(A)$. For $R = \mathbb{Z}$ it is a free $\mathbb{Z}$-module of rank $n - r$ (a submodule of $\mathbb{Z}^n$ is free), so it is a [lattice](/lattice/) in $\mathbb{Z}^n$. It is *saturated*: if $c x \in \operatorname{null}_{\mathbb{Z}}(A)$ for an integer $c \neq 0$ and $x \in \mathbb{Z}^n$, then $x \in \operatorname{null}_{\mathbb{Z}}(A)$.

**Solutions of $A x = b$.** If $x_0$ is one solution of $A x = b$, the set of all solutions is the affine set $x_0 + \operatorname{null}(A)$: $A x = b$ if and only if $A(x - x_0) = 0$. So a solvable system has a unique solution exactly when the nullspace is $\{0\}$, that is, when the columns of $A$ are [linearly independent](/linear-independence/).

## Examples and non-examples

**A one-dimensional nullspace.** For

$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}, \qquad E = \begin{pmatrix} 1 & 0 & -1 \\ 0 & 1 & 2 \\ 0 & 0 & 0 \end{pmatrix},$$

the pivot columns are $1$ and $2$, and column $3$ is free. The rule above gives $u_3 = (1, -2, 1)^T$, so $\operatorname{null}(A) = \{ t (1, -2, 1)^T : t \in \mathbb{Q} \}$ and the nullity is $1 = 3 - 2$. Over $\mathbb{Z}$, $\operatorname{null}_{\mathbb{Z}}(A) = \mathbb{Z} (1, -2, 1)^T$.

**The field changes the nullspace.** The integer matrix with rows $(1, 1, 0)$, $(0, 1, 1)$, $(1, 0, 1)$ has determinant $2$. Over $\mathbb{Q}$ its nullspace is $\{0\}$. Over $\mathbb{Z}/2\mathbb{Z}$ its reduced form has rows $(1, 0, 1)$, $(0, 1, 1)$, $(0, 0, 0)$, and the nullspace is $\{ 0, (1, 1, 1)^T \}$.

**Extreme shapes.** The nullspace of the $m \times n$ zero matrix is all of $K^n$. For $n = 0$ the nullspace is $K^0 = \{0\}$. For $m = 0$ (no equations) it is $K^n$. An invertible $n \times n$ matrix has nullspace $\{0\}$.

**Non-example: a basis over $\mathbb{Q}$ scaled to integers.** For the $1 \times 3$ matrix $A = (2 \;\; 1 \;\; 1)$ the reduced form is $(1 \;\; \tfrac12 \;\; \tfrac12)$, with basis $(-\tfrac12, 1, 0)^T$ and $(-\tfrac12, 0, 1)^T$. Clearing the denominator of each gives $w_1 = (-1, 2, 0)^T$ and $w_2 = (-1, 0, 2)^T$. These are a basis of $\operatorname{null}_{\mathbb{Q}}(A)$, but they generate only a sublattice of index $2$ in $\operatorname{null}_{\mathbb{Z}}(A)$: the gcd of the $2 \times 2$ minors of $(w_1, w_2)$ is $\gcd(2, -2, 4) = 2$, while a basis such as $(1, -2, 0)^T, (0, -1, 1)^T$ has minors $-1, 1, -2$ with gcd $1$. The integer vector $(0, -1, 1)^T$ is a solution that is not an integer combination of $w_1$ and $w_2$. An integer basis needs a [Hermite normal form](/hermite-normal-form/) or a similar unimodular method.

**Non-example: the solutions of $A x = b$ for $b \neq 0$.** They do not form a subspace, since $x = 0$ is not a solution. They form a translate of the nullspace, or the empty set.

**Non-example: the column space.** The column space $\{ A x : x \in K^n \}$ is a subspace of $K^m$, not of $K^n$. For a square matrix both are subspaces of $K^n$, but they are different in general: for $A = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ both are the line spanned by $(1, 0)^T$, and for $A = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$ the nullspace is spanned by $(0, 1)^T$ and the column space by $(1, 0)^T$.

## Related definitions

- [Rank](/rank/): the dimension of the column space. The [rank-nullity theorem](/rank-nullity-theorem/) says rank plus nullity is $n$.
- [Linear independence](/linear-independence/): the columns of $A$ are independent exactly when the nullspace is $\{0\}$.
- [Reduced row echelon form](/reduced-row-echelon-form/): the form from which a nullspace basis is read off as above.
- [Nullspace computation](/nullspace-computation/): the problem of computing a basis, over a field or over $\mathbb{Z}$, and its algorithms.
- [Linear Diophantine system](/linear-diophantine-system/): integer solutions of $A x = b$, which form a translate of $\operatorname{null}_{\mathbb{Z}}(A)$ when they exist.
- [System of linear equations modulo 2](/linear-system-modulo-2/): the nullspace over $\mathbb{Z}/2\mathbb{Z}$ gives the dependencies used in factoring by sieves.

## References
