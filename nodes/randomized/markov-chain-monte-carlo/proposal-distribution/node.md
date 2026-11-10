---
tag: 3NFXW7
kind: concept
slug: proposal-distribution
name: Proposal distribution
aliases:
- proposal kernel
- instrumental distribution
area: randomized/markov-chain-monte-carlo
level: intro
summary: The distribution Q(x, ·) from which a Metropolis-type sampler draws a candidate next state. It must make the chain irreducible; its shape and scale decide how fast the chain mixes.
prereqs: [metropolis-hastings]
see_also: [acceptance-probability, random-walk-metropolis, independence-sampler, metropolis-adjusted-langevin-algorithm, hamiltonian-monte-carlo, gibbs-sampling, importance-sampling, rejection-sampling]
sources:
  - paper: doi:10.1093/biomet/57.1.97
    title: W. Keith Hastings, Monte Carlo sampling methods using Markov chains and their applications, Biometrika 57(1), 1970
    locator: pages 97 to 109 (arbitrary proposal matrices and the correction factor for asymmetric proposals)
  - paper: doi:10.1214/aos/1176325750
    title: Luke Tierney, Markov chains for exploring posterior distributions, Annals of Statistics 22(4), 1994
    locator: Section 2 (random walk, independence and other proposal types; mixtures and cycles of kernels)
  - paper: doi:10.1239/jap/1183667414
    title: Gareth O. Roberts and Jeffrey S. Rosenthal, Coupling and ergodicity of adaptive Markov chain Monte Carlo algorithms, Journal of Applied Probability 44(2), 2007
    locator: pages 458 to 475 (diminishing adaptation and containment)
  - paper: doi:10.1214/ss/1015346320
    title: Gareth O. Roberts and Jeffrey S. Rosenthal, Optimal scaling for various Metropolis-Hastings algorithms, Statistical Science 16(4), 2001
    locator: pages 351 to 367 (the scale 2.38/√d and the acceptance rates 0.234 and 0.574)
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 7 (independent and random walk Metropolis-Hastings, and the calibration of the proposal)
---

The proposal distribution $Q(x, \cdot)$ of a [Metropolis-Hastings](/metropolis-hastings/) sampler is the distribution from which the sampler draws a candidate $y$ when the chain is at $x$. The [acceptance probability](/acceptance-probability/) then makes the chain correct for the target $\pi$ for almost any choice of $Q$. So the proposal does not decide *whether* the chain targets $\pi$, but it decides *how fast* it gets there: two proposals for the same target can differ by many orders of magnitude in [mixing time](/mixing-time/). This page covers the conditions on $Q$, the main families, and how to set the scale.

## In plain words

A Metropolis-type sampler moves in two parts. First a simple random rule suggests where to go next. Then a test decides whether to go there or to stay. The proposal distribution is the first part, the rule that suggests.

The test fixes any bias of the rule, so almost any rule gives correct samples in the long run. But the rule decides the speed. If it suggests tiny steps, almost every step is accepted, but the walk crawls. If it suggests huge jumps, almost every jump lands in an unlikely place and is refused, so the walk stands still. A good rule makes steps of about the size of the region that holds most of the probability, and follows its shape.

## The idea

**Definition.** A proposal kernel on a state space $\mathcal{X}$ is a map $x \mapsto Q(x, \cdot)$ where each $Q(x, \cdot)$ is a probability distribution on $\mathcal{X}$ with a density $Q(x, y)$ with respect to the same reference measure as the target $\pi$. The sampler must be able to draw from $Q(x, \cdot)$ and to evaluate the ratio $Q(y, x)/Q(x, y)$.

**Conditions.**

- *Matching supports.* For the Metropolis-Hastings kernel to be reversible, a move $x \to y$ can be accepted only if $Q(y, x) > 0$. A proposal with $Q(x, y) > 0$ but $Q(y, x) = 0$ is legal, but that move is always rejected.
- *Irreducibility.* The chain can reach every set of positive $\pi$-probability only if $Q$ can. A sufficient condition on $\mathbb{R}^d$: $\pi$ is positive on an open connected support and $Q(x, y) > 0$ for all $x, y$ with $|x - y| < \delta$, for some $\delta > 0$. A proposal that only moves on a lattice, or only in one coordinate direction, can fail this.
- *Aperiodicity.* Any positive chance of rejection makes an irreducible chain aperiodic.

**Families.**

