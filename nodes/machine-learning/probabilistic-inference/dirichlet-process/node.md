---
tag: CRF0XV
kind: model
slug: dirichlet-process
name: Dirichlet process
aliases:
- Chinese restaurant process
area: machine-learning/probabilistic-inference
level: research
summary: "A distribution over discrete distributions, used as a nonparametric prior for mixtures. Built by stick breaking or the Chinese restaurant process; for large n, n draws use about α log n clusters."
history:
  year: 1973
  people: [Thomas S. Ferguson, David Blackwell, James B. MacQueen, Jayaram Sethuraman]
  note: Ferguson defined the Dirichlet process in 1973. Blackwell and MacQueen gave its Polya urn scheme the same year, and Sethuraman gave the stick-breaking construction in 1994.
prereqs: [conjugate-prior, stirling-numbers-first-kind]
see_also: [gaussian-mixture-model, latent-dirichlet-allocation, gibbs-sampling, gaussian-process, variational-inference, harmonic-series, set-partition-generation, bayesian-inference]
sources:
  - paper: doi:10.1214/aos/1176342360
    title: "Thomas S. Ferguson, A Bayesian analysis of some nonparametric problems, Annals of Statistics 1(2):209-230, 1973"
    locator: the definition by Dirichlet distributed finite partitions, the mean and variance, the discreteness of the draws, and the posterior DP(α + n, ·)
  - paper: doi:10.1214/aos/1176342372
    title: "David Blackwell and James B. MacQueen, Ferguson distributions via Polya urn schemes, Annals of Statistics 1(2):353-355, 1973"
    locator: the generalized Polya urn whose limit distribution is the Dirichlet process, and the predictive rule
  - paper: "Jayaram Sethuraman, A constructive definition of Dirichlet priors, Statistica Sinica 4(2):639-650, 1994"
    title: Sethuraman 1994
    locator: the stick-breaking representation with Beta(1, α) fractions and independent atoms from H
  - paper: doi:10.1214/aos/1176342871
    title: "Charles E. Antoniak, Mixtures of Dirichlet processes with applications to Bayesian nonparametric problems, Annals of Statistics 2(6):1152-1174, 1974"
    locator: mixtures of Dirichlet processes, and the distribution of the number of distinct values in a sample, with Stirling numbers of the first kind
  - paper: "Warren J. Ewens, The sampling theory of selectively neutral alleles, Theoretical Population Biology 3(1):87-112, 1972"
    title: Ewens 1972
    locator: the Ewens sampling formula for the allele partition of a sample under the neutral infinite alleles model
  - paper: "Radford M. Neal, Markov chain sampling methods for Dirichlet process mixture models, Journal of Computational and Graphical Statistics 9(2):249-265, 2000"
    title: Neal 2000
    locator: Gibbs samplers for DP mixtures, including the collapsed sampler on cluster indicators for conjugate priors (Algorithm 3) and auxiliary parameters for non-conjugate priors (Algorithm 8)
  - paper: "Yee Whye Teh, Michael I. Jordan, Matthew J. Beal and David M. Blei, Hierarchical Dirichlet processes, Journal of the American Statistical Association 101(476):1566-1581, 2006"
    title: Teh, Jordan, Beal and Blei 2006
    locator: the hierarchical DP and the Chinese restaurant franchise, for groups of data that share clusters
  - paper: "Hemant Ishwaran and Lancelot F. James, Gibbs sampling methods for stick-breaking priors, Journal of the American Statistical Association 96(453):161-173, 2001"
    title: Ishwaran and James 2001
    locator: truncated stick-breaking priors and blocked Gibbs sampling
  - paper: "David M. Blei and Michael I. Jordan, Variational inference for Dirichlet process mixtures, Bayesian Analysis 1(1):121-143, 2006"
    title: Blei and Jordan 2006
    locator: mean field variational inference on the truncated stick-breaking representation
  - paper: "Michael D. Escobar and Mike West, Bayesian density estimation and inference using mixtures, Journal of the American Statistical Association 90(430):577-588, 1995"
    title: Escobar and West 1995
    locator: Gibbs sampling for DP mixtures of normals, with a Gamma prior on α and its update
  - paper: "Jeffrey W. Miller and Matthew T. Harrison, A simple example of Dirichlet process mixture inconsistency for the number of components, Advances in Neural Information Processing Systems 26, 2013"
    title: Miller and Harrison 2013
    locator: the posterior of the number of clusters of a DP mixture does not concentrate at the true finite number
