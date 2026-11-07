---
tag: 9SDATC
kind: theorem
slug: bauer-fike-theorem
name: Bauer-Fike theorem
aliases:
- Bauer-Fike bound
area: numerical/eigenproblems
level: advanced
summary: If A = V Λ V^(-1) is diagonalizable, every eigenvalue of A + E lies within κ(V) ‖E‖ of an eigenvalue of A, in any p-norm. For normal A the bound is ‖E‖ itself.
prereqs: [diagonalization, matrix-norms, condition-number]
see_also: [eigenvalue-condition-number, gershgorin-circle-theorem, pseudospectrum, weyls-inequality, hoffman-wielandt-theorem, schur-decomposition, jordan-normal-form, nonsymmetric-eigenproblem]
sources:
  - paper: doi:10.1007/BF01386217
    title: F. L. Bauer and C. T. Fike, Norms and exclusion theorems, Numerische Mathematik 2, 1960
    locator: pp. 137 to 141 (the exclusion theorem for diagonalizable matrices)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.2.2, Eigenvalue Sensitivity (the Bauer-Fike theorem and the Schur-based bound for non-diagonalizable matrices)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 6.3, Eigenvalue perturbation theorems (the Bauer-Fike theorem and its residual form)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.3, Perturbation Theory (the Bauer-Fike theorem and its relation to the condition numbers of single eigenvalues)
  - book: isbn:9780126702309
    title: G. W. Stewart and Ji-guang Sun, Matrix Perturbation Theory, Academic Press, 1990
    locator: Chapter IV, The Perturbation of Eigenvalues (Section 3 on diagonalizable matrices)
---

The Bauer-Fike theorem bounds how far the eigenvalues of a diagonalizable matrix can move under a perturbation. If $A = V \Lambda V^{-1}$ with $\Lambda$ diagonal, then every eigenvalue $\mu$ of $A + E$ satisfies $\min_i |\mu - \lambda_i| \le \kappa_p(V) \|E\|_p$, where $\kappa_p(V) = \|V\|_p \|V^{-1}\|_p$ is the [condition number](/condition-number/) of the eigenvector matrix. For a normal matrix one can take $V$ unitary, and the bound is just $\|E\|_2$. For a non-normal matrix with nearly parallel eigenvectors, $\kappa(V)$ is large, and the eigenvalues can be very sensitive. The theorem also bounds the error of an approximate eigenvalue by its residual, the basic a posteriori test of eigenvalue codes.

## Statement

Let $A \in \mathbb{C}^{n \times n}$ be diagonalizable, $A = V \Lambda V^{-1}$ with $\Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n)$ and $V$ nonsingular. Let $\|\cdot\|$ be a matrix norm induced by a vector norm such that $\|D\| = \max_i |d_i|$ for every diagonal $D$; every $p$-norm, $1 \le p \le \infty$, has this property ([matrix norms](/matrix-norms/)). Let $\kappa(V) = \|V\| \, \|V^{-1}\|$.

1. **Perturbation form.** For every $E \in \mathbb{C}^{n \times n}$ and every eigenvalue $\mu$ of $A + E$,
$$\min_{1 \le i \le n} |\mu - \lambda_i| \le \kappa(V) \, \|E\| .$$
2. **Residual form.** For every $\mu \in \mathbb{C}$ and every vector $x$ with $\|x\| = 1$,
$$\min_{1 \le i \le n} |\mu - \lambda_i| \le \kappa(V) \, \|A x - \mu x\| .$$
3. **Counting.** Let $D_i$ be the closed disc with centre $\lambda_i$ and radius $\kappa(V) \|E\|$. If the union of $k$ of these discs is disjoint from the union of the others, it contains exactly $k$ eigenvalues of $A + E$, counted with algebraic multiplicity.
4. **Normal matrices.** If $A$ is normal, $V$ can be chosen unitary, and in the 2-norm $\min_i |\mu - \lambda_i| \le \|E\|_2$ and $\min_i |\mu - \lambda_i| \le \|A x - \mu x\|_2$ for $\|x\|_2 = 1$.

The bound holds for every choice of $V$; since the columns of $V$ can be scaled, the best constant is $\inf \kappa(V)$ over all eigenvector matrices of $A$.

