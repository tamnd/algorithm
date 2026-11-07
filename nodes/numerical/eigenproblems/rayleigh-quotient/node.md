---
tag: DEK6EN
kind: definition
slug: rayleigh-quotient
name: Rayleigh quotient
aliases:
- Rayleigh quotient of a matrix
- Rayleigh-Ritz quotient
area: numerical/eigenproblems
level: core
summary: ρ(x) = x* A x / x* x for nonzero x. It equals λ at an eigenvector, minimizes the residual for a given x, and for Hermitian A its error is quadratic in the eigenvector error.
prereqs: [eigenvalue, eigenvector, spectral-theorem]
see_also: [rayleigh-quotient-iteration, rayleigh-ritz-method, courant-fischer-theorem, power-iteration, inverse-iteration, weyls-inequality, generalized-eigenvalue-problem, backward-error-analysis]
sources:
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 1, Basic Facts about Self-Adjoint Matrices (the Rayleigh quotient and its stationary points); Chapter 4, Simple Vector Iterations (the residual and the error bounds)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 27, Rayleigh Quotient, Inverse Iteration (the quadratic accuracy of the Rayleigh quotient)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.1, Properties and Decompositions (the variational characterization); Section 8.2, Power Iterations (Rayleigh quotient iteration)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 4.2, Variational characterizations of eigenvalues of Hermitian matrices
---

The Rayleigh quotient of a square matrix $A$ at a nonzero vector $x$ is the number $\rho(x) = x^* A x / x^* x$. When $x$ is an [eigenvector](/eigenvector/) with eigenvalue $\lambda$, $\rho(x) = \lambda$, and for other $x$ it is the scalar $\mu$ that makes the residual $\|A x - \mu x\|_2$ smallest. For a Hermitian (real symmetric) $A$ it lies between the smallest and the largest [eigenvalue](/eigenvalue/), and an error of angle $\theta$ in $x$ gives an error of order $\theta^2$ in $\rho(x)$. That is why [power iteration](/power-iteration/), [Rayleigh quotient iteration](/rayleigh-quotient-iteration/) and the [Rayleigh-Ritz method](/rayleigh-ritz-method/) all use it as their eigenvalue estimate.

## Definition

**Notation.** $A \in \mathbb C^{n \times n}$, $x \in \mathbb C^n$ with $x \ne 0$, $x^*$ the conjugate transpose. For a Hermitian $A$ the eigenvalues are $\lambda_1 \ge \dots \ge \lambda_n$ with orthonormal eigenvectors $v_1, \dots, v_n$ ([spectral theorem](/spectral-theorem/)).

The **Rayleigh quotient** of $A$ at $x$ is

$$\rho(x) = \rho_A(x) = \frac{x^* A x}{x^* x}.$$

For real $A$ and real $x$ this is $x^T A x / x^T x$. The **residual** of $x$ is $r(x) = A x - \rho(x) x$. The set $W(A) = \{\rho(x) : x \ne 0\}$ is the *field of values* (numerical range) of $A$.

**Basic facts.** Each follows in one or two lines from the definition.

