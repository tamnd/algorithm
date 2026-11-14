---
title: Tukey's test has family-wise error rate exactly alpha for balanced normal data
proves: [correctness, termination]
status: full
---

We prove that for balanced normal data the largest standardized pairwise difference of the group means, centred at the true means, has the studentized range law, so the Tukey intervals cover all pairwise differences at once with probability exactly $1 - \alpha$ and the tests control the family-wise error rate at $\alpha$ in the strong sense. We derive the integral that the helper evaluates, and the exact check for two groups. The model is $y_{ij} = \mu_i + e_{ij}$, $i = 1, \dots, k$, $j = 1, \dots, n_i$, with iid $N(0, \sigma^2)$ errors, $N = \sum n_i$, $\nu = N - k$, and $MSE = SSW/\nu$.

**Definition.** Let $Z_1, \dots, Z_k$ be iid $N(0, 1)$ and $V \sim \chi^2_\nu$ independent of them. The range is $R = \max_i Z_i - \min_i Z_i$, and the studentized range is $Q_{k,\nu} = R/\sqrt{V/\nu}$. For $\nu = \infty$, $Q_{k,\infty} = R$. $q_{(k, \nu, 1-\alpha)}$ is its upper $\alpha$ point.

**Lemma 1 (the law of the range).** For $w > 0$,

$$P(R \le w) = k\int_{-\infty}^{\infty}\varphi(z)\big(\Phi(z + w) - \Phi(z)\big)^{k-1}dz,$$

and, with $A(z) = 1 - \Phi(z)$,

$$P(R > w) = k\int_{-\infty}^{\infty}\varphi(z)\Big(A(z)^{k-1} - \big(A(z) - A(z + w)\big)^{k-1}\Big)dz .$$

*Proof.* With probability 1 the $Z_i$ are distinct, so exactly one index attains the minimum. $R \le w$ happens exactly when, for the index $i$ of the minimum, every other $Z_j$ lies in $(Z_i, Z_i + w]$. These $k$ events are disjoint. Conditioning on $Z_i = z$, the other $k - 1$ variables are independent with $P(z < Z_j \le z + w) = \Phi(z + w) - \Phi(z)$, which gives the first formula after integrating against $\varphi(z)$ and adding the $k$ equal terms. The same argument with $w = \infty$ gives $1 = k\int\varphi(z)A(z)^{k-1}dz$ (some index is the minimum). Subtract the first formula from this and use $\Phi(z + w) - \Phi(z) = A(z) - A(z + w)$. $\square$

The helper evaluates the bracket as $-A^{k-1}\,\mathrm{expm1}\big((k - 1)\log(1 - r)\big)$ with $r = A(z + w)/A(z)$, which is the same number written without the cancellation of two nearly equal powers in the tails.

**Lemma 2 (the law of $Q$).** $P(Q_{k,\nu} > q) = \int_0^\infty g_\nu(s)P(R > qs)ds$, where $g_\nu$ is the density of $S = \sqrt{V/\nu}$: $g_\nu(s) = \frac{\nu^{\nu/2}}{\Gamma(\nu/2)2^{\nu/2-1}}s^{\nu-1}e^{-\nu s^2/2}$.

*Proof.* $R$ and $S$ are independent, so $P(R/S > q) = E[P(R > qS \mid S)] = \int g_\nu(s)P(R > qs)ds$. The density of $S$ follows from the $\chi^2_\nu$ density of $V = \nu S^2$ by the change of variables $v = \nu s^2$, $dv = 2\nu s\,ds$. $\square$

**Lemma 3 (the pivot).** Let all $n_i = n$. Then

$$\max_{i < j}\frac{\big|(\bar y_i - \bar y_j) - (\mu_i - \mu_j)\big|}{\sqrt{MSE/n}} \sim Q_{k, \nu}.$$

*Proof.* Let $Z_i = \sqrt n(\bar y_i - \mu_i)/\sigma$. The $Z_i$ are iid $N(0, 1)$, because the groups are independent and each $\bar y_i - \mu_i$ is the mean of $n$ iid $N(0, \sigma^2)$ errors. $V = SSW/\sigma^2 \sim \chi^2_\nu$ is independent of the vector of group means by Lemma 3 of the [one-way ANOVA](/one-way-anova/) proof (the within-group residuals and the group means are projections onto orthogonal subspaces). Then $\big((\bar y_i - \bar y_j) - (\mu_i - \mu_j)\big)/\sqrt{MSE/n} = (Z_i - Z_j)/\sqrt{V/\nu}$. The largest $|Z_i - Z_j|$ over pairs is $\max Z - \min Z = R$. $\square$

