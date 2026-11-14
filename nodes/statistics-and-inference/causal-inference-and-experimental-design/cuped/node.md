---
tag: Y9J2V9
kind: algorithm
slug: cuped
name: CUPED
aliases:
- controlled-experiment using pre-experiment data
- regression adjustment for A/B tests
area: statistics-and-inference/causal-inference-and-experimental-design
level: research
summary: Reduces the variance of an online experiment's estimate by subtracting theta times a pre-experiment covariate, with theta the regression coefficient, as in control variates.
model: real-ram
complexity:
  vars: {n: "the number of units in both arms"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, unbiased_for_fixed_theta: true, equals_ancova_with_within_theta: true, needs_pre_treatment_covariate: true}
history:
  year: 2013
  people: [Alex Deng, Ya Xu, Ron Kohavi, Toby Walker]
  note: Deng, Xu, Kohavi and Walker brought the control variates idea of Monte Carlo simulation to online controlled experiments at Microsoft in 2013, using the same metric measured before the experiment as the covariate. The estimator is the analysis of covariance of classical experimental design.
prereqs: [randomized-experiment, welch-t-test]
see_also: [monte-carlo-integration, ordinary-least-squares, augmented-inverse-probability-weighting, statistical-power, sample-size-determination, difference-in-differences, double-machine-learning, average-treatment-effect]
sources:
  - paper: doi:10.1145/2433396.2433413
    title: Alex Deng, Ya Xu, Ron Kohavi and Toby Walker, Improving the sensitivity of online controlled experiments by utilizing pre-experiment data, Proceedings of the Sixth ACM International Conference on Web Search and Data Mining (WSDM), 2013
    locator: pp. 123 to 132 (the control variates estimator, the optimal theta and the factor 1 - rho^2)
  - paper: doi:10.1214/12-AOAS583
    title: Winston Lin, Agnostic notes on regression adjustments to experimental data, reexamining Freedman's critique, The Annals of Applied Statistics 7(1), 2013
    locator: pp. 295 to 318 (regression adjustment with treatment by covariate interactions cannot hurt asymptotic precision, and the sandwich variance is valid)
  - paper: doi:10.1016/j.aam.2006.12.003
    title: David A. Freedman, On regression adjustments to experimental data, Advances in Applied Mathematics 40(2), 2008
    locator: pp. 180 to 193 (under randomization, ANCOVA has a bias of order 1/n and can lose precision when arm sizes differ)
---

CUPED (controlled-experiment using pre-experiment data) makes a [randomized experiment](/randomized-experiment/) more sensitive by removing from each unit's outcome the part that a covariate measured before the experiment already predicts. For a metric $Y$ and a pre-experiment covariate $X$, usually the same metric over an earlier period, it replaces $Y_i$ with $Y_i - \theta(X_i - \bar x)$ and compares the arm means of the adjusted values. Because $X$ is fixed before the coin is tossed, the adjustment does not move the mean of the estimate, but with $\theta$ the regression slope of $Y$ on $X$ it cuts the variance by the factor $1 - \rho^2$, where $\rho$ is the correlation of $X$ and $Y$. It is the control variates method of [Monte Carlo integration](/monte-carlo-integration/) applied to an A/B test, and with the within-arm slope it gives exactly the analysis of covariance (ANCOVA) estimate. The cost is one pass over the data.

## In plain words

Some users spend much more than others, week after week. In an A/B test this spread is noise: it hides the small change that the new version makes. But we already know how much each user spent last month, before the test started. CUPED takes away from each user's number the part that last month's number predicts, and compares what is left between the two groups.

Last month's spending cannot be affected by the new version, and the two groups were formed at random, so the subtraction takes away the same amount from both groups on average and the comparison stays fair. What it takes away is the spread that the two months share. If the months are strongly related, the remaining numbers are much less noisy, and the test needs fewer users or less time to detect the same change.

## The problem

**Identification.** This is the identification of a randomized experiment. Each unit has [potential outcomes](/potential-outcomes-framework/) $Y(1)$ and $Y(0)$, the observed outcome is $Y = TY(1) + (1 - T)Y(0)$ under [SUTVA](/sutva/), and the treatment $T$ is assigned at random, so $T$ is independent of $(Y(1), Y(0), X)$. The estimand is the [average treatment effect](/average-treatment-effect/) $\tau = \mathbb{E}[Y(1) - Y(0)]$, or its finite population version $\frac1n\sum_i(Y_i(1) - Y_i(0))$. It is identified by the difference of the arm means, $\tau = \mathbb{E}[Y \mid T = 1] - \mathbb{E}[Y \mid T = 0]$; no model is needed. The one extra assumption is that $X$ is a pre-treatment covariate: it is measured before the assignment, so the treatment cannot change it. This is checkable in part: the arms should have the same distribution of $X$, and a test of $\bar x_t = \bar x_c$ is a test of the randomization and of this assumption.

