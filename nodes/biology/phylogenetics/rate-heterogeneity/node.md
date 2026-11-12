---
tag: R7P245
kind: concept
slug: rate-heterogeneity
name: Rate heterogeneity among sites
aliases:
- gamma rate heterogeneity
- among-site rate variation
- discrete gamma model
area: biology/phylogenetics
level: advanced
summary: Sites of a gene change at different speeds. Models scale Q by a random rate per site, usually a discrete gamma with K classes (+G) and a share of invariable sites (+I).
prereqs: [substitution-model, phylogenetic-likelihood]
see_also: [jukes-cantor-model, gtr-model, felsenstein-pruning, maximum-likelihood-phylogeny, gauss-laguerre-quadrature, expectation-maximization, long-branch-attraction, hky-model]
sources:
  - paper: doi:10.1007/BF00160154
    title: Ziheng Yang, Maximum likelihood phylogenetic estimation from DNA sequences with variable rates over sites, approximate methods, Journal of Molecular Evolution 39(3) (1994)
    locator: pp. 306 to 314 (the discrete gamma model with K equal-probability categories, the mean and median rates of each category, and the accuracy for small K)
  - paper: doi:10.1093/oxfordjournals.molbev.a040235
    title: Xun Gu, Yun-Xin Fu and Wen-Hsiung Li, Maximum likelihood estimation of the heterogeneity of substitution rate among nucleotide sites, Molecular Biology and Evolution 12(4) (1995)
    locator: pp. 546 to 557 (the model with a proportion of invariable sites and gamma rates for the rest)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 1 (the gamma distance) and Chapter 4 (models of rate variation among sites in the likelihood of a tree)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 16, Likelihood methods (rate variation among sites, hidden Markov models of rates)
---

The substitution models on the earlier pages give every site of an alignment the same rate matrix $Q$. In real genes this is false. Sites that are critical for the function of a protein almost never change, third positions of codons change fast, and loops change faster than cores. *Rate heterogeneity* models keep one $Q$ but give each site its own rate $r$, so that the site evolves under $rQ$. The rate is not observed, so the likelihood of a site averages over a rate distribution with mean 1. The standard choice is a gamma distribution with shape $\alpha$, approximated by $K$ equal-probability classes (Yang 1994), often with an extra class of invariable sites. Models with these parts carry the suffixes +G (or +$\Gamma$) and +I, as in GTR+I+G.

## In plain words

Some letters in a gene can hardly change without killing the organism, while others change freely. If you assume they all change at one speed, you misread the data. The fast positions look as if they changed only a little, because many of their changes are hidden, and the slow positions make the tree look shorter than it is.

So the model says each position has its own speed, drawn at random from a spread of speeds. You do not know the speed of any one position. Instead, you work out the chance of what you see at that position for a few typical speeds, from very slow to very fast, and you take the average. A second option adds a group of positions that never change at all. One number sets how wide the spread of speeds is.

## The idea

**A rate per site.** Let $f(r)$ be a density on $r \ge 0$ with mean 1. Given the rate $r$, a site evolves on the tree under $rQ$, so every branch of length $t$ acts as a branch of length $rt$. If $L_s(r)$ is the [phylogenetic likelihood](/phylogenetic-likelihood/) of site $s$ with all branch lengths multiplied by $r$, then

$$L_s = \int_0^\infty f(r)\, L_s(r)\, dr, \qquad \ln L = \sum_s \ln L_s.$$

Sites stay independent, and the rates are independent across sites. The mean of 1 keeps branch lengths in expected substitutions per site.

**The gamma distribution.** The standard density is the gamma with shape $\alpha$ and rate $\alpha$:

$$f(r) = \frac{\alpha^\alpha}{\Gamma(\alpha)} r^{\alpha - 1} e^{-\alpha r}, \qquad \mathbb E[r] = 1, \quad \mathrm{Var}[r] = \frac1\alpha.$$

One parameter controls the spread. For $\alpha < 1$ the density is L-shaped: most sites are nearly invariant and a few are very fast. For large $\alpha$ the rates cluster near 1, and $\alpha \to \infty$ gives back the model with one rate.

**The discrete gamma.** The integral over $r$ has no closed form on a tree, because $L_s(r)$ is a sum of products of the matrices $P(rt_e)$ over all internal states. Yang's 1994 method replaces $f$ by $K$ classes of equal probability $1/K$. The cut points $c_1 < \cdots < c_{K-1}$ are the $k/K$ quantiles of the gamma distribution, and class $k$ gets one rate $r_k$:

- the *mean method* uses the mean of $r$ inside the class. Because $r f(r)$ is the density of a gamma with shape $\alpha + 1$ and rate $\alpha$, the mean is $r_k = K \left[ G(c_k) - G(c_{k-1}) \right]$, where $G$ is the distribution function of that gamma (with $c_0 = 0$ and $c_K = \infty$). These rates have mean exactly 1.
- the *median method* uses the median of each class, then rescales the $K$ rates so that their mean is 1.

