---
title: The restricted likelihood is the likelihood of the error contrasts, gives the divisor n - p, and has a closed form in the balanced one-way layout
proves: [correctness, termination]
status: full
---

Throughout, $X$ is $n \times p$ of rank $p < n$, $V = V(\theta) = \sum_j\theta_jV_j$ is positive definite, $A = X^\top V^{-1}X$, $P = V^{-1} - V^{-1}XA^{-1}X^\top V^{-1}$, $\hat b = A^{-1}X^\top V^{-1}y$ and

$$\ell_R(\theta) = -\tfrac12\bigl[(n - p)\log 2\pi + \log|V| + \log|A| - \log|X^\top X| + y^\top Py\bigr].$$

The vector $b$ holds the fixed-effect coefficients. Two facts about $P$ are used: $PX = V^{-1}X - V^{-1}XA^{-1}A = 0$, and $VPV = V - XA^{-1}X^\top$, by direct multiplication. Also $y^\top Py = (y - X\hat b)^\top V^{-1}(y - X\hat b)$, because $V^{-1}(y - X\hat b) = Py$ and $\hat b^\top X^\top Py = 0$.

**Lemma 1 (error contrasts).** Let $K$ be $n \times (n - p)$ of rank $n - p$ with $K^\top X = 0$. Then (a) $K(K^\top VK)^{-1}K^\top = P$, and (b) $|K^\top VK| = |K^\top K|\,|V|\,|A|/|X^\top X|$. So $w = K^\top y \sim N(0, K^\top VK)$ has log density $\ell_R(\theta) - \frac12\log|K^\top K|$, which is $\ell_R(\theta)$ when $K^\top K = I$.

*Proof.* $K^\top VK$ is positive definite because $K$ has full column rank. The $n \times n$ matrix $[VK\ X]$ is invertible: if $VK\alpha + X\beta = 0$, multiply by $K^\top$ to get $K^\top VK\alpha = 0$, so $\alpha = 0$, and then $X\beta = 0$ gives $\beta = 0$. Let $Q = K(K^\top VK)^{-1}K^\top$. Then $QVK = K$ and $QX = 0$, and also $PVK = K - V^{-1}XA^{-1}X^\top K = K$ and $PX = 0$. So $Q$ and $P$ agree on the columns of an invertible matrix, and $Q = P$. This is (a).

For (b) let $T = [K\ X]$, which is invertible by the same argument with $V = I$. Since $K^\top X = 0$, $T^\top T$ is block diagonal and $|T|^2 = |K^\top K|\,|X^\top X|$. Now

$$T^\top VT = \begin{pmatrix} K^\top VK & K^\top VX \\ X^\top VK & X^\top VX \end{pmatrix},$$

and the Schur complement of the upper block is $X^\top VX - X^\top VQVX = X^\top(V - VPV)X = X^\top XA^{-1}X^\top X$ by (a) and the fact $VPV = V - XA^{-1}X^\top$. So $|T^\top VT| = |K^\top VK|\,|X^\top X|^2/|A|$. Also $|T^\top VT| = |T|^2|V| = |K^\top K|\,|X^\top X|\,|V|$. Equating the two gives (b).

Finally $E[w] = K^\top Xb = 0$ and $\operatorname{Cov}(w) = K^\top VK$, so the log density of $w$ is $-\frac12[(n - p)\log 2\pi + \log|K^\top VK| + w^\top(K^\top VK)^{-1}w]$. By (a) the quadratic form is $y^\top Qy = y^\top Py$, and by (b) the log determinant is $\log|K^\top K| + \log|V| + \log|A| - \log|X^\top X|$. $\square$

*Consequences.* $\ell_R$ does not depend on $b$. If $X$ is replaced by $XM$ for an invertible $p \times p$ matrix $M$, then $|A|$ and $|X^\top X|$ are both multiplied by $|M|^2$ and $P$ does not change, so $\ell_R$ depends on $X$ only through its column space.

**Lemma 2 (score and expected information).** If $V = \sum_j\theta_jV_j$, then $\partial\ell_R/\partial\theta_j = -\frac12\operatorname{tr}(PV_j) + \frac12y^\top PV_jPy$, and $E[-\partial^2\ell_R/\partial\theta_j\partial\theta_l] = \frac12\operatorname{tr}(PV_jPV_l)$.

