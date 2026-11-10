---
tag: KCFDXJ
kind: concept
slug: burn-in
name: Burn-in
aliases:
- warm-up period
- warm-up
area: randomized/markov-chain-monte-carlo
level: intro
summary: The first B states of an MCMC run, thrown away because their law is still far from π. It removes the bias of the start, at the cost of B steps. No output test can prove that B is large enough.
prereqs: [markov-chain, mixing-time]
see_also: [gelman-rubin-diagnostic, thinning, effective-sample-size, mcmc-autocorrelation, total-variation-distance, coupling-from-the-past, independence-sampler]
sources:
  - book: isbn:9781420079418
    title: Steve Brooks, Andrew Gelman, Galin L. Jones and Xiao-Li Meng (editors), Handbook of Markov Chain Monte Carlo, Chapman and Hall/CRC, 2011
    locator: Chapter 1, Charles J. Geyer, Introduction to Markov chain Monte Carlo (the section on burn-in, and the argument that a good starting point makes it unnecessary)
  - book: isbn:9781439840955
    title: Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, third edition, CRC Press, 2013
    locator: Section 11.4, Inference and assessing convergence (warm-up, and discarding the first half of each chain)
  - paper: doi:10.1080/01621459.1996.10476956
    title: Mary Kathryn Cowles and Bradley P. Carlin, Markov chain Monte Carlo convergence diagnostics, a comparative review, Journal of the American Statistical Association 91(434), 1996
    locator: pages 883 to 904 (diagnostics for the length of the burn-in, and how each can be misled)
  - book: isbn:9781470429621
    title: David A. Levin, Yuval Peres and Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, AMS, 2017
    locator: Chapter 4 (total variation distance and the mixing time) and Chapter 12 (bounds from the spectral gap for reversible chains)
  - paper: doi:10.1214/ss/1177011136
    title: Andrew Gelman and Donald B. Rubin, Inference from iterative simulation using multiple sequences, Statistical Science 7(4), 1992
    locator: pages 457 to 472 (overdispersed starts, and discarding the first half of each sequence)
---

Burn-in is the practice of discarding the first $B$ states $X_0, \ldots, X_{B-1}$ of an MCMC run and averaging only over $X_B, X_{B+1}, \ldots$. The chain starts from some point $x_0$ that is usually not a draw from $\pi$, so the early states have the wrong distribution, and averages that include them are biased toward $x_0$. After $B$ steps, the law of $X_B$ is within [total variation distance](/total-variation-distance/) $\varepsilon$ of $\pi$ once $B$ is at least the [mixing time](/mixing-time/) $t_{\mathrm{mix}}(\varepsilon)$. In practice the mixing time is not known, so $B$ is chosen by rules of thumb and checked with diagnostics such as the [Gelman-Rubin diagnostic](/gelman-rubin-diagnostic/). Those checks can show that $B$ is too small. They can never show that it is large enough. Modern software calls the discarded phase warm-up and also uses it to tune the sampler.

## In plain words

An MCMC sampler has to start somewhere, and that place is usually an arbitrary guess. The first states are close to the guess, not to typical points of the target. If you count them in your average, the average leans toward your guess.

So you let the chain run for a while, throw those states away, and keep only the later ones. The question is how long "a while" is. If you start far away, you need longer. If you start at a typical point of the target, you hardly need any burn-in at all. No test on the output can tell you for certain that the chain has forgotten its start.

## The idea

**What burn-in removes.** Let $\mu$ be the law of $X_0$ and $P$ the kernel, so $X_t \sim \mu P^t$. For a bounded function $f$,

$$|E f(X_t) - E_\pi f| \le 2\|f\|_\infty\,\|\mu P^t - \pi\|_{TV}.$$

So after $B \ge t_{\mathrm{mix}}(\varepsilon)$ steps, every bounded expectation is within $2\varepsilon\|f\|_\infty$ of its target value, and since $\|\mu P^t - \pi\|_{TV}$ does not increase in $t$, the same holds at every later step. For a reversible finite chain with absolute spectral gap $1 - \lambda_\star$, starting at $x$, the distance is at most $\frac12\sqrt{(1 - \pi(x))/\pi(x)}\,\lambda_\star^t$ (Levin, Peres and Wilmer, Chapter 12). This gives a guaranteed burn-in when $\lambda_\star$ is known, which is rare.

**How much it matters.** Suppose the chain is geometrically ergodic and $|E f(X_t) - E_\pi f| \le C\rho^t$ for some $C$ and $\rho < 1$ that depend on the start. Then the bias of the average of $X_{B+1}, \ldots, X_{B+n}$ is at most

