---
tag: AN6TYE
kind: algorithm
slug: double-machine-learning
name: Double machine learning
aliases:
- DML
- debiased machine learning
area: statistics-and-inference/causal-inference-and-experimental-design
level: research
summary: Estimates a causal parameter with machine learning for the nuisance functions, using orthogonal scores and cross-fitting so that the parameter is root-n consistent.
model: real-ram
complexity:
  vars: {n: "the number of units", k: "the number of folds", C: "the cost of fitting one learner on at most n units and predicting"}
  time: {worst: "Θ(n + k C)", best: "Θ(n + k C)"}
  space: {extra: Θ(n)}
properties: {deterministic_given_folds: true, cross_fitted: true, neyman_orthogonal_score: true, doubly_robust_ate_score: true, needs_positivity: true}
history:
  year: 2018
  people: [Victor Chernozhukov, Denis Chetverikov, Mert Demirer, Esther Duflo, Christian Hansen, Whitney Newey, James Robins]
  note: Chernozhukov and coauthors combined Neyman orthogonal scores with cross-fitting in 2018, building on Robinson's 1988 residual-on-residual estimator and on the post-double-selection method of Belloni, Chernozhukov and Hansen (2014).
prereqs: [augmented-inverse-probability-weighting, m-estimator, influence-function]
see_also: [targeted-maximum-likelihood-estimation, cross-validation, lasso-regression, random-forest, gradient-boosting, ordinary-least-squares, average-treatment-effect, propensity-score]
sources:
  - paper: doi:10.1111/ectj.12097
    title: Victor Chernozhukov, Denis Chetverikov, Mert Demirer, Esther Duflo, Christian Hansen, Whitney Newey and James Robins, Double/debiased machine learning for treatment and structural parameters, The Econometrics Journal 21(1), 2018
    locator: pp. C1 to C68 (Neyman orthogonal scores, cross-fitting, the DML1 and DML2 estimators, the partially linear model and the ATE)
  - paper: doi:10.2307/1912705
    title: P. M. Robinson, Root-N-consistent semiparametric regression, Econometrica 56(4), 1988
    locator: pp. 931 to 954 (the coefficient of the partially linear model from residuals of Y and T on X)
  - paper: doi:10.1093/restud/rdt044
    title: Alexandre Belloni, Victor Chernozhukov and Christian Hansen, Inference on treatment effects after selection among high-dimensional controls, The Review of Economic Studies 81(2), 2014
    locator: pp. 608 to 650 (post-double-selection with the lasso, a forerunner of the orthogonal approach)
  - paper: doi:10.1080/01621459.1994.10476818
    title: James M. Robins, Andrea Rotnitzky and Lue Ping Zhao, Estimation of regression coefficients when some regressors are not always observed, Journal of the American Statistical Association 89(427), 1994
    locator: pp. 846 to 866 (the augmented estimating function used as the ATE score)
  - paper: doi:10.2307/2998560
    title: Jinyong Hahn, On the role of the propensity score in efficient semiparametric estimation of average treatment effects, Econometrica 66(2), 1998
    locator: pp. 315 to 331 (the efficiency bound reached by the ATE score)
---

Double machine learning (DML) estimates a low-dimensional causal parameter, such as the [average treatment effect](/average-treatment-effect/) or the coefficient of a treatment in a partially linear model, when the nuisance functions (the [propensity score](/propensity-score/), the outcome regressions) are fitted by flexible learners such as the [lasso](/lasso-regression/), [random forests](/random-forest/) or [gradient boosting](/gradient-boosting/). Two ideas make this work. The estimate solves a *Neyman orthogonal* score, whose mean does not move to first order when the nuisances are slightly wrong, so the learners' bias enters only as a product of two errors. And the nuisances for each unit are fitted on the other folds of the data (*cross-fitting*), so the unit's own noise cannot leak into its own prediction. Under rate conditions that many learners meet, the estimate is $\sqrt n$-consistent and asymptotically normal, with an ordinary confidence interval.

## In plain words

Machine learning models predict well, but they are biased on purpose: they trade bias for less noise. If you plug their predictions straight into an effect estimate, that bias goes straight into the answer, and the usual confidence interval is wrong.

