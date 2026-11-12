---
tag: Q297EA
kind: problem
slug: maximum-agreement-forest
name: Maximum agreement forest
aliases:
- MAF
area: biology/phylogenetics
level: research
summary: Cut two phylogenetic trees on the same leaves into the fewest pieces on which they agree. NP-hard; its size minus one is the rSPR distance (with a root leaf) or the TBR distance.
prereqs: [maximum-agreement-subtree, rooted-and-unrooted-trees]
see_also: [rspr-maf-equivalence, spr-distance, tree-bisection-and-reconnection, subtree-prune-and-regraft, phylogenetic-network, horizontal-gene-transfer, fixed-parameter-tractable, bounded-search-tree]
sources:
  - paper: doi:10.1016/S0166-218X(96)00062-5
    title: J. Hein, T. Jiang, L. Wang and K. Zhang, On the complexity of comparing evolutionary trees, Discrete Applied Mathematics 71, 1996, 153-169
    locator: the definition of agreement forests, NP-hardness and an approximation algorithm
  - paper: doi:10.1007/s00026-001-8006-8
    title: B. L. Allen and M. Steel, Subtree transfer operations and their induced metrics on evolutionary trees, Annals of Combinatorics 5, 2001, 1-15
    locator: the theorem that TBR distance equals the unrooted maximum agreement forest size minus one, and the reductions that give a kernel
  - paper: doi:10.1007/s00026-004-0229-z
    title: M. Bordewich and C. Semple, On the computational complexity of the rooted subtree prune and regraft distance, Annals of Combinatorics 8, 2005, 409-423
    locator: the root leaf convention, rSPR distance equals the rooted maximum agreement forest size minus one, NP-hardness and the kernel
  - paper: doi:10.1137/110845045
    title: C. Whidden, R. G. Beiko and N. Zeh, Fixed-parameter algorithms for maximum agreement forests, SIAM Journal on Computing 42(4), 2013, 1431-1466
    locator: the branching rules, the O(2.42^k n) and O(3^k n) algorithms, and the linear-time 3-approximations
  - paper: "M. Bordewich, C. McCartin and C. Semple, A 3-approximation algorithm for the subtree distance between phylogenies, Journal of Discrete Algorithms 6(3), 2008"
    title: M. Bordewich, C. McCartin and C. Semple, A 3-approximation algorithm for the subtree distance between phylogenies, 2008
    locator: pp. 458 to 471, the 3-approximation for rooted maximum agreement forests
  - paper: "M. Baroni, S. Grünewald, V. Moulton and C. Semple, Bounding the number of hybridisation events for a consistent evolutionary history, Journal of Mathematical Biology 51, 2005"
    title: M. Baroni, S. Grünewald, V. Moulton and C. Semple, Bounding the number of hybridisation events for a consistent evolutionary history, 2005
    locator: pp. 171 to 182, acyclic agreement forests and the hybridization number
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 2, restrictions of trees and the rearrangement metrics
---

A maximum agreement forest of two [phylogenetic trees](/phylogenetic-tree/) on the same leaves is a partition of the leaves into as few blocks as possible, such that both trees show the same tree on each block and the parts of each tree that connect the blocks do not overlap. It is the many-piece version of the [maximum agreement subtree](/maximum-agreement-subtree/), which keeps one largest piece and drops the other leaves. For unrooted trees, the size of a maximum agreement forest minus one is the [TBR](/tree-bisection-and-reconnection/) distance (Allen and Steel 2001). For rooted trees, with an extra root leaf $\rho$, it is the rooted [SPR distance](/spr-distance/) (Bordewich and Semple 2005, see [the equivalence](/rspr-maf-equivalence/)). The problem is [NP-hard](/np-hard/) and [fixed-parameter tractable](/fixed-parameter-tractable/) in the number of cuts.

## In plain words

Draw two family trees for the same species. Now cut edges of the first tree, so that it falls into pieces. You want each piece to look the same in the second tree, and the pieces must also come from cutting the second tree. The goal is the fewest pieces.

If the trees are the same, one piece is enough. Each extra piece stands for one event that moved a group of species to a new place in the tree. So the number of pieces, less one, counts the moves that turn one tree into the other.

