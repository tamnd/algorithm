---
tag: 3FKDGH
kind: concept
slug: eigenvalue-condition-number
name: Eigenvalue condition number
aliases:
- eigenvalue sensitivity
- condition number of an eigenvalue
area: numerical/eigenproblems
level: advanced
summary: For a simple eigenvalue with unit right and left eigenvectors x and y, κ(λ) = 1/|y*x| bounds the first-order change of λ per unit change of A in the 2-norm. Normal matrices give κ = 1.
prereqs: [eigenvector, condition-number]
see_also: [bauer-fike-theorem, pseudospectrum, schur-decomposition, nonsymmetric-eigenproblem, matrix-balancing, weyls-inequality, jordan-normal-form, davis-kahan-theorem]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.2, Perturbation Theory (eigenvalue sensitivity, the condition of a simple eigenvalue, and eigenvector sensitivity through sep)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.3, Perturbation Theory (condition number of a simple eigenvalue, the spectral projector and the distance to the nearest matrix with a multiple eigenvalue)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 2, Perturbation Theory (the numbers s_i = y_i^T x_i and the bidiagonal example with 20 on the superdiagonal)
  - book: isbn:9780126702309
    title: G. W. Stewart and Ji-guang Sun, Matrix Perturbation Theory, Academic Press, 1990
    locator: Chapter IV, The Perturbation of Eigenvalues, and Chapter V, Invariant Subspaces
  - paper: "J. H. Wilkinson, Note on matrices with a very ill-conditioned eigenproblem, Numerische Mathematik 19, 1972, pp. 176 to 178"
    title: J. H. Wilkinson, Note on matrices with a very ill-conditioned eigenproblem
    locator: the bound on the distance to a matrix with a multiple eigenvalue in terms of the condition number
  - paper: "J. W. Demmel, On condition numbers and the distance to the nearest ill-posed problem, Numerische Mathematik 51, 1987, pp. 251 to 289"
    title: J. W. Demmel, On condition numbers and the distance to the nearest ill-posed problem
    locator: Section on the eigenvalue problem (condition number as reciprocal distance to a defective matrix)
---

The condition number of a simple [eigenvalue](/eigenvalue/) $\lambda$ of $A \in \mathbb{C}^{n \times n}$ is $\kappa(\lambda) = 1/|y^* x|$, where $x$ and $y$ are right and left [eigenvectors](/eigenvector/) for $\lambda$ with $\|x\|_2 = \|y\|_2 = 1$. It is the largest first-order change of $\lambda$ per unit change of $A$ in the 2-norm: $|\delta\lambda| \le \kappa(\lambda) \|E\|_2 + O(\|E\|_2^2)$, and some $E$ attains it. A backward stable eigensolver therefore gives errors near $\kappa(\lambda)\, u\, \|A\|_2$, where $u$ is the unit roundoff. Every eigenvalue of a normal matrix has $\kappa = 1$, while a nonnormal matrix can have values of $10^{12}$ at $n = 20$.

## In plain words

Each eigenvalue has two special directions: the direction that the matrix keeps when it acts from the right, and the one it keeps when it acts from the left. For symmetric matrices the two are the same. For other matrices they can be almost at right angles.

The condition number of the eigenvalue measures that angle. When the two directions agree, a small change in the matrix moves the eigenvalue by about the same small amount. When they are close to perpendicular, the eigenvalue can move by a factor of millions more than the change in the matrix. No program can then compute it accurately, because rounding the input already changes the matrix a little.

A large condition number also warns that the matrix is close to one where two eigenvalues meet.

## The idea

**Notation.** $A \in \mathbb{C}^{n \times n}$ has eigenvalues $\lambda_1, \dots, \lambda_n$, listed in any fixed order (for Hermitian $A$, $\lambda_1 \ge \dots \ge \lambda_n$). For a simple eigenvalue $\lambda$, let $x$ and $y$ satisfy $A x = \lambda x$, $y^* A = \lambda y^*$ and $\|x\|_2 = \|y\|_2 = 1$. Norms are 2-norms, $A^*$ is the conjugate transpose and $u$ is the unit roundoff.

**$y^* x \neq 0$ for a simple eigenvalue.** The null space of $(A - \lambda I)^*$ is spanned by $y$, so the range of $A - \lambda I$ is $y^\perp$. If $y^* x = 0$, then $x = (A - \lambda I) z$ for some $z$, so $(A - \lambda I)^2 z = 0$ while $(A - \lambda I) z \neq 0$. This is a Jordan chain of length 2, and the algebraic multiplicity of $\lambda$ is then at least 2. That contradicts simplicity, so $\kappa(\lambda) = 1/|y^* x|$ is finite. By the Cauchy-Schwarz inequality, $\kappa(\lambda) \ge 1$.

