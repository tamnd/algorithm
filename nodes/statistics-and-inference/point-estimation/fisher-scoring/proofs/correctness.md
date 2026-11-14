---
title: Fisher scoring stops at an approximate root of the score, never lowers the likelihood, and equals Newton's method for canonical links
proves: [correctness]
status: full
---

The arithmetic is exact. $\ell$ is the log-likelihood of the sample, $U = \nabla\ell$ its score and $I(\theta)$ the expected information of the sample, which is symmetric and positive definite at every $\theta$ where it is used. Line numbers refer to the `main` pseudocode. Write $T(\theta) = \theta + I(\theta)^{-1}U(\theta)$ for one full scoring step.

**Lemma 1 (fixed points are roots of the score).** $T(\theta) = \theta$ if and only if $U(\theta) = 0$.

*Proof.* $T(\theta) - \theta = I(\theta)^{-1}U(\theta)$, and $I(\theta)^{-1}$ is nonsingular. $\square$

**Lemma 2 (the stopping test).** Let $g = U(\theta)$ and $\delta = I(\theta)^{-1}g$ as in lines L3 to L5. Then $g^{\mathsf T}\delta = g^{\mathsf T}I(\theta)^{-1}g \ge 0$, with equality if and only if $g = 0$. If line L6 returns, then $g^{\mathsf T}I(\theta)^{-1}g \le \varepsilon$; for $\varepsilon = 0$ this means $U(\theta) = 0$.

*Proof.* $I(\theta)^{-1}$ is positive definite because $I(\theta)$ is. So the quadratic form is nonnegative and is zero only for $g = 0$. The return in line L6 happens only when the test holds. $\square$

The quantity $g^{\mathsf T}I^{-1}g$ is the score statistic for the hypothesis that the current $\theta$ is the true value. So the test of line L6 stops when the data give no evidence against the current point; it does not depend on how the parameters are scaled.

**Lemma 3 (ascent direction).** Let $\ell$ be differentiable at $\theta$ and $U(\theta) \ne 0$. Then there is $s_0 > 0$ with $\ell(\theta + s\delta) > \ell(\theta)$ for all $0 < s \le s_0$.

*Proof.* The derivative of $s \mapsto \ell(\theta + s\delta)$ at $s = 0$ is $U(\theta)^{\mathsf T}\delta = g^{\mathsf T}I(\theta)^{-1}g$, which is positive by Lemma 2. A function with positive derivative at 0 is larger than its value at 0 on some interval $(0, s_0]$. $\square$

**Lemma 4 (the likelihood never falls).** With $\ell$ given, every step taken in line L10 satisfies $\ell(\theta_{\text{new}}) \ge \ell(\theta_{\text{old}})$. The loop of line L8 ends after at most $\lceil\log_2(1/s_{\min})\rceil + 1$ halvings.

*Proof.* Line L9 returns without a step when the halved step still lowers $\ell$. So a step that reaches line L10 has $\ell(\theta + s\delta) \ge \ell(\theta)$. The loop of line L8 halves $s$, starting from 1, and stops when $s \le s_{\min}$ at the latest. By Lemma 3, if $s_{\min} < s_0/2$, the first power of 2 that is at most $s_0$ is larger than $s_{\min}$ and gives an increase, so the loop stops there and line L9 does not return. $\square$

**Lemma 5 (canonical links: scoring is Newton's method).** Let $Y_1, \ldots, Y_n$ be independent with densities $\exp(y\eta_i - b(\eta_i) + c(y))$, a canonical exponential family, and $\eta_i = x_i^{\mathsf T}\beta$ (a generalized linear model with canonical link). Then the observed information $J(\beta) = -\nabla^2\ell(\beta)$ equals the expected information $I(\beta)$ for every $\beta$ and every data set, so each scoring step equals the Newton step from the same point.

*Proof.* $\ell(\beta) = \sum_i (Y_i x_i^{\mathsf T}\beta - b(x_i^{\mathsf T}\beta) + c(Y_i))$. Its gradient is $\sum_i x_i(Y_i - b'(\eta_i))$ and its Hessian is $-\sum_i x_i x_i^{\mathsf T} b''(\eta_i)$, which does not contain the data $Y_i$. So it equals its own expectation: $J(\beta) = \sum_i x_i x_i^{\mathsf T}b''(\eta_i) = \mathrm E_\beta J(\beta) = I(\beta)$. Line L5 then solves the same system as Newton's method. $\square$

Logistic regression ($b(\eta) = \log(1 + e^\eta)$) and Poisson regression with log link ($b(\eta) = e^\eta$) are of this form. For them the local quadratic convergence of [Newton's method](/newton-raphson-method/) near a root with nonsingular $J$ applies to scoring without change.

**Lemma 6 (local rate for other models).** Let $U$ and $I$ be continuously differentiable near a root $\hat\theta$ of $U$, and $J(\hat\theta) = -\nabla U(\hat\theta)$. The Jacobian of $T$ at $\hat\theta$ is

$$\nabla T(\hat\theta) = I_k - I(\hat\theta)^{-1}J(\hat\theta).$$

*Proof.* Differentiate $T(\theta) = \theta + I(\theta)^{-1}U(\theta)$ by the product rule. The term that contains the derivative of $I(\theta)^{-1}$ is multiplied by $U(\hat\theta) = 0$, and the other term is $I(\hat\theta)^{-1}\nabla U(\hat\theta) = -I(\hat\theta)^{-1}J(\hat\theta)$. $\square$

By Ostrowski's theorem on fixed-point iterations, if the spectral radius $r$ of $I_k - I(\hat\theta)^{-1}J(\hat\theta)$ is less than 1, then full scoring steps started close enough to $\hat\theta$ converge to $\hat\theta$, and the error falls asymptotically by about the factor $r$ per step. Under a correct model, $J(\hat\theta)/n$ and $I(\hat\theta)/n$ both converge to the information of one observation, so $r \to 0$ as $n$ grows; this is a statement about large samples, and for a given data set $r$ can be near or above 1.

**Theorem.** (a) If FISHER-SCORING returns in line L6, the returned $\theta$ satisfies $U(\theta)^{\mathsf T}I(\theta)^{-1}U(\theta) \le \varepsilon$, and with $\varepsilon = 0$ it is a root of the likelihood equation. (b) With $\ell$ given, the sequence $\ell(\theta_0), \ell(\theta_1), \ldots$ of accepted iterates is nondecreasing. (c) For a canonical exponential family or a GLM with canonical link, without step halving, the iterates are exactly those of Newton's method from the same start.

*Proof.* (a) is Lemma 2, (b) is Lemma 4 and (c) is Lemma 5. $\blacksquare$

The theorem does not say that the returned root is the global maximizer, or that the iteration converges from every start. Neither is true in general: a likelihood can have several local maxima, and for separated data in logistic regression the maximum is not attained at any finite $\beta$.
