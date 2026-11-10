---
tag: G7ZY4M
kind: model
slug: hard-core-model
name: Hard-core model
aliases:
- hard-core lattice gas
- independent set model
area: randomized/markov-chain-monte-carlo
level: advanced
summary: The distribution π(I) ∝ λ^|I| on the independent sets I of a graph. Its partition function is the independence polynomial, and sampling and counting change from easy to hard at λ_c(Δ).
prereqs: [independent-set, ising-model]
see_also: [glauber-dynamics, gibbs-sampling, path-coupling, fpras, approximate-counting, counting-problem, mixing-time, coupling-from-the-past]
sources:
  - paper: doi:10.1145/1132516.1132538
    title: Dror Weitz, Counting independent sets up to the tree threshold, Proceedings of the 38th ACM Symposium on Theory of Computing (STOC), 2006
    locator: pages 140 to 149 (a deterministic FPTAS for λ < λ_c(Δ) by correlation decay on the self-avoiding walk tree)
  - paper: doi:10.1109/FOCS.2010.34
    title: Allan Sly, Computational transition at the uniqueness threshold, Proceedings of the 51st IEEE Symposium on Foundations of Computer Science (FOCS), 2010
    locator: pages 287 to 296 (no FPRAS for λ slightly above λ_c(Δ) unless NP = RP)
  - paper: doi:10.1214/13-AOP888
    title: Allan Sly and Nike Sun, Counting in two-spin models on d-regular graphs, Annals of Probability 42(6), 2014
    locator: pages 2383 to 2416 (hardness for every λ > λ_c(Δ))
  - paper: doi:10.1109/focs46700.2020.00125
    title: Nima Anari, Kuikui Liu and Shayan Oveis Gharan, Spectral independence in high-dimensional expanders and applications to the hardcore model, Proceedings of the 61st IEEE Symposium on Foundations of Computer Science (FOCS), 2020
    locator: pages 1319 to 1330 (Glauber dynamics mixes in polynomial time for every λ < λ_c(Δ))
  - book: isbn:9781470429621
    title: David A. Levin, Yuval Peres and Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, AMS, 2017
    locator: Chapter 3 (the hard-core model as an example of Metropolis and Glauber chains) and Chapter 14 (path coupling)
  - book: isbn:9783764369460
    title: Mark Jerrum, Counting, Sampling and Integrating, Birkhäuser, 2003
    locator: Chapter 3 (the reduction from approximate counting to almost uniform sampling for self-reducible problems)
---

The hard-core model is the probability distribution on the independent sets of a graph $G = (V, E)$ that gives an independent set $I$ weight $\lambda^{|I|}$, for a fugacity (activity) $\lambda > 0$. Each vertex is occupied or empty, and two neighbors may not both be occupied. At $\lambda = 1$ it is the uniform distribution on independent sets, and its partition function counts them. For graphs of maximum degree $\Delta$, the model has a sharp computational threshold at the tree uniqueness point $\lambda_c(\Delta) = (\Delta - 1)^{\Delta - 1}/(\Delta - 2)^{\Delta}$: below it, sampling and approximate counting are easy (Weitz 2006, Anari, Liu and Oveis Gharan 2020), and above it they are hard unless $\mathrm{NP} = \mathrm{RP}$ (Sly 2010, Sly and Sun 2014). This makes it a central test case for the link between [mixing time](/mixing-time/), phase transitions and [approximate counting](/approximate-counting/).

## The machine

A configuration is a set $I \subseteq V$ with no edge inside it, an [independent set](/independent-set/), or equally a vector $\eta \in \{0, 1\}^V$ with $\eta_u\eta_v = 0$ for every edge $uv$. The distribution is

$$\pi(I) = \frac{\lambda^{|I|}}{Z_G(\lambda)}, \qquad Z_G(\lambda) = \sum_{I \text{ independent}}\lambda^{|I|} = \sum_{k \ge 0}i_k(G)\lambda^k,$$

where $i_k(G)$ is the number of independent sets of size $k$. $Z_G$ is the independence polynomial of $G$, and $Z_G(1)$ is the number of independent sets. The constraint is "hard": a forbidden configuration has weight 0, not a small weight.

**Small examples.** The coefficient lists $(i_0, i_1, \ldots)$ are:

| graph | $i_k$ | $Z_G(1)$ | $Z_G(2)$ |
|---|---|---|---|
| path $P_4$ | 1, 4, 3 | 8 | 21 |
| cycle $C_4$ | 1, 4, 2 | 7 | 17 |
| cycle $C_5$ | 1, 5, 5 | 11 | 31 |
| $3 \times 3$ grid | 1, 9, 24, 22, 6, 1 | 63 | 419 |

For the 5-cycle at $\lambda = 2$, the mean number of occupied vertices is $(5 \cdot 2 + 2 \cdot 5 \cdot 4)/31 = 50/31$, and the [Gibbs sampling](/gibbs-sampling/) page checks a long seeded run against this exact value.

