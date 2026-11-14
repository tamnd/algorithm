---
tag: 33J9EX
kind: algorithm
slug: engle-granger-test
name: Engle-Granger test
aliases:
- Engle-Granger two-step method
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: Tests for cointegration by regressing one series on the others and applying a unit root test to the residuals.
model: real-ram
complexity:
  vars: {n: the length of the series, m: the number of regressors, p: the number of lagged differences}
  time: {worst: Θ(n (m + p)^2), best: Θ(n (m + p)^2)}
  space: {extra: Θ(n (m + p))}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1987
  people: [Robert F. Engle, Clive W. J. Granger]
  note: Engle and Granger (1987) defined cointegration formally, proved the Granger representation theorem, and proposed testing for it by a unit root test on the residuals of the levels regression, followed by an error correction model in a second step.
prereqs: [cointegration, augmented-dickey-fuller-test, ordinary-least-squares]
see_also: [johansen-test, vector-autoregression, kpss-test, arima-model, linear-regression, granger-causality]
sources:
  - paper: doi:10.2307/1913236
    title: Robert F. Engle and C. W. J. Granger, Co-integration and error correction, representation, estimation, and testing, Econometrica 55(2) (1987), pages 251 to 276
    locator: the residual-based tests, the two-step estimator, and the Granger representation theorem
  - paper: doi:10.2307/1911260
    title: James H. Stock, Asymptotic properties of least squares estimators of cointegrating vectors, Econometrica 55(5) (1987), pages 1035 to 1056
    locator: the superconsistency of the levels regression (rate n) and its second-order bias
  - paper: doi:10.2307/2938339
    title: P. C. B. Phillips and S. Ouliaris, Asymptotic properties of residual based tests for cointegration, Econometrica 58(1) (1990), pages 165 to 193
    locator: the limit laws of the residual-based statistics as functionals of a vector Brownian motion, which depend on the number of variables
  - paper: "James G. MacKinnon, Critical values for cointegration tests, Queen's Economics Department Working Paper No. 1227, Queen's University, 2010"
    title: MacKinnon 2010
    locator: "Table 2, the response surface coefficients for N = 1 to 12 variables, cases c and ct"
  - book: isbn:9780691042893
    title: James D. Hamilton, Time Series Analysis, Princeton University Press, 1994
    locator: Chapter 19 (cointegration), the residual-based tests and their critical values
  - paper: doi:10.1016/0304-4076(74)90034-7
    title: C. W. J. Granger and P. Newbold, Spurious regressions in econometrics, Journal of Econometrics 2(2) (1974), pages 111 to 120
    locator: the simulations of regressions between independent random walks
---

The Engle-Granger test asks whether two or more nonstationary series are [cointegrated](/cointegration/), that is, whether some linear combination of them is stationary. It runs in two steps. First it regresses one series on the others in levels by [ordinary least squares](/ordinary-least-squares/), which estimates the candidate combination. Then it applies a Dickey-Fuller unit root test to the residuals. If the residuals have a unit root, the series are not cointegrated; if the test rejects the unit root, the combination is stationary. Because the residuals come from a fitted regression, which makes them look more stationary than they are, the critical values are more negative than those of the [augmented Dickey-Fuller test](/augmented-dickey-fuller-test/), and they depend on the number of series. The same two steps also give the "two-step method": the residual, lagged once, is the error correction term in a regression of the differences.

## In plain words

Two series can each wander without limit and still stay close together, like a dog on a leash and its owner. The test first finds the best straight-line rule that links one series to the others, for example "the price in market A is about twice the price in market B plus one". It then looks at how far each point is from that rule. If the gaps keep coming back toward zero, the series are tied together. If the gaps wander as freely as the series themselves, the link was an accident of two trends. The usual unit root table is too generous here, because the rule was chosen to make the gaps small, so a stricter table is used.

## The problem

**Model and hypotheses.** Let $y_t$ and $x_t = (x_{1t}, \dots, x_{mt})$ be integrated of order one, I(1), as on the [ARIMA model](/arima-model/) page, $t = 1, \dots, n$. Consider the levels regression
$$y_t = \delta^\top d_t + \beta^\top x_t + u_t,$$
with $d_t = 1$ (case "c") or $d_t = (1, t)$ (case "ct"). The null hypothesis is $H_0$: $u_t$ is I(1) for every $\beta$, so $(y_t, x_t)$ is not cointegrated. The alternative is $H_1$: for the true $\beta$, $u_t$ is stationary, so $(1, -\beta^\top)$ is a cointegrating vector. The test assumes at most one cointegrating relation, and that $y_t$ enters it with a nonzero coefficient.

