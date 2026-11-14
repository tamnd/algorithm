---
tag: 813GT7
kind: model
slug: garch-model
name: GARCH model
aliases:
- generalized autoregressive conditional heteroscedasticity
- GARCH(1, 1)
- ARCH model
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: Bollerslev's model in which the conditional variance depends on past squared errors, as in Engle's ARCH, and on its own past values. It captures volatility clustering.
history:
  year: 1986
  people: [Tim Bollerslev, Robert F. Engle]
  note: Engle (1982) made the conditional variance a linear function of past squared errors, with an application to United Kingdom inflation. Bollerslev (1986) added lagged conditional variances, which gives long memory in volatility with few parameters. Engle shared the 2003 Nobel Memorial Prize in Economic Sciences for these methods.
prereqs: [arma-model, stationary-process]
see_also: [quasi-likelihood, maximum-likelihood-estimation, heteroscedasticity-consistent-standard-errors, ljung-box-test, score-test, martingale, markov-chain, bfgs]
sources:
  - paper: doi:10.2307/1912773
    title: Robert F. Engle, Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation, Econometrica 50(4) (1982), pages 987 to 1007
    locator: the conditional variance as a function of past squared errors, its moments, the maximum likelihood estimator and the Lagrange multiplier test
  - paper: doi:10.1016/0304-4076(86)90063-1
    title: Tim Bollerslev, Generalized autoregressive conditional heteroskedasticity, Journal of Econometrics 31(3) (1986), pages 307 to 327
    locator: the GARCH(p, q) recursion, Theorem 1 (wide-sense stationarity if and only if the coefficients sum to less than 1), the fourth moment of GARCH(1, 1) and the autocorrelations of the squared errors
  - paper: doi:10.1017/S0266466600005296
    title: Daniel B. Nelson, Stationarity and persistence in the GARCH(1, 1) model, Econometric Theory 6(3) (1990), pages 318 to 334
    locator: strict stationarity if and only if the expected logarithm of beta plus alpha times z squared is negative, and the integrated case
  - paper: doi:10.1017/S0266466600008215
    title: Sang-Won Lee and Bruce E. Hansen, Asymptotic theory for the GARCH(1, 1) quasi-maximum likelihood estimator, Econometric Theory 10(1) (1994), pages 29 to 52
    locator: consistency and asymptotic normality of the Gaussian quasi-maximum likelihood estimator, including the integrated case
  - paper: doi:10.3150/bj/1068128975
    title: István Berkes, Lajos Horváth and Piotr Kokoszka, GARCH processes, structure and estimation, Bernoulli 9(2) (2003), pages 201 to 227
    locator: the structure of GARCH(p, q) processes and the consistency and asymptotic normality of the quasi-maximum likelihood estimator
  - paper: doi:10.3150/bj/1093265632
    title: Christian Francq and Jean-Michel Zakoïan, Maximum likelihood estimation of pure GARCH and ARMA-GARCH processes, Bernoulli 10(4) (2004), pages 605 to 637
    locator: the quasi-maximum likelihood estimator under strict stationarity only, with the limit covariance (E z to the fourth minus 1) times the inverse of J
  - paper: doi:10.1080/07474939208800229
    title: Tim Bollerslev and Jeffrey M. Wooldridge, Quasi-maximum likelihood estimation and inference in dynamic models with time-varying covariances, Econometric Reviews 11(2) (1992), pages 143 to 172
    locator: the robust sandwich covariance of the Gaussian quasi-maximum likelihood estimator
  - paper: doi:10.1080/07474938608800095
    title: Robert F. Engle and Tim Bollerslev, Modelling the persistence of conditional variances, Econometric Reviews 5(1) (1986), pages 1 to 50
    locator: integrated GARCH, with coefficients that sum to 1
  - paper: doi:10.2307/2938260
    title: Daniel B. Nelson, Conditional heteroskedasticity in asset returns, a new approach, Econometrica 59(2) (1991), pages 347 to 370
    locator: exponential GARCH, a recursion for the logarithm of the conditional variance
  - paper: doi:10.1016/0304-4076(92)90067-2
    title: Philippe Bougerol and Nico Picard, Stationarity of GARCH processes and of some nonnegative time series, Journal of Econometrics 52(1-2) (1992), pages 115 to 127
    locator: strict stationarity of GARCH(p, q) if and only if the top Lyapunov exponent is negative
  - paper: doi:10.1111/j.1540-6261.1993.tb05128.x
    title: Lawrence R. Glosten, Ravi Jagannathan and David E. Runkle, On the relation between the expected value and the volatility of the nominal excess return on stocks, Journal of Finance 48(5) (1993), pages 1779 to 1801
    locator: the threshold term that gives negative shocks a larger effect on the conditional variance
