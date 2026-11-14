---
tag: 9RNYDH
kind: definition
slug: akaike-information-criterion
name: Akaike information criterion
aliases:
- AIC
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: "AIC = -2 log L + 2k. It estimates how well a fitted model will predict new data from the same source. Lower is better, and only differences on the same data mean anything."
prereqs: [deviance-statistic, kullback-leibler-divergence, maximum-likelihood-estimation]
see_also: [bayesian-information-criterion, cross-validation, stepwise-regression, widely-applicable-information-criterion, minimum-description-length, overfitting, feature-selection, post-selection-inference]
sources:
  - paper: doi:10.1109/TAC.1974.1100705
    title: "Hirotugu Akaike, A new look at the statistical model identification, IEEE Transactions on Automatic Control 19(6), 1974, pp. 716 to 723"
    locator: The whole paper (the criterion -2 log L + 2k as the estimate of the expected log-likelihood of the fitted model, proposed for model order selection)
  - paper: doi:10.1007/978-1-4612-1694-0_15
    title: "Hirotugu Akaike, Information theory and an extension of the maximum likelihood principle, Second International Symposium on Information Theory, Akadémiai Kiadó, Budapest, 1973, pp. 267 to 281; reprinted in S. Kotz and N. L. Johnson (eds.), Breakthroughs in Statistics, Volume I, Springer, 1992, pp. 610 to 624"
    locator: The whole paper (the derivation of the bias k of the maximized log-likelihood from the expected Kullback-Leibler discrepancy)
  - paper: doi:10.1093/biomet/76.2.297
    title: "Clifford M. Hurvich and Chih-Ling Tsai, Regression and time series model selection in small samples, Biometrika 76(2), 1989, pp. 297 to 307"
    locator: The whole paper (the corrected criterion AICc and its exact unbiasedness in normal linear regression)
  - paper: doi:10.1093/biomet/68.1.45
    title: "Ritei Shibata, An optimal selection of regression variables, Biometrika 68(1), 1981, pp. 45 to 54"
    locator: The whole paper (asymptotic efficiency of AIC-type selection when the true regression has infinitely many terms)
  - paper: doi:10.1093/biomet/92.4.937
    title: "Yuhong Yang, Can the strengths of AIC and BIC be shared? A conflict between model identification and regression estimation, Biometrika 92(4), 2005, pp. 937 to 950"
    locator: The whole paper (no selection rule is both consistent and minimax-rate optimal for estimating the regression function)
  - paper: doi:10.1111/j.2517-6161.1977.tb01603.x
    title: "M. Stone, An asymptotic equivalence of choice of model by cross-validation and Akaike's criterion, Journal of the Royal Statistical Society, Series B 39(1), 1977, pp. 44 to 47"
    locator: The whole paper (leave-one-out cross-validation of the log-likelihood and AIC agree to first order)
  - book: isbn:9780521852258
    title: Gerda Claeskens and Nils Lid Hjort, Model Selection and Model Averaging, Cambridge University Press, 2008
    locator: Chapter 2 (the derivation of AIC, the Takeuchi criterion for misspecified models and AICc) and Chapter 4 (comparison of AIC and BIC, consistency and efficiency)
  - book: isbn:9780387953649
    title: "Kenneth P. Burnham and David R. Anderson, Model Selection and Multimodel Inference: A Practical Information-Theoretic Approach, second edition, Springer, 2002"
    locator: Chapter 2 (AIC, AICc and Akaike weights)
---

The Akaike information criterion of a model fitted by [maximum likelihood](/maximum-likelihood-estimation/) is $\mathrm{AIC} = -2\log L(\hat\theta) + 2k$, where $L(\hat\theta)$ is the maximized likelihood and $k$ is the number of estimated parameters. The maximized log-likelihood is a biased estimate of how well the fitted model will predict new data from the same source: the fit was tuned to the data it is scored on, and the bias is about $k$. AIC removes this bias. Among models fitted to the same data, the model with the smallest AIC has the best estimated fit to new data. AIC does not test a model, and its absolute value has no meaning; only differences between models on the same data do.

## Definition

Let $y = (y_1, \dots, y_n)$ be the data, and let a model be a family of densities $f(y; \theta)$ with $\theta$ in an open subset of $\mathbb R^k$. Let $\hat\theta$ be the maximum likelihood estimate and $l(\hat\theta) = \log f(y; \hat\theta)$. Then

$$\mathrm{AIC} = -2\,l(\hat\theta) + 2k.$$

