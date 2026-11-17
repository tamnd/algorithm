---
title: ComBat computes conditional posterior means under moment-fitted priors, its iteration converges, and without shrinkage it equalizes the batches exactly
proves: [correctness]
status: full
---

We prove what each step of ComBat computes. Without shrinkage, the adjusted data of every gene have the same mean and the same sample variance in every batch (Theorem 2). With shrinkage, line L7 is the posterior mean of the batch shift for a fixed scale (Lemma 3), line L8 is the posterior mean of the scale for a fixed shift (Lemma 4), line L6 fits the inverse gamma prior by the method of moments (Lemma 5), and the iteration of lines L7 to L9 converges to a point where both equations hold (Theorem 6). That the batch effects in real data follow the model, and that removing them keeps the biology, are assumptions; the tests measure them on simulated data. There is no theorem that the empirical Bayes estimates have lower error than the plain estimates for every parameter value, as there is for the James-Stein estimator.

**Setting.** Data $Y_{gj}$ for genes $g = 1, \dots, G$ and samples $j = 1, \dots, N$. Sample $j$ is in batch $b(j)$, batch $i$ has $n_i \ge 2$ samples, and $x_j$ is a row of covariates. Line L1 fits, for each gene, $Y_{gj} \approx c_{g,b(j)} + x_j\beta_g$ by least squares, where $c_{gi}$ is a coefficient for each batch, and sets $\alpha_g = \sum_i n_ic_{gi}/N$. Let $\mu_{gj} = \alpha_g + x_j\beta_g$ and let $r_{gj}$ be the residuals of the fit. Line L2 sets $\sigma_g^2 = \frac1N\sum_j r_{gj}^2$, and line L3 sets $Z_{gj} = (Y_{gj} - \mu_{gj})/\sigma_g$. Line L4 sets $\hat\gamma_{ig}$ and $\hat\delta^2_{ig}$ to the mean and the sample variance (divisor $n_i - 1$) of $Z_{gj}$ over the samples of batch $i$. Line L10 returns
$$Y^\ast_{gj} = \frac{\sigma_g}{\delta^\ast_{ig}}\big(Z_{gj} - \gamma^\ast_{ig}\big) + \mu_{gj}, \qquad i = b(j).$$

**Lemma 1 (the standardized data).** For each gene and batch, $Z_{gj} - \hat\gamma_{ig} = r_{gj}/\sigma_g$ for the samples of batch $i$, and $\hat\gamma_{ig} = (c_{gi} - \alpha_g)/\sigma_g$.

*Proof.* The design has an indicator column for each batch, so the normal equations make the residuals of each batch sum to 0. In batch $i$, $Y_{gj} - \mu_{gj} = (c_{gi} - \alpha_g) + r_{gj}$, so the batch mean of $Z_{gj}$ is $(c_{gi} - \alpha_g)/\sigma_g$, and subtracting it leaves $r_{gj}/\sigma_g$. $\square$

So $\hat\gamma_{ig}$ is the shift of batch $i$ in units of $\sigma_g$, and $\hat\delta^2_{ig}$ is the variance of the residuals of batch $i$ in units of $\sigma_g^2$. The covariates are fitted together with the batches, so a covariate effect is not counted as a batch effect, as long as the covariates are not collinear with the batches.

**Theorem 2 (location and scale without shrinkage).** With $\gamma^\ast = \hat\gamma$ and $\delta^\ast = \hat\delta$, for every gene $g$ and batch $i$, the values $Y^\ast_{gj} - \mu_{gj}$ over the samples of batch $i$ have mean 0 and sample variance $\sigma_g^2$.

*Proof.* $Y^\ast_{gj} - \mu_{gj} = \sigma_g(Z_{gj} - \hat\gamma_{ig})/\hat\delta_{ig}$. Over batch $i$, the mean of $Z_{gj} - \hat\gamma_{ig}$ is 0 and its sample variance is $\hat\delta^2_{ig}$, so the mean is 0 and the sample variance is $\sigma_g^2\hat\delta^2_{ig}/\hat\delta^2_{ig}$. $\square$

