---
tag: PEBREY
kind: model
slug: birth-death-process
name: Birth-death process
aliases:
- birth-death model
- constant-rate birth-death process
area: biology/phylogenetics
level: advanced
summary: A model of speciation and extinction in which each lineage splits at rate lambda and dies at rate mu, giving random trees of species.
history:
  year: 1948
  people: [David G. Kendall]
  note: Kendall found the distribution of the population size of the birth-death process in 1948.
prereqs: [yule-model, markov-chain]
see_also: [yule-model, kingman-coalescent, coalescent-theory, phylogenetic-tree, bayesian-phylogenetic-inference, divergence-time-estimation, duplication-loss-model, linearity-of-expectation]
sources:
  - paper: doi:10.1214/aoms/1177730285
    title: David G. Kendall, On the generalized birth-and-death process, Annals of Mathematical Statistics 19(1), 1948
    locator: pp. 1-15 (the distribution of N(t) for constant and for time-dependent rates)
  - paper: doi:10.1098/rstb.1994.0068
    title: Sean Nee, Robert M. May and Paul H. Harvey, The reconstructed evolutionary process, Philosophical Transactions of the Royal Society of London B 344(1309), 1994
    locator: pp. 305-311 (the reconstructed tree of surviving lineages and the lineages-through-time curve)
  - paper: doi:10.1016/j.jtbi.2008.04.005
    title: Tanja Gernhard, The conditioned reconstructed process, Journal of Theoretical Biology 253(4), 2008
    locator: pp. 769-778 (the reconstructed tree conditioned on the number of living species)
---

The birth-death process is a random model of a tree of species. Each living lineage splits into two at rate $\lambda$ (a speciation) and ends at rate $\mu$ (an extinction), independently of the other lineages. With $\mu = 0$ it is the [Yule model](/yule-model/). Kendall found the distribution of the number of living lineages at each time in 1948. In phylogenetics the observed tree contains only the lineages that survive to the present, and this *reconstructed* tree has its own law, found by Nee, May and Harvey in 1994.

## The machine

**The state.** The state is the number $k$ of living lineages, together with the tree drawn so far. It is a continuous-time [Markov chain](/markov-chain/) on $\{0, 1, 2, \ldots\}$ and $0$ is absorbing.

**The moves.** With $k$ living lineages, the next event comes after an exponential time with rate $k(\lambda + \mu)$. It is a birth with probability $\lambda/(\lambda + \mu)$ and a death otherwise, and the lineage that splits or dies is uniform among the $k$. Write $r = \lambda - \mu$ for the net rate of diversification.

**The start and the stop.** The process starts from one lineage at time 0 (the origin of the clade) and stops at a time $t$, the present. Some writers start from two lineages at the root instead.

```pseudo id=main
SIMULATE-BIRTH-DEATH(λ, μ, t_max)
L1  k ← 1; t ← 0
L2  loop
L3      if k = 0 then return 0              ▷ the clade is extinct
L4      draw w from Exp(k(λ + μ))
L5      if t + w > t_max then return k
L6      t ← t + w
L7      with probability λ/(λ + μ): k ← k + 1     ▷ a birth
L8      otherwise: k ← k − 1                    ▷ a death
```

This is Gillespie's method. The number of steps is the number of events, and its mean grows like $e^{rt}$ when $r > 0$. Keep the living lineages in a list and record the parent and the times of each lineage to get the whole tree, not only its size.

**The complete and the reconstructed tree.** The complete tree has all lineages, also the extinct ones. The reconstructed tree removes every lineage with no living descendant at time $t$. Only the reconstructed tree can come from the DNA of living species.

## What it counts

- $N(t)$, the number of living lineages at time $t$, and the probability that the clade is extinct by $t$.
- The number of lineages in the reconstructed tree at each earlier time $s$, the *lineages-through-time* curve.
- The speciation times and the topology of the reconstructed tree, as a prior on trees in [Bayesian phylogenetics](/bayesian-phylogenetic-inference/) and in [divergence time estimation](/divergence-time-estimation/).

## Relation to other models

- **[Yule model](/yule-model/).** The case $\mu = 0$. The reconstructed tree of the birth-death process is again a pure-birth tree, but with a rate that changes with time (see below), so its labeled topology has the Yule law, and its branch lengths do not.
- **[Kingman coalescent](/kingman-coalescent/).** The coalescent is a backward model of gene copies inside one population; the birth-death process is a forward model of species. The coalescent tree and the reconstructed birth-death tree with the same number of tips both give each ranked labeled history the same probability.
- **[Duplication-loss model](/duplication-loss-model/).** Inside each branch of a species tree, the copies of a gene family follow a birth-death process, with duplication as birth and loss as death.
- **Models with varying rates.** Rates can change with time, with the lineage, or with a trait. Kendall's 1948 paper already gives $N(t)$ for rates that depend on time.

## Known results in the model

Write $z = e^{rt}$ and, for $\lambda \ne \mu$,

