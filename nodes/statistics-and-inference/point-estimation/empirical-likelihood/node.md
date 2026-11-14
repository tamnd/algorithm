---
tag: DSWA0W
kind: technique
slug: empirical-likelihood
name: Empirical likelihood
aliases:
- Owen's empirical likelihood
area: statistics-and-inference/point-estimation
level: research
summary: Owen's nonparametric likelihood that puts weights on the data points subject to moment constraints. Its ratio has a chi-squared limit, so it gives tests and intervals without a model.
prereqs: [likelihood-ratio-test, wilks-theorem, generalized-method-of-moments]
see_also: [lagrange-multiplier, bootstrap-method, kullback-leibler-divergence, m-estimator, convex-hull, t-confidence-interval, quantile-regression, median]
sources:
  - paper: doi:10.1093/biomet/75.2.237
    title: Art B. Owen, Empirical likelihood ratio confidence intervals for a single functional, Biometrika 75(2), 1988
    locator: pp. 237 to 249 (the definition, intervals for a mean, M-estimates and smooth functionals, and the chi-squared limit)
  - paper: doi:10.1214/aos/1176347494
    title: Art B. Owen, Empirical likelihood ratio confidence regions, Annals of Statistics 18(1), 1990
    locator: pp. 90 to 120 (the vector mean, the chi-squared limit with q degrees of freedom, and coverage error)
  - paper: doi:10.1214/aos/1176325370
    title: Jing Qin and Jerry Lawless, Empirical likelihood and general estimating equations, Annals of Statistics 22(1), 1994
    locator: pp. 300 to 325 (estimating equations with more conditions than parameters, the maximum empirical likelihood estimator and its efficiency)
  - book: isbn:9781584880714
    title: Art B. Owen, Empirical Likelihood, Chapman and Hall/CRC, 2001
    locator: the chapters on the univariate and the vector mean, and the chapter on computation (the pseudo-logarithm and the dual problem)
---

Empirical likelihood builds a likelihood ratio without a parametric model. It gives each observation a weight $w_i$, with the weights on the data points only, and asks how far the weights must move from $1/n$ for a hypothesis $\mathbb{E}[m(X, \theta)] = 0$ to hold exactly. The profile ratio

$$R(\theta) = \max\Big\{\prod_{i=1}^n n w_i \;:\; w_i \ge 0,\; \sum_i w_i = 1,\; \sum_i w_i\, m(x_i, \theta) = 0\Big\}$$