**Lemma 3 (line L7).** Let $Z_1, \dots, Z_n$ be independent $N(\gamma, \delta^2)$ given $\gamma$, with $\delta^2$ known, and let $\gamma \sim N(\bar\gamma, \tau^2)$. Then the posterior mean of $\gamma$ is
$$\gamma^\ast = \frac{n\tau^2\hat\gamma + \delta^2\bar\gamma}{n\tau^2 + \delta^2}, \qquad \hat\gamma = \tfrac1n\textstyle\sum_j Z_j.$$

*Proof.* The log of the posterior density is, up to a constant, $-(\gamma - \bar\gamma)^2/2\tau^2 - \sum_j(Z_j - \gamma)^2/2\delta^2$. This is a quadratic in $\gamma$ with leading coefficient $-\frac12(1/\tau^2 + n/\delta^2)$ and linear coefficient $\bar\gamma/\tau^2 + n\hat\gamma/\delta^2$, so the posterior is normal with mean $(\bar\gamma/\tau^2 + n\hat\gamma/\delta^2)/(1/\tau^2 + n/\delta^2)$. Multiply the numerator and the denominator by $\tau^2\delta^2$. $\square$

The estimate moves $\hat\gamma$ toward $\bar\gamma$ by the factor $\delta^2/(n\tau^2 + \delta^2)$, which is large when the batch is small or noisy and small when the genes disagree a lot about the shift ($\tau^2$ large).

**Lemma 4 (line L8).** Let $Z_1, \dots, Z_n$ be independent $N(\gamma, \delta^2)$ given $\delta^2$, with $\gamma$ known, and let $\delta^2$ have the inverse gamma density proportional to $(\delta^2)^{-\lambda - 1}e^{-\theta/\delta^2}$. Then the posterior is inverse gamma with shape $\lambda + n/2$ and scale $\theta + \frac12\sum_j(Z_j - \gamma)^2$, and its mean is
$$\delta^{\ast2} = \frac{\theta + \frac12\sum_j(Z_j - \gamma)^2}{n/2 + \lambda - 1}.$$

*Proof.* The likelihood is proportional to $(\delta^2)^{-n/2}e^{-\sum_j(Z_j - \gamma)^2/2\delta^2}$. Multiplying by the prior gives the stated shape and scale. An inverse gamma with shape $a > 1$ and scale $b$ has mean $b/(a - 1)$. Here $a = \lambda + n/2 > 1$ because $\lambda > 2$ by Lemma 5. $\square$

**Lemma 5 (line L6).** Let $D$ and $S^2 > 0$ be the mean and the sample variance of the values $\hat\delta^2_{ig}$ over the genes. Then $\lambda = (D^2 + 2S^2)/S^2$ and $\theta = (D^3 + DS^2)/S^2$ are the only parameters with $\lambda > 2$ for which the inverse gamma has mean $D$ and variance $S^2$, and $\lambda > 2$, $\theta > 0$.

*Proof.* For $\lambda > 2$ the inverse gamma has mean $\theta/(\lambda - 1)$ and variance $\theta^2/((\lambda - 1)^2(\lambda - 2))$. Setting the mean to $D$ gives $\theta = D(\lambda - 1)$, and then the variance is $D^2/(\lambda - 2) = S^2$, so $\lambda = 2 + D^2/S^2$ and $\theta = D(1 + D^2/S^2)$, which are the formulas. $D > 0$ and $S^2 > 0$ give $\lambda > 2$ and $\theta > 0$. $\square$

In the same way line L5 sets the normal prior to the mean and the sample variance of the $\hat\gamma_{ig}$ over the genes. These are method of moments fits, so the prior is estimated from all genes at once, which is what makes the method empirical Bayes.

