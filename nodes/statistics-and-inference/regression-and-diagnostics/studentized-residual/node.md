---
tag: NDSGPG
kind: definition
slug: studentized-residual
name: Studentized residual
aliases:
- externally studentized residual
- deleted residual
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: A residual divided by an estimate of its standard deviation that accounts for its leverage. With the point left out of the variance estimate it has a t distribution.
prereqs: [hat-matrix, leverage-statistics, sample-variance]
see_also: [cooks-distance, q-q-plot, bonferroni-correction, student-t-test, cross-validation, sherman-morrison-formula, heteroscedasticity, huber-m-estimator]
sources:
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Section 10.2 (residuals, their variances and the internally and externally studentized residuals) and Section 10.6.3 (leave-one-out diagnostics)
  - book: isbn:9780412242809
    title: R. Dennis Cook and Sanford Weisberg, Residuals and Influence in Regression, Chapman and Hall, 1982
    locator: Chapter 2 (diagnostic methods using residuals, the studentized residuals, the mean shift outlier model and the Bonferroni outlier test)
  - book: isbn:9780471058564
    title: David A. Belsley, Edwin Kuh and Roy E. Welsch, Regression Diagnostics, Wiley, 1980
    locator: Chapter 2 (the studentized residual RSTUDENT with the deleted variance estimate s(i))
---

A studentized residual is a regression residual divided by an estimate of its own standard deviation. Raw residuals do not have equal variances even when the errors do: $\operatorname{Var}(e_i) = \sigma^2(1 - h_{ii})$, where $h_{ii}$ is the [leverage](/leverage-statistics/), so residuals at high-leverage points are small by construction. Dividing by $s\sqrt{1 - h_{ii}}$ puts all residuals on one scale. The *internal* version uses the usual $s$; the *external* version uses $s_{(i)}$, computed without observation $i$, and under normal errors it has the t distribution with $n - p - 1$ degrees of freedom exactly. Both come from one fit, without refitting.

## Definition

Let $y = Xb + \varepsilon$ with $X$ an $n \times p$ matrix of rank $p$ (intercept included in the $p$ columns), $b$ the coefficient vector and $\varepsilon$ with uncorrelated entries of mean 0 and variance $\sigma^2$. Let $\hat b$ be the least squares estimate, $e = y - X\hat b$ the residuals, $h_{ii}$ the diagonal of the [hat matrix](/hat-matrix/), and $s^2 = \sum e_j^2/(n - p)$. Assume $h_{ii} < 1$.

**Internally studentized residual** (also called the standardized residual):

$$r_i = \frac{e_i}{s\sqrt{1 - h_{ii}}}.$$

**Deleted variance.** Let $s_{(i)}^2$ be the residual variance estimate of the fit without observation $i$, with $n - p - 1$ degrees of freedom. One fit gives it:

$$s_{(i)}^2 = \frac{(n - p)s^2 - e_i^2/(1 - h_{ii})}{n - p - 1}.$$

**Externally studentized residual** (also called the deleted studentized residual, or RSTUDENT):

$$t_i = \frac{e_i}{s_{(i)}\sqrt{1 - h_{ii}}} = r_i\sqrt{\frac{n - p - 1}{n - p - r_i^2}}.$$

**The deleted residual and why $t_i$ is a t statistic.** Let $\hat y_{(i)} = x_i^\top\hat b_{(i)}$ be the prediction of $y_i$ from the fit without $i$. By the [Sherman-Morrison formula](/sherman-morrison-formula/), the deleted (or PRESS) residual is $d_i = y_i - \hat y_{(i)} = e_i/(1 - h_{ii})$, and $\operatorname{Var}(d_i) = \sigma^2\big(1 + x_i^\top(X_{(i)}^\top X_{(i)})^{-1}x_i\big) = \sigma^2/(1 - h_{ii})$. So $t_i = d_i/(s_{(i)}/\sqrt{1 - h_{ii}})$ is the prediction error of a point not used in the fit, divided by its estimated standard error. Under iid $N(0, \sigma^2)$ errors, $y_i$ is independent of the other $n - 1$ observations, and from those, $\hat b_{(i)}$ and $s_{(i)}^2$ are independent with $(n - p - 1)s_{(i)}^2/\sigma^2 \sim \chi^2_{n-p-1}$. So $d_i$ is normal with mean 0, independent of $s_{(i)}$, and

$$t_i \sim t_{n-p-1} \quad \text{exactly, for each fixed } i.$$

The $t_i$ for different $i$ are not independent. This needs the fit without $i$ to have rank $p$, that is, $h_{ii} < 1$.