## In plain words

When you change a matrix a little, its eigenvalues change too. For some matrices they change by about as much as the matrix did. For others they change far more. The theorem says what decides this: the eigenvectors. If the eigenvectors are close to perpendicular, the eigenvalues are safe. If two eigenvectors point in almost the same direction, the eigenvalues can jump a lot.

The theorem also gives a test for a computed answer. Multiply the matrix by the computed vector and compare with the computed number times the vector. The difference, scaled by the same eigenvector factor, bounds how far the number is from a true eigenvalue.

## Proof

**Part 1.** If $\mu$ equals some $\lambda_i$, there is nothing to prove. Otherwise $\mu I - \Lambda$ is nonsingular. Since $\mu$ is an eigenvalue of $A + E$, the matrix $\mu I - A - E$ is singular, and so is
$$V^{-1}(\mu I - A - E) V = (\mu I - \Lambda) - V^{-1} E V = (\mu I - \Lambda)\left(I - (\mu I - \Lambda)^{-1} V^{-1} E V\right).$$
So $I - F$ is singular for $F = (\mu I - \Lambda)^{-1} V^{-1} E V$. Then $F y = y$ for some $y \ne 0$, and $\|F\| \ge 1$. Hence
$$1 \le \|(\mu I - \Lambda)^{-1}\| \, \|V^{-1}\| \, \|E\| \, \|V\| = \frac{\kappa(V)\|E\|}{\min_i |\mu - \lambda_i|},$$
using $\|(\mu I - \Lambda)^{-1}\| = \max_i 1/|\mu - \lambda_i|$ for the diagonal matrix. $\square$

**Part 2.** Let $r = A x - \mu x$ and $E = -r x^\dagger$, where $x^\dagger$ is a dual functional of $x$: a linear functional with $x^\dagger x = 1$ and dual norm 1 (it exists by the Hahn-Banach theorem; in the 2-norm, $x^\dagger = x^*$). Then $(A + E) x = A x - r = \mu x$, so $\mu$ is an eigenvalue of $A + E$, and $\|E\| = \|r\| \, \|x^\dagger\|_* = \|r\|$. Apply part 1. $\square$

**Part 3.** Let $A(t) = A + tE$ for $t \in [0, 1]$. By part 1, every eigenvalue of $A(t)$ lies in the union of the discs of radius $t \kappa(V) \|E\|$, so in $\bigcup_i D_i$. Let $\mathcal{U}$ be the union of the $k$ chosen discs and $\mathcal{W}$ the union of the others. Since the eigenvalues of $A(t)$ depend continuously on $t$ and never enter the gap between the disjoint compact sets $\mathcal{U}$ and $\mathcal{W}$, the number of eigenvalues in $\mathcal{U}$ is constant in $t$. This is the same argument as in part 3 of the [Gershgorin theorem](/gershgorin-circle-theorem/). At $t = 0$ it is $k$, so it is $k$ at $t = 1$. $\square$

**Part 4.** A normal matrix is unitarily diagonalizable, $A = Q \Lambda Q^*$ with $Q$ unitary (by the [Schur decomposition](/schur-decomposition/)), and $\kappa_2(Q) = 1$. $\blacksquare$

## Consequences

