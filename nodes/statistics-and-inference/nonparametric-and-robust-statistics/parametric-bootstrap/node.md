---
tag: EDDGAQ
kind: technique
slug: parametric-bootstrap
name: Parametric bootstrap
aliases:
- model-based bootstrap
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Fit a parametric model, simulate new data sets from the fitted model, and recompute the statistic on each. Accurate when the model is right, and misleading when it is wrong.
prereqs: [bootstrap-method, likelihood-function, estimator, standard-error, pivotal-quantity]
see_also: [bootstrap-t-interval, kolmogorov-smirnov-test, t-confidence-interval, permutation-test, monte-carlo-integration, delta-method]
sources:
  - book: isbn:9780412042317
    title: Bradley Efron and Robert J. Tibshirani, An Introduction to the Bootstrap, Chapman and Hall, 1993
    locator: Chapter 6 (the bootstrap estimate of standard error, with the parametric bootstrap as a variant)
  - book: isbn:9780521574716
    title: A. C. Davison and D. V. Hinkley, Bootstrap Methods and their Application, Cambridge University Press, 1997
    locator: Chapter 2 (parametric simulation) and Chapter 4 (tests, including parametric bootstrap tests and Monte Carlo tests)
  - paper: doi:10.1214/aos/1176344552
    title: Bradley Efron, Bootstrap methods, another look at the jackknife, The Annals of Statistics 7(1), 1979
    locator: pp. 1 to 26 (the bootstrap from an estimated distribution, which may be parametric)
  - paper: doi:10.1080/01621459.1967.10482916
    title: Hubert W. Lilliefors, On the Kolmogorov-Smirnov test for normality with mean and variance unknown, Journal of the American Statistical Association 62(318), 1967
    locator: pp. 399 to 402 (critical values by simulation when the parameters are estimated)
---

The parametric bootstrap estimates the sampling distribution of a statistic by simulation from a fitted model. It fits a parametric family $\{F_\theta\}$ to the data, draws many data sets of the same size from $F_{\hat\theta}$, and recomputes the statistic on each. It differs from the nonparametric [bootstrap](/bootstrap-method/) only in the distribution it draws from: $F_{\hat\theta}$ instead of the empirical distribution $\hat F_n$. When the model is right it is more accurate, and when the statistic is pivotal in the model, a test based on it has exact level.

## In plain words

You have seven survival times and you believe they follow an exponential law, the law of waiting times with no memory. That law has only one number to choose, its average. So you set the average to the average of your data.

Now you have a full model, and a computer can produce as many fake data sets from it as you like. Make a few thousand fake sets of seven times, compute your statistic on each, and look at how much it varies. That spread is your error estimate.

The ordinary bootstrap reuses only the seven numbers you saw. The model-based version can produce values that you did not see, for example a time longer than the longest one. This helps when the model is good. If the model is bad, the fake data are wrong, and so is the answer.

## When it applies

- The data come from a parametric family $F_\theta$ that you trust, for example exponential lifetimes, Poisson counts or a normal linear model, and $\theta$ has a consistent estimator $\hat\theta$, often the [maximum likelihood estimate](/maximum-likelihood-estimation/).
- The statistic has no closed-form distribution, or only a large-sample approximation that is poor at your $n$.
- The model can be simulated. Each replicate costs one simulation and one evaluation of the statistic, and often one refit.
- For tests: the null hypothesis is a parametric model with unknown nuisance parameters. Simulate from the model fitted under the null.

## The template

The holes are the model family $F_\theta$, the fitting rule, the statistic $s$ and the number of replicates $b$.

```pseudo id=main
PARAMETRIC-BOOTSTRAP(x_1, ..., x_n, fit, F, s, b)
L1  θ̂ ← fit(x_1, ..., x_n)
L2  for j ← 1 to b do
L3      x* ← n independent draws from F_θ̂
L4      θ*_j ← s(x*)                         ▷ s may refit the model on x*
L5  return θ*_1, ..., θ*_b
```

The replicates are then used as in the nonparametric bootstrap: their standard deviation is a standard error, their mean minus $s(x)$ is a bias estimate, and their quantiles give intervals.

**A test with exact level.** Let $T$ be a test statistic whose law under the null model $F_\theta$ is the same for every $\theta$. Such a $T$ is a [pivotal quantity](/pivotal-quantity/) under $H_0$. Then the simulated values $T(x^*_1), \ldots, T(x^*_b)$ have exactly the null law of $T(X)$, whatever $\hat\theta$ is, and the observed value and the $b$ simulated values are exchangeable under $H_0$. So the Monte Carlo p-value $(1 + c)/(1 + b)$, with $c$ the number of simulated values at least as large as the observed one, satisfies $P(p \le \alpha) \le \alpha$ by the rank argument of the [permutation test](/permutation-test/). If $T$ is not pivotal, the level is only approximate, because $\hat\theta \neq \theta$.

**Exponential model, exactly.** If $F_\mu$ is exponential with mean $\mu$, then $\hat\mu = \bar x$, and $\bar X^*$ is the mean of $n$ exponential draws with mean $\bar x$. That is a Gamma law with shape $n$ and scale $\bar x/n$, with mean $\bar x$ and variance $\bar x^2/n$. So the ideal parametric bootstrap standard error of the mean is $\bar x/\sqrt{n}$, which is also the standard error that the inverse Fisher information of the model gives at $\hat\mu$. The nonparametric bootstrap gives $\sqrt{(n - 1)/n} \, S/\sqrt{n}$ instead. The two agree only if $S \approx \bar x$, which the exponential model predicts.

