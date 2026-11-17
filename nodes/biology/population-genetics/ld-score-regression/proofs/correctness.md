---
title: The expected chi-squared statistic is linear in the LD score, and weighted regression recovers the line
proves: [correctness]
status: full
---

**Setting.** There are $M$ SNPs. Let $R$ be the $M \times M$ matrix of population correlations between the standardized genotypes, and let the LD score of SNP $j$ be $l_j = \sum_k R_{jk}^2$. A GWAS of $N$ people gives the statistics $z_j$ and $\chi^2_j = z_j^2$. We use the model of the summary statistics

$$z = \sqrt N\, R \beta + \varepsilon + \sqrt{N a}\, s, \qquad \beta \sim (0, \tfrac{h^2}{M} I), \quad \varepsilon \sim (0, R), \quad s \sim (0, I),$$

with $\beta$, $\varepsilon$ and $s$ independent, where $(\mu, \Sigma)$ gives the mean and the covariance of a law. Here $\sqrt N R \beta$ is the part of $z$ due to the polygenic effects $\beta$ of the standardized SNPs, $\varepsilon$ is the sampling noise, which has the LD correlation, and $\sqrt{N a}\, s$ is confounding that adds the same variance $N a$ to every SNP. The genetic variance has mean $\mathrm E[\beta^\top R \beta] = \frac{h^2}{M} \operatorname{tr} R = h^2$, since $R_{jj} = 1$.

**Lemma 1 (equation 1 of Bulik-Sullivan and coworkers).** $\mathrm E[\chi^2_j] = N h^2 l_j / M + N a + 1$.

*Proof.* The three terms of $z_j$ have mean $0$ and are independent, so $\mathrm E[z_j^2]$ is the sum of their variances. $\operatorname{Var}(\sqrt N (R\beta)_j) = N \sum_k R_{jk}^2 \operatorname{Var}(\beta_k) = N h^2 l_j / M$. $\operatorname{Var}(\varepsilon_j) = R_{jj} = 1$, and $\operatorname{Var}(\sqrt{N a}\, s_j) = N a$. $\square$

So the points $(l_j, \chi^2_j)$ scatter around a line with slope $N h^2 / M$ and intercept $1 + N a$. Confounding moves the intercept and polygenicity moves the slope. The summary model is an approximation of the individual-level model with $N$ large and each SNP of small effect, where $z_j \approx \sqrt N \hat r_j$ for the sample correlation $\hat r_j$ of the trait and SNP $j$.

**Lemma 2 (the corrected $r^2$, line L2).** Let $\hat r$ be the sample correlation of $n$ independent pairs from a bivariate normal law with correlation $\rho$, and $\tilde r^2 = \hat r^2 - (1 - \hat r^2)/(n - 2) = ((n - 1) \hat r^2 - 1)/(n - 2)$. If $\rho = 0$, $\mathrm E[\tilde r^2] = 0$. For any $\rho$, $\mathrm E[\tilde r^2] = \rho^2 + O(\rho^2 (1 - \rho^2)/n)$.

*Proof.* If $\rho = 0$, $\hat r^2$ follows the beta law with parameters $\frac12$ and $\frac{n-2}{2}$, whose mean is $1/(n - 1)$, and $\mathrm E[\tilde r^2] = ((n-1)/(n-1) - 1)/(n - 2) = 0$. For general $\rho$, the exact mean of $\hat r^2$ under the bivariate normal law is $\mathrm E[\hat r^2] = 1 - \frac{n-2}{n-1} (1 - \rho^2)\, {}_2F_1(1, 1; \tfrac{n+1}{2}; \rho^2)$, and ${}_2F_1(1, 1; \tfrac{n+1}{2}; \rho^2) = 1 + \frac{2 \rho^2}{n + 1} + O(\rho^4 / n^2)$. Substituting, $\mathrm E[\tilde r^2] = 1 - (1 - \rho^2)\,{}_2F_1(\cdot) = \rho^2 - \frac{2\rho^2 (1 - \rho^2)}{n + 1} + O(\rho^4 (1 - \rho^2)/n^2)$. $\square$

The plain $\hat r^2$ has the bias $(1 - \rho^2)/(n - 1)$ at every pair, and a window holds many pairs with $\rho$ near $0$, so without the correction the LD score of every SNP would be too large by about $w/n$ for a window of $w$ SNPs. Line L1 adds $\tilde r^2_{jk}$ for each pair in the window once to $l_j$ and once to $l_k$, and line L2 adds $1$ for $k = j$, where $\tilde r^2 = 1$ exactly. So the code returns $\sum_{k \in \text{window}(j)} \tilde r^2_{jk}$, which estimates $l_j$ when $R_{jk}$ is negligible outside the window.

**Lemma 3 (weighted regression, lines L4 to L6).** Let $w_j > 0$ be weights that depend on the LD scores only, and let $(\hat a, \hat b)$ minimize $\sum_j w_j (\chi^2_j - a - b\, l_j)^2$, with not all $l_j$ equal. Then $\mathrm E[\hat a] = 1 + N a$ and $\mathrm E[\hat b] = N h^2 / M$. If every $\chi^2_j$ is exactly $1 + N a + (N h^2/M) l_j$, then $\hat a$ and $\hat b$ equal these values for any positive weights.

*Proof.* The weighted least squares estimate is $(\hat a, \hat b)^\top = (L^\top W L)^{-1} L^\top W \chi^2$ with the rows $(1, l_j)$ of $L$ and $W = \operatorname{diag}(w)$, a linear function of $\chi^2$ whose matrix is fixed. $L^\top W L$ is invertible because the weighted variance of the $l_j$ is positive. By Lemma 1, $\mathrm E[\chi^2] = L (1 + N a, N h^2/M)^\top$, and $(L^\top W L)^{-1} L^\top W L = I$. The exact case is the same computation without the expectation. Line L6 multiplies $\hat b$ by $M/N$. $\square$

The weights of line L4 are those of the method. $1/\max(l_j, 1)$ lowers the weight of SNPs in high LD, whose statistics are correlated with many others and so count more than once. $1/(a + N h^2 l_j/M)^2$ is proportional to $1/\operatorname{Var}(\chi^2_j)$ when $z_j$ is normal, since then $\operatorname{Var}(z_j^2) = 2\,\mathrm E[z_j^2]^2$, which makes the fit more efficient. In the code they depend on $h^2$ and $a$ of the previous round, so they depend weakly on the data. Lemma 3 then holds only approximately. The estimate stays consistent when the weights converge, since a weighted least squares estimate with any fixed positive weights is consistent for the line of Lemma 1.

**The jackknife, line L7.** The SNPs are split into $B$ blocks of consecutive SNPs. For each block $t$ the code refits the line without the block, with the weights held fixed, and returns $\sqrt{\frac{B-1}{B} \sum_t (\hat\theta_{(t)} - \bar\theta)^2}$ for $\theta = h^2$ and for the intercept. This is the delete-one-group jackknife estimate of the standard error. The statistics are correlated within an LD window, so the blocks must be much longer than a window, and then the blocks are close to independent. The jackknife is used because the dependence between the $\chi^2_j$ through $R$ makes the usual standard error of the regression too small. When all points lie on the line, every refit returns the same line, so both standard errors are $0$, which the tests check.

**What this does not cover.** Lemma 1 is about the summary model. In real data the LD scores come from a reference panel, which differs from the GWAS sample in ancestry and size, and the effect sizes may depend on allele frequency or LD. Then the slope and the intercept are biased in ways that this version does not model.
