---
tag: QWM2HP
kind: model
slug: stochastic-block-model
name: Stochastic block model
aliases:
- SBM
- planted partition model
area: graphs/network-analysis
level: advanced
summary: Random graph with community structure set by a block-wise edge probability matrix.
prereqs: [erdos-renyi-model, community-detection]
see_also: [erdos-renyi-model, community-detection, modularity, spectral-clustering, belief-propagation, planted-clique, configuration-model, girvan-newman-algorithm]
sources:
  - paper: doi:10.1016/0378-8733(83)90021-7
    title: Paul W. Holland, Kathryn Blackmond Laskey and Samuel Leinhardt, Stochastic blockmodels, first steps, Social Networks 5(2), 109 to 137 (1983)
    locator: the definition of the stochastic blockmodel with known blocks, and its estimation
  - paper: doi:10.1103/PhysRevE.83.016107
    title: Brian Karrer and M. E. J. Newman, Stochastic blockmodels and community structure in networks, Physical Review E 83(1), 016107 (2011)
    locator: the degree-corrected stochastic block model, its likelihood, and fitting it to find communities
  - paper: doi:10.1103/PhysRevE.84.066106
    title: Aurelien Decelle, Florent Krzakala, Cristopher Moore and Lenka Zdeborová, Asymptotic analysis of the stochastic block model for modular networks and its algorithmic applications, Physical Review E 84(6), 066106 (2011)
    locator: the belief propagation analysis and the conjectured detectability threshold for the sparse model
  - paper: doi:10.1109/TIT.2015.2490670
    title: Emmanuel Abbe, Afonso S. Bandeira and Georgina Hall, Exact recovery in the stochastic block model, IEEE Transactions on Information Theory 62(1), 471 to 487 (2016)
    locator: the sharp threshold for exact recovery of two equal communities with edge probabilities of order log n over n
  - paper: arxiv:1703.10146
    title: Emmanuel Abbe, Community detection and stochastic block models, recent developments, Journal of Machine Learning Research 18(177), 1 to 86 (2018)
    locator: the survey of the recovery requirements (exact, almost exact, partial) and their thresholds, Sections 3 to 5
---

The stochastic block model (SBM) is a random graph in which every vertex belongs to one of $k$ groups, and the probability of an edge depends only on the groups of its two ends. With high probability inside groups and low probability between them, it produces graphs with communities; with the reverse, it produces nearly bipartite structure. Holland, Laskey and Leinhardt (1983) introduced it in sociology, and it is now the standard test bed for [community detection](/community-detection/): an algorithm is judged by whether it can recover the hidden groups from the graph alone, and the model has sharp thresholds that say exactly when this is possible.

## The machine

**Parameters.** A number of vertices $n$, a number of blocks $k$, an assignment $\sigma : \{1, \dots, n\} \to \{1, \dots, k\}$ of vertices to blocks (fixed, or drawn independently with probabilities $\pi_1, \dots, \pi_k$), and a symmetric $k \times k$ matrix $P$ with entries in $[0, 1]$.

**Generation.** For each pair $i < j$, independently, add the undirected edge $\{i, j\}$ with probability $P_{\sigma(i)\sigma(j)}$. The graph is simple and unweighted; $k = 1$ is the [Erdős-Rényi model](/erdos-renyi-model/). The *directed* version uses a matrix that need not be symmetric and draws each ordered pair; the *weighted* version draws a weight for each pair from a distribution set by the two blocks, for example Poisson counts.

**The planted partition model.** The special case $P_{aa} = p$ and $P_{ab} = q$ for $a \ne b$. It is *assortative* when $p > q$, and *disassortative* when $p < q$. In the sparse regime, $p = a/n$ and $q = b/n$ with constants $a$ and $b$, so the mean degree is bounded; with two equal blocks it is $(a + b)/2$.

**The degree-corrected model.** Real networks have heavy-tailed degrees, which the plain SBM cannot produce, since all vertices in a block have the same expected degree. Karrer and Newman (2011) give each vertex a parameter $\theta_i$ and draw a Poisson number of edges between $i$ and $j$ with mean $\theta_i \theta_j \omega_{\sigma(i)\sigma(j)}$, so that degrees vary within a block. Fitting the plain model to a network with hubs tends to put the hubs in a block of their own.

**Likelihood.** Given a graph $G$ with edge set $E$, the probability of $G$ under the parameters is

$$L(\sigma, P) = \prod_{i < j} P_{\sigma(i)\sigma(j)}^{A_{ij}} \bigl(1 - P_{\sigma(i)\sigma(j)}\bigr)^{1 - A_{ij}}.$$

For a fixed $\sigma$, the maximizing $P_{ab}$ is the number of edges between blocks $a$ and $b$ divided by the number of pairs. Fitting the model means searching over $\sigma$, which is NP-hard in general and is done by local search, belief propagation, spectral methods or Monte Carlo sampling.

