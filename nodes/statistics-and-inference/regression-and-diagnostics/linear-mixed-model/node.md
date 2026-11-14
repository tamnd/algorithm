---
tag: RBPBWM
kind: model
slug: linear-mixed-model
name: Linear mixed model
aliases:
- mixed-effects model
- random effects model
- hierarchical linear model
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: A linear model y = X b + Z u + e with fixed effects b and random effects u. It models grouped or repeated measures with correlated errors.
prereqs: [generalized-least-squares, ordinary-least-squares, covariance-matrix, likelihood-ratio-test]
see_also: [henderson-mixed-model-equations, restricted-maximum-likelihood, one-way-anova, hierarchical-bayesian-model, generalized-estimating-equations, cluster-robust-standard-errors, kriging, laplace-approximation]
sources:
  - paper: doi:10.2307/2529876
    title: "Nan M. Laird and James H. Ware, Random-effects models for longitudinal data, Biometrics 38(4), 1982, pp. 963 to 974"
    locator: The whole paper (the two-stage model y_i = X_i b + Z_i u_i + e_i for repeated measures, and its fit by EM with ML and REML)
  - paper: doi:10.2307/2529430
    title: "C. R. Henderson, Best linear unbiased estimation and prediction under a selection model, Biometrics 31(2), 1975, pp. 423 to 447"
    locator: The mixed model equations and the BLUE and BLUP they give
  - paper: doi:10.1214/ss/1177011926
    title: "G. K. Robinson, That BLUP is a good thing: the estimation of random effects, Statistical Science 6(1), 1991, pp. 15 to 32"
    locator: The whole paper (derivations of BLUP, its links to Bayes, kriging and smoothing, and the one-way example)
  - paper: doi:10.1080/01621459.1977.10480998
    title: "David A. Harville, Maximum likelihood approaches to variance component estimation and to related problems, Journal of the American Statistical Association 72(358), 1977, pp. 320 to 338"
    locator: The whole paper (ML and REML for the mixed model, their properties and algorithms)
  - paper: doi:10.1080/01621459.1987.10478472
    title: "Steven G. Self and Kung-Yee Liang, Asymptotic properties of maximum likelihood estimators and likelihood ratio tests under nonstandard conditions, Journal of the American Statistical Association 82(398), 1987, pp. 605 to 610"
    locator: The mixture of chi-squared laws for a parameter on the boundary, case 5 (one variance component)
  - paper: doi:10.2307/2533455
    title: "Daniel O. Stram and Jae Won Lee, Variance components testing in the longitudinal mixed effects model, Biometrics 50(4), 1994, pp. 1171 to 1177"
    locator: The whole paper (the mixtures for tests of random intercepts and random slopes)
  - paper: doi:10.1111/j.1467-9868.2004.00438.x
    title: "Ciprian M. Crainiceanu and David Ruppert, Likelihood ratio tests in linear mixed models with one variance component, Journal of the Royal Statistical Society Series B 66(1), 2004, pp. 165 to 185"
    locator: The whole paper (the exact finite sample null law of the LR and restricted LR statistics, and when the 50:50 mixture fails)
  - paper: doi:10.2307/2533558
    title: "Michael G. Kenward and James H. Roger, Small sample inference for fixed effects from restricted maximum likelihood, Biometrics 53(3), 1997, pp. 983 to 997"
    locator: The whole paper (the adjusted covariance and the F approximation for tests of fixed effects)
  - book: isbn:9780471621621
    title: Shayle R. Searle, George Casella and Charles E. McCulloch, Variance Components, Wiley, 1992
    locator: Chapter 3 (the balanced one-way classification, ANOVA estimators and their distributions) and Chapter 7 (prediction of random variables, BLUP)
  - book: isbn:9780387989570
    title: José C. Pinheiro and Douglas M. Bates, Mixed-Effects Models in S and S-PLUS, Springer, 2000
    locator: Chapters 1 and 2 (the model, ML and REML, tests of variance components on the boundary)
---

