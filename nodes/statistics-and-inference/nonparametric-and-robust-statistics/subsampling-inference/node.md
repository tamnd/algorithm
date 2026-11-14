---
tag: HBQCGG
kind: technique
slug: subsampling-inference
name: Subsampling
aliases:
- m-out-of-n bootstrap
- Politis-Romano subsampling
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: Approximate the sampling distribution from statistics on subsamples of size m much smaller than n. It is consistent in cases where the bootstrap fails.
prereqs: [bootstrap-method, sampling-distribution, confidence-interval, order-statistic]
see_also: [jackknife-resampling, block-bootstrap, bootstrap-percentile-interval, random-sampling, central-limit-theorem, quantile, median, bca-bootstrap-interval]
sources:
  - paper: doi:10.1214/aos/1176325770
    title: Dimitris N. Politis and Joseph P. Romano, Large sample confidence regions based on subsamples under minimal assumptions, The Annals of Statistics 22(4), 1994
    locator: pp. 2031 to 2050 (subsampling for iid and stationary data, consistency when b/n tends to 0 and a limit law exists)
  - book: isbn:9780387988542
    title: Dimitris N. Politis, Joseph P. Romano and Michael Wolf, Subsampling, Springer, 1999
    locator: Chapter 2 (subsampling for iid data) and the chapters on dependent data and on estimating the rate of convergence (general locator)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, 3rd edition, Springer, 2005
    locator: Section 15.7 (subsampling, and comparison with the bootstrap)
  - paper: "P. J. Bickel, F. Götze and W. R. van Zwet, Resampling fewer than n observations: gains, losses, and remedies for losses, Statistica Sinica 7(1), 1 to 31, 1997"
    title: P. J. Bickel, F. Götze and W. R. van Zwet, Resampling fewer than n observations, 1997
    locator: pp. 1 to 31 (the m-out-of-n bootstrap with replacement and its relation to subsampling without replacement)
  - paper: doi:10.1214/aos/1176345637
    title: Peter J. Bickel and David A. Freedman, Some asymptotic theory for the bootstrap, The Annals of Statistics 9(6), 1981
    locator: pp. 1196 to 1217 (the bootstrap fails for the sample maximum of a uniform sample)
  - paper: doi:10.1214/aos/1176347263
    title: Jun Shao and C. F. J. Wu, A general theory for jackknife variance estimation, The Annals of Statistics 17(3), 1989
    locator: pp. 1176 to 1197 (the delete-d jackknife, which uses the same subsets)
---

Subsampling estimates the sampling distribution of a statistic from its values on subsets of the data of size $m$, drawn without replacement, with $m \to \infty$ and $m/n \to 0$. Each subset is a true sample of size $m$ from the unknown distribution $F$, not from the empirical distribution, so the method needs only that the suitably scaled statistic has some limit law. It is consistent in cases where the [bootstrap](/bootstrap-method/) fails, such as the maximum of a uniform sample, the mean with infinite variance and many nonstandard estimators. The price is a loss of accuracy where the bootstrap works, and the need to know the rate of convergence and to choose $m$. The m-out-of-n bootstrap is a related method that draws the $m$ values with replacement.

## In plain words

You want to know how much a statistic computed from $n$ points would vary over new samples. You have only one sample. Take a smaller group of $m$ points from it, without repeats, and compute the statistic on that group. Do this for many groups. Each group really is a sample from the population, so the spread of these values shows how the statistic varies for samples of size $m$. If you know how the spread shrinks as the sample grows, you can scale it down to size $n$. The groups must be much smaller than the full sample. Otherwise they overlap too much and look too much like the full sample and like each other.

## When it applies

- **Data.** Independent and identically distributed observations. For a stationary time series, use blocks of $m$ consecutive observations instead of arbitrary subsets.
- **A limit law.** There is a known rate $\tau_n$ such that $\tau_n(\hat\theta_n - \theta)$ converges in law to a continuous limit $J$. The limit can be anything: it need not be normal, and it need not be known. For smooth statistics $\tau_n = \sqrt n$; for the maximum of a uniform sample $\tau_n = n$.
- **Subsample size.** $m \to \infty$, $m/n \to 0$ and $\tau_m/\tau_n \to 0$.

Under these conditions Politis and Romano (1994) proved that the subsampling distribution converges to $J$ and that the subsampling intervals have asymptotic coverage $1 - \alpha$. The proof uses only that a U-statistic of order $m$ concentrates when $m/n \to 0$, so it needs much less than the bootstrap.

