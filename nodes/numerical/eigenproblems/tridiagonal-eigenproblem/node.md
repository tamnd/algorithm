---
tag: RMS8DY
kind: problem
slug: tridiagonal-eigenproblem
name: Tridiagonal eigenproblem
aliases:
- symmetric tridiagonal eigenproblem
- Jacobi matrix eigenproblem
area: numerical/eigenproblems
level: core
summary: Find the eigenvalues, and if asked the eigenvectors, of a real symmetric tridiagonal matrix, the core subproblem left after reducing a dense symmetric matrix.
model: floating-point-model
complexity:
  vars: {n: "the order of T"}
  time: {values: O(n^2), vectors: O(n^3)}
  flops: {qr_values: "O(n^2)", qr_vectors: "6 n^3", mrrr: "O(n^2)"}
prereqs: [symmetric-eigenproblem, tridiagonalization]
see_also: [qr-algorithm, wilkinson-shift, bisection-eigenvalue-algorithm, sturm-sequence-eigenvalue-count, divide-and-conquer-eigensolver, mrrr-algorithm, dqds-algorithm, secular-equation]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.3 (the implicit symmetric tridiagonal QR step and the symmetric QR algorithm), Section 8.4 (bisection, Sturm sequences, divide and conquer, MRRR)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.3 (tridiagonal QR, Rayleigh quotient iteration, divide and conquer, bisection and inverse iteration, with timings), Section 5.4 (high relative accuracy)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics edition, 1998
    locator: Chapter 7 (tridiagonal form, distinct eigenvalues, Sturm sequences), Chapter 8 (the QL and QR algorithms and Wilkinson's convergence theorem)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 5 (Sturm sequences and the matrices W21 plus and W21 minus)
  - paper: "J. H. Wilkinson, Global convergence of tridiagonal QR algorithm with origin shifts, Linear Algebra and its Applications 1, 1968"
    title: Global convergence of tridiagonal QR algorithm with origin shifts
    locator: Linear Algebra Appl. 1 (1968), pp. 409 to 420
  - paper: "J. J. M. Cuppen, A divide and conquer method for the symmetric tridiagonal eigenproblem, Numerische Mathematik 36, 1981"
    title: A divide and conquer method for the symmetric tridiagonal eigenproblem
    locator: Numer. Math. 36 (1981), pp. 177 to 195
  - paper: "Inderjit S. Dhillon and Beresford N. Parlett, Multiple representations to compute orthogonal eigenvectors of symmetric tridiagonal matrices, Linear Algebra and its Applications 387, 2004"
    title: Multiple representations to compute orthogonal eigenvectors of symmetric tridiagonal matrices
    locator: Linear Algebra Appl. 387 (2004), pp. 1 to 28
---

The tridiagonal eigenproblem asks for the eigenvalues $\lambda_1 \ge \dots \ge \lambda_n$, and optionally the orthonormal eigenvectors, of a real symmetric tridiagonal matrix $T$ with diagonal $a_1, \dots, a_n$ and off-diagonal $b_1, \dots, b_{n-1}$. Every dense [symmetric eigenproblem](/symmetric-eigenproblem/) is reduced to it by [tridiagonalization](/tridiagonalization/) in $O(n^3)$ flops, after which only $3n - 2$ numbers matter. This structure makes the problem much cheaper than the dense one: a [Sturm count](/sturm-sequence-eigenvalue-count/) costs $O(n)$ flops, a QR step costs $O(n)$ flops, all eigenvalues cost $O(n^2)$ flops, and [MRRR](/mrrr-algorithm/) finds all eigenvectors in $O(n^2)$ flops as well. When no off-diagonal entry is zero the eigenvalues are distinct, but they can still be extremely close.

## In plain words

After the first cleanup step, a symmetric table only has numbers on its main diagonal and right next to it. Each row now talks only to its two neighbours, which makes every operation cheap: counting how many answers lie below a given value takes one quick pass down the diagonal. If one of the side numbers is zero, the problem splits into two smaller independent problems. When none is zero, all the answers are different from each other. Several good methods exist, and they trade speed against how easily they produce directions that are exactly at right angles.

## Definition

**Notation.** $T \in \mathbb R^{n \times n}$ symmetric with $t_{ii} = a_i$, $t_{i,i+1} = t_{i+1,i} = b_i$, and zeros elsewhere. Its eigenvalues are $\lambda_1 \ge \dots \ge \lambda_n$ with orthonormal eigenvectors $v_1, \dots, v_n$. $T_k$ is the leading $k \times k$ principal submatrix, and $u$ is the unit roundoff.

**Problem.** Given $a \in \mathbb R^n$ and $b \in \mathbb R^{n-1}$, return $\hat\lambda_i$, and if asked $\hat V$, with $\hat V \operatorname{diag}(\hat\lambda) \hat V^T = T + E$, $E$ symmetric, $\|E\|_2 \le c(n) u \|T\|_2$, and $\|\hat V^T \hat V - I\|_2 \le c(n) u$. Variants ask for the eigenvalues in an interval $[\alpha, \beta)$, or for those with given indices.

**Basic facts.**

1. *Splitting.* If some $b_i = 0$, $T = \operatorname{diag}(T_{1:i}, T_{i+1:n})$ and the two blocks are solved separately. A matrix with every $b_i \ne 0$ is called unreduced.
2. *Signs of $b_i$ do not matter.* With $D = \operatorname{diag}(\pm 1)$ chosen suitably, $D T D$ has off-diagonal $|b_i|$ and the same eigenvalues; the eigenvectors change only by signs.
3. *Distinct eigenvalues.* If $T$ is unreduced, deleting the first row and the last column of $T - \lambda I$ leaves a lower triangular matrix with diagonal $b_1, \dots, b_{n-1}$, so $\operatorname{rank}(T - \lambda I) \ge n - 1$ for every $\lambda$. Each eigenspace is then one-dimensional, and since $T$ is diagonalizable every eigenvalue is simple. Also the first and last components of every eigenvector are nonzero.
4. *The characteristic polynomials of the leading submatrices* satisfy $p_0 = 1$, $p_1(x) = a_1 - x$ and $p_k(x) = (a_k - x) p_{k-1}(x) - b_{k-1}^2 p_{k-2}(x)$, where $p_k(x) = \det(T_k - x I)$. For unreduced $T$ the zeros of $p_{k-1}$ strictly interlace those of $p_k$ ([Cauchy interlacing](/cauchy-interlacing-theorem/)), which gives the Sturm count.

## Variants

- **All eigenvalues.** Root-free QR (Pal-Walker-Kahan) or [dqds](/dqds-algorithm/) on a positive definite shift of $T$ factored as $L D L^T$.
- **All eigenpairs.** Implicit QR or QL with the [Wilkinson shift](/wilkinson-shift/), accumulating the rotations; [divide and conquer](/divide-and-conquer-eigensolver/); or MRRR.
- **Selected eigenpairs.** [Bisection](/bisection-eigenvalue-algorithm/) on the Sturm count for the values, then [inverse iteration](/inverse-iteration/) or MRRR for the vectors.
- **Relative accuracy.** If $T - \sigma I = L D L^T$ is a factorization of a shifted $T$, small relative changes in the entries of $L$ and $D$ cause small relative changes in the eigenvalues, under conditions that hold for positive definite $T$; dqds and MRRR use such representations to get eigenvalues with high relative accuracy (Dhillon and Parlett 2004).
- **The inverse problem.** Recover $T$ from its eigenvalues and the first components of its eigenvectors, solved by the Lanczos process or by orthogonal polynomials; this is the Jacobi matrix of Gaussian quadrature read in reverse.

## Examples

**The second difference matrix.** For $a_i = 2$ and $b_i = -1$ the eigenvalues are $2 - 2\cos(k\pi/(n+1))$, $k = 1, \dots, n$, with eigenvectors $\sin(jk\pi/(n+1))$. For $n = 4$ they are $0.38197$, $1.38197$, $2.61803$, $3.61803$. At $x = 1.5$ the pivots of $T - 1.5 I = L D L^T$ are $0.5$, $-1.5$, $1.1667$, $-0.3571$; two are negative, so two eigenvalues lie below $1.5$, as the list confirms.

**Unreduced but nearly double: Wilkinson's $W_{21}^+$.** Take $n = 21$, $a_i = |11 - i|$ (so $10, 9, \dots, 1, 0, 1, \dots, 10$) and $b_i = 1$. The matrix is unreduced, so its eigenvalues are distinct, yet bisection on the exact Sturm count in rational arithmetic gives $\lambda_1 = 10.746194182903393$ and $\lambda_2 = 10.746194182903322$, which differ by $7.16 \times 10^{-14}$. The next pair, $9.210678647361332$ and $9.210678647304919$, differs by $5.6 \times 10^{-11}$. So "unreduced" does not mean "well separated", and eigenvectors of such pairs need care: inverse iteration must reorthogonalize, and the computed pair is only determined as a two-dimensional invariant subspace to working accuracy.

**A split.** $a = (1, 2, 3)$, $b = (0, 4)$ splits into $(1)$ and $\begin{pmatrix} 2 & 4 \\ 4 & 3 \end{pmatrix}$, giving eigenvalues $1$ and $(5 \pm \sqrt{65})/2$.

## Known algorithms

| algorithm | output | flops | status |
|---|---|---|---|
| implicit QR or QL, [Wilkinson shift](/wilkinson-shift/) | all eigenvalues; vectors by accumulation | $O(n)$ per step, about $2$ steps per eigenvalue, so $O(n^2)$; about $6n^3$ with vectors | global convergence proved (Wilkinson 1968), at least linear and usually cubic; the step count is observed |
| root-free QR, dqds | all eigenvalues | $O(n^2)$ | typical; dqds has high relative accuracy |
| [bisection](/bisection-eigenvalue-algorithm/) on the Sturm count | eigenvalues in an interval | $O(n)$ per count, $O(n \log(\|T\|/\epsilon))$ per eigenvalue to width $\epsilon$ | proved |
| [inverse iteration](/inverse-iteration/) | vectors for given eigenvalues | $O(n)$ per vector, more for clusters | typical; orthogonality needs reorthogonalization in clusters |
| [divide and conquer](/divide-and-conquer-eigensolver/) (Cuppen; Gu and Eisenstat) | all eigenpairs | at most about $4n^3/3$, often $O(n^{2.3})$ observed through deflation | typical |
| [MRRR](/mrrr-algorithm/) (Dhillon and Parlett) | all or some eigenpairs | $O(n^2)$ for all, $O(nk)$ for $k$ of them | typical; the orthogonality proof needs relative gaps above a threshold at each level |

## Bounds

- **Cost lower bound.** The input has $3n - 2$ numbers and the output $n$, so $\Omega(n)$ is trivial. The standard methods spend $O(n)$ flops per eigenvalue, $O(n^2)$ in all; whether all eigenvalues can be found to working accuracy in $o(n^2)$ flops is not settled by these methods (divide and conquer with fast multipole updates is asymptotically faster in theory, Gu and Eisenstat 1995).
- **Perturbation.** For a symmetric $E$, $|\lambda_i(T + E) - \lambda_i(T)| \le \|E\|_2$ ([Weyl's inequality](/weyls-inequality/)). An eigenvector of a simple eigenvalue moves by at most $\|E\|_2 / \mathrm{gap}$ in angle, up to a constant ([Davis-Kahan theorem](/davis-kahan-theorem/)).
- **Backward stability.** The QR algorithm with rotations and bisection with the Sturm count are backward stable: QR returns the eigenvalues of $T + E$ with $\|E\|_2 = O(n u)\|T\|_2$ (GVL Section 8.3), and the computed Sturm count at $x$ is the exact count for a matrix whose off-diagonal entries are perturbed relatively by a few units of $u$ (Kahan 1966; Demmel Section 5.3).
- **Interlacing.** For unreduced $T$, $\lambda_{i+1}(T) < \lambda_i(T_{n-1}) < \lambda_i(T)$ for $i = 1, \dots, n - 1$. The gaps are positive, but no positive lower bound in terms of the $b_i$ alone holds uniformly, as $W_{21}^+$ shows.

## Reductions

- **From the dense symmetric problem.** $A = Q T Q^T$ by [tridiagonalization](/tridiagonalization/) in $4n^3/3$ flops; eigenvectors are $Q v_i$, at $2n^3$ flops for all of them.
- **From the bidiagonal SVD.** If $B$ is upper bidiagonal, the matrix obtained by a perfect shuffle of $\begin{pmatrix} 0 & B \\ B^T & 0 \end{pmatrix}$ is tridiagonal with zero diagonal (the Golub-Kahan matrix), and its eigenvalues are $\pm \sigma_i(B)$.
- **From orthogonal polynomials.** The three-term recurrence of a family of orthogonal polynomials is the recurrence of fact 4, so the zeros of the $n$-th polynomial are the eigenvalues of the $n \times n$ Jacobi matrix (Golub-Welsch).
- **To the secular equation.** Splitting $T$ in the middle by a rank-one change and solving each half reduces the problem to the roots of a [secular equation](/secular-equation/), which is divide and conquer.

## Applications

The second phase of every dense symmetric eigensolver (LAPACK `xSTEQR`, `xSTERF`, `xSTEBZ`, `xSTEDC`, `xSTEMR`), the Ritz values of the [Lanczos algorithm](/lanczos-algorithm/), Gaussian quadrature nodes and weights, the SVD through the Golub-Kahan matrix, one-dimensional Schrödinger and vibrating-string discretizations, and birth-death Markov chains.

## References
