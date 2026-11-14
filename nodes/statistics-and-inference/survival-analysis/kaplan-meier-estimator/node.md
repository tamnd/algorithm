---
tag: FNVF5H
kind: algorithm
slug: kaplan-meier-estimator
name: Kaplan-Meier estimator
aliases:
- product-limit estimator
area: statistics-and-inference/survival-analysis
level: core
summary: Estimates the survival function under right censoring as the product over event times of one minus the deaths over the number at risk. It is the nonparametric MLE.
model: real-ram
complexity:
  vars: {n: the number of subjects, k: the number of distinct event times}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1958
  people: [Edward L. Kaplan, Paul Meier]
  note: Kaplan and Meier published the product-limit estimate, its variance and its maximum likelihood property in JASA in 1958. Efron (1967) gave the redistribute-to-the-right construction and the self-consistency equation.
prereqs: [censoring, survival-function, empirical-distribution-function, maximum-likelihood-estimation]
see_also: [greenwood-formula, nelson-aalen-estimator, log-rank-test, turnbull-estimator, hazard-function, aalen-johansen-estimator, cox-proportional-hazards-model, breslow-estimator]
sources:
  - paper: doi:10.1080/01621459.1958.10501452
    title: E. L. Kaplan and Paul Meier, Nonparametric estimation from incomplete observations, Journal of the American Statistical Association 53(282), 1958
    locator: pp. 457 to 481 (the product-limit estimate, its derivation as a maximum likelihood estimate, and its variance)
  - paper: "Bradley Efron, The two sample problem with censored data, Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, Vol. 4, University of California Press, 1967"
    locator: pp. 831 to 853 (the redistribute-to-the-right construction and self-consistency on pp. 842 and 843)
  - book: isbn:9780387953991
    title: John P. Klein and Melvin L. Moeschberger, Survival Analysis, Techniques for Censored and Truncated Data, 2nd edition, Springer, 2003
    locator: Chapter 4 (nonparametric estimation of basic quantities for right-censored and left-truncated data)
  - book: isbn:9780387945194
    title: Per Kragh Andersen, Ørnulf Borgan, Richard D. Gill and Niels Keiding, Statistical Models Based on Counting Processes, Springer, 1993
    locator: Chapter IV (nonparametric estimation, including the product-limit estimator, its consistency and its weak convergence)
---

The Kaplan-Meier estimator estimates the [survival function](/survival-function/) $S(t) = P(T > t)$ from data in which some event times are right censored: for those subjects we know only that the event had not happened by the time follow-up stopped. At each distinct event time $t_j$ it counts the $n_j$ subjects still at risk and the $d_j$ events, estimates the conditional probability of getting past $t_j$ as $1 - d_j/n_j$, and multiplies these factors:

$$\hat S(t) = \prod_{j:\, t_j \le t} \left(1 - \frac{d_j}{n_j}\right).$$

A censored subject counts in every risk set up to its censoring time and then leaves without causing a step. With no censoring, $\hat S$ is one minus the [empirical distribution function](/empirical-distribution-function/). Under [independent censoring](/censoring/) $\hat S$ is the nonparametric maximum likelihood estimate of $S$, and the computation is one sort and one pass.

## In plain words

Patients enter a study and are followed until they die or until the study stops watching them. For a patient who left the study alive after 10 weeks, we do not know the death time, only that it is later than 10 weeks. To estimate the chance of surviving past 20 weeks, go through time in order. Each time someone dies, look at the people who were still being followed just before, and note the fraction who survived that moment. Multiply these fractions together. A person who left early helps in every fraction up to the time they left, and then drops out of the count. Throwing that person away, or counting them as dead, would both make survival look worse than it is.

## The problem

**Input.** Observations $(y_i, \delta_i)$ for $i = 1, \ldots, n$, where $y_i = \min(T_i, C_i)$ is the observed time, $T_i$ the event time, $C_i$ the censoring time, and $\delta_i = 1$ if $T_i \le C_i$ (an event) and $0$ otherwise (censored).

**Model.** The pairs $(T_i, C_i)$ are independent across $i$, the $T_i$ have survival function $S$, and censoring is independent: given that a subject is still at risk at time $t$, the chance of an event at $t$ does not depend on the censoring. No form of $S$ is assumed. The [censoring](/censoring/) page states these conditions in full.

