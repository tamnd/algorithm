---
title: The Welch statistic, the Welch-Satterthwaite degrees of freedom, their bounds and the limits where the size is exact
proves: [correctness, termination]
status: full
---

We prove what is true of Welch's test and say plainly what is not. The test is approximate: we derive the degrees of freedom by moment matching, prove their bounds, prove that equal sample sizes give the pooled statistic, and prove that the size tends to $\alpha$ in two limits. We do not prove that the size equals $\alpha$, because it does not. Throughout, $X_1, \dots, X_m$ are iid $N(\mu_X, \sigma_X^2)$ and $Y_1, \dots, Y_n$ are iid $N(\mu_Y, \sigma_Y^2)$, independent of each other, with $m, n \ge 2$, and $\sigma_X, \sigma_Y > 0$ are unknown and may differ. $S_X^2$ and $S_Y^2$ are the sample variances with divisors $m - 1$ and $n - 1$. Write

$$A = S_X^2/m, \quad B = S_Y^2/n, \quad \alpha_0 = \sigma_X^2/m, \quad \beta_0 = \sigma_Y^2/n, \quad \theta = \alpha_0 + \beta_0 = \operatorname{Var}(\bar X - \bar Y),$$

$T = (\bar X - \bar Y - \delta_0)/\sqrt{A + B}$ and $\nu(a, b) = (a + b)^2/\big(a^2/(m - 1) + b^2/(n - 1)\big)$. The code returns $T$, $\hat\nu = \nu(A, B)$ and the $t_{\hat\nu}$ tail of $T$.

**Lemma 1 (the parts are independent).** $Z = (\bar X - \bar Y - (\mu_X - \mu_Y))/\sqrt\theta \sim N(0, 1)$, $(m - 1)S_X^2/\sigma_X^2 \sim \chi^2_{m-1}$, $(n - 1)S_Y^2/\sigma_Y^2 \sim \chi^2_{n-1}$, and the three are independent.

*Proof.* Within one normal sample, the mean and the sample variance are independent, the mean is $N(\mu, \sigma^2/\text{size})$, and (size $- 1$) times the sample variance over $\sigma^2$ is chi-square with size $- 1$ degrees of freedom. This is Helmert's transformation, Lemma 1 of the correctness proof of [Student's t-test](/student-t-test/). The two samples are independent, so $\bar X, S_X^2, \bar Y, S_Y^2$ are four independent variables. $\bar X - \bar Y$ is normal with mean $\mu_X - \mu_Y$ and variance $\alpha_0 + \beta_0 = \theta$. $\square$

So under $H_0: \mu_X - \mu_Y = \delta_0$, $T = Z\big/\sqrt{(A + B)/\theta}$ with $Z \sim N(0, 1)$ independent of $A + B$. If $(A + B)/\theta$ were $\chi^2_\nu/\nu$ for some $\nu$, $T$ would be $t_\nu$ exactly. It is not: $A + B = \alpha_0 V_1/(m - 1) + \beta_0 V_2/(n - 1)$ with independent $V_1 \sim \chi^2_{m-1}$ and $V_2 \sim \chi^2_{n-1}$, a weighted sum of two chi-square variables, whose law depends on the ratio $\alpha_0/\beta_0$.

**Lemma 2 (the first two moments).** $E[A + B] = \theta$ and $\operatorname{Var}(A + B) = 2\alpha_0^2/(m - 1) + 2\beta_0^2/(n - 1)$.

*Proof.* A $\chi^2_k$ variable has mean $k$ and variance $2k$ (it is a sum of $k$ independent squares of standard normals, and $E[Z^2] = 1$, $E[Z^4] = 3$). So $A = \alpha_0 V_1/(m - 1)$ has mean $\alpha_0$ and variance $\alpha_0^2 \cdot 2(m - 1)/(m - 1)^2 = 2\alpha_0^2/(m - 1)$, and the same for $B$. $A$ and $B$ are independent, so the variances add. $\square$

