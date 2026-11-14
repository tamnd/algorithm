---
tag: NMWAP1
kind: definition
slug: bayesian-information-criterion
name: Bayesian information criterion
aliases:
- BIC
- Schwarz criterion
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: "BIC = -2 log L + k log n. It approximates -2 times the log marginal likelihood up to a bounded error, and it picks the true model among a fixed finite list as n grows."
prereqs: [akaike-information-criterion, marginal-likelihood, likelihood-ratio-test]
see_also: [laplace-approximation, bayes-factor, lindley-paradox, bayesian-model-averaging, minimum-description-length, widely-applicable-information-criterion, stepwise-regression, leaps-and-bounds]
sources:
  - paper: doi:10.1214/aos/1176344136
    title: "Gideon Schwarz, Estimating the dimension of a model, Annals of Statistics 6(2), 1978, pp. 461 to 464"
    locator: The whole paper (the criterion log L - (k/2) log n as the leading terms of the log posterior probability of a model, for exponential families)
  - paper: doi:10.1080/01621459.1995.10476572
    title: "Robert E. Kass and Adrian E. Raftery, Bayes factors, Journal of the American Statistical Association 90(430), 1995, pp. 773 to 795"
    locator: Section 4 (the Laplace approximation of the marginal likelihood and the Schwarz criterion, with its O(1) error)
  - paper: doi:10.1080/01621459.1995.10476592
    title: "Robert E. Kass and Larry Wasserman, A reference Bayesian test for nested hypotheses and its relationship to the Schwarz criterion, Journal of the American Statistical Association 90(431), 1995, pp. 928 to 934"
    locator: The whole paper (with the unit-information prior, the Schwarz criterion approximates the log Bayes factor with error O(n^(-1/2)))
  - paper: doi:10.1214/aos/1176350709
    title: "Dominique M. A. Haughton, On the choice of a model to fit data from an exponential family, Annals of Statistics 16(1), 1988, pp. 342 to 355"
    locator: The whole paper (the expansion of the log posterior probability of a model for exponential families and the consistency of BIC)
  - paper: doi:10.1214/aos/1176346522
    title: "Ryuei Nishii, Asymptotic properties of criteria for selection of variables in multiple regression, Annals of Statistics 12(2), 1984, pp. 758 to 765"
    locator: The whole paper (consistency of criteria whose penalty grows to infinity more slowly than n, such as k log n, in normal regression)
  - paper: doi:10.1093/biomet/92.4.937
    title: "Yuhong Yang, Can the strengths of AIC and BIC be shared? A conflict between model identification and regression estimation, Biometrika 92(4), 2005, pp. 937 to 950"
    locator: The whole paper (a consistent criterion such as BIC is not minimax-rate optimal for estimating the regression function)
  - book: isbn:9780521852258
    title: Gerda Claeskens and Nils Lid Hjort, Model Selection and Model Averaging, Cambridge University Press, 2008
    locator: Chapter 3 (the derivation of BIC by the Laplace approximation) and Chapter 4 (consistency of BIC and comparison with AIC)
---

The Bayesian information criterion of a model fitted by maximum likelihood is $\mathrm{BIC} = -2\log L(\hat\theta) + k\log n$, with $k$ estimated parameters and $n$ observations. Schwarz (1978) found it as the part of the log [marginal likelihood](/marginal-likelihood/) of a model that grows with $n$: for regular models, $-\frac12\mathrm{BIC}$ differs from the log marginal likelihood by a term that stays bounded, whatever the prior. So the difference of two BIC values approximates $-2$ times the log [Bayes factor](/bayes-factor/), and the model with the smallest BIC has approximately the largest posterior probability under equal prior weights. Its penalty per parameter, $\log n$, is larger than the 2 of the [Akaike information criterion](/akaike-information-criterion/) once $n \ge 8$. As a result, BIC picks the true model with probability tending to 1 when the true model is in a fixed finite list, but it predicts less well than AIC when no candidate is true.

## Definition

Let $y = (y_1, \dots, y_n)$, let a model have densities $f(y; \theta)$ with $\theta$ in an open subset of $\mathbb R^k$, let $\hat\theta$ be the maximum likelihood estimate and $l(\hat\theta) = \log f(y; \hat\theta)$. Then

$$\mathrm{BIC} = -2\,l(\hat\theta) + k\log n.$$

For a normal linear regression with an $n \times p$ design matrix whose columns include the intercept, coefficient vector $b$ and residual sum of squares RSS, $k = p + 1$ and $\mathrm{BIC} = n\log(2\pi\,\mathrm{RSS}/n) + n + (p + 1)\log n$. Given a prior density $\pi$ on $\theta$, the marginal likelihood of the model is $m(y) = \int f(y; \theta)\pi(\theta)\,d\theta$.

