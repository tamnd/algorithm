---
tag: 57633W
kind: technique
slug: nearest-neighbor-interchange
name: Nearest-neighbor interchange
aliases:
- NNI
area: biology/phylogenetics
level: core
summary: Tree rearrangement that swaps two subtrees across an internal edge. Each unrooted binary tree on n taxa has exactly 2(n - 3) NNI neighbors.
prereqs: [phylogenetic-tree, rooted-and-unrooted-trees, local-search]
see_also: [subtree-prune-and-regraft, tree-bisection-and-reconnection, splits-of-a-tree, robinson-foulds-distance, maximum-parsimony, maximum-likelihood-phylogeny, minimum-evolution, tree-rotation]
sources:
  - paper: doi:10.1016/0095-8956(71)90020-7
    title: D. F. Robinson, Comparison of labeled trees with valency three, Journal of Combinatorial Theory, Series B 11(2), 1971, 105-119
    locator: the nearest neighbour interchange on trees whose internal vertices have valency three, and the count of 2n - 6 neighbours
  - paper: doi:10.1016/0022-5193(73)90251-8
    title: G. W. Moore, M. Goodman and J. Barnabas, An iterative approach from the standpoint of the additive hypothesis to the dendrogram problem posed by molecular data sets, Journal of Theoretical Biology 38(3), 1973, 423-457
    locator: the local exchange of subtrees across an internal edge as a step of an iterative tree search
  - paper: "B. DasGupta, X. He, T. Jiang, M. Li, J. Tromp and L. Zhang, On computing the nearest neighbor interchange distance, in Discrete Mathematical Problems with Medical Applications, DIMACS Series in Discrete Mathematics and Theoretical Computer Science 55, AMS, 2000"
    title: DasGupta, He, Jiang, Li, Tromp and Zhang 2000
    locator: the NP-hardness of the NNI distance between unlabeled and labeled trees, and an O(log n) approximation
  - paper: doi:10.1006/jtbi.1996.0188
    title: M. Li, J. Tromp and L. Zhang, On the nearest neighbour interchange distance between evolutionary trees, Journal of Theoretical Biology 182(4), 1996, 463-467
    locator: the upper bound of order n log n on the NNI distance
  - paper: doi:10.1080/10635150390235520
    title: S. Guindon and O. Gascuel, A simple, fast, and accurate algorithm to estimate large phylogenies by maximum likelihood, Systematic Biology 52(5), 2003, 696-704
    locator: NNI moves evaluated with local branch length optimization in a maximum likelihood search (PhyML)
  - paper: doi:10.1089/106652702761034136
    title: R. Desper and O. Gascuel, Fast and accurate phylogeny reconstruction algorithms based on the minimum-evolution principle, Journal of Computational Biology 9(5), 2002, 687-705
    locator: the NNI searches under the ordinary and balanced minimum evolution length (FastME)
  - paper: doi:10.1093/molbev/msu300
    title: L.-T. Nguyen, H. A. Schmidt, A. von Haeseler and B. Q. Minh, IQ-TREE, a fast and effective stochastic algorithm for estimating maximum-likelihood phylogenies, Molecular Biology and Evolution 32(1), 2015, 268-274
    locator: the perturbation of candidate trees by random NNIs followed by hill climbing
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 4, Finding the best tree by heuristic search, the section on nearest-neighbor interchanges
---

Nearest-neighbor interchange (NNI) is the smallest move in the search for a good [phylogenetic tree](/phylogenetic-tree/). Pick an internal edge of an unrooted binary tree. It has four subtrees hanging from its two ends, two on each side, and the move swaps one subtree of one side with one subtree of the other side. Each internal edge gives two new trees, so a tree on $n$ taxa has exactly $2(n-3)$ NNI neighbors (Robinson 1971). A [local search](/local-search/) that moves to a better neighbor until none is better is the simplest heuristic for [maximum parsimony](/maximum-parsimony/), [maximum likelihood](/maximum-likelihood-phylogeny/) and [minimum evolution](/minimum-evolution/), all of which search a space of $(2n-5)!!$ trees.

## In plain words

Picture a tree drawn on paper with the species at the tips. Choose one inner branch. At each end of it, two groups of species hang off. Take one group from the left end and one group from the right end, and swap them. Everything else stays where it was. There are two ways to do this for each inner branch.

This is the smallest change that gives a different tree. A search program starts from some tree, tries every such swap, keeps the best new tree if it scores better, and repeats. It stops when no swap helps. The result is good locally, but a better tree may need several swaps in a row that each look worse, and the search cannot see it.

## When it applies

The model is a set of $n \ge 4$ taxa, each with a sequence of $m$ aligned sites (binary, multistate or DNA characters), and the trees are unrooted and binary: every internal vertex has degree 3. Such a tree has $n - 2$ internal vertices, $2n - 3$ edges and $n - 3$ internal edges. The number of trees is $(2n-5)!! = 1 \cdot 3 \cdot 5 \cdots (2n-5)$, which is $2027025$ for $n = 10$ and about $2.2 \times 10^{20}$ for $n = 20$, so exhaustive search stops at about a dozen taxa.

