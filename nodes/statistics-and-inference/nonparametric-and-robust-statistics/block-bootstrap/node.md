---
tag: Q86QP6
kind: algorithm
slug: block-bootstrap
name: Block bootstrap
aliases:
- moving block bootstrap
- stationary bootstrap
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: Resamples blocks of consecutive observations of a time series to keep their dependence. The stationary bootstrap of Politis and Romano uses blocks of random length.
model: real-ram
complexity:
  vars: {n: the length of the series, b: the number of bootstrap replicates}
  time: {worst: Θ(b n)}
  space: {extra: Θ(b + n)}
properties: {deterministic: false, randomized: true, exact: false, online: false, recursive: false}
history:
  year: 1989
  people: [Hans Künsch, Regina Liu, Kesar Singh, Dimitris Politis, Joseph Romano]
  note: Künsch (1989) and, independently, Liu and Singh (1992) introduced the moving block bootstrap; Politis and Romano added the circular (1992) and stationary (1994) versions.
prereqs: [bootstrap-method, standard-error, sampling-distribution]
see_also: [stationary-process, autoregressive-model, autocorrelation, effective-sample-size, mcmc-autocorrelation, subsampling-inference, jackknife-resampling, parametric-bootstrap]
sources:
  - paper: doi:10.1214/aos/1176347265
    title: Hans R. Künsch, The jackknife and the bootstrap for general stationary observations, The Annals of Statistics 17(3), 1989
    locator: pp. 1217 to 1241 (the moving block bootstrap and the blockwise jackknife, consistency for smooth functions of the mean)
  - paper: doi:10.1080/01621459.1994.10476870
    title: Dimitris N. Politis and Joseph P. Romano, The stationary bootstrap, Journal of the American Statistical Association 89(428), 1994
    locator: pp. 1303 to 1313 (blocks of geometric length that wrap around, the stationarity of the resampled series and the variance of the resample mean)
  - paper: "Dimitris N. Politis and Joseph P. Romano, A circular block-resampling procedure for stationary data, in R. LePage and L. Billard (eds.), Exploring the Limits of Bootstrap, Wiley, New York, 263 to 270, 1992"
    title: D. N. Politis and J. P. Romano, A circular block-resampling procedure for stationary data, 1992
    locator: pp. 263 to 270 (the circular block bootstrap)
  - paper: doi:10.1093/biomet/82.3.561
    title: Peter Hall, Joel L. Horowitz and Bing-Yi Jing, On blocking rules for the bootstrap with dependent data, Biometrika 82(3), 1995
    locator: pp. 561 to 574 (optimal block lengths of order n^(1/3) for variance and bias, n^(1/4) and n^(1/5) for distribution functions)
  - book: isbn:9780387009285
    title: S. N. Lahiri, Resampling Methods for Dependent Data, Springer, 2003
    locator: the chapters on block bootstrap methods and their comparison (general locator)
  - book: isbn:9780521574716
    title: A. C. Davison and D. V. Hinkley, Bootstrap Methods and their Application, Cambridge University Press, 1997
    locator: Chapter 8 (complex dependence, block resampling and the choice of block length)
---

The block bootstrap resamples a time series by joining blocks of consecutive observations, drawn with replacement, instead of single observations. Inside each block the original dependence is kept, so the resampled series has nearly the right short-range correlation, and the [bootstrap](/bootstrap-method/) estimates of variance and of sampling distributions stay valid for weakly dependent [stationary series](/stationary-process/). The moving block bootstrap uses all $n - l + 1$ overlapping blocks of a fixed length $l$. The stationary bootstrap, a variant, uses blocks of random geometric length that wrap around the end of the series, which makes the resampled series stationary.

## In plain words

The ordinary bootstrap shuffles single data points. For a time series this destroys the pattern that each value is close to the one before it, so the bootstrap thinks the average is much more precise than it is. The block bootstrap cuts the series into short runs of neighbouring values, such as runs of five, picks runs at random with replacement and joins them into a new series of the same length. Inside each run the pattern is kept. Only at the joins is it broken. Longer runs keep more of the pattern, but there are fewer different runs to pick from, so the answer is noisier. The block length is a balance between these two errors.

## The problem

**Input.** A series $x_1, \ldots, x_n$ from a stationary process with dependence that dies out with the lag, a statistic $s$, a block length $1 \le l \le n$ and a number of replicates $b$.

**Output.** Replicates $\theta^*_1, \ldots, \theta^*_b$ of $s$, whose spread estimates the sampling variability of $\hat\theta = s(x)$, for example its [standard error](/standard-error/).

