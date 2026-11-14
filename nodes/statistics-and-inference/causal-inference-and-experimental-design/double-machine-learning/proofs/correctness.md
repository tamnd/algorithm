---
title: Cross-fitting makes the bias of the DML estimate a product of nuisance errors, and the score is Neyman orthogonal
proves: [correctness]
status: full
---

The units $W_i = (X_i, T_i, Y_i)$, $i = 1, \ldots, n$, are independent copies of $W = (X, T, Y)$. For the ATE, assume consistency with SUTVA, ignorability and positivity as on the [AIPW page](/augmented-inverse-probability-weighting/), and write $e(x) = \Pr[T = 1 \mid X = x]$ and $\mu_t(x) = \mathbb{E}[Y \mid T = t, X = x]$. For working functions $\eta = (\tilde e, m_1, m_0)$ the AIPW score is

$$\psi(W; \eta) = m_1(X) - m_0(X) + \frac{T(Y - m_1(X))}{\tilde e(X)} - \frac{(1 - T)(Y - m_0(X))}{1 - \tilde e(X)}.$$

**Lemma 1 (folds).** MAKE-FOLDS gives every unit one label in $\{0, \ldots, k - 1\}$, and the fold sizes differ by at most 1.

*Proof.* The unit at position $p$ of the permutation, $0 \le p < n$, gets label $\lfloor pk/n\rfloor$, which is in $\{0, \ldots, k - 1\}$. Label $f$ goes to the positions $p$ with $fn/k \le p < (f + 1)n/k$, which number $\lceil (f + 1)n/k\rceil - \lceil fn/k\rceil$. This is $\lfloor n/k\rfloor$ or $\lceil n/k\rceil$, since $\lceil a + n/k\rceil - \lceil a\rceil$ is one of these two for every real $a$. $\square$

**Lemma 2 (the loop).** DML-ATE returns $\hat\tau = \frac1n\sum_i \psi(W_i; \hat\eta^{(-f(i))})$, where $f(i)$ is the fold of unit $i$ and $\hat\eta^{(-f)}$ is fitted on the units outside fold $f$. If the learners ignore their training data and return fixed functions $\eta$, then $\hat\tau$ is the AIPW estimate with $\eta$, for every $k$ and every fold assignment.

*Proof.* Line L2 visits each fold once, and by Lemma 1 every unit is in exactly one fold, so line L6 sets each $\psi_i$ once, with the nuisances of line L3 and L4 fitted on the other folds. Line L7 averages. If the learners return fixed $\eta$, every $\hat\eta^{(-f)} = \eta$. $\square$

## Exact bias with cross-fitting

**Theorem 3.** Let $D_{-f}$ be the units outside fold $f$, and suppose the fitted propensity satisfies $\hat e^{(-f)}(x) \in [c, 1 - c]$. For a unit $i$ in fold $f$,

$$\mathbb{E}\big[\psi(W_i; \hat\eta^{(-f)}) \,\big|\, D_{-f}\big] - \tau = \mathbb{E}_X\left[\Big(\frac{e}{\hat e} - 1\Big)(\mu_1 - \hat m_1) - \Big(\frac{1 - e}{1 - \hat e} - 1\Big)(\mu_0 - \hat m_0)\right],$$

with $\hat e, \hat m_t$ the functions fitted on $D_{-f}$ and $\mathbb{E}_X$ the expectation over a new $X$. Hence

$$\big|\mathbb{E}[\psi(W_i; \hat\eta^{(-f)}) \mid D_{-f}] - \tau\big| \le \frac1c\,\|e - \hat e\|\,\big(\|\mu_1 - \hat m_1\| + \|\mu_0 - \hat m_0\|\big),$$

where $\|g\| = (\mathbb{E}_X[g(X)^2])^{1/2}$.

*Proof.* The units are independent, so $W_i$ is independent of $D_{-f}$, and given $D_{-f}$ the functions $\hat\eta^{(-f)}$ are fixed. The bias identity of the AIPW page (Theorem 2 there) holds for any fixed working functions, so it applies to $\hat\eta^{(-f)}$ conditionally on $D_{-f}$. The bound follows by the Cauchy-Schwarz inequality, as in Corollary 4 there. $\square$

Without cross-fitting ($k = 1$), $\hat\eta$ depends on $W_i$ itself, the conditioning step fails, and $\mathbb{E}[\psi(W_i; \hat\eta)]$ has no such form; an overfitted learner can then make the residuals $Y_i - \hat m_{T_i}(X_i)$ small for the units it was fitted on. The tests check the key fact behind Theorem 3: with cross-fitting, raising $Y_i$ by 1 changes $\psi_i$ by exactly $1/\hat e_i$ (or $-1/(1 - \hat e_i)$) and leaves the other scores of its fold unchanged, while with $k = 1$ other scores change too.

## Neyman orthogonality

**Theorem 4 (ATE score).** Let $\eta_0 = (e, \mu_1, \mu_0)$, and for bounded directions $h = (h_e, h_1, h_0)$ let $\eta_r = \eta_0 + rh$. Then $\frac{d}{dr}\mathbb{E}[\psi(W; \eta_r)]\big|_{r = 0} = 0$.

