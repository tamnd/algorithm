---
tag: T508RZ
kind: algorithm
slug: augmented-inverse-probability-weighting
name: Augmented inverse probability weighting
aliases:
- AIPW
- doubly robust estimator
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Combines an outcome regression with inverse probability weighting of its residuals. It is consistent if either model is right and efficient if both are.
model: real-ram
complexity:
  vars: {n: "the number of units"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, single_pass: true, doubly_robust: true, needs_positivity: true, unbiased_with_one_correct_fixed_model: true, stays_in_outcome_range: false}
history:
  year: 1994
  people: [James M. Robins, Andrea Rotnitzky, Lue Ping Zhao]
  note: Robins, Rotnitzky and Zhao added an outcome-model term to inverse probability weighted estimating equations in 1994. Scharfstein, Rotnitzky and Robins pointed out the double robustness in 1999, and Hahn derived the efficiency bound that the estimator reaches in 1998.
prereqs: [inverse-probability-weighting, average-treatment-effect, m-estimator]
see_also: [targeted-maximum-likelihood-estimation, double-machine-learning, influence-function, propensity-score, rosenbaum-sensitivity-analysis, off-policy-evaluation, missing-data-mechanism, monte-carlo-integration]
sources:
  - paper: doi:10.1080/01621459.1994.10476818
    title: James M. Robins, Andrea Rotnitzky and Lue Ping Zhao, Estimation of regression coefficients when some regressors are not always observed, Journal of the American Statistical Association 89(427), 1994
    locator: pp. 846 to 866 (augmented inverse probability weighted estimating equations and the efficient member of the class)
  - paper: doi:10.2307/2998560
    title: Jinyong Hahn, On the role of the propensity score in efficient semiparametric estimation of average treatment effects, Econometrica 66(2), 1998
    locator: pp. 315 to 331 (the semiparametric efficiency bound for the ATE)
  - paper: doi:10.1080/01621459.1999.10473862
    title: Daniel O. Scharfstein, Andrea Rotnitzky and James M. Robins, Adjusting for nonignorable drop-out using semiparametric nonresponse models, Journal of the American Statistical Association 94(448), 1999
    locator: pp. 1096 to 1120, with the discussion and rejoinder in the same issue (the augmented estimator is consistent if either working model is right)
  - paper: doi:10.1111/j.1541-0420.2005.00377.x
    title: Heejung Bang and James M. Robins, Doubly robust estimation in missing data and causal inference models, Biometrics 61(4), 2005
    locator: pp. 962 to 973 (doubly robust estimators, including the regression on a clever covariate)
  - paper: doi:10.1214/07-STS227
    title: Joseph D. Y. Kang and Joseph L. Schafer, Demystifying double robustness, a comparison of alternative strategies for estimating a population mean from incomplete data, Statistical Science 22(4), 2007
    locator: pp. 523 to 539 (simulations in which both working models are slightly wrong and the propensities are near 0)
  - book: isbn:9780387324487
    title: Anastasios A. Tsiatis, Semiparametric Theory and Missing Data, Springer, 2006
    locator: Chapter 9 (augmented inverse probability weighted complete-case estimators) and Chapter 13 (the double-robust estimator of the average causal treatment effect, pp. 323 to 337)
---

Augmented inverse probability weighting (AIPW) estimates the [average treatment effect](/average-treatment-effect/) $\tau = \mathbb{E}[Y(1) - Y(0)]$ with two working models: a model $\tilde e(x)$ of the [propensity score](/propensity-score/) and models $m_1(x)$ and $m_0(x)$ of the mean outcome in each arm. It predicts both potential outcomes for every unit with the outcome models, and then corrects the predictions with the [inverse probability weighted](/inverse-probability-weighting/) residuals of the units that were actually observed in each arm. The estimate has mean $\tau$ when either the propensity model or the outcome models are right, which is why it is called doubly robust. When both are right, its variance reaches the smallest value that any regular estimator of the ATE can have. With the working models fitted, the estimate takes one pass over the data.

## In plain words

There are two common ways to adjust for differences between treated and untreated groups. One is to model how the outcome depends on the measured traits, and to predict for every person the outcome with and without treatment. The other is to weight people by one over their chance of getting the treatment they got. Each method fails if its model is wrong.

