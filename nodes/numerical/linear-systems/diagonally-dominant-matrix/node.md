---
tag: E9431Y
kind: definition
slug: diagonally-dominant-matrix
name: Diagonally dominant matrix
aliases:
- strictly diagonally dominant matrix
- diagonal dominance
- irreducibly diagonally dominant matrix
area: numerical/linear-systems
level: core
summary: A matrix whose diagonal entries dominate their rows, which guarantees pivot-free stability and iterative convergence.
prereqs: [matrix-norms]
see_also: [jacobi-method, gauss-seidel-method, gershgorin-circle-theorem, growth-factor, partial-pivoting, thomas-algorithm, positive-definite-matrix, banded-matrix]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 9.5, Diagonally Dominant and Banded Matrices (Theorem 9.9, LU without pivoting and growth factor at most 2)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.1, Diagonal Dominance and Symmetry (Theorem 4.1.1, LU of a column diagonally dominant matrix with multipliers at most 1)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 4.2.3, Diagonally Dominant Matrices (convergence of Jacobi and Gauss-Seidel, irreducible diagonal dominance)
  - book: "Richard S. Varga, Matrix Iterative Analysis, second edition, Springer, 2000"
    locator: Section 1.5, Diagonally Dominant Matrices (irreducibility and the Taussky theorem)
  - paper: doi:10.1016/0024-3795(75)90112-3
    title: James M. Varah, A lower bound for the smallest singular value of a matrix, Linear Algebra and its Applications 11, 1975
    locator: pp. 3 to 5 (the bound on the infinity norm of the inverse of a strictly diagonally dominant matrix)
  - paper: "Olga Taussky, A recurring theorem on determinants, The American Mathematical Monthly 56(10), 1949"
    locator: pp. 672 to 676 (history of the nonsingularity theorem and the irreducible case)
  - paper: doi:10.1145/321075.321076
    title: James H. Wilkinson, Error analysis of direct methods of matrix inversion, Journal of the ACM 8(3), 1961
    locator: pp. 281 to 330 (growth factor at most 2 for diagonally dominant matrices)
---

A square matrix is **diagonally dominant** when, in every row, the diagonal entry is at least as large in absolute value as the sum of the absolute values of the other entries. With strict inequality the matrix is **strictly diagonally dominant**, and then it is nonsingular, Gaussian elimination needs no pivoting and has growth factor at most 2, and the [Jacobi](/jacobi-method/) and [Gauss-Seidel](/gauss-seidel-method/) iterations converge. Discretized diffusion problems, implicit time steps and spline systems give such matrices.

## Definition

Let $A = (a_{ij})$ be $n \times n$, real or complex. Write $R_i = \sum_{j \ne i} |a_{ij}|$ (off-diagonal row sum) and $C_j = \sum_{i \ne j} |a_{ij}|$ (off-diagonal column sum).

- $A$ is **diagonally dominant by rows** if $|a_{ii}| \ge R_i$ for all $i$, and **strictly diagonally dominant by rows** if $|a_{ii}| > R_i$ for all $i$.
- $A$ is **diagonally dominant by columns** if $A^T$ is diagonally dominant by rows, that is $|a_{jj}| \ge C_j$ for all $j$; strictly so with $>$.
- $A$ is **irreducibly diagonally dominant** if it is diagonally dominant by rows, irreducible (the directed graph with an edge $i \to j$ for each $a_{ij} \ne 0$, $i \ne j$, is strongly connected), and $|a_{ii}| > R_i$ for at least one $i$.

"Diagonally dominant" without qualification means by rows in most texts (Saad, Varga), but Golub and Van Loan state the LU results for columns. Notation as in [solving linear systems](/linear-system-solving/): $\rho_n$ is the [growth factor](/growth-factor/), $\kappa_\infty(A) = \|A\|_\infty \|A^{-1}\|_\infty$, $G_J = I - D^{-1} A$ the Jacobi iteration matrix with $D = \operatorname{diag}(A)$.

The main consequences, with the hypotheses that each one needs:

