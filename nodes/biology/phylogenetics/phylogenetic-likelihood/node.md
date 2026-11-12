---
tag: YT44NT
kind: definition
slug: phylogenetic-likelihood
name: Phylogenetic likelihood
aliases:
- likelihood of a tree
- tree likelihood
area: biology/phylogenetics
level: core
summary: The probability of an alignment given a tree, its branch lengths and a substitution model. Sites are independent, and each site sums over all states of the internal nodes.
prereqs: [substitution-model, phylogenetic-tree, maximum-likelihood-estimation]
see_also: [felsenstein-pruning, maximum-likelihood-phylogeny, rate-heterogeneity, ancestral-sequence-reconstruction, bayesian-phylogenetic-inference, hidden-markov-model, variable-elimination, maximum-parsimony]
sources:
  - paper: doi:10.1007/BF01734359
    title: Joseph Felsenstein, Evolutionary trees from DNA sequences, a maximum likelihood approach, Journal of Molecular Evolution 17 (1981)
    locator: pp. 368 to 376 (the likelihood of a tree as a product over sites, the sum over the states of the internal nodes, and the pulley principle)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 4, Section 4.2 (the likelihood of a tree, the pruning algorithm, time reversibility and the root of the tree)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 16, Likelihood methods
  - paper: "Chris Tuffley and Mike Steel, Links between maximum likelihood and maximum parsimony under a simple model of site substitution, Bulletin of Mathematical Biology 59(3), 1997, pages 581 to 607"
    locator: the no common mechanism model, under which maximum likelihood and maximum parsimony choose the same trees
---

