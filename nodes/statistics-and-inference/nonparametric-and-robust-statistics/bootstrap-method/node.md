---
tag: V0JBK5
kind: technique
slug: bootstrap-method
name: Bootstrap
aliases:
- Efron's bootstrap
- bootstrap resampling
area: statistics-and-inference/nonparametric-and-robust-statistics
level: intro
summary: Estimate the sampling distribution of a statistic by recomputing it on many samples drawn with replacement from the data. It gives standard errors, bias and intervals.
prereqs: [estimator, standard-error, sampling-distribution, estimator-bias, empirical-distribution-function]
see_also: [bootstrap-percentile-interval, parametric-bootstrap, jackknife-resampling, block-bootstrap, permutation-test, bagging, phylogenetic-bootstrap, monte-carlo-integration]
sources:
  - paper: doi:10.1214/aos/1176344552
    title: Bradley Efron, Bootstrap methods, another look at the jackknife, The Annals of Statistics 7(1), 1979
    locator: pp. 1 to 26 (the bootstrap, the exact computation for the mean, and the comparison with the jackknife)
  - book: isbn:9780412042317
    title: Bradley Efron and Robert J. Tibshirani, An Introduction to the Bootstrap, Chapman and Hall, 1993
    locator: Chapter 6 (the bootstrap estimate of standard error, Algorithm 6.1 and the choice of B) and Chapter 10 (bootstrap estimates of bias)
  - book: isbn:9780521574716
    title: A. C. Davison and D. V. Hinkley, Bootstrap Methods and their Application, Cambridge University Press, 1997
    locator: Chapter 2 (the basic bootstraps, the plug-in principle and the number of simulations) and Chapter 3 (further ideas, including the smoothed and the parametric bootstrap)
  - paper: doi:10.1214/aos/1176345637
    title: Peter J. Bickel and David A. Freedman, Some asymptotic theory for the bootstrap, The Annals of Statistics 9(6), 1981
    locator: pp. 1196 to 1217 (consistency for the mean and for von Mises functionals, and the failure for the sample maximum)
  - paper: doi:10.1214/aos/1176350371
    title: K. B. Athreya, Bootstrap of the mean in the infinite variance case, The Annals of Statistics 15(2), 1987
    locator: pp. 724 to 731 (the bootstrap of the mean has a random limit when the variance is infinite)
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Chapter 8 (the bootstrap, bootstrap variance estimation and intervals)
---

The bootstrap estimates the sampling distribution of a statistic from one sample. It treats the sample as if it were the population: it draws many new samples of the same size with replacement from the data, computes the statistic on each, and uses the spread of these values as an estimate of the spread of the statistic over repeated real samples. Bradley Efron introduced it in 1979. It gives [standard errors](/standard-error/), [bias](/estimator-bias/) estimates and confidence intervals for statistics that have no simple formula, such as a median, a ratio or a correlation.

## In plain words

You measured seven mice and computed their median survival time. How much would that median change if you could repeat the study with seven new mice? You cannot repeat the study, so you use the seven numbers you have as a stand-in for all mice.

Put the seven numbers in a hat. Draw one, write it down, and put it back. Do this seven times. Some numbers come out twice and some not at all. That is one "bootstrap sample". Compute its median. Repeat a few thousand times. The medians that you get scatter around, and their spread tells you how much the real median would scatter from study to study. The only work is computing, and the same recipe works for almost any statistic.

## When it applies

- The data $X_1, \ldots, X_n$ are independent and identically distributed from an unknown distribution $F$. The basic bootstrap does not apply to time series, clustered data or other dependent data; see the [block bootstrap](/block-bootstrap/) for stationary series.
- The quantity of interest is a functional $\theta = t(F)$, such as a mean, a quantile or a correlation, and the estimate is the plug-in value $\hat\theta = t(\hat F_n)$, where $\hat F_n$ is the [empirical distribution function](/empirical-distribution-function/).
- The statistic is a smooth function of $\hat F_n$. Then the bootstrap distribution of $\sqrt{n}(\hat\theta^* - \hat\theta)$ approaches the true distribution of $\sqrt{n}(\hat\theta - \theta)$ (Bickel and Freedman 1981). The mean with finite variance, smooth functions of means, and quantiles of a distribution with a positive density all qualify.
- It does not apply as is to extremes (the sample maximum), to the mean when the variance is infinite, to parameters on the boundary of the parameter space, or to very small samples. See the pitfalls below.

## The template

The holes are the statistic $s$, the resampling plan (here: draw from $\hat F_n$) and the number of replicates $b$.