**Example.** Take $n = 6$, blocks $\{0, 1, 2\}$ and $\{3, 4, 5\}$, $p = 0.8$ and $q = 0.1$. The expected number of edges is $6 \times 0.8 = 4.8$ inside the blocks and $9 \times 0.1 = 0.9$ between them. The graph made of the two triangles and the edge 2-3 has probability $0.8^6 \times 0.1 \times 0.9^8 \approx 0.0113$, log-likelihood $-4.48$. Under the same $P$, the partition $\{0, 1, 2, 3\}$, $\{4, 5\}$ has log-likelihood $-9.57$. With $P$ refitted for each partition, the true partition gives $P_{11} = P_{22} = 1$ and $P_{12} = 1/9$ with log-likelihood $-3.14$, and the other gives $P_{11} = 2/3$, $P_{12} = 1/4$, $P_{22} = 1$ with $-8.32$, so maximum likelihood picks the true blocks.

## What it counts

- **Recovery of the blocks.** Given only the graph, how much of $\sigma$ can be recovered, up to a renaming of the blocks? Three standards are used: *exact recovery* (all of $\sigma$, with probability tending to 1), *almost exact recovery* (all but a vanishing fraction of the vertices), and *detection* or *partial recovery* (a fraction of the vertices correct that is better than chance by a constant).
- **The overlap.** For two equal blocks, if a guess agrees with $\sigma$ on a fraction $x$ of the vertices, after the better of the two namings, the overlap is $2x - 1$, which is 0 for a random guess and 1 for a perfect one.
- **Testing.** Whether a graph has block structure at all, against the Erdős-Rényi graph with the same mean degree.
- **Graph statistics.** Expected degrees, the [giant component](/giant-component/), and the counts of small subgraphs, which follow from $P$ and the block sizes.

## Relation to other models

- **[Erdős-Rényi model](/erdos-renyi-model/).** The case $k = 1$, or $p = q$. Each block of an SBM is an Erdős-Rényi graph, and the edges between two blocks form a random bipartite graph.
- **[Configuration model](/configuration-model/).** The degree-corrected SBM combines the degree heterogeneity of the configuration model with block structure.
- **[Modularity](/modularity/).** Maximizing modularity is equivalent to maximum likelihood in a degree-corrected planted partition model with a specific relation between the parameters (Newman, 2016), which explains both its success and its resolution limit.
- **[Planted clique](/planted-clique/).** Another planted model, with one small block with edge probability 1; its hardness is conjectured, while the SBM thresholds below are achieved by efficient algorithms.
- **Mixed membership and graphons.** Mixed-membership models let a vertex belong to several blocks; a graphon replaces the finite set of blocks by a continuum, and the SBM is a step-function graphon.

## Known results in the model

All results are for two blocks of equal size $n/2$ unless stated, as $n \to \infty$.

**Detection (sparse regime).** With $p = a/n$ and $q = b/n$, detection is possible if and only if

$$(a - b)^2 > 2(a + b).$$

Decelle, Krzakala, Moore and Zdeborová (2011) conjectured this threshold from belief propagation; Mossel, Neeman and Sly proved that detection is impossible below it, and Massoulié and Mossel, Neeman and Sly gave efficient algorithms above it. Plain spectral clustering with the adjacency matrix fails in this regime, because high-degree vertices dominate the top eigenvectors; non-backtracking and Bethe Hessian spectra reach the threshold. A simulation with $n = 2000$ and mean degree 5, splitting by the median of the second eigenvector of the Bethe Hessian $(c - 1)I - \sqrt{c}A + D$ with $c$ the mean degree (mean of 5 graphs):

| $a$, $b$ | 9, 1 | 8, 2 | 7.5, 2.5 | 7, 3 | 6.5, 3.5 | 6, 4 |
|---|---|---|---|---|---|---|
| $(a - b)^2 / (2(a + b))$ | 3.2 | 1.8 | 1.25 | 0.8 | 0.45 | 0.2 |
| overlap | 0.91 | 0.67 | 0.41 | 0.11 | 0.04 | 0.03 |

The overlap falls toward the level of chance, a few percent at this $n$, as the ratio drops below 1; at finite $n$ the transition is smooth.

**Exact recovery (logarithmic regime).** With $p = a \log n / n$ and $q = b \log n / n$, exact recovery is possible if and only if

$$\bigl(\sqrt{a} - \sqrt{b}\bigr)^2 > 2,$$

(Abbe, Bandeira and Hall; Mossel, Neeman and Sly), and it is achieved by semidefinite programming and by spectral methods followed by local cleanup. Below the threshold, some vertex has more neighbours in the other block than in its own, and no method can place it correctly. Exact recovery needs mean degree of order $\log n$ for the same reason the Erdős-Rényi graph needs it for connectivity: with bounded degrees, some vertices are isolated and carry no information.

**More blocks.** For $k$ equal blocks in the sparse regime, the Kesten-Stigum condition $(a - b)^2 > k(a + (k - 1)b)$ is sufficient for efficient detection. For $k \ge 5$ detection is possible information-theoretically somewhat below it, but no efficient algorithm is known there, a conjectured gap between what is possible and what is efficient.

**Disconnected graphs and ties.** In the sparse regime, the graph has a giant component and many small ones; vertices in small components cannot be classified better than chance, which is one reason the thresholds concern partial recovery. Ties in a maximum likelihood search, from the symmetry of renaming the blocks, are removed by measuring agreement up to a permutation.

## References
