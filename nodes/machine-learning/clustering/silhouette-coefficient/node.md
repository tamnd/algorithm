---
tag: 9J34RM
kind: definition
slug: silhouette-coefficient
name: Silhouette coefficient
aliases:
- silhouette score
- silhouette width
- Rousseeuw silhouette
area: machine-learning/clustering
level: core
summary: "For each object, s = (b - a)/max(a, b): a is its mean distance to its own cluster, b to the nearest other cluster. The mean of s over all objects scores the clustering."
prereqs: [clustering-problem, metric-space, euclidean-distance]
see_also: [calinski-harabasz-index, davies-bouldin-index, dunn-index, cluster-validity, partitioning-around-medoids, elbow-method, gap-statistic]
sources:
  - paper: doi:10.1016/0377-0427(87)90125-7
    title: "Peter J. Rousseeuw, Silhouettes, a graphical aid to the interpretation and validation of cluster analysis, Journal of Computational and Applied Mathematics 20, 1987, pages 53 to 65"
    locator: the definitions of a(i), b(i) and s(i), the convention s(i) = 0 for a cluster with one object, the silhouette plot and the average silhouette width for the choice of k
  - book: isbn:9780471878766
    title: Leonard Kaufman and Peter J. Rousseeuw, Finding Groups in Data, an Introduction to Cluster Analysis, Wiley, 1990
    locator: Chapter 2 (partitioning around medoids), the silhouette plot, the silhouette coefficient as the largest average width over k, and its rough scale of interpretation
---

The silhouette coefficient scores how well each object sits in its cluster. For object $i$, it compares $a(i)$, the mean distance from $i$ to the other objects of its own cluster, with $b(i)$, the mean distance from $i$ to the objects of the nearest other cluster. The score $s(i) = (b(i) - a(i))/\max(a(i), b(i))$ is between $-1$ and 1. It is near 1 when $i$ is much closer to its own cluster, near 0 when $i$ is between two clusters, and negative when $i$ is closer to another cluster. Peter Rousseeuw defined it in 1987. The mean of $s(i)$ over all objects is an internal [cluster validity](/cluster-validity/) index: it needs no true classes, only the distances and the clustering.

## Definition

**Setting.** $X = \{x_1, \ldots, x_n\}$ is a set of $n$ objects with a dissimilarity $d(x_i, x_j) \ge 0$. Rousseeuw allows any dissimilarity, and the triangle inequality is not needed. A common case is points in $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/), which the implementation uses by default. A clustering $\mathcal{C} = \{C_1, \ldots, C_k\}$ of $X$ is given, with $2 \le k \le n - 1$. For object $i$, $C(i)$ is its cluster.

**Mean distances.** For a cluster $C$ and an object $i$, let $\bar d(i, C)$ be the mean of $d(x_i, x_j)$ over $x_j \in C$, $j \ne i$. Then

$$a(i) = \bar d(i, C(i)), \qquad b(i) = \min_{C \ne C(i)} \bar d(i, C).$$

The cluster that reaches the minimum in $b(i)$ is the **neighbor** of $i$: the cluster that $i$ would join if its own cluster did not exist.

**The silhouette of one object.**

$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))} = \begin{cases} 1 - a(i)/b(i) & \text{if } a(i) < b(i), \\ 0 & \text{if } a(i) = b(i), \\ b(i)/a(i) - 1 & \text{if } a(i) > b(i). \end{cases}$$

If $C(i)$ has only the object $i$, then $a(i)$ is not defined, and $s(i) = 0$ by convention. If $a(i) = b(i) = 0$ (repeated points), the implementation also returns 0.

**Means.** The mean silhouette of a cluster is the mean of $s(i)$ over its objects. The **mean silhouette** of the clustering, also called the average silhouette width, is

$$\bar s(\mathcal{C}) = \frac{1}{n} \sum_{i=1}^{n} s(i).$$

To choose $k$, compute $\bar s$ for the best clustering with each $k \ge 2$ and take the $k$ with the largest value. Kaufman and Rousseeuw call that largest value the silhouette coefficient of the data set.

**Cost.** $a(i)$ and $b(i)$ need the distances from $i$ to every other object, so the whole computation needs all $n(n-1)/2$ distances: $O(n^2 d)$ time for points in $\mathbb{R}^d$. With one pass over the objects for each $i$, the extra memory is $O(k)$ for the sums for each cluster. This quadratic cost is the reason that libraries offer a mean silhouette over a random sample of the objects.