$$\alpha(t) = \frac{\mu (z - 1)}{\lambda z - \mu}, \qquad \beta(t) = \frac{\lambda (z - 1)}{\lambda z - \mu}.$$

**The number of lineages (Kendall 1948).** From one lineage,

$$P(N(t) = 0) = \alpha, \qquad P(N(t) = n) = (1 - \alpha)(1 - \beta)\beta^{\,n-1} \quad (n \ge 1).$$

So, given survival, $N(t)$ is geometric. If $\lambda = \mu$, then $\alpha = \beta = \lambda t/(1 + \lambda t)$.

*Proof.* Let $G(x, t) = E[x^{N(t)}]$. Condition on the first event in a short time $h$: the lineage splits with probability $\lambda h$, dies with probability $\mu h$, and the two daughters of a split run as independent copies. This gives the backward equation $\partial G/\partial t = \lambda G^2 - (\lambda + \mu) G + \mu = (\lambda G - \mu)(G - 1)$, with $G(x, 0) = x$. For $\lambda \ne \mu$, the partial fractions $\frac{1}{(\lambda G - \mu)(G - 1)} = \frac{1}{r}\left(\frac{1}{G - 1} - \frac{\lambda}{\lambda G - \mu}\right)$ separate the variables, and integration gives

$$\frac{G - 1}{\lambda G - \mu} = z \cdot \frac{x - 1}{\lambda x - \mu}.$$

Solved for $G$, this is $G = \alpha + (1 - \alpha)(1 - \beta)\frac{x}{1 - \beta x}$, the generating function of the law above. For $\lambda = \mu$ the equation is $\partial G / \partial t = \lambda (G - 1)^2$, with solution $\frac{1}{1 - G} = \frac{1}{1 - x} + \lambda t$, which gives the second form. $\square$

**The mean.** $E[N(t)] = (1 - \alpha)/(1 - \beta) = e^{rt}$. It also follows from $\frac{d}{dt} E[N] = (\lambda - \mu) E[N]$.

**Extinction.** The probability that the clade dies out at some time is $\mu/\lambda$ if $\lambda > \mu$ and 1 if $\lambda \le \mu$. It is the limit of $\alpha(t)$: for $r > 0$, $z \to \infty$ and $\alpha \to \mu/\lambda$; for $r < 0$, $z \to 0$ and $\alpha \to 1$; for $r = 0$, $\lambda t/(1 + \lambda t) \to 1$. So even a clade with $\lambda = \mu$ dies out with probability 1, although its mean size stays at 1.

**Survival for a time $u$.** From the formula for $\alpha$,

$$p(u) = 1 - \alpha(u) = \frac{r}{\lambda - \mu e^{-ru}}.$$

**Lineages through time (Nee, May and Harvey 1994).** Let the present be at time $T$. The expected number of lineages at time $s \le T$ that have a living descendant at $T$ is

$$E[\text{LTT}(s)] = e^{rs}\, p(T - s).$$

*Proof.* By the branching property, each lineage alive at $s$ starts an independent copy of the process, which survives for the remaining time $T - s$ with probability $p(T - s)$. By [linearity of expectation](/linearity-of-expectation/), the expected count is $E[N(s)]\, p(T - s)$. $\square$

On a log scale this curve has slope $r$ in the deep past, where $p(T - s)$ is almost constant. Near the present, $p(T - s) \to 1$ and the slope tends to $r + \mu = \lambda$: the lineages that arose a short time ago have not yet had time to die out. Nee, May and Harvey called this upturn the *pull of the present*. A plot of the log number of lineages in a reconstructed tree against time thus contains information on $\mu$, although no extinct lineage is seen.

**The reconstructed process.** Read forward in time, the reconstructed tree is a pure-birth process in which each lineage splits at the time-dependent rate $\lambda\, p(T - s)$ (Nee, May and Harvey 1994). Given $n$ living species and the time of origin, the $n - 1$ speciation times of the reconstructed tree are independent draws from one density (Gernhard 2008). Because a pure-birth process picks the lineage that splits uniformly whatever the rate, the labeled topology of the reconstructed tree has the [Yule](/yule-model/) law.

**An example.** Take $\lambda = 1$, $\mu = 0.5$ and $t = 2$, so $r = 0.5$ and $z = e \approx 2.718$. Then $\alpha \approx 0.387$ and $\beta \approx 0.775$. The clade is extinct by time 2 with probability $0.387$, it has one lineage with probability $0.138$ and two with probability $0.107$, and its mean size is $e \approx 2.718$. It dies out at some time with probability $0.5$.

For the lineages-through-time curve, take the same rates and a present at $T = 3$:

| time $s$ | $E[N(s)]$ | $E[\text{LTT}(s)]$ |
|---|---|---|
| 0 | 1.000 | 0.563 |
| 1 | 1.649 | 1.010 |
| 2 | 2.718 | 1.951 |
| 2.9 | 4.263 | 4.065 |
| 3 | 4.482 | 4.482 |

The gap between the columns is the expected number of lineages that have no living descendant. It is large in the past and closes at the present.

## References
