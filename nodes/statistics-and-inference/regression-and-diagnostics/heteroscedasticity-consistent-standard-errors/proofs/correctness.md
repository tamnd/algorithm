---
title: The QR form of the heteroscedasticity-consistent covariance equals the sandwich formula, HC2 is unbiased under equal variances, and HC3 is a sum of leave-one-out changes
proves: [correctness, termination]
status: full
---

The arithmetic is exact. $X$ is a fixed real $n \times p$ matrix of rank $p < n$ with rows $x_i^\top$, $\hat b = (X^\top X)^{-1}X^\top y$, $e = y - X\hat b$, and $H = X(X^\top X)^{-1}X^\top$ with diagonal $h_{ii}$. The target of each estimator is

$$\widehat V_\omega = (X^\top X)^{-1}X^\top\Omega X(X^\top X)^{-1}, \qquad \Omega = \operatorname{diag}(\omega_1, \dots, \omega_n),$$

with $\omega_i = e_i^2$ (HC0), $e_i^2n/(n - p)$ (HC1), $e_i^2/(1 - h_{ii})$ (HC2) or $e_i^2/(1 - h_{ii})^2$ (HC3).

**Lemma 1 (lines L1 to L4).** Line L1 gives an upper triangular nonsingular $R$ with $X^\top X = R^\top R$, and line L2 gives $\hat b$. The vectors $q_i = R^{-\top}x_i$ of line L4 are the rows of $Q_1 = XR^{-1}$, which has orthonormal columns, and $h_{ii} = \lVert q_i\rVert^2$.

*Proof.* The Householder argument (Lemma 1 of the proof on the [weighted least squares](/weighted-least-squares/) page, with unit weights) gives $Q^\top X = \binom{R}{0}$ with $Q$ orthogonal and $\hat b = R^{-1}c_{1..p}$, so $X = Q_1R$ with $Q_1$ the first $p$ columns of $Q$, and $X^\top X = R^\top Q_1^\top Q_1R = R^\top R$. Row $i$ of $XR^{-1}$ is $x_i^\top R^{-1} = (R^{-\top}x_i)^\top = q_i^\top$. Then $H = X(R^\top R)^{-1}X^\top = (XR^{-1})(XR^{-1})^\top = Q_1Q_1^\top$, whose $(i, i)$ entry is $\lVert q_i\rVert^2$. $\square$

**Lemma 2 (lines L5 to L7 compute the sandwich).** $R^{-1}\bigl(\sum_i\omega_iq_iq_i^\top\bigr)R^{-\top} = \widehat V_\omega$.

*Proof.* $\sum_i\omega_iq_iq_i^\top = Q_1^\top\Omega Q_1 = R^{-\top}X^\top\Omega XR^{-1}$. So $R^{-1}(\cdot)R^{-\top} = (R^\top R)^{-1}X^\top\Omega X(R^\top R)^{-1}$, and $R^\top R = X^\top X$. $\square$

So the algorithm returns the HC0 to HC3 matrices exactly, and it never forms an $n \times n$ matrix.

**Lemma 3 (HC2 is unbiased when the variances are equal).** If $\mathrm E[\varepsilon] = 0$ and $\operatorname{Cov}(\varepsilon) = \sigma^2I$, then $\mathrm E[e_i^2] = \sigma^2(1 - h_{ii})$ and $\mathrm E[\widehat V_{\mathrm{HC2}}] = \sigma^2(X^\top X)^{-1} = \operatorname{Cov}(\hat b)$.

*Proof.* $e = (I - H)\varepsilon$, so $\operatorname{Cov}(e) = \sigma^2(I - H)(I - H)^\top = \sigma^2(I - H)$, because $I - H$ is symmetric and idempotent. Its diagonal gives $\mathrm E[e_i^2] = \sigma^2(1 - h_{ii})$, so $\mathrm E[e_i^2/(1 - h_{ii})] = \sigma^2$ and $\mathrm E[\Omega] = \sigma^2I$. The sandwich is linear in $\Omega$, so $\mathrm E[\widehat V_{\mathrm{HC2}}] = \sigma^2(X^\top X)^{-1}X^\top X(X^\top X)^{-1} = \sigma^2(X^\top X)^{-1}$. $\square$

Under the same assumption, $\mathrm E[\widehat V_{\mathrm{HC0}}] = \sigma^2(X^\top X)^{-1}X^\top(I - \operatorname{diag}(h_{ii}))X(X^\top X)^{-1}$, which is smaller than $\sigma^2(X^\top X)^{-1}$ by a positive semidefinite matrix; HC0 is biased down, and most where the leverages are large. HC3 is biased up in this case. Under unequal variances none of the four is exactly unbiased.

**Lemma 4 (HC3 is a sum of leave-one-out changes).** Let $\hat b_{(i)}$ be the least squares estimate without row $i$, and $h_{ii} < 1$ for all $i$. Then

$$\hat b_{(i)} - \hat b = -\frac{(X^\top X)^{-1}x_ie_i}{1 - h_{ii}}, \qquad \widehat V_{\mathrm{HC3}} = \sum_{i=1}^n(\hat b_{(i)} - \hat b)(\hat b_{(i)} - \hat b)^\top.$$

*Proof.* Deleting row $i$ changes $X^\top X$ to $A = X^\top X - x_ix_i^\top$ and $X^\top y$ to $X^\top y - x_iy_i$. By the [Sherman-Morrison formula](/sherman-morrison-formula/), with $G = (X^\top X)^{-1}$, $A^{-1} = G + Gx_ix_i^\top G/(1 - h_{ii})$, since $x_i^\top Gx_i = h_{ii}$. Then

$$\hat b_{(i)} = A^{-1}(X^\top y - x_iy_i) = \hat b + \frac{Gx_i\,x_i^\top\hat b}{1 - h_{ii}} - Gx_iy_i - \frac{Gx_ih_{ii}y_i}{1 - h_{ii}} = \hat b - \frac{Gx_i(y_i - x_i^\top\hat b)}{1 - h_{ii}}.$$

Summing the outer products gives $G\bigl(\sum_ix_ix_i^\top e_i^2/(1 - h_{ii})^2\bigr)G = \widehat V_{\mathrm{HC3}}$. $\square$

The jackknife variance of MacKinnon and White (1985) centers the $\hat b_{(i)}$ at their mean $\bar b_{(\cdot)}$ instead of at $\hat b$ and multiplies by $(n - 1)/n$; with $d_i = \hat b_{(i)} - \hat b$ and $\bar d$ their mean, it equals $\frac{n - 1}{n}\bigl(\widehat V_{\mathrm{HC3}} - n\bar d\bar d^\top\bigr)$, by expanding the square. The two differ by a term that is small when no row dominates.

**What is cited, not proved.** Under independent errors with bounded higher moments and regularity conditions on $X$ (the leverages go to 0 and $X^\top X/n$ converges to a nonsingular limit), $n\widehat V_\omega$ converges in probability to the limit of $n\operatorname{Cov}(\hat b)$ for each of HC0 to HC3, so the t statistics are asymptotically standard normal. This is the theorem of Eicker (1967), Huber (1967) and White (1980); it is not proved here, and the coverage figures on the page are measured.

**Termination.** Line L1 is $p$ Householder steps, lines L2 to L4 are $n + 1$ triangular solves of size $p$, line L5 is $n$ scalar operations, and lines L6 and L7 are finite sums: $\Theta(np^2)$ operations in total.
