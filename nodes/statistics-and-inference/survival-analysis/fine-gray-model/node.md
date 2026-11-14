---
tag: YSYJCC
kind: model
slug: fine-gray-model
name: Fine-Gray model
aliases:
- subdistribution hazard model
- proportional subdistribution hazards
area: statistics-and-inference/survival-analysis
level: research
summary: A proportional hazards model for the subdistribution hazard of one cause, so covariate effects act directly on its cumulative incidence.
prereqs: [competing-risks, cox-proportional-hazards-model, cox-partial-likelihood, aalen-johansen-estimator, inverse-probability-weighting]
see_also: [breslow-estimator, kaplan-meier-estimator, censoring, schoenfeld-residuals, frailty-model, m-estimator, cluster-robust-standard-errors, accelerated-failure-time-model]
sources:
  - paper: doi:10.1080/01621459.1999.10474144
    title: Jason P. Fine and Robert J. Gray, A proportional hazards model for the subdistribution of a competing risk, Journal of the American Statistical Association 94(446), 1999
    locator: pp. 496 to 509 (the model, the risk set with inverse probability of censoring weights, the estimating equation, its asymptotic normality and the robust variance, and the simulation design used here)
  - paper: doi:10.1214/aos/1176350951
    title: Robert J. Gray, A class of K-sample tests for comparing the cumulative incidence of a competing risk, Annals of Statistics 16(3), 1988
    locator: pp. 1141 to 1154 (the subdistribution hazard and its risk set, and the K-sample test)
  - paper: doi:10.1002/sim.2712
    title: H. Putter, M. Fiocco and R. B. Geskus, Tutorial in biostatistics, competing risks and multi-state models, Statistics in Medicine 26(11), 2007
    locator: pp. 2389 to 2430 (the interpretation of subdistribution hazard ratios next to cause-specific hazard ratios)
  - book: isbn:9780471363576
    title: John D. Kalbfleisch and Ross L. Prentice, The Statistical Analysis of Failure Time Data, 2nd edition, Wiley, 2002
    locator: Chapter 8 (competing risks, cause-specific hazards and cumulative incidence)
---

The Fine-Gray model is a regression model for the cumulative incidence of one cause in a [competing risks](/competing-risks/) problem. A [Cox model](/cox-proportional-hazards-model/) on the cause-specific hazard tells how a covariate changes the rate of cause 1 among event-free subjects, but the risk of cause 1, $F_1(t) = P(T \le t, \text{cause} = 1)$, also depends on the other causes. Fine and Gray (1999) put the proportional hazards form on the subdistribution hazard of Gray (1988),

$$\tilde h_1(t \mid x) = -\frac{d}{dt}\log\bigl(1 - F_1(t \mid x)\bigr) = \tilde h_{10}(t)\exp(\beta^{\mathsf T}x),$$

so that $1 - F_1(t \mid x) = (1 - F_{10}(t))^{\exp(\beta^{\mathsf T}x)}$: a positive $\beta_k$ raises the cumulative incidence of cause 1 at every time. The model is fitted by a weighted [partial likelihood](/cox-partial-likelihood/) in which subjects who had another cause stay in the risk set, with weights from the censoring distribution.

## The machine

**The data.** For subject $i$ we observe $y_i$, the cause $c_i \in \{0, 1, \ldots, K\}$, with $0$ for censored, and covariates $x_i$. Censoring is independent of the event process, and in the basic form also of the covariates.

**The subdistribution time.** Let $T^\ast = T$ if the cause is $1$ and $T^\ast = \infty$ otherwise. Then $P(T^\ast \le t) = F_1(t)$, an improper distribution with mass $1 - F_1(\infty)$ at infinity, and its hazard is $\tilde h_1$. The risk set of $T^\ast$ at $t$ is

$$\{i : T_i \ge t\} \cup \{i : T_i < t,\ c_i \notin \{0, 1\}\},$$

the subjects still event-free and the subjects that already had another cause. The second group is not at risk of anything in reality, but it is at risk in the arithmetic of $1 - F_1$.

**The conditions.**

1. **Proportional subdistribution hazards.** $\tilde h_1(t \mid x) = \tilde h_{10}(t)e^{\beta^{\mathsf T}x}$ with an unspecified $\tilde h_{10}$, for the cause of interest only. The other causes are left unmodeled.
2. **Independent censoring**, independent of $x$ in the basic form. Covariate-dependent censoring needs censoring weights that depend on $x$.
3. **Independent subjects.**

**Equivalent form.** $F_1(t \mid x) = 1 - (1 - F_{10}(t))^{\exp(\beta^{\mathsf T}x)} = 1 - \exp\bigl(-\tilde H_{10}(t)e^{\beta^{\mathsf T}x}\bigr)$, with $\tilde H_{10} = \int_0^t \tilde h_{10}$. *Proof.* Integrate the definition: $-\log(1 - F_1(t \mid x)) = \tilde H_{10}(t)e^{\beta^{\mathsf T}x}$. $\square$

