---
tag: 541ATV
kind: problem
slug: singular-value-decomposition
name: Singular value decomposition
aliases:
- SVD
- singular value problem
area: numerical/eigenproblems
level: core
summary: Factor any m by n matrix as A = U Σ V* with unitary U and V and a nonnegative diagonal Σ. It gives the rank, the 2-norm, the best low-rank approximations and the pseudoinverse.
model: floating-point-model
complexity:
  vars: {m: "the number of rows of A", n: "the number of columns, n ≤ m"}
  time: {worst: O(m n^2)}
  flops: {values: "4 m n^2 - 4 n^3 / 3", thin_with_vectors: "14 m n^2 + 8 n^3"}
prereqs: [spectral-theorem, matrix-norms]
see_also: [golub-kahan-svd-algorithm, dqds-algorithm, pseudoinverse, least-squares-problem, principal-component-analysis, rank-revealing-factorization, symmetric-eigenproblem, jacobi-eigenvalue-algorithm]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 2.4 (the SVD and its properties, Eckart-Young), Section 8.6 (computing the SVD, bidiagonalization, the Golub-Kahan step, Jacobi methods, and the table of flop counts)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 4 (the SVD), Lecture 5 (more on the SVD, low-rank approximation), Lecture 31 (computing the SVD, the operation counts of bidiagonalization)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 3.2.3 (the SVD and least squares), Section 5.2 (perturbation theory for singular values), Section 5.4 (algorithms for the SVD and high relative accuracy)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 7.3, The singular value and polar decompositions
  - paper: "C. Eckart and G. Young, The approximation of one matrix by another of lower rank, Psychometrika 1, 1936"
    title: The approximation of one matrix by another of lower rank
    locator: Psychometrika 1(3) (1936), pp. 211 to 218
  - paper: "G. Golub and W. Kahan, Calculating the singular values and pseudo-inverse of a matrix, Journal of the Society for Industrial and Applied Mathematics, Series B: Numerical Analysis 2, 1965"
    title: Calculating the singular values and pseudo-inverse of a matrix
    locator: SIAM J. Numer. Anal. Ser. B 2(2) (1965), pp. 205 to 224
  - paper: "James Demmel and W. Kahan, Accurate singular values of bidiagonal matrices, SIAM Journal on Scientific and Statistical Computing 11, 1990"
    title: Accurate singular values of bidiagonal matrices
    locator: SIAM J. Sci. Stat. Comput. 11(5) (1990), pp. 873 to 912
  - paper: "G. W. Stewart, On the early history of the singular value decomposition, SIAM Review 35, 1993"
    title: On the early history of the singular value decomposition
    locator: SIAM Rev. 35(4) (1993), pp. 551 to 566
---

The singular value decomposition writes any $m \times n$ matrix as $A = U \Sigma V^*$, with $U$ and $V$ unitary and $\Sigma$ diagonal with entries $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_{\min(m,n)} \ge 0$. The singular values $\sigma_i$ give the 2-norm $\|A\|_2 = \sigma_1$, the rank (the number of nonzero $\sigma_i$), the distance to the nearest matrix of lower rank, and the condition number $\sigma_1 / \sigma_n$ of a square matrix. Unlike the eigenvalue decomposition, it exists for every matrix, rectangular or square, and its factors are always unitary. The singular values are well conditioned: no singular value moves by more than $\|E\|_2$ when $A$ changes to $A + E$. The standard algorithm reduces $A$ to bidiagonal form and then runs a QR-type iteration on the bidiagonal matrix, at a cost of $O(m n^2)$ flops.

## In plain words

Any table of numbers that turns arrows into arrows can be described in three moves: a turn, then a stretch along fixed directions at right angles to each other, then another turn. The stretch amounts are the singular values; they are never negative, and they come sorted from the largest to the smallest. The biggest one says how much the table can lengthen an arrow. Small ones say that some directions are almost flattened, which is what makes systems of equations hard to solve. Keeping only the few largest stretches gives the best simple copy of the table, which is the idea behind compressing data and finding its main trends.

