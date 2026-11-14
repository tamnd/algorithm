---
tag: 04CJ2P
kind: algorithm
slug: likelihood-ratio-test
name: Likelihood ratio test
aliases:
- LRT
- generalized likelihood ratio test
area: statistics-and-inference/hypothesis-testing
level: core
summary: Compares the maximized likelihood under the null with that under the full model, and rejects when twice the log ratio is large. Wilks' theorem gives its null distribution.
model: real-ram
complexity:
  vars: {n: the number of observations, m: the number of cells of a multinomial}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1928
  people: [Jerzy Neyman, Egon S. Pearson]
  note: Neyman and Pearson proposed the ratio of maximized likelihoods as a general test criterion in 1928. Wilks (1938) proved that twice its log has a chi-squared limit, which made the test usable for any regular model.
prereqs: [statistical-hypothesis-test, p-value, likelihood-function, maximum-likelihood-estimation, neyman-pearson-lemma]
see_also: [wilks-theorem, wald-test, score-test, deviance-statistic, chi-squared-goodness-of-fit-test, akaike-information-criterion, parametric-bootstrap, e-variable]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 8.2.1 (likelihood ratio tests, with the normal and exponential examples) and Section 10.3.1 (the asymptotic distribution of the LRT)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Part II (large-sample theory), the chapters on likelihood ratio tests in quadratic mean differentiable families
  - paper: "Jerzy Neyman and Egon S. Pearson, On the use and interpretation of certain test criteria for purposes of statistical inference, Part I, Biometrika 20A (1928), pages 175 to 240"
    title: Neyman and Pearson 1928
    locator: the likelihood ratio criterion lambda for composite hypotheses
  - paper: doi:10.1214/aoms/1177732360
    title: S. S. Wilks, The large-sample distribution of the likelihood ratio for testing composite hypotheses, Annals of Mathematical Statistics 9(1) (1938), pages 60 to 62
    locator: the chi-squared limit of -2 log lambda
---