**Blocks.** Let $B_i = (x_i, \ldots, x_{i+l-1})$ for $i = 1, \ldots, N$ with $N = n - l + 1$, and $k = \lceil n/l \rceil$. A moving block resample is $B_{I_1}, \ldots, B_{I_k}$ joined and cut to its first $n$ values, with $I_1, \ldots, I_k$ independent and uniform on $\{1, \ldots, N\}$. With $l = 1$ this is the ordinary bootstrap.

## The algorithm

```pseudo id=main
MOVING-BLOCK-BOOTSTRAP(x_1, ..., x_n, s, l, b)
L1  k ← ⌈n/l⌉, N ← n - l + 1
L2  for j ← 1 to b do
L3      x* ← the empty sequence
L4      for q ← 1 to k do
L5          I ← a uniform random index in {1, ..., N}
L6          append x_I, x_{I+1}, ..., x_{I+l-1} to x*
L7      cut x* to its first n values
L8      θ*_j ← s(x*)
L9  return θ*_1, ..., θ*_b
```

The standard error estimate is the standard deviation of the replicates. The implementation also has the circular and the stationary versions of lines L4 to L7 described under Variants, and closed forms for the exact bootstrap variance of the mean, which the tests compare with full enumeration.

## Example

A series of $n = 120$ values from the AR(1) model $X_t = 0.5\, X_{t-1} + \varepsilon_t$ with standard normal $\varepsilon_t$, started in its stationary law (seed 2024), has mean $\bar x = 0.248$. For this model the true standard error of $\bar x$ is $0.182$; see [autoregressive model](/autoregressive-model/). The bootstrap estimates of the standard error are:

| method | standard error of $\bar x$ |
|---|---|
| iid bootstrap ($l = 1$), exact | 0.104 |
| moving blocks, $l = 5$, exact | 0.145 |
| moving blocks, $l = 5$, $b = 2000$ (seed 1) | 0.150 |
| circular blocks, $l = 5$, $b = 2000$ (seed 1) | 0.147 |
| stationary, $p = 1/5$, exact | 0.156 |
| stationary, $p = 1/5$, $b = 2000$ (seed 1) | 0.160 |

The iid bootstrap is far too small. For an AR(1) process with coefficient $\phi$ the variance of the mean is about $\frac{1 + \phi}{1 - \phi}$ times what independence would give, so the iid bootstrap variance is too small by the factor $\frac{1 - \phi}{1 + \phi} = \frac13$.

**Choice of block length (measured).** For 2000 such series, the ratio of the exact moving block bootstrap variance of $\bar x$ to the true variance had this mean and root mean squared error (seed 12):

| $l$ | 1 | 2 | 4 | 5 | 8 | 12 | 20 | 30 | 40 |
|---|---|---|---|---|---|---|---|---|---|
| mean ratio | 0.33 | 0.49 | 0.66 | 0.71 | 0.77 | 0.79 | 0.76 | 0.67 | 0.56 |
| RMSE | 0.67 | 0.52 | 0.38 | 0.36 | 0.35 | 0.39 | 0.49 | 0.59 | 0.65 |

Short blocks break too much dependence (bias), and long blocks leave too few distinct blocks (variance and, for very long blocks, a downward bias from centring at the mean of few blocks). The best values are near $l = 5$ to $8$, close to $n^{1/3} = 4.9$. The stationary bootstrap with $p = 1/l$ gave a slightly larger RMSE at each of these lengths.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). What is proved:

- When $l$ divides $n$, the resample mean of the moving block bootstrap is the average of $k$ independent uniform draws from the $N$ block means $\bar B_1, \ldots, \bar B_N$. So its exact bootstrap mean is $\bar B = \frac1N\sum_i \bar B_i$ and its exact bootstrap variance is $\frac{1}{k} \cdot \frac{1}{N}\sum_i (\bar B_i - \bar B)^2$. The tests compare this with all $N^k$ block choices.
- $\bar B \ne \bar x$ in general: the moving blocks give less weight to the first and last $l - 1$ observations. The circular and the stationary bootstraps are exactly centred, $E^*\bar x^* = \bar x$.
- The stationary bootstrap resample is a stationary sequence given the data, and $\mathrm{Var}^*(\bar x^*) = \frac{\hat c(0)}{n} + \frac{2}{n}\sum_{i=1}^{n-1}\bigl(1 - \frac in\bigr)(1 - p)^i \hat c(i)$, with circular sample autocovariances $\hat c(i)$. The tests check this against all $n^n$ index paths.

What is not proved here: consistency. Künsch (1989) proved that, under mixing and moment conditions, the block bootstrap variance of a smooth function of means is consistent when $l \to \infty$ and $l/n \to 0$. The tables above are measurements.

## Complexity

