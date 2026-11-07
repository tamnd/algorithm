---
tag: 58Y2TF
kind: definition
slug: secular-equation
name: Secular equation
aliases:
- rank-one update equation
- secular function
- characteristic equation of a rank-one modification
area: numerical/eigenproblems
level: advanced
summary: The equation 1 + ρ Σ z_i^2 / (d_i - λ) = 0, whose roots are the eigenvalues of the diagonal plus rank-one matrix D + ρ z z^T. One root lies in each gap between the d_i.
prereqs: [spectral-theorem, eigenvalue]
see_also: [divide-and-conquer-eigensolver, tridiagonal-eigenproblem, cauchy-interlacing-theorem, weyls-inequality, symmetric-eigenproblem, deflation, polynomial-root-finding, singular-value-decomposition]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.4.4 (divide and conquer for the symmetric tridiagonal problem, the rank-one update and its secular equation), Section 8.5 on the related updating problems
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.3.3, Divide-and-Conquer (the secular equation, the solver, Löwner's theorem and the Gu-Eisenstat eigenvectors)
  - paper: "Gene H. Golub, Some modified matrix eigenvalue problems, SIAM Review 15, 1973"
    title: Some modified matrix eigenvalue problems
    locator: SIAM Rev. 15(2) (1973), pp. 318 to 334
  - paper: "James R. Bunch, Christopher P. Nielsen and Danny C. Sorensen, Rank-one modification of the symmetric eigenproblem, Numerische Mathematik 31, 1978"
    title: Rank-one modification of the symmetric eigenproblem
    locator: Numer. Math. 31 (1978), pp. 31 to 48
  - paper: "J. J. M. Cuppen, A divide and conquer method for the symmetric tridiagonal eigenproblem, Numerische Mathematik 36, 1981"
    title: A divide and conquer method for the symmetric tridiagonal eigenproblem
    locator: Numer. Math. 36 (1981), pp. 177 to 195
  - paper: "Ming Gu and Stanley C. Eisenstat, A divide-and-conquer algorithm for the symmetric tridiagonal eigenproblem, SIAM Journal on Matrix Analysis and Applications 16, 1995"
    title: A divide-and-conquer algorithm for the symmetric tridiagonal eigenproblem
    locator: SIAM J. Matrix Anal. Appl. 16(1) (1995), pp. 172 to 191
---

The secular equation is the scalar equation

$$f(\lambda) = 1 + \rho \sum_{i=1}^n \frac{z_i^2}{d_i - \lambda} = 0,$$

whose roots are the eigenvalues of the symmetric matrix $D + \rho z z^T$, a diagonal matrix plus a rank-one term. When the $d_i$ are distinct and every $z_i \ne 0$, $f$ is strictly monotone between its poles, so it has exactly one root in each interval between consecutive $d_i$ and one beyond the last, and the eigenvalues interlace the $d_i$. Each root gives its eigenvector in closed form, $(D - \lambda I)^{-1} z$. Solving $n$ such equations at $O(n)$ flops per function evaluation is the merge step of the [divide-and-conquer eigensolver](/divide-and-conquer-eigensolver/) for the [tridiagonal eigenproblem](/tridiagonal-eigenproblem/). The name comes from celestial mechanics, where "secular equation" once meant the characteristic equation of any symmetric matrix, after the slow (secular) perturbations of planetary orbits.

## Definition

**Notation.** $D = \operatorname{diag}(d_1, \dots, d_n)$ with $d_1 > d_2 > \dots > d_n$, $z \in \mathbb R^n$, and $\rho \ne 0$ real. The eigenvalues of $D + \rho z z^T$ are $\lambda_1 \ge \dots \ge \lambda_n$, with eigenvectors $v_1, \dots, v_n$.

**The secular function** is $f(\lambda) = 1 + \rho z^T (D - \lambda I)^{-1} z = 1 + \rho \sum_i z_i^2 / (d_i - \lambda)$, defined for $\lambda \notin \{d_i\}$.

**Why its roots are the eigenvalues.** For $\lambda$ not equal to any $d_i$,

$$D + \rho z z^T - \lambda I = (D - \lambda I)\bigl(I + \rho (D - \lambda I)^{-1} z z^T\bigr),$$

and $\det(I + x y^T) = 1 + y^T x$, so $\det(D + \rho z z^T - \lambda I) = \prod_i (d_i - \lambda) \cdot f(\lambda)$. So such a $\lambda$ is an eigenvalue exactly when $f(\lambda) = 0$.

**Properties, assuming $d_i$ distinct, all $z_i \ne 0$, and $\rho > 0$.**

1. $f'(\lambda) = \rho \sum_i z_i^2 / (d_i - \lambda)^2 > 0$, so $f$ increases strictly on each interval between poles. It goes from $-\infty$ to $+\infty$ on each $(d_{i+1}, d_i)$, and from $-\infty$ to $1$ on $(d_1, \infty)$. So there is exactly one root in each of $(d_{i+1}, d_i)$ and exactly one in $(d_1, \infty)$, in fact in $(d_1, d_1 + \rho z^T z]$.
2. Interlacing: $d_1 < \lambda_1 \le d_1 + \rho z^T z$ and $d_i < \lambda_i < d_{i-1}$ for $i = 2, \dots, n$. No $d_i$ is an eigenvalue. For $\rho < 0$ the picture is reflected: $\lambda_i \in (d_{i+1}, d_i)$ and $\lambda_n \in [d_n + \rho z^T z, d_n)$.
3. Eigenvectors: $v_i = (D - \lambda_i I)^{-1} z / \|(D - \lambda_i I)^{-1} z\|_2$, since $(D + \rho z z^T)(D - \lambda_i I)^{-1} z = \lambda_i (D - \lambda_i I)^{-1} z + z \, f(\lambda_i)$.
4. Löwner's formula: given numbers $\lambda_i$ that interlace the $d_i$ as in item 2, there is a vector $\hat z$ such that the $\lambda_i$ are exactly the eigenvalues of $D + \rho \hat z \hat z^T$, namely $\hat z_i^2 = \prod_j (\lambda_j - d_i) / \bigl(\rho \prod_{j \ne i} (d_j - d_i)\bigr)$. Gu and Eisenstat (1995) compute the eigenvectors from $\hat z$ instead of $z$, which makes them numerically orthogonal even when computed roots are close to poles.

**Deflation.** If $z_i = 0$, then $d_i$ is an eigenvalue with eigenvector $e_i$, and the index $i$ is removed from $f$. If $d_i = d_j$, a rotation in the plane $(i, j)$ makes one of $z_i, z_j$ zero. In floating point, both tests use tolerances of the order $u \|D + \rho z z^T\|_2$, and they remove a large fraction of the indices in practice.

## Examples and non-examples

**A $3 \times 3$ example.** $d = (3, 2, 1)$, $z = (1, 1, 1)$, $\rho = 1$, so $D + \rho z z^T = \begin{pmatrix} 4 & 1 & 1 \\ 1 & 3 & 1 \\ 1 & 1 & 2 \end{pmatrix}$, with characteristic polynomial $t^3 - 9t^2 + 23t - 17$. The secular function $1 + 1/(3 - \lambda) + 1/(2 - \lambda) + 1/(1 - \lambda)$ has the roots $5.214320 \in (3, 6]$, $2.460811 \in (2, 3)$ and $1.324869 \in (1, 2)$. Their sum is $9$, the trace, and their product is $17$, the determinant. The eigenvector formula gives $v_1 = -(0.755789, 0.520657, 0.397113)$, with residual $4 \times 10^{-16}$ in double precision, and Löwner's formula applied to the computed roots returns $\hat z_i^2 = 1.000000$ for each $i$.

**A non-example: a nonsymmetric rank-one change.** For $D + u w^T$ the same determinant identity gives $1 + \sum_i u_i w_i / (d_i - \lambda) = 0$, but the weights $u_i w_i$ can have both signs, $f$ is not monotone, and the roots can be complex: $\operatorname{diag}(1, -1) + (1, 1)^T (-1, 1)$ has eigenvalues $\pm i$, while $\operatorname{diag}(1, -1)$ is real.

**A non-example: a repeated pole without deflation.** For $d_1 = d_2$ and $z_1, z_2 \ne 0$, the eigenvalue $d_1$ is a root of $\det$ but not of $f$, which only has $n - 1$ distinct poles; the rotation of the deflation step recovers it.

**The SVD form.** For the bidiagonal divide and conquer for the [SVD](/singular-value-decomposition/), the merge step solves $1 + \rho \sum_i z_i^2 / (d_i^2 - \sigma^2) = 0$, a secular equation in $\sigma^2$.

## Related definitions

- **Solving it.** Plain Newton's method fails because $f$ has poles; the standard solvers fit a rational model with one or two poles to $f$ near the target interval (Bunch, Nielsen and Sorensen 1978; Li's "middle way" of 1994; LAPACK `xLAED4`), which converges quadratically and takes a small number of iterations per root in practice. Each evaluation of $f$ costs $O(n)$ flops, so all roots cost $O(n^2)$; with fast multipole methods this falls to $O(n \log n)$ in theory (Gu and Eisenstat).
- **The rank-$k$ form.** For $D + Z R Z^T$ with $Z \in \mathbb R^{n \times k}$, the eigenvalues are where the $k \times k$ matrix $R^{-1} + Z^T (D - \lambda I)^{-1} Z$ is singular, which is the secular equation of a rank-$k$ update.
- **Interlacing.** Properties 1 and 2 are the rank-one case of [Weyl's inequality](/weyls-inequality/) and of [Cauchy interlacing](/cauchy-interlacing-theorem/).
- **Trust regions.** In optimization, the equation $\|(H + \mu I)^{-1} g\|_2 = \Delta$ for the Lagrange multiplier of the trust-region subproblem is also called a secular equation; in the eigenbasis of $H$ it is $\sum_i g_i^2 / (\lambda_i + \mu)^2 = \Delta^2$.
- **Updating and downdating.** Adding or removing a row of a least squares problem, or a rank-one change to a covariance matrix, changes the eigenvalues through the same equation (Golub 1973).

## References
