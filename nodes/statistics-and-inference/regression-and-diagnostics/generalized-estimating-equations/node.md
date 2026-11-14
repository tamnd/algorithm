---
tag: F7TMV3
kind: technique
slug: generalized-estimating-equations
name: Generalized estimating equations
aliases:
- GEE
- Liang-Zeger estimating equations
area: statistics-and-inference/regression-and-diagnostics
level: advanced
summary: 'Liang and Zeger''s method for correlated responses: solve GLM-type score equations with a working correlation, and use the sandwich for valid standard errors.'
prereqs: [quasi-likelihood, generalized-linear-model, cluster-robust-standard-errors, m-estimator]
see_also: [generalized-least-squares, linear-mixed-model, inverse-probability-weighting, missing-data-mechanism, logistic-regression, fisher-scoring, generalized-method-of-moments, heteroscedasticity-consistent-standard-errors]
sources:
  - paper: doi:10.1093/biomet/73.1.13
    title: "Kung-Yee Liang and Scott L. Zeger, Longitudinal data analysis using generalized linear models, Biometrika 73(1), 1986, pp. 13 to 22"
    locator: The whole paper (the estimating equations with a working correlation, the consistency of the estimate when only the mean model is right, and the robust covariance)
  - paper: doi:10.2307/2531248
    title: "Scott L. Zeger and Kung-Yee Liang, Longitudinal data analysis for discrete and continuous outcomes, Biometrics 42(1), 1986, pp. 121 to 130"
    locator: The whole paper (the method for binary, count and continuous repeated measures, with the moment estimates of the correlation and examples)
  - paper: doi:10.1080/03610919408813210
    title: "Margaret S. Pepe and Garnet L. Anderson, A cautionary note on inference for marginal regression models with longitudinal data and general correlated response data, Communications in Statistics, Simulation and Computation 23(4), 1994, pp. 939 to 951"
    locator: The whole paper (with time-varying covariates a non-diagonal working correlation can bias the estimate unless the mean given all covariates of the cluster equals the mean given the current one)
  - paper: doi:10.1111/j.0006-341X.2001.00126.x
    title: "Lloyd A. Mancl and Timothy A. DeRouen, A covariance estimator for GEE with improved small-sample properties, Biometrics 57(1), 2001, pp. 126 to 134"
    locator: The whole paper (the robust covariance is biased downward with few clusters, and a leverage-type correction)
  - paper: doi:10.1111/j.0006-341X.2001.00120.x
    title: "Wei Pan, Akaike's information criterion in generalized estimating equations, Biometrics 57(1), 2001, pp. 120 to 125"
    locator: The whole paper (QIC for choosing the working correlation and QICu for choosing covariates)
  - paper: doi:10.1080/01621459.1995.10476493
    title: "James M. Robins, Andrea Rotnitzky and Lue Ping Zhao, Analysis of semiparametric regression models for repeated outcomes in the presence of missing data, Journal of the American Statistical Association 90(429), 1995, pp. 106 to 121"
    locator: The whole paper (inverse probability weighted estimating equations that stay consistent when responses are missing at random)
---

Generalized estimating equations fit a regression model for the mean of correlated responses, such as repeated measures on the same person or pupils in the same school. The data come in $G$ independent clusters, and the model specifies only the marginal mean $E y_{ij} = \mu_{ij} = g^{-1}(x_{ij}^\top b)$ and a variance function, as in [quasi-likelihood](/quasi-likelihood/). The correlation inside a cluster is replaced by a working guess $R(\alpha)$. Liang and Zeger (1986) showed that the estimate is consistent even when the guess is wrong, as long as the mean model is right, and that the sandwich covariance $B^{-1}MB^{-1}$ gives valid standard errors as the number of clusters grows. A good guess only makes the estimate more precise. With the independence guess the estimate is the ordinary [generalized linear model](/generalized-linear-model/) fit, and the sandwich is the [cluster-robust covariance](/cluster-robust-standard-errors/).

