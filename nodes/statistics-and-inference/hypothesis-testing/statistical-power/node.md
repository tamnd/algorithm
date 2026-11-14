---
tag: 558Q0H
kind: definition
slug: statistical-power
name: Statistical power
aliases:
- power of a test
- power function
area: statistics-and-inference/hypothesis-testing
level: intro
summary: The probability that a test rejects the null hypothesis when a given alternative is true. It grows with the sample size and the effect size.
prereqs: [statistical-hypothesis-test, type-i-and-type-ii-errors]
see_also: [sample-size-determination, effect-size, z-test, student-t-test, neyman-pearson-lemma, uniformly-most-powerful-test, p-value, binomial-test]
sources:
  - paper: doi:10.1098/rsta.1933.0009
    title: "J. Neyman and E. S. Pearson, On the problem of the most efficient tests of statistical hypotheses, Philosophical Transactions of the Royal Society A 231, 1933, pp. 289 to 337"
    locator: The whole paper (the probability of rejecting a false hypothesis, and the most powerful critical region at a given size)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 8.3.1 (error probabilities and the power function, with the normal power function as an example)
  - book: isbn:9780805802832
    title: Jacob Cohen, Statistical Power Analysis for the Behavioral Sciences, second edition, Lawrence Erlbaum, 1988
    locator: Chapter 1 (the concepts of power analysis) and Chapter 2 (power tables for the t-test)
  - paper: doi:10.1198/000313001300339897
    title: "John M. Hoenig and Dennis M. Heisey, The abuse of power: the pervasive fallacy of power calculations for data analysis, The American Statistician 55(1), 2001, pp. 19 to 24"
    locator: The whole paper (observed power is a one-to-one function of the p-value and adds no information)
---

The power of a [statistical hypothesis test](/statistical-hypothesis-test/) at an alternative $\theta_1$ is the probability that the test rejects the null hypothesis when the data come from $\theta_1$. It is one minus the [type II error](/type-i-and-type-ii-errors/) probability at $\theta_1$. Power is not one number for a test: it is a value of the function $\pi(\theta) = P_\theta(\text{reject } H_0)$, which runs over the whole parameter space, equals the type I error probability on the null and the power on the alternative. Power grows with the sample size and with the distance of $\theta_1$ from the null, and falls as the level $\alpha$ is made stricter.

## Definition

Let a test of $H_0: \theta \in \Theta_0$ against $H_1: \theta \in \Theta_1$ reject when the data $X$ fall in a region $R$ (or, for a randomized test $\phi$, with probability $\phi(X)$). Its power function is

$$\pi(\theta) = P_\theta(X \in R) \quad \big(= E_\theta[\phi(X)]\big), \qquad \theta \in \Theta .$$

- For $\theta \in \Theta_1$, $\pi(\theta)$ is the **power** of the test at $\theta$, and $\beta(\theta) = 1 - \pi(\theta)$ is its type II error probability.
- For $\theta \in \Theta_0$, $\pi(\theta)$ is the type I error probability, and the test has level $\alpha$ when $\sup_{\Theta_0}\pi \le \alpha$.

We write $\pi$ for the power function, as $\beta$ is used for the type II error; Casella and Berger write $\beta(\theta)$ for the power function itself.

**The normal mean.** For the two-sided [z-test](/z-test/) of $H_0: \mu = \mu_0$ with $n$ iid $N(\mu, \sigma^2)$ observations, known $\sigma$, and $\lambda = \sqrt n(\mu - \mu_0)/\sigma$,

$$\pi(\mu) = \Phi(\lambda - z_{1-\alpha/2}) + \Phi(-\lambda - z_{1-\alpha/2}) .$$

It equals $\alpha$ at $\mu = \mu_0$, is symmetric in $\lambda$, increases with $|\lambda|$, and tends to 1 as $|\lambda| \to \infty$. It depends on $\mu$, $\sigma$ and $n$ only through $\lambda$, so power at a fixed alternative grows like $\sqrt n$ times the standardized [effect size](/effect-size/) $(\mu - \mu_0)/\sigma$ inside $\Phi$.

## Examples and non-examples

**A power table.** For the z-test with $n = 9$, $\sigma = 4$, $\mu_0 = 500$ and $\alpha = 0.05$ two-sided, the formula gives $\pi = 0.0663, 0.1165, 0.3230, 0.6141, 0.8508, 0.9633$ at $\mu = 500.5, 501, 502, 503, 504, 505$. The same test detects a shift of 5 almost always and a shift of 1 rarely; "the power of the test" means nothing until the alternative is named.

**A t-test design.** For the two-sample t-test with 64 observations per group at $\alpha = 0.05$ two-sided, the power at a standardized difference $d$ is 0.2023, 0.3915, 0.6124, 0.8015, 0.9205 and 0.9943 at $d = 0.2, 0.3, 0.4, 0.5, 0.6, 0.8$ (noncentral t probabilities computed by numerical integration, as on [sample size determination](/sample-size-determination/)). The design has 80% power at $d = 0.5$, which is how 64 per group is usually justified.

**The cost of estimating $\sigma$.** With 10 observations at $\alpha = 0.05$ two-sided, the one-sample t-test has power 0.293 at $d = 0.5$ and 0.803 at $d = 1$, against 0.353 and 0.885 for the z-test with $\sigma$ known.

**Non-example: observed power.** Plugging the observed effect into the power formula after the study gives a number that is a fixed function of the p-value (Hoenig and Heisey, 2001). For the two-sided z-test, observed power is $\Phi(|z| - 1.96) + \Phi(-|z| - 1.96)$:

| observed $\lvert z \rvert$ | two-sided p-value | observed power |
|---|---|---|
| 1.000 | 0.3173 | 0.1701 |
| 1.645 | 0.1000 | 0.3766 |
| 1.960 | 0.0500 | 0.5001 |
| 2.576 | 0.0100 | 0.7311 |
| 3.000 | 0.0027 | 0.8508 |

A non-significant result always has observed power below about 0.5, so "the result was not significant because the power was low" says only that $p$ was large. Power belongs to the design stage, at an effect chosen for its importance.

**Non-example: the probability that a significant result is true.** Power is $P(\text{reject} \mid \theta_1)$. The share of true effects among significant results also depends on how many of the tested nulls are true, which power does not include.

## Related definitions

- **Size and level.** The supremum of $\pi$ over $\Theta_0$, and a bound $\alpha$ on it; see [type I and type II errors](/type-i-and-type-ii-errors/).
- **Most powerful and uniformly most powerful tests.** A level-$\alpha$ test is most powerful at $\theta_1$ if no level-$\alpha$ test has larger $\pi(\theta_1)$, and [uniformly most powerful](/uniformly-most-powerful-test/) if this holds at every $\theta_1 \in \Theta_1$. The [Neyman-Pearson lemma](/neyman-pearson-lemma/) gives the most powerful test for simple hypotheses. The one-sided z-test is uniformly most powerful; a two-sided test cannot be, but the two-sided z-test is uniformly most powerful among unbiased tests.
- **Unbiased test.** $\pi(\theta) \ge \alpha$ for all $\theta \in \Theta_1$: rejection is at least as likely under any alternative as under the null.
- **Consistent test.** A sequence of tests with $\pi_n(\theta) \to 1$ for every $\theta \in \Theta_1$ as $n \to \infty$; the z-test and the t-test are consistent.
- **[Sample size determination](/sample-size-determination/).** The inverse problem: the smallest $n$ at which $\pi_n(\theta_1) \ge 1 - \beta$.

## References
