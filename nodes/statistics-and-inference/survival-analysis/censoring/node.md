---
tag: MXZ7M1
kind: definition
slug: censoring
name: Censoring
aliases:
- right censoring
- censored data
area: statistics-and-inference/survival-analysis
level: intro
summary: Partial knowledge of an event time, such as knowing only that it exceeds the end of follow-up. Survival methods use censored times without discarding them.
prereqs: [survival-function, likelihood-function]
see_also: [kaplan-meier-estimator, turnbull-estimator, hazard-function, nelson-aalen-estimator, missing-data-mechanism, competing-risks, order-statistic, maximum-likelihood-estimation]
sources:
  - book: isbn:9780387953991
    title: John P. Klein and Melvin L. Moeschberger, Survival Analysis, Techniques for Censored and Truncated Data, 2nd edition, Springer, 2003
    locator: Chapter 3 (right censoring of types I and II and random censoring, left and interval censoring, left and right truncation, and the likelihood for each)
  - book: isbn:9780471363576
    title: John D. Kalbfleisch and Ross L. Prentice, The Statistical Analysis of Failure Time Data, 2nd edition, Wiley, 2002
    locator: Chapter 1 (failure time data and the forms of censoring)
  - paper: doi:10.1073/pnas.72.1.20
    title: Anastasios Tsiatis, A nonidentifiability aspect of the problem of competing risks, Proceedings of the National Academy of Sciences 72(1), 1975
    locator: pp. 20 to 22 (every joint distribution of the latent times has an independent counterpart with the same observable distribution)
---

An event time is censored when the data say only that it lies in some set, not where in the set. The common case is right censoring: a patient is alive when the study ends, so the time of death is known only to exceed the follow-up time. Censoring is the defining feature of survival data. Discarding the censored subjects, or treating their censoring times as event times, both bias the answer, while the [survival function](/survival-function/) and the [hazard](/hazard-function/) can still be estimated from all the data, by the [Kaplan-Meier](/kaplan-meier-estimator/) and [Nelson-Aalen](/nelson-aalen-estimator/) estimators. Those estimators need one assumption that the data cannot check: that censoring is independent of the event, given the covariates in the model.

## Definition

Let $T \ge 0$ be the event time of a subject.

**Right censoring.** There is a censoring time $C$, and we observe

$$Y = \min(T, C), \qquad \delta = 1\{T \le C\}.$$

When $\delta = 1$ the event is seen at $Y = T$. When $\delta = 0$ we learn only that $T > Y$. A censored time is often written with a plus, as in $7^+$.

**Left censoring.** We learn only that $T \le L$ for a known $L$: the event had already happened when the subject was first examined, as when a child already has a skill at the first assessment, or an assay concentration is below the detection limit.

**Interval censoring.** We learn only that $L < T \le R$, as when a condition is found at a visit and was absent at the previous one. Right censoring is the case $R = \infty$, left censoring the case $L = 0$, and an exact time the limit $L \uparrow R$. In current status data each subject is examined once, at a time $c$, so the interval is $(0, c]$ or $(c, \infty)$. The [Turnbull estimator](/turnbull-estimator/) handles all of these.

**How the censoring times arise.**

1. **Type I.** Every subject is followed up to a fixed time $c$, so $C = c$. In generalized type I censoring subjects enter at different calendar times and the study stops on a fixed date, so each subject has its own fixed $C_i$.
2. **Type II.** $n$ units go on test together and the test stops at the $r$-th failure. The data are the first $r$ [order statistics](/order-statistic/) $T_{(1)} \le \cdots \le T_{(r)}$, and the other $n - r$ units are censored at $T_{(r)}$. Here $r$ is fixed and the duration is random.
3. **Random.** $C$ is a random variable, such as the time to loss to follow-up or to the end of the study for a subject who entered at a random time.

**Independent censoring.** Censoring is independent when, at each time $t$, the subjects still under observation have the same hazard as all subjects still alive:

$$P(t \le T < t + dt \mid T \ge t, C \ge t) = P(t \le T < t + dt \mid T \ge t).$$

This holds when $T$ and $C$ are independent, or independent given covariates that are in the model. With independent continuous $T$ and $C$, densities $f, g$ and survival functions $S, G$, a subject contributes $f(y) G(y)$ to the likelihood when $\delta = 1$ and $S(y) g(y)$ when $\delta = 0$. Censoring is noninformative when $G$ and $g$ do not involve the parameters of $T$; then the [likelihood](/likelihood-function/) for those parameters is

