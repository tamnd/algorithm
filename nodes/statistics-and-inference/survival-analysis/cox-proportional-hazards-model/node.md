---
tag: KRES0P
kind: model
slug: cox-proportional-hazards-model
name: Cox proportional hazards model
aliases:
- Cox regression
- proportional hazards regression
area: statistics-and-inference/survival-analysis
level: core
summary: Models the hazard as an unspecified baseline hazard times exp(x^T beta), so covariates scale the hazard by a constant factor over time.
prereqs: [hazard-function, survival-function, censoring, maximum-likelihood-estimation]
see_also: [cox-partial-likelihood, breslow-estimator, schoenfeld-residuals, log-rank-test, accelerated-failure-time-model, frailty-model, fine-gray-model, harrell-c-index]
sources:
  - paper: doi:10.1111/j.2517-6161.1972.tb00899.x
    title: D. R. Cox, Regression models and life-tables, Journal of the Royal Statistical Society, Series B 34(2), 1972
    locator: pp. 187 to 220 (the proportional hazards model, the conditional likelihood for the coefficients, ties and the discrete logistic model, with the discussion)
  - paper: doi:10.1214/aos/1176345976
    title: Per Kragh Andersen and Richard D. Gill, Cox's regression model for counting processes, a large sample study, Annals of Statistics 10(4), 1982
    locator: pp. 1100 to 1120 (the counting process form of the model, consistency and asymptotic normality of the estimate, and the Breslow estimator)
  - paper: doi:10.1214/aos/1176345335
    title: Anastasios A. Tsiatis, A large sample study of Cox's regression model, Annals of Statistics 9(1), 1981
    locator: pp. 93 to 108 (consistency and asymptotic normality of the estimate and of the estimated cumulative hazard, for time-fixed covariates)
  - paper: doi:10.1080/01621459.1977.10480613
    title: Bradley Efron, The efficiency of Cox's likelihood function for censored data, Journal of the American Statistical Association 72(359), 1977
    locator: pp. 557 to 565 (the efficiency of the partial likelihood estimate and the Efron approximation for ties)
  - book: isbn:9780471363576
    title: John D. Kalbfleisch and Ross L. Prentice, The Statistical Analysis of Failure Time Data, 2nd edition, Wiley, 2002
    locator: the chapter on relative risk (Cox) regression models (the model, the partial likelihood, ties, time-dependent covariates and stratification)
  - book: isbn:9780387987842
    title: Terry M. Therneau and Patricia M. Grambsch, Modeling Survival Data, Extending the Cox Model, Springer, 2000
    locator: the chapters on the Cox model, residuals and the test of proportional hazards
---

The Cox proportional hazards model relates the [hazard function](/hazard-function/) of an event time $T$ to a covariate vector $x$ by

$$h(t \mid x) = h_0(t)\,\exp(\beta^{\mathsf T}x).$$

The baseline hazard $h_0$ is any nonnegative function and is not modeled. The coefficient vector $\beta$ is the only finite-dimensional parameter. A change of $x$ by one unit in coordinate $k$ multiplies the hazard by $e^{\beta_k}$ at every time, so the model makes a strong assumption about the shape over time and no assumption about the level. Cox (1972) proposed the model together with a likelihood for $\beta$ in which $h_0$ does not appear, the [partial likelihood](/cox-partial-likelihood/). This made the model the standard regression model for censored survival data.

## The machine

**The data.** For subjects $i = 1, \ldots, n$ we observe $y_i = \min(T_i, C_i)$, the flag $\delta_i = 1\{T_i \le C_i\}$ and a covariate vector $x_i \in \mathbb{R}^p$. Here $T_i$ is the event time and $C_i$ the censoring time, as on the [censoring](/censoring/) page.

**The conditions.**

1. **Proportional hazards.** Given $x_i$, $T_i$ has the hazard $h_0(t)\exp(\beta^{\mathsf T}x_i)$, with the same $h_0$ for all subjects.
2. **Independent censoring.** Given $x_i$ and that subject $i$ is still at risk at $t$, the censoring does not change the hazard of the event at $t$. Censoring can depend on $x_i$.
3. **Independent subjects.** The triples $(T_i, C_i, x_i)$ are independent.
4. **No intercept.** The covariates have no constant column, because a constant $c$ in $\beta^{\mathsf T}x$ can move into $h_0$ as the factor $e^c$.

**Identifiability.** If $\operatorname{Var}(x)$ is nonsingular, then $\beta$ and $h_0$ are identified from the law of $(T, x)$: the log ratio $\log h(t \mid x) - \log h(t \mid x') = \beta^{\mathsf T}(x - x')$ fixes $\beta$ on the span of the differences $x - x'$, and then $h_0(t) = h(t \mid x)e^{-\beta^{\mathsf T}x}$. With censoring, the law is identified only up to the largest time at which subjects are still at risk.