AIPW uses both. It starts from the predictions, then looks at how far off the predictions were for the people we actually saw in each group, and adds back those errors with the weights. If the predictions are good, the errors average out to nothing and the weights do not matter. If the weights are right, they fix whatever the predictions got wrong. Only when both are wrong does the estimate go wrong.

## The problem

The two parts of the problem are kept apart: what the data can identify, and how to estimate it.

**Identification.** This is the same as for [IPW](/inverse-probability-weighting/). Each unit has [potential outcomes](/potential-outcomes-framework/) $Y(1)$ and $Y(0)$, a treatment $T \in \{0, 1\}$ and covariates $X$ measured before treatment, and the units are independent draws from one distribution. The estimand is $\tau = \mathbb{E}[Y(1) - Y(0)]$. The assumptions are consistency with [SUTVA](/sutva/) ($Y = TY(1) + (1 - T)Y(0)$, no interference, no hidden versions of treatment), [ignorability](/ignorability/) $(Y(0), Y(1)) \perp T \mid X$, and positivity $0 < e(X) < 1$. With $e(x) = \Pr[T = 1 \mid X = x]$ and $\mu_t(x) = \mathbb{E}[Y \mid T = t, X = x]$, there are two identification formulas,

$$\tau = \mathbb{E}\big[\mu_1(X) - \mu_0(X)\big] = \mathbb{E}\left[\frac{TY}{e(X)} - \frac{(1 - T)Y}{1 - e(X)}\right],$$

the first by standardization (the g-formula) and the second by weighting. AIPW uses a third formula that combines them:

$$\tau = \mathbb{E}\left[\mu_1(X) - \mu_0(X) + \frac{T(Y - \mu_1(X))}{e(X)} - \frac{(1 - T)(Y - \mu_0(X))}{1 - e(X)}\right].$$

The added terms have mean 0 because a residual has mean 0 within each arm and stratum. Positivity can be checked in part from the estimated propensities. Ignorability and SUTVA cannot be checked from the observed data.

**Estimation.** The input is $n$ units with $(T_i, Y_i)$ and three numbers from the working models: $\tilde e_i = \tilde e(X_i) \in (0, 1)$, $m_{1i} = m_1(X_i)$ and $m_{0i} = m_0(X_i)$. A usual choice fits $\tilde e$ by [logistic regression](/logistic-regression/) of $T$ on features of $X$, and fits $m_t$ by [least squares](/ordinary-least-squares/) of $Y$ on features of $X$ among the units with $T = t$. The output is the estimate

$$\hat\tau = \frac1n\sum_{i=1}^n \psi_i, \qquad \psi_i = m_{1i} - m_{0i} + \frac{T_i(Y_i - m_{1i})}{\tilde e_i} - \frac{(1 - T_i)(Y_i - m_{0i})}{1 - \tilde e_i},$$

its two parts $\hat\mu_1$ and $\hat\mu_0$ (estimates of $\mathbb{E}[Y(1)]$ and $\mathbb{E}[Y(0)]$), and a standard error. With $m_1 = m_0 = 0$ the estimate is the Horvitz-Thompson form of IPW. Without the two residual terms it is the regression (standardization) estimate.

## The algorithm

```pseudo id=main
AIPW-ATE(T, Y, ẽ, m1, m0)                      ▷ n units; needs 0 < ẽ_i < 1
L1  s1 ← 0;  s0 ← 0
L2  for i ← 1 to n do
L3      if ẽ_i ≤ 0 or ẽ_i ≥ 1 then error "positivity fails"
L4      if T_i = 1 then s1 ← s1 + m1_i + (Y_i - m1_i) / ẽ_i;  s0 ← s0 + m0_i
L5      else s1 ← s1 + m1_i;  s0 ← s0 + m0_i + (Y_i - m0_i) / (1 - ẽ_i)
L6  μ1 ← s1 / n;  μ0 ← s0 / n
L7  return (μ1 - μ0, μ1, μ0)
```

Every unit adds its predicted outcome under both treatments. Line L4 corrects the treated prediction with the weighted residual of a treated unit, and line L5 corrects the control prediction with the weighted residual of a control. A unit gives no residual for the arm it was not in; the weights make up for the missing residuals, as in IPW. Line L3 stops on a propensity of 0 or 1.

