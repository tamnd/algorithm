---
tag: C1XC0A
kind: algorithm
slug: local-polynomial-regression
name: Local polynomial regression
aliases:
- LOESS
- LOWESS
- locally weighted scatterplot smoothing
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Fits a low-degree polynomial by weighted least squares around each point. It removes the boundary bias of kernel regression; LOWESS adds robust reweighting.
model: real-ram
complexity:
  vars: {n: the number of data points, p: the degree, q: the number of points where the estimate is wanted, k: the number of neighbours in a window, t: the number of robustness iterations}
  time: {worst: O(q (n p + p^3)), lowess: O(n log n + (t + 1) n k)}
  space: {extra: O(p^2)}
properties: {deterministic: true, randomized: false, exact: true, linear_smoother: true, reproduces_polynomials_of_degree_p: true}
history:
  year: 1979
  people: [William S. Cleveland, Susan J. Devlin, Charles J. Stone, Jianqing Fan, Irène Gijbels]
  note: Cleveland published LOWESS, a robust local linear smoother, in 1979, and LOESS with Devlin in 1988. Fan showed in 1992 and 1993 that the local linear fit has no boundary or design bias of order h.
prereqs: [nadaraya-watson-estimator, weighted-least-squares, normal-equations]
see_also: [kde-bandwidth-selection, savitzky-golay-filter, smoothing-spline, stl-decomposition, regression-discontinuity-design, tukey-biweight, iteratively-reweighted-least-squares, median-absolute-deviation]
sources:
  - paper: doi:10.1080/01621459.1979.10481038
    title: William S. Cleveland, Robust locally weighted regression and smoothing scatterplots, Journal of the American Statistical Association 74(368), 1979
    locator: pp. 829 to 836 (LOWESS; the tricube weights on the nearest neighbours, and the robustness iterations with bisquare weights and 6 times the median absolute residual)
  - paper: doi:10.1080/01621459.1988.10478639
    title: William S. Cleveland and Susan J. Devlin, Locally weighted regression. An approach to regression analysis by local fitting, Journal of the American Statistical Association 83(403), 1988
    locator: pp. 596 to 610 (LOESS with several predictors and local quadratic fits)
  - paper: doi:10.1080/01621459.1992.10476255
    title: Jianqing Fan, Design-adaptive nonparametric regression, Journal of the American Statistical Association 87(420), 1992
    locator: pp. 998 to 1004 (the local linear smoother has no design bias)
  - paper: doi:10.1214/aos/1176349022
    title: Jianqing Fan, Local linear regression smoothers and their minimax efficiencies, The Annals of Statistics 21(1), 1993
    locator: pp. 196 to 216 (minimax efficiency of the local linear smoother)
  - paper: doi:10.1214/aos/1176348900
    title: Jianqing Fan and Irène Gijbels, Variable bandwidth and local linear regression smoothers, The Annals of Statistics 20(4), 1992
    locator: pp. 2008 to 2036 (the local linear fit adapts automatically to the boundary)
  - paper: doi:10.1214/aos/1176325632
    title: D. Ruppert and M. P. Wand, Multivariate locally weighted least squares regression, The Annals of Statistics 22(3), 1994
    locator: pp. 1346 to 1370 (bias and variance of local polynomial fits, in the interior and at the boundary, in several dimensions)
  - book: isbn:9780412983214
    title: Jianqing Fan and Irène Gijbels, Local Polynomial Modelling and Its Applications, Chapman and Hall, 1996
    locator: Chapter 3 (the local polynomial fit, its equivalent kernel, and its bias and variance)
---

Local polynomial regression estimates a regression function $m(x) = \mathbb{E}[Y \mid X = x]$ by fitting, at each point $x$, a polynomial of low degree $p$ to the nearby data by weighted least squares, and taking the value of that polynomial at $x$. The weights come from a kernel of bandwidth $h$. With $p = 0$ it is the [Nadaraya-Watson estimator](/nadaraya-watson-estimator/). With $p = 1$, the local linear fit, it reproduces straight lines exactly, so it has no bias of order $h$ at the ends of the data or where the design is uneven. LOWESS (Cleveland 1979) is a local linear fit on nearest-neighbour windows with tricube weights, followed by a few robustness iterations that give less weight to points with large residuals. LOESS is the same idea with local quadratics and several predictors.

