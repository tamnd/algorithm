---
tag: VSMQ48
kind: algorithm
slug: lca-reconciliation
name: LCA-based reconciliation
aliases:
- least common ancestor mapping
- LCA mapping
area: biology/phylogenetics
level: advanced
summary: Map each gene tree node to the LCA in the species tree of the species below it. This gives the fewest duplications and losses.
solves: [tree-reconciliation]
model: word-ram
complexity:
  vars: {n: the number of gene tree nodes, m: the number of species tree nodes}
  time: {worst: O(n + m)}
  space: {extra: O(n + m)}
history:
  year: 1979
  people: [Morris Goodman, John Czelusniak, G. William Moore, A. E. Romero-Herrera, Genji Matsuda]
  note: Goodman and coauthors fitted globin gene trees into species trees by a parsimony count of duplications and losses in 1979.
prereqs: [tree-reconciliation, lowest-common-ancestor]
see_also: [euler-tour-lca, rmq-lca-equivalence, range-minimum-query, duplication-loss-model, horizontal-gene-transfer, postorder-traversal, rooted-tree]
sources:
  - paper: doi:10.2307/2412519
    title: Morris Goodman, John Czelusniak, G. William Moore, A. E. Romero-Herrera and Genji Matsuda, Fitting the gene lineage into its species lineage, a parsimony strategy illustrated by cladograms constructed from globin sequences, Systematic Zoology 28(2), 1979
    locator: pp. 132-163 (the parsimony count of duplications and losses of a gene tree in a species tree)
  - paper: doi:10.1093/sysbio/43.1.58
    title: Roderic D. M. Page, Maps between trees and cladistic analysis of historical associations among genes, organisms, and areas, Systematic Biology 43(1), 1994
    locator: pp. 58-77 (the LCA map of a gene tree into a species tree, and the duplication count)
  - paper: doi:10.1089/cmb.1997.4.177
    title: Louxin Zhang, On a Mirkin-Muchnik-Smith conjecture for comparing molecular phylogenies, Journal of Computational Biology 4(2), 1997
    locator: pp. 177-187 (the LCA mapping gives the fewest duplications and losses)
  - paper: doi:10.1016/j.tcs.2006.05.019
    title: Paweł Górecki and Jerzy Tiuryn, DLS-trees, a model of evolutionary scenarios, Theoretical Computer Science 359(1-3), 2006
    locator: pp. 378-399 (the LCA mapping minimizes duplications, losses and their weighted sums)
  - paper: doi:10.1093/bioinformatics/17.9.821
    title: Christian M. Zmasek and Sean R. Eddy, A simple algorithm to infer gene duplication and speciation events on a gene tree, Bioinformatics 17(9), 2001
    locator: pp. 821-828 (a simple implementation of the LCA mapping)
---

LCA-based reconciliation maps each node of a rooted gene tree to a node of a rooted species tree: a gene leaf goes to the species it was sampled from, and an internal gene node goes to the [lowest common ancestor](/lowest-common-ancestor/) (LCA) of the images of its two children. A gene node that maps to the same species node as one of its children is a duplication; the others are speciations. The number of gene losses follows from the depths of the images. Among all valid maps, the LCA map has the fewest duplications and the fewest losses, and with constant-time LCA queries it takes linear time.

## In plain words

A gene family evolves inside a tree of species. When a species splits, the gene splits with it. Sometimes a gene is copied inside one species, so both copies are passed down, and sometimes a copy is lost.

We know the tree of the gene copies, and we know which species each copy is from. For each branching point of the gene tree, we look at all species below it and place it at the youngest species ancestor that has all of them. If the branching point lands at the same place as one of its two branches, the two branches did not come from a species split, so it must have been a copy event.

Placing each point as low as it can go explains the gene tree with the fewest copies and the fewest losses.

## The problem

**Input.** A rooted binary gene tree $G$, a rooted species tree $S$, and a map $\sigma$ from the leaves of $G$ to the leaves of $S$. Several gene leaves can map to the same species.