**First-order perturbation.** Let $A(\varepsilon) = A + \varepsilon E$. A simple eigenvalue is a simple root of the [characteristic polynomial](/characteristic-polynomial/), so by the implicit function theorem $\lambda(\varepsilon)$ and a normalized $x(\varepsilon)$ are analytic near $\varepsilon = 0$. Differentiate $A(\varepsilon) x(\varepsilon) = \lambda(\varepsilon) x(\varepsilon)$ at $0$: $E x + A x' = \lambda' x + \lambda x'$. Multiply on the left by $y^*$ and use $y^* A = \lambda y^*$. The terms with $x'$ cancel, and

$$\lambda'(0) = \frac{y^* E x}{y^* x}, \qquad |\lambda'(0)| \le \frac{\|y\|_2 \|E\|_2 \|x\|_2}{|y^* x|} = \kappa(\lambda) \|E\|_2.$$

The perturbation $E = y x^*$ has $\|E\|_2 = 1$ and gives $\lambda'(0) = (y^* y)(x^* x)/(y^* x) = 1/(y^* x)$, so the bound is attained. Thus $\kappa(\lambda)$ is the absolute [condition number](/condition-number/) of $\lambda$ as a function of $A$ in the 2-norm, and in the Frobenius norm also, since $\|y x^*\|_F = 1$. The relative condition number is $\kappa(\lambda) \|A\|_2 / |\lambda|$.

**Spectral projector.** The matrix $P = x y^* / (y^* x)$ is the oblique projector onto $\operatorname{span}(x)$ along the invariant subspace $y^\perp$. Its norm is $\|P\|_2 = \|x\|_2 \|y\|_2 / |y^* x| = \kappa(\lambda)$. So the condition number also measures how far the eigen-decomposition is from orthogonal.

**Schur form.** Let $A = Q T Q^*$ be a [Schur decomposition](/schur-decomposition/) with $\lambda$ first, so $T = \begin{pmatrix} \lambda & t^* \\ 0 & T_{22} \end{pmatrix}$. In these coordinates $x = e_1$, and the left eigenvector is $(1, z^*)$ with $z^* = -t^* (T_{22} - \lambda I)^{-1}$. Hence

$$\kappa(\lambda) = \sqrt{1 + \|t^* (T_{22} - \lambda I)^{-1}\|_2^2} \le \sqrt{1 + \frac{\|t\|_2^2}{\sigma_{\min}(T_{22} - \lambda I)^2}}.$$

The value is large only when the strictly upper part of $T$ is large, or when $\lambda$ is close to the spectrum of $T_{22}$ in the sense of $\sigma_{\min}$. When $t = 0$, as for every normal matrix, $\kappa(\lambda) = 1$. LAPACK's `xTRSNA` uses this formula on the computed Schur form and returns $1/\kappa$ in `S`.

**Relation to the eigenvector matrix.** If $A = V \Lambda V^{-1}$, then column $v_i$ of $V$ and row $w_i^*$ of $V^{-1}$ are right and left eigenvectors with $w_i^* v_i = 1$. Thus $\kappa(\lambda_i) = \|v_i\|_2 \|w_i\|_2 \le \|V\|_2 \|V^{-1}\|_2 = \kappa_2(V)$. The [Bauer-Fike theorem](/bauer-fike-theorem/) uses $\kappa_2(V)$ as one constant for all eigenvalues, holds for every $\|E\|$ and not only to first order. The individual $\kappa(\lambda_i)$ are sharper but describe only small perturbations. For an eigenvector matrix with unit columns, $\|V\|_2 \le \|V\|_F = \sqrt n$ and $\|V^{-1}\|_2 \le \|V^{-1}\|_F \le \sqrt n \max_i \kappa(\lambda_i)$, so $\max_i \kappa(\lambda_i) \le \kappa_2(V) \le n \max_i \kappa(\lambda_i)$ for that scaling.

