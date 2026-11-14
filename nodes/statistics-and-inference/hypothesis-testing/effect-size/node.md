---
tag: Q9FA7V
kind: definition
slug: effect-size
name: Effect size
aliases:
- Cohen's d
- standardized mean difference
area: statistics-and-inference/hypothesis-testing
level: intro
summary: A scale-free measure of how large an effect is, such as a mean difference divided by a standard deviation. Unlike a p-value it does not grow with n.
prereqs: [variance, statistical-hypothesis-test]
see_also: [statistical-power, sample-size-determination, p-value, student-t-test, welch-t-test, confidence-interval, estimator-bias, standard-error]
sources:
  - book: isbn:9780805802832
    title: Jacob Cohen, Statistical Power Analysis for the Behavioral Sciences, second edition, Lawrence Erlbaum, 1988
    locator: Chapter 2, Section 2.2 (the effect size index d for the difference of two means, and the conventional values 0.2, 0.5 and 0.8)
  - paper: doi:10.3102/10769986006002107
    title: "Larry V. Hedges, Distribution theory for Glass's estimator of effect size and related estimators, Journal of Educational Statistics 6(2), 1981, pp. 107 to 128"
    locator: The bias of the sample standardized mean difference and the exact correction factor J
---

An effect size is a number that says how large an effect is, as opposed to how surely it differs from zero. The most used one, Cohen's $d$, is the difference of two means divided by their common standard deviation, a unitless quantity. A [p-value](/p-value/) depends on both the effect and the sample size, while an effect size estimates a property of the populations that does not change with $n$. Effect sizes are what power calculations and meta-analyses work with.

## Definition

**Population value.** For two populations with means $\mu_1, \mu_2$ and a common standard deviation $\sigma$ (the root of the [variance](/variance/)), Cohen's $d$ is

$$\delta = \frac{\mu_1 - \mu_2}{\sigma} .$$

For one population and a reference value $\mu_0$ it is $(\mu - \mu_0)/\sigma$.

**Sample value.** With samples of sizes $n_1, n_2$ and the pooled variance $S_p^2 = \big((n_1 - 1)S_1^2 + (n_2 - 1)S_2^2\big)/(n_1 + n_2 - 2)$ (divisor $n_1 + n_2 - 2$),

$$d = \frac{\bar X_1 - \bar X_2}{S_p}, \qquad t = d\sqrt{\frac{n_1 n_2}{n_1 + n_2}},$$

where $t$ is the pooled [Student t](/student-t-test/) statistic. So $t$ grows like $\sqrt n$ at a fixed $d$, while $d$ does not.

**Hedges's correction.** Under normal data, $d$ overestimates $|\delta|$: $E[d] = \delta/J(\nu)$ with $\nu = n_1 + n_2 - 2$ and

$$J(\nu) = \frac{\Gamma(\nu/2)}{\sqrt{\nu/2}\,\Gamma((\nu - 1)/2)} \approx 1 - \frac{3}{4\nu - 1} .$$

The reason is that $\bar X_1 - \bar X_2$ and $S_p$ are independent and $E[\sigma/S_p] = 1/J(\nu)$. Hedges's $g = J(\nu)\,d$ is therefore unbiased for $\delta$ (Hedges, 1981).

**Conventions.** Cohen called $\delta = 0.2$, $0.5$ and $0.8$ small, medium and large, as defaults for when nothing better is known about the field. For two normal populations with a common $\sigma$, $P(X_1 > X_2) = \Phi(\delta/\sqrt 2)$, which is 0.556, 0.638 and 0.714 at these values.

## Examples and non-examples

**A computation.** $x = 5, 7, 9, 6, 8$ and $y = 3, 5, 4, 6, 2$. The means are 7 and 4, each sum of squared deviations is 10, so $S_p^2 = 20/8 = 2.5$ and $S_p = 1.5811$. Then $d = 3/1.5811 = 1.8974$. With $\nu = 8$, $J(8) = 0.902703$ (the approximation gives 0.903226), so $g = 1.7128$. The t statistic is $1.8974\sqrt{25/10} = 3.0$ with 8 degrees of freedom, two-sided $p = 0.0171$.

**The bias, measured.** Monte Carlo with $n_1 = n_2 = 5$, normal data with $\delta = 0.5$, $r = 20000$ replications, seed 41: the mean of $d$ is 0.5459 (the exact value is $0.5/J(8) = 0.5539$) and the mean of $g$ is 0.4928.

**Non-example: the p-value.** With the same sample $d = 0.3$ and $n$ observations per group, the two-sided t-test p-value is 0.511 at $n = 10$, 0.137 at $n = 50$, 0.0029 at $n = 200$ and $2.6 \times 10^{-11}$ at $n = 1000$. The p-value moved by ten orders of magnitude; the effect size did not move.

**Non-example: the t statistic.** $t = d\sqrt{n_1 n_2/(n_1 + n_2)}$ is a test statistic, not an effect size, because it grows with $n$.

**Not standardized, still an effect size.** A raw difference such as "3 mm Hg lower blood pressure" is an effect size in the units of the measurement. It is often more useful than $d$ when the units mean something; $d$ is needed to compare or combine studies that measured on different scales.

## Related definitions

- **Glass's $\Delta$.** The difference of means divided by the standard deviation of the control group only, used when the treatment may change the variance.
- **Paired data.** $d_z = \bar D/S_D$ uses the standard deviation of the differences. With within-pair correlation $\rho$ and equal variances, $\sigma_D = \sigma\sqrt{2(1 - \rho)}$, so $d_z$ and $d$ are on different scales and must not be compared directly.
- **Other effect sizes.** The correlation coefficient $r$, the odds ratio and the risk difference for binary outcomes, and $\eta^2$ for analysis of variance.
- **Use in power analysis.** The power of the t-test depends on $\delta$ and $n$ only, so $\delta$ is the input of [sample size determination](/sample-size-determination/).
- **Report with an interval.** A sample effect size is an estimate, and it should come with a [confidence interval](/confidence-interval/).

## References
