---
tag: M5X8EB
kind: concept
slug: relaxed-molecular-clock
name: Relaxed molecular clock
aliases:
- uncorrelated relaxed clock
area: biology/phylogenetics
level: advanced
summary: A clock model in which each branch has its own rate, drawn from a prior, so that branch length is rate times time. Rates are autocorrelated along the tree or drawn independently per branch.
prereqs: [molecular-clock]
see_also: [divergence-time-estimation, bayesian-phylogenetic-inference, rate-heterogeneity, phylogenetic-likelihood, regularization, ultrametric-tree-reconstruction, birth-death-process, yule-model]
sources:
  - paper: doi:10.1093/oxfordjournals.molbev.a025892
    title: Jeffrey L. Thorne, Hirohisa Kishino and Ian S. Painter, Estimating the rate of evolution of the rate of molecular evolution, Molecular Biology and Evolution 15(12), 1998, 1647-1657
    locator: the autocorrelated model, in which the log rate changes along the tree like a Brownian motion, and its Bayesian MCMC fit
  - paper: doi:10.1371/journal.pbio.0040088
    title: Alexei J. Drummond, Simon Y. W. Ho, Matthew J. Phillips and Andrew Rambaut, Relaxed phylogenetics and dating with confidence, PLoS Biology 4(5), 2006, e88
    locator: the uncorrelated lognormal and uncorrelated exponential clocks, with rates drawn independently for each branch, and the joint estimate of tree and times
  - paper: doi:10.1186/1741-7007-8-114
    title: Alexei J. Drummond and Marc A. Suchard, Bayesian random local clocks, or one rate to rule them all, BMC Biology 8, 2010, 114
    locator: the random local clock, in which a few rate changes on the tree are inferred from the data
  - paper: doi:10.1093/oxfordjournals.molbev.a025731
    title: Michael J. Sanderson, A nonparametric approach to estimating divergence times in the absence of rate constancy, Molecular Biology and Evolution 14(12), 1997, 1218-1231
    locator: nonparametric rate smoothing, which chooses times so that rates change as little as possible between adjacent branches
  - book: isbn:9780199602605
    title: Ziheng Yang, Molecular Evolution, a Statistical Approach, Oxford University Press, 2014
    locator: Chapter 10, Molecular clock and estimation of species divergence times, Section 10.4, Bayesian estimation, the priors on rates
---

A relaxed molecular clock gives each branch of a dated tree its own substitution rate, so that the length of a branch is its rate times its duration, but the rates are tied together by a prior. A [strict clock](/molecular-clock/) has one rate for the whole tree and is often rejected by data. A model with a free length on every branch fits any data but says nothing about time. A relaxed clock sits between them: it keeps the ages of the nodes as parameters and explains the departures from a clock by rate variation with a known distribution. In the autocorrelated model of Thorne, Kishino and Painter (1998), the rate drifts along the tree, so that close relatives have close rates. In the uncorrelated models of Drummond et al. (2006), each branch draws its rate on its own from a lognormal or exponential distribution. Relaxed clocks are the standard models of [divergence time estimation](/divergence-time-estimation/).

## In plain words

A strict clock says that every species changes at the same speed. That is often false: some groups, such as those with short generations, change faster. But if every branch could have any speed at all, the data could not tell a fast short branch from a slow long one, and you could not learn the ages.

A relaxed clock takes a middle road. Each branch gets its own speed, but the speeds must look like draws from one common pattern. In one version, a branch's speed is close to the speed of the branch above it, so relatives change at similar speeds. In the other version, each branch picks its speed at random, on its own, from the same spread of values. The pattern lets the method separate speed from time, with help from known fossil dates.

## The idea

**The model.** Take $n$ taxa with $m$ aligned sites and a rooted binary tree with node ages $t_v$, the leaves at age 0. Each branch $e$ from a vertex $u$ to its child $v$ has a rate $r_e$ and a duration $\Delta_e = t_u - t_v$, and its length in expected substitutions per site is
$$b_e = r_e\, \Delta_e.$$
The [phylogenetic likelihood](/phylogenetic-likelihood/) depends on the $b_e$ only. There are $2n - 2$ rates and $n - 1$ ages, more numbers than the $2n - 3$ branch lengths the data can identify on the unrooted tree, so the rates and ages are told apart only by their priors and by calibrations. As for every clock model, the topology is either fixed or sampled from among the $(2n-3)!!$ rooted trees by a heuristic search or MCMC.

