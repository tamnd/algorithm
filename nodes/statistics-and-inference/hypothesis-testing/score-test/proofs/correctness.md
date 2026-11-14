---
title: The score test returns the quadratic form of the score, equals Pearson's statistic for a multinomial, is invariant under reparametrization, and has size tending to alpha
proves: [correctness, termination]
status: full
---

We prove that SCORE-TEST returns $S = u^\top J^{-1} u$ with $u$ the score and $J$ the Fisher information at the restricted MLE, that the closed forms are correct, that the multinomial score statistic is exactly Pearson's $X^2$, that $S$ does not depend on the parametrization when $J$ is the expected information, that inverting the binomial score test gives the Wilson interval, and that $S \to \chi^2_r$ under $H_0$. For a simple null the limit is proved from the central limit theorem alone. With nuisance parameters it is proved under the regularity conditions of the page on the [asymptotic normality of the MLE](/asymptotic-normality-of-mle/), which we use as hypotheses. Finite-sample sizes are not proved; the tests compute them by enumeration.

**Lemma 1 (the solve and the sign).** If $J$ is nonsingular, lines L4 and L5 return $S = u^\top J^{-1}u$. If $J$ is symmetric positive definite, $S \ge 0$.

*Proof.* Gaussian elimination with partial pivoting uses only row swaps and row operations that keep the solution set; every pivot is nonzero when $J$ is nonsingular, since a zero pivot column would make the leading columns dependent; back substitution then gives the unique $y = J^{-1}u$. If $J$ is positive definite, so is $J^{-1}$, and $u^\top J^{-1}u \ge 0$. $\square$

**Lemma 2 (closed forms).** The first four rows of the table are correct.

*Proof.* Binomial: $\ell(p) = k\log p + (n - k)\log(1 - p)$, so $U_n(p) = k/p - (n - k)/(1 - p) = (k - np)/(p(1 - p))$, and $I_n(p) = n/(p(1 - p))$. Then $S = U_n^2/I_n = (k - np_0)^2/(np_0(1 - p_0))$. Poisson: $\ell(\lambda) = t\log\lambda - n\lambda$, $U_n = t/\lambda - n = (t - n\lambda)/\lambda$, $I_n = n/\lambda$, and $S = (t - n\lambda_0)^2/(n\lambda_0)$. Normal with $\sigma$ known: $U_n(\mu) = n(\bar x - \mu)/\sigma^2$ and $I_n = n/\sigma^2$. Normal with $\sigma^2$ unknown: under $H_0$ the log-likelihood $-\tfrac n2\log v - \sum(x_i - \mu_0)^2/(2v)$ is maximized at $\tilde v_0 = \sum(x_i - \mu_0)^2/n$, where the score for $v$ is 0. The score for $\mu$ is $n(\bar x - \mu_0)/\tilde v_0$, and the information matrix of $(\mu, v)$ is $\operatorname{diag}(n/v, n/(2v^2))$, so $S = n(\bar x - \mu_0)^2/\tilde v_0 = n^2(\bar x - \mu_0)^2/\sum(x_i - \mu_0)^2$. With $SS = \sum(x_i - \bar x)^2$, $\sum(x_i - \mu_0)^2 = SS + n(\bar x - \mu_0)^2$ and $T^2 = n(n - 1)(\bar x - \mu_0)^2/SS$, which gives $S = nT^2/(n - 1 + T^2)$. $\square$