## In plain words

When the same patient is measured many times, the measurements are related, so they carry less information than the same number of measurements from different patients. Ordinary regression ignores this and reports too much certainty. This method fits the usual kind of regression line for the average response, but it also takes a guess at how measurements in the same group are related. The guess decides how much weight each measurement gets. If the guess is good, the estimate is more precise. If it is bad, the estimate is still right on average for many groups. The uncertainty is then measured from how much the groups really differ from each other, not from the guess, so it stays honest either way.

## When it applies

- **Clustered data.** Clusters $i = 1, \dots, G$ are independent, with $m_i$ responses $y_i = (y_{i1}, \dots, y_{im_i})$ and an $m_i \times p$ matrix $X_i$ of covariates. Responses inside a cluster may be correlated in any way.
- **A marginal mean model.** $E[y_{ij} \mid X_i] = \mu_{ij} = g^{-1}(x_{ij}^\top b)$, with a link $g$ and $\operatorname{Var}y_{ij} = \phi V(\mu_{ij})$ for a variance function $V$. The coefficients describe the population average, not a single cluster.
- **The estimating equations.** With $D_i = \partial\mu_i/\partial b$ ($m_i \times p$), $S_i = \operatorname{diag}(\sqrt{V(\mu_{ij})})$ and the working covariance $V_i = \phi S_iR(\alpha)S_i$,

$$U(b) = \sum_{i=1}^GD_i^\top V_i^{-1}(y_i - \mu_i) = 0.$$

- **Why a wrong guess does not bias it.** For any fixed $\alpha$, $D_i$ and $V_i$ depend on $X_i$ and $b$ only, so $E[D_i^\top V_i^{-1}(y_i - \mu_i) \mid X_i] = D_i^\top V_i^{-1}E[y_i - \mu_i \mid X_i] = 0$ at the true $b$. This is exact, and it is the reason for consistency. It needs the mean of $y_{ij}$ given all of $X_i$, not only given $x_{ij}$, to follow the model; Pepe and Anderson (1994) showed that this can fail with time-varying covariates.
- **Many clusters.** The asymptotic theory lets $G \to \infty$ with bounded $m_i$. The working correlation must have a parameter $\alpha$ that can be estimated at rate $\sqrt G$; any moment estimate below qualifies.

## The template

```pseudo id=main
GEE((X_1, y_1), ..., (X_G, y_G))
L1  choose LINK g, VARIANCE-FUNCTION V, WORKING-CORRELATION R(α)    ▷ holes
L2  b ← START                                                       ▷ hole: 0, or the independence fit
L3  repeat
L4      (φ̂, α̂) ← MOMENTS of the Pearson residuals rᵢⱼ = (yᵢⱼ - μᵢⱼ) / √V(μᵢⱼ)
L5      for each cluster i: μᵢ, Dᵢ = ∂μᵢ/∂b, Vᵢ = Sᵢ R(α̂) Sᵢ
L6      b ← b + (Σᵢ DᵢᵀVᵢ⁻¹Dᵢ)⁻¹ Σᵢ DᵢᵀVᵢ⁻¹(yᵢ - μᵢ)               ▷ a Fisher scoring step
L7  until the step is small
L8  return b, B⁻¹MB⁻¹ with B = Σᵢ DᵢᵀVᵢ⁻¹Dᵢ, M = Σᵢ DᵢᵀVᵢ⁻¹(yᵢ - μᵢ)(yᵢ - μᵢ)ᵀVᵢ⁻¹Dᵢ
```