**Statistic.** Let $\hat u_t$ be the least squares residuals. Fit the Dickey-Fuller regression with no deterministic terms, because the residuals already have mean zero (and no trend in case "ct"),
$$\nabla\hat u_t = \rho\hat u_{t-1} + \sum_{i=1}^{p}\gamma_i\nabla\hat u_{t-i} + e_t, \qquad t = p + 2, \dots, n,$$
and take the t ratio $\tau = \hat\rho/\operatorname{se}(\hat\rho)$.

**Null distribution.** Asymptotic and nonstandard. Under $H_0$, $\tau$ converges to a functional of an $N$-dimensional Brownian motion, $N = m + 1$, which depends on $N$ and on the case but not on the covariance of the increments (Phillips and Ouliaris 1990). This limit is cited, not proved here. Its quantiles are tabulated by simulation.

**Rejection rule and size.** Reject $H_0$ when $\tau < c_\alpha(N, T)$, with the response surface of MacKinnon (2010), where $T = n - p - 1$:

| case | $N$ | 1% | 5% | 10% | 5% at $T = 100$ |
|---|---|---|---|---|---|
| "c" | 2 | $-3.896$ | $-3.336$ | $-3.044$ | $-3.398$ |
| "c" | 3 | $-4.294$ | $-3.741$ | $-3.452$ | $-3.827$ |
| "c" | 4 | $-4.643$ | $-4.096$ | $-3.810$ | $-4.209$ |
| "ct" | 2 | $-4.328$ | $-3.781$ | $-3.496$ | $-3.877$ |
| "ct" | 3 | $-4.663$ | $-4.119$ | $-3.835$ | $-4.240$ |

The first three columns are the limits $T \to \infty$. For $N = 2$ in case "c" the 5% point $-3.34$ is far below the ADF value $-2.86$. The size is asymptotically $\alpha$.

**p-value.** MacKinnon (1996) gives response surface p-values for $\tau$ by $N$ and case. A Monte Carlo p-value from independent random walks is also valid asymptotically, since the limit does not depend on nuisance parameters.

**Sensitivity and power.** The test detects a stationary combination. Its power falls as the residual becomes more persistent and as $N$ grows, because the critical values move to the left. When there is more than one cointegrating relation, the regression estimates some combination of them, and the test says nothing about how many there are. For that, use the [Johansen test](/johansen-test/).

## The algorithm

```pseudo id=main
ENGLE-GRANGER(y, x₁..x_m, case, p)
L1  (δ̂, β̂) ← OLS of y_t on d_t and x_t;  û_t ← y_t − δ̂ᵀd_t − β̂ᵀx_t
L2  Δû_t ← û_t − û_{t−1}, t = 2..n
L3  fit Δû_t = ρ û_{t−1} + Σ_{i=1..p} γ_i Δû_{t−i} + e_t by OLS, t = p+2..n
L4  τ ← ρ̂ / se(ρ̂)
L5  c ← MacKinnon(N = m + 1, case, T = n − p − 1, α)
L6  return (τ, β̂, reject ⇔ τ < c)
```

The two-step method continues after a rejection. With $\hat u_{t-1}$ from line L1, fit the error correction model
$$\nabla y_t = \mu + \alpha\hat u_{t-1} + \theta^\top\nabla x_t + \sum_{i=1}^{q}\left(a_i\nabla y_{t-i} + b_i^\top\nabla x_{t-i}\right) + \varepsilon_t$$
by OLS. All regressors are stationary under cointegration, so the usual t and F tests apply to this regression, and $\alpha < 0$ measures how fast $y$ returns to the long-run relation. The number of lags $p$ in line L3 is chosen as for the ADF test, by AIC or BIC on common rows.

## Example

**By hand.** Take $n = 10$, $x = (0, 1, 3, 2, 4, 5, 7, 6, 8, 9)$ and $y = (2, 2, 7, 6, 8, 12, 15, 12, 18, 18)$, case "c" and $p = 0$.

