---
tag: YBKBR8
kind: model
slug: exponential-random-graph-model
name: Exponential random graph model
aliases:
- ERGM
- p* model
area: graphs/network-analysis
level: advanced
summary: Exponential-family distribution over graphs defined by chosen structural statistics.
prereqs: [erdos-renyi-model, exponential-family-distribution, triangle-counting]
see_also: [stochastic-block-model, erdos-renyi-model, triadic-closure, reciprocity, homophily, gibbs-sampling, metropolis-hastings, markov-random-field]
sources:
  - paper: doi:10.1080/01621459.1981.10477598
    title: Paul W. Holland and Samuel Leinhardt, An exponential family of probability distributions for directed graphs, Journal of the American Statistical Association 76(373), 33 to 50 (1981)
    locator: the p1 model, with parameters for density, reciprocity and the out- and in-degree of each vertex, and its fit by maximum likelihood
  - paper: doi:10.1080/01621459.1986.10478342
    title: Ove Frank and David Strauss, Markov graphs, Journal of the American Statistical Association 81(395), 832 to 842 (1986)
    locator: the Markov dependence assumption, and the theorem, from the Hammersley-Clifford theorem, that the statistics are then counts of stars and triangles
  - paper: doi:10.1080/01621459.1990.10475327
    title: David Strauss and Michael Ikeda, Pseudolikelihood estimation for social networks, Journal of the American Statistical Association 85(409), 204 to 212 (1990)
    locator: the conditional logit form of each edge given the rest of the graph, and the maximum pseudolikelihood estimate by logistic regression
  - paper: doi:10.1007/BF02294547
    title: Stanley Wasserman and Philippa Pattison, Logit models and logistic regressions for social networks, I, an introduction to Markov graphs and p*, Psychometrika 61(3), 401 to 425 (1996)
    locator: the general exponential family p* over graphs and its change statistics
  - paper: doi:10.1111/j.1467-9531.2006.00176.x
    title: Tom A. B. Snijders, Philippa E. Pattison, Garry L. Robins and Mark S. Handcock, New specifications for exponential random graph models, Sociological Methodology 36, 99 to 153 (2006)
    locator: the degeneracy of Markov models with star and triangle counts, and the alternating k-star and k-triangle statistics that avoid it
  - paper: doi:10.1198/106186006X133069
    title: David R. Hunter and Mark S. Handcock, Inference in curved exponential family models for networks, Journal of Computational and Graphical Statistics 15(3), 565 to 583 (2006)
    locator: the geometrically weighted statistics as a curved exponential family, and maximum likelihood by Markov chain Monte Carlo
  - paper: doi:10.1214/10-AAP740
    title: Shankar Bhamidi, Guy Bresler and Allan Sly, Mixing time of exponential random graphs, Annals of Applied Probability 21(6), 2146 to 2170 (2011)
    locator: the high and low temperature phases of models with nonnegative parameters, the mixing time of the Glauber dynamics in each, and the closeness to an Erdős-Rényi graph at high temperature
  - paper: doi:10.1214/13-AOS1155
    title: Sourav Chatterjee and Persi Diaconis, Estimating and understanding exponential random graph models, Annals of Statistics 41(5), 2428 to 2461 (2013)
    locator: the large deviation limit of the normalizing constant, and the theorem that the edge-triangle model with a nonnegative triangle parameter looks like an Erdős-Rényi graph or a mixture of them
---

An exponential random graph model, or ERGM, is a probability distribution on the graphs with a fixed set of $n$ vertices in which the probability of a graph $G$ is proportional to $\exp(\theta_1 s_1(G) + \cdots + \theta_k s_k(G))$. The statistics $s_i$ are counts the modeller chooses, such as the number of edges, of [triangles](/triangle-counting/), of mutual pairs or of edges between vertices of the same group, and the parameters $\theta_i$ say how much each one is favoured. With the number of edges alone, it is the [Erdős-Rényi model](/erdos-renyi-model/) $G(n, p)$. ERGMs are the main statistical model of social networks, because they can express dependence between edges, such as the tendency of two friends of one person to become friends. Their normalizing constant is a sum over $2^{\binom n2}$ graphs, so they are fitted and sampled by Markov chain Monte Carlo, and badly chosen statistics make them *degenerate*, putting almost all of their mass on nearly empty or nearly complete graphs.

## The machine

**Parameters.** A number $n$ of labelled vertices, a vector of statistics $s(G) = (s_1(G), \ldots, s_k(G))$, each a real function of a graph on $\{1, \ldots, n\}$, and a parameter vector $\theta \in \mathbb{R}^k$. The graphs can be undirected or directed, and the statistics can use fixed attributes of the vertices, such as age or group.

**The distribution.** Let $\mathcal{G}_n$ be the set of all simple graphs on the $n$ vertices. Then

