---
tag: TPJ777
kind: definition
slug: widely-applicable-information-criterion
name: Widely applicable information criterion
aliases:
- WAIC
- Watanabe-Akaike information criterion
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: An estimate of out-of-sample predictive accuracy for Bayesian models. It is the log pointwise posterior predictive density minus the posterior variance of the log likelihood.
prereqs: [posterior-predictive-distribution, bayesian-inference, kullback-leibler-divergence, cross-validation]
see_also: [pareto-smoothed-importance-sampling-loo, akaike-information-criterion, bayesian-information-criterion, bayes-factor, stacking, posterior-predictive-check, hamiltonian-monte-carlo, deviance-statistic]
sources:
  - paper: "Sumio Watanabe, Asymptotic equivalence of Bayes cross validation and widely applicable information criterion in singular learning theory, Journal of Machine Learning Research 11, 2010"
    title: Watanabe 2010
    locator: pages 3571 to 3594 (the definition of WAIC as the Bayes training loss plus the functional variance over n, and its asymptotic equivalence with Bayes leave-one-out cross-validation; general locator)
  - paper: doi:10.1007/s11222-013-9416-2
    title: "Andrew Gelman, Jessica Hwang and Aki Vehtari, Understanding predictive information criteria for Bayesian models, Statistics and Computing 24(6), 2014"
    locator: the comparison of AIC, DIC, WAIC and leave-one-out cross-validation, the two penalties p_WAIC1 and p_WAIC2, and the deviance scale (general locator)
  - paper: doi:10.1007/s11222-016-9696-4
    title: "Aki Vehtari, Andrew Gelman and Jonah Gabry, Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC, Statistics and Computing 27(5), 2017"
    locator: pages 1413 to 1432 (the estimates from posterior draws, their standard errors, and the cases where WAIC is less reliable than PSIS-LOO; general locator)
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 7, Sections 7.1 and 7.2 (log predictive density, AIC, DIC and WAIC)
  - paper: "Sumio Watanabe, A widely applicable Bayesian information criterion, Journal of Machine Learning Research 14, 2013"
    title: Watanabe 2013
    locator: WBIC, an approximation to the log marginal likelihood that is a different criterion from WAIC (general locator)
---

The widely applicable information criterion (WAIC) estimates how well a fitted Bayesian model will predict new data points from the same source. It takes the log of each point's posterior predictive density, sums over the data, and subtracts a penalty: the sum over the points of the posterior variance of the log likelihood. Watanabe (2010) defined it and proved that it is asymptotically equivalent to Bayesian leave-one-out [cross-validation](/cross-validation/), also for singular models such as mixtures and neural networks where the posterior is not close to normal. It is computed from posterior draws, like [PSIS-LOO](/pareto-smoothed-importance-sampling-loo/), which estimates the same target.

## Definition

Let $y_1, \ldots, y_n$ be the data, $f(y_i \mid \theta)$ the density of one point given the parameter, and $p(\theta \mid y)$ the posterior. Write $\mathbb{E}_{\text{post}}$ and $\mathrm{Var}_{\text{post}}$ for the mean and variance over $\theta \sim p(\theta \mid y)$.

The **target** is the expected log pointwise predictive density for new data $\tilde y_1, \ldots, \tilde y_n$ drawn from the true distribution $q$:

$$\mathrm{elpd} = \sum_{i=1}^n \mathbb{E}_{\tilde y_i \sim q}\big[\log p(\tilde y_i \mid y)\big], \qquad p(\tilde y \mid y) = \mathbb{E}_{\text{post}}\big[f(\tilde y \mid \theta)\big].$$

Up to a term that does not depend on the model, $-\mathrm{elpd}/n$ is the Kullback-Leibler divergence from $q$ to the [posterior predictive distribution](/posterior-predictive-distribution/), so a larger elpd means a predictive closer to the truth.

**WAIC.** With the log pointwise predictive density and the penalty