---

GARCH describes a series whose size changes over time. Large changes tend to follow large changes and small changes follow small ones, which is the volatility clustering seen in daily stock returns, exchange rates and inflation. The series itself has no autocorrelation, but its squares do. The model, whose name stands for generalized autoregressive conditional heteroscedasticity, writes each value as $\varepsilon_t = \sigma_tz_t$, with independent standardized shocks $z_t$ and a conditional variance $\sigma_t^2$ that is a linear function of past squared values and of past conditional variances. Robert Engle introduced the dependence on past squares in 1982, and Tim Bollerslev added the lagged variances in 1986. GARCH(1, 1), with three parameters, is the standard model for volatility in finance and the base of many risk measures. The parameters are estimated by the Gaussian [quasi-likelihood](/quasi-likelihood/).

## The machine

Let $(z_t)_{t \in \mathbb{Z}}$ be IID with $\mathbb{E}z_t = 0$ and $\mathbb{E}z_t^2 = 1$. The **GARCH($p$, $q$) process** is a sequence $(\varepsilon_t)$ with
$$\varepsilon_t = \sigma_tz_t, \qquad \sigma_t^2 = \omega + \sum_{i=1}^{q}\alpha_i\varepsilon_{t-i}^2 + \sum_{j=1}^{p}\beta_j\sigma_{t-j}^2,$$
where $\omega > 0$, $\alpha_i \ge 0$ and $\beta_j \ge 0$. These signs keep $\sigma_t^2$ positive. A solution is **nonanticipative** if $\sigma_t$ is a function of $z_{t-1}, z_{t-2}, \dots$ only. Then $z_t$ is independent of $\sigma_t$, and with $\mathcal{F}_{t-1}$ the past of the shocks,
$$\mathbb{E}[\varepsilon_t \mid \mathcal{F}_{t-1}] = 0, \qquad \operatorname{Var}(\varepsilon_t \mid \mathcal{F}_{t-1}) = \sigma_t^2.$$
So $\varepsilon_t$ is a [martingale](/martingale/) difference, and $\sigma_t^2$ is known one step ahead.

The main case is **GARCH(1, 1)**:
$$\sigma_t^2 = \omega + \alpha\varepsilon_{t-1}^2 + \beta\sigma_{t-1}^2 = \omega + (\beta + \alpha z_{t-1}^2)\sigma_{t-1}^2.$$
The second form shows that $(\sigma_t^2)$ is a [Markov chain](/markov-chain/) driven by the IID multipliers $c_t = \beta + \alpha z_t^2$.

In applications $\varepsilon_t$ is the innovation of a model for the mean, for example $y_t = \mu + \phi y_{t-1} + \varepsilon_t$ or an [ARMA model](/arma-model/). Then the [ARMA](/arma-model/) part gives the conditional mean and the GARCH part gives the conditional variance.

**Hand example.** Take $\omega = 0.05$, $\alpha = 0.1$, $\beta = 0.85$, the start $\sigma_1^2 = 1$ and the values $\varepsilon_1 = 1$, $\varepsilon_2 = -2$, $\varepsilon_3 = 0.5$. Then
- $\sigma_2^2 = 0.05 + 0.1 \cdot 1 + 0.85 \cdot 1 = 1$,
- $\sigma_3^2 = 0.05 + 0.1 \cdot 4 + 0.85 \cdot 1 = 13/10$,
- $\sigma_4^2 = 0.05 + 0.1 \cdot 0.25 + 0.85 \cdot 1.3 = 59/50 = 1.18$.

The large value $\varepsilon_2 = -2$ raises the next variance by 30%, and the variance then decays toward its long-run level 1 at the rate $\alpha + \beta = 0.95$ per step. The sign of $\varepsilon_2$ has no effect.

