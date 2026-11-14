---
title: The AIPW estimate has mean equal to the ATE if either the propensity model or the outcome model is right
proves: [correctness]
status: full
---

Unit $i$ has treatment $T_i \in \{0, 1\}$, outcome $Y_i$, a propensity value $\tilde e_i$ with $0 < \tilde e_i < 1$ and two outcome predictions $m_{1i}$ and $m_{0i}$. Write

$$\psi_i = m_{1i} - m_{0i} + \frac{T_i(Y_i - m_{1i})}{\tilde e_i} - \frac{(1 - T_i)(Y_i - m_{0i})}{1 - \tilde e_i}.$$

All arithmetic is exact.

**Lemma 1 (the loop).** AIPW-ATE returns $\hat\mu_1 = \frac1n\sum_i \big(m_{1i} + T_i(Y_i - m_{1i})/\tilde e_i\big)$, $\hat\mu_0 = \frac1n\sum_i\big(m_{0i} + (1 - T_i)(Y_i - m_{0i})/(1 - \tilde e_i)\big)$ and $\hat\tau = \hat\mu_1 - \hat\mu_0 = \frac1n\sum_i\psi_i$.

*Proof.* Line L1 sets $s_1 = s_0 = 0$, and the loop L2 visits each unit once. Line L3 changes nothing. For a treated unit, line L4 adds $m_{1i} + (Y_i - m_{1i})/\tilde e_i$ to $s_1$ and $m_{0i}$ to $s_0$; these are the unit's terms of the two sums, because $T_i = 1$ and $1 - T_i = 0$. For a control, line L5 adds $m_{1i}$ to $s_1$ and $m_{0i} + (Y_i - m_{0i})/(1 - \tilde e_i)$ to $s_0$, again the unit's terms. Line L6 divides by $n$, and the difference of the two sums is $\sum_i \psi_i$ term by term. $\square$

## The double robustness identity

Here the units $(X_i, T_i, Y_i(0), Y_i(1))$ are independent copies of $(X, T, Y(0), Y(1))$. Let $e(x) = \Pr[T = 1 \mid X = x]$ be the true propensity and $\mu_t(x) = \mathbb{E}[Y(t) \mid X = x]$ the true outcome regressions. Assume consistency $Y = TY(1) + (1 - T)Y(0)$, ignorability $(Y(0), Y(1)) \perp T \mid X$, positivity $0 < e(X) < 1$, and $\mathbb{E}|Y(t)| < \infty$ for $t = 0, 1$. The working models are fixed functions $\tilde e(x)$, $m_1(x)$, $m_0(x)$ that do not depend on the sample, with $0 < \tilde e(X) < 1$, and with $m_t(X)$, $m_t(X)/\tilde e(X)$ and $m_t(X)/(1 - \tilde e(X))$ integrable. Put $\tilde e_i = \tilde e(X_i)$ and $m_{ti} = m_t(X_i)$, and let $\psi$ be the score of a generic unit.

**Theorem 2 (bias identity).** With $\tau = \mathbb{E}[Y(1) - Y(0)]$,

$$\mathbb{E}[\psi] - \tau = \mathbb{E}\left[\left(\frac{e(X)}{\tilde e(X)} - 1\right)\big(\mu_1(X) - m_1(X)\big)\right] - \mathbb{E}\left[\left(\frac{1 - e(X)}{1 - \tilde e(X)} - 1\right)\big(\mu_0(X) - m_0(X)\big)\right].$$

*Proof.* By consistency $T Y = T Y(1)$. By ignorability $T \perp Y(1) \mid X$, so $\mathbb{E}[TY \mid X] = e(X)\mu_1(X)$, and $\mathbb{E}[T m_1(X) \mid X] = e(X)m_1(X)$. Since $\tilde e(X)$ is a function of $X$,

$$\mathbb{E}\left[\frac{T(Y - m_1(X))}{\tilde e(X)} \,\middle|\, X\right] = \frac{e(X)}{\tilde e(X)}\big(\mu_1(X) - m_1(X)\big).$$