$$\Pr_\theta[G] = \frac{\exp(\theta \cdot s(G))}{Z(\theta)}, \qquad Z(\theta) = \sum_{H \in \mathcal{G}_n} \exp(\theta \cdot s(H)).$$

This is an [exponential family](/exponential-family-distribution/) with sufficient statistic $s(G)$ and log-normalizer $\psi(\theta) = \log Z(\theta)$. The observed network is one draw from it.

**Common statistics.**

- *Edges* $E(G)$, the number of edges; its parameter sets the density.
- *$k$-stars* $S_k(G) = \sum_v \binom{d(v)}{k}$, which reward spread or concentration of the degrees.
- *Triangles* $T(G)$, which reward [triadic closure](/triadic-closure/).
- *Mutual pairs* in a directed graph, the pairs with both arcs, for [reciprocity](/reciprocity/).
- *Attribute matches*, the number of edges between vertices of the same group, for [homophily](/homophily/).
- *Geometrically weighted* statistics, such as the alternating $k$-triangles of Snijders, Pattison, Robins and Handcock, which add the shared partners of each edge with weights that decrease geometrically.

**The conditional form of one edge.** For a pair $\{i, j\}$, let $G^+_{ij}$ and $G^-_{ij}$ be $G$ with and without the edge $\{i, j\}$, and let $\delta_{ij}(G) = s(G^+_{ij}) - s(G^-_{ij})$ be the *change statistic*. Then, given all the other pairs,

$$\log \frac{\Pr_\theta[\{i,j\} \in G \mid \text{rest}]}{\Pr_\theta[\{i,j\} \notin G \mid \text{rest}]} = \theta \cdot \delta_{ij}(G).$$

*Proof.* Given the rest, $G$ is either $G^+_{ij}$ or $G^-_{ij}$, so the ratio of the two conditional probabilities is the ratio $\Pr_\theta[G^+_{ij}] / \Pr_\theta[G^-_{ij}] = \exp(\theta \cdot s(G^+_{ij}) - \theta \cdot s(G^-_{ij}))$; $Z(\theta)$ cancels. $\square$

For the edge count, $\delta_{ij} = 1$; for the triangle count, $\delta_{ij}$ is the number of common neighbours of $i$ and $j$. So a positive triangle parameter makes an edge more likely the more friends its ends share.

**Sampling.** The conditional form gives a [Gibbs sampler](/gibbs-sampling/): repeatedly pick a pair and set it with the probability $1/(1 + \exp(-\theta \cdot \delta_{ij}))$. A [Metropolis-Hastings](/metropolis-hastings/) chain that proposes to toggle one pair works the same way. Neither needs $Z(\theta)$, and the stationary distribution is $\Pr_\theta$.

**Fitting.** The likelihood of an observed graph $G_{\mathrm{obs}}$ is $\exp(\theta \cdot s(G_{\mathrm{obs}}) - \psi(\theta))$. Since $\nabla \psi(\theta) = \mathbb{E}_\theta[s(G)]$, the [maximum likelihood estimate](/maximum-likelihood-estimation/), when it exists, is the $\theta$ with

$$\mathbb{E}_\theta[s(G)] = s(G_{\mathrm{obs}}),$$

which matches the expected statistics to the observed ones. *Proof of the gradient.* $\partial \psi / \partial \theta_i = \frac{1}{Z} \sum_H s_i(H) e^{\theta \cdot s(H)} = \mathbb{E}_\theta[s_i]$; $\psi$ is convex, as a log-sum of exponentials of linear functions, so a stationary point is a maximum of the log-likelihood. $\square$ The expectations are estimated by sampling, which is maximum likelihood by Markov chain Monte Carlo (Hunter and Handcock). The older shortcut of Strauss and Ikeda maximizes the *pseudolikelihood* $\prod_{i<j} \Pr_\theta[\text{pair } ij \mid \text{rest}]$, which by the conditional form is a [logistic regression](/logistic-regression/) of the pair indicators on their change statistics. It is fast, but its estimates and standard errors can be badly off when the edges depend strongly on each other.

## What it counts

**The edge model is $G(n, p)$.** With $s(G) = E(G)$ alone, $\Pr_\theta[G] \propto e^{\theta |E(G)|} = \prod_{i<j} e^{\theta x_{ij}}$, where $x_{ij}$ is the indicator of the pair. The pairs are independent, each present with probability $p = e^\theta/(1 + e^\theta)$. So $\theta = 0$ gives the uniform graph, $p = \frac12$, and $\theta = -1$ gives $p \approx 0.269$.

**Dyad independence.** If each statistic is a sum over pairs of a function of that pair alone, such as edges, attribute matches and, for directed graphs, mutual pairs, then the pairs, or dyads, are independent, and fitting is a logistic regression. Holland and Leinhardt's $p_1$ model is of this kind: it has a density, a reciprocity parameter and a parameter for the out-degree and the in-degree of each vertex. The [stochastic block model](/stochastic-block-model/) with known groups is also dyad independent.

