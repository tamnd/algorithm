---
tag: 43QS5G
kind: problem
slug: sample-size-determination
name: Sample size determination
aliases:
- power analysis
- sample size calculation
area: statistics-and-inference/hypothesis-testing
level: core
summary: Find the smallest sample size for which a level-alpha test reaches a target power at a stated effect, or an interval reaches a target width. Closed form for z; numerical for t.
prereqs: [statistical-power, effect-size, z-test, student-t-test]
see_also: [type-i-and-type-ii-errors, confidence-interval, t-confidence-interval, welch-t-test, binomial-test, bisection-method, simpsons-rule, monte-carlo-integration]
sources:
  - book: isbn:9780805802832
    title: Jacob Cohen, Statistical Power Analysis for the Behavioral Sciences, second edition, Lawrence Erlbaum, 1988
    locator: Chapter 2 (the t-test for means, the effect size d, and the power and sample size tables)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 8.3.1 (error probabilities and the power function, with the sample size choice for a normal mean)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 3 (uniformly most powerful tests) and Chapter 4 (unbiasedness), used for the bound that the t-test needs at least the z-test sample size
---

Sample size determination is the problem of choosing the number of observations before the data are collected. In its testing form, it asks for the smallest $n$ at which a level-$\alpha$ [statistical hypothesis test](/statistical-hypothesis-test/) has [power](/statistical-power/) at least $1 - \beta$ against a stated alternative, usually given as an [effect size](/effect-size/). In its estimation form, it asks for the smallest $n$ at which a confidence interval is at most a given width. For the [z-test](/z-test/) the answer is the closed form $n = \lceil((z_{1-\alpha/2} + z_{1-\beta})\sigma/\delta)^2\rceil$, up to one observation; for the [t-test](/student-t-test/) it needs the noncentral t distribution and a numerical method.

## In plain words

Before an experiment, you must decide how many subjects to measure. Too few, and a real effect of the size you care about will often be missed. Too many, and you waste money, time or patients. So you state four things: the smallest effect worth finding, how much single measurements scatter, how often you accept a false alarm, and how often you want to catch the effect when it is there. Then you find the smallest number of measurements that meets all four. For the simplest tests a short formula gives the answer. For the usual t-test, which estimates the scatter from the data, the answer is a little larger and needs a computer. The answer is only as good as the guessed effect and scatter.

## Definition

Let $\{\phi_n\}$ be a family of level-$\alpha$ tests, one for each sample size $n$, of $H_0: \theta \in \Theta_0$, and let $\pi_n(\theta) = P_\theta(\phi_n \text{ rejects})$ be the power function. Given a level $\alpha$, an alternative $\theta_1 \notin \Theta_0$ and a target power $1 - \beta$ with $\alpha < 1 - \beta < 1$, find

$$n^* = \min\{n : \pi_n(\theta_1) \ge 1 - \beta\} .$$

For the tests of a normal mean, $\theta_1$ enters only through the standardized effect $d = \delta/\sigma$, where $\delta$ is the true difference $\mu - \mu_0$ (one sample, or paired differences) or $\mu_1 - \mu_2$ (two groups of $n$ each). With the noncentrality $\lambda = |d|\sqrt{n/g}$, where $g = 1$ for one sample and $g = 2$ for two groups:

