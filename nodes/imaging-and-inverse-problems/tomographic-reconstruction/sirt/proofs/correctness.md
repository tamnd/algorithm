---
title: Correctness and convergence of SIRT
proves: [correctness, convergence]
status: full
---

We use the notation of the page. $A$ is an $m \times N$ matrix with $a_{ij} \ge 0$, all row sums $r_i = \sum_j a_{ij}$ and all column sums $c_j = \sum_i a_{ij}$ are positive (a zero row or column gets the weight 0 in the code, which is the same as removing it), $R = \operatorname{diag}(1/r_i)$ and $C = \operatorname{diag}(1/c_j)$. Without line L8, lines L4 to L7 compute
$$x_{k+1} = x_k + \lambda\, C A^T R\,(y - A x_k). \tag{1}$$
This is a direct reading of the lines: L4 forms $y - A x_k$, L5 multiplies by $R$, L6 by $A^T$, and L7 by $\lambda C$ and adds. We work in exact arithmetic.

**The change of variables.** Put
$$B = R^{1/2} A C^{1/2}, \qquad b = R^{1/2} y, \qquad x = C^{1/2} z.$$
Multiply (1) on the left by $C^{-1/2}$:
$$z_{k+1} = z_k + \lambda\, C^{1/2} A^T R\,(y - A C^{1/2} z_k) = z_k + \lambda\, B^T (b - B z_k). \tag{2}$$
So SIRT is the Landweber iteration for the system $B z = b$ with the step $\lambda$. Also $\|y - A x\|_R^2 = \sum_i (y - A x)_i^2 / r_i = \|b - B z\|^2$ and $\|x - x'\|_{C^{-1}}^2 = \sum_j c_j (x_j - x'_j)^2 = \|z - z'\|^2$.

**Lemma 1 (the norm).** $\|B\|_2 = 1$.

*Proof.* Let $z \in \mathbb{R}^N$. For each row $i$, the Cauchy-Schwarz inequality with the weights $a_{ij} \ge 0$ gives
$$\Big(\sum_j a_{ij}\, c_j^{-1/2} z_j\Big)^2 \le \Big(\sum_j a_{ij}\Big)\Big(\sum_j a_{ij}\, c_j^{-1} z_j^2\Big) = r_i \sum_j a_{ij}\, c_j^{-1} z_j^2.$$
So $(B z)_i^2 = r_i^{-1}\big(\sum_j a_{ij} c_j^{-1/2} z_j\big)^2 \le \sum_j a_{ij} c_j^{-1} z_j^2$. Sum over $i$ and use $\sum_i a_{ij} = c_j$:
$$\|B z\|^2 \le \sum_j c_j^{-1} z_j^2 \sum_i a_{ij} = \|z\|^2.$$
So $\|B\| \le 1$. For $z = (\sqrt{c_j})_j$, $(B z)_i = r_i^{-1/2} \sum_j a_{ij} = \sqrt{r_i}$, so $\|B z\|^2 = \sum_i r_i = \sum_{i,j} a_{ij} = \sum_j c_j = \|z\|^2 > 0$. So $\|B\| = 1$. $\square$

**Theorem 1 (filter factors).** Let $B = \sum_{q=1}^{p} \sigma_q u_q v_q^T$ be a singular value decomposition with $\sigma_q > 0$, and let $P_0$ be the orthogonal projector onto the null space of $B$. Then for every $k \ge 0$,
$$z_k = P_0 z_0 + \sum_{q=1}^{p}\Big[(1 - \lambda\sigma_q^2)^k\, v_q^T z_0 + \big(1 - (1 - \lambda\sigma_q^2)^k\big)\frac{u_q^T b}{\sigma_q}\Big] v_q.$$

