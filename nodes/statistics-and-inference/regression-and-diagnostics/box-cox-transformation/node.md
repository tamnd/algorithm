---
tag: KHKPKJ
kind: technique
slug: box-cox-transformation
name: Box-Cox transformation
aliases:
- Box-Cox power transform
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: Transforms a positive response by (y^lambda - 1) / lambda, or log y at lambda = 0, choosing lambda by profile likelihood to make errors closer to normal with constant variance.
prereqs: [likelihood-function, maximum-likelihood-estimation, ordinary-least-squares]
see_also: [q-q-plot, heteroscedasticity, wilks-theorem, golden-section-search, bisection-method, generalized-linear-model, catastrophic-cancellation, regression-f-test]
sources:
  - paper: doi:10.1111/j.2517-6161.1964.tb00553.x
    title: "G. E. P. Box and D. R. Cox, An analysis of transformations, Journal of the Royal Statistical Society, Series B 26(2), 1964, pp. 211 to 243"
    locator: The whole paper (the power family, the likelihood with the Jacobian, the maximized log-likelihood in lambda and its approximate confidence region, the biological and textile examples)
  - paper: doi:10.1093/biomet/87.4.954
    title: "In-Kwon Yeo and Richard A. Johnson, A new family of power transformations to improve normality or symmetry, Biometrika 87(4), 2000, pp. 954 to 959"
    locator: The whole paper (a power family defined for all real y)
  - paper: doi:10.1080/01621459.1981.10477649
    title: "Peter J. Bickel and Kjell A. Doksum, An analysis of transformations revisited, Journal of the American Statistical Association 76, 1981, pp. 296 to 311"
    locator: The whole paper (the extra variance of the regression coefficients when lambda is estimated)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Chapter 10 (departures from the assumptions, transforming the response, the Box-Cox method)
---

The Box-Cox transformation replaces a positive response $y$ by $y^{(\lambda)} = (y^\lambda - 1)/\lambda$, which is $\log y$ in the limit $\lambda = 0$, and chooses the power $\lambda$ by maximum likelihood. The model is that for some $\lambda$ the transformed responses follow a linear model with independent normal errors of constant variance. Maximizing out the coefficients and the variance leaves a one-dimensional function, the profile log-likelihood $\ell(\lambda) = -\frac n2\log(\mathrm{RSS}(\lambda)/n) + (\lambda - 1)\sum_i\log y_i$, whose second term is the Jacobian of the change of scale. One QR factorization of the design matrix makes each value of $\ell$ cost $O(np)$, so a grid search, a golden-section refinement and a likelihood ratio interval for $\lambda$ cost little more than one fit. George Box and David Cox published the method in 1964. It is a choice of scale for the analysis, not a cure: it cannot make every data set normal, and it needs $y > 0$.

## In plain words

Many measurements, such as incomes, concentrations and times, are skewed, and their spread grows with their size. A straight-line model with even scatter fits them badly. Taking logs often helps; taking square roots or reciprocals sometimes helps more. The Box-Cox method tries the whole range of powers between them and asks the data which one makes the scatter around the fitted model look most like even, bell-shaped noise. To compare different powers fairly, it corrects for the fact that a power stretches or squeezes the scale. The answer comes with a range of powers that fit about equally well, so a simple power in that range, such as the log, can be used.

## When it applies

- The response is strictly positive, and the analysis is a linear model in some scale: $y_i^{(\lambda)} = x_i^\top b + \varepsilon_i$ with $X$ an $n \times p$ matrix of rank $p < n$.
- The departures to fix are skewness and a variance that changes with the mean, and one power can fix both at once. Often it can: if the standard deviation is proportional to the mean to the power $\alpha$, then $\lambda = 1 - \alpha$ stabilizes the variance to first order (the log for $\alpha = 1$, the square root for Poisson-like counts with $\alpha = 1/2$).
- The ratio of the largest to the smallest $y$ is not close to 1. If all $y$ lie in a narrow band, every power is nearly linear on it and the data cannot tell the powers apart.
- The transformed scale has a meaning for the user, or only tests and predictions are needed. Coefficients on the $\lambda = 0.23$ scale are hard to interpret.

