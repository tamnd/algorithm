---
tag: MBJNZK
kind: algorithm
slug: mm-estimator
name: MM-estimator
aliases:
- Yohai MM-estimator
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: Yohai's regression estimator that starts from a high-breakdown S-estimate of scale and then solves an efficient M-estimation step. It has both high breakdown and high efficiency.
model: real-ram
complexity:
  vars: {n: the number of observations, p: the number of coefficients, m: the number of random subsets, t: the number of reweighting steps}
  time: {worst: O(m (p³ + n p) + t n p²), average: O(m (p³ + n p) + t n p²), best: O(m (p³ + n p) + n p²)}
  space: {extra: O(n + p²)}
properties: {deterministic: false, randomized: true, exact_in_exact_arithmetic: false, in_place: false, online: false}
history:
  year: 1987
  people: [Víctor J. Yohai]
  note: Yohai defined the MM-estimator in 1987 and proved that it has breakdown point one half and any chosen efficiency at the normal. It builds on the S-estimators of Rousseeuw and Yohai (1984).
prereqs: [tukey-biweight, huber-m-estimator, breakdown-point, m-estimator, ordinary-least-squares]
see_also: [least-median-of-squares, least-trimmed-squares, iteratively-reweighted-least-squares, minimum-covariance-determinant, ransac, robust-model-fitting, leverage-statistics, cooks-distance]
sources:
  - paper: doi:10.1214/aos/1176350366
    title: Víctor J. Yohai, High breakdown-point and high efficiency robust estimates for regression, The Annals of Statistics 15(2), 1987
    locator: pp. 642 to 656 (the MM-estimator, its breakdown point and its efficiency at the normal)
  - paper: doi:10.1007/978-1-4615-7821-5_15
    title: Peter J. Rousseeuw and Víctor J. Yohai, Robust regression by means of S-estimators, in Robust and Nonlinear Time Series Analysis, Lecture Notes in Statistics 26, Springer, 1984
    locator: pp. 256 to 272 (S-estimators of regression, the M-scale and their breakdown point)
  - paper: doi:10.1198/106186006X113629
    title: Matías Salibián-Barrera and Víctor J. Yohai, A fast algorithm for S-regression estimates, Journal of Computational and Graphical Statistics 15(2), 2006
    locator: pp. 414 to 427 (random subsets with local improvement steps for the S-estimate)
  - book: isbn:9781119214687
    title: Ricardo A. Maronna, R. Douglas Martin, Victor J. Yohai and Matías Salibián-Barrera, Robust Statistics, Theory and Methods (with R), second edition, Wiley, 2019
    locator: Chapter 5 (S-estimators, MM-estimators, the choice of the constants and the computation by subsampling)
  - book: isbn:9780471852339
    title: Peter J. Rousseeuw and Annick M. Leroy, Robust Regression and Outlier Detection, Wiley, 1987
    locator: Chapter 3 (high-breakdown regression and the subsampling algorithm)
---

The MM-estimator of linear regression runs in two stages. First, an S-estimate gives a fit $\hat\beta_0$ and a robust scale $\hat s$ of its residuals, with breakdown point one half. Second, with $\hat s$ fixed, a [Tukey biweight](/tukey-biweight/) M-estimate is computed by reweighted least squares, starting from $\hat\beta_0$. The second stage raises the efficiency at the normal to a chosen level, usually 95%. Yohai (1987) proved that it keeps the breakdown point of the first stage. The S-estimate is a hard nonconvex problem, so in practice it is approximated by fits through random subsets of $p$ points.

## In plain words

Fitting a line by least squares fails when a few points are far off, in particular points with unusual $x$ values. The MM method first finds a rough line that most points agree with. It tries many lines, each through a few randomly chosen points, and keeps the line whose residuals are the smallest in a robust sense. This also gives a robust size of a typical residual. Then it improves the line: points with small residuals count fully, points with larger residuals count less, and points with very large residuals do not count. The improved line is nearly as precise as least squares when the data are clean.

## The problem

The input is a design matrix $X$ with rows $x_i \in \mathbb R^p$ (with a column of ones for an intercept) and responses $y_1, \ldots, y_n$, with $n \ge 2p$. Let $\rho_c(u) = 1 - (1 - (u/c)^2)^3$ for $|u| \le c$ and $\rho_c(u) = 1$ beyond: the biweight loss scaled to a maximum of 1. Write $r_i(\beta) = y_i - x_i^{\mathsf T}\beta$.

- The **M-scale** $s(r)$ of residuals $r_1, \ldots, r_n$ is the solution $s > 0$ of $\frac1n\sum_i \rho_{c_0}(r_i/s) = b$. With $c_0 = 1.54764$ and $b = 1/2$, it is consistent for $\sigma$ at the normal and has breakdown point one half.
- The **S-estimate** is $\hat\beta_0 = \arg\min_\beta s(r(\beta))$, and $\hat s = s(r(\hat\beta_0))$.
- The **MM-estimate** is a local minimizer of $\sum_i \rho_{c_1}(r_i(\beta)/\hat s)$ with $c_1 = 4.685$, reached from $\hat\beta_0$, with $\hat s$ fixed.

