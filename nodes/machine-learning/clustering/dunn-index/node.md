---
tag: PBD47N
kind: definition
slug: dunn-index
name: Dunn index
aliases:
- Dunn validity index
area: machine-learning/clustering
level: advanced
summary: The smallest distance between points of different clusters divided by the largest cluster diameter. Higher is better, and a value above 1 means compact, well-separated clusters.
prereqs: [clustering-problem, metric-space]
see_also: [silhouette-coefficient, davies-bouldin-index, calinski-harabasz-index, cluster-validity, single-linkage-clustering, maximum-spacing-k-clustering]
sources:
  - paper: doi:10.1080/01969727408546059
    title: "J. C. Dunn, A fuzzy relative of the ISODATA process and its use in detecting compact well-separated clusters, Journal of Cybernetics 4(1), 1974, pages 95 to 104"
    locator: compact and well-separated clusters, and the separation index given by the least distance between clusters over the largest diameter
  - paper: doi:10.1109/3477.678624
    title: "James C. Bezdek and Nikhil R. Pal, Some new indexes of cluster validity, IEEE Transactions on Systems, Man, and Cybernetics, Part B 28(3), 1998, pages 301 to 315"
    locator: the generalized Dunn indices, with other set distances and diameters, and the sensitivity of the original index to noise
  - paper: doi:10.1023/A:1012801612483
    title: "Maria Halkidi, Yannis Batistakis and Michalis Vazirgiannis, On clustering validation techniques, Journal of Intelligent Information Systems 17(2-3), 2001, pages 107 to 145"
    locator: the Dunn index among the relative criteria, and its cost and sensitivity to noise
---

The Dunn index scores a clustering by its worst separation and its worst spread. It divides the smallest distance between two points in different clusters by the largest diameter of a cluster. **Higher is better.** J. C. Dunn defined it in 1974 to detect clusters that are compact and well separated, and a value above 1 means exactly that: every distance inside a cluster is smaller than every distance between clusters. It is an internal [cluster validity](/cluster-validity/) index that works with any dissimilarity. Because it uses a minimum and a maximum, one outlier can change it a lot.

## Definition

**Setting.** $X = \{x_1, \ldots, x_n\}$ is a set of $n$ objects with a dissimilarity $d$, for example a [metric](/metric-space/) or points in $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/), which the implementation uses by default. A clustering $C_1, \ldots, C_k$ of $X$ is given, with $k \ge 2$.

**Separation and diameter.**

$$\delta(C_i, C_j) = \min_{x \in C_i,\ y \in C_j} d(x, y), \qquad \Delta(C_l) = \max_{x, y \in C_l} d(x, y).$$

$\delta$ is the single linkage distance between two clusters, and $\Delta$ is the diameter of a cluster. A cluster with one object has diameter 0.

**The index.**

$$D = \frac{\min_{i \ne j} \delta(C_i, C_j)}{\max_{l} \Delta(C_l)}.$$

If every cluster has diameter 0, the implementation returns $+\infty$.

**Compact and well-separated clusters.** Dunn calls a clustering compact and well separated if every distance between two objects of the same cluster is smaller than every distance between two objects of different clusters.

**Claim.** For a clustering with at least one cluster of two or more objects, $D > 1$ if and only if the clustering is compact and well separated.

*Proof.* The numerator is the smallest between-cluster distance and the denominator is the largest within-cluster distance. So $D > 1$ says that the smallest between-cluster distance exceeds the largest within-cluster distance, which is the same as the condition for all pairs. $\square$

**Choosing $k$.** Compute $D$ for a good clustering for each $k \ge 2$ in a range, and take the $k$ with the largest value.

**Cost.** Both the minimum and the maximum range over pairs of objects, so a direct computation takes $O(n^2)$ distance evaluations, $O(n^2 d)$ time in $\mathbb{R}^d$, with $O(1)$ extra memory.

**Properties.**