$$\mathrm{lppd} = \sum_{i=1}^n \log \mathbb{E}_{\text{post}}\big[f(y_i \mid \theta)\big], \qquad p_{\mathrm{WAIC}} = \sum_{i=1}^n \mathrm{Var}_{\text{post}}\big[\log f(y_i \mid \theta)\big],$$

the estimate of elpd is

$$\widehat{\mathrm{elpd}}_{\mathrm{WAIC}} = \mathrm{lppd} - p_{\mathrm{WAIC}}, \qquad \mathrm{WAIC} = -2\, \widehat{\mathrm{elpd}}_{\mathrm{WAIC}}.$$

The factor $-2$ puts WAIC on the deviance scale of AIC, where smaller is better. Watanabe's own definition is per observation and without the $-2$: the Bayes training loss $-\mathrm{lppd}/n$ plus the functional variance $p_{\mathrm{WAIC}}$ divided by $n$. All three scales order models in the same way.

**From draws.** With posterior draws $\theta^{(1)}, \ldots, \theta^{(S)}$, replace $\mathbb{E}_{\text{post}} f(y_i \mid \theta)$ by $\frac1S\sum_s f(y_i \mid \theta^{(s)})$, computed as a log-sum-exp, and $\mathrm{Var}_{\text{post}}$ by the sample variance of $\log f(y_i \mid \theta^{(s)})$. The standard error of $\widehat{\mathrm{elpd}}_{\mathrm{WAIC}}$ is $\sqrt n$ times the standard deviation of the $n$ pointwise terms. The function `waic` of the [PSIS-LOO](/pareto-smoothed-importance-sampling-loo/) implementation computes exactly this.

**Effective number of parameters.** $p_{\mathrm{WAIC}}$ plays the role of the parameter count $k$ in AIC. An older form, $p_{\mathrm{WAIC1}} = 2\sum_i\big(\log \mathbb{E}_{\text{post}} f(y_i \mid \theta) - \mathbb{E}_{\text{post}} \log f(y_i \mid \theta)\big)$, has the same limit in regular models; Gelman, Hwang and Vehtari (2014) recommend the variance form.

**What is proved and what is not.** Watanabe (2010) proved that the expectation of WAIC over data sets equals that of the generalization loss up to $o(1/n)$, and that WAIC and Bayesian leave-one-out cross-validation differ by $o_p(1/n)$ per observation, under conditions that include singular models. These are asymptotic results. For a given finite data set, WAIC is an estimate whose error is only measured, and Vehtari, Gelman and Gabry (2017) found that it is less reliable than PSIS-LOO when some observations are very influential.

## Examples and non-examples

**Example: a normal mean, exact.** Let $y = (0.5, 1, 2, 2.5, 4)$, $f(y_i \mid \theta) = N(y_i; \theta, 1)$ and a flat prior on $\theta$. The posterior is $N(\bar y, v)$ with $\bar y = 2$ and $v = 1/n = 0.2$. Write $d_i = y_i - \bar y$, so $\sum_i d_i^2 = 7.5$.

- The posterior predictive of a point is $N(\bar y, 1 + v)$, so $\mathrm{lppd} = \sum_i \big(-\tfrac12\log(2\pi \cdot 1.2) - d_i^2/2.4\big) = -8.1755$.
- Since $y_i - \theta = d_i - e$ with $e \sim N(0, v)$, $\mathrm{Var}_{\text{post}}\big[(y_i - \theta)^2/2\big] = d_i^2 v + v^2/2$. The pointwise penalties are $0.47, 0.22, 0.02, 0.07, 0.82$, and $p_{\mathrm{WAIC}} = n v^2/2 + v\sum_i d_i^2 = 0.1 + 1.5 = 1.6$.
- So $\widehat{\mathrm{elpd}}_{\mathrm{WAIC}} = -9.7755$ and $\mathrm{WAIC} = 19.551$.