**Theorem 6 (the iteration).** For one gene and batch, let $d_0 = \hat\delta^2$, and for $t \ge 0$ let $g_{t+1} = c(d_t)$ and $d_{t+1} = h(d_t)$, where $c(x) = (n\tau^2\hat\gamma + x\bar\gamma)/(n\tau^2 + x)$ and $h(x) = (\theta + \frac12\sum_j(Z_j - c(x))^2)/(n/2 + \lambda - 1)$. This is lines L7 and L8. The sequence $d_t$ is monotone and converges to a limit $d^\ast > 0$ with $h(d^\ast) = d^\ast$, and $g_t$ converges to $c(d^\ast)$. Every $g_t$ lies between $\hat\gamma$ and $\bar\gamma$.

*Proof.* For $x > 0$, $\hat\gamma - c(x) = x(\hat\gamma - \bar\gamma)/(n\tau^2 + x)$, so $c(x)$ lies between $\hat\gamma$ and $\bar\gamma$, and $|\hat\gamma - c(x)|$ does not decrease as $x$ grows and is at most $|\hat\gamma - \bar\gamma|$. Since $\hat\gamma$ is the mean of the $Z_j$, $\sum_j(Z_j - c)^2 = \sum_j(Z_j - \hat\gamma)^2 + n(\hat\gamma - c)^2$. So $h$ is continuous and non-decreasing on $(0, \infty)$, and its values lie in a bounded interval $[h_0, h_1]$ with $h_0 \ge \theta/(n/2 + \lambda - 1) > 0$. If $d_1 \ge d_0$, then $d_2 = h(d_1) \ge h(d_0) = d_1$, and by induction the sequence does not decrease; if $d_1 \le d_0$ it does not increase. A monotone bounded sequence converges, and its limit $d^\ast \ge h_0 > 0$. By continuity, $d^\ast = \lim h(d_t) = h(d^\ast)$, and $g_t = c(d_{t-1}) \to c(d^\ast)$. $\square$

The code stops when the relative change of both values is below $10^{-4}$, as the sva package does, which happens after finitely many steps because both sequences converge. The fixed point is the pair of the two conditional posterior means of Lemmas 3 and 4. It is in general not the mean of the joint posterior of $(\gamma, \delta^2)$; it is the estimate that Johnson, Li and Rabinovic define. The proof does not show that $h$ has only one fixed point.

**What the lines compute.** Lines L1 to L3 are Lemma 1, line L4 the batch estimates, lines L5 and L6 the priors of Lemma 5, lines L7 to L9 Theorem 6, and line L10 the adjustment, which is Theorem 2 when the shrinkage is off. A gene with $Y_{gj} + a$ in place of $Y_{gj}$ gets $\mu_{gj} + a$ and the same $Z$, so its output moves by $a$. If all data are multiplied by $s > 0$, then $Z$ and the priors do not change and the output is multiplied by $s$.

**Complexity.** With $p$ columns in the design, the least squares fit of one gene takes $O(Np^2 + p^3)$ time, so lines L1 to L3 take $O(G(Np^2 + p^3))$. Lines L4 to L6 take $O(GN)$. Each step of the iteration takes $O(n_i)$ time for one gene and batch, so $T$ steps take $O(GNT)$ in all. The number of steps $T$ is finite by Theorem 6 but has no proved bound. The space is $O(GN)$.

**What the tests check.** The test file checks the page example. It checks Theorem 2 with and without a covariate, Lemma 5 against the inverse gamma moments, Theorem 6 (the fixed point equations, the monotone sequence and the position of $\gamma^\ast$) on random inputs, and Lemma 3 against numerical integration. It checks the shift and scale rules above. Two simulations are measurements, not theorems: with batches of 3 samples the empirical Bayes output is closer to the batch free data than the location and scale output; and with a biological group that is unbalanced across batches, leaving out the covariate removes much of the group difference.
