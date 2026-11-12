---
tag: ARJW26
kind: definition
slug: quartet
name: Quartet
aliases:
- four-taxon subtree
- quartet tree
- quartet topology
area: biology/phylogenetics
level: core
summary: A split ab|cd of four taxa, the unrooted shape a tree gives to those four. An unrooted tree is determined by the quartets it displays.
prereqs: [phylogenetic-tree, splits-of-a-tree]
see_also: [rooted-triplet, four-point-condition, four-point-method, tree-comparison, quartet-max-cut, maximum-quartet-consistency, astral, split-system]
sources:
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 6 (quartets displayed by a tree and trees determined by their quartets)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 12, Quartets of species
  - paper: doi:10.1007/s00453-003-1065-y
    title: Gerth Stølting Brodal, Rolf Fagerberg and Christian N. S. Pedersen, Computing the quartet distance between evolutionary trees in time O(n log n), Algorithmica 38, 2004, 377-395
    locator: the definition of the quartet distance and the O(n log n) algorithm for binary trees
---

A quartet is a split $ab \mid cd$ of a set of four taxa: the statement that $a$ and $b$ are on one side of some edge and $c$ and $d$ on the other. Four taxa have three quartets, $ab \mid cd$, $ac \mid bd$ and $ad \mid bc$, and an unrooted binary [phylogenetic tree](/phylogenetic-tree/) displays exactly one of them on each set of four taxa. A tree is determined by the set of quartets it displays, so quartets are the smallest pieces from which an unrooted tree can be rebuilt. They are to unrooted trees what [rooted triplets](/rooted-triplet/) are to rooted trees.

## Definition

Let $X$ be a set of taxa. A *quartet* on $X$ is a split $ab \mid cd$ of a set $\{a, b, c, d\} \subseteq X$ of four distinct taxa. As with all [splits](/splits-of-a-tree/), $ab \mid cd$, $ba \mid cd$ and $cd \mid ab$ are the same quartet.

**Displayed quartets.** Let $T$ be an unrooted phylogenetic $X$-tree. $T$ *displays* the quartet $ab \mid cd$ if some edge of $T$ has $a$ and $b$ on one side and $c$ and $d$ on the other; that is, if some split $A \mid B \in \Sigma(T)$ has $a, b \in A$ and $c, d \in B$. The set of quartets that $T$ displays is $Q(T)$.

**Lemma.** These three conditions are equivalent.
1. $T$ displays $ab \mid cd$.
2. The path from $a$ to $b$ and the path from $c$ to $d$ in $T$ have no vertex in common.
3. The *restriction* $T|\{a, b, c, d\}$ (the smallest subtree that holds the four leaves, with each vertex of degree 2 suppressed) is the tree with one inner edge that separates $\{a, b\}$ from $\{c, d\}$.

*Proof.* (1 to 2) If an edge $e$ separates $\{a, b\}$ from $\{c, d\}$, the path from $a$ to $b$ stays in one subtree of $T - e$ and the path from $c$ to $d$ in the other. (2 to 1) Let $P$ be a shortest path from a vertex of the $a$ to $b$ path to a vertex of the $c$ to $d$ path. It has at least one edge, since the two paths are disjoint. Its first edge $e$ is on neither path, so after deleting $e$ the $a$ to $b$ path is still connected, and so is the $c$ to $d$ path with the rest of $P$. These are in different subtrees of $T - e$, because $T$ has only one path between any two vertices. (2 and 3) The restriction is a tree on four leaves, so it is either the star or one of the three trees with one inner edge. Restricting keeps paths and their intersections, and in the tree with inner edge $ab \mid cd$ exactly the pair of paths $a$ to $b$ and $c$ to $d$ is disjoint. $\square$

**At most one quartet per set of four.** Two different quartets on $\{a, b, c, d\}$, say $ab \mid cd$ and $ac \mid bd$, cannot both be displayed. If splits $E \mid F$ and $G \mid H$ of $T$ gave them, then $a \in E \cap G$, $b \in E \cap H$, $c \in F \cap G$ and $d \in F \cap H$, so the two splits would be incompatible, which the splits of a tree never are. So $T$ displays one quartet on $\{a, b, c, d\}$, or none, which happens when the restriction is the star. If $T$ is binary, the restriction is binary too, so $T$ displays exactly one quartet on each set of four taxa and $|Q(T)| = \binom{n}{4}$.

**Quartets and distances.** If the edges of $T$ have positive lengths and $d_T$ is the path-length metric, then $T$ displays $ab \mid cd$ exactly when
$$d_T(a, b) + d_T(c, d) < d_T(a, c) + d_T(b, d) = d_T(a, d) + d_T(b, c).$$
The difference of the two sides is twice the length of the path that joins the two disjoint paths. This is the [four-point condition](/four-point-condition/), and it is how distance methods such as the [four-point method](/four-point-method/) infer quartets from data.

### Trees are determined by their quartets

**Theorem.** Let $T$ be an unrooted phylogenetic $X$-tree and $A \mid B$ an $X$-split with $|A| \ge 2$ and $|B| \ge 2$. Then $A \mid B \in \Sigma(T)$ if and only if $T$ displays $aa' \mid bb'$ for all distinct $a, a' \in A$ and all distinct $b, b' \in B$. So $Q(T)$ determines $\Sigma(T)$, and by the [splits-equivalence theorem](/splits-of-a-tree/) it determines $T$: two phylogenetic $X$-trees with the same quartets are equal.