**Autocorrelated rates.** Thorne, Kishino and Painter (1998) let the log rate evolve along the tree as a Brownian motion. If a vertex $u$ has rate $r_u$, its child $v$ at duration $\Delta$ below it has
$$\ln r_v \sim \mathcal N\bigl(\ln r_u,\ \nu \Delta\bigr),$$
where $\nu$ is the rate of change of the rate. Some versions subtract $\nu\Delta/2$ from the mean so that the expected rate stays at $r_u$. The rate of a branch is often taken as the mean of the rates at its two ends. Sister lineages have similar rates, and the rates drift apart over long times.

**Uncorrelated rates.** Drummond et al. (2006) draw each branch rate independently from one distribution. In the uncorrelated lognormal clock (UCLN), $\ln r_e \sim \mathcal N(\mu, \sigma^2)$; to give mean rate 1, set $\mu = -\sigma^2/2$. The coefficient of variation of the rates is $\sqrt{e^{\sigma^2} - 1}$, which measures how far the data are from a strict clock; $\sigma = 0$ is the strict clock. In the uncorrelated exponential clock (UCED), the rates are exponential, with a coefficient of variation of 1. Here a branch can be fast while its sister is slow.

**Smoothing instead of a prior.** Sanderson's nonparametric rate smoothing (1997) chooses ages so that the rates of adjacent branches differ as little as possible, with no likelihood. Penalized likelihood (Sanderson 2002) adds the same kind of penalty to the likelihood, a form of [regularization](/regularization/); it is on the [divergence time page](/divergence-time-estimation/).

**Local clocks.** A local clock has one rate per clade: a few branches mark rate changes, and all branches between changes share a rate. The random local clock of Drummond and Suchard (2010) infers the number and places of the changes.

## Examples

**The lognormal with $\sigma = 0.5$.** With mean 1, $\mu = -0.125$, so the median rate is $e^{-0.125} = 0.8825$, below the mean because the distribution is skewed to the right, and the coefficient of variation is $\sqrt{e^{0.25} - 1} = 0.533$.

**Rates on a time tree.** Take the time tree $((A{:}2, B{:}2){:}3, (C{:}4, D{:}4){:}1)$ with root age 5, and lengths in units of the mean rate times one time unit. Under a strict clock with rate 1, every leaf is at distance 5 from the root. Draw the six branch rates from a UCLN with $\sigma = 0.5$, in the order A, B, AB, C, D, CD, with `random.Random(1)` and `lognormvariate(-0.125, 0.5)`.

| branch | A | B | AB | C | D | CD |
|---|---|---|---|---|---|---|
| duration | 2 | 2 | 3 | 4 | 4 | 1 |
| UCLN rate | 1.196 | 0.876 | 1.633 | 1.466 | 0.746 | 1.622 |
| length | 2.391 | 1.753 | 4.899 | 5.865 | 2.983 | 1.622 |

The root-to-tip distances become 7.29 for A, 6.65 for B, 7.49 for C and 4.61 for D, so the tree is no longer ultrametric. The rates of the sisters C and D, 1.466 and 0.746, are not related, as the model allows.

For the autocorrelated model, start with rate 1 at the root and $\nu = 0.1$ per time unit, and draw the log rate of each vertex from a normal around its parent's log rate with variance $0.1\,\Delta$, in the order AB, CD, A, B, C, D, with `random.Random(1)`. The vertex rates are 2.025 at AB, 1.582 at CD, 2.086 at A, 1.439 at B, 0.793 at C and 1.613 at D, and the branch rates, as the means of the two ends, are 2.056 for A and 1.732 for B, which are close to the rate 1.513 of the branch above them. The root-to-tip distances are 8.65, 8.00, 6.04 and 7.68.

## Where it is used

- **Dating.** BEAST, MCMCTree and similar programs use relaxed clocks with fossil calibrations to estimate the ages of nodes, as on the [divergence time page](/divergence-time-estimation/).
- **Tree inference.** A relaxed clock also roots the tree, and in a [Bayesian](/bayesian-phylogenetic-inference/) analysis the topology, the ages and the rates are sampled together.
- **Measuring rate variation.** The fitted $\sigma$ of a UCLN, or $\nu$ of an autocorrelated model, says how far the data depart from a strict clock.
- **Not site rates.** A relaxed clock varies the rate across branches. [Rate heterogeneity](/rate-heterogeneity/) varies it across sites, and the two are often used together.

## References
