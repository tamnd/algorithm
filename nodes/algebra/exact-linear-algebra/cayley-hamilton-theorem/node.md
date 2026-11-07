---
tag: SKQSEP
kind: theorem
slug: cayley-hamilton-theorem
name: Cayley-Hamilton theorem
aliases:
- Hamilton-Cayley theorem
area: algebra/exact-linear-algebra
level: intro
summary: Every square matrix over a commutative ring satisfies its own characteristic polynomial.
prereqs: [characteristic-polynomial, cramers-rule]
see_also: [characteristic-polynomial, matrix-minimal-polynomial, faddeev-leverrier-algorithm, berkowitz-algorithm, wiedemann-algorithm, matrix-power, linear-recurrence-nth-term, jordan-normal-form]
sources:
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition
    locator: Chapter 6, Section 6.3, Annihilating polynomials (the Cayley-Hamilton theorem and the minimal polynomial)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition
    locator: Section 2.4, Consequences of Schur's triangularization theorem (the Cayley-Hamilton theorem)
  - paper: doi:10.1098/rstl.1858.0002
    title: Arthur Cayley, A memoir on the theory of matrices, Philosophical Transactions of the Royal Society of London 148, 1858
    locator: pp. 17 to 37 (the statement, checked for matrices of order 2 and 3)
  - paper: "Ferdinand Georg Frobenius, Ueber lineare Substitutionen und bilineare Formen, Journal fur die reine und angewandte Mathematik 84, 1878"
    locator: pp. 1 to 63 (a proof for all orders, and the minimal polynomial)
  - book: "William Rowan Hamilton, Lectures on Quaternions, Dublin, 1853"
    locator: the lectures on linear functions of quaternions (the special case for quaternions)
---