DML does two things. First, it uses an estimating formula built so that errors in the predictions cancel to first order. With two separate predictions, one for the treatment and one for the outcome, only the product of their errors is left, and a product of two small numbers is very small. Second, it splits the data into parts. The predictions for each part come from models trained on the other parts, so no person's own outcome is used to make that person's prediction. Then it pools the answers.

## The problem

**Identification.** For the ATE: [potential outcomes](/potential-outcomes-framework/) $Y(1), Y(0)$, treatment $T \in \{0, 1\}$, covariates $X$, and the estimand $\tau = \mathbb{E}[Y(1) - Y(0)]$. Under consistency with [SUTVA](/sutva/), [ignorability](/ignorability/) and positivity, $\tau = \mathbb{E}[\psi(W; \eta_0)]$ with the AIPW score

$$\psi(W; \eta) = m_1(X) - m_0(X) + \frac{T(Y - m_1(X))}{e(X)} - \frac{(1 - T)(Y - m_0(X))}{1 - e(X)},$$

evaluated at the true nuisances $\eta_0 = (e, \mu_1, \mu_0)$, as on the [AIPW page](/augmented-inverse-probability-weighting/). For the partially linear model $Y = \theta T + g(X) + U$ with $\mathbb{E}[U \mid X, T] = 0$ and a continuous or binary $T$, the parameter is $\theta$. It is causal if, in addition, $T$ is as good as random given $X$ and the effect of $T$ is the same constant $\theta$ for everyone; it is identified by $\theta = \mathbb{E}[(T - m(X))(Y - l(X))]/\mathbb{E}[(T - m(X))^2]$ with $m(X) = \mathbb{E}[T \mid X]$, $l(X) = \mathbb{E}[Y \mid X]$, if $T$ is not a function of $X$. Ignorability, SUTVA and the constant effect cannot be checked from the observed data.

**Estimation.** The input is $n$ units $(X_i, T_i, Y_i)$, a number of folds $k$ (5 is common), and learners: functions that take training data and return a predictor. The output is the estimate, its standard error and a normal [confidence interval](/confidence-interval/).

## The algorithm

```pseudo id=main
DML-ATE(X, T, Y, k, learn_e, learn_m)
L1  give each unit a fold label in {0, ..., k - 1}: a random permutation cut into k near-equal parts
L2  for f ← 0 to k - 1 do
L3      ê ← learn_e(units not in fold f)                      ▷ predicts T from X
L4      m̂1 ← learn_m(treated units not in fold f);  m̂0 ← learn_m(control units not in fold f)
L5      for each unit i in fold f do
L6          ψ_i ← m̂1(X_i) - m̂0(X_i) + T_i (Y_i - m̂1(X_i)) / ê(X_i) - (1 - T_i)(Y_i - m̂0(X_i)) / (1 - ê(X_i))
L7  τ̂ ← (1/n) Σ_i ψ_i
L8  return τ̂ and v = Σ_i (ψ_i - τ̂)² / (n (n - 1))
```

Lines L3 and L4 never see the units of fold $f$, and line L6 uses the fitted functions only on those units. Line L7 pools all the scores (the DML2 form of Chernozhukov et al.); averaging the $k$ fold estimates instead (DML1) gives the same answer here when the folds have equal sizes, because the score is linear in $\tau$. The interval is $\hat\tau \pm z_{1 - \alpha/2}\sqrt v$. Predicted propensities can be clipped to $[\beta, 1 - \beta]$ for a small $\beta$; the clip changes the estimand slightly and should be reported.

**Partially linear model.** The same loop fits $\hat l$ (a regression of $Y$ on $X$) and $\hat m$ (of $T$ on $X$) on the other folds, forms the residuals $\tilde Y_i = Y_i - \hat l(X_i)$ and $\tilde T_i = T_i - \hat m(X_i)$, and returns the residual-on-residual coefficient $\hat\theta = \sum_i\tilde T_i\tilde Y_i/\sum_i\tilde T_i^2$ (Robinson 1988). Its sandwich variance is $\frac1n\cdot\frac{\frac1n\sum_i\hat\psi_i^2}{(\frac1n\sum_i\tilde T_i^2)^2}$ with $\hat\psi_i = (\tilde Y_i - \hat\theta\tilde T_i)\tilde T_i$.

