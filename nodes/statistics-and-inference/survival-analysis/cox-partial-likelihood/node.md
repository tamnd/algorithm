---
tag: 9HJDFT
kind: technique
slug: cox-partial-likelihood
name: Partial likelihood
aliases:
- Cox partial likelihood
area: statistics-and-inference/survival-analysis
level: advanced
summary: Cox's likelihood for beta that multiplies, over event times, the chance that the unit that failed is the one to fail among those at risk. The baseline hazard drops out.
prereqs: [cox-proportional-hazards-model, likelihood-function, score-function, newton-raphson-method]
see_also: [breslow-estimator, schoenfeld-residuals, log-rank-test, score-test, likelihood-ratio-test, fine-gray-model, logistic-regression, prefix-sums]
sources:
  - paper: doi:10.1111/j.2517-6161.1972.tb00899.x
    title: D. R. Cox, Regression models and life-tables, Journal of the Royal Statistical Society, Series B 34(2), 1972
    locator: pp. 187 to 220 (the conditional likelihood of the event at each time given the risk set, and the discrete logistic model for ties)
  - paper: doi:10.1093/biomet/62.2.269
    title: D. R. Cox, Partial likelihood, Biometrika 62(2), 1975
    locator: pp. 269 to 276 (the general definition of partial likelihood and the argument that the usual large-sample results apply)
  - paper: doi:10.2307/2529620
    title: N. E. Breslow, Covariance analysis of censored survival data, Biometrics 30(1), 1974
    locator: pp. 89 to 99 (the approximation for tied times and the estimate of the baseline hazard)
  - paper: doi:10.1080/01621459.1977.10480613
    title: Bradley Efron, The efficiency of Cox's likelihood function for censored data, Journal of the American Statistical Association 72(359), 1977
    locator: pp. 557 to 565 (the efficiency of the partial likelihood and the approximation for tied times)
  - paper: doi:10.1093/biomet/68.3.703
    title: Mitchell H. Gail, Jay H. Lubin and Lawrence V. Rubinstein, Likelihood calculations for matched case-control studies and survival studies with tied death times, Biometrika 68(3), 1981
    locator: pp. 703 to 707 (the recursion for the exact conditional likelihood with tied times)
  - paper: doi:10.1214/aos/1176345976
    title: Per Kragh Andersen and Richard D. Gill, Cox's regression model for counting processes, a large sample study, Annals of Statistics 10(4), 1982
    locator: pp. 1100 to 1120 (consistency and asymptotic normality of the maximum partial likelihood estimate)
  - paper: doi:10.1111/j.0006-341X.2001.00114.x
    title: Georg Heinze and Michael Schemper, A solution to the problem of monotone likelihood in Cox regression, Biometrics 57(1), 2001
    locator: pp. 114 to 119 (monotone likelihood and the Firth penalized partial likelihood)
---

The partial likelihood is the function of $\beta$ that Cox used to fit the [proportional hazards model](/cox-proportional-hazards-model/) $h(t \mid x) = h_0(t)\exp(\beta^{\mathsf T}x)$ without any model for $h_0$. At each event time $t_j$ it takes the probability that the event happened to the subject that had it, given that exactly one event happened among the subjects at risk:

$$L(\beta) = \prod_{j} \frac{\exp(\beta^{\mathsf T}x_{(j)})}{\sum_{i \in R(t_j)} \exp(\beta^{\mathsf T}x_i)}, \qquad R(t_j) = \{i : y_i \ge t_j\}.$$

The factor $h_0(t_j)\,dt$ is the same in the numerator and in every term of the denominator, so it cancels. The result is not the likelihood of the data, but Cox (1975) and Andersen and Gill (1982) showed that its maximizer behaves like a maximum likelihood estimate. The log of $L$ is concave, and one sort followed by running sums gives each Newton step in $O(np^2)$ time.

## In plain words