**The natural Markov chain.** Heat-bath [Glauber dynamics](/glauber-dynamics/) picks a uniform vertex $v$. If a neighbor of $v$ is occupied, $v$ becomes empty. Otherwise, $v$ becomes occupied with probability $\lambda/(1 + \lambda)$ and empty with probability $1/(1 + \lambda)$. This is the random-scan Gibbs sampler for $\pi$, so it is reversible with respect to $\pi$, and it is irreducible because every independent set can reach $\emptyset$ by removing vertices one at a time.

## What it counts

- **Independent sets.** $Z_G(1)$ is the number of independent sets, a #P-complete count even for restricted graph classes. Sampling at $\lambda = 1$ and approximate counting are equivalent up to polynomial factors, by the self-reducibility argument of Jerrum, Valiant and Vazirani: $Z_G = Z_{G - v}\big/\Pr_{\pi_G}(v \notin I)$ for each vertex $v$, so $n$ estimated ratios give $Z_G$ (see the [FPRAS](/fpras/) page).
- **Weighted counts and densities.** $Z_G(\lambda)$ for general $\lambda$, and the expected density $E|I|/n = \frac{\lambda}{n}\frac{d}{d\lambda}\log Z_G(\lambda)$.
- **Maximum independent sets.** As $\lambda \to \infty$, $\pi$ concentrates on the independent sets of maximum size. So sampling for large $\lambda$ is at least as hard as finding a maximum independent set, which is NP-hard.

## Relation to other models

- **[Ising model](/ising-model/).** Both are two-spin systems on a graph. The hard-core model is the limit of an antiferromagnetic lattice gas in which the repulsion of two occupied neighbors becomes infinite, so its behavior is antiferromagnetic: on bipartite graphs at large $\lambda$, it prefers one side of the bipartition.
- **[Gibbs sampling](/gibbs-sampling/) and [Glauber dynamics](/glauber-dynamics/).** The heat-bath chain above is the standard sampler.
- **[Counting problems](/counting-problem/).** Counting independent sets is the classic example where the threshold for approximate counting matches a phase transition of a statistical physics model.
- **Monotone coupling.** On a bipartite graph, flipping the meaning of occupied on one side makes the heat-bath chain monotone, so [coupling from the past](/coupling-from-the-past/) can sample exactly with two extreme starts.

## Known results in the model

**The tree threshold.** On the infinite $\Delta$-regular tree, the hard-core model has a unique Gibbs measure exactly when $\lambda \le \lambda_c(\Delta) = (\Delta - 1)^{\Delta - 1}/(\Delta - 2)^{\Delta}$. The values are

| $\Delta$ | 3 | 4 | 5 | 6 |
|---|---|---|---|---|
| $\lambda_c(\Delta)$ | 4 | 27/16 = 1.6875 | 256/243 ≈ 1.0535 | 3125/4096 ≈ 0.7629 |

and $\lambda_c(\Delta) \approx e/\Delta$ for large $\Delta$.

**Algorithms below the threshold.**

- **Path coupling.** If $\lambda < 1/(\Delta - 1)$, Glauber dynamics mixes in $O(n\log n)$ steps. Couple two configurations that differ only at $v$ by updating the same vertex with the same coin. An update at $v$ removes the difference, with probability $1/n$. An update at a neighbor $w$ of $v$ can create a new difference only if the coin says "occupied", with probability at most $\lambda/(1 + \lambda)$ for each of at most $\Delta$ neighbors. So the expected distance changes by at most $-\frac1n + \frac{\Delta\lambda}{(1 + \lambda)n}$, which is negative when $\lambda < 1/(\Delta - 1)$, and [path coupling](/path-coupling/) gives the bound.
- **Correlation decay.** Weitz (2006) gave a deterministic FPTAS for $Z_G(\lambda)$ for every $\lambda < \lambda_c(\Delta)$ on graphs of maximum degree $\Delta$, by computing marginals on a tree of self-avoiding walks and truncating it. Since $\lambda_c(5) > 1$, this counts independent sets approximately in graphs of maximum degree at most 5.
- **Spectral independence.** Anari, Liu and Oveis Gharan (2020) proved that Glauber dynamics mixes in polynomial time for every $\lambda < \lambda_c(\Delta)$, which matches the threshold with a Markov chain. Later work improved the bound to $O(n\log n)$ for constant $\Delta$.

**Hardness above the threshold.** Sly (2010) proved that for each $\Delta \ge 3$ there is an $\varepsilon(\Delta) > 0$ such that for $\lambda_c(\Delta) < \lambda < \lambda_c(\Delta) + \varepsilon(\Delta)$, there is no FPRAS for $Z_G(\lambda)$ on graphs of maximum degree $\Delta$ unless $\mathrm{NP} = \mathrm{RP}$. Sly and Sun (2014) removed the restriction and proved hardness for every $\lambda > \lambda_c(\Delta)$. Since $\lambda_c(6) < 1$, approximately counting independent sets in graphs of maximum degree 6 is hard. The reductions use random bipartite regular graphs, where the model at $\lambda > \lambda_c$ prefers one side, and the side can encode a maximum cut. On the same graphs, Glauber dynamics mixes in exponential time.

**On the lattice.** On $\mathbb{Z}^2$, the model has a phase transition: for large $\lambda$ the even and odd sublattices give two different phases, by a Peierls-type argument. The exact critical value on $\mathbb{Z}^2$ is not known.

## References