**Estimation.** The input is the outcomes and covariates of the $n_t$ treated units and the $n_c$ control units, and a rule for $\theta$. The output is an estimate $\hat\delta$ of $\tau$, the coefficient $\theta$ used, and an estimated variance. The estimator is

$$\hat\delta(\theta) = \frac{1}{n_t}\sum_{T_i = 1}\big(Y_i - \theta(X_i - \bar x)\big) - \frac{1}{n_c}\sum_{T_i = 0}\big(Y_i - \theta(X_i - \bar x)\big) = (\bar y_t - \bar y_c) - \theta(\bar x_t - \bar x_c).$$

The second form shows what happens: if the treated arm happened to have a larger pre-period mean, the estimate is moved down by $\theta$ times that chance difference. Three rules for $\theta$ are common:

- **Fixed in advance**, for example from an earlier experiment. Then $\hat\delta$ is exactly unbiased over the randomization.
- **Pooled**: the slope of $Y$ on $X$ over all units, ignoring the arms, $\hat\theta = \sum_i(X_i - \bar x)(Y_i - \bar y)/\sum_i(X_i - \bar x)^2$. This is the control variates formula $\operatorname{Cov}(X, Y)/\operatorname{Var}(X)$.
- **Within**: the slope fitted inside each arm and pooled, which is the coefficient of $X$ in the regression of $Y$ on $(1, T, X)$.

An estimated $\theta$ makes $\hat\delta$ biased by a term of order $1/n$, which is negligible next to its standard error of order $n^{-1/2}$. The variance estimate is the Welch form $s_t^2/n_t + s_c^2/n_c$ computed on the adjusted values, with $\theta$ treated as fixed, and a normal interval follows. Unlike the propensity weighted estimators of observational studies, nothing here can fail by positivity: the assignment probabilities are known and away from 0 and 1 by design.

## The algorithm

```pseudo id=main
CUPED(Yt, Xt, Yc, Xc, rule)                    ▷ X measured before the experiment
L1  θ ← the value given by rule: fixed, pooled slope of Y on X, or within-arm slope
L2  x̄ ← mean of X over all n_t + n_c units
L3  for every unit i: A_i ← Y_i - θ (X_i - x̄)
L4  δ ← mean of A over the treated - mean of A over the controls
L5  v ← s²(A over treated) / n_t + s²(A over controls) / n_c
L6  return (δ, θ, v)
```

Line L1 is one pass of sums for the slope. Line L2 only centres the adjusted values; by the second form of $\hat\delta$ it does not change $\delta$, but it keeps the adjusted values on the scale of $Y$ so that the per-arm means can be reported. Line L5 is the usual [Welch](/welch-t-test/) variance of a difference in means, applied to the adjusted metric, and the interval is $\delta \pm z_{1 - \alpha/2}\sqrt v$.

## Example

Six users, three per arm. The covariate is last month's spending and the outcome is this month's.

| arm | $X$ | $Y$ |
| --- | --- | --- |
| treated | 2, 4, 6 | 5, 8, 11 |
| control | 1, 3, 5 | 2, 6, 7 |

The plain difference in means is $8 - 5 = 3$, with Welch variance $9/3 + 7/3 = 16/3$. But the treated users also spent more last month: $\bar x_t = 4$ against $\bar x_c = 3$.

**Within-arm $\theta$.** About the arm means, the treated deviations are $X: -2, 0, 2$ and $Y: -3, 0, 3$, and the control deviations are $X: -2, 0, 2$ and $Y: -3, 1, 2$. So $\sum(X - \bar x_{\text{arm}})(Y - \bar y_{\text{arm}}) = 12 + 10 = 22$ and $\sum(X - \bar x_{\text{arm}})^2 = 8 + 8 = 16$, and $\theta = 11/8$. With $\bar x = 7/2$, the adjusted values $Y - \frac{11}{8}(X - \frac72)$ are

| arm | adjusted values | mean | $s^2$ |
| --- | --- | --- | --- |
| treated | 113/16, 117/16, 121/16 | 117/16 | 1/16 |
| control | 87/16, 107/16, 79/16 | 91/16 | 13/16 |

