---
tag: W9KZM4
kind: technique
slug: multiple-imputation
name: Multiple imputation
aliases:
- Rubin's rules
area: statistics-and-inference/point-estimation
level: core
summary: Fill in missing values several times from a predictive model, analyse each completed data set, and pool the results with Rubin's rules so the variance reflects the missingness.
prereqs: [t-confidence-interval, posterior-predictive-distribution, missing-data-mechanism]
see_also: [multiple-imputation-by-chained-equations, ignorability, expectation-maximization, bayesian-linear-regression, inverse-probability-weighting, gibbs-sampling, standard-error, bootstrap-method]
sources:
  - book: isbn:9780471087052
    title: Donald B. Rubin, Multiple Imputation for Nonresponse in Surveys, Wiley, 1987
    locator: Chapter 3 (the Bayesian derivation of the combining rules and the t reference distribution) and Chapter 4 (randomization-based evaluation, proper imputation)
  - paper: doi:10.1093/biomet/86.4.948
    title: John Barnard and Donald B. Rubin, Small-sample degrees of freedom with multiple imputation, Biometrika 86(4), 1999
    locator: pp. 948 to 955 (degrees of freedom that never exceed the complete-data degrees of freedom)
  - book: isbn:9780470526798
    title: Roderick J. A. Little and Donald B. Rubin, Statistical Analysis with Missing Data, third edition, Wiley, 2019
    locator: Chapter 10 (Bayes and multiple imputation)
  - book: isbn:9781138588318
    title: Stef van Buuren, Flexible Imputation of Missing Data, second edition, CRC Press, 2018
    locator: Chapter 2 (the pooling rules and the fraction of missing information) and Chapter 3 (Bayesian normal linear imputation)
---

Multiple imputation handles missing data in three steps. First, replace each missing value by a random draw from its predictive distribution given the observed data, and do this $m$ times to get $m$ completed data sets. Second, run the analysis you would run on complete data on each of them. Third, combine the $m$ estimates and their variances with Rubin's rules: the point estimate is the mean $\bar Q$, and the variance $T = W + (1 + 1/m)B$ adds the spread between the imputations to the mean variance within them. When the values are [missing at random](/missing-data-mechanism/) and the imputation model is correct and proper, $\bar Q$ is consistent and the interval $\bar Q \pm t_\nu\sqrt T$ has close to nominal coverage. A single imputation gives the same kind of point estimate but treats guesses as data, so its standard errors are too small.

## In plain words

Some values in your table are empty. You could guess each one from the rest of the data, but then you would treat the guesses as if you had measured them, and you would claim more certainty than you have.

Instead, make several guesses for each empty value, each a little different, in the way a real value could differ. This gives several complete tables. Analyse each table in the usual way. The answers will not agree exactly. Their average is your answer. How much they disagree tells you how much the empty values cost you, and you add that to the usual uncertainty.

This works when the reason a value is missing depends only on things you can see in the data, and when the guessing model fits the data well.

## When it applies

- The missingness is [ignorable](/ignorability/): missing at random given the variables in the imputation model, with distinct parameters. Under missing not at random, the imputation model must include a model for the mechanism, or the results are only a sensitivity analysis.
- There is a predictive model for the missing values given the observed ones, such as a normal linear regression, a logistic regression, or [chained equations](/multiple-imputation-by-chained-equations/) for many incomplete variables.
- The analysis of complete data gives an estimate $Q$ of a scalar and a variance $U$, with $(Q - \theta)/\sqrt U$ close to normal, as for means, regression coefficients and log odds ratios. Rubin's rules use only $Q$ and $U$.
- The imputation model includes every variable in the analysis, the outcome too, and any variable that predicts missingness.

## The template

```pseudo id=main
MULTIPLE-IMPUTATION(Y_obs, m)
L1  for j ← 1 to m do
L2      fit IMPUTATION-MODEL on the rows with y observed          ▷ hole: normal regression of y on x
L3      draw σ*² from its posterior                               ▷ proper: a draw, not the estimate
L4      draw β* from its posterior given σ*²
L5      each missing y_i ← x_i'β* + σ* z_i, z_i ~ N(0, 1)          ▷ observed values stay as they are
L6      (Q_j, U_j) ← ANALYSIS(completed data set j)               ▷ hole: the complete-data method
L7  Q̄ ← (1/m) Σ_j Q_j;  W ← (1/m) Σ_j U_j;  B ← (1/(m-1)) Σ_j (Q_j - Q̄)²
L8  T ← W + (1 + 1/m) B
L9  return Q̄ ± t_ν √T                                           ▷ hole: Rubin or Barnard-Rubin ν
```

The holes are the imputation model (lines L2 to L5), the analysis (line L6) and the degrees of freedom (line L9). For normal linear regression with the prior $p(\beta, \log\sigma) \propto 1$, fitted on $n_{\text{obs}}$ rows with $p$ predictors, line L3 draws $\sigma_*^2 = \text{RSS}/\chi^2_{n_{\text{obs}} - p}$ and line L4 draws $\beta_* \sim N(\hat\beta, \sigma_*^2(X_{\text{obs}}^{\mathsf T}X_{\text{obs}})^{-1})$. The imputed value then has the exact [posterior predictive distribution](/posterior-predictive-distribution/), a t law centered at $x_i^{\mathsf T}\hat\beta$.