*Proof.* Take $K$ with $K^\top K = I$ and write $\Sigma = K^\top VK$, $\Sigma_j = \partial\Sigma/\partial\theta_j = K^\top V_jK$, so that $\ell_R = -\frac12[\text{const} + \log|\Sigma| + w^\top\Sigma^{-1}w]$ by Lemma 1. The rules $\partial\log|\Sigma| = \operatorname{tr}(\Sigma^{-1}\partial\Sigma)$ and $\partial\Sigma^{-1} = -\Sigma^{-1}(\partial\Sigma)\Sigma^{-1}$ give

$$\frac{\partial\ell_R}{\partial\theta_j} = -\tfrac12\operatorname{tr}(\Sigma^{-1}\Sigma_j) + \tfrac12w^\top\Sigma^{-1}\Sigma_j\Sigma^{-1}w.$$

By Lemma 1(a), $K\Sigma^{-1}K^\top = P$, so $\operatorname{tr}(\Sigma^{-1}K^\top V_jK) = \operatorname{tr}(PV_j)$ and $w^\top\Sigma^{-1}K^\top V_jK\Sigma^{-1}w = y^\top PV_jPy$. Since $\Sigma$ is linear in $\theta$, differentiating again gives

$$-\frac{\partial^2\ell_R}{\partial\theta_j\partial\theta_l} = -\tfrac12\operatorname{tr}(\Sigma^{-1}\Sigma_l\Sigma^{-1}\Sigma_j) + \tfrac12w^\top\Sigma^{-1}(\Sigma_l\Sigma^{-1}\Sigma_j + \Sigma_j\Sigma^{-1}\Sigma_l)\Sigma^{-1}w.$$

With $E[w^\top Bw] = \operatorname{tr}(B\Sigma)$ the expectation of the second term is $\operatorname{tr}(\Sigma^{-1}\Sigma_j\Sigma^{-1}\Sigma_l)$, and the sum is $\frac12\operatorname{tr}(\Sigma^{-1}\Sigma_j\Sigma^{-1}\Sigma_l) = \frac12\operatorname{tr}(PV_jPV_l)$, again by Lemma 1(a). $\square$

The ML criterion $\ell = -\frac12[n\log 2\pi + \log|V| + y^\top Py]$ has the score $-\frac12\operatorname{tr}(V^{-1}V_j) + \frac12y^\top PV_jPy$ and the information $\frac12\operatorname{tr}(V^{-1}V_jV^{-1}V_l)$ by the same rules; this is the "ml" branch of the implementation.

**Theorem 1 (one variance: the divisor n - p).** Let $V = \sigma^2I$ ($k = 1$, $V_1 = I$) and $\mathrm{RSS} = \min_b\lVert y - Xb\rVert^2 > 0$. The REML estimate is $\hat\sigma^2_R = \mathrm{RSS}/(n - p)$, which is unbiased, and the ML estimate is $\hat\sigma^2_M = \mathrm{RSS}/n$. For one normal sample, $X = \mathbf 1$ and $p = 1$, so $\hat\sigma^2_R = \frac{1}{n-1}\sum_i(y_i - \bar y)^2$, the sample variance $S^2$ with divisor $n - 1$.

*Proof.* Here $|V| = \sigma^{2n}$, $A = X^\top X/\sigma^2$ so $\log|A| - \log|X^\top X| = -p\log\sigma^2$, and $P = (I - H)/\sigma^2$ with $H = X(X^\top X)^{-1}X^\top$, so $y^\top Py = \mathrm{RSS}/\sigma^2$. Hence

$$\ell_R(\sigma^2) = -\tfrac12\bigl[(n - p)\log 2\pi + (n - p)\log\sigma^2 + \mathrm{RSS}/\sigma^2\bigr].$$

The function $g(s) = c\log s + R/s$ with $c, R > 0$ has $g'(s) = (cs - R)/s^2$, negative for $s < R/c$ and positive for $s > R/c$, so $-\frac12 g$ has its unique maximum at $s = R/c$. With $c = n - p$ this is $\mathrm{RSS}/(n - p)$; for ML, $c = n$ and the maximum is $\mathrm{RSS}/n$. Since $y - X\hat b = (I - H)y = (I - H)(y - Xb)$ and $I - H$ is a projection of rank $n - p$, $E[\mathrm{RSS}] = \operatorname{tr}((I - H)\sigma^2I) = (n - p)\sigma^2$. $\square$

