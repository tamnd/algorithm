---
tag: KWBQ5Q
kind: definition
slug: hilbert-matrix
name: Hilbert matrix
aliases:
- Hilbert matrix example
- Hilbert matrices
area: numerical/linear-systems
level: intro
summary: A classic extremely ill-conditioned matrix with entries 1/(i+j-1).
prereqs: [condition-number, positive-definite-matrix]
see_also: [linear-system-solving, cholesky-decomposition, least-squares-problem, orthogonal-polynomials, vandermonde-matrix, iterative-refinement]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 28.1, The Hilbert and Cauchy Matrices (positive definiteness, the explicit inverse, the growth of the condition number)
  - paper: doi:10.1007/BF02418278
    title: David Hilbert, Ein Beitrag zur Theorie des Legendre'schen Polynoms, Acta Mathematica 18, 1894
    locator: pp. 155 to 159 (the determinant of the matrix with entries 1/(i + j - 1))
  - paper: "Man-Duen Choi, Tricks or treats with the Hilbert matrix, The American Mathematical Monthly 90(5), 1983"
    locator: pp. 301 to 312 (the Gram matrix view, the integer inverse and its formula, the determinant)
  - paper: "John Todd, The condition of the finite segments of the Hilbert matrix, National Bureau of Standards Applied Mathematics Series 39, 1954"
    locator: pp. 109 to 116 (the exponential growth of the condition number)
---

The Hilbert matrix of order $n$ is the $n \times n$ matrix $H_n$ with entries $h_{ij} = 1/(i + j - 1)$. It is [symmetric positive definite](/positive-definite-matrix/), its inverse has integer entries, and its [condition number](/condition-number/) grows exponentially in $n$, so it is the standard test case for the effect of ill-conditioning on [linear system solvers](/linear-system-solving/). It comes up in practice as the matrix of the normal equations for fitting a polynomial in the monomial basis on $[0, 1]$.

## Definition

For an integer $n \ge 1$, the **Hilbert matrix** is
$$H_n = \left( \frac{1}{i + j - 1} \right)_{i, j = 1}^{n}, \qquad H_3 = \begin{pmatrix} 1 & \tfrac12 & \tfrac13 \\ \tfrac12 & \tfrac13 & \tfrac14 \\ \tfrac13 & \tfrac14 & \tfrac15 \end{pmatrix}.$$

Its main properties, with the notation of [solving linear systems](/linear-system-solving/):

1. **Gram matrix.** $h_{ij} = \int_0^1 t^{i-1} t^{j-1} \, dt$. So for $c \in \mathbb{R}^n$, $c^T H_n c = \int_0^1 p(t)^2 \, dt$ with $p(t) = \sum_i c_i t^{i-1}$. This is positive when $c \ne 0$, since then $p$ is a nonzero polynomial and vanishes at finitely many points. So $H_n$ is symmetric positive definite.
2. **Cauchy matrix.** $h_{ij} = 1/(a_i + b_j)$ with $a_i = i$ and $b_j = j - 1$. Cauchy's determinant formula gives $\det H_n = \prod_{i < j} (a_j - a_i)(b_j - b_i) / \prod_{i, j} (a_i + b_j)$, which equals $c_n^4 / c_{2n}$ with $c_n = \prod_{k=1}^{n-1} k!$. The values for $n = 1, 2, 3, 4$ are $1$, $1/12$, $1/2160$ and $1/6048000$.
3. **Integer inverse.** The entries of $H_n^{-1}$ are integers:
$$(H_n^{-1})_{ij} = (-1)^{i+j} (i + j - 1) \binom{n + i - 1}{n - j} \binom{n + j - 1}{n - i} \binom{i + j - 2}{i - 1}^2$$
(Choi 1983; Higham, Section 28.1). The sum of all entries of $H_n^{-1}$ is $n^2$.
4. **Condition number.** $\kappa_2(H_n)$ grows like $(1 + \sqrt 2)^{4n} \approx 34^n$, up to a factor that is polynomial in $n$ (Todd 1954). The table gives the values, with $\kappa_2$ from the extreme eigenvalues and $\kappa_\infty$ from the exact inverse.