**Why the draws must include the parameters.** If line L5 used $\hat\beta$ and $\hat\sigma$ in place of the draws, the imputations would show the noise around the fitted line but not the uncertainty of the line itself. $B$ would then be too small, and so would $T$. Rubin calls imputations that include this uncertainty proper.

**Where $T$ comes from.** Think of $\theta$ in a Bayesian way. Its posterior given the observed data is the mixture, over the missing values, of its posterior given the completed data. By the laws of total expectation and total variance,

$$\mathbb{E}[\theta \mid Y_{\text{obs}}] = \mathbb{E}\big[\mathbb{E}[\theta \mid Y_{\text{obs}}, Y_{\text{mis}}]\big], \qquad \operatorname{Var}[\theta \mid Y_{\text{obs}}] = \mathbb{E}\big[\operatorname{Var}[\theta \mid Y_{\text{obs}}, Y_{\text{mis}}]\big] + \operatorname{Var}\big[\mathbb{E}[\theta \mid Y_{\text{obs}}, Y_{\text{mis}}]\big].$$

With $Q_j$ and $U_j$ as the completed-data posterior mean and variance, $\bar Q$ and $W$ estimate the first terms and $B$ estimates the last one. The factor $1 + 1/m$ accounts for estimating $\mathbb{E}[\theta \mid Y_{\text{obs}}]$ by a mean of only $m$ draws: $\operatorname{Var}\bar Q = B_\infty/m$. These two identities are proved. The t reference law in line L9 is an approximation that Rubin (1987) derived for finite $m$ and large complete-data samples; its accuracy is measured, not proved.

**Degrees of freedom.** With $r = (1 + 1/m)B/W$, the relative increase in variance, and $\lambda = (1 + 1/m)B/T$, Rubin's degrees of freedom are

$$\nu_m = (m - 1)\left(1 + \frac1r\right)^2 = \frac{m - 1}{\lambda^2}.$$

When $B$ is small, $\nu_m$ is very large, even if the complete-data analysis has only a few degrees of freedom $\nu_{\text{com}}$. Barnard and Rubin (1999) use

$$\nu = \left(\frac1{\nu_m} + \frac1{\hat\nu_{\text{obs}}}\right)^{-1}, \qquad \hat\nu_{\text{obs}} = \frac{\nu_{\text{com}} + 1}{\nu_{\text{com}} + 3}\,\nu_{\text{com}}(1 - \lambda),$$

which never exceeds $\nu_m$ or $\nu_{\text{com}}$ and tends to $\nu_m$ as $\nu_{\text{com}} \to \infty$. When $B = 0$, $\nu_m = \infty$ and the normal quantile is used.

## Classic examples

**Rubin's rules by hand.** Take $m = 3$ estimates $Q = (1, 2, 3)$, each with $U = 1/2$. Then $\bar Q = 2$, $W = 1/2$, $B = 1$, $T = 1/2 + (4/3)(1) = 11/6$, $r = 8/3$, $\lambda = 8/11$ and $\nu_m = 2(11/8)^2 = 121/32 \approx 3.78$. The 95% interval is $2 \pm 2.841\sqrt{11/6} = (-1.85, 5.85)$. Most of the variance here comes from the disagreement of the imputations.

**A mean with MAR outcome.** Take $x = 1, \ldots, 12$ and $y = 2.1, 3.0, 3.8, ?, 6.2, 6.9, ?, 9.1, ?, 11.8, ?, 14.2$, where $y$ is missing at $x = 4, 7, 9, 11$. The analysis is the mean of $y$ with $U = S^2/n$ (divisor $n - 1$ in $S^2$). The complete-case mean is $7.138$; it is too low because the missing values lie mostly at large $x$. Normal regression imputation with $m = 5$ (seed 1) gave the means $7.644$, $7.854$, $7.918$, $7.895$ and $7.866$, so $\bar Q = 7.835$, $W = 1.318$, $B = 0.0121$ and $T = 1.332$. Rubin's $\nu_m$ is about 33800, but the complete-data analysis has $\nu_{\text{com}} = 11$, and the Barnard-Rubin value is $9.32$. The 95% interval is $(5.24, 10.43)$.

**Coverage under MAR, measured.** With $x \sim N(0, 1)$, $y = 1 + 2x + e$, $e \sim N(0, 1)$, $n = 200$, and $y$ missing with probability $1/(1 + e^{0.5 - 1.5x})$ (about 41% missing), the target is $\mathbb{E}y = 1$. Over 1000 data sets, nominal 95%:

| Method | coverage | mean bias | mean width |
|---|---|---|---|
| complete cases | 0.005 | $-0.876$ | 0.718 |
| single regression imputation | 0.905 | 0.001 | 0.592 |
| multiple imputation, $m = 2$ | 0.949 | 0.000 | 0.822 |
| multiple imputation, $m = 5$ | 0.952 | 0.001 | 0.714 |
| multiple imputation, $m = 20$ | 0.957 | 0.001 | 0.695 |