| family | $Q(x, y)$ | the ratio $Q(y, x)/Q(x, y)$ | page |
|---|---|---|---|
| random walk | $g(y - x)$ with $g$ symmetric | 1 | [random-walk Metropolis](/random-walk-metropolis/) |
| independence | $q(y)$ | $q(x)/q(y)$ | [independence sampler](/independence-sampler/) |
| Langevin | $\mathcal{N}(x + \frac{\varepsilon^2}{2}\nabla\log\pi(x), \varepsilon^2 I)$ | not 1, computed | [MALA](/metropolis-adjusted-langevin-algorithm/) |
| Hamiltonian | the end point of a leapfrog trajectory with a fresh momentum | 1 on the extended space | [HMC](/hamiltonian-monte-carlo/) |
| full conditional | $\pi(y_i \mid x_{-i})$ in one coordinate $i$ | makes $r = 1$ | [Gibbs sampling](/gibbs-sampling/) |
| dimension change | a map with auxiliary variables | includes a Jacobian | [reversible jump](/reversible-jump-mcmc/) |

**Combining kernels.** If $P_1, \ldots, P_k$ each leave $\pi$ invariant, then the product $P_1 P_2 \cdots P_k$ (a cycle) and any mixture $\sum_j w_j P_j$ with fixed weights also leave $\pi$ invariant. A mixture of reversible kernels is reversible. A cycle in general is not. So a sampler can mix a local random walk with rare large jumps, or update blocks of coordinates in turn.

**Scale.** For the random-walk proposal $\mathcal{N}(x, \sigma^2\Sigma)$ on a target in $d$ dimensions, the step must shrink as $d$ grows. For product targets, the best scale is $\sigma = 2.38/\sqrt{d}$ in units of the target's standard deviation, and the acceptance rate then tends to $0.234$ (Roberts, Gelman and Gilks 1997). For MALA the best step scales as $d^{-1/3}$ and the rate tends to $0.574$ (Roberts and Rosenthal 1998). Both results have exact hypotheses, stated on the pages of the samplers. For a Gaussian target with covariance $\Sigma$, the best random-walk proposal has covariance $(2.38^2/d)\,\Sigma$, so the shape of the proposal should follow the shape of the target.

**Adaptation.** Learning $Q$ from the past of the chain, for example its sample covariance, breaks the Markov property. The chain stays correct if the adaptation dies down (diminishing adaptation) and a containment condition holds (Roberts and Rosenthal 2007). The safe practice is to adapt only during the [burn-in](/burn-in/) and then fix $Q$.

**Not the same as in importance sampling.** In [rejection sampling](/rejection-sampling/) and [importance sampling](/importance-sampling/), a "proposal" is also called an instrumental distribution, but there it must cover the target with heavier tails, because its draws are reweighted, not chained. A Metropolis-Hastings proposal needs no such bound, except for the independence sampler.

## Examples

**The scale trade-off in one dimension.** Let $\pi = \mathcal{N}(0, 1)$ and $Q(x, \cdot) = \mathcal{N}(x, \sigma^2)$. The stationary acceptance rate is $(2/\pi)\arctan(2/\sigma)$ (proved on the [random-walk Metropolis](/random-walk-metropolis/) page). The expected squared jump $E(X_{t+1} - X_t)^2$ is a direct measure of progress, and for a stationary chain the lag-1 autocorrelation is $\rho_1 = 1 - E(X_{t+1} - X_t)^2/2$.

| $\sigma$ | acceptance rate | $E(X_{t+1} - X_t)^2$ | $\rho_1$ |
|---|---|---|---|
| 0.25 | 0.921 | 0.05 | 0.97 |
| 0.5 | 0.844 | 0.17 | 0.91 |
| 1 | 0.705 | 0.45 | 0.78 |
| 2.4 | 0.442 | 0.74 | 0.63 |
| 5 | 0.242 | 0.57 | 0.72 |
| 10 | 0.126 | 0.32 | 0.84 |

Small steps are almost always accepted but barely move. Large steps are mostly rejected. The jump is largest near $\sigma = 2.4$, with an acceptance rate near $0.44$, which is the usual rule of thumb in one dimension.

**A proposal that cannot reach.** On the integers with $\pi$ positive everywhere, the proposal $y = x \pm 2$ never changes the parity of $x$. The chain is reducible, and its averages converge to the conditional of $\pi$ on the even or on the odd integers, not to $\pi$.

**Asymmetric by design.** For a target on $(0, \infty)$, the proposal $y = x e^{\sigma Z}$ with $Z \sim \mathcal{N}(0, 1)$ has $Q(y, x)/Q(x, y) = y/x$. Leaving this factor out gives the wrong target (see the [acceptance probability](/acceptance-probability/) page).

## Where it is used

- Every sampler of the [Metropolis-Hastings](/metropolis-hastings/) kind, and their tuning during [burn-in](/burn-in/).
- [Parallel tempering](/parallel-tempering/), where the swap of two chains is a deterministic proposal on the product space.
- [Simulated annealing](/simulated-annealing/), where the proposal is the neighborhood move of a local search.

## References
