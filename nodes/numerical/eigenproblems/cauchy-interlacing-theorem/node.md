---
tag: XG2R64
kind: theorem
slug: cauchy-interlacing-theorem
name: Cauchy interlacing theorem
aliases:
- interlacing eigenvalues
- Cauchy interlace theorem
- Poincaré separation theorem
area: numerical/eigenproblems
level: advanced
summary: The eigenvalues of a Hermitian matrix and of a principal submatrix of order n − 1 alternate, λ_1 ≥ μ_1 ≥ λ_2 ≥ ... ≥ μ_(n−1) ≥ λ_n, and the same holds for compressions U*AU.
prereqs: [courant-fischer-theorem, spectral-theorem]
see_also: [weyls-inequality, sturm-sequence-eigenvalue-count, lanczos-algorithm, rayleigh-ritz-method, divide-and-conquer-eigensolver, secular-equation, bisection-eigenvalue-algorithm, positive-definite-matrix]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 4.3, Eigenvalue inequalities for Hermitian matrices (interlacing for bordered matrices and principal submatrices, and the converse)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 10, Approximations from a Subspace (the Cauchy interlace theorem and its corollaries)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.1.2, Eigenvalue Sensitivity (the interlacing property and rank-one updates)
  - book: isbn:9780387948461
    title: Rajendra Bhatia, Matrix Analysis, Graduate Texts in Mathematics 169, Springer, 1997
    locator: Chapter III, Variational Principles for Eigenvalues (Section III.1, the interlacing theorem)
  - paper: "A. L. Cauchy, Sur l'équation à l'aide de laquelle on détermine les inégalités séculaires des mouvements des planètes, Exercices de mathématiques 4, 1829"
    title: A. L. Cauchy, Sur l'équation à l'aide de laquelle on détermine les inégalités séculaires des mouvements des planètes
    locator: the separation of the roots of the secular equation of a symmetric system and its bordered subsystem
  - paper: "K. Fan and G. Pall, Imbedding conditions for Hermitian and normal matrices, Canadian Journal of Mathematics 9, 1957, pp. 298 to 304"
    title: K. Fan and G. Pall, Imbedding conditions for Hermitian and normal matrices
    locator: the converse, every interlacing pair of sequences is realized by a bordered matrix
---

The Cauchy interlacing theorem says that deleting one row and the same column of a Hermitian matrix moves its eigenvalues only within the gaps between them. If $A$ has the eigenvalues $\lambda_1 \ge \dots \ge \lambda_n$ and the principal submatrix $B$ of order $n - 1$ has $\mu_1 \ge \dots \ge \mu_{n-1}$, then $\lambda_k \ge \mu_k \ge \lambda_{k+1}$ for every $k$. More generally, the eigenvalues of any compression $U^* A U$ with orthonormal columns lie between eigenvalues of $A$ in the same way. The theorem underlies the Sturm sequence count of [bisection](/bisection-eigenvalue-algorithm/), the monotone convergence of Ritz values in the [Lanczos algorithm](/lanczos-algorithm/), and the rank-one update step of [divide and conquer](/divide-and-conquer-eigensolver/).

## Statement

Let $A \in \mathbb{C}^{n \times n}$ be Hermitian with eigenvalues $\lambda_1 \ge \dots \ge \lambda_n$.

1. **Principal submatrix.** If $B$ is obtained from $A$ by deleting row $i$ and column $i$, and $B$ has the eigenvalues $\mu_1 \ge \dots \ge \mu_{n-1}$, then
$$\lambda_1 \ge \mu_1 \ge \lambda_2 \ge \mu_2 \ge \dots \ge \lambda_{n-1} \ge \mu_{n-1} \ge \lambda_n .$$
2. **Compression.** If $U \in \mathbb{C}^{n \times m}$ has orthonormal columns and $B = U^* A U$ has the eigenvalues $\mu_1 \ge \dots \ge \mu_m$, then $\lambda_k \ge \mu_k \ge \lambda_{k + n - m}$ for $k = 1, \dots, m$. A principal submatrix of order $m$ is the case where the columns of $U$ are $m$ columns of $I$.
3. **Strictness.** Write $A = \begin{pmatrix} B & b \\ b^* & a \end{pmatrix}$ (after a symmetric permutation) and $B = W \operatorname{diag}(\mu_j) W^*$ with $W$ unitary. If the $\mu_j$ are distinct and every component of $W^* b$ is nonzero, all inequalities in part 1 are strict.
4. **Converse (Fan and Pall).** For any real numbers with $\lambda_1 \ge \mu_1 \ge \lambda_2 \ge \dots \ge \mu_{n-1} \ge \lambda_n$, there is a real symmetric $A$ of order $n$, in fact a bordered diagonal matrix, whose eigenvalues are the $\lambda_k$ and whose leading principal submatrix of order $n - 1$ has the eigenvalues $\mu_k$.