| step | value |
|---|---|
| L1: $\bar x$, $\bar y$, $S_{xx}$, $S_{xy}$ | $9/2$, $10$, $165/2$, $160$ |
| L1: $\hat\beta = S_{xy}/S_{xx}$, $\hat\delta = \bar y - \hat\beta\bar x$ | $64/33 = 1.9394$, $14/11 = 1.2727$ |
| L1: $\hat u_t$ | $0.727, -1.212, -0.091, 0.848, -1.030, 1.030, 0.152, -0.909, 1.212, -0.727$ |
| L3: $\hat\rho = \sum\hat u_{t-1}\nabla\hat u_t/\sum\hat u_{t-1}^2$ | $(-1442/121)/(2602/363) = -2163/1301 = -1.6626$ |
| L3: $s^2 = \mathrm{RSS}/(9 - 1)$ | 0.50266 |
| L4: $\operatorname{se}(\hat\rho) = \sqrt{s^2/\sum\hat u_{t-1}^2}$, $\tau$ | 0.26481, $-6.278$ |
| L5: $c_{0.05}(N = 2, T = 9)$ | $-4.099$ |

Since $-6.28 < -4.10$, the test rejects "no cointegration". The residuals change sign almost every step, which is the opposite of a random walk. With only 10 points the response surface is an extrapolation, so this is an illustration of the steps, not a reliable decision.

**A cointegrated pair and a spurious pair.** With seed 2026, let $x_t$ be a Gaussian random walk of length 200, $u_t = 0.5u_{t-1} + \varepsilon_t$, and $y_t = 1 + 2x_t + u_t$. Then a second, independent random walk $w_t$ is regressed on $x_t$.

| pair | $\hat\beta$ | slope t ratio | lags | $\tau$ | $c_{0.05}$ | decision |
|---|---|---|---|---|---|---|
| $y$ on $x$ | 1.968 | | 2 | $-7.20$ | $-3.367$ | cointegrated |
| $w$ on $x$ | $-0.795$ | $-9.53$ | 0 | $-0.76$ | $-3.367$ | not cointegrated |

The spurious regression of $w$ on $x$ has $R^2 = 0.31$ and a slope t ratio of $-9.5$, which a t table would call overwhelming. The residual test shows that the residuals are a random walk. For the cointegrated pair the second step gives $\hat\alpha = -0.533$ (standard error 0.064) on $\hat u_{t-1}$ and $1.951$ on $\nabla x_t$, close to the true values $-0.5$ and $2$.

**Superconsistency.** For $y_t = 2x_t + u_t$ with $x_t$ a random walk and $u_t$ iid $N(0, 1)$, the interquartile range of $\hat\beta$ over 400 samples was $0.0752$ at $n = 50$, $0.0179$ at $n = 200$ and $0.0049$ at $n = 800$. So $n$ times the range stayed near 3.6 to 3.9: the error shrinks like $1/n$, not like $1/\sqrt n$. With two independent random walks of length 100, the 5% rejection rate against $c_{0.05}(2, 99)$ was 0.054 in 2000 samples.

## Correctness

The correctness proof shows four facts. Line L1 computes the least squares fit, and the residual vector is the projection of $y$ onto the orthogonal complement of the regressors, so $\tau$ depends on $y$ only through that projection. Hence $\tau$ is unchanged when $y$ is replaced by $a + cy + d^\top x$ ($c \ne 0$) or when $x$ is replaced by an invertible affine map of itself, and under the null with independent Gaussian random walks its law does not depend on $\beta$ or the scales. Lines L2 to L4 compute the Dickey-Fuller t ratio of the residuals, by the same argument as on the ADF page. Under cointegration with $x_t$ a random walk independent of the stationary error, $n(\hat\beta - \beta)$ is bounded in probability, with $E\,S_{xx} = \sigma_v^2(n^2 - 1)/6$ exactly. The null limit law of $\tau$ (Phillips and Ouliaris 1990) and the general superconsistency result (Stock 1987) are cited, not proved.

## Complexity

On a [real RAM](/real-ram/), line L1 is a least squares fit with $n$ rows and $m + 1$ or $m + 2$ columns, $\Theta(nm^2)$ by QR. Lines L2 to L4 are a regression with $p + 1$ columns, $\Theta(np^2)$. With lag selection over $p \le p_{\max}$, the second step costs $\Theta(np_{\max}^3)$, or $\Theta(np_{\max}^2)$ with column updates of the QR factorization. The total is $\Theta(n(m + p)^2)$ time and $\Theta(n(m + p))$ space for the design matrices. The error correction step is one more regression of the same size.

**Numerical stability.** I(1) regressors in levels have large and strongly correlated columns, and the constant is close to their span when the series are far from zero. Use a QR factorization, not the normal equations, and center the columns if needed. Centering changes $\hat\delta$ but not $\hat\beta$ or the residuals.