The exact leave-one-out value is $\sum_i \log N(y_i; \bar y_{-i}, 1 + 1/(n - 1)) = -9.8401$, close to WAIC. The outlying point $y_5 = 4$ carries the largest penalty. With $S = 1000$, $4000$ and $16000$ posterior draws from `random.Random(1)`, the estimates from draws are $-9.7808$, $-9.7489$ and $-9.7506$; the Monte Carlo error is in the penalty, not in the lppd.

**Example: the penalty tracks the fit of the model.** In the same model with $v = 1/n$, the expected penalty over data sets is about $1$, the number of parameters, when the data really have variance 1. If the data have variance 4, the model's likelihood is too narrow and $p_{\mathrm{WAIC}}$ goes to about $4$; for $n = 200$ points drawn by `random.Random(5)` it is $1.26$ for variance 1 and $5.04$ for variance 4. AIC would still charge $1$. This is the case where the posterior variance penalty, like Takeuchi's criterion, is the more honest one.

**Non-example: AIC.** AIC $= -2\log f(y \mid \hat\theta) + 2k$ uses the maximum likelihood plug-in, not the posterior, and the count $k$, not a variance. In the example, $\log f(y \mid \hat\theta) = -8.3447$ and $\mathrm{AIC} = 18.689$. AIC estimates the predictive accuracy of the plug-in density $f(\cdot \mid \hat\theta)$; WAIC estimates that of the posterior predictive. See [Akaike information criterion](/akaike-information-criterion/).

**Non-example: BIC.** $\mathrm{BIC} = -2\log f(y \mid \hat\theta) + k \log n$ approximates $-2\log m(x)$, the log [marginal likelihood](/marginal-likelihood/). Its target is the posterior probability of a model, not predictive accuracy, and its penalty grows with $n$. See [Bayesian information criterion](/bayesian-information-criterion/). Watanabe's WBIC (2013) is the singular-model counterpart of BIC and is a different criterion from WAIC.

**Non-example: DIC.** The deviance information criterion plugs in the posterior mean, $-2\log f(y \mid \bar\theta) + 2p_D$ with $p_D = 2\big(\log f(y \mid \bar\theta) - \mathbb{E}_{\text{post}}\log f(y \mid \theta)\big)$. It uses the joint likelihood of all the data, not a sum of pointwise terms, and it is not invariant to reparametrization. In the example $p_D = 1.0$ and $p_{\mathrm{WAIC1}} = 1.338$, against $p_{\mathrm{WAIC}} = 1.6$.

**Non-example: the Bayes factor.** A [Bayes factor](/bayes-factor/) compares how well models predicted all the data from the prior. WAIC compares how well they predict each point from the posterior. A Bayes factor changes without limit as a prior becomes more diffuse; WAIC changes very little.

## Related definitions

- **[PSIS-LOO](/pareto-smoothed-importance-sampling-loo/).** Estimates the same elpd by importance sampling for each left-out point, and its $\hat k$ values flag the points where the estimate is unreliable. WAIC has no such diagnostic.
- **[Cross-validation](/cross-validation/).** Exact leave-one-out cross-validation refits the model $n$ times. WAIC and PSIS-LOO are two ways to avoid that.
- **[Akaike information criterion](/akaike-information-criterion/).** The plug-in, regular-model ancestor. In a regular model with a weak prior and much data, $p_{\mathrm{WAIC}} \to k$ when the model is correct and WAIC is close to AIC.
- **[Bayesian information criterion](/bayesian-information-criterion/).** A different target: model probability rather than prediction.
- **[Deviance statistic](/deviance-statistic/).** WAIC on the $-2$ scale is a penalized deviance.
- **[Stacking](/stacking/).** Uses pointwise predictive densities like those of WAIC or PSIS-LOO to choose weights for combining models.
- **[Posterior predictive check](/posterior-predictive-check/).** Asks whether the data look like draws from the predictive, not how well the model will predict new data.

## References
