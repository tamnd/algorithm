---
title: The z-test has exact size alpha under normal data with known sigma, and the proportion z-test has size tending to alpha
proves: [correctness, termination]
status: full
---

We prove that the statistic of Z-TEST has the standard normal distribution under $H_0$, that the rejection rules have size exactly $\alpha$, that the p-values are the stated tail probabilities and are uniform under $H_0$, and that the proportion version has size that tends to $\alpha$. $\Phi$ is the standard normal CDF and $z_p = \Phi^{-1}(p)$ is its lower $p$-quantile.

**Lemma 1 (the null distribution).** Let $X_1, \dots, X_n$ be iid $N(\mu, \sigma^2)$ with $\sigma > 0$ known. Then $Z = \sqrt n(\bar X - \mu_0)/\sigma$ has the distribution $N(\lambda, 1)$ with $\lambda = \sqrt n(\mu - \mu_0)/\sigma$. In particular $Z \sim N(0, 1)$ exactly when $\mu = \mu_0$, for every $n \ge 1$.

*Proof.* The moment generating function of $X_i$ is $M(s) = \exp(\mu s + \sigma^2 s^2/2)$. By independence, the moment generating function of $\sum X_i$ is $M(s)^n = \exp(n\mu s + n\sigma^2 s^2/2)$, which is that of $N(n\mu, n\sigma^2)$. A moment generating function that is finite near 0 fixes the distribution, so $\sum X_i \sim N(n\mu, n\sigma^2)$. An affine map $a + bY$ of a normal $Y \sim N(m, v)$ is $N(a + bm, b^2 v)$, by the same argument. With $b = 1/(\sqrt n\,\sigma)$ and $a = -\sqrt n\,\mu_0/\sigma$, $Z = a + b\sum X_i$ has mean $\sqrt n(\mu - \mu_0)/\sigma$ and variance $n\sigma^2/(n\sigma^2) = 1$. $\square$

**Lemma 2 (the two-sample statistic).** Let $X_1, \dots, X_m$ be iid $N(\mu_X, \sigma_X^2)$ and $Y_1, \dots, Y_n$ iid $N(\mu_Y, \sigma_Y^2)$, the two samples independent, with $\sigma_X, \sigma_Y$ known. Then $Z = (\bar X - \bar Y - \delta_0)/\sqrt{\sigma_X^2/m + \sigma_Y^2/n} \sim N(0, 1)$ when $\mu_X - \mu_Y = \delta_0$.

*Proof.* By Lemma 1, $\bar X \sim N(\mu_X, \sigma_X^2/m)$ and $\bar Y \sim N(\mu_Y, \sigma_Y^2/n)$, and they are independent. The product of their moment generating functions at $s$ and $-s$ shows $\bar X - \bar Y \sim N(\mu_X - \mu_Y, \sigma_X^2/m + \sigma_Y^2/n)$. Standardize as in Lemma 1. $\square$

**Lemma 3 (p-values and size).** Let $Z \sim N(0, 1)$ under $H_0$, and let $z$ be the observed value. The p-values computed by NORMAL-P-VALUE are $P_{H_0}(Z \ge z)$ for "greater", $P_{H_0}(Z \le z)$ for "less" and $P_{H_0}(|Z| \ge |z|)$ for "two-sided". For each, $P_{H_0}(p \le u) = u$ for every $u \in [0, 1]$. So the rule "reject when $p \le \alpha$" has size exactly $\alpha$.

*Proof.* $P(Z \ge z) = 1 - \Phi(z) = \bar\Phi(z)$, which the code computes as $\tfrac12\operatorname{erfc}(z/\sqrt2)$; this is the same function, since $\Phi(x) = \tfrac12\operatorname{erfc}(-x/\sqrt2)$ and $\operatorname{erfc}(-t) = 2 - \operatorname{erfc}(t)$. $P(Z \le z) = \Phi(z)$. By symmetry of the standard normal, $P(|Z| \ge |z|) = 2\bar\Phi(|z|)$, which is at most 1 because $\bar\Phi(|z|) \le 1/2$; the min with 1 only guards rounding. For uniformity, take "greater": $p = \bar\Phi(Z)$, and $\bar\Phi$ is continuous and strictly decreasing, so $\{p \le u\} = \{Z \ge \bar\Phi^{-1}(u)\}$, which has probability $u$. For "two-sided", $\{p \le u\} = \{|Z| \ge z_{1-u/2}\}$, which has probability $2(1 - (1 - u/2)) = u$. "less" is the mirror image of "greater". $\square$

