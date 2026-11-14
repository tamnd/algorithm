---
tag: 6YVPGK
kind: algorithm
slug: restricted-maximum-likelihood
name: Restricted maximum likelihood
aliases:
- REML
- residual maximum likelihood
area: statistics-and-inference/regression-and-diagnostics
level: advanced
summary: Estimates variance components by maximizing the likelihood of error contrasts that do not depend on the fixed effects. It removes the downward bias of ML variance estimates.
model: real-ram
complexity:
  vars: {n: the number of observations, p: the number of fixed-effect columns, k: the number of variance components, t: the number of likelihood evaluations}
  time: {worst: "Θ(t k n^3)", best: "Θ(k n^3)"}
  space: {extra: "Θ(k n^2)"}
  flops: {worst: "t ((2 k + 7/3) n^3 + 2 (k^2 + p^2) n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1971
  people: [H. D. Patterson, Robin Thompson]
  note: "Patterson and Thompson maximized the likelihood of the error contrasts to recover inter-block information in designs with unequal block sizes, which extended the balanced case of W. A. Thompson (1962) to any linear mixed model."
prereqs: [linear-mixed-model, generalized-least-squares, fisher-scoring, estimator-bias, kkt-conditions]
see_also: [henderson-mixed-model-equations, marginal-likelihood, sample-variance, one-way-anova, likelihood-ratio-test, expectation-maximization, projected-gradient-descent, laplace-approximation]
sources:
  - paper: doi:10.1093/biomet/58.3.545
    title: "H. D. Patterson and R. Thompson, Recovery of inter-block information when block sizes are unequal, Biometrika 58(3), 1971, pp. 545 to 554"
    locator: The whole paper (the likelihood of the error contrasts, its score equations and their iterative solution)
  - paper: doi:10.1214/aoms/1177704731
    title: "W. A. Thompson, The problem of negative estimates of variance components, Annals of Mathematical Statistics 33(1), 1962, pp. 273 to 289"
    locator: The restricted likelihood for balanced designs and the estimates that replace a negative value by 0
  - paper: doi:10.1093/biomet/61.2.383
    title: "David A. Harville, Bayesian inference for variance components using only error contrasts, Biometrika 61(2), 1974, pp. 383 to 385"
    locator: The whole paper (the restricted likelihood in determinant form and as the marginal likelihood with a flat prior on the fixed effects)
  - paper: doi:10.1080/01621459.1977.10480998
    title: "David A. Harville, Maximum likelihood approaches to variance component estimation and to related problems, Journal of the American Statistical Association 72(358), 1977, pp. 320 to 338"
    locator: The whole paper (ML and REML compared, their score equations, and Newton, scoring and EM algorithms)
  - paper: doi:10.2307/2529876
    title: "Nan M. Laird and James H. Ware, Random-effects models for longitudinal data, Biometrics 38(4), 1982, pp. 963 to 974"
    locator: The EM algorithm for ML and REML estimates in the two-stage model
  - paper: doi:10.1080/01621459.1988.10478693
    title: "Mary J. Lindstrom and Douglas M. Bates, Newton-Raphson and EM algorithms for linear mixed-effects models for repeated-measures data, Journal of the American Statistical Association 83(404), 1988, pp. 1014 to 1022"
    locator: The whole paper (Newton-Raphson on the profiled ML and REML likelihoods compared with EM)
  - paper: doi:10.2307/2533274
    title: "Arthur R. Gilmour, Robin Thompson and Brian R. Cullis, Average information REML: an efficient algorithm for variance parameter estimation in linear mixed models, Biometrics 51(4), 1995, pp. 1440 to 1450"
    locator: The whole paper (the average of the observed and expected information and its computation from the mixed model equations)
  - paper: doi:10.18637/jss.v067.i01
    title: "Douglas Bates, Martin Mächler, Ben Bolker and Steve Walker, Fitting linear mixed-effects models using lme4, Journal of Statistical Software 67(1), 2015, pp. 1 to 48"
    locator: Sections 3 and 4 (the profiled REML criterion from a sparse Cholesky factor and its optimization with bounds that allow a variance of 0)
  - paper: doi:10.1080/01621459.1987.10478472
    title: "Steven G. Self and Kung-Yee Liang, Asymptotic properties of maximum likelihood estimators and likelihood ratio tests under nonstandard conditions, Journal of the American Statistical Association 82(398), 1987, pp. 605 to 610"
    locator: The mixture of chi-squared laws when the true parameter is on the boundary
  - paper: doi:10.1111/j.1467-9868.2004.00438.x
    title: "Ciprian M. Crainiceanu and David Ruppert, Likelihood ratio tests in linear mixed models with one variance component, Journal of the Royal Statistical Society Series B 66(1), 2004, pp. 165 to 185"
    locator: The whole paper (the exact null law of the restricted likelihood ratio and its mass at 0)
  - paper: doi:10.2307/2533558
    title: "Michael G. Kenward and James H. Roger, Small sample inference for fixed effects from restricted maximum likelihood, Biometrics 53(3), 1997, pp. 983 to 997"
    locator: The whole paper (the covariance of the fixed effects after REML and the F approximation)
  - book: isbn:9780471621621
    title: Shayle R. Searle, George Casella and Charles E. McCulloch, Variance Components, Wiley, 1992
    locator: Chapter 6 (ML and REML) and Chapter 8 (computing ML and REML estimates)
---

Restricted maximum likelihood (REML), also called residual maximum likelihood, estimates the covariance parameters $\theta$ of a [linear mixed model](/linear-mixed-model/) $y \sim N(Xb, V(\theta))$ by maximizing the likelihood of $n - p$ error contrasts $K^\top y$ with $K^\top X = 0$. On this page $b$ is the vector of fixed-effect coefficients. The contrasts have mean 0 whatever $b$ is, so their likelihood depends on $\theta$ only. Plain maximum likelihood estimates $b$ and $\theta$ together and does not allow for the degrees of freedom that the estimate of $b$ uses, so its variance estimates are too small; REML makes that allowance, and for a single normal sample it gives the sample variance with divisor $n - 1$. After $\hat\theta$ is found, $b$ is estimated by [generalized least squares](/generalized-least-squares/) at $V(\hat\theta)$. REML is the default method for variance components in mixed model software. The algorithm on this page maximizes the restricted likelihood by Fisher scoring, keeps every variance component at 0 or above, and reports which components end at 0.

## In plain words

Pupils sit in classes, and you want to know two things: how much the classes differ, and how much pupils in one class differ. Plain maximum likelihood fits the averages first and then measures the spread around the fitted averages. The fitted averages follow the data a little too closely, so the measured spread comes out too small. REML first removes everything the averages can explain. It keeps only what is left over, which carries no information about the averages, and asks which spreads make those leftovers most likely. For one sample this gives the usual sample variance that divides by one less than the sample size. The search moves uphill one step at a time. If the best value for the spread between classes would be negative, the method holds it at zero and says so.

## The problem

**Input.** A response $y \in \mathbb R^n$; a fixed-effects design $X$ ($n \times p$) of rank $p < n$; symmetric positive semidefinite matrices $V_1, \dots, V_k$ ($n \times n$) with $V_k = I$, so that $V(\theta) = \theta_1V_1 + \dots + \theta_kV_k$. For the one-way layout, $V_1 = ZZ^\top$ and $\theta = (\sigma_u^2, \sigma_e^2)$. The parameter space is $\theta_1, \dots, \theta_{k-1} \ge 0$ and $\theta_k > 0$.

**Output.** A maximizer $\hat\theta$ of the restricted log-likelihood over the parameter space, the GLS estimate $\hat b$ at $\hat\theta$, the maximum value, the set of components with $\hat\theta_j = 0$ and the score there.

**The criterion.** With $A = X^\top V^{-1}X$ and $P = V^{-1} - V^{-1}XA^{-1}X^\top V^{-1}$,

$$\ell_R(\theta) = -\tfrac12\bigl[(n - p)\log 2\pi + \log|V| + \log|A| - \log|X^\top X| + y^\top Py\bigr].$$

This is the log density of $w = K^\top y$ for any $n \times (n - p)$ matrix $K$ with $K^\top X = 0$ and $K^\top K = I$. The ML criterion is $\ell(\theta) = -\frac12[n\log 2\pi + \log|V| + y^\top Py]$, with $b$ already replaced by $\hat b$; the difference is the term $\log|A| - \log|X^\top X|$ and $n - p$ in place of $n$. The score and the expected information of $\ell_R$ are

$$s_j = -\tfrac12\operatorname{tr}(PV_j) + \tfrac12 y^\top PV_jPy, \qquad I_{jl} = \tfrac12\operatorname{tr}(PV_jPV_l).$$

For ML, $V^{-1}$ replaces $P$ in both trace terms.

## The algorithm

```pseudo id=main
REML-FISHER-SCORING(y[1..n], X[1..n, 1..p], V_1, ..., V_k, θ⁰, tol, max_iter)
L1  θ ← θ⁰, each entry raised to a small positive floor
L2  (ℓ, s, I) ← restricted log-likelihood, score and information at θ
L3  for it ← 1 to max_iter
L4      F ← {1, ..., k}                                          ▷ the free components
L5      δ_F ← solution of I[F, F] δ_F = s_F;  δ_j ← 0 for j ∉ F
L6      if some j ∈ F has θ_j = 0 and δ_j < 0 then remove those j from F and go to L5
L7      λ ← 1
L8      θ' ← max(θ + λδ, 0) entry by entry;  θ'_k ← max(θ'_k, floor)
L9      (ℓ', s', I') ← the same quantities at θ';  if ℓ' ≥ ℓ then go to L11
L10     λ ← λ/2;  if λ < 10⁻⁸ then θ' ← θ (no move) else go to L8
L11     record the change max_j |θ'_j - θ_j|;  (θ, ℓ, s, I) ← (θ', ℓ', s', I')
L12     if the change ≤ tol (1 + max_j θ_j) then leave the loop
L13 return θ, b̂ = A⁻¹X^⊤V⁻¹y at θ, ℓ, the set {j : θ_j = 0} and s
```

Line L5 is a Fisher scoring step, the Newton step with the expected information in place of the Hessian. Lines L4 to L6 are an active set: a component already at 0 whose step points below 0 is held at 0, and the step for the other components is solved again without it. Line L8 projects the step onto the parameter space, and lines L9 and L10 halve the step until the restricted likelihood does not decrease. The floor in line L8 keeps the residual variance positive, so $V$ stays positive definite. Each evaluation in lines L2 and L9 forms $V$, its Cholesky factor, $A$, $P$ and the products $PV_j$.

**Boundary behavior.** A variance component of 0 is a boundary point, and the algorithm can stop there. Line L8 puts a component that would go negative at exactly 0, and line L6 keeps it there while the step still points out of the parameter space. At a maximum on the boundary the score of that component is at most 0, which is the [Karush-Kuhn-Tucker condition](/kkt-conditions/) for the bound $\theta_j \ge 0$; at a maximum inside, the score is 0. Line L13 returns the score and the set of components at 0, so that the caller can check this condition and knows that the usual standard errors and the usual $\chi^2$ tests do not apply to those components.

## Example

Three data sets in the one-way layout $y_{ij} = b_0 + u_i + e_{ij}$, each with an intercept and $\theta = (\sigma_u^2, \sigma_e^2)$. Balanced: $y = (10, 12, 14;\ 15, 16, 17;\ 18, 20, 22)$. Unbalanced: $y = (10, 12, 14;\ 15, 17;\ 18, 20, 22, 24)$. Near-null: $y = (10, 14, 12;\ 11, 13, 15;\ 12, 10, 14)$. The start is the sample variance divided by 2 for each component, and $\mathrm{tol} = 10^{-10}$.

| data | method | $\hat\sigma_u^2$ | $\hat\sigma_e^2$ | $\hat b_0$ | $\hat\ell$ | iterations |
|---|---|---|---|---|---|---|
| balanced | REML | 15 | 3 | 16 | $-18.5185$ | 2 |
| balanced | ML | $29/3 = 9.6667$ | 3 | 16 | $-21.2649$ | 2 |
| unbalanced | REML | 19.2418 | 4.9723 | 16.3693 | $-20.2490$ | 9 |
| unbalanced | ML | 12.4571 | 4.9413 | 16.3867 | $-23.1356$ | 10 |
| near-null | REML | 0 | 3.25 | 12.3333 | $-16.0661$ | 3 |
| near-null | ML | 0 | 2.8889 | 12.3333 | $-17.5444$ | 3 |

In the balanced data the group means are 12, 16 and 20, so $\mathrm{MSA} = 48$ and $\mathrm{MSE} = 3$. REML gives $\hat\sigma_e^2 = \mathrm{MSE}$ and $\hat\sigma_u^2 = (\mathrm{MSA} - \mathrm{MSE})/3 = 15$, the unbiased ANOVA estimates. ML gives $\hat\sigma_u^2 = (\mathrm{SSA}/3 - \mathrm{MSE})/3 = 29/3$, smaller because it divides the sum of squares between groups by 3 groups instead of 2 degrees of freedom. In the unbalanced data there is no closed form, and REML again gives a larger $\hat\sigma_u^2$ than ML.

In the near-null data the group means are 12, 13 and 12, so $\mathrm{MSA} = 1 < \mathrm{MSE} = 4$ and the ANOVA estimate of $\sigma_u^2$ is $-1$. REML stops at $\hat\sigma_u^2 = 0$ with $\hat\sigma_e^2 = \mathrm{SST}/8 = 26/8$, the pooled variance of all 9 values. The returned score for $\sigma_u^2$ is $-0.639$ (ML: $-1.198$), which is at most 0, so the KKT condition holds and the point is the maximum on the boundary.

A test of $\sigma_u^2 = 0$ in the balanced data compares the REML fit with the REML fit without the random effect, which has $\hat\sigma_e^2 = 14.25$ and $\hat\ell = -21.9785$. Both models have the same $X$, so their restricted likelihoods are comparable. The statistic is $2(-18.5185 + 21.9785) = 6.920$. The null value is on the boundary, so the reference law for many groups is $\frac12\chi^2_0 + \frac12\chi^2_1$ (Chernoff 1954; Self and Liang 1987), and the p-value is $\frac12P(\chi^2_1 \ge 6.920) = 0.0043$ instead of the $\chi^2_1$ value 0.0085. With only 3 groups this large-sample law is itself rough; the [linear mixed model](/linear-mixed-model/) page gives the exact mass at 0 for the balanced layout.

## Correctness

The proof in this folder shows these facts exactly. First, for every $K$ of rank $n - p$ with $K^\top X = 0$, $K(K^\top VK)^{-1}K^\top = P$ and $|K^\top VK| = |K^\top K|\,|V|\,|A|/|X^\top X|$, so the log density of $K^\top y$ is $\ell_R(\theta) - \frac12\log|K^\top K|$; the criterion depends on $X$ only through its column space and not on $b$. Second, the score and the expected information have the forms above. Third, with $V = \sigma^2I$ the REML estimate is $\mathrm{RSS}/(n - p)$, which is unbiased, and the ML estimate is $\mathrm{RSS}/n$; for one normal sample ($X = \mathbf 1$) the REML estimate is the sample variance with divisor $n - 1$. Fourth, in the balanced one-way layout REML gives the ANOVA estimates when $\mathrm{MSA} \ge \mathrm{MSE}$ and $(0, \mathrm{SST}/(N - 1))$ otherwise, and the score of $\sigma_u^2$ at that boundary point is at most 0. Fifth, the loops stop after at most $\mathrm{max\_iter}$ outer passes, every iterate is in the parameter space, and the restricted likelihood does not decrease from one iterate to the next.

What is proved is the criterion, its derivatives, the closed forms in the two special cases and the termination. Convergence of Fisher scoring to the global maximum is not proved: $\ell_R$ need not be concave in $\theta$, and the active set rule of line L6 does not by itself guarantee the sign of the score of a component held at 0. These are measured: the tests check the closed forms against the iterative output on random balanced data, including data that end on the boundary, and check the score against a numerical derivative.

## Complexity

One evaluation in this dense implementation costs a Cholesky factor and an inverse of $V$ ($\frac73n^3$ flops), the $k$ products $PV_j$ ($2kn^3$) and the $k^2$ traces of the information ($2k^2n^2$), plus $O(p^2n^2)$ for $P$. With $t$ evaluations the time is $\Theta(tkn^3)$ and the extra space $\Theta(kn^2)$ for the products. The number of outer iterations is not bounded by a formula; it was 2 to 10 in the example, and each outer iteration with no halving costs one evaluation. Production programs never form $V$: they work with Henderson's equations of order $p + q$ or a sparse Cholesky factor, so that one evaluation costs about as much as one factorization of the mixed model coefficient matrix.

## Properties

- **Reparametrization.** Centering covariates, rescaling them or changing the coding of a factor does not change the column space of $X$, so it does not change the REML estimates.
- **Not exactly unbiased in general.** The unbiased closed forms hold only in special cases such as the [sample variance](/sample-variance/). Elsewhere the equations are nonlinear, and the truncation at 0 moves the mean of $\hat\sigma_u^2$ up, as the simulation below shows.
- **Bayesian view.** Integrating the normal likelihood over $b$ with a flat prior gives $\exp\ell_R$ up to a constant (Harville 1974), so REML maximizes a [marginal likelihood](/marginal-likelihood/) for $\theta$.
- **Boundary rates.** In the balanced one-way layout with $a$ groups of size $m$, the ML estimate of $\sigma_u^2$ is 0 exactly when $(a - 1)\mathrm{MSA}/a \le \mathrm{MSE}$, more often than REML. With $a = 5$, $m = 4$ and $\sigma_u^2 = \sigma_e^2$ the exact probabilities of an estimate of 0 are $P(F_{4,15} \le 1/5) = 0.0656$ for REML and $P(F_{4,15} \le 1/4) = 0.0948$ for ML.
- **Measured bias.** In 2000 simulated balanced data sets with $a = 5$, $m = 4$ and $\sigma_u^2 = \sigma_e^2 = 1$ (seed 20261114, using the closed forms proved here), the mean of $\hat\sigma_u^2$ was 1.025 for REML, 0.775 for ML and 1.018 for the ANOVA estimate, which can be negative; the mean of $\hat\sigma_e^2$ was 0.996 for REML and 0.991 for ML. The estimate was 0 in 6.95% of the REML fits and 9.5% of the ML fits.

## Variants and improvements

- **Newton-Raphson.** The observed information in line L5 converges faster near the maximum but can fail to be positive definite far from it (Lindstrom and Bates 1988).
- **EM.** Treating $u$ as missing data gives an EM algorithm for ML and REML (Laird and Ware 1982; see [expectation-maximization](/expectation-maximization/)). Each step is cheap and keeps the variances positive, but convergence is slow, most when a variance is near 0, and an estimate of exactly 0 is reached only in the limit.
- **Average information.** Gilmour, Thompson and Cullis (1995) use the average of the observed and expected information, which needs only quadratic forms in $Py$ and is cheap to compute from the mixed model equations. This is the standard algorithm in animal breeding programs.
- **Through the mixed model equations.** The traces need not use $V$. For $G = \sigma_u^2I_q$, $\operatorname{tr}(Z^\top PZ) = q/\sigma_u^2 - \operatorname{tr}(C^{22})/\sigma_u^4$, where $C^{22}$ is the lower block of the inverse of the coefficient matrix of [Henderson's mixed model equations](/henderson-mixed-model-equations/).
- **Profiled criterion with bounds.** lme4 (Bates et al. 2015) writes the random effects through a relative covariance factor, profiles out $b$ and the residual variance, and minimizes the REML criterion over the factor with a derivative-free optimizer and lower bounds of 0, so a component at 0 is an ordinary bound.

## When to use it

Use REML to estimate variance and covariance parameters in a linear mixed model, most of all when the number of groups is small or $p$ is not small compared with $n$, where the ML bias is largest. Use the REML fit for the standard errors of $\hat b$ and for comparing covariance structures with the same fixed effects. Use ML when the fixed effects differ between the models compared: REML likelihoods with different fixed effects cannot be compared (use ML for those LR tests). For generalized linear mixed models the likelihood has no closed form; a [Laplace approximation](/laplace-approximation/) or numerical integration replaces it.

## Pitfalls

- **Comparing different fixed effects.** Two models with different $X$ have different error contrasts, so their restricted likelihoods are densities of different data, and their difference, or an AIC computed from it, means nothing.
- **Testing a variance component.** The [likelihood ratio test](/likelihood-ratio-test/) of $\sigma_u^2 = 0$ does not have the $\chi^2_1$ law of [Wilks' theorem](/wilks-theorem/) because the null value is on the boundary; use $\frac12\chi^2_0 + \frac12\chi^2_1$ for one component, check it by a parametric bootstrap when there are few groups (Crainiceanu and Ruppert 2004), and do not use a Wald test with the inverse information.
- **Estimates at 0.** A component at 0 is a valid maximum, not a failure, but the inverse information gives no standard error for it. Removing the component or keeping it at 0 gives the same fit of $b$.
- **Local maxima and slow convergence.** With many components or a weakly identified structure, scoring can stop at a local maximum or take many halvings; try several starts and compare $\hat\ell$.
- **Plug-in standard errors.** $(X^\top V(\hat\theta)^{-1}X)^{-1}$ ignores the error in $\hat\theta$; use the Kenward and Roger (1997) adjustment for small samples.
- **Floating point.** Forming $V$ and $P$ for large $n$ is slow and can lose accuracy when the components differ much in size; the methods that use the mixed model equations or a profiled Cholesky factor avoid this.

## Implementations

## History

W. A. Thompson (1962) maximized the likelihood of the part of the data that is free of the fixed effects in balanced designs, and set negative estimates to 0. Patterson and Thompson (1971) gave the method for any design with unequal block sizes, with its score equations and an iterative solution. Harville (1974) wrote the restricted likelihood in the determinant form used on this page and showed that it is a marginal likelihood with a flat prior on the fixed effects, and Harville (1977) reviewed ML and REML and their algorithms. EM for REML came with Laird and Ware (1982), Newton-Raphson with Lindstrom and Bates (1988), and the average information algorithm with Gilmour, Thompson and Cullis (1995). The lme4 package (Bates et al. 2015) made the profiled REML criterion with sparse Cholesky factors the common route in general software.

## References
