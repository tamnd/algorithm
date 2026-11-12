---
tag: W7JB3Z
kind: problem
slug: phylogenetic-network-inference
name: Phylogenetic network inference
aliases:
- hybridization network inference
area: biology/phylogenetics
level: research
summary: Find a rooted network that explains given gene trees or sequences with the fewest reticulations. NP-hard even for two trees, but FPT in the number of reticulations.
prereqs: [phylogenetic-network, maximum-agreement-forest, np-hard]
see_also: [rspr-maf-equivalence, subtree-prune-and-regraft, fixed-parameter-tractable, incomplete-lineage-sorting, horizontal-gene-transfer, ancestral-recombination-graph, perfect-phylogeny, species-tree-estimation]
sources:
  - paper: doi:10.1007/s00285-005-0315-9
    title: Mihaela Baroni, Stefan Grunewald, Vincent Moulton and Charles Semple, Bounding the number of hybridisation events for a consistent evolutionary history, Journal of Mathematical Biology 51(2), 2005, pages 171 to 182
    locator: acyclic agreement forests, and the theorem that the hybridization number of two rooted binary trees is the size of a maximum acyclic agreement forest minus one
  - paper: doi:10.1016/j.dam.2006.08.008
    title: Magnus Bordewich and Charles Semple, Computing the minimum number of hybridization events for a consistent evolutionary history, Discrete Applied Mathematics 155(8), 2007, pages 914 to 928
    locator: NP-hardness of the hybridization number of two rooted binary trees
  - paper: doi:10.1109/tcbb.2007.1019
    title: Magnus Bordewich and Charles Semple, Computing the hybridization number of two phylogenetic trees is fixed-parameter tractable, IEEE/ACM Transactions on Computational Biology and Bioinformatics 4(3), 2007, pages 458 to 466
    locator: a kernel by subtree and chain reductions, which gives an FPT algorithm in the hybridization number
  - paper: doi:10.1371/journal.pgen.1005896
    title: Claudia Solis-Lemus and Cecile Ane, Inferring phylogenetic networks with maximum pseudolikelihood under incomplete lineage sorting, PLOS Genetics 12(3), 2016
    locator: SNaQ, the network model with incomplete lineage sorting, and the pseudolikelihood from quartet concordance factors
  - book: isbn:9780521755962
    title: Daniel H. Huson, Regula Rupp and Celine Scornavacca, Phylogenetic Networks, Concepts, Algorithms and Applications, Cambridge University Press, 2010
    locator: the chapters on networks from trees and from clusters, with hybridization networks and their computation
---

Phylogenetic network inference asks for a rooted [phylogenetic network](/phylogenetic-network/) that explains a set of trees or sequences with as few reticulation events as possible. In the combinatorial version, the input is a set of rooted gene trees on the same taxa, and the network must display every one of them. The smallest possible reticulation number is the *hybridization number* $h$. For two rooted binary trees, Baroni, Grunewald, Moulton and Semple (2005) showed that $h$ equals the size of a maximum *acyclic* [agreement forest](/maximum-agreement-forest/) minus one. Computing it is NP-hard (Bordewich and Semple 2007), and it is fixed-parameter tractable in $h$. Statistical versions add a model of gene tree variation, such as [incomplete lineage sorting](/incomplete-lineage-sorting/), and search for the network of best likelihood or pseudolikelihood.

## In plain words

Different genes of the same species can have different trees. One cause is hybridization: a hybrid species gets some genes from one parent and some from the other. A network with a hybrid vertex can show both histories at once, since each gene picks one parent at each hybrid.

Given the gene trees, you want the simplest network that contains them all, with the fewest hybrid vertices. For two trees, this is the same as cutting both trees into the fewest pieces on which they agree, with one extra rule: the pieces must not form a loop of "above" relations. Each cut beyond the first piece costs one hybrid. Finding the fewest pieces is hard in general, but it is fast when the answer is small.

## Definition

**Input.** A finite set $X$ of taxa and rooted binary [phylogenetic trees](/phylogenetic-tree/) $T_1, \ldots, T_k$ on $X$.

