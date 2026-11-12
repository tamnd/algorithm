---
tag: 905VMZ
kind: problem
slug: tree-rooting
name: Tree rooting
aliases:
- root placement
- rooting a phylogeny
area: biology/phylogenetics
level: intro
summary: Choose the point of an unrooted phylogenetic tree where the common ancestor lies. Outgroups, midpoint, minimum variance and clock methods each use different extra information.
prereqs: [rooted-and-unrooted-trees, phylogenetic-tree]
see_also: [midpoint-rooting, molecular-clock, relaxed-molecular-clock, maximum-likelihood-phylogeny, long-branch-attraction, tree-reconciliation, divergence-time-estimation, tree-diameter]
sources:
  - paper: doi:10.1007/BF01734359
    title: Joseph Felsenstein, Evolutionary trees from DNA sequences, a maximum likelihood approach, Journal of Molecular Evolution 17(6), 1981, 368-376
    locator: the pulley principle, by which the likelihood under a reversible model does not depend on the position of the root
  - paper: doi:10.1371/journal.pone.0182238
    title: Uyen Mai, Erfan Sayyari and Siavash Mirarab, Minimum variance rooting of phylogenetic trees and implications for species tree reconstruction, PLoS ONE 12(8), 2017, e0182238
    locator: the minimum variance rooting criterion, its linear-time algorithm, and the comparison with midpoint rooting under rate variation
  - paper: doi:10.1038/s41559-017-0193
    title: Fernando D. K. Tria, Giddy Landan and Tal Dagan, Phylogenetic rooting using minimal ancestor deviation, Nature Ecology and Evolution 1, 2017, article 0193
    locator: the MAD rooting criterion based on the deviations of all pairs of leaves from a clock
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 16, Likelihood methods (the section Unrootedness)
---

Tree rooting is the problem of finding the point on an unrooted [phylogenetic tree](/phylogenetic-tree/) where the common ancestor of all its taxa lies. Most reconstruction methods return an unrooted tree, because under the usual reversible models of sequence change the data say nothing about the root. So the root must come from extra information: taxa known to lie outside the group (an outgroup), an assumption about rates such as a [molecular clock](/molecular-clock/), or a criterion on the branch lengths such as [midpoint rooting](/midpoint-rooting/) or minimum variance rooting. Each method is exact under its assumption and can be wrong when the assumption fails.

## In plain words

An unrooted tree shows which species are close to which, but not which branching came first. To read it as a history, we must say where the oldest ancestor sits. That choice is the root.

The sequences alone usually cannot tell us. The common way out is to add one or more species that we already know are only distant relatives. They branch off first, so the root sits where they join the rest.

Without such relatives, we can use the branch lengths. If all lineages changed at the same speed, every species would be equally far from the root, and the root would sit at the middle of the longest path between two species. Other methods pick the point from which the distances to the species are as equal as possible. These methods fail when some lineages changed much faster than others.

## Definition

**Input.** An unrooted phylogenetic tree $U$ on a set $X$ of $n$ taxa, usually with branch lengths $\ell(e) \ge 0$, and possibly extra information: a set $O \subset X$ of outgroup taxa, a model of rates, or the sampling dates of the taxa.

**Output.** A *root position*: an edge $e = \{u, v\}$ of $U$ and a distance $0 \le t \le \ell(e)$ from $u$, or a vertex. Subdividing $e$ at that point by a new vertex $\rho$ and directing the edges away from $\rho$ gives a rooted tree (see [rooted and unrooted trees](/rooted-and-unrooted-trees/)).

The topology of the rooted tree depends only on the edge, and the branch lengths at the root depend on $t$. A binary tree has $2n - 3$ edges, so there are $2n - 3$ rooted topologies to choose from.

**Why the data do not fix the root.** Under a time-reversible substitution model, the likelihood of a tree does not change when the root moves along the tree, as long as the sum of the lengths of the two edges at the root stays the same. This is Felsenstein's *pulley principle* (1981). So a [maximum likelihood](/maximum-likelihood-phylogeny/) tree under such a model is unrooted, and the same holds for parsimony with symmetric costs. Rooting is a separate step that needs information from outside the model.

## Variants

- **Outgroup rooting.** Given taxa $O$ that are known to be outside the *ingroup* $I = X \setminus O$, place the root on the edge whose split is $O \mid I$. If $O \mid I$ is not a split of $U$, the outgroup is not a clade on the tree and the method gives no answer. Outgroup rooting fixes the edge but not $t$.
- **Midpoint rooting.** Place the root at the midpoint of a longest leaf-to-leaf path. It is exact for an ultrametric (clock-like) tree; see [midpoint rooting](/midpoint-rooting/).
- **Minimum variance (MV) rooting.** Place the root at the point that minimizes the variance of the root-to-tip distances (Mai, Sayyari and Mirarab, 2017). On each edge the variance is a quadratic function of $t$, so the best point of each edge has a closed form.
- **Minimal ancestor deviation (MAD).** For each candidate root, measure how far each pair of leaves deviates from the clock assumption, and take the root with the least mean deviation (Tria, Landan and Dagan, 2017).
- **Clock rooting.** Fit a [molecular clock](/molecular-clock/) or a [relaxed clock](/relaxed-molecular-clock/) model, whose likelihood depends on the root, and take the root of the best fit. With sampling dates, as for virus sequences, choose the root at which the root-to-tip distances best fit a linear function of the dates.
- **Rooting gene trees.** A gene tree with several copies per species can be rooted at the point that needs the fewest duplications and losses when it is reconciled with a species tree; see [tree reconciliation](/tree-reconciliation/).

