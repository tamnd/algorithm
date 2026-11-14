---
tag: V69XGW
kind: definition
slug: schoenfeld-residuals
name: Schoenfeld residuals
aliases:
- scaled Schoenfeld residuals
area: statistics-and-inference/survival-analysis
level: advanced
summary: For each event, the covariate of the unit that failed minus its risk-weighted mean over the risk set. A trend in time signals a failure of proportional hazards.
prereqs: [cox-proportional-hazards-model, cox-partial-likelihood]
see_also: [breslow-estimator, score-test, log-rank-test, hazard-function, accelerated-failure-time-model, frailty-model, martingale]
sources:
  - paper: doi:10.1093/biomet/69.1.239
    title: David Schoenfeld, Partial residuals for the proportional hazards regression model, Biometrika 69(1), 1982
    locator: pp. 239 to 241 (the definition of the residuals and their use to check proportional hazards)
  - paper: doi:10.1093/biomet/81.3.515
    title: Patricia M. Grambsch and Terry M. Therneau, Proportional hazards tests and diagnostics based on weighted residuals, Biometrika 81(3), 1994
    locator: pp. 515 to 526 (the scaled residuals, their approximate expectation beta(t), and the score tests of proportional hazards)
  - book: isbn:9780387987842
    title: Terry M. Therneau and Patricia M. Grambsch, Modeling Survival Data, Extending the Cox Model, Springer, 2000
    locator: Chapter 6 (testing proportional hazards with the scaled Schoenfeld residuals, with worked examples and plots)
---

Schoenfeld residuals are the residuals of a fitted [Cox model](/cox-proportional-hazards-model/) that belong to the event times, not to the subjects. At each event, they compare the covariate vector of the subject that had the event with the average covariate vector of the risk set, weighted by the relative risks $\exp(\beta^{\mathsf T}x_i)$. Their sum is the score of the [partial likelihood](/cox-partial-likelihood/), so they sum to zero at the estimate. If the proportional hazards assumption holds, they show no trend in time. Plotted against time after scaling, they estimate how the coefficient $\beta(t)$ of a covariate changes in time, and a regression on a function of time gives a test of proportional hazards.

## Definition

Fit a Cox model to data $(y_i, \delta_i, x_i)$, $i = 1, \ldots, n$, with $x_i \in \mathbb{R}^p$, and let $\beta$ be a coefficient vector, usually the estimate $\hat\beta$. For a time $t$ let $R(t) = \{i : y_i \ge t\}$ be the risk set and

$$\bar x(\beta, t) = \frac{\sum_{i \in R(t)} x_i \exp(\beta^{\mathsf T}x_i)}{\sum_{i \in R(t)} \exp(\beta^{\mathsf T}x_i)}, \qquad V(\beta, t) = \frac{\sum_{i \in R(t)} (x_i - \bar x)(x_i - \bar x)^{\mathsf T}\exp(\beta^{\mathsf T}x_i)}{\sum_{i \in R(t)} \exp(\beta^{\mathsf T}x_i)},$$

the weighted mean and covariance of the covariates over the risk set. Under the model, if one event happens at $t$, the subject that has it is $i \in R(t)$ with probability $\pi_i = \exp(\beta^{\mathsf T}x_i)/\sum_{l \in R(t)}\exp(\beta^{\mathsf T}x_l)$, so $\bar x$ and $V$ are the mean and covariance of the covariate of the subject that has the event.

**Schoenfeld residual.** For each subject $i$ with an event ($\delta_i = 1$),

$$r_i = x_i - \bar x(\hat\beta, y_i) \in \mathbb{R}^p.$$

There is one residual vector per event and none for a censored subject. With tied events, each of the $d_j$ subjects at $t_j$ gets its own residual against the same $\bar x(\hat\beta, t_j)$, which matches the Breslow rule for ties.

**They sum to the score.** For every $\beta$, $\sum_{i:\,\delta_i = 1}\bigl(x_i - \bar x(\beta, y_i)\bigr) = U(\beta)$, the score of the Breslow partial likelihood. *Proof.* The log partial likelihood is $\ell(\beta) = \sum_{i:\,\delta_i = 1}\bigl(\beta^{\mathsf T}x_i - \log\sum_{l \in R(y_i)}\exp(\beta^{\mathsf T}x_l)\bigr)$, and the gradient of the $\log\sum$ term is $\bar x(\beta, y_i)$. $\square$ So at the estimate, where $U(\hat\beta) = 0$, the residuals sum to the zero vector. They are not independent, but they are nearly uncorrelated across event times, as the increments of a martingale are.

**Scaled Schoenfeld residuals.** Let $D$ be the number of events and $\widehat{\operatorname{Var}}(\hat\beta) = \mathcal I(\hat\beta)^{-1}$ the inverse of the information matrix. Grambsch and Therneau (1994) define

$$r_i^* = \hat\beta + D\,\mathcal I(\hat\beta)^{-1} r_i.$$