Single imputation removes the bias but its interval is too narrow. Multiple imputation keeps the bias away and restores the coverage; a larger $m$ makes the interval shorter.

**Regression with incomplete covariates.** For a regression with several incomplete covariates, imputation by [chained equations](/multiple-imputation-by-chained-equations/) fills in all of them, and Rubin's rules pool each coefficient. The outcome must be in the imputation model of each covariate, or the coefficients are biased toward zero.

## Variations

- **Several parameters at once.** For a vector $Q$ with covariance $U$, $\bar Q$ and $T$ have the same form with $B$ a matrix. Tests of several coefficients use an F reference law with a pooled $r$, because $B$ is poorly estimated for small $m$.
- **Joint models.** Draw all missing values together from one multivariate model, such as a multivariate normal fitted by data augmentation, which is a [Gibbs sampler](/gibbs-sampling/) on parameters and missing values.
- **Predictive mean matching.** Replace the draw of line L5 by the observed value of a donor whose predicted mean is close. The imputations are always values that occur in the data.
- **Other analysis-side methods.** [Expectation-maximization](/expectation-maximization/) gives the maximum likelihood estimate under MAR without imputation, and [inverse probability weighting](/inverse-probability-weighting/) reweights the complete cases. Both need the variance to be computed in another way, such as by the [bootstrap](/bootstrap-method/).

## Pitfalls

- **Imputing without the outcome.** If the outcome is left out of the model for an incomplete covariate, the imputed covariate is unrelated to the outcome, and its coefficient is biased toward zero.
- **Improper imputation.** Drawing from the fitted model at $\hat\beta$, $\hat\sigma$ gives intervals that are too narrow, the more so when many values are missing.
- **Uncongenial models.** If the imputation model assumes less than the analysis, such as no interaction where the analysis has one, the pooled estimate is biased for that term. If it assumes more and is right, $T$ can be too large.
- **Too few imputations.** Rubin's efficiency of $\bar Q$ with $m$ imputations relative to $m = \infty$ is $(1 + \gamma/m)^{-1}$, with $\gamma$ the fraction of missing information: 0.943 for $\gamma = 0.3$, $m = 5$. This is about the point estimate. Standard errors, p values and their reproducibility need more, often $m$ at least the percentage of incomplete cases.
- **Pooling the wrong quantity.** Apply Rubin's rules to quantities that are close to normal: pool log odds ratios, not odds ratios, and Fisher-transformed correlations, not correlations. Do not average p values or test statistics.
- **MNAR data.** No imputation model fitted to the observed data can find a dependence of missingness on the missing values themselves. Vary the imputation model, for example by shifting the imputed values, and report how much the answer moves.

## Exercises

1. Show that when all $m$ imputations are equal, $T = W$ and the method reduces to the analysis of one completed data set.
   *Answer.* Equal data sets give equal $Q_j$, so $B = 0$ and $T = W + 0 = W$, the common $U_j$.
2. Given $Q = (4.1, 4.4, 3.9, 4.3, 4.3)$ and $U_j = 0.04$ for all $j$, compute $\bar Q$, $B$, $T$ and $\nu_m$.
   *Answer.* $\bar Q = 4.2$; the deviations are $-0.1, 0.2, -0.3, 0.1, 0.1$, so $B = 0.16/4 = 0.04$. Then $T = 0.04 + 1.2 \cdot 0.04 = 0.088$, $r = 1.2$, and $\nu_m = 4(1 + 1/1.2)^2 = 4(11/6)^2 = 13.44$.
3. Prove that the Barnard-Rubin $\nu$ is at most $\min(\nu_m, \nu_{\text{com}})$.
   *Answer.* $\nu^{-1} = \nu_m^{-1} + \hat\nu_{\text{obs}}^{-1}$ is larger than each term, so $\nu < \nu_m$ and $\nu < \hat\nu_{\text{obs}}$. And $\hat\nu_{\text{obs}} \le \nu_{\text{com}}$ since $(\nu_{\text{com}} + 1)/(\nu_{\text{com}} + 3) < 1$ and $1 - \lambda \le 1$.
4. Explain why imputing the conditional mean $x_i^{\mathsf T}\hat\beta$ for a missing outcome gives an unbiased estimate of $\mathbb{E}y$ under MAR on $x$ but a wrong estimate of $\operatorname{Var}y$.
   *Answer.* The regression line is correct under MAR on $x$, so the mean of the predictions estimates $\mathbb{E}[\mathbb{E}(y \mid x)] = \mathbb{E}y$. But each imputed value has no residual, so the completed data have variance that misses $\sigma^2$ for the imputed fraction, and $\operatorname{Var}y$ is too small.
5. With $\gamma = 0.5$, how many imputations make the efficiency at least 0.99?
   *Answer.* $(1 + 0.5/m)^{-1} \ge 0.99$ means $0.5/m \le 1/99$, so $m \ge 49.5$, and $m = 50$.

## References