1. *Scale invariance.* $\rho(c x) = \rho(x)$ for each nonzero scalar $c$, so $\rho$ is a function of the direction of $x$.
2. *Eigenvectors.* If $A x = \lambda x$ then $\rho(x) = \lambda \, x^* x / x^* x = \lambda$.
3. *Least squares.* For fixed $x$, the function $\mu \mapsto \|A x - \mu x\|_2^2 = \|A x\|^2 - 2 \operatorname{Re}(\bar\mu \, x^* A x) + |\mu|^2 x^* x$ is smallest at $\mu = \rho(x)$, the solution of the normal equation $(x^* x) \mu = x^* A x$. At this $\mu$ the residual is orthogonal to $x$: $x^* r(x) = 0$.
4. *Backward error.* For a unit vector $x$, let $E = -r(x) x^*$. Then $(A + E) x = A x - r(x) = \rho(x) x$, so $(\rho(x), x)$ is an exact eigenpair of $A + E$, with $\|E\|_2 = \|r(x)\|_2$. If $A$ is Hermitian, $E = -(r x^* + x r^*)$ is Hermitian, does the same job because $x^* r = 0$, and also has $\|E\|_2 = \|r\|_2$. With [Weyl's inequality](/weyls-inequality/) this gives an eigenvalue $\lambda_j$ of a Hermitian $A$ with $|\lambda_j - \rho(x)| \le \|r(x)\|_2$.
5. *Bounds for Hermitian A.* Write $x = \sum_i c_i v_i$. Then $\rho(x) = \sum_i \lambda_i |c_i|^2 / \sum_i |c_i|^2$, a weighted mean of the eigenvalues. So $\lambda_n \le \rho(x) \le \lambda_1$, with equality at $v_n$ and at $v_1$. This is the first case of the [Courant-Fischer theorem](/courant-fischer-theorem/).
6. *Stationary points.* For a real symmetric $A$ and real $x \ne 0$, the gradient is $\nabla \rho(x) = \frac{2}{x^T x} \bigl(A x - \rho(x) x\bigr)$. It vanishes exactly when $x$ is an eigenvector.

**Quadratic accuracy for Hermitian A.** Let $\theta$ be the angle between $x$ and the eigenvector $v_j$, and write the unit vector $x / \|x\|$ as $\cos\theta \, v_j + \sin\theta \, w$ (after a phase change of $x$, which does not change $\rho$), with $w$ a unit vector orthogonal to $v_j$. The two cross terms of $\rho(x)$ are $\cos\theta \sin\theta \, (w^* A v_j + v_j^* A w)$. Here $w^* A v_j = \lambda_j w^* v_j = 0$ for each $A$, and $v_j^* A w = (A v_j)^* w = \lambda_j v_j^* w = 0$ because $A^* = A$ and $\lambda_j$ is real. So

$$\rho(x) = \cos^2\theta \, \lambda_j + \sin^2\theta \, \rho(w), \qquad \rho(x) - \lambda_j = \sin^2\theta \, \bigl(\rho(w) - \lambda_j\bigr),$$

and since $\lambda_n \le \rho(w) \le \lambda_1$,

$$|\rho(x) - \lambda_j| \le (\lambda_1 - \lambda_n) \sin^2\theta.$$

An eigenvector correct to $k$ digits gives an eigenvalue correct to about $2k$ digits, relative to the spread $\lambda_1 - \lambda_n$.

**For a nonnormal A the accuracy is only linear.** The step $v_j^* A w = 0$ uses that $v_j$ is also a left eigenvector, which holds for Hermitian and, more generally, normal $A$. In general $\rho(x) - \lambda_j = O(\theta)$ and no better. The *two-sided* Rayleigh quotient $y^* A x / y^* x$, with $y$ an estimate of a left eigenvector, is again second order in the errors of $x$ and $y$.

**Generalized Rayleigh quotient.** For the pencil $A - \lambda B$ with $A$ Hermitian and $B$ Hermitian positive definite, $\rho(x) = x^* A x / x^* B x$. Its stationary values are the eigenvalues of the [generalized eigenvalue problem](/generalized-eigenvalue-problem/) $A x = \lambda B x$.

## Examples and non-examples

**Quadratic accuracy.** Let $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, with $\lambda_1 = 3$, $v_1 = (1, 1)^T / \sqrt 2$ and $\lambda_2 = 1$. At $x = (1, 0)^T$, $\rho(x) = 2$, the midpoint, since $\theta = 45$ degrees. At $x = (1, 0.9)^T$, $\rho(x) = 5.42 / 1.81 = 2.994475\ldots$. The angle to $v_1$ is $\theta = 0.0526$ radians, but the error is $3 - \rho(x) = 0.005525 = 2 \sin^2\theta$, which is the formula above with $\rho(w) = \lambda_2 = 1$.

**Non-example: linear error for a nonsymmetric matrix.** Let $A = \begin{pmatrix} 1 & 1 \\ 0 & 2 \end{pmatrix}$, with the eigenvector $(1, 0)^T$ for $\lambda = 1$. At $x = (1, \varepsilon)^T$, $\rho(x) = (1 + \varepsilon + 2\varepsilon^2) / (1 + \varepsilon^2)$. For $\varepsilon = 10^{-1}, 10^{-2}, 10^{-3}$ the errors $\rho(x) - 1$ are $0.1089$, $0.010099$, $0.0010010$: they shrink like $\varepsilon$, not $\varepsilon^2$.

**The field of values is larger than the spectrum.** For $A = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ the only eigenvalue is $0$, but with $x = (\cos t, e^{i\phi} \sin t)^T$ we get $\rho(x) = e^{i\phi} \cos t \sin t$, so $W(A)$ is the closed disc of radius $1/2$. For a normal matrix, $W(A)$ is the convex hull of the eigenvalues, and for a Hermitian one it is the interval $[\lambda_n, \lambda_1]$.

**Non-example: the zero vector.** $\rho(0)$ is not defined. Codes that normalize $x$ must check for $x = 0$, which happens for example when power iteration meets $A x = 0$.

## Related definitions

- [Rayleigh quotient iteration](/rayleigh-quotient-iteration/): [inverse iteration](/inverse-iteration/) with the shift $\rho(x_k)$, cubically convergent for Hermitian matrices.
- [Rayleigh-Ritz method](/rayleigh-ritz-method/): the matrix analogue, $V^* A V$ for an orthonormal basis $V$ of a subspace; its eigenvalues are the Ritz values.
- [Courant-Fischer theorem](/courant-fischer-theorem/): each $\lambda_k$ of a Hermitian matrix is a min-max of $\rho$ over subspaces.
- [Power iteration](/power-iteration/): uses $\rho(q_k)$ as its eigenvalue estimate, which converges at twice the rate of the vector for a Hermitian $A$.
- [Backward error analysis](/backward-error-analysis/): fact 4 above says that the residual norm is the backward error of the pair $(\rho(x), x)$.

## References
