---
tag: S7N8B0
kind: definition
slug: characteristic-polynomial
name: Characteristic polynomial
aliases:
- char poly
- secular polynomial
- characteristic equation
area: algebra/exact-linear-algebra
level: core
summary: The polynomial det(xI - A), whose roots are the eigenvalues of A.
prereqs: [determinant, polynomial]
see_also: [cayley-hamilton-theorem, characteristic-polynomial-computation, eigenvalue, matrix-minimal-polynomial, rational-canonical-form, jordan-normal-form, berkowitz-algorithm, faddeev-leverrier-algorithm]
sources:
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition
    locator: Chapter 6, Section 6.2, Characteristic values (the characteristic polynomial and its invariance under similarity)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition
    locator: Section 1.2, The characteristic polynomial and algebraic multiplicity (the coefficients as sums of principal minors)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2.4, Computing the characteristic polynomial
---

The characteristic polynomial of a square matrix $A$ is $\chi_A(x) = \det(xI - A)$, a monic polynomial of degree $n$ whose roots in a field are the [eigenvalues](/eigenvalue/) of $A$. Its coefficients are, up to sign, the sums of the principal minors of $A$; the two ends are $-\operatorname{tr} A$ and $(-1)^n \det A$. Similar matrices have the same characteristic polynomial, and by the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/) each matrix is a root of its own.

Notation: $R$ is a commutative ring, $K$ is a field, and $A = (a_{ij})$ is an $n \times n$ matrix over $R$. For a set $S \subseteq \{1, \dots, n\}$, $A[S]$ is the principal submatrix with rows and columns in $S$.

## Definition

Let $x$ be an indeterminate over $R$. The **characteristic polynomial** of $A$ is

$$
\chi_A(x) = \det(xI_n - A) \in R[x],
$$

the [determinant](/determinant/) of a matrix over the commutative ring $R[x]$. Write $\chi_A(x) = \sum_{k=0}^{n} c_k x^k$. The equation $\chi_A(\lambda) = 0$ is the *characteristic equation*. Some books use $\det(A - xI) = (-1)^n \chi_A(x)$ instead; it has the same roots, but it is monic only for even $n$. For $n = 0$, $\chi_A = 1$.

**Proposition.** Let $A$ be an $n \times n$ matrix over a commutative ring $R$.

- (a) $\chi_A$ is monic of degree $n$, and for $0 \le k \le n$ the coefficient of $x^{n-k}$ is $(-1)^k E_k(A)$, where $E_k(A) = \sum_{|S| = k} \det A[S]$ is the sum of the $\binom{n}{k}$ principal minors of order $k$. In particular $c_{n-1} = -\operatorname{tr} A$ and $c_0 = (-1)^n \det A$.
- (b) If $P$ is invertible over $R$, then $\chi_{P^{-1}AP} = \chi_A$.
- (c) $\chi_{A^T} = \chi_A$.
- (d) Over a field $K$, $\lambda \in K$ is an eigenvalue of $A$, that is $Av = \lambda v$ for some $v \ne 0$, exactly when $\chi_A(\lambda) = 0$.

*Proof.* (a) Column $j$ of $xI - A$ is $x e_j - a_j$. The determinant is multilinear in the columns, so it expands into $2^n$ terms, one for each set $S$ of the columns where we take $-a_j$, with $x e_j$ in the columns outside $S$. Factor out $x$ from each column outside $S$, which gives $x^{n - |S|}$. The remaining matrix has the unit vector $e_j$ in each column $j \notin S$ and $-a_j$ in each column $j \in S$. In the Leibniz formula, a unit column $e_j$ forces $\sigma(j) = j$, so the determinant equals the determinant of the submatrix in rows $S$ and columns $S$ of $-A$, which is $(-1)^{|S|} \det A[S]$. Summing over the sets $S$ with $|S| = k$ gives the coefficient of $x^{n-k}$. For $k = 0$ it is $1$, for $k = 1$ it is $-\sum_i a_{ii}$, and for $k = n$ it is $(-1)^n \det A$.

