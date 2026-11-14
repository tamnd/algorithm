---
tag: J9VXM1
kind: theorem
slug: delta-method
name: Delta method
aliases:
- propagation of error
area: statistics-and-inference/point-estimation
level: core
summary: If sqrt(n)(T_n - theta) converges in distribution to N(0, sigma^2) and g is differentiable at theta, then sqrt(n)(g(T_n) - g(theta)) converges to N(0, g'(theta)^2 sigma^2).
prereqs: [slutsky-theorem, central-limit-theorem, standard-error]
see_also: [asymptotic-normality-of-mle, wald-test, fieller-theorem, wilson-score-interval, confidence-interval, bootstrap-method, m-estimator, logistic-regression]
sources:
  - paper: doi:10.1214/aoms/1177732594
    title: J. L. Doob, The limiting distributions of certain statistics, Annals of Mathematical Statistics 6(3), 1935
    locator: pages 160 to 169 (limit laws of smooth functions of asymptotically normal statistics)
  - paper: "J. M. Ver Hoef, Who invented the delta method?, The American Statistician 66(2), 2012"
    locator: pages 124 to 127 (history of the method, Dorfman 1938, and earlier uses)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 5.5.4, Theorem 5.5.24 (delta method), Theorem 5.5.26 (second-order delta method) and Theorem 5.5.28 (multivariate delta method)
  - book: isbn:9780521496032
    title: A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998
    locator: Chapter 3, Theorem 3.1 (delta method for maps between Euclidean spaces) and Section 3.2 (variance-stabilizing transformations)
---

The delta method gives the limit law of a smooth function of an asymptotically normal statistic. If $T_n$ is close to $\theta$ with an error of order $1/\sqrt n$ that is asymptotically normal, then $g(T_n)$ is close to $g(\theta)$, and to first order the error is the old error times the slope $g'(\theta)$. The result turns the [central limit theorem](/central-limit-theorem/) for a mean into a limit law, and so into a [standard error](/standard-error/), for a ratio, a log odds, a correlation or any other smooth function of means. The proof is a first-order Taylor step and one use of [Slutsky's theorem](/slutsky-theorem/).

## Statement

**Theorem (delta method).** Let $T_n$ be real random variables and $\theta$ a constant. Assume:

1. $\sqrt n\,(T_n - \theta) \xrightarrow{d} Y$ for some random variable $Y$;
2. $g$ is a real function on an open set that contains $\theta$ and the values of $T_n$, and $g$ is differentiable at $\theta$.

Then $\sqrt n\,(g(T_n) - g(\theta)) \xrightarrow{d} g'(\theta)\,Y$. In particular, if $Y \sim N(0, \sigma^2)$, then