In the same way $(1 - T)Y = (1 - T)Y(0)$ and $T \perp Y(0) \mid X$ give $\mathbb{E}[(1 - T)(Y - m_0(X))/(1 - \tilde e(X)) \mid X] = \frac{1 - e(X)}{1 - \tilde e(X)}(\mu_0(X) - m_0(X))$. The integrability conditions make every term integrable (as in the identification proof of the [IPW page](/inverse-probability-weighting/), with absolute values first). So

$$\mathbb{E}[\psi \mid X] = m_1 - m_0 + \frac{e}{\tilde e}(\mu_1 - m_1) - \frac{1 - e}{1 - \tilde e}(\mu_0 - m_0),$$

with every function evaluated at $X$. Subtract $\mu_1 - \mu_0 = (\mu_1 - m_1) - (\mu_0 - m_0) + (m_1 - m_0)$:

$$\mathbb{E}[\psi \mid X] - (\mu_1 - \mu_0) = \left(\frac{e}{\tilde e} - 1\right)(\mu_1 - m_1) - \left(\frac{1 - e}{1 - \tilde e} - 1\right)(\mu_0 - m_0).$$

Take expectations. By the tower property of [conditional expectation](/conditional-expectation/), $\mathbb{E}[\mathbb{E}[\psi \mid X]] = \mathbb{E}[\psi]$, and $\mathbb{E}[\mu_1(X) - \mu_0(X)] = \tau$. $\square$

**Corollary 3 (double robustness).** If $\tilde e = e$, or if $m_1 = \mu_1$ and $m_0 = \mu_0$, then $\mathbb{E}[\psi] = \tau$. So with fixed working models of which at least one is right, $\mathbb{E}[\hat\tau] = \tau$, and $\hat\tau \to \tau$ almost surely by the strong [law of large numbers](/law-of-large-numbers/).