---

A Dirichlet process $\mathrm{DP}(\alpha, H)$ is a probability distribution whose draws are themselves probability distributions. It has a *base distribution* $H$, which is the mean of the draws, and a *concentration* $\alpha > 0$, which controls how close the draws are to $H$. Ferguson defined it in 1973 as a prior for Bayesian statistics with no fixed number of parameters. Its draws are discrete with probability 1, so samples from a draw repeat earlier values. This makes the DP the standard prior for mixture models with an unknown number of clusters: for large $n$, $n$ data points use about $\alpha \log n$ clusters, and the number grows as data arrive. Two constructions make it computable: the *Chinese restaurant process*, which is the Polya urn of Blackwell and MacQueen (1973), and *stick breaking* (Sethuraman 1994).

## The machine

**Definition.** Let $H$ be a probability distribution on a space $\Theta$ and let $\alpha > 0$. A random probability distribution $G$ on $\Theta$ is a Dirichlet process, $G \sim \mathrm{DP}(\alpha, H)$, if for every finite partition $A_1, \ldots, A_r$ of $\Theta$ into measurable sets,

$$\big(G(A_1), \ldots, G(A_r)\big) \sim \mathrm{Dir}\big(\alpha H(A_1), \ldots, \alpha H(A_r)\big).$$

Ferguson showed that such a process exists. From the Dirichlet marginals, for each set $A$,

$$\mathbb{E}[G(A)] = H(A), \qquad \operatorname{Var}[G(A)] = \frac{H(A)\,(1 - H(A))}{\alpha + 1}.$$

So $H$ is the mean, and a large $\alpha$ gives draws close to $H$.

**Conjugacy.** If $G \sim \mathrm{DP}(\alpha, H)$ and $\theta_1, \ldots, \theta_n$ are independent draws from $G$, then

$$G \mid \theta_1, \ldots, \theta_n \;\sim\; \mathrm{DP}\Big(\alpha + n,\ \frac{\alpha H + \sum_{i=1}^{n} \delta_{\theta_i}}{\alpha + n}\Big),$$

where $\delta_\theta$ is the point mass at $\theta$ (Ferguson 1973). On each finite partition this is the [conjugate](/conjugate-prior/) update of a Dirichlet prior by multinomial counts. Taking the mean of the posterior gives the *predictive rule*:

$$\theta_{n+1} \mid \theta_1, \ldots, \theta_n \;\sim\; \frac{\alpha}{\alpha + n} H + \frac{1}{\alpha + n} \sum_{i=1}^{n} \delta_{\theta_i}.$$

The new value is a fresh draw from $H$ with probability $\alpha/(\alpha + n)$, and otherwise a copy of an old value chosen uniformly. This is the Blackwell-MacQueen urn.

**DP mixtures.** Since $G$ is discrete, data are usually modeled with an extra layer (Antoniak 1974):

$$G \sim \mathrm{DP}(\alpha, H), \qquad \theta_i \mid G \sim G, \qquad x_i \mid \theta_i \sim F(\theta_i).$$

Data points with the same $\theta$ form a cluster, and $F$ is the cluster distribution, for example a normal distribution with mean $\theta$. This is a mixture model with infinitely many components, of which only finitely many are used by $n$ points.

## What it counts

The quantities of interest for $n$ draws $\theta_1, \ldots, \theta_n$ are combinatorial. With $G$ integrated out, the draws are fixed by a random partition of $\{1, \ldots, n\}$ into blocks of equal values, together with one draw from $H$ for each block. The model counts:

- **the probability of a partition**, which depends only on the block sizes (the Ewens formula below);
- **the number of blocks** $K_n$, which is the number of clusters a DP mixture uses for $n$ points: its distribution, its mean $\sum_{i=1}^n \alpha/(\alpha + i - 1)$, and its growth $\alpha \log n$;
- **the weights of $G$**, in the stick-breaking construction, and the mass left after the first $K$ weights.

Sampling costs are counted in draws from the uniform, Beta and base distributions and in arithmetic operations.

## Relation to other models

- **Finite Dirichlet mixtures.** A mixture with $K$ components and weights $\pi \sim \mathrm{Dir}(\alpha/K, \ldots, \alpha/K)$ gives, as $K \to \infty$, the same distribution on partitions as the DP. So a DP mixture is the limit of a [Gaussian mixture model](/gaussian-mixture-model/) or other finite mixture with a symmetric Dirichlet prior on the weights and more and more components.
- **Latent Dirichlet allocation.** [LDA](/latent-dirichlet-allocation/) gives each document a finite Dirichlet mixture over $K$ shared topics. The hierarchical Dirichlet process of Teh et al. (2006) draws a global $G_0 \sim \mathrm{DP}(\gamma, H)$ and each document's $G_d \sim \mathrm{DP}(\alpha, G_0)$. Because $G_0$ is discrete, the documents share atoms, and the number of topics is unbounded.
- **Pitman-Yor process.** Adding a discount $0 \le d < 1$ to the restaurant (a new table with probability $(\alpha + d K)/(\alpha + n)$, an existing table $j$ with probability $(n_j - d)/(\alpha + n)$) gives $K_n$ growing like $n^d$, a power law, instead of $\log n$. The DP is the case $d = 0$.
- **Gaussian processes.** A [Gaussian process](/gaussian-process/) is the other basic nonparametric prior: it is a prior over functions, where the DP is a prior over distributions.
- **Ewens sampling formula.** In population genetics the same partition distribution describes how a sample of $n$ genes splits into allele types under neutral mutation, with Ewens's $\theta$ in place of $\alpha$ (Ewens 1972).

## Known results in the model

### The two constructions

```pseudo id=main
CHINESE-RESTAURANT(n, α)
L1  no tables; sizes ← empty list
L2  for i ← 1 to n                         ▷ customer i arrives; i − 1 are seated
L3      draw u uniform on [0, α + i − 1)   ▷ table j takes length n_j, a new table takes α
L4      if u falls in the new table part: open a table of size 1 (and draw its value θ ~ H)
L5      else: join table j, so n_j ← n_j + 1
L6  return the table of each customer and the sizes

STICK-BREAKING(α, H, K)
L7  remaining ← 1
L8  for k ← 1 to K
L9      V_k ~ Beta(1, α);  π_k ← V_k · remaining;  remaining ← remaining · (1 − V_k);  θ_k ~ H
L10 return the weights π_1..π_K, the atoms θ_1..θ_K, and remaining
```

In the restaurant, customer $i$ joins an existing table $j$ with probability $n_j/(\alpha + i - 1)$ and opens a new table with probability $\alpha/(\alpha + i - 1)$. Giving each table a value from $H$ gives the Blackwell-MacQueen urn: $\theta_i$ is the value of the table of customer $i$. Each customer costs $O(K)$ time for $K$ open tables, so seating $n$ customers costs $O(n K_n)$, about $O(\alpha\, n \log n)$ on average.

Sethuraman's theorem: with $V_k \sim \mathrm{Beta}(1, \alpha)$ and $\theta_k \sim H$ all independent, $G = \sum_{k=1}^{\infty} \pi_k \delta_{\theta_k}$ with $\pi_k = V_k \prod_{j<k} (1 - V_j)$ is a draw from $\mathrm{DP}(\alpha, H)$. This shows directly that $G$ is discrete. The construction must be cut at some $K$. The mass left after $K$ sticks is $\prod_{j \le K} (1 - V_j)$, and since $\mathbb{E}[1 - V_j] = \alpha/(1 + \alpha)$ and the $V_j$ are independent,

