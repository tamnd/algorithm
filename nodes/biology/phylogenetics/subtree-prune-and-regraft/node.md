---
tag: PCRYBM
kind: technique
slug: subtree-prune-and-regraft
name: Subtree prune and regraft
aliases:
- SPR
area: biology/phylogenetics
level: advanced
summary: Tree rearrangement that cuts off a subtree and reattaches it on any edge of the rest. An unrooted binary tree on n taxa has exactly 2(n - 3)(2n - 7) SPR neighbors.
prereqs: [nearest-neighbor-interchange]
see_also: [tree-bisection-and-reconnection, spr-distance, maximum-agreement-forest, rspr-maf-equivalence, maximum-parsimony, maximum-likelihood-phylogeny, parsimony-ratchet, stepwise-addition]
sources:
  - paper: doi:10.1007/s00026-001-8006-8
    title: B. L. Allen and M. Steel, Subtree transfer operations and their induced metrics on evolutionary trees, Annals of Combinatorics 5, 2001, 1-15
    locator: Theorem 2.1, the size 2(n - 3)(2n - 7) of the SPR neighborhood of an unrooted binary tree with n leaves
  - paper: doi:10.1093/bioinformatics/btl446
    title: A. Stamatakis, RAxML-VI-HPC, maximum likelihood-based phylogenetic analyses with thousands of taxa and mixed models, Bioinformatics 22(21), 2006, 2688-2690
    locator: the lazy subtree rearrangement, SPR moves within a radius of the pruning point with local branch length optimization
  - paper: doi:10.1080/10635150390235520
    title: S. Guindon and O. Gascuel, A simple, fast, and accurate algorithm to estimate large phylogenies by maximum likelihood, Systematic Biology 52(5), 2003, 696-704
    locator: the NNI search that later SPR searches extend
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 4, Finding the best tree by heuristic search, the section on subtree pruning and regrafting
---

Subtree prune and regraft (SPR) is a move on [phylogenetic trees](/phylogenetic-tree/) that cuts one edge, takes the subtree on one side, and attaches it by its cut end to any edge of the other side. It is larger than [nearest-neighbor interchange](/nearest-neighbor-interchange/), which only slides a subtree across one vertex, and smaller than [tree bisection and reconnection](/tree-bisection-and-reconnection/), which also lets the pruned subtree reroot. An unrooted binary tree on $n \ge 4$ taxa has exactly $2(n-3)(2n-7)$ SPR neighbors, whatever its shape (Allen and Steel 2001). SPR [hill climbing](/hill-climbing/) is the main move of many parsimony and likelihood programs. The least number of SPR moves between two trees is a separate topic, the [SPR distance](/spr-distance/).

## In plain words

Think of the tree as a mobile hanging from strings. Cut one string. A part of the mobile falls off, with the cut end still on it. Now tie that cut end onto any other string of the part that is left. You get a new tree in which one group of species sits in a new place, while the group itself keeps its inner shape.

A search program tries every cut and every place to tie, scores each new tree, and moves to the best one if it is better than the current tree. A group can jump across the whole tree in one step, so the search escapes many traps that the smallest swaps cannot.

## When it applies

The model is the one of NNI: $n$ taxa with $m$ aligned sites (binary, multistate or DNA characters), unrooted binary trees, and a score to minimize, such as a parsimony length or a negative log [likelihood](/phylogenetic-likelihood/). Search over the $(2n-5)!!$ trees is a heuristic, because finding the best tree is NP-hard for [parsimony](/maximum-parsimony-np-hard/) and for [likelihood](/ml-tree-np-hard/).

SPR is the right move when NNI search stops too early and the budget allows $\Theta(n^2)$ neighbors per round instead of $\Theta(n)$. It also needs a way to score a regrafted tree without a full pass, because a round has about $4n^2$ neighbors.

## The template

A tree is an adjacency map with leaves $0, \ldots, n-1$ and internal vertices of degree 3. Cutting the edge $\{u, v\}$ next to an internal vertex $u$ prunes the subtree $S$ at $v$. The vertex $u$ is left with two neighbors $x$ and $y$, and it is suppressed: the path $x, u, y$ becomes one edge $\{x, y\}$. The regraft puts a new vertex on an edge $\{p, q\}$ of the remaining tree $R$ and joins it to $v$. The hole is SCORE, used by the hill climb exactly as in NNI-HILL-CLIMB on the [NNI page](/nearest-neighbor-interchange/).

```pseudo id=main
SPR-NEIGHBORS(T)
L1  for each internal vertex u of T and each neighbor v of u do
L2      cut the edge {u, v}; the subtree S at v is pruned
L3      suppress u: join its two other neighbors x and y by one edge
L4      for each edge {p, q} of the remaining tree R do
L5          T' ← R with a new vertex on {p, q} joined to v
L6          output T' if its topology is not T and not output before
```

There are $2(2n-3)$ ordered pairs $(u, v)$ minus the $n$ pairs with $u$ a leaf, so $3n - 6$ cuts, and for each cut fewer than $2n$ regraft edges. So the loop makes $O(n^2)$ moves. Building a tree costs $O(n)$, and the duplicate check on line L6 compares split sets at $O(n^2)$ each, for $O(n^4)$ time in this simple form. Regrafting $S$ back onto the edge $\{x, y\}$ gives $T$ again, which is why line L6 drops it.