$$L = \prod_{i=1}^n f(y_i)^{\delta_i}\, S(y_i)^{1 - \delta_i} = \prod_{i=1}^n h(y_i)^{\delta_i}\, S(y_i),$$

with $h = f/S$ the hazard. Each event contributes its density, and each censored subject the probability of surviving past its censoring time.

**Independence cannot be tested.** Tsiatis (1975) showed that for every joint distribution of $(T, C)$ there is a pair of independent times $(T^*, C^*)$ that gives the same distribution of the observed $(Y, \delta)$. Data of the form $(Y, \delta)$ therefore cannot tell dependent censoring from independent censoring; the assumption has to come from how the study was run.

## Examples and non-examples

**A hand example.** Five subjects have observed times $2, 3^+, 5, 7^+, 8$: three events and two right-censored times.

- Under an exponential model with rate $\lambda$ the log-likelihood is $d \log\lambda - \lambda \sum_i y_i$, with $d = 3$ events and total time at risk $\sum_i y_i = 25$. The maximum likelihood estimate is $\hat\lambda = d / \sum_i y_i = 3/25 = 0.12$.
- Treating the censored times as events gives $5/25 = 0.2$, and dropping the censored subjects gives $3/(2 + 5 + 8) = 0.2$. Both overstate the rate: the first counts two deaths that did not happen, and the second throws away 10 units of event-free time.
- Without a model, $P(T > 6)$ is estimated by the Kaplan-Meier product $(1 - \frac15)(1 - \frac13) = \frac{8}{15} \approx 0.533$: five at risk at time 2 and three at time 5. Treating $3^+$ and $7^+$ as events gives $\frac25$, the fraction of the five times above 6, and dropping them gives $\frac13$, the fraction of $2, 5, 8$ above 6. Both are lower.

**Type II censoring.** Ten lamps go on test and the test stops at the fourth failure, at hours $40, 75, 90, 130$. The exponential estimate is $\hat\lambda = 4 / (40 + 75 + 90 + 130 + 6 \cdot 130) = 4/1115$ per hour, because the six survivors each add 130 hours at risk.

**Dependent censoring.** In a trial, patients whose condition worsens are withdrawn to receive another treatment, and are recorded as censored at withdrawal. The subjects who remain at risk are healthier than all survivors, and the Kaplan-Meier curve overstates survival. Nothing in $(Y, \delta)$ reveals this. Recording the reason for withdrawal, and using covariates that predict it, is the remedy.

**Non-examples.**

- **Truncation is not censoring.** A censored subject is in the sample with partial information about $T$. A truncated subject is not in the sample at all. Under left truncation, or delayed entry, a subject enters at age $V$ and is seen only if $T > V$, as in a study of residents of a retirement home who are recruited at entry, so deaths before entry leave no trace. The likelihood factor becomes $f(y)/S(v)$ or $S(y)/S(v)$, and the risk set at $t$ contains only the subjects with $V < t \le Y$. Ignoring left truncation overstates survival at early ages, because everyone in the sample has already survived to entry.
- **Death from another cause.** When a patient dies of a heart attack in a cancer study, treating the death as censoring estimates survival in a world without heart attacks, which needs independence between the causes and is often not the quantity of interest. The [competing risks](/competing-risks/) framework handles this.
- **Missing values.** A missing covariate is a [missing data](/missing-data-mechanism/) problem. Independent censoring plays a role close to that of missing at random, but censoring carries partial information, a lower bound on $T$, that a missing value does not.
- **Rounding.** Event times recorded to the nearest day are, strictly, interval censored, but when the intervals are short relative to the spread of $T$ they are usually treated as exact with ties.

## Related definitions

- **Survival and hazard.** The [survival function](/survival-function/) $S(t) = P(T > t)$ is the probability a censored subject contributes; the [hazard](/hazard-function/) is what independent censoring leaves unchanged among those at risk.
- **Risk set and counts.** With right censoring, at each distinct event time $t_j$ there are $n_j$ subjects at risk, with $Y_i \ge t_j$, and $d_j$ events. The [Kaplan-Meier](/kaplan-meier-estimator/) and [Nelson-Aalen](/nelson-aalen-estimator/) estimators and the [log-rank test](/log-rank-test/) are built from these counts alone.
- **Coarsened data.** Censoring is one form of coarsening, in which the exact value is replaced by a set that contains it. Interval data lead to the [Turnbull estimator](/turnbull-estimator/), an [EM](/expectation-maximization/) algorithm on the sets.
- **Maximum likelihood.** The likelihood above is the basis of [maximum likelihood](/maximum-likelihood-estimation/) for parametric survival models, and its nonparametric maximum is the Kaplan-Meier estimator.

## References