$$\mathbb{E}\Big[1 - \sum_{k=1}^{K} \pi_k\Big] = \Big(\frac{\alpha}{1 + \alpha}\Big)^{K}.$$

For $\alpha = 2$ and $K = 5$ this is $(2/3)^5 \approx 0.132$, and $K = 12$ brings it below $0.01$. The expected remainder falls geometrically, but slowly for large $\alpha$: about $\alpha \log(1/\varepsilon)$ sticks are needed for a remainder $\varepsilon$. Truncated stick breaking is the basis of blocked Gibbs samplers (Ishwaran and James 2001) and of variational inference for DP mixtures (Blei and Jordan 2006). The tests of this page check the formula for the remainder by simulation, and check that the two constructions agree on $P(\theta_1 = \theta_2)$: it is $1/(1 + \alpha)$ in the urn, and $\mathbb{E}[\sum_k \pi_k^2] = 1/(1 + \alpha)$ for stick breaking.

### The Ewens sampling formula

**Theorem.** The probability that the restaurant seats $n$ customers in a given partition with blocks of sizes $n_1, \ldots, n_K$ is

$$P(n_1, \ldots, n_K) = \frac{\alpha^K \prod_{j=1}^{K} (n_j - 1)!}{\alpha (\alpha + 1) \cdots (\alpha + n - 1)}.$$

*Proof.* Follow the customers in order. Customer $i$ has the denominator $\alpha + i - 1$ whatever happens, so the denominators multiply to the rising factorial $\alpha^{(n)} = \alpha(\alpha + 1)\cdots(\alpha + n - 1)$. The first customer of each block opens a table, with numerator $\alpha$, which gives $\alpha^K$. The later customers of a block of size $n_j$ join it when it has $1, 2, \ldots, n_j - 1$ people, with numerators that multiply to $(n_j - 1)!$. $\square$

The probability depends only on the block sizes, not on the order of the customers, so the partition is exchangeable, as the draws $\theta_i$ from $G$ must be. The tests check the theorem exactly with rational $\alpha$: for $n \le 6$ they enumerate all $B_n$ partitions (203 for $n = 6$), compare the product of the seating steps with the formula, and check that the probabilities add up to 1.

### The number of clusters

**Theorem (Antoniak 1974).** The number of tables $K_n$ satisfies

$$P(K_n = k) = \frac{\left[{n \atop k}\right] \alpha^k}{\alpha (\alpha + 1) \cdots (\alpha + n - 1)}, \qquad \mathbb{E}[K_n] = \sum_{i=1}^{n} \frac{\alpha}{\alpha + i - 1},$$

where $\left[{n \atop k}\right]$ is the unsigned [Stirling number of the first kind](/stirling-numbers-first-kind/), the number of permutations of $n$ elements with $k$ cycles.

*Proof.* Sum the Ewens formula over all partitions with $k$ blocks. Each term has the factor $\alpha^k / \alpha^{(n)}$, and $\sum \prod_j (n_j - 1)!$ counts the permutations with $k$ cycles, since a block of size $m$ can be made into a cycle in $(m - 1)!$ ways. For the mean, customer $i$ opens a new table with probability $\alpha/(\alpha + i - 1)$, whatever the earlier seating was, and $K_n$ is the sum of these indicators. $\square$

The indicators are in fact independent, so $\operatorname{Var}[K_n] = \sum_i \alpha (i - 1)/(\alpha + i - 1)^2$. The mean equals $\alpha\big(\psi(\alpha + n) - \psi(\alpha)\big)$, with $\psi$ the digamma function, and it is close to $\alpha \log(1 + n/\alpha)$ for large $n$. For $\alpha = 1$ it is the [harmonic number](/harmonic-series/) $H_n$, and for $n = 1000$ it is $7.4855$. For $\alpha = 10$ and $n = 1000$ it is $46.65$, against $10 \log 101 \approx 46.15$. The number of clusters grows without bound, but only logarithmically.