**Output.** The distinct event times $t_1 < \cdots < t_k$, with $n_j = \#\{i : y_i \ge t_j\}$ at risk and $d_j = \#\{i : y_i = t_j, \delta_i = 1\}$ events at each, and the values $\hat S(t_j)$. The estimate is the right-continuous step function that equals $1$ before $t_1$ and $\hat S(t_j)$ on $[t_j, t_{j+1})$.

**Ties.** A censoring time equal to an event time counts as later: the censored subject is in the risk set $n_j$. This is the convention of Kaplan and Meier, and it matches the usual reading that a subject censored at $t$ was seen alive at $t$.

## The algorithm

```pseudo id=main
KAPLAN-MEIER(y[1..n], δ[1..n])
L1  sort the indices 1..n by y
L2  r ← n;  S ← 1;  out ← empty list
L3  i ← 1
L4  while i ≤ n
L5      t ← y of the i-th sorted index;  d ← 0;  c ← 0
L6      while i ≤ n and y of the i-th sorted index = t: add 1 to d if δ = 1, else to c;  i ← i + 1
L7      if d > 0 then S ← S · (1 - d/r);  append (t, r, d, S) to out
L8      r ← r - d - c                            ▷ the d + c subjects leave the risk set after t
L9  return out
```

Line L1 sorts the times. The variable $r$ is the size of the current risk set; it starts at $n$ and line L8 removes each group of tied subjects after their time is processed, so censored subjects at $t$ are still counted at $t$. Line L7 makes a step only at event times. The code returns the list of steps together with the largest observed time $y_{(n)}$, and evaluates $\hat S(t)$ by a scan or a binary search over the steps.

If the largest observation is censored, $\hat S$ does not reach $0$, and the data say nothing about $S$ beyond $y_{(n)}$: the code raises an error for $t > y_{(n)}$ in that case. If the largest observation is an event, $\hat S$ drops to $0$ there.

## Example

The 6-MP arm of the leukemia trial of Freireich et al. (1963), as listed by Gehan (1965), has 21 remission times in weeks, with $+$ marking a censored time:

6, 6, 6, 6+, 7, 9+, 10, 10+, 11+, 13, 16, 17+, 19+, 20+, 22, 23, 25+, 32+, 32+, 34+, 35+.

The pass of lines L4 to L8 visits 16 distinct times. The rows with $d > 0$ form the output:

| $t$ | $r$ at $t$ | $d$ | $c$ | factor $1 - d/r$ | $\hat S(t)$ | decimal |
|---|---|---|---|---|---|---|
| 6 | 21 | 3 | 1 | 18/21 | 6/7 | 0.8571 |
| 7 | 17 | 1 | 0 | 16/17 | 96/119 | 0.8067 |
| 9 | 16 | 0 | 1 | none | 96/119 | 0.8067 |
| 10 | 15 | 1 | 1 | 14/15 | 64/85 | 0.7529 |
| 11 | 13 | 0 | 1 | none | 64/85 | 0.7529 |
| 13 | 12 | 1 | 0 | 11/12 | 176/255 | 0.6902 |
| 16 | 11 | 1 | 0 | 10/11 | 32/51 | 0.6275 |
| 17, 19, 20 | 10, 9, 8 | 0 | 1 each | none | 32/51 | 0.6275 |
| 22 | 7 | 1 | 0 | 6/7 | 64/119 | 0.5378 |
| 23 | 6 | 1 | 0 | 5/6 | 160/357 | 0.4482 |
| 25, 32, 34, 35 | 5, 4, 2, 1 | 0 | 1, 2, 1, 1 | none | 160/357 | 0.4482 |

At $t = 6$ the censored subject is in the risk set of 21, and only after the step does $r$ fall by $d + c = 4$ to 17. The estimated median remission time, the first $t$ with $\hat S(t) \le 1/2$, is 23 weeks. The last observation, 35, is censored, so $\hat S$ stays at $160/357$ up to 35 and is undefined after it. The [Greenwood formula](/greenwood-formula/) gives standard errors 0.0764 at $t = 6$ and 0.1346 at $t = 23$.

