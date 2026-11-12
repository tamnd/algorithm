---
tag: PA4HJT
kind: problem
slug: supertree
name: Supertree
aliases:
- supertree construction
area: biology/phylogenetics
level: advanced
summary: Combine trees on overlapping taxon sets into one tree on all the taxa. Polynomial for compatible rooted trees by BUILD, NP-hard for unrooted trees.
prereqs: [consensus-tree, rooted-triplet, quartet]
see_also: [maximum-quartet-consistency, maximum-rooted-triplet-consistency, quartet-max-cut, maximum-parsimony, strict-consensus, species-tree-estimation, astral, perfect-phylogeny]
sources:
  - paper: doi:10.1137/0210030
    title: Alfred V. Aho, Yehoshua Sagiv, Thomas G. Szymanski and Jeffrey D. Ullman, Inferring a tree from lowest common ancestors with an application to the optimization of relational expressions, SIAM Journal on Computing 10(3), 1981, pages 405 to 421
    locator: the BUILD algorithm, which decides whether a set of rooted triplets is compatible
  - paper: doi:10.1007/BF02618470
    title: Mike Steel, The complexity of reconstructing trees from qualitative characters and subtrees, Journal of Classification 9(1), 1992, pages 91 to 116
    locator: NP-completeness of the compatibility of unrooted trees and of quartets, and a polynomial algorithm for the strict consensus of all trees that display a set of rooted trees
  - paper: "Bernard R. Baum, Combining trees as a way of combining data sets for phylogenetic inference, and the desirability of combining gene trees, Taxon 41, 1992, pages 3 to 10"
    title: Bernard R. Baum, Combining trees as a way of combining data sets for phylogenetic inference
    locator: the matrix representation of trees, coded for parsimony
  - paper: doi:10.1016/1055-7903(92)90035-F
    title: Mark A. Ragan, Phylogenetic inference based on matrix representation of trees, Molecular Phylogenetics and Evolution 1(1), 1992, pages 53 to 58
    locator: matrix representation with parsimony (MRP)
  - paper: doi:10.1016/S0166-218X(00)00202-X
    title: Charles Semple and Mike Steel, A supertree method for rooted trees, Discrete Applied Mathematics 105(1-3), 2000, pages 147 to 158
    locator: the MinCut supertree, which extends BUILD to incompatible input
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 6, Subtrees and supertrees
  - book: isbn:9781107184718
    title: Tandy Warnow, Computational Phylogenetics, 2017
    locator: Chapter 7, Supertrees
---

The supertree problem takes trees whose taxon sets overlap but differ, and asks for one tree on the union of all the taxa that agrees with the input trees as well as possible. When all trees have the same taxa, it is the [consensus tree](/consensus-tree/) problem. The exact question, whether some tree agrees with every input tree, is easy for rooted trees, by the BUILD algorithm on [rooted triplets](/rooted-triplet/), and NP-complete for unrooted trees, because it contains the [quartet](/quartet/) compatibility problem (Steel 1992). Real inputs conflict, so practical methods optimize a score, for example the parsimony score of a matrix that codes the input trees.

## In plain words

Different studies build trees for different groups of species. One study has cats, dogs and bears. Another has dogs, bears, seals and walruses. No study has all of them. A supertree method joins these small trees into one large tree on all the species.

The large tree should show each small tree when you look only at that tree's species. Sometimes no large tree can do that for all small trees, because the studies disagree. Then the method has to decide which statements to keep. Different methods decide in different ways: some count how many small groupings the big tree keeps, some code each small tree as a table of yes and no answers and fit a tree to the table.

## Definition

**Restriction.** For a tree $T$ on a leaf set $X$ and a set $L \subseteq X$, the restriction $T|L$ is the smallest subtree of $T$ that connects the leaves in $L$, with each node of degree 2 suppressed. For a rooted tree, keep the lowest common ancestor of $L$ as the root.

**Display.** A tree $T$ *displays* a tree $t$ on the leaf set $L \subseteq X$ if $T|L$ equals $t$ or refines $t$, which means that $t$ is obtained from $T|L$ by contracting edges.

**Input.** A profile $P = (t_1, \ldots, t_k)$ of trees, all rooted or all unrooted, where $t_i$ has the leaf set $L_i$. Let $X = L_1 \cup \cdots \cup L_k$ and $n = |X|$.

**Compatibility (decision).** Is there a tree $T$ on $X$ that displays every $t_i$? Such a profile is *compatible*.

**Optimization.** Return a tree $T$ on $X$ that minimizes a cost $\mathrm{cost}(T, P)$. Common costs are the number of input [rooted triplets](/rooted-triplet/) or [quartets](/quartet/) that $T$ does not display, the parsimony score of a matrix that codes $P$, and the sum of [Robinson-Foulds distances](/robinson-foulds-distance/) between $T|L_i$ and $t_i$.

A rooted tree displays $t$ if and only if it displays every rooted triplet of $t$. An unrooted binary tree displays $t$ if and only if it displays every quartet of $t$. So every supertree input can be written as a set of triplets or of quartets.

## Variants