**Fitting the working models.** The reference code fits $\tilde e$ by Newton-Raphson on the logistic log-likelihood and stops when the largest coefficient step is below $10^{-10}$, and raises an error after 50 steps. If the treatment is perfectly separated by the features, the maximum likelihood estimate does not exist and the fitted propensities go to 0 or 1; this is a positivity failure in the model, and line L3 then stops the estimate. The outcome fits solve the normal equations, which is adequate for a few well scaled features; use a QR solve for an ill conditioned design.

**Variance.** If both working models are right, $\sqrt n(\hat\tau - \tau)$ is asymptotically normal with variance $V = \mathbb{E}[(\psi - \tau)^2]$, and fitting the models adds nothing to $V$ in the limit (Robins, Rotnitzky and Zhao 1994; Tsiatis 2006). The plug-in estimate is

$$v = \frac{S_\psi^2}{n}, \qquad S_\psi^2 = \frac{1}{n - 1}\sum_{i=1}^n (\psi_i - \hat\tau)^2,$$

with divisor $n - 1$, and $\hat\tau \pm z_{1 - \alpha/2}\sqrt v$ is a normal [confidence interval](/confidence-interval/) of approximate level $1 - \alpha$. If one model is wrong, $\hat\tau$ stays consistent but $v$ is not always right; a sandwich variance of the joint [M-estimator](/m-estimator/) that stacks the model fits and $\psi$, or the [bootstrap](/bootstrap-method/) of the whole procedure, takes the model fits into account.

## Example

The eight patients of the [IPW page](/inverse-probability-weighting/) have a stratum $x$ (0 mild, 1 severe), and the design treated mild patients with probability $1/4$ and severe patients with probability $3/4$.

| unit | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $x$ | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| $T$ | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 |
| $Y$ | 8 | 7 | 6 | 5 | 7 | 4 | 3 | 1 |
| design $e$ | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 3/4 | 3/4 | 3/4 |

Take a poor outcome model that ignores $x$: $m_1 = 11/2$ (the treated mean) and $m_0 = 19/4$ (the control mean), with the design propensities. Line L4 gives the treated units the terms $\tfrac{11}2 + 4(8 - \tfrac{11}2) = \tfrac{31}2$, $\tfrac{11}2 + 4(7 - \tfrac{11}2) = \tfrac{23}2$, $\tfrac{11}2 + \tfrac43(4 - \tfrac{11}2) = \tfrac72$ and $\tfrac{11}2 + \tfrac43(3 - \tfrac{11}2) = \tfrac{13}6$ in $s_1$, and line L5 adds $11/2$ for each of the four controls, so $s_1 = 164/3$ and $\hat\mu_1 = 41/6$. In the same way $s_0 = 4 \cdot \tfrac{19}4 + (\tfrac{19}4 + \tfrac53) + (\tfrac{19}4 + \tfrac13) + (\tfrac{19}4 + 3) + (\tfrac{19}4 - 15) = 28$ and $\hat\mu_0 = 7/2$. So $\hat\tau = 41/6 - 7/2 = 10/3$.

The table puts this next to the other choices of the working models. The stratified estimate, $\tfrac58(7.5 - 6) + \tfrac38(3.5 - 1) = 15/8$, is the reference.

| propensity | outcome models | $\hat\tau$ |
|---|---|---|
| design $e$ | $m = 0$ (pure IPW, Horvitz-Thompson) | $31/6$ |
| design $e$ | arm means, ignore $x$ | $10/3$ |
| design $e$ | cell means $m_1 = (7.5, 3.5)$, $m_0 = (6, 1)$ | $15/8$ |
| $1/2$ for all, ignores $x$ | arm means, ignore $x$ | $3/4$ (the naive difference) |
| $1/2$ for all, ignores $x$ | cell means | $15/8$ |
| empirical $2/5$ and $2/3$ | arm means, ignore $x$ | $15/8$ |
| empirical $2/5$ and $2/3$ | $m = 0$ | $15/8$ |

With the cell means, the residuals add to zero within each cell, and the propensities no longer matter. With the empirical propensities, the weights fix any outcome model. Only when both models ignore $x$ does the estimate fall back to the naive $3/4$. The proofs show that both exact agreements with $15/8$ hold for every discrete covariate. The design propensities are the true ones, but the sample is small, so with a poor outcome model the estimate is $10/3$, not $15/8$: double robustness is a statement about the mean, not about each sample.