**Output.** A rooted phylogenetic network $N$ on $X$ that displays every $T_i$, in the sense that some switching of $N$ (one parent arc kept at each reticulation) gives $T_i$, and that minimizes the reticulation number
$$h(N) = \sum_{v \ne \rho} (\mathrm{indeg}(v) - 1).$$
The minimum is the *hybridization number* $h(T_1, \ldots, T_k)$.

**Acyclic agreement forests.** Add a new leaf $\rho$ above the root of both trees. An agreement forest of $T_1$ and $T_2$ is a partition of $X \cup \{\rho\}$ into blocks $L_0 \ni \rho, L_1, \ldots, L_m$ such that each block induces the same tree in $T_1$ and in $T_2$, and the subtrees that the blocks span are vertex disjoint in $T_1$ and in $T_2$. It is *acyclic* if the graph on the blocks with an arc $L_i \to L_j$, whenever the root of the subtree of $L_i$ is an ancestor of the root of the subtree of $L_j$ in $T_1$ or in $T_2$, has no directed cycle. Then
$$h(T_1, T_2) = m_a(T_1, T_2) - 1,$$
where $m_a$ is the smallest number of blocks of an acyclic agreement forest. Without the acyclic rule, the smallest number of blocks minus one is the rooted [SPR distance](/rspr-maf-equivalence/), so $h \ge d_{\mathrm{rSPR}}$.

## Variants

- **Two trees or many trees.** For two trees, the forest characterization holds. For three or more trees, the forest view does not carry over directly, and exact methods search over networks or over sequences of trees.
- **Nonbinary trees.** Gene trees with polytomies are displayed if some refinement of them is displayed. The forest view extends with some changes.
- **Restricted classes.** The network can be required to be tree-child, time-consistent or level-1, which changes the optimum and often the complexity. Galled trees, which are level-1 networks, can be found in polynomial time from sequences in some models.
- **From sequences.** With recombination, each site has a tree, and the goal is the fewest recombinations that explain the sites. This is minimum recombination, and the network is an [ancestral recombination graph](/ancestral-recombination-graph/). Without any recombination, the sites must fit a [perfect phylogeny](/perfect-phylogeny/).
- **Clusters instead of trees.** The input is a set of clusters, and the network must represent each cluster as a softwired or hardwired cluster. This is the version solved by cluster network methods in Dendroscope.
- **Statistical inference.** Gene trees differ also because of incomplete lineage sorting. Models such as the network multispecies coalescent compute the probability of each gene tree under a network. SNaQ (Solis-Lemus and Ane 2016) maximizes a pseudolikelihood built from the frequencies of quartets, and other methods use full likelihood or Bayesian sampling.
- **Transfer networks.** For [horizontal gene transfer](/horizontal-gene-transfer/), the network is a species tree plus transfer arcs between branches of the same time, and the problem is to reconcile gene trees with it.

## Examples

**One hybrid.** Let $T_1$ = `((a,b),c);` and $T_2$ = `(a,(b,c));`. The trees differ, so $h \ge 1$. The forest $\{\rho, a, c\}, \{b\}$ is an acyclic agreement forest with two blocks: both trees restricted to $a, c, \rho$ give $((a, c), \rho)$, and a single leaf spans only itself. So $h = 2 - 1 = 1$. The network is the one of the [phylogenetic network](/phylogenetic-network/) page: $b$ is a reticulation with one parent on the lineage of $a$ and one on the lineage of $c$.

**Two hybrids.** Let $T_1$ = `((a,b),(c,d));` and $T_2$ = `((a,c),(b,d));`. A brute force over all 52 partitions of $\{a, b, c, d, \rho\}$ finds that the smallest agreement forest has 3 blocks, and so does the smallest acyclic one. One of them is $\{\rho, a, d\}, \{b\}, \{c\}$: both trees restricted to $a, d, \rho$ give $((a, d), \rho)$, and the leaves $b$ and $c$ are single blocks. So $d_{\mathrm{rSPR}} = 2$ and $h = 2$. A network that shows both histories has $b$ and $c$ as hybrids.

