---
tag: 9TAFH9
kind: concept
slug: scale-free-network
name: Scale-free network
aliases:
- power-law network
area: graphs/network-analysis
level: core
summary: Network whose degree distribution follows a power law.
prereqs: [degree-distribution, degree, graph]
see_also: [preferential-attachment, barabasi-albert-model, degree-distribution, configuration-model, chung-lu-model, percolation, small-world-network, assortativity]
sources:
  - paper: doi:10.1126/science.286.5439.509
    title: Albert-László Barabási and Réka Albert, Emergence of scaling in random networks, Science 286(5439), 509 to 512 (1999)
    locator: the whole paper (power-law degree distributions in the web, actor and citation networks, and the model with growth and preferential attachment)
  - paper: doi:10.1137/070710111
    title: Aaron Clauset, Cosma Rohilla Shalizi and M. E. J. Newman, Power-law distributions in empirical data, SIAM Review 51(4), 661 to 703 (2009)
    locator: Section 3, the maximum likelihood estimator of the exponent and its standard error, and Section 4, the goodness-of-fit test
  - paper: doi:10.1038/35019019
    title: Réka Albert, Hawoong Jeong and Albert-László Barabási, Error and attack tolerance of complex networks, Nature 406, 378 to 382 (2000)
    locator: the whole paper (removal of random vertices against removal of the vertices of highest degree)
  - paper: doi:10.1103/PhysRevLett.86.3200
    title: Romualdo Pastor-Satorras and Alessandro Vespignani, Epidemic spreading in scale-free networks, Physical Review Letters 86(14), 3200 to 3203 (2001)
    locator: the whole paper (the epidemic threshold proportional to the ratio of the first to the second moment of the degree, which vanishes when the second moment diverges)
  - paper: doi:10.1038/s41467-019-08746-5
    title: Anna D. Broido and Aaron Clauset, Scale-free networks are rare, Nature Communications 10, 1017 (2019)
    locator: the whole paper (the test of almost 1000 real networks against a power law and its alternatives)
  - paper: doi:10.1103/PhysRevLett.90.058701
    title: Reuven Cohen and Shlomo Havlin, Scale-free networks are ultrasmall, Physical Review Letters 90(5), 058701 (2003)
    locator: the whole paper (distances of order ln ln n for degree exponents between 2 and 3)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 8, The large-scale structure of networks (the section on degree distributions and power laws)
---

A scale-free network is a network whose [degree distribution](/degree-distribution/) follows a power law: the fraction of vertices of [degree](/degree/) $k$ falls like $k^{-\gamma}$ for large $k$, with a fixed exponent $\gamma$, usually between 2 and 3. Such a network has a few hubs with a very large degree and many vertices with a small one, and no degree is typical. Barabási and Albert (1999) reported power laws in the web and in other networks and explained them by [preferential attachment](/preferential-attachment/); how common true power laws are in real data is still debated.

## In plain words

In many networks, most members have only a few links, but a few members have an enormous number. On the web, most pages get a handful of links and a few sites get millions. In airline networks, most airports have a few routes and a few hubs have hundreds.

If you count how many members have each number of links, the counts drop in a regular way: each time the number of links doubles, the count drops by the same factor. This rule is called a power law. It has no natural scale: the picture looks the same whether you look at small or at large numbers of links.

The hubs matter a lot. They keep the network together when random members fail, but removing the hubs breaks it quickly. They also help diseases and rumours spread.

## The idea

**Definition.** Let $p_k$ be the fraction of vertices of degree $k$ in an undirected graph, or the limit of this fraction for a family of random graphs as $n \to \infty$. The network is *scale-free* when there are constants $\gamma > 1$, $c > 0$ and $k_{\min} \ge 1$ such that

$$p_k \sim c\, k^{-\gamma} \quad \text{for } k \ge k_{\min}.$$

For a directed graph, the in-degrees and the out-degrees are tested separately; the web graph has an in-degree exponent near 2.1. The definition uses the number of edges, not their weights; for a weighted graph the same test can be applied to the strengths (the sums of weights), which is a different statement. A finite graph can only fit a power law approximately, over a range of degrees, so the claim is statistical.

**Why "scale-free".** A power law is the only form with $p_{ak} / p_k$ independent of $k$: for $f(k) = c k^{-\gamma}$, $f(ak) = a^{-\gamma} f(k)$ for every $a > 0$. A change of the unit of degree only changes the constant. An exponential or a Poisson law has a typical scale, the mean, beyond which it falls off quickly.

**Moments.** The $r$-th moment $\langle k^r \rangle = \sum_k k^r p_k$ is finite exactly when $\sum_k k^{r - \gamma}$ converges, that is, when $\gamma > r + 1$. So:

- for $\gamma > 3$, the mean and the variance of the degree are finite;
- for $2 < \gamma \le 3$, the mean is finite but $\langle k^2 \rangle = \infty$ in the limit;
- for $\gamma \le 2$, even the mean diverges, which a sparse graph cannot have, since its mean degree is bounded.

In a finite graph, the moments are cut off at the largest degree $k_{\max}$, and $\langle k^2 \rangle$ grows like $k_{\max}^{3 - \gamma}$ when $2 < \gamma < 3$.