## The algorithm

```pseudo id=main
MM(X, y, m)                                    ▷ c0 = 1.54764, b = 1/2, c1 = 4.685
L1  for j ← 1 to m do
L2      J ← a random set of p rows; if X_J is singular then skip; β ← the solution of X_J β = y_J
L3      s ← M-SCALE(y − Xβ)
L4      if s is the least scale so far then (β0, s0) ← (β, s)
L5  β ← β0; ŝ ← s0; if ŝ = 0 then return (β, ŝ)
L6  repeat
L7      r_i ← y_i − x_iᵀβ for each i
L8      w_i ← (1 − (r_i/(c1 ŝ))²)² if |r_i| < c1 ŝ, else 0
L9      β' ← the weighted least squares fit with weights w_i
L10     if ‖β' − β‖ ≤ tol then return (β', ŝ)
L11     β ← β'

M-SCALE(r)
L12 if at most n b residuals are nonzero then return 0
L13 lo ← min_{r_i ≠ 0} |r_i| / c0; hi ← a value with h(hi) ≤ b, where h(s) = (1/n) Σ ρ_{c0}(r_i/s)
L14 bisect: if h(mid) > b then lo ← mid else hi ← mid; return hi when the bracket is as small as the precision
```

$h$ is continuous and nonincreasing in $s$. At $lo$ every nonzero term is 1, so $h(lo) > b$. Since $\rho_{c_0}(u) \le 3u^2/c_0^2$, any $hi \ge \sqrt{3\,\overline{r^2}/b}/c_0$ has $h(hi) \le b$.

## Example

Take $x = 1, \ldots, 10$, an intercept, and $y = (3.1, 4.8, 7.2, 9.1, 10.8, 13.2, 15.0, 16.9, 2.0, 1.0)$. The first eight points lie near $y = 1 + 2x$. The last two are bad leverage points.

- **Least squares** gives $7.307 + 0.182x$. The two bad points turn the slope almost flat.
- **S-stage**, with all 45 pairs as the subsets: the least M-scale, $\hat s = 0.2162$, comes from the line through $(4, 9.1)$ and $(7, 15.0)$, that is $\hat\beta_0 = (37/30, 59/30) \approx (1.233, 1.967)$. Its residuals are $(-0.10, -0.37, 0.07, 0, -0.27, 0.17, 0, -0.07, -16.93, -19.90)$. The terms $\rho_{c_0}(r_i/\hat s)$ are $(0.245, 1, 0.114, 0, 0.951, 0.575, 0, 0.114, 1, 1)$, and their mean is $1/2$, as the scale equation requires.
- **M-stage**, with $c_1\hat s = 1.013$:

| step | $\beta$ | $\sum \rho_{c_1}(r_i/\hat s)$ |
|---|---|---|
| 0 | (1.2333, 1.9667) | 2.67162 |
| 1 | (1.0758, 1.9881) | 2.52365 |
| 2 | (1.0604, 1.9901) | 2.52205 |
| 3 | (1.0589, 1.9902) | 2.52204 |

The iteration stops at $\hat\beta = (1.0587, 1.9902)$ after 10 steps. The two bad points have weight 0, and the eight good points have weights between 0.89 and 1. The objective never rises. Each bad point adds exactly 1 to it.

## Correctness

The statistical properties are cited, not proved here. The page proves that the computation does what the pseudocode claims; `proofs/correctness.md` has the details.

- **M-SCALE.** $h$ is continuous and nonincreasing. If more than $nb$ residuals are nonzero, $h$ is strictly decreasing near any root, so the root is unique, and the bisection keeps it in $[lo, hi]$.
- **S-stage.** Lines L1 to L4 return the subset fit with the least M-scale among those tried. This is the S-estimate only if the best fit is among the subset fits. In general it is an approximation.
- **M-stage.** $\rho_{c_1}(u) = g(u^2)$ with $g$ concave, as on the [Tukey biweight](/tukey-biweight/) page. So the objective lies below a weighted sum of squares that touches it at the current $\beta$, and line L9 minimizes that sum. Hence the objective does not increase. Since $c_1 > c_0$, $\rho_{c_1} \le \rho_{c_0}$, so the objective at the start is at most $nb = n/2$. Each point with zero weight adds 1, so at most $n/2$ points have zero weight at every step. If every $p$ rows of $X$ are linearly independent and $n \ge 2p$, the weighted least squares problem in line L9 has a unique solution.

## Complexity

