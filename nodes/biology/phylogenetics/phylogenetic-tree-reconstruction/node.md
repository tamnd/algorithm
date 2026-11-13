---
tag: 3XP9QQ
kind: problem
slug: phylogenetic-tree-reconstruction
name: Phylogenetic tree reconstruction
aliases:
- phylogeny inference
- phylogenetic inference
area: biology/phylogenetics
level: intro
summary: Infer the evolutionary tree that relates a set of taxa from their sequences, characters or distances. Most optimality criteria make it NP-hard.
prereqs: [phylogenetic-tree]
see_also: [neighbor-joining, maximum-parsimony, maximum-likelihood-phylogeny, bayesian-phylogenetic-inference, additive-tree-reconstruction, species-tree-estimation, long-branch-attraction, phylogenetic-bootstrap]
sources:
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 3, How many trees are there; Chapter 11, Distance matrix methods; Chapters 1 and 16, parsimony and likelihood methods
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, 2003
    locator: Chapters 2 and 7, the counts of phylogenetic trees and tree metrics
  - paper: doi:10.1016/S0196-8858(82)80004-3
    title: L. R. Foulds and R. L. Graham, The Steiner problem in phylogeny is NP-complete, Advances in Applied Mathematics 3(1), 1982, pages 43 to 49
    locator: NP-completeness of maximum parsimony
  - paper: doi:10.1145/1183907.1183909
    title: Benny Chor and Tamir Tuller, Finding a maximum likelihood tree is hard, Journal of the ACM 53(5), 2006, pages 722 to 744
    locator: NP-hardness of the maximum likelihood tree (conference version at RECOMB 2005)
  - paper: doi:10.1109/TCBB.2006.4
    title: Sebastien Roch, A short proof that phylogenetic tree reconstruction by maximum likelihood is hard, IEEE/ACM Transactions on Computational Biology and Bioinformatics 3(1), 2006
    locator: NP-hardness of the maximum likelihood tree
  - paper: doi:10.1007/BF02458863
    title: William H. E. Day, Computational complexity of inferring phylogenies from dissimilarity matrices, Bulletin of Mathematical Biology 49(4), 1987, pages 461 to 467
    locator: NP-hardness of least squares fits by a tree metric
  - paper: "Samuel Fiorini and Gwenaël Joret, Approximating the balanced minimum evolution problem, Operations Research Letters 40(1), 2012, pages 31 to 35"
    title: Fiorini and Joret 2012
    locator: NP-hardness of balanced minimum evolution
  - paper: "Joseph Felsenstein, Cases in which parsimony or compatibility methods will be positively misleading, Systematic Zoology 27(4), 1978, pages 401 to 410"
    title: Felsenstein 1978
    locator: the four-taxon example where parsimony is inconsistent
  - book: isbn:9781107184718
    title: Tandy Warnow, Computational Phylogenetics, Cambridge University Press, 2017
    locator: the chapters on distance-based, parsimony and likelihood tree estimation
---

Phylogenetic tree reconstruction is the problem of inferring, from data on a set of taxa, the [phylogenetic tree](/phylogenetic-tree/) that describes how they descend from common ancestors. The data are usually aligned DNA or protein sequences, sometimes other characters or a matrix of distances. Methods choose a tree by a criterion such as fit to distances, the fewest changes, or likelihood under a model of evolution, and for most of these criteria the best tree is NP-hard to find.

## In plain words

You have DNA from several species and want to know who is most closely related to whom, drawn as a branching tree. Species that changed little from a shared ancestor should sit close together in the tree. There are many ways to score a tree: how well it explains the measured differences, how few changes it needs, or how probable the data are if evolution ran along it. The number of possible trees grows very quickly with the number of species, so for large groups no method can check them all. Programs build a good tree fast and then improve it by small changes.

## Definition

**Input.** A set $X$ of $n$ taxa and data for each taxon. The common forms are an alignment, which gives each taxon a string of length $m$ over an alphabet such as $\{A, C, G, T\}$ with the same positions in all strings, or a symmetric matrix $D$ of distances.

**Output.** A phylogenetic tree with leaf set $X$: usually an unrooted binary tree, often with a length on each edge. A rooted tree is obtained afterwards by [tree rooting](/tree-rooting/), or directly when a [molecular clock](/molecular-clock/) is assumed.