```pseudo id=main
BOOTSTRAP(x_1, ..., x_n, s, b)
L1  for j ← 1 to b do
L2      x* ← n independent draws from x_1 .. x_n, each with probability 1/n
L3      θ*_j ← s(x*)
L4  se ← sqrt( Σ_j (θ*_j - θ̄*)² / (b - 1) )        ▷ θ̄* is the mean of the θ*_j
L5  bias ← θ̄* - s(x_1, ..., x_n)
L6  return θ*_1, ..., θ*_b, se, bias
```

**The plug-in principle.** The true distribution of $\hat\theta - \theta$ depends on $F$, which is unknown. The bootstrap replaces $F$ by $\hat F_n$ and $\theta$ by $\hat\theta = t(\hat F_n)$, and uses the distribution of $\hat\theta^* - \hat\theta$ when $X_1^*, \ldots, X_n^*$ are drawn from $\hat F_n$. This *ideal bootstrap distribution* is a fixed function of the data. Lines L1 to L3 approximate it by [Monte Carlo integration](/monte-carlo-integration/). So there are two errors: the statistical error of replacing $F$ by $\hat F_n$, which does not shrink with $b$, and the Monte Carlo error, which shrinks like $1/\sqrt{b}$.

**The ideal bootstrap is a finite distribution.** There are $n^n$ ordered resamples, each with probability $n^{-n}$. Only the multiset of drawn indices matters for a symmetric statistic, and there are $\binom{2n - 1}{n}$ multisets. A multiset in which index $i$ appears $c_i$ times has the multinomial probability $\frac{n!}{c_1! \cdots c_n!} n^{-n}$. For $n = 7$ there are 1716 multisets instead of 823543 ordered resamples, so the ideal bootstrap can be computed exactly for small $n$. The code does this, and the tests check it against all $n^n$ resamples for $n \le 5$.

**The mean, exactly.** Each $X_i^*$ is drawn from $\hat F_n$, which has mean $\bar x$ and variance $\hat\sigma^2 = \frac{1}{n} \sum_i (x_i - \bar x)^2$. The draws are independent, so

$$E^*[\bar X^*] = \bar x, \qquad \operatorname{Var}^*(\bar X^*) = \frac{\hat\sigma^2}{n} = \frac{1}{n^2} \sum_{i=1}^n (x_i - \bar x)^2 = \frac{n - 1}{n} \cdot \frac{S^2}{n}.$$

So the ideal bootstrap standard error of the mean is $\sqrt{(n - 1)/n}$ times the usual $S/\sqrt{n}$. It is slightly too small for small $n$, because $\hat F_n$ has less spread than $F$ on average.

**How many replicates.** For a standard error, $b$ between 200 and 1000 is usually enough, since the Monte Carlo error is then small against the statistical error. For the tails of a distribution, as in a percentile interval, use $b \ge 2000$. Efron and Tibshirani (Chapter 6) discuss the rule.

**Worked example.** The 7 treated mice of Efron and Tibshirani (Table 2.1) lived 94, 197, 16, 38, 99, 141 and 23 days. The mean is 86.86 and $S/\sqrt{7} = 25.24$. The exact bootstrap variance of the mean is $187228/343$, so the ideal bootstrap standard error is $23.36 = \sqrt{6/7} \cdot 25.24$. With `random.Random(1)` and $b = 2000$, lines L1 to L4 gave $23.50$.

The median is 94, and it has no simple standard error formula. The ideal bootstrap distribution of the median puts probability 0.306 on 94, 0.239 on each of 38 and 99, 0.098 on each of 23 and 141, and 0.010 on each of 16 and 197. Its standard deviation is 37.83, and its mean is 79.73, so the ideal bootstrap bias estimate is $-14.27$. With `random.Random(1)` the Monte Carlo standard error was 36.33 at $b = 25$, 37.53 at $b = 200$ and 38.49 at $b = 4000$. Here the median has a standard error about 1.6 times that of the mean, because the values next to the median, 38 and 99, are far from it.

## Classic examples

- **The standard error of a median, a trimmed mean or a ratio**, as in the worked example. For the [trimmed mean](/trimmed-mean/) and the [Hodges-Lehmann estimator](/hodges-lehmann-estimator/) the formulas are asymptotic and hard to use, but the bootstrap is direct.
- **Confidence intervals.** The [percentile interval](/bootstrap-percentile-interval/), the [bootstrap-t interval](/bootstrap-t-interval/) and the [BCa interval](/bca-bootstrap-interval/) all start from the replicates of line L3.
- **Bias correction.** Line L5 estimates the bias; $\hat\theta - \widehat{\text{bias}} = 2\hat\theta - \bar\theta^*$ is the bias-corrected estimate. The [jackknife](/jackknife-resampling/) gives a cheaper estimate of the same bias.
- **Regression.** Resample the pairs $(x_i, y_i)$, which allows any form of heteroscedasticity, or fit once and resample the residuals, which assumes that the errors are exchangeable.
- **Bagging.** [Bagging](/bagging/) and [random forests](/random-forest/) average a predictor over bootstrap samples to reduce its variance. The goal there is a better predictor, not an error estimate.
- **Phylogenetics.** The [phylogenetic bootstrap](/phylogenetic-bootstrap/) resamples alignment columns and reports how often each clade of the tree appears.
- **Parametric models.** The [parametric bootstrap](/parametric-bootstrap/) draws from a fitted model $F_{\hat\theta}$ instead of $\hat F_n$.