**Equivalent forms.** With $H_0(t) = \int_0^t h_0(u)\,du$ and a continuous $T$:

$$H(t \mid x) = H_0(t)\,e^{\beta^{\mathsf T}x}, \qquad S(t \mid x) = S_0(t)^{\exp(\beta^{\mathsf T}x)}, \qquad \log(-\log S(t \mid x)) = \log H_0(t) + \beta^{\mathsf T}x.$$

*Proof.* Integrate the hazard from $0$ to $t$ to get the first form. Then $S(t \mid x) = \exp(-H(t \mid x)) = (\exp(-H_0(t)))^{\exp(\beta^{\mathsf T}x)}$ with $S_0 = \exp(-H_0)$. Take $\log(-\log)$ of the second form to get the third. $\square$

The third form gives the usual graphical check: the curves of $\log(-\log \hat S)$ against $t$ (or $\log t$) for groups of subjects are parallel under the model.

**The counting process form.** Let $N_i(t) = 1\{y_i \le t, \delta_i = 1\}$ and $Y_i(t) = 1\{y_i \ge t\}$. Under the conditions, $N_i$ has the intensity $Y_i(t)\,h_0(t)\exp(\beta^{\mathsf T}x_i)$, so $N_i(t) - \int_0^t Y_i(u) h_0(u) e^{\beta^{\mathsf T}x_i}\,du$ is a [martingale](/martingale/). Andersen and Gill (1982) used this form. It also allows covariates $x_i(t)$ that change in time, recurrent events and delayed entry: only $Y_i$ and $x_i(t)$ change. With time-dependent covariates the hazard ratio of two subjects is no longer constant, so the name "proportional hazards" then refers to the form of the model, not to the data.

**Strata.** A stratified model allows a separate baseline hazard $h_{0s}$ in each stratum $s$ with a common $\beta$. Use it for a factor that does not satisfy proportional hazards and whose effect is not of interest.

## What it counts

- **Parameters.** $\beta \in \mathbb{R}^p$, the log hazard ratios, and the baseline hazard $h_0$, an infinite-dimensional nuisance parameter.
- **The hazard ratio.** $e^{\beta_k}$ is the ratio of the hazards of two subjects that differ by one unit in $x_k$ and agree in the other covariates. It is the same at every time. It is not a ratio of survival probabilities, of medians or of mean times.
- **Survival curves.** $S(t \mid x) = \exp(-H_0(t)e^{\beta^{\mathsf T}x})$. The [Breslow estimator](/breslow-estimator/) gives $\hat H_0$, and so a curve for every covariate value.
- **The risk score.** $\beta^{\mathsf T}x$ orders the subjects by risk at every time. The [Harrell C-index](/harrell-c-index/) measures how well this order agrees with the observed times.
- **Effective sample size.** The information about $\beta$ comes from the events, not from the subjects. A common rule asks for 10 to 20 events per coefficient. This is a rule of thumb, not a theorem.

## Relation to other models

- **Parametric proportional hazards models.** A constant $h_0$ gives exponential regression and $h_0(t) = \lambda\rho t^{\rho - 1}$ gives Weibull regression. The Cox model keeps the hazard ratio and drops the assumption on $h_0$.
- **Accelerated failure time models.** The [AFT model](/accelerated-failure-time-model/) makes covariates stretch the time scale. The Weibull model is both a Cox model and an AFT model, and the AFT page proves that no other family is both when $x$ takes a continuum of values.
- **Frailty models.** A [frailty model](/frailty-model/) multiplies the Cox hazard by an unobserved random factor. If the frailty is left out, the marginal hazards are not proportional, and the fitted hazard ratio moves toward $1$ over time.
- **Competing risks.** The Cox model can be fitted to each cause-specific hazard, with the other causes treated as censoring. The [Fine-Gray model](/fine-gray-model/) puts the same form on the subdistribution hazard of one cause instead (see [competing risks](/competing-risks/)).
- **Discrete time.** If the time axis is cut into intervals and the continuous model holds, then the conditional probability $h_j(x)$ of an event in interval $j$, given survival to its start, satisfies $\log(-\log(1 - h_j(x))) = \alpha_j + \beta^{\mathsf T}x$. This is a binary [generalized linear model](/generalized-linear-model/) with the complementary log-log link. *Proof:* $1 - h_j(x) = S(a_{j+1} \mid x)/S(a_j \mid x) = (S_0(a_{j+1})/S_0(a_j))^{\exp(\beta^{\mathsf T}x)}$ for the interval $[a_j, a_{j+1})$; take $\log(-\log)$. The model with the logit link in place of the complementary log-log link is Cox's (1972) discrete model, a [logistic regression](/logistic-regression/) on the risk sets.
- **Poisson regression.** With a baseline hazard that is constant on intervals, the likelihood is that of a [Poisson](/poisson-distribution/) generalized linear model for the event counts with the log exposure time as an offset. When the baseline hazard may jump at each event time, the profile likelihood of $\beta$ is the partial likelihood with the Breslow rule for ties. The [Breslow estimator](/breslow-estimator/) page proves this.