## Examples

Take the rooted tree $((A{:}1, B{:}6){:}1, (C{:}1, D{:}1){:}1)$: the lineage of $B$ evolved six times as fast as the others. Unrooted, it is the tree with inner vertices $P$ (joined to $A$, $B$) and $Q$ (joined to $C$, $D$), and with the edges $P - A$ of length 1, $P - B$ of length 6, $Q - C$ and $Q - D$ of length 1, and $P - Q$ of length $1 + 1 = 2$. The true root is on the edge $P - Q$, at distance 1 from $P$.

| method | root position | rooted topology | right? |
|---|---|---|---|
| outgroup $\{C, D\}$ | edge $P - Q$ (split $AB \mid CD$) | $((A,B),(C,D))$ | yes, edge only |
| midpoint | edge $B - P$, at $9/2$ from $B$ | $(B,(A,(C,D)))$ | no |
| minimum variance | edge $B - P$, at $25/6$ from $B$ | $(B,(A,(C,D)))$ | no |

The longest path is $B$ to $C$ (or $D$), of length $6 + 2 + 1 = 9$, so the midpoint is at $9/2$ from $B$, inside the long edge of $B$. At the MV root the root-to-tip distances are $B$: $25/6$, $A$: $17/6$, $C$ and $D$: $29/6$, with variance $2/3$. At the true root they are $2, 7, 2, 2$, with variance $75/16$. Both methods trade the true root for a point where the tips look more equally far away, because they assume rates that are close to equal.

Now take the ultrametric tree $((A{:}2, B{:}2){:}1, (C{:}1, D{:}1){:}2)$, in which every leaf is at distance 3 from the root. Unrooted, $P - Q$ has length 3. The longest path has length 6, its midpoint is on $P - Q$ at distance 1 from $P$, and the root-to-tip distances there are all 3, with variance 0. So midpoint and MV rooting both return the true root and the true branch lengths.

## Known algorithms

- **Outgroup rooting** finds the edge with split $O \mid I$ in $O(n)$ time: root the tree at any leaf of $I$, compute the number of outgroup taxa below each vertex, and take the vertex whose cluster is exactly $O$.
- **[Midpoint rooting](/midpoint-rooting/)** finds a longest path by a double sweep, as in the [tree diameter](/tree-diameter/) problem, and walks to its middle: $O(n)$ time.
- **MV rooting** computes, for every edge, the sums of the root-to-tip distances and of their squares on each side, by two traversals, and minimizes a quadratic on each edge: $O(n)$ time (Mai, Sayyari and Mirarab, 2017).
- **MAD rooting** looks at all pairs of leaves for each candidate root, so it takes at least quadratic time; this is fast enough for trees of a few thousand taxa. Tria, Landan and Dagan also describe a clock-based variant, MCCV, which is the same criterion as MV rooting.
- **Clock rooting** by likelihood tries the root on each edge and optimizes the clock model; its cost is that of $2n - 3$ likelihood optimizations, usually reduced by searching near the current best edge.

## Bounds

- Any method must read the tree, so $\Omega(n)$ time is needed; outgroup, midpoint and MV rooting reach it.
- **No information from topology alone.** Without branch lengths or outgroups, all $2n - 3$ edges are equally consistent with an unrooted tree, so no rooting method can do better than guess.
- **No information from reversible models.** By the pulley principle, likelihood under a reversible model is flat over root positions, so a likelihood-based root needs a clock or a non-reversible model.

## Reductions

- **Rooting at a leaf.** Rooting at the edge of a leaf $r$ turns every split $A \mid B$ into the cluster of its side without $r$. Many algorithms on unrooted trees, such as [Day's algorithm](/day-algorithm/), use this to reduce to rooted trees; it is a rooting of convenience, not a claim about history.
- **Outgroup rooting to split lookup.** The outgroup method succeeds exactly when $O \mid X \setminus O$ is in the [split set](/splits-of-a-tree/) of $U$, so it is a membership test in a [split system](/split-system/).
- **Midpoint rooting to the tree center.** The midpoint of a longest path is the center of the tree as a metric space: the point that minimizes the largest distance to a leaf.

## Applications

- **Reading a tree as a history.** Rooting decides which groups are clades, which character states are ancestral, and in which order lineages split.
- **Dating.** [Divergence time estimation](/divergence-time-estimation/) needs a rooted tree, and the root position changes the dates.
- **Species tree methods.** Methods that combine rooted gene trees, and methods based on [rooted triplets](/rooted-triplet/), need each gene tree to be rooted; MV rooting was designed with this use in mind.
- **Outbreak studies.** Virus trees are rooted by the sampling dates to find the time and place of the first infection.
- **Pitfall of distant outgroups.** A very distant outgroup has a long branch, which can join the longest branch of the ingroup by [long branch attraction](/long-branch-attraction/) and place the root wrongly. A close outgroup, or several outgroups, reduces the risk.

## References
