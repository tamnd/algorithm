---
title: Student's t statistic has the t distribution with n - 1 degrees of freedom under normal iid data
proves: [correctness, termination]
status: full
---

We prove that the statistics of the one-sample, paired and pooled t-tests have exact t null distributions under their normal models, that the returned p-values are the stated tail probabilities with size exactly $\alpha$, and that without normality the size tends to $\alpha$. Write $t_{\nu}$ for the t distribution with $\nu$ degrees of freedom: the law of $Z/\sqrt{V/\nu}$ where $Z \sim N(0, 1)$ and $V \sim \chi^2_\nu$ are independent. $S^2$ always has the divisor $n - 1$.

**Lemma 1 (Helmert's transformation).** Let $X_1, \dots, X_n$ be iid $N(\mu, \sigma^2)$, $n \ge 2$. Then $\bar X$ and $S^2 = \frac{1}{n-1}\sum (X_i - \bar X)^2$ are independent, $\bar X \sim N(\mu, \sigma^2/n)$, and $(n - 1)S^2/\sigma^2 \sim \chi^2_{n-1}$.

*Proof.* Let $H$ be an orthogonal $n \times n$ matrix whose first row is $(1/\sqrt n, \dots, 1/\sqrt n)$; one exists because a unit vector can be completed to an orthonormal basis (Gram-Schmidt). Let $W = (X - \mu\mathbf 1)/\sigma$, a vector of iid $N(0, 1)$ variables, with density $(2\pi)^{-n/2}\exp(-\|w\|^2/2)$. Let $U = HW$. The map $w \mapsto Hw$ has Jacobian $|\det H| = 1$ and keeps $\|w\|$, so $U$ has the same density: $U_1, \dots, U_n$ are iid $N(0, 1)$. Now $U_1 = \sqrt n\,\bar W = \sqrt n(\bar X - \mu)/\sigma$. Also $\sum_{i=1}^n U_i^2 = \|W\|^2 = \sum W_i^2$, so $\sum_{i=2}^n U_i^2 = \sum W_i^2 - n\bar W^2 = \sum (W_i - \bar W)^2 = (n - 1)S^2/\sigma^2$. So $\bar X$ is a function of $U_1$ alone, and $S^2$ of $U_2, \dots, U_n$ alone, which makes them independent. $U_1 \sim N(0, 1)$ gives the law of $\bar X$, and a sum of $n - 1$ squares of iid standard normals is $\chi^2_{n-1}$ by definition. $\square$

**Lemma 2 (the one-sample null law).** Under the model of Lemma 1, $T = (\bar X - \mu_0)/(S/\sqrt n)$ has the law of $(Z + \lambda)/\sqrt{V/(n-1)}$ with $Z \sim N(0, 1)$, $V \sim \chi^2_{n-1}$ independent, and $\lambda = \sqrt n(\mu - \mu_0)/\sigma$. In particular $T \sim t_{n-1}$ when $\mu = \mu_0$, whatever $\sigma$ is.

*Proof.* Divide the numerator and the denominator by $\sigma/\sqrt n$: $T = Z'/\sqrt{V/(n-1)}$ with $Z' = \sqrt n(\bar X - \mu_0)/\sigma \sim N(\lambda, 1)$ and $V = (n - 1)S^2/\sigma^2$. By Lemma 1, $Z'$ and $V$ are independent and $V \sim \chi^2_{n-1}$. At $\mu = \mu_0$, $\lambda = 0$, and the law is $t_{n-1}$ by definition. $\sigma$ has cancelled. $\square$

**Lemma 3 (paired data).** If the pairs $(X_i, Y_i)$ are iid and $D_i = X_i - Y_i \sim N(\delta, \sigma_D^2)$, then the paired statistic is the one-sample statistic of $D_1, \dots, D_n$ with $\mu_0 = \delta_0$, and it is $t_{n-1}$ under $H_0: \delta = \delta_0$.

*Proof.* The code forms $d_i = x_i - y_i$ and calls the one-sample test, and the $D_i$ are iid $N(\delta, \sigma_D^2)$, so Lemma 2 applies. This holds in particular when each pair is bivariate normal, whatever the correlation in the pair. $\square$

**Lemma 4 (the pooled null law).** Let $X_1, \dots, X_m$ be iid $N(\mu_X, \sigma^2)$ and $Y_1, \dots, Y_n$ iid $N(\mu_Y, \sigma^2)$, independent, with the same $\sigma$, and $m + n \ge 3$. Let $S_p^2 = (SS_X + SS_Y)/(m + n - 2)$, where $SS$ is the sum of squared deviations from the sample's own mean. Then $T = (\bar X - \bar Y - \delta_0)/(S_p\sqrt{1/m + 1/n}) \sim t_{m+n-2}$ when $\mu_X - \mu_Y = \delta_0$.

*Proof.* By Lemma 1 applied to each sample (for a sample of size 1, $SS = 0$ and the claims about $\bar X$ hold trivially), $\bar X$, $SS_X$, $\bar Y$, $SS_Y$ are independent, with $SS_X/\sigma^2 \sim \chi^2_{m-1}$ and $SS_Y/\sigma^2 \sim \chi^2_{n-1}$ (where $\chi^2_0$ is the point mass at 0). A sum of independent chi-square variables is chi-square with the summed degrees of freedom (multiply their moment generating functions $(1 - 2s)^{-k/2}$), so $V = (SS_X + SS_Y)/\sigma^2 \sim \chi^2_{m+n-2}$. Also $\bar X - \bar Y \sim N(\mu_X - \mu_Y, \sigma^2(1/m + 1/n))$, independent of $V$. Under $H_0$, $T = Z/\sqrt{V/(m + n - 2)}$ with $Z \sim N(0, 1)$. $\square$

The common $\sigma$ is used twice: it makes $V$ chi-square, and it makes the same $\sigma$ cancel from $Z$ and $V$. With $\sigma_X \ne \sigma_Y$, $(SS_X + SS_Y)$ is a weighted sum of two chi-square variables, $T$ is not $t$, and its law depends on $\sigma_X/\sigma_Y$.

**Lemma 5 (p-values and size).** Let $F_\nu$ be the CDF of $t_\nu$ and $\bar F_\nu = 1 - F_\nu$. The code returns $\bar F_\nu(t)$ ("greater"), $\bar F_\nu(-t) = F_\nu(t)$ ("less") and $2\bar F_\nu(|t|)$ (two-sided). Under a null where $T \sim t_\nu$, each p-value satisfies $P(p \le u) = u$ for $u \in [0, 1]$, so rejecting when $p \le \alpha$ has size exactly $\alpha$.

*Proof.* The $t_\nu$ law is symmetric about 0 (because $Z$ is) and has a positive density on the real line, so $F_\nu$ is continuous and strictly increasing, and $\bar F_\nu(-t) = F_\nu(t)$. The p-values are the probabilities of $\{T \ge t\}$, $\{T \le t\}$ and $\{|T| \ge |t|\}$. Uniformity follows as for any continuous statistic: $\{\bar F_\nu(T) \le u\} = \{T \ge F_\nu^{-1}(1 - u)\}$ has probability $u$, and $\{2\bar F_\nu(|T|) \le u\} = \{|T| \ge F_\nu^{-1}(1 - u/2)\}$ has probability $u$. The helper function t_sf computes $\bar F_\nu(t) = \tfrac12 I_{\nu/(\nu + t^2)}(\nu/2, 1/2)$ for $t \ge 0$, the standard identity for the t tail through the regularized incomplete beta function. $\square$

**Lemma 6 (the composite one-sided null).** For $H_0: \mu \le \mu_0$, the rule "reject when $T \ge F_{n-1}^{-1}(1 - \alpha)$" has size exactly $\alpha$.

*Proof.* By Lemma 2, $P_{\mu,\sigma}(T \ge c) = P((Z + \lambda)/\sqrt{V/\nu} \ge c)$. For each fixed value of $V$, the event $\{Z \ge c\sqrt{V/\nu} - \lambda\}$ grows with $\lambda$, so by independence and averaging over $V$ the probability is nondecreasing in $\lambda$, which increases with $\mu$. Its supremum over $\mu \le \mu_0$ and all $\sigma$ is its value at $\lambda = 0$, which is $\alpha$. $\square$

**Lemma 7 (without normality).** Let $X_1, \dots, X_n$ be iid with mean $\mu_0$ and variance $\sigma^2 \in (0, \infty)$, of any shape. Then $T$ converges in distribution to $N(0, 1)$, and the size of each rule tends to $\alpha$.

*Proof.* By the [central limit theorem](/central-limit-theorem/), $\sqrt n(\bar X - \mu_0)/\sigma$ converges in distribution to $N(0, 1)$. By the [law of large numbers](/law-of-large-numbers/), $\frac1n\sum X_i^2 \to \sigma^2 + \mu_0^2$ and $\bar X \to \mu_0$ in probability, so $S^2 = \frac{n}{n-1}(\frac1n\sum X_i^2 - \bar X^2) \to \sigma^2$ in probability, and $\sigma/S \to 1$ in probability by continuity. Slutsky's theorem (a product with a factor that converges in probability to a constant) gives $T = \frac{\sigma}{S}\cdot\frac{\sqrt n(\bar X - \mu_0)}{\sigma} \to N(0, 1)$ in distribution. The critical values $F_{n-1}^{-1}(1 - \alpha)$ tend to $z_{1-\alpha}$, because $V/\nu \to 1$ in probability for $V \sim \chi^2_\nu$. The limit law is continuous, so the rejection probabilities tend to $\alpha$. $\square$

**Termination.** The one-sample test makes two passes over $n$ numbers and a constant number of further operations. The p-value calls the incomplete beta continued fraction, which stops when a step changes the value by a relative amount below $10^{-16}$ or after a fixed cap of iterations. So the test stops after $O(n)$ arithmetic operations plus a bounded number of iterations.

**Theorem.** Under iid normal data, Student's one-sample and paired tests return $T$ with $T \sim t_{n-1}$ under $H_0$, the pooled test returns $T \sim t_{m+n-2}$ under $H_0$ when the two variances are equal, and the p-values give tests of size exactly $\alpha$ for every sample size. Without normality, for iid data with finite positive variance, the one-sample size tends to $\alpha$.

*Proof.* Lemmas 1 to 6 for the exact claims, and Lemma 7 for the limit. $\blacksquare$
