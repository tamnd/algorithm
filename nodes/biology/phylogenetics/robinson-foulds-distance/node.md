---
tag: 1D4SCP
kind: definition
slug: robinson-foulds-distance
name: Robinson-Foulds distance
aliases:
- RF distance
- symmetric difference distance
- partition distance
area: biology/phylogenetics
level: core
summary: The number of splits that are in exactly one of two phylogenetic trees on the same taxa. It is a metric, at most 2(n-3) for binary trees, and computable in linear time.
prereqs: [splits-of-a-tree]
see_also: [day-algorithm, tree-comparison, nearest-neighbor-interchange, spr-distance, maximum-agreement-subtree, consensus-tree, quartet]
sources:
  - paper: doi:10.1016/0025-5564(81)90043-2
    title: D. F. Robinson and L. R. Foulds, Comparison of phylogenetic trees, Mathematical Biosciences 53(1-2), 1981, 131-147
    locator: the distance as the size of the symmetric difference of the two sets of partitions given by the edges
  - paper: doi:10.1007/BF01908061
    title: William H. E. Day, Optimal algorithms for comparing trees with labeled leaves, Journal of Classification 2(1), 1985, 7-28
    locator: the linear-time computation of the distance with a cluster table
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 30, Consensus trees and distances between trees (the symmetric difference distance and its relatives)
---