## In plain words

Take a symmetric matrix and remove one row and the matching column. The smaller matrix has one eigenvalue fewer. The theorem says that its eigenvalues sit in the gaps between the old ones: one in each gap, and never outside the old range. So the old and the new eigenvalues alternate on the number line.

This is useful because it holds for every row you remove, and also when you look at the matrix only on a smaller set of directions. Methods that approximate eigenvalues from a smaller subspace can therefore never overshoot.

## Proof

**Part 2 (from Courant-Fischer).** For $y \ne 0$, $\rho_B(y) = y^* U^* A U y / y^* y = \rho_A(U y)$, because $\|U y\|_2 = \|y\|_2$. The map $T \mapsto U T$ sends subspaces of $\mathbb{C}^m$ of dimension $k$ to some of the subspaces of $\mathbb{C}^n$ of dimension $k$. By the max-min form of the [Courant-Fischer theorem](/courant-fischer-theorem/),
$$\mu_k = \max_{\dim T = k} \min_{0 \ne y \in T} \rho_A(U y) \le \max_{\dim S = k} \min_{0 \ne x \in S} \rho_A(x) = \lambda_k,$$
as a maximum over fewer subspaces. By the min-max form, $\mu_k = \min_{\dim T = m - k + 1} \max_{y \in T} \rho_A(U y)$. The subspaces $U T$ have dimension $m - k + 1 = n - (k + n - m) + 1$, so the same comparison gives $\mu_k \ge \lambda_{k + n - m}$. $\square$

**Part 1.** Take $U = [e_1, \dots, e_{i-1}, e_{i+1}, \dots, e_n]$ and $m = n - 1$ in part 2. $\square$

**Part 3 (the secular equation).** Let $c = W^* b$ and conjugate $A$ by $\operatorname{diag}(W, 1)$; this gives the arrowhead matrix $\begin{pmatrix} \operatorname{diag}(\mu) & c \\ c^* & a \end{pmatrix}$ with the eigenvalues of $A$. By the Schur complement, for $\lambda$ not equal to any $\mu_j$,
$$\det(\lambda I - A) = \prod_{j}(\lambda - \mu_j) \cdot f(\lambda), \qquad f(\lambda) = \lambda - a - \sum_{j=1}^{n-1} \frac{|c_j|^2}{\lambda - \mu_j}.$$
If all $c_j \ne 0$ and the $\mu_j$ are distinct, then no $\mu_j$ is an eigenvalue: the polynomial $\det(\lambda I - A)$ at $\lambda = \mu_j$ equals $-|c_j|^2 \prod_{i \ne j}(\mu_j - \mu_i) \ne 0$. The function $f$ has $f'(\lambda) = 1 + \sum_j |c_j|^2 / (\lambda - \mu_j)^2 > 0$, so it increases strictly on each interval between consecutive poles, from $-\infty$ to $+\infty$, and also on $(\mu_1, \infty)$ and $(-\infty, \mu_{n-1})$. So it has exactly one root in each of the $n$ open intervals $(\mu_1, \infty)$, $(\mu_2, \mu_1)$, ..., $(-\infty, \mu_{n-1})$, and these are the $n$ eigenvalues of $A$. $\square$

**Part 4 (sketch).** For strict interlacing, set $B = \operatorname{diag}(\mu)$, $a = \sum_k \lambda_k - \sum_j \mu_j$, and choose
$$|c_j|^2 = -\frac{\prod_k (\mu_j - \lambda_k)}{\prod_{i \ne j} (\mu_j - \mu_i)} .$$
The strict interlacing makes the right side positive. With these values, the polynomial $\prod_j(\lambda - \mu_j) f(\lambda)$ and $\prod_k(\lambda - \lambda_k)$ are monic of degree $n$, agree at the $n - 1$ points $\mu_j$, and have the same coefficient of $\lambda^{n-1}$, so they are equal. The case of equalities follows by a limit or by splitting off common values. $\blacksquare$

## Consequences