**Repeated splits.** The estimate depends on the random folds. Chernozhukov et al. suggest repeating the whole procedure with several fold assignments and reporting the median estimate, with a variance that adds the spread across splits.

## Example

With $k = 1$ (no cross-fitting) and least squares on the same features for both nuisances, the partially linear estimate is exactly the coefficient of $T$ in the [least squares](/ordinary-least-squares/) regression of $Y$ on $T$ and those features. Take four units with $X = (0, 1, 2, 3)$, $T = (0, 1, 1, 3)$ and $Y = (1, 2, 4, 7)$, and the features $(1, x)$. The regression of $T$ on $(1, x)$ has intercept $-0.1$ and slope $0.9$, with fitted values $(-0.1, 0.8, 1.7, 2.6)$, so $\tilde T = (0.1, 0.2, -0.7, 0.4)$. The regression of $Y$ on $(1, x)$ has intercept $0.5$ and slope 2, with fitted values $(0.5, 2.5, 4.5, 6.5)$, so $\tilde Y = (0.5, -0.5, -0.5, 0.5)$. Then $\hat\theta = (0.05 - 0.1 + 0.35 + 0.2)/(0.01 + 0.04 + 0.49 + 0.16) = 0.5/0.7 = 5/7$. The regression of $Y$ on $(1, x, T)$ gives $Y = \tfrac47 + \tfrac{19}{14}x + \tfrac57T$, with the same coefficient $5/7$ on $T$. This is the Frisch-Waugh-Lovell theorem, and DML generalizes it: replace the two linear fits by any learners, and fit them on other folds.

**Simulation.** For the ATE, take $X$ uniform on $[0, 1]$, $e(x) = \operatorname{expit}(-2 + 4x)$ and $Y = x + 2x^2 + T(1 + x) + \varepsilon$ with standard normal $\varepsilon$, so the true ATE is 1.5. The learners are regressograms: the mean in each of $b$ equal bins of $[0, 1]$. With $n = 1000$, $k = 5$ and 300 samples (seed 2026):

| outcome learner | propensity learner | estimator | mean | SD | 95% coverage |
|---|---|---|---|---|---|
| 2 bins | 10 bins | plug-in regression $\frac1n\sum(\hat m_1 - \hat m_0)$ | 1.782 | 0.080 | |
| 2 bins | 10 bins | DML | 1.495 | 0.084 | 0.970 |
| 10 bins | 10 bins | DML | 1.520 | 0.083 | 0.950 |

The coarse outcome learner alone is biased by 0.28; the orthogonal score removes almost all of it, because the propensity learner is good. For the partially linear model with $T = \cos(2\pi X) + V$ and $Y = 0.5T + 2\cos(2\pi X) + U$, the regression of $Y$ on $(1, X, T)$ gives a mean of 1.169 (coverage 0), while DML with 20-bin learners gives 0.510 (SD 0.035, coverage 0.913). These numbers are measured, not proved.

## Correctness

The proofs establish:

- the folds partition the units, with sizes that differ by at most 1, and with learners that ignore their training data DML is exactly the AIPW estimate;
- with cross-fitting, conditionally on the other folds, the mean of each unit's score differs from $\tau$ by the exact AIPW bias formula, which is bounded by $\frac1c\|e - \hat e\|(\|\mu_1 - \hat m_1\| + \|\mu_0 - \hat m_0\|)$: a product of the two nuisance errors;
- the ATE score and the partially linear score are Neyman orthogonal: the derivative of their mean in any direction of the nuisances is 0 at the truth;
- without cross-fitting and with linear learners on the same features, the partially linear estimate is the OLS coefficient (Frisch-Waugh-Lovell).

The asymptotic normality of $\sqrt n(\hat\tau - \tau)$ under the rate condition $\|e - \hat e\|\cdot\|\mu_t - \hat m_t\| = o_P(n^{-1/2})$, and the validity of the interval, are cited from Chernozhukov et al. (2018), not proved.

## Complexity

Each of the $k$ folds fits three learners (one for the propensity and one per arm) on about $n(k - 1)/k$ units and predicts on about $n/k$ units, so the total is about $3k$ fits; with a learner that costs $C(m)$ on $m$ units, the time is $\Theta(n) + 3k\,C(n)$ up to the change from $n$ to $n(k - 1)/k$. The scores need $\Theta(n)$ space. The fold assignment is a random permutation, $\Theta(n)$. In practice the learners dominate, and repeated splits multiply the cost by their number.

