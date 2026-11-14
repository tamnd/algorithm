---
title: The Breusch-Pagan statistic is half the explained sum of squares of the auxiliary regression, equals the score test, is a rescaled Koenker statistic, and has a null law free of b and sigma under normal errors
proves: [correctness, termination]
status: full
---

The arithmetic is exact. $X$ is a fixed real $n \times p$ matrix of rank $p < n$, $e = (I - H)y$ are the least squares residuals with $H = X(X^\top X)^{-1}X^\top$, $\hat\sigma^2 = \frac1n\sum_ie_i^2 > 0$, $g_i = e_i^2/\hat\sigma^2$, and $Z$ is the $n \times (q + 1)$ matrix with rows $(1, z_i^\top)$ and rank $q + 1 < n$. Let $P_Z$ be the projection onto the columns of $Z$,

$$\mathrm{ESS} = \lVert P_Zg - \bar g\mathbf 1\rVert^2, \quad \mathrm{TSS} = \lVert g - \bar g\mathbf 1\rVert^2, \quad \mathrm{LM}_{\mathrm{BP}} = \tfrac12\mathrm{ESS}, \quad \mathrm{LM}_{\mathrm K} = n\,\mathrm{ESS}/\mathrm{TSS} = nR^2.$$

**Lemma 1 (lines L2 to L6).** $\bar g = 1$ exactly. If $Q_Z^\top Z = \binom{R_Z}{0}$ is the Householder factorization of line L3 and $d = Q_Z^\top g$, then $\mathrm{ESS} = d_1^2 + \dots + d_q^2$ (counting the entries of $d$ from 0), and $\mathrm{TSS} = \sum_i(g_i - 1)^2$. So lines L5 and L6 return $\mathrm{LM}_{\mathrm{BP}}$ and $\mathrm{LM}_{\mathrm K}$.

*Proof.* $\sum_ig_i = \sum_ie_i^2/\hat\sigma^2 = n$. For the second claim, the residual sum of squares of $g$ on all of $Z$ is $\sum_{j > q}d_j^2$, and on its first column (the constant) it is $\sum_{j \ge 1}d_j^2$, because the first $j$ columns of $Q_Z$ span the first $j$ columns of $Z$; this is the argument of the proof on the [F-test for nested linear models](/regression-f-test/) page. The difference is $d_1^2 + \dots + d_q^2$, and it equals $\mathrm{ESS}$, since the regression on the constant alone fits $\bar g\mathbf 1$ and $P_Zg - \bar g\mathbf 1$ is orthogonal to $g - P_Zg$. $\square$

**Lemma 2 (the score test).** Let $y_i \sim N(x_i^\top b, \sigma_i^2)$ independently with $\sigma_i^2 = h(\alpha_0 + z_i^\top\alpha)$, where $h$ is any positive differentiable function with $h'(\alpha_0) \ne 0$ at the null value. The [score test](/score-test/) statistic of $H_0: \alpha = 0$, with the expected information, is $\mathrm{LM}_{\mathrm{BP}}$, for every such $h$.

*Proof.* The log-likelihood is $\ell = -\frac12\sum_i\bigl[\log\sigma_i^2 + (y_i - x_i^\top b)^2/\sigma_i^2\bigr]$ up to a constant. Under $H_0$ the maximum likelihood estimates are $\hat b$ of least squares and $h(\hat\alpha_0) = \hat\sigma^2$. Write $\gamma = (\alpha_0, \alpha)$ and $c = h'(\alpha_0)$. At the restricted estimates the scores are

$$\frac{\partial\ell}{\partial b} = \frac{X^\top e}{\hat\sigma^2} = 0, \qquad \frac{\partial\ell}{\partial\gamma} = \frac{c}{2\hat\sigma^2}\sum_i(1, z_i^\top)^\top(g_i - 1) = \frac{c}{2\hat\sigma^2}Z^\top(g - \mathbf 1).$$

Under $H_0$ with normal errors, $\mathrm E[(\varepsilon_i^2/\sigma^2 - 1)^2] = 2$ and the mixed second derivatives in $b$ and $\gamma$ have mean 0, because they contain $\varepsilon_i$ or $\varepsilon_i^3$. So the expected information is block diagonal with $\gamma$ block $\frac{c^2}{2\sigma^4}Z^\top Z$. The score statistic is the quadratic form of the score in the inverse information:

$$\mathrm{LM} = \frac{c^2}{4\hat\sigma^4}(g - \mathbf 1)^\top Z\cdot\frac{2\hat\sigma^4}{c^2}(Z^\top Z)^{-1}\cdot Z^\top(g - \mathbf 1) = \tfrac12(g - \mathbf 1)^\top P_Z(g - \mathbf 1).$$

The factor $c$ cancels, so $h$ does not matter. Since $\mathbf 1$ is a column of $Z$ and $\bar g = 1$, $P_Z(g - \mathbf 1) = P_Zg - \bar g\mathbf 1$, and the quadratic form is $\mathrm{ESS}$. $\square$

**Lemma 3 (Breusch-Pagan versus Koenker).** With $\hat v = \frac1n\sum_i(e_i^2 - \hat\sigma^2)^2$,

$$\mathrm{LM}_{\mathrm{BP}} = \frac{\hat v}{2\hat\sigma^4}\,\mathrm{LM}_{\mathrm K}.$$

*Proof.* $\mathrm{TSS} = \sum_i(e_i^2/\hat\sigma^2 - 1)^2 = n\hat v/\hat\sigma^4$, so $\mathrm{ESS} = \mathrm{LM}_{\mathrm K}\,\mathrm{TSS}/n = \mathrm{LM}_{\mathrm K}\,\hat v/\hat\sigma^4$, and $\mathrm{LM}_{\mathrm{BP}} = \mathrm{ESS}/2$. $\square$

Under normal errors $\hat v/(2\hat\sigma^4) \to 1$, and the two statistics agree to first order. For errors with kurtosis $\kappa$, $\hat v/(2\hat\sigma^4) \to (\kappa - 1)/2$, so if Koenker's statistic has a $\chi^2_q$ limit, the Breusch-Pagan statistic has the limit $\frac{\kappa - 1}{2}\chi^2_q$ and its size is wrong unless $\kappa = 3$.

**Lemma 4 (the null law is free of b and sigma).** Under $H_0$ with $\varepsilon \sim N(0, \sigma^2I)$, the law of $(\mathrm{LM}_{\mathrm{BP}}, \mathrm{LM}_{\mathrm K})$ depends only on $X$ and $Z$. So the Monte Carlo p-value $(1 + \#\{T^* \ge T\})/(1 + B)$ from $B$ samples with standard normal errors gives a test of exact size $\alpha$ when $\alpha(B + 1)$ is an integer.

*Proof.* For any $a \ne 0$ and $c \in \mathbb R^p$, the residuals of $ay + Xc$ are $(I - H)(ay + Xc) = ae$. Then $\hat\sigma^2$ becomes $a^2\hat\sigma^2$, and $g$, $\mathrm{ESS}$, $\mathrm{TSS}$ and both statistics do not change. Under $H_0$, $y = Xb + \sigma\varepsilon_0$ with $\varepsilon_0 \sim N(0, I)$, so the statistics are the same functions of $\varepsilon_0$ for every $b$ and $\sigma$. The $B + 1$ values $T, T_1^*, \dots, T_B^*$ are then exchangeable and have no ties with probability 1, so the rank of $T$ is uniform on $\{1, \dots, B + 1\}$ and $P\bigl((1 + \#\{T^* \ge T\})/(1 + B) \le \alpha\bigr) = \alpha$. $\square$

**What is cited, not proved.** Under $H_0$ with normal errors and conditions on $X$ and $Z$, $\mathrm{LM}_{\mathrm{BP}} \to \chi^2_q$ in law (Breusch and Pagan 1979, the general theory of the score test). Under $H_0$ with independent identically distributed errors with a finite fourth moment, $\mathrm{LM}_{\mathrm K} \to \chi^2_q$ (Koenker 1981). Neither limit is proved here, and the size and power figures on the page are measured.

**Termination.** Lines L1 and L3 are Householder factorizations with $p$ and $q + 1$ steps, and the other lines are finite sums: $\Theta(n(p^2 + q^2))$ operations.
