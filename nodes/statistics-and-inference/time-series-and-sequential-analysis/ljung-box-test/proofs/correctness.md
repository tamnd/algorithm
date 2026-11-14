---
title: For an IID series the Ljung-Box and Box-Pierce statistics tend to chi-square with h degrees of freedom, and the Ljung-Box weights make the mean exactly h for normal noise
proves: [correctness]
status: full
---

**Setting.** $e_1, \ldots, e_n$ is a series and $1 \le h < n$. Write $\bar e = \frac1n\sum_t e_t$, $c_0 = \sum_{t=1}^n (e_t - \bar e)^2$, $c_k = \sum_{t=k+1}^{n}(e_t - \bar e)(e_{t-k} - \bar e)$, $\hat r_k = c_k/c_0$, and

$$Q_{\mathrm{LB}} = n(n + 2)\sum_{k=1}^{h}\frac{\hat r_k^2}{n - k}, \qquad Q_{\mathrm{BP}} = n\sum_{k=1}^{h}\hat r_k^2 .$$

**Claim 1 (lines L1 to L6 compute the statistic).** Line L1 computes $\bar e$, line L2 computes $c_0$ and line L3 computes $\hat r_1, \ldots, \hat r_h$. Line L4 computes $Q_{\mathrm{LB}}$ (or $Q_{\mathrm{BP}}$), line L5 sets $\mathrm{df} = h - s$, and line L6 returns $P(\chi^2_{\mathrm{df}} > Q)$ from the regularized upper incomplete gamma function of the helper module.

*Proof.* Each line is the formula above. The sums use `math.fsum`, so the only rounding is in the individual terms. The code rejects a constant series, for which $c_0 = 0$, and $h \ge n$, for which some $n - k \le 0$. $\square$

**Claim 2 (exact moments for normal noise with known mean).** Let $e_1, \ldots, e_n$ be IID $N(0, \sigma^2)$ and define $r_k = \sum_{t=k+1}^n e_t e_{t-k} / \sum_{t=1}^n e_t^2$, the autocorrelation without centering. Then $\mathbb{E}[r_k] = 0$, $\mathrm{Var}(r_k) = (n - k)/(n(n + 2))$, and $\mathrm{Cov}(r_j, r_k) = 0$ for $j \ne k$. Hence, with $r_k$ in place of $\hat r_k$,

$$\mathbb{E}[Q_{\mathrm{LB}}] = h, \qquad \mathbb{E}[Q_{\mathrm{BP}}] = \sum_{k=1}^{h}\frac{n - k}{n + 2} = \frac{h(2n - h - 1)}{2(n + 2)} < h.$$

*Proof.* The vector $e$ has a spherically symmetric law, so $U = e/\lVert e \rVert$ is uniform on the unit sphere of $\mathbb{R}^n$, and $r_k = \sum_{t=k+1}^n U_t U_{t-k}$. The law of $U$ does not change when one coordinate changes sign, so a moment $\mathbb{E}[U_a U_b U_c U_d]$ is 0 unless every index appears an even number of times. For the uniform law on the sphere, $\mathbb{E}[U_a^2 U_b^2] = 1/(n(n + 2))$ for $a \ne b$. (Proof: by symmetry $\mathbb{E}[U_a^4] = A$ and $\mathbb{E}[U_a^2U_b^2] = B$ do not depend on $a \ne b$. From $\lVert U \rVert = 1$, $nA + n(n - 1)B = 1$. For a standard normal vector $Z$, $Z = \lVert Z \rVert U$ with $\lVert Z \rVert$ independent of $U$ and $\mathbb{E}\lVert Z \rVert^4 = n(n + 2)$, so $3 = \mathbb{E}Z_a^4 = n(n + 2)A$ and $1 = \mathbb{E}Z_a^2 Z_b^2 = n(n + 2)B$.) Each term $U_t U_{t-k}$ has two different indices, so $\mathbb{E}[r_k] = 0$. In

$$\mathbb{E}[r_j r_k] = \sum_{t=k+1}^{n}\sum_{s=j+1}^{n}\mathbb{E}[U_t U_{t-k} U_s U_{s-j}],$$

a term is nonzero only if $\{t, t-k\} = \{s, s-j\}$ as sets. The case $t = s - j$, $t - k = s$ gives $j + k = 0$, which is impossible. The case $t = s$, $t - k = s - j$ needs $j = k$. So the covariance is 0 for $j \ne k$, and for $j = k$ the $n - k$ terms with $s = t$ each give $1/(n(n + 2))$. Then $\mathbb{E}[Q_{\mathrm{LB}}] = n(n + 2)\sum_k \frac{n - k}{n(n + 2)(n - k)} = h$, and $\mathbb{E}[Q_{\mathrm{BP}}] = n\sum_k \frac{n - k}{n(n + 2)}$. $\square$

This is the reason for the weights $(n + 2)/(n - k)$. The code centres the series at $\bar e$, which changes the moments by terms of order $1/n$, so for the centred statistic the claim is an approximation. For $n = 30$ and $h = 10$, $\mathbb{E}[Q_{\mathrm{BP}}] = 245/32 = 7.66$, far below the mean 10 of $\chi^2_{10}$.

