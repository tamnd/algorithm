---
title: The fixed versus random t-test has the stated false alarm rate for large groups and detects every difference of means
proves: [correctness]
status: full
---

Fix one sample $j$ and one set of traces. The fixed group $x_1, \ldots, x_n$ is independent and identically distributed with mean $\mu_x$ and variance $\sigma_x^2 \in (0, \infty)$; the random group $y_1, \ldots, y_n$ is independent of it and identically distributed with mean $\mu_y$ and variance $\sigma_y^2 \in (0, \infty)$. Line L3 computes $t_n = (\bar x - \bar y) / \sqrt{(s_x^2 + s_y^2)/n}$, where $\bar x$ and $s_x^2$ are the sample mean and the unbiased sample variance, and the same for $y$. The code computes exactly these sums, so we study $t_n$.

**Lemma 1.** $s_x^2 \to \sigma_x^2$ and $s_y^2 \to \sigma_y^2$ with probability 1.

*Proof.* $s_x^2 = \frac{n}{n-1}\big(\frac1n \sum_i x_i^2 - \bar x^2\big)$. By the strong [law of large numbers](/law-of-large-numbers/), $\frac1n\sum_i x_i^2 \to \sigma_x^2 + \mu_x^2$ and $\bar x \to \mu_x$, and $\frac{n}{n-1} \to 1$. $\square$

**Theorem 1 (false alarms).** If $\mu_x = \mu_y$, then $t_n$ converges in distribution to the standard normal law, so for every $C > 0$,

$$\lim_{n \to \infty} \Pr[|t_n| > C] = 2(1 - \Phi(C)),$$

which is about $6.8 \times 10^{-6}$ for $C = 4.5$. If the two sets of line L1 are independent, the probability that line L4 flags the sample tends to $(2(1 - \Phi(C)))^2$, about $4.6 \times 10^{-11}$.

*Proof.* The differences $x_i - y_i$ are independent with mean 0 and variance $\sigma_x^2 + \sigma_y^2$, so by the central limit theorem $\sqrt{n}(\bar x - \bar y)/\sqrt{\sigma_x^2 + \sigma_y^2}$ converges in distribution to $\mathcal{N}(0, 1)$. By Lemma 1, $\sqrt{(\sigma_x^2 + \sigma_y^2)/(s_x^2 + s_y^2)} \to 1$ with probability 1. By Slutsky's lemma the product, which is $t_n$, converges to $\mathcal{N}(0, 1)$ in distribution. The normal law has no atom at $\pm C$, so the probabilities converge. The values of the two sets are independent, so the probability that both exceed $C$ is the product. $\square$

**Theorem 2 (detection).** If $\mu_x \ne \mu_y$, then $\Pr[|t_n| > C] \to 1$ for every $C$, and so the flag of line L4 has probability tending to 1.

*Proof.* $t_n = \sqrt{n} (\bar x - \bar y)/\sqrt{s_x^2 + s_y^2}$. The ratio $(\bar x - \bar y)/\sqrt{s_x^2 + s_y^2}$ converges with probability 1 to $(\mu_x - \mu_y)/\sqrt{\sigma_x^2 + \sigma_y^2} \ne 0$, so $|t_n| \to \infty$ with probability 1. $\square$

So the test with large groups has the claimed rate of false alarms at each sample that does not leak at first order, and it finds every sample whose mean depends on the input class. The rate is a limit, not a bound for finite $n$; for finite $n$ and Gaussian data, the law of $t_n$ is close to a Student $t$ law with heavier tails.

**Proposition 3 (first-order masking).** In the masked model, $\ell[0] = \mathrm{HW}(x \oplus m) + N_0$ and $\ell[1] = \mathrm{HW}(m) + N_1$ with $x = S(p \oplus k)$, a uniform 4-bit mask $m$ independent of $p$, and independent centred noise. Then the mean of each sample is 2 for every input $p$, so by Theorem 1 the first-order test has the false alarm rate of a device with no leak. The centred product has mean $1 - \mathrm{HW}(x)/2$ given $x$.

*Proof.* For a fixed $x$, the map $m \mapsto x \oplus m$ is a bijection of $\{0, \ldots, 15\}$, so $x \oplus m$ is uniform, and $\mathrm{E}[\mathrm{HW}(x \oplus m)] = 4 \cdot \frac12 = 2$. Also $\mathrm{E}[\mathrm{HW}(m)] = 2$. Write $\mathrm{HW}(v) - 2 = \sum_{q=0}^{3} (v_q - \tfrac12)$ for the bits $v_q$ of $v$, and $u_q = m_q - \tfrac12$, so that $(x \oplus m)_q - \tfrac12 = (1 - 2x_q) u_q$, because a bit of $x$ equal to 1 flips the bit of $m$. Then

$$\mathrm{E}\Big[\sum_q (1 - 2x_q) u_q \cdot \sum_r u_r\Big] = \sum_q (1 - 2x_q)\,\mathrm{E}[u_q^2] = \tfrac14 \sum_q (1 - 2x_q) = 1 - \tfrac{\mathrm{HW}(x)}{2},$$

because the $u_q$ are independent with mean 0 and $\mathrm{E}[u_q^2] = \tfrac14$. The noise terms are independent of everything and centred, so they add nothing to the mean of the product. $\blacksquare$

With the population means in place of the group means, the second-order test is the first-order test of Theorems 1 and 2 applied to the product. For the fixed value $x = \texttt{F}$ the mean is $-1$, and over a uniform $x$ it is 0, because the mean of $\mathrm{HW}(x)$ is 2. So by Theorem 2 the second-order test detects the masked device when $n$ grows. The code centres with the means of each group; those converge to the population means with probability 1, and the difference changes the product by terms that tend to 0, so the limits are the same.