- **Rooted compatibility.** Decide whether a set of rooted trees has a common supertree. The BUILD algorithm of Aho, Sagiv, Szymanski and Ullman (1981) does this in polynomial time and returns a tree when one exists.
- **Unrooted compatibility.** The same question for unrooted trees, or for quartets, is NP-complete (Steel 1992).
- **[Maximum rooted triplet consistency](/maximum-rooted-triplet-consistency/).** Find a rooted tree that displays as many input triplets as possible.
- **[Maximum quartet consistency](/maximum-quartet-consistency/).** Find an unrooted tree that displays as many input quartets as possible. [Quartet MaxCut](/quartet-max-cut/) is a heuristic for it.
- **Matrix representation with parsimony (MRP).** Code each nontrivial cluster or split of each input tree as a binary character: 1 for the taxa in the cluster, 0 for the other taxa of that tree, and missing for taxa outside the tree. Return a [maximum parsimony](/maximum-parsimony/) tree of this matrix (Baum 1992, Ragan 1992).
- **MinCut supertree.** When BUILD finds a connected graph, cut it with a minimum cut of a weighted graph and go on (Semple and Steel 2000).
- **Robinson-Foulds supertree.** Minimize $\sum_i d_{RF}(T|L_i, t_i)$.
- **Strict consensus of all supertrees.** When the rooted profile is compatible, return the clusters shared by all trees that display it. Steel (1992) gives a polynomial algorithm.

## Examples

**A compatible rooted profile.** Let $t_1$ = `((A,B),C);` on ABC and $t_2$ = `((B,C),D);` on BCD. The tree `(((A,B),C),D);` displays both: its restriction to ABC is $t_1$, and its restriction to BCD is `((B,C),D);`. BUILD finds it: on all four taxa, the triplet graph has the edges AB (from $t_1$) and BC (from $t_2$), so its components are ABC and D. Inside ABC, the edge AB gives the components AB and C.

**An incompatible rooted profile.** Take the four triplets $ab|c$, $bc|d$, $cd|a$ and $da|b$. Any two of them are displayed by one tree; for example `(((a,b),c),d);` displays $ab|c$ and $bc|d$. But on all four taxa, the triplet graph has the edges ab, bc, cd and da, which form one component. So no rooted tree displays all four. Brute force over all 26 rooted trees on four taxa shows that no tree displays three of them either. Six trees display two, for example `(((a,b),c),d);` with $ab|c$ and $bc|d$, and `((a,b),(c,d));` with $ab|c$ and $cd|a$.

**MRP coding.** For $t_1$ and $t_2$ above, the nontrivial clusters are AB and BC. The matrix has one column for each:

| taxon | AB in $t_1$ | BC in $t_2$ |
|---|---|---|
| A | 1 | ? |
| B | 1 | 1 |
| C | 0 | 1 |
| D | ? | 0 |

A tree on ABCD that needs one change per column is a maximum parsimony tree, and `(((A,B),C),D);` is one of them. It fills the missing entry of A in the second column with 1 and that of D in the first column with 0.

## Known algorithms

| problem | method | result |
|---|---|---|
| rooted compatibility | BUILD (Aho et al. 1981), described on the [rooted triplet](/rooted-triplet/) page | polynomial time |
| unrooted compatibility | none in polynomial time unless P = NP | [NP-complete](/np-complete/) (Steel 1992) |
| strict consensus of all compatible supertrees | Steel (1992) | polynomial time |
| MRP | heuristic parsimony search | NP-hard optimum |
| MinCut supertree | BUILD with minimum cuts (Semple and Steel 2000) | polynomial time, heuristic |
| maximum quartet consistency | [Quartet MaxCut](/quartet-max-cut/), quartet amalgamation | NP-hard optimum |

## Bounds

- **Rooted compatibility is in P.** BUILD splits the taxa by the connected components of a graph, and each split costs polynomial time.
- **Unrooted compatibility is NP-complete.** Steel (1992) proved this already for inputs that are all quartets.
- **The optimization problems are NP-hard.** This holds for [maximum rooted triplet consistency](/maximum-rooted-triplet-consistency/), for [maximum quartet consistency](/maximum-quartet-consistency/), and for MRP, because [maximum parsimony](/maximum-parsimony/) is NP-hard.
- **A fraction 1/3 of triplets is always possible.** For any set of rooted triplets, some tree displays at least one third of them, and one third is the best constant for the set of all triplets (Gąsieniec, Jansson, Lingas and Östlin 1999).

## Reductions

- **Rooted trees to triplets.** Replace each rooted tree by its triplets. A rooted tree displays the profile if and only if it displays all these triplets. This is how BUILD handles trees.
- **Unrooted trees to quartets.** Replace each unrooted tree by its quartets. Quartet compatibility is NP-complete, so unrooted supertree compatibility is NP-complete too.
- **To character compatibility.** The MRP matrix turns the supertree problem into a problem on binary characters with missing data. A profile of rooted trees is compatible exactly when the missing entries can be filled so that the columns, read as clusters, are pairwise compatible. That is a rooted [perfect phylogeny](/perfect-phylogeny/) with missing data.
- **Consensus is a special case.** If all $L_i$ are equal, a supertree method becomes a consensus method. Many methods are required to return the [strict consensus](/strict-consensus/) in that case.

## Applications

- **Large trees from many studies.** Supertrees join published trees into trees with thousands of taxa, for example for mammals or for flowering plants, when no single data set covers all taxa.
- **Divide and conquer.** A method can build trees on overlapping subsets of a large data set and then join them with a supertree method. Disk-covering methods and SuperFine use this idea.
- **Gene trees with missing taxa.** When genes are missing from some species, the gene trees have different taxon sets. [Species tree estimation](/species-tree-estimation/) methods such as [ASTRAL](/astral/) solve a related quartet problem.
- **Dating and taxonomy.** Supertrees serve as a frame for divergence times and for comparisons of rates of diversification.

## References
