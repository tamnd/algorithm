---
tag: Z68QXE
kind: model
slug: frailty-model
name: Frailty model
aliases:
- shared frailty model
- random effects survival model
area: statistics-and-inference/survival-analysis
level: advanced
summary: A survival model with an unobserved random factor that multiplies the hazard, shared within a cluster, to model heterogeneity and dependence between event times.
prereqs: [cox-proportional-hazards-model, hazard-function, survival-function, expectation-maximization]
see_also: [linear-mixed-model, cluster-robust-standard-errors, accelerated-failure-time-model, schoenfeld-residuals, breslow-estimator, laplace-transform, competing-risks, kaplan-meier-estimator]
sources:
  - paper: doi:10.2307/2061224
    title: James W. Vaupel, Kenneth G. Manton and Eric Stallard, The impact of heterogeneity in individual frailty on the dynamics of mortality, Demography 16(3), 1979
    locator: pp. 439 to 454 (the term frailty, the gamma-distributed factor, and the gap between individual and population hazards)
  - paper: doi:10.1093/biomet/65.1.141
    title: David G. Clayton, A model for association in bivariate life tables and its application in epidemiological studies of familial tendency in chronic disease incidence, Biometrika 65(1), 1978
    locator: pp. 141 to 151 (the bivariate model with a constant cross-ratio, which is the shared gamma frailty model)
  - book: isbn:9780387988733
    title: Philip Hougaard, Analysis of Multivariate Survival Data, Springer, 2000
    locator: Chapters 7 to 10 (univariate and shared frailty models, the gamma and positive stable laws, and estimation)
  - book: isbn:9780387945194
    title: Per Kragh Andersen, Ørnulf Borgan, Richard D. Gill and Niels Keiding, Statistical Models Based on Counting Processes, Springer, 1993
    locator: Chapter IX (frailty models and the EM algorithm for the gamma frailty model)
  - book: isbn:9780387987842
    title: Terry M. Therneau and Patricia M. Grambsch, Modeling Survival Data, Extending the Cox Model, Springer, 2000
    locator: Chapter 9 (frailty models fitted by penalized partial likelihood, with gamma and Gaussian frailties)
---

A frailty model adds to a hazard model an unobserved positive factor $Z$, the frailty, that multiplies the hazard. In the shared frailty model, the subjects of one cluster (the members of a family, the two eyes of a patient, the repeated infections of one child, the patients of one hospital) share the same value $Z_k$:

$$h(t \mid x_{ki}, Z_k) = Z_k\, h_0(t)\, \exp(\beta^{\mathsf T}x_{ki}).$$

Given $Z_k$ the event times in the cluster are independent, but $Z_k$ is not observed, so they are dependent in the data: a family with a high frailty has early events for all its members. With one subject per cluster, the frailty models unmeasured differences between subjects. The model explains two facts that a plain [Cox model](/cox-proportional-hazards-model/) cannot: events in a cluster are correlated, and population hazard ratios drift toward $1$ over time even when every subject's hazard ratio is constant. This page proves both for the gamma frailty.

## The machine

**The data.** Clusters $k = 1, \ldots, K$ with $n_k$ subjects each. For subject $i$ of cluster $k$ we observe $y_{ki}$, $\delta_{ki}$ and $x_{ki}$, as on the [censoring](/censoring/) page.

**The conditions.**

1. **Conditional proportional hazards.** Given $Z_k$, subject $(k, i)$ has the hazard $Z_k h_0(t)\exp(\beta^{\mathsf T}x_{ki})$.
2. **Conditional independence.** Given $Z_k$ and the covariates, the event times in cluster $k$ are independent, and censoring is independent of the event times.
3. **The frailty law.** $Z_1, \ldots, Z_K$ are independent and identically distributed, independent of the covariates, with $E[Z] = 1$ so that $h_0$ is identified. The variance $\theta = \operatorname{Var}(Z)$ measures the heterogeneity. The case $\theta = 0$ is the Cox model.
4. **Independent clusters.**

