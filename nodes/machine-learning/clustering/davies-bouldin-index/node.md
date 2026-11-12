---
tag: 7PAEH8
kind: definition
slug: davies-bouldin-index
name: Davies-Bouldin index
aliases:
- Davies-Bouldin cluster separation measure
area: machine-learning/clustering
level: advanced
summary: "The mean over clusters of the worst ratio (S_i + S_j)/M_ij of spread to centroid distance. Lower is better. This page uses q = 1 and p = 2."
prereqs: [k-means-problem, euclidean-distance]
see_also: [calinski-harabasz-index, silhouette-coefficient, dunn-index, cluster-validity, k-means]
sources:
  - paper: doi:10.1109/TPAMI.1979.4766909
    title: "David L. Davies and Donald W. Bouldin, A cluster separation measure, IEEE Transactions on Pattern Analysis and Machine Intelligence PAMI-1(2), 1979, pages 224 to 227"
    locator: the dispersion S_i with exponent q, the Minkowski distance M_ij of order p between centroids, R_ij = (S_i + S_j)/M_ij, and the mean of the largest R_ij
  - paper: doi:10.1023/A:1012801612483
    title: "Maria Halkidi, Yannis Batistakis and Michalis Vazirgiannis, On clustering validation techniques, Journal of Intelligent Information Systems 17(2-3), 2001, pages 107 to 145"
    locator: the relative criteria for choosing k, with the Davies-Bouldin index among the internal indices
---

The Davies-Bouldin index scores a clustering of points in $\mathbb{R}^d$ by how much each cluster overlaps its most similar neighbor. For two clusters $i$ and $j$, it compares the sum of their spreads $S_i + S_j$ with the distance $M_{ij}$ between their centroids. For each cluster it takes the worst ratio over the other clusters, and the index is the mean of these worst ratios. **Lower is better**: a low value means compact clusters that are far apart. David Davies and Donald Bouldin defined it in 1979 with two exponents, $q$ for the spread and $p$ for the centroid distance. This page and its implementation use $q = 1$ and $p = 2$: the spread is the mean Euclidean distance to the centroid, and the centroid distance is Euclidean. It is an internal [cluster validity](/cluster-validity/) index.

## Definition

**Setting.** $X = \{x_1, \ldots, x_n\}$ is a set of $n$ points in $\mathbb{R}^d$. A clustering $C_1, \ldots, C_k$ of $X$ is given, with $k \ge 2$ and $n_i = |C_i|$. The centroid of $C_i$ is $c_i = \frac{1}{n_i} \sum_{x \in C_i} x$.

**Spread of a cluster.** For an exponent $q \ge 1$,

$$S_i = \Big( \frac{1}{n_i} \sum_{x \in C_i} \|x - c_i\|^q \Big)^{1/q},$$

with the [Euclidean norm](/euclidean-distance/). With $q = 1$ it is the mean distance to the centroid. With $q = 2$ it is the root of the mean squared distance.

**Distance of two centroids.** For an exponent $p \ge 1$, the Minkowski distance

$$M_{ij} = \Big( \sum_{t=1}^{d} |c_{i,t} - c_{j,t}|^p \Big)^{1/p}.$$

With $p = 2$ it is the Euclidean distance.

**The index.**

$$R_{ij} = \frac{S_i + S_j}{M_{ij}}, \qquad R_i = \max_{j \ne i} R_{ij}, \qquad \mathrm{DB} = \frac{1}{k} \sum_{i=1}^{k} R_i.$$

**Defaults and edge cases.** The implementation uses $q = 1$ and $p = 2$ by default and accepts other values. If two centroids are equal and the clusters are not both single points, $M_{ij} = 0$ and the index is $+\infty$, which the implementation returns.

**Choosing $k$.** Compute DB for a good clustering for each $k \ge 2$ in a range, and take the $k$ with the smallest value.

**Cost.** The centroids and spreads take $O(nd)$ time, and the $k(k-1)/2$ centroid distances take $O(k^2 d)$. So the index costs $O(nd + k^2 d)$, far less than the $O(n^2 d)$ of the [silhouette coefficient](/silhouette-coefficient/).