So "reject when $p \le \alpha$" is the same as "reject when $z \ge z_{1-\alpha}$" ("greater"), "$z \le z_\alpha$" ("less") or "$|z| \ge z_{1-\alpha/2}$" ("two-sided").

**Lemma 4 (the one-sided test is valid on the composite null).** For $H_0: \mu \le \mu_0$ against $H_1: \mu > \mu_0$, the rule "reject when $Z \ge z_{1-\alpha}$" has size exactly $\alpha$.

*Proof.* By Lemma 1, $P_\mu(Z \ge z_{1-\alpha}) = 1 - \Phi(z_{1-\alpha} - \lambda)$, which increases in $\lambda$ and so in $\mu$. Its supremum over $\mu \le \mu_0$ is its value at $\mu_0$, which is $\alpha$. $\square$

**Lemma 5 (the power function).** The two-sided test at level $\alpha$ rejects with probability $\pi(\mu) = \Phi(\lambda - z_{1-\alpha/2}) + \Phi(-\lambda - z_{1-\alpha/2})$. It is even in $\lambda$, equals $\alpha$ at $\lambda = 0$, and increases in $|\lambda|$, so the test is unbiased.

*Proof.* By Lemma 1, with $c = z_{1-\alpha/2}$, $P(Z \ge c) = \Phi(\lambda - c)$ and $P(Z \le -c) = \Phi(-\lambda - c)$. The sum is even in $\lambda$. Its derivative in $\lambda$ is $\varphi(\lambda - c) - \varphi(\lambda + c)$, where $\varphi$ is the standard normal density. For $\lambda > 0$ and $c > 0$, $|\lambda - c| < \lambda + c$, so $\varphi(\lambda - c) > \varphi(\lambda + c)$ and the derivative is positive. $\square$

**Lemma 6 (the proportion test is asymptotic).** Let $K \sim \text{Binomial}(n, p_0)$ with $0 < p_0 < 1$ fixed, and $Z_n = (K - np_0)/\sqrt{np_0(1 - p_0)}$. Then $Z_n$ converges in distribution to $N(0, 1)$, and the size of each rule of Lemma 3 tends to $\alpha$ as $n \to \infty$.

*Proof.* $K$ is a sum of $n$ iid Bernoulli($p_0$) variables with mean $p_0$ and variance $p_0(1 - p_0) \in (0, \infty)$, so the [central limit theorem](/central-limit-theorem/) gives the convergence in distribution. The limit CDF $\Phi$ is continuous, so $P(Z_n \ge c) \to 1 - \Phi(c)$ for each fixed $c$, and the same for the lower and the two-sided rules. $\square$

The convergence of Lemma 6 is not uniform in $p_0$: for fixed $n$, the size can be far from $\alpha$ when $np_0$ is small. For each finite $n$ the size is a sum of binomial terms, which the tests compute exactly.

**Termination.** Z-TEST makes one pass over the $n$ observations and then a constant number of operations, so it stops after $n + O(1)$ steps.

**Theorem.** Under the model of Lemma 1 (or Lemma 2), Z-TEST returns the statistic $Z$ and the p-value $P_{H_0}(\text{a statistic at least as extreme as } z)$, and rejecting when $p \le \alpha$ gives a test of size exactly $\alpha$, for every $n \ge 1$. The proportion version has size that tends to $\alpha$.

*Proof.* Lemmas 1 to 4 for the normal versions, and Lemma 6 for the proportion version. $\blacksquare$