The site likelihood becomes $L_s = \frac1K \sum_{k=1}^{K} L_s(r_k)$. It costs $K$ runs of [pruning](/felsenstein-pruning/), so the time is $K$ times that of the model with one rate. Yang found that $K = 4$ already gives a close approximation, and $K = 4$ is the default of most programs.

**Invariable sites.** The +I model says that a share $p$ of the sites cannot change, with rate 0, and the rest have rate $r/(1 - p)$, which keeps the mean at 1. If the leaves of site $s$ all show base $x$, the invariable class adds $p\, \pi_x$ to $L_s$; for any other site it adds 0. So

$$L_s = p \cdot [\text{site } s \text{ is constant at } x]\, \pi_x + (1 - p) \cdot L_s^{\text{var}},$$

where $L_s^{\text{var}}$ uses the scaled rates. Gu, Fu and Li combined it with the gamma in 1995 to give +I+G. The two parameters $\alpha$ and $p$ explain the same feature of the data, an excess of constant sites, so their estimates are strongly correlated, and some authors advise against fitting both.

**A distance with gamma rates.** For two sequences under JC69 with gamma rates, the probability of a difference is $\tfrac34 \left(1 - \mathbb E\left[e^{-4dr/3}\right]\right)$, and the moment generating function of the gamma gives $\mathbb E[e^{-4dr/3}] = (1 + \tfrac{4d}{3\alpha})^{-\alpha}$. Solving for $d$,

$$\hat d = \frac34 \alpha \left[ \left(1 - \frac43 \hat p\right)^{-1/\alpha} - 1 \right].$$

As $\alpha \to \infty$, this tends to the [JC69 distance](/jukes-cantor-model/).

**Other rate models.** A *free-rate* model lets the $K$ class rates and weights be free parameters instead of gamma quantiles. Partitioned models give each codon position or each gene its own rate. *Covarion* models let a site switch between on and off over time, and hidden Markov models of rates let neighbouring sites have similar rates; the [forward-backward algorithm](/forward-backward-algorithm/) handles the latter. A [Gauss-Laguerre quadrature](/gauss-laguerre-quadrature/) of the gamma integral is another way to choose the class rates, with unequal weights.

## Examples

**Discrete gamma rates.** With $K = 4$ and the mean method:

| $\alpha$ | $r_1$ | $r_2$ | $r_3$ | $r_4$ | cut points |
|---|---|---|---|---|---|
| 0.5 | 0.0334 | 0.2519 | 0.8203 | 2.8944 | 0.1015, 0.4549, 1.3233 |
| 1 | 0.1370 | 0.4768 | 1.0000 | 2.3863 | 0.2877, 0.6931, 1.3863 |
| 2 | 0.2933 | 0.6550 | 1.0700 | 1.9817 | 0.4806, 0.8392, 1.3463 |

For $\alpha = 1$ the gamma is the exponential distribution, and the cut points are $\ln(4/3)$, $\ln 2$ and $\ln 4$. For $\alpha = 0.5$, the median method gives $0.0291, 0.2807, 0.9248, 2.7654$ instead. At $\alpha = 0.5$ the fastest quarter of the sites changes 87 times as fast as the slowest quarter.

**One site on two taxa.** Two sequences are at distance $d = 0.5$ under JC69, and the likelihood of a site is $\tfrac14 P_{xy}(0.5 r)$, averaged over the rate classes.

| model | identical site | differing site |
|---|---|---|
| JC69 | 0.158766 | 0.030411 |
| JC69+G, $\alpha = 0.5$, $K = 4$ | 0.181908 | 0.022697 |
| JC69+I, $p = 0.2$ | 0.165190 | 0.028270 |

Both extensions put more probability on identical sites and less on differing ones, for the same distance. So when the data have many constant sites and some very variable ones, the extended models fit better and estimate a longer distance.

**Distances.** For $\hat p = 0.2$ the JC69+G distance is $0.322314$ at $\alpha = 0.5$, $0.272727$ at $\alpha = 1$ and $0.251623$ at $\alpha = 2$, against $0.232616$ with one rate. A model with one rate underestimates the distance, and more so when the rates are spread wider.

## Where it is used

- **Tree inference.** [Maximum likelihood phylogeny](/maximum-likelihood-phylogeny/) programs and [Bayesian phylogenetic inference](/bayesian-phylogenetic-inference/) fit $\alpha$ (and $p$) with the tree; GTR+G and HKY+G are common defaults. The cost is $K$ times the cost of one rate.
- **Avoiding artifacts.** Ignoring rate variation makes long branches too short and can cause [long branch attraction](/long-branch-attraction/) in likelihood methods, as it does in parsimony.
- **Distances.** Gamma distances such as the one above feed [neighbor joining](/neighbor-joining/) and other distance methods.
- **Finding fast and slow sites.** The posterior probability of each rate class at a site, $L_s(r_k) / (K L_s)$, ranks sites by rate. It is used to find conserved sites and sites under selection.

## References