- **Hermitian eigenvalues are well conditioned.** For Hermitian $A$ and any $E$, every eigenvalue of $A + E$ is within $\|E\|_2$ of an eigenvalue of $A$. For Hermitian $E$, [Weyl's inequality](/weyls-inequality/) says more: the $k$-th eigenvalues of $A$ and $A + E$ in sorted order differ by at most $\|E\|_2$.
- **A posteriori error bounds.** Every eigenvalue code can check its output $(\mu, x)$ by the residual. For normal $A$ the eigenvalue error is at most $\|r\|_2$. For a general $A$ it is at most $\kappa(V)\|r\|$. For Hermitian $A$ and $\mu = \rho(x)$, the error is at most $\|r\|_2^2 / \text{gap}$, a quadratic bound.
- **Backward stable methods.** A backward stable method computes the exact eigenvalues of $A + E$ with $\|E\| = O(u \|A\|)$. So its computed eigenvalues are within $O(\kappa(V) u \|A\|)$ of true ones. The [QR algorithm](/qr-algorithm/) is an example.
- **Pseudospectra.** In the 2-norm, the $\varepsilon$-[pseudospectrum](/pseudospectrum/) $\{z : \|(zI - A)^{-1}\|_2 \ge 1/\varepsilon\}$ is the set of eigenvalues of all $A + E$ with $\|E\|_2 \le \varepsilon$. By part 1 it lies in the union of the discs of radius $\varepsilon \kappa_2(V)$ about the eigenvalues.
- **Single eigenvalues.** For a simple eigenvalue $\lambda_i$ with unit right and left eigenvectors $x_i$ and $y_i$, the first-order change is $|\delta \lambda_i| \le \|E\|_2 / |y_i^* x_i|$. The factor $1/|y_i^* x_i|$ is the [eigenvalue condition number](/eigenvalue-condition-number/) of $\lambda_i$. With the columns of $V$ scaled to unit length, $1/|y_i^* x_i| \le \kappa_2(V)$. So Bauer-Fike is a global, worst-case version of the individual bounds.
- **Non-diagonalizable matrices.** If $A = Q(D + N)Q^*$ is a Schur decomposition with $D$ diagonal, $N$ strictly upper triangular, and $N^p = 0$, then every eigenvalue $\mu$ of $A + E$ satisfies $\min_i |\mu - \lambda_i| \le \max(\theta, \theta^{1/p})$ with $\theta = \|E\|_2 \sum_{k=0}^{p-1} \|N\|_2^k$ (Golub and Van Loan, Section 7.2.2). For a Jordan block of order $p$ the $p$-th root is attained.

## Tightness

- **Normal matrices.** For $E = \varepsilon I$, every eigenvalue moves by exactly $\varepsilon = \|E\|_2$, and $\kappa_2(V) = 1$, so part 4 is attained.
- **Non-normal matrices, attained up to a factor of 2.** Let $A = \begin{pmatrix} 1 & t \\ 0 & 2 \end{pmatrix}$ with $t = 100$, with eigenvectors $(1, 0)^T$ and $(t, 1)^T$. With unit columns, $\kappa_2(V) = 200.005$. For $E = \begin{pmatrix} 0 & 0 \\ \delta & 0 \end{pmatrix}$ with $\delta = 10^{-8}$, the characteristic polynomial of $A + E$ is $(1 - z)(2 - z) - t\delta$. So the eigenvalue 1 moves to $(3 - \sqrt{1 + 4t\delta})/2$, a change of $1.0 \times 10^{-6} = t \delta$, a hundred times $\|E\|_2$. The bound of part 1 gives $2.0 \times 10^{-6}$. The individual condition number of the eigenvalue 1 is $\sqrt{1 + t^2} = 100.005$, which predicts the change to first order.
- **Diagonalizability is needed.** The Jordan block $J$ of order $n$ with eigenvalue 0 has no eigenvector basis. $J + \varepsilon e_n e_1^T$ has the eigenvalues $\varepsilon^{1/n} e^{2\pi i k/n}$, which move by $\varepsilon^{1/n} \gg \varepsilon$. No bound of the form $C \|E\|$ holds. Matrices close to $J$ are diagonalizable but have $\kappa(V) \to \infty$.
- **The constant can be pessimistic for single eigenvalues.** $\kappa(V)$ is governed by the worst-conditioned eigenvalue. A well-conditioned eigenvalue of a matrix that has an ill-conditioned cluster elsewhere moves much less than $\kappa(V)\|E\|$. The individual condition numbers, or pseudospectra, then give sharper information.

## History

Friedrich L. Bauer and C. T. Fike published the theorem in 1960, in a paper on norms and exclusion theorems, which are results that exclude regions of the complex plane from containing eigenvalues. It belongs to the same family as the [Gershgorin theorem](/gershgorin-circle-theorem/). Wilkinson's 1965 book put the condition of the eigenvector matrix, and the condition numbers $1/|y_i^* x_i|$ of single eigenvalues, at the centre of the error analysis of eigenvalue algorithms. The later theory of pseudospectra, developed by Trefethen and others from the 1990s, refines the theorem for strongly non-normal matrices.

## References