- **S-stage.** Each subset costs $O(p^3)$ for the $p \times p$ solve and $O(np)$ for the residuals. M-SCALE costs $O(n)$ for each bisection step, and a fixed number of steps reaches the floating-point precision. So the stage costs $O(m(p^3 + np))$.
- **Number of subsets.** If a fraction $\varepsilon$ of the points are outliers, a random $p$-subset is clean with probability $(1 - \varepsilon)^p$. So $m \ge \log\delta / \log(1 - (1 - \varepsilon)^p)$ subsets give a clean one with probability $1 - \delta$. For $p = 2$, $\varepsilon = 0.3$ and $\delta = 0.01$ this is $m = 7$; for $p = 10$ and $\varepsilon = 0.5$ it is $m = 4714$ (the bound is $4713.4$). The count grows exponentially in $p$.
- **M-stage.** Each step costs $O(np^2)$ to form the weighted normal equations and $O(p^3)$ to solve them. The convergence is linear.
- **Space.** $O(n + p^2)$.

## Properties

Proved on this page: the descent and the well-defined steps of the computation. Cited: the statistical properties below. Measured: the numbers in the tests.

- **Breakdown point one half (cited).** If the S-estimate uses $b = \tfrac12\max\rho$ and $\rho_{c_1} \le \rho_{c_0}$, the MM-estimate has asymptotic breakdown point $\tfrac12$ (Yohai 1987). It holds for outliers in $y$ and for bad leverage points in $x$. The S-estimate alone has this breakdown point (Rousseeuw and Yohai 1984).
- **Efficiency (cited).** Under normal errors the MM-estimate has the same asymptotic distribution as the M-estimate with the true $\sigma$, so $c_1 = 4.685$ gives 95% efficiency relative to least squares (Yohai 1987). The S-estimate with $c_0 = 1.54764$ alone has an efficiency of only about 29% (Maronna et al. 2019).
- **Measured.** In the tests, on 60 points with 30% bad leverage points the least squares slope is off by more than 1, and the MM slope is within 0.15 of the truth. On 40 clean replications of 40 points the variance ratio of the slopes, least squares over MM, is 0.94.
- **Equivariance.** The MM-estimate is regression, scale and affine equivariant, when the subsets are chosen independently of the values.
- **Exact fit.** If more than half of the points lie exactly on a hyperplane, the M-scale of that fit is 0, and the algorithm returns that fit when a subset from those points is drawn.

## Variants and improvements

- **Fast-S.** Improve each subset fit by a few local steps for the S-objective, keep the best few, and refine them fully (Salibián-Barrera and Yohai 2006). This needs far fewer subsets than the plain search.
- **Deterministic starts.** Use the [least trimmed squares](/least-trimmed-squares/) or the [least median of squares](/least-median-of-squares/) fit as the start instead of random subsets.
- **Other losses.** Optimal $\rho$ functions, or a Huber loss in the M-stage. A monotone $\psi$ gives a unique M-stage solution, but leverage points then have more influence.
- **Inference.** Use the sandwich covariance of the M-stage with $\hat s$ fixed. Robust tests and robust model selection build on it.
- **Robust multivariate methods.** For location and scatter, the analogous two-stage idea starts from the [minimum covariance determinant](/minimum-covariance-determinant/).

## When to use it

Use MM-regression as the default robust linear regression when outliers in $y$ or bad leverage points in $x$ are possible and you want an efficiency close to least squares on clean data. Use plain least squares with [Cook's distance](/cooks-distance/) and [leverage](/leverage-statistics/) diagnostics when the data are clean or the outliers are few and easy to see. Use [RANSAC](/ransac/) in geometric fitting with a known inlier threshold. Use the [Huber M-estimator](/huber-m-estimator/) in regression only when $x$ has no outliers.

## Pitfalls

- **The constant $b$ depends on how $\rho$ is scaled.** With $\rho$ scaled to a maximum of 1, $b = 1/2$. With the biweight $\rho$ of maximum $c_0^2/6$, the same estimator needs $b = c_0^2/12$. Mixing the two conventions gives a wrong scale.
- **Too few subsets.** With a large $p$ and many outliers, all random subsets can contain an outlier, and the S-stage fails. Use Fast-S or a deterministic start.
- **Updating the scale.** The scale must stay fixed in the M-stage. Recomputing it from the M-stage residuals destroys the breakdown guarantee.
- **Efficiency is asymptotic.** With few points per coefficient, the efficiency on clean data can be well below 95%.
- **A local solution.** The M-stage finds a stationary point near the start. A different start can give a different answer.
- **Singular weighted designs.** With factor variables or many zero weights, the weighted design can be singular. Check the rank.

## Implementations

## History

Rousseeuw (1984) introduced the least median of squares, the first affine equivariant regression estimator with breakdown point one half. Rousseeuw and Yohai (1984) defined S-estimators, which have high breakdown and are asymptotically normal, but have low efficiency. Yohai (1987) combined an S-estimate of scale with an efficient M-step and proved that the result keeps both properties. Salibián-Barrera and Yohai (2006) gave the Fast-S algorithm that most software uses for the first stage.

## References