*Proof.* By (2), $z_{k+1} = (I - \lambda B^T B) z_k + \lambda B^T b$. The vectors $v_q$ and the null space of $B$ are invariant under $I - \lambda B^T B$, with the factor $1 - \lambda\sigma_q^2$ on $v_q$ and the factor 1 on the null space, and $B^T b = \sum_q \sigma_q (u_q^T b) v_q$ has no part in the null space. So $P_0 z_{k+1} = P_0 z_k$ and, with $\gamma_k = v_q^T z_k$ and $\rho = 1 - \lambda\sigma_q^2$, $\gamma_{k+1} = \rho\gamma_k + \lambda\sigma_q (u_q^T b)$. The solution of this recursion is $\gamma_k = \rho^k \gamma_0 + (1 - \rho^k)(u_q^T b)/\sigma_q$, because $(1 - \rho)/\sigma_q = \lambda\sigma_q$. $\square$

**Theorem 2 (convergence).** If $0 < \lambda < 2$, then $x_k$ converges for every $y$ and every $x_0$. The limit $x^*$ minimizes $\|y - A x\|_R$, and among all minimizers it is the unique one closest to $x_0$ in the $C^{-1}$ norm. In particular, if $A x = y$ has a solution, $x^*$ is a solution, and from $x_0 = 0$ with $A$ of full row rank,
$$x^* = C A^T (A C A^T)^{-1} y.$$

*Proof.* By Lemma 1, $0 < \sigma_q \le 1$, so $-1 < 1 - \lambda\sigma_q^2 < 1$ and $(1 - \lambda\sigma_q^2)^k \to 0$. By Theorem 1, $z_k \to z^* = P_0 z_0 + B^\dagger b$. The set of minimizers of $\|b - B z\|$ is $B^\dagger b + \operatorname{null}(B)$, and $B^\dagger b$ lies in the range of $B^T$, which is orthogonal to the null space. For a minimizer $z = B^\dagger b + w$ with $w \in \operatorname{null}(B)$, Pythagoras gives $\|z - z_0\|^2 = \|B^\dagger b - (I - P_0) z_0\|^2 + \|w - P_0 z_0\|^2$, which is smallest exactly for $w = P_0 z_0$, that is for $z = z^*$. Map back with $x = C^{1/2} z$, which carries the two norms as shown above. If $A x = y$ is solvable, the minimum of the residual is 0. For full row rank, the minimizers of $\|z - 0\|$ subject to $B z = b$ give $z^* = B^T (B B^T)^{-1} b$, and $C^{1/2} B^T (B B^T)^{-1} b = C A^T R^{1/2} (R^{1/2} A C A^T R^{1/2})^{-1} R^{1/2} y = C A^T (A C A^T)^{-1} y$. $\square$

**Theorem 3 (the weighted residual).** For $0 < \lambda \le 2$, $\|y - A x_{k+1}\|_R \le \|y - A x_k\|_R$.

*Proof.* From (2), $b - B z_{k+1} = (I - \lambda B B^T)(b - B z_k)$. The matrix $B B^T$ is symmetric with eigenvalues in $[0, 1]$ by Lemma 1, so $I - \lambda B B^T$ is symmetric with eigenvalues in $[1 - \lambda, 1] \subseteq [-1, 1]$, and its norm is at most 1. $\square$

**Theorem 4 (the bound on lambda is sharp).** If $\lambda > 2$, $x_0 = 0$ and $\sum_i y_i \ne 0$, then $\|x_k\| \to \infty$.

*Proof.* Let $S = (\sum_i r_i)^{1/2} = (\sum_j c_j)^{1/2}$, $u_1 = (\sqrt{r_i})_i / S$ and $v_1 = (\sqrt{c_j})_j / S$. Since $B_{ij} = a_{ij}/\sqrt{r_i c_j}$, we get $(B v_1)_i = \sum_j a_{ij} / (\sqrt{r_i}\, S) = \sqrt{r_i}/S$ and $(B^T u_1)_j = \sum_i a_{ij} / (\sqrt{c_j}\, S) = \sqrt{c_j}/S$. So $B v_1 = u_1$ and $B^T u_1 = v_1$, a singular pair with $\sigma = 1$, and we may choose an SVD that contains it. By Theorem 1 with $z_0 = 0$, the coefficient of $v_1$ in $z_k$ is $(1 - \rho^k)\, u_1^T b$ with $\rho = 1 - \lambda < -1$. Here $u_1^T b = \sum_i \sqrt{r_i}\, y_i / \sqrt{r_i} / S = \sum_i y_i / S \ne 0$, so the coefficient grows without bound, and so does $\|z_k\|$. Since $x_j = z_j / \sqrt{c_j}$, $\|x_k\| \ge \|z_k\| / \max_j \sqrt{c_j} \to \infty$. $\square$