**Scoring a regraft in $O(m)$ for Fitch parsimony.** Root $R$ on each edge in turn with a two-pass Fitch computation over $R$, in $O(nm)$ time per cut. The length of $T'$ is the length of $S$, plus the length of $R$, which does not depend on the root, plus the number of sites where the Fitch set at the root of $S$ and the Fitch set of $R$ rooted on $\{p, q\}$ are disjoint. So each regraft costs $O(m)$, and a full SPR round costs $O(n^2 m)$ in the worst case, against $O(n^3 m)$ if each neighbor is scored from scratch.

**Theorem (Allen and Steel 2001, Theorem 2.1).** For $n \ge 4$, every unrooted binary tree with $n$ labeled leaves has exactly $2(n-3)(2n-7)$ trees at SPR distance 1.

The count is the same for every shape: $2, 12, 30, 56, 90$ for $n = 4, 5, 6, 7, 8$. It contains the $2(n-3)$ NNI neighbors, since an NNI is an SPR that moves a subtree across one vertex.

A tree $T' \ne T$ is an SPR neighbor of $T$ exactly when, for some split $A \mid B$ of both trees and one leaf $b \in B$, the two trees agree on $B$ and on $A \cup \{b\}$. Here "agree on a set" means that the two trees restricted to that set are the same tree. The split is the edge that joins the pruned subtree, with leaf set $A$, to the rest. Agreement on $B$ says that the rest is unchanged, and agreement on $A \cup \{b\}$ says that the pruned subtree keeps its shape and its root; any leaf $b$ of $B$ gives the same test.

## Classic examples

**Escaping an NNI optimum.** Take six DNA sequences: A = AACCCC, B = CCCCCA, C = CACAAC, D = CACCCA, E = ACAAAA and F = CAAAAC, with the Fitch length as SCORE. The tree $((B,E),D,(A,(C,F)))$ has length 10. Its six NNI neighbors have lengths 11, 12, 12, 11, 11 and 11, so NNI search stops there. Prune the leaf E and regraft it on the pendant edge of F. The result is $((B,D),A,(C,(E,F)))$ with length 9, the unique most parsimonious tree of the 105. The two trees share no nontrivial split, so no path of fewer than 3 NNIs joins them, but one SPR does.

**Maximum likelihood search.** RAxML (Stamatakis 2006) uses lazy SPR moves: it regrafts each pruned subtree only on edges within a fixed radius of the pruning point, and it optimizes only the branches next to the new attachment before it compares likelihoods. The [likelihood](/phylogenetic-likelihood/) is computed by [Felsenstein pruning](/felsenstein-pruning/) from stored partial vectors.

**Parsimony search.** SPR rounds with the $O(m)$ regraft score above are a standard step of searches for [maximum parsimony](/maximum-parsimony/) trees, after a start tree from [stepwise addition](/stepwise-addition/).

**Rooted trees and gene transfer.** On rooted trees, an SPR moves a subtree to a new parent edge. One rooted SPR models one [horizontal gene transfer](/horizontal-gene-transfer/) or one recombination event, and the rooted SPR distance equals the size of a [maximum agreement forest](/maximum-agreement-forest/) minus 1 ([rSPR and MAF](/rspr-maf-equivalence/)).

## Variations

- **Radius limit.** Regraft only on edges within distance $r$ of the edge $\{x, y\}$. The number of moves falls from $\Theta(n^2)$ to $O(n\,2^r)$ in the worst case. With $r = 1$, the regraft edges share an end with $\{x, y\}$, and the moves are exactly the NNIs.
- **First improvement.** Accept the first better regraft, then restart the scan from the new tree.
- **Rooted SPR.** On rooted trees the edge above the root is also a regraft place, and the pruned subtree keeps its root. This is the move behind the rooted [SPR distance](/spr-distance/).
- **TBR.** [Tree bisection and reconnection](/tree-bisection-and-reconnection/) also chooses the edge of $S$ that is joined, which adds rerootings of the pruned part.

## Pitfalls

- **The trivial move.** Regrafting onto the edge that was created by suppressing $u$ gives back $T$. A search that does not drop it wastes work and may report a zero change as a move.
- **Double counts.** Different (cut, regraft) pairs often give the same tree; the $O(n^2)$ moves give only $2(n-3)(2n-7)$ distinct trees. A neighbor count based on the number of moves is wrong.
- **Branch lengths.** Under likelihood, the three branches at the new attachment point need new lengths before the score means anything.
- **The distance is not the search.** A tree at SPR distance $k$ from the optimum may still need more than $k$ hill climbing steps, or never reach it, because the climb only takes improving steps.

## Exercises

1. For $n = 5$, show that every tree has 12 SPR neighbors, so every other tree of the 15 is one SPR away except two. Which two?
2. Prove that an SPR that moves a subtree across $k$ vertices is a sequence of $k$ NNIs, and use it to bound the NNI distance by $n$ times the SPR distance.
3. Prove the regraft formula for Fitch parsimony: the length of the joined tree is the length of $S$ plus the length of $R$ plus the number of sites with disjoint root sets.
4. Write an SPR round that skips regraft edges at distance more than $r$ from the cut. How many neighbors does it produce on a caterpillar with $n$ leaves for $r = 2$?

## References
