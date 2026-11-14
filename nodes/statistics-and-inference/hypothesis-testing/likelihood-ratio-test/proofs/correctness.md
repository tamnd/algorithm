---
title: The likelihood ratio test returns a nonnegative statistic with the stated closed forms, its p-value has size tending to alpha, and the finite routine returns the Neyman-Pearson test
proves: [correctness, termination]
status: full
---

We prove that LIKELIHOOD-RATIO-TEST returns $\Lambda = 2(\ell(\hat\theta) - \ell(\hat\theta_0)) \ge 0$, that $\Lambda$ does not depend on the parametrization, that the closed forms of the model table are correct, that the deviance series is exact, that the p-value has size tending to $\alpha$ under the conditions of Wilks' theorem (and exactly $\alpha$ for a normal mean with known $\sigma$), and that the routine for a simple null against a simple alternative on a finite sample space returns a most powerful test of size $\alpha$. We do not prove Wilks' theorem here; it is proved on its own page.

**Lemma 1 (nonnegative).** If $\Theta_0 \subseteq \Theta$, $\hat\theta$ maximizes $\ell$ over $\Theta$ and $\hat\theta_0$ maximizes $\ell$ over $\Theta_0$, then $\Lambda \ge 0$.

*Proof.* $\hat\theta_0 \in \Theta_0 \subseteq \Theta$, so $\ell(\hat\theta_0) \le \sup_\Theta \ell = \ell(\hat\theta)$. $\square$

Line L4 does not change the value when the maximizers are exact. It only sets to 0 a negative value that comes from rounding or from an optimizer that stops early.

**Lemma 2 (invariance).** Let $g$ be a one-to-one map from $\Theta$ onto $\Psi$, and write the model in the new parameter as $\tilde\ell(\psi) = \ell(g^{-1}(\psi))$, with null set $\Psi_0 = g(\Theta_0)$. Then the LRT statistic in $\psi$ equals $\Lambda$.

*Proof.* $\sup_{\psi \in \Psi} \tilde\ell(\psi) = \sup_{\theta \in \Theta} \ell(\theta)$, because $g$ is a bijection from $\Theta$ to $\Psi$; the same holds for $\Psi_0$ and $\Theta_0$. The statistic depends only on these two suprema. $\square$

**Lemma 3 (the deviance form).** For $a \ge 0$ and $b > 0$, let $D(a, b) = a\log(a/b) - a + b$ with $0\log 0 = 0$. Then $D(a, b) = b\,h(a/b)$ with $h(t) = t\log t - t + 1 \ge 0$, and $h(t) = 0$ only at $t = 1$. For $|d| < 1$, $h(1 + d) = \sum_{j \ge 2} (-1)^j d^j/(j(j - 1))$.

*Proof.* $b\,h(a/b) = a\log(a/b) - a + b$ by expanding. $h(1) = 0$, $h'(t) = \log t$, and $h''(t) = 1/t > 0$, so $h$ is strictly convex with its minimum 0 at $t = 1$; $h(0) = 1$ by continuity. For the series, $h(1 + d) = (1 + d)\log(1 + d) - d$. With $\log(1 + d) = \sum_{j \ge 1} (-1)^{j+1}d^j/j$ for $|d| < 1$, the coefficient of $d^j$ in $(1 + d)\log(1 + d)$ is $(-1)^{j+1}/j + (-1)^j/(j - 1)$ for $j \ge 2$, which equals $(-1)^j/(j(j - 1))$, and the coefficient of $d$ is 1, which cancels with $-d$. $\square$

When $|d| < 0.1$, the terms of the series decrease in size by a factor of at least $0.1$ and alternate in sign after the first, so stopping when a term is below $10^{-17}$ of the sum leaves a relative error below that bound, plus rounding. No subtraction of nearly equal numbers occurs, because every term is computed from $d$ directly.

**Lemma 4 (closed forms).** The table of the algorithm section is correct:

1. Binomial, $K = k$ successes in $n$ trials, $H_0: p = p_0$: $\Lambda = 2(D(k, np_0) + D(n - k, n(1 - p_0)))$.
2. Poisson, $n$ counts with sum $t$, $H_0: \lambda = \lambda_0$: $\Lambda = 2D(t, n\lambda_0)$.
3. Normal, $\sigma$ known, $H_0: \mu = \mu_0$: $\Lambda = n(\bar x - \mu_0)^2/\sigma^2$.
4. Normal, $\sigma$ unknown, $H_0: \mu = \mu_0$, with $SS = \sum (x_i - \bar x)^2 > 0$: $\Lambda = n\log(1 + n(\bar x - \mu_0)^2/SS) = n\log(1 + T^2/(n - 1))$, where $T = \sqrt n(\bar x - \mu_0)/S$ and $S^2 = SS/(n - 1)$.
5. Multinomial, counts $O_1, \dots, O_m$ with sum $n$, $H_0$: probabilities $q_j > 0$: $\Lambda = 2\sum_j D(O_j, nq_j)$.

*Proof.* (1) $\ell(p) = k\log p + (n - k)\log(1 - p)$ plus a constant, maximized at $\hat p = k/n$ (at an endpoint if $k \in \{0, n\}$, with $0\log 0 = 0$). Then $\Lambda = 2[k\log(k/(np_0)) + (n - k)\log((n - k)/(n(1 - p_0)))]$. The linear parts of the two $D$ terms are $-k + np_0 - (n - k) + n(1 - p_0) = 0$, so the sum of the $D$ terms is the same.

(2) $\ell(\lambda) = t\log\lambda - n\lambda$ plus a constant, maximized at $\hat\lambda = t/n$. So $\Lambda = 2[t\log(t/(n\lambda_0)) - t + n\lambda_0] = 2D(t, n\lambda_0)$.

(3) $\ell(\mu) = -\sum (x_i - \mu)^2/(2\sigma^2)$ plus a constant, maximized at $\bar x$. With $\sum (x_i - \mu_0)^2 = SS + n(\bar x - \mu_0)^2$, $\Lambda = n(\bar x - \mu_0)^2/\sigma^2$.

(4) $\ell(\mu, v) = -\tfrac n2\log v - \sum(x_i - \mu)^2/(2v)$ plus a constant. For fixed $\mu$ it is maximized at $v(\mu) = \sum(x_i - \mu)^2/n$, with value $-\tfrac n2\log v(\mu) - \tfrac n2$. The full maximum is at $\mu = \bar x$, $v = SS/n$; the restricted one at $v_0 = (SS + n(\bar x - \mu_0)^2)/n$. So $\Lambda = n\log(v_0/(SS/n)) = n\log(1 + n(\bar x - \mu_0)^2/SS)$. Since $T^2 = n(\bar x - \mu_0)^2(n - 1)/SS$, this is $n\log(1 + T^2/(n - 1))$.

