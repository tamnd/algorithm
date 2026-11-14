---
title: Two-stage least squares computes the projection formula, reduces to the Wald ratio with one binary instrument, and is consistent under valid instruments
proves: [correctness]
status: full
---

Let $y$ be an $n$-vector, $X$ an $n \times k$ matrix and $Z$ an $n \times l$ matrix with $l \ge k$. Assume $Z^\top Z$ is invertible and write $P = Z(Z^\top Z)^{-1}Z^\top$, the orthogonal projection on the column span of $Z$. $P$ is symmetric and $P^2 = P$. TSLS computes $\Pi = (Z^\top Z)^{-1}Z^\top X$ (line L1), $\hat X = Z\Pi$ (line L2) and solves $\hat X^\top X\,b = \hat X^\top y$ (line L3).

**Lemma 1 (the projection form).** $\hat X = PX$, $\hat X^\top X = \hat X^\top\hat X = X^\top PX$ and $\hat X^\top y = X^\top Py$. So if $X^\top PX$ is invertible,

$$b = (X^\top PX)^{-1}X^\top Py,$$

and $b$ is also the least squares coefficient of $y$ on $\hat X$.

*Proof.* $\hat X = Z(Z^\top Z)^{-1}Z^\top X = PX$. Then $\hat X^\top X = X^\top P^\top X = X^\top PX$ and $\hat X^\top\hat X = X^\top P^\top PX = X^\top PX$, using $P^\top = P$ and $P^2 = P$. Also $\hat X^\top y = X^\top Py$. The least squares coefficient of $y$ on $\hat X$ solves $\hat X^\top\hat X\,c = \hat X^\top y$, the same system as line L3. $\square$

**Theorem 2 (just-identified).** If $l = k$ and $Z^\top X$ is invertible, then $b = (Z^\top X)^{-1}Z^\top y$.

*Proof.* $X^\top PX = (X^\top Z)(Z^\top Z)^{-1}(Z^\top X)$ is a product of three invertible $k \times k$ matrices, with inverse $(Z^\top X)^{-1}(Z^\top Z)(X^\top Z)^{-1}$. Multiplying by $X^\top Py = (X^\top Z)(Z^\top Z)^{-1}Z^\top y$ gives $(Z^\top X)^{-1}Z^\top y$. $\square$

**Theorem 3 (no endogeneity).** If $Z = X$ (every regressor is its own instrument) and $X^\top X$ is invertible, $b$ is the OLS coefficient and $\hat X = X$; the HC0 variance of line L6 is then White's OLS sandwich.

*Proof.* $PX = X$ when the columns of $X$ span the space of $P$. Then $\hat X = X$, and lines L3 and L6 become the OLS normal equations and the OLS sandwich. $\square$

**Theorem 4 (the Wald ratio).** Let $X = [\mathbf 1, d]$ and $Z = [\mathbf 1, z]$ with $z \in \{0, 1\}$, both values present. Write $\bar y_1, \bar d_1$ for the means over the units with $z = 1$ and $\bar y_0, \bar d_0$ for $z = 0$. If $\bar d_1 \ne \bar d_0$, then the 2SLS slope is

$$b_d = \frac{\bar y_1 - \bar y_0}{\bar d_1 - \bar d_0},$$

and the intercept is $\bar y - b_d\bar d$.

*Proof.* The model is just-identified, and $Z^\top X$ is invertible: its determinant is $n\sum_i z_id_i - \sum_i z_i\sum_i d_i = n n_1(\bar d_1 - \bar d) = n_1n_0(\bar d_1 - \bar d_0) \ne 0$, with $n_1, n_0$ the group sizes. By Theorem 2, $b = (a, b_d)$ solves $Z^\top(y - Xb) = 0$, that is, $\sum_i(y_i - a - b_dd_i) = 0$ and $\sum_{z_i = 1}(y_i - a - b_dd_i) = 0$. Subtracting, the residuals also sum to 0 over $z = 0$. Dividing by the group sizes, $\bar y_1 = a + b_d\bar d_1$ and $\bar y_0 = a + b_d\bar d_0$. Subtracting gives $b_d$, and the first equation gives $a$. $\square$

