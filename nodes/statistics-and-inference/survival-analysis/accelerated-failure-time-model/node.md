---
tag: MRHNZ0
kind: model
slug: accelerated-failure-time-model
name: Accelerated failure time model
aliases:
- AFT model
area: statistics-and-inference/survival-analysis
level: core
summary: Models log T as a linear function of covariates plus an error, so covariates stretch or shrink time. The Weibull model is both AFT and proportional hazards.
prereqs: [survival-function, hazard-function, censoring, maximum-likelihood-estimation, linear-regression]
see_also: [cox-proportional-hazards-model, kaplan-meier-estimator, schoenfeld-residuals, frailty-model, log-rank-test, m-estimator, ordinary-least-squares, newton-raphson-method]
sources:
  - book: isbn:9780471363576
    title: John D. Kalbfleisch and Ross L. Prentice, The Statistical Analysis of Failure Time Data, 2nd edition, Wiley, 2002
    locator: Chapters 2 and 3 (failure time models, including the accelerated failure time and proportional hazards classes, and inference for parametric regression models)
  - book: isbn:9780387953991
    title: John P. Klein and Melvin L. Moeschberger, Survival Analysis, Techniques for Censored and Truncated Data, 2nd edition, Springer, 2003
    locator: Chapter 12 (inference for parametric regression models, with the Weibull, log-logistic and lognormal accelerated failure time models)
  - paper: doi:10.1093/biomet/66.3.429
    title: Jonathan Buckley and Ian James, Linear regression with censored data, Biometrika 66(3), 1979
    locator: pp. 429 to 436 (the iterative estimate that replaces each censored log time by its conditional expectation under the Kaplan-Meier estimate of the residuals)
  - paper: doi:10.1214/aos/1176347504
    title: Anastasios A. Tsiatis, Estimating regression parameters using linear rank tests for censored data, Annals of Statistics 18(1), 1990
    locator: pp. 354 to 372 (rank estimating equations for the semiparametric model and their asymptotic normality)
  - paper: doi:10.1093/biomet/90.2.341
    title: Zhezhen Jin, D. Y. Lin, L. J. Wei and Zhiliang Ying, Rank-based inference for the accelerated failure time model, Biometrika 90(2), 2003
    locator: pp. 341 to 353 (the Gehan-weighted estimating function as a convex objective solved by linear programming, and variance estimation by resampling)
---

An accelerated failure time (AFT) model says that covariates change the speed at which time passes for a subject. If $T_0$ is the event time of a subject with $x = 0$, a subject with covariates $x$ has the event time $T = e^{\gamma^{\mathsf T}x}T_0$: everything that happens to the baseline subject at time $t$ happens to this subject at time $e^{\gamma^{\mathsf T}x}t$. On the log scale this is a linear regression with a censored response,

$$\log T = \mu + \gamma^{\mathsf T}x + \sigma W,$$

where $W$ is an error with a fixed distribution. The coefficients are log time ratios: $e^{\gamma_k}$ multiplies every quantile of $T$, including the median. This page states the model, proves the equivalent forms, and proves when an AFT model is also a [proportional hazards model](/cox-proportional-hazards-model/). The usual claim that "the Weibull is the only model that is both" needs a condition, and the page gives a counterexample for a single binary covariate.

## The machine

**The data.** For subjects $i = 1, \ldots, n$ we observe $y_i = \min(T_i, C_i)$, $\delta_i = 1\{T_i \le C_i\}$ and $x_i \in \mathbb{R}^p$, as on the [censoring](/censoring/) page.

**The conditions.**

1. **Log-linear form.** $\log T_i = \mu + \gamma^{\mathsf T}x_i + \sigma W_i$, with $\sigma > 0$ and $W_1, \ldots, W_n$ independent with a common distribution, independent of $x_i$. In a parametric AFT model the law of $W$ is fixed, with survival function $S_W$ and density $f_W$. In the semiparametric model it is unknown.
2. **Independent censoring.** Given $x_i$, censoring does not change the hazard of the event among the subjects at risk.
3. **Independent subjects.**