**Marginal survival.** Let $\Lambda_{ki}(t) = H_0(t)e^{\beta^{\mathsf T}x_{ki}}$, with $H_0(t) = \int_0^t h_0$. Given $Z$, the survival function is $e^{-Z\Lambda}$, so the marginal survival function is the [Laplace transform](/laplace-transform/) $\mathcal L(s) = E[e^{-sZ}]$ of the frailty, read at $\Lambda$:

$$S(t \mid x) = \mathcal L\bigl(\Lambda(t)\bigr), \qquad S(t_1, \ldots, t_{n_k} \mid \text{cluster } k) = \mathcal L\Bigl(\sum_i \Lambda_{ki}(t_i)\Bigr).$$

The second form holds because, given $Z_k$, the joint survival function is the product $\prod_i e^{-Z_k\Lambda_{ki}(t_i)} = e^{-Z_k\sum_i\Lambda_{ki}(t_i)}$.

**The gamma frailty.** The common choice is $Z \sim \text{Gamma}$ with shape $1/\theta$ and rate $1/\theta$, so $E[Z] = 1$ and $\operatorname{Var}(Z) = \theta$. Its Laplace transform is $\mathcal L(s) = (1 + \theta s)^{-1/\theta}$. *Proof.* With $a = 1/\theta$, $\int_0^\infty e^{-sz}\frac{a^a z^{a-1}e^{-az}}{\Gamma(a)}\,dz = \frac{a^a}{(a + s)^a} = (1 + s/a)^{-a}$. $\square$ Other laws in use are the positive stable law, with $\mathcal L(s) = e^{-s^\alpha}$, $0 < \alpha \le 1$ (it has no mean, so $E[Z] = 1$ is replaced by this scaling), and the lognormal law, which has no closed Laplace transform.

## What it counts

- **The coefficients $\beta$** are conditional log hazard ratios: they compare two subjects with the same frailty, such as two members of one family. They are not the hazard ratios of the population, which the next section shows to be smaller and not constant.
- **The variance $\theta$** measures both the heterogeneity between clusters and the dependence within a cluster. For the shared gamma frailty, the dependence between two event times in a cluster has Kendall's tau $\theta/(\theta + 2)$.
- **The frailty of a cluster** can be predicted from its data. For the gamma law, the conditional mean given the follow-up of cluster $k$ is

  $$E[Z_k \mid \text{data}] = \frac{1/\theta + D_k}{1/\theta + \sum_i \Lambda_{ki}(y_{ki})},$$

  where $D_k$ is the number of events in cluster $k$. *Proof.* The likelihood of the cluster given $Z_k = z$ is proportional to $z^{D_k}e^{-z\sum_i\Lambda_{ki}(y_{ki})}$. Times the gamma density $z^{1/\theta - 1}e^{-z/\theta}$, it is a gamma kernel with shape $1/\theta + D_k$ and rate $1/\theta + \sum_i\Lambda_{ki}(y_{ki})$, whose mean is the ratio. $\square$ A cluster with more events than its cumulative hazard predicts gets a frailty above $1$.

## Relation to other models

- **The Cox model** is the case $\theta = 0$. A Cox model that leaves out the frailty assumes proportional marginal hazards, which the gamma model does not have, so its estimate is a time-averaged population effect closer to $0$ than $\beta$. Its usual standard errors also ignore the dependence in a cluster. [Cluster-robust standard errors](/cluster-robust-standard-errors/) fix the standard errors, not the change in meaning of the coefficient.
- **Mixed models.** The frailty plays the role of the cluster term of a [linear mixed model](/linear-mixed-model/), on the log hazard scale: $\log Z_k$ is added to $\beta^{\mathsf T}x$. A lognormal frailty is a Gaussian term on that scale.
- **Copulas.** The joint survival function of a shared frailty model is an Archimedean copula of the marginal survival functions. For the gamma law, $S_i^{-\theta} = 1 + \theta\Lambda_i$, so

  $$S(t_1, t_2) = \bigl(1 + \theta(\Lambda_1 + \Lambda_2)\bigr)^{-1/\theta} = \bigl(S_1(t_1)^{-\theta} + S_2(t_2)^{-\theta} - 1\bigr)^{-1/\theta},$$

  the Clayton copula. Clayton (1978) derived it from the condition that the cross-ratio, the hazard of $T_1$ at $t_1$ given $T_2 = t_2$ over that given $T_2 > t_2$, equals the constant $1 + \theta$.
