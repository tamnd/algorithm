---
tag: T7ND6C
kind: concept
slug: gelman-rubin-diagnostic
name: Gelman-Rubin diagnostic
aliases:
- R-hat
- potential scale reduction factor
- split R-hat
area: randomized/markov-chain-monte-carlo
level: core
summary: Runs several chains and compares the variance between them with the variance inside them. R̂ = √(var⁺/W) is near 1 when they agree. It can show chains have not converged, never that they have.
prereqs: [burn-in, variance]
see_also: [effective-sample-size, mcmc-autocorrelation, thinning, mixing-time, parallel-tempering, stationary-distribution]
sources:
  - paper: doi:10.1214/ss/1177011136
    title: Andrew Gelman and Donald B. Rubin, Inference from iterative simulation using multiple sequences, Statistical Science 7(4), 1992
    locator: pages 457 to 472 (overdispersed starting points, the between- and within-sequence variances, and the potential scale reduction)
  - paper: doi:10.1080/10618600.1998.10474787
    title: Stephen P. Brooks and Andrew Gelman, General methods for monitoring convergence of iterative simulations, Journal of Computational and Graphical Statistics 7(4), 1998
    locator: pages 434 to 455 (the corrected degrees-of-freedom factor, interval-based and multivariate versions)
  - paper: doi:10.1214/20-BA1221
    title: Aki Vehtari, Andrew Gelman, Daniel Simpson, Bob Carpenter and Paul-Christian Bürkner, Rank-normalization, folding, and localization, an improved R-hat for assessing convergence of MCMC, Bayesian Analysis 16(2), 2021
    locator: pages 667 to 718 (rank-normalized split R-hat, the folded version for scale, and the threshold 1.01)
  - book: isbn:9781439840955
    title: Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, third edition, CRC Press, 2013
    locator: Section 11.4, Inference and assessing convergence (split R-hat)
  - paper: doi:10.1214/ss/1177011137
    title: Charles J. Geyer, Practical Markov chain Monte Carlo, Statistical Science 7(4), 1992
    locator: pages 473 to 483 (the case for one long run, and the limits of convergence diagnostics)
---

The Gelman-Rubin diagnostic, or $\hat R$, checks a set of $m \ge 2$ MCMC chains that started from widely spread points. If the chains have all forgotten their starts, they describe the same distribution, so the variance between the chain means is what the variance within the chains predicts, and $\hat R$ is close to 1. If they have not, the between-chain variance is too large and $\hat R > 1$. Gelman and Rubin (1992) called it the potential scale reduction factor: the factor by which the spread of the current estimate might shrink if the chains ran forever. The modern form is the rank-normalized split $\hat R$ of Vehtari et al. (2021), with the threshold $\hat R < 1.01$. Like every convergence diagnostic, it can only detect some failures. A value near 1 never proves that the chains have converged.

## In plain words

Start several copies of the sampler from very different places and let them run. If they all end up wandering over the same region in the same way, that is evidence that they found the target. If one copy still lives in a different region, the copies disagree.

The diagnostic puts a number on this. It compares how far apart the copies' averages are with how much each copy moves around on its own. If the averages are much farther apart than the inside spread explains, the number is above 1, and you must run longer. A value near 1 is necessary, but it is not proof: all copies can be stuck in the same wrong place and agree perfectly.

## The idea

**The statistic.** Let $\theta_{jt}$, $j = 1, \ldots, m$, $t = 1, \ldots, n$, be the draws of a scalar quantity after [burn-in](/burn-in/). Let $\bar\theta_j$ be the mean of chain $j$ and $\bar\theta$ the mean of all draws. Define

$$W = \frac1m\sum_{j=1}^{m}s_j^2, \quad s_j^2 = \frac{1}{n-1}\sum_{t=1}^{n}(\theta_{jt} - \bar\theta_j)^2, \qquad B = \frac{n}{m-1}\sum_{j=1}^{m}(\bar\theta_j - \bar\theta)^2,$$

$$\widehat{\operatorname{var}}^+ = \frac{n-1}{n}W + \frac1nB, \qquad \hat R = \sqrt{\widehat{\operatorname{var}}^+/W}.$$

$W$ is the mean within-chain [variance](/variance/) and $B/n$ is the sample variance of the chain means.

**Why it works.** Suppose first that the $m$ chains are independent and stationary, and let $\gamma_0 = \operatorname{Var}_\pi\theta$ and $V_n = \operatorname{Var}\bar\theta_j$. The computation on the [autocorrelation](/mcmc-autocorrelation/) page gives $E\sum_t(\theta_{jt} - \bar\theta_j)^2 = n\gamma_0 - nV_n$, so $E[W] = \frac{n}{n-1}(\gamma_0 - V_n)$. The chain means are independent with variance $V_n$, so $E[B/n] = V_n$. Then

$$E[\widehat{\operatorname{var}}^+] = (\gamma_0 - V_n) + V_n = \gamma_0.$$

So in stationarity $\widehat{\operatorname{var}}^+$ is an unbiased estimate of $\operatorname{Var}_\pi\theta$, while $W$ is too small by about $V_n \approx \tau\gamma_0/n$, where $\tau$ is the integrated autocorrelation time. Hence, roughly,

