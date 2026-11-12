---
tag: KE4P29
kind: concept
slug: lance-williams-formula
name: Lance-Williams formula
aliases:
- Lance-Williams recurrence
area: machine-learning/clustering
level: advanced
summary: "One recurrence that gives the dissimilarity of a merged cluster to each other cluster from old values, with a coefficient row per linkage."
prereqs: [linkage-criterion, agglomerative-clustering]
see_also: [ward-method, nearest-neighbor-chain, single-linkage-clustering, complete-linkage-clustering, upgma, wpgma]
sources:
  - paper: doi:10.1093/comjnl/9.4.373
    title: "G. N. Lance and W. T. Williams, A general theory of classificatory sorting strategies 1. Hierarchical systems, The Computer Journal 9(4) (1967), 373-380"
    locator: the linear recurrence with four parameters, the values for each strategy, and the flexible strategy
  - book: isbn:9780130222787
    title: Anil K. Jain and Richard C. Dubes, Algorithms for Clustering Data
    locator: Chapter 3, Section 3.2 (the Lance-Williams recurrence and its table of coefficients)
  - url: https://arxiv.org/abs/1109.2378
    title: "Daniel Müllner, Modern hierarchical, agglomerative clustering algorithms, arXiv:1109.2378 (2011)"
    locator: Section 2, the table of update formulas for the seven methods, with the squared Euclidean input for centroid, median and Ward
  - paper: doi:10.1002/widm.53
    title: "Fionn Murtagh and Pedro Contreras, Algorithms for hierarchical clustering: an overview, WIREs Data Mining and Knowledge Discovery 2(1) (2012), 86-97"
    locator: the table of Lance-Williams coefficients and the remark on the reducibility of the methods
---

The Lance-Williams formula updates the dissimilarity matrix of [agglomerative clustering](/agglomerative-clustering/) after a merge. When clusters $i$ and $j$ merge, the dissimilarity of each other cluster $k$ to the union is

$$D(k, i \cup j) = \alpha_i D(k, i) + \alpha_j D(k, j) + \beta D(i, j) + \gamma \lvert D(k, i) - D(k, j) \rvert,$$

where the four coefficients depend only on the [linkage criterion](/linkage-criterion/) and the sizes $n_i$, $n_j$, $n_k$. Each update takes $O(1)$ time, so one round of updates takes $O(n)$ time, and one program serves all seven classic linkages. For centroid, median and Ward linkage the formula is exact only when $D$ holds squared Euclidean distances. Lance and Williams published it in 1967.

## In plain words

After two groups join, you need the distance from the new group to each other group. You could go back to the items and measure again, but that is slow.

The formula lets you skip that. For each other group, it takes three numbers that you already have: the distance to the first old group, the distance to the second old group, and the distance between the two old groups. It mixes them with fixed weights. The weights depend on the rule for the distance between groups, and on how many items each group has.

## The idea

The coefficients for the seven linkages, with $s = n_i + n_j$ and $t = n_i + n_j + n_k$, are these.

| linkage | $\alpha_i$ | $\alpha_j$ | $\beta$ | $\gamma$ | input |
|---|---|---|---|---|---|
| single | $1/2$ | $1/2$ | $0$ | $-1/2$ | any dissimilarity |
| complete | $1/2$ | $1/2$ | $0$ | $1/2$ | any dissimilarity |
| average (UPGMA) | $n_i/s$ | $n_j/s$ | $0$ | $0$ | any dissimilarity |
| weighted (WPGMA) | $1/2$ | $1/2$ | $0$ | $0$ | any dissimilarity |
| centroid (UPGMC) | $n_i/s$ | $n_j/s$ | $-n_i n_j/s^2$ | $0$ | squared Euclidean |
| median (WPGMC) | $1/2$ | $1/2$ | $-1/4$ | $0$ | squared Euclidean |
| Ward | $(n_i + n_k)/t$ | $(n_j + n_k)/t$ | $-n_k/t$ | $0$ | squared Euclidean |

**Why the rows are right.** The single and complete rows use $\min(x, y) = \frac{x + y}{2} - \frac{|x - y|}{2}$ and $\max(x, y) = \frac{x + y}{2} + \frac{|x - y|}{2}$. The average row holds because the sum of the distances from $k$ to $i \cup j$ is the sum to $i$ plus the sum to $j$. The weighted row is the definition of weighted linkage. The centroid, median and Ward rows come from one identity for squared distances: for $z = \alpha x + \beta' y$ with $\alpha + \beta' = 1$,

$$\lVert u - z \rVert^2 = \alpha \lVert u - x \rVert^2 + \beta' \lVert u - y \rVert^2 - \alpha \beta' \lVert x - y \rVert^2.$$

