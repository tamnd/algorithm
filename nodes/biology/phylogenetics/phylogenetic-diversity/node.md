---
tag: P2RFHN
kind: concept
slug: phylogenetic-diversity
name: Phylogenetic diversity
aliases:
- PD
- Faith's phylogenetic diversity
area: biology/phylogenetics
level: advanced
summary: The phylogenetic diversity of a set of taxa is the total branch length of the part of the phylogenetic tree that connects them.
prereqs: [phylogenetic-tree, rooted-and-unrooted-trees]
see_also: [phylogenetic-diversity-maximization, submodular-function, greedy-max-coverage, postorder-traversal, linearity-of-expectation, phylogenetic-independent-contrasts]
sources:
  - paper: doi:10.1016/0006-3207(92)91201-3
    title: Daniel P. Faith, Conservation evaluation and phylogenetic diversity, Biological Conservation 61(1), 1992
    locator: pp. 1-10 (the definition of PD as the length of the minimum spanning path of a set of taxa)
  - paper: doi:10.1080/10635150590947023
    title: Mike Steel, Phylogenetic diversity and the greedy algorithm, Systematic Biology 54(4), 2005
    locator: pp. 527-529 (PD on rooted and unrooted trees, and its maximization)
  - paper: doi:10.1371/journal.pone.0000296
    title: Nick J. B. Isaac, Samuel T. Turvey, Ben Collen, Carly Waterman and Jonathan E. M. Baillie, Mammals on the EDGE, conservation priorities based on threat and phylogeny, PLoS ONE 2(3), 2007
    locator: e296 (evolutionary distinctiveness, a share of branch length per species)
---

The phylogenetic diversity (PD) of a set $S$ of taxa is the sum of the branch lengths of the smallest part of a [phylogenetic tree](/phylogenetic-tree/) that connects the taxa of $S$. Faith defined it in 1992 as a measure of the variety of features that a set of species carries: a long branch stands for much independent evolution, so a set that spans long and distinct branches carries more feature diversity than a set of close relatives. On a [rooted tree](/rooted-and-unrooted-trees/), PD usually also counts the path up to the root. PD is the objective of [PD maximization](/phylogenetic-diversity-maximization/) in conservation planning, and it is a standard measure of the diversity of ecological communities.

## In plain words

Draw the family tree of all species in a group, with long branches for long times of separate evolution. Now pick some of the species and color the branches that link them. The total length of the colored branches is the phylogenetic diversity of your pick.

Two close cousins add little to each other: most of their branches are shared. A species on its own old branch adds much. So two sets with the same number of species can have very different diversity.

This makes it a good guide for saving species. If only a few can be protected, pick a set that keeps as much of the tree as possible.

## The idea

**The definition.** Let $T$ be a tree with leaf set $X$ and a length $\ell(e) \ge 0$ on each edge $e$. For $S \subseteq X$:

- the *unrooted* PD is the total length of the minimal subtree of $T$ that contains $S$;
- the *rooted* PD is the total length of the minimal subtree that contains $S$ and the root.

The two differ only by the path from the root to the subtree of $S$. They agree when $S$ has taxa on both sides of the root. Faith stated PD as the length of the minimum spanning path of the set. Much later work, and the PD index of community ecology, use the rooted form, which makes the PD of one taxon its distance from the root, not 0.

**Computing it.** An edge $e$ lies in the rooted PD subtree exactly when some taxon of $S$ is below $e$, and in the unrooted one exactly when $S$ has taxa both below and not below $e$. One [postorder traversal](/postorder-traversal/) counts the taxa of $S$ below each edge, so PD takes $O(n)$ time on a tree with $n$ leaves.

**It is a coverage function.** In the rooted version, each edge is an item of weight $\ell(e)$, and a taxon covers the edges on its path to the root. Then $\mathrm{PD}(S)$ is the total weight of the items covered by $S$. So rooted PD is monotone and [submodular](/submodular-function/): the gain of adding a taxon $x$ to $S$, which is the length of the part of its root path not yet covered, can only shrink as $S$ grows. Maximizing PD with $k$ taxa is thus a case of [weighted maximum coverage](/greedy-max-coverage/). The tree structure makes it much easier than general coverage: the greedy algorithm is exactly optimal, see [PD maximization](/phylogenetic-diversity-maximization/).

**PD is not species richness.** For a star tree with equal edge lengths, PD is proportional to the number of taxa. On any other tree, sets of the same size can differ widely in PD.

**Expected PD.** If each taxon $i$ survives a period independently with probability $p_i$, then by [linearity of expectation](/linearity-of-expectation/) the expected rooted PD of the survivors is

$$E[\mathrm{PD}] = \sum_{e} \ell(e) \Big(1 - \prod_{i \text{ below } e} (1 - p_i)\Big),$$

because an edge survives when at least one taxon below it survives. This is the objective of the probabilistic forms of the conservation problem.

**Sharing PD among species.** Measures of *evolutionary distinctiveness* divide the length of each edge among the taxa below it, for example in equal parts. The share of a taxon is large when it sits alone on a long branch. The EDGE program combines it with the threat status of each species.

## Examples

Take the rooted tree $((A{:}1, B{:}2){:}3, (C{:}4, (D{:}1, E{:}1){:}2){:}1)$, in which the number after a colon is the length of the edge above that node. Its total length is 15.

| set $S$ | unrooted PD | rooted PD |
|---|---|---|
| $\{A\}$ | 0 | 4 |
| $\{A, B\}$ | 3 | 6 |
| $\{D, E\}$ | 2 | 5 |
| $\{A, C\}$ | 9 | 9 |
| $\{A, B, C\}$ | 11 | 11 |
| $\{B, C, D\}$ | 13 | 13 |

The pair $\{A, B\}$ shares the edge of length 3, so it spans less than the pair $\{A, C\}$, which uses both sides of the tree. The gain of adding $D$ is $1 + 2 + 1 = 4$ to the empty set, $3$ to $\{C\}$ and $1$ to $\{E\}$: the more of its path is already covered, the less $D$ adds.

If each of the five taxa survives with probability $1/2$, the expected rooted PD of the survivors is

$$\tfrac12 (1 + 2 + 4 + 1 + 1) + \tfrac34 (3 + 2) + \tfrac78 \cdot 1 = 4.5 + 3.75 + 0.875 = 9.125,$$

since the edge above $\{C, D, E\}$ is lost only when all three of $C$, $D$ and $E$ are lost.

## Where it is used

- **Conservation priorities.** Choosing which species or areas to protect so that the surviving PD is large, possibly with costs and survival probabilities ([PD maximization](/phylogenetic-diversity-maximization/)).
- **Community ecology.** The PD of the species found at a site compares sites beyond their species counts, and the PD of a sample of microbial sequences on a reference tree is a standard diversity index in microbiome studies.
- **Species rankings.** Evolutionary distinctiveness scores, as in the EDGE lists of mammals and other groups, rank species by the amount of the tree that they alone carry.
- **Biogeography.** PD per area, and PD restricted to taxa found only in one area, show where old and unique lineages live.

## References