For rooted trees, one extra leaf is added above the root of both trees. It records where the root is, and without it the count can be too small.

## Definition

Let $X$ be a set of $n$ leaf labels. For a tree $T$ and $L \subseteq X$, the *restriction* $T|L$ is the smallest subtree that connects the leaves in $L$, with nodes of degree 2 suppressed. Write $T(L)$ for that smallest connecting subtree before suppression, as a subgraph of $T$.

**Unrooted.** Let $T_1$ and $T_2$ be unrooted binary trees on $X$. An *agreement forest* is a partition $\{L_1, \ldots, L_m\}$ of $X$ such that

1. $T_1|L_i = T_2|L_i$ as unrooted leaf-labelled trees, for every $i$, and
2. the subtrees $T_1(L_1), \ldots, T_1(L_m)$ are vertex-disjoint in $T_1$, and the subtrees $T_2(L_1), \ldots, T_2(L_m)$ are vertex-disjoint in $T_2$.

**Rooted.** Let $T_1$ and $T_2$ be rooted binary trees on $X$. Form $T^\rho$ by adding a new root whose two children are the old root and a new leaf $\rho$. A rooted agreement forest is a partition $\{L_\rho, L_1, \ldots, L_k\}$ of $X \cup \{\rho\}$ with $\rho \in L_\rho$, which meets conditions 1 and 2 for $T_1^\rho$ and $T_2^\rho$, with equality as rooted trees.

Condition 2 says that the forest is what remains of each tree after some edges are deleted, and degree-2 nodes and leafless parts are removed. An agreement forest with $m$ blocks comes from deleting exactly $m - 1$ edges of each tree.

**The problem.** Given $T_1$ and $T_2$, find an agreement forest with the least number of blocks $m(T_1, T_2)$. The decision version asks whether some agreement forest has at most $k + 1$ blocks.

## Variants

- **Rooted (rMAF).** With $\rho$. The answer gives $d_{\mathrm{rSPR}} = m - 1$.
- **Unrooted (uMAF).** No $\rho$. The answer gives $d_{\mathrm{TBR}} = m - 1$. It does not give the uSPR distance, which can be larger.
- **Maximum acyclic agreement forest.** The rooted forest must also satisfy an acyclicity condition: no block may need to sit both above and below another one in the two trees. Its size minus one is the hybridization number, the least number of reticulations in a [phylogenetic network](/phylogenetic-network/) that displays both trees (Baroni, Grünewald, Moulton and Semple 2005).
- **More than two trees.** The forest must agree with every tree in the input. It is NP-hard too, since two trees are a special case.
- **Nonbinary trees.** With multifurcations, condition 1 is usually weakened to compatibility, so that a block may be resolved in one tree and unresolved in the other.

## Examples

**Rooted, with the root leaf.** Let $T_1 = ((a,(b,c)),d)$ and $T_2 = (((a,d),b),c)$. The blocks $\{a, d\}$ and $\{b, c\}$ agree in both trees, and their connecting subtrees are disjoint in both. Without $\rho$ this gives a forest with 2 blocks. With $\rho$, one block must hold it. In $T_2^\rho$, the path from the parent of $a$ and $d$ up to $\rho$ passes through the parent of $b$ and through the old root, and $T_2(\{b, c\})$ uses both of these nodes. The block $\{b, c, \rho\}$ fails in the same way in $T_1$. A search over all cuts shows that a maximum agreement forest is

$$\{\{a\}, \{b\}, \{c, d, \rho\}\}, \qquad T_1^\rho|\{c,d,\rho\} = T_2^\rho|\{c,d,\rho\} = ((c,d),\rho).$$

So $m = 3$ and $d_{\mathrm{rSPR}}(T_1, T_2) = 2$, which a breadth-first search over the 15 rooted trees on 4 leaves confirms. Without the root, both trees are the quartet $ad \mid bc$, so the unrooted forest has one block.

