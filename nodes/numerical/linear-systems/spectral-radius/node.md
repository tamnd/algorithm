---
tag: PM2GGS
kind: definition
slug: spectral-radius
name: Spectral radius
aliases:
- rho(A)
- Gelfand formula
area: numerical/linear-systems
level: core
summary: Largest absolute eigenvalue; an iteration converges exactly when it is below 1.
prereqs: [eigenvalue, matrix-norms]
see_also: [matrix-splitting, neumann-series, jacobi-method, successive-over-relaxation, power-iteration, perron-frobenius-theorem, gershgorin-circle-theorem, pseudospectrum]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 5.6, Matrix norms (the bound of the spectral radius by every matrix norm, the norm within ε of the spectral radius, the convergence of A^k to 0, and the formula ρ(A) = lim ||A^k||^(1/k))
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 17, Stationary Iterative Methods (convergence when ρ(M^-1 N) < 1); Chapter 18, Matrix Powers (the transient behavior of ||A^k|| for nonnormal A, and powers in floating point)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 1.11, Perron-Frobenius theory and the spectral radius; Section 4.2.1, the general convergence result for stationary iterations
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 6.5, Basic Iterative Methods (the iteration matrix, the rate of convergence measured by the spectral radius, and the model problem)
---

The spectral radius $\rho(A)$ of a square matrix is the largest modulus of its eigenvalues. It decides the fate of the powers $A^k$: they tend to zero exactly when $\rho(A) < 1$, and in each norm $\|A^k\|^{1/k} \to \rho(A)$. So it is the quantity that decides whether a [stationary iterative method](/matrix-splitting/) converges, and how fast in the long run. It is a lower bound for each consistent [matrix norm](/matrix-norms/), but it is not itself a norm, and for a nonnormal matrix it says nothing about the first steps of an iteration.

## Definition

Let $A \in \mathbb{C}^{n \times n}$ (in particular a real matrix) with eigenvalues $\lambda_1, \ldots, \lambda_n$, which may be complex even when $A$ is real. The *spectral radius* is

$$\rho(A) = \max_{1 \le i \le n} |\lambda_i|.$$

For a stationary iteration $x_{k+1} = G x_k + c$ with *iteration matrix* $G$, the *asymptotic rate of convergence* is $R_\infty(G) = -\log_{10} \rho(G)$: about $1/R_\infty$ steps are needed for each decimal digit, in the long run.

**Facts.** For each $A \in \mathbb{C}^{n \times n}$ (Horn and Johnson, Section 5.6):