**Facts.**

1. **The Laplace approximation (sketch with conditions).** Assume: the $y_i$ are independent and identically distributed; the log-likelihood is three times continuously differentiable, with third derivatives bounded by $nC$ on a fixed neighborhood of the true $\theta_0$; $\hat J = -\nabla^2 l(\hat\theta)/n$ tends in probability to a positive definite matrix $J$; $\hat\theta \to \theta_0$ in probability; $\pi$ is continuous and positive at $\theta_0$; and for each $\delta > 0$ there is $\varepsilon > 0$ with $\sup_{|\theta - \hat\theta| > \delta}[l(\theta) - l(\hat\theta)] < -n\varepsilon$ with probability tending to 1. Split $m(y)$ into the integral over the ball $|\theta - \hat\theta| \le \delta$ and over the rest. Outside the ball the integrand is at most $e^{l(\hat\theta) - n\varepsilon}$ times $\pi$, exponentially smaller than the main term. Inside, $l(\theta) = l(\hat\theta) - \frac n2(\theta - \hat\theta)^\top\hat J(\theta - \hat\theta) + R$ with $|R| \le nC|\theta - \hat\theta|^3$, since the score is 0 at $\hat\theta$. Put $u = \sqrt n(\theta - \hat\theta)$, so $d\theta = n^{-k/2}du$ and $R = O(|u|^3/\sqrt n)$. The integral is $e^{l(\hat\theta)}n^{-k/2}\int e^{-u^\top\hat Ju/2}\pi(\hat\theta + u/\sqrt n)\,du\,(1 + o_p(1))$, and the Gaussian integral is $(2\pi)^{k/2}\det(\hat J)^{-1/2}\pi(\theta_0)(1 + o_p(1))$. Taking logarithms,

$$\log m(y) = l(\hat\theta) - \frac k2\log n + \underbrace{\log\pi(\hat\theta) + \frac k2\log 2\pi - \frac12\log\det\hat J}_{\text{tends to a constant}} + o_p(1).$$

So $-2\log m(y) = \mathrm{BIC} + O_p(1)$. The $O_p(1)$ term depends on the prior and on $J$ and does not tend to 0. It is small compared with $\log n$, but it is not small in absolute terms. Kass and Raftery (1995, Section 4) give the full statement.