## Known results in the model

**The partial likelihood.** Cox (1972, 1975) estimated $\beta$ by maximizing

$$L(\beta) = \prod_{j} \frac{\exp(\beta^{\mathsf T}x_{(j)})}{\sum_{i \in R(t_j)} \exp(\beta^{\mathsf T}x_i)},$$

where $x_{(j)}$ is the covariate of the subject with the event at $t_j$ and $R(t_j) = \{i : y_i \ge t_j\}$ is the risk set. Each factor is the conditional probability that the event at $t_j$ happens to the subject that had it, given that one event happens at $t_j$ among the subjects in $R(t_j)$. The factor does not contain $h_0$. The [partial likelihood](/cox-partial-likelihood/) page proves that $\log L$ is concave, gives the Newton iteration in $O(np^2)$ per step after one sort, and gives the rules of Breslow, Efron and the exact rule for tied times.

**Large samples.** Under the conditions above and regularity conditions on the covariates, the maximizer $\hat\beta$ is consistent, and $\sqrt n(\hat\beta - \beta)$ converges to a normal law with covariance matrix the inverse of the limit of $\mathcal I(\beta)/n$, where $\mathcal I$ is the negative Hessian of $\log L$ (Andersen and Gill 1982, with the counting process form; Tsiatis 1981 earlier for time-fixed covariates). We cite these results and do not prove them. So the [Wald test](/wald-test/), the [score test](/score-test/) and the [likelihood ratio test](/likelihood-ratio-test/) of $\beta$ all work as if $L$ were a likelihood.

**Efficiency.** The baseline hazard is unknown, so some information about $\beta$ is lost compared with a model with a known $h_0$. Efron (1977) showed that the partial likelihood estimate keeps all the information that is left: it is asymptotically efficient in the model with an arbitrary $h_0$.

**The log-rank test is the score test.** With one binary covariate, the score test of $\beta = 0$ is the [log-rank test](/log-rank-test/). The partial likelihood page proves this exactly when there are no ties, and shows which variance appears with each rule for ties.

**Checking the assumption.** The [Schoenfeld residuals](/schoenfeld-residuals/) of each covariate have mean near $0$ at every time if the hazards are proportional. A trend in time is evidence that the coefficient changes in time. The Grambsch and Therneau test makes this a score test.

**No finite estimate under separation.** If at every event time the subject with the event has the largest value of $\beta^{\mathsf T}x$ in its risk set for some direction $\beta$, then $\log L$ increases without bound along that direction and $\hat\beta$ is infinite. This is the *monotone likelihood* of survival data. It happens with small samples and binary covariates. The Firth penalty gives a finite estimate (Heinze and Schemper 2001).

**Worked example.** The leukemia remission data of Freireich et al. (1963), listed by Gehan (1965), have 21 patients on 6-MP (12 censored) and 21 on placebo (none censored), with 30 events in all. They are the data of the [Kaplan-Meier](/kaplan-meier-estimator/) page. Let $x = 1$ for placebo. The fits with the three rules for ties give:

| ties | $\hat\beta$ | standard error | hazard ratio | 95% interval | likelihood ratio | score test |
|---|---|---|---|---|---|---|
| Breslow | 1.5092 | 0.4096 | 4.52 | 2.03 to 10.09 | 15.21 | 15.93 |
| Efron | 1.5721 | 0.4124 | 4.82 | 2.15 to 10.81 | 16.35 | 17.25 |
| exact | 1.6282 | 0.4331 | 5.09 | 2.18 to 11.91 | 16.25 | 16.79 |

The hazard of the end of remission on placebo is about 4.8 times that on 6-MP, at every time. The exact score statistic 16.79 is the log-rank statistic of the [log-rank](/log-rank-test/) page. The Grambsch-Therneau test with $g(t) = t$ gives $0.019$ ($p = 0.89$), so these data show no evidence against proportional hazards. A Weibull AFT fit to the same data gives the hazard ratio 5.65 (see the [AFT page](/accelerated-failure-time-model/)).

**Checks in code.** The reference code is on the [partial likelihood](/cox-partial-likelihood/) page. Its tests check the log partial likelihood against a direct sum over risk sets and subsets, the score and information against numerical derivatives, Newton's estimate against a fine grid, the score test against the log-rank test in exact fractions, and the values in the table above.

## References