*Proof.* If the edge $e$ gives $A \mid B$, then $e$ separates $\{a, a'\}$ from $\{b, b'\}$ for every choice, so $T$ displays $aa' \mid bb'$.

Conversely, assume that $T$ displays all the quartets $aa' \mid bb'$. Let $U$ be the union of the paths between pairs of taxa of $A$, and $W$ the same for $B$. These are subtrees of $T$. Suppose $U$ and $W$ share a vertex $v$. Then $v$ lies on the path between some distinct $a, a' \in A$ and on the path between some distinct $b, b' \in B$, so these paths meet, and by the lemma $T$ does not display $aa' \mid bb'$. This contradicts the assumption, so $U$ and $W$ are disjoint. Let $e$ be the first edge of a shortest path from $U$ to $W$. As in the lemma, deleting $e$ leaves $U$ on one side and $W$ on the other. Each taxon is in $A \subseteq U$ or $B \subseteq W$, so the split of $e$ is exactly $A \mid B$. $\square$

The trivial splits are in $\Sigma(T)$ for every tree, and a split with $|A| \ge 2$ and $|B| \ge 2$ is tested by the theorem, so $\Sigma(T)$ is fixed by $Q(T)$. For a binary tree a much smaller set is enough. An inner edge $e$ has two other edges at each end, and these lead to four subtrees; pick one taxon from each, $a, a'$ from the two subtrees at one end and $b, b'$ from the two at the other. The $n - 3$ quartets $aa' \mid bb'$, one for each inner edge, are displayed by no other tree on $X$.

**Not every set of quartets comes from a tree.** Pick one quartet for each set of four taxa. A tree that displays all of them may not exist: on five taxa, the choices $ab \mid cd$, $ac \mid be$ and $ae \mid bd$ (and any choices for the other two sets) are not displayed together by any tree. For the full set, with one quartet for each set of four, whether a tree exists can be decided in polynomial time. For a partial set the question is NP-complete (Steel, 1992), and finding a tree that displays the most quartets of a set is the problem of [maximum quartet consistency](/maximum-quartet-consistency/), with heuristics such as [Quartet MaxCut](/quartet-max-cut/).

## Examples and non-examples

**A binary tree on six taxa.** The tree `(((A,B),C),(D,(E,F)));` has the nontrivial splits $AB \mid CDEF$, $ABC \mid DEF$ and $ABCD \mid EF$, and it displays $\binom{6}{4} = 15$ quartets, one for each set of four taxa. For example:

| taxa | quartet | the split that gives it |
|---|---|---|
| $A, B, C, D$ | $AB \mid CD$ | $AB \mid CDEF$ |
| $A, C, D, E$ | $AC \mid DE$ | $ABC \mid DEF$ |
| $B, C, E, F$ | $BC \mid EF$ | $ABC \mid DEF$ or $ABCD \mid EF$ |
| $A, B, E, F$ | $AB \mid EF$ | any of the three |

For $A, C, D, E$ the split $AB \mid CDEF$ puts only $A$ on its first side, so it gives the trivial split $A \mid CDE$ of the four taxa and no quartet; the split $ABC \mid DEF$ gives $AC \mid DE$.

**A tree with a polytomy.** The tree `((A,B),C,D,E);` has one inner edge, with split $AB \mid CDE$, and one vertex of degree 4. It displays $AB \mid CD$, $AB \mid CE$ and $AB \mid DE$, but on $\{A, C, D, E\}$ and on $\{B, C, D, E\}$ it displays no quartet: the restriction is the star. So $|Q(T)| = 3 < \binom{5}{4} = 5$.

**Quartets from distances.** In a tree with the quartet $ab \mid cd$, leaf edges of length 1 and an inner edge of length 2, the distances are $d(a, b) = d(c, d) = 2$ and $d(a, c) = d(a, d) = d(b, c) = d(b, d) = 4$. The three sums are $2 + 2 = 4$ for $ab \mid cd$ and $4 + 4 = 8$ for the other two, so the smallest sum picks $ab \mid cd$, and the gap $8 - 4 = 4$ is twice the inner edge.

**Non-example: the star.** The star on $\{a, b, c, d\}$ displays no quartet. It is still a phylogenetic tree, and its quartet set, the empty set, determines it among the trees on four taxa.

**Non-example: a rooted statement.** "$a$ and $b$ are sister taxa" is not a quartet. It depends on the root, and it is the [rooted triplet](/rooted-triplet/) $ab \mid c$ for each other taxon $c$. The quartet $ab \mid cd$ holds for both rootings $((a,b),(c,d))$ and $(c,(d,(a,b)))$, but $a, b$ are not sisters in the rooting $(a,(b,(c,d)))$, which also displays $ab \mid cd$.

## Related definitions

- [Splits of a tree](/splits-of-a-tree/) give the quartets: each split $A \mid B$ gives all $aa' \mid bb'$ with $a, a' \in A$ and $b, b' \in B$.
- A [rooted triplet](/rooted-triplet/) is the three-taxon piece of a rooted tree, and adding a leaf at the root turns each triplet $ab \mid c$ into the quartet $ab \mid c\rho$.
- The *quartet distance* between two trees counts the sets of four taxa on which they display different quartets. It is computed in $O(n \log n)$ time for binary trees (Brodal, Fagerberg and Pedersen, 2004); see [tree comparison](/tree-comparison/).
- Quartet-based methods build a tree from quartets inferred one set of four at a time: [Quartet MaxCut](/quartet-max-cut/) for the combination, and [ASTRAL](/astral/) for species trees from gene trees, where under the multispecies coalescent the most frequent quartet of four species is the species tree's quartet.

## References
