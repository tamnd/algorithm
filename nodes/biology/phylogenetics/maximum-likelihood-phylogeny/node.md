---
tag: FWRY3J
kind: problem
slug: maximum-likelihood-phylogeny
name: Maximum likelihood phylogeny
aliases:
- ML tree inference
- maximum likelihood tree
area: biology/phylogenetics
level: core
summary: Find the unrooted tree, branch lengths and model parameters that maximize the likelihood of an alignment under a substitution model. NP-hard, solved in practice by hill-climbing.
prereqs: [phylogenetic-likelihood, felsenstein-pruning]
see_also: [ml-tree-np-hard, maximum-parsimony, nearest-neighbor-interchange, subtree-prune-and-regraft, stepwise-addition, phylogenetic-bootstrap, bayesian-phylogenetic-inference, neighbor-joining]
sources:
  - paper: doi:10.1007/BF01734359
    title: Joseph Felsenstein, Evolutionary trees from DNA sequences, a maximum likelihood approach, Journal of Molecular Evolution 17 (1981)
    locator: pp. 368 to 376 (the likelihood of a tree for DNA sequences, the tree search by stepwise addition and local rearrangements)
  - paper: doi:10.1080/10635150390235520
    title: Stéphane Guindon and Olivier Gascuel, A simple, fast, and accurate algorithm to estimate large phylogenies by maximum likelihood, Systematic Biology 52(5) (2003)
    locator: pp. 696 to 704 (PhyML, hill-climbing that changes the topology and the branch lengths together, from a distance tree)
  - paper: doi:10.1093/bioinformatics/btl446
    title: Alexandros Stamatakis, RAxML-VI-HPC, maximum likelihood-based phylogenetic analyses with thousands of taxa and mixed models, Bioinformatics 22(21) (2006)
    locator: pp. 2688 to 2690 (lazy subtree rearrangements and the parallel search)
  - paper: doi:10.1093/molbev/msu300
    title: Lam-Tung Nguyen, Heiko A. Schmidt, Arndt von Haeseler and Bui Quang Minh, IQ-TREE, a fast and effective stochastic algorithm for estimating maximum-likelihood phylogenies, Molecular Biology and Evolution 32(1) (2015)
    locator: pp. 268 to 274 (hill-climbing with nearest neighbor interchanges, random perturbation of the trees, and a set of candidate trees)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 4, Maximum likelihood methods (Section 4.5 on the numerical optimization of branch lengths and parameters, and the sections on tree search and the properties of the method)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 16, Likelihood methods
---

