---
tag: GHRJ1G
kind: algorithm
slug: stl-decomposition
name: STL decomposition
aliases:
- seasonal-trend decomposition using LOESS
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: Cleveland's decomposition of a series into trend, seasonal and remainder parts by alternating LOESS smoothers in an inner and a robust outer loop.
model: real-ram
complexity:
  vars: {n: the length of the series, m: the seasonal period, s: "the seasonal span n_s, counted up to the number of cycles", u: the trend span n_t, l: the low-pass span n_l, k: the number of inner passes n_i, r: the number of robustness passes n_o}
  time: {worst: Θ(k (r + 1) n (s + u + l) + r n log n), best: Θ(k (r + 1) n (s + u + l) + r n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1990
  people: [Robert B. Cleveland, William S. Cleveland, Jean E. McRae, Irma Terpenning]
  note: Cleveland, Cleveland, McRae and Terpenning, at AT&T Bell Laboratories and the U.S. Bureau of Labor Statistics, built STL from the LOESS smoother of Cleveland (1979) as a simple, robust alternative to the X-11 seasonal adjustment method.
prereqs: [moving-average, ordinary-least-squares]
see_also: [local-polynomial-regression, holt-winters-method, iteratively-reweighted-least-squares, smoothing-spline, nadaraya-watson-estimator, median, periodogram, arima-model]
sources:
  - paper: "Robert B. Cleveland, William S. Cleveland, Jean E. McRae and Irma Terpenning, STL: a seasonal-trend decomposition procedure based on loess, Journal of Official Statistics 6(1) (1990), pages 3 to 73"
    title: Robert B. Cleveland, William S. Cleveland, Jean E. McRae and Irma Terpenning, STL, a seasonal-trend decomposition procedure based on loess, Journal of Official Statistics 6(1) (1990), pages 3 to 73
    locator: the inner and outer loops, the low-pass filter, the default spans and the robustness weights
  - paper: doi:10.1080/01621459.1979.10481038
    title: William S. Cleveland, Robust locally weighted regression and smoothing scatterplots, Journal of the American Statistical Association 74(368) (1979), pages 829 to 836
    locator: the tricube weights, the local line fit and the bisquare robustness iterations
  - paper: doi:10.1080/01621459.1988.10478639
    title: William S. Cleveland and Susan J. Devlin, Locally weighted regression, an approach to regression analysis by local fitting, Journal of the American Statistical Association 83(403) (1988), pages 596 to 610
    locator: LOESS with local lines and quadratics, its operator form and its degrees of freedom
---

STL splits a time series $Y_t$ into three parts, $Y_t = T_t + S_t + R_t$: a smooth trend, a seasonal part that repeats roughly every $m$ steps but may change slowly, and a remainder. It does this with nothing but LOESS, a local weighted least squares line fit, applied in a fixed pattern. An inner loop smooths each "cycle-subseries" (all Januaries, all Februaries, and so on) to get the season, takes out the slow part of that season with moving averages, then smooths the deseasonalized series to get the trend. An optional outer loop gives small weights to points with large remainders and repeats, which makes the result robust to outliers. STL handles any period, lets the season change over the years at a rate the user picks, and is the default decomposition in many statistics packages.

## In plain words

Monthly sales rise over the years and also swing with the month of the year. To separate the two, look at all the Januaries together and draw a smooth curve through them, then do the same for every other month. Put these curves back in time order: that is a first guess at the seasonal pattern, but it may also contain some of the slow growth, so smooth it heavily and subtract that slow part. Take the season away from the data and draw a smooth curve through what is left: that is the trend. Repeat this a couple of times. What is left after taking away both trend and season is the remainder. If a few points are wild, give them less say and do it again.

## The problem

Given $Y_1, \dots, Y_n$ and an integer period $m \ge 2$ with $n \ge 2m$, find a trend $T$, a seasonal component $S$ and a remainder $R$ with
$$Y_t = T_t + S_t + R_t, \qquad t = 1..n,$$
where $T$ varies slowly, $S$ is close to periodic with period $m$ and changes slowly from cycle to cycle, and $R$ is what neither explains. "Slowly" is set by three odd spans: $n_s$ for LOESS along each cycle-subseries (how fast the season may change), $n_t$ for the trend, and $n_l$ for the low-pass filter. The decomposition is not unique, so STL is defined by its procedure, not by an objective function.

**LOESS.** For data $y_1, \dots, y_N$ at positions $1..N$, span $q$ and a position $x$ (which may lie outside $1..N$), let $\lambda_q(x)$ be the distance from $x$ to the farthest of the $q$ positions nearest $x$; if $q > N$, use all $N$ positions and multiply the distance by $q/N$. The weight of position $i$ is the tricube $W(u) = (1 - u^3)^3$ for $0 \le u < 1$ and 0 otherwise, at $u = |i - x|/\lambda_q(x)$, times a robustness weight $\rho_i$. The LOESS value at $x$ is the value at $x$ of the weighted least squares line through these points (Cleveland 1979). This is [local polynomial regression](/local-polynomial-regression/) of degree 1 with a nearest-neighbor bandwidth.

## The algorithm

```pseudo id=main
STL(Y₁..Y_n, m, n_s, n_t, n_l, n_i, n_o)
L1  T ← 0;  ρ ← 1
    for pass ← 0 to n_o
L2      repeat n_i times
L3          D ← Y − T                                       ▷ detrend
L4          for each cycle-subseries j = 1..m: C_j ← LOESS(D_j, n_s, ρ_j) at positions 0..len(D_j)+1
            ▷ C, in time order, covers times 1−m .. n+m
L5          L ← LOESS(MA₃(MA_m(MA_m(C))), n_l)              ▷ low-pass, length n
L6          S ← C_{1..n} − L
L7          H ← Y − S                                       ▷ deseasonalize
L8          T ← LOESS(H, n_t, ρ)
L9      R ← Y − S − T
L10     if pass < n_o: h ← 6 median|R_t|;  ρ_t ← B(|R_t|/h), with B(u) = (1 − u²)² for u < 1, else 0
L11 return (S, T, R, ρ)
```

The cycle-subseries $D_j$ holds the values at times $j, j + m, j + 2m, \dots$. Line L4 evaluates its LOESS fit one step beyond each end, so the series $C$ has $n + 2m$ values. The three moving averages of line L5 have lengths $m$, $m$ and 3 and shorten it by $2m$, back to $n$; they remove the seasonal pattern, and line L5's LOESS smooths what remains. Line L6 subtracts that slow part from $C$, so the trend is not counted twice. Lines L3 to L8 form the inner loop. Lines L9 and L10 form the outer loop, which reweights points by the bisquare $B$ of their remainder, as in Cleveland (1979).

Cleveland et al. (1990) give defaults: $n_l$ is the smallest odd integer $\ge m$, and $n_t$ is the smallest odd integer $\ge 1.5m/(1 - 1.5/n_s)$. They recommend $n_s \ge 7$ and odd, chosen by looking at the seasonal-diagnostic plots. R's `stl` uses $n_i = 2$, $n_o = 0$ without robustness and $n_i = 1$, $n_o = 15$ with it. A very large $n_s$ (R's "periodic") makes every cycle-subseries nearly constant, so the season repeats exactly.

## Example

**By hand.** Take the quarterly series $Y = (12, 8, 14, 10, 16, 11, 17, 14, 19, 14, 21, 17)$, $m = 4$, $n_s = 7$. The default rules give $n_l = 5$ and $n_t = $ the smallest odd integer $\ge 6/(1 - 1.5/7) = 7.64$, which is 9. Use $n_i = 2$ and no robustness passes.

In the first pass $T = 0$, so the first cycle-subseries is $(12, 16, 19)$ at positions 1, 2, 3. Since $n_s = 7 > 3$, all three points are used and the bandwidth is stretched by $7/3$. At position 2 the outer points get the weight $W(3/7) = (316/343)^3 = 0.782$ and the fitted line gives 12.156. The fits at positions 0 to 4 are $8.633, 12.156, 15.695, 19.156, 22.633$. Doing the same for the other quarters gives $C$ on times $-3..16$. The low-pass filter of line L5 gives $L = (9.757, 10.603, 11.448, \dots, 19.036)$, close to a line rising 0.845 per quarter, which is the growth that the subseries fits had picked up. Then $S = C - L$ starts $(2.400, -2.603, 2.395, -2.137, \dots)$, and the trend LOESS of $Y - S$ gives $T = (9.703, 10.577, \dots, 19.012)$.

The second pass starts from this trend. The final components, to three decimals, are:

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $Y_t$ | 12 | 8 | 14 | 10 | 16 | 11 | 17 | 14 | 19 | 14 | 21 | 17 |
| $S_t$ | 2.437 | $-2.591$ | 2.389 | $-2.156$ | 2.565 | $-2.979$ | 2.482 | $-1.966$ | 2.631 | $-3.356$ | 2.660 | $-1.852$ |
| $T_t$ | 9.683 | 10.564 | 11.438 | 12.308 | 13.164 | 14.003 | 14.836 | 15.658 | 16.504 | 17.336 | 18.166 | 18.996 |
| $R_t$ | $-0.120$ | 0.027 | 0.173 | $-0.152$ | 0.271 | $-0.024$ | $-0.318$ | 0.308 | $-0.135$ | 0.020 | 0.174 | $-0.144$ |

Each column adds up to $Y_t$ exactly. The season is not forced to sum to 0 over a year: the first four values sum to 0.078. The second quarter's seasonal value drifts from $-2.59$ to $-3.36$, because the $n_s = 7$ fit lets the season change. All values are rational, and the tests compute them in exact fractions.

**Exact recovery.** For $Y_t = 5 + t/2 + \sigma_t$ with $\sigma = (3, -1, -4, 2)$ repeating, STL with any odd $n_s \ge 3$ returns $S_t = \sigma_t$, $T_t = 5 + t/2$ and $R = 0$ exactly, with or without robustness passes. The correctness page proves this.

**Outliers.** With seed 2026, simulate 120 months of a trend $50 + 0.2t + 5\sin(2\pi t/60)$, a fixed season $8\sin(2\pi t/12) + 3\cos(4\pi t/12)$ and standard Gaussian noise, with $n_s = 13$ ($n_t = 21$, $n_l = 13$). The root mean square errors against the true components are 0.489 for the season and 0.453 for the trend. Add 25 to the points at $t = 30, 31, 75$. Without robustness ($n_i = 2$, $n_o = 0$), the errors grow to 1.557 and 1.291, and the outliers' remainders are only 17 to 20, because part of each outlier has leaked into $S$ and $T$. With $n_i = 1$ and $n_o = 15$, the errors are 0.506 and 0.654, the three points get weight 0, and their remainders are about 25. These numbers are measured on one sample.

## Correctness

STL is defined by its steps, so "correct" here means three provable facts, shown on the correctness page. The components add up to $Y$ exactly, by line L9. Without robustness passes, the map from $Y$ to $(S, T, R)$ is linear. The procedure reproduces its target model exactly: if $Y$ is a line plus a periodic season that sums to 0 over a period, then $S$ is that season, $T$ is that line and $R = 0$, for any spans, any number of passes, and from any linear starting trend. The proof uses two lemmas: LOESS of degree 1 reproduces a line at every position, including the extrapolated end points, and the three moving averages map a line plus a zero-sum season to the line, shifted to the right times. The robustness weights lie in $[0, 1]$ and vanish for remainders above $6$ times the median absolute remainder. Statistical properties, such as the bias and variance of each component or the frequency response of the filters in Cleveland et al. (1990), are not proved here.

## Complexity

On a [real RAM](/real-ram/), the LOESS value at one position costs $\Theta(q)$ for span $q$. Line L4 fits $m$ subseries of about $n/m + 2$ points each, so it costs $\Theta(n\,n_s)$ when $n_s$ is at most the subseries length. Line L5 costs $\Theta(n)$ for the moving averages with running sums (the reference implementation sums each window again, $\Theta(nm)$, which is no more than the $\Theta(n\,n_l)$ of the LOESS), and line L8 costs $\Theta(n\,n_t)$. One inner pass is $\Theta(n(n_s + n_t + n_l))$, and line L10 needs a median, $\Theta(n \log n)$ by sorting or $\Theta(n)$ by selection. With the default spans, $n_t$ and $n_l$ are about $1.5m$ and $m$, so a pass costs $\Theta(n(n_s + m))$. The extra space is $\Theta(n)$. Cleveland's Fortran code evaluates each LOESS only at every $j$-th position and interpolates linearly in between (the "jump" parameters), which divides the time by about $j$.

**Numerical stability.** Each LOESS fit is a weighted least squares line on at most $q$ consecutive positions. Centering the positions at their weighted mean, as the code does, keeps the normal equations well conditioned. If only one point has positive weight, which happens for $q = 3$ at an interior position, the fit is that point's value. Robustness weights can make all weights in a window 0; the implementation then keeps the nearest observation, while other codes leave the value missing.

## Properties

- **Additive by construction.** $S + T + R = Y$ exactly at every $t$.
- **Linear without robustness.** With $n_o = 0$, each step is a linear filter, so $S$, $T$ and $R$ are fixed linear functions of $Y$. The robust version is not linear, but it is scale equivariant: multiplying $Y$ by $c \neq 0$ multiplies every component by $c$ and leaves the weights unchanged.
- **Exact on its model.** A line plus a zero-sum periodic season is split exactly.
- **Changing seasons.** The span $n_s$ controls how fast the seasonal pattern may evolve. A large $n_s$ gives a nearly fixed season; a small one lets it follow the data.
- **Robust option.** Bisquare weights from the remainder downweight outliers and level shifts in single points, so they stay in $R$.
- **Local.** Each output depends only on data within the spans, so a change in $Y_t$ affects the components only near $t$ (and, through the subseries fits, at the same season in nearby years).
- **Season does not sum exactly to 0.** The low-pass step removes the slow part from $C$, but the seasonal values in one period sum to 0 only approximately.

## Variants and improvements

- **Periodic season.** Set $n_s$ very large, or replace line L4 by the subseries mean, to force an identical season every year.
- **Degree.** Cleveland et al. allow local constants or lines in each of the three LOESS steps. Local quadratics for the trend follow peaks better.
- **Jumps.** Evaluate each LOESS at every $j$-th position and interpolate, for long series.
- **Multiplicative seasons.** Apply STL to $\log Y$ when the seasonal swing grows with the level.
- **Several periods.** MSTL (Bandara, Hyndman and Bergmeir 2021) applies STL repeatedly, one period at a time, for hourly or daily data with daily, weekly and yearly cycles.
- **Forecasting.** Forecast the seasonally adjusted series $Y - S$ with any method (for example [Holt's method](/holt-winters-method/) or an [ARIMA model](/arima-model/)) and add back the last year's season.
- **Robust regression.** The outer loop is an iteratively reweighted fit with bisquare weights, the same idea as [IRLS](/iteratively-reweighted-least-squares/) for M-estimators.

## When to use it

Use STL to look at a seasonal series: to see the trend without the season, to see whether the season changes over the years, and to find outliers in the remainder. It suits any integer period, monthly, weekly or other, and long series. Use the robust version whenever outliers are possible. Use it as a first step before forecasting the seasonally adjusted series. For official seasonal adjustment with trading-day and holiday effects, use X-13ARIMA-SEATS. For forecasting a short series with a stable season, a seasonal ARIMA model or the Holt-Winters method is simpler.

## Pitfalls

- **Choosing $n_s$.** A small $n_s$ lets the season soak up noise, and a large one forces a fixed season onto a changing pattern. Look at the cycle-subseries plots before choosing it.
- **Non-integer or several periods.** STL needs one integer period. Weekly data with a 52.18-week year, or hourly data with daily and weekly cycles, need special handling.
- **Multiplicative seasons.** STL is additive. A season that grows with the level shows up as structure in $R$; take logs first.
- **End effects.** At the ends of the series the fits extrapolate, so the last values of $T$ and $S$ change when new data arrive.
- **Remainder is not white noise.** $R$ is what is left, not an estimate of an independent error; it is usually autocorrelated, and tests that assume independence do not apply to it directly.
- **Not unique.** Different spans give different, equally valid decompositions. Report the spans used.
- **Zero median remainder.** If more than half of the remainders are 0, the scale $h$ of line L10 is 0. The implementation then gives weight 1 to zero remainders and 0 to the rest; other codes add a small constant.

## Implementations

## History

Seasonal adjustment by moving averages goes back to the 1920s. The U.S. Census Bureau's X-11 program of the 1960s combined many fixed moving averages with rules for outliers. Cleveland (1979) introduced robust locally weighted regression (LOWESS), with tricube weights and bisquare robustness iterations. Robert B. Cleveland, William S. Cleveland, Jean E. McRae and Irma Terpenning (1990) built STL from it, aiming at a method that was simple, fast, robust, able to handle any period and missing values, and easy to explain. STL was added to S and then R, and later to Python's statsmodels. Bandara, Hyndman and Bergmeir (2021) extended it to several seasonal periods as MSTL.

## References
