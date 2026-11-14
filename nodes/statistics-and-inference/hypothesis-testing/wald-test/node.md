---
tag: QP1T8S
kind: algorithm
slug: wald-test
name: Wald test
aliases:
- Wald chi-squared test
area: statistics-and-inference/hypothesis-testing
level: core
summary: Tests a parameter by the squared distance of its estimate from the null value, scaled by the estimated variance. It needs only the unrestricted fit.
model: real-ram
complexity:
  vars: {n: the number of observations, r: the number of parameters tested}
  time: {worst: Θ(n + r^3), best: Θ(n + r^3)}
  space: {extra: Θ(r^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1943
  people: [Abraham Wald]
  note: Wald proposed the statistic in 1943 as a large-sample test of a general hypothesis from the unrestricted maximum likelihood estimate and proved its asymptotic optimality.
prereqs: [statistical-hypothesis-test, p-value, maximum-likelihood-estimation, fisher-information-matrix, asymptotic-normality-of-mle]
see_also: [likelihood-ratio-test, score-test, wilks-theorem, standard-error, delta-method, wilson-score-interval, heteroscedasticity-consistent-standard-errors, logistic-regression]
sources:
  - paper: doi:10.1090/S0002-9947-1943-0012401-3
    title: Abraham Wald, Tests of statistical hypotheses concerning several parameters when the number of observations is large, Transactions of the American Mathematical Society 54(3) (1943), pages 426 to 482
    locator: the statistic built from the unrestricted maximum likelihood estimate and its asymptotic chi-squared law
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 10.3.2 (other large-sample tests, with the Wald statistic)
  - paper: doi:10.1080/01621459.1977.10479969
    title: Walter W. Hauck and Allan Donner, Wald's test as applied to hypotheses in logit analysis, Journal of the American Statistical Association 72(360) (1977), pages 851 to 853
    locator: the Wald statistic of a logistic coefficient falls to 0 as the coefficient grows
  - paper: doi:10.2307/1914072
    title: E. R. Berndt and N. E. Savin, Conflict among criteria for testing hypotheses in the multivariate linear regression model, Econometrica 45(5) (1977), pages 1263 to 1277
    locator: the inequality W >= LR >= LM in the normal linear model
---

The Wald test checks a null value $\theta_0$ by asking how many standard errors the [maximum likelihood estimate](/maximum-likelihood-estimation/) $\hat\theta$ is from it. For one parameter its statistic is $W = (\hat\theta - \theta_0)^2/\widehat{\operatorname{Var}}(\hat\theta)$, the square of the familiar "estimate over standard error" ratio; for $r$ parameters it is the quadratic form $W = (\hat\theta - \theta_0)^\top \hat V^{-1}(\hat\theta - \theta_0)$. It needs only the unrestricted fit, which is why regression software prints a Wald z or chi-squared value next to every coefficient. Its null distribution is $\chi^2_r$ only in the limit, it is not invariant under a change of parameter, and in some models it can fall as the evidence grows.

## In plain words

Fit the model once, with every setting free, and get an estimate and its standard error. Ask how far the estimate is from the claimed value, counted in standard errors. Square that count. If the claim is true and the sample is large, this squared count behaves like a square of a standard normal number, so values above about 3.84 happen only 5% of the time. If several settings are tested together, the same idea uses the joint spread of the estimates. The test is cheap, because it never fits the model under the claim. The price is that the answer depends on the scale in which the setting is written.

## The problem

**Model and hypotheses.** The data $x_1, \dots, x_n$ are iid with density $f(x; \theta)$, $\theta \in \Theta \subseteq \mathbb R^k$. The null hypothesis fixes $r$ coordinates, $H_0: \theta_{(1)} = \theta_0$ with $\theta_{(1)} \in \mathbb R^r$, and leaves the other $k - r$ coordinates free. The alternative is $\theta_{(1)} \ne \theta_0$. A general smooth restriction $h(\theta) = 0$ works the same way with $h(\hat\theta)$ and its [delta method](/delta-method/) covariance $H\hat V H^\top$.

**Statistic.** With $\hat\theta$ the unrestricted MLE and $\hat V$ a consistent estimate of the covariance of its first $r$ coordinates,
$$W = (\hat\theta_{(1)} - \theta_0)^\top \hat V^{-1} (\hat\theta_{(1)} - \theta_0).$$
The usual $\hat V$ is the $r \times r$ block of $I_n(\hat\theta)^{-1}$, the inverse of the expected [Fisher information](/fisher-information-matrix/) $I_n = nI$, or of the observed information $-\nabla^2 \ell(\hat\theta)$. For one parameter, $W = z^2$ with $z = (\hat\theta - \theta_0)/\widehat{\mathrm{se}}$.

**Null distribution.** Asymptotic. Under $H_0$ and the conditions of the [asymptotic normality of the MLE](/asymptotic-normality-of-mle/), $\sqrt n(\hat\theta - \theta) \to N(0, I(\theta)^{-1})$, and $n\hat V \to$ the matching block of $I(\theta)^{-1}$ in probability, so $W \to \chi^2_r$ in distribution. It is exact only when $\hat\theta$ is exactly normal with a known covariance, as for a normal mean with known $\sigma$.

**Rejection rule and size.** Reject at level $\alpha$ when $W \ge \chi^2_{r, 1-\alpha}$. For one parameter this is $|z| \ge z_{1-\alpha/2}$. The size tends to $\alpha$, and for finite $n$ it can be well above $\alpha$.

**p-value.** $p = P(\chi^2_r \ge W) = Q(r/2, W/2)$.

**Sensitivity and power.** Under local alternatives $\theta_{(1)} = \theta_0 + h/\sqrt n$, $W$ tends to a noncentral $\chi^2_r$ with noncentrality $h^\top (I^{-1})_{11}^{-1} h$, the same limit as the [likelihood ratio test](/likelihood-ratio-test/) and the [score test](/score-test/). Far from the null the three differ, and the Wald test can lose power badly (the Hauck-Donner effect below).

## The algorithm

```pseudo id=main
WALD-TEST(θ̂, θ₀, V̂)        ▷ θ̂, θ₀ ∈ ℝ^r; V̂ an r × r estimate of Cov(θ̂), positive definite
L1  d ← θ̂ − θ₀
L2  solve V̂ y = d for y        ▷ Gaussian elimination or Cholesky; never form V̂⁻¹
L3  W ← dᵀ y
L4  p ← Q(r/2, W/2)             ▷ P(χ²_r ≥ W), the upper tail directly
L5  return (W, p)
```

The input comes from one fit: $\hat\theta$ from the MLE, and $\hat V$ from the inverse information at $\hat\theta$, or from a sandwich estimate when the model may be wrong. For the common one-parameter models the steps reduce to closed forms:

| model, null | $\hat\theta$ | $\widehat{\operatorname{Var}}(\hat\theta)$ | $W$ |
|---|---|---|---|
| binomial, $p = p_0$ | $\hat p = k/n$ | $\hat p(1 - \hat p)/n$ | $n(\hat p - p_0)^2/(\hat p(1 - \hat p))$ |
| binomial, log odds $\beta = \beta_0$ | $\hat\beta = \log(k/(n - k))$ | $1/(n\hat p(1 - \hat p))$ | $(\hat\beta - \beta_0)^2 n\hat p(1 - \hat p)$ |
| Poisson, $\lambda = \lambda_0$ | $\hat\lambda = \bar x$ | $\hat\lambda/n$ | $n(\hat\lambda - \lambda_0)^2/\hat\lambda$ |
| normal, $\mu = \mu_0$, $\sigma$ known | $\bar x$ | $\sigma^2/n$ | $n(\bar x - \mu_0)^2/\sigma^2$ |
| normal, $\mu = \mu_0$, $\sigma$ unknown | $\bar x$ | $\hat\sigma^2/n$, $\hat\sigma^2 = SS/n$ | $n^2(\bar x - \mu_0)^2/SS$ |

When $\hat p \in \{0, 1\}$ or $\hat\lambda = 0$, the estimated variance is 0, and the implementation returns $W = \infty$ and $p = 0$. This is a known defect of the test: one sample with no successes "proves" that $p \ne p_0$ for every $p_0$. On the log odds scale the MLE does not exist at all in that case, and the implementation raises an error.

## Example

**A binomial count.** In 20 trials there are 15 successes, and $H_0: p = 0.5$.

| step | value |
|---|---|
| $\hat p$, $\widehat{\operatorname{Var}}(\hat p) = 0.75 \cdot 0.25/20$ | 0.75, 0.009375 |
| L1: $d = 0.75 - 0.5$ | 0.25 |
| L2: $y = d/0.009375$ | 26.6667 |
| L3: $W = d\,y$ | 6.6667 |
| L4: $p = P(\chi^2_1 \ge 6.6667)$ | 0.00982 |

The same data give $\Lambda = 5.2325$ ($p = 0.0222$) for the likelihood ratio test and $S = 5.0$ ($p = 0.0253$) for the score test. All three reject at 5%, but the Wald p-value is less than half of the others. On the log odds scale, $\hat\beta = \log 3 = 1.0986$, $\widehat{\operatorname{Var}} = 1/(20 \cdot 0.75 \cdot 0.25) = 0.2667$, and $W = 4.5261$ ($p = 0.0334$). The data and the null are the same, but the Wald statistic changed from 6.67 to 4.53 because the parameter was written differently.

**Two parameters.** For the nine pack weights of the [z-test](/z-test/) page, $\bar x = 502.7778$ and $\hat\sigma^2 = SS/9 = 8.3951$. At the MLE the inverse information is diagonal, with entries $\hat\sigma^2/n$ and $2\hat\sigma^4/n$. For $H_0: (\mu, \sigma^2) = (500, 16)$,
$$W = \frac{9(2.7778)^2}{8.3951} + \frac{9(8.3951 - 16)^2}{2(8.3951)^2} = 8.2721 + 3.6928 = 11.9649,$$
with $r = 2$ and $p = 0.00252$. The first term alone, $8.2721$ ($p = 0.0040$), is the Wald test of $\mu = 500$ with $\sigma$ free. The exact t-test of the same null gives $p = 0.0266$, so here the Wald p-value is too small by a factor of more than 6.

**The Hauck-Donner effect.** Keep $n = 20$ and $H_0: p = 0.5$, but test it on the log odds scale, $H_0: \beta = 0$, as a logistic regression with only an intercept does. As the number of successes $k$ grows, the evidence against $H_0$ grows, and the likelihood ratio statistic grows with it. The Wald statistic does not:

| $k$ | 15 | 16 | 17 | 18 | 19 |
|---|---|---|---|---|---|
| Wald $W$ (log odds) | 4.53 | 6.15 | 7.67 | 8.69 | 8.24 |
| likelihood ratio $\Lambda$ | 5.23 | 7.71 | 10.82 | 14.72 | 19.79 |

The Wald statistic is largest at $k = 18$ and falls after it. As $\hat p \to 1$, $\hat\beta^2 n\hat p(1 - \hat p) \to 0$, and at $k = 20$ the MLE of $\beta$ does not exist.

## Correctness

Line L2 solves $\hat V y = d$, so $y = \hat V^{-1}d$ and line L3 returns $d^\top \hat V^{-1} d$, which is $\ge 0$ when $\hat V$ is positive definite. The table follows from the explicit MLEs and their inverse informations. Under $H_0$, asymptotic normality of the MLE gives $\sqrt n(\hat\theta_{(1)} - \theta_0) \to N(0, \Sigma)$ with $\Sigma$ positive definite, and $n\hat V \to \Sigma$ in probability; by [Slutsky's theorem](/slutsky-theorem/) $W \to Z^\top Z$ with $Z \sim N(0, I_r)$, which is $\chi^2_r$. So the size of "reject when $p \le \alpha$" tends to $\alpha$. This is proved. The finite-sample sizes below are only measured, by exact enumeration. The correctness proof gives each step.

## Complexity

On a [real RAM](/real-ram/), the closed forms need one pass over the data, $\Theta(n)$ time and $\Theta(1)$ extra space. The matrix form needs $\Theta(r^3)$ time and $\Theta(r^2)$ space for the solve in line L2, after a fit that is not part of the test. In practice the cost of the Wald test is the one unrestricted fit; the likelihood ratio test needs that fit and a second one under $H_0$.

**Numerical stability.** Line L2 solves a linear system and does not invert $\hat V$. Solving with [Cholesky](/cholesky-decomposition/) or [Gaussian elimination](/gaussian-elimination/) with partial pivoting is backward stable, while forming $\hat V^{-1}$ first and then multiplying adds error for no gain. When $\hat V$ is close to singular, for example with nearly collinear regressors, $W$ is sensitive to small errors in $\hat V$: its relative error is of order the condition number of $\hat V$ times the unit roundoff. The implementation stops with an error when a pivot is exactly 0 and when $W < 0$, which shows that $\hat V$ is not positive definite. Line L4 computes the upper tail directly, so tiny p-values do not round to 0.

## Properties

- **One fit.** Only the unrestricted MLE is needed. This makes it the default for many coefficients at once: each coefficient gets its own Wald z from the same fit.
- **Asymptotically $\chi^2_r$, and equivalent to the LR and score tests.** Under $H_0$ and local alternatives, the three statistics differ by $o_p(1)$.
- **Not invariant under reparametrization.** $W$ for $p = 0.5$ and for $\log(p/(1 - p)) = 0$ differ, as the example shows. The likelihood ratio and score tests do not have this defect (the score test is invariant when the information is expected).
- **Ordered in the normal linear model.** For linear restrictions on the mean of a normal linear model with unknown variance, $W \ge \Lambda \ge S$, so the Wald test rejects most often (Berndt and Savin 1977). For a normal mean, with $u = T^2/(n - 1)$, the three are $nu$, $n\log(1 + u)$ and $nu/(1 + u)$.
- **Liberal in small samples.** In the normal mean model the exact size of the nominal 5% Wald test is $0.155$ at $n = 5$, $0.096$ at $n = 10$, $0.071$ at $n = 20$ and $0.058$ at $n = 50$ (computed from the t distribution; the LRT has $0.098$, $0.070$, $0.059$, $0.054$ and the score test $0.022$, $0.042$, $0.047$, $0.049$).
- **Gives an interval directly.** Inverting the test gives $\hat\theta \pm z_{1-\alpha/2}\,\widehat{\mathrm{se}}$, the Wald interval.

## Variants and improvements

- **Wald z and Wald interval.** For one parameter, report $z = (\hat\theta - \theta_0)/\widehat{\mathrm{se}}$ and the interval $\hat\theta \pm z_{1-\alpha/2}\widehat{\mathrm{se}}$. For a binomial proportion this interval has poor coverage: with $n = 20$ the exact coverage of the nominal 95% interval is $0.959$ at $p = 0.5$, $0.895$ at $p = 0.75$ and $0.639$ at $p = 0.95$. The [Wilson score interval](/wilson-score-interval/), which inverts the score test, is much better.
- **Observed or expected information.** Both give the same limit. The observed information is often more accurate in finite samples, and the two agree in exponential families with the natural parameter.
- **Sandwich covariance.** Replace $I_n^{-1}$ by $A^{-1}BA^{-1}$, with $A$ the observed information and $B$ the outer product of the per-observation scores. The test is then valid when the model is wrong but the estimating equation is right. See [heteroscedasticity-consistent standard errors](/heteroscedasticity-consistent-standard-errors/) and [cluster-robust standard errors](/cluster-robust-standard-errors/).
- **Nonlinear restrictions.** For $H_0: h(\theta) = 0$, use $W = h(\hat\theta)^\top (H\hat V H^\top)^{-1} h(\hat\theta)$ with $H$ the Jacobian of $h$. The value depends on how the restriction is written: $\theta_1\theta_2 = 1$ and $\theta_1 = 1/\theta_2$ give different $W$.
- **F form.** In the normal linear model with unknown variance, $W/r$ with the unbiased variance estimate has an exact $F_{r, n-k}$ law; this is the [regression F-test](/regression-f-test/).
- **Choosing the scale.** Compute $W$ on a scale where $\hat\theta$ is closer to normal, such as the log of a rate or the log odds near the middle, and transform the interval back.

## When to use it

Use the Wald test when only the unrestricted model is fitted or easy to fit, and the sample is large compared with the number of parameters: reading coefficient tables, testing a few coefficients of a large regression, or building quick intervals. Prefer the likelihood ratio test when both fits are cheap, when the estimate is near the edge of the parameter space, or when the parameter has no natural scale. Prefer the score test when the full model is expensive or fails to converge, as when screening many candidate terms. For small samples use an exact test.

## Pitfalls

- **The Hauck-Donner effect.** For a logistic coefficient, the Wald statistic first rises and then falls as the estimate grows, because the standard error grows faster than the estimate (the last example). In logistic regression with separated or nearly separated data, a large and real effect can have a small Wald z. Use the likelihood ratio test there.
- **Zero variance estimates.** With $\hat p = 0$ the plug-in variance is 0 and $W = \infty$ for every $p_0$. Use the score test or an exact test.
- **Different answers for the same hypothesis.** The parametrization and the form of a nonlinear restriction change $W$. Report the scale used.
- **Reading the Wald p-value as exact.** It is liberal in small samples, as the size table shows.
- **Ignoring the covariance.** Testing two coefficients jointly needs the full $2 \times 2$ block of $\hat V$; two separate z-tests are not the same test.

## Implementations

## History

Abraham Wald introduced the test in a long paper in the Transactions of the American Mathematical Society in 1943, where he proved that the statistic built from the unrestricted MLE has a chi-squared limit and that tests based on it have the best average power over certain families of alternatives, among tests based on large samples. The likelihood ratio statistic of Neyman and Pearson (1928) and Wilks (1938) and the score statistic of Rao (1948) complete what is now called the trinity of classical tests. Hauck and Donner (1977) showed the loss of power in logit models, and Berndt and Savin (1977) proved the ordering $W \ge \Lambda \ge S$ in normal linear models. The general use of robust sandwich covariances in Wald tests comes from the work of Huber (1967) and White (1980).

## References