## Properties

- **Product rate.** The bias is a product of the two nuisance errors. If each error is of order $n^{-1/4}$ or smaller, which lasso, forests and boosting can reach under sparsity or smoothness conditions, the product is $o(n^{-1/2})$, and the bias is negligible next to the standard error.
- **Efficient.** With the AIPW score, the limiting variance is $\mathbb{E}[(\psi(W; \eta_0) - \tau)^2]$, Hahn's (1998) efficiency bound.
- **Doubly robust.** The ATE score inherits the double robustness of AIPW: the conditional bias is 0 if either the propensity or the outcome learner is exactly right.
- **No Donsker condition.** Cross-fitting replaces the empirical-process conditions that a learner fitted on the same data would need. That is why the learners can be as complex as forests or neural networks.
- **Randomness from the split.** Two runs with different folds give slightly different estimates; in the simulation, the cross-fitted and the full-sample estimates with 10-bin learners differed by 0.015 on average.

## Variants and improvements

- **Other orthogonal scores.** The partially linear IV model, the ATT, the local average treatment effect, quantile effects and conditional effects on a few groups each have their own orthogonal score; the algorithm is the same.
- **Post-double-selection.** With lasso learners, Belloni, Chernozhukov and Hansen (2014) select the controls that predict $Y$ and those that predict $T$, then run OLS on the union. It is an early form of the orthogonal idea.
- **Cross-validated TMLE.** [TMLE](/targeted-maximum-likelihood-estimation/) with cross-fitted initial fits reaches the same limit with a plug-in estimate.
- **Choosing the learners.** Use [cross-validation](/cross-validation/) within the training folds to tune each learner, or an ensemble. The learner for the propensity should be judged by its fit, not by the effect estimate.

## When to use it

Use DML when there are many covariates, or the confounding is nonlinear, so that a parametric propensity or outcome model is likely wrong, and you want a valid confidence interval for one effect. It needs enough data to fit good learners on $(k - 1)/k$ of the sample, and enough overlap that the propensity stays away from 0 and 1. With few covariates and a small sample, AIPW with simple parametric models is easier to check and often as good.

## Pitfalls

- **Learners too slow.** The guarantee needs the product of the nuisance errors to shrink faster than $1/\sqrt n$. A learner that does not converge, such as an outcome model that ignores an important covariate and a propensity model that is also poor, leaves a bias that cross-fitting cannot remove.
- **Weak overlap.** Large weights $1/\hat e$ inflate the variance of the ATE score, exactly as in IPW. Look at the distribution of the predicted propensities, and consider the ATT, trimming or the partially linear model.
- **The partially linear estimate under heterogeneity.** If the effect varies with $X$, $\theta$ is a weighted average of the effects with weights $\operatorname{Var}[T \mid X]$, not the ATE.
- **Reporting one split.** Report the number of folds and splits, and the variation across splits.
- **Bad controls.** Flexible learners do not decide which variables to adjust for. A covariate affected by the treatment, or a collider, biases the estimate however good the learner is; see the [backdoor criterion](/backdoor-criterion/).
- **Untested ignorability.** DML is about estimation. It inherits the identifying assumptions of the score, which the data cannot check; follow with a [sensitivity analysis](/rosenbaum-sensitivity-analysis/).

## Implementations

## History

Robinson (1988) showed that the coefficient of the partially linear model can be estimated at the $\sqrt n$ rate by regressing the residual of $Y$ on the residual of $T$, both from nonparametric regressions on $X$. Robins, Rotnitzky and Zhao (1994) and the later semiparametric work built the augmented scores that are orthogonal in the same sense, and Neyman's earlier $C(\alpha)$ tests had used scores that are insensitive to nuisance parameters. Belloni, Chernozhukov and Hansen (2014) gave valid inference after lasso selection of many controls. Chernozhukov, Chetverikov, Demirer, Duflo, Hansen, Newey and Robins (2018) combined orthogonal scores with cross-fitting into a general recipe that works with any learner that converges fast enough, and named it double or debiased machine learning.

## References
