---
tag: S23RH6
kind: technique
slug: tree-bisection-and-reconnection
name: Tree bisection and reconnection
aliases:
- TBR
area: biology/phylogenetics
level: advanced
summary: Tree rearrangement that cuts one edge and joins the two parts again by a new edge between any edge of one part and any edge of the other. It contains every SPR and NNI move.
prereqs: [subtree-prune-and-regraft]
see_also: [nearest-neighbor-interchange, maximum-agreement-forest, spr-distance, parsimony-ratchet, maximum-parsimony, splits-of-a-tree, stepwise-addition, local-search]
sources:
  - paper: doi:10.1007/s00026-001-8006-8
    title: B. L. Allen and M. Steel, Subtree transfer operations and their induced metrics on evolutionary trees, Annals of Combinatorics 5, 2001, 1-15
    locator: the upper bound (2n - 3)(n - 3)^2 on the TBR neighborhood, and the TBR distance as the size of a maximum agreement forest minus one
  - paper: doi:10.1109/TCBB.2013.66
    title: P. J. Humphries and T. Wu, On the neighborhoods of trees, IEEE/ACM Transactions on Computational Biology and Bioinformatics 10(3), 2013, 721-728
    locator: Theorem 3.6, the exact size 4 Γ(T) - (4n - 2)(n - 3) of the TBR neighborhood; Corollary 4.2, the maximum, reached exactly by caterpillars
  - paper: doi:10.1111/j.1096-0031.1999.tb00277.x
    title: Kevin C. Nixon, The parsimony ratchet, a new method for rapid parsimony analysis, Cladistics 15(4), 1999, 407-414
    locator: TBR branch swapping as the search inside each ratchet iteration
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 4, Finding the best tree by heuristic search, the section on tree bisection and reconnection
---

Tree bisection and reconnection (TBR) is a move on unrooted binary [phylogenetic trees](/phylogenetic-tree/). It cuts one edge, which splits the tree into two parts, and then joins the parts again by a new edge from any edge of the first part to any edge of the second. It is the largest of the three standard moves: every [NNI](/nearest-neighbor-interchange/) and every [SPR](/subtree-prune-and-regraft/) is a TBR, and TBR adds the moves that also reroot the cut part. Unlike the NNI and SPR counts, the number of TBR neighbors depends on the shape of the tree. It is $4\Gamma(T) - (4n-2)(n-3)$, where $\Gamma(T)$ sums $|A|\,|B|$ over the nontrivial splits $A \mid B$ of $T$ (Humphries and Wu 2013). TBR is the default swap of large [parsimony](/maximum-parsimony/) searches and the inner search of the [parsimony ratchet](/parsimony-ratchet/).

## In plain words

Cut one branch of the tree, so that it falls into two pieces. Each piece is a smaller tree. Now pick any branch of the first piece and any branch of the second piece, and tie them together with a new branch. If a piece is a single species, tie at that species.

A prune and regraft move keeps the cut end of the moved piece as the place where it is tied back. This move does not: the moved piece can be tied by any of its own branches, so it can turn around as well as move. That gives many more new trees per step, and a search that uses it gets stuck less often, at a higher cost per step.

## When it applies

The model is the one of the other tree moves: $n \ge 4$ taxa with $m$ aligned sites (binary, multistate or DNA characters), unrooted binary trees, and a score to minimize, usually a [parsimony](/maximum-parsimony/) length. Search over the $(2n-5)!!$ trees is a heuristic: maximum parsimony is [NP-hard](/maximum-parsimony-np-hard/), and a TBR local optimum need not be a global one.

TBR pays off when the score of a joined tree is cheap. For Fitch parsimony, the length of the tree made by joining part $P$ at edge $e$ to part $Q$ at edge $f$ is the length of $P$, plus the length of $Q$, plus the number of sites where the Fitch set of $P$ rooted on $e$ and the Fitch set of $Q$ rooted on $f$ are disjoint. With the root sets of all edges of both parts computed once per cut, in $O(nm)$ time, each of the $O(n^2)$ reconnections of the cut costs $O(m)$.

## The template

A tree is an adjacency map with leaves $0, \ldots, n-1$. Cutting the edge $\{u, v\}$ leaves the part $T_u$ that holds $u$ and the part $T_v$ that holds $v$. If $u$ is internal, it has degree 2 in $T_u$ and is suppressed, so that $T_u$ is binary again. The places of a part are its edges, or the one vertex of a part that is a single leaf. The hole is SCORE, used in a hill climb as on the [NNI page](/nearest-neighbor-interchange/).

```pseudo id=main
TBR-NEIGHBORS(T)
L1  for each edge {u, v} of T do
L2      cut {u, v} into the part T_u that holds u and the part T_v that holds v
L3      suppress u in T_u and v in T_v, and list the places of each part
L4      for each place a of T_u and each place b of T_v do
L5          T' ← T_u and T_v with a new vertex on a joined to a new vertex on b
L6          output T' if its topology is not T and not output before
```

A part with $k \ge 2$ leaves has $2k - 3$ places. The cut of a split $A \mid B$ with $|A| = k$ gives at most $(2k - 3)(2(n-k) - 3)$ joins, so a round makes $O(n^3)$ moves. Joining the two places that came from the suppressed vertices gives back $T$, which line L6 drops. This simple form builds each tree in $O(n)$ and checks duplicates by split sets in $O(n^2)$, for $O(n^5)$ time per round.

