---
tag: 17ZKKX
kind: definition
slug: cointegration
name: Cointegration
aliases:
- cointegrated series
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: Nonstationary series are cointegrated when some linear combination of them is stationary, so they share a common stochastic trend.
prereqs: [arima-model, stationary-process]
see_also: [engle-granger-test, johansen-test, vector-autoregression, augmented-dickey-fuller-test, kpss-test, granger-causality, ordinary-least-squares, canonical-correlation-analysis]
sources:
  - paper: doi:10.1016/0304-4076(81)90079-8
    title: C. W. J. Granger, Some properties of time series data and their use in econometric model specification, Journal of Econometrics 16(1) (1981), pages 121 to 130
    locator: the first statement of the idea that integrated series can have a linear combination of lower order
  - paper: doi:10.2307/1913236
    title: Robert F. Engle and C. W. J. Granger, Co-integration and error correction, representation, estimation, and testing, Econometrica 55(2) (1987), pages 251 to 276
    locator: the definition of CI(d, b), the Granger representation theorem, and the link to error correction models
  - paper: doi:10.2307/2938278
    title: Søren Johansen, Estimation and hypothesis testing of cointegration vectors in Gaussian vector autoregressive models, Econometrica 59(6) (1991), pages 1551 to 1580
    locator: the condition that the matrix of the levels term has reduced rank, and the representation of the process as common trends plus a stationary part
  - book: isbn:9780198774501
    title: Søren Johansen, Likelihood-Based Inference in Cointegrated Vector Autoregressive Models, Oxford University Press, 1995
    locator: Chapter 3 (the definitions of I(0), I(1) and the cointegrating space) and Chapter 4 (the Granger representation theorem)
  - paper: doi:10.1016/0304-4076(74)90034-7
    title: C. W. J. Granger and Paul Newbold, Spurious regressions in econometrics, Journal of Econometrics 2(2) (1974), pages 111 to 120
    locator: the simulation that shows how often a regression of one independent random walk on another looks significant
  - paper: doi:10.1016/0304-4076(86)90001-1
    title: P. C. B. Phillips, Understanding spurious regressions in econometrics, Journal of Econometrics 33(3) (1986), pages 311 to 340
    locator: the limit theory of the spurious regression, where the slope has a random limit and the t statistic diverges
  - paper: doi:10.1080/01621459.1988.10478707
    title: James H. Stock and Mark W. Watson, Testing for common trends, Journal of the American Statistical Association 83(404) (1988), pages 1097 to 1107
    locator: the common trends representation and the tests for the number of common trends
  - paper: doi:10.1016/0304-4076(88)90045-0
    title: C. W. J. Granger, Some recent development in a concept of causality, Journal of Econometrics 39(1-2) (1988), pages 199 to 211
    locator: the result that cointegrated series have Granger causality in at least one direction
  - book: isbn:9780691042893
    title: James D. Hamilton, Time Series Analysis, Princeton University Press, 1994
    locator: Chapter 19 (cointegration, the error correction form and the common trends form)
---

Two or more series are cointegrated when each one wanders like a random walk, but some linear combination of them stays near a fixed level. The series then share a common stochastic trend, and the combination measures how far they are from a long-run relation. Examples are the prices of one good in two markets, interest rates of different maturities, and the logarithms of consumption and income. Clive Granger gave the idea in 1981, and Robert Engle and Granger made it formal in 1987. Their representation theorem says that cointegrated series follow an error correction model: the change in each series reacts to the gap from the long-run relation. Cointegration is tested by the [Engle-Granger test](/engle-granger-test/) and the [Johansen test](/johansen-test/). It also explains when a regression of one trending series on another is real and when it is spurious.

## Definition

**Orders of integration.** A $K$-dimensional series $u_t$ is **I(0)** if it is a [stationary](/stationary-process/) linear process $u_t - \mathbb{E}u_t = \sum_{i \ge 0}C_i\varepsilon_{t-i}$, with $\varepsilon_t$ white noise, $\sum_i\|C_i\|$ finite and $\sum_iC_i \neq 0$. The last condition excludes over-differenced series such as $\varepsilon_t - \varepsilon_{t-1}$. A series $Y_t$ is **I($d$)**, integrated of order $d$, if $\nabla^dY_t$ is I(0) (after a suitable choice of starting values) and $\nabla^{d-1}Y_t$ is not. A random walk is I(1), and an [ARIMA($p$, $d$, $q$)](/arima-model/) series is I($d$).

**Cointegration (Engle and Granger 1987).** Let every component of $Y_t$ be I($d$). Then $Y_t$ is **cointegrated of order $(d, b)$**, written $Y_t \sim \mathrm{CI}(d, b)$ with $b > 0$, if there is a vector $\beta \neq 0$ such that $\beta^\top Y_t$ is I($d - b$). Such a $\beta$ is a **cointegrating vector**. The most common case is CI(1, 1): I(1) series with a stationary combination.

