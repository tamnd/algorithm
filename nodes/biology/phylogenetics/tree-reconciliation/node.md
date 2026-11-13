---
tag: J3QYY1
kind: problem
slug: tree-reconciliation
name: Gene tree-species tree reconciliation
aliases:
- reconciliation
- gene tree reconciliation
- DTL reconciliation
area: biology/phylogenetics
level: advanced
summary: Map a gene tree into a species tree at the least cost, and explain each discordance by a duplication, a loss or a transfer.
prereqs: [phylogenetic-tree, rooted-tree]
see_also: [lca-reconciliation, duplication-loss-model, horizontal-gene-transfer, incomplete-lineage-sorting, tree-dynamic-programming, np-hard, phylogenetic-network, species-tree-estimation]
sources:
  - paper: doi:10.2307/2412519
    title: Morris Goodman, John Czelusniak, G. William Moore, A. E. Romero-Herrera and Genji Matsuda, Fitting the gene lineage into its species lineage, a parsimony strategy illustrated by cladograms constructed from globin sequences, Systematic Zoology 28(2), 1979
    locator: pp. 132-163 (the first reconciliation of a gene tree with a species tree by duplications and losses)
  - paper: doi:10.1093/sysbio/43.1.58
    title: Roderic D. M. Page, Maps between trees and cladistic analysis of historical associations among genes, organisms, and areas, Systematic Biology 43(1), 1994
    locator: pp. 58-77 (maps between trees for genes in species, parasites in hosts and taxa in areas)
  - paper: doi:10.1109/TCBB.2010.14
    title: Ali Tofigh, Michael Hallett and Jens Lagergren, Simultaneous identification of duplications and lateral gene transfers, IEEE/ACM Transactions on Computational Biology and Bioinformatics 8(2), 2011
    locator: pp. 517-535 (polynomial-time reconciliation with duplications and transfers when time consistency is not required)
  - paper: doi:10.1093/bioinformatics/bts225
    title: Mukul S. Bansal, Eric J. Alm and Manolis Kellis, Efficient algorithms for the reconciliation problem with gene duplication, horizontal transfer and loss, Bioinformatics 28(12), 2012
    locator: pp. i283-i291 (an O(mn) algorithm for DTL reconciliation on undated species trees)
  - paper: doi:10.1089/cmb.2009.0240
    title: Yaniv Ovadia, Daniel Fielder, Chris Conow and Ran Libeskind-Hadas, The cophylogeny reconstruction problem is NP-complete, Journal of Computational Biology 18(1), 2011
    locator: pp. 59-65 (NP-completeness of reconciliation with transfers under time consistency)
  - paper: doi:10.1016/j.tcs.2006.05.019
    title: Paweł Górecki and Jerzy Tiuryn, DLS-trees, a model of evolutionary scenarios, Theoretical Computer Science 359(1-3), 2006
    locator: pp. 378-399 (duplication-loss scenarios and the optimality of the LCA mapping)
  - paper: doi:10.1101/gr.123901.111
    title: Matthew D. Rasmussen and Manolis Kellis, Unified modeling of gene duplication, loss, and coalescence using a locus tree, Genome Research 22(4), 2012
    locator: pp. 755-765 (reconciliation with duplications, losses and incomplete lineage sorting)
---

Gene tree-species tree reconciliation takes a rooted gene tree, a rooted species tree and the species of each gene, and asks for the cheapest way to draw the gene tree inside the species tree. Each place where the two trees disagree must be explained by an event: a gene duplication, a gene loss, or a [horizontal gene transfer](/horizontal-gene-transfer/) from one species lineage to another. With duplications and losses only, the [LCA mapping](/lca-reconciliation/) solves the problem exactly in linear time. With transfers, a dynamic program over pairs of nodes solves it in $O(mn)$ time if the transfers may contradict the order of time, and the problem is NP-hard if they must respect it.

## In plain words

Genes live inside species. When a species splits in two, each gene in it splits too, so a gene's family tree normally follows the species tree. But genes also get copied inside a species, get lost, or jump from one species to another. Then the gene tree looks different from the species tree.

Reconciliation finds the story that fits the gene tree into the species tree with the fewest of these unusual events, or with the lowest total cost when each kind of event has its own price. The story tells us which genes are copies of each other inside a species and which are the same gene in different species.

## Definition

**Input.** A rooted binary gene tree $G$ with $n$ nodes, a rooted binary species tree $S$ with $m$ nodes, a leaf map $\sigma$ from the leaves of $G$ to the leaves of $S$, and event costs $c_D$, $c_T$, $c_L \ge 0$.

**A reconciliation** assigns each node $g$ of $G$ a species node or species edge $M(g)$ and an event: a leaf, a speciation, a duplication or a transfer. Each event has local rules:

- A *speciation* at species node $s$ sends the two children of $g$ into the two subtrees below the two different children of $s$.
- A *duplication* at $s$ keeps both children of $g$ in the subtree of $s$.
- A *transfer* keeps one child of $g$ in the subtree of $s$ and moves the other child to a species node that is not an ancestor or descendant of $s$.
- A *loss* is counted for each species node that a gene lineage passes through without leaving a descendant on one side.

**Output.** A reconciliation that minimizes $c_D D + c_T T + c_L L$, where $D$, $T$ and $L$ are the numbers of duplications, transfers and losses.

