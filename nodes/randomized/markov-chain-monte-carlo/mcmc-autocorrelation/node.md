---
tag: FP07MM
kind: concept
slug: mcmc-autocorrelation
name: Autocorrelation (MCMC)
aliases:
- serial correlation
- MCMC autocorrelation
- integrated autocorrelation time
area: randomized/markov-chain-monte-carlo
level: core
summary: The correlation ρ_k between f(X_t) and f(X_{t+k}) in a stationary chain. Its sum τ = 1 + 2Σρ_k sets the variance of an MCMC average, Var ≈ τ Var_π(f)/n.
prereqs: [markov-chain, variance]
see_also: [effective-sample-size, thinning, burn-in, gelman-rubin-diagnostic, central-limit-theorem, autocorrelation, spectral-gap, mixing-time]
sources:
  - paper: doi:10.1214/ss/1177011137
    title: Charles J. Geyer, Practical Markov chain Monte Carlo, Statistical Science 7(4), 1992
    locator: pages 473 to 483 (the asymptotic variance, and the initial positive, monotone and convex sequence estimators for reversible chains)
  - book: isbn:9781420079418
    title: Steve Brooks, Andrew Gelman, Galin L. Jones and Xiao-Li Meng (editors), Handbook of Markov Chain Monte Carlo, Chapman and Hall/CRC, 2011
    locator: Chapter 1, Charles J. Geyer, Introduction to Markov chain Monte Carlo (autocovariance, the Markov chain CLT, batch means and initial sequence estimators)
  - book: isbn:9780198517979
    title: M. E. J. Newman and G. T. Barkema, Monte Carlo Methods in Statistical Physics, Oxford University Press, 1999
    locator: Chapter 3 (correlation times and errors of Monte Carlo estimates)
  - paper: doi:10.1214/aos/1176325750
    title: Luke Tierney, Markov chains for exploring posterior distributions, Annals of Statistics 22(4), 1994
    locator: pages 1701 to 1728 (central limit theorems for ergodic averages)
---

In a Markov chain $X_0, X_1, \ldots$ in its stationary distribution $\pi$, the values $f(X_t)$ of a function $f$ are correlated, because each state is built from the one before. The autocorrelation at lag $k$ is $\rho_k = \operatorname{Corr}(f(X_t), f(X_{t+k}))$, and the integrated autocorrelation time is $\tau = 1 + 2\sum_{k \ge 1}\rho_k$. It is the factor that MCMC loses against independent sampling: the average of $n$ correlated draws has variance about $\tau\operatorname{Var}_\pi(f)/n$, so it is worth about $n/\tau$ independent draws, the [effective sample size](/effective-sample-size/). This page is about autocorrelation as it is used in MCMC output analysis. The [autocorrelation](/autocorrelation/) page in signal processing treats the same function for signals.

## In plain words

Each state of a Markov chain is a small change of the state before it, so consecutive samples look alike. If you measure something on each sample, today's value tells you a lot about tomorrow's value. That is autocorrelation.

Correlated samples carry less information than independent ones. A thousand samples that each look like their neighbor may be worth only fifty independent samples. The autocorrelation time measures this: it is about the number of steps the chain needs to forget where it was. Divide the number of samples by it to get the number of independent samples you really have.

## The idea

**Definitions.** Let $X_0, X_1, \ldots$ be a stationary sequence, for example a Markov chain started from $\pi$, let $f$ be a function with $\operatorname{Var}_\pi f < \infty$, and write $Y_t = f(X_t)$ and $\mu = E_\pi f$. The autocovariance and autocorrelation at lag $k$ are

$$\gamma_k = \operatorname{Cov}(Y_t, Y_{t+k}), \qquad \rho_k = \gamma_k/\gamma_0.$$

By stationarity they do not depend on $t$, and $\gamma_0 = \operatorname{Var}_\pi f$. The asymptotic variance and the integrated autocorrelation time are

$$\sigma^2_{\mathrm{asy}} = \gamma_0 + 2\sum_{k=1}^{\infty}\gamma_k, \qquad \tau = \frac{\sigma^2_{\mathrm{asy}}}{\gamma_0} = 1 + 2\sum_{k=1}^{\infty}\rho_k.$$

**Theorem (variance of the mean of a stationary sequence).** Let $\bar Y_n = \frac1n\sum_{t=1}^{n}Y_t$. Then