**Lemma 3 (the multinomial score statistic is Pearson's $X^2$).** Let $O_1, \dots, O_m$ be multinomial counts with total $n$, and $H_0$: probabilities $q_1, \dots, q_m > 0$. Parametrize by $q_1, \dots, q_{m-1}$ with $q_m = 1 - \sum_{j<m} q_j$. Then the score test statistic is $\sum_{j=1}^m (O_j - nq_j)^2/(nq_j)$.

*Proof.* $\ell = \sum_j O_j\log q_j$, so $U_j = O_j/q_j - O_m/q_m$ for $j < m$. The information is $J = n(D + \mathbf 1\mathbf 1^\top/q_m)$ with $D = \operatorname{diag}(1/q_1, \dots, 1/q_{m-1})$, since $E[O_j] = nq_j$ and $-\partial^2\ell/\partial q_i\partial q_j = O_i\delta_{ij}/q_i^2 + O_m/q_m^2$. By the Sherman-Morrison formula, $J^{-1} = \tfrac1n\left(D^{-1} - D^{-1}\mathbf 1\mathbf 1^\top D^{-1}/(q_m + \mathbf 1^\top D^{-1}\mathbf 1)\right) = \tfrac1n(\operatorname{diag}(q) - qq^\top)$, where $q = (q_1, \dots, q_{m-1})$ and we used $q_m + \sum_{j<m} q_j = 1$. Write $a_j = O_j - nq_j$, so $\sum_{j=1}^m a_j = 0$ and $U_j = a_j/q_j - a_m/q_m$. Then
$$u^\top\operatorname{diag}(q)\,u = \sum_{j<m} q_j\left(\frac{a_j}{q_j} - \frac{a_m}{q_m}\right)^2 = \sum_{j<m}\frac{a_j^2}{q_j} + \frac{2a_m^2}{q_m} + \frac{a_m^2(1 - q_m)}{q_m^2},$$
using $\sum_{j<m} a_j = -a_m$ and $\sum_{j<m} q_j = 1 - q_m$. Also $q^\top u = \sum_{j<m}(a_j - q_ja_m/q_m) = -a_m - a_m(1 - q_m)/q_m = -a_m/q_m$, so $u^\top qq^\top u = a_m^2/q_m^2$. Subtracting, $nS = \sum_{j<m} a_j^2/q_j + a_m^2/q_m$, which is $\sum_{j=1}^m a_j^2/q_j$. $\square$

**Lemma 4 (invariance).** Let $\theta = g(\psi)$ with $g$ one-to-one and differentiable with nonsingular Jacobian $G = \partial\theta/\partial\psi$. With expected information, the score statistic in $\psi$ at $\psi_0 = g^{-1}(\theta_0)$ equals the one in $\theta$ at $\theta_0$.

*Proof.* By the chain rule the score in $\psi$ is $G^\top U(\theta)$, and the expected information in $\psi$ is $G^\top I(\theta)G$, because the information is the covariance of the score. So $(G^\top U)^\top(G^\top IG)^{-1}(G^\top U) = U^\top G G^{-1}I^{-1}G^{-\top}G^\top U = U^\top I^{-1}U$. With nuisance parameters, $g$ must map the null set onto the null set; then the restricted MLEs correspond, and the same computation applies at $\tilde\theta_0 = g(\tilde\psi_0)$. $\square$

The observed information in $\psi$ has the extra term $-\sum_i U_i(\theta)\,\partial^2\theta_i/\partial\psi^2$, which is not 0 unless the score is 0, so with the observed information the statistic is not invariant.

**Lemma 5 (the Wilson interval).** For a binomial count $k$ out of $n$, the set $\{p_0 \in (0, 1) : S(p_0) < z^2\}$ with $z = z_{1-\alpha/2}$ is the open interval between the roots of $(k - np)^2 = z^2np(1 - p)$, which are $\left(\hat p + \tfrac{z^2}{2n} \pm z\sqrt{\hat p(1 - \hat p)/n + z^2/(4n^2)}\right)/(1 + z^2/n)$.

*Proof.* $S(p) < z^2$ is $(k - np)^2 < z^2np(1 - p)$, that is $(n^2 + z^2n)p^2 - (2kn + z^2n)p + k^2 < 0$. This quadratic in $p$ has positive leading coefficient, so the set is the open interval between its roots, which the quadratic formula gives as stated after dividing by $n^2(1 + z^2/n)$. Both roots are in $[0, 1]$ because the quadratic is $k^2 \ge 0$ at $p = 0$ and $(n - k)^2 \ge 0$ at $p = 1$, and it is negative at $p = \hat p$ when $0 < k < n$. $\square$

**Lemma 6 (null distribution, simple null).** If $H_0: \theta = \theta_0$ is simple and $I(\theta_0)$ is finite and positive definite, with $E_{\theta_0}[u(\theta_0; X)] = 0$ and $\operatorname{Cov}_{\theta_0}[u(\theta_0; X)] = I(\theta_0)$, then $S \to \chi^2_k$ under $H_0$.

*Proof.* $U_n(\theta_0) = \sum_i u(\theta_0; X_i)$ is a sum of $n$ iid vectors with mean 0 and covariance $I = I(\theta_0)$. By the multivariate [central limit theorem](/central-limit-theorem/), $U_n/\sqrt n \to Z \sim N(0, I)$. Since $I_n = nI$, $S = (U_n/\sqrt n)^\top I^{-1}(U_n/\sqrt n) \to Z^\top I^{-1}Z$ by continuous mapping, and $Z^\top I^{-1}Z = Y^\top Y$ with $Y = I^{-1/2}Z \sim N(0, I_k)$, which is $\chi^2_k$. $\square$

The mean 0 and covariance $I$ of the score hold under the condition that differentiation under the integral sign is allowed, as on the [score function](/score-function/) page. For the normal mean with $\sigma$ known, $S = Z^2$ exactly with $Z \sim N(0, 1)$, so the size is exactly $\alpha$ for every $n$.

**Lemma 7 (null distribution with nuisance parameters).** Write $\theta = (\alpha, \beta)$ with $\alpha \in \mathbb R^r$ tested and $\beta$ free, and let $\tilde\beta$ be the MLE of $\beta$ with $\alpha = \alpha_0$. Assume the conditions of the asymptotic normality of the MLE for the model with $\alpha$ fixed, so that $\tilde\beta$ is consistent and $\frac1n\nabla^2\ell$ converges in probability to $-I$ uniformly near the true value. Then $S \to \chi^2_r$ under $H_0$.

*Proof.* Write $U = (U_\alpha, U_\beta)$ at the true $\theta = (\alpha_0, \beta)$ and split $I$ into blocks. A first-order expansion of $U_\beta(\alpha_0, \tilde\beta) = 0$ around $\beta$ gives $\sqrt n(\tilde\beta - \beta) = I_{\beta\beta}^{-1}U_\beta/\sqrt n + o_p(1)$, and the same expansion of $U_\alpha$ gives
$$\frac{U_\alpha(\alpha_0, \tilde\beta)}{\sqrt n} = \frac{U_\alpha - I_{\alpha\beta}I_{\beta\beta}^{-1}U_\beta}{\sqrt n} + o_p(1).$$
By the central limit theorem the right side tends to $N(0, I_{\alpha\alpha} - I_{\alpha\beta}I_{\beta\beta}^{-1}I_{\beta\alpha})$. This covariance is $((I^{-1})_{\alpha\alpha})^{-1}$, by the formula for the inverse of a block matrix. The score for $\beta$ is 0 at $\tilde\theta_0$, so $S = U_\alpha^\top (I_n(\tilde\theta_0)^{-1})_{\alpha\alpha} U_\alpha = (U_\alpha/\sqrt n)^\top (I(\tilde\theta_0)^{-1})_{\alpha\alpha}(U_\alpha/\sqrt n)$, and $I(\tilde\theta_0) \to I$ in probability by consistency and continuity. As in Lemma 6, the limit is $\chi^2_r$. $\square$

**Lemma 8 (size).** If $S \to \chi^2_r$ under $H_0$, then $P_{H_0}(Q(r/2, S/2) \le \alpha) \to \alpha$.

*Proof.* The upper tail $G(c) = Q(r/2, c/2)$ of $\chi^2_r$ is continuous and strictly decreasing, so $\{G(S) \le \alpha\} = \{S \ge G^{-1}(\alpha)\}$, and its probability tends to $\alpha$ because the limit law has a continuous distribution function. $\square$

**Termination.** Line L1 is one call of the null fit. The solve makes $O(k^3)$ operations, the quadratic form $O(k)$, and the tail one evaluation of the incomplete gamma function, which stops after a bounded number of iterations. The closed forms make one pass over the data or the cells.

**Theorem.** For a positive definite information, SCORE-TEST returns $S = u^\top J^{-1}u \ge 0$ at the restricted MLE and $p = P(\chi^2_r \ge S)$. The closed forms equal this statistic, the multinomial one is Pearson's $X^2$, the statistic is invariant under reparametrization with expected information, and rejecting when $p \le \alpha$ has size tending to $\alpha$ under the stated conditions.

*Proof.* Lemmas 1 to 8. $\blacksquare$