- the two-sided **z-test** with known $\sigma$ has $\pi_n = \Phi(\lambda - z_{1-\alpha/2}) + \Phi(-\lambda - z_{1-\alpha/2})$;
- the two-sided **t-test** has $\pi_n = P(|T'_{\nu,\lambda}| \ge t_{(\nu, 1-\alpha/2)})$, where $T'_{\nu,\lambda} = (Z + \lambda)/\sqrt{V/\nu}$ with $Z \sim N(0, 1)$ and $V \sim \chi^2_\nu$ independent is the noncentral t variable and $\nu = g(n - 1)$.

The one-sided versions keep only the near tail, with $z_{1-\alpha}$ and $t_{(\nu, 1-\alpha)}$. The estimation form: find the smallest $n$ with half-width $q\,\sigma/\sqrt n \le h$ (fixed width when $\sigma$ is known), or, when $\sigma$ is estimated, with a bound on the expected half-width or on the probability that the half-width exceeds $h$.

## Variants

- **Sides and level.** One-sided tests replace $z_{1-\alpha/2}$ by $z_{1-\alpha}$ and need fewer observations.
- **Unequal allocation.** With $n_1$ and $n_2 = kn_1$ and a common $\sigma$, $\operatorname{Var}(\bar X_1 - \bar X_2) = \sigma^2(1 + 1/k)/n_1$, so $n_1 = (1 + 1/k)\big((z_{1-\alpha/2} + z_{1-\beta})\sigma/\delta\big)^2$ for the z-test. For a fixed total $n_1 + n_2$ the variance $\sigma_1^2/n_1 + \sigma_2^2/n_2$ is smallest at $n_1/n_2 = \sigma_1/\sigma_2$ (Cauchy-Schwarz), which is $k = 1$ when the variances are equal.
- **Unequal variances.** The two-sample size uses $\sigma_1^2 + \sigma_2^2$ in place of $2\sigma^2$, and the test is then the [Welch t-test](/welch-t-test/).
- **Proportions.** For binomial data the z-test variance is $p(1 - p)$ under the null and the alternative, and an exact binomial test has a power that is not monotone in $n$ (Examples).
- **Precision instead of power.** Choose $n$ so that a [confidence interval](/confidence-interval/) has a given half-width. For the z interval this is $n = \lceil(z_{1-\alpha/2}\sigma/h)^2\rceil$; for the [t interval](/t-confidence-interval/) the half-width is random and the target is its expectation or a high quantile.
- **Clustered and sequential designs.** Cluster sampling multiplies the variance by a design effect, and group sequential designs fix a maximum $n$ with interim looks; both reduce to the fixed-$n$ problem with an adjusted variance or level.

## Examples

All values are at $\alpha = 0.05$ with $\sigma = 1$, computed by the code of this page: the z sizes from the closed form followed by an exact power search, the t sizes by an upward search over $n$ with the t power computed by numerical integration (see Known algorithms). $n$ is the size per group.

| design | $d$ | target power | sides | closed form, unrounded | z-test $n$ | t-test $n$ | t power at $n$ and $n - 1$ |
|---|---|---|---|---|---|---|---|
| two groups | 0.5 | 0.8 | 2 | 62.791 | 63 | 64 | 0.80146, 0.79517 |
| two groups | 0.2 | 0.8 | 2 | 392.444 | 393 | 394 | 0.80059, 0.79959 |
| two groups | 0.8 | 0.8 | 2 | 24.528 | 25 | 26 | 0.80749, 0.79145 |
| two groups | 0.5 | 0.9 | 2 | 84.059 | 85 | 86 | 0.90323, 0.89989 |
| two groups | 0.5 | 0.8 | 1 | 49.460 | 50 | 51 | 0.80590, 0.79894 |
| one sample | 0.5 | 0.8 | 2 | 31.396 | 32 | 34 | 0.80778, 0.79537 |
| one sample | 1.0 | 0.8 | 2 | 7.849 | 8 | 10 | 0.80310, 0.74802 |
| one sample | 0.5 | 0.8 | 1 | 24.730 | 25 | 27 | 0.81183, 0.79805 |

The first row is the familiar 64 per group for a "medium" effect in Cohen's terms. For it, $z_{0.975} = 1.959964$, $z_{0.8} = 0.841621$, and $2(2.801585/0.5)^2 = 62.791$. The t-test needs 1 more per group with two groups and 2 more with one sample, because the estimated $\sigma$ costs power, most at small $n$: with 10 observations at $d = 0.5$ the t power is 0.293 against 0.353 for the z-test, and at $d = 1$ it is 0.803 against 0.885.

**The power curve at a fixed design.** With 64 per group, two-sided t-test, the power is 0.2023 at $d = 0.2$, 0.3915 at $d = 0.3$, 0.6124 at $d = 0.4$, 0.8015 at $d = 0.5$, 0.9205 at $d = 0.6$ and 0.9943 at $d = 0.8$. The design has 80% power only against effects of at least about $0.5\sigma$.

**The far tail.** The closed form ignores the probability of rejecting in the wrong direction. At $d = 0.05$ with target power 0.3, the formula gives $\lceil 824.337\rceil = 825$, but the exact two-sided z power is 0.30024 at $n = 824$ and 0.29994 at $n = 823$, so $n^* = 824$.

**Precision.** For a 95% z interval of half-width 0.5 with $\sigma = 2$: $(1.959964 \times 2/0.5)^2 = 61.46$, so $n = 62$.

**A power that is not monotone in $n$.** The exact one-sided binomial test of $H_0: p = 0.5$ at level 0.05, rejecting for $X \ge k$ with the smallest $k$ whose null tail is at most 0.05, has power at $p = 0.7$ (exact sums): 0.8071 at $n = 37$, 0.7745 at $n = 38$, 0.7397 at $n = 39$ and 0.8074 at $n = 40$. The smallest $n$ with power at least 0.8 is 37, but $n = 38$ and $n = 39$ have less, because the attained size, 0.0494 at $n = 37$ and 0.0266 at $n = 39$, jumps with the integer critical value. For discrete tests the answer must say which of the two questions it answers.

## Known algorithms

- **Closed form for the z-test.** The near tail alone gives $\pi_n \ge \Phi(\lambda - z_{1-\alpha/2})$, which is at least $1 - \beta$ once $\lambda \ge z_{1-\alpha/2} + z_{1-\beta}$, that is $n \ge g\big((z_{1-\alpha/2} + z_{1-\beta})/d\big)^2$. The ceiling of this value always reaches the target, and the far tail $\Phi(-\lambda - z_{1-\alpha/2}) \le \alpha/2$ can make one fewer enough. The code steps down from the formula while the exact power at $n - 1$ still reaches the target; the exact z power increases with $n$ because $\frac{d}{d\lambda}\pi = \varphi(\lambda - c) - \varphi(\lambda + c) > 0$ for $\lambda, c > 0$. For one-sided tests the formula is exact up to the ceiling.
- **t power by numerical integration.** Conditioning on $V$, with $s = \sqrt V$ having the chi density with $\nu$ degrees of freedom,

  $$\pi_n = \int_0^\infty \Big[\Phi\Big(\lambda - c\frac{s}{\sqrt\nu}\Big) + \Phi\Big(-\lambda - c\frac{s}{\sqrt\nu}\Big)\Big] f_{\chi_\nu}(s)\,ds, \qquad c = t_{(\nu, 1-\alpha/2)} .$$

  This is exact: given $V$, the rejection event is a normal tail. The code integrates over $[\max(0, m - 12), m + 12]$ with $m = \sqrt{\max(\nu - 1, 0)}$, the mode of the chi density, whose standard deviation is below 0.8, and splits the range where the bracket falls from 1 to 0 (near $s = \lambda\sqrt\nu/c$ and $s = 0$). Each piece uses the composite [Simpson rule](/simpsons-rule/) with 800 intervals. The method's accuracy is checked, not proved: at $\lambda = 0$ the integral returns $\alpha$ within $10^{-8}$ for the tested $\nu$, and the power agrees with Monte Carlo simulation of the t-test within four standard errors ($r = 6000$, seeds 1 to 3, at $(n, d, g) = (10, 1, 1), (6, 1.2, 2), (3, 2, 1)$).
- **Search for $n^*$ for the t-test.** Start at the z-test answer $n_z$ and step up until $\pi_n \ge 1 - \beta$. This returns $n^*$ without assuming that the t power is monotone in $n$, because every $n < n_z$ has t power at most its z power, which is below the target (Bounds). Each step costs one integral, and the examples need at most 2 steps.
- **Simulation.** For designs without a power formula (mixed models, non-normal data, complex stopping rules), estimate $\pi_n$ by [Monte Carlo](/monte-carlo-integration/) simulation at a grid of $n$ and search. The error of each estimate is $\sqrt{\pi(1 - \pi)/r}$, so near $\pi = 0.8$ with $r = 10000$ it is 0.004, enough to move $n^*$ by a few units when the power curve is flat.
- **Root finding.** When $\pi_n$ is monotone in a continuous $n$, [bisection](/bisection-method/) on $n$ followed by a check of the two neighbouring integers is an alternative to the linear scan.

## Bounds

- **The t-test needs at least the z-test sample size.** For one-sided alternatives the z-test with known $\sigma$ is uniformly most powerful among level-$\alpha$ tests of $\mu \le \mu_0$, and for two-sided alternatives it is uniformly most powerful among unbiased level-$\alpha$ tests (Lehmann and Romano, Chapters 3 and 4, applied with $\sigma$ fixed). For each fixed $\sigma$ the t-test is a level-$\alpha$ test, and unbiased, in the model with that $\sigma$ known. So its power at every $n$ is at most the z power, and $n^*_t \ge n^*_z$. The examples show differences of 1 to 2.
- **The closed form overshoots by at most a little.** For two-sided z-tests $n^*_z \le \lceil n_f\rceil$ with $n_f = g((z_{1-\alpha/2} + z_{1-\beta})/d)^2$, and $n^*_z$ is at least the size that the near tail would need with target $1 - \beta - \alpha/2$, because the far tail adds at most $\alpha/2$.
- **Scaling.** $n^*$ grows like $1/d^2$: halving the effect quadruples the sample size, as the rows with $d = 0.2, 0.5, 0.8$ show (393, 63, 25). Raising the power from 0.8 to 0.9 multiplies $n$ by $(z_{0.975} + z_{0.9})^2/(z_{0.975} + z_{0.8})^2 = 10.507/7.849 = 1.34$.
- **Cost.** The closed form is $O(1)$. The t search costs $O(n^* - n^*_z + 1)$ integrals, each with a fixed number of normal CDF evaluations, independent of $n$.

## Reductions

- **Paired designs** reduce to the one-sample problem on the differences, with $\sigma_D$ in place of $\sigma$; a positive correlation $\rho$ within pairs gives $\sigma_D^2 = 2\sigma^2(1 - \rho)$ and a smaller $n$.
- **Power of the t-test** reduces to the CDF of the noncentral t distribution, which reduces to a one-dimensional integral over the chi distribution, as above.
- **Sample size for an interval** reduces to inverting the half-width $q\sigma/\sqrt n$, a monotone function of $n$, and through [test-interval duality](/test-interval-duality/) a precision target is a power-like target for the dual test.
- **Sample size for a proportion** reduces to the z-test case with $\sigma^2 = p(1 - p)$ for large $n$, by the [central limit theorem](/central-limit-theorem/) for the [binomial distribution](/binomial-distribution/); for small $n$ it needs the exact [binomial test](/binomial-test/) power and a scan over $n$.

## Applications

- **Clinical trials.** Protocols state $\alpha$, the power (often 0.8 or 0.9), the clinically relevant difference and the assumed variance, and justify the number of patients from them; too small a trial exposes patients without a reliable answer.
- **Online experiments.** A/B tests choose the number of users per arm from the smallest lift worth detecting and the variance of the metric.
- **Surveys.** The precision form sets the number of respondents for a margin of error, often with $p = 1/2$ as the worst case of $p(1 - p)$.
- **Replication studies.** A replication is sized for the effect that matters, not for the effect observed in the original study, which tends to be inflated.

The answer depends on guesses of $\delta$ and $\sigma$. Computing the power from the observed effect after a study ("observed power") adds nothing: it is a function of the p-value.

## References