**Reversed caterpillars.** For $T_1$ = `(((a,b),c),d);` and $T_2$ = `(((d,c),b),a);`, the brute force gives 3 blocks, so $h = 2$. On five taxa, the caterpillar $((((a, b), c), d), e)$ and its reverse give 4 blocks, so $h = 3$.

**When acyclicity matters.** For larger trees, the smallest agreement forest can be cyclic, and then $h > d_{\mathrm{rSPR}}$. A cycle means that block $A$ is above block $B$ in $T_1$ and below it in $T_2$. A network built from such a forest would need $A$ to be both an ancestor and a descendant of $B$, which is impossible in a directed acyclic graph. A brute force compared the caterpillar and a balanced tree on five taxa with each of the 105 rooted binary trees on these taxa, and it also tried 200 random pairs on six taxa. The two numbers were always equal, so such examples are rare on few taxa.

## Known algorithms

| method | input | type | cost |
|---|---|---|---|
| brute force over partitions | two trees | exact, by the forest theorem | exponential in $n$ |
| kernel of Bordewich and Semple (2007), then search | two binary trees | exact, FPT | polynomial reductions to a kernel whose size depends only on $h$, then a search exponential in $h$ |
| bounded search trees on acyclic forests | two trees | exact, FPT | about $c^h \cdot \mathrm{poly}(n)$ for a constant $c$ |
| cluster networks (Dendroscope) | clusters of many trees | heuristic, not minimum | polynomial |
| SNaQ (Solis-Lemus and Ane 2016) | gene trees or quartet frequencies | statistical, under incomplete lineage sorting | heuristic search over level-1 networks |
| likelihood and Bayesian methods (PhyloNet and others) | gene trees or sequences | statistical | expensive, limited to few taxa and reticulations |

## Bounds

- **Lower bound by rSPR.** $h(T_1, T_2) \ge d_{\mathrm{rSPR}}(T_1, T_2)$, because every acyclic agreement forest is an agreement forest. The two can differ.
- **Upper bound.** $h(T_1, T_2) \le n - 2$ for $n \ge 2$ taxa. Take the forest that keeps two taxa $x, y$ with $\rho$ and makes every other taxon a single block. Both trees restricted to $x, y, \rho$ give $((x, y), \rho)$, the single leaves are not on the paths between $x$, $y$ and $\rho$, and the forest is acyclic, because single leaves have no descendants in either tree. It has $n - 1$ blocks.
- **Hardness.** Computing $h$ for two rooted binary trees is NP-hard and APX-hard (Bordewich and Semple 2007).
- **Parameterized.** The problem is [fixed-parameter tractable](/fixed-parameter-tractable/) in $h$: after reductions that collapse common subtrees and shorten common chains, the instance has size bounded by a function of $h$ (Bordewich and Semple 2007).
- **Number of displayed trees.** A network with $h$ binary reticulations displays at most $2^h$ trees, so $k$ distinct gene trees need $h \ge \lceil \log_2 k \rceil$.

## Reductions

- **To acyclic agreement forests.** For two binary trees, the hybridization number problem is exactly the minimum acyclic agreement forest problem, so algorithms for one solve the other.
- **From maximum agreement forest.** The rSPR distance is the minimum agreement forest without the acyclic rule. The NP-hardness proofs for both problems use similar reductions, and the FPT algorithms share the reduction rules.
- **From tree containment.** Checking a proposed network is the tree containment problem, whether a network displays a given tree. It is NP-complete in general, which makes even the verification of a solution hard without restrictions on the network.

## Applications

- **Hybrid speciation.** Plants, fish and some animal groups have hybrid species, and networks show which parents they came from.
- **Introgression and admixture.** Networks summarize gene flow between populations or species, as in the history of modern humans and archaic hominins.
- **Gene transfer in microbes.** For bacteria and archaea, transfer networks show which genes moved between lineages.
- **Recombination in genes.** Recombination networks show the mosaic structure of sequences, for example in viruses.

## References
