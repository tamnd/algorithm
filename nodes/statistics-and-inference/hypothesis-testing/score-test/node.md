---
tag: 6H761T
kind: algorithm
slug: score-test
name: Score test
aliases:
- Rao score test
- Lagrange multiplier test
area: statistics-and-inference/hypothesis-testing
level: core
summary: Tests a null by the size of the score at the restricted estimate, scaled by the Fisher information. It needs only the fit under the null.
model: real-ram
complexity:
  vars: {n: the number of observations, k: the number of parameters, m: the number of cells of a multinomial}
  time: {worst: Θ(n + m + k^3), best: Θ(n + m + k^3)}
  space: {extra: Θ(k^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1948
  people: [C. R. Rao]
  note: Rao proposed the test in 1948, using the score and the information at the null value. Aitchison and Silvey (1958) and Silvey (1959) derived it from the Lagrange multiplier of the restricted maximization, which gave its second name.
prereqs: [statistical-hypothesis-test, p-value, score-function, fisher-information-matrix, maximum-likelihood-estimation]
see_also: [likelihood-ratio-test, wald-test, wilks-theorem, wilson-score-interval, chi-squared-goodness-of-fit-test, lagrange-multiplier, log-rank-test, breusch-pagan-test]
sources:
  - paper: doi:10.1017/S0305004100023987
    title: C. R. Rao, Large sample tests of statistical hypotheses concerning several parameters with applications to problems of estimation, Proceedings of the Cambridge Philosophical Society 44(1) (1948), pages 50 to 57
    locator: the score statistic for simple and composite hypotheses
  - paper: doi:10.1214/aoms/1177706538
    title: J. Aitchison and S. D. Silvey, Maximum-likelihood estimation of parameters subject to restraints, Annals of Mathematical Statistics 29(3) (1958), pages 813 to 828
    locator: the Lagrange multipliers of the restricted MLE and their asymptotic distribution
  - paper: doi:10.1214/aoms/1177706259
    title: S. D. Silvey, The Lagrangian multiplier test, Annals of Mathematical Statistics 30 (1959), pages 389 to 407
    locator: the test based on the Lagrange multipliers and its equivalence with the score test
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 10.3.2 (other large-sample tests, with the score statistic)
---

The score test asks whether the log-likelihood is still climbing at the null value. If $H_0$ is true, the slope of the log-likelihood, the [score](/score-function/) $U_n(\theta)$, should be near 0 at the best fit under $H_0$; a large slope says that the data pull the parameter away from the null. The statistic is $S = U_n(\tilde\theta_0)^\top I_n(\tilde\theta_0)^{-1} U_n(\tilde\theta_0)$, the squared score in the metric of the [Fisher information](/fisher-information-matrix/), where $\tilde\theta_0$ is the MLE under $H_0$. It needs only the fit under the null, so it is the cheap test when the full model is hard to fit. Its null distribution is $\chi^2_r$ only in the limit. Many classical tests are score tests: the one-proportion z-test, Pearson's chi-squared test, the log-rank test and the Breusch-Pagan test.

## In plain words

Fit the model under the claim, holding the claimed settings fixed. Then ask: if you were allowed to move those settings a little, how steeply would the fit improve? A steep slope means the claim sits on the side of a hill, away from where the data want to be. Measure the slope in units of its natural spread, square it, and compare with a standard table that depends on the number of fixed settings. You never fit the bigger model. That is the main reason to use this test: it lets you check many possible extensions of a simple model, each at the cost of one slope.

## The problem

**Model and hypotheses.** The data $x_1, \dots, x_n$ are iid with density $f(x; \theta)$, $\theta \in \Theta \subseteq \mathbb R^k$. The null hypothesis fixes $r$ coordinates, $H_0: \theta_{(1)} = \theta_0$, and leaves $k - r$ nuisance coordinates free, or more generally imposes $r$ smooth restrictions $h(\theta) = 0$.

**Statistic.** Let $\tilde\theta_0$ be the MLE under $H_0$, $U_n(\theta) = \nabla\ell(\theta)$ the score of the sample and $I_n(\theta) = nI(\theta)$ the expected Fisher information. Then
$$S = U_n(\tilde\theta_0)^\top I_n(\tilde\theta_0)^{-1} U_n(\tilde\theta_0).$$
The score for the nuisance coordinates is 0 at $\tilde\theta_0$, because $\tilde\theta_0$ maximizes over them; only the $r$ tested coordinates contribute, through the matching block of $I_n^{-1}$. For one parameter and a simple null, $S = U_n(\theta_0)^2/I_n(\theta_0)$.

**Null distribution.** Asymptotic. Under $H_0$, $U_n(\theta)/\sqrt n \to N(0, I(\theta))$ by the [central limit theorem](/central-limit-theorem/), since the score is a sum of iid terms with mean 0 and variance $I(\theta)$. So $S \to \chi^2_r$. For a simple null this needs only the moment conditions of the score; with nuisance parameters it needs the conditions of the [asymptotic normality of the MLE](/asymptotic-normality-of-mle/) for $\tilde\theta_0$.

**Rejection rule and size.** Reject at level $\alpha$ when $S \ge \chi^2_{r, 1-\alpha}$. For one parameter one can also use the signed root $U_n/\sqrt{I_n}$ against $N(0, 1)$, which gives one-sided tests. The size tends to $\alpha$.

**p-value.** $p = P(\chi^2_r \ge S) = Q(r/2, S/2)$.

**Sensitivity and power.** Under local alternatives $\theta_{(1)} = \theta_0 + h/\sqrt n$, $S$ tends to the same noncentral $\chi^2_r$ as the [Wald test](/wald-test/) and the [likelihood ratio test](/likelihood-ratio-test/). For a one-sided alternative in a one-parameter family, the test based on $U_n(\theta_0)$ is locally most powerful: it has the largest slope of the power function at $\theta_0$ among tests of size $\alpha$. Far from the null, the score test can lose power, because the information at $\theta_0$ may not describe the data well there.

## The algorithm

```pseudo id=main
SCORE-TEST(x, U, I, Θ₀, r)        ▷ U(θ): score vector; I(θ): Fisher information of the sample
L1  θ̃₀ ← a maximizer of ℓ(θ; x) over Θ₀       ▷ the only fit
L2  u ← U(θ̃₀)                                  ▷ 0 in the nuisance coordinates
L3  J ← I(θ̃₀)
L4  solve J y = u for y                          ▷ never form J⁻¹
L5  S ← uᵀ y
L6  p ← Q(r/2, S/2)                              ▷ P(χ²_r ≥ S), the upper tail directly
L7  return (S, p)
```

For the common models the steps reduce to closed forms, all of them at the null value:

| model, null | $U_n(\theta_0)$ | $I_n(\theta_0)$ | $S$ |
|---|---|---|---|
| binomial, $p = p_0$ | $(k - np_0)/(p_0(1 - p_0))$ | $n/(p_0(1 - p_0))$ | $(k - np_0)^2/(np_0(1 - p_0))$ |
| Poisson, $\lambda = \lambda_0$ | $(t - n\lambda_0)/\lambda_0$, $t = \sum x_i$ | $n/\lambda_0$ | $(t - n\lambda_0)^2/(n\lambda_0)$ |
| normal, $\mu = \mu_0$, $\sigma$ known | $n(\bar x - \mu_0)/\sigma^2$ | $n/\sigma^2$ | $n(\bar x - \mu_0)^2/\sigma^2$ |
| normal, $\mu = \mu_0$, $\sigma$ unknown | $n(\bar x - \mu_0)/\tilde\sigma_0^2$ | $n/\tilde\sigma_0^2$ | $n^2(\bar x - \mu_0)^2/\sum(x_i - \mu_0)^2$ |
| multinomial, probabilities $q_j$ | $O_j/q_j - O_m/q_m$, $j < m$ | $n(\operatorname{diag}(1/q_j) + \mathbf 1\mathbf 1^\top/q_m)$ | $\sum_j (O_j - nq_j)^2/(nq_j)$ |

In the fourth row, $\tilde\sigma_0^2 = \sum(x_i - \mu_0)^2/n$ is the MLE of $\sigma^2$ under $H_0$, and $S = nT^2/(n - 1 + T^2)$ in terms of the t statistic $T$. In the last row, the score test is exactly Pearson's chi-squared statistic, as the correctness proof shows.

**Why it is also called the Lagrange multiplier test.** Maximize $\ell(\theta)$ subject to $h(\theta) = 0$ with a [Lagrange multiplier](/lagrange-multiplier/) $\lambda$. At the restricted maximum, $\nabla\ell(\tilde\theta_0) = H(\tilde\theta_0)^\top\tilde\lambda$, where $H$ is the Jacobian of $h$. The multiplier $\tilde\lambda$ is the price of the constraint: the rate at which the maximum log-likelihood would rise if the constraint were relaxed. A test that rejects when $\tilde\lambda$ is large, in the metric of its asymptotic covariance, is the Lagrange multiplier test of Aitchison and Silvey (1958) and Silvey (1959). Because $U_n(\tilde\theta_0) = H^\top\tilde\lambda$, its statistic is the same number $S$. Econometrics uses the name "LM test"; statistics uses "score test".

## Example

**A binomial count.** In 20 trials there are 15 successes, and $H_0: p = 0.5$.

| step | value |
|---|---|
| L1: $\tilde\theta_0 = p_0$ (simple null, nothing to fit) | 0.5 |
| L2: $u = (15 - 10)/0.25$ | 20 |
| L3: $J = 20/0.25$ | 80 |
| L4: $y = 20/80$ | 0.25 |
| L5: $S = u\,y$ | 5.0 |
| L6: $p = P(\chi^2_1 \ge 5)$ | 0.02535 |

This is the square of the z statistic $(15 - 10)/\sqrt{20 \cdot 0.25} = 2.2361$ of the one-proportion [z-test](/z-test/). The Wald test gives $W = 6.67$ and the likelihood ratio test $\Lambda = 5.23$. Inverting the score test, the values $p_0$ that it does not reject at 5% form the interval $(0.5313, 0.8881)$, which is the [Wilson score interval](/wilson-score-interval/).

**A normal mean with unknown variance.** For the nine pack weights of the z-test page and $H_0: \mu = 500$, line L1 fits $\sigma^2$ with $\mu$ held at 500: $\tilde\sigma_0^2 = \sum(x_i - 500)^2/9 = 145/9 = 16.1111$. The score for $\mu$ is $9 \cdot 2.7778/16.1111 = 1.5517$, the score for $\sigma^2$ is 0, the information for $\mu$ is $9/16.1111 = 0.5586$, and $S = 1.5517^2/0.5586 = 4.3103$, with $p = 0.0379$. The other two give $W = 8.2721$ ($p = 0.0040$) and $\Lambda = 5.8668$ ($p = 0.0154$), and the exact t-test gives $p = 0.0266$. Here $W \ge \Lambda \ge S$, as always in this model.

**Counts in cells.** For the counts $18, 30, 52$ and $H_0$: probabilities $0.25, 0.25, 0.5$, the score test is Pearson's statistic $X^2 = 49/25 + 25/25 + 4/50 = 3.04$ with $r = 2$ and $p = 0.2187$. The likelihood ratio (G) statistic of the same data is $3.1921$.

## Correctness

Line L4 solves $Jy = u$, so line L5 returns $u^\top J^{-1}u$, which is $\ge 0$ when $J$ is positive definite. The closed forms follow from the scores and informations of each model; for a multinomial the quadratic form equals Pearson's $X^2$ exactly, which the tests check in rational arithmetic. Under a simple null, the score is a sum of $n$ iid vectors with mean 0 and covariance $I(\theta_0)$, so $U_n/\sqrt n \to N(0, I)$ and $S \to \chi^2_r$; with nuisance parameters, the restricted MLE adds a correction that turns the covariance of the tested part of the score into the inverse of the matching block of $I^{-1}$, and the limit is again $\chi^2_r$. The size of the test therefore tends to $\alpha$; this is proved. Finite-sample sizes are only measured, here by exact enumeration. The correctness proof gives each step.

## Complexity

On a [real RAM](/real-ram/), the closed forms need one pass over the data: $\Theta(n)$ time, or $\Theta(m)$ after counting for a multinomial with $m$ cells, and $\Theta(1)$ extra space. The general form costs one fit under $H_0$, plus $\Theta(nk)$ to sum the score, $\Theta(nk^2)$ for an observed or empirical information, and $\Theta(k^3)$ for the solve in line L4. The likelihood ratio test needs two fits and the Wald test one fit of the full model; the score test needs only the fit of the smaller model, which often has a closed form when the full one does not.

**Numerical stability.** Line L4 solves a system and does not invert $J$. In the closed forms there is no cancellation of large terms: $k - np_0$ is a difference of the data and a constant, computed once, and squared. When the score is computed from a sum of per-observation scores that nearly cancel, use [compensated summation](/kahan-summation/) or math.fsum. Line L6 computes the upper tail directly.

## Properties

- **Only the null fit.** The score test fits only $\Theta_0$. To screen many candidate extensions of a model, such as many extra regressors one at a time, the score test needs one fit in total, while the Wald and likelihood ratio tests need one new fit per candidate.
- **Invariant under reparametrization** when $I_n$ is the expected information. Under $\theta = g(\psi)$, the score and the information change by the Jacobian of $g$ and its square, and the quadratic form does not change. With the observed information this is not true in general.
- **Exists at the edge.** At $\hat p = 0$ the score test is finite, while the Wald statistic is infinite. It uses the variance under $H_0$, which does not depend on the data.
- **Asymptotically $\chi^2_r$, and equivalent to the Wald and LR tests** under $H_0$ and local alternatives.
- **Conservative in the normal mean model.** With $u = T^2/(n - 1)$, $S = nu/(1 + u) \le n\log(1 + u) = \Lambda \le nu = W$. The exact size of the nominal 5% score test is $0.022$ at $n = 5$, $0.042$ at $n = 10$, $0.047$ at $n = 20$ and $0.049$ at $n = 50$ (computed from the t distribution). For the binomial the sizes go both ways: $0.0215$ at $n = 10$, $p_0 = 0.5$, and $0.0608$ at $n = 30$, $p_0 = 0.05$ (exact enumeration).
- **Locally most powerful.** For a one-sided alternative in a one-parameter family, rejecting for large $U_n(\theta_0)$ maximizes the derivative of the power at $\theta_0$ among tests of size $\alpha$.

## Variants and improvements

- **Signed score statistic.** For one parameter, $Z = U_n(\theta_0)/\sqrt{I_n(\theta_0)}$ gives one-sided tests. For the binomial it is the one-proportion z-test.
- **Score intervals.** Inverting the score test gives the [Wilson score interval](/wilson-score-interval/) for a proportion, which has much better coverage than the Wald interval.
- **Observed information or outer product.** Replacing $I_n$ by the observed information $-\nabla^2\ell(\tilde\theta_0)$, or by the outer product of the per-observation scores (the $nR^2$ form common in econometrics), gives statistics with the same limit. They differ in finite samples, and the outer product form often has poor size.
- **Robust score test.** With a sandwich estimate of the covariance of the score, the test stays valid when the variance model is wrong, as in [generalized estimating equations](/generalized-estimating-equations/).
- **Famous special cases.** Pearson's [chi-squared goodness-of-fit test](/chi-squared-goodness-of-fit-test/) and the [chi-squared test of independence](/chi-squared-test-of-independence/); the [log-rank test](/log-rank-test/), which is the score test of the Cox model for a group indicator; the [Breusch-Pagan test](/breusch-pagan-test/) for heteroscedasticity; and the LM test of Engle (1982) for ARCH effects in time series.

## When to use it

Use the score test when the null model is easy to fit and the full model is not: testing whether a simple model needs an extra term, a nonzero variance component, an interaction or a more general error structure. It is the natural choice for screening many candidate extensions, since all of them share the one null fit. Use it for a proportion near 0 or 1, where the Wald test fails. When both models are easy to fit, the likelihood ratio test is usually more accurate. For small samples, use an exact test when one exists.

## Pitfalls

- **Expected or observed information.** They give different numbers in finite samples, and only the expected information makes the test invariant. State which one is used.
- **Nuisance parameters must be refitted.** The score must be evaluated at the restricted MLE $\tilde\theta_0$, not at the full MLE and not at guessed nuisance values. With other plug-in values the variance of the score is wrong and the $\chi^2_r$ limit fails.
- **Loss of power far from the null.** The test uses the curvature at $\theta_0$. For some models the score at the null can be small even when the alternative is far away, so the power can be low or even fall as the effect grows.
- **Boundary nulls.** For a variance component equal to 0, the one-sided nature of the alternative must be taken into account, as for the likelihood ratio test.
- **Reading the asymptotic size as exact.** The size can be well below or above $\alpha$ for small samples and discrete data, as the size values above show.

## Implementations

## History

C. R. Rao proposed the test in 1948 in the Proceedings of the Cambridge Philosophical Society, as a large-sample test that uses only quantities at the null value: the score and the information. Aitchison and Silvey (1958) studied the maximum likelihood estimate under restrictions and the asymptotic law of its Lagrange multipliers, and Silvey (1959) built the test on the multipliers and named it the Lagrangian multiplier test; it is the same statistic as Rao's. Econometricians adopted the name "LM test" in the 1970s and 1980s, with work by Breusch and Pagan and by Engle, and used it for specification tests of regression models. Pearson's chi-squared statistic of 1900 and the log-rank test of the 1960s turned out to be score tests of their models.

## References