1. **Nonsingularity (Levy-Desplanques).** Strictly diagonally dominant by rows (or columns) implies nonsingular. Proof: if $A v = 0$ with $\|v\|_\infty = |v_i| > 0$, then $|a_{ii}| |v_i| = |\sum_{j \ne i} a_{ij} v_j| \le R_i |v_i|$, a contradiction. Equivalently, $0$ lies outside every [Gershgorin disc](/gershgorin-circle-theorem/). Irreducibly diagonally dominant matrices are also nonsingular (Taussky 1949); weak dominance alone is not enough.
2. **Inverse bound (Varah 1975).** If $A$ is strictly diagonally dominant by rows, then $\|A^{-1}\|_\infty \le 1 / \min_i (|a_{ii}| - R_i)$. With $q = \max_i R_i / |a_{ii}| < 1$, this gives $\kappa_\infty(A) \le \frac{1 + q}{1 - q} \cdot \frac{\max_i |a_{ii}|}{\min_i |a_{ii}|}$.
3. **Elimination without pivoting.** If $A$ is nonsingular and diagonally dominant by rows or by columns, then it has an LU factorization without pivoting and $\rho_n \le 2$ (Wilkinson 1961; Higham, Theorem 9.9). The Schur complement after one step of elimination is again diagonally dominant of the same kind. If $A$ is diagonally dominant by columns, the multipliers satisfy $|l_{ij}| \le 1$, so [partial pivoting](/partial-pivoting/) performs no row interchanges (Golub and Van Loan, Theorem 4.1.1). The backward error bound of elimination then holds with $\rho_n \le 2$.
4. **Iterative convergence.** If $A$ is strictly diagonally dominant by rows, then $\|G_J\|_\infty = q < 1$, so Jacobi and Gauss-Seidel converge for every start, at least at rate $q$ per sweep in the infinity norm. Irreducible diagonal dominance also gives convergence of both (Saad, Section 4.2.3).
5. **Definiteness.** A real symmetric matrix that is diagonally dominant with nonnegative diagonal is positive semidefinite, and positive definite if the dominance is strict. This follows from the Gershgorin discs, which then lie in $[0, \infty)$ or $(0, \infty)$.

## Examples and non-examples

- **Strict dominance and the inverse bound.** $A = \begin{pmatrix} 4 & -1 & 0 \\ -1 & 4 & -1 \\ 0 & -1 & 4 \end{pmatrix}$ (the matrix of the [Jacobi example](/jacobi-method/)) has $|a_{ii}| - R_i = 3, 2, 3$, so Varah's bound gives $\|A^{-1}\|_\infty \le 1/2$. The exact inverse has $\|A^{-1}\|_\infty = 3/7$.
- **Weak dominance, irreducible.** The second difference matrix $T_n = \operatorname{tridiag}(-1, 2, -1)$ is diagonally dominant with equality in rows $2$ to $n - 1$ and strict inequality in rows $1$ and $n$, and it is irreducible. So it is nonsingular, but Varah's bound says nothing, and indeed $\|T_n^{-1}\|_\infty = \max_i i(n + 1 - i)/2 \approx (n + 1)^2/8$ (it is $3$ for $n = 4$). Elimination without pivoting on it, which is the [Thomas algorithm](/thomas-algorithm/), is stable.
- **Growth factor 2 is attained.** $\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}$ is diagonally dominant by columns (with equality) and nonsingular. One elimination step gives $u_{22} = 1 - (1)(-1) = 2$, so $\rho_2 = 2$.
- **Non-example: weak dominance without irreducibility can be singular.** $\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ is diagonally dominant (with equality in both rows) and singular. It is irreducible, but no row is strict. The Jacobi matrix has $\rho(G_J) = 1$.
- **Non-example: rows but not columns.** $\begin{pmatrix} 1 & 0 \\ 3 & 4 \end{pmatrix}$ is strictly diagonally dominant by rows but not by columns, since $|a_{11}| = 1 < 3 = C_1$. Elimination without pivoting uses the multiplier $3$, so the column statement $|l_{ij}| \le 1$ fails and partial pivoting would swap the rows; the growth factor is still $1 \le 2$, as Theorem 9.9 of Higham promises for row dominance.
- **Non-example: positive definite but not dominant.** The matrix with unit diagonal and off-diagonal entries $0.8$ ($n = 3$) is symmetric positive definite, but $R_i = 1.6 > 1$. Jacobi diverges on it, while Gauss-Seidel converges because it is positive definite.

## Related definitions

- [Gershgorin circle theorem](/gershgorin-circle-theorem/): the eigenvalue localization behind facts 1 and 5.
- [Growth factor](/growth-factor/) and [partial pivoting](/partial-pivoting/): diagonal dominance is the main class where pivoting can be skipped safely.
- [Positive definite matrix](/positive-definite-matrix/): the other classic class where elimination needs no pivoting; fact 5 connects them.
- [Banded matrix](/banded-matrix/): banded diagonally dominant systems can be factored in band storage with no pivoting, so the band does not widen.
- $M$-matrices and $H$-matrices: $A$ is an $H$-matrix if $A D$ is strictly diagonally dominant for some positive diagonal $D$ (generalized diagonal dominance); a nonsingular $M$-matrix is an $H$-matrix with $a_{ii} > 0$ and $a_{ij} \le 0$ (Varga, Chapter 3). Incomplete factorizations are guaranteed to exist for $M$-matrices ([incomplete LU](/incomplete-lu-factorization/)).

## References