**Claim 3 (joint limit of the autocorrelations).** Let $e_1, e_2, \ldots$ be IID with mean $\mu$ and variance $\sigma^2 \in (0, \infty)$, and fix $h$. Then $\sqrt{n}(\hat r_1, \ldots, \hat r_h) \to N(0, I_h)$ in distribution.

*Proof.* Put $d_t = e_t - \mu$. Fix $\lambda \in \mathbb{R}^h$ and let $Y_t = d_t \sum_{k=1}^h \lambda_k d_{t-k}$ for $t > h$. The sequence $(Y_t)$ is strictly stationary and $h$-dependent, because $Y_t$ is a function of $d_{t-h}, \ldots, d_t$. Its mean is 0, since $d_t$ is independent of the other factors. Its variance is $\mathbb{E}[d_t^2]\,\mathbb{E}[(\sum_k \lambda_k d_{t-k})^2] = \sigma^4\lVert\lambda\rVert^2$. For $j \ge 1$, $\mathbb{E}[Y_t Y_{t+j}] = 0$, because $d_{t+j}$ appears once in the product and is independent of all the other factors, whose indices are smaller. The central limit theorem for strictly stationary $m$-dependent sequences with finite variance (Brockwell and Davis 1991, Chapter 6) gives $n^{-1/2}\sum_{t=h+1}^{n} Y_t \to N(0, \sigma^4\lVert\lambda\rVert^2)$. The terms with $t \le h$ in $\sum_t d_t d_{t-k}$ are a fixed number of $O_p(1)$ terms, so by the Cramér-Wold device

$$n^{-1/2}\Big(\sum_{t=k+1}^n d_t d_{t-k}\Big)_{k=1}^{h} \to N(0, \sigma^4 I_h).$$

Next, the centering. With $\delta = \bar e - \mu$,
$$c_k = \sum_{t=k+1}^n d_t d_{t-k} - \delta\Big(\sum_{t=k+1}^n d_t + \sum_{t=1}^{n-k} d_t\Big) + (n - k)\delta^2 .$$
By Chebyshev's inequality, $\delta = O_p(n^{-1/2})$ and the two partial sums are $O_p(n^{1/2})$, so the last two terms are $O_p(1)$ and vanish after division by $\sqrt{n}$. Finally $c_0/n = \frac1n\sum_t d_t^2 - \delta^2 \to \sigma^2$ almost surely by the strong law of large numbers. By Slutsky's lemma, $\sqrt{n}\,\hat r_k = (n^{-1/2}c_k)/(c_0/n)$ has the joint limit $N(0, \sigma^4 I_h)/\sigma^2 = N(0, I_h)$. $\square$

**Claim 4 (the size tends to $\alpha$ for a raw series).** Under the hypotheses of Claim 3, $Q_{\mathrm{BP}} \to \chi^2_h$ and $Q_{\mathrm{LB}} \to \chi^2_h$ in distribution. So with $s = 0$, the test that rejects when $Q \ge \chi^2_{(h,\,1-\alpha)}$ has size tending to $\alpha$, for either statistic.

*Proof.* $Q_{\mathrm{BP}} = \lVert \sqrt{n}\,\hat r \rVert^2$ is a continuous function of $\sqrt{n}\,\hat r$, so by Claim 3 and the continuous mapping theorem it tends to the squared length of an $N(0, I_h)$ vector, which is $\chi^2_h$. Next,
$$Q_{\mathrm{LB}} - Q_{\mathrm{BP}} = \sum_{k=1}^h n\hat r_k^2\Big(\frac{n + 2}{n - k} - 1\Big) = \sum_{k=1}^h n\hat r_k^2\,\frac{k + 2}{n - k},$$
where $n\hat r_k^2 = O_p(1)$ and $(k + 2)/(n - k) \to 0$. So the difference tends to 0 in probability, and $Q_{\mathrm{LB}}$ has the same limit. The $\chi^2_h$ law is continuous, so $P(Q \ge \chi^2_{(h,\,1-\alpha)}) \to \alpha$. $\square$

The tests check Claim 1 against an exact `Fraction` computation of $Q_{\mathrm{LB}}$ and $Q_{\mathrm{BP}}$ on random integer series and on the worked example, the helper `chi2_sf` against the closed forms for 1 and 2 degrees of freedom, and Claim 4 by Monte Carlo sizes for IID normal series.

**Cited, not proved here.** For the residuals of an ARMA($p$, $q$) model fitted by an efficient method, $\sqrt{n}(\hat r_1, \ldots, \hat r_h)$ tends to a normal law with covariance $I_h - J$, where $J$ is a projection of rank $p + q$ when $h$ is large. Hence $Q$ is approximately $\chi^2_{h - p - q}$ (Box and Pierce 1970; Brockwell and Davis 1991, Section 9.4). For fixed $h$ the limit is a weighted sum of chi-square variables, not exactly $\chi^2_{h - p - q}$. The page measures the size of this approximation for AR(1) residuals.