## In plain words

To estimate a curve at some place, take the data points nearby, give the closest ones the most weight, and fit a straight line through them by least squares. The height of that line at the place is the estimate. Then move to the next place and fit a new line.

A plain weighted average of the nearby points does well in the middle of the data, but at the ends all the neighbours are on one side, and a rising curve gets pulled down or up. A line through the neighbours follows the slope, so it does not have this error. LOWESS adds one more idea: after a first fit, points far from the curve are probably bad, so it fits again with less weight on them.

## The problem

The input is $n$ pairs $(x_1, y_1), \ldots, (x_n, y_n)$ from the model $y_i = m(x_i) + e_i$, a kernel $K \ge 0$, a bandwidth $h$ and a degree $p$. At a point $x$, the local fit minimizes
$$\sum_{i=1}^n K\!\left(\frac{x_i - x}{h}\right)\Big(y_i - \sum_{k=0}^p \beta_k (x_i - x)^k\Big)^2,$$
and the estimate is $\hat m(x) = \hat\beta_0$. The other coefficients estimate the derivatives: $k!\,\hat\beta_k$ estimates $m^{(k)}(x)$. LOWESS uses $p = 1$, the tricube kernel $(1 - |u|^3)^3$ and, at each $x_i$, the bandwidth $h_i$ equal to the distance to the $r$-th nearest $x_j$, where $r = \lfloor fn + \frac12 \rfloor$ for a span $f$, often $2/3$.

## The algorithm

```pseudo id=main
LOCAL-POLYNOMIAL(x, (x_i, y_i), h, p, δ)          ▷ δ: robustness weights, all 1 by default
L1  w_i ← δ_i · K((x_i − x)/h) for all i
L2  S_jk ← Σ_i w_i (x_i − x)^(j+k);  t_j ← Σ_i w_i (x_i − x)^j y_i   for 0 ≤ j, k ≤ p
L3  solve S β = t;  return β_0                    ▷ undefined if S is singular

LOWESS((x_i, y_i), f, t)
L4  δ_i ← 1 for all i;  h_i ← the distance from x_i to its r-th nearest x_j, r = round(f n)
L5  repeat t + 1 times
L6      ŷ_i ← LOCAL-POLYNOMIAL(x_i, data, h_i, 1, δ) with the tricube kernel, for all i
L7      r_i ← y_i − ŷ_i;  s ← median |r_i|
L8      δ_i ← B(r_i / (6s)), with B(u) = (1 − u²)² for |u| < 1 and 0 otherwise
L9  return ŷ
```

Lines L2 and L3 are the [normal equations](/normal-equations/) of a [weighted least squares](/weighted-least-squares/) fit in the shifted variable $x_i - x$, so that $\beta_0$ is the value at $x$. They have $p + 1$ unknowns, usually 2 or 3. The robustness weights of line L8 are the [Tukey biweight](/tukey-biweight/) of the residuals, scaled by 6 times their median absolute value; this is [iteratively reweighted least squares](/iteratively-reweighted-least-squares/) with a local fit in place of a global one. The code skips line L8 after the last fit, and when $s = 0$ it gives weight 1 to the points with residual 0 and weight 0 to the others.

## Example

**Local linear against local constant.** Seven points on $y = x^2$ at $x = 0, 1, \ldots, 6$, the Epanechnikov kernel $\frac34(1 - u^2)$ and $h = 3$. Exact values from the test file:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| true $x^2$ | 0 | 1 | 4 | 9 | 16 | 25 | 36 |
| local linear | −20/73 ≈ −0.27 | 67/35 ≈ 1.91 | 28/5 = 5.6 | 53/5 = 10.6 | 17.6 | 907/35 ≈ 25.91 | 2608/73 ≈ 35.73 |
| local constant | 14/11 ≈ 1.27 | 43/15 ≈ 2.87 | 5.6 | 10.6 | 17.6 | 343/15 ≈ 22.87 | 302/11 ≈ 27.45 |