**Theorem 2 (balanced one-way layout).** Let $y_{ij} = b_0 + u_i + e_{ij}$ for $a \ge 2$ groups of size $m \ge 2$, $N = am$, $\theta = (\sigma_u^2, \sigma_e^2)$, $V_1 = ZZ^\top$, $V_2 = I$, $X = \mathbf 1$. Let $\mathrm{SSA}$, $\mathrm{SSE}$ and $\mathrm{SST} = \mathrm{SSA} + \mathrm{SSE}$ be the sums of squares between groups, within groups and in total, with $\mathrm{MSA} = \mathrm{SSA}/(a - 1)$ and $\mathrm{MSE} = \mathrm{SSE}/(a(m - 1))$, and assume $\mathrm{SSA} > 0$ and $\mathrm{SSE} > 0$. Then the maximizer of $\ell_R$ over $\sigma_u^2 \ge 0$, $\sigma_e^2 > 0$ is

- $\hat\sigma_e^2 = \mathrm{MSE}$ and $\hat\sigma_u^2 = (\mathrm{MSA} - \mathrm{MSE})/m$ if $\mathrm{MSA} \ge \mathrm{MSE}$,
- $\hat\sigma_u^2 = 0$ and $\hat\sigma_e^2 = \mathrm{SST}/(N - 1)$ if $\mathrm{MSA} < \mathrm{MSE}$.

For ML the same holds with $\mathrm{SSA}/a$ in place of $\mathrm{MSA}$ and $\mathrm{SST}/N$ in place of $\mathrm{SST}/(N - 1)$. In the second case the score of $\sigma_u^2$ at the maximum is negative.

*Proof.* Let $\lambda = \sigma_e^2 + m\sigma_u^2$. $V$ is block diagonal with blocks $\sigma_e^2I_m + \sigma_u^2\mathbf 1\mathbf 1^\top$, which have the eigenvalue $\lambda$ on $\mathbf 1$ and $\sigma_e^2$ on the $m - 1$ directions orthogonal to $\mathbf 1$. So $|V| = \lambda^a\sigma_e^{2a(m-1)}$, and

$$(y - \mathbf 1b_0)^\top V^{-1}(y - \mathbf 1b_0) = \frac{\mathrm{SSE}}{\sigma_e^2} + \frac{m\sum_i(\bar y_{i\cdot} - b_0)^2}{\lambda},$$

which is smallest at $b_0 = \bar y_{\cdot\cdot}$, so $y^\top Py = \mathrm{SSE}/\sigma_e^2 + \mathrm{SSA}/\lambda$. Also $A = \mathbf 1^\top V^{-1}\mathbf 1 = N/\lambda$ and $X^\top X = N$, so $\log|A| - \log|X^\top X| = -\log\lambda$. Therefore, with the precisions $\mu = 1/\sigma_e^2$ and $\nu = 1/\lambda$,

$$\ell_R = \text{const} + \tfrac12\bigl[c_e\log\mu - \mathrm{SSE}\,\mu + c_\lambda\log\nu - \mathrm{SSA}\,\nu\bigr], \qquad c_e = a(m - 1),\ c_\lambda = a - 1.$$

For ML the same calculation without the $\log|A|$ terms gives $c_\lambda = a$. The constraint $\sigma_u^2 \ge 0$ is $\lambda \ge \sigma_e^2$, that is $\nu \le \mu$. So the problem is to maximize $f(\mu, \nu) = c_e\log\mu - \mathrm{SSE}\,\mu + c_\lambda\log\nu - \mathrm{SSA}\,\nu$ over the convex set $D = \{0 < \nu \le \mu\}$.

$f$ is strictly concave and tends to $-\infty$ as $\nu \to 0$ or $\mu \to \infty$ in $D$, so it has a maximum on $D$, and the maximum is unique. Its unconstrained maximizer is $\mu^* = c_e/\mathrm{SSE}$, $\nu^* = c_\lambda/\mathrm{SSA}$, by the argument for $g$ in Theorem 1 applied to each variable.

If $\mathrm{SSA}/c_\lambda \ge \mathrm{SSE}/c_e$, then $\nu^* \le \mu^*$, so $(\mu^*, \nu^*) \in D$ is the maximum: $\hat\sigma_e^2 = \mathrm{SSE}/c_e$ and $\hat\lambda = \mathrm{SSA}/c_\lambda$, and $\hat\sigma_u^2 = (\hat\lambda - \hat\sigma_e^2)/m$. For REML $\mathrm{SSA}/c_\lambda = \mathrm{MSA}$, which gives the first case.