- **Sturm sequences.** For an unreduced symmetric tridiagonal $T$, the leading blocks $T_1, T_2, \dots, T_n$ have strictly interlacing eigenvalues. So the signs of the leading minors $\det(T_i - x I)$ change exactly $c(x)$ times, where $c(x)$ is the number of eigenvalues below $x$. This is the [Sturm sequence count](/sturm-sequence-eigenvalue-count/) that bisection uses. The same argument shows that an unreduced symmetric tridiagonal matrix has distinct eigenvalues.
- **Ritz values.** The Ritz values of $A$ on any $m$-dimensional subspace interlace the eigenvalues of $A$ in the sense of part 2. In the Lanczos algorithm $T_k$ is the leading block of $T_{k+1}$, so the Ritz values of consecutive steps interlace, and the extreme ones move monotonically outward ([Rayleigh-Ritz method](/rayleigh-ritz-method/)).
- **Rank-one updates.** If $\rho > 0$, the eigenvalues $\lambda_i'$ of $A + \rho z z^*$ satisfy $\lambda_1' \ge \lambda_1 \ge \lambda_2' \ge \lambda_2 \ge \dots \ge \lambda_n' \ge \lambda_n$, and $\sum_i (\lambda_i' - \lambda_i) = \rho \|z\|_2^2$. Each updated eigenvalue is a root of the [secular equation](/secular-equation/) $1 + \rho \sum_j |w_j|^2/(\lambda_j - \lambda) = 0$, with $w$ the coordinates of $z$ in the eigenvectors of $A$, one in each gap. Divide and conquer solves exactly this equation.
- **Multiplicities.** An eigenvalue of multiplicity $p$ of $A$ is an eigenvalue of multiplicity at least $p - 1$ of every principal submatrix of order $n - 1$, and of multiplicity at least $p - (n - m)$ of every principal submatrix of order $m$.
- **Positive definiteness.** If all leading principal minors of a Hermitian matrix are positive, then by induction each leading block has all eigenvalues positive: interlacing leaves at most one eigenvalue of the next block below the smallest one of the previous block, and the positive determinant rules out a single negative eigenvalue. This is Sylvester's criterion for [positive definite](/positive-definite-matrix/) matrices.
- **Graphs.** The adjacency eigenvalues of an induced subgraph interlace those of the graph. Huang used this, for a signed adjacency matrix of the hypercube, in his 2019 proof of the sensitivity conjecture.

## Tightness

- **A worked example.** $T_4 = \operatorname{tridiag}(-1, 2, -1)$ of order 4 has the eigenvalues 3.618034, 2.618034, 1.381966 and 0.381966, and its leading block $T_3$ has $2 + \sqrt{2} = 3.414214$, 2 and $2 - \sqrt{2} = 0.585786$. They interlace strictly: $3.618034 > 3.414214 > 2.618034 > 2 > 1.381966 > 0.585786 > 0.381966$, as part 3 predicts for an unreduced tridiagonal matrix.
- **Equality.** If $b = 0$, then $A = \operatorname{diag}(B, a)$, the $\mu_k$ are among the $\lambda_k$, and one $\lambda$ equals $a$; then some inequalities are equalities. So part 1 cannot be made strict without a condition like that of part 3.
- **Hermitian is needed.** $A = \begin{pmatrix} 3 & 1 \\ -4 & -1 \end{pmatrix}$ has trace 2 and determinant 1, so both eigenvalues equal 1, while the principal submatrix $(3)$ has the eigenvalue 3. That lies outside $[\lambda_2, \lambda_1] = [1, 1]$.
- **The index shift in part 2 is sharp.** For $A = \operatorname{diag}(1, 0, \dots, 0, -1)$ and $U = [e_2, \dots, e_{m+1}]$ with $m \le n - 2$, every $\mu_k = 0$. That equals $\lambda_k = 0$ for $2 \le k \le m$, and also $\lambda_{k + n - m} = 0$ for $k + n - m \le n - 1$. So for $2 \le k \le m - 1$ both bounds are attained.

## History

Cauchy proved the separation of the roots in 1829. He studied the secular equation of Lagrange and Laplace for the perturbations of planetary orbits, comparing a symmetric system with the system obtained by deleting one variable. Poincaré (1890) gave the separation theorem for compressions, which is why part 2 is also called the Poincaré separation theorem. After Fischer (1905) and Courant (1920), the theorem became a corollary of the min-max principle. Fan and Pall (1957) proved the converse. Short direct proofs were later given by Hwang (2004) and Fisk (2005).

## References