## Variants

- **Duplication only (D).** Minimize $D$. This is the gene duplication problem.
- **Duplication and loss (DL).** Transfers are not allowed. The probabilistic form is the [duplication-loss model](/duplication-loss-model/).
- **Duplication, transfer and loss (DTL), undated.** Transfers can go between any two species lineages that are not ancestor and descendant.
- **DTL with time consistency.** All transfers together must fit a single order of the species tree nodes in time: a transfer goes only between lineages that exist at the same time, and a set of transfers must not force a cycle in time.
- **DTL on a dated species tree.** The species tree has known node times, cut into time slices, and transfers go only within a slice.
- **With incomplete lineage sorting.** Add [deep coalescence](/incomplete-lineage-sorting/) as an explanation for discordance, as in the locus-tree model of Rasmussen and Kellis (2012).
- **Non-binary trees.** Polytomies in the gene tree or the species tree must be resolved or given special rules.
- **Host and parasite trees.** The same mathematics with host and parasite in place of species and gene, where transfers become host switches. This is cophylogeny reconstruction.

## Examples

Take the species tree $((a, b), c)$ and the gene tree $((a_1, c_1), b_1)$, with costs $c_D = 2$, $c_T = 3$, $c_L = 1$.

**A DL reconciliation.** The LCA mapping puts $(a_1, c_1)$ at the species root as a speciation. Its $a$ side passes through the node $ab$ and is lost in $b$: one loss. The gene root then maps to the species root too, so it is a duplication, and the copy that leads to $b_1$ is lost in $c$ and in $a$: two more losses. The cost is $2 \cdot 1 + 1 \cdot 3 = 5$.

**A DTL reconciliation.** Put the gene root at the node $ab$ as a speciation, with $(a_1, c_1)$ on the $a$ side and $b_1$ on the $b$ side. The node $(a_1, c_1)$ is a transfer from the lineage of $a$ into $c$. The cost is $3$, so with these costs the transfer story wins. With $c_T = 6$ the DL story wins.

Under the [multispecies coalescent](/multispecies-coalescent/), the same gene tree also arises without any duplication, loss or transfer, by incomplete lineage sorting in the ancestral species of $a$ and $b$.

## Known algorithms

- **LCA mapping, for D and DL.** Map each gene node to the LCA of the species below it. It minimizes duplications and losses at the same time, and runs in $O(n + m)$ with constant-time LCA queries (Page 1994; Zhang 1997; Górecki and Tiuryn 2006). See [LCA reconciliation](/lca-reconciliation/).
- **Dynamic programming for undated DTL.** Let $c(g, s)$ be the least cost of the subtree of $g$ when $g$ maps to $s$. A postorder pass over $G$ fills $c(g, s)$ for all $s$ from the values of the children of $g$, with three options: a speciation that sends the children into the two child subtrees of $s$, a duplication that keeps both in the subtree of $s$, or a transfer that keeps one and moves the other to a species node off the root path of $s$. Each option needs a minimum over a subtree of $S$ or over its complement, with the losses on the path. Precomputing these minima with one postorder and one preorder pass over $S$ per gene node gives $O(1)$ work per pair, so $O(mn)$ time in total (Bansal, Alm and Kellis 2012). Tofigh, Hallett and Lagergren (2011) gave an earlier polynomial algorithm for this undated problem.
- **Dated species trees.** With transfers restricted to time slices, the same kind of dynamic program runs over pairs of gene nodes and slice edges, in polynomial time.
- **Probabilistic reconciliation.** Under the duplication-loss model or its extensions with transfers, a reconciliation has a likelihood, and samplers or sums over all reconciliations replace the single best one.

## Bounds

- Reading the input takes $\Omega(n + m)$ time, and the LCA mapping meets this bound for D and DL.
- Undated DTL is in $O(mn)$ time.
- DTL with time consistency is NP-hard (Ovadia et al. 2011). The undated dynamic program does not enforce it, so it can return a set of transfers that no ordering of the species tree in time allows, and a check or repair step is needed.

## Reductions

- **DL to LCA queries.** DL reconciliation reduces to $n$ [lowest common ancestor](/lowest-common-ancestor/) queries in $S$ plus depth differences.
- **Gene duplication problem for species trees.** To choose the species tree that minimizes the total duplication cost over many gene trees, reconciliation is the inner step of a search over species trees. That outer problem is NP-hard.
- **Cophylogeny.** Host-parasite reconciliation with host switches is the same problem as DTL, so the hardness result of Ovadia et al. holds for both.

## Applications

- **Orthology and paralogy.** Two genes whose last common ancestor is a speciation are orthologs, and genes whose last common ancestor is a duplication are paralogs. Genome annotation pipelines use reconciliation to find these relations.
- **Gene family evolution.** Counts of duplications, losses and transfers on each species branch show when gene families grew or shrank.
- **Microbial evolution.** DTL reconciliation finds transferred genes in bacteria and archaea, where transfers are common.
- **Species tree inference.** Gene tree parsimony uses the reconciliation cost to score candidate species trees, as a [species tree estimation](/species-tree-estimation/) method for gene families with paralogs.
- **Host and parasite studies.** Cophylogeny tools reconcile parasite trees with host trees to find cospeciation and host switches.

## References