$$\operatorname{Var}\bar Y_n = \frac1n\Big(\gamma_0 + 2\sum_{k=1}^{n-1}\Big(1 - \frac kn\Big)\gamma_k\Big),$$

and if $\sum_k|\gamma_k| < \infty$, then $n\operatorname{Var}\bar Y_n \to \sigma^2_{\mathrm{asy}}$ as $n \to \infty$.

*Proof.* By bilinearity of covariance, $\operatorname{Var}\sum_{t=1}^{n}Y_t = \sum_{s=1}^{n}\sum_{t=1}^{n}\operatorname{Cov}(Y_s, Y_t) = \sum_{s, t}\gamma_{|s - t|}$. The diagonal $s = t$ gives $n\gamma_0$. For $k \ge 1$, there are $n - k$ pairs with $t - s = k$ and $n - k$ pairs with $s - t = k$, so the off-diagonal terms give $2\sum_{k=1}^{n-1}(n - k)\gamma_k$. Divide by $n^2$ to get the formula. For the limit, $n\operatorname{Var}\bar Y_n = \gamma_0 + 2\sum_{k \ge 1}a_{n,k}$ with $a_{n,k} = (1 - k/n)\gamma_k$ for $k < n$ and $a_{n,k} = 0$ otherwise. Each $a_{n,k} \to \gamma_k$, and $|a_{n,k}| \le |\gamma_k|$, which is summable, so by dominated convergence $\sum_k a_{n,k} \to \sum_k\gamma_k$. $\blacksquare$

So for large $n$, $\operatorname{Var}\bar Y_n \approx \tau\gamma_0/n$, and $n$ correlated draws give the same precision as $n/\tau$ independent draws. For a Markov chain, the [central limit theorem](/central-limit-theorem/) $\sqrt n(\bar Y_n - \mu) \Rightarrow \mathcal{N}(0, \sigma^2_{\mathrm{asy}})$ holds under conditions such as geometric ergodicity with $E_\pi|f|^{2+\delta} < \infty$, or reversibility with $\sigma^2_{\mathrm{asy}} < \infty$, and then it holds from every start, not only from $\pi$.

**Reversible chains.** If the chain is reversible and has a finite state space, the transition matrix has real eigenvalues $1 = \lambda_0 > \lambda_1 \ge \cdots \ge \lambda_{N-1} \ge -1$ with $\pi$-orthonormal eigenvectors $\phi_j$. Write $f - \mu = \sum_{j \ge 1}c_j\phi_j$. Then

$$\gamma_k = \sum_{j \ge 1}c_j^2\lambda_j^k, \qquad \sigma^2_{\mathrm{asy}} = \sum_{j \ge 1}c_j^2\,\frac{1 + \lambda_j}{1 - \lambda_j}.$$

Since $(1 + \lambda)/(1 - \lambda)$ increases with $\lambda$, $\tau \le (1 + \lambda_1)/(1 - \lambda_1)$ for every $f$, which links $\tau$ to the [spectral gap](/spectral-gap/) $1 - \lambda_1$. Negative eigenvalues give negative correlations and $\tau < 1$ (antithetic chains). The formula also shows the fact that Geyer (1992) used: the sums of adjacent pairs, $\Gamma_m = \gamma_{2m} + \gamma_{2m+1} = \sum_j c_j^2\lambda_j^{2m}(1 + \lambda_j)$, are positive, decreasing and convex in $m$. The same holds for general reversible chains through the spectral theorem.

**Estimation.** The sample autocovariance is $\hat\gamma_k = \frac1n\sum_{t=1}^{n-k}(Y_t - \bar Y)(Y_{t+k} - \bar Y)$. One cannot simply plug all of them into $\tau$: since $\sum_t(Y_t - \bar Y) = 0$, the square of this sum is 0, and the computation of the proof gives $\hat\gamma_0 + 2\sum_{k=1}^{n-1}\hat\gamma_k = 0$ exactly. The far lags are mostly noise, so the sum must be cut off. The usual choices are:

- **Initial sequence estimators** (Geyer 1992). Sum $\hat\Gamma_m$ while it stays positive (initial positive sequence), and also force it to decrease (initial monotone sequence) or to be convex (initial convex sequence). For reversible chains, Geyer showed that they do not underestimate $\sigma^2_{\mathrm{asy}}$ in the limit $n \to \infty$.
- **Automatic windows.** Sum $\hat\rho_k$ up to a window $W$ chosen as the smallest $W$ with $W \ge c\hat\tau(W)$ for a constant $c$ near 5 (Sokal's rule, common in physics).
- **Batch means.** Split the run into $b$ batches of length $L = n/b$; for $L \gg \tau$, the batch means are nearly independent with variance about $\sigma^2_{\mathrm{asy}}/L$.
- **Spectral estimators.** $\sigma^2_{\mathrm{asy}}$ is $2\pi$ times the spectral density of $Y$ at frequency 0, which can be estimated with a lag window.

## Examples

**AR(1).** Let $Y_{t+1} = \phi Y_t + \varepsilon_{t+1}$ with independent $\varepsilon_t \sim \mathcal{N}(0, 1)$ and $|\phi| < 1$. Then $\rho_k = \phi^{|k|}$, $\gamma_0 = 1/(1 - \phi^2)$ and

$$\tau = 1 + 2\sum_{k \ge 1}\phi^k = \frac{1 + \phi}{1 - \phi}.$$

| $\phi$ | $-0.5$ | 0 | 0.5 | 0.9 | 0.99 |
|---|---|---|---|---|---|
| $\tau$ | 1/3 | 1 | 3 | 19 | 199 |

With $\phi = 0.9$ and $n = 10\,000$, $\operatorname{Var}\bar Y_n \approx 19 \cdot 5.263/10\,000 = 0.01$, the same as from 526 independent draws. The tests of the [effective sample size](/effective-sample-size/) and [Gelman-Rubin](/gelman-rubin-diagnostic/) code use AR(1) series because $\tau$ is known exactly.

**Gibbs sampling a correlated normal.** For a bivariate normal with correlation $\rho$, the [Gibbs sampler](/gibbs-sampling/) draws $x \mid y \sim \mathcal{N}(\rho y, 1 - \rho^2)$ and $y \mid x$ in the same way. The $x$-sequence of the systematic scan is an AR(1) with $\phi = \rho^2$, so $\tau = (1 + \rho^2)/(1 - \rho^2)$, which is 99.5 at $\rho = 0.99$.

**Random-walk Metropolis.** For a $\mathcal{N}(0, 1)$ target with Gaussian steps of scale $\sigma$, the lag-1 autocorrelation of $X_t$ in stationarity is $\rho_1 = 1 - E(X_{t+1} - X_t)^2/2$. It is about 0.97 for $\sigma = 0.25$, 0.63 for $\sigma = 2.4$ and 0.84 for $\sigma = 10$ (the [proposal distribution](/proposal-distribution/) page has the full table). Too small steps and too large steps both give high autocorrelation, for different reasons: small moves, or many rejections.

**The full sum is zero.** For any data $y_1, \ldots, y_n$ that are not all equal, $1 + 2\sum_{k=1}^{n-1}\hat\rho_k = 0$. So a program that sums all sample autocorrelations reports $\tau = 0$ and an infinite effective sample size.

## Where it is used

- **Error bars for MCMC averages.** The Monte Carlo standard error is $\sqrt{\hat\gamma_0\hat\tau/n}$.
- **[Effective sample size](/effective-sample-size/)**, which is $n/\tau$.
- **[Thinning](/thinning/) and [burn-in](/burn-in/)** decisions, which are often stated in units of $\tau$.
- **Comparing samplers.** The cost per independent sample is $\tau$ times the cost per step. Statistical physicists use the dynamic exponent $z$ in $\tau \sim L^z$ near a critical point, and cluster methods such as [Swendsen-Wang](/swendsen-wang/) were designed to reduce it.
- **Tuning.** The lag-1 autocorrelation, or the expected squared jump $E|X_{t+1} - X_t|^2 = 2\gamma_0(1 - \rho_1)$ for each coordinate, is a cheap target for adapting a proposal.

The quantity $\tau$ is not the [mixing time](/mixing-time/). Mixing time measures the distance from $\pi$ of the law of $X_t$ after a bad start, in the worst case over starts and functions. The autocorrelation time measures the variance of averages in stationarity for one function $f$. A chain can have small $\tau$ for some $f$ and still be far from mixed, for example if it has not yet found a second mode.

## References