The holes are the mean and variance model and the working correlation (line L1) and the start (line L2). Common working correlations are independence ($R = I$), exchangeable ($R_{jk} = \alpha$ for $j \ne k$) and first-order autoregressive ($R_{jk} = \alpha^{|j-k|}$). The implementation estimates $\phi$ by $\sum r_{ij}^2/(N - p)$, with $N = \sum m_i$, and $\alpha$ by the mean of $r_{ij}r_{ik}$ over the pairs of the structure divided by $\hat\phi$; it keeps $\alpha$ inside the range where $R$ is positive definite. Since $\phi$ cancels from line L6, the update needs $V_i$ only up to the factor $\phi$, and $\phi$ enters only the model-based covariance $\hat\phi(\sum_iD_i^\top(S_iRS_i)^{-1}D_i)^{-1}$, which is valid only if $R$ is right. One step costs $\Theta(\sum_i(m_i^3 + m_i^2p + m_ip^2) + p^3)$.

**What is proved and what is cited.** The page and the tests show four exact facts. With $R = I$, $D_i^\top V_i^{-1}(y_i - \mu_i) = \sum_jx_{ij}\frac{d\mu_{ij}}{d\eta}\frac{y_{ij} - \mu_{ij}}{\phi V(\mu_{ij})}$, which is the generalized linear model score, so the fit is the GLM fit. For the identity link with $V = 1$ and a fixed $\alpha$, the equations are $\sum_iX_i^\top R^{-1}(y_i - X_ib) = 0$, the normal equations of [generalized least squares](/generalized-least-squares/) with a block diagonal covariance, and line L6 reaches them in one step. With $R = I$ and the identity link, $B^{-1}MB^{-1} = (X^\top X)^{-1}\big(\sum_iX_i^\top e_ie_i^\top X_i\big)(X^\top X)^{-1}$, the CR0 cluster-robust covariance. And the estimating function has mean zero for every working correlation, shown above. The following are cited from Liang and Zeger (1986): if the mean model is right and $\hat\alpha$ and $\hat\phi$ are $\sqrt G$-consistent, then $\hat b$ is consistent and $\sqrt G(\hat b - b)$ is asymptotically normal with a covariance consistently estimated by $G$ times line L8, whatever $R$ is; and if $R$ is right, the estimate is efficient among estimates of this form. These are results for $G \to \infty$, and the coverage at a given $G$ is only measured.

## Classic examples

**The independence fit is the GLM fit.** The page example of the [cluster-robust standard errors](/cluster-robust-standard-errors/) has $x = 1, \dots, 6$, $y = (2, 3, 2, 4, 7, 8)$ and the clusters $\{1, 2\}$, $\{3, 4\}$, $\{5, 6\}$, with an intercept. With the identity link and $V = 1$:

| working correlation | $\hat b$ | slope SE, sandwich | slope SE, model-based |
|---|---|---|---|
| independence | $(-1/15, 44/35)$ | 0.2171 | 0.2848 |
| exchangeable, $\alpha = 1/2$ fixed | $(-13/123, 52/41)$ | 0.1953 | |
| exchangeable, $\hat\alpha = 0.587$ | $(-0.1189, 1.2721)$ | 0.1903 | 0.3218 |

The independence row is least squares, $\hat\phi = 149/105$ is the residual mean square, and the sandwich SE 0.2171 is the CR0 value on the cluster-robust page; the tests check these in exact arithmetic. The fixed-$\alpha$ row equals generalized least squares with the block diagonal covariance, also exactly. With only 3 clusters none of these standard errors can be trusted, which is the point of the next example.

**Random intercept data, measured.** Take $G = 30$ clusters of 4, $y_{ij} = 1 + 0.5x_i + 0.5w_{ij} + a_i + \varepsilon_{ij}$ with $a_i$ and $\varepsilon_{ij}$ independent $N(0, 1)$, so that the true correlation is exchangeable with $\alpha = 0.5$, a cluster-level covariate $x_i$ and a covariate $w_{ij}$ that varies inside clusters. Over 1000 data sets, the coverage of 95% Wald intervals was:

| interval | slope of $x_i$ | slope of $w_{ij}$ |
|---|---|---|
| independence, model-based | 0.777 | 0.943 |
| independence, sandwich | 0.921 | 0.928 |
| exchangeable, sandwich | 0.921 | 0.916 |
| exchangeable, model-based | 0.929 | 0.949 |

The standard deviation of the estimate of the $w$ slope was 0.1317 with the independence correlation and 0.1055 with the exchangeable one, a variance ratio of 0.64. So the right working correlation pays for covariates that vary inside clusters, and the ordinary model-based errors are far too small for covariates that are constant inside clusters. The sandwich covers a little below 0.95 with 30 clusters; the Monte Carlo standard error of each coverage is about 0.007. This is the same model as a [linear mixed model](/linear-mixed-model/) with a random intercept, whose marginal covariance is exchangeable.

**Overdispersed counts.** With $G = 40$ clusters of 4 Poisson counts whose means share a gamma-distributed cluster factor with mean 1 and shape 2, the marginal mean is still $\exp(x_{ij}^\top b)$. The log link with $V(\mu) = \mu$ and an exchangeable working correlation converged in all 500 data sets, with a mean $\hat\alpha$ of 0.484. The coverage for the cluster-level slope was 0.770 for the independence model-based interval and 0.928 for both sandwich intervals; for the within-cluster slope it was 0.948, 0.918 and 0.924.

**Binary responses.** With the logit link and $V(\mu) = \mu(1 - \mu)$, the coefficients are population-averaged log odds ratios, as in [logistic regression](/logistic-regression/). They differ from the cluster-specific coefficients of a random-effects logistic model, which are larger in absolute value; neither is wrong, they answer different questions.

**Missing responses.** If some $y_{ij}$ are missing, the unweighted equations stay unbiased only when the responses are missing completely at random. Under missing at random, weighting each term by the inverse of the probability of being observed, as in [inverse probability weighting](/inverse-probability-weighting/), restores consistency (Robins, Rotnitzky and Zhao, 1995); see the [missing data mechanism](/missing-data-mechanism/) page for the definitions.

## Variations

- **Choice of working correlation.** Use independence, exchangeable, AR(1) for equally spaced times, or an unstructured matrix when clusters are small and many. Pan (2001) proposed QIC, a quasi-likelihood analogue of AIC, to compare working correlations, and QICu to compare mean models.
- **Small-sample corrections.** Mancl and DeRouen (2001) replace $y_i - \mu_i$ in $M$ by $(I - H_{ii})^{-1}(y_i - \mu_i)$, where $H_{ii}$ is the cluster block of a leverage matrix, which removes most of the downward bias of the sandwich with few clusters. Using $t$ quantiles with $G - p$ or $G - 1$ degrees of freedom also helps, as for [cluster-robust standard errors](/cluster-robust-standard-errors/).
- **Weighted equations for missing data.** Inverse probability weights inside $U$ handle responses missing at random (Robins, Rotnitzky and Zhao, 1995).
- **Estimating functions in general.** The equations are an [M-estimator](/m-estimator/) summed over clusters, and the sandwich is the general M-estimator covariance, which also covers [heteroscedasticity-consistent standard errors](/heteroscedasticity-consistent-standard-errors/) and exactly identified [generalized method of moments](/generalized-method-of-moments/). Line L6 is [Fisher scoring](/fisher-scoring/) for the quasi-score.

## Pitfalls

