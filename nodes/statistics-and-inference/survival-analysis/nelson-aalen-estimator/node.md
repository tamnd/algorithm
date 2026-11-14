---
tag: 2X5FTW
kind: algorithm
slug: nelson-aalen-estimator
name: Nelson-Aalen estimator
aliases:
- Nelson-Aalen cumulative hazard estimator
area: statistics-and-inference/survival-analysis
level: core
summary: Estimates the cumulative hazard as the sum over event times of the deaths over the number at risk. It is a counting process martingale estimator.
model: real-ram
complexity:
  vars: {n: the number of subjects}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1972
  people: [Wayne Nelson, Odd O. Aalen]
  note: Nelson proposed the estimate for hazard plotting of censored failure data in 1969 and 1972. Aalen (1978) derived it for counting processes with a multiplicative intensity and proved its properties with martingale methods.
prereqs: [hazard-function, censoring, martingale]
see_also: [kaplan-meier-estimator, greenwood-formula, breslow-estimator, cox-proportional-hazards-model, aalen-johansen-estimator, log-rank-test, competing-risks, poisson-distribution]
sources:
  - paper: "Wayne Nelson, Hazard plotting for incomplete failure data, Journal of Quality Technology 1(1), 1969"
    locator: pp. 27 to 52 (the cumulative hazard plot, with the sum of the reciprocals of the numbers at risk)
  - paper: "Wayne Nelson, Theory and applications of hazard plotting for censored failure data, Technometrics 14(4), 1972"
    locator: from p. 945 (the theory of the cumulative hazard estimate and its plots)
  - paper: doi:10.1214/aos/1176344247
    title: Odd Aalen, Nonparametric inference for a family of counting processes, Annals of Statistics 6(4), 1978
    locator: pp. 701 to 726 (the multiplicative intensity model, the estimator of the integrated intensity and its martingale properties)
  - book: isbn:9780387945194
    title: Per Kragh Andersen, Ørnulf Borgan, Richard D. Gill and Niels Keiding, Statistical Models Based on Counting Processes, Springer, 1993
    locator: Chapter IV (the Nelson-Aalen estimator, its variance estimators, the tie conventions and the large-sample theory)
  - book: isbn:9780387953991
    title: John P. Klein and Melvin L. Moeschberger, Survival Analysis, Techniques for Censored and Truncated Data, 2nd edition, Springer, 2003
    locator: Chapter 4 (the Nelson-Aalen estimator of the cumulative hazard with its variance and confidence intervals)
---

The Nelson-Aalen estimator estimates the cumulative hazard $H(t) = \int_0^t h(u)\,du$ of an event time from right-censored data. At each distinct event time $t_j$ it adds the number of events $d_j$ divided by the number $n_j$ still at risk:

$$\hat H(t) = \sum_{j:\, t_j \le t} \frac{d_j}{n_j}.$$

Each term estimates the [hazard](/hazard-function/) at $t_j$, the chance that a subject at risk has the event at that time, so the sum estimates the accumulated hazard. It uses the same table of $n_j$ and $d_j$ as the [Kaplan-Meier estimator](/kaplan-meier-estimator/), which multiplies $1 - d_j/n_j$ instead of adding $d_j/n_j$. Nelson-Aalen is the natural estimate when the quantity of interest is the hazard itself, for checking a parametric model by a plot, and for the baseline of the Cox model, where the [Breslow estimator](/breslow-estimator/) reduces to it when all coefficients are zero.

## In plain words

Follow a group of patients over time. Each time someone has the event, look at how many people were still being watched just before, and write down one divided by that number (or the number of events divided by it, if several happen at once). Keep a running total. The total grows fast when events happen among few people at risk, and slowly when they happen among many. It measures how much risk has built up so far. People who leave the study early count in the totals until the time they leave and then stop counting.

## The problem

**Input.** Observations $(y_i, \delta_i)$ for $i = 1, \ldots, n$, with $y_i = \min(T_i, C_i)$ the observed time and $\delta_i = 1\{T_i \le C_i\}$ the event indicator, as on the [censoring](/censoring/) page.