$$\hat R^2 \approx 1 + \frac{\tau - 1}{n},$$

and $\hat R < 1.01$ needs $n$ of order $50\,\tau$ draws per chain. Before convergence, from overdispersed starts, the chains have not yet covered $\pi$: $W$ is too small because each chain has seen only part of the target, and $B$ is too large because the chains sit in different places. Both effects push $\hat R$ above 1. As $n \to \infty$ for an ergodic chain, $W \to \gamma_0$ and $B/n \to 0$, so $\hat R \to 1$.

**Versions.**

- **Gelman and Rubin (1992)** also multiplied by a factor for the sampling variability of $\widehat{\operatorname{var}}^+$, based on a $t$ approximation with $d$ degrees of freedom. Brooks and Gelman (1998) corrected that factor and added a multivariate version. Current software drops the factor.
- **Split $\hat R$** (BDA3). Cut each chain in half and compute $\hat R$ on the $2m$ halves. This detects a trend inside each chain, which the original version misses when all chains drift together.
- **Rank-normalized split $\hat R$** (Vehtari et al. 2021). Replace each draw by the normal score $\Phi^{-1}((r - 3/8)/(S + 1/4))$ of its rank $r$ among all $S$ draws, then compute split $\hat R$. This works for targets without a finite variance and is unchanged by monotone transformations. Also compute it for the folded draws $|\theta - \operatorname{median}|$, which detects chains that agree in location but not in scale, and report the larger of the two values. The recommended rule is $\hat R < 1.01$, together with an [effective sample size](/effective-sample-size/) of at least 100 per chain. The older rule was $\hat R < 1.1$.

**Diagnostics cannot prove convergence.** All convergence diagnostics look only at the output of a finite run. Take any run and a target $\pi'$ that equals $\pi$ on the region the chains visited but has an extra mode of mass $1/2$ elsewhere, behind a barrier the chains did not cross. A sampler on $\pi'$ can produce exactly this output with high probability, so the output looks the same for $\pi$ and for $\pi'$, and no function of it can tell whether the chains have converged. $\hat R$ can show that chains disagree. It cannot show that they agree with $\pi$. Overdispersed starts, several diagnostics, and knowledge of the target reduce this risk but do not remove it. Exact methods such as [coupling from the past](/coupling-from-the-past/), or proven [mixing time](/mixing-time/) bounds, are the only ways to certify convergence.

## Examples

**By hand.** Two chains of length 4: $(1, 2, 3, 4)$ and $(3, 4, 5, 6)$. The means are 2.5 and 4.5, and each $s_j^2 = 5/3$, so $W = 5/3$. Then $B = 4((2.5 - 3.5)^2 + (4.5 - 3.5)^2)/1 = 8$, $\widehat{\operatorname{var}}^+ = \frac34 \cdot \frac53 + \frac84 = 3.25$, and $\hat R = \sqrt{3.25/(5/3)} = \sqrt{39/20} = 1.396$.

The following cases are tests in the Python file, on AR(1) chains $\theta_{t+1} = \phi\theta_t + \varepsilon_{t+1}$, where $\tau = (1 + \phi)/(1 - \phi)$ is known.

| case | chains | classic $\hat R$ | split or rank $\hat R$ |
|---|---|---|---|
| stationary, $\phi = 0.9$, $n = 20\,000$ | 4 | below 1.01 | below 1.01 |
| starts $\pm 20, \pm 50$, $\phi = 0.99$, $n = 200$ | 4 | 2.32 | 3.17 (rank) |
| means 0, 0, 2, 2, $\phi = 0.5$, $n = 2000$ | 4 | 1.42 | |
| common trend $3t/n$, $\phi = 0.5$ | 4 | 1.00003 | 1.18 (split) |
| scales 1, 1, 1, 3, $\phi = 0.5$ | 4 | 1.0008 (split) | 1.15 (rank, folded) |
| all in one mode of a two-mode target | 4 | | 1.0001 (rank) |

The last row is the important one. The target is an equal mixture of $\mathcal{N}(-5, 1)$ and $\mathcal{N}(5, 1)$ with mean 0. All four chains sit in the right mode, $\hat R$ is 1.0001, and the pooled mean is about 5. The diagnostic passes, and the answer is wrong.

A test also checks the approximation $\hat R^2 \approx 1 + (\tau - 1)/n$: with $\phi = 0.9$ ($\tau = 19$) and $n = 400$, the mean of $\hat R^2 - 1$ over 300 repetitions is within 30% of $18/400 = 0.045$.

## Where it is used

- **Stan, PyMC and other probabilistic programming systems** report rank-normalized split $\hat R$ for every parameter, with the bulk and tail [effective sample size](/effective-sample-size/).
- **Choosing the [burn-in](/burn-in/).** Run until $\hat R$ is near 1 for the quantities of interest, then use the second half of each chain.
- **Detecting multimodality.** Chains from different starts that stay apart point to separated modes, where [parallel tempering](/parallel-tempering/) or other moves are needed.

Geyer (1992) argued for one long run instead of several short ones, because a long run explores more and the burn-in is paid once. The two views agree on the main point: the output alone cannot prove convergence, and several chains from spread-out starts are a cheap way to find some failures.

## References