The parameter count $k$ includes every estimated parameter, for example the variance of a normal model. For a normal linear regression with an $n \times p$ design matrix $X$ of rank $p$ whose columns include the intercept, coefficient vector $b$ and residual sum of squares RSS, the estimates are $\hat b$ and $\hat\sigma^2 = \mathrm{RSS}/n$, so $k = p + 1$ and

$$\mathrm{AIC} = n\log\frac{2\pi\,\mathrm{RSS}}{n} + n + 2(p + 1).$$

The **corrected criterion** of Hurvich and Tsai (1989) is

$$\mathrm{AICc} = \mathrm{AIC} + \frac{2k(k + 1)}{n - k - 1}, \qquad n > k + 1.$$

For a list of models $M_1, \dots, M_R$ with criteria $A_r$, let $\Delta_r = A_r - \min_s A_s$. The **Akaike weights** are $w_r = e^{-\Delta_r/2}/\sum_s e^{-\Delta_s/2}$.

**Facts.**

1. **What AIC estimates.** Let $y^*$ be a new sample of the same size, independent of $y$ and with the same law $g$, and let $T = \mathrm E_y\,\mathrm E_{y^*}\log f(y^*; \hat\theta(y))$ be the expected log-likelihood of new data under the fitted model. Then $-2T$ equals $-2\,\mathrm E_{y^*}\log g(y^*)$, which is the same for all models, plus twice the expected [Kullback-Leibler divergence](/kullback-leibler-divergence/) from the fitted model to $g$. So ranking models by $-2T$ ranks them by expected divergence. Under the conditions of [asymptotic normality of the MLE](/asymptotic-normality-of-mle/), and if $g$ is a member of the model, $\mathrm E[l(\hat\theta)] - T \to k$. Then $\mathrm{AIC}$ estimates $-2T$ with a bias that tends to 0. The next fact sketches why.
2. **Sketch of the bias $k$.** Let $\theta_0$ minimize the divergence from $f(\cdot; \theta)$ to $g$, let $J$ be minus the expected Hessian of $\log f$ for one observation at $\theta_0$, and let $K$ be the variance of the score of one observation at $\theta_0$. Expand $l(\theta_0)$ around $\hat\theta$, where the score is 0, and $\mathrm E_{y^*}\log f(y^*; \hat\theta)$ around $\theta_0$, where its gradient is 0. Each expansion loses $\frac{n}{2}(\hat\theta - \theta_0)^\top J(\hat\theta - \theta_0) + o_p(1)$. So $l(\hat\theta) - \mathrm E_{y^*}\log f(y^*; \hat\theta)$ equals $n(\hat\theta - \theta_0)^\top J(\hat\theta - \theta_0)$ plus a term with mean 0 plus $o_p(1)$. Since $\sqrt n(\hat\theta - \theta_0)$ tends to $N(0, J^{-1}KJ^{-1})$, the mean of the quadratic form tends to $\operatorname{tr}(KJ^{-1})$, if the expectations converge (uniform integrability is needed for that step). When $g$ is in the model, $K = J$ and the trace is $k$. Otherwise the penalty $2\operatorname{tr}(\hat K\hat J^{-1})$ gives Takeuchi's criterion TIC. Claeskens and Hjort (2008, Chapter 2) give the full conditions.
3. **Exact small-sample correction.** In normal linear regression where the candidate model contains the true mean, AICc is an exactly unbiased estimate of $-2T$ (Hurvich and Tsai 1989; cited here, not proved). AICc and AIC differ by $O(k^2/n)$, so they agree for large $n$, and AICc is the safer choice when $n/k$ is small.
4. **AIC overfits with a fixed probability.** For nested models that differ by $q$ parameters, AIC prefers the larger model exactly when the [likelihood ratio](/likelihood-ratio-test/) statistic $2(l_1 - l_0)$ exceeds $2q$. If the smaller model is true, [Wilks' theorem](/wilks-theorem/) gives, as $n \to \infty$, $P(\text{larger chosen}) \to P(\chi^2_q > 2q)$: 0.157, 0.135, 0.112, 0.075 and 0.029 for $q = 1, 2, 3, 5, 10$. This does not tend to 0 as $n$ grows, so AIC is not consistent for the true model. In regression, adding one column lowers AIC when $n\log(\mathrm{RSS}_0/\mathrm{RSS}_1) > 2$, which is about $|t| > \sqrt 2 = 1.414$ for the t statistic of the new coefficient.
5. **AIC is efficient for prediction.** If the true regression function is not in any candidate model (for example, it has infinitely many nonzero terms), Shibata (1981) showed that the model chosen by AIC has a prediction error that, as $n \to \infty$, is as small as that of the best candidate. This is cited, not proved here. Yang (2005) showed that no criterion can be both consistent, as [BIC](/bayesian-information-criterion/) is, and minimax-rate optimal for prediction, as AIC is.
6. **AIC and cross-validation.** Stone (1977) showed that AIC and leave-one-out [cross-validation](/cross-validation/) of the log-likelihood choose the same model to first order as $n \to \infty$. AIC needs one fit per model; cross-validation needs $n$, but does not need the model to contain $g$.
7. **Only differences matter.** A constant added to every $l$, such as the term $-\frac{n}{2}\log 2\pi$, does not change the choice, so programs that drop constants report different AIC values for the same models. Values from different programs must not be mixed.

## Examples and non-examples

**Polynomial degree.** Take $x = 1, 2, \dots, 10$ and $y = (3, 4, 6, 5, 7, 6, 6, 5, 3, 2)$, and fit polynomials of degree 0 to 4 by least squares with normal errors. Then $k$ is the degree plus 2:

| degree | RSS | $k$ | $-2l$ | AIC | AICc | $\Delta$ AIC | weight |
|---|---|---|---|---|---|---|---|
| 0 | 24.100 | 2 | 37.175 | 41.175 | 42.889 | 18.58 | 0.000 |
| 1 | 23.006 | 3 | 36.710 | 42.710 | 46.710 | 20.11 | 0.000 |
| 2 | 2.521 | 4 | 14.600 | 22.600 | 30.600 | 0 | 0.646 |
| 3 | 2.504 | 5 | 14.534 | 24.534 | 39.534 | 1.93 | 0.246 |
| 4 | 2.415 | 6 | 14.170 | 26.170 | 54.170 | 3.57 | 0.108 |

The RSS values are $241/10$, $3796/165$, $416/165$, $5372/2145$ and $1036/429$. RSS falls with each degree, so $-2l$ falls too. AIC is smallest at degree 2: a parabola captures the single peak of the data, and the higher degrees lower RSS too little to pay for their extra parameters. AIC gives degree 3 a weight of 0.246, so the data do not rule it out. AICc, with $n = 10$, punishes degrees 3 and 4 much harder.

**Many candidate columns.** Take 10 orthogonal candidate columns that are all noise, and a large $n$. The model with the smallest AIC keeps exactly the columns with $|t| > 1.414$ (approximately), and each one passes with probability near 0.157. So the search keeps at least one noise column with probability about $1 - 0.843^{10} = 0.82$. Fact 4 is about one comparison; a search over many models overfits more, and the AIC of the chosen model is too optimistic. See [stepwise regression](/stepwise-regression/) and [post-selection inference](/post-selection-inference/).

**Non-example: different responses.** A model for $y$ and a model for $\log y$ have likelihoods on different scales, and their AIC values cannot be compared. Adding the Jacobian term $-2\sum\log y_i$ to the AIC of the model for $\log y$ puts both on the scale of $y$, and then the comparison is valid.

**Non-example: different data.** If one model drops the rows with a missing value of $x_3$ and the other keeps them, the two log-likelihoods sum over different rows. Fit all candidates to the same rows.

**Non-example: REML likelihoods with different fixed effects.** The [restricted maximum likelihood](/restricted-maximum-likelihood/) criterion of a [linear mixed model](/linear-mixed-model/) is the likelihood of contrasts that depend on $X$, so two models with different fixed effects have likelihoods of different data. Compare them with ordinary maximum likelihood fits.

## Related definitions

- **[Bayesian information criterion](/bayesian-information-criterion/).** The penalty $k\log n$ in place of $2k$; it targets the true model, not prediction.
- **[Deviance](/deviance-statistic/).** For a fixed family, $-2l(\hat\theta)$ is the scaled deviance minus a term that depends only on the data, so AIC differences are deviance differences plus $2\Delta k$.
- **Mallows' $C_p$.** For normal regression with $\sigma^2$ estimated from the largest model, $C_p = \mathrm{RSS}_p/\hat\sigma^2 - n + 2p$. It equals AIC with known $\sigma^2$ up to a constant, so the two choose the same model to first order.
- **[Widely applicable information criterion](/widely-applicable-information-criterion/).** The Bayesian analogue, which replaces $l(\hat\theta)$ and $k$ by the posterior log predictive density and its variance, and stays valid for singular models.
- **[Minimum description length](/minimum-description-length/).** A coding view of model choice whose two-part code gives a $\frac{k}{2}\log n$ penalty, like BIC.
- **[Overfitting](/overfitting/).** AIC is one of the standard corrections for it.

## References