**Which trees are neighbors.** $T' \ne T$ is a TBR neighbor of $T$ exactly when some split $A \mid B$ belongs to both trees, and the two trees restricted to $A$ agree, and the two trees restricted to $B$ agree. The kept split is the new edge. The move is an SPR exactly when, in addition, the two trees agree on $A \cup \{b\}$ for a leaf $b$ of $B$, or on $B \cup \{a\}$ for a leaf $a$ of $A$: then one of the two parts keeps its root.

**Theorem (Humphries and Wu 2013, Theorem 3.6).** For an unrooted binary tree $T$ with $n \ge 4$ leaves,
$$|N_{\mathrm{TBR}}(T)| = 4\,\Gamma(T) - (4n-2)(n-3), \qquad \Gamma(T) = \sum_{A \mid B \in \Sigma(T),\ |A|, |B| \ge 2} |A|\,|B|.$$

**Bounds.** Allen and Steel (2001) proved $|N_{\mathrm{TBR}}(T)| \le (2n-3)(n-3)^2$. Humphries and Wu (Corollary 4.2) show that the maximum over trees with $n$ leaves is $\frac{2}{3}n^3 - 4n^2 + \frac{16}{3}n + 2$, reached exactly by the caterpillars, the trees whose internal vertices lie on one path. The neighborhood of a caterpillar grows as $\Theta(n^3)$, and Humphries and Wu also bound the minimum from below by a term of order $n^2 \log n$.

| $n$ | NNI | SPR | TBR, all shapes | TBR maximum | Allen-Steel bound |
|---|---|---|---|---|---|
| 4 | 2 | 2 | 2 | 2 | 5 |
| 5 | 4 | 12 | 12 | 12 | 28 |
| 6 | 6 | 30 | 30, 34 | 34 | 81 |
| 7 | 8 | 56 | 64, 72 | 72 | 176 |
| 8 | 10 | 90 | 106, 114, 118, 130 | 130 | 325 |

The "all shapes" column lists the sizes over all $(2n-5)!!$ trees for each $n$.

## Classic examples

**Two shapes on six taxa.** The caterpillar $(((A,B),C),D,(E,F))$ has nontrivial splits of sizes $2 \mid 4$, $3 \mid 3$ and $2 \mid 4$, so $\Gamma = 8 + 9 + 8 = 25$ and it has $100 - 66 = 34$ TBR neighbors. The tree $((A,B),(C,D),(E,F))$ with three cherries has three splits of size $2 \mid 4$, so $\Gamma = 24$ and it has $30$ TBR neighbors, the same as its 30 SPR neighbors: for this tree, TBR adds no tree that SPR cannot reach.

**Parsimony search.** A common search for [maximum parsimony](/maximum-parsimony/) trees runs TBR branch swapping from many random [stepwise addition](/stepwise-addition/) starts and keeps the shortest trees found. The regraft score for Fitch parsimony above makes each reconnection cost $O(m)$.

**The parsimony ratchet.** Nixon's [ratchet](/parsimony-ratchet/) runs a TBR search under reweighted characters and then under the original weights. Its page gives seven taxa where a tree of length 33 has no better TBR neighbor while the best tree has length 32, and the ratchet escapes it.

**Agreement forests.** For unrooted trees, the TBR distance between two trees is the size of a [maximum agreement forest](/maximum-agreement-forest/) minus one (Allen and Steel 2001). Each TBR move cuts one edge, which matches one more component of the forest. The distance is NP-hard to compute.

## Variations

- **Limited reconnection.** Only join places within a distance of the cut, as in radius-limited SPR. This removes most of the $\Theta(n^3)$ moves of long caterpillars.
- **SPR as a special case.** Fix the place $a$ to be the edge that came from the suppressed vertex $u$; then the move keeps the root of $T_u$, and it is an SPR.
- **First improvement.** Accept the first join that lowers the score and start the next round from it. Each round is cheaper, but the search may stop at a different local optimum.

## Pitfalls

- **Counting moves instead of trees.** A round makes up to $(2n-3)\,n^2$ joins in the simple form, but many give the same tree. The neighborhood size is the formula above, not the number of joins.
- **Shape matters.** Two trees with the same $n$ have neighborhoods of different size, so the cost of one TBR round depends on where the search is.
- **Still a local search.** A TBR local optimum can be far from the best tree. Restart from many trees, or perturb as the ratchet does.
- **Trivial joins.** Joining the two places of the suppressed vertices gives $T$; a single leaf part has one place, not zero.

## Exercises

1. Show that $\Gamma(T) = \sum_{i < j} (d(i, j) - 2)$, where $d(i, j)$ is the number of edges on the path between leaves $i$ and $j$. Use it to compute $\Gamma$ for the caterpillar on $n$ leaves.
2. Verify the formula $4\Gamma(T) - (4n-2)(n-3)$ for $n = 5$ by listing the 12 neighbors of one tree.
3. For the three-cherry tree on six taxa, explain why every TBR move is also an SPR move.
4. Write the $O(m)$ join score for Fitch parsimony and use it to make one TBR round cost $O(n^3 m)$.

## References
