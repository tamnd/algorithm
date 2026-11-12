---
tag: XCPYZW
kind: problem
slug: tree-comparison
name: Tree comparison
aliases:
- tree distance computation
- phylogenetic tree distance
area: biology/phylogenetics
level: core
summary: Measure how far apart two phylogenetic trees on the same taxa are. RF and quartet distances take near-linear time; NNI, SPR and TBR distances are NP-hard; agreement subtrees lie between.
prereqs: [phylogenetic-tree, splits-of-a-tree]
see_also: [robinson-foulds-distance, day-algorithm, quartet, rooted-triplet, spr-distance, maximum-agreement-subtree, maximum-agreement-forest, consensus-tree]
sources:
  - paper: doi:10.1016/0025-5564(81)90043-2
    title: D. F. Robinson and L. R. Foulds, Comparison of phylogenetic trees, Mathematical Biosciences 53(1-2), 1981, 131-147
    locator: the symmetric difference distance and its relation to the moves between trees
  - paper: doi:10.1007/BF01908061
    title: William H. E. Day, Optimal algorithms for comparing trees with labeled leaves, Journal of Classification 2(1), 1985, 7-28
    locator: the O(n) algorithm for the symmetric difference distance
  - paper: doi:10.1007/s00453-003-1065-y
    title: Gerth Stølting Brodal, Rolf Fagerberg and Christian N. S. Pedersen, Computing the quartet distance between evolutionary trees in time O(n log n), Algorithmica 38, 2004, 377-395
    locator: the O(n log n) algorithm for the quartet distance of two binary trees
  - paper: doi:10.1007/s00026-001-8006-8
    title: Benjamin L. Allen and Mike Steel, Subtree transfer operations and their induced metrics on evolutionary trees, Annals of Combinatorics 5(1), 2001, 1-15
    locator: the TBR distance as the size of a maximum agreement forest minus one, its NP-hardness and its fixed-parameter algorithm
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 30, Consensus trees and distances between trees
---