behaves like a parametric [likelihood ratio](/likelihood-ratio-test/): if $m$ has $q$ components and finite, nonsingular covariance at the true $\theta_0$, then $-2\log R(\theta_0) \to \chi^2_q$ in distribution (Owen 1988, 1990), the same limit as [Wilks' theorem](/wilks-theorem/). So it gives tests and confidence regions whose shape the data choose, with no variance estimate and no model for the law of $X$.

## In plain words

Think of the data as the only values the random quantity can take, each with its own probability. With no constraint, the most likely choice is equal probabilities. Now ask a question such as "is the mean 5?". Find the probabilities closest to equal that make the mean of the data exactly 5. The more you must bend the probabilities, the less the data support the answer.

A known reference law tells you how much bending is too much. Collect all answers that need only a little bending, and you have a confidence interval. It needs no formula for the spread and no assumption about the shape of the data. The interval stays inside the range of the data and leans toward the side where the data are spread out more.

## When it applies

- The data $X_1, \ldots, X_n$ are iid from an unknown law $F$, and the quantity of interest is defined by estimating equations $\mathbb{E}_F[m(X, \theta)] = 0$ with $m(x, \theta) \in \mathbb{R}^q$: a mean ($m = x - \mu$), a quantile ($m = \mathbf 1\{x \le \theta\} - p$), regression coefficients, the conditions of an [M-estimator](/m-estimator/) or of the [generalized method of moments](/generalized-method-of-moments/).
- For the chi-squared limit, $\operatorname{Var}[m(X, \theta_0)]$ is finite and nonsingular. For a quantile the indicator function satisfies this for any $F$ that is continuous at $\theta_0$.
- The hypothesis value must be reachable: $0$ must lie inside the [convex hull](/convex-hull/) of $m(x_1, \theta), \ldots, m(x_n, \theta)$. Otherwise $R(\theta) = 0$.
- For dependent data the plain form fails; blocks of observations take the place of single observations.

## The template

```pseudo id=main
EL-TEST(x_1, ..., x_n, θ)
L1  choose ESTIMATING-FUNCTION m(x, θ) ∈ R^q               ▷ hole: x - μ for a mean
L2  d_i ← m(x_i, θ) for i ← 1 to n
L3  if 0 is not inside the convex hull of d_1, ..., d_n then return ∞
L4  λ ← root of Σ_i d_i / (1 + λ'd_i) = 0 with every 1 + λ'd_i > 0   ▷ hole: Newton on the dual
L5  w_i ← 1 / (n (1 + λ'd_i)) for i ← 1 to n
L6  r ← 2 Σ_i log(1 + λ'd_i)                               ▷ r = -2 log R(θ)
L7  return r, and reject when r > CRITICAL-VALUE           ▷ hole: chi-squared q, Bartlett or bootstrap
```

The holes are the estimating function (line L1), the solver for $\lambda$ (line L4) and the calibration (line L7). A confidence region is the set of $\theta$ with $r(\theta)$ at most the critical value; for a scalar mean, $r$ is 0 at $\bar x$ and increases on each side, so each end of the interval is found by bisection.

**The weights (line L5).** Maximize $\sum_i \log w_i$ subject to $\sum_i w_i = 1$ and $\sum_i w_i d_i = 0$. The objective is strictly concave and the constraints are linear, so a point that satisfies the conditions of the [Lagrange multiplier](/lagrange-multiplier/) rule is the unique maximum. With multipliers $\gamma$ and $n\lambda$, the stationarity condition is $1/w_i = \gamma + n\lambda^{\mathsf T}d_i$. Multiplying by $w_i$ and summing gives $n = \gamma$, so $w_i = 1/(n(1 + \lambda^{\mathsf T}d_i))$, and the constraint $\sum_i w_i d_i = 0$ becomes the equation of line L4. Then $\prod_i n w_i = \prod_i (1 + \lambda^{\mathsf T}d_i)^{-1}$, which is line L6. This is proved.

**Solving for $\lambda$ (line L4).** The function $D(\lambda) = -\sum_i \log(1 + \lambda^{\mathsf T}d_i)$ is convex on the set where every $1 + \lambda^{\mathsf T}d_i > 0$, and its gradient is minus the left side of line L4, so $\lambda$ is the minimizer of $D$. Owen's computation replaces $\log z$ for $z < 1/n$ by the quadratic with the same value, slope and curvature at $1/n$. The new function is convex and defined everywhere, so damped Newton steps can start at $\lambda = 0$. A true solution has all $1 + \lambda^{\mathsf T}d_i > 1/n$, because each weight is below 1, so the change does not move it. When the solver ends with some $1 + \lambda^{\mathsf T}d_i < 1/n$, or with weights that do not sum to 1, the point $0$ is outside the hull and line L3 applies.

**Why the limit is chi-squared (sketch, $q = 1$).** Let $d_i = x_i - \mu_0$ with variance $\sigma^2 > 0$. One shows that $\lambda = O_p(n^{-1/2})$ and $\max_i \lvert d_i\rvert = o_p(n^{1/2})$, so $\lambda d_i \to 0$ uniformly. Expanding line L4 to first order gives $\lambda = \sum_i d_i / \sum_i d_i^2 + o_p(n^{-1/2})$, and expanding $\log(1 + u) = u - u^2/2 + \ldots$ in line L6 gives

$$-2\log R(\mu_0) = \frac{n\,\bar d^{\,2}}{\frac1n\sum_i d_i^2} + o_p(1) \to \chi^2_1 \quad \text{in distribution},$$

by the central limit theorem, the law of large numbers and [Slutsky's theorem](/slutsky-theorem/). The full proof, for vectors, is in Owen (1990). The leading term is the score statistic with the variance estimated under the hypothesis, which is why the method needs no separate variance estimate.

## Classic examples

**A mean.** For the eight values $0.4, 0.9, 1.3, 2.1, 2.8, 3.6, 5.2, 9.7$, $\bar x = 3.25$ and $S = 3.036$ (divisor $n - 1$). At $\mu = 2$ the multiplier is $\lambda = 0.3078$, $-2\log R = 2.434$, and the weights fall from $0.246$ on the smallest value to $0.037$ on the largest. At $\mu = 5$, $\lambda = -0.1342$, $-2\log R = 2.117$, and the largest value gets the weight $0.338$. With the $\chi^2_1$ quantile $3.841$, the 95% empirical likelihood interval is $(1.760, 5.694)$. The [t interval](/t-confidence-interval/) is $(0.712, 5.788)$: symmetric about $\bar x$ and reaching close to the smallest value. The empirical likelihood interval is shorter on the left, where the data are dense, and has the long side toward the long tail.

**Quantiles.** With $m(x, \theta) = \mathbf 1\{x \le \theta\} - p$, the constraint fixes the total weight on the points at most $\theta$. The weights are then $p/k$ on those $k$ points and $(1 - p)/(n - k)$ on the rest, so $-2\log R$ is the binomial likelihood ratio statistic for $k$ successes in $n$ trials. The interval for the [median](/median/) is close to the sign test interval, and it is valid whenever $F$ is continuous at the quantile.

**Estimating equations.** With $q$ conditions for $k \le q$ parameters, maximize $R(\theta)$ over $\theta$ (Qin and Lawless 1994). The maximum empirical likelihood estimate has the same first-order law as efficient [GMM](/generalized-method-of-moments/), $(G^{\mathsf T}S^{-1}G)^{-1}/n$, without a weight matrix. The ratio $-2\log(R(\theta_0)/R(\hat\theta))$ is $\chi^2_k$ and $-2\log R(\hat\theta)$ is $\chi^2_{q-k}$, which tests the surplus conditions as the $J$ test does.

**Side information.** If the population mean of an auxiliary variable is known, as in a survey, adding it as a constraint changes the weights, and the weighted mean of the variable of interest gains precision. The weights $w_i$ then act like calibration weights.

**Mean and variance together.** With $m = (x - \mu,\; (x - \mu)^2 - \sigma^2)$ and $q = 2$, the test of a joint value of $(\mu, \sigma^2)$ uses $\chi^2_2$, and the region for both is not an ellipse but follows the data.

## Variations

- **Bartlett correction.** For smooth functions of means, the mean of $-2\log R$ is $q(1 + a/n) + O(n^{-2})$, and dividing by $1 + \hat a/n$ lowers the coverage error from order $n^{-1}$ to order $n^{-2}$ (DiCiccio, Hall and Romano, 1991). The parametric likelihood ratio has the same property.
- **Bootstrap calibration.** Take the critical value from the [bootstrap](/bootstrap-method/) law of $-2\log R(\hat\theta^*)$ instead of the chi-squared table. In practice this corrects most of the undercoverage seen in small skewed samples.
- **Adjusted empirical likelihood.** Add one artificial point $-a_n \bar d$ so that $0$ is always inside the hull, which removes the empty-set problem of line L3 with little change for large $n$.
- **Other divergences.** Empirical likelihood minimizes $\sum_i \log(1/(n w_i))$, a [Kullback-Leibler divergence](/kullback-leibler-divergence/) from the uniform weights. Exponential tilting uses the reverse divergence and Euclidean likelihood a chi-squared distance, which allows negative weights and has a closed form. All of them form generalized empirical likelihood, with the same first-order limits.
- **Profile and nuisance parameters.** For a parameter of interest with nuisance parameters, maximize $R$ over the nuisance part. The limit keeps the chi-squared form with as many degrees of freedom as the parameter of interest.
- **Blocks for time series.** Replace single observations by averages over blocks of consecutive observations, with a scale factor, to keep the limit under dependence.

## Pitfalls

- **Undercoverage in small, skewed samples.** The limit is proved; the accuracy at a given $n$ is only measured. For 95% intervals for the mean, from 4000 samples each, with the $\chi^2_1$ calibration:

| Law | $n = 10$ | $n = 20$ | $n = 40$ | $n = 80$ |
|---|---|---|---|---|
| normal, EL | 0.900 | 0.932 | 0.943 | 0.945 |
| normal, t | 0.952 | 0.949 | 0.948 | 0.949 |
| exponential, EL | 0.862 | 0.906 | 0.928 | 0.936 |
| exponential, t | 0.889 | 0.913 | 0.924 | 0.933 |
| lognormal, EL | 0.812 | 0.869 | 0.900 | 0.919 |
| lognormal, t | 0.841 | 0.867 | 0.897 | 0.913 |

In these runs the plain empirical likelihood interval was no better than the t interval at $n \le 20$, and only about equal at $n = 40$ and 80. Its gain is the shape of the interval, not the coverage. Use a Bartlett or bootstrap calibration, or an F quantile in place of the chi-squared one, for small $n$.
- **The convex hull.** Any $\theta$ for which $0$ is outside the hull of the $m(x_i, \theta)$ gets $R = 0$. For the mean, the interval can never reach beyond $(\min x_i, \max x_i)$, even when the true mean does, as with a heavy right tail and few data. With many constraints compared with $n$, the hull can miss the true value with high probability.
- **No moments, no limit.** The chi-squared limit needs $\operatorname{Var}[m] < \infty$. For a mean of Cauchy data the method gives intervals, but their coverage has no guarantee.
- **Numerical trouble near the hull.** As $\theta$ nears the edge of the feasible set, $\lambda$ grows without bound and a plain Newton step can leave the domain $1 + \lambda^{\mathsf T}d_i > 0$. Use the pseudo-logarithm or a bisection that keeps every weight positive.
- **Profiling is a hard problem.** $\log R(\theta)$ need not be concave in $\theta$ when $m$ is nonlinear in $\theta$, and the region can be non-convex or in parts.

## Exercises

1. For $n = 2$ and $x_1 < \mu < x_2$, find $-2\log R(\mu)$ for the mean, and its value at the midpoint.
   *Answer.* The two constraints fix $w_1 = (x_2 - \mu)/(x_2 - x_1)$ and $w_2 = 1 - w_1$, so $-2\log R(\mu) = -2\log(4 w_1 w_2)$. At the midpoint $w_1 = w_2 = 1/2$ and the value is 0.
2. Show that $-2\log R(\mu) = 0$ exactly at $\mu = \bar x$, and is $\infty$ for $\mu \notin (\min x_i, \max x_i)$ when the $x_i$ are not all equal.
   *Answer.* At $\bar x$, the equal weights satisfy the constraint, so $\lambda = 0$ and $R = 1$. For $\mu \le \min x_i$ all $d_i \ge 0$ with some positive, so $\sum_i w_i d_i = 0$ forces positive weight only on the points with $d_i = 0$, which leaves some $w_i = 0$ and $R = 0$.
3. Show that the empirical likelihood interval for a mean is equivariant under $x \mapsto a + bx$ with $b \ne 0$.
   *Answer.* The constraint $\sum_i w_i(a + bx_i - (a + b\mu)) = b\sum_i w_i(x_i - \mu) = 0$ has the same feasible weights, so $R$ at $a + b\mu$ for the new data equals $R$ at $\mu$ for the old data.
4. For a quantile, show that $-2\log R = 2k\log(k/(np)) + 2(n - k)\log((n - k)/(n(1 - p)))$, where $k$ is the number of $x_i \le \theta$, $0 < k < n$.
   *Answer.* The constraint fixes the total weight on the $k$ points at $p$. Given that total, $\prod_i w_i$ is largest with equal weights within each group, $p/k$ and $(1 - p)/(n - k)$. Then $\log R = k\log(np/k) + (n - k)\log(n(1 - p)/(n - k))$.
5. Use the expansion in the template section to show that for the mean, $-2\log R(\mu)$ and $n(\bar x - \mu)^2/\hat\sigma_\mu^2$ with $\hat\sigma_\mu^2 = \frac1n\sum_i (x_i - \mu)^2$ differ by $o_p(1)$ when $\mu$ is the true mean, and explain why the interval is not symmetric about $\bar x$.
   *Answer.* The leading term of the expansion is exactly that ratio. The cubic term of $\log(1 + u)$ is of order $n^{-1/2}$ and carries the third moment of the data, so for a finite $n$ the ends move toward the long tail.

## References
