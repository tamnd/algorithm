---
tag: H16W80
kind: model
slug: potts-model
name: Potts model
area: machine-learning/probabilistic-inference
level: advanced
summary: "A distribution on graph colourings with q states per vertex and weight exp(K) for each edge whose ends agree. With q = 2 it is the Ising model. Exact Z is #P-hard."
prereqs: [markov-random-field, partition-function, ising-model]
see_also: [gibbs-sampling, glauber-dynamics, swendsen-wang, tutte-polynomial, chromatic-polynomial, graph-coloring, image-segmentation, fpras]
sources:
  - paper: doi:10.1017/S0305004100027419
    title: Renfrey B. Potts, Some generalized order-disorder transformations, Mathematical Proceedings of the Cambridge Philosophical Society 48(1), 1952, pages 106 to 109
    locator: the q-state model with interaction energy only between equal neighbouring states
  - paper: doi:10.1103/RevModPhys.54.235
    title: Fa-Yueh Wu, The Potts model, Reviews of Modern Physics 54(1), 1982, pages 235 to 268
    locator: survey of the definition, the critical point of the square lattice, the order of the transition, and the relation to the Tutte polynomial and the random-cluster model
  - paper: doi:10.1137/0222066
    title: Mark Jerrum and Alistair Sinclair, Polynomial-time approximation algorithms for the Ising model, SIAM Journal on Computing 22(5), 1993, pages 1087 to 1116
    locator: exact computation of the Ising partition function is #P-hard; an FPRAS for the ferromagnetic case; no FPRAS for the antiferromagnetic case unless RP = NP
  - paper: "François Jaeger, Dirk L. Vertigan and Dominic J. A. Welsh, On the computational complexity of the Jones and Tutte polynomials, Mathematical Proceedings of the Cambridge Philosophical Society 108(1), 1990, pages 35 to 53"
    title: Jaeger, Vertigan and Welsh 1990
    locator: evaluating the Tutte polynomial is #P-hard at all but a few points of the plane, which covers the Potts partition function for integer q of at least 2
  - paper: doi:10.1103/PhysRevLett.58.86
    title: Robert H. Swendsen and Jian-Sheng Wang, Nonuniversal critical dynamics in Monte Carlo simulations, Physical Review Letters 58(2), 1987, pages 86 to 88
    locator: the cluster algorithm for the Potts model based on the random-cluster representation
  - paper: doi:10.1109/34.969114
    title: Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 2001, pages 1222 to 1239
    locator: the Potts energy in vision, NP-hardness of its minimization for three or more labels, and the alpha-expansion algorithm with a factor 2 guarantee
---

The Potts model is a probability distribution on the ways to give each vertex of a graph one of $q$ states, in which neighbours that share a state get a bonus. Renfrey Potts proposed it in 1952, following a suggestion of Cyril Domb, as a generalization of the [Ising model](/ising-model/), which is the case $q = 2$. In physics it models magnets and alloys with $q$ phases. In machine learning it is the standard pairwise [Markov random field](/markov-random-field/) prior for labelling problems such as [image segmentation](/image-segmentation/). Its normalizing constant, the [partition function](/partition-function/), is #P-hard to compute exactly.

## The machine

**Configurations and weights.** Let $G = (V, E)$ be a graph with $n = |V|$ and $m = |E|$, and let $q \ge 2$. A configuration $x \in \{1, \dots, q\}^V$ gives each vertex a state. The energy is

$$H(x) = -J \sum_{uv \in E} \delta(x_u, x_v),$$

where $\delta(a, b) = 1$ if $a = b$ and $0$ otherwise. At inverse temperature $\beta$ the distribution is

$$\pi(x) = \frac{e^{-\beta H(x)}}{Z} = \frac{e^{K a(x)}}{Z}, \qquad Z = \sum_{x} e^{K a(x)},$$

with the coupling $K = \beta J$ and $a(x)$ the number of edges whose two ends agree. The model is *ferromagnetic* if $K > 0$, so that agreement is favoured, and *antiferromagnetic* if $K < 0$. A field term $\sum_v h_v(x_v)$ can be added to the exponent; in labelling problems it carries the data.

**One vertex given the rest.** The conditional distribution of $x_v$ given all the other states is

$$\pi(x_v = s \mid x_{V \setminus v}) = \frac{e^{K\, c_s}}{\sum_{t=1}^q e^{K\, c_t}},$$

where $c_s$ is the number of neighbours of $v$ in state $s$. It depends only on the neighbours, which form the [Markov blanket](/markov-blanket/) of $v$. A [Gibbs sampler](/gibbs-sampling/) draws from this distribution at one vertex after another.

**A small example.** On a triangle with $q = 3$, the $27$ configurations have $3$ agreeing edges (all equal, 3 ways), $1$ agreeing edge (two equal and one different, 18 ways) or $0$ agreeing edges (all different, 6 ways). Two agreeing edges are impossible. So $Z = 6 + 18 e^K + 3 e^{3K}$; with $e^K = 2$, $Z = 66$.

## What it counts