### A worked example

Take $\alpha = 2$ and $n = 4$, so $\alpha^{(4)} = 2 \cdot 3 \cdot 4 \cdot 5 = 120$. The seating "1 and 2 together, 3 alone, 4 alone" has the steps

$$\frac{2}{2} \cdot \frac{1}{3} \cdot \frac{2}{4} \cdot \frac{2}{5} = \frac{1}{15},$$

and the Ewens formula gives the same: $2^3 \cdot 1! \cdot 0! \cdot 0! / 120 = 8/120 = 1/15$. The seating "1 alone, 2 and 3 together, 4 alone" has the steps $\frac{2}{2} \cdot \frac{2}{3} \cdot \frac{1}{4} \cdot \frac{2}{5} = \frac{1}{15}$ too, as exchangeability says. The Stirling numbers $\left[{4 \atop k}\right] = 6, 11, 6, 1$ for $k = 1, 2, 3, 4$ give

| $k$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $P(K_4 = k)$ | $12/120 = 1/10$ | $44/120 = 11/30$ | $48/120 = 2/5$ | $16/120 = 2/15$ |

and $\mathbb{E}[K_4] = 1 + 2/3 + 2/4 + 2/5 = 77/30 \approx 2.567$. A simulation of 40000 restaurants with seed 1 matches the 15 partition probabilities within total variation 0.015.

### Inference in DP mixtures

The posterior of a DP mixture given data $x_1, \ldots, x_n$ has no closed form, and Markov chain Monte Carlo is the standard tool. Neal (2000) reviews the [Gibbs samplers](/gibbs-sampling/). When $H$ is a conjugate prior for $F$, the parameters integrate out, and his Algorithm 3 resamples each cluster indicator $c_i$ in turn:

$$P(c_i = c \mid c_{-i}, x) \propto \begin{cases} n_{-i,c} \displaystyle\int F(x_i \mid \theta) \, dH_{-i,c}(\theta) & \text{for an existing cluster } c, \\[2mm] \alpha \displaystyle\int F(x_i \mid \theta) \, dH(\theta) & \text{for a new cluster,} \end{cases}$$

where $H_{-i,c}$ is the posterior of $\theta$ given the other points of cluster $c$. This is the restaurant rule with each table weighted by how well it predicts $x_i$. For non-conjugate $H$, Neal's Algorithm 8 adds auxiliary parameters for the new clusters. Truncated stick breaking gives blocked Gibbs samplers and [variational](/variational-inference/) methods instead.

### Pitfalls

- **Reading $K_n$ as the true number of clusters.** The DP prior makes $K_n$ grow like $\alpha \log n$ even when the data have a fixed number of clusters, and the posterior of the number of clusters in a DP mixture is not consistent for a finite true number (Miller and Harrison showed this in 2013). Treat the clusters as a flexible density model, not a count.
- **Fixing $\alpha$ carelessly.** $\alpha$ controls the number of clusters directly. Put a Gamma prior on it and sample it, as Escobar and West did, or check the prior mean $\sum_i \alpha/(\alpha + i - 1)$ against what is plausible.
- **Truncating too early.** With large $\alpha$, the remainder $(\alpha/(1 + \alpha))^K$ shrinks slowly. Check the mass left, or let the truncation level grow.
- **Continuous data in the urn.** The urn gives ties with positive probability. Applied directly to continuous observations, which never tie, the DP is the wrong model; use a DP mixture.
- **Label switching.** The cluster numbers are arbitrary, so posterior averages of per-cluster quantities over samples are meaningless without matching the clusters. Quantities such as "do $i$ and $j$ share a cluster" are safe.

## References
