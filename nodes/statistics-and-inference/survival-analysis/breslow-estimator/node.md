---
tag: NMKKND
kind: algorithm
slug: breslow-estimator
name: Breslow estimator
aliases:
- Breslow baseline hazard estimator
area: statistics-and-inference/survival-analysis
level: advanced
summary: Estimates the cumulative baseline hazard of a Cox model by summing the deaths over the risk-weighted sum of exp(x^T beta) of those at risk at each event time.
model: real-ram
complexity:
  vars: {n: the number of subjects, k: the number of distinct event times, p: the number of covariates}
  time: {worst: Θ(n log n + n p)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1974
  people: [Norman E. Breslow]
  note: Breslow gave the estimate in his 1972 discussion of Cox's paper and in Biometrics in 1974, as the maximum likelihood estimate of a baseline hazard that is constant between event times. Tsiatis (1981) and Andersen and Gill (1982) proved its large-sample properties.
prereqs: [cox-proportional-hazards-model, cox-partial-likelihood, nelson-aalen-estimator, maximum-likelihood-estimation]
see_also: [kaplan-meier-estimator, schoenfeld-residuals, survival-function, hazard-function, prefix-sums, fine-gray-model, frailty-model, harrell-c-index]
sources:
  - paper: doi:10.2307/2529620
    title: N. E. Breslow, Covariance analysis of censored survival data, Biometrics 30(1), 1974
    locator: pp. 89 to 99 (the estimate of the baseline hazard and its derivation as a maximum likelihood estimate)
  - paper: doi:10.1214/aos/1176345335
    title: Anastasios A. Tsiatis, A large sample study of Cox's regression model, Annals of Statistics 9(1), 1981
    locator: pp. 93 to 108 (the joint asymptotic normality of the coefficient estimate and the estimated cumulative baseline hazard, with the variance term from estimating beta)
  - paper: doi:10.1214/aos/1176345976
    title: Per Kragh Andersen and Richard D. Gill, Cox's regression model for counting processes, a large sample study, Annals of Statistics 10(4), 1982
    locator: pp. 1100 to 1120 (the martingale proof of the weak convergence of the Breslow estimator)
  - paper: doi:10.1080/01621459.1977.10480613
    title: Bradley Efron, The efficiency of Cox's likelihood function for censored data, Journal of the American Statistical Association 72(359), 1977
    locator: pp. 557 to 565 (the approximation for tied times, which gives the Efron form of the increment)
  - book: isbn:9780387987842
    title: Terry M. Therneau and Patricia M. Grambsch, Modeling Survival Data, Extending the Cox Model, Springer, 2000
    locator: Chapters 3 and 4 (estimation of the baseline hazard and survival curves after a Cox fit, and residuals)
---

The Breslow estimator turns a fitted [Cox model](/cox-proportional-hazards-model/) into survival curves. The [partial likelihood](/cox-partial-likelihood/) estimates $\beta$ but says nothing about the baseline hazard $h_0$. Given $\beta$, Breslow's estimate of the cumulative baseline hazard $H_0(t) = \int_0^t h_0(u)\,du$ is

$$\hat H_0(t) = \sum_{j:\, t_j \le t} \frac{d_j}{\sum_{i \in R(t_j)} \exp(\beta^{\mathsf T}x_i)},$$

where $t_j$ are the distinct event times, $d_j$ the number of events at $t_j$ and $R(t_j) = \{i : y_i \ge t_j\}$ the risk set. The survival curve for covariate $x$ is then $\hat S(t \mid x) = \exp\bigl(-\hat H_0(t)\, e^{\beta^{\mathsf T}x}\bigr)$. At $\beta = 0$ the estimate is the [Nelson-Aalen estimator](/nelson-aalen-estimator/). One sort and one backward pass of running sums compute it in $\Theta(n \log n)$ time.

## In plain words

The Nelson-Aalen estimator adds, at each event time, the number of events divided by the number of people at risk. In a Cox model people at risk are not equal: someone with relative risk 3 counts like three people with relative risk 1. So the Breslow estimator divides the number of events by the sum of the relative risks of the people at risk. The result is the cumulative hazard of a person whose covariates are all zero. Multiply it by a person's relative risk to get that person's cumulative hazard, and take $e$ to minus that to get their survival curve.

## The problem

**Input.** Observations $(y_i, \delta_i, x_i)$ for $i = 1, \ldots, n$, where $y_i$ is the observed time, $\delta_i = 1$ for an event and $0$ for a censored time, and $x_i \in \mathbb{R}^p$. A coefficient vector $\beta$, usually the Cox estimate $\hat\beta$. The code takes the risk scores $w_i = \exp(\beta^{\mathsf T}x_i)$, which cost $O(np)$ to compute.

**Model.** The hazard of subject $i$ is $h_0(t) w_i$ with $h_0$ unspecified, and censoring is independent, as on the [censoring](/censoring/) page.

**Output.** The distinct event times $t_1 < \cdots < t_k$, and at each the risk sum $S_j = \sum_{i \in R(t_j)} w_i$, the count $d_j$, the increment, $\hat H_0(t_j)$, and the variance term $\sum_{l \le j} d_l/S_l^2$. $\hat H_0$ is the right-continuous step function with these values, $0$ before $t_1$.

**Ties.** A censored time equal to an event time counts as at risk at that time. With tied events the Breslow rule adds $d_j/S_j$. The Efron rule, which matches the Efron partial likelihood, adds $\sum_{r=0}^{d_j - 1} 1/(S_j - \frac{r}{d_j}D_j)$, where $D_j$ is the sum of $w_i$ over the $d_j$ subjects with the event.

## The algorithm

```pseudo id=main
BRESLOW(y[1..n], δ[1..n], w[1..n], ties)
L1  sort the indices 1..n by decreasing y
L2  S ← 0;  rows ← empty list
L3  for each distinct time t in that order
L4      for each i with y_i = t:  S ← S + w_i;  if δ_i = 1 then d ← d + 1, D ← D + w_i
L5      if d > 0 then append (t, S, d, D) to rows
L6  reverse rows                                  ▷ now in increasing time
L7  H ← 0;  V ← 0;  for each (t, S, d, D) in rows
L8      inc ← d / S   (Efron: Σ_{r<d} 1 / (S - rD/d))
L9      H ← H + inc;  V ← V + d / S²;  output (t, S, d, inc, H, V)
```

Line L1 sorts once. Lines L3 and L4 visit the times from the largest down, so $S$ is a running sum that only grows: when the group at time $t$ is done, $S = \sum_{y_i \ge t} w_i$, which is exactly the risk sum at $t$. The counters $d$ and $D$ start at $0$ for each group. Line L5 keeps only event times. Lines L7 to L9 then add the increments in time order. $V$ estimates the variance of $\hat H_0(t)$ when $\beta$ is known.

## Example

**A small example.** Times $1, 2, 3^+, 4, 5$ with $x = 1, 0, 1, 0, 1$. At $\beta = 0$ all $w_i = 1$, the risk sums are $5, 4, 2, 1$ at the event times $1, 2, 4, 5$, and

$$\hat H_0 = \tfrac15,\quad \tfrac15 + \tfrac14 = \tfrac{9}{20},\quad \tfrac{9}{20} + \tfrac12 = \tfrac{19}{20},\quad \tfrac{19}{20} + 1 = \tfrac{39}{20},$$

the Nelson-Aalen estimate. There are no tied events, so the Efron rule gives the same values.

**The leukemia data.** The Gehan data have 21 patients on 6-MP and 21 on placebo, with 30 events at 17 distinct times. Take $x = 1$ for placebo and the Breslow-ties estimate $\hat\beta = 1.509191$, so a placebo patient has $w = e^{\hat\beta} = 4.5231$ and a 6-MP patient $w = 1$. At $t = 1$ all 42 are at risk, so $S_1 = 21 + 21 \cdot 4.5231 = 115.98$ and the increment is $2/115.98 = 0.01724$. Some rows of the output:

| $t$ | $d_j$ | $S_j$ | $\hat H_0(t)$ | standard error, $\beta$ fixed | $\hat S(t)$, 6-MP | $\hat S(t)$, placebo |
|---|---|---|---|---|---|---|
| 1 | 2 | 115.98 | 0.0172 | 0.0122 | 0.983 | 0.925 |
| 4 | 2 | 93.37 | 0.0676 | 0.0256 | 0.935 | 0.737 |
| 8 | 4 | 70.28 | 0.2021 | 0.0498 | 0.817 | 0.401 |
| 12 | 2 | 39.14 | 0.3134 | 0.0706 | 0.731 | 0.242 |
| 17 | 1 | 23.57 | 0.4641 | 0.1036 | 0.629 | 0.123 |
| 23 | 2 | 10.52 | 0.7788 | 0.1912 | 0.459 | 0.030 |

The 6-MP column is $\exp(-\hat H_0(t))$ and the placebo column is $\exp(-4.5231\,\hat H_0(t))$. Compare the [Kaplan-Meier](/kaplan-meier-estimator/) values of the two arms: 0.448 for 6-MP at week 23, and $8/21 = 0.381$ for placebo after week 8. The model curves are close but not equal, because the Cox model forces the two curves to be powers of each other. With the Efron rule, $\hat H_0(23) = 0.8400$ at the Efron estimate. Summing the residuals $w_i \hat H_0(y_i)$ over all 42 patients gives exactly 30, the number of events.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows five things. First, the backward pass keeps the invariant that $S = \sum_{y_i > t} w_i$ at the start of the group at $t$, so every output row is $(t_j, S_j, d_j)$ and $H = \hat H_0(t_j)$ after line L9. Second, at $\beta = 0$ the estimate is Nelson-Aalen, and the Efron increment is at least $d_j/n_j$, with equality iff $d_j = 1$. Third, for fixed $\beta$, $\hat H_0$ is the unique maximizer of the full likelihood over all step-function cumulative hazards, and the maximum equals $e^{-d}\prod_j d_j^{d_j}$ times the Breslow-ties partial likelihood, so the Cox estimate with $\hat H_0(\cdot\,; \hat\beta)$ is a joint profile maximum likelihood estimate. Fourth, the Cox-Snell residuals $w_i\hat H_0(y_i)$ sum to the number of events $d$ for every $\beta$. Fifth, with $\beta$ fixed, $V$ estimates the variance by the Nelson-Aalen argument. The extra variance from estimating $\beta$ is cited, not proved.

## Complexity

The risk scores cost $\Theta(np)$. The sort in line L1 costs $\Theta(n \log n)$ comparisons. Lines L3 and L4 visit each subject once, and lines L7 to L9 visit each event time once, so the passes cost $\Theta(n)$ with the Breslow rule. The Efron rule adds $d_j$ terms at $t_j$, $\Theta(n)$ in total. The extra space is $\Theta(n)$ for the order and the $k \le n$ rows. A value $\hat H_0(t)$ then costs $O(\log k)$ by a binary search, and a whole survival curve for a new $x$ costs $O(k + p)$.

In floating point, each $S_j$ is a sum of positive terms with a relative error of about $n$ units in the last place, and no cancellation happens. A forward pass that starts from the total and subtracts the scores that leave would give the same values in exact arithmetic but can lose all digits when the late scores are much smaller than the early ones. With rational scores, such as the integer $1$ at $\beta = 0$, the code returns exact Fractions.

## Properties

- **Reduces to Nelson-Aalen.** At $\beta = 0$, $S_j = n_j$ and the estimate is $\sum_{t_j \le t} d_j/n_j$.
- **Profile maximum likelihood.** It is the nonparametric maximum likelihood estimate of $H_0$ for fixed $\beta$. Profiling it out of the full likelihood gives back the Breslow partial likelihood.
- **Martingale residuals sum to zero.** $\sum_i (\delta_i - w_i\hat H_0(y_i)) = 0$ for every $\beta$, with the Breslow rule.
- **Equivariance.** Shifting a covariate, $x \to x + c$, multiplies every $w_i$ by $e^{\beta^{\mathsf T}c}$ and divides $\hat H_0$ by the same factor. $\hat H_0$ is the cumulative hazard at $x = 0$, so center the covariates if that value is not meaningful. The survival curve for a given $x$ does not change.
- **Large-sample behavior.** If $\hat\beta$ is the Cox estimate and the model holds, $\sqrt n(\hat H_0 - H_0)$ converges on $[0, \tau]$ to a Gaussian process whose variance is $\int_0^t dH_0/s^{(0)}$ plus the term $q(t)^{\mathsf T}\Sigma q(t)$ from the uncertainty in $\hat\beta$ (Tsiatis 1981; Andersen and Gill 1982). This is cited, not proved here.
- **The curves do not cross.** For two covariate values $x_1, x_2$, $\hat S(t \mid x_2) = \hat S(t \mid x_1)^{\exp(\beta^{\mathsf T}(x_2 - x_1))}$, so the curves never cross.

## Variants and improvements

- **Efron increments.** With many tied events, use the Efron rule of line L8 together with the Efron partial likelihood, so the estimate is consistent with the fit.
- **Kalbfleisch-Prentice estimate.** Solve, at each $t_j$, for a conditional survival probability $\alpha_j$ so that $\hat S_0(t) = \prod_{t_j \le t}\alpha_j$ is the maximum likelihood estimate under a discrete baseline. It reduces to [Kaplan-Meier](/kaplan-meier-estimator/) at $\beta = 0$, as the Breslow estimate reduces to Nelson-Aalen.
- **Product-limit form.** $\prod_{t_j \le t}(1 - d_j/S_j)^{e^{\beta^{\mathsf T}x}}$, a Kaplan-Meier style variant, avoids the exponential. It is close to $\exp(-\hat H_0 e^{\beta^{\mathsf T}x})$ when every $d_j/S_j$ is small.
- **Strata.** With a stratified Cox model, run the pass once per stratum to get one $\hat H_{0s}$ per stratum.
- **Time-dependent covariates and delayed entry.** The risk sum must use $w_i(t_j)$ and the subjects under observation at $t_j$. A pass in time order that adds entries and removes exits replaces the backward pass.
- **Weighted versions.** Weights in the risk sums give the baseline of the [Fine-Gray model](/fine-gray-model/), and the frailty-weighted sums in the EM algorithm for the [frailty model](/frailty-model/).

## When to use it

Use it after a Cox fit whenever you need absolute risks rather than hazard ratios: predicted survival probabilities, median survival for a covariate profile, the Cox-Snell and martingale residuals, or calibration plots. Use it with the same tie rule as the fit. For one group without covariates use [Kaplan-Meier](/kaplan-meier-estimator/) or Nelson-Aalen directly.

## Pitfalls

- **The baseline is at $x = 0$.** If $x = 0$ is far from the data, such as age 0, $\hat H_0$ is a large extrapolation and its numbers are not meaningful. Center the covariates or report curves for actual covariate profiles.
- **Standard errors with $\beta$ fixed are too small.** The variance $V$ ignores the uncertainty in $\hat\beta$. Add the Tsiatis term for intervals on $\hat S(t \mid x)$.
- **Tie rule mismatch.** Breslow increments with an Efron fit give residuals that do not sum exactly to $d$ and curves that are slightly off.
- **Censored ties.** Count a censored subject at $t$ in the risk sum at $t$, as for Kaplan-Meier.
- **Proportional hazards.** The curves for different $x$ are powers of each other. If the hazards are not proportional, the curves are wrong in shape, not only in level. Check with the [Schoenfeld residuals](/schoenfeld-residuals/), or stratify.
- **The tail.** After the last event time with few subjects at risk, the increments are large and unstable, as in the last rows of the table.

## Implementations

## History

Norman Breslow proposed the estimate in his discussion of Cox's 1972 paper and published it in Biometrics in 1974. He took the baseline hazard to be constant between event times and maximized the full likelihood, which gave both the baseline estimate and his approximation for tied times. Kalbfleisch and Prentice (1973) gave the discrete product form. Tsiatis (1981) proved that $\hat\beta$ and $\hat H_0$ are jointly asymptotically normal, and Andersen and Gill (1982) gave the counting process proof, in which the Breslow estimator is the Nelson-Aalen estimator with the number at risk replaced by the risk sum.

## References