$$\frac1n\sum_{t=B+1}^{B+n}C\rho^t \le \frac{C\rho^{B+1}}{n(1 - \rho)},$$

which is $O(1/n)$ even for $B = 0$. The standard deviation of the average is about $\sqrt{\tau\operatorname{Var}_\pi f/n}$, of order $1/\sqrt n$, by the variance formula on the [autocorrelation](/mcmc-autocorrelation/) page. So for long runs, burn-in matters only when $C$ is large, that is, when the start is far out in the tails or in the wrong mode. This is Geyer's point in the Handbook: any point that you would not mind having in the sample is a good starting point, and from such a point no burn-in is needed. Burn-in is a cheap correction for a bad start, not a cure for a slowly mixing chain.

**Rules of thumb.**

- Discard the first half of each chain (Gelman and Rubin 1992, BDA3). With $m$ chains from overdispersed starts, compute $\hat R$ on the second halves.
- Look at trace plots of several quantities, and discard until they look stationary. This catches gross problems only.
- Start at a mode or at a draw from an approximation to $\pi$, and use a short burn-in.
- If the sampler adapts its tuning parameters (step size, proposal covariance, mass matrix), discard the whole adaptation phase. During adaptation the kernel changes, so those draws are not from a fixed $\pi$-invariant chain. Stan's warm-up is such a phase.

**What burn-in cannot do.** A convergence diagnostic is a function of a finite output. If the chain has not found a mode of $\pi$, the output is the same as for a target without that mode, and every diagnostic passes. Only proven bounds on the [mixing time](/mixing-time/), or exact methods such as [coupling from the past](/coupling-from-the-past/), which return a draw from exactly $\pi$ with no burn-in, give a guarantee.

## Examples

**An independence sampler with known distances.** On the [independence sampler](/independence-sampler/) page, the chain with $\pi = (1/6, 1/3, 1/2)$ and $M = 2$ has $\|P^t(0, \cdot) - \pi\|_{TV} = 1/3, 13/96, 1/16, 1/32, 1/64$ for $t = 1, \ldots, 5$, and the bound $(1 - 1/M)^t = 2^{-t}$ holds from every start. So $B = 5$ guarantees that every later state is within $1/32$ of $\pi$ from any start, and in fact within $1/64$ from state 0.

**AR(1) from a far start.** Let $X_{t+1} = 0.9X_t + \varepsilon_{t+1}$ with standard normal noise, so $\pi = \mathcal{N}(0, 1/0.19)$, $E X_t = 0.9^tx_0$, and $\tau = 19$. With $n = 10\,000$ kept draws, the standard deviation of the average is $\sqrt{19 \cdot 5.263/10\,000} = 0.1$.

| start $x_0$ | burn-in $B$ | bias of the average | standard deviation |
|---|---|---|---|
| 10 | 0 | 0.009 | 0.1 |
| 1000 | 0 | 0.9 | 0.1 |
| 1000 | 110 | 0.000008 | 0.1 |

From $x_0 = 10$ the bias is a tenth of the noise, and burn-in hardly matters. From $x_0 = 1000$ the bias is nine times the noise. After $B = 110$ steps, $1000 \cdot 0.9^{110} < 0.01$, and the bias is gone. The required $B$ grows with $\log|x_0|$ here, because the chain contracts at a fixed rate.

**A bimodal target.** For an equal mixture of $\mathcal{N}(-5, 1)$ and $\mathcal{N}(5, 1)$, a [random-walk Metropolis](/random-walk-metropolis/) chain with unit steps rarely crosses between the modes. A chain that starts at 5 looks stationary after a few dozen steps, but it has not converged: the mixing time is set by the crossing time, which is far longer than any reasonable burn-in. The [Gelman-Rubin](/gelman-rubin-diagnostic/) page shows four such chains with $\hat R = 1.0001$.

## Where it is used

- **Every practical MCMC run.** Bayesian software discards a warm-up phase, by default often the first half of each chain, and uses it to adapt the sampler.
- **Statistical physics.** "Equilibration" runs before measurement, often for a number of sweeps that is a multiple of the measured autocorrelation time.
- **Burn-in versus [thinning](/thinning/).** Burn-in removes the bias of the start. Thinning removes draws from the stationary part and never lowers the variance. The two are often confused, but they answer different questions.
- **Theory.** Results on [mixing time](/mixing-time/) and [coupling](/coupling-method/) tell how long the burn-in must be for a guarantee, and they are the only source of such guarantees.

## References
