---
title: The Chebyshev iteration computes the min-max polynomial and converges at rate q
proves: [correctness, termination]
status: full
---

Notation of the page; $0 < \lambda_{\min} < \lambda_{\max}$ (the case $\delta = 0$ is Richardson iteration with $\omega = 1/\theta$, for which $e_{k+1} = (I - A/\theta) e_k$). Let $s(\lambda) = (\theta - \lambda)/\delta$, which maps $[\lambda_{\min}, \lambda_{\max}]$ onto $[-1, 1]$ and $0$ to $\sigma_1 > 1$. Define $\tau_k = T_k(\sigma_1) \ge 1$ and $p_k(\lambda) = T_k(s(\lambda)) / \tau_k$, so $p_k(0) = 1$.

**Lemma 1 (the scalars).** The values $\rho_k$ of L1 and L8 satisfy $\rho_k = \tau_k / \tau_{k+1}$.

*Proof.* $\rho_0 = 1/\sigma_1 = \tau_0/\tau_1$. The recurrence $\tau_{k+1} = 2 \sigma_1 \tau_k - \tau_{k-1}$ gives $\tau_k/\tau_{k+1} = 1/(2\sigma_1 - \tau_{k-1}/\tau_k) = 1/(2\sigma_1 - \rho_{k-1})$, which is L8. $\square$

**Lemma 2 (polynomial recurrence).** For $k \ge 1$,
$$p_{k+1}(\lambda) = 2 \rho_k s(\lambda) p_k(\lambda) - \rho_k \rho_{k-1} p_{k-1}(\lambda).$$

*Proof.* Divide $T_{k+1}(s) = 2 s T_k(s) - T_{k-1}(s)$ by $\tau_{k+1}$ and use $\tau_k/\tau_{k+1} = \rho_k$ and $\tau_{k-1}/\tau_{k+1} = \rho_{k-1}\rho_k$. $\square$

**Theorem 1 (polynomial form).** In exact arithmetic, for every $k$ reached, $e_k = p_k(A) e_0$, $r_k = A e_k$, and $d_k = e_k - e_{k+1}$.

*Proof.* L6 and L7 give $x_{k+1} = x_k + d_k$ and $r_{k+1} = r_k - A d_k$, so $r_k = b - A x_k$ for all $k$ by induction (true at $k = 0$ by L2), i.e. $r_k = A e_k$, and $e_{k+1} = e_k - d_k$. It remains to show $e_k = p_k(A) e_0$.

$k = 0$: $p_0 = 1$. $k = 1$: $d_0 = r_0/\theta = A e_0/\theta$, so $e_1 = (I - A/\theta) e_0$, and $p_1(\lambda) = s(\lambda)/\sigma_1 = (\theta - \lambda)/\theta = 1 - \lambda/\theta$.

Step: by L9, $d_k = \rho_k \rho_{k-1} d_{k-1} + (2\rho_k/\delta) r_k$ for $k \ge 1$ (with the $\rho$ indices of Lemma 1). So
$$e_{k+1} = e_k - \rho_k \rho_{k-1} (e_{k-1} - e_k) - \frac{2\rho_k}{\delta} A e_k = (1 + \rho_k\rho_{k-1}) e_k - \frac{2\rho_k}{\delta} A e_k - \rho_k\rho_{k-1} e_{k-1}.$$
From $\tau_{k+1} = 2\sigma_1\tau_k - \tau_{k-1}$, $1 = 2\sigma_1\rho_k - \rho_k\rho_{k-1}$, so $1 + \rho_k\rho_{k-1} = 2 \rho_k \sigma_1$, and $2\rho_k\sigma_1 I - (2\rho_k/\delta) A = 2\rho_k s(A)$. Hence $e_{k+1} = 2\rho_k s(A) e_k - \rho_k\rho_{k-1} e_{k-1}$, which by the induction hypothesis and Lemma 2 is $p_{k+1}(A) e_0$. $\square$

**Theorem 2 (min-max property).** For any real polynomial $p$ of degree $\le k$ with $p(0) = 1$, $\max_{[\lambda_{\min}, \lambda_{\max}]} |p| \ge 1/\tau_k = \max_{[\lambda_{\min}, \lambda_{\max}]} |p_k|$.

*Proof.* $|T_k| \le 1$ on $[-1, 1]$ with equality at the $k + 1$ points $s_j = \cos(j\pi/k)$, where $T_k(s_j) = (-1)^j$; so $\max |p_k| = 1/\tau_k$, attained with alternating signs at $\lambda_j = \theta - \delta s_j$. Suppose $\max |p| < 1/\tau_k$. Then $q = p_k - p$ has degree $\le k$, $q(0) = 0$, and $q(\lambda_j)$ has the sign of $(-1)^j$ for $j = 0, \dots, k$, so $q$ has at least $k$ roots in the interval, plus the root $0$ outside it: $k + 1$ roots, so $q = 0$, a contradiction. $\square$

**Theorem 3 (error bound).** If $A$ is symmetric with eigenvalues in $[\lambda_{\min}, \lambda_{\max}]$, then $\|e_k\|_2 \le \|e_0\|_2 / \tau_k \le 2 q^k \|e_0\|_2$, and the same holds for $r_k$ and in the $A$-norm.

*Proof.* With $A = Q \Lambda Q^T$, $\|p_k(A)\|_2 = \max_i |p_k(\lambda_i)| \le 1/\tau_k$; $p_k(A)$ commutes with $A$ and $A^{1/2}$, giving the residual and $A$-norm versions. For $\sigma > 1$, $T_k(\sigma) = \frac{1}{2}(w^k + w^{-k})$ with $w = \sigma + \sqrt{\sigma^2 - 1}$. For $\sigma = \sigma_1 = (\kappa + 1)/(\kappa - 1)$, $\sqrt{\sigma_1^2 - 1} = 2\sqrt\kappa/(\kappa - 1)$, so $w = (\sqrt\kappa + 1)^2/(\kappa - 1) = (\sqrt\kappa + 1)/(\sqrt\kappa - 1) = 1/q$. Hence $\tau_k \ge \frac{1}{2} q^{-k}$. $\square$

**Corollary (step count).** $2 q^k \le \varepsilon$ when $k \ge \ln(2/\varepsilon)/\ln(1/q)$. Since $\ln(1/q) = \ln\frac{1 + 1/\sqrt\kappa}{1 - 1/\sqrt\kappa} \ge 2/\sqrt\kappa$, $k = \lceil (\sqrt\kappa/2) \ln(2/\varepsilon) \rceil$ suffices.

**Theorem 4 (termination).** The loop L3 runs at most $\mathrm{kmax} + 1$ times and each pass either returns or finishes, so the code returns. $\blacksquare$