**Hermitian and normal matrices.** For normal $A$ one can take $y = x$, so $\kappa(\lambda) = 1$ for every simple eigenvalue. For Hermitian $A$ and Hermitian $E$, [Weyl's inequality](/weyls-inequality/) gives $|\lambda_i(A + E) - \lambda_i(A)| \le \|E\|_2$ exactly, for all sizes of $E$ and also for multiple eigenvalues.

**Distance to a multiple eigenvalue.** If $\kappa(\lambda) > 1$, there is an $E$ with

$$\|E\|_2 \le \frac{\|A\|_2}{\sqrt{\kappa(\lambda)^2 - 1}}$$

such that $\lambda$ is a multiple eigenvalue of $A + E$ (Wilkinson 1972). So an ill-conditioned eigenvalue lies close to a matrix where it collides with another one. Demmel (1987) places this inside a general rule: the condition number of a problem is close to the reciprocal of the distance to the nearest ill-posed problem.

**Defective and multiple eigenvalues.** At a multiple eigenvalue the formula does not apply. If the eigenvalue has a single Jordan block of size $m \ge 2$, its right and left eigenvectors satisfy $y^* x = 0$, so one sets $\kappa = \infty$. A change of size $\varepsilon$ can then move the eigenvalue by about $\varepsilon^{1/m}$. The eigenvalue is Hölder continuous with exponent $1/m$, not Lipschitz. See [Jordan normal form](/jordan-normal-form/).

**Eigenvectors and invariant subspaces.** The eigenvector $x$ has a different condition number. In the Schur coordinates above, a perturbation $E$ turns $x$ by an angle of at most about $\|E\|_2 / \operatorname{sep}(\lambda, T_{22})$ to first order, where $\operatorname{sep}(\lambda, T_{22}) = \sigma_{\min}(T_{22} - \lambda I)$. For Hermitian $A$ this is the gap $\min_{j \ne i} |\lambda_i - \lambda_j|$, and the [Davis-Kahan theorem](/davis-kahan-theorem/) makes it a bound valid for all $E$. For a cluster of eigenvalues, the spanned invariant subspace and the mean of the cluster can be well conditioned even when each eigenvalue is not.

**Effect of computation.** The QR algorithm and its relatives are backward stable. They return the exact eigenvalues of $A + E$ with $\|E\|_2 \le p(n)\, u\, \|A\|_2$ for a modest $p(n)$. To first order the error in a simple eigenvalue is then at most $\kappa(\lambda)\, p(n)\, u\, \|A\|_2$. Since $\kappa(\lambda)$ changes under nonunitary similarity, [balancing](/matrix-balancing/) by a diagonal $D$ can reduce $\|D^{-1} A D\|$ and with it the error bound, even though the eigenvalues do not change.

## Examples

**Upper triangular 2 by 2.** For $A = \begin{pmatrix} 1 & t \\ 0 & 2 \end{pmatrix}$, the eigenvalue 1 has $x = e_1$ and $y = (1, -t)^T / \sqrt{1 + t^2}$, so $\kappa(1) = \sqrt{1 + t^2}$. The eigenvalue 2 has $x = (t, 1)^T / \sqrt{1 + t^2}$ and $y = e_2$, and the same $\kappa$. With $t = 100$, $\kappa = 100.005$. A change of $10^{-8}$ in entry $(2, 1)$ moves each eigenvalue by about $10^{-6}$, as the [Bauer-Fike page](/bauer-fike-theorem/) shows.

**A mildly nonnormal 3 by 3.** Let $S = \begin{pmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & 1 \end{pmatrix}$, $S^{-1} = \tfrac12 \begin{pmatrix} 1 & -1 & 1 \\ 1 & 1 & -1 \\ -1 & 1 & 1 \end{pmatrix}$ and $A = S \operatorname{diag}(2, 4, 6) S^{-1}$. Each column of $S$ has norm $\sqrt 2$ and each row of $S^{-1}$ has norm $\sqrt 3 / 2$, so every eigenvalue has $\kappa = \sqrt 6 / 2 \approx 1.2247$. The matrix $S = I + P$ with $P$ a cyclic permutation is normal with eigenvalues $2$, $1 + \omega$ and $1 + \omega^2$, where $\omega = e^{2\pi i/3}$. So $\kappa_2(S) = 2$, larger than every individual $\kappa(\lambda_i)$.

**Wilkinson's bidiagonal matrix.** Let $W$ be the $20 \times 20$ upper bidiagonal matrix with diagonal $20, 19, \dots, 1$ and every superdiagonal entry 20. Its eigenvalues are the integers 1 to 20. Exact back substitution in rational arithmetic gives the condition numbers below. They are symmetric: the value for $\lambda$ equals the value for $21 - \lambda$.

| $\lambda$ | 20, 1 | 19, 2 | 18, 3 | 17, 4 | 16, 5 | 15, 6 | 14, 7 | 13, 8 | 12, 9 | 11, 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\kappa(\lambda)$ | 8.45e7 | 1.46e9 | 1.21e10 | 6.39e10 | 2.42e11 | 6.94e11 | 1.57e12 | 2.84e12 | 4.18e12 | 5.07e12 |

Now add $\varepsilon = 10^{-10}$ in entry $(20, 1)$. The characteristic polynomial becomes $\prod_{k=1}^{20} (z - k) - \varepsilon \cdot 20^{19}$, and $\varepsilon \cdot 20^{19} \approx 5.24 \times 10^{14}$. Its roots, checked by an exact Newton step, are:

- real: 0.9958, 2.1092, 2.5749, 18.4237, 18.8906 and 20.0042;
- complex pairs: $3.9653 \pm 1.0877i$, $5.894 \pm 1.9485i$, $8.1181 \pm 2.5292i$, $10.5 \pm 2.7334i$, $12.8819 \pm 2.5292i$, $15.106 \pm 1.9485i$ and $17.0346 \pm 1.0878i$.

For $\lambda = 20$ the first-order formula gives $\lambda'(0) = y_{20} x_1 / (y^* x) \approx 4.31 \times 10^7$, a predicted shift of $0.00431$. The actual shift is $0.0042$, within the bound $\kappa \varepsilon = 0.0084$. For $\lambda = 10$ and 11 the formula predicts a shift of 398, but the actual eigenvalues moved by less than 3 and left the real axis. The first-order model fails here because $\varepsilon$ is beyond its range. By the symmetry of the polynomial about $z = 10.5$, the eigenvalues 10 and 11 meet at $\varepsilon = \prod_{k=1}^{20} (10.5 - k) / 20^{19} \approx 7.80 \times 10^{-14}$. The bound of Wilkinson (1972) gives a distance of at most $\|W\|_2 / \sqrt{\kappa^2 - 1} < 40 / 5.07 \times 10^{12} \approx 7.9 \times 10^{-12}$ to a matrix with a multiple eigenvalue, which agrees with this.

**Jordan block.** The $10 \times 10$ Jordan block $J$ with eigenvalue 0, plus $\varepsilon = 10^{-10}$ in entry $(10, 1)$, has characteristic polynomial $z^{10} - \varepsilon$. All ten eigenvalues have modulus $\varepsilon^{1/10} = 0.1$, a change $10^9$ times larger than $\varepsilon$. Here $x = e_1$ and $y = e_{10}$, so $y^* x = 0$.

## Where it is used

- **Error bounds for eigensolvers.** LAPACK's expert drivers `xGEEVX` and `xGEESX` return reciprocal condition numbers (`RCONDE` for eigenvalues and `RCONDV` for eigenvectors) so a user can turn a backward error into a forward error bound. See the [nonsymmetric eigenproblem](/nonsymmetric-eigenproblem/).
- **Pseudospectra.** For small $\varepsilon$ the $\varepsilon$-[pseudospectrum](/pseudospectrum/) near a simple $\lambda$ is about a disc of radius $\kappa(\lambda)\, \varepsilon$. Large condition numbers show up as large pseudospectral regions, which matter for transient growth in $\exp(tA)$ and $A^k$.
- **Choice of method.** The value $\kappa = 1$ for Hermitian matrices is one reason symmetric solvers can promise absolute accuracy $O(u \|A\|_2)$ for every eigenvalue. For nonnormal matrices, Schur vectors and invariant subspaces are preferred to eigenvectors.
- **Polynomial roots.** Roots of a polynomial computed as eigenvalues of a companion matrix inherit the condition of the roots in the coefficients. [Wilkinson's polynomial](/wilkinson-polynomial/) is the classical example.
- **Structured and relative perturbation theory.** When $E$ has structure (real, symmetric, sparse, or relative to entries), smaller structured condition numbers replace $\kappa(\lambda)$. These explain the high relative accuracy of [Jacobi's method](/jacobi-eigenvalue-algorithm/) on graded matrices.
- **Generalized problems.** For a simple eigenvalue of a pencil, $A x = \lambda B x$ and $y^* A = \lambda y^* B$ with unit $x$ and $y$, the same differentiation applied to $(A + \varepsilon E) x = \lambda (B + \varepsilon F) x$ gives $\lambda'(0) = y^* (E - \lambda F) x / (y^* B x)$. So $|y^* B x|$ takes the place of $|y^* x|$; see the [generalized eigenvalue problem](/generalized-eigenvalue-problem/).

## References