**The largest degree.** In a sample of $n$ degrees drawn from the law, the largest degree is typically where the expected number of vertices with degree at least $k$ falls to 1. Since $\sum_{j \ge k} p_j \approx \frac{c}{\gamma - 1} k^{-(\gamma - 1)}$, this gives

$$k_{\max} \approx k_{\min}\, n^{1/(\gamma - 1)}$$

up to a constant factor. For $\gamma < 3$, $k_{\max}$ grows faster than $\sqrt n$, which means a simple graph cannot hold such a sample without hubs that share many neighbours; this is the origin of the structural cutoff and of the negative degree correlation ([disassortativity](/assortativity/)) of many such graphs.

**Consequences.** When $\langle k^2 \rangle$ diverges:

- **Robustness.** The threshold for the [giant component](/giant-component/) under random removal of vertices ([percolation](/percolation/)) is governed by $\langle k^2 \rangle / \langle k \rangle$, and the network stays connected after the removal of almost all vertices at random. Removing the hubs first destroys it quickly (Albert, Jeong and Barabási).
- **Epidemics.** In the [SIR](/sir-epidemic-model/) and SIS models on such a network, the epidemic threshold is proportional to $\langle k \rangle / \langle k^2 \rangle$, which goes to 0 (Pastor-Satorras and Vespignani). Any infection rate can cause an outbreak in a large network.
- **Distances.** For $2 < \gamma < 3$, random graphs with this degree law have typical distances of order $\ln \ln n$, shorter than the $\ln n$ of the [small world](/small-world-network/) (Cohen and Havlin).

**Testing for a power law.** A straight line on a log-log plot of the histogram is not a test. Clauset, Shalizi and Newman fit $\gamma$ by maximum likelihood above a cut-off $x_{\min}$ (chosen to minimize the Kolmogorov-Smirnov distance), test the fit by a bootstrap, and compare it with alternatives such as the log-normal and the stretched exponential. For degrees $x_1, \ldots, x_N \ge x_{\min}$, the approximate estimator for integer data is

$$\hat\gamma = 1 + N \Bigl[\sum_{i=1}^{N} \ln \frac{x_i}{x_{\min} - \tfrac12}\Bigr]^{-1}, \qquad \text{with standard error about } \frac{\hat\gamma - 1}{\sqrt N}.$$

Broido and Clauset applied such tests to almost 1000 networks and found strong evidence for a power law in only a small fraction of them, while log-normal laws often fit as well or better.

## Examples

**Moments with a cutoff.** Take $p_k = k^{-2.5}/\zeta(2.5)$ for $k \ge 1$, where $\zeta(2.5) \approx 1.3415$. The mean degree is $\zeta(1.5)/\zeta(2.5) \approx 1.947$. If the degrees stop at $k_{\max}$, the second moment is $\sum_{k \le k_{\max}} k^{-0.5}/\zeta(2.5)$, which is about 13.9 for $k_{\max} = 100$ and about 148 for $k_{\max} = 10^4$: it grows like $\sqrt{k_{\max}}$ and has no limit.

**The largest degree.** With $\gamma = 2.5$, $k_{\min} = 1$ and $n = 10^6$ vertices, $k_{\max} \approx n^{1/1.5} = 10^4$. In a Poisson degree law with the same mean of about 2, the probability of a degree of even 30 is below $10^{-20}$.

**Fitting.** The ten degrees $1, 1, 1, 1, 2, 2, 3, 5, 8, 20$ with $x_{\min} = 1$ give $\hat\gamma = 1 + 10/\sum_i \ln(2x_i) \approx 1.62$, with a standard error of about $0.62/\sqrt{10} \approx 0.20$. Ten values are far too few for a test: the method needs hundreds of values above $x_{\min}$ to tell a power law from a log-normal.

**Models.**

- The [Barabási-Albert model](/barabasi-albert-model/) with $m$ edges per new vertex gives $p_k = \frac{2m(m+1)}{k(k+1)(k+2)}$ for $k \ge m$ in the limit, so $\gamma = 3$.
- The [configuration model](/configuration-model/) and the [Chung-Lu model](/chung-lu-model/) produce any prescribed degree law, including power laws with any $\gamma$.
- The [Erdős-Rényi model](/erdos-renyi-model/) and the [Watts-Strogatz model](/watts-strogatz-model/) are not scale-free: their degree laws have a Poisson or faster tail.

## Where it is used

- [Preferential attachment](/preferential-attachment/) and the [Barabási-Albert model](/barabasi-albert-model/): the main mechanism proposed to produce power laws.
- [Percolation](/percolation/) and network robustness: random failures against targeted attacks.
- [SIR epidemic model](/sir-epidemic-model/): the vanishing epidemic threshold and the case for vaccinating hubs.
- [Triangle counting](/triangle-counting/) and other graph algorithms: hubs make the naive methods slow, and degree-ordered methods were designed for heavy-tailed degrees.
- [Degree distribution](/degree-distribution/) and [assortativity](/assortativity/): the measures that describe the hubs and how they connect.

## References