**Properties.**

- $\mathrm{DB} \ge 0$, with equality only if every $S_i = 0$, that is, each cluster is one repeated point.
- $R_{ij} = R_{ji}$. Davies and Bouldin first state a few conditions on a similarity of two clusters: it is nonnegative and symmetric, it grows when a spread grows with the distance fixed, and it falls when the distance grows with the spreads fixed. They then choose $(S_i + S_j)/M_{ij}$ as one simple form that meets them.
- With $p = 2$, DB is invariant under translations, rotations and uniform scaling of the points, because $S_i$ and $M_{ij}$ scale in the same way.
- DB uses only centroids, so it measures clusters as balls. Two clusters with the same centroid give $+\infty$, however well they are separated.
- Each cluster counts once, whatever its size. A small cluster near a large one can dominate the value.

## Examples and non-examples

**Two clusters on a line.** $C_1 = \{0, 2\}$ and $C_2 = \{10, 14\}$. The centroids are 1 and 12, the spreads are $S_1 = 1$ and $S_2 = 2$, and $M_{12} = 11$. So $R_{12} = 3/11$ and $\mathrm{DB} = 3/11 \approx 0.273$. In one dimension each point of a cluster here is at the same distance from its centroid, so $q = 2$ and $p = 1$ give the same value, $3/11$.

**Nine points in the plane.** Take the three triangles $\{(0, 0), (2, 0), (1, 3)\}$, $\{(8, 0), (10, 0), (9, 3)\}$ and $\{(4, 8), (6, 8), (5, 11)\}$. The centroids are $(1, 1)$, $(9, 1)$ and $(5, 9)$. In each triangle the distances to the centroid are $\sqrt 2$, $\sqrt 2$ and 2, so

$$S = \frac{2\sqrt 2 + 2}{3} \approx 1.60948$$

for each cluster. The centroid distances are $M_{12} = 8$ and $M_{13} = M_{23} = \sqrt{80} \approx 8.944$.

| $i$ | $R_{ij}$ for the other clusters | $R_i$ |
|---|---|---|
| 1 | $R_{12} = 2S/8 = 0.40237$, $R_{13} = 2S/\sqrt{80} = 0.35990$ | 0.40237 |
| 2 | $R_{21} = 0.40237$, $R_{23} = 0.35990$ | 0.40237 |
| 3 | $R_{31} = R_{32} = 0.35990$ | 0.35990 |

So $\mathrm{DB} = (0.40237 + 0.40237 + 0.35990)/3 \approx 0.38821$.

If the first two triangles are merged, the merged cluster has centroid $(5, 1)$ and spread $S_1 \approx 4.24448$, the third cluster keeps $S_2 \approx 1.60948$, and $M_{12} = 8$. Then $\mathrm{DB} = (4.24448 + 1.60948)/8 \approx 0.73174$, which is worse (higher) than 0.38821.

**Rings.** For 12 points evenly on a circle of radius 1 and 12 on a circle of radius 4, both centered at the origin, the clustering into the two rings has equal centroids and $\mathrm{DB} = +\infty$. A cut into a left half and a right half gets $\mathrm{DB} \approx 1.34$.

**Non-examples.**

- DB is not "higher is better" like the [Calinski-Harabasz index](/calinski-harabasz-index/) and the [silhouette coefficient](/silhouette-coefficient/). Mixing up the direction picks the worst $k$.
- DB is not defined for a general dissimilarity. It needs centroids. Variants replace the centroid by a medoid, but that is a different index.
- Values from different choices of $q$ and $p$ are not comparable. A report must state them.

## Related definitions

- [Calinski-Harabasz index](/calinski-harabasz-index/): a centroid-based index that uses total scatter, not the worst pair.
- [Dunn index](/dunn-index/): uses the smallest distance between clusters and the largest diameter, not centroids.
- [Silhouette coefficient](/silhouette-coefficient/): uses all pairwise distances.
- [k-means](/k-means/): the method whose clusters DB most often scores.
- [Cluster validity](/cluster-validity/) gives the overview of external and internal indices.

## References
