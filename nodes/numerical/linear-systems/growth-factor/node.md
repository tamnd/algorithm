---
tag: 80CG8A
kind: concept
slug: growth-factor
name: Growth factor
aliases:
- element growth
- pivot growth
- growth factor of Gaussian elimination
area: numerical/linear-systems
level: advanced
summary: Ratio of the largest entry during elimination to the largest entry of the matrix, which controls the stability of LU.
prereqs: [gaussian-elimination, backward-error-analysis, floating-point-model]
see_also: [partial-pivoting, complete-pivoting, lup-decomposition, diagonally-dominant-matrix, cholesky-decomposition, backward-error-analysis, condition-number, hilbert-matrix]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 9.3, Error Analysis (Theorems 9.3 and 9.4); Section 9.4, The Growth Factor (bounds for partial, complete and rook pivoting, Wilkinson's matrix); Section 9.5, Diagonally Dominant and Banded Matrices; Section 9.6, Tridiagonal Matrices
  - paper: doi:10.1145/321075.321076
    title: J. H. Wilkinson, Error analysis of direct methods of matrix inversion, Journal of the ACM 8(3), 1961
    locator: pp. 281 to 330 (the growth factor, the bound 2^(n-1) for partial pivoting and the bound for complete pivoting)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 22, Stability of Gaussian Elimination (Theorem 22.2 and the discussion of random matrices)
  - paper: doi:10.1137/0611023
    title: Lloyd N. Trefethen and Robert S. Schreiber, Average-case stability of Gaussian elimination, SIAM Journal on Matrix Analysis and Applications 11(3), 1990
    locator: pp. 335 to 360 (observed growth about n^(2/3) for partial and n^(1/2) for complete pivoting on random matrices)
  - paper: doi:10.1137/0914014
    title: Stephen J. Wright, A collection of problems for which Gaussian elimination with partial pivoting is unstable, SIAM Journal on Scientific Computing 14(1), 1993
    locator: pp. 231 to 238 (exponential growth from two-point boundary value problems)
  - paper: doi:10.1137/0610012
    title: Nicholas J. Higham and Desmond J. Higham, Large growth factors in Gaussian elimination with pivoting, SIAM Journal on Matrix Analysis and Applications 10(2), 1989
    locator: pp. 155 to 164 (matrices with large growth for partial and complete pivoting)
---

The growth factor of [Gaussian elimination](/gaussian-elimination/) measures how much the entries grow during the elimination:

$$\rho_n = \frac{\max_{i,j,k} |\hat a^{(k)}_{ij}|}{\max_{i,j} |a_{ij}|},$$

where $\hat a^{(k)}_{ij}$ are the computed entries of the active matrices. It is the one quantity that separates a backward stable LU factorization from an unstable one. With $|l_{ij}| \le 1$ the backward error of the computed solution is at most $n^2 \gamma_{3n} \rho_n \|A\|_\infty$, so LU is backward stable exactly when $\rho_n$ is modest. With [partial pivoting](/partial-pivoting/), $\rho_n \le 2^{n-1}$, attained by Wilkinson's matrix; with [complete pivoting](/complete-pivoting/) it is subexponential; and in practice it is almost always small.

## In plain words

Elimination keeps replacing numbers by differences of numbers. If those differences become much larger than the original entries, the small rounding errors made along the way become large compared with the data, and the answer can be ruined. The growth factor is the ratio of the biggest number that ever appears to the biggest number at the start. A growth factor near one means the method is safe for that matrix. Pivoting keeps it small in almost every case seen in practice, though there are rare matrices where it still becomes huge.

## The idea

**Notation.** $A \in \mathbb{R}^{n \times n}$, $A^{(k)}$ the active matrix before step $k$ (so $A^{(1)} = A$ and $A^{(n)}$ gives $U$), $\hat L, \hat U$ the computed factors, $u = 2^{-53}$, $\gamma_n = n u/(1 - n u)$, $\kappa_\infty(A) = \|A\|_\infty \|A^{-1}\|_\infty$. Some books use $\max|u_{ij}|/\max|a_{ij}|$ (Trefethen and Bau) or the exact rather than computed entries; the bounds below hold for either, with small changes in constants.

**Why it controls the error (proved).** Higham's Theorems 9.3 and 9.4: if $n u < 1$ and elimination runs to completion, the computed solution satisfies

$$(A + \Delta A)\hat x = b, \qquad |\Delta A| \le \gamma_{3n} |\hat L|\,|\hat U|.$$

This holds for every row ordering, with $A$ replaced by $P A$. If $|\hat l_{ij}| \le 1$ (partial or complete pivoting), then $\|\,|\hat L|\,\|_\infty \le n$ and $\|\hat U\|_\infty \le n \rho_n \max|a_{ij}| \le n \rho_n \|A\|_\infty$, so

$$\frac{\|\Delta A\|_\infty}{\|A\|_\infty} \le n^2 \gamma_{3n} \rho_n, \qquad \frac{\|x - \hat x\|_\infty}{\|x\|_\infty} \lesssim n^2 \gamma_{3n} \rho_n\, \kappa_\infty(A).$$

The second bound follows from the first by the standard perturbation theorem whenever $\kappa_\infty(A) \|\Delta A\|_\infty / \|A\|_\infty < 1$. The $n^2$ is a worst case; the observed backward error is usually closer to $u \rho_n$.

**Bounds by matrix class.** The last column says whether the result is a theorem or an observation.

| class and pivoting | bound on $\rho_n$ | status |
|---|---|---|
| any $A$, no pivoting | unbounded | proved (the $2 \times 2$ tiny pivot) |
| any $A$, partial pivoting | $2^{n-1}$, attained | proved (Wilkinson 1961) |
| any $A$, complete pivoting | $n^{1/2}(2 \cdot 3^{1/2} \cdots n^{1/(n-1)})^{1/2} \approx n^{(\ln n)/4 + 1/2}$ | proved, not attained |
| any $A$, rook pivoting | $1.5\, n^{(3/4)\ln n}$ | proved (Foster 1997) |
| diagonally dominant by rows or columns, no pivoting | $2$ | proved (Wilkinson; Higham, Section 9.5) |
| symmetric positive definite, no pivoting | $1$ | proved |
| upper Hessenberg, partial pivoting | $n$ | proved |
| tridiagonal, partial pivoting | $2$ | proved (Higham, Section 9.6) |
| totally nonnegative, no pivoting | $1$ | proved |
| random Gaussian entries, partial pivoting | about $n^{2/3}$ | observed (Trefethen and Schreiber 1990) |
| random Gaussian entries, complete pivoting | about $n^{1/2}$ | observed |

For symmetric positive definite $A$ the bound $1$ holds because every Schur complement is again positive definite, and the entries of a positive definite matrix are bounded by its largest diagonal entry, which can only decrease during elimination.

## Examples

**The tiny pivot.** For $A = \begin{pmatrix} \varepsilon & 1 \\ 1 & 1 \end{pmatrix}$ without pivoting, $u_{22} = 1 - 1/\varepsilon$, so $\rho_2 \approx 1/\varepsilon$. With $\varepsilon = 10^{-20}$ in binary64 the computed $x_1$ has relative error $1$, although $\kappa_\infty(A) \approx 4$.

**Wilkinson's matrix.** Let $w_{ii} = 1$, $w_{ij} = -1$ for $i > j$, $w_{in} = 1$, and $0$ elsewhere. For $n = 4$,

$$W_4 = \begin{pmatrix} 1 & 0 & 0 & 1 \\ -1 & 1 & 0 & 1 \\ -1 & -1 & 1 & 1 \\ -1 & -1 & -1 & 1 \end{pmatrix}, \qquad U = \begin{pmatrix} 1 & 0 & 0 & 1 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & 4 \\ 0 & 0 & 0 & 8 \end{pmatrix}.$$

Partial pivoting makes no swaps (every candidate in the column has magnitude $1$ and the first is kept), each step doubles the last column, and $\rho_n = 2^{n-1}$. The condition number $\kappa_\infty(W_n)$ is only about $n$. Measured in binary64 with partial pivoting, for $b = W_n x$ with $x$ uniform in $[-1, 1]^n$ (seed 1), the normwise backward error and the relative forward error are $1.5 \times 10^{-12}$ and $1.5 \times 10^{-11}$ for $n = 20$, $1.4 \times 10^{-4}$ and $3.8 \times 10^{-3}$ for $n = 50$, and $2.2 \times 10^{-2}$ and $1.1$ for $n = 60$: at $n = 60$ no digit is correct. Complete pivoting on $W_n$ has growth $2$.

**A matrix from an application.** Wright (1993) showed that multiple shooting for the two-point boundary value problem $y' = M y$ leads to block bidiagonal matrices on which partial pivoting has growth that is exponential in the number of shooting intervals, and Foster (1994) found a similar example from a Volterra integral equation. These are the known practical cases.

**The [Hilbert matrix](/hilbert-matrix/).** $H_n$ is positive definite, so elimination without pivoting has $\rho_n \le 1$, and the backward error stays near $u$; the large forward error, about $10^{-4}$ for $n = 10$, is entirely due to $\kappa(H_{10}) \approx 1.6 \times 10^{13}$.

## Where it is used

- **Choosing a pivoting strategy.** The bounds explain why [partial pivoting](/partial-pivoting/) is the default, why [complete pivoting](/complete-pivoting/) and rook pivoting exist, and why [Cholesky](/cholesky-decomposition/) needs no pivoting for stability.
- **Structured solvers.** Skipping pivoting is justified exactly when a class has a growth bound: [diagonally dominant](/diagonally-dominant-matrix/) and SPD systems, the [Thomas algorithm](/thomas-algorithm/), block elimination for M-matrices.
- **Diagnostics.** LAPACK's expert driver `gesvx` returns the reciprocal pivot growth $\max_j \|a_j\|_\infty / \|u_j\|_\infty$; a small value warns that the factorization may be unstable, and [iterative refinement](/iterative-refinement/) or a better pivoting strategy can then be used.
- **Sparse and parallel LU.** Threshold pivoting, static pivoting and tournament pivoting trade a weaker growth bound for less fill or less communication, and they are judged by the growth they allow.
- **Probabilistic analysis.** Smoothed and average-case analyses of Gaussian elimination (Trefethen and Schreiber; Sankar, Spielman and Teng) study the distribution of $\rho_n$ to explain why exponential growth is so rare.

## References