A linear mixed model, or mixed-effects model, is a linear regression in which part of the coefficients are fixed unknown numbers and part are random variables with mean 0. In matrix form $y = Xb + Zu + e$, where $b$ is the vector of fixed effects (on this page the coefficient vector is written $b$), $u \sim N(0, G)$ is the vector of random effects and $e \sim N(0, R)$ is the error. The random effects make the observations of the same group, subject or plot correlated, so the model fits clustered data, repeated measures and longitudinal studies, split plots, and genetic evaluation of animals. Given the covariance parameters, $b$ is estimated by [generalized least squares](/generalized-least-squares/) and $u$ is predicted by BLUP, both from [Henderson's mixed model equations](/henderson-mixed-model-equations/). The covariance parameters themselves are usually estimated by [restricted maximum likelihood](/restricted-maximum-likelihood/).

## The machine

**Data.** A response $y \in \mathbb R^n$, a fixed-effects design $X$ ($n \times p$, rank $p$, usually with an intercept column) and a random-effects design $Z$ ($n \times q$).

**Model.**

$$y = Xb + Zu + e, \qquad u \sim N_q(0, G(\theta)), \qquad e \sim N_n(0, R(\theta)), \qquad u \text{ and } e \text{ independent}.$$

The matrices $G$ and $R$ depend on a short vector $\theta$ of covariance parameters. The commonest choice is $R = \sigma_e^2 I$, and $G$ block diagonal with one block for each random factor.

**The marginal law.** Since $y$ is a linear function of the independent normal vectors $u$ and $e$,

$$y \sim N_n(Xb, V(\theta)), \qquad V = ZGZ^\top + R.$$

All inference on $b$ and $\theta$ uses this law; $u$ is not a parameter and is predicted, not estimated.

**Parameter space.** $b \in \mathbb R^p$, and $\theta$ in the set where $G(\theta)$ is positive semidefinite and $R(\theta)$ is positive definite. A variance component equal to 0 is allowed, and it is a boundary point of this set.

**Common layouts.**

- *Random intercepts (one-way).* Groups $i = 1, \dots, a$ with $n_i$ observations, $y_{ij} = b_0 + u_i + e_{ij}$, $u_i \sim N(0, \sigma_u^2)$, $e_{ij} \sim N(0, \sigma_e^2)$. Here $Z$ is the $n \times a$ matrix of group indicators and $G = \sigma_u^2 I_a$.
- *Random intercepts and slopes (Laird and Ware 1982).* For subject $i$, $y_i = X_ib + Z_iu_i + e_i$ with $u_i \sim N(0, D)$ and $e_i \sim N(0, \sigma_e^2 I)$; for a straight line in time, $Z_i$ has columns $\mathbf 1$ and the times, and $D$ is a $2 \times 2$ covariance matrix.
- *Nested and crossed factors.* Pupils in classes in schools give nested blocks of $G$; subjects crossed with test items give two random factors whose indicators overlap, and $V$ has no block diagonal form.
- *Known relationships.* In animal breeding $G = \sigma_a^2\mathcal A$, where $\mathcal A$ is the matrix of additive relationships computed from the pedigree.

## What it counts

- **The fixed effects $b$.** In a linear mixed model $E[y] = Xb$, so $b$ is both the effect within a group and the effect averaged over the population. (In a mixed model with a nonlinear link these two differ.)
- **The variance components** $\theta$, for example $\sigma_u^2$ and $\sigma_e^2$, and functions of them such as the intraclass correlation $\rho = \sigma_u^2/(\sigma_u^2 + \sigma_e^2)$.
- **The predicted random effects** $\tilde u = GZ^\top V^{-1}(y - X\hat b)$, the best linear unbiased predictor, and predictions such as $x_0^\top\hat b + z_0^\top\tilde u$ for a known group. In the one-way layout, $\tilde u_i = \frac{n_i\sigma_u^2}{n_i\sigma_u^2 + \sigma_e^2}(\bar y_{i\cdot} - \hat b_0)$: the group mean is pulled toward the overall mean, more for small groups.
- **Standard errors** from $\operatorname{Cov}(\hat b) = (X^\top V^{-1}X)^{-1}$ and from the prediction error variance of $\tilde u$, both at the true $\theta$; plugging in $\hat\theta$ makes them too small in small samples.

## Relation to other models

- **[Ordinary least squares](/ordinary-least-squares/)** is the case $G = 0$, $R = \sigma^2 I$.
- **[Generalized least squares](/generalized-least-squares/)** is the case of a known $V$. The mixed model gives $V$ a structure with few parameters, so that it can be estimated.
- **Fixed group effects.** Treating the $u_i$ as fixed (one indicator column for each group) is the limit $\sigma_u^2 \to \infty$ of the mixed model; then $\tilde u_i$ becomes the plain group mean minus the overall mean, and the model cannot estimate effects of variables that are constant within groups.
- **[Ridge regression](/ridge-regression/).** With $G = \sigma_u^2 I$ and $R = \sigma_e^2 I$, the BLUP of $u$ is the ridge estimate with penalty $\sigma_e^2/\sigma_u^2$, as Henderson's equations show. Penalized splines and [smoothing splines](/smoothing-spline/) can be written as mixed models in the same way, so REML chooses their smoothing parameter.
- **Bayesian models.** With a flat prior on $b$ and $\theta$ known, the posterior mean of $u$ is the BLUP. Putting a prior on $\theta$ as well gives a [hierarchical Bayesian model](/hierarchical-bayesian-model/); plugging in an estimate $\hat\theta$ is [empirical Bayes](/empirical-bayes/).
- **[Kriging](/kriging/) and [Gaussian processes](/gaussian-process/).** A spatial process with a parametric covariance is a mixed model with $Z = I$; the kriging predictor is the BLUP, and universal kriging estimates the mean by GLS.
- **Marginal models.** [Generalized estimating equations](/generalized-estimating-equations/) and [cluster-robust standard errors](/cluster-robust-standard-errors/) target $b$ only and do not need the normal law or a model for $G$; they give no predictions of group effects.
- **[One-way ANOVA](/one-way-anova/) with a random factor** is the balanced one-way layout below.
- **Survival data.** A random effect inside a hazard model is a [frailty model](/frailty-model/). Non-normal responses with random effects in a generalized linear model need numerical integration or a Laplace approximation for the likelihood.

## Known results in the model

**1. Within-group correlation (proved here).** In the one-way layout, $\operatorname{Var}(y_{ij}) = \sigma_u^2 + \sigma_e^2$, $\operatorname{Cov}(y_{ij}, y_{ik}) = \sigma_u^2$ for $j \ne k$, and observations in different groups are independent. *Proof.* $\operatorname{Cov}(b_0 + u_i + e_{ij}, b_0 + u_{i'} + e_{i'k}) = \operatorname{Cov}(u_i, u_{i'}) + \operatorname{Cov}(e_{ij}, e_{i'k})$ by independence of $u$ and $e$; the first term is $\sigma_u^2$ when $i = i'$ and 0 otherwise, the second is $\sigma_e^2$ when $(i, j) = (i', k)$ and 0 otherwise. $\square$ So each block of $V$ has the compound symmetry form $\sigma_e^2 I + \sigma_u^2\mathbf 1\mathbf 1^\top$, and the correlation of two observations in one group is $\rho$. A test or interval that treats the $n$ observations as independent uses the wrong variance: the variance of a group mean is $\sigma_u^2 + \sigma_e^2/n_i$, and the $\sigma_u^2$ part does not shrink with $n_i$.