*Proof.* If $\tilde e = e$, then $e/\tilde e - 1 = 0$ and $(1 - e)/(1 - \tilde e) - 1 = 0$ for every $x$. If $m_t = \mu_t$, then $\mu_t - m_t = 0$. In both cases each product in Theorem 2 is 0 for every $x$. By Lemma 1 and [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[\hat\tau] = \mathbb{E}[\psi] = \tau$. The $\psi_i$ are independent and identically distributed with finite mean, so the strong law applies. $\square$

**Corollary 4 (product bound).** If $\tilde e(X) \in [c, 1 - c]$ for a constant $c > 0$, and $\|f\| = (\mathbb{E}[f(X)^2])^{1/2}$, then

$$|\mathbb{E}[\psi] - \tau| \le \frac1c\,\|e - \tilde e\|\,\big(\|\mu_1 - m_1\| + \|\mu_0 - m_0\|\big).$$

*Proof.* $e/\tilde e - 1 = (e - \tilde e)/\tilde e$ and $(1 - e)/(1 - \tilde e) - 1 = (\tilde e - e)/(1 - \tilde e)$, and both denominators are at least $c$. Apply the Cauchy-Schwarz inequality to each term of Theorem 2. $\square$

The bias is a product of the two errors, so it is small when both errors are moderately small. This product form is the reason that [double machine learning](/double-machine-learning/) can use slowly converging learners for both nuisances.

## Estimated working models

**Theorem 5 (consistency).** Let $\hat e$, $\hat m_1$, $\hat m_0$ be estimated from the sample, and suppose there are fixed functions $\bar e$, $\bar m_1$, $\bar m_0$ with $\bar e(x) \in [c, 1 - c]$ for all $x$ and $\mathbb{E}|\bar m_t(X)| < \infty$, such that $\delta_n = \sup_x |\hat e(x) - \bar e(x)| + \sum_t \sup_x |\hat m_t(x) - \bar m_t(x)| \to 0$ in probability. If $\bar e = e$ or $(\bar m_1, \bar m_0) = (\mu_1, \mu_0)$, then $\hat\tau \to \tau$ in probability.

*Proof.* Write $\hat\tau(\hat e, \hat m)$ and $\hat\tau(\bar e, \bar m)$ for the estimate with the estimated and the limit functions. On the event $\delta_n < c/2$, whose probability tends to 1, every $\hat e(X_i)$ lies in $[c/2, 1 - c/2]$. For a treated unit,

$$\frac{Y_i - \hat m_{1i}}{\hat e_i} - \frac{Y_i - \bar m_{1i}}{\bar e_i} = (Y_i - \bar m_{1i})\left(\frac{1}{\hat e_i} - \frac{1}{\bar e_i}\right) - \frac{\hat m_{1i} - \bar m_{1i}}{\hat e_i},$$

and $|1/\hat e_i - 1/\bar e_i| = |\bar e_i - \hat e_i|/(\hat e_i\bar e_i) \le 2\delta_n/c^2$, so the absolute value is at most $(2/c^2)\,\delta_n|Y_i - \bar m_{1i}| + (2/c)\,\delta_n$. The control term has the same bound with $\bar m_0$, and the two $m$ terms differ by at most $2\delta_n$. Hence

$$|\hat\tau(\hat e, \hat m) - \hat\tau(\bar e, \bar m)| \le \delta_n\left(2 + \frac{4}{c} + \frac{2}{c^2}\cdot\frac1n\sum_i \big(|Y_i - \bar m_{1i}| + |Y_i - \bar m_{0i}|\big)\right).$$

The average on the right converges to a finite constant by the law of large numbers, so the right side tends to 0 in probability. By Corollary 3, $\hat\tau(\bar e, \bar m) \to \tau$. $\square$

The uniform convergence holds, for example, for a logistic propensity model and linear outcome models fitted by maximum likelihood and least squares on a bounded covariate space with a nonsingular design: the coefficients converge to the minimizers of the population criteria (the limits $\bar e$ and $\bar m$), whether or not the models are right.

## Exact identities with a discrete covariate

Let $X$ take finitely many values, let stratum $x$ have $n_x$ units, $n_{1x} \ge 1$ treated and $n_{0x} \ge 1$ controls, and let $\bar Y_{tx}$ be the mean outcome of arm $t$ in stratum $x$. The stratified estimate is $\hat\tau_S = \sum_x \frac{n_x}{n}(\bar Y_{1x} - \bar Y_{0x})$.

**Theorem 6.** (a) If $\tilde e(x) = n_{1x}/n_x$, then $\hat\tau = \hat\tau_S$ for all functions $m_1(x), m_0(x)$. (b) If $m_t(x) = \bar Y_{tx}$, then $\hat\tau = \hat\tau_S$ for every function $\tilde e(x)$ with values in $(0, 1)$.

*Proof.* Fix a stratum $x$ and look at its share of $n\hat\mu_1$, which is $n_x m_1(x) + \sum_{i:\,X_i = x,\,T_i = 1}(Y_i - m_1(x))/\tilde e(x) = n_x m_1(x) + n_{1x}(\bar Y_{1x} - m_1(x))/\tilde e(x)$. In case (a), $n_{1x}/\tilde e(x) = n_x$, so the share is $n_x\bar Y_{1x}$. In case (b), $\bar Y_{1x} - m_1(x) = 0$, so the share is again $n_x\bar Y_{1x}$. The same steps with $1 - \tilde e(x) = n_{0x}/n_x$ or $m_0(x) = \bar Y_{0x}$ give the share $n_x\bar Y_{0x}$ of $n\hat\mu_0$. Sum over the strata and divide by $n$. $\square$

Theorem 6 is the sample version of Corollary 3: the empirical propensity and the cell means are the saturated estimates of $e$ and $\mu_t$, and either one alone gives the stratified estimate exactly.

## What is not proved here

The asymptotic normality of $\sqrt n(\hat\tau - \tau)$ with estimated working models, the fact that the plug-in variance $S_\psi^2/n$ is consistent when both models are right, and the fact that the variance $\mathbb{E}[(\psi - \tau)^2]$ with the true $e$ and $\mu_t$ equals the semiparametric efficiency bound are cited on the page (Robins, Rotnitzky and Zhao 1994; Hahn 1998; Tsiatis 2006, Chapter 13). The coverage figures on the page are measured by simulation.