**Lemma 4 (exact simultaneous coverage).** With equal sizes the code's interval for $\mu_i - \mu_j$ is $\bar y_i - \bar y_j \pm q_{(k,\nu,1-\alpha)}\sqrt{MSE/n}$, and

$$P\big(\text{every interval covers its } \mu_i - \mu_j\big) = 1 - \alpha$$

for every $\mu$ and $\sigma$.

*Proof.* The code's standard error is $\sqrt{\frac{MSE}2(\frac1{n_i} + \frac1{n_j})}$, which is $\sqrt{MSE/n}$ when $n_i = n_j = n$. All intervals cover if and only if the maximum in Lemma 3 is at most $q_{(k,\nu,1-\alpha)}$. The law of $Q$ is continuous, so this has probability exactly $1 - \alpha$. $\square$

**Lemma 5 (strong FWER control).** With equal sizes, reject $H_{ij}: \mu_i = \mu_j$ when $q_{ij} = |\bar y_i - \bar y_j|/\sqrt{MSE/n} > q_{(k,\nu,1-\alpha)}$, which is the same as $p_{ij} = P(Q > q_{ij}) < \alpha$. For every configuration of the means, the probability of rejecting at least one true $H_{ij}$ is at most $\alpha$, and it equals $\alpha$ when all $k$ means are equal.

*Proof.* If $H_{ij}$ is true and rejected, then $|(\bar y_i - \bar y_j) - (\mu_i - \mu_j)| = |\bar y_i - \bar y_j| > q\sqrt{MSE/n}$, so the interval for $\mu_i - \mu_j$ misses. By Lemma 4 the probability that some interval misses is $\alpha$. When all means are equal, every $H_{ij}$ is true, and some $H_{ij}$ is rejected exactly when the maximum in Lemma 3 exceeds $q$, which has probability $\alpha$. The p-value form is the same event because $P(Q > \cdot)$ is strictly decreasing. $\square$

This is the [family-wise error rate](/family-wise-error-rate/) in the strong sense, under the normal model with equal variances and equal group sizes, with no other assumption on the dependence of the tests.

**Lemma 6 (two groups).** For $k = 2$, $Q_{2,\nu} = \sqrt2|T|$ with $T \sim t_\nu$, and the code's statistic is $q_{12} = \sqrt2|t|$, where $t$ is the pooled two-sample t statistic. So $P(Q_{2,\nu} > q) = P(|T_\nu| > q/\sqrt2)$.

*Proof.* $R = |Z_1 - Z_2|$ and $Z_1 - Z_2 \sim N(0, 2)$, so $R = \sqrt2|Z|$ with $Z \sim N(0,1)$, and $Q = \sqrt2|Z|/\sqrt{V/\nu} = \sqrt2|T|$. For the statistic: the pooled t uses $S_p^2 = MSE$ and the standard error $\sqrt{MSE(1/n_1 + 1/n_2)}$, while the code divides by $\sqrt{\frac{MSE}2(1/n_1 + 1/n_2)}$, which is smaller by the factor $\sqrt2$. This holds for unequal sizes as well. $\square$

This gives an exact check of the numerical integration, which the tests run for several $\nu$.

**What is measured, not proved.** The helper computes Lemma 2 by composite Gauss-Legendre rules: 17 panels of 10 nodes on $[-8.5, 8.5]$ for the inner integral and 40 panels of 10 nodes for the outer one, over the range of $s$ that holds all but $10^{-30}$ of the chi-square mass. Its error is measured, not bounded: it matches Lemma 6 to $10^{-14}$ for $\nu \le 30$ and to $10^{-12}$ for $\nu$ up to 1000, it reproduces published table values of $q_{(k,\nu,0.95)}$ to the printed digits, and it agrees with Monte Carlo within the sampling error. With unequal sizes, the Tukey-Kramer intervals have coverage at least $1 - \alpha$; this is Hayter's theorem (1984), which we cite and do not prove.

**Termination.** L1 makes two passes over the data. L2 inverts the tail by Illinois false position with at most 100 steps after a doubling search for an upper bracket, which stops because $P(Q > q) \to 0$ as $q$ grows. Each tail evaluation is a fixed number of quadrature nodes, $40 \cdot 10$ outer times $17 \cdot 10$ inner. The pair loop runs $k(k-1)/2$ times with one tail evaluation each.

**Theorem.** Under the normal model with equal variances and equal group sizes, the intervals returned by the code have simultaneous coverage exactly $1 - \alpha$, the pairwise tests control the family-wise error rate at exactly $\alpha$ under the complete null and at most $\alpha$ under every other configuration, and with two groups the test is the two-sided pooled t-test. The accuracy of the numerical studentized range is measured as stated above.

*Proof.* Lemmas 1 to 6. $\blacksquare$