**Triangles on three vertices.** Take $n = 3$ and $s = (E, T)$ with $\theta = (-1, 2)$. The 8 graphs fall into four kinds.

| graph | how many | $\theta \cdot s$ | probability of each |
|---|---|---|---|
| empty | 1 | 0 | 0.348 |
| one edge | 3 | $-1$ | 0.128 |
| two edges | 3 | $-2$ | 0.047 |
| triangle | 1 | $-3 + 2 = -1$ | 0.128 |

Here $Z = 1 + 4e^{-1} + 3e^{-2} \approx 2.878$. The expected density is $0.350$, and the triangle has probability $0.128$. In $G(3, 0.350)$, with the same density, the triangle has probability $0.350^3 \approx 0.043$. The triangle parameter has made closed triads three times as likely.

**How the triangle parameter pushes mass to the extremes.** Take $n = 4$, with the edge parameter $-1$, and sum over the 64 graphs exactly.

| triangle parameter | 0 | 0.5 | 1 | 1.5 | 2 |
|---|---|---|---|---|---|
| expected edges, of 6 | 1.614 | 1.733 | 1.983 | 2.613 | 4.002 |
| expected triangles, of 4 | 0.078 | 0.142 | 0.297 | 0.767 | 1.974 |
| probability of the empty graph | 0.153 | 0.145 | 0.131 | 0.102 | 0.053 |
| probability of $K_4$ | 0.000 | 0.003 | 0.018 | 0.102 | 0.393 |

At the parameter 2, the complete graph alone has probability 0.39 while the empty graph keeps 0.05, so the distribution has two humps far apart and little mass on graphs of middling density. On larger graphs this split becomes sharp: the observed density is between the humps and almost no sampled graph looks like it. This is the degeneracy that Snijders and co-authors describe.

## Relation to other models

- **[Erdős-Rényi model](/erdos-renyi-model/).** The ERGM with the edge count alone, as shown above.
- **[Stochastic block model](/stochastic-block-model/).** With known groups, the edge counts within and between each pair of groups as statistics give exactly the block model. With unknown groups the block model is a mixture of such ERGMs.
- **Markov random fields.** The pair indicators are the variables of a [Markov random field](/markov-random-field/) whose dependence graph has a node for each pair. Frank and Strauss call a graph model *Markov* if two pair indicators are dependent given the rest only when the pairs share a vertex, and prove with the Hammersley-Clifford theorem that the Markov models are exactly the ERGMs whose statistics are the edge count, the $k$-star counts and the triangle count.
- **The Ising model.** The edge-triangle model is a spin system on the $\binom n2$ pairs with a three-body interaction, close to the [Ising model](/ising-model/), and it has a similar phase transition.
- **Configuration and degree models.** Fixing the degree of each vertex by parameters, as in the $p_1$ model, gives the maximum entropy relative of the [configuration model](/configuration-model/).
- **Growth models.** Unlike the [Barabási-Albert model](/barabasi-albert-model/), an ERGM has no time and no mechanism; it only describes which graphs are likely.

## Known results in the model

| question | result |
|---|---|
| edge model | $G(n, p)$ with $p = e^\theta / (1 + e^\theta)$ |
| Markov graphs | the statistics are edges, $k$-stars and triangles (Frank and Strauss, 1986) |
| maximum likelihood | the estimate matches $\mathbb{E}_\theta[s]$ to $s(G_{\mathrm{obs}})$; it does not exist when $s(G_{\mathrm{obs}})$ lies on the boundary of the convex hull of the possible values of $s$ |
| mixing, nonnegative parameters, high temperature | the Glauber dynamics mixes in $\Theta(n^2 \log n)$ steps, and a sample is close to $G(n, p)$ for some $p$ (Bhamidi, Bresler and Sly, 2011) |
| mixing, nonnegative parameters, low temperature | the Glauber dynamics, and any chain that changes few pairs per step, needs a time exponential in $n$ to mix (Bhamidi, Bresler and Sly, 2011) |
| edge-triangle model, dense scaling | with the triangle count divided by $n$ and a nonnegative triangle parameter, the graph is close to $G(n, u^\ast)$ or to a mixture of such graphs, where $u^\ast$ maximizes an explicit function of one variable; on a curve of parameters $u^\ast$ jumps (Chatterjee and Diaconis, 2013) |
| degeneracy | Markov models with star and triangle counts put most of their mass near the empty or complete graph over large parameter regions; geometrically weighted statistics avoid much of this (Snijders, Pattison, Robins and Handcock, 2006) |

The last three rows say the same thing from three sides: the obvious dependence statistics either do almost nothing, because the model stays close to $G(n, p)$, or do too much, because the model jumps between nearly empty and nearly full graphs. This is why fitted models in practice use geometrically weighted statistics and attribute terms, and check the fit by simulating from the estimate and comparing degree, shared partner and distance distributions with the data.

## References