## Definition

**Notation.** $A \in \mathbb C^{m \times n}$, often real, and $p = \min(m, n)$. The singular values are $\sigma_1 \ge \dots \ge \sigma_p \ge 0$; $u_i$ and $v_i$ are the left and right singular vectors, the columns of $U$ and $V$. For a real $A$, $U$ and $V$ are real orthogonal and $V^* = V^T$. $u$ is the unit roundoff.

**The decomposition.** A singular value decomposition of $A$ is a factorization

$$A = U \Sigma V^*, \qquad U \in \mathbb C^{m \times m}, \ V \in \mathbb C^{n \times n} \text{ unitary}, \qquad \Sigma = \operatorname{diag}(\sigma_1, \dots, \sigma_p) \in \mathbb R^{m \times n}.$$

Equivalently $A v_i = \sigma_i u_i$ and $A^* u_i = \sigma_i v_i$ for $i \le p$. It exists for every $A$: the Hermitian positive semidefinite matrix $A^* A$ has an orthonormal eigenvector basis $v_1, \dots, v_n$ with eigenvalues $\sigma_1^2 \ge \dots \ge 0$ by the [spectral theorem](/spectral-theorem/); for $\sigma_i > 0$ put $u_i = A v_i / \sigma_i$, which are orthonormal because $u_i^* u_j = v_i^* A^* A v_j / (\sigma_i \sigma_j) = \delta_{ij}$, and complete them to an orthonormal basis of $\mathbb C^m$. The singular values are unique; for distinct nonzero $\sigma_i$ the pair $(u_i, v_i)$ is unique up to a common factor $e^{i\phi}$.

**The thin SVD.** For $m \ge n$, $A = U_1 \Sigma_1 V^*$ with $U_1 \in \mathbb C^{m \times n}$ having orthonormal columns and $\Sigma_1 = \operatorname{diag}(\sigma_1, \dots, \sigma_n)$. Most applications need only this form, and it is much cheaper to compute when $m \gg n$.

**The floating-point problem.** Return computed $\hat\sigma_i$ and, if asked, $\hat U$ and $\hat V$ such that $\hat U \operatorname{diag}(\hat\sigma) \hat V^* = A + E$ with $\|E\|_2 \le c(m, n) \, u \, \|A\|_2$, and $\hat U$ and $\hat V$ within $c(m, n) u$ of unitary matrices. By the perturbation bound below, each $\hat\sigma_i$ then has the absolute error $|\hat\sigma_i - \sigma_i| \le c(m,n) u \sigma_1$. Small singular values can therefore have large relative errors, unless the algorithm has high relative accuracy for the class of input.

## Variants

- **Singular values only.** Bidiagonalize and use [dqds](/dqds-algorithm/), which computes every singular value of a bidiagonal matrix to high relative accuracy in $O(n^2)$ flops.
- **Thin SVD with vectors.** Bidiagonalization, then the [Golub-Kahan SVD algorithm](/golub-kahan-svd-algorithm/) (implicit shifted QR on the bidiagonal matrix) or bidiagonal divide and conquer (LAPACK `xGESDD`).
- **Truncated SVD.** The $k$ largest triplets of a large or sparse matrix, by Lanczos bidiagonalization, by the [Lanczos algorithm](/lanczos-algorithm/) on $\begin{pmatrix} 0 & A \\ A^* & 0 \end{pmatrix}$, or by randomized range finders followed by a small dense SVD.
- **High relative accuracy.** One-sided [Jacobi](/jacobi-eigenvalue-algorithm/) computes all singular values to high relative accuracy for matrices $A = B D$ with $D$ diagonal and $B$ well conditioned; Demmel and Kahan (1990) proved the same for bidiagonal matrices with their zero-shift QR.
- **Generalized SVD.** For a pair $(A, B)$ with the same number of columns, $A = U C X$ and $B = V S X$ with $C$ and $S$ diagonal, related to the [generalized eigenvalue problem](/generalized-eigenvalue-problem/) for $A^* A - \lambda B^* B$.