Each replicate copies $n$ values in $k$ blocks and evaluates $s$, which costs $\Theta(n)$ for the mean, so the time is $\Theta(b n)$. The extra space is $\Theta(n)$ for one resample and $\Theta(b)$ for the replicates. For the mean, the exact bootstrap variances need no resampling: the moving block closed form costs $\Theta(n)$ with prefix sums for the block means, and the stationary bootstrap formula costs $\Theta(n^2)$ for the $n$ circular autocovariances.

## Properties

- **Keeps dependence inside blocks.** The resample has the original joint law of up to $l$ consecutive values within each block and independence between blocks.
- **Block length trade-off.** For the variance of the mean, the bias of the block bootstrap estimate is of order $1/l$ and its variance of order $l/n$, so the mean squared error is smallest for $l$ of order $n^{1/3}$. For one-sided and two-sided distribution functions the optimal orders are $n^{1/4}$ and $n^{1/5}$ (Hall, Horowitz and Jing 1995). The constants depend on the autocorrelation and must be estimated.
- **End effects.** The moving block bootstrap is not centred at $\bar x$, which matters for bootstrap-t intervals and tests; centre at $\bar B$ instead.
- **The stationary bootstrap is less sensitive to $l$** than fixed blocks, but for the same mean block length its mean squared error is somewhat larger.
- **Long-range dependence and nonstationarity** are outside the basic theory: for long-memory processes the block bootstrap of the mean can fail, and trends must be removed first.

## Variants and improvements

- **Stationary bootstrap** (Politis and Romano 1994). Start at a uniform random position. At each step, with probability $p$ jump to a new uniform position, otherwise move to the next value, wrapping from $x_n$ to $x_1$. The blocks have geometric lengths with mean $1/p$. Given the data, the index sequence is a Markov chain started in its uniform stationary law, so the resampled series is stationary, which gives the method its name, and it is exactly centred.
- **Circular block bootstrap** (Politis and Romano 1992). Wrap the series into a circle so that all $n$ positions start a block of length $l$. Every value has the same weight, and the resample mean is exactly centred at $\bar x$.
- **Non-overlapping blocks** (Carlstein 1986). Use only the $n/l$ disjoint blocks. It is simpler, but its variance estimate is less efficient than that of overlapping blocks.
- **Blocks of blocks.** For a statistic that depends on the joint law of $m$ consecutive values, such as a lag-$m$ autocorrelation, first form the vectors $(x_t, \ldots, x_{t+m-1})$, then resample blocks of these vectors (Künsch 1989).
- **Sieve bootstrap.** Fit an [autoregressive model](/autoregressive-model/) of growing order, resample its residuals and generate new series from the fitted model. It is a [parametric bootstrap](/parametric-bootstrap/) with a model that grows with $n$, and it works well for linear processes.
- **Block subsampling.** Compute the statistic on each of the $N$ blocks of length $m$ without resampling; see [subsampling](/subsampling-inference/). It needs fewer conditions than the block bootstrap.
- **Block length selection.** Plug-in rules estimate the constants of the $n^{1/3}$ rule from the autocorrelations of the data.

## When to use it

Use it for standard errors and confidence intervals of statistics of a stationary, weakly dependent series: means, autocorrelations, quantiles, regression coefficients with dependent errors, and the output of a Markov chain Monte Carlo run, where the [effective sample size](/effective-sample-size/) and [MCMC autocorrelation](/mcmc-autocorrelation/) pages give model-based alternatives. Use the iid bootstrap only after checking that the [autocorrelation](/autocorrelation/) is negligible. If a good parametric time series model is available, the sieve or model-based bootstrap is often more accurate.

## Pitfalls

- **Ignoring the dependence.** With positive autocorrelation the iid bootstrap is overconfident; in the example its standard error is $0.104$ against a true $0.182$.
- **Block length chosen by eye.** Results can change a lot with $l$. Report the rule used, and check a few lengths around it.
- **Too few blocks.** With $l$ close to $n$, there are few distinct blocks, and the bootstrap distribution is very discrete and centred badly.
- **Centring in the moving block bootstrap.** Bootstrap-t statistics should use $\bar B$, not $\bar x$, as the centre, or the circular version.
- **Trends and seasonality.** Blocks of a nonstationary series mix different regimes. Remove the trend and the seasonal pattern first, or resample residuals of a model.

## Implementations

## History

Edward Carlstein (1986) used non-overlapping blocks to estimate the variance of a statistic of a time series. Hans Künsch (1989) introduced the moving block bootstrap with overlapping blocks, together with a blockwise jackknife, and proved its consistency; Regina Liu and Kesar Singh developed the same method independently, published in 1992. Dimitris Politis and Joseph Romano proposed the circular block bootstrap in 1992 and the stationary bootstrap in 1994, to remove the end effects and to make the resampled series stationary. Peter Hall, Joel Horowitz and Bing-Yi Jing (1995) derived the optimal orders of the block length, and S. N. Lahiri's 2003 book collected the theory.

## References