**Properties.**

- $-1 \le s(i) \le 1$ for each object. The value 1 needs $a(i) = 0$, so all objects of the cluster coincide with $x_i$.
- $s(i) < 0$ means that $i$ is on average closer to its neighbor cluster than to its own cluster. A clustering with many negative values has objects in the wrong cluster.
- $s(i)$ is invariant under a uniform scaling of all distances, because it is a ratio.
- The singleton convention matters. Without it, $k = n$ would give the best possible value. With it, a clustering with many singletons gets many zeros.
- The mean silhouette favors compact, convex and well-separated clusters. A cluster with a long or curved shape has a large $a(i)$ for its far ends, even when the clustering is right.

## Examples and non-examples

**Five points on a line.** $X = \{0, 1, 2, 6, 7\}$ with $d(x, y) = |x - y|$, and the clusters $\{0, 1, 2\}$ and $\{6, 7\}$.

| $x_i$ | $a(i)$ | $b(i)$ | $s(i)$ |
|---|---|---|---|
| 0 | $(1 + 2)/2 = 3/2$ | $(6 + 7)/2 = 13/2$ | $1 - 3/13 = 10/13$ |
| 1 | $(1 + 1)/2 = 1$ | $(5 + 6)/2 = 11/2$ | $1 - 2/11 = 9/11$ |
| 2 | $(2 + 1)/2 = 3/2$ | $(4 + 5)/2 = 9/2$ | $1 - 1/3 = 2/3$ |
| 6 | 1 | $(6 + 5 + 4)/3 = 5$ | $4/5$ |
| 7 | 1 | $(7 + 6 + 5)/3 = 6$ | $5/6$ |

The point 2 has the lowest value: it is the point of the first cluster that is nearest to the second.

**Nine points in the plane.** Take the points $(0, 0), (2, 0), (1, 3)$, then $(8, 0), (10, 0), (9, 3)$, then $(4, 8), (6, 8), (5, 11)$, with the Euclidean distance. For the clustering into these three triangles, consider the point $(0, 0)$:

- $a = (2 + \sqrt{10})/2 \approx 2.5811$,
- the mean distance to the second triangle is $(8 + 10 + \sqrt{90})/3 \approx 9.1623$, and to the third triangle it is $(\sqrt{80} + 10 + \sqrt{146})/3 \approx 10.3424$, so $b \approx 9.1623$ and the neighbor is the second triangle,
- $s = 1 - 2.5811/9.1623 \approx 0.7183$.

All nine values are 0.7183, 0.6418, 0.5657, 0.6418, 0.7183, 0.5657, 0.6636, 0.6636 and 0.7075, and the mean silhouette is 0.6540. If the first two triangles are merged into one cluster, the mean drops to 0.4403: the merged cluster has a mean silhouette of 0.3145, against 0.6919 for the third triangle. So the mean silhouette prefers $k = 3$ to this $k = 2$ clustering, as it should.

**Rings.** Put 12 points evenly on a circle of radius 1 and 12 on a circle of radius 4, both centered at the origin. The clustering into the two rings has a mean silhouette of 0.198. A cut of the plane into a left half and a right half, which mixes the rings, has a higher mean silhouette, 0.226. The silhouette measures compact and separated clusters, not connected ones.

**Non-examples.**

- The silhouette is not an external index. It does not use the true classes, and a high value does not mean that the clusters match any classes.
- $b(i)$ is not the distance from $i$ to the nearest object of another cluster. It is a mean over the nearest cluster.
- The mean silhouette is not defined for $k = 1$. So it cannot say that the data have no cluster structure; the [gap statistic](/gap-statistic/) can.

## Related definitions

- [Calinski-Harabasz index](/calinski-harabasz-index/) and [Davies-Bouldin index](/davies-bouldin-index/): internal indices that use centroids, so they cost $O(nd)$ and $O(nd + k^2 d)$ instead of $O(n^2 d)$, but they need points in $\mathbb{R}^d$.
- [Dunn index](/dunn-index/): an internal index that uses the smallest gap and the largest diameter, not means.
- [Partitioning around medoids](/partitioning-around-medoids/): the method with which Kaufman and Rousseeuw present the silhouette plot.
- [Elbow method](/elbow-method/) and [gap statistic](/gap-statistic/): other ways to choose $k$.
- [Cluster validity](/cluster-validity/) gives the overview of external and internal indices.

## References