## The template

Let $L_{n,m}$ be the distribution of the roots $\tau_m(\hat\theta_{m,S} - \hat\theta_n)$ over subsets $S$ of size $m$, where $\hat\theta_{m,S}$ is the statistic on the subset. It estimates the law of $\tau_n(\hat\theta_n - \theta)$, so its quantiles $c_p$ give the interval $[\hat\theta_n - c_{1-\alpha/2}/\tau_n,\ \hat\theta_n - c_{\alpha/2}/\tau_n]$.

```pseudo id=main
SUBSAMPLING-INTERVAL(x_1, ..., x_n, s, m, τ, α, b)
L1  θ̂ ← s(x_1, ..., x_n)
L2  for j ← 1 to b do
L3      S ← m distinct indices drawn uniformly from {1, ..., n}
L4      r_j ← τ(m) (s(x_S) - θ̂)
L5  sort r_1, ..., r_b
L6  c_lo ← r_(⌈b α/2⌉), c_hi ← r_(⌈b (1 - α/2)⌉)
L7  return [θ̂ - c_hi / τ(n), θ̂ - c_lo / τ(n)]
```

With all $\binom nm$ subsets in place of $b$ random ones, this is the exact subsampling distribution, and the implementation does that when it is called without $b$. Random subsets add a Monte Carlo error that vanishes as $b$ grows, as for the bootstrap. Politis and Romano write $b$ for the subsample size; this page writes $m$, to keep $b$ for the number of replicates as on the other resampling pages.

**Subsampling and the m-out-of-n bootstrap.** The m-out-of-n bootstrap of Bickel, Götze and van Zwet (1997) uses the same roots and the same scaling, but draws the $m$ values with replacement from the data. Its subsamples are samples from $\hat F_n$, not from $F$, and contain repeated values. If $m^2/n \to 0$, a with-replacement sample of size $m$ has no repeated index with probability tending to 1, and the two methods agree asymptotically. The m-out-of-n bootstrap can be used with $m$ larger than $n$ and for smoothing, while subsampling has a simpler theory and needs weaker conditions.

## Classic examples

**The maximum of a uniform sample.** For $X_i$ uniform on $(0, \theta)$, $\hat\theta = X_{(n)}$ and $n(\theta - X_{(n)})/\theta$ is asymptotically exponential. The bootstrap fails: a resample contains $X_{(n)}$ with probability $1 - (1 - 1/n)^n \to 1 - e^{-1} = 0.632$, so the bootstrap law of $n(X^*_{(n)} - X_{(n)})$ has an atom of size $0.632$ at 0, while the true limit is continuous. A random subset of size $m$ contains $X_{(n)}$ with probability $m/n \to 0$. More precisely, its maximum is the $k$-th smallest value with probability $\binom{k-1}{m-1}/\binom nm$; the tests check this law by listing all subsets.

For one sample of $n = 100$ uniform values with $\theta = 1$ (seed 31), $X_{(n)} = 0.9963$, and the exact 95% upper confidence bound is $X_{(n)}/0.05^{1/n} = 1.0266$. With $b = 2000$ (seed 1) the one-sided 95% bounds $X_{(n)} - c_{0.05}/n$ were $1.0037$ for the bootstrap, whose roots were 0 in $63.8\%$ of the replicates, $1.0192$ for subsampling with $m = 10$, and $1.0219$ for the m-out-of-n bootstrap with $m = 10$.

**Measured coverage.** Over 1000 data sets with $n = 100$ and $b = 500$ (seed 41), the one-sided 95% bound covered $\theta$ in this fraction of cases:

| method | $m$ | coverage |
|---|---|---|
| bootstrap | 100 | 0.766 |
| m-out-of-n bootstrap | 10 | 0.891 |
| m-out-of-n bootstrap | 20 | 0.908 |
| subsampling | 10 | 0.885 |
| subsampling | 20 | 0.898 |
| subsampling | 50 | 0.764 |

With $n = 1000$ (400 data sets, seed 43), subsampling gave $0.958$ with $m = 30$ and $0.950$ with $m = 100$, and the m-out-of-n bootstrap gave $0.920$ with $m = 30$. The bootstrap stays wrong for every $n$; subsampling approaches the nominal level slowly, and $m = 50$ out of $100$ is too large. These are measurements, with a Monte Carlo standard error of about $0.007$ for 1000 data sets and $0.011$ for 400.