- **Accelerated failure time.** With $\theta = 1$ and a Weibull baseline $H_0 = \lambda t^\rho$, the marginal law $S = (1 + \lambda t^\rho e^{\beta^{\mathsf T}x})^{-1}$ is a log-logistic [AFT model](/accelerated-failure-time-model/). Without clusters, the data cannot tell this frailty model from that AFT model.
- **Competing risks.** Correlated frailties for two causes give dependent latent times, one of the models in which the latent failure times of [competing risks](/competing-risks/) are dependent.

## Known results in the model

**The marginal hazard of the gamma frailty model.** One subject, gamma frailty with variance $\theta > 0$. Then

$$S(t \mid x) = \bigl(1 + \theta H_0(t)e^{\beta^{\mathsf T}x}\bigr)^{-1/\theta}, \qquad h(t \mid x) = \frac{h_0(t)\,e^{\beta^{\mathsf T}x}}{1 + \theta H_0(t)e^{\beta^{\mathsf T}x}}.$$

*Proof.* The first is $\mathcal L(\Lambda(t))$ with the gamma transform. Then $h = -\frac{d}{dt}\log S = \frac1\theta\cdot\frac{\theta h_0(t)e^{\beta^{\mathsf T}x}}{1 + \theta H_0(t)e^{\beta^{\mathsf T}x}}$. $\square$

The same hazard is $h_0(t)e^{\beta^{\mathsf T}x}E[Z \mid T \ge t, x]$, with $E[Z \mid T \ge t, x] = 1/(1 + \theta\Lambda(t))$ by the posterior formula above with $D = 0$. The survivors at time $t$ are less frail on average, because the frail have already had the event. Vaupel, Manton and Stallard (1979) used this to explain why population mortality curves rise more slowly than individual ones.

**The marginal hazards are not proportional.** Compare $x = 1$ and $x = 0$ for one binary covariate, with $r = e^{\beta} \ne 1$ and $\theta > 0$. The ratio of the marginal hazards is

$$\frac{h(t \mid 1)}{h(t \mid 0)} = r\,\frac{1 + \theta H_0(t)}{1 + \theta r H_0(t)}.$$

*Proof that it is not constant.* As a function of $u = H_0(t) \ge 0$, the derivative of $(1 + \theta u)/(1 + \theta ru)$ is $\theta(1 - r)/(1 + \theta ru)^2$, which is not $0$. So the ratio is strictly monotone in $u$. It equals $r$ at $u = 0$ and tends to $r \cdot \frac{\theta u}{\theta r u} = 1$ as $u \to \infty$. Since $H_0$ increases, the population hazard ratio moves from $r$ toward $1$ over time. $\square$

With $\theta = 1$ and $r = 2$, exactly:

| $H_0(t)$ | 0 | 0.5 | 1 | 3 | 9 | $\to\infty$ |
|---|---|---|---|---|---|---|
| marginal hazard ratio | 2 | 3/2 | 4/3 | 8/7 | 20/19 | 1 |

So a Cox model fitted to data from this frailty model sees a hazard ratio that is close to $2$ early and fades, and its [Schoenfeld residuals](/schoenfeld-residuals/) show a downward trend. A treatment that halves every subject's hazard can look like a treatment whose effect wears off.