- **Scale.** $D$ does not change when all distances are multiplied by the same factor.
- **Sensitive to outliers.** One object far from the rest of its cluster sets the largest diameter and lowers $D$ for the whole clustering. One object between two clusters sets the smallest gap and also lowers $D$.
- **Shape.** $D$ does not use centroids, so it can see clusters that are not round. Two nested rings that are far apart get a good value.
- **Link to single linkage.** For a fixed $k$, [single linkage](/single-linkage-clustering/) stopped at $k$ clusters maximizes the numerator, the smallest gap between clusters; this is the [maximum spacing k-clustering](/maximum-spacing-k-clustering/). It does not control the denominator, so it need not maximize $D$.

**Generalized Dunn indices.** Bezdek and Pal replaced $\delta$ by other distances between sets (for example the mean distance over all pairs, or the distance between centroids) and $\Delta$ by other measures of spread (for example twice the mean distance to the centroid). The variants that use means are less sensitive to single outliers than the original index.

## Examples and non-examples

**Nine points in the plane.** Take the three triangles $\{(0, 0), (2, 0), (1, 3)\}$, $\{(8, 0), (10, 0), (9, 3)\}$ and $\{(4, 8), (6, 8), (5, 11)\}$ with the Euclidean distance.

- Each triangle has sides 2, $\sqrt{10}$ and $\sqrt{10}$, so the largest diameter is $\sqrt{10} \approx 3.162$.
- The closest pair in different clusters is $(1, 3)$ and $(4, 8)$, at distance $\sqrt{9 + 25} = \sqrt{34} \approx 5.831$. The pair $(9, 3)$ and $(6, 8)$ is at the same distance, and $(2, 0)$ and $(8, 0)$ are at distance 6.
- $D = \sqrt{34}/\sqrt{10} = \sqrt{3.4} \approx 1.844$. It is above 1, so the clusters are compact and well separated.

If the first two triangles are merged, the smallest gap is still $\sqrt{34}$, but the merged cluster has diameter 10 (from $(0, 0)$ to $(10, 0)$). Then $D = \sqrt{34}/10 \approx 0.583$.

**One point changes the value.** On a line, take $\{0, 1, 2\}$ and $\{10, 11, 12\}$. The gap is 8 and the largest diameter is 2, so $D = 4$.

| change | gap | largest diameter | $D$ |
|---|---|---|---|
| none | 8 | 2 | 4 |
| move 12 to 40 | 8 | 30 | $8/30 \approx 0.267$ |
| move 2 to 6 | 4 | 6 | $4/6 \approx 0.667$ |

One point moved out of place divides $D$ by 15 in the second row and by 6 in the third row, although the other five points did not move.

**Rings.** For 12 points evenly on a circle of radius 1 and 12 on a circle of radius 4, both centered at the origin, the clustering into the two rings has gap 3 and largest diameter 8, so $D = 0.375$. A cut into a left half and a right half gets only 0.067. Here the Dunn index prefers the rings, while the [silhouette coefficient](/silhouette-coefficient/), the [Calinski-Harabasz index](/calinski-harabasz-index/) and the [Davies-Bouldin index](/davies-bouldin-index/) all prefer the halves.

**Non-examples.**

- $\delta$ is not the distance between centroids. With centroids, the rings above would have separation 0.
- The Dunn index is not a mean over clusters or points. It looks only at the single worst gap and the single worst diameter.
- A value below 1 does not mean that the clustering is wrong. Real clusters often touch or overlap, and then no clustering is compact and well separated.

## Related definitions

- [Single linkage clustering](/single-linkage-clustering/) and [maximum spacing k-clustering](/maximum-spacing-k-clustering/): the clusterings that maximize the smallest gap $\delta$.
- [Davies-Bouldin index](/davies-bouldin-index/): also compares spread with separation, but with centroids and a mean over clusters.
- [Silhouette coefficient](/silhouette-coefficient/): uses means of distances for each object, so one outlier has a small effect.
- [Cluster validity](/cluster-validity/) gives the overview of external and internal indices.

## References