The Robinson-Foulds distance between two [phylogenetic trees](/phylogenetic-tree/) on the same taxa is the number of [splits](/splits-of-a-tree/) that are in one tree but not the other. It is zero exactly when the trees are equal, it is a metric, and for binary trees on $n$ taxa it is an even number between 0 and $2(n-3)$. It is the most used distance between trees because it is easy to explain and [Day's algorithm](/day-algorithm/) computes it in $O(n)$ time. Some authors and programs report half of this number, so a value of RF must always come with its convention.

## Definition

Let $T_1$ and $T_2$ be unrooted phylogenetic trees on the same set $X$ of $n$ taxa, with split sets $\Sigma(T_1)$ and $\Sigma(T_2)$. The *Robinson-Foulds distance* is the size of the symmetric difference of the split sets:
$$d_{RF}(T_1, T_2) = |\Sigma(T_1) \,\triangle\, \Sigma(T_2)| = |\Sigma(T_1) \setminus \Sigma(T_2)| + |\Sigma(T_2) \setminus \Sigma(T_1)|.$$
Both trees have all $n$ trivial splits, so they cancel, and the same number comes from the nontrivial splits alone. If $s$ is the number of shared nontrivial splits and $c_1, c_2$ are the numbers of nontrivial splits of the two trees, then
$$d_{RF}(T_1, T_2) = (c_1 - s) + (c_2 - s).$$

**Conventions.** This page uses the full symmetric difference, as in Robinson and Foulds (1981) and in Day (1985). Some authors and programs report half of it, $\frac{1}{2} d_{RF}$; for binary trees this half is $n - 3 - s$, the number of splits of one tree missing from the other. The *normalized* distance divides by the largest possible value, $c_1 + c_2$, or $2(n-3)$ for binary trees, to give a number between 0 and 1.

**Rooted trees.** For rooted trees the same definition is used with clusters in place of splits: $d_{RF}$ counts the clusters that are in exactly one of the two trees. The rooted and the unrooted distances of the same pair of trees can differ, because moving the root changes the clusters.

### Properties

1. **It is a metric on the trees on $X$.** The symmetric difference is a metric on finite sets: $|P \triangle R| \le |P \triangle Q| + |Q \triangle R|$, because $P \triangle R \subseteq (P \triangle Q) \cup (Q \triangle R)$. By the splits-equivalence theorem, $\Sigma(T_1) = \Sigma(T_2)$ only when $T_1 = T_2$, so $d_{RF}(T_1, T_2) = 0$ only for equal trees.
2. **Range.** A tree on $n \ge 3$ taxa has at most $n - 3$ nontrivial splits, so $d_{RF} \le 2(n - 3)$. Two binary trees both have exactly $n - 3$ nontrivial splits, so $d_{RF} = 2(n - 3 - s)$ is even.
3. **The maximum is reached.** For each $n \ge 4$ there are binary trees with no common nontrivial split, so the bound $2(n-3)$ is reached. The caterpillar on $a_1, a_2, \ldots, a_n$ has the clusters $\{a_1, \ldots, a_k\}$ for $2 \le k \le n - 2$, and the caterpillar on $a_2, \ldots, a_n, a_1$ has the clusters $\{a_2, \ldots, a_{k+1}\}$. A cluster of the first kind holds $a_1$ but not $a_n$; a cluster of the second kind, and its complement, does not. The example below is the case $n = 6$.
4. **Bound by NNI.** A [nearest neighbor interchange](/nearest-neighbor-interchange/) removes one nontrivial split of a binary tree and adds one, so it changes $d_{RF}$ by at most 2. Hence $d_{RF}(T_1, T_2) \le 2\, d_{NNI}(T_1, T_2)$, where $d_{NNI}$ is the least number of NNI moves from $T_1$ to $T_2$.
5. **No such bound by SPR.** One [subtree prune and regraft](/subtree-prune-and-regraft/) move can change all $n - 3$ nontrivial splits, so $d_{RF}$ can be at its maximum while the [SPR distance](/spr-distance/) is 1.

**Computation.** With each split stored as a bit mask of the side that does not hold a fixed taxon $r$, put the masks of $T_1$ in a hash set and look up the masks of $T_2$. The masks have $n$ bits, so this takes $O(n^2 / w)$ time on a machine with $w$-bit words, plus the hashing. [Day's algorithm](/day-algorithm/) avoids the bit masks: it numbers the leaves so that each cluster of $T_1$ is an interval, and it reaches $O(n)$ time, which is optimal since the input has size $\Theta(n)$.

## Examples and non-examples

**One NNI apart.** Let $T_1 = (((A,B),C),(D,(E,F)))$ and $T_2 = (((A,C),B),(D,(E,F)))$, read as unrooted binary trees on six taxa. Their nontrivial splits are:

| $T_1$ | $T_2$ |
|---|---|
| $AB \mid CDEF$ | $AC \mid BDEF$ |
| $ABC \mid DEF$ | $ABC \mid DEF$ |
| $ABCD \mid EF$ | $ABCD \mid EF$ |

Two splits are shared and one split of each tree is not, so $d_{RF} = 1 + 1 = 2$, the half distance is 1, and the normalized distance is $2/6 = 1/3$. The trees are one NNI apart (swap $B$ and $C$ across the edge of $ABC \mid DEF$), and the bound $d_{RF} \le 2\, d_{NNI}$ holds with equality.

**The maximum, from one leaf.** Let $T_1$ be the caterpillar $(A,(B,(C,(D,(E,F)))))$ and $T_2$ the caterpillar $(B,(C,(D,(E,(F,A)))))$. Their nontrivial splits are $AB \mid CDEF$, $ABC \mid DEF$, $ABCD \mid EF$ and $BC \mid DEFA$, $BCD \mid EFA$, $BCDE \mid FA$. None is shared, so $d_{RF} = 6 = 2(6 - 3)$, the largest value for six taxa. Yet $T_2$ is $T_1$ with only the leaf $A$ moved from one end to the other: one SPR move, and the two trees agree on the five taxa $B, \ldots, F$. RF reads this one move as a complete disagreement.

**A star.** If $T_2$ is the star on $X$, then $d_{RF}(T_1, T_2) = c_1$, the number of nontrivial splits of $T_1$, for every $T_1$. A tree with no resolution is close to all trees, so a small distance to a poorly resolved tree does not mean agreement.

**Non-example: different taxon sets.** The distance is not defined for trees on different sets of taxa: a split of $\{A, B, C, D, E\}$ is not a split of $\{A, B, C, D\}$. To compare such trees, restrict both to the shared taxa first, which removes the leaves that are not shared and suppresses the vertices of degree 2.

## Related definitions

- [Splits of a tree](/splits-of-a-tree/) are the objects that RF counts, and [Day's algorithm](/day-algorithm/) computes RF in linear time.
- [Tree comparison](/tree-comparison/) gives the other distances: the quartet and triplet distances, the [SPR distance](/spr-distance/) and TBR distance, and the [maximum agreement subtree](/maximum-agreement-subtree/). These react less strongly to the move of one leaf.
- The *weighted* RF distance adds, over all splits, the absolute difference of the branch lengths of the split in the two trees, with length 0 for a missing split. The branch score distance of Kuhner and Felsenstein (1994) uses the squares of these differences.
- The majority-rule [consensus tree](/consensus-tree/) is a median tree for RF: no tree on $X$ has a smaller sum of RF distances to the input trees (Barthélemy and McMorris, 1986).

## References