**Lemma 3 (Satterthwaite's moment matching).** The scaled chi-square variable $c\,\chi^2_\nu/\nu$ with the same mean and variance as $A + B$ has $c = \theta$ and $\nu = \nu(\alpha_0, \beta_0)$.

*Proof.* $c\,\chi^2_\nu/\nu$ has mean $c$ and variance $2c^2/\nu$. Matching the mean gives $c = \theta$. Matching the variance gives $2\theta^2/\nu = 2\alpha_0^2/(m - 1) + 2\beta_0^2/(n - 1)$ by Lemma 2, so $\nu = (\alpha_0 + \beta_0)^2/\big(\alpha_0^2/(m - 1) + \beta_0^2/(n - 1)\big) = \nu(\alpha_0, \beta_0)$. $\square$

The unknown $\alpha_0, \beta_0$ are replaced by their unbiased estimates $A, B$, which gives $\hat\nu = \nu(A, B)$, the value of welch_df. Both steps are approximations: the law of $A + B$ is not a scaled chi-square, and $\hat\nu$ is random. Lemma 3 explains the formula; it does not give an exact null law.

**Lemma 4 (bounds on $\nu$).** For $a, b \ge 0$ with $a + b > 0$, $\min(m, n) - 1 \le \nu(a, b) \le m + n - 2$. The upper bound is an equality exactly when $a/(m - 1) = b/(n - 1)$, and the lower bound is approached when the variance part of the smaller sample dominates.

*Proof.* Let $p = m - 1$ and $q = n - 1$. Upper bound: by the Cauchy-Schwarz inequality for the vectors $(a/\sqrt p, b/\sqrt q)$ and $(\sqrt p, \sqrt q)$,

$$(a + b)^2 = \Big(\frac{a}{\sqrt p}\sqrt p + \frac{b}{\sqrt q}\sqrt q\Big)^2 \le \Big(\frac{a^2}{p} + \frac{b^2}{q}\Big)(p + q),$$

so $\nu \le p + q = m + n - 2$, with equality exactly when the vectors are proportional, that is $a/p = b/q$. Lower bound: let $k = \min(p, q)$. Then $a^2/p + b^2/q \le (a^2 + b^2)/k \le (a + b)^2/k$, the last step because $2ab \ge 0$, so $\nu \ge k$. If $b = 0$ then $\nu = p$, and if $a = 0$ then $\nu = q$; so $\nu$ moves from the degrees of freedom of the sample that carries all the variance to $p + q$ when the two parts are balanced. $\square$

**Lemma 5 (equal sample sizes).** If $m = n$, the Welch statistic equals the pooled statistic $T_p = (\bar X - \bar Y - \delta_0)/(S_p\sqrt{2/n})$, and $\hat\nu \le 2n - 2$ with equality exactly when $S_X^2 = S_Y^2$.

*Proof.* With $m = n$, $S_p^2 = \big((n - 1)S_X^2 + (n - 1)S_Y^2\big)/(2n - 2) = (S_X^2 + S_Y^2)/2$, so $S_p^2 \cdot 2/n = (S_X^2 + S_Y^2)/n = A + B$, and the denominators agree. The claim on $\hat\nu$ is Lemma 4 with $p = q$: equality iff $A = B$, that is $S_X^2 = S_Y^2$. $\square$

So with equal sizes the two tests differ only in the degrees of freedom: the pooled test uses $2n - 2$ and Welch's test uses a data-dependent value at most $2n - 2$.

**Lemma 6 (one dominant variance: the size tends to $\alpha$ exactly).** Fix $m$, $n$ and $\sigma_X$, and let $\sigma_Y \to 0$. Under $H_0$, the rejection probability of each of the three rules at level $\alpha$ tends to $\alpha$. The same holds with the roles of the samples exchanged.

*Proof.* Write $\bar X - \bar Y - \delta_0 = (\bar X - \mu_X) - (\bar Y - \mu_Y)$ under $H_0$. As $\sigma_Y \to 0$, $\bar Y - \mu_Y \sim N(0, \beta_0)$ and $B = \beta_0 V_2/(n - 1)$ both tend to 0 in probability, while the law of $(\bar X, A)$ does not change. So, by Slutsky's theorem and the continuity of $(u, a, b) \mapsto u/\sqrt{a + b}$ at $b = 0$, $a > 0$ (and $A > 0$ almost surely), $T$ converges in distribution to $T_X = (\bar X - \mu_X)/\sqrt{A}$, the one-sample t statistic of the $X$ sample, which is $t_{m-1}$ by Lemma 2 of the Student proof. In the same way $\hat\nu = \nu(A, B) \to \nu(A, 0) = m - 1$, jointly with $T$. The p-value is a continuous function of $(t, \nu)$ for $\nu > 0$ (the $t_\nu$ tail is continuous in both arguments), so by the continuous mapping theorem it converges in distribution to the $t_{m-1}$ tail of $T_X$, which is uniform on $[0, 1]$ (Lemma 5 of the Student proof). The uniform law is continuous at $\alpha$, so $P(p \le \alpha) \to \alpha$. $\square$

**Lemma 7 (large samples: the size tends to $\alpha$).** Let $X_1, \dots, X_m$ be iid with mean $\mu_X$ and finite variance $\sigma_X^2 > 0$ and $Y_1, \dots, Y_n$ iid with mean $\mu_Y$ and finite variance $\sigma_Y^2 > 0$, independent, of any shape. If $m, n \to \infty$ (at any relative rate), then under $H_0$ the statistic $T$ converges in distribution to $N(0, 1)$ and the size of each rule tends to $\alpha$.

*Proof.* Let $Z_X = (\bar X - \mu_X)/\sqrt{\alpha_0}$ and $Z_Y = (\bar Y - \mu_Y)/\sqrt{\beta_0}$, and $w_X = \sqrt{\alpha_0/\theta}$, $w_Y = \sqrt{\beta_0/\theta}$, so $w_X^2 + w_Y^2 = 1$ and $(\bar X - \bar Y - \delta_0)/\sqrt\theta = w_X Z_X - w_Y Z_Y$ under $H_0$. By the [central limit theorem](/central-limit-theorem/), the characteristic functions $\varphi_X$ of $Z_X$ and $\varphi_Y$ of $Z_Y$ tend to $e^{-s^2/2}$, and by Lévy's continuity theorem the convergence is uniform for $s$ in compact sets. The weights stay in $[0, 1]$, so by independence the characteristic function of $w_X Z_X - w_Y Z_Y$ at $s$ is $\varphi_X(w_X s)\varphi_Y(-w_Y s) = e^{-w_X^2 s^2/2}e^{-w_Y^2 s^2/2} + o(1) = e^{-s^2/2} + o(1)$, which gives the $N(0, 1)$ limit. By the [law of large numbers](/law-of-large-numbers/), $A/\alpha_0 = S_X^2/\sigma_X^2 \to 1$ and $B/\beta_0 \to 1$ in probability, so $(A + B)/\theta = w_X^2 (A/\alpha_0) + w_Y^2 (B/\beta_0) \to 1$ in probability, and Slutsky's theorem gives $T \to N(0, 1)$ in distribution. By Lemma 4, $\hat\nu \ge \min(m, n) - 1 \to \infty$, so the $t_{\hat\nu}$ critical values tend to the normal ones. The limit law is continuous, so the rejection probabilities tend to $\alpha$. $\square$

**What is not proved.** Between these limits the exact size of the Welch rule is a function of $\sigma_X^2/\sigma_Y^2$, $m$ and $n$ that is not constant and not equal to $\alpha$. This is the Behrens-Fisher problem. We do not prove a formula for it; the measurements on the page (for example a size of 0.119 at $m = 2$, $n = 20$, equal variances, $\alpha = 0.05$, with $r = 20000$ replications and seed 11) show that it can differ from $\alpha$ by much more than the Monte Carlo error.

**Termination.** Lines L1 and L2 make two passes over each sample, L3 to L5 are a constant number of operations, and the $t_{\hat\nu}$ tail is the incomplete beta continued fraction of the shared helper, which stops after a fixed cap of iterations. So the test stops after $O(m + n)$ arithmetic operations plus a bounded number of iterations.

**Theorem.** For independent normal samples, Welch's test returns $T$ and $\hat\nu = \nu(A, B)$ with $\min(m, n) - 1 \le \hat\nu \le m + n - 2$. With $m = n$ its statistic is the pooled statistic. Its size tends to $\alpha$ when one of the two variances tends to 0, and, for any populations with finite positive variances, when both sample sizes grow. Elsewhere it is an approximation whose error is measured, not bounded.

*Proof.* Lemmas 4 and 5 for the first two claims, Lemmas 6 and 7 for the limits, and Lemma 3 with the remark after Lemma 1 for the nature of the approximation. $\blacksquare$
