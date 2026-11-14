---
tag: 6A6QRB
kind: algorithm
slug: split-conformal-prediction
name: Split conformal prediction
aliases:
- inductive conformal prediction
area: statistics-and-inference/nonparametric-and-robust-statistics
level: research
summary: Fit the model on one part of the data, compute residual scores on the other, and widen predictions by their quantile. It gives finite-sample marginal coverage cheaply.
model: real-ram
complexity:
  vars: {n: the number of data points, f: the time to fit the model on the training part and predict at the calibration points}
  time: {worst: Θ(f + n log n), best: Θ(f + n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true, exact: true, online: false, recursive: false}
history:
  year: 2002
  people: [Harris Papadopoulos, Kostas Proedrou, Vladimir Vovk, Alex Gammerman]
  note: Papadopoulos, Proedrou, Vovk and Gammerman introduced inductive conformal prediction for regression in 2002; Lei, G'Sell, Rinaldo, Tibshirani and Wasserman (2018) named it split conformal and proved the upper bound on its coverage.
prereqs: [conformal-prediction, prediction-interval, quantile, order-statistic]
see_also: [cross-validation, quantile-regression, linear-regression, permutation-test, jackknife-resampling, random-sampling, quickselect, fisher-yates-shuffle]
sources:
  - paper: doi:10.1007/3-540-36755-1_29
    title: Harris Papadopoulos, Kostas Proedrou, Volodya Vovk and Alex Gammerman, Inductive confidence machines for regression, Machine Learning, ECML 2002, Lecture Notes in Computer Science 2430, Springer, 2002
    locator: pp. 345 to 356 (the inductive, or split, procedure for regression with a ridge regression model)
  - paper: doi:10.1080/01621459.2017.1307116
    title: Jing Lei, Max G'Sell, Alessandro Rinaldo, Ryan J. Tibshirani and Larry Wasserman, Distribution-free predictive inference for regression, Journal of the American Statistical Association 113(523), 2018
    locator: Section 2.2 and Theorem 2.2 (split conformal coverage, between 1 - alpha and 1 - alpha + 2/(n + 2) with n/2 calibration points and continuous residuals)
  - book: isbn:9780387001524
    title: Vladimir Vovk, Alex Gammerman and Glenn Shafer, Algorithmic Learning in a Random World, Springer, 2005
    locator: Chapter 4 (modifications of conformal predictors, including inductive conformal predictors), general locator
  - paper: "Yaniv Romano, Evan Patterson and Emmanuel J. Candès, Conformalized quantile regression, Advances in Neural Information Processing Systems 32, 2019"
    title: Yaniv Romano, Evan Patterson and Emmanuel J. Candès, Conformalized quantile regression, 2019
    locator: the CQR score max(lo(x) - y, y - hi(x)) and its coverage guarantee
  - paper: doi:10.1093/imaiai/iaaa017
    title: Rina Foygel Barber, Emmanuel J. Candès, Aaditya Ramdas and Ryan J. Tibshirani, The limits of distribution-free conditional predictive inference, Information and Inference 10(2), 2021
    locator: pp. 455 to 482 (coverage conditional on x is not possible without assumptions)
  - paper: doi:10.1561/2200000101
    title: Anastasios N. Angelopoulos and Stephen Bates, Conformal prediction, a gentle introduction, Foundations and Trends in Machine Learning 16(4), 2023
    locator: pp. 494 to 591 (split conformal with many scores, and the Beta law of the coverage given the calibration set)
---

Split conformal prediction builds a prediction interval around any fitted model with a coverage guarantee that holds for every sample size and every distribution. It fits the model once on a training part of the data, computes the absolute residuals on the other part, the calibration set, and widens each prediction by $q$, the $\lceil (n_2 + 1)(1 - \alpha) \rceil$-th smallest of the $n_2$ calibration residuals. If the data and the new point are exchangeable, the interval holds the new response with probability at least $1 - \alpha$, and at most $1 - \alpha + 1/(n_2 + 1)$ when the residuals have no ties. It costs one fit, where [full conformal prediction](/conformal-prediction/) needs one fit for each candidate response.

## In plain words

Split your data in two piles. Train any model you like on the first pile. Then use the model on the second pile, where you know the answers, and write down how far off each prediction was.

Sort those errors. For a 90% interval, take an error size that about 90% of the errors do not exceed; the exact rank is fixed by a small formula. For a new input, predict with the model and add and subtract that error size.

The new case is just like one more member of the second pile. Its error is equally likely to land anywhere in the sorted list, so it is bigger than the chosen error only about 10% of the time. That holds whatever the model is, and however good or bad it is. A bad model only makes the interval wider.

## The problem

Given data $Z_i = (X_i, Y_i)$, $i = 1, \ldots, n$, a new input $X_{n+1}$, a learning algorithm that maps a data set to a predictor $\hat\mu$, and a level $\alpha \in (0, 1)$, find an interval $C(X_{n+1})$ with

$$P\bigl(Y_{n+1} \in C(X_{n+1})\bigr) \ge 1 - \alpha$$

whenever $Z_1, \ldots, Z_{n+1}$ are exchangeable, with no other assumption about their law or about $\hat\mu$. The probability is over the data, the new point and the random split. This is a [prediction interval](/prediction-interval/) for a new response, not a confidence interval for a parameter, and its coverage is marginal: averaged over $X_{n+1}$.

## The algorithm

```pseudo id=main
SPLIT-CONFORMAL(z_1, ..., z_n, n_1, fit, α)
L1  split {1, ..., n} at random into I_1 of size n_1 and I_2 of size n_2 = n - n_1
L2  μ̂ ← fit({z_i : i ∈ I_1})
L3  R_i ← |y_i - μ̂(x_i)| for each i ∈ I_2
L4  k ← ⌈(n_2 + 1)(1 - α)⌉
L5  if k > n_2 then q ← ∞
L6  else q ← the k-th smallest of {R_i : i ∈ I_2}
L7  return x ↦ [μ̂(x) - q, μ̂(x) + q]
```

Line L1 is a random [shuffle](/fisher-yates-shuffle/) and a cut; any split that does not look at the data works, and so does a fixed split of data in random order. The fit of line L2 can be any procedure at all, as long as it sees only the training part. Line L6 is a [selection](/quickselect/) of one [order statistic](/order-statistic/). Line L5 is needed: with fewer than $1/\alpha - 1$ calibration points, no finite $q$ is guaranteed to work, and the honest answer is the whole line.

## Example

Forty points with $x$ uniform on $[0, 10]$ and $y = 1 + 0.5x + \varepsilon$, $\varepsilon$ standard normal (`random.Random(2026)`), were split by `random.Random(1)` into $n_1 = 20$ training and $n_2 = 20$ calibration points. A least squares line was fitted on the training part.

- For $\alpha = 0.1$: $k = \lceil 21 \cdot 0.9 \rceil = \lceil 18.9 \rceil = 19$, so $q$ is the 19th smallest of the 20 absolute calibration residuals, $q = 1.565$. At $x = 5$ the line predicts $3.33$ and the interval is $[1.76, 4.90]$. For comparison, the ideal 90% half width for standard normal errors with a known line is $1.645$.
- For $\alpha = 0.2$: $k = \lceil 21 \cdot 0.8 \rceil = 17$ and $q = 1.469$.
- With the same data and $n_2 = 10$: $k = \lceil 11 \cdot 0.9 \rceil = 10$, and $q = 1.738$ is the largest calibration residual.
- With $n_2 = 4$: $k = \lceil 5 \cdot 0.9 \rceil = 5 > 4$, so line L5 sets $q = \infty$.

**Coverage, measured.** The theorem gives the exact value $k/(n_2 + 1)$ for continuous errors, so these runs only check the code. Each row has 4000 data sets with one new point each, $\alpha = 0.1$ and a least squares line.

| errors | $n$ | $n_2$ | $k/(n_2 + 1)$ | measured coverage | median width $2q$ | seed |
|---|---|---|---|---|---|---|
| normal | 40 | 20 | $19/21 = 0.905$ | 0.908 | 3.65 | 3 |
| Cauchy | 40 | 20 | $19/21 = 0.905$ | 0.906 | 19.6 | 4 |
| normal | 200 | 100 | $91/101 = 0.901$ | 0.909 | 3.37 | 5 |
| normal | 40 | 10 | $10/11 = 0.909$ | 0.920 | 3.80 | 6 |

The coverage stays at its level even with Cauchy errors, where least squares is a poor fit; the intervals are then wide. With 4000 data sets the standard error of each measured value is about $0.0046$.

## Correctness

The proof is in the [correctness file](proofs/correctness.md). Fix the training part. Then $\hat\mu$ is fixed, and the $n_2$ calibration scores and the score $R_{n+1} = \lvert Y_{n+1} - \hat\mu(X_{n+1}) \rvert$ of the new point are $n_2 + 1$ exchangeable numbers. The new point is covered exactly when $R_{n+1}$ is at most the $k$-th smallest calibration score, and that happens when at most $k - 1$ calibration scores are strictly smaller than $R_{n+1}$. At least $k$ of the $n_2 + 1$ scores have this property, and exactly $k$ when they are distinct, so by exchangeability

$$1 - \alpha \le \frac{k}{n_2 + 1} \le P\bigl(Y_{n+1} \in C(X_{n+1})\bigr),$$

with equality in the second step for distinct scores. Since $k < (n_2 + 1)(1 - \alpha) + 1$, the coverage with continuous scores is then below $1 - \alpha + 1/(n_2 + 1)$. Lei et al. (2018, Theorem 2.2) state the upper bound as $1 - \alpha + 2/(n + 2)$ for an even split, $n_2 = n/2$, which is the same number.

The tests check the exact coverage by exchangeability: for six calibration and test points they enumerate all $720$ orderings and get exactly $k/6$ for each $\alpha$ when the scores are distinct, and at least $1 - \alpha$ with tied scores.

## Complexity

With $f$ the cost of the fit and of the $n_2$ predictions, the method takes $\Theta(f + n \log n)$ time with sorting at line L6, or $\Theta(f + n)$ with a linear-time selection, and $\Theta(n)$ extra space. After that, each new point costs one prediction. Full conformal prediction needs a refit for every candidate response and every new point.

## Properties

- **Finite-sample, distribution-free.** The coverage bounds hold for every $n$, every law of the data and every model, under exchangeability only.
- **Marginal only.** The probability is over the training data, the calibration data and the new point. It does not hold for each $x$, and no method can achieve coverage at each $x$ for every law with intervals of finite expected length (Barber et al. 2021).
- **Random given the calibration set.** For continuous scores, the coverage conditional on the training and calibration data is $F(q)$, where $F$ is the law of a new score. It has the Beta law with parameters $k$ and $n_2 + 1 - k$, with mean $k/(n_2 + 1)$. For $n_2 = 20$ and $\alpha = 0.1$ its standard deviation is $0.063$ and it is below $0.85$ with probability $0.18$; for $n_2 = 100$ the standard deviation is $0.030$; for $n_2 = 1000$ it is $0.0095$.
- **Constant width.** With the absolute residual score the interval has the same width $2q$ at every $x$. Other scores change this; see the variants.
- **Uses only part of the data to fit.** The fitted model is worse than one fitted on all $n$ points, so the intervals are usually a little wider than those of full conformal prediction.

## Variants and improvements

- **Conformalized quantile regression** (Romano, Patterson and Candès 2019). Fit lower and upper [quantile regressions](/quantile-regression/) $\hat q_{\mathrm{lo}}$ and $\hat q_{\mathrm{hi}}$ at levels $\alpha/2$ and $1 - \alpha/2$ on the training part. Use the score $E_i = \max\bigl(\hat q_{\mathrm{lo}}(x_i) - y_i,\ y_i - \hat q_{\mathrm{hi}}(x_i)\bigr)$ and return $[\hat q_{\mathrm{lo}}(x) - q, \hat q_{\mathrm{hi}}(x) + q]$. The guarantee is the same, and the width now follows the spread of $y$ given $x$. In the heteroscedastic example under Pitfalls, with 8-bin empirical quantiles as the quantile fit, the coverage was $0.941$ for $\lvert x \rvert < 0.25$ and $0.887$ for $\lvert x \rvert > 0.75$, against $1.000$ and $0.760$ for the absolute residual score.
- **Scaled residuals.** Use $\lvert y - \hat\mu(x) \rvert/\hat\sigma(x)$ with a fitted spread $\hat\sigma$, and return $\hat\mu(x) \pm q\,\hat\sigma(x)$.
- **Classification.** Use a score such as one minus the fitted probability of the true label, and return all labels whose score is at most $q$.
- **Cross-conformal, jackknife+ and CV+.** Use every point for both fitting and calibration through K folds or leave-one-out fits, as in [cross-validation](/cross-validation/). They give narrower intervals with a weaker worst-case guarantee, at least $1 - 2\alpha$ for the jackknife+ and CV+.
- **Label-conditional (Mondrian) calibration.** Calibrate separately within each class or group, which gives coverage within each group if each group has enough calibration points.
- **Full conformal prediction.** [Conformal prediction](/conformal-prediction/) refits on each candidate. It uses all the data for fitting at a much higher cost.

## When to use it

Use split conformal prediction when you have a model you trust for point prediction, enough data to set aside a calibration set of a few hundred points, and a need for intervals whose coverage does not rest on model assumptions. It is the usual choice for large models, where a refit for each candidate is not possible. With very little data, prefer the jackknife+ or full conformal prediction, which use all points for fitting. If you need coverage for each $x$ or for each subgroup, the plain method does not give it; use group-wise calibration or an adaptive score and check the coverage in each group.

## Pitfalls

- **Marginal coverage only.** With $x$ uniform on $[-1, 1]$, errors with standard deviation $0.1 + \lvert x \rvert$, $n = 400$ split $200/200$, $\alpha = 0.1$ and 3000 data sets (seed 7), the overall coverage was $0.905$, but $1.000$ for $\lvert x \rvert < 0.25$ and $0.760$ for $\lvert x \rvert > 0.75$.
- **Wrong rank.** Taking the $\lceil n_2(1 - \alpha) \rceil$-th score, the plain empirical quantile, gives coverage $\lceil n_2(1 - \alpha)\rceil/(n_2 + 1)$, which can be below $1 - \alpha$: for $n_2 = 20$ and $\alpha = 0.1$ it is $18/21 = 0.857$. The $+1$ counts the new point.
- **Reusing the training data.** Residuals on the training part are too small, because the model was fitted to them. Calibrating on them gives intervals that are too short.
- **Choosing the split, the model or $\alpha$ after looking at the calibration set.** Any choice that depends on the calibration scores breaks exchangeability.
- **Small calibration sets.** The guarantee holds on average over calibration sets, and for a single small calibration set the actual coverage varies a lot (see Properties). Use at least a few hundred calibration points when a single deployed interval matters.
- **Exchangeability fails.** Drift over time and covariate shift between training and use break the argument.

## Implementations

## History

Vladimir Vovk, Alex Gammerman and Glenn Shafer developed conformal prediction in the late 1990s and early 2000s. Its main cost was one refit for each candidate. In 2002 Harris Papadopoulos, Kostas Proedrou, Vovk and Gammerman proposed the inductive version, which fits once on a training set and calibrates on the rest, and applied it to ridge regression. Vovk, Gammerman and Shafer treated inductive conformal predictors in their 2005 book. Jing Lei, Max G'Sell, Alessandro Rinaldo, Ryan Tibshirani and Larry Wasserman (2018) studied the method for regression under the name split conformal, proved the upper bound on its coverage and compared it with full conformal prediction. Romano, Patterson and Candès (2019) combined it with quantile regression. Because it needs only one fit, it is the form of conformal prediction that is used with large models.

## References