If $\mathrm{SSA}/c_\lambda < \mathrm{SSE}/c_e$, then $(\mu^*, \nu^*) \notin D$. Suppose the maximum $(\mu_0, \nu_0)$ had $\nu_0 < \mu_0$. Then it would be a local maximum of $f$ on an open set, so $\nabla f(\mu_0, \nu_0) = 0$, and by strict concavity it would be the unconstrained maximizer, which is not in $D$. So $\nu_0 = \mu_0 = \omega$, which maximizes $(c_e + c_\lambda)\log\omega - \mathrm{SST}\,\omega$, so $\omega = (c_e + c_\lambda)/\mathrm{SST}$. Then $\hat\sigma_u^2 = 0$ and $\hat\sigma_e^2 = \mathrm{SST}/(c_e + c_\lambda)$, which is $\mathrm{SST}/(N - 1)$ for REML and $\mathrm{SST}/N$ for ML.

For the score, $\partial/\partial\sigma_u^2 = m\,\partial/\partial\lambda$ with $\sigma_e^2$ fixed, so $s_u = \frac m2[\mathrm{SSA}/\lambda^2 - c_\lambda/\lambda]$. At $\lambda = \sigma_e^2 = \hat\sigma^2 = \mathrm{SST}/(c_e + c_\lambda)$ this is $\frac{m c_\lambda}{2\hat\sigma^4}[\mathrm{SSA}/c_\lambda - \hat\sigma^2]$. Since $\hat\sigma^2$ is the weighted mean of $\mathrm{SSA}/c_\lambda$ and $\mathrm{SSE}/c_e$ with weights $c_\lambda$ and $c_e$, $\mathrm{SSA}/c_\lambda < \hat\sigma^2$ exactly in the second case, and then $s_u < 0$. $\square$

So in the balanced layout $\hat\sigma_{u,R}^2 = \max((\mathrm{MSA} - \mathrm{MSE})/m, 0)$, and the KKT condition (score $\le 0$ at a component equal to 0) holds at the REML boundary point. With $\gamma = \sigma_u^2/\sigma_e^2$, $\mathrm{MSA}/((1 + m\gamma)\mathrm{MSE})$ has the $F_{a-1, a(m-1)}$ law (proved on the linear mixed model page), so $P(\hat\sigma_{u,R}^2 = 0) = P(F_{a-1, a(m-1)} \le 1/(1 + m\gamma))$ and $P(\hat\sigma_{u,M}^2 = 0) = P(F_{a-1, a(m-1)} \le a/((a - 1)(1 + m\gamma)))$.

**Theorem 3 (termination, feasibility and monotonicity).** Assume $V_1, \dots, V_{k-1}$ are positive semidefinite and $V_k = I$. Then the algorithm stops after at most $\mathrm{max\_iter}$ passes of the loop L3, with at most $28\,\mathrm{max\_iter} + 1$ evaluations; every iterate has $\theta_j \ge 0$ and $\theta_k \ge$ the floor, so $V(\theta)$ is positive definite; and the accepted values of $\ell_R$ never decrease, apart from the relative tolerance $10^{-12}$ that the implementation allows for rounding.

*Proof.* Lines L5 and L6 repeat only when at least one index leaves $F$, so they run at most $k + 1$ times in one pass. In lines L8 to L10, $\lambda$ takes the values $2^0, 2^{-1}, \dots$ and the loop ends at the latest when $\lambda < 10^{-8}$, after at most 28 evaluations, since $2^{-27} < 10^{-8}$. Line L3 runs at most $\mathrm{max\_iter}$ times. Line L1 and line L8 set every entry to at least 0 and the last entry to at least the floor, so $V = \sum_{j<k}\theta_jV_j + \theta_kI$ is a positive semidefinite matrix plus a positive multiple of $I$, hence positive definite. A trial point is accepted in line L9 only if its $\ell_R$ is not below the current value, and otherwise line L10 keeps $\theta$. $\square$

If the information matrix $I[F, F]$ is positive definite and $s_F \ne 0$, the direction $\delta$ has $s^\top\delta = s_F^\top I[F,F]^{-1}s_F > 0$, and for small $\lambda$ no free component is clipped in line L8 (those at 0 in $F$ have $\delta_j \ge 0$), so the halving in line L10 finds an increase in exact arithmetic. A pass that ends with no move has a change of 0 and stops the loop in line L12. That a stopping point is the global maximum, and that a component held at 0 has a score at most 0, is not proved for general $V_j$; Theorem 2 gives the answer in the balanced one-way case, and the tests check the output against it.