So for nonnegative data that are not all zero, SIRT from $x_0 = 0$ diverges for every $\lambda > 2$. For $\lambda = 2$ the same coefficient oscillates between $0$ and $2 u_1^T b$ and does not converge.

**Theorem 5 (the nonnegative variant).** With line L8, and $0 < \lambda < 2$, the iterates converge to a minimizer of $\|y - A x\|_R$ over $x \ge 0$.

*Proof.* Since $C^{1/2}$ is diagonal with positive entries, $x \ge 0$ if and only if $z \ge 0$, and clipping $x$ at 0 is the same as clipping $z$ at 0, which is the Euclidean projection onto the orthant. So in the variable $z$, lines L4 to L8 are
$$z_{k+1} = \Pi_{\ge 0}\big(z_k - \lambda \nabla f(z_k)\big), \qquad f(z) = \tfrac{1}{2}\|b - B z\|^2,$$
the projected gradient method for the convex function $f$ over a closed convex set. The gradient $\nabla f(z) = B^T(B z - b)$ is Lipschitz with the constant $L = \|B\|^2 = 1$ (Lemma 1). The function $f$ is a convex quadratic and bounded below, so it attains its minimum on the orthant (a convex quadratic bounded below on a polyhedron attains its infimum, by the Frank-Wolfe theorem). For a step in $(0, 2/L)$, the projected gradient method on a convex function with an $L$-Lipschitz gradient converges to a minimizer whenever one exists (the iteration is an averaged operator, and the Krasnoselskii-Mann theorem applies). Map back with $x = C^{1/2} z$. $\square$

**Corollary (the discrepancy stop).** Let $0 < \lambda < 2$, let $x^*$ be the limit of Theorem 2 or Theorem 5, and let $\|y - A x^*\| < \tau\delta$. Then the test of line L4 succeeds after a finite number of steps.

*Proof.* The map $x \mapsto \|y - A x\|$ is continuous and $x_k \to x^*$, so $\|y - A x_k\| \to \|y - A x^*\| < \tau\delta$, and some finite $k$ passes the test. $\square$

The hypothesis is needed. Line L4 tests the plain norm of the residual, while SIRT minimizes the $R$-weighted norm, so $\|y - A x^*\|$ can exceed $\|e\|$ even when $y = A x^\dagger + e$. If all row sums are equal, the two norms differ by a constant factor and the limit minimizes the plain residual too, so $\|y - A x^*\| \le \|e\| \le \delta < \tau\delta$ for every $\tau > 1$ (with clipping, this needs $x^\dagger \ge 0$). The convergence rate of the stopping index under a source condition is a result on the Landweber iteration for $B$; see the page.

**Cost.** Line L1 reads each nonzero entry of $A$ once. In each iteration, line L4 reads each nonzero entry once, line L6 reads each nonzero entry of a row with $e_i \ne 0$ once, and lines L5, L7 and L8 take $O(m)$ and $O(N)$ time. So one iteration costs $O(\operatorname{nnz}(A) + m + N)$ time and $O(m + N)$ extra space. For a ray-driven projector of an $n \times n$ image with $a$ angles of $d$ bins, $\operatorname{nnz}(A) = O(a d n)$, $m = a d$ and $N = n^2$, so one iteration costs $O(a d n + n^2)$, which is $O(a d n)$ when $a d \ge n$, as in any scan that can determine the image. $\square$