**2. Estimation and prediction for known $\theta$.** The GLS estimate $\hat b = (X^\top V^{-1}X)^{-1}X^\top V^{-1}y$ is the maximum likelihood estimate of $b$ and the best linear unbiased estimator (Aitken). The predictor $\tilde u = GZ^\top V^{-1}(y - X\hat b)$ has the smallest mean squared error among linear predictors $\tilde u = Ly$ with $E[Ly - u] = 0$ for all $b$ (Henderson 1975). Both come from one linear system; the proofs are on the [mixed model equations](/henderson-mixed-model-equations/) page.

**3. The balanced one-way layout (proved here).** Let $n_i = m$ for all $a$ groups and $N = am$. Let $\mathrm{SSA} = m\sum_i(\bar y_{i\cdot} - \bar y_{\cdot\cdot})^2$ with $a - 1$ degrees of freedom and $\mathrm{SSE} = \sum_{i,j}(y_{ij} - \bar y_{i\cdot})^2$ with $a(m - 1)$, and $\mathrm{MSA}$, $\mathrm{MSE}$ the mean squares. Then $\mathrm{SSA}/(\sigma_e^2 + m\sigma_u^2) \sim \chi^2_{a-1}$ and $\mathrm{SSE}/\sigma_e^2 \sim \chi^2_{a(m-1)}$, and they are independent.