**Estimation.** The Gaussian quasi-log-likelihood of $\theta = (\omega, \alpha, \beta)$, given a start value $\tilde\sigma_1^2$ such as the sample variance, is
$$\ell_n(\theta) = -\frac12\sum_{t=1}^{n}\left(\log\tilde\sigma_t^2(\theta) + \frac{\varepsilon_t^2}{\tilde\sigma_t^2(\theta)}\right),$$
with $\tilde\sigma_t^2$ from the recursion. One evaluation costs $\Theta(n)$ time for GARCH(1, 1). The maximum is found by a numerical method such as [BFGS](/bfgs/) or a [Newton](/newton-raphson-method/) type method, under the constraints $\omega > 0$, $\alpha, \beta \ge 0$. The estimator is called quasi-maximum likelihood, because $\ell_n$ is used even when $z_t$ is not Gaussian.

## What it counts

For GARCH(1, 1) with Gaussian $z_t$ and $\alpha + \beta < 1$, the quantities below follow from the results in the next section. The last column uses $\omega = 0.05$, $\alpha = 0.1$, $\beta = 0.85$.

| quantity | formula | value |
|---|---|---|
| unconditional variance $\mathbb{E}\varepsilon_t^2$ | $\omega/(1 - \alpha - \beta)$ | 1 |
| persistence | $\alpha + \beta$ | 0.95 |
| half-life of a variance shock, in steps | $\log\frac12/\log(\alpha + \beta)$ | 13.5 |
| autocorrelation of $\varepsilon_t$ at lag $h \ge 1$ | 0 | 0 |
| kurtosis $\mathbb{E}\varepsilon_t^4/(\mathbb{E}\varepsilon_t^2)^2$ | $3(1 - (\alpha + \beta)^2)/(1 - (\alpha + \beta)^2 - 2\alpha^2)$ | 3.774 |
| autocorrelation of $\varepsilon_t^2$ at lag 1 | $\alpha(1 - \alpha\beta - \beta^2)/(1 - 2\alpha\beta - \beta^2)$ | 0.1791 |
| autocorrelation of $\varepsilon_t^2$ at lag $h \ge 1$ | $(\alpha + \beta)^{h-1}\rho_1$ | 0.1701 at $h = 2$ |
| $h$-step variance forecast | $s + (\alpha + \beta)^{h-1}(\sigma_{t+1}^2 - s)$, $s = \omega/(1 - \alpha - \beta)$ | |

**A measured check.** A simulation with these parameters, Gaussian $z_t$, seed 2026, a burn-in of 1000 and $n = 200000$ gave sample variance 0.986, sample kurtosis 3.646, lag-1 autocorrelation 0.1689 for $\varepsilon_t^2$ and 0.001 for $\varepsilon_t$. The variance and the autocorrelations agree with the formulas within sampling error. The sample kurtosis converges slowly, because it depends on the eighth moment, which is finite here ($\mathbb{E}c_t^4 = 0.959 < 1$) but large. The values are measured, not proved.

The model counts no operations in the sense of a cost model. Its counted quantities are the moments above, and the cost of fitting is $\Theta(n)$ per likelihood evaluation times the number of iterations of the optimizer.

## Relation to other models

- **[ARMA model](/arma-model/).** The squares of a GARCH(1, 1) process with a finite fourth moment form an ARMA(1, 1) process with autoregressive coefficient $\alpha + \beta$ and moving-average coefficient $-\beta$ (Theorem 3 below). GARCH is to the conditional variance what ARMA is to the conditional mean.
- **White noise but not independent.** A covariance stationary GARCH process is white noise, so an ARMA fit to it finds nothing. The dependence shows only in nonlinear functions such as $\varepsilon_t^2$ or $|\varepsilon_t|$.
- **Testing for GARCH effects.** Engle (1982) gave a Lagrange multiplier ([score](/score-test/)) test: regress $\varepsilon_t^2$ on a constant and $\varepsilon_{t-1}^2, \dots, \varepsilon_{t-q}^2$, and compare $nR^2$ with $\chi^2_q$. A [Ljung-Box test](/ljung-box-test/) on the squared residuals is the other common check.
- **Regression with conditional heteroscedasticity.** If a regression has GARCH errors, least squares is still consistent, but the usual standard errors are wrong. [Heteroscedasticity-consistent standard errors](/heteroscedasticity-consistent-standard-errors/) fix the standard errors, and fitting the GARCH part gives a more efficient estimator.
- **Stochastic volatility.** In stochastic volatility models, $\log\sigma_t^2$ has its own shock, so $\sigma_t^2$ is not known one step ahead and the likelihood has no closed form. In GARCH the variance is a deterministic function of the past, so the likelihood is a product of simple terms.