The phylogenetic likelihood is the probability of an observed alignment under a model of evolution on a given tree. The model has three parts: a tree topology, a length for each branch, and a [substitution model](/substitution-model/) that turns each branch length into a matrix of change probabilities. Each site is an independent draw from this model, and the bases at the internal nodes are not observed, so the likelihood of a site is a sum over all their possible states. The likelihood is the objective of [maximum likelihood phylogeny](/maximum-likelihood-phylogeny/), the basis of the posterior in [Bayesian phylogenetic inference](/bayesian-phylogenetic-inference/), and it is computed in linear time by [Felsenstein's pruning algorithm](/felsenstein-pruning/).

## Definition

**The data.** An alignment $X$ of $n$ taxa and $m$ sites, with $x_{v s}$ the state of taxon $v$ at site $s$, from an alphabet of $k$ states. The column $x_s = (x_{1s}, \ldots, x_{ns})$ is the *site pattern* of site $s$.

**The model.** A [phylogenetic tree](/phylogenetic-tree/) $T$ whose leaves are the $n$ taxa, a length $t_e \ge 0$ on each edge, and a rate matrix $Q$ with stationary distribution $\pi$, so that edge $e$ has the matrix $P(t_e) = e^{Q t_e}$. Root $T$ at any vertex $\rho$ and direct each edge $e = (u, v)$ away from the root.

**The site likelihood.** Let $V^\circ$ be the internal vertices. A labelling $a$ gives a state $a_v$ to each internal vertex, and the leaves keep their observed states. Then

$$L_s(T, t, Q) = \sum_{a \in [k]^{V^\circ}} \pi_{a_\rho} \prod_{(u, v) \in E(T)} P_{a_u a_v}(t_{uv}),$$

the probability that the process, started from $\pi$ at the root and run independently along each edge, puts the pattern $x_s$ at the leaves.

**The likelihood of the alignment.** Sites are independent and identically distributed, so

$$L(T, t, Q \mid X) = \prod_{s=1}^{m} L_s, \qquad \ell = \ln L = \sum_{s=1}^{m} \ln L_s.$$

As a function of the model it is a likelihood in the sense of [maximum likelihood estimation](/maximum-likelihood-estimation/): it is the probability of the fixed data, read as a function of $T$, $t$ and $Q$.

**Site patterns.** Two sites with the same pattern have the same likelihood. If pattern $y$ occurs $c_y$ times, $\ell = \sum_y c_y \ln L_y$. There are at most $\min(m, k^n)$ distinct patterns, and programs compute each one only once.

**Missing data.** A gap or an unknown base at a leaf is handled as a sum over its states. In the formula this is the same as treating the leaf as an internal vertex with no further children, and in pruning it is a leaf vector of all ones.

**The pulley principle.** Suppose $Q$ is reversible with respect to $\pi$, and the root is drawn from $\pi$. Then $L_s$ does not depend on the choice of the root vertex, nor on where on an edge the root is placed. The key step: if the root $w$ sits on an edge between $u$ and $v$ at distances $s'$ and $t - s'$, it contributes

$$\sum_w \pi_w P_{wu}(s') P_{wv}(t - s') = \sum_w \pi_u P_{uw}(s') P_{wv}(t - s') = \pi_u P_{uv}(t),$$

using detailed balance $\pi_w P_{wu}(s') = \pi_u P_{uw}(s')$ and then the Chapman-Kolmogorov equation. The result is the same for each $s'$ and equals the formula with the root at $u$. So under a reversible model only the unrooted tree and its branch lengths are identifiable, and the likelihood is a function of the unrooted tree. Felsenstein named this fact the pulley principle: the root can slide along the tree like a rope on a pulley.

**Extensions.** With [rate heterogeneity](/rate-heterogeneity/), $L_s$ becomes a mixture $\sum_k w_k L_s(r_k)$ over rate classes. Under a [molecular clock](/molecular-clock/) the branch lengths come from node heights, and the root is part of the model.

## Examples and non-examples

**Two taxa.** For a tree with one edge of length $t$ between taxa $x$ and $y$, the site likelihood is $L_s = \pi_{x_s} P_{x_s y_s}(t)$. Under [JC69](/jukes-cantor-model/), a pair of sequences with $h$ differences among $m$ sites has

$$\ell(t) = m \ln \tfrac14 + (m - h) \ln\left(\tfrac14 + \tfrac34 e^{-4t/3}\right) + h \ln\left(\tfrac14 - \tfrac14 e^{-4t/3}\right),$$

and its maximum is at the JC69 distance $t = -\tfrac34 \ln(1 - \tfrac43 h/m)$.

**Four taxa, one site.** Take the rooted tree $((1{:}0.1, 2{:}0.2)u{:}0.1, (3{:}0.1, 4{:}0.3)w{:}0.2)r$ under JC69, where each number is the branch length above a node, and the site pattern A, C, A, A at leaves 1 to 4. The sum over the $4^3 = 64$ states of $u$, $w$ and $r$ gives

$$L_s = 0.00724868.$$

The [pruning](/felsenstein-pruning/) page computes this value step by step. Moving the root to $u$, so that the edge from $u$ to $w$ has length $0.1 + 0.2 = 0.3$, gives the same value, as the pulley principle says.

**An exact check.** Write $x_e = e^{-4t_e/3}$. Under JC69 each entry of $P(t_e)$ is linear in $x_e$, so for rational $x_e$ the likelihood is a rational number. The pulley principle then becomes an identity of rational numbers: splitting a root edge with $x = 3/5$ into parts with $x = 1$ and $x = 3/5$, $x = 3/4$ and $x = 4/5$, or $x = 3/5$ and $x = 1$ gives exactly the same likelihood. The tests of the pruning code check this with fractions.

**Non-example: the maximum over internal states.** The quantity $\max_a \pi_{a_\rho} \prod_{(u,v)} P_{a_u a_v}(t_{uv})$ is the probability of the best single history, not of the data. It is the objective of joint [ancestral sequence reconstruction](/ancestral-sequence-reconstruction/), and the trees that maximize it can differ from the maximum likelihood trees.

**Non-example: no common mechanism.** If every site gets its own branch lengths, the model has more parameters than data. Tuffley and Steel showed that maximizing this likelihood over trees picks the same trees as [maximum parsimony](/maximum-parsimony/). So parsimony is a maximum likelihood method, but for a model very different from the one defined here, where all sites share the branch lengths.

**Non-example: a non-reversible model.** Under a rate matrix that is not reversible, the formula still defines a likelihood, but the value changes when the root moves. Then the root is a parameter, and the tree is rooted.

## Related definitions

- [Felsenstein's pruning algorithm](/felsenstein-pruning/) evaluates $L_s$ in $O(n k^2)$ time instead of the $k^{n-1}$ terms of the sum, by pushing the sums inside the products. This is [variable elimination](/variable-elimination/) on a tree-shaped graphical model.
- A [hidden Markov model](/hidden-markov-model/) is the same kind of model on a path instead of a tree: hidden states linked by transition matrices, observed symbols at some nodes. Its forward algorithm is the special case of pruning on a caterpillar-shaped tree.
- [Maximum likelihood phylogeny](/maximum-likelihood-phylogeny/) maximizes $\ell$ over $T$, $t$ and $Q$. Finding the best $T$ is NP-hard ([ML tree is NP-hard](/ml-tree-np-hard/)).
- [Bayesian phylogenetic inference](/bayesian-phylogenetic-inference/) multiplies $L$ by a prior and samples from the posterior.
- [Ancestral sequence reconstruction](/ancestral-sequence-reconstruction/) uses the terms of the sum to score states at internal nodes.

## References