| $n$ | 2 | 4 | 6 | 8 | 10 | 12 | 14 |
|---|---|---|---|---|---|---|---|
| $\kappa_2(H_n)$ | $1.93 \times 10^{1}$ | $1.55 \times 10^{4}$ | $1.50 \times 10^{7}$ | $1.53 \times 10^{10}$ | $1.60 \times 10^{13}$ | $1.71 \times 10^{16}$ | $1.85 \times 10^{19}$ |
| $\kappa_\infty(H_n)$ | $27$ | $2.84 \times 10^{4}$ | $2.91 \times 10^{7}$ | $3.39 \times 10^{10}$ | $3.54 \times 10^{13}$ | $4.12 \times 10^{16}$ | $4.54 \times 10^{19}$ |

From $n = 12$ on, $\kappa_2(H_n) u > 1$ in binary64 ($u = 2^{-53}$): a backward stable solver can then return a solution with no correct digit.

## Examples and non-examples

- **The inverse of $H_3$.** $H_3^{-1} = \begin{pmatrix} 9 & -36 & 30 \\ -36 & 192 & -180 \\ 30 & -180 & 180 \end{pmatrix}$, whose entries sum to $9$. Here $\|H_3\|_\infty = 11/6$ and $\|H_3^{-1}\|_\infty = 408$, so $\kappa_\infty(H_3) = 748$.
- **Large inverse entries.** The largest entry of $H_{10}^{-1}$ in absolute value is $3480673996800 \approx 3.5 \times 10^{12}$, while each entry of $H_{10}$ lies in $[1/19, 1]$.
- **Non-example: the stored matrix.** In binary64, $1/3$, $1/5$ and most other entries are rounded, so the matrix in the computer is $\mathrm{fl}(H_n) = H_n + E$ with $|E| \le u |H_n|$. It is not a Hilbert matrix, and its inverse differs from $H_n^{-1}$: the largest entry of the difference, relative to the largest entry of $H_n^{-1}$, is $7.9 \times 10^{-11}$ for $n = 6$, $3.0 \times 10^{-9}$ for $n = 8$ and $9.0 \times 10^{-5}$ for $n = 10$. A test that compares a computed inverse with the integer formula therefore measures the rounding of the data as well as the error of the solver. The test should compare with the exact inverse of the stored matrix, computed in rational arithmetic.
- **Non-example: positive definite in exact arithmetic only.** $\mathrm{fl}(H_n)$ is positive definite for small $n$, but rounding can destroy this when $\kappa_2(H_n) u$ is near 1. A plain [Cholesky decomposition](/cholesky-decomposition/) in binary64 with inner products summed from left to right succeeds on $\mathrm{fl}(H_n)$ for $n \le 13$ and meets a non-positive pivot at $n = 14$. The exact $H_{14}$ is positive definite.
- **A solve.** With $b$ the rounded sum of the columns of $\mathrm{fl}(H_8)$, elimination with partial pivoting gives a normwise backward error near $2.6 \times 10^{-17}$ and a forward error near $2.3 \times 10^{-7}$; see [solving linear systems](/linear-system-solving/) for the details. The small backward error and the large forward error together are the signature of a stable method on an ill-conditioned matrix.
- **Non-example: a Hilbert-like matrix.** The matrix $(1/(i + j))_{i,j=1}^n$ is also a Cauchy matrix and is also positive definite and ill-conditioned, but it is not $H_n$; it is the block of rows 2 to $n + 1$ and columns 1 to $n$ of $H_{n+1}$. It is positive definite because $1/(i + j) = \int_0^1 t^{i - 1/2} t^{j - 1/2} \, dt$.

## Related definitions

- [Condition number](/condition-number/) and [matrix norms](/matrix-norms/): the quantities that the table measures.
- [Positive definite matrix](/positive-definite-matrix/): the class that $H_n$ belongs to.
- [Vandermonde matrix](/vandermonde-matrix/): the other classic ill-conditioned matrix of polynomial fitting. With the monomial basis, the [least squares problem](/least-squares-problem/) of fitting on $[0, 1]$ leads to $H_n$ through the [normal equations](/normal-equations/).
- [Orthogonal polynomials](/orthogonal-polynomials/): in the basis of shifted Legendre polynomials the Gram matrix on $[0, 1]$ is diagonal, which is the remedy for the ill-conditioning of $H_n$.
- [Iterative refinement](/iterative-refinement/) and [Hager's condition estimator](/hagers-condition-estimator/): tools that are often tested on $H_n$.

## References
