---
title: The heavy ball method attains the rate ((√κ - 1)/(√κ + 1))^k on quadratics and the O(1/k) averaged rate on convex functions
proves: [correctness, termination, gradients.quadratic, gradients.convex_average]
status: full
---

**Setting.** HEAVY-BALL sets $x_{-1} = x_0$ (line L1) and then computes $x_{k+1} = x_k - \alpha\nabla f(x_k) + \beta(x_k - x_{k-1})$ for $k = 0, \ldots, K - 1$ (lines L2 to L5). The loop has $K$ passes, so the method terminates, and the claims below are about the iterates it computes. Write $g_k = \nabla f(x_k)$.

**Claim 1.** Let $f(x) = \frac12(x - x^*)^\top A(x - x^*) + f^*$, where $A$ is symmetric with all eigenvalues in $[\mu, L]$, $0 < \mu \le L$. Let $\kappa = L/\mu$, $\rho = (\sqrt\kappa - 1)/(\sqrt\kappa + 1)$, $\alpha = 4/(\sqrt L + \sqrt\mu)^2$ and $\beta = \rho^2$. Then $\|x_k - x^*\| \le (1 + (1 + \rho)k)\rho^k\|x_0 - x^*\|$ for every $k \ge 0$.

*Proof.* Let $q_1, \ldots, q_n$ be an orthonormal basis of eigenvectors of $A$ with eigenvalues $\lambda_i$, and write $x_k - x^* = \sum_ie_k^{(i)}q_i$. Since $g_k = A(x_k - x^*)$, each coordinate obeys, for $k \ge 0$,

$$e_{k+1} = (1 + \beta - \alpha\lambda)e_k - \beta e_{k-1}, \qquad e_{-1} = e_0,$$

where we drop the index $i$. Let $t(\lambda) = 1 + \beta - \alpha\lambda$. Since $(\sqrt L + \sqrt\mu)^2(1 + \beta) = (\sqrt L + \sqrt\mu)^2 + (\sqrt L - \sqrt\mu)^2 = 2(L + \mu)$,

$$t(\mu) = \frac{2(L + \mu) - 4\mu}{(\sqrt L + \sqrt\mu)^2} = \frac{2(\sqrt L - \sqrt\mu)}{\sqrt L + \sqrt\mu} = 2\rho, \qquad t(L) = \frac{2(L + \mu) - 4L}{(\sqrt L + \sqrt\mu)^2} = -2\rho.$$

As $t$ is affine in $\lambda$, $|t(\lambda)| \le 2\rho$ for $\lambda \in [\mu, L]$. If $\rho = 0$ (that is, $\mu = L$), then $t = 0$, $\beta = 0$ and $e_1 = 0$, so the claim holds. Otherwise let $c = t/(2\rho) \in [-1, 1]$ and $e_k = \rho^kp_k$. Dividing the recurrence by $\rho^{k+1}$ gives

$$p_{k+1} = 2cp_k - p_{k-1}, \qquad p_0 = e_0, \quad p_{-1} = \rho e_0.$$

Let $T_k$ and $U_k$ be the Chebyshev polynomials of the first and second kind ([Chebyshev polynomials](/chebyshev-polynomials/)), with $U_{-1} = 0$. Both $y_k = T_k(c)$ and $y_k = U_{k-1}(c)$ satisfy $y_{k+1} = 2cy_k - y_{k-1}$ for $k \ge 1$. The sequence $s_k = e_0\left(T_k(c) + (c - \rho)U_{k-1}(c)\right)$ satisfies the same recurrence, and $s_0 = e_0 = p_0$, $s_1 = e_0(c + c - \rho) = (2c - \rho)e_0 = 2cp_0 - p_{-1} = p_1$. So $p_k = s_k$ for all $k \ge 0$.

For $c = \cos\theta \in [-1, 1]$, $|T_k(c)| = |\cos k\theta| \le 1$ and $|U_{k-1}(c)| \le k$. The second bound holds because $U_{k-1}(\cos\theta) = \sin k\theta/\sin\theta$ for $\sin\theta \ne 0$ and $|\sin k\theta| \le k|\sin\theta|$ (by induction, $|\sin(k+1)\theta| \le |\sin k\theta||\cos\theta| + |\cos k\theta||\sin\theta| \le (k + 1)|\sin\theta|$), and by continuity at $c = \pm1$. With $|c - \rho| \le 1 + \rho$,