- **The partition function.** As a polynomial in $w = e^K$, $Z = \sum_k c_k w^k$, where $c_k$ counts the configurations with $k$ agreeing edges. On the $3 \times 3$ grid with $q = 3$ there are $3^9 = 19683$ configurations and $m = 12$ edges, and $c_0, \dots, c_{12} = 246, 840, 2376, 3984, 5148, 3672, 2232, 792, 270, 96, 24, 0, 3$.
- **Colourings.** At $w = 0$, that is $K \to -\infty$, only configurations with no agreeing edge remain, so $Z$ is the number of proper $q$-colourings, the [chromatic polynomial](/chromatic-polynomial/) $P_G(q)$. The $3 \times 3$ grid has $246$ proper $3$-colourings.
- **Expectations.** The mean number of agreeing edges is $\frac{d}{dK} \log Z$. On the $3 \times 3$ grid with $q = 3$ it rises from $4$ at $K = 0$ to about $6.235$ at $K = 0.7$.
- **The random-cluster sum.** Fortuin and Kasteleyn (1972) showed that

$$Z = \sum_{A \subseteq E} q^{k(A)} (e^K - 1)^{|A|},$$

where $k(A)$ is the number of connected components of $(V, A)$, counting isolated vertices. To see it, write $e^{K \delta(x_u, x_v)} = 1 + (e^K - 1)\delta(x_u, x_v)$, expand the product over edges, and note that the states in each component of $A$ must all be equal. The right side makes sense for every real $q > 0$, and it is an evaluation of the [Tutte polynomial](/tutte-polynomial/) of $G$.

## Relation to other models

- **The Ising model.** With $q = 2$ and spins $\sigma_v = \pm 1$, $\delta(x_u, x_v) = (1 + \sigma_u \sigma_v)/2$. So $Z_{\text{Potts}}(K) = e^{K m / 2}\, Z_{\text{Ising}}(\beta = K/2)$, and the two models have the same configurations with the same probabilities.
- **Markov random fields.** The Potts model is the pairwise [Markov random field](/markov-random-field/) with a single parameter per edge that rewards equal labels. Many vision models add a data term per pixel to this prior.
- **Graph colouring.** The antiferromagnet at zero temperature is the uniform distribution on proper colourings, the subject of [graph colouring](/graph-coloring/) and of counting colourings.
- **Random-cluster model.** The sum above defines a distribution on edge subsets. The [Swendsen-Wang](/swendsen-wang/) algorithm alternates between the Potts configuration and a random-cluster configuration.
- **Clock and vector models.** The clock model uses the energy $-J \cos(2\pi (x_u - x_v)/q)$, which rewards near agreement and not only exact agreement. For $q = 2$ and $q = 3$ it is equivalent to the Potts model.

## Known results in the model

**Phase transition on the square lattice.** For the ferromagnet on $\mathbb{Z}^2$, the self-dual point $e^{K_c} = 1 + \sqrt{q}$ is the critical coupling. For $q = 2$ this is Onsager's point. Baxter (1973) computed the free energy at this point and found a continuous transition for $q \le 4$ and a discontinuous one for $q > 4$; rigorous proofs came much later (see Wu 1982 for the physics and the surveys of Duminil-Copin for the proofs).

**Exact computation is hard.**

- Computing $Z$ exactly is #P-hard. For $q = 2$, Jerrum and Sinclair (1993) note that the coefficients of $Z$ count cuts by size. For general integer $q \ge 2$ and $K \ne 0$, the hardness follows from the result of Jaeger, Vertigan and Welsh (1990) on the Tutte polynomial. The case $w = 0$ is counting proper $q$-colourings, which is #P-complete for $q \ge 3$. See [counting problem](/counting-problem/).
- For graphs of bounded [treewidth](/treewidth/), $Z$ can be computed in time linear in $n$ by dynamic programming over a tree decomposition, which is what the [junction tree algorithm](/junction-tree-algorithm/) does.

**Approximate counting.**

- For $q = 2$, Jerrum and Sinclair (1993) gave an [FPRAS](/fpras/) for the ferromagnetic partition function on every graph, and showed that the antiferromagnet has none unless $\mathrm{RP} = \mathrm{NP}$.
- For the ferromagnet with $q \ge 3$, no FPRAS is known, and Goldberg and Jerrum showed that approximating $Z$ is as hard as counting independent sets in bipartite graphs (#BIS), a problem believed to have no FPRAS.

**Sampling.** Single-site [Glauber dynamics](/glauber-dynamics/), which is the Gibbs sampler above, mixes fast at high temperature but slowly near and below the transition on large grids, because the $q$ ordered phases are separated by bottlenecks. The [Swendsen-Wang](/swendsen-wang/) cluster algorithm flips whole clusters at once and is much faster near the critical point in practice.

**Energy minimization.** In vision, the most likely labelling under a Potts prior plus a data term minimizes $\sum_v D_v(x_v) + \lambda \sum_{uv \in E} [x_u \ne x_v]$. For $q = 2$ this is a minimum cut problem. Boykov, Veksler and Zabih (2001) showed that it is NP-hard for $q \ge 3$, and gave the alpha-expansion algorithm, whose local minima are within a factor $2$ of the optimum.

## References