**The estimating equation with censoring.** Subjects with another cause are not followed after their event, so whether they would have been censored later is unknown. Fine and Gray give them the weight

$$w_i(t) = \frac{\hat G(t-)}{\hat G(y_i-)} \quad \text{for } y_i < t,\ c_i \notin \{0, 1\},$$

and weight $1$ while $y_i \ge t$, where $\hat G$ is the [Kaplan-Meier](/kaplan-meier-estimator/) estimate of the censoring distribution, with events leaving before censorings at tied times. The weight is the estimated probability that the subject would still be uncensored at $t$ given that it was at $y_i$, a form of [inverse probability weighting](/inverse-probability-weighting/). The weighted log partial likelihood is

$$\ell(\beta) = \sum_{j}\Bigl[\beta^{\mathsf T}s_j - d_j\log\sum_i w_i(t_j)e^{\beta^{\mathsf T}x_i}\Bigr],$$

over the distinct times $t_j$ of cause 1, with $d_j$ events of cause 1 and covariate sum $s_j$, using the Breslow rule for ties. It is concave by the argument of the partial likelihood page, since the weights do not depend on $\beta$.

**Computation.** The reference code splits the weighted risk sums into a backward running sum over $\{y_i \ge t_j\}$ and $\hat G(t_j-)$ times a forward running sum of $e^{\beta^{\mathsf T}x_i}x_i^{\otimes r}/\hat G(y_i-)$ over the subjects with another cause before $t_j$. After one sort, a Newton step costs $O(np^2 + p^3)$, as for the Cox model. The baseline $\tilde H_{10}$ is a Breslow-type sum of $d_j/\sum_i w_i(t_j)e^{\hat\beta^{\mathsf T}x_i}$.

## What it counts

- **The subdistribution hazard ratio** $e^{\beta_k}$. It is the factor on $\tilde h_1$, and so it orders the cumulative incidence curves: $e^{\beta^{\mathsf T}x} > 1$ means $F_1(t \mid x) > F_{10}(t)$ at every $t$. It is not the ratio of the rates of cause 1 among event-free subjects. That is the cause-specific hazard ratio.
- **Predicted risks.** $\hat F_1(t \mid x) = 1 - \exp(-\hat{\tilde H}_{10}(t)e^{\hat\beta^{\mathsf T}x})$ for any $x$. This is what the model is for.
- **Only one cause.** Each cause needs its own model. The models of different causes are not linked, and they cannot all hold, as proved below.

## Relation to other models

- **Cox model on $T^\ast$.** Without censoring, every weight is $1$, and the fit is exactly a Cox model in which the subjects with another cause get the time $+\infty$. The tests check this against a direct Cox fit.
- **Cause-specific hazards.** $\tilde h_1(t) = h_1(t)\dfrac{S(t)}{1 - F_1(t)} \le h_1(t)$, where $S$ is the all-cause survival. *Proof.* $\frac{d}{dt}F_1 = S h_1$, and $S \le 1 - F_1$ because $S + \sum_k F_k = 1$. $\square$ The two hazards agree as long as no other cause has happened. Proportional cause-specific hazards for all causes do not give proportional subdistribution hazards in general, and the converse fails too, so the two models are different assumptions, not two fits of one model.
- **The Aalen-Johansen estimator.** With no covariates, or at $\beta = 0$, the weighted product-limit estimate of $F_1$ is exactly the [Aalen-Johansen](/aalen-johansen-estimator/) estimate. This is proved below.
- **Direct binomial and pseudo-observation models.** Other models for $F_1$ use other links, such as the logit, with censoring weights or jackknife pseudo-values. The Fine-Gray model is the case of the complementary log-log link, $\log(-\log(1 - F_1)) = \log\tilde H_{10}(t) + \beta^{\mathsf T}x$.

## Known results in the model

**A censoring identity.** Let $\hat S$ be the all-cause Kaplan-Meier estimate and $\hat G$ the Kaplan-Meier estimate of the censoring distribution, with events leaving before censorings at tied times, and let $n_j = \#\{i : y_i \ge t_j\}$. Then $n_j/n = \hat S(t_j-)\hat G(t_j-)$ for every time $t_j$.

*Proof.* At a distinct observed time $u$ with $r$ at risk, $d$ events and $c$ censorings, $\hat S$ has the factor $(r - d)/r$ and $\hat G$ the factor $(r - d - c)/(r - d)$, or $1$ if $c = 0$. Their product is $(r - d - c)/r$, the ratio of the numbers at risk just after and at $u$. The product over all $u < t_j$ telescopes to $n_j/n$. (If $r = d$, then $c = 0$ and both sides are $0$.) $\square$