## The template

The input is $y_1, \dots, y_n > 0$, the design matrix $X$ (with an intercept unless there is a reason not to have one), a search range $[\lambda_{lo}, \lambda_{hi}]$ with $m$ grid points, a tolerance and a confidence level $1 - \alpha$.

```pseudo id=main
BOX-COX(y[1..n], X, λlo, λhi, m, tol, level)
L1  if some y_i ≤ 0 then error "Box-Cox needs y > 0"
L2  L_i ← log y_i; G ← mean of the L_i; factor X = QR once by Householder reflections
L3  define ℓ(λ) = −(n/2) log(RSS(λ)/n) + (λ − 1) Σ L_i     ▷ RSS of the fit of y^(λ) on X, O(np) with Q
L4  evaluate ℓ at m equally spaced λ_j in [λlo, λhi]; let λ_k be the best
L5  λ̂ ← golden-section maximum of ℓ on [λ_(k−1), λ_(k+1)], to tolerance tol
L6  target ← ℓ(λ̂) − χ²_(1, level)/2
L7  lower end: bisection between λ̂ and the first grid point below λ̂ with ℓ < target (none: open)
L8  upper end: bisection between λ̂ and the first grid point above λ̂ with ℓ < target (none: open)
    return λ̂, ℓ(λ̂) and the interval
```

**Why this function of $\lambda$.** If $z_i = y_i^{(\lambda)}$ has density $N(x_i^\top b, \sigma^2)$, the density of $y_i$ is that density times $|dz_i/dy_i| = y_i^{\lambda - 1}$. So the log-likelihood of $(b, \sigma^2, \lambda)$ is

$$-\frac n2\log(2\pi\sigma^2) - \frac{\lVert y^{(\lambda)} - Xb\rVert^2}{2\sigma^2} + (\lambda - 1)\sum_i\log y_i.$$

For fixed $\lambda$ the maximum over $b$ is the [least squares](/ordinary-least-squares/) fit of $y^{(\lambda)}$ on $X$, and over $\sigma^2$ it is $\mathrm{RSS}(\lambda)/n$. Substituting gives $\ell(\lambda) - \frac n2(\log 2\pi + 1)$. Without the Jacobian term, the residual sums of squares at different $\lambda$ are in different units and cannot be compared: $\mathrm{RSS}(\lambda)$ alone mixes the quality of the fit with the change of units, and its minimum has no meaning. An equivalent form divides $y^{(\lambda)}$ by $\dot y^{\lambda - 1}$, where $\dot y$ is the geometric mean; then $\ell$ is $-\frac n2\log$ of the residual sum of squares of the scaled responses over $n$.

**Why one factorization suffices.** $X$ does not depend on $\lambda$. With $X = QR$ by [Householder reflections](/householder-reflections/), $\mathrm{RSS}(\lambda)$ is the squared norm of the last $n - p$ entries of $Q^\top y^{(\lambda)}$, which costs $O(np)$ to apply. The factorization costs $O(np^2)$ once.

**Numerical form.** Evaluating $(y^\lambda - 1)/\lambda$ directly loses all digits for small $|\lambda|$ ([catastrophic cancellation](/catastrophic-cancellation/)), and $y^\lambda$ overflows for large $|\lambda|\log y$. The implementation uses centered logs $d_i = L_i - G$ and the identity

$$\frac{y_i^{(\lambda)}}{\dot y^{\lambda - 1}} = \dot y\cdot\frac{\operatorname{expm1}(\lambda d_i) - \operatorname{expm1}(-\lambda G)}{\lambda}.$$