**Common choices of $W$.**

| law of $W$ | $S_W(w)$ | law of $T$ | hazard shape |
|---|---|---|---|
| minimum extreme value | $\exp(-e^w)$ | Weibull (exponential if $\sigma = 1$) | monotone |
| logistic | $1/(1 + e^w)$ | log-logistic | rises and falls if $\sigma < 1$ |
| standard normal | $1 - \Phi(w)$ | lognormal | rises and falls |

**Equivalent forms.** Write $\eta = \gamma^{\mathsf T}x$, and let $S_0$, $h_0$ and $H_0$ be the survival function, hazard and cumulative hazard of $T_0 = e^{\mu + \sigma W}$. Then

$$S(t \mid x) = S_0(te^{-\eta}), \qquad h(t \mid x) = e^{-\eta}h_0(te^{-\eta}), \qquad t_q(x) = e^{\eta}t_q(0),$$

where $t_q(x)$ is the $q$-quantile of $T$ given $x$. *Proof.* $T = e^{\eta}T_0$, so $P(T > t) = P(T_0 > te^{-\eta}) = S_0(te^{-\eta})$. Then $H(t \mid x) = H_0(te^{-\eta})$, and differentiating in $t$ gives the hazard. Finally $S(e^\eta t_q(0) \mid x) = S_0(t_q(0)) = 1 - q$. $\square$

So the hazard of an AFT model at time $t$ is the baseline hazard read at the rescaled time $te^{-\eta}$, times the rate factor $e^{-\eta}$. The hazards are not proportional in general.

**The likelihood.** With $z_i = (\log y_i - \mu - \gamma^{\mathsf T}x_i)/\sigma$, the log-likelihood is

$$\ell(\mu, \gamma, \sigma) = \sum_i \Bigl[\delta_i\bigl(\log f_W(z_i) - \log\sigma - \log y_i\bigr) + (1 - \delta_i)\log S_W(z_i)\bigr],$$