**The internal version is bounded.** Under the same model, $r_i^2/(n - p)$ has the Beta$\big(\frac12, \frac{n-p-1}{2}\big)$ law, so $|r_i| \le \sqrt{n - p}$ always. A single wild point cannot have a large $r_i$ in a small sample, because it also inflates $s$. This is the reason to prefer $t_i$ for outlier detection: $t_i$ is a monotone function of $r_i$, but its scale is unbounded and its law is the familiar $t$.

**Mean shift outlier model.** Add to $X$ the indicator column $u_i$ of observation $i$. The t statistic of its coefficient is exactly $t_i$. So $|t_i| \ge t_{(n-p-1, 1-\alpha/2)}$ is the level $\alpha$ test that observation $i$, chosen in advance, is shifted. For the largest $|t_i|$, chosen after looking, the Bonferroni bound gives the cutoff $t_{(n-p-1, 1-\alpha/(2n))}$, which is conservative.

## Examples and non-examples

**Six points, one far in $x$.** Take $x = (1, 2, 3, 4, 5, 10)$ and $y = (2, 3, 5, 4, 6, 4)$ with $p = 2$. The fit is $\hat y = 3.2623 + 0.1770\,x$, $s^2 = 641/305 = 2.1016$ and $n - p - 1 = 3$. Exact arithmetic, checked by refitting without each point:

| $i$ | $x_i$ | $h_{ii}$ | $e_i$ | $r_i$ | $s_{(i)}^2$ | $t_i$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 0.3639 | $-1.4393$ | $-1.2449$ | 1.7165 | $-1.3775$ |
| 2 | 2 | 0.2590 | $-0.6164$ | $-0.4939$ | 2.6313 | $-0.4414$ |
| 3 | 3 | 0.1934 | 1.2066 | 0.9267 | 2.2005 | 0.9057 |
| 4 | 4 | 0.1672 | 0.0295 | 0.0223 | 2.8018 | 0.0193 |
| 5 | 5 | 0.1803 | 1.8525 | 1.4114 | 1.4067 | 1.7252 |
| 6 | 10 | 0.8361 | $-1.0328$ | $-1.7595$ | 0.6333 | $-3.2052$ |

The sixth raw residual is the third smallest in size, yet its studentized residuals are the largest: $\sqrt{1 - 0.8361} = 0.405$ scales it up by 2.5, and leaving it out drops the variance estimate from 2.10 to 0.63. Its internal value $-1.76$ is close to the bound $\sqrt{n - p} = 2$. Its external value $-3.21$ has two-sided p-value 0.049 against $t_3$, just under 0.05 for a point chosen in advance. Chosen as the largest of six, the Bonferroni p-value is $\min(1, 12 \cdot 0.0246) = 0.295$, and the Bonferroni cutoff is $t_{(3, 1 - 0.05/12)} = 6.23$. With $n = 6$ the data cannot prove an outlier, which is the honest answer.

**The identity between $r_i$ and $t_i$.** For point 6, $-1.7595\sqrt{3/(4 - 1.7595^2)} = -3.2050$, which agrees with the refit value up to the rounding of $r_6$.

**Non-example: $e_i/s$.** Dividing by $s$ alone ignores $1 - h_{ii}$. For point 6 it gives $-0.71$, which hides the point. Some software calls $e_i/s$ the standardized residual, so check the definition before reading a plot.

**Non-example: residuals of a robust fit.** For an M-estimator such as the [Huber M-estimator](/huber-m-estimator/), $e_i$ divided by a robust scale is a useful residual, but it has neither of the exact laws above.

**Naming.** The terms vary between books and programs. "Studentized" usually means $t_i$ (external) and "standardized" means $r_i$ (internal), but some texts call $r_i$ studentized. "Deleted residual" can mean $t_i$ or the unscaled $d_i = e_i/(1 - h_{ii})$.

## Related definitions

- **PRESS statistic.** $\sum_i d_i^2 = \sum_i e_i^2/(1 - h_{ii})^2$, the leave-one-out prediction error sum of squares; leave-one-out [cross-validation](/cross-validation/) for least squares is PRESS$/n$. For the example it is 52.85, against the in-sample $\mathrm{RSS} = 8.41$.
- **[Cook's distance](/cooks-distance/).** $D_i = \frac{r_i^2}{p}\frac{h_{ii}}{1 - h_{ii}}$, the internal residual times a leverage factor.
- **DFFITS.** $t_i\sqrt{h_{ii}/(1 - h_{ii})}$, the external residual times the same kind of factor.
- **[Q-Q plot](/q-q-plot/) of residuals.** Plotting the ordered $t_i$ against $t_{n-p-1}$ or normal quantiles checks the normality of the errors; the raw $e_i$ have unequal variances and are less suited.
- **Studentization.** Dividing a statistic by an estimate of its standard deviation, after Student, as in the [t-test](/student-t-test/). The residuals are "studentized" in the same sense.

## References
