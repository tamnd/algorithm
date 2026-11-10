---
tag: KEPQ21
kind: concept
slug: effective-sample-size
name: Effective sample size
aliases:
- ESS
- effective number of simulation draws
area: randomized/markov-chain-monte-carlo
level: core
summary: The number of independent draws that would give an average the same variance as n correlated MCMC draws, ESS = n/τ with τ = 1 + 2Σρ_k. The standard error is sd/√ESS.
prereqs: [mcmc-autocorrelation]
see_also: [gelman-rubin-diagnostic, thinning, burn-in, importance-sampling, central-limit-theorem, variance]
sources:
  - paper: doi:10.1214/ss/1177011137
    title: Charles J. Geyer, Practical Markov chain Monte Carlo, Statistical Science 7(4), 1992
    locator: pages 473 to 483 (the initial positive, monotone and convex sequence estimators of the asymptotic variance)
  - paper: doi:10.1214/20-BA1221
    title: Aki Vehtari, Andrew Gelman, Daniel Simpson, Bob Carpenter and Paul-Christian Bürkner, Rank-normalization, folding, and localization, an improved R-hat for assessing convergence of MCMC, Bayesian Analysis 16(2), 2021
    locator: pages 667 to 718 (the multi-chain ESS, bulk-ESS and tail-ESS, and the recommended thresholds)
  - book: isbn:9781439840955
    title: Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, third edition, CRC Press, 2013
    locator: Section 11.5, Effective number of simulation draws
  - book: isbn:9781420079418
    title: Steve Brooks, Andrew Gelman, Galin L. Jones and Xiao-Li Meng (editors), Handbook of Markov Chain Monte Carlo, Chapman and Hall/CRC, 2011
    locator: Chapter 1, Charles J. Geyer, Introduction to Markov chain Monte Carlo (the Monte Carlo standard error and its estimation)
---

The effective sample size of $n$ MCMC draws of a quantity $f$ is the number of independent draws from $\pi$ that would estimate $E_\pi f$ with the same variance. For a stationary chain it is $\mathrm{ESS} = n/\tau$, where $\tau = 1 + 2\sum_{k \ge 1}\rho_k$ is the integrated [autocorrelation](/mcmc-autocorrelation/) time of $f(X_t)$. It turns a run length into a measure of information: the Monte Carlo standard error of the mean is $\operatorname{sd}_\pi(f)/\sqrt{\mathrm{ESS}}$. ESS depends on the function $f$, not only on the chain, and it must be estimated from the output, usually with Geyer's (1992) initial sequence estimators or the multi-chain estimator of Vehtari et al. (2021). It is a different quantity from the effective sample size of [importance sampling](/importance-sampling/).

## In plain words

MCMC samples are not independent: each one looks like the one before. So 10 000 samples do not give you the precision of 10 000 independent samples. The effective sample size tells you how many independent samples your correlated samples are worth.

If the chain forgets its past quickly, the effective sample size is close to the number of samples. If it moves slowly, the effective sample size can be a small fraction of it. Use it to decide whether you have run long enough, and to compute error bars. It answers only "how precise is my average?". It does not tell you whether the chain has found all of the target.

## The idea

**Definition.** Let $Y_t = f(X_t)$ for a stationary chain, with variance $\gamma_0 = \operatorname{Var}_\pi f$, autocovariances $\gamma_k$, and asymptotic variance $\sigma^2_{\mathrm{asy}} = \gamma_0 + 2\sum_{k \ge 1}\gamma_k$. The [autocorrelation](/mcmc-autocorrelation/) page proves that

$$\operatorname{Var}\bar Y_n = \frac1n\Big(\gamma_0 + 2\sum_{k=1}^{n-1}\Big(1 - \frac kn\Big)\gamma_k\Big) \sim \frac{\sigma^2_{\mathrm{asy}}}{n}.$$

The mean of $N$ independent draws has variance $\gamma_0/N$. Set the two equal and solve for $N$:

$$\mathrm{ESS} = \frac{n\gamma_0}{\sigma^2_{\mathrm{asy}}} = \frac{n}{\tau}, \qquad \tau = 1 + 2\sum_{k=1}^{\infty}\rho_k.$$

So $\operatorname{Var}\bar Y_n \approx \gamma_0/\mathrm{ESS}$, and the Monte Carlo standard error is $\mathrm{MCSE} = \sqrt{\gamma_0/\mathrm{ESS}}$. A finite-$n$ version uses the exact formula, $\mathrm{ESS}_n = n\gamma_0\big/\big(\gamma_0 + 2\sum_{k<n}(1 - k/n)\gamma_k\big)$, but the difference is small when $n \gg \tau$.

**Properties.**

- $\mathrm{ESS} < n$ when the correlations are positive, which is the usual case.
- $\mathrm{ESS} > n$ is possible when correlations are negative, for antithetic chains or overrelaxation. For AR(1) with $\phi = -0.5$, $\tau = 1/3$ and $\mathrm{ESS} = 3n$.
- ESS depends on $f$. A chain can have large ESS for the mean and small ESS for a tail quantile, or the reverse.
- ESS is additive over independent chains in stationarity: $m$ chains of length $n$ with the same $\tau$ give $mn/\tau$.

**Estimators for one chain.** The sample autocorrelations $\hat\rho_k$ cannot be summed over all lags, because the full sum gives exactly $\hat\tau = 0$ (see the [autocorrelation](/mcmc-autocorrelation/) page). Geyer (1992) used the pair sums $\hat\Gamma_m = \hat\rho_{2m} + \hat\rho_{2m+1}$, which are positive and decreasing in $m$ for a reversible chain:

1. Compute $\hat\Gamma_0, \hat\Gamma_1, \ldots$ and stop at the first $M$ with $\hat\Gamma_M \le 0$ (initial positive sequence).
2. Replace each $\hat\Gamma_m$ by $\min(\hat\Gamma_0, \ldots, \hat\Gamma_m)$ (initial monotone sequence).
3. Set $\hat\tau = -1 + 2\sum_{m<M}\hat\Gamma_m$ and $\widehat{\mathrm{ESS}} = n/\hat\tau$.

The $-1$ is there because $\hat\Gamma_0$ contains $\hat\rho_0 = 1$, which appears once in $\tau$, not twice. Batch means is a simpler alternative: with $b$ batches of length $L \gg \tau$, $\hat\sigma^2_{\mathrm{asy}} = L$ times the sample variance of the batch means.

**Several chains.** Gelman et al. (BDA3) and Vehtari et al. (2021) combine $m$ chains of length $n$. With $W$ the mean of the within-chain variances, $B/n$ the variance of the chain means, and $\widehat{\operatorname{var}}^+ = \frac{n-1}{n}W + \frac Bn$ as in the [Gelman-Rubin diagnostic](/gelman-rubin-diagnostic/), they set

$$\hat\rho_k = 1 - \frac{W - \frac1m\sum_j\hat\gamma_{k,j}}{\widehat{\operatorname{var}}^+},$$

where $\hat\gamma_{k,j}$ is the lag-$k$ autocovariance of chain $j$, and then apply Geyer's rule to get $\widehat{\mathrm{ESS}} = mn/\hat\tau$. If the chains disagree, $B$ is large, $\hat\rho_k$ stays near 1 for many lags, and the ESS collapses. Vehtari et al. also compute it on rank-normalized draws (bulk-ESS) and on the indicators of the 5% and 95% quantiles (tail-ESS), so that it is defined for targets without a finite variance.

The Python file computes the single-chain estimator with the initial monotone sequence and the multi-chain estimator above. Its tests use AR(1) series, where $\tau = (1 + \phi)/(1 - \phi)$ is known exactly.

## Examples

**A short series by hand.** Take $y = (0.5, 1.2, 1.0, 1.6, 0.4, -0.2, 0.3, 0.9)$, so $n = 8$ and $\bar y = 0.7125$. The sample autocovariances with divisor $n$ are $\hat\gamma_0 = 0.2861$, $\hat\gamma_1 = 0.0748$, $\hat\gamma_2 = -0.0713$ and $\hat\gamma_3 = -0.1285$, so $\hat\rho_1 = 0.2615$, $\hat\rho_2 = -0.2492$ and $\hat\rho_3 = -0.4491$. Then $\hat\Gamma_0 = 1.2615 > 0$ and $\hat\Gamma_1 = -0.6983 \le 0$, so the sum stops after one pair: $\hat\tau = -1 + 2(1.2615) = 1.523$ and $\widehat{\mathrm{ESS}} = 8/1.523 = 5.25$.

**AR(1).** For $Y_{t+1} = \phi Y_t + \varepsilon_{t+1}$, $\mathrm{ESS}/n = (1 - \phi)/(1 + \phi)$:

| $\phi$ | $-0.5$ | 0 | 0.5 | 0.9 | 0.99 |
|---|---|---|---|---|---|
| ESS per 10 000 draws | 30 000 | 10 000 | 3333 | 526 | 50 |

The tests check that the estimator is within 15% of these values on 40 000 draws, and that intervals $\bar y \pm 1.96\,\mathrm{MCSE}$ for $\phi = 0.9$ and $n = 2000$ cover the true mean in about 95% of repeated runs.

**Gibbs sampling with correlation 0.99.** For the bivariate normal of the [Gibbs sampling](/gibbs-sampling/) page, $\tau = (1 + \rho^2)/(1 - \rho^2) = 99.5$, so 10 000 sweeps give an ESS of about 100 for the mean of $x$.

**Disagreeing chains.** Four AR(1) chains with $\phi = 0.5$ and means 0, 3, 6 and 9 each look well mixed, and each has a single-chain ESS near $n/3$. The multi-chain estimator sees the large $B$ and reports an ESS less than 5% of that of four chains with a common mean, as one test checks.

**Not the importance sampling ESS.** For weighted draws $w_1, \ldots, w_n$, Kish's effective sample size $(\sum_i w_i)^2/\sum_i w_i^2$ measures how uneven the weights are. It is used for [importance sampling](/importance-sampling/) and [sequential Monte Carlo](/sequential-monte-carlo/), and it has nothing to do with autocorrelation.

## Where it is used

- **Stopping rules.** Run until the ESS of each quantity of interest is large enough for the needed precision. Vehtari et al. (2021) recommend running at least four chains and requiring a bulk-ESS and tail-ESS of at least 100 per chain, together with $\hat R < 1.01$.
- **Error bars.** Report $\bar y \pm 2\,\mathrm{MCSE}$ with $\mathrm{MCSE} = \operatorname{sd}/\sqrt{\mathrm{ESS}}$.
- **Comparing samplers.** ESS per second, or ESS per gradient evaluation, is the usual measure of efficiency. For example, [HMC](/hamiltonian-monte-carlo/) and [NUTS](/no-u-turn-sampler/) are compared with [random-walk Metropolis](/random-walk-metropolis/) this way, and the effect of [thinning](/thinning/) is measured in ESS.
- **Tests of samplers.** The tests of the continuous samplers in this section use the tolerance $5\,\operatorname{sd}/\sqrt{\widehat{\mathrm{ESS}}}$ for each moment.

A large ESS does not show convergence. If all chains are stuck in one mode of a two-mode target, the ESS can be large and the estimate still wrong. Use it with the [Gelman-Rubin diagnostic](/gelman-rubin-diagnostic/) and with knowledge of the target.

## References