the censored-data likelihood of the censoring page written on the log scale. The term $-\log y_i$ is the Jacobian of $t \mapsto \log t$. It does not depend on the parameters, but it must be kept to compare the log-likelihoods of an AFT model and a model fitted on the time scale. For the three laws above, $\ell$ is concave in $(\mu, \gamma)$ for fixed $\sigma$, because $\log f_W$ and $\log S_W$ are concave, and [Newton's method](/newton-raphson-method/) in $(\mu, \gamma, \log\sigma)$ converges quickly from a least squares start.

## What it counts

- **The time ratio.** $e^{\gamma_k}$ is the factor by which a one-unit increase in $x_k$ multiplies the median, every other quantile and, when it exists, the mean of $T$. A time ratio of 2 means the event takes twice as long. This is often easier to explain than a hazard ratio.
- **The scale $\sigma$.** It sets the spread of $\log T$ and the shape of the hazard. For the Weibull model the shape parameter is $\rho = 1/\sigma$: the hazard increases if $\sigma < 1$ and decreases if $\sigma > 1$.
- **Prediction.** The model gives the whole distribution of $T$ for each $x$, including the tail beyond the follow-up, which a semiparametric model cannot give. That extrapolation rests only on the chosen law of $W$.
- **Without censoring**, the model is the [linear regression](/linear-regression/) of $\log T$ on $x$, and for normal $W$ the maximum likelihood estimate of $(\mu, \gamma)$ is [ordinary least squares](/ordinary-least-squares/).

## Relation to other models

- **Proportional hazards.** The Weibull AFT model is a proportional hazards model. *Proof.* With $S_W(w) = \exp(-e^w)$, $S(t \mid x) = \exp\bigl(-(te^{-\mu - \eta})^{1/\sigma}\bigr)$, so $H(t \mid x) = (te^{-\mu})^{1/\sigma}e^{-\eta/\sigma} = H_0(t)\exp(-\gamma^{\mathsf T}x/\sigma)$. $\square$ So the hazard ratio coefficient is $\beta = -\gamma/\sigma$. A longer time (positive $\gamma$) means a lower hazard. The converse needs care; see the next section.
- **Proportional odds.** The log-logistic AFT model is a proportional odds model: the odds of having had the event, $(1 - S)/S$, are $(te^{-\mu})^{1/\sigma}e^{-\eta/\sigma}$, so covariates multiply the odds by $e^{-\eta/\sigma}$ at every time. Its hazard ratio between two covariate values starts at $e^{-(\eta_1 - \eta_2)/\sigma}$ near $t = 0$ and tends to $1$ as $t \to \infty$.
- **The Cox model.** The [Cox model](/cox-proportional-hazards-model/) fixes the form of the hazard ratio and leaves the baseline free. The semiparametric AFT model fixes the time ratio and leaves the law of $W$ free. Both are semiparametric, but the AFT estimating equations are not smooth, which makes them harder to compute.
- **Frailty.** If a proportional hazards model holds given an unobserved factor, the marginal hazard ratio is not constant. In a [frailty model](/frailty-model/) with a gamma factor of variance $\theta = 1$ and a Weibull baseline $H_0(t) = \lambda t^\rho$, the marginal survival is $S(t \mid x) = 1/(1 + \lambda t^\rho e^{\beta^{\mathsf T}x})$, which is a log-logistic AFT model with $\gamma = -\beta/\rho$. So data from a frailty model can look exactly like data from an AFT model.
- **Censored regression.** With normal $W$ and censoring at fixed known points the model is the Tobit model of econometrics, on the log scale.

## Known results in the model

**When is an AFT model also proportional hazards?** Let $S_0 = e^{-H_0}$, with $H_0$ continuous and strictly increasing from $0$ to $\infty$ on $(0, \infty)$. For a time ratio $c > 0$ the AFT survival function is $S_0(t/c)$, and it is a proportional hazards model with the factor $k(c)$ when

$$H_0(t/c) = k(c)\,H_0(t) \quad \text{for all } t > 0. \tag{$*$}$$

*Theorem.* If $(*)$ holds for every $c > 0$, or for two values $c_1, c_2 \ne 1$ with $\log c_1/\log c_2$ irrational, then $H_0(t) = \lambda t^{\rho}$ for some $\lambda, \rho > 0$: the baseline is Weibull.

*Proof.* Put $u = \log t$ and $g(u) = \log H_0(e^u)$, which is continuous. With $a_i = \log c_i$ and $\kappa_i = \log k(c_i)$, $(*)$ says $g(u - a_i) = g(u) + \kappa_i$ for all $u$. Let $q(u) = g(u) + (\kappa_1/a_1)u$. Then $q(u - a_1) = q(u)$, so $q$ is continuous and periodic, hence bounded. Also $q(u - a_2) = q(u) + e$ with $e = \kappa_2 - \kappa_1 a_2/a_1$, so $q(u - ma_2) = q(u) + me$ for every integer $m$. Since $q$ is bounded, $e = 0$, and $q$ has the periods $a_1$ and $a_2$. Their ratio is irrational, so the set $\{ma_1 + m'a_2\}$ of periods is dense in $\mathbb{R}$, and a continuous function with a dense set of periods is constant. So $g(u) = g(0) - (\kappa_1/a_1)u$, which is $H_0(t) = \lambda t^\rho$ with $\lambda = H_0(1)$ and $\rho = -\kappa_1/a_1$; $\rho > 0$ because $H_0$ increases. If $(*)$ holds for every $c > 0$, pick two values with an irrational log ratio. $\square$

*A counterexample with one binary covariate.* Fix $L > 0$, a small $a > 0$ and $c = e^L$, and let

$$H_0(t) = t\Bigl(1 + a\sin\frac{2\pi\log t}{L}\Bigr).$$

Its derivative is $1 + a\sin(\cdot) + a\frac{2\pi}{L}\cos(\cdot) \ge 1 - a\sqrt{1 + (2\pi/L)^2}$, which is positive for small $a$, so $H_0$ is a cumulative hazard from $0$ to $\infty$. Because $\log(t/c) = \log t - L$ leaves the sine unchanged, $H_0(t/c) = H_0(t)/c$. So with a binary $x$, the two-group model with time ratio $c$ is also a proportional hazards model with hazard ratio $1/c$, but $H_0$ is not Weibull. The "only Weibull" statement is therefore a statement about covariates that take enough values, not about the two-sample case.

**Parametric fits.** For the leukemia data of the [Kaplan-Meier](/kaplan-meier-estimator/) page (21 patients on 6-MP, 21 on placebo, 30 events), with $x = 1$ for placebo, maximum likelihood gives:

| law | $\hat\gamma$ (standard error) | $\hat\sigma$ | time ratio, 6-MP over placebo | log-likelihood |
|---|---|---|---|---|
| Weibull | -1.2673 (0.3106) | 0.7322 | 3.55 | -106.580 |
| log-logistic | -1.2655 (0.3257) | 0.5466 | 3.55 | -107.661 |
| lognormal | -1.3468 (0.3165) | 0.9239 | 3.85 | -106.705 |

The log-likelihoods include the $-\log y_i$ term. The three laws agree that 6-MP stretches the time to relapse by a factor of about 3.5 to 3.9. The Weibull fit has $\hat\mu = 3.5157$ and the shape $1/\hat\sigma = 1.366$, an increasing hazard. Its medians are 25.7 weeks for 6-MP and 7.2 weeks for placebo, against the Kaplan-Meier medians of 23 and 8. As a proportional hazards model it gives $\beta = -\hat\gamma/\hat\sigma = 1.731$ for placebo, a hazard ratio of 5.65, against 4.52 to 5.09 for the Cox fits with the three rules for ties on the Cox page. The log-logistic fit has a hazard ratio that starts near 10.1 at $t = 0$ and falls toward 1. These numbers were computed with Newton's method on numerical derivatives in a short script, and they are measured, not proved. There is no reference code for this page.

**Semiparametric estimation.** When the law of $W$ is left free, there is no likelihood to maximize, and three approaches are used.

- *Buckley-James (1979).* Replace each censored $\log y_i$ by its conditional expectation given $\log T_i > \log y_i$, computed from the Kaplan-Meier estimate of the residuals, and refit by least squares. Iterate. The iteration may cycle between two values instead of converging.
- *Rank estimating equations (Tsiatis 1990).* At the true $\gamma$, the residuals $e_i = \log y_i - \gamma^{\mathsf T}x_i$ are a censored sample with the same law for every $x$, so a weighted [log-rank](/log-rank-test/) statistic of $x$ on the residuals has mean zero. Solve $U(\gamma) = \sum_i \delta_i\, w(e_i)\bigl(x_i - \bar x(e_i)\bigr) \approx 0$, where $\bar x(e)$ is the mean of $x$ over the subjects with residual at least $e$, and $w = 1$ gives the log-rank weight. $U$ is a step function of $\gamma$, so "solve" means find a sign change or minimize $\|U\|$. The estimate is consistent and asymptotically normal under regularity conditions. This is cited, not proved here.
- *Gehan weights (Jin, Lin, Wei and Ying 2003).* With the Gehan weight the estimating function is the gradient of the convex function $\sum_i\sum_j \delta_i (e_i - e_j)^-$, so the estimate is the minimizer of a convex piecewise linear function, a linear program. Its variance is estimated by resampling.

**The choice of law.** The parametric fits rest on the law of $W$. The log-likelihoods of the table can be compared, since the three models have the same number of parameters, and here the Weibull fits best by a small margin. Compare the fitted curves with the Kaplan-Meier curves of each group before trusting a prediction beyond the follow-up.

## References