Maximum likelihood phylogeny is the problem of finding the tree that makes an alignment most probable. Each candidate is a [phylogenetic tree](/phylogenetic-tree/) with a length on each branch, together with the parameters of a [substitution model](/substitution-model/), and its score is the [phylogenetic likelihood](/phylogenetic-likelihood/) of the data. For a fixed tree, the score takes linear time by [Felsenstein's pruning algorithm](/felsenstein-pruning/), and the branch lengths are found by numerical optimization. The hard part is the choice of the tree: there are $(2n - 5)!!$ unrooted binary trees on $n$ taxa, and the problem is [NP-hard](/ml-tree-np-hard/). Programs such as PhyML, RAxML and IQ-TREE solve it by local search with tree rearrangements. Maximum likelihood is the most used method of tree inference from sequences, together with [Bayesian inference](/bayesian-phylogenetic-inference/).

## In plain words

You have a gene from each of some species, lined up letter by letter, and a model of how letters change over time. Each possible family tree, with a length on each branch, gives a chance of seeing exactly these genes. Maximum likelihood picks the tree and the lengths that make the data most likely.

For one tree, finding the best branch lengths is a smooth search, like turning several knobs until a meter reads its highest. The hard part is that the number of trees grows faster than exponentially with the number of species, so no one can try them all. Programs start from a quick guess, try small changes to the tree, keep any change that raises the score, and stop when no small change helps.

## Definition

**Input.** An alignment $X$ of $n \ge 3$ taxa and $m$ sites over an alphabet of $k$ states, and a family of substitution models with parameters $\theta$, for example [GTR](/gtr-model/) with gamma [rate heterogeneity](/rate-heterogeneity/).

**Output.** An unrooted binary tree $T$ with leaves labelled by the taxa, branch lengths $t \in [0, \infty)^{E(T)}$ and parameters $\theta$ that maximize

$$\ell(T, t, \theta) = \sum_{s=1}^{m} \ln L_s(T, t, \theta),$$

where $L_s$ is the [likelihood](/phylogenetic-likelihood/) of site $s$. For a reversible model the likelihood does not depend on the root, so the answer is an unrooted tree.

**Decision version.** Given $X$, a model and a number $B$, is there a tree $T$ and lengths $t$ with $\ell(T, t) \ge B$? The [hardness proofs](/ml-tree-np-hard/) use this form, with the model fixed and only the topology and branch lengths free.

**Two levels.** The problem nests two optimizations. The inner one, for a fixed $T$, is $\ell^*(T) = \max_{t, \theta} \ell(T, t, \theta)$, a continuous problem in $2n - 3$ branch lengths and a few model parameters. The outer one is $\max_T \ell^*(T)$ over the discrete set of topologies. The optimum may have zero-length branches, which then collapse into a tree with a node of higher degree.

## Variants

- **Fixed topology.** Only branch lengths and model parameters are fitted. This is the inner problem; it is used to compare given trees and to fit models.
- **Molecular clock.** The tree is rooted and every leaf is at the same distance from the root ([molecular clock](/molecular-clock/)). The free parameters are the $n - 1$ node heights. This variant is also NP-hard.
- **Ancestral maximum likelihood.** Maximize the probability of the data and of the internal states together, over trees, branch lengths and internal states. Addario-Berry, Chor, Hallett, Lagergren, Panconesi and Wareham showed in 2004 that this is NP-hard too.
- **No common mechanism.** Each site has its own branch lengths. Tuffley and Steel proved that the maximum likelihood trees under this model are the [maximum parsimony](/maximum-parsimony/) trees.
- **Partitioned and mixture models.** Different genes or codon positions get their own models, branch length scalings or rate classes, and the likelihood multiplies over the parts.
- **Model selection.** Choosing among the nested models JC69, K80, HKY85, GTR and their +I and +G forms by likelihood ratio tests or information criteria, before or during the tree search.

## Examples

**Four taxa, fourteen sites.** Under [JC69](/jukes-cantor-model/), take

| taxon | sequence |
|---|---|
| 1 | ACGTACGTAAGTCA |
| 2 | ACGTACGTACGTCA |
| 3 | ACGAACGTTCGACA |
| 4 | ACGAACCTTCGATA |

The pairs differ at 1 (taxa 1 and 2), 4 (1, 3), 6 (1, 4), 3 (2, 3), 5 (2, 4) and 2 (3, 4) sites. There are three unrooted topologies. For each one, coordinate ascent on the five branch lengths, from several random starts, gives the best values

| topology | $\ell^*(T)$ | branch lengths at the optimum |
|---|---|---|
| 12\|34 | $-42.6180$ | $t_1 = 0.0751$, $t_2 = 0$, internal $0.2524$, $t_3 = 0$, $t_4 = 0.1585$ |
| 13\|24 | $-49.2968$ | internal $0$: the star tree |
| 14\|23 | $-49.2968$ | internal $0$: the star tree |

So the maximum likelihood tree is 12|34. For both other topologies the best internal branch has length 0, and the optimum is the star tree with $t_1 = 0.0751$, $t_2 = 0$, $t_3 = 0.2524$, $t_4 = 0.4850$. Some of the best branch lengths are on the boundary: in 12|34, the lengths $t_2$ and $t_3$ are 0, and $t_1 = 0.0751$ is the JC69 distance for 1 difference in 14 sites. A first run of the coordinate ascent on 13|24 stopped at $-50.6872$, at a point that is not the maximum, which shows that the inner problem can have local optima.

**Two taxa.** With one branch, the maximum likelihood branch length under JC69 is the JC69 distance $-\tfrac34 \ln(1 - \tfrac43 \hat p)$, or infinity when $\hat p \ge 3/4$.

**Felsenstein zone.** For four taxa with two long branches that are not neighbors, [maximum parsimony](/maximum-parsimony/) prefers the wrong tree as the data grow ([long branch attraction](/long-branch-attraction/)). Maximum likelihood under the true model is consistent on the same trees and picks the right tree when the alignment is long enough.

## Known algorithms

- **Exhaustive search.** Score all $(2n - 5)!!$ topologies, with branch length optimization for each. There are 15 trees for 5 taxa, 10395 for 8 and about $2 \times 10^{20}$ for 20, so this works only for very small $n$.
- **Branch lengths for a fixed tree.** Optimize one branch at a time by [Newton-Raphson](/newton-raphson-method/) steps, using the first and second derivatives from the upward and downward pruning vectors, or by a [golden section](/golden-section-search/) or Brent search. Repeat sweeps over the branches until the gain is small. [EM](/expectation-maximization/) updates are an alternative. Each sweep costs $O(m n k^2)$.
- **Stepwise addition and rearrangement.** Felsenstein's 1981 program adds the taxa one at a time at the best position ([stepwise addition](/stepwise-addition/)), then tries local rearrangements of the tree.
- **PhyML (Guindon and Gascuel, 2003).** Starts from a [BIONJ](/bionj/) distance tree and runs a hill-climbing that changes the topology by [nearest neighbor interchanges](/nearest-neighbor-interchange/) and the branch lengths at the same time, applying many improving moves in each round. It made maximum likelihood practical for hundreds of taxa.
- **RAxML (Stamatakis, 2006).** Uses lazy [subtree prune and regraft](/subtree-prune-and-regraft/) moves, which score each regrafting with only the branch lengths near the new position optimized, and a fast parallel implementation for thousands of taxa.
- **IQ-TREE (Nguyen, Schmidt, von Haeseler and Minh, 2015).** Keeps a set of good candidate trees, perturbs them at random, and improves each with NNI hill-climbing, which helps it leave local optima.
- **Branch and bound.** Exact bounds on the likelihood of partial trees are weak, so branch and bound solves only small instances.

## Bounds

- **NP-hard.** Chor and Tuller proved in 2005 that the decision version is NP-hard under the Jukes-Cantor model and its generalizations, and that approximating the maximum log-likelihood within a small constant factor is also NP-hard. Roch gave a short proof for the two-state model in 2006. See [ML tree is NP-hard](/ml-tree-np-hard/).
- **The inner problem.** For a fixed topology, $\ell$ is a smooth but not concave function of the branch lengths, and it can have more than one local maximum. No polynomial algorithm with a guarantee of the global maximum is known in general.
- **Statistical consistency.** Under the model that generated the data, with all branch lengths positive, the probability that maximum likelihood returns the true topology tends to 1 as $m \to \infty$. This follows from the identifiability of the tree from the site pattern distribution.
- **Sequence length.** The number of sites needed to recover the tree with high probability grows with the depth of the tree and with how short the shortest internal branch is.

## Reductions

- **From vertex cover through parsimony.** Roch's proof reduces [vertex cover](/vertex-cover/) on bounded-degree graphs to [maximum parsimony](/maximum-parsimony/), and then parsimony to maximum likelihood, by adding many all-zero characters that force every branch to be short. Then the log-likelihood is close to a fixed multiple of the parsimony score ([the theorem](/ml-tree-np-hard/)). The proof of Chor and Tuller also starts from the hardness of vertex cover, through longer constructions.
- **To parsimony, under no common mechanism.** By the result of Tuffley and Steel, the maximum likelihood trees with a separate set of branch lengths per site are the maximum parsimony trees.
- **Distance methods as a first step.** [Neighbor joining](/neighbor-joining/) on model-corrected distances gives a starting tree in $O(n^3)$ time, and it is consistent under the same models.

## Applications

- **Tree inference** from genes and genomes, the standard method in molecular systematics, often followed by the [phylogenetic bootstrap](/phylogenetic-bootstrap/) for branch support.
- **Hypothesis tests** that compare fixed topologies, rates or clocks by likelihood ratio.
- **Model fitting** for the parameters of substitution and rate models, which are then used in [ancestral sequence reconstruction](/ancestral-sequence-reconstruction/), dating and [phylogenetic placement](/phylogenetic-placement/).
- **Large trees** of thousands of taxa in phylogenomics and epidemiology, with RAxML, IQ-TREE and similar programs.

## References