The exact scaling is $r_i^* = \hat\beta + V(\hat\beta, y_i)^{-1}r_i$. Since $\mathcal I(\hat\beta) = \sum_i V(\hat\beta, y_i)$, replacing each $V$ by the average $\mathcal I/D$ gives the form above, which is stable even when one risk set is small. If the coefficient changes in time, as $\beta(t) = \beta + \theta g(t)$ for a known function $g$, then $E[r_i^*] \approx \beta(y_i)$. A smooth of $r_i^*$ against time, or against $\log t$ or the rank of $t$, estimates $\beta(t)$. A flat line is what proportional hazards predicts.

**The test of proportional hazards.** The score test of $\theta = 0$ in $\beta(t) = \beta + \theta g(t)$, for one covariate, is close to

$$T = \frac{D\bigl(\sum_i (g_i - \bar g)\, r_i\bigr)^2}{\mathcal I(\hat\beta)\sum_i (g_i - \bar g)^2},$$

with $g_i = g(y_i)$ and $\bar g$ their mean over the events. $T$ is approximately $\chi^2_1$ under proportional hazards, and it is $D$ times the squared correlation statistic between the scaled residuals and $g$ in the sense of Grambsch and Therneau. The exact score test replaces $\mathcal I$ by the full information of $(\beta, \theta)$.

## Examples and non-examples

**A hand example.** Five subjects with times $1, 2, 3^+, 4, 5$ and $x = 1, 0, 1, 0, 1$. There are four events, so four residuals.

- At $\beta = 0$ the risk-set means are $3/5, 1/2, 1/2, 1$ at times $1, 2, 4, 5$, so the residuals are $2/5, -1/2, -1/2, 0$. They sum to $-3/5 = U(0)$.
- At $\hat\beta = -0.8341$ the residuals are $0.6056, -0.3028, -0.3028, 0$, which sum to $0$. The scaled residuals, with $D = 4$ and $\mathcal I(\hat\beta)^{-1} = 1.5127$, are $2.830, -2.666, -2.666, -0.834$.
- The residual at time 5 is $0$ for every $\beta$, because the risk set has one member. The last event time often gives a zero residual, and its scaled residual is $\hat\beta$ itself.

**The leukemia data.** For the Gehan data with $x = 1$ for placebo and the Breslow-ties fit $\hat\beta = 1.5092$, there are 30 residuals, and they sum to $2 \times 10^{-15}$, zero up to rounding. At $t = 1$ both events are on placebo and the weighted mean is $21 \cdot 4.5231/115.98 = 0.8189$, so both residuals are $0.1811$, and their scaled value is $1.509 + 30 \cdot 0.1677 \cdot 0.1811 = 2.420$. The tests of proportional hazards give:

| $g(t)$ | $T$ above | p-value | exact score test | p-value |
|---|---|---|---|---|
| $t$ | 0.0187 | 0.891 | 0.0176 | 0.894 |
| $\log t$ | 0.321 | 0.571 | 0.348 | 0.555 |

There is no sign that the effect of placebo changes over the 23 weeks. The values were computed by the reference code of the partial likelihood page.

**A model that is not proportional.** If the hazard ratio of a treatment falls from 4 early to 1 late, the residuals of the treated subjects are positive among the early events and near zero or negative among the late ones. The scaled residuals then trend down from about $\log 4$ toward $0$, and the test with $g(t) = t$ detects the trend when there are enough events. The [frailty model](/frailty-model/) gives one mechanism for such a decline.

**Non-examples.**

- **Martingale residuals** are not Schoenfeld residuals. They are defined per subject, $\delta_i - \exp(\hat\beta^{\mathsf T}x_i)\hat H_0(y_i)$, with $\hat H_0$ the [Breslow estimator](/breslow-estimator/), they exist for censored subjects, and they check the functional form of a covariate, not proportional hazards.
- **Score residuals** are per subject too. They add to each subject's Schoenfeld term the changes in $\bar x$ over the times it was at risk, and they are used for influence and for robust variances.
- **A raw difference of Kaplan-Meier curves** is not a residual. Crossing curves suggest non-proportional hazards, but they do not adjust for the other covariates.

## Related definitions

- **Score and information.** The residuals add up to the [score](/score-function/) $U(\beta)$, and $\sum_i V(\beta, y_i) = \mathcal I(\beta)$ is the information of the Breslow partial likelihood. At $\beta = 0$ with one binary covariate the sum is $O - E$ of the [log-rank test](/log-rank-test/).
- **Cumulative sums.** The process $\sum_{y_i \le t} r_i$, a sum of martingale-like increments, is the basis of the Lin, Wei and Ying tests of proportional hazards, which compare it with simulated paths under the model.
- **Time-varying coefficients.** The model $h(t \mid x) = h_0(t)\exp(\beta(t)^{\mathsf T}x)$ is the alternative that the scaled residuals estimate. Fitting it with $x\,g(t)$ as an extra time-dependent covariate gives the exact score test of the table.
- **Stratification.** If a covariate fails the check, a common remedy is to stratify on it, so that each stratum has its own baseline hazard, as described on the [Cox model](/cox-proportional-hazards-model/) page.
- **Accelerated failure time.** When the hazard ratio drifts in time but the survival curves look like stretched copies of each other, an [accelerated failure time model](/accelerated-failure-time-model/) may fit better.

## References
