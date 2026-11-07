---
title: The Lanczos recurrence gives an orthonormal Krylov basis and a tridiagonal projection
proves: [correctness, termination]
status: full
---

Notation of the page: $A = A^* \in \mathbb{C}^{n \times n}$ with eigenvalues $\lambda_1 \ge \dots \ge \lambda_n$ and orthonormal eigenvectors $v_i$; $b \ne 0$; $K_k(A, b) = \operatorname{span}\{b, Ab, \dots, A^{k-1} b\}$; $Q_k = [q_1, \dots, q_k]$; $T_k$ the $k \times k$ real symmetric tridiagonal matrix with diagonal $\alpha_1, \dots, \alpha_k$ and off-diagonal $\beta_1, \dots, \beta_{k-1}$. Exact arithmetic unless stated; the reorthogonalization of line L5 then changes nothing, since it subtracts zero.

**Theorem 1 (orthonormal basis and the Lanczos relation).** Suppose the loop runs steps $1, \dots, k$ with $\beta_1, \dots, \beta_{k-1} > 0$. Then $q_1, \dots, q_k$ are orthonormal, $\operatorname{span}\{q_1, \dots, q_j\} = K_j(A, b)$ for $j \le k$, and
$$A Q_k = Q_k T_k + \beta_k q_{k+1} e_k^T, \qquad Q_k^* q_{k+1} = 0, \qquad Q_k^* A Q_k = T_k,$$
where $\beta_k q_{k+1}$ means the vector $w$ of step $k$ (which may be zero).

*Proof.* By induction on $j$. For $j = 1$, $q_1 = b / \|b\|_2$. Assume $q_1, \dots, q_j$ are orthonormal, span $K_j$, and satisfy $A q_i = \beta_{i-1} q_{i-1} + \alpha_i q_i + \beta_i q_{i+1}$ for $i < j$ (with $\beta_0 q_0 = 0$). Step $j$ forms $w = A q_j - \beta_{j-1} q_{j-1} - \alpha_j q_j$ with $\alpha_j = q_j^* A q_j$, real because $A$ is Hermitian.

- $q_j^* w = q_j^* A q_j - \alpha_j = 0$, using $q_j^* q_{j-1} = 0$.
- $q_{j-1}^* w = q_{j-1}^* A q_j - \beta_{j-1}$. By symmetry, $q_{j-1}^* A q_j = (A q_{j-1})^* q_j = (\beta_{j-2} q_{j-2} + \alpha_{j-1} q_{j-1} + \beta_{j-1} q_j)^* q_j = \beta_{j-1}$, as the $\beta$ are real. So $q_{j-1}^* w = 0$.
- For $i \le j - 2$, $q_i^* w = (A q_i)^* q_j = (\beta_{i-1} q_{i-1} + \alpha_i q_i + \beta_i q_{i+1})^* q_j = 0$, because the indices are at most $j - 1$.

This is the point where symmetry is used: $w$ is orthogonal to all earlier vectors although only two are subtracted. If $\beta_j = \|w\|_2 > 0$, then $q_{j+1} = w / \beta_j$ is a unit vector orthogonal to $q_1, \dots, q_j$, and $A q_j = \beta_{j-1} q_{j-1} + \alpha_j q_j + \beta_j q_{j+1}$. As $A q_j \in A K_j \subseteq K_{j+1}$, also $q_{j+1} \in K_{j+1}$; the $j + 1$ orthonormal vectors in $K_{j+1}$, which has dimension at most $j + 1$, span it. Writing the relations for $i = 1, \dots, k$ as columns gives $A Q_k = Q_k T_k + w e_k^T$, and multiplying by $Q_k^*$ gives $Q_k^* A Q_k = T_k$. $\square$

**Theorem 2 (termination and breakdown).** Let $m$ be the number of distinct eigenvalues $\lambda$ for which $b$ has a nonzero component in the eigenspace of $\lambda$. Then $\beta_1, \dots, \beta_{m-1} > 0$ and $\beta_m = 0$. At that step $K_m(A, b)$ is invariant under $A$, and the eigenvalues of $T_m$ are exactly those $m$ eigenvalues of $A$. So the loop stops after at most $\min(k, m) \le n$ steps.

*Proof.* Write $b = \sum_{\ell=1}^{m} c_\ell z_\ell$ with $z_\ell$ unit vectors in the eigenspaces of distinct eigenvalues $\mu_1, \dots, \mu_m$, and $c_\ell \ne 0$. Then $K_j = \{p(A) b : \deg p < j\}$, and $p(A) b = \sum_\ell c_\ell p(\mu_\ell) z_\ell$ is zero only if $p$ vanishes at all $\mu_\ell$. So $\dim K_j = j$ for $j \le m$ and $K_{m+1} = K_m$. By Theorem 1, as long as $\beta_{j} > 0$, the basis has $j + 1$ elements in $K_{j+1}$; this is impossible for $j = m$. So $\beta_j > 0$ for $j < m$ (otherwise $A K_j \subseteq K_j$, giving $K_{j+1} = K_j$ of dimension $j < j + 1$) and $\beta_m = 0$. With $\beta_m = 0$, $A Q_m = Q_m T_m$, so $K_m$ is invariant and every eigenpair $(\theta, s)$ of $T_m$ gives an eigenpair $(\theta, Q_m s)$ of $A$. The eigenvalues of $T_m$ are distinct (an unreduced symmetric tridiagonal matrix has simple eigenvalues), and the restriction of $A$ to $K_m = \operatorname{span}\{z_\ell\}$ has the eigenvalues $\mu_1, \dots, \mu_m$. $\square$