**Unrooted.** Let $T_1 = ((A,B),C,(D,(E,F)))$ and $T_2 = ((A,C),B,(F,(D,E)))$. Both trees have the split $\{A, B, C\} \mid \{D, E, F\}$. Each side is a star on 3 leaves, the same in both trees. So $\{\{A, B, C\}, \{D, E, F\}\}$ is an agreement forest. The trees differ, so $m = 2$ and $d_{\mathrm{TBR}} = 1$. The uSPR distance of this pair is 2, which shows that agreement forests do not give uSPR.

## Known algorithms

| case | method | time | source |
|---|---|---|---|
| both | try every set of $k$ edges of $T_1$, check the pieces in $T_2$ | $\binom{2n}{k}$ cut sets, each checked in polynomial time | exhaustive search |
| both | subtree and chain reduction to a kernel with $O(k)$ leaves | polynomial, then exhaustive | Allen and Steel 2001; Bordewich and Semple 2005 |
| rooted | [bounded search tree](/bounded-search-tree/) on sibling pairs | $O(2.42^k n)$ | Whidden, Beiko and Zeh 2013 |
| unrooted | bounded search tree on sibling pairs | $O(3^k n)$ | Whidden, Beiko and Zeh 2013 |
| rooted | 3-approximation | polynomial | Bordewich, McCartin and Semple 2008 |
| both | 3-approximation | $O(n)$ | Whidden, Beiko and Zeh 2013 |

The branching methods work on a *sibling pair* $\{a, b\}$ of $T_1$, two leaves or pendant subtrees with the same parent. If $a$ and $b$ are also siblings in $T_2$, they are merged into one leaf. If not, some edge near them must be cut in any agreement forest, and the algorithm branches on two or three choices. Each branch cuts one edge, so the depth is at most $k$. The exhaustive search of this page's implementation tries all $\binom{2n}{k}$ cut sets of $T_1^\rho$ for $k = 0, 1, \ldots$ and checks each against $T_2^\rho$, which is enough for trees with up to about 10 leaves.

## Bounds

- **Range.** $1 \le m \le n$ unrooted, and $1 \le m \le n + 1$ rooted. The upper bounds come from singletons, plus $\{\rho\}$ in the rooted case.
- **Against agreement subtrees.** If $S$ is a maximum agreement subtree, then $S$ together with the leaves outside $S$ as singletons is an agreement forest. With $\rho$ added to the block $S$, this holds for rooted trees too. So $m \le n - |S| + 1$.
- **Unrooted against rooted.** For the same pair of trees, the unrooted size is at most the rooted size, because $d_{\mathrm{TBR}} \le d_{\mathrm{uSPR}} \le d_{\mathrm{rSPR}}$.
- **Hardness.** Both versions are NP-hard (Hein, Jiang, Wang and Zhang 1996 for unrooted; Bordewich and Semple 2005 for rooted).
- **Parameterized.** Both are fixed-parameter tractable in $k = m - 1$, with linear [kernels](/kernelization/).

## Reductions

- **rSPR distance.** $d_{\mathrm{rSPR}}(T_1, T_2) = m_\rho(T_1, T_2) - 1$. The proof of this equality is on [the equivalence page](/rspr-maf-equivalence/).
- **TBR distance.** $d_{\mathrm{TBR}}(T_1, T_2) = m(T_1, T_2) - 1$ for unrooted trees (Allen and Steel 2001).
- **Hybridization number.** Add acyclicity to the rooted problem, as in the variants.
- **Common pendant subtrees.** If a subtree on leaf set $A$ is pendant in both trees and the same in both, replace it by one new leaf in both. A maximum agreement forest of the result gives one of the same size for the input. This is the subtree reduction behind the kernels.

## Applications

- **Tree distances.** Programs that compute rSPR and TBR distances solve an agreement forest problem underneath.
- **Lateral gene transfer.** Each block of a rooted forest of a gene tree and a species tree is a group of species whose part of the gene tree can be explained without a transfer. The cuts mark candidate [transfers](/horizontal-gene-transfer/).
- **Phylogenetic networks.** Acyclic agreement forests give the least number of hybrid events for two trees and are the base of network construction methods.
- **Supertrees and consensus.** The blocks show which groups of leaves two analyses agree on, which helps to locate the conflict between them.

## References