**A valid map** is a function $M$ from the nodes of $G$ to the nodes of $S$ with $M(\ell) = \sigma(\ell)$ for each leaf $\ell$, and $M(g) \succeq M(g')$ for each child $g'$ of $g$, where $x \succeq y$ means that $x$ is an ancestor of $y$ or equal to it. An internal node $g$ with children $g_1, g_2$ is a *speciation* under $M$ if $M(g_1)$ and $M(g_2)$ lie below two different children of $M(g)$; otherwise it is a *duplication*. Write $\delta(g) = 1$ for a duplication and $\delta(g) = 0$ for a speciation.

**Costs.** With $d(x, y)$ the number of edges from $x$ down to $y$, the number of losses is

$$L(M) = \sum_{g \text{ internal}} \ \sum_{i = 1, 2} \Big( d\big(M(g), M(g_i)\big) - 1 + \delta(g) \Big),$$

since a speciation at $M(g)$ sends one copy into each child of $M(g)$, and each species node skipped below that is a loss, while a duplication at $M(g)$ leaves both copies at $M(g)$. $D(M)$ is the number of duplications.

**Output.** The valid map that minimizes $D$, $L$, or $c_D D + c_L L$, with its events.

## The algorithm

```pseudo id=main
LCA-RECONCILE(G, S, σ)
L1  preprocess S for constant-time LCA queries and node depths
L2  for each node g of G, in postorder do
L3      if g is a leaf then M(g) ← σ(g)
L4      else M(g) ← lca_S(M(g1), M(g2))
L5          if M(g) = M(g1) or M(g) = M(g2) then mark g as a duplication
L6          else mark g as a speciation
L7          losses ← losses + Σ over i of (depth(M(gi)) − depth(M(g)) − 1 + [g is a duplication])
L8  return M, the events, and losses
```

Line L1 can use an [Euler tour of S and a range minimum structure](/euler-tour-lca/) over the depths of the tour; the [equivalence of LCA and RMQ](/rmq-lca-equivalence/) gives constant-time queries after linear preprocessing. Line L5 is the duplication rule for the LCA map: since $M(g)$ is the LCA of the two images, $g$ is a speciation exactly when neither image equals $M(g)$.

## Example

Species tree $((a, b), c)$, with internal nodes $ab$ and the root $r$. Gene tree $((a_1, b_1), (a_2, c_1))$, where each leaf name gives its species.

| gene node | children map to | $M$ | event | losses on its child edges |
|---|---|---|---|---|
| $(a_1, b_1)$ | $a$, $b$ | $ab$ | speciation | $0 + 0$ |
| $(a_2, c_1)$ | $a$, $c$ | $r$ | speciation | $1 + 0$ (the copy in $ab$ is lost in $b$) |
| root | $ab$, $r$ | $r$ | duplication, since $M = M(\text{right child})$ | $1 + 0$ (the copy that leads to $(a_1, b_1)$ is lost in $c$) |

So $D = 1$ and $L = 2$: a duplication before the split of $c$ from $ab$, then a loss of one copy in $b$ and of the other copy in $c$.

## Correctness

Every LCA image is at or above the images of the children, so the LCA map is valid. Any valid map $M'$ has $M'(g) \succeq M(g)$ at each node, by induction from the leaves. Take a lowest node where $M'$ differs from $M$ and move its image down to $M(g)$: the map stays valid, no duplication is created, and the number of losses drops by at least the number of levels moved. Repeating this reaches $M$, so $M$ is the unique map with fewest losses, it has the fewest duplications, and it is the unique optimum of $c_D D + c_L L$ for $c_D \ge 0$ and $c_L > 0$. The full proof is in the proof file.

## Complexity

Line L1 takes $O(m)$ time with a linear-time LCA structure, or $O(m \log m)$ with a sparse table over the Euler tour, which is what the implementation uses. The loop does $O(1)$ work per gene node, so the total is $O(n + m)$ time and $O(n + m)$ space with the linear-time structure, and $O(n + m \log m)$ time and space with the sparse table. With a walk up the species tree for each LCA instead, the time is $O(nh)$ for a species tree of height $h$.

## Properties

- The map depends only on the clusters of species below each gene node, so it is fixed by the topologies and $\sigma$, with no free choices.
- Every valid map is at or above the LCA map at each node, so the LCA map is the lowest valid map.
- Every duplication of the LCA map is also a duplication of every other valid map: these duplications are forced by the data.
- The count $D$ alone does not identify the map: other valid maps can have the same number of duplications but more losses.

## Variants and improvements

- **Non-binary species trees.** A species polytomy may be a soft one, an unresolved split. Then a gene node with both images below the same polytomy need not be a duplication, and the counts need other rules.
- **Non-binary gene trees.** Unresolved gene nodes can be resolved to minimize the cost, which is solvable in polynomial time for duplication and loss costs.
- **Unrooted gene trees.** Try each edge as the root and keep the root with the lowest cost; a single traversal can update the counts from one root to the next.
- **Transfers.** With horizontal transfers, the LCA map is no longer enough: duplication-transfer-loss reconciliation uses dynamic programming over pairs of nodes, see [horizontal gene transfer](/horizontal-gene-transfer/).
- **Probabilistic reconciliation.** Under the [duplication-loss model](/duplication-loss-model/), a reconciliation has a probability, and the most parsimonious map need not be the most likely one.

## When to use it

- To label each node of a gene tree as a duplication or speciation, and so to split a gene family into orthologs and paralogs.
- To score gene trees, or candidate species trees, by the number of duplications and losses, as in gene tree parsimony.
- As a fast first pass before a model-based reconciliation, when transfers are rare.

## Pitfalls

- **Errors in the gene tree.** One misplaced leaf can raise the image of every ancestor and create spurious duplications and many losses near the root. Low-support gene nodes should be collapsed or rearranged before counting.
- **Incomplete lineage sorting.** Discordance from [incomplete lineage sorting](/incomplete-lineage-sorting/) is explained by the LCA map as duplications and losses that never happened.
- **Missing species.** A loss count assumes that every species in the tree was sampled. A gene absent because a genome was not sequenced counts as a loss.
- **Losses above the root.** The formula counts no losses above $M(\text{root of } G)$. Some tools also count losses on the path from the species root down to it.

## Implementations

## History

Goodman and coauthors (1979) introduced the idea of fitting a gene tree into a species tree with the fewest duplications and losses, for globin genes. Page (1994) stated the LCA map as a general tool for associations between trees, for genes in species and for parasites in hosts. Zhang (1997) proved that the LCA map gives the fewest duplications and losses, and Górecki and Tiuryn (2006) developed a formal model of duplication and loss scenarios with these optimality results. Zmasek and Eddy (2001) gave a short algorithm that made the method standard in genome annotation.

## References
