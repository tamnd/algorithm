---
tag: AX73CB
kind: definition
slug: cooks-distance
name: Cook's distance
aliases:
- Cook's D
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: 'A measure of the influence of one observation: how far all fitted values move when it is deleted, scaled by p times the residual variance.'
prereqs: [studentized-residual, leverage-statistics]
see_also: [hat-matrix, influence-function, sherman-morrison-formula, confidence-interval, least-trimmed-squares, huber-m-estimator, cross-validation, ordinary-least-squares]
sources:
  - paper: doi:10.1080/00401706.1977.10489493
    title: "R. Dennis Cook, Detection of influential observation in linear regression, Technometrics 19(1), 1977, pp. 15 to 18"
    locator: The whole paper (the definition of D_i through the confidence ellipsoid, the closed form in the studentized residual and the leverage, and the comparison with percentiles of F(p, n - p))
  - book: isbn:9780412242809
    title: R. Dennis Cook and Sanford Weisberg, Residuals and Influence in Regression, Chapman and Hall, 1982
    locator: Chapter 3 (the assessment of influence, Cook's distance and the deletion of several cases)
  - book: isbn:9780471058564
    title: David A. Belsley, Edwin Kuh and Roy E. Welsch, Regression Diagnostics, Wiley, 1980
    locator: Chapter 2 (the deletion diagnostics DFBETAS and DFFITS and their cutoffs)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Section 10.6.3 (leave-one-out case diagnostics, including Cook's D)
---

Cook's distance $D_i$ measures the influence of observation $i$ on a least squares fit: how much all the fitted values move when that observation is deleted, in units of $p$ times the estimated error variance. It combines the two ingredients of influence, the size of the [studentized residual](/studentized-residual/) (is the point off the line?) and the [leverage](/leverage-statistics/) (can the point move the line?). R. Dennis Cook introduced it in 1977. It is computed from one fit, without $n$ refits. It is a descriptive measure, not a test, and it looks at one point at a time.

## Definition

Let $y = Xb + \varepsilon$ with $X$ an $n \times p$ matrix of rank $p$ (intercept included in the $p$ columns) and $b$ the coefficient vector. Let $\hat b$ be the least squares estimate, $\hat y = X\hat b$, $e = y - \hat y$ and $s^2 = \sum e_j^2/(n - p)$. Let $\hat b_{(i)}$ be the estimate without observation $i$ and $\hat y_{(i)} = X\hat b_{(i)}$, the fitted values of all $n$ points from that fit. Assume $h_{ii} < 1$. **Cook's distance** of observation $i$ is

$$D_i = \frac{\lVert \hat y - \hat y_{(i)}\rVert^2}{p\,s^2} = \frac{(\hat b - \hat b_{(i)})^\top X^\top X(\hat b - \hat b_{(i)})}{p\,s^2}.$$

The two forms agree because $\hat y - \hat y_{(i)} = X(\hat b - \hat b_{(i)})$.

**One-fit formula.** By the [Sherman-Morrison formula](/sherman-morrison-formula/), $\hat b - \hat b_{(i)} = (X^\top X)^{-1}x_i\,e_i/(1 - h_{ii})$. Substituting, with $x_i^\top(X^\top X)^{-1}x_i = h_{ii}$,

$$D_i = \frac{e_i^2\,h_{ii}}{p\,s^2(1 - h_{ii})^2} = \frac{r_i^2}{p}\cdot\frac{h_{ii}}{1 - h_{ii}},$$

where $r_i = e_i/(s\sqrt{1 - h_{ii}})$ is the internally studentized residual. The first factor measures the outlyingness of $y_i$; the second, $h_{ii}/(1 - h_{ii})$, grows without bound as $h_{ii} \to 1$. All $n$ distances cost $O(np^2)$ for the QR factorization and $O(np)$ after it.

**Reading the size.** The $100(1 - \alpha)\%$ confidence ellipsoid for $b$ under normal errors is $\{\beta : (\beta - \hat b)^\top X^\top X(\beta - \hat b) \le p\,s^2 F_{(p, n-p, 1-\alpha)}\}$. So $D_i = F_{(p, n-p, 1-\alpha)}$ means that deleting observation $i$ moves the estimate to the boundary of that ellipsoid. Cook proposed to judge $D_i$ by the percentile of $F_{p, n-p}$ that it reaches; for example, $D_i$ near the median of $F_{p, n-p}$ (about 1 for moderate $n - p$) moves the estimate to the edge of a 50% confidence region. His paper gives no fixed cutoff. The rules $D_i > 1$ and $D_i > 4/n$, common in software, are later conventions. $D_i$ does not have an F distribution: the F percentiles are a ruler, not a null law, so "$D_i$ is significant" has no meaning.

**Scale.** $D_i$ does not change when $y$ is multiplied by a constant or when $X$ is replaced by $XA$ for a nonsingular $A$: it depends only on the fitted values.

## Examples and non-examples

**Six points, one far in $x$.** For $x = (1, 2, 3, 4, 5, 10)$ and $y = (2, 3, 5, 4, 6, 4)$, $p = 2$, $s^2 = 2.1016$. With the leverages and residuals of the [studentized residual](/studentized-residual/) example:

| $i$ | $h_{ii}$ | $r_i$ | $D_i$ | percentile of $F_{2,4}$ |
|---|---|---|---|---|
| 1 | 0.3639 | $-1.2449$ | 0.4434 | 0.33 |
| 2 | 0.2590 | $-0.4939$ | 0.0426 | 0.04 |
| 3 | 0.1934 | 0.9267 | 0.1030 | 0.10 |
| 4 | 0.1672 | 0.0223 | 0.00005 | 0.00 |
| 5 | 0.1803 | 1.4114 | 0.2191 | 0.19 |
| 6 | 0.8361 | $-1.7595$ | 7.8947 | 0.96 |

For $F_{2, \nu}$ the CDF is $1 - (1 + 2x/\nu)^{-\nu/2}$, which gives the last column. Exact arithmetic gives $D_6 = 202419/25640$. Refitting without point 6 gives the line $1.3 + 0.9x$ instead of $3.2623 + 0.1770x$; the sum of squared changes of the six fitted values divided by $2s^2$ is again $7.8947$, exactly. Deleting point 6 moves the estimate to just outside the 95% confidence ellipse of the full fit. Point 1 has the second largest leverage and a moderate residual; $D_1 = 0.44$ is about half the median of $F_{2,4}$, which is $2(\sqrt 2 - 1) = 0.83$.

**High leverage, no influence.** If $y_6$ is changed to 10.3, which lies on the line through the other five points, then $e_6 = 0$ and $D_6 = 0$ although $h_{66} = 0.836$.

**Masking: two far points hide each other.** Duplicate the far point: $x = (1, 2, 3, 4, 5, 10, 10)$, $y = (2, 3, 5, 4, 6, 4, 4)$. Each copy now has $h_{ii} = 0.455$, below $2p/n = 0.571$, and $D_i = 0.135$, a small value, because deleting one copy leaves the other in place. Deleting both copies at once moves the fitted values by a generalized Cook's distance $\lVert\hat y - \hat y_{(6,7)}\rVert^2/(2s^2) = 20.1$. One-at-a-time diagnostics miss clusters of influential points.

**Non-example: the largest residual.** In the six-point example the largest $|e_i|$ is at $x = 5$, whose $D_5 = 0.22$ is modest. The most influential point has only the third largest residual.

**Non-example: a test for outliers.** $D_i$ has no null distribution to compare with. An outlier test uses the externally studentized residual $t_i$ with a Bonferroni cutoff.

## Related definitions

- **DFFITS.** $\mathrm{DFFITS}_i = t_i\sqrt{h_{ii}/(1 - h_{ii})}$, the change of the own fitted value $\hat y_i - \hat y_{i(i)}$ divided by $s_{(i)}\sqrt{h_{ii}}$. It uses $s_{(i)}$ instead of $s$, and $D_i = \frac{s_{(i)}^2}{p\,s^2}\mathrm{DFFITS}_i^2$. Belsley, Kuh and Welsch suggest the cutoff $2\sqrt{p/n}$.
- **DFBETAS.** The change of one coefficient, $(\hat b_j - \hat b_{j(i)})/(s_{(i)}\sqrt{[(X^\top X)^{-1}]_{jj}})$, with the cutoff $2/\sqrt n$.
- **Leverage and residual.** $D_i$ is the product of a function of $r_i$ and a function of $h_{ii}$; the [hat matrix](/hat-matrix/) gives both.
- **[Influence function](/influence-function/).** The infinitesimal version: the derivative of an estimator with respect to the weight of one point. For least squares it is unbounded in both $x$ and $y$, which is why robust fits such as the [Huber M-estimator](/huber-m-estimator/) (bounded in $y$) and [least trimmed squares](/least-trimmed-squares/) (bounded in both) exist.
- **Generalized Cook's distance.** For a set $I$ of deleted points, $\lVert\hat y - \hat y_{(I)}\rVert^2/(p\,s^2)$, as in the masking example. The number of subsets grows exponentially, which is why multiple-case diagnostics use robust fits instead of enumeration.

## References