The centroid of $i \cup j$ is $z$ with $\alpha = n_i/s$, the median point uses $\alpha = 1/2$, and the Ward row follows when each squared centroid distance is written through the Ward value $\frac{n_a n_b}{n_a + n_b} \lVert c_a - c_b \rVert^2$. The identity needs squares of Euclidean distances, which is why these three rows fail on plain distances. The full derivation of each row is in the [correctness proof of agglomerative clustering](/agglomerative-clustering/), and its code checks each row exactly, with rational arithmetic, against the values recomputed from the points.

**Scaling.** The formula is linear and has no constant term. So if a row holds for $D$, it holds for $c \cdot D$ for each constant $c > 0$. This is why the Ward row is right both for the increase $\Delta$ of the sum of squares and for $2\Delta$, the value that many programs store.

**Monotone rows.** If $\gamma = 0$, $\alpha_i, \alpha_j \ge 0$, $\beta \le 0$ and $\alpha_i + \alpha_j + \beta \ge 1$, then the merge heights never decrease. When $i$ and $j$ are the closest pair, $m = \min(D(k, i), D(k, j)) \ge D(i, j)$, so the new value is at least $(\alpha_i + \alpha_j) m + \beta m \ge m$. Average, weighted and Ward linkage meet this test, and single and complete linkage are a minimum and a maximum. Centroid and median linkage have $\alpha_i + \alpha_j + \beta < 1$, and they can make inversions.

**The flexible strategy.** Lance and Williams also proposed a family with $\alpha_i = \alpha_j = (1 - \beta)/2$, $\gamma = 0$ and a free parameter $\beta < 1$, often $\beta = -1/4$. A negative $\beta$ makes the method dilate space, like complete linkage, and a positive $\beta$ makes it contract space, like single linkage.

## Examples

Take the points $a, b, c$ at $0, 2, 3$ on a line. The first merge joins $b$ and $c$. The table gives the new value $D(a, \{b, c\})$, with $D(a, b) = 2$, $D(a, c) = 3$ and $D(b, c) = 1$. For the last three rows, the inputs are the squares $4$, $9$ and $1$, and for Ward they are the Ward values of single points, half the squares: $2$, $9/2$ and $1/2$.

| linkage | update | value | check from the points |
|---|---|---|---|
| single | $\frac{1}{2} 2 + \frac{1}{2} 3 - \frac{1}{2} \lvert 2 - 3 \rvert$ | $2$ | $\min(2, 3)$ |
| complete | $\frac{1}{2} 2 + \frac{1}{2} 3 + \frac{1}{2} \lvert 2 - 3 \rvert$ | $3$ | $\max(2, 3)$ |
| average | $\frac{1}{2} 2 + \frac{1}{2} 3$ | $5/2$ | $(2 + 3)/2$ |
| centroid | $\frac{1}{2} 4 + \frac{1}{2} 9 - \frac{1}{4} 1$ | $25/4$ | $(0 - 5/2)^2$ |
| Ward | $\frac{2}{3} 2 + \frac{2}{3} \cdot \frac{9}{2} - \frac{1}{3} \cdot \frac{1}{2}$ | $25/6$ | $\frac{1 \cdot 2}{3}(0 - 5/2)^2$ |

**Average and weighted differ after the second merge.** Add the point $d$ at $7$, and merge $a$ with $\{b, c\}$. Average linkage gives $D(d, \{a, b, c\}) = \frac{1}{3} \cdot 7 + \frac{2}{3} \cdot \frac{9}{2} = \frac{16}{3}$, the mean of $7, 5, 4$. Weighted linkage gives $\frac{1}{2} \cdot 7 + \frac{1}{2} \cdot \frac{9}{2} = \frac{23}{4}$, because it gives the point $a$ the same weight as the pair $\{b, c\}$.

**Plain distances break the Ward row.** With plain distances $2, 3, 1$ as the input, the Ward row gives $\frac{2}{3} 2 + \frac{2}{3} 3 - \frac{1}{3} 1 = 3$, but no Ward value of these clusters is $3$: the right value is $25/6$ on the scale of $\Delta$, $25/3$ on the scale of $2\Delta$, and $\sqrt{25/3} \approx 2.89$ on the scale of $\sqrt{2\Delta}$, where single points are at their plain distance.

## Where it is used

- The naive and the priority queue versions of [agglomerative clustering](/agglomerative-clustering/) update the matrix with it.
- The [nearest-neighbor chain](/nearest-neighbor-chain/) uses it to update the row of a merged cluster, and its coefficients show which linkages are reducible.
- Statistics libraries, such as `hclust` in R and `linkage` in SciPy, update their matrices with these rows.
- [UPGMA](/upgma/) and [WPGMA](/wpgma/) in phylogenetics are the average and weighted rows.
- The [complete linkage](/complete-linkage-clustering/) and [single linkage](/single-linkage-clustering/) rows are a maximum and a minimum, so faster special methods such as [SLINK](/slink/) exist for them.

## References