- **Few clusters.** The theory is for $G \to \infty$. With 30 clusters the sandwich intervals covered about 92% instead of 95% in the table above, and with fewer than about 20 clusters a correction is needed. The rank of $M$ is at most $G - 1$, so with $p \ge G$ the sandwich is singular.
- **Time-varying covariates.** A non-diagonal working correlation uses $x$ values from other times in the same cluster. If $E[y_{ij} \mid X_i] \ne E[y_{ij} \mid x_{ij}]$, for example when past responses affect future covariates, the estimate is biased; Pepe and Anderson (1994) recommend the independence working correlation in that case.
- **Missing data.** The unweighted equations need responses missing completely at random. Dropout that depends on observed earlier responses biases them.
- **No likelihood.** There is no likelihood ratio test and no AIC. Use Wald tests with the sandwich covariance, or score tests based on $U$, and QIC for model choice.
- **Marginal versus conditional effects.** With a nonlinear link, the coefficients are averages over the population of clusters. They are not the effect for a given cluster, and they are smaller in absolute value than those of a mixed model for the logit link.
- **An impossible working correlation.** The moment estimate of $\alpha$ can fall outside the range where $R(\alpha)$ is positive definite, for example below $-1/(m - 1)$ for an exchangeable $R$; the implementation clips it.

## Exercises

1. Show that with the independence working correlation the equations are the score equations of the generalized linear model, for any $\phi$.
   *Answer.* With $R = I$, $V_i = \phi S_i^2$ is diagonal and $D_i = \operatorname{diag}(d\mu_{ij}/d\eta)X_i$, so $D_i^\top V_i^{-1}(y_i - \mu_i) = \sum_jx_{ij}(d\mu_{ij}/d\eta)(y_{ij} - \mu_{ij})/(\phi V(\mu_{ij}))$. Summed over $i$ this is the GLM score divided by $\phi$, and $\phi$ does not change its root.
2. For the identity link, $V = 1$ and a fixed $\alpha$, show that the solution is $\hat b = (\sum_iX_i^\top R_i^{-1}X_i)^{-1}\sum_iX_i^\top R_i^{-1}y_i$.
   *Answer.* $D_i = X_i$ and $V_i = \phi R_i$, so $U(b) = \phi^{-1}\sum_iX_i^\top R_i^{-1}(y_i - X_ib)$, which is linear in $b$. Setting it to 0 gives the formula, which is generalized least squares with the block diagonal covariance $\operatorname{diag}(R_1, \dots, R_G)$.
3. For an exchangeable $R = (1 - \alpha)I + \alpha\mathbf 1\mathbf 1^\top$ of size $m$, show that $R^{-1} = \frac{1}{1 - \alpha}\big(I - \frac{\alpha}{1 + (m - 1)\alpha}\mathbf 1\mathbf 1^\top\big)$, and say for which $\alpha$ it exists.
   *Answer.* Multiply: $(1 - \alpha)I \cdot \frac{1}{1-\alpha}(I - c\mathbf 1\mathbf 1^\top) + \alpha\mathbf 1\mathbf 1^\top\frac{1}{1-\alpha}(I - c\mathbf 1\mathbf 1^\top) = I + \mathbf 1\mathbf 1^\top\big(-c + \frac{\alpha(1 - mc)}{1 - \alpha}\big)$, and with $c = \alpha/(1 + (m - 1)\alpha)$ the bracket is 0. $R$ has the eigenvalues $1 - \alpha$ and $1 + (m - 1)\alpha$, so it is positive definite for $-1/(m - 1) < \alpha < 1$.
4. Show that $M$ in line L8 has rank at most $G - 1$ at the solution.
   *Answer.* $M = \sum_iU_iU_i^\top$ with $U_i = D_i^\top V_i^{-1}(y_i - \mu_i)$, a sum of $G$ rank-one matrices. At the solution $\sum_iU_i = 0$, so the $U_i$ span a space of dimension at most $G - 1$.
5. In the random intercept example, why does the independence model-based interval undercover for $x_i$ but not for $w_{ij}$?
   *Answer.* The model-based variance treats the $4G = 120$ responses as independent. For a covariate that is constant within clusters, the information is about that of the 30 cluster means, each with variance $(1 + 1/4)$ instead of $2/4$ per response, so the true variance is about 2.5 times the model-based one when $\alpha = 0.5$. A covariate that varies inside clusters is compared within clusters, where the shared $a_i$ cancels, so the independence variance is not too small for it.

## References