At each moment when someone has the event, look at everyone who could have had it then. Under the model, each of them had a chance proportional to $e^{\beta^{\mathsf T}x}$, their relative risk. The partial likelihood asks how probable it was that the person who actually had the event was the one picked. Multiply these chances over all event times. Good values of $\beta$ make the people who had events look like the high-risk members of their risk sets. The baseline hazard tells us when events happen, but not who has them, so it does not enter. Censored people count in every risk set up to the time they leave.

## When it applies

- The model is a relative risk model: $h_i(t) = h_0(t)\,r(\beta, x_i(t))$ with the same unknown $h_0$ for every subject, usually $r = e^{\beta^{\mathsf T}x}$. Covariates may change in time.
- Censoring and delayed entry are independent: given the past, leaving or entering the risk set does not depend on the future event times. The risk set at $t$ is then exactly the set of subjects under observation just before $t$.
- The idea works for any process where the probability of "which unit" at each step does not depend on the nuisance parameter that rules "when". Cox (1975) gives the general definition. A matched case-control study with one case per set has the same form, which gives conditional logistic regression.
- It does not apply directly when the hazards of different subjects have different baseline functions (use strata), or when $h_0$ itself is the target (use the [Breslow estimator](/breslow-estimator/) after the fit).

## The template

```pseudo id=main
COX-NEWTON(y[1..n], δ[1..n], x[1..n], ties)
L1  sort the subjects by decreasing y
L2  β ← 0
L3  repeat
L4      S0 ← 0;  S1 ← 0;  S2 ← 0;  ℓ ← 0;  U ← 0;  I ← 0
L5      for each distinct time t, from the largest down
L6          add w_i, w_i x_i and w_i x_i x_iᵀ to S0, S1, S2 for each i with y_i = t    ▷ w_i = exp(βᵀx_i)
L7          if t has d > 0 events, add their terms to ℓ, U and I                       ▷ hole: the rule for ties
L8      Δ ← I⁻¹ U;  halve Δ until ℓ(β + Δ) ≥ ℓ(β)
L9      β ← β + Δ
L10 until every entry of Δ is small
L11 return β, ℓ, I⁻¹
```

Line L1 is the only sort. Because the times are visited from the largest down, the sums $S_0 = \sum_{i \in R(t)} w_i$, $S_1 = \sum_{i \in R(t)} w_i x_i$ and $S_2 = \sum_{i \in R(t)} w_i x_i x_i^{\mathsf T}$ only grow, so line L6 keeps them as running [prefix sums](/prefix-sums/) of positive terms, without subtraction. A censored subject tied with an event time joins the sums before line L7, so it is in the risk set at that time.

**The terms of line L7.** Let $D$ be the set of the $d$ subjects with an event at $t$, $s = \sum_{i \in D} x_i$, and $\bar x = S_1/S_0$. Then:

- *Breslow (1974):* $\ell$ gains $\beta^{\mathsf T}s - d\log S_0$, $U$ gains $s - d\bar x$, and $I$ gains $d\,(S_2/S_0 - \bar x\bar x^{\mathsf T})$. It treats the $d$ events as if each had the whole risk set.
- *Efron (1977):* the $r$-th event, $r = 0, \ldots, d - 1$, sees the risk set with a fraction $r/d$ of each dead subject removed: replace $(S_0, S_1, S_2)$ by $(S_0 - \tfrac rd D_0, S_1 - \tfrac rd D_1, S_2 - \tfrac rd D_2)$, where $D_k$ are the same sums over $D$, and add the $d$ single-event terms.
- *Exact (Cox's discrete model):* $\ell$ gains $\beta^{\mathsf T}s - \log e_d$, where $e_d = \sum_{A \subseteq R(t),\, |A| = d} \exp(\beta^{\mathsf T}\sum_{i \in A} x_i)$. The recursion of Gail, Lubin and Rubinstein (1981) computes $e_d$, its gradient and its Hessian over the risk set in $O(|R(t)|\,d\,p^2)$ time.

With $d = 1$ the three rules agree.

**The log partial likelihood is concave.** For each rule, $\ell(\beta)$ is a linear function minus a sum of functions of the form $\log \sum_k c_k \exp(\beta^{\mathsf T}z_k)$ with $c_k > 0$. *Proof.* For Breslow, the sum is $S_0 = \sum_{i \in R(t)} \exp(\beta^{\mathsf T}x_i)$. For Efron, it is $S_0 - \tfrac rd D_0$, in which each dead subject has the coefficient $1 - r/d > 0$ and each other subject the coefficient $1$. For the exact rule, it is $e_d$, a sum over subsets with $z_A = \sum_{i \in A} x_i$. Now let $g(\beta) = \log \sum_k c_k e^{\beta^{\mathsf T}z_k}$ and $\pi_k = c_k e^{\beta^{\mathsf T}z_k}/\sum_m c_m e^{\beta^{\mathsf T}z_m}$. Then $\nabla g = \sum_k \pi_k z_k$ and

$$\nabla^2 g = \sum_k \pi_k z_k z_k^{\mathsf T} - \Bigl(\sum_k \pi_k z_k\Bigr)\Bigl(\sum_k \pi_k z_k\Bigr)^{\mathsf T} = \operatorname{Cov}_\pi(z),$$

the covariance matrix of $z$ under the weights $\pi$, which is positive semidefinite. So each $g$ is a [convex function](/convex-function/), and $\ell$, a linear function minus a sum of convex functions, is concave. $\square$

The information matrix $I = -\nabla^2\ell$ is the sum of these weighted covariance matrices. It is positive definite, and $\ell$ is strictly concave, when the vectors $x_i - x_k$ for $i, k$ in a common risk set at an event time span $\mathbb{R}^p$. Then the maximizer is unique if it exists, and Newton's method with the step halving of line L8 converges to it. Each Newton step costs $O(np^2)$ for the sums plus $O(p^3)$ for the solve, and the sort of line L1 costs $O(n \log n)$ once. The reference code sorts again in each evaluation, which adds $O(n \log n)$ per step and keeps the code short.

**The score test at $\beta = 0$ is the log-rank test.** Take one binary covariate ($x_i = 1$ in group 1, $0$ in group 0). Let $n_j$ and $n_{1j}$ be the numbers at risk in all and in group 1 at $t_j$, $n_{0j} = n_j - n_{1j}$, $d_j$ the number of events and $o_{1j}$ the number of events in group 1.

*No ties.* At $\beta = 0$ all $w_i = 1$, so $\bar x = n_{1j}/n_j$ and $S_2/S_0 = n_{1j}/n_j$ (since $x^2 = x$). The score is $U(0) = \sum_j (o_{1j} - n_{1j}/n_j) = O - E$, and the information is $I(0) = \sum_j \frac{n_{1j}}{n_j}\bigl(1 - \frac{n_{1j}}{n_j}\bigr) = \sum_j \frac{n_{1j}n_{0j}}{n_j^2}$. With $d_j = 1$, the hypergeometric variance of the [log-rank test](/log-rank-test/), $\frac{n_{1j}n_{0j}d_j(n_j - d_j)}{n_j^2(n_j - 1)}$, is also $\frac{n_{1j}n_{0j}}{n_j^2}$. So $U(0)^2/I(0) = (O - E)^2/V$, the log-rank statistic. $\square$

*Exact rule with ties.* At $\beta = 0$, $e_d(\beta)/\binom{n_j}{d_j} = E[\exp(\beta S)]$, where $S$ is the number of group 1 subjects in a uniformly random subset of size $d_j$ of $R(t_j)$. So $\log e_d$ is a cumulant generating function plus a constant, its gradient at $0$ is $E[S] = d_j n_{1j}/n_j$ and its Hessian at $0$ is $\operatorname{Var}(S)$. $S$ is hypergeometric, with variance $\frac{n_{1j}n_{0j}d_j(n_j - d_j)}{n_j^2(n_j - 1)}$. So the exact-rule score test at $0$ is the log-rank test with its usual hypergeometric variance, for any ties. $\square$

*Breslow rule with ties.* The score is still $O - E$, but the information is $\sum_j d_j n_{1j}n_{0j}/n_j^2$, the binomial variance, which is larger than the hypergeometric one by the factor $(n_j - 1)/(n_j - d_j)$ at each time with $d_j \ge 2$. So the Breslow score statistic is a little smaller than the log-rank statistic. The Efron score at $0$ is not $O - E$ when there are ties.

## Classic examples

**A hand example.** Five subjects with times $1, 2, 3^+, 4, 5$ ($3^+$ censored) and $x = 1, 0, 1, 0, 1$. The risk sets at the event times 1, 2, 4 and 5 have the covariates $\{1,0,1,0,1\}$, $\{0,1,0,1\}$, $\{0,1\}$ and $\{1\}$. At $\beta = 0$ the weighted means are $3/5$, $1/2$, $1/2$ and $1$, so

$$U(0) = (1 - \tfrac35) + (0 - \tfrac12) + (0 - \tfrac12) + (1 - 1) = -\tfrac35, \qquad I(0) = \tfrac{6}{25} + \tfrac14 + \tfrac14 + 0 = \tfrac{37}{50},$$

and $\ell(0) = -\log(5 \cdot 4 \cdot 2 \cdot 1) = -3.6889$. The score statistic is $U^2/I = 18/37 = 0.486$. Newton's method from $0$ stops after 5 steps at $\hat\beta = -0.8341$ with $\ell(\hat\beta) = -3.4433$ and $I(\hat\beta) = 0.6611$, so the likelihood ratio statistic is $0.491$ and the standard error is $1.230$. The last risk set has one member, so its factor is $1$ for every $\beta$: a subject alone in its risk set gives no information.

**The leukemia data and the three rules for ties.** For the Gehan data of the [Cox model](/cox-proportional-hazards-model/) page ($x = 1$ for placebo, 30 events at 17 distinct times, with up to 4 events at one time):

| ties | $\ell(0)$ | $\ell(\hat\beta)$ | $\hat\beta$ | standard error | $I(0)$ | score statistic |
|---|---|---|---|---|---|---|
| Breslow | -93.985 | -86.380 | 1.5092 | 0.4096 | 6.596 | 15.93 |
| Efron | -93.184 | -85.008 | 1.5721 | 0.4124 | 6.482 | 17.25 |
| exact | -82.669 | -74.543 | 1.6282 | 0.4331 | 6.257 | 16.79 |

The score $U(0) = O - E = 10.2505$ for Breslow and the exact rule. The exact information $6.257$ is the log-rank variance and $10.2505^2/6.257 = 16.79$ is the log-rank statistic. The Breslow information is larger, so its statistic is smaller, as proved above. With many ties, Breslow pulls $\hat\beta$ toward $0$ compared with the exact rule; Efron lies between them here and is the default of most software.

**Matched case-control studies.** If each matched set has one case and the controls, and the "risk set" is the matched set, the partial likelihood is the conditional likelihood of the conditional logistic regression for matched data. Survival software fits such studies with the exact rule.

**Strata.** With strata $s$, each with its own $h_{0s}$, the log partial likelihood is the sum over strata of the stratum log partial likelihoods. The sort and the running sums are done within each stratum.

## Variations

- **Time-dependent covariates.** If $x_i(t)$ changes in time, the risk-set sums must use the values at each $t_j$. Split each subject into intervals with constant covariates and use risk sets $\{i : a_i < t_j \le y_i\}$. The running sums then need both entries and exits, so they are computed by a pass in time order that adds and removes intervals.
- **Delayed entry.** A subject that enters at time $a_i$ is in $R(t)$ only for $a_i < t \le y_i$. The same pass with entries and exits handles it.
- **Weighted partial likelihood.** Weights $v_i(t)$ in the risk-set sums give the case-cohort designs, inverse probability weighting and the [Fine-Gray model](/fine-gray-model/), where subjects with a competing event stay in the risk set with a censoring weight.
- **Penalized partial likelihood.** A penalty on $\beta$ (ridge or lasso) keeps the problem concave. The Firth penalty, $\frac12 \log\det I(\beta)$, gives finite estimates under a monotone likelihood (Heinze and Schemper 2001).
- **Robust variance.** If the subjects are clustered or the model is not exactly right, replace $I^{-1}$ by a sandwich estimate built from the score residuals, as with [cluster-robust standard errors](/cluster-robust-standard-errors/).

## Pitfalls

- **It is not a full likelihood.** Do not compare $\ell(\hat\beta)$ across data sets or with a parametric likelihood. Differences of $\ell$ for nested models with the same data and risk sets give valid likelihood ratio tests.
- **Ties.** With many ties, the Breslow rule is biased toward $0$. Use Efron, or the exact rule when the ties come from a truly discrete time scale.
- **The monotone likelihood.** If, for some direction, the subjects with events always have the largest score in their risk sets, $\ell$ increases without bound. Newton's steps then grow in that direction, the reported $\hat\beta$ depends on when the iteration stopped, and the Wald test is useless. Check for a slowly increasing $\ell$ and a huge standard error. The reference code reports `converged = False`.
- **Overflow.** $\exp(\beta^{\mathsf T}x_i)$ overflows for large scores. Subtract the largest $\beta^{\mathsf T}x_i$ before taking exponentials. The shift cancels in every ratio.
- **Cancellation.** A pass forward in time that subtracts the subjects who leave from $S_0$ can lose all digits when the late weights are small. The backward pass of line L5 only adds.
- **Tied censoring.** A censored time equal to an event time must count as at risk at that time. Changing this convention changes $\hat\beta$.
- **Only the measured part is measured.** The large-sample results are cited (Andersen and Gill 1982), not proved here. The tests of the reference code measure the size of the score test at level 0.05 in one setting (2000 data sets of 40 subjects), which says nothing about small samples with heavy censoring.

## Exercises

1. Show that $L(\beta)$ does not change if the same vector $c$ is added to every $x_i$.
   *Answer.* Each factor gains $e^{\beta^{\mathsf T}c}$ in the numerator and in every term of the denominator, so it cancels. This is why the model has no intercept.
2. Two subjects are at risk at the only event time, and the subject with the event has the larger scalar covariate. Find $\hat\beta$.
   *Answer.* $L(\beta) = 1/(1 + e^{-\beta(x_1 - x_2)})$ increases in $\beta$ to $1$, so there is no finite maximizer. This is the smallest monotone likelihood.
3. Show that the three rules for ties give the same $\ell$, $U$ and $I$ at a time with one event.
   *Answer.* With $d = 1$, Efron has only $r = 0$, which is the Breslow term, and $e_1 = S_0$.
4. Show that the Breslow information at $\beta = 0$ for one binary covariate is $d_j n_{1j}n_{0j}/n_j^2$ at $t_j$, and that it is at least the hypergeometric variance, with equality exactly when $d_j = 1$ (or $n_{1j}n_{0j} = 0$).
   *Answer.* $d_j(S_2/S_0 - \bar x^2) = d_j(n_{1j}/n_j)(1 - n_{1j}/n_j)$. The ratio of the two variances is $(n_j - d_j)/(n_j - 1) \le 1$, with equality iff $d_j = 1$.
5. Show that the score $U(\beta)$ is the sum of the [Schoenfeld residuals](/schoenfeld-residuals/), so that they sum to $0$ at $\hat\beta$.
   *Answer.* With the Breslow rule, the term of line L7 is $s - d\bar x = \sum_{i \in D}(x_i - \bar x)$, a sum of the residuals at $t$. At $\hat\beta$ the score is $0$.

## References