The likelihood ratio test (LRT) compares two fits of the same model: the best fit under the null hypothesis and the best fit with the parameter free. Its statistic is $\Lambda = 2(\ell(\hat\theta) - \ell(\hat\theta_0))$, twice the gain in log-likelihood from freeing the parameter, and the test rejects when $\Lambda$ is large. By [Wilks' theorem](/wilks-theorem/), $\Lambda$ has an approximate $\chi^2_r$ null distribution, where $r$ is the number of constraints, so the p-value is an upper chi-squared tail and is only asymptotic. For a simple null against a simple alternative the same ratio gives the most powerful test of the [Neyman-Pearson lemma](/neyman-pearson-lemma/).

## In plain words

You have a model with some settings you do not know, and a claim that fixes some of them. Fit the model twice. First let every setting take its best value for the data. Then hold the claimed settings fixed and let only the rest move. The first fit always explains the data at least as well. Measure how much better, on a log scale, and double it. If the claim is true, this gain is a matter of chance, and for large samples its typical size is known from a standard table that depends only on how many settings the claim fixed. If the gain is much larger than chance usually gives, reject the claim.

## The problem

**Model and hypotheses.** The data $x = (x_1, \dots, x_n)$ are iid with density $f(x; \theta)$, $\theta \in \Theta \subseteq \mathbb R^k$. The log-likelihood is $\ell(\theta) = \sum_i \log f(x_i; \theta)$, as on the [likelihood function](/likelihood-function/) page. The null hypothesis $H_0: \theta \in \Theta_0$ restricts $\theta$ to a subset of dimension $k - r$, for example by fixing $r$ coordinates. The alternative is $H_1: \theta \in \Theta \setminus \Theta_0$.

**Statistic.** With $\hat\theta$ the [maximum likelihood estimate](/maximum-likelihood-estimation/) over $\Theta$ and $\hat\theta_0$ the restricted MLE over $\Theta_0$,
$$\Lambda = 2\left(\ell(\hat\theta) - \ell(\hat\theta_0)\right) = -2\log\frac{\sup_{\theta \in \Theta_0} L(\theta; x)}{\sup_{\theta \in \Theta} L(\theta; x)} \ \ge\ 0.$$

**Null distribution.** Asymptotic: under $H_0$ and the regularity conditions of [Wilks' theorem](/wilks-theorem/), $\Lambda \to \chi^2_r$ in distribution. Exact in a few models: for a normal mean with known $\sigma$, $\Lambda = n(\bar x - \mu_0)^2/\sigma^2$, which is exactly $\chi^2_1$; for a normal mean with unknown variance, $\Lambda = n\log(1 + T^2/(n - 1))$ with $T$ the [Student t](/student-t-test/) statistic, so the exact null law comes from $t_{n-1}$.

**Rejection rule and size.** Reject at level $\alpha$ when $\Lambda \ge \chi^2_{r, 1-\alpha}$, the upper $\alpha$ point of $\chi^2_r$. The size tends to $\alpha$ as $n \to \infty$. For finite $n$ it is only near $\alpha$, and it can be far off for small samples or discrete data.

**p-value.** $p = P(\chi^2_r \ge \Lambda)$, computed as an upper incomplete gamma function, $p = Q(r/2, \Lambda/2)$.

**Sensitivity and power.** The test reacts to any departure from $\Theta_0$ in the $r$ constrained directions. Under local alternatives $\theta_n = \theta_0 + h/\sqrt n$, $\Lambda$ tends to a noncentral $\chi^2_r(\delta)$, where $\delta$ grows with the squared distance of $h$ from the null set in the metric of the [Fisher information](/fisher-information-matrix/). For a scalar parameter the two-sided LRT has the same local power as the [Wald test](/wald-test/) and the [score test](/score-test/).

## The algorithm

```pseudo id=main
LIKELIHOOD-RATIO-TEST(x, ℓ, Θ, Θ₀, r)       ▷ r = dim Θ − dim Θ₀ ≥ 1
L1  θ̂ ← a maximizer of ℓ(θ; x) over Θ
L2  θ̂₀ ← a maximizer of ℓ(θ; x) over Θ₀
L3  Λ ← 2 (ℓ(θ̂; x) − ℓ(θ̂₀; x))
L4  Λ ← max(Λ, 0)                              ▷ guards rounding and a weak optimizer
L5  p ← Q(r/2, Λ/2)                             ▷ P(χ²_r ≥ Λ), the upper tail directly
L6  return (Λ, p)
```

Lines L1 and L2 are where the work is. For most models they need a numerical optimizer, such as [Newton's method](/newton-raphson-method/) or [Fisher scoring](/fisher-scoring/). For the common models below the maximizers have closed forms, and line L3 becomes a sum of deviance terms $D(a, b) = a\log(a/b) - a + b \ge 0$, with $0\log 0 = 0$:

| model, null | $\Lambda$ | $r$ |
|---|---|---|
| binomial, $p = p_0$ | $2\left(D(k, np_0) + D(n - k, n(1 - p_0))\right)$ | 1 |
| Poisson, $\lambda = \lambda_0$ | $2D(\textstyle\sum x_i, n\lambda_0)$ | 1 |
| normal, $\mu = \mu_0$, $\sigma$ known | $n(\bar x - \mu_0)^2/\sigma^2$ | 1 |
| normal, $\mu = \mu_0$, $\sigma$ unknown | $n\log\left(1 + n(\bar x - \mu_0)^2/SS\right)$, $SS = \sum(x_i - \bar x)^2$ | 1 |
| multinomial, cell probabilities $q_j$ | $2\sum_j D(O_j, nq_j)$, the G-statistic | $m - 1$ |

In the deviance form the linear terms $-a + b$ add up to 0 over the cells, so the table equals the usual $2\sum O\log(O/E)$. For the normal model with unknown variance, $\hat\sigma^2 = SS/n$ and $\hat\sigma_0^2 = SS/n + (\bar x - \mu_0)^2$, both with divisor $n$ (the MLE), and $\Lambda = n\log(\hat\sigma_0^2/\hat\sigma^2)$.

## Example

**A binomial count.** In 20 trials there are 15 successes. Test $H_0: p = 0.5$ against $p \ne 0.5$ at $\alpha = 0.05$.

| step | value |
|---|---|
| L1: $\hat p = 15/20$ | 0.75 |
| L2: $\hat p_0$ | 0.5 |
| L3: $D(15, 10) = 15\log 1.5 - 5$ | 1.081977 |
| L3: $D(5, 10) = 5\log 0.5 + 5$ | 1.534264 |
| L3: $\Lambda = 2(1.081977 + 1.534264)$ | 5.232481 |
| L5: $p = P(\chi^2_1 \ge 5.232481)$ | 0.022169 |

Since $5.2325 \ge 3.8415$, the test rejects at the 5% level. The test rejects exactly when $K \le 5$ or $K \ge 15$, so its exact size is $2\sum_{k \le 5}\binom{20}{k}2^{-20} = 0.0414$, below the nominal $0.05$. Its exact power is $0.1272$ at $p = 0.6$, $0.4164$ at $p = 0.7$ and $0.8042$ at $p = 0.8$.

**A normal mean.** The nine pack weights of the [z-test](/z-test/) page, $502, 498, 505, 503, 501, 507, 499, 504, 506$, have $\bar x = 502.7778$ and $SS = 75.5556$. For $H_0: \mu = 500$:

| case | $\Lambda$ | $\chi^2_1$ p-value | exact p-value |
|---|---|---|---|
| $\sigma = 4$ known | 4.3403 | 0.0372 | 0.0372 (exact, $\Lambda = z^2$) |
| $\sigma$ unknown | 5.8668 | 0.0154 | 0.0266 (from $t_8$, $T = 2.7116$) |

With $\sigma$ unknown the chi-squared p-value is too small by a factor of almost 2 at $n = 9$. The t-test is the exact form of this LRT.

**A multinomial.** Counts $18, 30, 52$ in three cells, with $H_0$: probabilities $0.25, 0.25, 0.5$. The expected counts are $25, 25, 50$, $\Lambda = G = 3.1921$ with $r = 2$, and $p = 0.2027$. The Pearson statistic of the [chi-squared goodness-of-fit test](/chi-squared-goodness-of-fit-test/) is $3.04$, with $p = 0.2187$. The two agree to first order, because the Pearson statistic is the score test of the same null.

## Correctness

The statistic is nonnegative, because $\Theta_0 \subseteq \Theta$ makes the unrestricted maximum at least the restricted one. It does not depend on the parametrization: a one-to-one change of parameter does not change the maximum values of the likelihood. The closed forms in the table follow from the explicit MLEs, and the deviance form follows from $\sum_j (O_j - nq_j) = 0$. The p-value $Q(r/2, \Lambda/2)$ is the upper tail of $\chi^2_r$. Under $H_0$ and regularity, Wilks' theorem gives $P(p \le \alpha) \to \alpha$, so the size is asymptotically $\alpha$. This is the only guarantee of the general test. It is exact only where $\Lambda$ is exactly $\chi^2_r$, as for the normal mean with known $\sigma$. The correctness proof below gives these steps, and also proves that the routine for a simple null against a simple alternative returns the Neyman-Pearson test.

## Complexity

On a [real RAM](/real-ram/), with closed-form maximizers, the statistic needs one pass over the data or the cells: $\Theta(n)$ time for the binomial, Poisson and normal forms, and $\Theta(m)$ for a multinomial with $m$ cells after counting. The p-value is one evaluation of the incomplete gamma function. The extra space is $\Theta(1)$. In the general case, the cost is that of the two optimizations in lines L1 and L2, typically a number of iterations times $\Theta(nk^2 + k^3)$ for Newton steps in $k$ parameters.

**Numerical stability.** Three points matter.

- **Cancellation near the null.** Written as $2[k\log(k/(np_0)) + (n - k)\log((n - k)/(n(1 - p_0)))]$, the binomial statistic is a difference of two large numbers when $\hat p$ is near $p_0$. With $n = 10^9$ and $k = 500\,000\,001$, the true $\Lambda$ is $4 \times 10^{-9}$, and the naive formula returns $-1.07 \times 10^{-7}$, a negative number. The deviance term $D(a, b) = b\,h(a/b)$ with $h(t) = t\log t - t + 1$ is computed from the series $h(1 + d) = \sum_{j \ge 2} (-1)^j d^j/(j(j - 1))$ when $|d| < 0.1$, which has no cancellation. This is [catastrophic cancellation](/catastrophic-cancellation/) of the same kind as in variance computations.
- **The general form.** Line L3 subtracts two log-likelihoods that can each be of order $n$. The difference keeps only the digits that the two values do not share. Line L4 clips the tiny negative values that rounding or an optimizer that stops early can produce. When accuracy matters, compute the difference in closed form, as the table does.
- **The upper tail.** Line L5 computes $Q(r/2, \Lambda/2)$ directly, by a continued fraction for large arguments. Computing $1 - P(r/2, \Lambda/2)$ returns 0 for p-values below about $10^{-16}$. For $\sigma$ unknown, $\log(1 + u)$ is computed with log1p.

## Properties

- **Invariant under reparametrization.** The value of $\Lambda$ does not change when $\theta$ is replaced by $g(\theta)$ for a one-to-one $g$. The Wald test does not have this property.
- **Nonnegative and nested.** $\Lambda \ge 0$, and adding constraints to $\Theta_0$ can only increase it.
- **Asymptotically $\chi^2_r$ under the null.** By Wilks' theorem, with the conditions stated there. The size is only near $\alpha$ for finite $n$.
- **Asymptotically equivalent to the Wald and score tests.** Under the null and local alternatives, the three statistics differ by $o_p(1)$. In finite samples they differ. For a normal mean with unknown variance, with $u = T^2/(n - 1)$, they are $W = nu$, $\Lambda = n\log(1 + u)$ and $S = nu/(1 + u)$, so $W \ge \Lambda \ge S$ always.
- **Optimal for simple hypotheses.** For a simple null against a simple alternative, rejecting for large $L(\theta_1; x)/L(\theta_0; x)$ is most powerful, by the Neyman-Pearson lemma. For composite hypotheses the LRT has no exact optimality in general, but it is asymptotically optimal in several senses, for example in Bahadur efficiency.
- **Needs both fits.** The LRT uses the restricted and the unrestricted MLE. The Wald test needs only the unrestricted fit, and the score test only the restricted one.

## Variants and improvements

- **Simple null against simple alternative.** On a finite sample space, the Neyman-Pearson test can be built directly: sort the points by $f_1/f_0$, reject at the points with the largest ratios until the size $\alpha$ is used, and randomize at the last point. The implementation provides it in exact rational arithmetic. Under $H_0$, the ratio $f_1(X)/f_0(X)$ has expectation at most 1, so it is also an [e-variable](/e-variable/).
- **Signed root.** For a scalar parameter, $r = \operatorname{sign}(\hat\theta - \theta_0)\sqrt\Lambda$ is approximately $N(0, 1)$ and gives one-sided tests and likelihood-based confidence intervals.
- **Profile likelihood intervals.** Inverting the LRT gives the set $\{\theta_0 : \Lambda(\theta_0) < \chi^2_{1, 1-\alpha}\}$, which is invariant under reparametrization and often better than the Wald interval. See [test-interval duality](/test-interval-duality/).
- **Bartlett correction.** Dividing $\Lambda$ by an estimate of $E_0\Lambda/r$ improves the chi-squared approximation from error $O(n^{-1})$ to $O(n^{-2})$. Wilks' theorem shows the numbers for the normal mean.
- **Parametric bootstrap.** Simulate data from the fitted null model $\hat\theta_0$, recompute $\Lambda$ each time, and use the simulated distribution in place of $\chi^2_r$. See [parametric bootstrap](/parametric-bootstrap/). This also handles boundary cases.
- **Deviance and G-test.** In generalized linear models, $\Lambda$ is a difference of [deviances](/deviance-statistic/). For counts, $\Lambda$ is the G-statistic.
- **Split likelihood ratio.** Fit the alternative on one half of the data and evaluate the ratio on the other half. The result is an e-variable for any composite null, with a valid level for every $n$ and no regularity conditions, at the cost of power (universal inference, Wasserman, Ramdas and Balakrishnan 2020).

## When to use it

Use the LRT for nested parametric models when both fits are easy to compute: comparing a model with and without a group of terms, testing a variance component that is not on the boundary, or testing a parameter whose Wald statistic depends badly on the scale. Prefer it to the Wald test when the estimate is near the edge of the parameter space or the likelihood is skewed, as for small binomial or Poisson counts. Use the score test when the full model is hard to fit. For small samples, use an exact test where one exists, such as the [binomial test](/binomial-test/) or the t-test, or calibrate $\Lambda$ by a parametric bootstrap.

## Pitfalls

- **Parameters on the boundary.** Testing a variance component equal to 0, or a mixture weight equal to 0, puts $\theta_0$ on the edge of $\Theta$. The null law is then a mixture such as $\tfrac12\chi^2_0 + \tfrac12\chi^2_1$, and the $\chi^2_1$ reference makes the test conservative. See [Wilks' theorem](/wilks-theorem/).
- **Parameters not identified under the null.** For the number of mixture components or an unknown change point, the chi-squared reference is wrong, and the error grows with $n$.
- **Non-nested models.** $\Lambda$ compares a model with a submodel. For two models where neither contains the other, the chi-squared reference does not apply. Use an information criterion such as the [AIC](/akaike-information-criterion/), or a test made for non-nested models.
- **Different data in the two fits.** If missing values remove different rows from the two fits, the likelihoods are of different data and $\Lambda$ means nothing. Fit both models to the same rows.
- **A local maximum.** If the optimizer stops at a local maximum in line L1, $\Lambda$ is too small, and it can even be negative. Start the full fit from the null fit, which guarantees $\ell(\hat\theta) \ge \ell(\hat\theta_0)$.
- **Reading the asymptotic size as exact.** The binomial test above has exact size 0.0414, and the normal LRT with unknown variance has size 0.098 at $n = 5$, not 0.05.

## Implementations

## History

Jerzy Neyman and Egon Pearson introduced the likelihood ratio criterion $\lambda$ in their 1928 papers in Biometrika, as a general principle to build tests of composite hypotheses. In 1933 they proved that for simple hypotheses the ratio gives the most powerful test. Samuel S. Wilks proved in 1938 that $-2\log\lambda$ is asymptotically chi-squared, which made the test practical. Abraham Wald (1943) showed its large-sample optimality and its equivalence with the Wald test, and Rao (1948) added the score test, which completed the trio of classical large-sample tests. The G-statistic for counts goes back to the same period and became common in biology through the textbook of Sokal and Rohlf.

## References