Tree comparison is the problem of measuring how different two [phylogenetic trees](/phylogenetic-tree/) on the same taxa are. There is no single answer: each distance counts a different kind of disagreement, such as the [splits](/splits-of-a-tree/) in one tree but not the other, the [quartets](/quartet/) or [rooted triplets](/rooted-triplet/) on which the trees differ, the number of moves that turn one tree into the other, or the taxa that must be removed to make the trees agree. The counting distances take near-linear time, while the move distances are NP-hard. Most studies report the [Robinson-Foulds distance](/robinson-foulds-distance/), which [Day's algorithm](/day-algorithm/) computes in $O(n)$ time.

## In plain words

Two studies of the same species often give different trees, and we want to say how different they are. One way is to list the groups each tree claims and count the claims that only one tree makes. Another is to look at every small set of four species and count the sets on which the trees disagree. A third is to count how many cut-and-paste moves of branches turn one tree into the other. A fourth is to ask how many species we must delete before the two trees look the same.

These ways can give very different numbers. Moving one species from one end of a tree to the other can look like a complete change to the first way and like a small change to the third and fourth. The first two are fast to compute, the third is hard, and the fourth is in between.

## Definition

**Input.** Two phylogenetic trees $T_1$ and $T_2$ on the same set $X$ of $n$ taxa, both rooted or both unrooted, and a choice of distance.

**Output.** The distance $d(T_1, T_2)$, a number that is 0 exactly when $T_1 = T_2$.

The usual distances are:

| distance | trees | what it counts |
|---|---|---|
| [Robinson-Foulds](/robinson-foulds-distance/) $d_{RF}$ | both | splits (or clusters) in exactly one tree |
| quartet distance $d_Q$ | unrooted | sets of four taxa on which the displayed [quartets](/quartet/) differ |
| triplet distance $d_R$ | rooted | sets of three taxa on which the displayed [triplets](/rooted-triplet/) differ |
| NNI distance $d_{NNI}$ | binary | fewest [nearest neighbor interchanges](/nearest-neighbor-interchange/) from $T_1$ to $T_2$ |
| [SPR distance](/spr-distance/) $d_{SPR}$ | binary | fewest [subtree prune and regraft](/subtree-prune-and-regraft/) moves |
| TBR distance $d_{TBR}$ | binary, unrooted | fewest [tree bisection and reconnection](/tree-bisection-and-reconnection/) moves |
| MAST distance | both | $n$ minus the number of taxa of a [maximum agreement subtree](/maximum-agreement-subtree/) |

For the quartet and triplet distances, a set of taxa counts as a difference when the two trees display different quartets on it, or when one displays a quartet and the other displays none. The RF distance here is the full symmetric difference; some programs report half of it.

## Variants

- **Rooted and unrooted.** RF, MAST and the SPR distance each have a rooted and an unrooted version. The rooted versions see the position of the root: two rootings of one unrooted tree are at rooted RF distance up to $2(n - 2)$.
- **Normalized distances.** Dividing by the largest possible value, such as $2(n-3)$ for RF of binary trees or $\binom{n}{4}$ for the quartet distance, gives numbers between 0 and 1 that can be compared across data sets of different sizes.
- **Branch lengths.** The weighted RF distance and the branch score distance (Kuhner and Felsenstein, 1994) compare the lengths of the edges of each split, so they also see trees with the same shape and different lengths.
- **Different taxon sets.** Trees from different studies often share only some taxa. The usual approach restricts both trees to the shared taxa, removing the other leaves and suppressing the vertices of degree 2, and then compares the restrictions.
- **Many trees.** For $m$ trees, the $\binom{m}{2}$ RF distances come from one hash table of the [splits](/split-system/) of all trees. Summaries of a set of trees, such as a [consensus tree](/consensus-tree/), come from the same table.

## Examples

**Two trees one NNI apart.** Let $T_1 = (((A,B),C),(D,(E,F)))$ and $T_2 = (((A,C),B),(D,(E,F)))$, unrooted. They differ only in the positions of $B$ and $C$.

| distance | value | why |
|---|---|---|
| RF | 2 | $AB \mid CDEF$ is only in $T_1$, $AC \mid BDEF$ only in $T_2$ |
| quartet | 3 of 15 | the sets $ABCD$, $ABCE$, $ABCF$; for example $AB \mid CD$ against $AC \mid BD$ |
| MAST distance | 1 | removing $C$ leaves the same tree $((A,B),(D,(E,F)))$ on five taxa |
| NNI, SPR, TBR | 1 | one interchange across the edge of $ABC \mid DEF$ |

**One leaf moved.** Let $T_1$ be the caterpillar $(A,(B,(C,(D,(E,F)))))$ and $T_2$ the caterpillar $(B,(C,(D,(E,(F,A)))))$: the leaf $A$ moved from one end to the other.

| distance | value | why |
|---|---|---|
| RF | 6 | the maximum $2(n-3)$; no nontrivial split is shared |
| quartet | 10 of 15 | the 10 sets of four that hold $A$; the 5 sets without $A$ agree |
| MAST distance | 1 | the two trees agree on $B, C, D, E, F$ |
| SPR, TBR | 1 | prune $A$ and regraft it next to $F$ |
| NNI | more than 1 | one NNI changes only one split, and RF is 6, so at least 3 NNIs are needed |

RF says the trees share nothing, while MAST and SPR say that one taxon is out of place. This is the main argument for the move and agreement distances, even though they are harder to compute.

**Two rooted trees.** For $((a,b),(c,(d,e)))$ and $((a,c),(b,(d,e)))$, the rooted RF distance is 4 (the clusters $ab$ and $cde$ against $ac$ and $bde$), and the triplet distance is 7 of 10: only $de \mid a$, $de \mid b$ and $de \mid c$ are shared.

## Known algorithms

- **RF distance.** [Day's algorithm](/day-algorithm/) numbers the leaves of $T_1$ so that each cluster is an interval, stores the intervals in a table, and checks each cluster of $T_2$ in $O(1)$ time. It runs in $O(n)$ time and space. Hashing bit masks of the splits takes $O(n^2/w)$ time with $w$-bit words and is simpler.
- **Quartet distance.** Checking all $\binom{n}{4}$ sets of four takes $O(n^4)$ time. For binary trees, Brodal, Fagerberg and Pedersen (2004) count the shared quartets in $O(n \log n)$ time with hierarchical decompositions of the trees. Trees with polytomies have polynomial algorithms too.
- **Triplet distance.** The naive method checks all $\binom{n}{3}$ sets of three. Counting the shared triplets over the vertices of one tree, with the other tree in a balanced data structure, gives near-linear time.
- **MAST.** The [maximum agreement subtree](/maximum-agreement-subtree/) of two trees is found in polynomial time by dynamic programming over pairs of subtrees; for two binary trees the best known algorithms take $O(n \log n)$ time.
- **SPR and TBR.** The TBR distance equals the size of a [maximum agreement forest](/maximum-agreement-forest/) of the two trees minus one (Allen and Steel, 2001), and the rooted SPR distance equals the size of a maximum rooted agreement forest minus one ([rSPR and MAF](/rspr-maf-equivalence/)). Both are NP-hard. They are fixed-parameter tractable in the distance $k$: kernels and branching algorithms solve them in time $f(k) \cdot \mathrm{poly}(n)$, which is practical when the trees are close.
- **NNI.** Computing the NNI distance is NP-hard (DasGupta and others, 1997). Upper bounds come from heuristic paths between the trees.

## Bounds

- Every distance here needs $\Omega(n)$ time, since it must read both trees. Day's $O(n)$ algorithm for RF is optimal.
- **Ranges.** For binary trees, $d_{RF} \le 2(n - 3)$, $d_Q \le \binom{n}{4}$, and $d_{TBR} \le d_{SPR} \le n - 3$: move the leaves one at a time.
- **Relations between the move distances.** Every NNI is an SPR and every SPR is a TBR, so $d_{TBR} \le d_{SPR} \le d_{NNI}$. One NNI changes one split, so $d_{RF} \le 2\, d_{NNI}$. An SPR can change all splits, so RF has no upper bound in terms of SPR: the caterpillar example has $d_{SPR} = 1$ and $d_{RF} = 2(n-3)$.
- **Hardness.** NNI, SPR and TBR distances are NP-hard, so no polynomial algorithm is expected. The MAST of three or more trees is NP-hard when the degree is unbounded.

## Reductions

- **RF to interval lookup.** After a postorder numbering of the leaves of $T_1$, each cluster of $T_1$ is an interval of numbers, and a cluster of $T_2$ is shared exactly when its numbers form an interval that is in a table. This is the reduction behind [Day's algorithm](/day-algorithm/).
- **Unrooted to rooted.** Rooting both unrooted trees at the same leaf $r$ turns splits into clusters, so unrooted RF reduces to rooted RF on $X \setminus \{r\}$ with no change in value.
- **Triplets to quartets.** Adding a new leaf $\rho$ above the root of both rooted trees turns each triplet $ab \mid c$ into the quartet $ab \mid c\rho$, so the triplet distance is the number of differing quartets that hold $\rho$.
- **Move distances to agreement forests.** TBR distance is maximum agreement forest, and rooted SPR distance is maximum rooted agreement forest, both minus one. Algorithms for the forests give the distances.

## Applications

- **Simulation studies.** The RF distance between the true tree and an estimated tree is the usual measure of accuracy of a [tree reconstruction method](/phylogenetic-tree-reconstruction/).
- **Gene tree discordance.** Distances between gene trees and a species tree measure conflict from [incomplete lineage sorting](/incomplete-lineage-sorting/) and [horizontal gene transfer](/horizontal-gene-transfer/); SPR distances give a lower bound on the number of transfer events.
- **Summaries of many trees.** Bootstrap and Bayesian samples of trees are summarized with split frequencies and [consensus trees](/consensus-tree/), and pairwise distances let one map a sample of trees in a low-dimensional picture.
- **Tree search.** Heuristic searches move by NNI, SPR and TBR steps, so the move distances say how many steps separate two local optima.

## References
