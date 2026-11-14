---
tag: X126D2
kind: algorithm
slug: cluster-robust-standard-errors
name: Cluster-robust standard errors
aliases:
- clustered standard errors
- Liang-Zeger standard errors
area: statistics-and-inference/regression-and-diagnostics
level: advanced
summary: A sandwich covariance that sums score contributions within clusters, so that inference stays valid when errors are correlated inside groups.
model: real-ram
complexity:
  vars: {n: the number of observations, p: "the number of columns of X, with p < n", G: the number of clusters}
  time: {worst: Θ(n p^2), best: Θ(n p^2)}
  space: {extra: Θ(n p)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1986
  people: [Kung-Yee Liang, Scott L. Zeger, Manuel Arellano, A. Colin Cameron, Jonah B. Gelbach, Douglas L. Miller]
  note: Liang and Zeger (1986) gave the cluster sandwich for estimating equations, Arellano (1987) for fixed effects panel regressions, and Cameron, Gelbach and Miller (2008) the wild cluster bootstrap for few clusters.
prereqs: [heteroscedasticity-consistent-standard-errors, ordinary-least-squares, qr-decomposition]
see_also: [generalized-estimating-equations, linear-mixed-model, generalized-least-squares, bootstrap-method, wald-test, difference-in-differences, m-estimator, standard-error]
sources:
  - paper: doi:10.1093/biomet/73.1.13
    title: "Kung-Yee Liang and Scott L. Zeger, Longitudinal data analysis using generalized linear models, Biometrika 73(1), 1986, pp. 13 to 22"
    locator: The whole paper (estimating equations for clustered data and the sandwich variance that sums score products within subjects)
  - paper: doi:10.1111/j.1468-0084.1987.mp49004006.x
    title: "Manuel Arellano, Computing robust standard errors for within-groups estimators, Oxford Bulletin of Economics and Statistics 49(4), 1987, pp. 431 to 434"
    locator: The whole paper (the cluster sandwich for the fixed effects panel regression, consistent as the number of units grows)
  - paper: doi:10.1162/rest.90.3.414
    title: "A. Colin Cameron, Jonah B. Gelbach and Douglas L. Miller, Bootstrap-based improvements for inference with clustered errors, The Review of Economics and Statistics 90(3), 2008, pp. 414 to 427"
    locator: The whole paper (over-rejection with 5 to 30 clusters, and the wild cluster bootstrap with the null imposed)
  - paper: doi:10.3368/jhr.50.2.317
    title: "A. Colin Cameron and Douglas L. Miller, A practitioner's guide to cluster-robust inference, Journal of Human Resources 50(2), 2015, pp. 317 to 372"
    locator: The whole paper (the CR1 factor, the choice of the cluster level, few clusters, and multiway clustering)
---

Cluster-robust standard errors, also called clustered or Liang-Zeger standard errors, keep the [ordinary least squares](/ordinary-least-squares/) fit and estimate its covariance when the observations fall into $G$ groups, such as pupils in schools or years of one firm, and the errors may be correlated in any way inside a group but are independent between groups. Each cluster contributes its total score $s_g = \sum_{i \in g}x_ie_i$, and the covariance estimate is the sandwich $(X^\top X)^{-1}\bigl(\sum_gs_gs_g^\top\bigr)(X^\top X)^{-1}$, usually times a small sample factor. With one observation per cluster it is the [heteroscedasticity-consistent](/heteroscedasticity-consistent-standard-errors/) estimate HC0. Its theory needs many clusters: the information about the variance comes from $G$ cluster totals, not from $n$ observations, so with few clusters the t intervals are too short and a wild cluster bootstrap is better.

## In plain words

When observations come in groups that share something, such as pupils in the same school, their errors tend to move together. The usual standard error treats every observation as new information, so it claims more certainty than the data give. This method first adds up, inside each group, how much the group pushes on the fitted line. It then measures how much these group totals vary. A group of a hundred similar pupils counts as roughly one piece of evidence about the noise, not a hundred. The method needs many groups to work well. With only a handful of groups it is still too optimistic.

## The problem

**Model.** $y = Xb + \varepsilon$ with $X$ a fixed real $n \times p$ matrix of rank $p < n$ (the intercept is one of the columns). The rows are split into $G$ clusters, with $X_g$, $y_g$ and $\varepsilon_g$ the rows of cluster $g$. The errors satisfy $\mathrm E[\varepsilon] = 0$, $\operatorname{Cov}(\varepsilon_g) = \Sigma_g$ of any form, and $\varepsilon_g$ is independent of $\varepsilon_h$ for $g \ne h$. Then

$$\operatorname{Cov}(\hat b) = (X^\top X)^{-1}\Bigl(\sum_gX_g^\top\Sigma_gX_g\Bigr)(X^\top X)^{-1}.$$

**Input.** $X$, $y$, a cluster label for each row, and the version.

**Output.** $\hat b$ and $\widehat V = a(X^\top X)^{-1}\bigl(\sum_gs_gs_g^\top\bigr)(X^\top X)^{-1}$ with $s_g = X_g^\top e_g$, where $a = 1$ for CR0 and

$$a = \frac{G}{G - 1}\cdot\frac{n - 1}{n - p}$$

for CR1, the default of most software. Intervals and tests use $t_{G-1}$, not $t_{n-p}$.

## The algorithm

```pseudo id=main
CLUSTER-COVARIANCE(X[1..n, 1..p], y[1..n], cluster[1..n], version)
L1  (R, c) ← Householder QR of X, applied to y      ▷ X = Q₁R, c = Qᵀy
L2  b̂ ← solve R b = c[1..p]
L3  eᵢ ← yᵢ - xᵢᵀ b̂ for all i
L4  for each cluster g:  s_g ← Σ_{i in g} xᵢ eᵢ;  u_g ← R⁻ᵀ s_g
L5  a ← 1 for CR0, or G/(G - 1) · (n - 1)/(n - p) for CR1
L6  V ← a · R⁻¹ (Σ_g u_g u_gᵀ) R⁻ᵀ
L7  seⱼ ← √Vⱼⱼ for j = 1..p
L8  return (b̂, V, se) with G - 1 degrees of freedom
```

Line L4 needs one pass over the rows and one triangular solve per cluster. Line L6 is the sandwich in factored form, because $R^{-1}R^{-\top} = (X^\top X)^{-1}$. A Wald test of $Cb = d$ with $q$ rows uses $(C\hat b - d)^\top(CVC^\top)^{-1}(C\hat b - d)/q$ against $F_{q, G-1}$, which needs $q \le G - 1$.

**Wild cluster bootstrap.** To test $b_j = \beta_0$ with few clusters: fit the model with $b_j = \beta_0$ imposed, keep its fitted values $\tilde y$ and residuals $\tilde e$, and compute the CR1 statistic $t = (\hat b_j - \beta_0)/\mathrm{se}_j$. For $B$ repetitions, draw an independent sign $v_g = \pm1$ for each cluster, set $y^* = \tilde y + v_g\tilde e$ on the rows of cluster $g$, refit, and compute $t^*$ in the same way. The p-value is $(1 + \#\{|t^*| \ge |t|\})/(1 + B)$. Because $X$ does not change, the QR of line L1 is computed once, and each repetition costs $\Theta(np)$.

## Example

Take $x = (1, 2, 3, 4, 5, 6)$, $y = (2, 3, 2, 4, 7, 8)$ with an intercept, and three clusters of two rows: $\{1, 2\}$, $\{3, 4\}$, $\{5, 6\}$. Exact arithmetic gives $\hat b = (-1/15, 44/35)$, and the residuals have the same sign inside each cluster: $(0.81, 0.55)$, $(-1.70, -0.96)$, $(0.78, 0.52)$. The cluster scores $s_g$ have intercept parts $143/105$, $-8/3$ and $137/105$, which add to 0, as do the slope parts $67/35$, $-941/105$ and $148/21$.

| method | se of slope |
|---|---|
| usual, $s^2(X^\top X)^{-1}$ | 0.2848 |
| HC1 | 0.2079 |
| CR0 | 0.2171 |
| CR1 | 0.2972 |

CR1 multiplies CR0's variance by $\frac{3}{2}\cdot\frac{5}{4} = 1.875$. With $G = 3$ the estimate rests on two degrees of freedom, so the interval uses $t_2$, whose 0.975 quantile is 4.30. The example only shows the steps; three clusters are far too few for the asymptotic theory.

**Measured coverage.** In each sample, cluster $g$ has $m = 10$ rows with $x_i = z_g + w_i$ and $y_i = 1 + x_i + a_g + \eta_i$, all of $z_g, w_i, a_g, \eta_i$ independent standard normal, so $x$ and the errors each have intraclass correlation 1/2. The nominal 95% intervals for the slope gave:

| setting | usual, $t_{n-2}$ | HC1, $t_{n-2}$ | CR1, normal | CR1, $t_{G-1}$ | wild cluster bootstrap |
|---|---|---|---|---|---|
| $G = 20$, $r = 1000$ | 0.707 | 0.691 | 0.897 | 0.920 | |
| $G = 6$, $r = 1000$ | 0.736 | 0.713 | 0.822 | 0.905 | |
| $G = 6$, $r = 200$, $B = 99$ | | | | | 0.950 |

For the bootstrap the entry is 1 minus the rejection rate of the 5% test of $b_1 = 1$. The seeds were 20261114, 20261115 and 20261116 for `random.Random`. Ignoring the clusters is badly wrong, and HC1 does not help, because the problem is correlation, not unequal variance. CR1 with $t_{G-1}$ is much better but still short; the bootstrap test held its size. These are measurements for one design, with a Monte Carlo standard error of about 0.007 for $r = 1000$ and 0.015 for $r = 200$.

## Correctness

The proof shows four exact facts. Lines L1 to L6 return exactly $a(X^\top X)^{-1}\bigl(\sum_gs_gs_g^\top\bigr)(X^\top X)^{-1}$. With one row per cluster CR0 is HC0 and CR1 is HC1. The cluster scores add to $X^\top e = 0$, so the middle matrix has rank at most $G - 1$; with one cluster the estimate is the zero matrix. In the wild cluster bootstrap with the null imposed, $|t^*|$ is the same for the signs $v$ and $-v$, so it has at most $2^{G-1}$ values. The proof also gives the exact expectation of the middle matrix, $\sum_gX_g^\top[(I - H)\Sigma(I - H)]_{gg}X_g$, which shows why CR0 is biased down.

The statistical property is cited, not proved: as $G \to \infty$, with independent clusters whose sizes do not dominate and with moment conditions, $G\widehat V$ is consistent for the limit of $G\operatorname{Cov}(\hat b)$ under any within-cluster correlation, and the t statistic is asymptotically normal (Liang and Zeger 1986, Arellano 1987). Using $t_{G-1}$ is a convention that works better in simulations. The bootstrap gives no exact size either.

## Complexity

The QR costs $\Theta(np^2)$, the residuals and the cluster scores $\Theta(np)$, the $G$ triangular solves $\Theta(Gp^2)$, and the sum and the sandwich $\Theta(Gp^2 + p^3)$. Since $G \le n$ and $p < n$, the total is $\Theta(np^2)$ time with $\Theta(np)$ extra space for the QR. Grouping the rows by cluster costs $\Theta(n)$ expected time with a hash table. Each wild bootstrap repetition costs $\Theta(np + Gp^2)$ because the QR is reused.

## Properties

- **Any within-cluster correlation.** No model for $\Sigma_g$ is used, so heteroscedasticity and correlation inside clusters are both covered.
- **Nesting.** If the clusters are merged into larger ones, the estimate stays valid but has fewer degrees of freedom. Clustering at a level that is too fine, for example by person when the treatment is assigned by school, misses correlation and gives intervals that are too short.
- **Rank.** The middle matrix has rank at most $\min(p, G - 1)$, so joint tests of more than $G - 1$ restrictions are impossible.
- **Sandwich form.** It is the general sandwich of an [M-estimator](/m-estimator/) with the scores summed by cluster first, and the same construction gives the variance of [generalized estimating equations](/generalized-estimating-equations/).
- **Equivariance.** Replacing $X$ by $XA$ for a nonsingular $A$ maps $\widehat V$ to $A^{-1}\widehat VA^{-\top}$. The labels of the clusters and the order of the rows do not matter.

## Variants and improvements

- **CR2 and CR3.** These replace $e_g$ by $(I - H_{gg})^{-1/2}e_g$ or $(I - H_{gg})^{-1}e_g$, the cluster forms of HC2 and HC3, and reduce the downward bias. With a degrees of freedom correction for the t reference, CR2 is the usual recommendation for few clusters.
- **Wild cluster bootstrap.** The version above, with the null imposed, gives tests close to the nominal size with as few as 6 clusters in many designs. With Rademacher signs and $G$ clusters there are only $2^{G-1}$ distinct values of $|t^*|$, so for $G < 10$ software often uses weights with six values.
- **Multiway clustering.** For errors correlated within firms and within years, add the one-way estimates for each dimension and subtract the estimate for their intersection. The result can fail to be positive semidefinite.
- **Fixed effects.** With cluster fixed effects, the scores of the transformed model are used, as in Arellano (1987); the degrees of freedom correction must not count the fixed effects as parameters when they are nested in the clusters.
- **Efficient alternatives.** If the correlation has a known form, such as a random intercept, [generalized least squares](/generalized-least-squares/) or a [linear mixed model](/linear-mixed-model/) is more efficient, and the cluster sandwich can still be used on top of it to protect against a wrong correlation model.

## When to use it

Use clustered standard errors whenever the observations come in groups that may share unobserved shocks and there are many groups, say 40 or more: panels of firms or people over time, surveys sampled by area, experiments randomized by school or village, and [difference-in-differences](/difference-in-differences/) designs with state-level policies. Cluster at the level at which the treatment is assigned or at which the shocks are shared. With fewer than about 40 clusters, or with clusters of very unequal size, use CR2 or the wild cluster bootstrap. If there is only one or two treated clusters, no version of the method gives reliable inference.

## Pitfalls

- **Few clusters.** The estimate is consistent only as $G$ grows. With $G$ below about 40, CR1 with normal critical values over-rejects, sometimes badly; use $t_{G-1}$ at least and preferably the wild cluster bootstrap.
- **Unequal cluster sizes.** A few large clusters dominate the sum and act like few clusters, even when $G$ is large.
- **Wrong level.** Clustering below the level of the shared shock leaves correlation between clusters and the standard errors too small. Clustering at a much coarser level than needed wastes degrees of freedom but is not invalid.
- **Not a fix for bias.** The method corrects the variance of OLS, not the estimate. Correlation with the regressors, for example a cluster effect correlated with $x$, still biases $\hat b$ and needs fixed effects or another design.
- **Version.** Packages differ in the factor $a$ and in the reference law; state both.

## Implementations

## History

The idea of summing score products within independent units goes back to the sandwich covariance of Huber (1967) and the heteroscedasticity-consistent estimate of White (1980). Liang and Zeger (1986) used it for longitudinal data in their generalized estimating equations, and Arellano (1987) gave it for within-groups estimators in econometric panels; the two forms are the same computation. Cameron, Gelbach and Miller (2008) showed the over-rejection with few clusters and proposed the wild cluster bootstrap, and Cameron and Miller (2015) wrote the standard practical guide.

## References