**Theorem 3 (Ritz pairs and their residuals).** Let $T_k s_i = \theta_i s_i$ with $\|s_i\|_2 = 1$, and let $y_i = Q_k s_i$. Then $\|y_i\|_2 = 1$ and
$$\|A y_i - \theta_i y_i\|_2 = \beta_k |e_k^T s_i|.$$
So, by the residual bound for Hermitian matrices, each interval $[\theta_i - \beta_k |e_k^T s_i|, \theta_i + \beta_k |e_k^T s_i|]$ contains an eigenvalue of $A$.

*Proof.* $A y_i = A Q_k s_i = Q_k T_k s_i + \beta_k q_{k+1} e_k^T s_i = \theta_i y_i + \beta_k (e_k^T s_i) q_{k+1}$, and $\|q_{k+1}\|_2 = 1$. For the interval: if $\|A y - \theta y\|_2 = \rho$ with $\|y\|_2 = 1$, then expanding $y$ in the eigenvectors gives $\rho^2 = \sum_i |v_i^* y|^2 (\lambda_i - \theta)^2 \ge \min_i (\lambda_i - \theta)^2$. $\square$

**Theorem 4 (monotone extremal Ritz values and the Kaniel-Paige-Saad bound).** The largest Ritz value $\theta_1^{(k)} = \max_{0 \ne x \in K_k} x^* A x / x^* x$ is nondecreasing in $k$ and satisfies
$$\lambda_1 \ge \theta_1^{(k)} \ge \lambda_1 - (\lambda_1 - \lambda_n) \left( \frac{\tan \phi_1}{C_{k-1}(1 + 2\gamma_1)} \right)^2, \qquad \gamma_1 = \frac{\lambda_1 - \lambda_2}{\lambda_2 - \lambda_n},$$
where $\cos \phi_1 = |v_1^* b| / \|b\|_2 > 0$, $C_{k-1}$ is the Chebyshev polynomial of degree $k - 1$, and $\lambda_2 > \lambda_n$.

*Proof.* By Theorem 1, $x = Q_k s$ ranges over $K_k$, and $x^* A x / x^* x = s^* T_k s / s^* s$, whose maximum is the largest eigenvalue of $T_k$ ([Courant-Fischer](/courant-fischer-theorem/)). Since $K_k \subseteq K_{k+1}$, the maximum does not decrease, and it is at most $\lambda_1$. For the lower bound take $x = p(A) b$ with $p(t) = C_{k-1}(1 + 2(t - \lambda_2)/(\lambda_2 - \lambda_n))$, of degree $k - 1$. Write $b = \sum_i c_i v_i$. Then
$$\lambda_1 - \frac{x^* A x}{x^* x} = \frac{\sum_{i \ge 2} |c_i|^2 p(\lambda_i)^2 (\lambda_1 - \lambda_i)}{\sum_i |c_i|^2 p(\lambda_i)^2} \le (\lambda_1 - \lambda_n) \frac{\sum_{i \ge 2} |c_i|^2}{|c_1|^2 p(\lambda_1)^2}.$$
For $i \ge 2$ the argument of $C_{k-1}$ lies in $[-1, 1]$, so $|p(\lambda_i)| \le 1$, while $p(\lambda_1) = C_{k-1}(1 + 2\gamma_1)$. Also $\sum_{i \ge 2} |c_i|^2 / |c_1|^2 = \tan^2 \phi_1$. $\square$

As $C_{k-1}(1 + 2\gamma) \ge \frac{1}{2}(1 + 2\sqrt{\gamma})^{k-1}$ for $\gamma \ge 0$, the error decreases at least like $(1 + 2\sqrt{\gamma_1})^{-2(k-1)}$, much faster than the $(\lambda_2/\lambda_1)^{2k}$ of [power iteration](/power-iteration/) for the same number of products. This is the bound of Kaniel (1966), corrected by Paige (1971) and Saad (1980); Golub and Van Loan give it in Section 10.1.

**Termination of the implementation.** The loop of line L2 runs at most $k$ times. It also stops when $\beta_j$ falls below $10 n u \max(|\alpha_j|, \beta_{j-1}, 1)$, the floating-point form of the breakdown of Theorem 2.

**Floating point.** Without line L5, rounding errors destroy the orthogonality of the $q_j$, and Theorem 1 then fails. Paige (1971, 1976, 1980) proved that the computed quantities still satisfy $A Q_k = Q_k T_k + \beta_k q_{k+1} e_k^T + F_k$ with $\|F_k\|$ of order $u \|A\|$. He also proved that the loss of orthogonality is tied to convergence: for a Ritz vector $y_i$, $|y_i^* q_{k+1}|$ is about $u \|A\| / (\beta_k |e_k^T s_i|)$, so orthogonality is lost exactly in the direction of the Ritz vectors that have converged. Every Ritz value is still within a small multiple of the residual estimate of an eigenvalue, but converged eigenvalues reappear as extra copies ("ghosts"). With full reorthogonalization by classical Gram-Schmidt applied twice, the computed $Q_k$ satisfies $\|Q_k^* Q_k - I\| = O(u)$ for each step, and Theorems 1 to 3 hold up to errors of order $u \|A\|$.