### Variants

- **GARCH(0, $q$).** Engle's original 1982 specification has no lagged variances: $\sigma_t^2 = \omega + \sum_{i=1}^{q}\alpha_i\varepsilon_{t-i}^2$. It is GARCH(0, $q$) in the notation above. Long volatility memory needs a large $q$, which is why the lagged variance of GARCH(1, 1) is useful: unrolling the GARCH(1, 1) recursion gives $\sigma_t^2 = \omega/(1 - \beta) + \alpha\sum_{k \ge 0}\beta^k\varepsilon_{t-1-k}^2$, an infinite-order version of Engle's form with geometric weights.
- **GARCH($p$, $q$).** Bollerslev (1986, Theorem 1): the process is covariance stationary if and only if $\sum_i\alpha_i + \sum_j\beta_j < 1$, and then $\mathbb{E}\varepsilon_t^2 = \omega/(1 - \sum_i\alpha_i - \sum_j\beta_j)$. Theorem 1 below proves the case $p = q = 1$.
- **Integrated GARCH.** Engle and Bollerslev (1986) studied $\alpha + \beta = 1$. Then shocks to the variance forecast never decay, and $\mathbb{E}\varepsilon_t^2 = \infty$, but the process is still strictly stationary (Theorem 4 below).
- **Exponential GARCH.** Nelson (1991) models $\log\sigma_t^2 = \omega + \beta\log\sigma_{t-1}^2 + \alpha(|z_{t-1}| - \mathbb{E}|z_{t-1}|) + \gamma z_{t-1}$. The logarithm removes the sign constraints, and $\gamma$ lets negative and positive shocks act differently.
- **Threshold GARCH.** Glosten, Jagannathan and Runkle (1993) use $\sigma_t^2 = \omega + (\alpha + \gamma\mathbf{1}\{\varepsilon_{t-1} < 0\})\varepsilon_{t-1}^2 + \beta\sigma_{t-1}^2$. With $\gamma > 0$, a fall raises the variance more than a rise of the same size, the leverage effect seen in stock returns.
- **Heavy-tailed shocks.** The shocks $z_t$ are often taken as a scaled Student t, since GARCH with Gaussian $z_t$ often does not explain all of the kurtosis of returns.

## Known results in the model

Results 1 to 3 and 5 are proved here for GARCH(1, 1). Results 4 and 6 are cited. Write $c_t = \beta + \alpha z_t^2$, so $\mathbb{E}c_t = \alpha + \beta$ and, for Gaussian $z_t$, $\mathbb{E}c_t^2 = \beta^2 + 2\alpha\beta + 3\alpha^2$.

**Theorem 1 (covariance stationarity).** A nonanticipative GARCH(1, 1) process with finite variance $\mathbb{E}\varepsilon_t^2 = s$ that does not depend on $t$ exists if and only if $\alpha + \beta < 1$. It is then unique, strictly stationary and white noise, with
$$\mathbb{E}\varepsilon_t^2 = \frac{\omega}{1 - \alpha - \beta}.$$

*Proof.* Necessity. Since $z_t$ is independent of $\sigma_t$, $\mathbb{E}\varepsilon_t^2 = \mathbb{E}\sigma_t^2\,\mathbb{E}z_t^2 = \mathbb{E}\sigma_t^2$. Take expectations in $\sigma_t^2 = \omega + \alpha\varepsilon_{t-1}^2 + \beta\sigma_{t-1}^2$: $s = \omega + \alpha s + \beta s$. So $s(1 - \alpha - \beta) = \omega > 0$. As $s \ge 0$, this forces $\alpha + \beta < 1$ and $s = \omega/(1 - \alpha - \beta)$.