The second term is the same for every $i$, so it is dropped when $X$ contains the intercept. At $\lambda = 0$ the expression is $\dot y\,L_i$, and the limit is continuous.

**What is exact and what is not.** The function $\ell$ is computed exactly up to rounding. The grid in L4 finds the best of $m$ points, and golden-section search (see [golden-section search](/golden-section-search/)) then converges to a local maximum in the bracket around it. If $\ell$ has two separated peaks of nearly equal height, the grid may pick the lower one; nothing in the method proves a global maximum, and a plot of $\ell$ is the check. The interval of L6 to L8 is the likelihood ratio interval: by [Wilks' theorem](/wilks-theorem/), $2(\ell(\hat\lambda) - \ell(\lambda_0)) \to \chi^2_1$ under $\lambda = \lambda_0$, so its coverage is only asymptotic. The [bisection method](/bisection-method/) finds the first crossing of the target level on each side; if $\ell$ dips below and rises again, the set is not an interval, and the method returns its inner part.

**Cost.** $O(np^2)$ for the factorization, then $O(np)$ for each of the $m + O(\log((\lambda_{hi} - \lambda_{lo})/(m\,\mathrm{tol})))$ evaluations: $O(np^2 + np(m + \log(1/\mathrm{tol})))$ time and $O(np)$ space.

**Example.** The eight values $y = (0.1, 0.2, 0.4, 0.5, 0.9, 1.3, 2.0, 3.6)$ of the [Q-Q plot](/q-q-plot/) example, with an intercept only ($p = 1$), give

| $\lambda$ | $-1$ | $-0.5$ | $0$ | $0.5$ | $1$ | $2$ |
|---|---|---|---|---|---|---|
| $\mathrm{RSS}(\lambda)$ | 76.03 | 21.83 | 9.977 | 7.849 | 9.795 | 34.49 |
| $\ell(\lambda)$ | $-2.226$ | 1.071 | 2.507 | 1.771 | $-0.810$ | $-9.235$ |

$\mathrm{RSS}$ alone is smallest near $\lambda = 0.5$; the Jacobian term moves the maximum of $\ell$. The search on $[-2, 2]$ with 81 grid points gives $\hat\lambda = 0.0778$ and $\ell(\hat\lambda) = 2.5342$. The 95% interval, where $\ell \ge 2.5342 - 3.8415/2$, is $[-0.587, 0.761]$. It contains 0, with likelihood ratio statistic $2(2.5342 - 2.5072) = 0.054$, so the log scale is supported. It excludes 1: the statistic for no transformation is $6.69$, with p-value 0.0097 against $\chi^2_1$. The Q-Q plot of the logs is nearly straight, with correlation 0.996.

**Measured coverage.** With $\log y_i = 1 + 0.3x_i + N(0, 0.25^2)$ on $n = 20$ equally spaced $x_i$ in $[1, 10]$ (true $\lambda = 0$), 1000 replications with seed 21 and the search range $[-3, 3]$ gave a coverage of 0.926 for the nominal 95% interval. With true $\lambda = 0.5$, $y_i^{(0.5)} = 2 + 0.5x_i + N(0, 0.5^2)$ (seed 22), it was 0.939, and with true $\lambda = 0$ and $n = 80$ (seed 23) it was 0.946. These are measurements for one design; they show the interval is a little short in small samples, as an asymptotic interval often is.

## Classic examples

- **Survival times in a factorial experiment.** Box and Cox (1964) analyzed the survival times of animals under three poisons and four treatments. The likelihood pointed near $\lambda = -1$, so they analyzed the reciprocal, the rate of dying. On that scale the variances were close to equal and the evidence for an interaction between poison and treatment became weak, so a simpler model and the usual [F-tests](/regression-f-test/) of the analysis of variance could be used.
- **Cycles to failure.** Their second example, the number of cycles to failure of worsted yarn in a $3^3$ design, pointed to the log. On the log scale a model with main effects only described the data well.
- **Fixing a fan of residuals.** When the residuals spread out with the fitted values, a Box-Cox power is one remedy for [heteroscedasticity](/heteroscedasticity/), next to weighting and robust standard errors.
- **Checking normality before a t-test or ANOVA.** Transform, then check the residuals with a [Q-Q plot](/q-q-plot/), as in the example.

## Variations

- **Shifted family.** $(y + \lambda_2)^{(\lambda_1)}$ allows $y > -\lambda_2$; Box and Cox gave it in the same paper. The likelihood in $\lambda_2$ can be unbounded as $\lambda_2 \to -\min y$, so $\lambda_2$ is usually fixed.
- **Yeo-Johnson.** A power family for all real $y$: $((y + 1)^\lambda - 1)/\lambda$ for $y \ge 0$ and $-((1 - y)^{2 - \lambda} - 1)/(2 - \lambda)$ for $y < 0$, with logs in the limits. The same profile likelihood method applies, with Jacobian $(\lambda - 1)\sum\operatorname{sign}(y_i)\log(|y_i| + 1)$.
- **Rounded powers.** Choose the simplest value in the interval, from $-1, -1/2, 0, 1/2, 1, 2$, and analyze on that scale. This is what Box and Cox did.
- **Transforming the predictors.** Box and Tidwell fit powers of the predictors instead of the response, for nonlinearity without a change of the error scale.
- **Modeling the mean and variance directly.** A [generalized linear model](/generalized-linear-model/) keeps $y$ on its own scale and states a link and a variance function, so the mean of $y$, not of a transform of $y$, is modeled.

## Pitfalls

- **Zeros and negative values.** The method is undefined for $y \le 0$. Adding a constant before the transform changes $\hat\lambda$ and the conclusions, and the choice of constant is arbitrary. Use the shifted family with care, or Yeo-Johnson, or a model for counts.
- **Inference after choosing $\lambda$.** Tests and intervals for $b$ that treat $\hat\lambda$ as known ignore its estimation. Bickel and Doksum (1981) showed that the variance of $\hat b$ can then grow a lot; Box and Cox replied that $b$ has no fixed meaning when the scale itself is estimated. A fixed round $\lambda$ chosen from the interval avoids most of the issue.
- **Back-transforming.** The inverse of the fitted mean on the log scale estimates the median of $y$, not its mean. For the mean under normal errors on the log scale, multiply by $\exp(\sigma^2/2)$.
- **Outliers decide $\lambda$.** One extreme $y$ can pull $\hat\lambda$ strongly. Check the influence of single points, for example with [Cook's distance](/cooks-distance/) on the chosen scale.
- **One power for three goals.** Linearity of the mean, constant variance and normality may need different powers. The likelihood finds a compromise; it may fix none of them well.
- **Comparing raw RSS.** Choosing $\lambda$ by the smallest $\mathrm{RSS}(\lambda)$ without the Jacobian, or by the residual standard deviation on each scale, is wrong. In the example it picks a value near 0.5 instead of 0.08.

## Exercises

1. Derive the profile log-likelihood $\ell(\lambda)$ from the normal density of $y^{(\lambda)}$, including the Jacobian.
2. Show that $y^{(\lambda)} \to \log y$ as $\lambda \to 0$, and that $\lambda \mapsto y^{(\lambda)}$ is increasing in $y$ for every $\lambda$.
3. Show that when $X$ contains the intercept, replacing $y$ by $cy$ with $c > 0$ does not change $\hat\lambda$ or the interval, and that it changes $\ell$ by the constant $-n\log c$.
4. Use the delta method to show that if $\operatorname{sd}(y) \propto E[y]^\alpha$, then $y^{1 - \alpha}$ (or $\log y$ when $\alpha = 1$) has approximately constant variance.
5. Write the profile log-likelihood for the Yeo-Johnson family and find its Jacobian term.

## References
