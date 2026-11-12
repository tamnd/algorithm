---
tag: T6VVWX
kind: concept
slug: linkage-criterion
name: Linkage criterion
aliases:
- cluster distance
area: machine-learning/clustering
level: intro
summary: "The rule that gives the dissimilarity of two clusters from the dissimilarities of their points: single, complete, average, weighted, centroid, median or Ward."
prereqs: [hierarchical-clustering-problem, euclidean-distance]
see_also: [agglomerative-clustering, lance-williams-formula, single-linkage-clustering, complete-linkage-clustering, ward-method, nearest-neighbor-chain, upgma, wpgma]
sources:
  - paper: doi:10.1093/comjnl/9.4.373
    title: "G. N. Lance and W. T. Williams, A general theory of classificatory sorting strategies 1. Hierarchical systems, The Computer Journal 9(4) (1967), 373-380"
    locator: the strategies nearest neighbour, furthest neighbour, group average, simple average, centroid and median, and the terms space-contracting and space-dilating
  - paper: "Michel Bruynooghe, Méthodes nouvelles en classification automatique de données taxinomiques nombreuses, Statistique et Analyse des Données (1977)"
    locator: the reducibility property of a cluster distance
  - paper: doi:10.1093/comjnl/26.4.354
    title: "Fionn Murtagh, A survey of recent advances in hierarchical clustering algorithms, The Computer Journal 26(4) (1983), 354-359"
    locator: the reducibility property, which linkages have it, and its use for reciprocal nearest neighbors
  - url: https://arxiv.org/abs/1109.2378
    title: "Daniel Müllner, Modern hierarchical, agglomerative clustering algorithms, arXiv:1109.2378 (2011)"
    locator: Section 2 (the seven linkage methods with their formulas, and the inversions of centroid and median linkage)
  - book: isbn:9780471878766
    title: Leonard Kaufman and Peter J. Rousseeuw, Finding Groups in Data, An Introduction to Cluster Analysis
    locator: Chapter 5 (agglomerative nesting, the group average and the other linkages)
---

A linkage criterion is the rule that turns the dissimilarities between points into a dissimilarity $D(A, B)$ between two clusters $A$ and $B$. [Agglomerative clustering](/agglomerative-clustering/) merges, at each step, the two clusters with the smallest $D$, so the linkage is the only choice in the method, and it decides the shape of the clusters. The seven classic linkages are single, complete, average (UPGMA), weighted (WPGMA), centroid, median and Ward. All seven can be updated after a merge in constant time by the [Lance-Williams formula](/lance-williams-formula/). Five of them are *reducible*, which makes the merge heights increase and lets the [nearest-neighbor chain](/nearest-neighbor-chain/) run in $O(n^2)$ time. Centroid and median linkage are not, and they can make a merge lower than an earlier one.

## In plain words

You know how far apart any two points are. Now you need to say how far apart two groups of points are, so that you can join the two closest groups.

There are several fair answers. You can use the two closest points, one from each group. You can use the two points that are farthest apart. You can take the average over all pairs. You can compare the centers of the two groups. Or you can ask how much the spread of the points grows if the two groups join.

Each answer is a linkage. The first one makes long, thin groups. The second one makes round, tight groups. The others are in between.

## The idea

Let $d$ be a dissimilarity on the points. For two disjoint clusters $A$ and $B$, with sizes $|A|$ and $|B|$:

| linkage | $D(A, B)$ | also called |
|---|---|---|
| single | $\min_{a \in A, b \in B} d(a, b)$ | nearest neighbor |
| complete | $\max_{a \in A, b \in B} d(a, b)$ | farthest neighbor |
| average | $\frac{1}{\lvert A \rvert \lvert B \rvert} \sum_{a \in A, b \in B} d(a, b)$ | group average, [UPGMA](/upgma/) |
| weighted | $\frac{1}{2}\bigl(D(A_1, B) + D(A_2, B)\bigr)$ if $A$ was made from $A_1$ and $A_2$ | McQuitty, [WPGMA](/wpgma/) |
| centroid | $\lVert c_A - c_B \rVert^2$, with $c_A$ the mean of $A$ | UPGMC |
| median | $\lVert m_A - m_B \rVert^2$, with $m_A = \frac{1}{2}(m_{A_1} + m_{A_2})$ | Gower, WPGMC |
| Ward | $\frac{\lvert A \rvert \lvert B \rvert}{\lvert A \rvert + \lvert B \rvert} \lVert c_A - c_B \rVert^2$ | minimum variance, [Ward's method](/ward-method/) |

Single, complete and average linkage need only the dissimilarities, and they work for any $d$. Weighted linkage gives each of the two parts of a cluster the same weight, whatever their sizes, so it depends on the order of the merges. Centroid, median and Ward linkage are defined for points in $\mathbb{R}^p$ with the squared [Euclidean distance](/euclidean-distance/). The Ward value is the increase of the within-cluster sum of squares when $A$ and $B$ merge, so Ward linkage merges greedily for the [k-means](/k-means-problem/) objective.

**Reducibility.** A linkage is *reducible* (Bruynooghe 1977) if, for all disjoint clusters $I$, $J$, $K$,

$$D(I, J) \le \min\bigl(D(I, K),\ D(J, K)\bigr) \implies D(I \cup J, K) \ge \min\bigl(D(I, K),\ D(J, K)\bigr).$$

In words: a merge of two clusters that are closer to each other than to $K$ does not make a new cluster closer to $K$ than both parts were. Single, complete, average, weighted and Ward linkage are reducible. For the first four, $D(I \cup J, K)$ is a minimum, a maximum or a weighted mean of $D(I, K)$ and $D(J, K)$, so it is at least their minimum. For Ward, the [Lance-Williams formula](/lance-williams-formula/) gives $D(I \cup J, K) = \alpha_I D(I, K) + \alpha_J D(J, K) + \beta D(I, J)$ with $\alpha_I, \alpha_J \ge 0$, $\beta \le 0$ and $\alpha_I + \alpha_J + \beta = 1$. With $m = \min(D(I, K), D(J, K)) \ge D(I, J)$, this is at least $(\alpha_I + \alpha_J) m + \beta m = m$. For centroid and median linkage, $\alpha_I + \alpha_J + \beta < 1$, and reducibility fails.

**Why it matters.** Reducibility has two results.

- **No inversions.** The greedy method merges the pair $I, J$ with the smallest $D$, so $D(I, J) \le \min(D(I, K), D(J, K))$ for every other $K$. Reducibility then keeps each new value at least $D(I, J)$, so the next merge is not lower. The [dendrogram](/dendrogram/) is monotone, and its cophenetic distance is an [ultrametric](/ultrametric/).
- **Nearest neighbors stay valid.** The [nearest-neighbor chain](/nearest-neighbor-chain/) follows nearest neighbors from cluster to cluster, and merges a pair as soon as the two are each other's nearest neighbors. It merges pairs in a different order than the greedy method. Reducibility makes sure that a merge elsewhere never brings a new cluster closer to a cluster on the chain than its current nearest neighbor. So the chain stays a chain of nearest neighbors, and the method finds the same tree as the greedy method. Without reducibility, the two methods can give different trees.

**Space contraction and dilation.** Lance and Williams (1967) called single linkage *space-contracting*: a growing cluster gets closer to all other points, so it tends to absorb them one at a time, which is called chaining. Complete linkage is *space-dilating*: a growing cluster gets farther from the others, which gives compact clusters of similar diameter. Average linkage is *space-conserving*, between the two.

## Examples

Take the points $a, b, c, d, e$ at $0, 2, 3, 7, 13$ on a line, and the clusters $A = \{a, b, c\}$ and $B = \{d, e\}$, where $A$ was made from $\{a\}$ and $\{b, c\}$. The six distances between them are $7, 13, 5, 11, 4, 10$.

| linkage | $D(A, B)$ |
|---|---|
| single | $4$, the pair $c, d$ |
| complete | $13$, the pair $a, e$ |
| average | $50/6 = 25/3$ |
| weighted | $\frac{1}{2}\bigl(10 + \frac{1}{2}(8 + 7)\bigr) = 35/4$ |
| centroid | $(5/3 - 10)^2 = 625/9$ |
| median | $(5/4 - 10)^2 = 1225/16$, with $m_A = \frac{1}{2}(0 + 5/2)$ |
| Ward | $\frac{3 \cdot 2}{5} \cdot \frac{625}{9} = 250/3$ |

**An inversion.** Put three points at the corners of an equilateral triangle with side $1$, and use centroid linkage with squared distances. The first merge joins two corners at height $1$. Their centroid is the midpoint of a side, at squared distance $3/4$ from the third corner. So the second merge is at $3/4$, below the first one. With the integer points $(0, 0)$, $(8, 0)$ and $(4, 7)$, the heights are $64$ and then $49$. Median linkage gives the same heights here, because the two parts have equal size.

**Different linkages, different trees.** On the points $0, 2, 3, 7, 13, 21$, single linkage adds one point at a time to one cluster, while complete linkage first makes $\{a, b, c\}$ and $\{d, e\}$. The trees are on the page [hierarchical clustering problem](/hierarchical-clustering-problem/).

## Where it is used

- [Agglomerative clustering](/agglomerative-clustering/) needs a linkage to choose each merge, and [divisive clustering](/divisive-clustering/) uses one to judge splits.
- [Single linkage](/single-linkage-clustering/) is the [minimum spanning tree](/minimum-spanning-tree/) in disguise, and it is the base of [HDBSCAN](/hdbscan/).
- [Complete linkage](/complete-linkage-clustering/) gives clusters of small diameter.
- [UPGMA](/upgma/) and [WPGMA](/wpgma/) build trees of species in phylogenetics.
- [Ward's method](/ward-method/) gives compact clusters of similar size, and it is the default linkage of the agglomerative clustering of scikit-learn.
- The [Lance-Williams formula](/lance-williams-formula/) updates all seven linkages, and the [nearest-neighbor chain](/nearest-neighbor-chain/) uses reducibility for an $O(n^2)$ algorithm.

## References