The two wrong ways to treat the censored times give quite different answers. If the 12 censored times are dropped, the 9 events alone have empirical median 10 weeks. If they are counted as events, the median is 16 weeks and the estimate at 23 weeks is $5/21 = 0.238$ instead of $0.448$. Both are biased downward, because both lose the information that the censored patients were still in remission.

The placebo arm of the same trial has no censoring (1, 1, 2, 2, 3, 4, 4, 5, 5, 8, 8, 8, 8, 11, 11, 12, 12, 15, 17, 22, 23). Its Kaplan-Meier estimate is the empirical survival function $\#\{y_i > t\}/21$: $19/21$ after week 1, $16/21$ after week 3, $8/21$ after week 8, and median 8 weeks. The [log-rank test](/log-rank-test/) compares the two arms.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows three things. First, the pass of lines L4 to L8 keeps the invariant that $r$ equals the number of subjects with $y_i \ge t$ when the group at time $t$ starts, so every output row is $(t_j, n_j, d_j, \prod_{l \le j}(1 - d_l/n_l))$. Second, under a likelihood that does not involve the censoring distribution, the product-limit estimate maximizes the likelihood over all distributions on $(0, \infty]$, and it is the unique maximizer on $[0, y_{(n)}]$. Third, it equals Efron's redistribute-to-the-right estimate, in which each censored subject passes its probability mass in equal shares to every subject later in time.

## Complexity

The sort in line L1 costs $\Theta(n \log n)$ comparisons in the worst case. The pass of lines L4 to L8 visits each subject once and does $O(1)$ arithmetic per subject and per distinct time, so it costs $\Theta(n)$. The output has $k \le n$ rows. The total is $\Theta(n \log n)$ time and $\Theta(n)$ extra space in the [real RAM](/real-ram/) model. If the data arrive sorted, the cost is $\Theta(n)$. After the pass, a value $\hat S(t)$ costs $O(\log k)$ by a binary search over the step times.

With exact rational arithmetic the numbers grow: the denominator of $\hat S(t_j)$ divides $n_1 n_2 \cdots n_j$, so the bit size of $\hat S$ can grow linearly in $k$. In floating point the product of $k$ factors in $(0, 1]$ has a relative error of at most about $3k$ units in the last place (one rounding each for $d/r$, the subtraction and the product), and no cancellation grows the error. For very long products the sum of $\log(1 - d_j/n_j)$, computed with `log1p`, avoids underflow.

## Properties