$$|e_k| = \rho^k|p_k| \le \rho^k\left(1 + (1 + \rho)k\right)|e_0|.$$

The bound is the same for every coordinate, so squaring and adding over $i$ gives the claim. $\square$

**Claim 2.** Let $f$ be convex and $L$-smooth with a minimizer $x^*$, $f^* = f(x^*)$ and $R = \|x_0 - x^*\|$. Let $0 \le \beta < 1$ and $0 < \alpha \le (1 - \beta)/L$. Then for every $T \ge 0$, with $\bar{x}_T = \frac{1}{T+1}\sum_{k=0}^Tx_k$,

$$f(\bar{x}_T) - f^* \le \frac{1}{T + 1}\sum_{k=0}^T(f(x_k) - f^*) \le \frac{1}{T + 1}\left(\frac{(1 - \beta)R^2}{2\alpha} + \frac{\beta}{1 - \beta}(f(x_0) - f^*)\right),$$

and the same bound holds for $\min_{0 \le k \le T}(f(x_k) - f^*)$.

*Proof.* Let $\gamma = \beta/(1 - \beta)$, $\eta = \alpha/(1 - \beta) \le 1/L$, and $z_k = x_k + \gamma(x_k - x_{k-1})$ for $k \ge 0$, so $z_0 = x_0$. Using $x_{k+1} - x_k = -\alpha g_k + \beta(x_k - x_{k-1})$,

$$z_{k+1} = x_k + (1 + \gamma)(x_{k+1} - x_k) = x_k + \frac{1}{1 - \beta}\left(-\alpha g_k + \beta(x_k - x_{k-1})\right) = z_k - \eta g_k.$$

Expanding the square,

$$\|z_{k+1} - x^*\|^2 = \|z_k - x^*\|^2 - 2\eta\,g_k^\top(x_k - x^*) - 2\eta\gamma\,g_k^\top(x_k - x_{k-1}) + \eta^2\|g_k\|^2.$$

For a convex $L$-smooth $f$, $f^* \ge f(x_k) + g_k^\top(x^* - x_k) + \frac{1}{2L}\|g_k\|^2$ ([smoothness](/smoothness/), item 3 with $\nabla f(x^*) = 0$), so $g_k^\top(x_k - x^*) \ge f(x_k) - f^* + \frac{1}{2L}\|g_k\|^2$. By convexity, $g_k^\top(x_k - x_{k-1}) \ge f(x_k) - f(x_{k-1})$. Hence

$$\|z_{k+1} - x^*\|^2 \le \|z_k - x^*\|^2 - 2\eta(f(x_k) - f^*) - 2\eta\gamma(f(x_k) - f(x_{k-1})) - \eta\left(\frac1L - \eta\right)\|g_k\|^2.$$

The last term is at most $0$ since $\eta \le 1/L$. Add these inequalities for $k = 0, \ldots, T$. The momentum terms telescope to $f(x_T) - f(x_{-1}) = f(x_T) - f(x_0) \ge -(f(x_0) - f^*)$, and the distance terms to at most $\|z_0 - x^*\|^2 = R^2$:

$$2\eta\sum_{k=0}^T(f(x_k) - f^*) \le R^2 + 2\eta\gamma(f(x_0) - f^*).$$

Divide by $2\eta(T + 1)$ and substitute $\eta$ and $\gamma$: the mean of $f(x_k) - f^*$ over $k \le T$ is at most the right side of the claim. Both the minimum and, by convexity (Jensen's inequality), $f(\bar{x}_T) - f^*$ are at most this mean. $\square$

**Remark on the averaged rate.** With $\alpha = (1 - \beta)/L$ and $f(x_0) - f^* \le \frac{L}{2}R^2$ (the descent lemma at $x^*$, where $\nabla f(x^*) = 0$), the bound is at most $\frac{LR^2}{2(T + 1)}\left(1 + \frac{\beta}{1 - \beta}\right) = \frac{LR^2}{2(1 - \beta)(T + 1)}$, so $O(LR^2/\varepsilon)$ iterations give accuracy $\varepsilon$ for a fixed $\beta$.