(5) $\ell(q) = \sum_j O_j\log q_j$ plus a constant, maximized over the simplex at $\hat q_j = O_j/n$ (Gibbs' inequality: $\sum_j O_j\log(\hat q_j/q_j) = n\,\mathrm{KL}(\hat q\,\|\,q) \ge 0$). So $\Lambda = 2\sum_j O_j\log(O_j/(nq_j))$, and the linear parts $\sum_j(-O_j + nq_j) = -n + n = 0$ add nothing. $\square$

**Lemma 5 (p-value and size).** Let $p = Q(r/2, \Lambda/2) = P(\chi^2_r \ge \Lambda)$.

1. If $\Lambda \sim \chi^2_r$ exactly under $H_0$, then $P_{H_0}(p \le \alpha) = \alpha$ for all $\alpha \in [0, 1]$.
2. If $\Lambda \to \chi^2_r$ in distribution under $H_0$, then $P_{H_0}(p \le \alpha) \to \alpha$.
3. For a normal mean with known $\sigma$, $\Lambda \sim \chi^2_1$ exactly under $H_0$, for every $n \ge 1$.

*Proof.* The survival function $G(c) = P(\chi^2_r \ge c)$ is continuous and strictly decreasing on $[0, \infty)$, from 1 to 0. So $\{p \le \alpha\} = \{\Lambda \ge G^{-1}(\alpha)\}$ for $0 < \alpha < 1$. In case 1 this has probability $G(G^{-1}(\alpha)) = \alpha$. In case 2 the limit law has a continuous CDF, so $P(\Lambda \ge c) \to G(c)$ for each fixed $c$, and the same set has probability tending to $\alpha$. For case 3, $Z = \sqrt n(\bar X - \mu_0)/\sigma \sim N(0, 1)$ under $H_0$, as on the z-test page, and $\Lambda = Z^2$, which is $\chi^2_1$ by definition. $\square$

Case 2 holds under the conditions of [Wilks' theorem](/wilks-theorem/). The routine does not check them, and for finite $n$ its size is only measured, not proved: the exact binomial sizes are computed in the tests by enumeration, for example 0.0414 at $n = 20$.

**Lemma 6 (the finite Neyman-Pearson routine).** Let $f_0, f_1$ be probability vectors on $\{1, \dots, m\}$ and $0 \le \alpha \le 1$. MOST-POWERFUL-TEST returns $\phi \in [0, 1]^m$ with $\sum_i \phi_i f_0(i) = \alpha$, and $\phi$ maximizes $\sum_i \phi_i f_1(i)$ over all $\psi \in [0, 1]^m$ with $\sum_i \psi_i f_0(i) \le \alpha$.

*Proof.* The routine sets $\phi_i = 1$ where $f_0(i) = 0 < f_1(i)$, which costs no size. It then takes the distinct values $k$ of $f_1/f_0$ on $\{f_0 > 0\}$ in decreasing order, including the value 0, and gives each class the share $\min(1, \text{budget}/\text{mass})$, where mass is the $f_0$ mass of the class, until the budget is 0. The total $f_0$ mass of all classes is 1 $\ge \alpha$, so the budget reaches 0 at some class; let $k^* \ge 0$ be its ratio. Every share is in $[0, 1]$, and the shares spend exactly $\alpha$, so $\sum_i \phi_i f_0(i) = \alpha$. Also $\phi_i = 1$ where $f_1(i) > k^* f_0(i)$, $\phi_i = 0$ where $f_1(i) < k^* f_0(i)$, and $\phi$ is constant on the class $f_1 = k^* f_0$. The points with $f_0 = 0 = f_1$ get $\phi_i = 0$ and contribute nothing to size or power. For optimality, take any $\psi$ as in the statement. For every $i$, $(\phi_i - \psi_i)(f_1(i) - k^* f_0(i)) \ge 0$, because $\phi_i = 1 \ge \psi_i$ where the second factor is positive and $\phi_i = 0 \le \psi_i$ where it is negative. Summing, $\sum(\phi_i - \psi_i) f_1(i) \ge k^* \sum(\phi_i - \psi_i) f_0(i) = k^*(\alpha - \sum \psi_i f_0(i)) \ge 0$. So the power of $\phi$ is at least that of $\psi$. $\square$

This is the sufficiency part of the [Neyman-Pearson lemma](/neyman-pearson-lemma/), applied to the vector the routine builds. The tests compare it with the best of all vertex tests of the linear program, in exact rational arithmetic.

**Termination.** The general routine calls each maximizer once and does a constant number of further operations, so it stops if the maximizers stop. Each closed form makes one pass over the data or the cells. The deviance series stops because its terms decrease geometrically when $|d| < 0.1$ and the sum is bounded below by its first term $d^2/2 > 0$ (the case $d = 0$ returns 0 after one term). MOST-POWERFUL-TEST loops at most $m$ times over the distinct ratio values.

**Theorem.** LIKELIHOOD-RATIO-TEST returns $\Lambda = 2(\ell(\hat\theta) - \ell(\hat\theta_0)) \ge 0$ and $p = P(\chi^2_r \ge \Lambda)$. The statistic is invariant under reparametrization, the closed forms agree with the general definition, and rejecting when $p \le \alpha$ has size tending to $\alpha$ whenever $\Lambda \to \chi^2_r$ under $H_0$, and size exactly $\alpha$ for the normal mean with known $\sigma$. MOST-POWERFUL-TEST returns a most powerful test of size $\alpha$.

*Proof.* Lemmas 1 to 6. $\blacksquare$