NNI needs three things.

- **An objective on trees.** A score to minimize, such as the parsimony length from [Fitch's algorithm](/fitch-algorithm/), the negative log [likelihood](/phylogenetic-likelihood/), or a least squares or minimum evolution length.
- **A start tree.** Often from [stepwise addition](/stepwise-addition/) or [neighbor joining](/neighbor-joining/).
- **A cheap neighbor score.** An NNI changes the tree only around one edge, so an implementation can rescore a neighbor from stored partial results of the rest of the tree.

Finding the best tree is NP-hard for parsimony ([Foulds and Graham](/maximum-parsimony-np-hard/)) and for likelihood ([Chor and Tuller](/ml-tree-np-hard/)). NNI search is a heuristic: it returns a tree that no NNI improves, with no bound on how far that tree is from the optimum.

## The template

A tree is stored as an adjacency map with leaves $0, \ldots, n-1$. For an internal edge $\{u, v\}$, let $a, b$ be the other neighbors of $u$ and $c, d$ the other neighbors of $v$. The tree has the split $A \cup B \mid C \cup D$ on this edge, where $A, B, C, D$ are the leaf sets of the subtrees at $a, b, c, d$. The two neighbors exchange $b$ with $c$ (giving $A \cup C \mid B \cup D$) or $b$ with $d$ (giving $A \cup D \mid B \cup C$). The hole is SCORE, the objective.

```pseudo id=main
NNI-NEIGHBORS(T)
L1  for each internal edge {u, v} of T do
L2      let a, b be the other neighbors of u, and c, d the other neighbors of v
L3      for each x in {c, d} do
L4          T' ← a copy of T without the edges {u, b} and {v, x}
L5          add the edges {u, x} and {v, b} to T'
L6          output T'
NNI-HILL-CLIMB(T, SCORE)
L7  best ← T
L8  loop
L9      compute SCORE(T') for each T' in NNI-NEIGHBORS(best)
L10     let T* be a neighbor of least score, if that score is below SCORE(best)
L11     if there is no such T* then
L12         return best
L13     best ← T*
```

Lines L1 to L6 build each neighbor in $O(n)$ time for the copy, so all $2(n-3)$ neighbors cost $O(n^2)$. With a Fitch score computed from scratch at $O(nm)$ per tree, one round of L9 costs $O(n^2 m)$ in the worst case. A parsimony length is an integer and drops by at least 1 per round, so the loop runs at most $L(T) - L^*$ rounds, where $L^*$ is the optimal length. For a likelihood score, a round must improve by more than a fixed tolerance for the same argument to apply.

**Theorem (Robinson 1971).** Let $T$ be an unrooted binary tree on $n \ge 3$ labeled leaves. The $2(n-3)$ trees built by NNI-NEIGHBORS are pairwise different and different from $T$. A binary tree $T'$ on the same leaves is one of them exactly when the split sets $\Sigma(T)$ and $\Sigma(T')$ differ in one split each: $|\Sigma(T) \,\triangle\, \Sigma(T')| = 2$.

*Proof.* Use two facts about [splits](/splits-of-a-tree/): the splits of a tree are pairwise compatible, and a tree is fixed by its set of splits.

*The move changes one split.* Take the move on edge $e = \{u, v\}$ that swaps $b$ and $c$. The four subtrees keep their inner edges, and the edges from $u$ or $v$ into them still cut off $A$, $B$, $C$ and $D$. Every other edge of $T$ lies inside one of the four subtrees. So all splits stay, except the split $A \cup B \mid C \cup D$ of $e$, which becomes $A \cup C \mid B \cup D$. The four sets $A, B, C, D$ are not empty, so $A \cup C \mid B \cup D$ is not compatible with $A \cup B \mid C \cup D$, and it is not a split of $T$. The symmetric difference is therefore exactly these two splits.

*All neighbors are different.* Two moves on different edges remove different splits of $T$, because two edges of a tree have different splits. The two moves on one edge add $A \cup C \mid B \cup D$ and $A \cup D \mid B \cup C$, which are different. So the $2(n-3)$ split sets are pairwise different, and none of them is $\Sigma(T)$.

*The converse.* Let $\Sigma(T) = X \cup \{S\}$ and $\Sigma(T') = X \cup \{S'\}$ with $S \ne S'$. Contract the edge of $S$ in $T$ and the edge of $S'$ in $T'$. Both results have the split set $X$, so they are the same tree $T_0$. $T_0$ has one vertex of degree 4, with four subtrees on leaf sets $A, B, C, D$, and its binary resolutions are the three trees with the extra split $AB|CD$, $AC|BD$ or $AD|BC$. $T$ and $T'$ are two different resolutions, and the move on the edge of $S$ in $T$ makes the other two. $\blacksquare$

So the NNI neighbors of $T$ are exactly the trees at [Robinson-Foulds distance](/robinson-foulds-distance/) 2, when that distance counts the size of the symmetric difference.

## Classic examples

**Parsimony on five taxa.** Take the DNA sequences A = AAGTC, B = AAGTT, C = ACGCA, D = GCACA and E = GCATA, and the Fitch length as SCORE. Over the 15 trees the lengths are 7 once, 8 three times, 9 three times and 10 eight times. Write a five-taxon tree as $((x, y), z, (w, t))$, with the cherry $(x, y)$, the middle taxon $z$ and the cherry $(w, t)$.

| round | tree | length | lengths of its 4 neighbors |
|---|---|---|---|
| 0 | ((A,D),C,(B,E)) | 10 | 10, 9, 10, 10 |
| 1 | ((B,E),A,(C,D)) | 9 | 10, 10, 8, 9 |
| 2 | ((A,B),E,(C,D)) | 8 | 9, 7, 9, 9 |
| 3 | ((A,B),C,(D,E)) | 7 | 8, 8, 8, 9 |

Each step keeps one cherry and replaces the other: AD becomes CD, then BE becomes AB, then CD becomes DE. The last tree is the unique most parsimonious tree, and on this data it is the only tree that no NNI improves, so the climb finds it from every start.

**Maximum likelihood.** PhyML (Guindon and Gascuel 2003) starts from a distance tree and applies NNIs under a [likelihood](/phylogenetic-likelihood/) score. For each internal edge it scores the two neighbors with only a local optimization of branch lengths at that edge, and it applies many improving NNIs in one round. The score is the [Felsenstein pruning](/felsenstein-pruning/) likelihood under a [substitution model](/substitution-model/).

**Minimum evolution.** FastME (Desper and Gascuel 2002) improves a start tree by NNIs under the balanced minimum evolution length. It gets the change of the length for each candidate NNI from a table of average distances between subtrees, without a new pass over the whole tree. See [minimum evolution](/minimum-evolution/).

**MCMC proposals.** A [Bayesian](/bayesian-phylogenetic-inference/) sampler can propose a random NNI as its topology move. The move is symmetric, because the reverse NNI on the same edge has the same probability, which keeps the [Metropolis-Hastings](/metropolis-hastings/) ratio simple.

## Variations

- **Rooted NNI.** On a rooted binary tree with $n$ leaves, an internal edge below the root has a child subtree pair at its lower end and a sibling subtree at its upper end. Swapping the sibling with either child gives 2 neighbors, so there are $2(n-2)$ neighbors. On ordered trees with a fixed left to right order this is a [tree rotation](/tree-rotation/), but rotations keep the in-order sequence and NNI does not.
- **First improvement.** Move to the first better neighbor instead of the best one. Each round is cheaper, and the path may end at a different local optimum.
- **Larger moves.** [Subtree prune and regraft](/subtree-prune-and-regraft/) moves a subtree anywhere, and [tree bisection and reconnection](/tree-bisection-and-reconnection/) also reroots it. Every NNI is an SPR and every SPR is a TBR.
- **Perturbation.** Some ML programs, such as IQ-TREE, apply random NNIs to the best tree found so far and restart the hill climb from the result, a form of [iterated local search](/iterated-local-search/).
- **NNI distance.** The least number of NNIs that turns one tree into another is NP-hard to compute (DasGupta et al. 2000), and it is $O(n \log n)$ for any two trees on $n$ taxa (Li, Tromp and Zhang 1996). The distance used for search spaces in practice is the [SPR distance](/spr-distance/) or the [Robinson-Foulds distance](/robinson-foulds-distance/).

## Pitfalls

- **Local optima.** NNI moves are small, and a tree with no better NNI neighbor can be far from the best tree. The [SPR page](/subtree-prune-and-regraft/) gives a six-taxon data set with a strict NNI local optimum at length 10 when the best tree has length 9. Use several start trees, SPR or TBR moves, or the [parsimony ratchet](/parsimony-ratchet/).
- **Ties.** Parsimony scores tie often. A climb that accepts only strict improvement stops on a plateau; one that accepts ties needs a rule against cycling, such as a tabu list.
- **Branch lengths.** For likelihood, a neighbor with stale branch lengths can look worse than it is. Optimize at least the branches around the changed edge before the comparison.
- **The count assumes binary trees.** A vertex of degree more than 3 has more than two ways to regroup its subtrees, and the formula $2(n-3)$ does not hold.

## Exercises

1. For $n = 4$, draw the three unrooted trees and show that each is an NNI neighbor of the other two.
2. List the two NNI neighbors of $((A,B),C,(D,E))$ across the edge with split $AB \mid CDE$, and give the split that each one gains.
3. Prove the rooted count $2(n-2)$ for rooted binary trees with $n \ge 2$ leaves.
4. Show that moving the attachment point of a subtree across one vertex is one NNI. Deduce that an SPR move that moves a subtree across $k$ vertices is a sequence of $k$ NNIs.
5. Show that the number of NNI neighbors does not depend on the shape of the tree, and compare with the TBR neighborhood, whose size does.

## References