**The positive stable frailty keeps proportional hazards.** With $\mathcal L(s) = e^{-s^\alpha}$, $S(t \mid x) = \exp\bigl(-H_0(t)^\alpha e^{\alpha\beta^{\mathsf T}x}\bigr)$, a proportional hazards model with baseline $H_0^\alpha$ and coefficient $\alpha\beta$. The marginal hazard ratio is constant, but it is $e^{\alpha\beta}$, closer to $1$ than the conditional $e^\beta$ (Hougaard 2000).

**Kendall's tau of the shared gamma frailty.** For the Clayton copula, $\tau = \theta/(\theta + 2)$. *Computation.* The copula is Archimedean with generator $\varphi(v) = (v^{-\theta} - 1)/\theta$, and for such copulas $\tau = 1 + 4\int_0^1 \varphi(v)/\varphi'(v)\,dv$, a known formula that we cite. Here $\varphi/\varphi' = -(v - v^{\theta + 1})/\theta$, whose integral over $[0, 1]$ is $-\frac1\theta\bigl(\frac12 - \frac{1}{\theta + 2}\bigr) = -\frac{1}{2(\theta + 2)}$. So $\tau = 1 - \frac{2}{\theta + 2} = \frac{\theta}{\theta + 2}$. $\square$ A variance $\theta = 1$ gives $\tau = 1/3$.

**The marginal likelihood of the gamma model.** Integrating out $Z_k$ gives, for cluster $k$,

$$L_k = \prod_i \bigl(h_0(y_{ki})e^{\beta^{\mathsf T}x_{ki}}\bigr)^{\delta_{ki}} \cdot \frac{\Gamma(1/\theta + D_k)\,\theta^{D_k}}{\Gamma(1/\theta)\,\bigl(1 + \theta\sum_i\Lambda_{ki}(y_{ki})\bigr)^{1/\theta + D_k}}.$$

*Proof.* Given $Z_k = z$ the likelihood is $\prod_i (zh_0e^{\beta^{\mathsf T}x})^{\delta}e^{-z\Lambda}$, and $E[Z^De^{-ZA}] = \frac{a^a\Gamma(a + D)}{\Gamma(a)(a + A)^{a + D}} = \frac{\Gamma(a + D)\,\theta^D}{\Gamma(a)(1 + \theta A)^{a + D}}$ with $a = 1/\theta$. $\square$ With a parametric $h_0$, such as Weibull, maximize $\sum_k\log L_k$ directly.

**Estimation with an unspecified baseline.** The [EM algorithm](/expectation-maximization/) treats the $Z_k$ as missing data. The E-step computes $E[Z_k \mid \text{data}]$ by the formula above (and $E[\log Z_k \mid \text{data}]$ for $\theta$). The M-step fits a Cox model with the offsets $\log E[Z_k \mid \text{data}]$ and updates the baseline by the [Breslow estimator](/breslow-estimator/) with the risk sums weighted by $E[Z_k \mid \text{data}]$. Each EM step does not decrease the marginal likelihood, a general property of EM. For $\theta$ one maximizes the profile likelihood over a grid or by a one-dimensional search. Therneau and Grambsch (2000) show that the same fit comes from a penalized partial likelihood. The asymptotic theory for the semiparametric estimate is harder than for the Cox model and is cited in Andersen et al. (1993), not proved here.

**Identifiability without clusters.** With one subject per cluster, the frailty law and $h_0$ are identified only through the assumed shape of the model. A gamma frailty with a Weibull baseline and a log-logistic AFT model give the same data distribution, as noted above, so conclusions about $\theta$ from univariate data rest on the parametric assumptions. Clusters with several subjects identify $\theta$ from the dependence within clusters.

**Checks.** There is no reference code for this page. The Laplace transform, the marginal survival and hazard, the non-constant hazard ratio, the posterior mean, the marginal likelihood and the Clayton form are proved above. The formula for Kendall's tau of Archimedean copulas and the asymptotics of the EM estimate are cited.

## References