At $x = 2, 3, 4$ the neighbours lie symmetrically, the slope term has no effect, and the two fits agree; both are too high by $1.6$, because they flatten the curvature. At the ends the local constant fit is far off: $27.45$ for $36$ at $x = 6$. The local linear fit is off by only $0.27$, because it follows the slope. For the line $y = 2x$ at the same points, the local linear fit gives exactly $0, 2, \ldots, 12$, while the local constant fit gives $18/11$ at $x = 0$.

**LOWESS with an outlier.** Ten points near $y = 2x + 1$, with one wild value at $x = 7$; span $f = 2/3$, so $r = 7$ neighbours:

| $x$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $y$ | 3.1 | 4.9 | 7.2 | 8.8 | 11.1 | 13.0 | **30.0** | 16.9 | 19.2 | 21.0 |
| no robustness ($t = 0$) | 3.05 | 5.03 | 7.01 | 9.01 | 12.50 | 16.84 | 19.31 | 20.07 | 20.47 | 20.49 |
| LOWESS, $t = 2$ | 3.05 | 5.03 | 7.01 | 9.01 | 11.00 | 12.99 | 15.01 | 17.03 | 19.04 | 21.06 |

Without robustness, the outlier lifts the curve from $x = 5$ to the end. After the first fit its residual is the largest by far, its bisquare weight is 0, and the next fits ignore it. The robust fit is within $0.07$ of the line $2x + 1$ everywhere.

## Correctness

If at least $p + 1$ distinct points have positive weight, the weighted least squares problem has one solution. If the data lie on a polynomial $q$ of degree at most $p$, that polynomial has weighted residual sum 0, so it is the fit, and $\hat m(x) = q(x)$ exactly, at every $x$, inside or at the edge of the data. For $p = 1$ this means the local linear fit reproduces any line. It follows that the equivalent weights $\ell_i(x)$ in $\hat m(x) = \sum_i \ell_i(x) y_i$ satisfy $\sum_i \ell_i = 1$ and $\sum_i \ell_i (x_i - x) = 0$. So for a smooth $m$, the constant and linear parts of the Taylor expansion cancel, and the bias comes from the second derivative only. At the end point of an equally spaced design,
$$\mathbb{E}\,\hat m(0) - m(0) = \frac{h^2}{2}m''(0)\,\frac{(\mu_2^+)^2 - \mu_1^+\mu_3^+}{\mu_0^+\mu_2^+ - (\mu_1^+)^2} + o(h^2),$$
with the one-sided moments $\mu_k^+ = \int_0^1 u^k K(u)\,du$. For the Epanechnikov kernel the factor is $-11/95$. The Nadaraya-Watson estimator has a boundary bias of order $h$ instead. The full proofs are below. The rates for random designs and the minimax efficiency are cited.

## Complexity

- **One point.** The weights cost $O(n)$, the $2p + 1$ power sums $O(np)$, and the solve $O(p^3)$: $O(np + p^3)$ time and $O(p^2)$ extra space. For $q$ points, $O(q(np + p^3))$.
- **Nearest-neighbour windows.** With sorted data, the $k$ nearest neighbours of each point form a window that slides along the data, so all $n$ fitted values cost $O(n \log n + nk)$ for fixed $p$. LOWESS repeats the fits $t + 1$ times, usually $t = 2$.
- **Interpolation.** LOESS software fits at a set of vertices and interpolates between them, which makes the cost nearly linear in $n$.
- **Grid.** On an equally spaced design, the equivalent weights are the same at every interior point, and the fit is a convolution: this is the [Savitzky-Golay filter](/savitzky-golay-filter/).

## Properties