so $\delta = 26/16 = 13/8 = 3 - \frac{11}{8}(4 - 3)$, and $v = \frac{1/16}{3} + \frac{13/16}{3} = 7/24$, against $16/3$ before. The least squares fit of $Y$ on $(1, T, X)$ is $Y = 7/8 + 13/8\,T + 11/8\,X$: the coefficient of $T$ is the CUPED estimate, as the theory says.

**Pooled $\theta$.** Over all six users, $\sum(X - \frac72)(Y - \frac{13}{2}) = 26.5$ and $\sum(X - \frac72)^2 = 17.5$, so $\theta = 53/35$ and $\delta = 3 - 53/35 = 52/35 \approx 1.486$. The pooled slope is larger because the treated users are both higher in $X$ and, through the treatment, higher in $Y$, so part of the effect looks like slope. In a sample this small the two rules differ by 0.14; in the simulation below, with 500 users per arm, they never differed by more than 0.0013.

**Simulation.** $X \sim N(0, 1)$, $Y = 2 + 0.1T + X + 0.75\varepsilon$, so $\rho^2 = 0.64$ and the predicted factor is $0.36$. Over 400 experiments with 500 users per arm (seed 2026), measured:

| estimator | mean | SD | 95% coverage |
| --- | --- | --- | --- |
| difference in means | 0.1065 | 0.0831 | 0.935 |
| CUPED, pooled $\theta$ | 0.1029 | 0.0499 | 0.930 |
| CUPED, within $\theta$ | 0.1030 | 0.0499 | 0.930 |

The ratio of the two Monte Carlo variances was 0.360, and the mean of the per-experiment ratio $v/v_{\text{naive}}$ was also 0.360. The same precision without CUPED would need about $1/0.36 \approx 2.8$ times as many users.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness.md). The key facts:

- **The form.** $\hat\delta(\theta) = (\bar y_t - \bar y_c) - \theta(\bar x_t - \bar x_c)$, whatever value is used for centring.
- **Unbiased for a fixed $\theta$.** Under complete randomization each unit is treated with probability $n_t/n$, so $\mathbb{E}[\bar x_t] = \mathbb{E}[\bar x_c] = \bar x$ and $\mathbb{E}[\bar y_t - \bar y_c] = \tau$. Hence $\mathbb{E}[\hat\delta(\theta)] = \tau$ exactly for any $\theta$ chosen without the assignment. The tests check this by listing all 20 assignments of 6 units with exact fractions.
- **Estimated $\theta$.** Under the sharp null $Y_i(1) = Y_i(0)$ the pooled slope does not depend on the assignment, so the estimate is exactly unbiased there. With a real effect, $\mathbb{E}[\hat\delta] = \tau - \mathbb{E}[\hat\theta(\bar x_t - \bar x_c)]$, which is not 0 in general; the tests show a case. Freedman (2008) shows the bias is of order $1/n$.
- **The factor $1 - \rho^2$.** $\operatorname{Var}(Y - \theta X) = \operatorname{Var}(Y) - 2\theta\operatorname{Cov}(X, Y) + \theta^2\operatorname{Var}(X)$ is smallest at $\theta^* = \operatorname{Cov}(X, Y)/\operatorname{Var}(X)$, where it equals $\operatorname{Var}(Y)(1 - \rho^2)$. If both arms have the same variance and the same covariance with $X$ (for example a constant effect), the variance of $\hat\delta$ falls by the same factor. The identity holds exactly for sample moments too, which the tests check.
- **ANCOVA.** In the regression of $Y$ on $(1, T, X)$, the residuals sum to 0 in each arm, which gives the coefficient of $T$ as $\hat\delta(g)$ with $g$ the coefficient of $X$; the normal equation for $X$ then makes $g$ the within-arm slope.

Proved: these exact statements. Cited, not proved: that an estimated $\theta$ leaves the large-sample distribution unchanged and that the interval has its nominal level (Deng et al. 2013; Lin 2013).

## Complexity