So the Aalen-Johansen increment $\hat S(t_j-)d_{kj}/n_j$ equals $d_{kj}/(n\hat G(t_j-))$, and $\hat F_k(t-) = \frac1n\sum_{y_i < t,\, c_i = k} 1/\hat G(y_i-)$: the Aalen-Johansen estimate is an inverse probability of censoring weighted proportion.

**At $\beta = 0$ the model reproduces Aalen-Johansen.** With all $e^{\beta^{\mathsf T}x_i} = 1$, let $\Delta_j = d_{1j}/\sum_i w_i(t_j)$ be the baseline jump at a time $t_j$ of cause 1. Then $1 - \prod_{t_j \le t}(1 - \Delta_j) = \hat F_1(t)$, the Aalen-Johansen estimate.

*Proof.* By the identity, the subjects still at risk contribute $n_j = n\hat S(t_j-)\hat G(t_j-)$, and the subjects with cause $k \ne 1$ before $t_j$ contribute $\hat G(t_j-)\sum_{y_i < t_j,\, c_i = k} 1/\hat G(y_i-) = n\hat G(t_j-)\hat F_k(t_j-)$. So

$$\sum_i w_i(t_j) = n\hat G(t_j-)\Bigl(\hat S(t_j-) + \sum_{k \ne 1}\hat F_k(t_j-)\Bigr) = n\hat G(t_j-)\bigl(1 - \hat F_1(t_j-)\bigr),$$

using $\hat S + \sum_k \hat F_k = 1$. The Aalen-Johansen increment at $t_j$ is $d_{1j}/(n\hat G(t_j-))$, so $\Delta_j = (\hat F_1(t_j) - \hat F_1(t_j-))/(1 - \hat F_1(t_j-))$, which is $1 - \hat F_1(t_j) = (1 - \hat F_1(t_j-))(1 - \Delta_j)$. Multiply over $j$. $\square$

The tests check both results in exact fractions on random data with ties.

**The models of two causes cannot both hold for all covariates.** Suppose cause 1 and cause 2 both follow Fine-Gray models with one covariate $x \in \mathbb{R}$ and coefficients $\beta_1, \beta_2 > 0$, with $0 < F_{k0}(t) < 1$ at some $t$. Then $F_k(t \mid x) = 1 - (1 - F_{k0}(t))^{e^{\beta_k x}} \to 1$ as $x \to \infty$ for both $k$, so $F_1 + F_2 > 1$ for large $x$, which is impossible. $\square$ With a bounded covariate the contradiction may not appear, but the two models remain separate approximations.

**Large samples.** Under the model and independent censoring, $\hat\beta$ is consistent and asymptotically normal. Its variance is not the inverse of the weighted information, because $\hat G$ is estimated and the weighted terms are not martingale increments. Fine and Gray (1999) give a sandwich variance with an extra term for $\hat G$. We cite these results and do not prove them. The reference code reports only the inverse information, which is labeled naive. Use the Fine-Gray variance, or the bootstrap, for inference.

**A simulation.** The tests use the design of Fine and Gray: a binary $x$, $F_1(t \mid x) = 1 - (1 - p(1 - e^{-t}))^{\exp(\beta_1 x)}$ with $p = 0.6$ and $\beta_1 = 0.5$, cause 2 given that cause 1 does not happen exponential with rate $e^{\beta_2 x}$, $\beta_2 = -0.5$, and censoring uniform on $(0, 3)$. The numbers are measured, for the stated seeds.

| fit (one data set, $n = 2000$: 950 cause 1, 386 cause 2, 664 censored) | coefficient of $x$ |
|---|---|
| Fine-Gray, cause 1 (truth 0.5) | 0.452 (naive standard error 0.066) |
| Cox on the cause-specific hazard of cause 1 | 0.298 (standard error 0.066) |
| Cox on the cause-specific hazard of cause 2 | -0.746 |
| Fine-Gray, cause 2 (not a true model in this design) | -0.871 |

Over 40 data sets of 200 subjects the Fine-Gray estimates had mean 0.480 and standard deviation 0.209, so the mean is within one standard error ($0.209/\sqrt{40} = 0.033$) of 0.5. The cause-specific coefficient of cause 1 is a different quantity: in this design the cause-specific hazards are not proportional, and its value is not an estimate of $\beta_1$. The predicted $F_1(1 \mid x = 1)$ from a fit to 2000 subjects is within 0.04 of the truth.

**Checks in code.** The tests compare the weighted risk sums with a direct $O(n^2)$ sum, the fit without censoring with a direct Cox fit with the competing times set to infinity, the score and information with numerical derivatives, the censoring identity and the Aalen-Johansen identity in exact fractions, and the simulation above.

## References