Existence. Let $\alpha + \beta < 1$ and define
$$\sigma_t^2 = \omega\sum_{k \ge 0}\prod_{i=1}^{k}c_{t-i},$$
where the empty product is 1. The terms are nonnegative, and by independence $\mathbb{E}\prod_{i=1}^{k}c_{t-i} = (\alpha + \beta)^k$. By monotone convergence $\mathbb{E}\sigma_t^2 = \omega/(1 - \alpha - \beta) < \infty$, so the series converges almost surely. Splitting off the first factor gives $\sigma_t^2 = \omega + c_{t-1}\sigma_{t-1}^2 = \omega + \alpha\varepsilon_{t-1}^2 + \beta\sigma_{t-1}^2$ with $\varepsilon_t = \sigma_tz_t$, so the recursion holds. $\sigma_t$ depends only on $z_{t-1}, z_{t-2}, \dots$ through a fixed function, so $(\varepsilon_t)$ is nonanticipative and strictly stationary. It is white noise: $\mathbb{E}\varepsilon_t = \mathbb{E}\sigma_t\,\mathbb{E}z_t = 0$, and for $h \ge 1$, $\mathbb{E}\varepsilon_t\varepsilon_{t-h} = \mathbb{E}z_t\,\mathbb{E}[\sigma_t\varepsilon_{t-h}] = 0$, where $\mathbb{E}|\sigma_t\varepsilon_{t-h}|$ is finite by the Cauchy-Schwarz inequality.

Uniqueness. Let $(\varepsilon_t', \sigma_t')$ be any nonanticipative solution with $\mathbb{E}\sigma_t'^2$ bounded by $M$. Iterating the recursion $m$ times gives
$$\sigma_t'^2 = \omega\sum_{k=0}^{m-1}\prod_{i=1}^{k}c_{t-i} + \Big(\prod_{i=1}^{m}c_{t-i}\Big)\sigma_{t-m}'^2.$$
$\sigma_{t-m}'$ is independent of $z_{t-m}, \dots, z_{t-1}$, so the last term has mean at most $(\alpha + \beta)^mM \to 0$. The first term increases to $\sigma_t^2$. So $\sigma_t'^2 = \sigma_t^2$ almost surely. $\blacksquare$

**Theorem 2 (fourth moment and kurtosis).** Let $\alpha + \beta < 1$ and let $z_t$ be Gaussian. Then $\mathbb{E}\varepsilon_t^4 < \infty$ if and only if $\beta^2 + 2\alpha\beta + 3\alpha^2 < 1$, and then
$$\kappa = \frac{\mathbb{E}\varepsilon_t^4}{(\mathbb{E}\varepsilon_t^2)^2} = \frac{3(1 - (\alpha + \beta)^2)}{1 - (\alpha + \beta)^2 - 2\alpha^2},$$
which is larger than 3 whenever $\alpha > 0$.

*Proof.* Let $\mu = \mathbb{E}c_t = \alpha + \beta$, $m_2 = \mathbb{E}c_t^2 = \beta^2 + 2\alpha\beta + 3\alpha^2$ and $P_k = \prod_{i=1}^{k}c_{t-i}$. All terms of the series of Theorem 1 are nonnegative, so $\mathbb{E}\sigma_t^4 = \omega^2\sum_{k, l \ge 0}\mathbb{E}P_kP_l$. For $k \le l$, $P_kP_l = \prod_{i \le k}c_{t-i}^2\prod_{k < i \le l}c_{t-i}$, so $\mathbb{E}P_kP_l = m_2^{k}\mu^{l-k}$. The diagonal terms are $m_2^k$, so the sum is finite only if $m_2 < 1$, and if $m_2 < 1$ it is $\sum_km_2^k(1 + 2\mu/(1 - \mu))$, which is finite. Hence $\mathbb{E}\sigma_t^4 = \omega^2(1 + \mu)/((1 - \mu)(1 - m_2))$. With $\mathbb{E}z_t^4 = 3$, $\mathbb{E}\varepsilon_t^4 = 3\mathbb{E}\sigma_t^4$, and $(\mathbb{E}\varepsilon_t^2)^2 = \omega^2/(1 - \mu)^2$, so
$$\kappa = \frac{3(1 + \mu)(1 - \mu)}{1 - m_2} = \frac{3(1 - \mu^2)}{1 - m_2}.$$
Finally $m_2 = (\alpha + \beta)^2 + 2\alpha^2$, so $1 - m_2 = 1 - \mu^2 - 2\alpha^2 < 1 - \mu^2$ when $\alpha > 0$. $\blacksquare$