$$\sqrt n\,\bigl(g(T_n) - g(\theta)\bigr) \xrightarrow{d} N\bigl(0,\ g'(\theta)^2\,\sigma^2\bigr).$$

If $g'(\theta) = 0$, the limit is the constant 0, and the next result applies.

**Theorem (second-order delta method).** Assume $\sqrt n\,(T_n - \theta) \xrightarrow{d} N(0, \sigma^2)$, $g'(\theta) = 0$, and $g$ is twice differentiable at $\theta$ with $g''(\theta) \ne 0$. Then

$$n\,\bigl(g(T_n) - g(\theta)\bigr) \xrightarrow{d} \tfrac12\,\sigma^2\,g''(\theta)\,\chi^2_1,$$

where $\chi^2_1$ is a chi-square random variable with 1 degree of freedom.

**Theorem (multivariate delta method).** Let $T_n$ and $\theta$ be in $\mathbb R^k$ with $\sqrt n\,(T_n - \theta) \xrightarrow{d} N_k(0, \Sigma)$. Let $g : \mathbb R^k \to \mathbb R^m$ be differentiable at $\theta$ with $m \times k$ Jacobian matrix $G = \partial g/\partial\theta^{\mathsf T}$ at $\theta$. Then $\sqrt n\,(g(T_n) - g(\theta)) \xrightarrow{d} N_m(0, G\,\Sigma\,G^{\mathsf T})$.

The variance $g'(\theta)^2\sigma^2$, or $G\Sigma G^{\mathsf T}$, is the asymptotic variance: the variance of the limit law. To use it you replace $\theta$ by $T_n$ and $\sigma^2$ by a consistent estimate. By Slutsky's theorem this does not change the limit if $g'$ is continuous at $\theta$ and $g'(\theta) \ne 0$.

## In plain words

You have an estimate that lands near the true value, with a small bell-shaped error. You feed the estimate into a smooth function. Near the true value the function looks like a straight line, so the output error is the input error times the slope of that line. The output error is still bell-shaped, and its spread is the input spread times the size of the slope.

When the slope at the true value is zero, the straight line is flat, and the first-order rule gives no error at all. The curve then takes over, the error becomes much smaller, and it is no longer bell-shaped.

The rule says what happens in the limit. For a fixed sample size the true spread can be quite different, and the error can be lopsided.

## Proof

**First-order theorem.** Define $h(t) = (g(t) - g(\theta))/(t - \theta)$ for $t \ne \theta$ and $h(\theta) = g'(\theta)$. Differentiability of $g$ at $\theta$ says exactly that $h$ is continuous at $\theta$. For every $t$,

$$g(t) - g(\theta) = h(t)\,(t - \theta).$$

Step 1: $T_n \xrightarrow{p} \theta$. By Step 2 of the proof of Slutsky's theorem, $\sqrt n\,(T_n - \theta)$ is bounded in probability: for each $\eta > 0$ there is $M$ with $P(\sqrt n\,|T_n - \theta| > M) < \eta$ for all large $n$. For $\varepsilon > 0$ and $n > (M/\varepsilon)^2$ we get $P(|T_n - \theta| > \varepsilon) \le P(\sqrt n\,|T_n - \theta| > M) < \eta$.

Step 2: $h(T_n) \xrightarrow{p} g'(\theta)$. Fix $\varepsilon > 0$. By continuity of $h$ at $\theta$ there is $\delta > 0$ with $|h(t) - g'(\theta)| < \varepsilon$ when $|t - \theta| < \delta$. So $P(|h(T_n) - g'(\theta)| \ge \varepsilon) \le P(|T_n - \theta| \ge \delta) \to 0$ by Step 1.

Step 3: $\sqrt n\,(g(T_n) - g(\theta)) = h(T_n)\cdot\sqrt n\,(T_n - \theta)$. The first factor converges in probability to the constant $g'(\theta)$ and the second converges in distribution to $Y$. Part (b) of Slutsky's theorem gives the limit $g'(\theta)\,Y$. If $Y \sim N(0, \sigma^2)$, then $g'(\theta)Y \sim N(0, g'(\theta)^2\sigma^2)$. $\blacksquare$

**Second-order theorem.** Since $g'(\theta) = 0$ and $g''(\theta)$ exists, Taylor's theorem with the Peano remainder gives $g(t) - g(\theta) = (\tfrac12 g''(\theta) + k(t))\,(t - \theta)^2$, where $k(\theta) = 0$ and $k$ is continuous at $\theta$. As in Step 2, $k(T_n) \xrightarrow{p} 0$. Write $W_n = \sqrt n\,(T_n - \theta)/\sigma$, so $W_n \xrightarrow{d} N(0, 1)$, and $W_n^2 \xrightarrow{d} \chi^2_1$ by the continuous mapping theorem with $x \mapsto x^2$. Then $n\,(g(T_n) - g(\theta)) = \sigma^2\,(\tfrac12 g''(\theta) + k(T_n))\,W_n^2$, and part (b) of Slutsky's theorem gives the limit $\tfrac12\sigma^2 g''(\theta)\,\chi^2_1$. $\blacksquare$

**Multivariate theorem.** Differentiability at $\theta$ means $g(t) - g(\theta) = G\,(t - \theta) + r(t)$ with $\|r(t)\|/\|t - \theta\| \to 0$ as $t \to \theta$. Put $q(t) = \|r(t)\|/\|t - \theta\|$ for $t \ne \theta$ and $q(\theta) = 0$; then $q$ is continuous at $\theta$. Step 1 holds in $\mathbb R^k$ with the same proof, so $q(T_n) \xrightarrow{p} 0$, and $\sqrt n\,\|r(T_n)\| = q(T_n)\cdot\sqrt n\,\|T_n - \theta\|$ converges in probability to 0, because the second factor is bounded in probability. Now $\sqrt n\,(g(T_n) - g(\theta)) = G\,\sqrt n\,(T_n - \theta) + \sqrt n\,r(T_n)$. The first term converges in distribution to $G Z$ with $Z \sim N_k(0, \Sigma)$, by the continuous mapping theorem, and $GZ \sim N_m(0, G\Sigma G^{\mathsf T})$. The vector form of Slutsky's theorem adds the second term, which converges in probability to 0. $\blacksquare$

## Consequences

**Asymptotic variance and exact variance.** Let $X_1, \ldots, X_n$ be iid $N(\mu, \sigma^2)$ and $g(t) = t^2$. The delta method gives the asymptotic variance $4\mu^2\sigma^2/n$ for $\bar X^2$. Here the exact variance is known: $\operatorname{Var}(\bar X^2) = 4\mu^2\sigma^2/n + 2\sigma^4/n^2$. The table compares the two in exact rational arithmetic.

| $\mu$ | $\sigma^2$ | $n$ | exact variance | delta method |
|---|---|---|---|---|
| 1 | 1 | 10 | 21/50 | 2/5 |
| 2 | 1 | 10 | 81/50 | 8/5 |
| 1 | 4 | 25 | 432/625 | 16/25 |

The relative error is $\sigma^2/(2n\mu^2)$, so the approximation is poor when $\mu$ is small compared with $\sigma/\sqrt n$. At $\mu = 0$ the slope $g'(0)$ is 0, and the second-order theorem applies: $n\bar X^2/\sigma^2$ is exactly $\chi^2_1$ for every $n$, which agrees with the limit $\tfrac12\sigma^2\cdot 2\cdot\chi^2_1$ for $n\bar X^2$.

**Variance-stabilizing transformations.** If $\sqrt n\,(T_n - \theta) \xrightarrow{d} N(0, v(\theta))$, a function with $g'(\theta) = 1/\sqrt{v(\theta)}$ gives a limit $N(0, 1)$ that does not depend on $\theta$. For a binomial proportion $\hat p$, $v(p) = p(1 - p)$ and $g(p) = \arcsin\sqrt p$ gives $n\operatorname{Var}(g(\hat p)) \to 1/4$. For a Poisson count $X$ with mean $\lambda$, $g(x) = \sqrt x$ gives $\operatorname{Var}(\sqrt X) \to 1/4$ as $\lambda \to \infty$. The exact values, summed over the support, show how slowly the limit can arrive:

| $\lambda$ | 1 | 2 | 5 | 10 | 20 | 100 |
|---|---|---|---|---|---|---|
| $\operatorname{Var}(\sqrt X)$ | 0.4022 | 0.3900 | 0.2861 | 0.2613 | 0.2551 | 0.2510 |

| $n$ | $p = 0.1$ | $p = 0.3$ | $p = 0.5$ |
|---|---|---|---|
| 20 | 0.3865 | 0.2714 | 0.2640 |
| 100 | 0.2608 | 0.2533 | 0.2526 |

The entries of the second table are $n\operatorname{Var}(\arcsin\sqrt{\hat p})$.

**Intervals on a transformed scale.** The delta method with $g(p) = \log(p/(1 - p))$ gives the [standard error](/standard-error/) $1/\sqrt{n\hat p(1 - \hat p)}$ of the sample log odds. A nominal 95% interval for the log odds is $g(\hat p) \pm z_{0.975}\,/\sqrt{n\hat p(1 - \hat p)}$, mapped back to $p$. The table compares its coverage with that of the Wald interval $\hat p \pm z_{0.975}\sqrt{\hat p(1 - \hat p)/n}$. Both columns are exact: they sum binomial probabilities over all outcomes $X = 0, \ldots, n$. For the log odds interval, the outcomes $X = 0$ and $X = n$ count as misses, because the interval is not defined there.

| $n$ | $p$ | log odds interval | Wald interval |
|---|---|---|---|
| 20 | 0.05 | 0.6256 | 0.6389 |
| 20 | 0.2 | 0.9563 | 0.9208 |
| 20 | 0.5 | 0.9586 | 0.9586 |
| 50 | 0.05 | 0.8853 | 0.9199 |
| 50 | 0.1 | 0.9703 | 0.8789 |
| 50 | 0.2 | 0.9507 | 0.9375 |
| 200 | 0.05 | 0.9672 | 0.9256 |
| 200 | 0.1 | 0.9561 | 0.9271 |
| 200 | 0.5 | 0.9440 | 0.9440 |

The theorem proves only that both coverages tend to 0.95 for each fixed $p$ in $(0, 1)$. The numbers in the table are computed, not proved, and they show that the transformation helps for moderate $p$ but cannot repair a sample that has very few successes. The [Wilson score interval](/wilson-score-interval/) does better near the boundary.

**Standard errors of functions of estimators.** Under the conditions of [asymptotic normality of the MLE](/asymptotic-normality-of-mle/), $\sqrt n\,(\hat\theta_n - \theta_0) \xrightarrow{d} N(0, I(\theta_0)^{-1})$, and the multivariate theorem gives the standard error $\sqrt{\nabla g(\hat\theta_n)^{\mathsf T} I(\hat\theta_n)^{-1}\,\nabla g(\hat\theta_n)/n}$ for $g(\hat\theta_n)$. This is the basis of [Wald tests](/wald-test/) for nonlinear functions of parameters, and of the sandwich variance of an [M-estimator](/m-estimator/).

## Tightness

**$g$ must be differentiable at $\theta$.** Let $g(t) = |t|$ and $\theta = 0$, with $\sqrt n\,\bar X \xrightarrow{d} N(0, \sigma^2)$. Then $\sqrt n\,|\bar X| \xrightarrow{d} |N(0, \sigma^2)|$, a half-normal law, not a normal one. The one-sided derivatives exist but differ, and the limit is not of the form $cY$.

**The asymptotic variance is not the limit of the variances.** Let $X_i$ be iid $N(\mu, \sigma^2)$ with $\mu \ne 0$, and $g(t) = 1/t$. The delta method gives $\sqrt n\,(1/\bar X - 1/\mu) \xrightarrow{d} N(0, \sigma^2/\mu^4)$. But $\bar X$ has a positive density at 0, so $\mathrm E|1/\bar X| = \infty$ for every $n$, and $1/\bar X$ has no finite mean or variance at any sample size. The theorem is a statement about convergence in distribution and gives no information about moments. The same problem affects ratio estimators; [Fieller's theorem](/fieller-theorem/) gives exact intervals for a ratio of normal means.

**The second-order limit needs the first derivative to vanish exactly.** If $g'(\theta)$ is small but not zero, the first-order theorem holds, but the normal limit is a poor guide at moderate $n$, as the $\bar X^2$ table shows for small $\mu$.

## History

Error formulas of this kind, which multiply an error variance by a squared derivative, were in use in the theory of errors of observation long before they had a limit theorem behind them. J. L. Doob proved limit theorems of this type for smooth functions of statistics in 1935. Robert Dorfman used the name "δ-method" in a note in the Biometric Bulletin in 1938, and Ver Hoef (2012) traces the history and names Dorfman's note as the first use of the term. Casella and Berger give the first-order, second-order and multivariate forms as Theorems 5.5.24, 5.5.26 and 5.5.28, and van der Vaart gives the general form for maps between Euclidean spaces as Theorem 3.1.

## References