**The same effect in the population.** Let $\Pr[X = 1] = 1/2$, $e(0) = 1/4$, $e(1) = 3/4$, $\mu_1(0) = 7$, $\mu_0(0) = 6$, $\mu_1(1) = 4$ and $\mu_0(1) = 1$, so $\tau = \tfrac12 \cdot 1 + \tfrac12 \cdot 3 = 2$. With $m = 0$ and the wrong propensity $\tilde e = 1/2$, the bias formula of the proofs gives $\mathbb{E}[\psi] - \tau = -\tfrac34 - \tfrac54 = -2$, so $\mathbb{E}[\psi] = 0$. Make either model right and the bias is exactly 0.

## Correctness

The proofs establish, in exact arithmetic:

- the loop computes the mean of the $\psi_i$;
- the *bias identity*: for fixed working models, $\mathbb{E}[\psi] - \tau = \mathbb{E}[(e/\tilde e - 1)(\mu_1 - m_1)] - \mathbb{E}[((1 - e)/(1 - \tilde e) - 1)(\mu_0 - m_0)]$, so the mean is $\tau$ if $\tilde e = e$ or $m_t = \mu_t$ (double robustness), and the bias is bounded by the product of the propensity error and the outcome error;
- *consistency* with estimated working models that converge uniformly to limits, if one of the limits is right;
- with a discrete $X$, the empirical propensities or the cell means each give the stratified estimate exactly.

The asymptotic normality, the consistency of $v$ when both models are right, and the efficiency of AIPW are cited, not proved (Robins, Rotnitzky and Zhao 1994; Hahn 1998; Tsiatis 2006, Chapter 13). The simulation numbers below are measured.

## Complexity

Given the working models, the loop does a constant number of arithmetic operations per unit, so the estimate takes $\Theta(n)$ time in the best and the worst case and $\Theta(1)$ extra space, and it can run on a stream. The scores $\psi_i$ for $v$ need a second pass, or running sums of $\psi_i$ and $\psi_i^2$. The model fits usually cost more: with $p$ propensity features and $q$ outcome features, the Newton-Raphson fit costs $O(n p^2 + p^3)$ per step and the two least squares fits $O(n q^2 + q^3)$.

## Properties

- **Doubly robust.** For fixed working models, the mean of $\psi$ is $\tau$ if either the propensity model or both outcome models are right. A simulation shows it: $X$ uniform on $[0, 1]$, $e(x) = \operatorname{expit}(-2 + 4x)$, $Y = x + 2x^2 + T(1 + x) + \varepsilon$ with standard normal $\varepsilon$, true ATE 1.5, $n = 1000$, 200 samples (seed 2026). The right outcome model uses $1, x, x^2$ in each arm, the wrong one a constant; the right propensity model is logistic in $1, x$, the wrong one a constant.

| working models | mean of $\hat\tau$ | SD | 95% coverage |
|---|---|---|---|
| both right | 1.506 | 0.073 | 0.955 |
| outcome wrong | 1.505 | 0.079 | 1.000 |
| propensity wrong | 1.507 | 0.073 | 0.920 |
| both wrong | 2.490 | 0.084 | 0.000 |
| IPW alone, right propensity | 1.511 | 0.087 | |

With both models wrong, AIPW is the naive difference of means, 2.49. These numbers are measured, not proved.

- **Product bias.** The bias is at most a constant times the product of the propensity error and the outcome error. Two models that are each a little wrong give a bias of second order.
- **Efficient when both are right.** With the true $e$ and $\mu_t$, the variance $\mathbb{E}[(\psi - \tau)^2]$ equals Hahn's (1998) bound $\mathbb{E}\big[\sigma_1^2(X)/e(X) + \sigma_0^2(X)/(1 - e(X)) + (\mu_1(X) - \mu_0(X) - \tau)^2\big]$, where $\sigma_t^2(x) = \operatorname{Var}[Y(t) \mid X = x]$. The function $\psi - \tau$ is the efficient [influence function](/influence-function/) of the ATE. In the table, AIPW with both models right has a smaller SD than IPW with the right propensity.
- **Not in range.** Like the Horvitz-Thompson form, $\hat\mu_1$ is not an average of the observed outcomes and can fall outside their range, for a binary outcome even outside $[0, 1]$. [TMLE](/targeted-maximum-likelihood-estimation/) fixes this.
- **Randomized experiments.** If $\tilde e$ is the known assignment probability, $\hat\tau$ is unbiased for every fixed outcome model, and a good outcome model only lowers the variance. This is regression adjustment for experiments, as in [CUPED](/cuped/).