**Criterion.** The problem becomes precise only with a criterion $f(T)$ to optimize over all trees $T$ with leaf set $X$:

- **Distance fit.** Minimize $\lVert D - d_T \rVert$, where $d_T$ is the [tree metric](/tree-metric/) of $T$ with fitted edge lengths ([least squares phylogeny](/least-squares-phylogeny/)), or minimize the total fitted length ([minimum evolution](/minimum-evolution/)).
- **Parsimony.** Minimize the number of state changes along the edges needed to explain the alignment ([maximum parsimony](/maximum-parsimony/)).
- **Likelihood.** Maximize the probability of the alignment under a [substitution model](/substitution-model/) on $T$, over edge lengths and model parameters ([maximum likelihood phylogeny](/maximum-likelihood-phylogeny/)).
- **Posterior.** Compute the posterior distribution of trees given the data and a prior ([Bayesian phylogenetic inference](/bayesian-phylogenetic-inference/)).

A method is **statistically consistent** under a model if the probability that it returns the true topology tends to 1 as $m$ grows.

## Variants

- **Distance-based.** The input is $D$, and the exact version is [additive tree reconstruction](/additive-tree-reconstruction/); with a clock it is [ultrametric tree reconstruction](/ultrametric-tree-reconstruction/).
- **Quartet-based.** Infer a tree on each set of four taxa and combine them; see [quartet](/quartet/), [quartet max cut](/quartet-max-cut/) and [maximum quartet consistency](/maximum-quartet-consistency/).
- **Species trees.** Gene trees from many loci disagree because of [incomplete lineage sorting](/incomplete-lineage-sorting/); [species tree estimation](/species-tree-estimation/) under the [multispecies coalescent](/multispecies-coalescent/) combines them, for example with [ASTRAL](/astral/).
- **Combining trees.** [Supertree](/supertree/) methods join trees on overlapping taxon sets; [consensus trees](/consensus-tree/) summarize trees on the same taxa.
- **Networks.** When hybridization or horizontal transfer occurs, the target is a [phylogenetic network](/phylogenetic-network/) instead of a tree.
- **Perfect phylogeny.** Decide whether a tree exists in which each state of each character forms a connected part; see [perfect phylogeny](/perfect-phylogeny/).

## Examples

**Counting trees.** With $n \ge 3$ taxa there are $(2n-5)!! = 1 \cdot 3 \cdot 5 \cdots (2n-5)$ unrooted binary trees and $(2n-3)!!$ rooted binary trees, because the $k$-th taxon can be added on any of the $2k-5$ edges of an unrooted binary tree on $k-1$ taxa.

| $n$ | unrooted | rooted |
|---|---|---|
| 4 | 3 | 15 |
| 5 | 15 | 105 |
| 6 | 105 | 945 |
| 10 | 2,027,025 | 34,459,425 |
| 20 | about $2.2 \times 10^{20}$ | about $8.2 \times 10^{21}$ |
| 50 | about $2.8 \times 10^{74}$ | |

**Four taxa, two criteria.** Take the alignment

| taxon | site 1 | site 2 | site 3 | site 4 | site 5 |
|---|---|---|---|---|---|
| A | A | C | G | T | A |
| B | A | C | T | C | A |
| C | G | T | G | C | A |
| D | G | T | T | C | A |

The three unrooted trees are AB|CD, AC|BD and AD|BC. Parsimony with the [Fitch algorithm](/fitch-algorithm/) gives 5, 6 and 7 changes, so it picks AB|CD: sites 1 and 2 support it, site 3 supports AC|BD, site 4 changes once on every tree and site 5 never changes. The proportions of differing sites are $D_{AB} = 2/5$, $D_{AC} = 3/5$, $D_{AD} = 4/5$, $D_{BC} = 3/5$, $D_{BD} = 2/5$ and $D_{CD} = 1/5$. The three pair sums are $D_{AB} + D_{CD} = 3/5$, $D_{AC} + D_{BD} = 1$ and $D_{AD} + D_{BC} = 7/5$, and the [four-point method](/four-point-method/) picks the split with the smallest sum, AB|CD again.