**Normal model, exactly.** If $F_\theta = N(\mu, \sigma^2)$, then for each simulated sample the studentized mean $T^* = (\bar X^* - \hat\mu)/(S^*/\sqrt{n})$ has exactly the $t_{n - 1}$ law, because $T^*$ is pivotal. So a parametric bootstrap-t interval reproduces the [t confidence interval](/t-confidence-interval/), up to Monte Carlo error. The tests check this: with $n = 10$, $b = 20000$ and seed 3, the 0.975 quantile of $T^*$ is within Monte Carlo error of $t_{9, 0.975} = 2.262157$.

**Worked example.** The 7 treated mice of Efron and Tibshirani (Table 2.1) lived 94, 197, 16, 38, 99, 141 and 23 days, with mean $86.86$ and $S = 66.77$.

- Under the exponential model, the standard error of the mean is $86.86/\sqrt{7} = 32.83$. With `random.Random(1)` and $b = 2000$, lines L1 to L5 gave $32.82$. The nonparametric bootstrap gives $23.36$. The difference comes from the model: an exponential law with mean 87 has standard deviation 87, and the data have only 67.
- The same run for the median gave a standard error of $33.59$, against $37.83$ for the ideal nonparametric bootstrap.
- A test of normality: the Kolmogorov-Smirnov distance between the data and the normal law with the sample mean and standard deviation is $D = 0.196$. With $b = 999$ simulated normal samples of size 7 and `random.Random(1)`, the Monte Carlo p-value is $279/500 = 0.558$. Seven values give no evidence against normality, which also shows how weak such a test is at this size.

## Classic examples

- **The Lilliefors test.** The [Kolmogorov-Smirnov test](/kolmogorov-smirnov-test/) with the normal mean and variance estimated from the data. The statistic is invariant under $x \mapsto a + c x$ with $c > 0$, so it is pivotal in the normal location-scale family, and the parametric bootstrap gives a test of exact level. Lilliefors (1967) made his table this way. With $b = 20000$ and seed 7 the simulated 5% critical value at $n = 20$ was $0.192$.
- **Standard errors in a model fit by maximum likelihood**, when the information-based standard error is unreliable, for example for a function of the parameters near a boundary.
- **The number of components of a mixture.** The likelihood ratio statistic for $k$ against $k + 1$ components does not have its usual chi-squared limit, because the null lies on the boundary. Simulate it from the fitted $k$-component model.
- **Goodness of fit for generalized linear models**, where the deviance is only roughly chi-squared for small counts.
- **The bootstrap-t interval** with a parametric resampling plan, which gives intervals with good coverage when the model is close to right; see the [bootstrap-t interval](/bootstrap-t-interval/).

## Variations

- **Semiparametric bootstrap.** Keep a parametric part and resample the rest from the data. In regression, fit the mean model and resample the residuals: the mean is parametric and the error law is nonparametric.
- **Simulation under the null.** For a test, fit the model under $H_0$, not under the alternative, and simulate from that fit. Simulating from the unrestricted fit gives a test with the wrong level.
- **Double bootstrap.** When $T$ is not pivotal, a second level of simulation from each $F_{\hat\theta^*}$ estimates and corrects the level error, at a cost of $b_1 b_2$ fits.
- **Smoothed bootstrap.** Draw from a kernel density estimate. It sits between the parametric and the nonparametric bootstrap.

## Pitfalls

- **A wrong model.** The method answers the question "how would the statistic vary if the model were true". For the mouse data, the exponential model gives a standard error for the mean 40% larger than the nonparametric one. Check the fit, or compare with the nonparametric bootstrap.
- **Ignoring the estimation of parameters.** Using the plain Kolmogorov-Smirnov p-value after estimating the mean and the variance is very conservative. In 2000 normal samples of size 20 with seed 6, the asymptotic Kolmogorov-Smirnov p-value was never below 0.05, though the nominal size is 0.05. Simulate the null law with the parameters re-estimated in each replicate, as line L4 does.
- **Not refitting in each replicate.** If the statistic involves $\hat\theta$, line L4 must recompute it on $x^*$. Reusing $\hat\theta$ from line L1 ignores its variability.
- **Simulating under the alternative.** For a test, the fitted model of line L1 must satisfy $H_0$.
- **Treating a non-pivotal test as exact.** The exact-level argument needs the null law of $T$ not to depend on $\theta$. Otherwise the level error is of the order of the error of $\hat\theta$, and a double bootstrap or a pivotal statistic is better.

## Exercises

1. Show that in the exponential model $\bar X^*$ has the Gamma law with shape $n$ and scale $\bar x/n$, and find the exact $0.025$ and $0.975$ quantiles of $\bar X^*/\bar x$ for $n = 7$ in terms of chi-squared quantiles.
2. Show that the Kolmogorov-Smirnov distance between $x$ and $N(\bar x, S^2)$ does not change under $x_i \mapsto a + c x_i$ with $c > 0$. Deduce that the parametric bootstrap test of normality has exact level.
3. In the normal model, show that the parametric bootstrap distribution of $(\bar X^* - \bar x)/(S^*/\sqrt{n})$ is $t_{n-1}$, and conclude that the parametric bootstrap-t interval is the t interval when $b \to \infty$.
4. In the Poisson model with mean $\lambda$, find the ideal parametric bootstrap variance of $\bar X^*$ and compare it with the nonparametric one.
5. Give a model and a statistic for which the parametric bootstrap test has a level far from $\alpha$ even for large $n$. (Hint: a statistic whose null law changes quickly with a nuisance parameter that is poorly estimated.)

## References
