---
tag: 1XEA6P
kind: algorithm
slug: innovations-algorithm
name: Innovations algorithm
aliases:
- Brockwell-Davis innovations algorithm
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: Computes one-step predictors and their error variances from a covariance function by orthogonalizing the observations. It gives the exact Gaussian likelihood.
model: real-ram
complexity:
  vars: {n: the number of observations, q: the band width of the covariance (the MA order)}
  time: {worst: Θ(n^3), banded: Θ(n q^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1987
  people: [Peter J. Brockwell, Richard A. Davis, Craig F. Ansley]
  note: Ansley (1979) computed the exact ARMA likelihood from the Cholesky factor of a banded covariance matrix. Brockwell and Davis presented the recursion for one-step predictors under the name innovations algorithm in the 1987 first edition of their book.
prereqs: [linear-prediction, cholesky-decomposition]
see_also: [yule-walker-equations, levinson-durbin-recursion, kalman-filter, moving-average-model, arma-model, gram-schmidt-process, prediction-error-method, wold-decomposition-theorem]
sources:
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 5.2 (the innovations algorithm, pp. 169 to 174), Section 5.3 (recursive prediction of an ARMA process, p. 175), Section 8.3 (preliminary MA estimates by the innovations algorithm, p. 245) and Section 8.6 (recursive calculation of the Gaussian likelihood, p. 254)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 2.5.4 (the innovations algorithm, p. 62), Section 5.1.3 (MA estimation, p. 132) and Section 5.2 (maximum likelihood, p. 139)
  - paper: doi:10.1093/biomet/66.1.59
    title: Craig F. Ansley, An algorithm for the exact likelihood of a mixed autoregressive-moving average process, Biometrika 66(1), 1979
    locator: pp. 59 to 65 (the Cholesky factor of the banded covariance of the transformed process)
---

The innovations algorithm turns a covariance function into one-step predictions. Given $\kappa(i, j) = \mathbb{E}[X_i X_j]$ for a series $X_1, X_2, \ldots$ with mean 0, it computes the best linear predictor $\hat X_{m+1}$ of each value from the ones before it, and the mean squared error $v_m$ of that prediction. The predictors are written in terms of the past prediction errors $X_j - \hat X_j$, called innovations, which are uncorrelated. This makes the recursion a Gram-Schmidt orthogonalization of the observations, or equally an $LDL^\top$ [Cholesky](/cholesky-decomposition/) factorization of their covariance matrix. Unlike the [Levinson-Durbin recursion](/levinson-durbin-recursion/), it does not need stationarity. For a [moving-average](/moving-average-model/) process of order $q$ the covariance is banded and the work falls from $\Theta(n^3)$ to $\Theta(n q^2)$. The errors and variances give the exact Gaussian likelihood, so the algorithm is the standard way to fit [MA](/moving-average-model/) and [ARMA](/arma-model/) models by maximum likelihood.

## In plain words

Watch a series one value at a time and predict the next value from all you have seen. When the value arrives, the gap between it and your prediction is the new information it brings, the innovation. Innovations from different times are unrelated to each other, so you can build each new prediction as a weighted sum of the past innovations, with weights that the covariances tell you. The recursion finds these weights one time step at a time. It also tells you how large each prediction error should be, and that is all the likelihood of normal data needs. If values far apart in time are unrelated, most weights are zero and the work is small.

## The problem

**Model.** $X_1, \ldots, X_n$ have mean 0 and known covariance $\kappa(i, j) = \mathbb{E}[X_i X_j]$. The covariance matrix $K_n = [\kappa(i, j)]_{i,j=1}^n$ is positive definite. Stationarity is not needed. For a stationary series, $\kappa(i, j) = \gamma(i - j)$.

**Output.** For $m = 0, \ldots, n - 1$, the coefficients $\theta_{m1}, \ldots, \theta_{mm}$ and the error variances $v_m$ such that

$$\hat X_1 = 0, \qquad \hat X_{m+1} = \sum_{j=1}^{m} \theta_{mj}\,(X_{m+1-j} - \hat X_{m+1-j}), \qquad v_m = \mathbb{E}[(X_{m+1} - \hat X_{m+1})^2],$$

where $\hat X_{m+1}$ is the best linear predictor of $X_{m+1}$ from $X_1, \ldots, X_m$.

**Uses.**

- **Prediction.** The predictors follow from the data and the $\theta_{mj}$ in $O(n^2)$ more operations, or $O(nq)$ when the covariance has band width $q$.
- **Likelihood.** For Gaussian data,
$$-2\log L = n \log(2\pi) + \sum_{j=1}^{n} \log v_{j-1} + \sum_{j=1}^{n} \frac{(X_j - \hat X_j)^2}{v_{j-1}},$$
with no matrix inverse or determinant.
- **MA estimation.** Run on the sample autocovariances, $\hat\theta_{m1}, \ldots, \hat\theta_{mq}$ estimate the MA($q$) coefficients when $m$ is large (Brockwell and Davis 1991, Section 8.3).

## The algorithm

```pseudo id=main
INNOVATIONS(κ, n)
L1  v[0] ← κ(1, 1)
L2  for m ← 1 to n - 1 do
L3      for k ← 0 to m - 1 do
L4          s ← κ(m+1, k+1) - Σ_{j=0}^{k-1} θ[k][k-j] · θ[m][m-j] · v[j]
L5          θ[m][m-k] ← s / v[k]
L6      v[m] ← κ(m+1, m+1) - Σ_{j=0}^{m-1} θ[m][m-j]² · v[j]
L7  return (θ, v)
```

For a covariance with band width $q$ ($\kappa(i, j) = 0$ when $|i - j| > q$), start the loops in L3, L4 and L6 at $\max(0, m - q)$ instead of 0; the skipped coefficients are 0. The code takes `q` as an optional argument for this. Line L5 divides by $v[k]$, which is positive when $K_n$ is positive definite. The code raises an error if some $v_m \le 0$. It uses only the four field operations, so it runs exactly on `Fraction` values.

## Example

Take the MA(1) process $X_t = \varepsilon_t + \frac12 \varepsilon_{t-1}$ with $\sigma^2 = 1$, so $\gamma(0) = 5/4$, $\gamma(1) = 1/2$ and $\gamma(h) = 0$ for $h \ge 2$.

- $v_0 = 5/4$.
- $m = 1$: $\theta_{11} = \gamma(1)/v_0 = 2/5$, and $v_1 = 5/4 - (2/5)^2 \cdot 5/4 = 21/20$.
- $m = 2$: $\theta_{22} = \kappa(3, 1)/v_0 = 0$, then $\theta_{21} = (1/2 - \theta_{11}\theta_{22}v_0)/v_1 = 10/21$, and $v_2 = 5/4 - (10/21)^2 \cdot 21/20 = 85/84$.
- $m = 3$: $\theta_{31} = 42/85$, $\theta_{32} = \theta_{33} = 0$, $v_3 = 341/340$.

In general $v_m = S_{m+1}/S_m$ and $\theta_{m1} = \theta/v_{m-1}$ with $S_m = 1 + \theta^2 + \cdots + \theta^{2m}$ and $\theta = 1/2$, so $v_m \to 1 = \sigma^2$ and $\theta_{m1} \to 1/2$.

Now observe $x = (1, -1, 2)$.

| $j$ | $x_j$ | $\hat x_j$ | innovation $x_j - \hat x_j$ | $v_{j-1}$ |
|---|---|---|---|---|
| 1 | 1 | 0 | 1 | 5/4 |
| 2 | -1 | $\frac25 \cdot 1 = 0.4$ | $-1.4$ | 21/20 |
| 3 | 2 | $\frac{10}{21} \cdot (-1.4) = -\frac23$ | $\frac83$ | 85/84 |
| 4 | | $\frac{42}{85} \cdot \frac83 = \frac{112}{85} = 1.3176$ | | 341/340 |

The quadratic form is $1/(5/4) + 1.96/(21/20) + (64/9)/(85/84) = 824/85 = 9.6941$, and the product of the variances is $85/64 = \det K_3$. So $-2\log L = 3\log(2\pi) + \log(85/64) + 9.6941 = 15.4915$. The tests check these values against the determinant and the inverse of $K_3$ in exact arithmetic.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The innovations $U_j = X_j - \hat X_j$ are orthogonal and span the same space as $X_1, \ldots, X_j$, so $\hat X_{m+1}$ is the sum of the projections of $X_{m+1}$ on each $U_{k+1}$, with coefficient $\langle X_{m+1}, U_{k+1}\rangle / v_k$. Expanding $U_{k+1}$ by its own predictor gives line L4, and Pythagoras gives line L6. In matrix form, $X = C U$ with $C$ unit lower triangular, so $K_n = C D C^\top$ with $D = \operatorname{diag}(v_0, \ldots, v_{n-1})$. This proves the likelihood formula. A banded covariance makes $X_{m+1}$ orthogonal to every $U_{k+1}$ with $m - k > q$, which justifies the shortened loops.

## Complexity

- **Full recursion.** L4 and L6 do $\sum_{m=1}^{n-1}(m^2 + m) = (n - 1)n(n + 1)/3$ multiplications, counting both products in each term, so the time is $\Theta(n^3)$, the same order as the [Cholesky decomposition](/cholesky-decomposition/) it is equivalent to. A run with a counting number type gave 330 multiplications for $n = 10$ and 170640 for $n = 80$, equal to the formula.
- **Banded, MA($q$).** Each step $m$ costs about $q(q + 1)$ multiplications, so the total is about $n q(q + 1)$, which is $\Theta(n q^2)$ and $2n$ for $q = 1$. Measured counts for $n = 100$ were 198, 590, 1172 and 1940 for $q = 1, 2, 3, 4$, just under $n q(q + 1) = 200, 600, 1200, 2000$.
- **Predictions.** Given the coefficients, the $n$ predictors cost $\Theta(n^2)$, or $\Theta(nq)$ in the banded case.
- **Space.** The code keeps all rows of $\theta$, which is $\Theta(n^2)$. The banded case needs only the last $q$ rows and the last $q$ variances, $O(q^2)$ for the recursion, if the predictors are computed on the fly.

For a stationary series with no band, the Durbin-Levinson recursion finds the same predictors in $\Theta(n^2)$, so the innovations algorithm is the better choice only for banded or nonstationary covariances.

## Properties

- **Exact.** In exact arithmetic it returns the exact predictors, error variances and likelihood. There is no truncation, and no stationary start-up assumption: the first predictions use only the data actually seen.
- **Online.** Step $m$ uses only $\kappa(i, j)$ for $i, j \le m + 1$, so a new observation adds one step, which costs $O(m^2)$ in general and $O(q^2)$ in the banded case.
- **Convergence to the Wold quantities.** For a stationary invertible MA($q$) process, $v_m \to \sigma^2$ and $\theta_{mj} \to \theta_j$ as $m \to \infty$. The rate is geometric when the roots of $\theta(z)$ are outside the unit circle. For MA(1) with $\theta = 1$, which is not invertible, $v_m = \sigma^2 (m + 2)/(m + 1)$, so the convergence is only like $1/m$.
- **Preliminary MA estimates (measured).** MA(1) with $\theta = 0.5$, $\hat\theta_{m1}$ from the sample autocovariances, 200 series per row:

  | $n$ | $m$ | mean | sd | $1/\sqrt{n}$ | maximum likelihood sd $\sqrt{(1 - \theta^2)/n}$ |
  |---|---|---|---|---|---|
  | 200 | 5 | 0.4902 | 0.0746 | 0.0707 | 0.0612 |
  | 200 | 10 | 0.4891 | 0.0704 | 0.0707 | 0.0612 |
  | 200 | 20 | 0.4989 | 0.0682 | 0.0707 | 0.0612 |
  | 1000 | 5 | 0.4957 | 0.0345 | 0.0316 | 0.0274 |
  | 1000 | 10 | 0.4972 | 0.0332 | 0.0316 | 0.0274 |
  | 1000 | 20 | 0.4970 | 0.0350 | 0.0316 | 0.0274 |

  The theory (Brockwell and Davis 1991, Section 8.3) gives $\sqrt{n}(\hat\theta_{m1} - \theta_1) \to N(0, 1)$ when $m \to \infty$ slowly with $n$, so the asymptotic variance is $1/n$, not the $(1 - \theta^2)/n$ of maximum likelihood. The simulation agrees: the estimate is consistent but not efficient, and it is a good start for the likelihood search.

## Variants and improvements

- **ARMA processes.** For a causal ARMA($p$, $q$) process, apply the recursion to $W_t = \sigma^{-1}X_t$ for $t \le m$ and $W_t = \sigma^{-1}\phi(B)X_t$ for $t > m$, with $m = \max(p, q)$. The covariance of $W$ is banded after the first $m$ rows, so the cost is $O(n m^2)$ (Brockwell and Davis 1991, Section 5.3). This is Ansley's method for the exact ARMA likelihood.
- **Durbin-Levinson recursion.** For stationary series it computes the predictor coefficients on $X$ instead of on the innovations, in $\Theta(n^2)$; see the [Yule-Walker equations](/yule-walker-equations/) and [Levinson-Durbin recursion](/levinson-durbin-recursion/) pages.
- **Kalman filter.** For a process in state space form, the [Kalman filter](/kalman-filter/) produces the same innovations and variances in $O(n r^3)$ for a state of dimension $r$, and also handles missing values and nonstationary starts.
- **Multivariate series.** The same recursion holds with matrices: $\Theta_{mj}$ are $k \times k$ matrices and $V_m$ are covariance matrices.
- **Preliminary ARMA estimates.** Combining the innovations estimates of the MA($\infty$) weights $\psi_j$ with the relation $\psi(z)\phi(z) = \theta(z)$ gives preliminary ARMA estimates (Brockwell and Davis 1991, Section 8.4).

## When to use it

Use it to compute the exact Gaussian likelihood or exact finite-sample forecasts of an MA or ARMA model, and for nonstationary covariances where Durbin-Levinson does not apply. It is the core of the [prediction error method](/prediction-error-method/) for these models. For a long stationary AR series, use Durbin-Levinson. For models with missing data, regression effects or time-varying parameters, a state space form with the Kalman filter is usually easier.

## Pitfalls

- **Indices.** The book indexes $\theta_{mj}$ by the step $m$ and the lag $j$ of the innovation, so $\theta[m][m-k]$ in L5 is the weight on the innovation $U_{k+1}$. Mixing the two indices is the most common error.
- **The cost without a band.** The full recursion is cubic, not quadratic. It is the predictor step, once the coefficients are known, that is quadratic.
- **A covariance that is not positive definite.** Sample autocovariances with the divisor $n - h$ can give a negative $v_m$. Use the divisor $n$.
- **Noninvertible MA models.** With a root of $\theta(z)$ on the unit circle, $v_m$ converges to $\sigma^2$ slowly and the estimates of $\theta$ often pile up at the boundary. Restrict the search to the invertible region.
- **Floating point.** The recursion is a Cholesky factorization in disguise and has the same rounding behaviour. Its error grows with the condition number of $K_n$, which is large when the spectral density is close to 0 at some frequency.

## Implementations

## History

The innovations idea comes from filtering theory, where Kailath's innovations approach of the late 1960s wrote linear estimation in terms of the uncorrelated prediction errors. For time series models, Ansley (1979) computed the exact Gaussian likelihood of an ARMA process by a Cholesky factorization of the banded covariance matrix of $\phi(B)X_t$. Brockwell and Davis gave the recursion for one-step predictors its standard form and name in the 1987 first edition of Time Series: Theory and Methods, together with its use for MA estimation and recursive likelihood evaluation. Their textbooks made it a standard tool, beside the Durbin-Levinson recursion and the Kalman filter.

## References