**Five taxa from distances.** The tree metric of `((A:2,B:7):1,E:5,(C:3,D:6):2);` is the input example on the page of [neighbor-joining](/neighbor-joining/), which returns this tree out of the 15 unrooted trees on five taxa. [UPGMA](/upgma/) fails on the same matrix because the edge lengths do not follow a clock.

## Known algorithms

| method | criterion or model | time | notes |
|---|---|---|---|
| [Neighbor-joining](/neighbor-joining/) | distances | $O(n^3)$ | exact on tree metrics, greedy for balanced minimum evolution |
| [BIONJ](/bionj/) | distances | $O(n^3)$ | NJ with variance-based reduction |
| [UPGMA](/upgma/) | distances with a clock | $O(n^3)$ | exact on ultrametrics |
| [Fitch-Margoliash](/fitch-margoliash/) | weighted least squares | heuristic search | fits lengths on each candidate tree |
| [Four-point method](/four-point-method/) | tree metric | $O(n^2)$ | exact reconstruction from additive distances |
| [Maximum parsimony](/maximum-parsimony/) | fewest changes | NP-hard; one tree in $O(nm)$ by the [Fitch algorithm](/fitch-algorithm/) | search with [branch and bound](/depth-first-branch-and-bound/) or local moves |
| [Maximum likelihood](/maximum-likelihood-phylogeny/) | substitution model | NP-hard; one tree in $O(nm s^2)$ by [Felsenstein pruning](/felsenstein-pruning/) for $s$ states | search with local moves |
| [Bayesian inference](/bayesian-phylogenetic-inference/) | model and prior | [Markov chain Monte Carlo](/metropolis-hastings/) | samples trees from the posterior |
| [Stepwise addition](/stepwise-addition/) | any score | $n$ insertions, each over all edges | builds a starting tree |
| [NNI](/nearest-neighbor-interchange/), [SPR](/subtree-prune-and-regraft/), [TBR](/tree-bisection-and-reconnection/) | any score | per move, $O(n)$, $O(n^2)$ and $O(n^3)$ neighbors | improve a tree by local search |

Support for the edges of the result is usually measured with the [phylogenetic bootstrap](/phylogenetic-bootstrap/).

## Bounds

- **Search space.** $(2n-5)!!$ unrooted binary trees, so exhaustive search is practical only up to about 10 to 12 taxa.
- **Maximum parsimony** is NP-complete in its decision form (Foulds and Graham 1982); see [maximum parsimony is NP-hard](/maximum-parsimony-np-hard/).
- **Maximum likelihood** is NP-hard (Chor and Tuller 2005, with a short proof by Roch 2006); see [ML tree NP-hardness](/ml-tree-np-hard/).
- **Least squares** fits by a tree metric are NP-hard in $L_1$ and $L_2$ (Day 1987).
- **Balanced minimum evolution** is NP-hard (Fiorini and Joret 2012).
- **Exact data.** When the distances form a tree metric, the tree is unique and found in $O(n^2)$ time.

## Reductions

- **Sequences to distances.** Count the differing sites of each pair and correct the counts with a substitution model, for example $d = -\frac{3}{4}\ln(1 - \frac{4}{3}p)$ in the [Jukes-Cantor model](/jukes-cantor-model/); then apply a distance method. The corrected distances converge to a tree metric of the true tree as $m$ grows, so a method that is exact on tree metrics and stable under small errors, such as neighbor-joining, is consistent.
- **Parsimony to Steiner trees.** Maximum parsimony with $m$ binary characters is the Steiner tree problem in the hypercube $\{0, 1\}^m$ with Hamming distance; Foulds and Graham use this form for their hardness proof.
- **Reconstruction to quartets.** A binary tree is determined by its set of induced quartet topologies, so reconstruction reduces to inferring quartets and finding a tree that agrees with the most of them.

## Applications

- **Systematics.** Classification of organisms by descent, the tree of life and the dating of divergences with a clock.
- **Epidemiology.** Tracing the spread of viruses such as HIV and influenza from their sequences.
- **Comparative biology.** Methods that compare traits across species correct for shared ancestry using the tree.
- **Sequence analysis.** [Progressive alignment](/progressive-alignment/) uses a guide tree to align many sequences.
- **Pitfall: long branch attraction.** Parsimony and some distance methods can join two long edges that are not sisters, and with more data they become more sure of the wrong tree (Felsenstein 1978); see [long branch attraction](/long-branch-attraction/).

## References
