---
title: The POD basis is orthonormal, its snapshot error is the sum of the discarded eigenvalues, and the reduced model error is bounded by the projection error
proves: [correctness, stability]
status: full
---

We assume exact arithmetic. $S$ is an $n$ by $m$ real matrix with columns $s_1, \ldots, s_m$, and $C = S^T S$ (line L1). $C$ is symmetric and positive semidefinite, so it has orthonormal eigenvectors $w_1, \ldots, w_m$ with eigenvalues $\lambda_1 \ge \cdots \ge \lambda_m \ge 0$ (line L2). Let $r \ge 1$ with $\lambda_r > 0$, and let $v_i = S w_i / \sqrt{\lambda_i}$ for $i \le r$ (line L3). For each $i$ with $\lambda_i > 0$ we define $v_i$ in the same way, and $V = [v_1, \ldots, v_r]$.

**Lemma 1 (orthonormal modes).** For $i, j$ with $\lambda_i, \lambda_j > 0$, $v_i^T v_j = \delta_{ij}$. For $\lambda_i = 0$, $S w_i = 0$.

*Proof.* $v_i^T v_j = w_i^T S^T S w_j / \sqrt{\lambda_i \lambda_j} = \lambda_j\, w_i^T w_j / \sqrt{\lambda_i \lambda_j} = \delta_{ij}$, because the $w_i$ are orthonormal. If $\lambda_i = 0$, then $\|S w_i\|^2 = w_i^T C w_i = 0$. $\square$

**Lemma 2 (the projection error).** $\sum_{j=1}^{m} \|s_j - V V^T s_j\|_2^2 = \sum_{i = r+1}^{m} \lambda_i$.

*Proof.* Let $W = [w_1, \ldots, w_m]$, an orthogonal matrix. Then $S = S W W^T = \sum_{i=1}^{m} (S w_i) w_i^T$. By Lemma 1 the terms with $\lambda_i = 0$ vanish, so

$$S = \sum_{\lambda_i > 0} \sqrt{\lambda_i}\, v_i w_i^T .$$

By Lemma 1, $V^T v_i = e_i$ for $i \le r$ and $V^T v_i = 0$ for $i > r$ with $\lambda_i > 0$. Hence $V V^T S = \sum_{i \le r} \sqrt{\lambda_i}\, v_i w_i^T$ and $S - V V^T S = \sum_{i > r, \lambda_i > 0} \sqrt{\lambda_i}\, v_i w_i^T$. The left side of the claim is the squared Frobenius norm of this matrix, which is the sum of the squared norms of its columns. The matrices $v_i w_i^T$ are orthonormal in the Frobenius inner product, because $\operatorname{tr}((v_i w_i^T)^T v_j w_j^T) = (v_i^T v_j)(w_j^T w_i) = \delta_{ij}$. So the squared norm is $\sum_{i > r} \lambda_i$. $\square$

The formula $S = \sum_i \sqrt{\lambda_i}\, v_i w_i^T$ is a singular value decomposition of $S$, with singular values $\sigma_i = \sqrt{\lambda_i}$. So Lemma 2 says that the error is the sum of the discarded $\sigma_i^2$. That no other $n$ by $r$ matrix with orthonormal columns gives a smaller error is the Schmidt-Eckart-Young theorem, which we do not prove here.

Now let $A$ be an $n$ by $n$ matrix, $f \in \mathbb{R}^n$ and $dt > 0$. The full states satisfy $(I - dt A) x_{k+1} = x_k + dt f$. Line L4 sets $A_r = V^T A V$, $f_r = V^T f$ and $z_0 = V^T x_0$, and line L6 sets $(I - dt A_r) z_{k+1} = z_k + dt f_r$.

**Lemma 3 (stability).** If $A + A^T$ is negative semidefinite, then for every $z \in \mathbb{R}^r$, $\|(I - dt A_r) z\|_2 \ge \|z\|_2$. So $I - dt A_r$ is invertible and $\|(I - dt A_r)^{-1}\|_2 \le 1$.

*Proof.* $A_r + A_r^T = V^T (A + A^T) V$, so $z^T (A_r + A_r^T) z = (V z)^T (A + A^T)(V z) \le 0$. Then

$$\|(I - dt A_r) z\|^2 = \|z\|^2 - dt\, z^T (A_r + A_r^T) z + dt^2 \|A_r z\|^2 \ge \|z\|^2 .$$

A matrix with this property has a zero kernel, so it is invertible, and $\|(I - dt A_r)^{-1} y\| \le \|y\|$ follows with $y = (I - dt A_r) z$. $\square$

A symmetric negative semidefinite $A$, such as the central difference matrix of $u_{xx}$ with zero boundary values, satisfies the hypothesis.

**Theorem (the error of the reduced model).** Let $\rho_k = x_k - V V^T x_k$ and $\theta_k = V^T x_k - z_k$. Then

1. $\|x_k - V z_k\|_2^2 = \|\rho_k\|_2^2 + \|\theta_k\|_2^2$ for each $k$;
2. $(I - dt A_r)\, \theta_{k+1} = \theta_k + dt\, V^T A \rho_{k+1}$, with $\theta_0 = 0$;
3. if $A + A^T$ is negative semidefinite, $\|\theta_K\|_2 \le dt \sum_{k=1}^{K} \|A \rho_k\|_2$.

*Proof.* (1) $x_k - V z_k = \rho_k + V \theta_k$. The vector $\rho_k$ is orthogonal to the range of $V$, because $V^T \rho_k = V^T x_k - V^T V V^T x_k = 0$, and $\|V \theta_k\| = \|\theta_k\|$. The claim is the theorem of Pythagoras.

(2) Multiply the full step by $V^T$: $V^T x_{k+1} - dt\, V^T A x_{k+1} = V^T x_k + dt\, f_r$. Write $x_{k+1} = V V^T x_{k+1} + \rho_{k+1}$, so $V^T A x_{k+1} = A_r V^T x_{k+1} + V^T A \rho_{k+1}$. This gives

$$(I - dt A_r) V^T x_{k+1} = V^T x_k + dt\, f_r + dt\, V^T A \rho_{k+1} .$$

Subtract the reduced step of line L6. $\theta_0 = V^T x_0 - z_0 = 0$ by line L4.

(3) By (2) and Lemma 3, $\|\theta_{k+1}\| \le \|\theta_k + dt\, V^T A \rho_{k+1}\| \le \|\theta_k\| + dt \|A \rho_{k+1}\|$, because $\|V^T y\| \le \|y\|$ for a matrix with orthonormal columns. Sum over $k = 0, \ldots, K-1$ and use $\theta_0 = 0$. $\blacksquare$

**Corollary (exact reproduction).** If every state $x_0, \ldots, x_K$ lies in the range of $V$, for example when the snapshots are these states and $r = \operatorname{rank} S$, then $V z_k = x_k$ for all $k$.

*Proof.* Then $\rho_k = 0$ for all $k$. By part (2), $(I - dt A_r) \theta_{k+1} = \theta_k$ for all $k$ and $\theta_0 = 0$. If $I - dt A_r$ is invertible (for example under the hypothesis of Lemma 3), induction gives $\theta_k = 0$, and part (1) gives $x_k = V z_k$. $\square$