## Variations

- **Parametric bootstrap.** Draw the resamples from a fitted parametric model. It is more accurate when the model is right, and wrong when it is not.
- **Smoothed bootstrap.** Draw from a kernel density estimate instead of $\hat F_n$, which removes the discreteness. It helps for quantiles in small samples.
- **Bayesian bootstrap.** Rubin (1981) weights the observations by a Dirichlet$(1, \ldots, 1)$ vector instead of multinomial counts. The result is a posterior distribution under a noninformative model on the support of the data.
- **Wild bootstrap.** For regression with heteroscedastic errors, multiply each residual by an independent random sign or another weight with mean 0 and variance 1, and keep each residual on its own design point.
- **Block bootstrap.** Resample blocks of consecutive values to keep the dependence of a time series; see the [block bootstrap](/block-bootstrap/).
- **Subsampling and the m-out-of-n bootstrap.** Draw samples of size $m \ll n$, without or with replacement. They are consistent in many cases where the ordinary bootstrap fails; see [subsampling](/subsampling-inference/).
- **Balanced and antithetic resampling.** Arrange the $b$ resamples so that each observation appears exactly $b$ times in total. This removes part of the Monte Carlo error at no extra cost (Davison and Hinkley, Chapter 9).
- **Exact enumeration.** For small $n$, enumerate the $\binom{2n - 1}{n}$ multisets as the code does, and get the ideal bootstrap without Monte Carlo error.

## Pitfalls

- **The maximum.** A resample contains the largest observation with probability $1 - (1 - 1/n)^n$, which is $0.672$ for $n = 5$ and tends to $1 - 1/e = 0.632$. So the bootstrap distribution of the maximum has an atom of about 63% at the observed maximum, while the true distribution of $n(\theta - X_{(n)})$ for a uniform $[0, \theta]$ sample is continuous (exponential in the limit). The bootstrap is not consistent here (Bickel and Freedman 1981). Use [subsampling](/subsampling-inference/) or a parametric model.
- **Infinite variance.** For the mean of a heavy-tailed distribution with infinite variance, the bootstrap distribution has a random limit and does not estimate the sampling distribution (Athreya 1987).
- **Dependent data.** Resampling single values of a time series destroys the dependence. For an AR(1) series with coefficient 0.5 the bootstrap variance of the mean is too small by a factor of about 3; see the [block bootstrap](/block-bootstrap/).
- **The wrong unit.** With clustered data (pupils in schools, repeated measures on patients), resample whole clusters.
- **Small samples.** The bootstrap cannot add information. With $n = 5$ the resamples come from only 5 values, and the ideal bootstrap standard error of the mean is still $\sqrt{4/5} = 0.89$ times the usual one.
- **Too few replicates.** $b = 25$ can give a usable standard error but not a usable 2.5% quantile. Report $b$ and the seed.
- **Not the same as particle resampling.** [Resampling in particle filters](/resampling/) draws from a weighted set of particles to reduce weight degeneracy. It uses the same multinomial draw but has a different purpose.

## Exercises

1. Show that the number of distinct bootstrap multisets of a sample of $n$ distinct values is $\binom{2n - 1}{n}$, and evaluate it for $n = 10$ and $n = 20$.
2. Prove that $\operatorname{Var}^*(\bar X^*) = \frac{1}{n^2} \sum_i (x_i - \bar x)^2$, and deduce that the ideal bootstrap standard error of the mean is $\sqrt{(n - 1)/n} \, S/\sqrt{n}$.
3. Show that $P^*(X^*_{(n)} = x_{(n)}) = 1 - (1 - 1/n)^n$ when the values are distinct, and that the expected number of distinct original values in a resample is $n(1 - (1 - 1/n)^n)$.
4. For the plug-in variance $\hat\sigma^2$, show that $E^*[\hat\sigma^{2*}] = \frac{n - 1}{n} \hat\sigma^2$. Find the bias-corrected estimate $2\hat\sigma^2 - E^*[\hat\sigma^{2*}]$ and compare it with $S^2$.
5. The Monte Carlo estimate of the ideal bootstrap probability $P^*(\hat\theta^* \le c)$ is the fraction of the $b$ replicates at most $c$. Show that its Monte Carlo standard error is at most $1/(2\sqrt{b})$, and find the $b$ that makes it at most $0.005$.

## References