*Proof.* Write $y_{ij} = b_0 + u_i + e_{ij}$. The within deviations $y_{ij} - \bar y_{i\cdot} = e_{ij} - \bar e_{i\cdot}$ do not involve $u$, and for each $i$ the vector $(e_{ij} - \bar e_{i\cdot})_j$ is independent of $\bar e_{i\cdot}$ (the sample mean and the deviations of a normal sample are independent), so $\mathrm{SSE}/\sigma_e^2 = \sum_i\sum_j(e_{ij} - \bar e_{i\cdot})^2/\sigma_e^2$ is a sum of $a$ independent $\chi^2_{m-1}$ variables. The group means $\bar y_{i\cdot} = b_0 + u_i + \bar e_{i\cdot}$ are functions of $u$ and the $\bar e_{i\cdot}$ only, hence independent of $\mathrm{SSE}$, and they are iid $N(b_0, \sigma_u^2 + \sigma_e^2/m)$. So $\sum_i(\bar y_{i\cdot} - \bar y_{\cdot\cdot})^2/(\sigma_u^2 + \sigma_e^2/m) \sim \chi^2_{a-1}$, which is the claim for $\mathrm{SSA}$. $\square$

So $E[\mathrm{MSA}] = \sigma_e^2 + m\sigma_u^2$ and $E[\mathrm{MSE}] = \sigma_e^2$, and the ANOVA estimator $\hat\sigma_u^2 = (\mathrm{MSA} - \mathrm{MSE})/m$ is unbiased. It is negative exactly when $\mathrm{MSA} < \mathrm{MSE}$. With $\gamma = \sigma_u^2/\sigma_e^2$, the ratio $F = \frac{\mathrm{MSA}/(1 + m\gamma)}{\mathrm{MSE}}$ has the $F_{a-1, a(m-1)}$ law, so

$$P(\hat\sigma_u^2 < 0) = P\Bigl(F_{a-1, a(m-1)} < \frac{1}{1 + m\gamma}\Bigr).$$

For $\gamma = 0$ and $m = 4$ this is 0.595, 0.562, 0.539 and 0.521 for $a = 3, 5, 10, 30$. For $a = 5$ and $\gamma = 1$ it is 0.066. W. A. Thompson (1962) and Searle, Casella and McCulloch discuss what to do with a negative estimate; REML and ML both return 0 instead, as the [REML](/restricted-maximum-likelihood/) page shows.

**4. Testing a variance component on the boundary.** The null $\sigma_u^2 = 0$ is on the edge of the parameter space, so [Wilks' theorem](/wilks-theorem/) does not apply. When the data have many independent groups, the likelihood ratio statistic $\Lambda$ for one variance component has the limit law $\frac12\chi^2_0 + \frac12\chi^2_1$ under the null (Chernoff 1954; Self and Liang 1987): $\Lambda = 0$ with probability $\frac12$, as when the estimate falls on the boundary, and otherwise $\chi^2_1$. The right p-value is half the $\chi^2_1$ tail, $P = \frac12P(\chi^2_1 \ge \Lambda)$ for $\Lambda > 0$, and the 5% cut is 2.706 instead of 3.841. For a random slope added to a random intercept, the limit is $\frac12\chi^2_1 + \frac12\chi^2_2$ (Stram and Lee 1994). The $\chi^2_1$ test is conservative. In the balanced example $y = (10, 12, 14;\ 15, 16, 17;\ 18, 20, 22)$ with $a = m = 3$, the REML fits give $\Lambda = 6.920$, so the $\chi^2_1$ p-value is 0.0085 and the mixture p-value is 0.0043.

The mixture is a large-sample result in the number of groups. In the balanced layout the restricted likelihood ratio is 0 exactly when $\mathrm{MSA} \le \mathrm{MSE}$, so by Result 3 its mass at 0 under the null is $P(F_{a-1, a(m-1)} \le 1)$, the $\gamma = 0$ values above. This tends to $\frac12$ only as $a \to \infty$; with $a$ fixed and $m \to \infty$ it tends to $P(\chi^2_{a-1} \le a - 1)$, which is $1 - e^{-1} = 0.632$ for $a = 3$. Crainiceanu and Ruppert (2004) give the exact finite sample law for one variance component and show cases where the mass at 0 is far above $\frac12$. A parametric bootstrap under the null fit is a safe check.

**5. Tests of fixed effects.** Wald and $F$ tests for $b$ use $(X^\top\hat V^{-1}X)^{-1}$, which ignores the error in $\hat\theta$. The Kenward-Roger (1997) correction adjusts this covariance and the degrees of freedom of the $F$ reference law. Likelihood ratio tests of fixed effects use maximum likelihood fits, not REML fits.

## References