The Cayley-Hamilton theorem says that each square matrix $A$ is a root of its own [characteristic polynomial](/characteristic-polynomial/): if $\chi_A(x) = \det(xI - A) = x^n + c_{n-1}x^{n-1} + \cdots + c_0$, then $A^n + c_{n-1}A^{n-1} + \cdots + c_1 A + c_0 I = 0$. It holds over every commutative ring, with a short proof through the adjugate. Algorithms use it to write $A^{-1}$ and high powers $A^k$ as polynomials in $A$ of degree less than $n$, and it is the reason why the sequences of [Wiedemann's method](/wiedemann-algorithm/) satisfy a linear recurrence.

Notation: $R$ is a commutative ring, $A$ is an $n \times n$ matrix over $R$ with $n \ge 1$, and $I$ is the identity. For a polynomial $p(x) = \sum_k p_k x^k \in R[x]$, $p(A) = \sum_k p_k A^k$ with $A^0 = I$.

## Statement

**Theorem.** Let $R$ be a commutative ring, $A \in R^{n \times n}$, and $\chi_A(x) = \det(xI_n - A) = \sum_{k=0}^{n} c_k x^k$ with $c_n = 1$. Then

$$
\chi_A(A) = \sum_{k=0}^{n} c_k A^k = 0.
$$

The polynomial is computed first, with $x$ as an indeterminate over $R$, and then $A$ is substituted into it.

## In plain words

From a square matrix one builds a special polynomial, its characteristic polynomial, whose degree is the size of the matrix. The theorem says: put the matrix itself into this polynomial, with matrix powers in place of the powers of the variable, and the result is the zero matrix. So a high power of the matrix is never new. It is a fixed combination of the identity and the first few powers, as many as the size of the matrix. This lets programs replace the inverse, or a huge power, by a short sum of small powers.

## Proof

Let $M(x) = xI - A$, a matrix over the polynomial ring $R[x]$, and let $B(x) = \operatorname{adj} M(x)$ be its adjugate. Part 1 of [Cramer's rule](/cramers-rule/) holds over the commutative ring $R[x]$, so

$$
(xI - A)\, B(x) = \det(xI - A)\, I = \chi_A(x)\, I. \qquad (1)
$$

Each entry of $B(x)$ is, up to sign, a determinant of order $n - 1$ of a submatrix of $xI - A$. Each entry of $xI - A$ has degree at most $1$, so each entry of $B(x)$ is a polynomial of degree at most $n - 1$. Collect the coefficients: $B(x) = \sum_{k=0}^{n-1} B_k x^k$ with $B_k \in R^{n \times n}$. Put $B_{-1} = B_n = 0$.

The two sides of (1) are matrices of polynomials, which we can read as polynomials with matrix coefficients. The left side is $\sum_{k=0}^{n-1} B_k x^{k+1} - \sum_{k=0}^{n-1} A B_k x^k$. Comparing the coefficients of $x^k$ for $k = 0, 1, \dots, n$ gives

$$
B_{k-1} - A B_k = c_k I \qquad (0 \le k \le n). \qquad (2)
$$

Multiply equation (2) for $k$ on the left by $A^k$ and add the $n + 1$ equations:

$$
\sum_{k=0}^{n} c_k A^k = \sum_{k=0}^{n} \left( A^k B_{k-1} - A^{k+1} B_k \right) = \sum_{k=1}^{n} A^k B_{k-1} - \sum_{k=0}^{n-1} A^{k+1} B_k.
$$

The first sum drops the term $k = 0$ because $B_{-1} = 0$, and the second drops $k = n$ because $B_n = 0$. With $k' = k + 1$, the second sum is $\sum_{k'=1}^{n} A^{k'} B_{k'-1}$, the same as the first. So the difference is $0$, and $\chi_A(A) = 0$. $\blacksquare$

The proof uses only ring operations on matrices and the comparison of coefficients. It never puts the matrix $A$ in place of $x$ in identity (1). That would be an error, since $x$ commutes with every matrix but $A$ does not.

**Example.** For $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$, $\chi_A(x) = x^2 - 5x - 2$, and $A^2 = \begin{pmatrix} 7 & 10 \\ 15 & 22 \end{pmatrix}$. Then $A^2 - 5A - 2I = 0$ entry by entry. For $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$, $\chi_M(x) = x^3 - 9x^2 + 24x - 18$, and $M^3 = \begin{pmatrix} 15 & 21 & 9 \\ 21 & 45 & 39 \\ 9 & 39 & 75 \end{pmatrix}$ equals $9M^2 - 24M + 18I$, where $M^2 = \begin{pmatrix} 5 & 5 & 1 \\ 5 & 11 & 7 \\ 1 & 7 & 17 \end{pmatrix}$.

## Consequences

- **Inverse as a polynomial.** $c_0 = \chi_A(0) = \det(-A) = (-1)^n \det A$. Write the theorem as $A (A^{n-1} + c_{n-1}A^{n-2} + \cdots + c_1 I) = -c_0 I$. If $\det A$ is a unit, then $A^{-1} = -c_0^{-1}(A^{n-1} + c_{n-1}A^{n-2} + \cdots + c_1 I)$. For $M$ above, $M^{-1} = \tfrac{1}{18}(M^2 - 9M + 24I) = \tfrac{1}{18}\begin{pmatrix} 11 & -4 & 1 \\ -4 & 8 & -2 \\ 1 & -2 & 5 \end{pmatrix}$. The [Faddeev-LeVerrier algorithm](/faddeev-leverrier-algorithm/) computes the coefficients $c_k$ and this inverse together.
- **Powers.** $A^k = r_k(A)$, where $r_k$ is the remainder of $x^k$ modulo $\chi_A$. So $A^k$ for a huge $k$ costs $O(\log k)$ multiplications of polynomials modulo $\chi_A$, plus one evaluation at $A$; see [matrix power](/matrix-power/) and [the N-th term of a linear recurrence](/linear-recurrence-nth-term/).
- **Linear recurrences.** For vectors $u$ and $v$, the scalar sequence $s_i = u^T A^i v$ satisfies $\sum_k c_k s_{i+k} = u^T A^i \chi_A(A) v = 0$. So it is linearly recurrent of order at most $n$. [Wiedemann's algorithm](/wiedemann-algorithm/) finds a recurrence of this sequence with the Berlekamp-Massey algorithm and uses it to solve sparse systems.
- **Minimal polynomial.** The monic polynomials $p$ with $p(A) = 0$ over a field $K$ form the nonzero ideal of $K[x]$ generated by the [minimal polynomial](/matrix-minimal-polynomial/) $\mu_A$. So $\mu_A$ divides $\chi_A$, and $\deg \mu_A \le n$.
- **Eigenvalues.** Over a field, $\chi_A$ and $\mu_A$ have the same roots. Each root of $\mu_A$ is a root of $\chi_A$ because $\mu_A$ divides $\chi_A$. Conversely, if $Av = \lambda v$ with $v \ne 0$, then $0 = \mu_A(A) v = \mu_A(\lambda) v$, so $\mu_A(\lambda) = 0$. The [Jordan normal form](/jordan-normal-form/) gives the multiplicities in both polynomials.

## Tightness

The degree $n$ cannot be lowered for every matrix. For $J = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$, $\chi_J(x) = x^2$, but no monic polynomial $x - c$ of degree $1$ annihilates $J$, because $J - cI$ has the entry $1$ in position $(1, 2)$. In general, a companion matrix of a monic polynomial $p$ of degree $n$ has $\chi = \mu = p$. On the other side, the theorem is not always sharp: $I_n$ has $\chi(x) = (x - 1)^n$ but is already killed by $x - 1$.

The proof uses the commutativity of $R$, through the adjugate identity over $R[x]$. The theorem in this form is a statement about commutative rings.

## History

Arthur Cayley stated the theorem in his 1858 memoir on matrices. He checked it for matrices of order $2$, said he had checked order $3$, and did not give a general proof. William Rowan Hamilton had earlier proved a special case for linear functions of quaternions. Ferdinand Georg Frobenius gave a proof for all orders in 1878, in the same paper in which he introduced the minimal polynomial.

## References