*Proof.* By the bias identity with $\tilde e = e + rh_e$ and $m_t = \mu_t + rh_t$,

$$\mathbb{E}[\psi(W; \eta_r)] - \tau = \mathbb{E}\left[\frac{-rh_e}{e + rh_e}(-rh_1) - \frac{rh_e}{1 - e - rh_e}(-rh_0)\right] = r^2\,\mathbb{E}\left[\frac{h_eh_1}{e + rh_e} + \frac{h_eh_0}{1 - e - rh_e}\right].$$

For $|r|$ small, $e + rh_e$ and $1 - e - rh_e$ stay above $c/2$ if $e \in [c, 1 - c]$, so the expectation is bounded, and the whole is $O(r^2)$. Its derivative at $r = 0$ is 0. $\square$

**Theorem 5 (partially linear score).** In the model $Y = \theta_0 T + g(X) + U$ with $\mathbb{E}[U \mid X, T] = 0$, let $m(X) = \mathbb{E}[T \mid X]$, $l(X) = \mathbb{E}[Y \mid X]$, and $\psi(W; \theta, l, m) = (Y - l(X) - \theta(T - m(X)))(T - m(X))$. Then $\mathbb{E}[\psi(W; \theta_0, l, m)] = 0$, and the derivative of $\mathbb{E}[\psi(W; \theta_0, l + rh_l, m + rh_m)]$ at $r = 0$ is 0. If $\mathbb{E}[(T - m(X))^2] > 0$, then $\theta_0 = \mathbb{E}[(T - m)(Y - l)]/\mathbb{E}[(T - m)^2]$.

*Proof.* $l(X) = \theta_0 m(X) + g(X)$, so $Y - l(X) - \theta_0(T - m(X)) = U$. Write $V = T - m(X)$, which has $\mathbb{E}[V \mid X] = 0$. Then $\mathbb{E}[UV] = \mathbb{E}[V\,\mathbb{E}[U \mid X, T]] = 0$. With the perturbed functions, the score is $(U - rh_l + \theta_0 rh_m)(V - rh_m)$, whose mean is

$$\mathbb{E}[UV] - r\,\mathbb{E}[Uh_m] - r\,\mathbb{E}[(h_l - \theta_0h_m)V] + r^2\,\mathbb{E}[(h_l - \theta_0h_m)h_m].$$

$\mathbb{E}[Uh_m(X)] = 0$ because $\mathbb{E}[U \mid X] = 0$, and $\mathbb{E}[(h_l - \theta_0h_m)(X)V] = 0$ because $\mathbb{E}[V \mid X] = 0$. So the mean is $r^2$ times a constant, with derivative 0 at $r = 0$. The last claim: $\mathbb{E}[V(Y - l)] = \mathbb{E}[V(\theta_0V + U)] = \theta_0\mathbb{E}[V^2]$. $\square$

**Theorem 6 (no cross-fitting, linear learners).** If $k = 1$ and both learners are least squares on the same feature vector $F(x)$, and the regression of $Y$ on $(T, F(X))$ has a unique solution, then $\hat\theta$ equals the OLS coefficient of $T$ in that regression.

*Proof.* This is the Frisch-Waugh-Lovell theorem. Let $\mathbf F$ be the $n \times q$ feature matrix, $P$ the projection on its columns and $M = I - P$. The fitted learners give the residuals $\tilde T = M\mathbf T$ and $\tilde Y = M\mathbf Y$, so $\hat\theta = \tilde T^\top\tilde Y/\tilde T^\top\tilde T$. The OLS fit is $\mathbf Y = b\mathbf T + \mathbf F\gamma + \mathbf u$ with $\mathbf F^\top\mathbf u = 0$ and $\mathbf T^\top\mathbf u = 0$. Then $P\mathbf u = 0$, and $M\mathbf Y = bM\mathbf T + M\mathbf F\gamma + M\mathbf u = b\tilde T + \mathbf u$. So $\tilde T^\top\tilde Y = b\,\tilde T^\top\tilde T + \mathbf T^\top M\mathbf u = b\,\tilde T^\top\tilde T + \mathbf T^\top\mathbf u = b\,\tilde T^\top\tilde T$. Uniqueness of the OLS solution means $\mathbf T$ is not in the column span of $\mathbf F$, so $\tilde T^\top\tilde T > 0$, and $\hat\theta = b$. $\square$

## What is not proved here

The asymptotic normality $\sqrt n(\hat\tau - \tau) \to N(0, V)$ with $V = \mathbb{E}[(\psi(W; \eta_0) - \tau)^2]$, under the conditions that the propensity stays in $[c, 1 - c]$, that each nuisance error tends to 0, and that the product of the propensity error and the outcome error is $o(n^{-1/2})$, and the same result for $\hat\theta$ in the partially linear model, are cited from Chernozhukov et al. (2018). Theorem 3 shows why the product condition controls the bias; the control of the remaining empirical-process term by cross-fitting is in that paper. The simulation numbers on the page are measured.