(b) $xI - P^{-1}AP = P^{-1}(xI - A)P$, since $x$ commutes with $P$. The product rule gives $\det P^{-1} \cdot \chi_A(x) \cdot \det P = \chi_A(x)$, because $\det P^{-1} \det P = \det I = 1$.

(c) $xI - A^T = (xI - A)^T$, and a matrix and its transpose have the same determinant.

(d) $Av = \lambda v$ with $v \ne 0$ means that $\lambda I - A$ has a nonzero kernel, which holds exactly when $\det(\lambda I - A) = 0$. Evaluation at $\lambda$ is a ring homomorphism $K[x] \to K$, so $\det(\lambda I - A) = \chi_A(\lambda)$. $\blacksquare$

The *algebraic multiplicity* of an eigenvalue $\lambda$ is its multiplicity as a root of $\chi_A$. Over an algebraically closed field, $\chi_A(x) = \prod_{i=1}^{n}(x - \lambda_i)$, so $\operatorname{tr} A = \sum_i \lambda_i$ and $\det A = \prod_i \lambda_i$.

## Examples and non-examples

- For $n = 2$, $\chi_A(x) = x^2 - (a_{11} + a_{22})x + (a_{11}a_{22} - a_{12}a_{21})$. For $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ this is $x^2 - 5x - 2$.
- For $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$: $E_1 = 2 + 3 + 4 = 9$, $E_2 = (6 - 1) + (8 - 0) + (12 - 1) = 24$, and $E_3 = \det M = 18$. So $\chi_M(x) = x^3 - 9x^2 + 24x - 18$.
- A triangular matrix has $\chi_A(x) = \prod_i (x - a_{ii})$, because $xI - A$ is triangular too.
- The companion matrix $C = \begin{pmatrix} 0 & 0 & -5 \\ 1 & 0 & 2 \\ 0 & 1 & 0 \end{pmatrix}$ of $p(x) = x^3 - 2x + 5$ has $\chi_C = p$. Each monic polynomial is the characteristic polynomial of its companion matrix, so the problem of finding eigenvalues contains the problem of finding the roots of a polynomial.
- Over $\mathbb{Z}/2\mathbb{Z}$, $A = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ has $\chi_A = x^2 - x - 1 = x^2 + x + 1$, which has no root in the field. So $A$ has no eigenvalue there, although $\chi_A$ is defined.

Non-examples:

- The [minimal polynomial](/matrix-minimal-polynomial/) is not the characteristic polynomial in general. $I_2$ has $\chi = (x - 1)^2$ and minimal polynomial $x - 1$.
- The characteristic polynomial does not determine a matrix up to similarity. $\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ and the zero matrix both have $\chi = x^2$, but only the zero matrix is similar to the zero matrix. The [Jordan normal form](/jordan-normal-form/) and the [rational canonical form](/rational-canonical-form/) do determine the similarity class.
- The product $\prod_i (x - a_{ii})$ of the diagonal factors is not $\chi_A$ unless the off-diagonal entries do not contribute. For $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ it is $x^2$, while $\chi = x^2 - 1$.

## Related definitions

- [Cayley-Hamilton theorem](/cayley-hamilton-theorem/): $\chi_A(A) = 0$.
- [Eigenvalue](/eigenvalue/): a root of $\chi_A$ in the field.
- [Minimal polynomial](/matrix-minimal-polynomial/): the monic generator of the polynomials that kill $A$. It divides $\chi_A$ and has the same roots.
- [Characteristic polynomial computation](/characteristic-polynomial-computation/): the problem of computing the coefficients of $\chi_A$ exactly, by the [Berkowitz algorithm](/berkowitz-algorithm/), the [Faddeev-LeVerrier algorithm](/faddeev-leverrier-algorithm/) or reduction to Hessenberg form.
- [Rational canonical form](/rational-canonical-form/): its invariant factors multiply to $\chi_A$.
- [Resultant](/resultant/): another determinant of a matrix of polynomial entries, with a similar role for pairs of polynomials.

## References
