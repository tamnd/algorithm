---
tag: SJ7E5W
kind: concept
slug: thinning
name: Thinning
aliases:
- subsampling chain
- subsampling MCMC output
area: randomized/markov-chain-monte-carlo
level: intro
summary: Keeping only every k-th state of an MCMC run. For a fixed run, the thinned average never has smaller variance than the full one. Thinning saves storage and the cost of evaluating f, not variance.
prereqs: [mcmc-autocorrelation, effective-sample-size]
see_also: [burn-in, gelman-rubin-diagnostic, variance, markov-chain, gibbs-sampling, random-walk-metropolis]
sources:
  - paper: doi:10.1080/00031305.1994.10476054
    title: Steven N. MacEachern and L. Mark Berliner, Subsampling the Gibbs sampler, The American Statistician 48(3), 1994
    locator: pages 188 to 190 (the average of the full stationary run has variance no larger than that of a subsampled run)
  - paper: doi:10.1111/j.2041-210X.2011.00131.x
    title: William A. Link and Mitchell J. Eaton, On thinning of chains in MCMC, Methods in Ecology and Evolution 3(1), 2012
    locator: pages 112 to 115 (thinning reduces precision, and is justified only by storage or computing costs)
  - paper: doi:10.1080/10618600.2017.1336446
    title: Art B. Owen, Statistically efficient thinning of a Markov chain sampler, Journal of Computational and Graphical Statistics 26(3), 2017
    locator: pages 738 to 744 (when evaluating f is costly, thinning by a large factor can improve efficiency per unit of computing)
  - paper: doi:10.1214/ss/1177011137
    title: Charles J. Geyer, Practical Markov chain Monte Carlo, Statistical Science 7(4), 1992
    locator: pages 473 to 483 (subsampling loses information, and the asymptotic variance of averages)
---

Thinning keeps only every $k$-th state of an MCMC run, $X_k, X_{2k}, X_{3k}, \ldots$, and discards the rest. It is often done to make the kept draws less correlated. But less correlated draws are not more informative ones: for a stationary run of length $nk$, the average of all $nk$ draws has variance no larger than the average of the $n$ thinned draws (MacEachern and Berliner 1994). The thinned draws have a higher [effective sample size](/effective-sample-size/) per draw, but a lower effective sample size in total. Thinning is useful for other reasons: it saves memory and disk, and it saves time when the function $f$ is much more expensive to evaluate than one step of the chain (Owen 2017). It is not the same as [burn-in](/burn-in/), which removes the start of the run.

## In plain words

MCMC samples next to each other look alike. A common habit is to keep only every tenth sample, so that the kept samples look more independent.

This does not make your answer more precise. The samples you throw away still carry some information, so the average of all samples is at least as good as the average of the kept ones. Thinning makes sense only when keeping or processing every sample costs too much: when you cannot store them all, or when the quantity you compute on each sample takes much longer than one step of the chain.

## The idea

**Theorem (MacEachern and Berliner 1994).** Let $Y_1, Y_2, \ldots$ be a stationary sequence with finite variance, for example $Y_t = f(X_t)$ for a chain started from $\pi$. For integers $n, k \ge 1$, let $\bar Y_{\mathrm{full}} = \frac{1}{nk}\sum_{t=1}^{nk}Y_t$ and $\bar Y_{\mathrm{thin}} = \frac1n\sum_{i=1}^{n}Y_{ik}$. Then

$$\operatorname{Var}\bar Y_{\mathrm{full}} \le \operatorname{Var}\bar Y_{\mathrm{thin}}.$$

*Proof.* Split the run into $k$ interleaved subsequences: for $j = 1, \ldots, k$, let $A_j = \frac1n\sum_{i=0}^{n-1}Y_{ik+j}$. Each $A_j$ is the average of $n$ values at spacing $k$, so by stationarity $A_j$ has the same distribution as $A_k = \bar Y_{\mathrm{thin}}$, and in particular $\operatorname{Var}A_j = \operatorname{Var}\bar Y_{\mathrm{thin}} = v$. The full average is $\bar Y_{\mathrm{full}} = \frac1k\sum_{j=1}^{k}A_j$. By the Cauchy-Schwarz inequality, $|\operatorname{Cov}(A_i, A_j)| \le \sqrt{\operatorname{Var}A_i\operatorname{Var}A_j} = v$, so

$$\operatorname{Var}\bar Y_{\mathrm{full}} = \frac{1}{k^2}\sum_{i=1}^{k}\sum_{j=1}^{k}\operatorname{Cov}(A_i, A_j) \le \frac{1}{k^2}\cdot k^2v = v. \qquad \blacksquare$$

