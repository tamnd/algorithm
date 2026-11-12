---
title: X-means stops, never exceeds k_max, and its score is the BIC of the hard clustering
proves: [correctness]
status: full
---

**Lemma 1 (the log-likelihood).** Let $R$ points in $\mathbb{R}^d$ be split into $K$ clusters with sizes $R_j \ge 1$ and means $c_j$, let $\mathrm{SSE} = \sum_i \|x_i - c_{a_i}\|^2$, and let $\sigma^2 > 0$. Then
$$\sum_{i} \log\Big(\frac{R_{a_i}}{R}\,\mathcal{N}(x_i \mid c_{a_i}, \sigma^2 I)\Big) = \sum_j R_j\log\frac{R_j}{R} - \frac{Rd}{2}\log(2\pi\sigma^2) - \frac{\mathrm{SSE}}{2\sigma^2} .$$

*Proof.* The density of $\mathcal{N}(c, \sigma^2 I)$ in $\mathbb{R}^d$ is $(2\pi\sigma^2)^{-d/2}\exp(-\|x - c\|^2/(2\sigma^2))$. Take the logarithm and sum over the points. The term $\log(R_{a_i}/R)$ appears $R_j$ times for each cluster $j$. $\square$

So the function `bic` computes $\ell - \frac{p}{2}\log R$ with $\ell$ the log-likelihood of the hard clustering under the spherical model with the variance $\hat\sigma^2 = \mathrm{SSE}/(d(R - K))$.

**Lemma 2 (the variance is the unbiased estimate).** Under the model, $\mathbb{E}[\mathrm{SSE}] = d(R - K)\sigma^2$ when the clusters are fixed, so $\hat\sigma^2$ is unbiased.

*Proof.* For one cluster of $R_j$ points from $\mathcal{N}(\mu, \sigma^2 I)$, each of the $d$ coordinates gives a sum of squared deviations from the sample mean with expectation $(R_j - 1)\sigma^2$. Summing over the $d$ coordinates and the $K$ clusters gives $d\sum_j (R_j - 1)\sigma^2 = d(R - K)\sigma^2$. $\square$

**Theorem.** X-means stops after at most $k_{\max} - k_{\min} + 1$ passes of lines L1 to L9. Each model it considers has at most $k_{\max}$ centers, and it returns the model with the highest BIC on all points among the models of line L2.

*Proof.* Let $K$ be the number of centers at line L1. If $K \ge k_{\max}$, line L3 returns. Otherwise, if no cluster is marked, line L8 returns. Otherwise line L9 replaces $s \ge 1$ marked centers by two children each, with $s \le k_{\max} - K$ by the cap, so the new number of centers $K + s$ satisfies $K < K + s \le k_{\max}$. So $K$ grows strictly and never exceeds $k_{\max}$, and since it starts at $k_{\min}$, there are at most $k_{\max} - k_{\min} + 1$ passes. Each pass runs Lloyd's algorithm, which stops by the correctness of [k-means](/k-means/), and finitely many 2-means runs, which stop for the same reason. Line L2 keeps the model with the highest score so far, and every return happens after line L2. $\square$

**Remark (what is not claimed).** The BIC is an asymptotic approximation to the log marginal likelihood. The theorem says nothing about whether the chosen number of clusters is the true one.
