---
title: The bottom generalized eigenvectors of the graph Laplacian minimize the weighted spread
proves: [correctness]
status: full
---

Let $W$ be a symmetric $n \times n$ matrix with $W_{ij} \ge 0$ and $W_{ii} = 0$, let $D = \operatorname{diag}(d_1, \dots, d_n)$ with $d_i = \sum_j W_{ij} > 0$, and let $L = D - W$.

**Lemma 1 (the quadratic form).** For each $f \in \mathbb{R}^n$, $f^\top Lf = \frac12\sum_{i,j}W_{ij}(f_i - f_j)^2$. So $L$ is symmetric positive semidefinite and $L\mathbf{1} = 0$.

*Proof.* $\frac12\sum_{i,j}W_{ij}(f_i^2 - 2f_if_j + f_j^2) = \frac12\sum_i d_if_i^2 - \sum_{i,j}W_{ij}f_if_j + \frac12\sum_j d_jf_j^2 = f^\top Df - f^\top Wf$, using the symmetry of $W$. The right side is a sum of nonnegative terms. Each row of $L$ sums to $d_i - d_i = 0$. $\square$

For $Y \in \mathbb{R}^{n \times m}$ with rows $y_i$, applying Lemma 1 to each column gives $\sum_{i,j}W_{ij}\|y_i - y_j\|^2 = 2\operatorname{tr}(Y^\top LY)$, which is the cost of the problem.

**Lemma 2 (the null space).** $Lf = 0$ if and only if $f$ is constant on each connected component of the graph with edges $\{i, j : W_{ij} > 0\}$. If the graph is connected, the null space of $L$ is spanned by $\mathbf{1}$.

*Proof.* If $Lf = 0$, then $f^\top Lf = 0$, and by Lemma 1 every term $W_{ij}(f_i - f_j)^2$ is 0, so $f_i = f_j$ across each edge, and by induction along paths, on each component. Conversely, such an $f$ gives $(Lf)_i = \sum_j W_{ij}(f_i - f_j) = 0$. $\square$

**Lemma 3 (the reduction to a symmetric problem).** Let $N = D^{-1/2}LD^{-1/2}$. Then $Nz = \lambda z$ if and only if $y = D^{-1/2}z$ satisfies $Ly = \lambda Dy$, and $y^\top Dy' = z^\top z'$ for any two such pairs. The vector $z_0 = D^{1/2}\mathbf{1}$ satisfies $Nz_0 = 0$.

*Proof.* $Ly = \lambda Dy$ with $y = D^{-1/2}z$ reads $LD^{-1/2}z = \lambda D^{1/2}z$; multiply on the left by $D^{-1/2}$, which is invertible. Then $y^\top Dy' = z^\top D^{-1/2}DD^{-1/2}z' = z^\top z'$. Finally $Nz_0 = D^{-1/2}L\mathbf{1} = 0$. $\square$

So the generalized eigenvalues $0 = \lambda_0 \le \lambda_1 \le \dots \le \lambda_{n-1}$ are the eigenvalues of the symmetric matrix $N$, which has an orthonormal eigenbasis $z_0, \dots, z_{n-1}$, and the $y_l = D^{-1/2}z_l$ are $D$-orthonormal. The implementation adds $\frac{c}{\operatorname{vol}}z_0z_0^\top$ to $N$, with $\operatorname{vol} = \sum_i d_i = \|z_0\|^2$ and $c = \operatorname{tr}(N) + 1$. This matrix agrees with $N$ on $z_0^\perp$ and has the eigenvalue $c$ on $z_0$. All eigenvalues of $N$ are at most $\operatorname{tr}(N)$, because they are nonnegative, so the eigenvalue $c$ is the largest, and the $m$ smallest eigenpairs of the shifted matrix are $\lambda_1, \dots, \lambda_m$ with eigenvectors in $z_0^\perp$.

**Theorem 1 (the minimizer).** Suppose the graph is connected. Over $Y \in \mathbb{R}^{n \times m}$ with $Y^\top DY = I$ and $Y^\top D\mathbf{1} = 0$, the minimum of $\operatorname{tr}(Y^\top LY)$ is $\lambda_1 + \dots + \lambda_m$, attained by $Y = [y_1, \dots, y_m]$.

*Proof.* Put $Z = D^{1/2}Y$. The constraints become $Z^\top Z = I$ and $Z^\top z_0 = 0$, and the cost becomes $\operatorname{tr}(Z^\top NZ)$. The matrix $N$ maps $z_0^\perp$ to itself, because it is symmetric and $Nz_0 = 0$. On that subspace its eigenvalues are $\lambda_1 \le \dots \le \lambda_{n-1}$, with eigenvectors $z_1, \dots, z_{n-1}$, by Lemma 2 and Lemma 3, which show that $\lambda_0 = 0$ is simple. The columns of $Z$ are an orthonormal $m$-frame in $z_0^\perp$. By Ky Fan's minimum principle, $\operatorname{tr}(Z^\top NZ) \ge \lambda_1 + \dots + \lambda_m$, with equality for $Z = [z_1, \dots, z_m]$. Going back with $Y = D^{-1/2}Z$ gives the claim. $\square$

For $m = 1$, Theorem 1 is the Rayleigh quotient principle: $\lambda_1 = \min\{f^\top Lf / f^\top Df : f \ne 0,\ f^\top D\mathbf{1} = 0\}$.

**Theorem 2 (the path graph).** For the path with vertices $0, \dots, n-1$ and unit weights, the generalized eigenpairs are $\lambda_k = 1 - \cos\theta_k$ and $y_k[j] = \cos(j\theta_k)$, with $\theta_k = \pi k/(n-1)$ and $k = 0, \dots, n-1$.

*Proof.* For an inner vertex $j$, $D_{jj} = 2$ and $(Ly_k)_j = 2\cos(j\theta) - \cos((j-1)\theta) - \cos((j+1)\theta) = 2\cos(j\theta) - 2\cos(j\theta)\cos\theta = 2(1 - \cos\theta)\cos(j\theta)$. At $j = 0$, $D_{00} = 1$ and $(Ly_k)_0 = 1 - \cos\theta$. At $j = n-1$, $\cos((n-1)\theta_k) = \cos(\pi k)$ and $\cos((n-2)\theta_k) = \cos(\pi k - \theta_k) = \cos(\pi k)\cos\theta_k$, so $(Ly_k)_{n-1} = (1 - \cos\theta_k)\cos(\pi k)$. In all cases $(Ly_k)_j = \lambda_kD_{jj}y_k[j]$. The $n$ values $\theta_k$ lie in $[0, \pi]$ and are distinct, so the $n$ eigenvalues are distinct, and these are all the eigenpairs. $\square$

For $n = 5$ this gives the eigenvalues $0, 0.293, 1, 1.707, 2$ and the coordinate of the example on the page. The test suite checks Theorem 2 for $n = 9$ and checks the equation $Ly = \lambda Dy$, the $D$-orthonormality and the constraint $Y^\top D\mathbf{1} = 0$ on a random heat kernel graph.