## Examples

**A $2 \times 2$ matrix.** $A = \begin{pmatrix} 3 & 0 \\ 4 & 5 \end{pmatrix}$ has $A^T A = \begin{pmatrix} 25 & 20 \\ 20 & 25 \end{pmatrix}$ with eigenvalues 45 and 5, so $\sigma_1 = 3\sqrt 5 = 6.708$ and $\sigma_2 = \sqrt 5 = 2.236$. The right singular vectors are $v_1 = (1, 1)^T / \sqrt 2$ and $v_2 = (1, -1)^T / \sqrt 2$, and $u_i = A v_i / \sigma_i$ gives $u_1 = (1, 3)^T / \sqrt{10}$ and $u_2 = (3, -1)^T / \sqrt{10}$. The checks: $\sigma_1 \sigma_2 = 15 = |\det A|$ and $\sigma_1^2 + \sigma_2^2 = 50 = \|A\|_F^2$. The best rank-one approximation is $\sigma_1 u_1 v_1^T = \begin{pmatrix} 1.5 & 1.5 \\ 4.5 & 4.5 \end{pmatrix}$, and $A$ minus it has 2-norm $\sqrt 5 = \sigma_2$, as the Eckart-Young theorem says.

**Why not form $A^* A$.** Let $A = \begin{pmatrix} 1 & 1 \\ \delta & 0 \\ 0 & \delta \end{pmatrix}$ with $\delta = 10^{-8}$ (Läuchli's example). Its singular values are $\sqrt{2 + \delta^2}$ and $\delta$. In double precision $1 + \delta^2$ rounds to $1$, so the computed $A^T A$ is exactly $\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$, which is singular: the square root of its smaller eigenvalue is $0$, not $10^{-8}$. A backward stable SVD algorithm works on $A$ directly and returns $\delta$ with an absolute error of order $u$.

**A rank-deficient matrix.** $\begin{pmatrix} 1 & 2 \\ 2 & 4 \\ 3 & 6 \end{pmatrix}$ has $\sigma_1 = \sqrt{70}$ and $\sigma_2 = 0$, because it equals $(1, 2, 3)^T (1, 2)$, and $\|(1,2,3)\| \, \|(1,2)\| = \sqrt{14} \sqrt 5$. In floating point the computed $\hat\sigma_2$ is of order $u \sqrt{70}$, not exactly zero, so the numerical rank is decided by a threshold such as $\max(m, n) \, u \, \hat\sigma_1$.

## Known algorithms

| algorithm | output | cost (leading term, $m \ge n$) | status of the count |
|---|---|---|---|
| Golub-Kahan bidiagonalization | $A = U_B B V_B^*$, $B$ upper bidiagonal | $4mn^2 - 4n^3/3$ flops (TB Lecture 31) | exact count |
| QR first, then bidiagonalize $R$ (Lawson-Hanson-Chan) | the same | $2mn^2 + 2n^3$ flops, cheaper when $m > 5n/3$ | exact count |
| [Golub-Kahan SVD algorithm](/golub-kahan-svd-algorithm/) (Golub-Reinsch) | $\Sigma$, $U_1$, $V$ | about $14mn^2 + 8n^3$ flops in total (GVL Section 8.6) | typical: iterations per singular value observed |
| [dqds](/dqds-algorithm/) | $\Sigma$ of a bidiagonal matrix | $O(n^2)$ flops | typical |
| bidiagonal divide and conquer | $\Sigma$ and vectors | about the same as QR for $U_1$, often faster | typical |
| one-sided Jacobi | $\Sigma$, $U_1$, $V$ with high relative accuracy | $O(mn^2)$ per sweep, a few sweeps | typical; quadratic convergence proved |
| Lanczos bidiagonalization or randomized | the $k$ largest triplets | products with $A$ and $A^*$, plus $O(m k^2)$ | depends on the singular value gaps |

## Bounds

- **Iterative by necessity.** The $\sigma_i^2$ are the eigenvalues of the Hermitian matrix $A^* A$, so the SVD is an eigenvalue problem in disguise, and as for eigenvalues every general method is iterative; the $O(mn^2)$ totals rest on observed iteration counts, while the bidiagonalization count is exact.
- **Weyl's bound.** For every $A$ and $E$ of the same size, $|\sigma_i(A + E) - \sigma_i(A)| \le \|E\|_2$ for each $i$. No assumption on $A$ is needed, in contrast to eigenvalues of nonnormal matrices (GVL Section 2.4; it follows from [Weyl's inequality](/weyls-inequality/) applied to the Hermitian matrix $\begin{pmatrix} 0 & A \\ A^* & 0 \end{pmatrix}$).
- **Mirsky's bound.** $\bigl(\sum_i (\sigma_i(A + E) - \sigma_i(A))^2\bigr)^{1/2} \le \|E\|_F$.
- **Eckart-Young-Mirsky.** For $k < \operatorname{rank} A$ and $A_k = \sum_{i \le k} \sigma_i u_i v_i^*$, $\min_{\operatorname{rank} B \le k} \|A - B\|_2 = \sigma_{k+1}$ and $\min_{\operatorname{rank} B \le k} \|A - B\|_F = (\sum_{i > k} \sigma_i^2)^{1/2}$, both attained by $A_k$ (Eckart and Young 1936 for the Frobenius norm; Mirsky 1960 for every unitarily invariant norm).
- **Singular vectors.** A singular subspace is sensitive in proportion to $\|E\| / \mathrm{gap}$, where the gap separates its singular values from the others (Wedin's $\sin\theta$ theorem, the SVD analogue of the [Davis-Kahan theorem](/davis-kahan-theorem/)).
- **Relative accuracy.** For a bidiagonal $B$, a relative perturbation of size $\eta$ in each entry changes each singular value by a relative amount of at most about $(2n - 1)\eta$, so tiny singular values are determined to high relative accuracy by the entries (Demmel and Kahan 1990).

## Reductions

- **To a Hermitian eigenproblem.** The eigenvalues of $\begin{pmatrix} 0 & A \\ A^* & 0 \end{pmatrix}$ are $\pm \sigma_1, \dots, \pm \sigma_p$ and $|m - n|$ zeros, with eigenvectors $(u_i, \pm v_i) / \sqrt 2$. This reduction is backward stable but doubles the order. The eigenvalues of $A^* A$ are $\sigma_i^2$, but forming $A^* A$ squares the condition and loses the small singular values, as Läuchli's example shows.
- **To a bidiagonal problem.** Householder reflectors from both sides give $A = U_B B V_B^*$ with $B$ upper bidiagonal; this is the first phase of every dense method.
- **Least squares and the pseudoinverse.** The [pseudoinverse](/pseudoinverse/) is $A^+ = V \Sigma^+ U^*$, and $x = A^+ b$ is the minimum-norm solution of the [least squares problem](/least-squares-problem/), also when $A$ is rank deficient.
- **Polar decomposition.** $A = (U V^*)(V \Sigma V^*)$ for square $A$: a unitary factor times a Hermitian positive semidefinite one.
- **Norms and conditioning.** $\|A\|_2 = \sigma_1$, $\|A\|_F = (\sum \sigma_i^2)^{1/2}$, and for square nonsingular $A$ the [condition number](/condition-number/) is $\kappa_2(A) = \sigma_1 / \sigma_n$, while $\sigma_n$ is the 2-norm distance to the nearest singular matrix.

## Applications

Low-rank approximation and data compression, [principal component analysis](/principal-component-analysis/) (the SVD of the centred data matrix), the numerical rank and [rank-revealing factorizations](/rank-revealing-factorization/), regularized and rank-deficient least squares, the Procrustes problem (the nearest orthogonal matrix to $A$ is $U V^*$), total least squares, latent semantic indexing in text retrieval, model reduction in control, image processing, and the computation of [pseudospectra](/pseudospectrum/) through $\sigma_{\min}(A - z I)$.

## References