**Lemma 5 (which residuals).** The residuals of line L4, $u = y - Xb$, and the residuals of the literal second regression, $\tilde u = y - \hat Xb$, differ by $(X - \hat X)b = (I - P)Xb$. In general $\tilde u^\top\tilde u \ne u^\top u$.

*Proof.* Subtract. For a concrete case, the example on the page has $u^\top u = 47/8$ and $\tilde u^\top\tilde u = 91/4$. $\square$

Under the model $y = X\beta + \varepsilon$, $u$ estimates $\varepsilon$, while $\tilde u = \varepsilon + (X - \hat X)\beta + \hat X(\beta - b)$ contains the first-stage error $(I - P)X\beta$. That is why a regression program run on $\hat X$ gives the right $b$ and the wrong standard errors.

## Consistency

**Theorem 6.** Let the rows $(y_i, x_i, z_i)$ be independent and identically distributed with finite second moments, $y_i = x_i^\top\beta + \varepsilon_i$, and assume

- exogeneity of the instruments: $\mathbb{E}[z_i\varepsilon_i] = 0$;
- rank: $Q_{zz} = \mathbb{E}[z_iz_i^\top]$ is invertible and $Q_{zx} = \mathbb{E}[z_ix_i^\top]$ has rank $k$.

Then $b \to \beta$ in probability.

*Proof.* Substituting $y = X\beta + \varepsilon$ in Lemma 1,

$$b - \beta = \Big(\tfrac{X^\top Z}{n}\big(\tfrac{Z^\top Z}{n}\big)^{-1}\tfrac{Z^\top X}{n}\Big)^{-1}\tfrac{X^\top Z}{n}\big(\tfrac{Z^\top Z}{n}\big)^{-1}\tfrac{Z^\top\varepsilon}{n}.$$

By the law of large numbers $Z^\top Z/n \to Q_{zz}$, $Z^\top X/n \to Q_{zx}$ and $Z^\top\varepsilon/n \to \mathbb{E}[z_i\varepsilon_i] = 0$. The matrix $Q_{zx}^\top Q_{zz}^{-1}Q_{zx}$ is invertible, because $Q_{zz}^{-1}$ is positive definite and $Q_{zx}$ has full column rank. Matrix inversion and multiplication are continuous at these limits, so by the continuous mapping theorem $b - \beta \to (Q_{zx}^\top Q_{zz}^{-1}Q_{zx})^{-1}Q_{zx}^\top Q_{zz}^{-1}\cdot 0 = 0$. $\square$

OLS, by the same argument with $Z = X$, tends to $\beta + Q_{xx}^{-1}\mathbb{E}[x_i\varepsilon_i]$, which differs from $\beta$ when a regressor is correlated with the error. With one endogenous regressor $d$, $\varepsilon = u$, $d = z^\top\pi + v$ and the simulation of the tests, the OLS limit is $\beta + \operatorname{Cov}(d, u)/\operatorname{Var}(d) = 1 + 0.6/1.75 \approx 1.343$.

## What is not proved here

The asymptotic normality $\sqrt n(b - \beta) \to N(0, V)$, the validity of the homoskedastic variance $\sigma^2(X^\top PX)^{-1}$ and of the HC0 sandwich, and the $\chi^2_{l - k}$ limit of Sargan's statistic under valid instruments and homoskedastic errors are cited from Sargan (1958) and the textbook treatment in Angrist and Pischke (2009). Theorem 6 needs a rank condition that holds in the limit; when the instruments are weak, $Q_{zx}$ is close to rank-deficient, and the normal approximation fails in samples of any practical size (Staiger and Stock 1997). The simulation numbers on the page are measured.
