---
title: The bootstrap-t interval inverts the bootstrap law of the studentized statistic
proves: [correctness]
status: full
---

We use the pseudocode of the page. The data are fixed, `est` returns $(\hat\theta, \widehat{se})$ with $\widehat{se} > 0$, and $T^* = (\hat\theta^* - \hat\theta)/\widehat{se}^*$ with the convention of the page when $\widehat{se}^* = 0$. $K$ is the bootstrap distribution function of $T^*$, $\hat K_b$ the empirical distribution function of the $b$ replicates, and $K^{-1}(p) = \inf\{t : K(t) \ge p\}$ for any distribution function $K$, with values in $[-\infty, \infty]$.

This file proves what the algorithm computes and when the ideal interval is exact. It does not prove a coverage level for a nonparametric $F$; that coverage is measured on the page.

**Claim 1 (lines L6 and L7).** $t_{lo} = \hat K_b^{-1}(\alpha/2)$ and $t_{hi} = \hat K_b^{-1}(1 - \alpha/2)$.

*Proof.* The argument of Claim 1 of the [percentile interval](/bootstrap-percentile-interval/) applies to any $b$ values in the extended real line: for $0 < p < 1$ and $k = \lceil b p \rceil$, at least $k$ replicates are $\le t^*_{(k)}$ and at most $k - 1 < b p$ are below it. $\square$

**Claim 2 (inversion).** For every $\theta$ and every pair $t_{lo} \le t_{hi}$,

$$t_{lo} \le \frac{\hat\theta - \theta}{\widehat{se}} \le t_{hi} \iff \hat\theta - t_{hi}\, \widehat{se} \le \theta \le \hat\theta - t_{lo}\, \widehat{se}.$$

*Proof.* Multiply by $\widehat{se} > 0$, which keeps the order, and subtract $\hat\theta$; then multiply by $-1$, which reverses both inequalities. $\square$

So line L8 returns the set of $\theta$ for which the studentized value $T = (\hat\theta - \theta)/\widehat{se}$ lies between the two bootstrap quantiles. Note that the upper quantile gives the lower endpoint.

**Claim 3 (exact coverage when the bootstrap law is the true law).** If $T$ has a continuous distribution function $K$, the interval $[\hat\theta - K^{-1}(1 - \alpha/2)\, \widehat{se},\ \hat\theta - K^{-1}(\alpha/2)\, \widehat{se}]$ contains $\theta$ with probability exactly $1 - \alpha$.

*Proof.* By Claim 2 the event is $K^{-1}(\alpha/2) \le T \le K^{-1}(1 - \alpha/2)$. For a continuous $K$, $K(K^{-1}(p)) = p$ and $P(T < K^{-1}(p)) = p$ as well. So the probability is $(1 - \alpha/2) - \alpha/2 = 1 - \alpha$. $\square$

Claim 3 is the reason for the method: if $T$ is a pivot, its law does not depend on $F$, and a bootstrap that reproduces it gives an exact interval. For normal data and the mean, $T$ has the Student law with $n - 1$ degrees of freedom, and the [parametric bootstrap](/parametric-bootstrap/) with the normal model reproduces it, so its ideal bootstrap-t interval is the [t interval](/t-confidence-interval/). The nonparametric bootstrap law $K$ is discrete and only approximates the law of $T$.

**Claim 4 (affine equivariance).** Let $c > 0$ and $d$ be real numbers, and suppose `est` is equivariant: $\mathrm{est}(c x + d) = (c \hat\theta + d,\ c\, \widehat{se})$ for every sample $x$. Run the algorithm on $x$ and on $y = c x + d$ with the same random numbers. If the first run returns $[L, U]$, the second returns $[c L + d,\ c U + d]$.

*Proof.* Line L3 draws the same indices in both runs, so the $j$-th resample of $y$ is $c x^* + d$. Line L4 gives $(c\hat\theta^* + d,\ c\, \widehat{se}^*)$. If $\widehat{se}^* > 0$, then $(c\hat\theta^* + d - c\hat\theta - d)/(c\, \widehat{se}^*) = t^*_j$. If $\widehat{se}^* = 0$, then $c\, \widehat{se}^* = 0$, and $c(\hat\theta^* - \hat\theta)$ has the sign of $\hat\theta^* - \hat\theta$, so the convention gives the same value. So both runs have the same $t^*_j$, the same $t_{lo}$ and $t_{hi}$, and line L8 gives $c\hat\theta + d - t_{hi}\, c\, \widehat{se} = c L + d$ and likewise $c U + d$. $\square$

The mean with $\widehat{se} = S/\sqrt n$ is equivariant in this sense. The tests check the claim with $c = 2$ and $d = 5$ up to rounding. For $c < 0$, $t^*$ changes sign and the order is reversed, so the two endpoints are mirror images only up to one rank, as in the percentile interval. The method is not equivariant under nonlinear monotone maps; the page shows a counterexample with the logarithm.

**Claim 5 (zero standard errors).** Line L5 is defined for every resample. Let $k = \lceil b\alpha/2 \rceil$ and $k' = \lceil b(1 - \alpha/2) \rceil$. The upper endpoint is $+\infty$ exactly when at least $k$ replicates are $-\infty$, which is the same as at least $b\alpha/2$ of them. The lower endpoint is $-\infty$ exactly when at least $b - k' + 1 = \lfloor b\alpha/2 \rfloor + 1$ replicates are $+\infty$, which is the same as more than $b\alpha/2$ of them.

*Proof.* The convention assigns a value in $\{-\infty, 0, +\infty\}$ when $\widehat{se}^* = 0$, so no division by zero happens. In sorted order, $t^*_{(k)} = -\infty$ exactly when at least $k$ values are $-\infty$, and $t^*_{(k')} = +\infty$ exactly when at least $b - k' + 1$ values are $+\infty$. The identity $b - \lceil b(1 - \alpha/2) \rceil = \lfloor b\alpha/2 \rfloor$ holds because $b$ is an integer. For an integer count $m$, $m \ge \lceil b\alpha/2 \rceil$ is the same as $m \ge b\alpha/2$. By line L8, $t_{lo} = -\infty$ makes the upper endpoint $+\infty$, and $t_{hi} = +\infty$ makes the lower endpoint $-\infty$. $\square$

The tests compute the ideal law of $T^*$ by listing all $n^n$ resamples for $n \le 5$ and compare it with the multiset enumeration of the implementation. For the sample $(0, 1)$ the law puts mass $1/4$ on $-\infty$, $1/2$ on $0$ and $1/4$ on $+\infty$.

**What is not proved.** For a nonparametric $F$ and a smooth statistic, Hall (1988) shows by Edgeworth expansions that each one-sided endpoint has coverage error $O(n^{-1})$, because the bootstrap reproduces the first skewness term of the expansion of the law of $T$. That result needs moment and smoothness conditions that this file does not check. The coverages on the page are measurements from a simulation with stated seeds, with a Monte Carlo standard error of about $0.007$.

**Cost.** The loop runs $b$ times; each pass draws $n$ indices and calls `est`, which costs $\Theta(n)$ for the mean. Line L6 sorts $b$ values in $\Theta(b \log b)$ time. The total is $\Theta(b n + b \log b)$ time and $\Theta(b + n)$ extra space.