**Cointegrating space and rank (Johansen 1995).** Let $Y_t$ be I(1). The vectors $\beta$ such that $\beta^\top Y_t$ is stationary for a suitable choice of starting values, together with $0$, form a linear subspace of $\mathbb{R}^K$, the **cointegrating space**. Its dimension $r$ is the **cointegrating rank**, with $0 \le r \le K - 1$. The value $r = K$ is not possible, because then every unit vector would give a stationary combination and $Y_t$ would be I(0). The columns of any $K \times r$ matrix $\beta$ of rank $r$ that spans the space are a basis. Only the space is determined: $\beta$ and $\beta Q$ span the same space for any nonsingular $r \times r$ matrix $Q$, so a normalization such as a leading identity block is needed to report numbers. A process with rank $r$ has $K - r$ **common stochastic trends**. This definition does not require every component to be I(1). A stationary component, if there is one, gives a unit vector in the cointegrating space.

**The Granger representation theorem.** Let $Y_t$ follow a VAR($p$) $A(L)Y_t = \varepsilon_t$ whose characteristic roots $\det A(z) = 0$ are either outside the unit circle or at $z = 1$. Write it in **error correction form**
$$\nabla Y_t = \Pi Y_{t-1} + \sum_{i=1}^{p-1}\Gamma_i\nabla Y_{t-i} + \varepsilon_t, \qquad \Pi = -A(1), \quad \Gamma = I - \sum_{i=1}^{p-1}\Gamma_i.$$
Then $Y_t$ is I(1) with cointegrating rank $r$ if and only if $\Pi = \alpha\beta^\top$ with $\alpha$ and $\beta$ of size $K \times r$ and rank $r$, and $\alpha_\perp^\top\Gamma\beta_\perp$ is nonsingular, where $\alpha_\perp$ and $\beta_\perp$ are $K \times (K - r)$ of full rank with $\alpha^\top\alpha_\perp = 0$ and $\beta^\top\beta_\perp = 0$. In that case
$$Y_t = C\sum_{i=1}^{t}\varepsilon_i + \sum_{i \ge 0}C_i^*\varepsilon_{t-i} + A_0, \qquad C = \beta_\perp(\alpha_\perp^\top\Gamma\beta_\perp)^{-1}\alpha_\perp^\top,$$
with $\beta^\top A_0 = 0$ and a stationary second term (Engle and Granger 1987; Johansen 1991; Johansen 1995, Chapter 4). This page cites the theorem and does not prove it. The $K - r$ random walks $\alpha_\perp^\top\sum_i\varepsilon_i$ are the common trends. The columns of $\beta$ give the long-run relations, and the **adjustment coefficients** $\alpha$ say how fast each series moves back toward them. Because $\beta^\top C = 0$, the trends cancel in $\beta^\top Y_t$, which is stationary.

## Examples and non-examples

- **A worked system.** Let $\varepsilon_{1t}$ and $\varepsilon_{2t}$ be independent white noise with variance 1, and
$$\nabla Y_{1t} = -\tfrac12(Y_{1,t-1} - Y_{2,t-1}) + \varepsilon_{1t}, \qquad \nabla Y_{2t} = \varepsilon_{2t}.$$
So $\alpha = (-\frac12, 0)^\top$, $\beta = (1, -1)^\top$ and $\Pi = \alpha\beta^\top = \begin{pmatrix}-1/2 & 1/2\\ 0 & 0\end{pmatrix}$. In levels it is the VAR(1) $Y_t = AY_{t-1} + \varepsilon_t$ with $A = I + \Pi = \begin{pmatrix}1/2 & 1/2\\ 0 & 1\end{pmatrix}$, whose eigenvalues are $\frac12$ and $1$.
  - $Y_{2t}$ is a random walk, so it is I(1).
  - The gap $z_t = Y_{1t} - Y_{2t}$ satisfies $z_t = \frac12Y_{1,t-1} + \frac12Y_{2,t-1} + \varepsilon_{1t} - Y_{2,t-1} - \varepsilon_{2t} = \frac12z_{t-1} + (\varepsilon_{1t} - \varepsilon_{2t})$. This is a stationary AR(1) with variance $2/(1 - \frac14) = 8/3$. So $\beta = (1, -1)^\top$ is a cointegrating vector.
  - $Y_{1t} = Y_{2t} + z_t$ is a random walk plus a stationary series, so it is I(1).
  - The rank is exactly 1. For any $b = (b_1, b_2)^\top$, $b^\top Y_t = (b_1 + b_2)Y_{2t} + b_1z_t$. This is stationary if and only if $b_1 + b_2 = 0$, because otherwise it is a nonzero multiple of a random walk plus a stationary term.
  - With $\alpha_\perp = (0, 1)^\top$, $\beta_\perp = (1, 1)^\top$ and $\Gamma = I$, the matrix $\alpha_\perp^\top\beta_\perp = 1$ is nonsingular and $C = \beta_\perp\alpha_\perp^\top = \begin{pmatrix}0 & 1\\ 0 & 1\end{pmatrix}$. The single common trend is $\sum_i\varepsilon_{2i}$, which enters both series with weight 1, and $\beta^\top C = 0$.
  - Only $Y_1$ adjusts to the gap. $Y_2$ does not react to it, and its past does help to forecast $Y_1$, so $Y_2$ [Granger-causes](/granger-causality/) $Y_1$ but not the reverse.