For $\omega = 0.05$, $\alpha = 0.1$, $\beta = 0.85$: $m_2 = 0.9225$ and $\kappa = 3 \cdot 0.0975/0.0775 = 3.774$. So a GARCH process with Gaussian shocks has heavier tails than the Gaussian distribution.

**Theorem 3 (the squares are ARMA(1, 1)).** Let $\alpha + \beta < 1$ and $\mathbb{E}\varepsilon_t^4 < \infty$. Put $\nu_t = \varepsilon_t^2 - \sigma_t^2 = \sigma_t^2(z_t^2 - 1)$. Then $(\nu_t)$ is white noise and
$$\varepsilon_t^2 = \omega + (\alpha + \beta)\varepsilon_{t-1}^2 + \nu_t - \beta\nu_{t-1}.$$
The autocorrelations of $\varepsilon_t^2$ are $\rho_1 = \alpha(1 - \alpha\beta - \beta^2)/(1 - 2\alpha\beta - \beta^2)$ and $\rho_h = (\alpha + \beta)^{h-1}\rho_1$ for $h \ge 1$.

*Proof.* Substitute $\sigma_t^2 = \varepsilon_t^2 - \nu_t$ and $\sigma_{t-1}^2 = \varepsilon_{t-1}^2 - \nu_{t-1}$ into $\sigma_t^2 = \omega + \alpha\varepsilon_{t-1}^2 + \beta\sigma_{t-1}^2$ to get the equation. $\nu_t$ has a finite variance because $\mathbb{E}\varepsilon_t^4$ is finite, and $\mathbb{E}[\nu_t \mid \mathcal{F}_{t-1}] = \sigma_t^2(\mathbb{E}z_t^2 - 1) = 0$, so $\nu_t$ is a martingale difference and hence white noise. So $\varepsilon_t^2$ is an ARMA(1, 1) with $\phi = \alpha + \beta$ and $\theta = -\beta$. For an ARMA(1, 1), $\rho_1 = (1 + \phi\theta)(\phi + \theta)/(1 + 2\phi\theta + \theta^2)$ and $\rho_h = \phi^{h-1}\rho_1$ (see the [ARMA model](/arma-model/) page). Here $\phi + \theta = \alpha$, $1 + \phi\theta = 1 - \alpha\beta - \beta^2$ and $1 + 2\phi\theta + \theta^2 = 1 - 2\alpha\beta - \beta^2$. $\blacksquare$

**Theorem 4 (strict stationarity, cited).** Nelson (1990): with $\omega > 0$, GARCH(1, 1) has a unique strictly stationary nonanticipative solution if and only if $\gamma = \mathbb{E}\log(\beta + \alpha z_t^2) < 0$. The solution is the series of Theorem 1, which converges almost surely because $\frac1k\log P_k \to \gamma$ by the strong law of large numbers. Bougerol and Picard (1992) extended this to GARCH($p$, $q$) through a top Lyapunov exponent. One consequence has a short proof: if $\alpha > 0$ and $\alpha + \beta \le 1$, then by the strict [Jensen inequality](/jensens-inequality/), $\gamma < \log\mathbb{E}c_t = \log(\alpha + \beta) \le 0$. So the covariance stationary region lies inside the strictly stationary one, and integrated GARCH is strictly stationary with infinite variance. The boundary depends on more than $\alpha + \beta$. Values of $\gamma$ for Gaussian $z_t$, computed by Simpson's rule on $[-12, 12]$ (numerical, not closed form):

| $\alpha$ | $\beta$ | $\alpha + \beta$ | $\gamma$ | strictly stationary |
|---|---|---|---|---|
| 0.1 | 0.9 | 1.00 | $-0.0082$ | yes |
| 0.2 | 0.85 | 1.05 | $+0.0219$ | no |
| 0.3 | 0.75 | 1.05 | $-0.0074$ | yes |
| 0.4 | 0.7 | 1.10 | $+0.0079$ | no |
| 0.5 | 0.6 | 1.10 | $-0.0376$ | yes |