## Properties

- **Superconsistent.** Under cointegration, $\hat\beta - \beta = O_p(1/n)$, faster than the $1/\sqrt n$ rate of stationary regression (Stock 1987). This holds even when $x_t$ is correlated with $u_t$, which would make OLS inconsistent in a stationary model.
- **Biased in finite samples.** When $u_t$ is correlated with $\nabla x_t$ or serially correlated, $\hat\beta$ has a bias of order $1/n$ and a nonstandard limit law, so t ratios from the levels regression are not valid. Fully modified OLS and dynamic OLS fix this.
- **Not invariant to normalization.** The choice of which series is $y_t$ changes $\hat\beta$ and $\tau$. In large samples all choices agree under cointegration, but in small samples they can give different answers.
- **Invariant to affine maps.** $\tau$ is unchanged by changes of level and scale of $y$ and of each $x_j$, and by adding a combination of the $x_j$ to $y$.
- **One relation only.** The residual test treats cointegration as a yes or no question with a single vector.
- **Critical values depend on $N$.** Each added regressor moves the 5% point to the left by about 0.35 to 0.4 in case "c".

## Variants and improvements

- **Phillips-Ouliaris tests.** Use the Phillips-Perron correction in place of the lagged differences, or a variance ratio statistic, on the same residuals.
- **Fully modified OLS (Phillips and Hansen 1990).** Corrects the levels regression for endogeneity and serial correlation with long-run covariance estimates, so that t tests on $\beta$ have normal limits.
- **Dynamic OLS (Stock and Watson 1993).** Adds leads and lags of $\nabla x_t$ to the levels regression for the same purpose.
- **Error correction test.** Test $\alpha = 0$ in the error correction model directly, with its own critical values. It can be more powerful when the long-run relation is known.
- **KPSS on the residuals.** Take cointegration as the null and test the residuals for stationarity with the [KPSS](/kpss-test/) statistic, with critical values that account for the estimated $\beta$.
- **Known cointegrating vector.** If theory fixes $\beta$, as for a spread or a ratio, form $u_t = y_t - \beta^\top x_t$ directly and use the ordinary ADF critical values. No estimation step means more power.
- **System methods.** The [Johansen test](/johansen-test/) estimates all cointegrating relations in a [vector autoregression](/vector-autoregression/) and treats all series alike.

## When to use it

Use the Engle-Granger test for two or three series, when there is at most one long-run relation and a natural choice of the dependent variable, for example a spot and a futures price, or consumption and income. It is simple to compute and explain. For more series, or when the number of relations is the question, use the Johansen test. If the cointegrating vector is known, test the known combination with the ADF test.

## Pitfalls

- **ADF critical values on residuals.** The residuals are chosen to be as small as possible, so they look stationary. Using $-2.86$ instead of $-3.34$ for $N = 2$ rejects "no cointegration" far too often.
- **Levels regression without a test.** A large $R^2$ and a large t ratio between two I(1) series mean nothing by themselves (Granger and Newbold 1974, Phillips 1986). In the example, independent walks gave $t = -9.5$.
- **t tests on $\hat\beta$.** The standard errors printed by the levels regression are not valid, even under cointegration. Use FM-OLS or DOLS for inference on $\beta$.
- **Constant in the residual regression.** The step-two regression has no constant; the critical values assume that. Adding one changes the null law.
- **Series of different orders.** If one series is I(0) and the other I(1), or one is I(2), the test does not measure cointegration. Test each series for a unit root first.
- **Normalization in small samples.** Report results for each choice of the dependent variable when the answers differ.
- **Breaks in the relation.** A shift in the long-run relation makes the residuals look like a random walk, and the test fails to find cointegration that holds in each regime.

## Implementations

## History

Clive Granger introduced the idea of cointegration around 1981, from his work on spurious regressions with Paul Newbold and on error correction models of the kind used by Davidson, Hendry, Srba and Yeo (1978). Robert Engle and Granger published the formal theory in Econometrica in 1987: the Granger representation theorem, which links cointegration and error correction, and the residual-based tests, with critical values they simulated. James Stock proved superconsistency in the same year. Phillips and Ouliaris (1990) derived the limit laws, and MacKinnon (1991, 2010) gave response surfaces for any number of variables. Engle and Granger shared the 2003 Nobel Memorial Prize in Economic Sciences, Granger for cointegration and Engle for ARCH-type volatility models.

## References