- **No censoring.** If every $\delta_i = 1$, then $n_{j+1} = n_j - d_j$, the product telescopes, and $\hat S(t) = \#\{i : y_i > t\}/n$, one minus the empirical distribution function.
- **Self-consistency.** For $t \le y_{(n)}$, $\hat S(t) = \frac{1}{n}\left[\#\{i : y_i > t\} + \sum_{i:\, \delta_i = 0,\, y_i \le t} \frac{\hat S(t)}{\hat S(y_i)}\right]$. Each censored subject contributes its conditional probability of being still alive at $t$, estimated by $\hat S$ itself (Efron 1967). The [Turnbull estimator](/turnbull-estimator/) solves the same kind of equation for interval-censored data.
- **Nonparametric MLE.** It maximizes the likelihood $\prod_i P(T = y_i)^{\delta_i} P(T > y_i)^{1 - \delta_i}$ over all distributions, as proved in the correctness file.
- **Consistency and limit law.** If $P(Y > \tau) > 0$, then $\sup_{t \le \tau} |\hat S(t) - S(t)| \to 0$ almost surely, and $\sqrt{n}(\hat S - S)$ converges on $[0, \tau]$ to a Gaussian process with variance $S(t)^2 \int_0^t \frac{dF(u)}{S(u)\, S(u-)\, G(u-)}$ for continuous $S$, where $G$ is the censoring survival function (Breslow and Crowley 1974; Andersen et al. 1993, Chapter IV). The [Greenwood formula](/greenwood-formula/) estimates this variance.
- **Relation to Nelson-Aalen.** $\exp(-\hat H(t)) \ge \hat S(t)$, where $\hat H$ is the [Nelson-Aalen estimator](/nelson-aalen-estimator/), because $e^{-x} \ge 1 - x$ for every factor. The two agree closely when every $d_j / n_j$ is small.

## Variants and improvements

- **Delayed entry (left truncation).** If subject $i$ enters observation at time $v_i$, the risk set at $t_j$ is $\{i : v_i < t_j \le y_i\}$. The same product with these $n_j$ estimates $S(t)/S(v)$ for $t > v = \min_i v_i$. Small risk sets early in time can make this estimate unstable.
- **Life-table (actuarial) estimate.** For grouped data in intervals, use $n_j - c_j/2$ as the effective number at risk, on the reading that censored subjects were at risk for half the interval.
- **Survival from the cumulative hazard.** $\exp(-\hat H(t))$, with $\hat H$ the Nelson-Aalen estimate, is an alternative estimate of $S$. It never reaches $0$.
- **Interval censoring.** When event times are known only to lie in intervals, the nonparametric MLE is the [Turnbull estimator](/turnbull-estimator/), which reduces to Kaplan-Meier for exact and right-censored data.
- **Competing risks.** With several causes of failure, $1 - \hat S$ computed with the other causes treated as censoring overestimates the cumulative incidence of one cause. The [Aalen-Johansen estimator](/aalen-johansen-estimator/) gives the correct estimate; see [competing risks](/competing-risks/).
- **Covariates.** The [Cox model](/cox-proportional-hazards-model/) with the [Breslow estimator](/breslow-estimator/) gives a survival curve for each covariate value. Without covariates it reduces to $\exp(-\hat H)$.
- **Dependent censoring.** If censoring depends on measured covariates, inverse probability of censoring weights, in the style of [inverse probability weighting](/inverse-probability-weighting/), restore consistency.

## When to use it

Use Kaplan-Meier to describe the survival of one group with right-censored data, to read off the median survival time or the survival probability at a fixed time, and as the first plot of any survival analysis. Report the number at risk under the plot, because the right end of the curve rests on few subjects. To compare groups, use the [log-rank test](/log-rank-test/), not the visual gap between curves. For pointwise confidence intervals use the [Greenwood formula](/greenwood-formula/), preferably on the log-log scale.

## Pitfalls

- **Dropping censored subjects, or treating them as events.** Both bias $\hat S$ downward, as the 6-MP example shows: medians of 10 and 16 weeks against 23.
- **Ties between events and censorings.** Count a censoring at $t_j$ in the risk set at $t_j$. Removing it first changes the factor at $t_j$.
- **The tail.** After the largest time, if it is censored, the estimate is undefined. The mean survival time $\int_0^\infty \hat S(t)\, dt$ is then undefined too; report the restricted mean $\int_0^\tau \hat S(t)\, dt$ with a stated $\tau$.
- **Informative censoring.** If sicker patients leave the study earlier, $\hat S$ is biased upward, and the data cannot reveal this (Tsiatis 1975): the bias is not testable from $(y_i, \delta_i)$ alone.
- **Competing risks.** Treating death from other causes as censoring and reporting $1 - \hat S$ as the risk of one cause overestimates that risk.
- **Large steps at the end.** When few subjects remain at risk, each event causes a large drop. Do not read the shape of the curve where $n_j$ is small.
- **Median.** If $\hat S$ never falls to $1/2$, the median is not estimable, and the code returns no value. Do not replace it with the last time.

## Implementations

## History

Edward Kaplan and Paul Meier each wrote a paper on the estimation of survival from incomplete observations, and they published them as one joint paper in the Journal of the American Statistical Association in 1958. The paper gives the product-limit estimate, shows that it is the maximum likelihood estimate among all distributions, and derives its variance by the same argument as Greenwood (1926). Actuaries had long used products of conditional survival probabilities in life tables. Efron (1967) gave the redistribute-to-the-right description and the self-consistency equation while studying two-sample tests with censored data. Breslow and Crowley (1974) proved the weak convergence of $\sqrt{n}(\hat S - S)$, and the counting process approach of Aalen and of Gill in the late 1970s and early 1980s gave the martingale proofs collected by Andersen, Borgan, Gill and Keiding (1993).

## References