The proof uses only stationarity, not the Markov property and not reversibility. Equality holds only when all the $A_j$ are perfectly correlated, which essentially never happens. So thinning a run that has already been computed always gives up some precision. The loss is small when $k$ is small compared to the integrated autocorrelation time $\tau$ of the [autocorrelation](/mcmc-autocorrelation/) page, and large when $k$ is large compared to $\tau$.

**When thinning helps.** The theorem compares the two averages for the same run. The comparison changes when costs are counted. If one step costs 1, evaluating or storing $f(X_t)$ costs $\theta$, and the budget is fixed, then keeping every state costs $1 + \theta$ per draw, while thinning by $k$ costs $k + \theta$ per kept draw. Owen (2017) showed that when $\theta$ is large and the chain is strongly correlated, the best $k$ can be large. Other good reasons are memory (a run of $10^8$ states of a model with $10^4$ parameters does not fit in memory) and plotting or downstream use, where nearly independent draws are convenient.

**What thinning does not do.** It does not remove the bias of a bad start ([burn-in](/burn-in/) does that). It does not make a chain that is stuck in one mode mix better. It does not change the law of each kept draw. And it does not make the kept draws exactly independent: thinning a chain by $k$ gives the chain with kernel $P^k$, which still has autocorrelation $\rho_k, \rho_{2k}, \ldots$ at lags $1, 2, \ldots$

## Examples

**AR(1) with $\phi = 0.9$.** Let $Y_{t+1} = 0.9Y_t + \varepsilon_{t+1}$, so $\gamma_0 = 1/(1 - 0.81) = 5.263$ and $\tau = 19$. Thinning by $k$ gives an AR(1) with coefficient $0.9^k$. For a run of $10\,000$ steps, using $\operatorname{Var}\bar Y \approx \tau\gamma_0/n$:

| thinning $k$ | kept draws | lag-1 correlation | $\tau$ of kept draws | ESS | $\operatorname{Var}$ of the mean |
|---|---|---|---|---|---|
| 1 | 10 000 | 0.9 | 19.0 | 526 | 0.0100 |
| 2 | 5000 | 0.81 | 9.53 | 525 | 0.0100 |
| 5 | 2000 | 0.590 | 3.88 | 515 | 0.0102 |
| 10 | 1000 | 0.349 | 2.07 | 483 | 0.0109 |
| 20 | 500 | 0.122 | 1.28 | 392 | 0.0134 |

The kept draws look much less correlated as $k$ grows, but the ESS only goes down. Thinning by 10 throws away 90% of the draws and loses about 8% of the information. Thinning by 20 loses about 26%.

**The same chain with an expensive $f$.** With the costs of the previous section, the variance for a fixed budget is proportional to $(k + \theta)\tau_k$ with $\tau_k = (1 + 0.9^k)/(1 - 0.9^k)$. Minimizing over $k$ gives:

| cost $\theta$ of one evaluation of $f$ | 0 | 1 | 10 | 100 |
|---|---|---|---|---|
| best $k$ | 1 | 8 | 17 | 32 |
| gain over $k = 1$ | 1.00 | 1.68 | 5.53 | 13.6 |

When $f$ is free, do not thin. When $f$ costs as much as 10 steps, thinning by about 17 is 5.5 times as efficient as evaluating $f$ at every state.

**Gibbs sampling a correlated normal.** For the bivariate normal with $\rho = 0.99$ on the [Gibbs sampling](/gibbs-sampling/) page, the $x$-sequence is AR(1) with $\phi = 0.9801$. Thinning by 100 keeps draws with lag-1 correlation $0.9801^{100} \approx 0.134$, which look nearly independent, but the ESS per sweep is still at most about $1/99.5$. Reparametrizing the target, or a better sampler, helps. Thinning does not.

## Where it is used

- **Storage.** Long runs of high-dimensional models are thinned so that the output fits in memory or on disk. This is the main practical reason, and it is a good one.
- **Expensive post-processing.** If each kept draw is fed into a costly computation, such as a simulation of predictions, thinning by a factor near the autocorrelation time loses little.
- **Old practice.** Early users of the [Gibbs sampler](/gibbs-sampling/) often thinned heavily to get "independent" draws. Geyer (1992), MacEachern and Berliner (1994), and Link and Eaton (2012) argued against thinning for precision.
- **Diagnostics.** The [effective sample size](/effective-sample-size/) and [Gelman-Rubin](/gelman-rubin-diagnostic/) diagnostics work on thinned or unthinned output alike, but the unthinned output gives more stable estimates.

## References