## Variants and improvements

- **Normalized weights.** Dividing each residual sum by the sum of its weights (the Hájek form of the correction) keeps the estimate more stable when some weights are large.
- **Regression on a clever covariate.** Bang and Robins (2005) obtain a doubly robust estimate by adding $T/\tilde e(X)$ and $(1 - T)/(1 - \tilde e(X))$ as covariates to the outcome regression and then standardizing. [TMLE](/targeted-maximum-likelihood-estimation/) is a general form of this idea that keeps the estimate in the range of the outcome.
- **Cross-fitting.** Fit the working models on other folds of the data than the ones where $\psi_i$ is computed. This is [double machine learning](/double-machine-learning/), and it allows flexible learners such as [random forests](/random-forest/) and [gradient boosting](/gradient-boosting/) for the nuisances.
- **Effect on the treated.** The ATT version uses the score $\big(T(Y - m_0(X)) - (1 - T)\,\tilde e(X)(Y - m_0(X))/(1 - \tilde e(X))\big)/\Pr[T = 1]$ and needs only an outcome model for the controls.
- **Missing data and policies.** The same form estimates a mean from data missing at random (see [missing-data mechanisms](/missing-data-mechanism/)), which was the first use, and the value of a new policy from logged actions ([off-policy evaluation](/off-policy-evaluation/)). In [Monte Carlo integration](/monte-carlo-integration/) terms, the outcome model is a control variate for the weighted estimate.

## When to use it

Use AIPW in an observational study when [ignorability](/ignorability/) given the measured $X$ is credible and you can fit both a propensity model and an outcome model. It is a good default over IPW alone or regression alone, because one of the models may be wrong and you do not know which. In a randomized experiment it adds precision without risk to the bias. Check overlap first: if many estimated propensities are near 0 or 1, the residual weights are large, and trimming or the ATT is a better target. Pair it with a [sensitivity analysis](/rosenbaum-sensitivity-analysis/), since no method that uses only $X$ can fix an unmeasured confounder.

## Pitfalls

- **Both models a little wrong.** Double robustness gives no guarantee when both models are wrong. Kang and Schafer (2007) built a simulation in which both models are only slightly wrong and some propensities are near 0, and AIPW was worse than the outcome regression alone. Check the weights and the balance of $X$.
- **Weights near the positivity limit.** The residual terms carry the weights $1/\tilde e$ and $1/(1 - \tilde e)$. A unit with $\tilde e = 0.01$ and a residual of 5 moves $\hat\mu_1$ by $500/n$.
- **Overfitted working models on the same data.** Flexible learners fitted and evaluated on the same units can make the residuals too small and bias the estimate. Use cross-fitting.
- **Treating the plug-in variance as exact.** With one wrong model, $v$ was conservative in one simulation case above (coverage 1.000) and too small in the other (0.920). Use a sandwich variance or the bootstrap when you doubt a model.
- **A model of the wrong thing.** The outcome models must be fitted separately in each arm, or with treatment interactions; a model with a common slope in $X$ for both arms is wrong when the effect varies with $X$.
- **Calling it unconfounded.** Double robustness is about two models of observed data. It does not protect against an unmeasured confounder or against a covariate measured after treatment.

## Implementations

## History

Robins, Rotnitzky and Zhao (1994) studied regression with covariates that are missing for some units, and showed that every regular estimator is, in the limit, an inverse probability weighted estimating equation plus an augmentation term; the best augmentation is the conditional mean of the missing part, which gives the form used here. Scharfstein, Rotnitzky and Robins (1999) pointed out that the augmented estimator stays consistent if either the missingness model or the outcome model is right, and the name "doubly robust" followed. Hahn (1998) derived the efficiency bound for the ATE. Bang and Robins (2005) wrote the doubly robust estimators for missing data and causal inference in a common form. Kang and Schafer (2007) showed by simulation that the property gives no protection when both models are wrong and the weights are large, which led to a long discussion and to the targeted and cross-fitted versions of the method. Tsiatis (2006) gives the theory in a textbook.

## References