- **Exact for polynomials of degree p.** Proved above, and checked in exact arithmetic for $p = 1, 2, 3$.
- **No boundary or design bias of order h.** For $p = 1$, the bias is $\frac{h^2}{2}\mu_2 m''(x)$ in the interior and of order $h^2$ at the boundary, with no term in $f'/f$ for an uneven design. The variance has the same order as for the local constant fit, $\sigma^2(x)R(K)/(nhf(x))$, with a larger constant at the boundary (Fan 1992; Fan and Gijbels 1996). The rates are cited, not proved here.
- **Odd degrees.** Going from an even $p$ to $p + 1$ removes a bias term without raising the variance order, so odd degrees ($p = 1$, or $p = 3$ for derivatives) are usually preferred.
- **Linear smoother.** Without robustness weights, $\hat m = Ly$ for a matrix that depends only on the $x_i$. Leave-one-out residuals and degrees of freedom $\operatorname{tr} L$ follow directly.
- **Robustness.** LOWESS resists isolated outliers in $y$. It does not resist many outliers in one window, and the robustness iterations have no general convergence guarantee.

## Variants and improvements

- **LOESS.** Cleveland and Devlin (1988) allow several predictors, local quadratic fits and conditionally parametric terms, and choose the span by a $C_p$-type criterion.
- **Derivatives.** $k!\,\hat\beta_k$ estimates $m^{(k)}(x)$; use $p = k + 1$.
- **Variable bandwidth.** Nearest-neighbour windows, as in LOWESS, or a bandwidth $h(x)$ from a plug-in rule (Fan and Gijbels 1992).
- **Bandwidth choice.** Cross-validation, generalized cross-validation, or plug-in rules for the regression AMISE; see [bandwidth selection](/kde-bandwidth-selection/).
- **Local likelihood.** For counts or binary responses, fit a local generalized linear model by local likelihood instead of local least squares.
- **Seasonal decomposition.** [STL](/stl-decomposition/) applies LOESS repeatedly to separate the trend and the seasonal part of a time series.

## When to use it

Use the local linear fit as the default nonparametric regression in one or a few predictors: it is simple, it behaves well at the ends of the data, and it adapts to uneven designs. Use LOWESS to draw a smooth trend through a scatter plot, especially when some points may be wild. In a [regression discontinuity design](/regression-discontinuity-design/), local linear fits on each side of the cut-off are the standard estimator, because the effect is measured at a boundary. For many predictors, or when you need a global smooth function, a [smoothing spline](/smoothing-spline/), an additive model or a Gaussian process is often better.

## Pitfalls

- **Sparse windows.** With a fixed $h$, a window with fewer than $p + 1$ distinct points makes the system singular, and a window with few points makes the fit unstable. Nearest-neighbour windows avoid both.
- **Higher degree is not always better.** Local quadratics and cubics need wider windows and have more variance, especially at the boundary. Prefer $p = 1$ unless the curve has sharp peaks.
- **Robustness with small spans.** With few points in each window, the robustness iterations can lock onto an outlier. On the example data with span $1/2$ (5 neighbours), the robust fit after four iterations passed through the outlier at $x = 7$ and stayed at 30 to the end; with span $2/3$ it did not. This is a measurement, not a rule.
- **Extrapolation.** The local line at the last data point continues its slope outside the data, which can be far off. Do not evaluate the fit far outside the data.
- **Confidence bands.** The bias does not vanish at the usual bandwidths, so bands from the variance alone cover too little; undersmooth or correct the bias.

## Implementations

## History

Fitting low-degree polynomials to moving windows is old: actuaries used it for graduation of mortality tables, and Savitzky and Golay (1964) used it on equally spaced spectra. Stone (1977) studied local polynomial fits in his work on consistent nonparametric regression. Cleveland (1979) introduced LOWESS for scatter plots, with nearest-neighbour windows, tricube weights and robustness iterations. Cleveland and Devlin (1988) extended it to LOESS. Fan (1992, 1993) and Fan and Gijbels (1992) showed that the local linear fit has no design bias, adapts to the boundary, and is minimax efficient among linear smoothers. Their 1996 book made local polynomial fitting the standard view of kernel regression, with the Nadaraya-Watson estimator as the case $p = 0$.

## References
