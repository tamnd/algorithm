---
title: The rotated computations equal REML and generalized least squares on the original data
proves: [correctness]
status: full
---

Let $y \in \mathbb R^n$, let $X$ be an $n \times p$ matrix of full column rank with $p < n$, and let $K$ be a symmetric $n \times n$ matrix with the eigendecomposition $K = U \operatorname{diag}(s) U^\top$ from line L1, where $U$ is orthogonal. For $\delta > -\min_i s_i$, put $H_\delta = K + \delta I$, which is positive definite, with $H_\delta = U \operatorname{diag}(s + \delta) U^\top$. The model is $y \sim N(X \beta, \sigma_g^2 H_\delta)$.

**Lemma 1 (rotation).** Let $\tilde y = U^\top y$ and $\tilde X = U^\top X$ (line L2), and $W_\delta = \operatorname{diag}(1/(s_i + \delta))$. Then for all $a, b$, $a^\top H_\delta^{-1} b = (U^\top a)^\top W_\delta (U^\top b)$, and $\log \det H_\delta = \sum_i \log(s_i + \delta)$.

*Proof.* $H_\delta^{-1} = U W_\delta U^\top$ since $U$ is orthogonal, and the determinant of $U \operatorname{diag}(s + \delta) U^\top$ is the product of the $s_i + \delta$. $\square$

**Lemma 2 (REML profile).** The restricted log-likelihood of $(\sigma_g^2, \delta)$, up to a constant that does not depend on them, is

$$\ell_R(\sigma_g^2, \delta) = -\tfrac12 \Bigl[(n - p) \log(2 \pi \sigma_g^2) + \log\det H_\delta + \log\det(X^\top H_\delta^{-1} X) + R(\delta) / \sigma_g^2\Bigr],$$

where $R(\delta) = (y - X \hat\beta_\delta)^\top H_\delta^{-1} (y - X \hat\beta_\delta)$ and $\hat\beta_\delta$ is the generalized least squares estimate. For fixed $\delta$ it is maximized at $\hat\sigma_g^2 = R(\delta)/(n - p)$, and the profile is

$$\ell_R(\delta) = \tfrac12 \Bigl[(n - p) \log \frac{n - p}{2 \pi R(\delta)} - (n - p) - \sum_i \log(s_i + \delta) - \log\det(\tilde X^\top W_\delta \tilde X)\Bigr],$$

which is the function of the code.

*Proof.* The first display is the standard REML likelihood of a linear model with covariance $\sigma_g^2 H_\delta$, with the term $\tfrac12 \log\det X^\top X$ left out (Patterson and Thompson; see the page on [restricted maximum likelihood](/restricted-maximum-likelihood/)). The derivative in $\sigma_g^2$ is $-\tfrac12[(n - p)/\sigma_g^2 - R/\sigma_g^4]$, which is zero only at $R/(n - p)$, and the function goes to $-\infty$ at $0$ and at $\infty$, so this is the maximum. Substituting gives $(n-p) \log(2\pi R/(n-p)) + (n - p)$ in the bracket. By Lemma 1, $\log\det H_\delta = \sum \log(s_i + \delta)$, $X^\top H_\delta^{-1} X = \tilde X^\top W_\delta \tilde X$, and $\hat\beta_\delta$ and $R(\delta)$ are the weighted least squares estimate and weighted residual sum of squares of $\tilde y$ on $\tilde X$ with the weights $W_\delta$. $\square$

So the search of line L3 maximizes the true REML profile, and line L4 returns the REML estimates of $\sigma_g^2$ and $\sigma_e^2 = \delta \sigma_g^2$ at the $\delta$ found. The search is a grid over $\log \delta$ followed by golden-section search between the neighbours of the best grid point. Golden-section search keeps a bracket that contains the maximizer of a unimodal function and shrinks it by a constant factor at each step, so it returns the maximum when $\ell_R$ is unimodal between these neighbours. The returned value is never below the best grid value, because the code keeps the grid point when it is better.

**Theorem (per-SNP test).** For a SNP with dosage vector $g$, let $Z = [X, g]$ and $V = \hat\sigma_g^2 H_{\hat\delta}$. Lines L5 to L7 return the generalized least squares estimate

$$\hat b = \bigl[(Z^\top V^{-1} Z)^{-1} Z^\top V^{-1} y\bigr]_{p+1}, \qquad \operatorname{Var}(\hat b) = \bigl[(Z^\top V^{-1} Z)^{-1}\bigr]_{p+1, p+1},$$

and $T = \hat b^2 / \operatorname{Var}(\hat b)$. If $y \sim N(X \beta, V)$ with this $V$, then $T$ follows the chi-squared law with 1 degree of freedom.

*Proof.* Line L5 computes $\tilde g = U^\top g$, so $U^\top Z = [\tilde X, \tilde g]$. By Lemma 1 with the weights $1/(\hat\sigma_g^2 (s_i + \hat\delta))$, $Z^\top V^{-1} Z$ and $Z^\top V^{-1} y$ are the weighted cross products of the rotated data, which line L6 forms and solves. So the code returns the stated $\hat b$ and variance. Under the model, $\hat b$ is a linear function of the normal vector $y$. Its mean is the coefficient of $g$ in the mean of $y$, which is $0$ under the null, and its variance is the stated one by the usual computation $\operatorname{Var}(A y) = A V A^\top$ with $A = (Z^\top V^{-1} Z)^{-1} Z^\top V^{-1}$. So $\hat b / \sqrt{\operatorname{Var}(\hat b)}$ is standard normal and $T$ is chi-squared with 1 degree of freedom. $\square$

**What the theorem does not say.** In practice $V$ is estimated, once, under the null and from the same data. Then $T$ is only approximately chi-squared. The approximation is good when each SNP explains a small part of the variance, which is the setting of the method. For a SNP with a large effect, the null estimate of $\sigma_g^2$ and $\sigma_e^2$ absorbs part of its effect, and the test loses some power. Re-estimating the components for each SNP gives the exact REML test at a cost of $O(n p^2)$ per evaluation of $\ell_R$ per SNP, after the same rotation.