**The variance of a mean, and the delete-d jackknife.** For the mean, the variance of $\bar x_S$ over all subsets of size $m$ is exactly $\frac{S^2}{m}(1 - \frac mn)$, the finite population formula. The plain subsampling estimate of $\mathrm{Var}(\bar x)$ rescales it by $\tau_m^2/\tau_n^2 = m/n$ and gives $\frac{S^2}{n}(1 - \frac mn)$, which is right only when $m/n \to 0$. The [delete-$d$ jackknife](/jackknife-resampling/) with $d = n - m$ uses the same subsets but rescales by $\frac{m}{n - m}$, which gives exactly $S^2/n$ for every $m$. The tests check both identities with exact fractions.

**Heavy tails.** For the mean of a distribution with infinite variance in the domain of attraction of a stable law, the bootstrap distribution has a random limit (Athreya 1987), while subsampling with the right rate is consistent. If the rate is unknown, it can be estimated from the spread of subsampling distributions at several values of $m$.

**Dependent data.** For a stationary series, the $n - m + 1$ blocks of $m$ consecutive values are the subsamples. This needs fewer conditions than the [block bootstrap](/block-bootstrap/), but is less accurate where both work.

## Variations

- **All subsets or random subsets.** The full set of $\binom nm$ subsets gives a U-statistic of order $m$; random subsets or a balanced design give the same limit at a cost of $b$ evaluations.
- **Symmetric and studentized roots.** Using $\tau_m\lvert\hat\theta_{m,S} - \hat\theta_n\rvert$ gives symmetric intervals. Dividing each root by a standard error computed on the subset removes the need for $\tau$ when the statistic is studentized.
- **Estimated rate.** When $\tau_n = n^\beta$ with unknown $\beta$, compare the spread of the subsampling distributions for two or more values of $m$ to estimate $\beta$ (Politis, Romano and Wolf 1999).
- **Choice of m.** Calibration by a second level of subsampling, or the minimum volatility rule, which picks the $m$ where the interval endpoints change least with $m$.
- **Extrapolation.** Combining several values of $m$ can reduce the bias of order $m/n$ that the table shows.
- **Hypothesis tests.** The quantiles of the subsampling distribution of a test statistic, computed under the null or centred at the estimate, give tests with asymptotically correct level.

## Pitfalls

- **m too large.** With $m/n$ not small, the subsets overlap heavily and look like the full sample. In the table, $m = 50$ of $n = 100$ covered only $76\%$.
- **m too small.** With very small $m$, the statistic on the subset is far from its limit law. A rule of thumb is to try several $m$ and look for a range where the answer is stable.
- **The wrong rate.** The method rescales by $\tau_m/\tau_n$. A wrong rate gives intervals of the wrong length, even asymptotically.
- **Centring at the estimate.** The roots are centred at $\hat\theta_n$, not at $\theta$. This adds an error of order $\tau_m/\tau_n$, which is the main reason for the slow convergence in the table.
- **Using it where the bootstrap works.** For smooth statistics such as a mean or a correlation, the bootstrap, especially the [BCa interval](/bca-bootstrap-interval/), is more accurate. Subsampling is the tool for cases where the bootstrap fails.

## Exercises

1. Show that a uniform random subset of size $m$ from $n$ distinct values has its maximum at the $k$-th smallest value with probability $\binom{k-1}{m-1}/\binom nm$, and that the probability that it contains the overall maximum is $m/n$.
2. Show that the variance of $\bar x_S$ over all subsets of size $m$ is $\frac{S^2}{m}(1 - \frac mn)$. Then show that the delete-$d$ jackknife with $d = n - m$ gives $S^2/n$ for every $m$.
3. Compute the probability that a with-replacement sample of size $m$ from $n$ indices has no repeated index, and show that it tends to 1 when $m^2/n \to 0$. Explain why the m-out-of-n bootstrap and subsampling then agree.
4. For the uniform maximum, find the limit of $P^*(X^*_{(n)} = X_{(n)})$ for the bootstrap and for the m-out-of-n bootstrap with $m/n \to 0$.
5. Run the implementation on the median of $n = 200$ normal values with $\tau_n = \sqrt n$ and several values of $m$, and compare the intervals with the bootstrap percentile interval.

## References