- **Least squares on the levels.** In the system above, the regression of $Y_1$ on $Y_2$ with an intercept estimates the cointegrating slope 1. With seed 2026 and 1000 samples, the root mean squared error of the slope was 0.259, 0.070 and 0.020 for $T = 50$, 200 and 800. Each fourfold increase of $T$ cut it by a factor of 3.5 to 3.7, near the factor 4 of the $1/T$ rate and far from the factor 2 of the usual $1/\sqrt{T}$ rate. This is the superconsistency proved on the [Engle-Granger test](/engle-granger-test/) page. The numbers are measured, not derived.
- **One common factor.** Let $W_t$ be a random walk, $u_{1t}$ and $u_{2t}$ stationary, $Y_{1t} = W_t + u_{1t}$ and $Y_{2t} = 2W_t + u_{2t}$. Then $2Y_{1t} - Y_{2t} = 2u_{1t} - u_{2t}$ is stationary, and the cointegrating space is spanned by $(2, -1)^\top$. With $K$ series that load on one random walk with loadings $\lambda$, the cointegrating space is every vector orthogonal to $\lambda$, and the rank is $K - 1$.
- **CI(2, 1).** Let $S_t$ be I(2), such as the running sum of a random walk, and $Y_{1t} = S_t$ and $Y_{2t} = S_t + W_t$ with $W_t$ a random walk. Both series are I(2), and $Y_{2t} - Y_{1t} = W_t$ is I(1). So $(Y_1, Y_2) \sim \mathrm{CI}(2, 1)$.
- **Non-example: independent random walks.** Let $Y_{1t}$ and $Y_{2t}$ be independent random walks with innovation variance 1. For any $b \neq 0$, $b^\top Y_t$ is a random walk with innovation variance $b_1^2 + b_2^2 > 0$, so no combination is stationary and the rank is 0. A regression of one on the other is still often "significant". With seed 2026 and 2000 samples, the usual t test of a zero slope at the 5% level rejected in 67.6% of samples for $T = 50$ and in 82.0% for $T = 200$. This is the spurious regression of Granger and Newbold (1974). Phillips (1986) proved that the slope estimate has a random limit and that the t statistic grows like $\sqrt{T}$, so the rejection rate goes to 1.
- **Non-example: stationary series.** If every component is I(0), every vector gives a stationary combination, and the idea has no content. The CI($d$, $b$) definition needs $d \ge 1$.
- **Non-example: mixed orders.** If $Y_1$ is I(1) and $Y_2$ is I(0), a combination $b^\top Y_t$ is stationary only when $b_1 = 0$. In the Engle-Granger sense the pair is not cointegrated, since the components do not have the same order. In Johansen's sense the rank is 1 with $\beta = (0, 1)^\top$. This matters in practice, since a stationary series in a Johansen system adds 1 to the rank.
- **Non-example: deterministic trends only.** If $Y_{it} = c_it + u_{it}$ with stationary $u_{it}$, the combination $c_2Y_{1t} - c_1Y_{2t}$ removes the trend. The series are trend stationary, not I(1), so this is not cointegration in the sense above. Some authors call it deterministic cointegration.

## Related definitions

- **Error correction model.** The form $\nabla Y_t = \alpha\beta^\top Y_{t-1} + \sum_i\Gamma_i\nabla Y_{t-i} + \varepsilon_t$ above. The Granger representation theorem says that cointegrated VAR series have this form with all terms I(0), and the reverse.
- **Common trends.** Stock and Watson (1988) write a cointegrated system as $K - r$ random walks plus stationary parts, as in the representation $C\sum_i\varepsilon_i$ above, and test for the number of trends.
- **[Vector autoregression](/vector-autoregression/).** A cointegrated system is a VAR with roots at $z = 1$, so it is not stable in the sense of that page. The VAR in levels is still correct, but tests on its coefficients can have nonstandard laws. A VAR in differences omits the term $\alpha\beta^\top Y_{t-1}$ and is misspecified.
- **Unit root tests.** The [augmented Dickey-Fuller test](/augmented-dickey-fuller-test/) and the [KPSS test](/kpss-test/) decide whether each series is I(1) before cointegration is tested. The Engle-Granger test applies a unit root test to the residuals of the levels regression.
- **Rank and canonical correlations.** The [Johansen test](/johansen-test/) estimates $r$ by the [canonical correlations](/canonical-correlation-analysis/) between $\nabla Y_t$ and $Y_{t-1}$, after both are adjusted for the lagged differences.
- **[Granger causality](/granger-causality/).** If two series are cointegrated, at least one of them Granger-causes the other (Granger 1988).
- **Spurious regression.** A regression between integrated series that are not cointegrated. Its residuals are I(1), which is what the residual-based tests look for.

## References