1. $\rho(A) \le \|A\|$ for each consistent matrix norm. The proof is on the page [matrix norms](/matrix-norms/).
2. For each $\varepsilon > 0$ there is an induced norm with $\|A\| \le \rho(A) + \varepsilon$.
3. $A^k \to 0$ as $k \to \infty$ if and only if $\rho(A) < 1$.
4. (Gelfand's formula) $\rho(A) = \lim_{k \to \infty} \|A^k\|^{1/k}$ in each matrix norm.

*Proof of 2.* By the Schur decomposition $A = Q T Q^*$, with $Q$ unitary and $T$ upper triangular with the eigenvalues on its diagonal. Let $D_t = \operatorname{diag}(1, t, t^2, \ldots, t^{n-1})$ with $t > 0$. Then $(D_t^{-1} T D_t)_{ij} = t^{j-i} t_{ij}$, so the diagonal is unchanged and the entries above it are multiplied by positive powers of $t$. For small $t$, the largest row sum of $|D_t^{-1} T D_t|$ is at most $\rho(A) + \varepsilon$. The norm $\|X\| = \|D_t^{-1} Q^* X Q D_t\|_\infty$ is induced by the vector norm $\|D_t^{-1} Q^* x\|_\infty$, and $\|A\| = \|D_t^{-1} T D_t\|_\infty \le \rho(A) + \varepsilon$. $\square$

*Proof of 3.* If $\rho(A) < 1$, choose $\varepsilon = (1 - \rho(A))/2$ in fact 2: then $\|A^k\| \le \|A\|^k \le (\rho(A) + \varepsilon)^k \to 0$. If $\rho(A) \ge 1$, let $A v = \lambda v$ with $|\lambda| \ge 1$ and $v \ne 0$; then $A^k v = \lambda^k v$ does not tend to $0$, so $A^k$ does not. $\square$

*Proof of 4.* By fact 1 applied to $A^k$, whose eigenvalues are the $\lambda_i^k$, $\rho(A)^k = \rho(A^k) \le \|A^k\|$. For $\varepsilon > 0$, the matrix $B = A/(\rho(A) + \varepsilon)$ has $\rho(B) < 1$, so $B^k \to 0$ by fact 3, and $\|A^k\| \le (\rho(A) + \varepsilon)^k$ for all large $k$. So $\rho(A) \le \|A^k\|^{1/k} \le \rho(A) + \varepsilon$ for large $k$. $\square$

**Consequence for iterations.** The error of $x_{k+1} = G x_k + c$ with fixed point $x$ satisfies $e_k = G^k e_0$. By fact 3, the iteration converges for each $x_0$ and each $c$ exactly when $\rho(G) < 1$. By fact 4, $\|e_k\| \le C_\varepsilon (\rho(G) + \varepsilon)^k \|e_0\|$ for each $\varepsilon > 0$, and for some $e_0$ no faster decay holds. This is the base of the theory of the [Jacobi](/jacobi-method/), [Gauss-Seidel](/gauss-seidel-method/) and [SOR](/successive-over-relaxation/) methods, and of the [Neumann series](/neumann-series/) $\sum G^k$.

## Examples and non-examples

**The model problem.** For $T_n = \operatorname{tridiag}(-1, 2, -1)$, the [Jacobi](/jacobi-method/) iteration matrix $G_J = I - T_n/2$ has eigenvalues $\cos(k\pi/(n+1))$, so $\rho(G_J) = \cos(\pi/(n+1))$. For $n = 10$ this is about $0.9595$, with $R_\infty \approx 0.0180$, so about $56$ steps for each decimal digit. The Gauss-Seidel matrix has $\rho = \cos^2(\pi/(n+1)) \approx 0.9206$, exactly the square, so Gauss-Seidel needs half as many steps; this relation holds for each consistently ordered matrix (see [SOR](/successive-over-relaxation/)). As $n$ grows, $\rho(G_J) \approx 1 - \pi^2/(2(n+1)^2)$, and the number of steps grows like $n^2$.

**Symmetric and normal matrices.** If $A$ is normal ($A^* A = A A^*$), in particular symmetric, then $\rho(A) = \|A\|_2$ and $\|A^k\|_2 = \rho(A)^k$ for each $k$, so the spectral radius describes every step, not only the limit.

**Transient growth.** $A = \begin{pmatrix} 0.9 & 1 \\ 0 & 0.9 \end{pmatrix}$ has $\rho(A) = 0.9$, and $A^k = \begin{pmatrix} 0.9^k & k\, 0.9^{k-1} \\ 0 & 0.9^k \end{pmatrix}$. So $\|A^k\|_\infty = 0.9^k + k\, 0.9^{k-1}$ is $1.9$ at $k = 1$, about $4.26$ at its peak at $k = 9$, $2.82$ at $k = 20$ and $0.0030$ at $k = 100$. An iteration with this matrix gets worse for nine steps before it converges. For larger nonnormal matrices the hump can exceed the precision, and the [pseudospectrum](/pseudospectrum/) describes the transient better than $\rho$ (Higham, Chapter 18).

**Nonnegative matrices.** For $A \ge 0$ entrywise, the [Perron-Frobenius theorem](/perron-frobenius-theorem/) gives an eigenvalue equal to $\rho(A)$ with a nonnegative eigenvector, and $\min_i \sum_j a_{ij} \le \rho(A) \le \max_i \sum_j a_{ij}$. This is used to compare the Jacobi and Gauss-Seidel methods on M-matrices.

**Bounds without eigenvalues.** By the [Gershgorin circle theorem](/gershgorin-circle-theorem/), $\rho(A) \le \max_i \sum_j |a_{ij}| = \|A\|_\infty$. For a strictly [diagonally dominant](/diagonally-dominant-matrix/) $A$, the Jacobi matrix $G_J = I - D^{-1}A$ has $\|G_J\|_\infty < 1$, so Jacobi converges.

**Non-example: not a norm.** $N = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ has $\rho(N) = 0$ though $N \ne 0$, and $\rho(N + N^T) = 1 > \rho(N) + \rho(N^T)$. Also $\rho(AB) = \rho(BA)$ always, but $\rho(AB) \le \rho(A)\rho(B)$ fails: for $A = N$ and $B = N^T$, $\rho(N N^T) = 1$.

**Non-example: a norm below one is sufficient, not necessary.** $A = \begin{pmatrix} 0.5 & 2 \\ 0 & 0.5 \end{pmatrix}$ has $\|A\|_1 = \|A\|_\infty = 2.5$ but $\rho(A) = 0.5$, so $A^k \to 0$ although these norms are above one.

**Computing it.** For a small dense matrix, compute all eigenvalues by the [QR algorithm](/qr-algorithm/). For a large sparse one, [power iteration](/power-iteration/) estimates $\rho(A)$ when one eigenvalue of largest modulus dominates; it converges like $(|\lambda_2|/|\lambda_1|)^k$.

## Related definitions

- [Eigenvalue](/eigenvalue/): $\rho$ is the largest eigenvalue modulus.
- [Matrix norms](/matrix-norms/): each consistent norm is an upper bound for $\rho$.
- [Matrix splitting](/matrix-splitting/): the iteration matrix $M^{-1}N$ of a splitting converges exactly when its spectral radius is below one.
- [Neumann series](/neumann-series/): $\sum_k G^k$ converges exactly when $\rho(G) < 1$.
- [Pseudospectrum](/pseudospectrum/): describes the transient behavior that $\rho$ misses.
- [Perron-Frobenius theorem](/perron-frobenius-theorem/): the spectral radius of a nonnegative matrix is an eigenvalue.

## References