Each step is a constant number of sums over the units, so the time is $\Theta(n)$. The code keeps the adjusted values, $\Theta(n)$ space; a streaming version that keeps the sums of $X$, $Y$, $X^2$, $XY$ and $Y^2$ per arm needs $\Theta(1)$ space, at the cost of the cancellation risk of the textbook variance formula (use [Welford's](/welford-algorithm/) updates for large values). The real cost is in data engineering: joining each unit to its pre-period metric.

## Properties

- **No bias from the adjustment.** The covariate is fixed before assignment, so the adjustment only removes noise. With a fixed $\theta$ this is exact; with an estimated $\theta$ the bias is of order $1/n$.
- **Gain set by the correlation.** The variance falls by $1 - \rho^2$. For $\rho = 0.5$ that is only 25%; for $\rho = 0.9$ it is 81%. Metrics that are stable per user over time, such as sessions or spend, gain the most.
- **Any $\theta$ is valid.** A poor $\theta$ only loses precision; with $\theta = 0$ the estimate is the plain difference in means.
- **Same as regression.** With the within-arm slope it is the ANCOVA coefficient exactly, so standard regression software gives the same point estimate.
- **Missing pre-period data.** New users have no $X$. A common fix is to set $X$ to a constant and add an indicator of missingness as a second covariate; this is valid because the indicator is also pre-treatment.

## Variants and improvements

- **Separate slopes (Lin's estimator).** Fit $\theta_t$ in the treated arm and $\theta_c$ in the control arm, and adjust each arm with its own slope around the overall $\bar x$. This is the regression with a $T \times X$ interaction. Lin (2013) shows that it is never less precise than the unadjusted estimate in large samples, which is not true of a common slope when the arms differ in size and the effect varies with $X$.
- **Several covariates.** Replace $\theta X$ by $\theta^\top X$ with $\theta$ from a multiple regression; the factor becomes $1 - R^2$, with $R^2$ the [coefficient of determination](/coefficient-of-determination/) of $Y$ on $X$.
- **Machine-learning predictions.** Use as the covariate a prediction of $Y$ from any model trained on pre-experiment data. As long as the model never sees the experiment's outcomes or assignments, the prediction is a pre-treatment covariate and the method stays valid. Cross-fitting as in [double machine learning](/double-machine-learning/) lets the model use the experiment's own covariates.
- **Stratification.** Post-stratifying by a discrete pre-period variable, when every stratum has units in both arms, is exactly the separate-slopes adjustment with the stratum indicators as covariates: in each arm the regression on the indicators fits the stratum means, and the adjusted arm mean weights them by the stratum shares.
- **Ratio metrics.** For metrics like clicks per session, apply CUPED to the linearized metric from the [delta method](/delta-method/).

## When to use it

Use CUPED in every A/B test where a pre-experiment version of the metric exists, which is most tests on returning users. It costs one join and one pass, and the gain is free power: the same sensitivity with fewer users or a shorter test. It helps little for metrics with weak memory (one-off conversions), for new users without history, and for very short pre-periods. In an observational study, where $X$ is also needed to remove confounding, use an adjustment estimator such as [AIPW](/augmented-inverse-probability-weighting/) instead: CUPED relies on randomization for its unbiasedness.

## Pitfalls

- **A covariate affected by the treatment.** If $X$ is measured after exposure starts, even partly, the treatment's effect on $X$ is subtracted out. The pre-period must end before the first exposure.
- **Choosing $\theta$ or the covariate after looking at the effect.** Trying several covariates and reporting the one with the best p-value inflates the type I error. Fix the rule in advance.
- **Common slope with unequal arms.** With very unbalanced arms and heterogeneous effects, the pooled or within slope can make the estimate less precise (Freedman 2008). Use separate slopes.
- **Reporting the pooled theta as the ANCOVA answer.** They agree only in large samples; in small samples, as in the example, they differ. Say which rule was used.
- **Variance of the wrong unit.** If users are randomized but the metric is per page view, the units are not independent; compute the variance at the randomization unit (see [cluster-robust standard errors](/cluster-robust-standard-errors/)).
- **Missing $X$ dropped.** Dropping units without pre-period data changes the population. Keep them with an imputed constant and an indicator.

## Implementations

## History

Analysis of covariance, the regression of an experiment's outcome on the treatment and a covariate measured beforehand, is part of classical experimental design and goes back to Fisher. The control variates method of Monte Carlo integration subtracts a correlated quantity with known mean in the same way. Deng, Xu, Kohavi and Walker (2013) brought the idea to online controlled experiments at Microsoft Bing, with the same metric over the pre-experiment period as the covariate, and named it CUPED; it became standard in the experimentation platforms of large web companies. Freedman (2008) had criticized regression adjustment of experiments for its finite sample bias and possible loss of precision, and Lin (2013) answered that the adjustment with treatment by covariate interactions and robust standard errors is safe in large samples.

## References