2. **The unit-information prior.** If $\pi$ is normal with mean at the null value and covariance $J^{-1}$ (the information of one observation), the bounded term of Fact 1 nearly cancels in a nested comparison when the estimate is within $O(n^{-1/2})$ of the null value. Kass and Wasserman (1995) showed that the BIC difference then approximates $-2$ times the log Bayes factor with error $O(n^{-1/2})$. This is the prior under which the BIC difference is more than an $O_p(1)$ approximation.
3. **BIC does not overfit in the limit.** Take nested models that differ by $q$ parameters. BIC prefers the larger model exactly when the [likelihood ratio](/likelihood-ratio-test/) statistic $2(l_1 - l_0)$ exceeds $q\log n$. If the smaller model is true and the conditions of [Wilks' theorem](/wilks-theorem/) hold, the statistic tends in law to $\chi^2_q$, a fixed law, while $q\log n \to \infty$. So the probability of choosing the larger model tends to 0. Proof: for any fixed $c$ and all $n$ with $q\log n > c$, $P(2(l_1 - l_0) > q\log n) \le P(2(l_1 - l_0) > c) \to P(\chi^2_q > c)$, and $c$ can be as large as needed.
4. **BIC is consistent.** If the larger model is true with a fixed parameter outside the smaller model, $2(l_1 - l_0)$ grows like $n$ times a positive Kullback-Leibler gap, which beats $q\log n$. With Fact 3, BIC chooses the true model among a fixed finite list with probability tending to 1. The general result needs conditions on the models; Nishii (1984) proved it for normal regression and Haughton (1988) for exponential families. It is cited here, not proved.
5. **The price of consistency.** When the true regression is not in any candidate, the $\log n$ penalty leaves out terms whose effects are small but not zero, and the prediction error of the chosen model is larger than the best possible rate. Yang (2005) showed that no criterion is both consistent, like BIC, and minimax-rate optimal for prediction, like AIC.
6. **What $n$ is.** The derivation needs the information to grow like $n$ times a fixed matrix. For dependent data the right $n$ is not always the number of observations. In a [linear mixed model](/linear-mixed-model/) the information about a variance of group effects grows with the number of groups, not with the number of observations. For censored survival data it grows with the number of events. Different programs make different choices.
7. **Singular models.** In mixtures, factor models and neural networks, $J$ is singular at the true parameter and the Laplace step of Fact 1 fails. The correct penalty there is smaller than $\frac k2\log n$; the [widely applicable information criterion](/widely-applicable-information-criterion/) is designed for that case.

## Examples and non-examples

**An exact case.** Let $y_i$ be normal with mean $\theta$ and variance 1, and give $\theta$ the normal prior with mean 0 and variance $\tau^2 = 1$. Then $l(\theta) = l(\hat\theta) - \frac n2(\theta - \bar y)^2$, and the marginal likelihood is exact:

$$\log m(y) - l(\hat\theta) = -\frac12\log n - \frac12\log\Bigl(\tau^2 + \frac1n\Bigr) - \frac{\bar y^2}{2(\tau^2 + 1/n)}.$$

BIC keeps only $-\frac12\log n$. With $\bar y = 0.5$ held fixed:

| $n$ | $\log m - l(\hat\theta)$ | BIC term $-\frac12\log n$ | error |
|---|---|---|---|
| 10 | -1.3126 | -1.1513 | -0.161 |
| 100 | -2.4313 | -2.3026 | -0.129 |
| 1000 | -3.5793 | -3.4539 | -0.125 |
| $10^6$ | -7.0328 | -6.9078 | -0.125 |

The error tends to $-\frac12\log\tau^2 - \bar y^2/(2\tau^2) = -0.125$, the bounded term of Fact 1. It does not tend to 0. With $\tau^2 = 100$ the limit would be $-2.30$, so the prior matters at every $n$.

**Bayes factor and p-value.** Test $\theta = 0$ against $\theta$ free in the same model, with $z = \sqrt n\,\bar y$ fixed, so $\bar y$ is within $O(n^{-1/2})$ of 0 and the prior is the unit-information prior of Fact 2. The exact Bayes factor $\mathrm{BF}_{10}$ under the prior above and its BIC approximation $\exp(z^2/2 - \frac12\log n)$ are:

| $n$ | $z$ | two-sided p-value | exact $\mathrm{BF}_{10}$ | BIC $\mathrm{BF}_{10}$ |
|---|---|---|---|---|
| 100 | 2 | 0.0455 | 0.721 | 0.739 |
| 100 | 3 | 0.0027 | 8.57 | 9.00 |
| $10^4$ | 2 | 0.0455 | 0.074 | 0.074 |
| $10^4$ | 3 | 0.0027 | 0.900 | 0.900 |

At $n = 10^4$ a result with $p = 0.0455$ gives a Bayes factor of about 13 in favor of $\theta = 0$. This is the [Lindley paradox](/lindley-paradox/): with $n$ large, a fixed p-value is evidence for the null.

**The equivalent test level.** For one added parameter, BIC adds it when $|z| > \sqrt{\log n}$:

| $n$ | 10 | 100 | 1000 | $10^4$ | $10^6$ |
|---|---|---|---|---|---|
| $\sqrt{\log n}$ | 1.517 | 2.146 | 2.628 | 3.035 | 3.717 |
| $P(\chi^2_1 > \log n)$ | 0.129 | 0.032 | 0.0086 | 0.0024 | 0.0002 |

AIC uses the fixed threshold $\sqrt 2 = 1.414$ with level 0.157 at every $n$. At $n = 100$ BIC adds $q = 2, 3, 5$ noise parameters with probabilities 0.0100, 0.0032 and 0.0003.

**Non-example: BIC as the log marginal likelihood.** $-\frac12\mathrm{BIC}$ is not an estimate of $\log m(y)$ in absolute terms; the exact case above is off by 0.125 at every $n$ for one prior and by 2.30 for another. Use BIC to compare models, or use a proper computation of $m(y)$.

**Non-example: comparing a model for $y$ with a model for $\log y$,** or models fitted to different rows. As for AIC, the likelihoods must be of the same data.

## Related definitions

- **[Akaike information criterion](/akaike-information-criterion/).** The same form with penalty $2k$; it targets prediction, while BIC targets the true model.
- **[Marginal likelihood](/marginal-likelihood/) and [Bayes factor](/bayes-factor/).** The exact quantities that BIC approximates; $\exp(-\Delta\mathrm{BIC}/2)$ is the BIC estimate of the Bayes factor, and normalized over a list it gives approximate posterior model probabilities for [Bayesian model averaging](/bayesian-model-averaging/).
- **[Minimum description length](/minimum-description-length/).** The two-part code length of the data has the same leading terms, $-l(\hat\theta) + \frac k2\log n$.
- **[Widely applicable information criterion](/widely-applicable-information-criterion/).** The criterion for singular models and for prediction under the posterior.
- **Model search.** BIC is often the criterion of [stepwise regression](/stepwise-regression/) and of exact subset search by [leaps and bounds](/leaps-and-bounds/).

## References