**Model.** The subjects are independent, and censoring is independent: given that a subject is at risk just before $t$, its chance of an event at $t$ is the hazard of $T$ at $t$ and does not depend on the censoring. In the counting process form, the number of observed events $N(t)$ has intensity $Y(t)\,h(t)$, where $Y(t) = \#\{i : y_i \ge t\}$ is the number at risk. This is Aalen's multiplicative intensity model.

**Output.** The distinct event times $t_j$ with $n_j = \#\{i : y_i \ge t_j\}$ and $d_j = \#\{i : y_i = t_j, \delta_i = 1\}$, the values $\hat H(t_j)$, and two variance estimates:

$$\hat\sigma^2_{P}(t) = \sum_{t_j \le t} \frac{d_j}{n_j^2}, \qquad \hat\sigma^2_{B}(t) = \sum_{t_j \le t} \frac{d_j(n_j - d_j)}{n_j^3}.$$

The first (Aalen's) treats the events at $t_j$ as Poisson, the second as binomial. They are close when every $d_j$ is small compared with $n_j$, and the first is always the larger.

## The algorithm

```pseudo id=main
NELSON-AALEN(y[1..n], δ[1..n])
L1  sort the indices 1..n by y
L2  r ← n;  H ← 0;  V ← 0;  out ← empty list
L3  i ← 1
L4  while i ≤ n
L5      t ← y of the i-th sorted index;  d ← 0;  c ← 0
L6      while i ≤ n and y of the i-th sorted index = t: add 1 to d if δ = 1, else to c;  i ← i + 1
L7      if d > 0 then H ← H + d/r;  V ← V + d/r²;  append (t, r, d, H, V) to out
L8      r ← r - d - c                            ▷ events and censorings at t leave after t
L9  return out
```

The structure is that of the Kaplan-Meier pass: a censored subject at $t$ is still in the risk set at $t$. The code also accumulates $\hat\sigma^2_B$ in line L7, and it has a second tie rule, `ties="sequential"`, which replaces $d/r$ by $1/r + 1/(r - 1) + \cdots + 1/(r - d + 1)$. That is the value obtained if the $d$ tied events are taken to happen one after another in a very short time. The survival estimate $\exp(-\hat H(t))$ is a separate function.

## Example

For the 6-MP arm of the leukemia trial (Freireich et al. 1963, as listed by Gehan 1965; the data are on the [Kaplan-Meier page](/kaplan-meier-estimator/)), the event times and the results are:

| $t_j$ | $n_j$ | $d_j$ | $d_j/n_j$ | $\hat H(t_j)$ | $\exp(-\hat H)$ | Kaplan-Meier | $\hat\sigma_P$ |
|---|---|---|---|---|---|---|---|
| 6 | 21 | 3 | 0.14286 | 0.14286 | 0.8669 | 0.8571 | 0.0825 |
| 7 | 17 | 1 | 0.05882 | 0.20168 | 0.8174 | 0.8067 | 0.1013 |
| 10 | 15 | 1 | 0.06667 | 0.26835 | 0.7646 | 0.7529 | 0.1213 |
| 13 | 12 | 1 | 0.08333 | 0.35168 | 0.7035 | 0.6902 | 0.1471 |
| 16 | 11 | 1 | 0.09091 | 0.44259 | 0.6424 | 0.6275 | 0.1730 |
| 22 | 7 | 1 | 0.14286 | 0.58545 | 0.5569 | 0.5378 | 0.2243 |
| 23 | 6 | 1 | 0.16667 | 0.75211 | 0.4714 | 0.4482 | 0.2795 |

Exactly, $\hat H(23) = 59071/78540$. At $t = 6$, with three tied events, $\hat\sigma^2_P = 3/441 = 0.00680$ and $\hat\sigma^2_B = 54/9261 = 0.00583$; the sequential tie rule gives $1/21 + 1/20 + 1/19 = 0.15025$ instead of $3/21 = 0.14286$. At every time $\exp(-\hat H)$ is above the Kaplan-Meier value, and the gap grows as $d_j/n_j$ grows. If the hazard were constant, $\hat H$ would grow linearly; here $\hat H(t)/t$ is about $0.024$ per week at $t = 6$ and $0.033$ at $t = 23$, but the late steps rest on risk sets of 6 and 7.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that the pass computes $\sum_{t_j \le t} d_j/n_j$ and the two variance sums, by the same invariant as for Kaplan-Meier. It then shows, for event times on a finite grid and under independent censoring, that $M(t) = \sum_{t_j \le t}(d_j - q_j n_j)$ is a martingale, where $q_j$ is the discrete hazard; that $E[\hat H(t)] = \sum_{t_j \le t} q_j P(n_j > 0)$, so the bias is $-\sum_{t_j \le t} q_j P(n_j = 0)$; and that $\hat H$ is the maximum likelihood estimate of the cumulative hazard $\sum_{t_j \le t} q_j$.

## Complexity

Line L1 sorts in $\Theta(n \log n)$ comparisons. Lines L4 to L8 handle each subject once with $O(1)$ arithmetic, in $\Theta(n)$. The total is $\Theta(n \log n)$ time and $\Theta(n)$ extra space in the [real RAM](/real-ram/) model, and $\Theta(n)$ if the data are already sorted. Every term is positive, so the floating-point sum has relative error at most about $k$ units in the last place for $k$ event times, with no cancellation.

## Properties

- **Martingale and bias.** In continuous time, $N(t) - \int_0^t Y(u)\,dH(u)$ is a martingale, and $\hat H(t) - H^*(t)$ with $H^*(t) = \int_0^t 1\{Y(u) > 0\}\,dH(u)$ is a martingale with mean zero (Aalen 1978). So $\hat H$ is unbiased for $H^*$, and $0 \le H(t) - E\hat H(t) \le H(t)\,P(Y(t) = 0)$, which is exponentially small in $n$ when $P(y_i \ge t) > 0$.
- **Variance.** The predictable variation of $\hat H - H^*$ is $\int_0^t 1\{Y > 0\}\,dH/Y$, estimated by $\hat\sigma^2_P(t)$. With ties, $\sum d_j(n_j - d_j)/(n_j^2(n_j - 1))$ is conditionally unbiased for the binomial variance; $\hat\sigma^2_B$ has $n_j$ in place of $n_j - 1$.
- **Large samples.** If $P(Y > \tau) > 0$, then $\sup_{t \le \tau}|\hat H(t) - H(t)| \to 0$ in probability, and $\sqrt n(\hat H - H)$ converges to a Gaussian martingale with variance $\int_0^t dH(u)/\pi(u)$ for continuous $H$, where $\pi(u) = P(y_i \ge u)$ (Andersen et al. 1993, Chapter IV).
- **Relation to Kaplan-Meier.** $\exp(-\hat H(t)) \ge \hat S_{KM}(t)$, because $e^{-x} \ge 1 - x$ term by term. The Kaplan-Meier estimate is the product integral of $\hat H$: $\hat S_{KM}(t) = \prod_{t_j \le t}(1 - \Delta\hat H(t_j))$. Both are consistent for $S$ in continuous time, where the hazard increments are small.
- **Maximum likelihood.** For a discrete model with hazards $q_j$ at the observed event times, $d_j/n_j$ is the MLE of $q_j$, and $\hat H$ is the MLE of $\sum q_j$.

The measured finite-sample behaviour, with $T \sim$ exponential with rate 1, independent $C \sim$ exponential with rate 0.5, $t$ with $S(t) = 0.5$ ($H(t) = 0.693$), $r = 10000$ replications and seed 1972:

| $n$ | mean of $\hat H$ | variance of $\hat H$ | mean of $\hat\sigma^2_P$ | mean of $\hat\sigma^2_B$ | plain 95% with $\hat\sigma_P$ | log-scale 95% |
|---|---|---|---|---|---|---|
| 20 | 0.690 | 0.0658 | 0.0642 | 0.0569 | 0.915 | 0.960 |
| 50 | 0.691 | 0.0253 | 0.0248 | 0.0238 | 0.933 | 0.949 |
| 200 | 0.691 | 0.00619 | 0.00610 | 0.00604 | 0.946 | 0.949 |

The log-scale interval is $\hat H \exp(\pm z\,\hat\sigma_P/\hat H)$. In the same runs, the mean of $\exp(-\hat H)$ was 0.517 at $n = 20$ against 0.502 for Kaplan-Meier, both for $S(t) = 0.5$.

## Variants and improvements

- **Tie rules.** The Breslow form $d_j/n_j$ and the sequential form $\sum_{l=0}^{d_j - 1} 1/(n_j - l)$. The second is larger and corresponds to events that are distinct but recorded at the same time.
- **Delayed entry.** With entry times $v_i$, use the risk set $\{i : v_i < t_j \le y_i\}$. The estimate is then of $H(t) - H(v)$.
- **Smoothed hazard.** A kernel smoother applied to the increments of $\hat H$ estimates the hazard $h(t)$ itself (Ramlau-Hansen 1983).
- **Covariates.** The [Breslow estimator](/breslow-estimator/) of the baseline cumulative hazard in the [Cox model](/cox-proportional-hazards-model/) replaces $n_j$ by $\sum_{i \in R_j} e^{\beta^{\mathsf T}x_i}$. Aalen's additive model gives covariate effects on the cumulative hazard scale.
- **Several states.** The Nelson-Aalen estimates of the transition hazards of a multi-state model, combined by a product integral, give the [Aalen-Johansen estimator](/aalen-johansen-estimator/) of the transition probabilities, used for [competing risks](/competing-risks/).

## When to use it

Use Nelson-Aalen when the hazard is of interest: to see whether it is constant ($\hat H$ linear in $t$), Weibull ($\log\hat H$ linear in $\log t$) or proportional between groups (parallel $\log\hat H$ curves). It is the building block for the cumulative incidence in competing risks and for the baseline hazard in regression. To estimate a survival probability, the [Kaplan-Meier estimator](/kaplan-meier-estimator/) is the standard choice; $\exp(-\hat H)$ is close to it when risk sets are large.

## Pitfalls

- **$\hat H$ is not a probability.** It can exceed 1, and it does when the curve continues long enough. $1 - \exp(-\hat H)$, not $\hat H$, is a probability.
- **Slope, not level.** The hazard is the slope of $H$. A large $\hat H(t)$ means much risk accumulated, not a high current hazard.
- **Ties in grouped data.** With coarse time units many events share a time, and the two tie rules and the two variance estimates differ. Report which one is used.
- **Plain intervals near zero.** For small $\hat H$ the interval $\hat H \pm z\hat\sigma$ can go below 0 and undercovers. Use the log-scale interval.
- **The right tail.** Late steps rest on few subjects and have large variance; $\hat\sigma^2_P$ grows by $d_j/n_j^2$ at each step.
- **Independent censoring.** As for Kaplan-Meier, dependent censoring biases $\hat H$, and the data cannot reveal it.

## Implementations

## History

Wayne Nelson, an engineer at General Electric, introduced the cumulative hazard plot for censored failure data in 1969 and gave its theory in Technometrics in 1972: one plots the running sum of $1/n_j$ against time on paper scaled for a parametric family and reads off whether the family fits. Odd Aalen, in his 1975 Berkeley thesis and his 1978 Annals paper, placed the estimate in the theory of counting processes: for any counting process with intensity $Y(t)h(t)$, the estimator of $\int h$ is a martingale transform, and martingale central limit theorems give its large-sample laws. This view, developed further by Gill and by Andersen, Borgan and Keiding, became the basis of modern survival analysis.

## References