For GARCH(0, 1), $\gamma = \log\alpha + \mathbb{E}\log z_t^2 = \log\alpha - \gamma_E - \log 2$, where $\gamma_E$ is the Euler-Mascheroni constant and $\mathbb{E}\log z_t^2 = -1.2704$ is exact for Gaussian $z_t$. So it is strictly stationary if and only if $\alpha < 2e^{\gamma_E} = 3.562$, while its variance is finite only for $\alpha < 1$.

**Theorem 5 (variance forecasts).** If $\alpha + \beta < 1$ and $s = \omega/(1 - \alpha - \beta)$, then for $h \ge 1$,
$$\mathbb{E}[\sigma_{t+h}^2 \mid \mathcal{F}_t] = s + (\alpha + \beta)^{h-1}(\sigma_{t+1}^2 - s).$$

*Proof.* For $k \ge 1$, $\mathbb{E}[\varepsilon_{t+k}^2 \mid \mathcal{F}_t] = \mathbb{E}[\sigma_{t+k}^2 \mid \mathcal{F}_t]$, because $z_{t+k}$ is independent of $\mathcal{F}_{t+k-1}$. So $g_k = \mathbb{E}[\sigma_{t+k}^2 \mid \mathcal{F}_t]$ satisfies $g_{k+1} = \omega + (\alpha + \beta)g_k$ with $g_1 = \sigma_{t+1}^2$. Subtract $s = \omega + (\alpha + \beta)s$ to get $g_{k+1} - s = (\alpha + \beta)(g_k - s)$. $\blacksquare$

**Theorem 6 (quasi-maximum likelihood, cited).** Let $\theta_0$ be in the interior of a compact parameter set, $z_t^2$ nondegenerate with $\mathbb{E}z_t^2 = 1$, the process strictly stationary ($\gamma < 0$), and the parameters identified (for GARCH(1, 1), $\alpha_0 > 0$ and $\beta_0 < 1$; the papers give the exact conditions). Then the Gaussian quasi-maximum likelihood estimator $\hat\theta_n$ is strongly consistent. If also $\mathbb{E}z_t^4 < \infty$, then
$$\sqrt{n}(\hat\theta_n - \theta_0) \xrightarrow{d} N\big(0, (\mathbb{E}z_t^4 - 1)J^{-1}\big), \qquad J = \mathbb{E}\left[\frac{1}{\sigma_t^4}\frac{\partial\sigma_t^2}{\partial\theta}\frac{\partial\sigma_t^2}{\partial\theta^\top}\right]_{\theta_0},$$
with no moment condition on $\varepsilon_t$ itself (Lee and Hansen 1994 for GARCH(1, 1); Berkes, Horváth and Kokoszka 2003; Francq and Zakoïan 2004). When $z_t$ is Gaussian, $\mathbb{E}z_t^4 - 1 = 2$ and the estimator is the maximum likelihood estimator. Otherwise the sandwich covariance of Bollerslev and Wooldridge (1992) gives valid standard errors. The effect of the start value $\tilde\sigma_1^2$ vanishes asymptotically. This page cites these results and does not prove them.

**A measured fit.** With $\theta_0 = (0.05, 0.1, 0.85)$, seed 2026, $n = 2000$ (after a burn-in of 500), the start value equal to the sample variance and a Nelder-Mead search, one sample gave:

| shocks | $\hat\omega$ | $\hat\alpha$ | $\hat\beta$ | $\hat\alpha + \hat\beta$ |
|---|---|---|---|---|
| Gaussian | 0.0368 | 0.0709 | 0.8873 | 0.958 |
| Student t with 5 degrees of freedom, scaled to variance 1 | 0.0253 | 0.0742 | 0.9031 | 0.977 |

Each row is one sample, so the numbers show the size of the error at this $n$, not a bias. $\hat\alpha$ and $\hat\beta$ move in opposite directions, and their sum is closer to 0.95 than each part is to its true value. These numbers are measured, not proved.

## References
