---
tag: 8Z3PGC
kind: definition
slug: calinski-harabasz-index
name: Calinski-Harabasz index
aliases:
- variance ratio criterion
- Calinski-Harabasz pseudo-F statistic
area: machine-learning/clustering
level: advanced
summary: "The ratio [tr(B)/(k-1)] / [tr(W)/(n-k)] of between-cluster to within-cluster scatter for points in R^d. Higher is better; it is the F statistic of a one-way ANOVA."
prereqs: [k-means-problem, covariance-matrix, euclidean-distance]
see_also: [silhouette-coefficient, davies-bouldin-index, dunn-index, cluster-validity, elbow-method, linear-discriminant-analysis, ward-method]
sources:
  - paper: doi:10.1080/03610927408827101
    title: "T. Caliński and J. Harabasz, A dendrite method for cluster analysis, Communications in Statistics 3(1), 1974, pages 1 to 27"
    locator: the variance ratio criterion [tr B/(k - 1)]/[tr W/(n - k)] and its use to choose the number of clusters
  - paper: doi:10.1007/BF02294245
    title: "Glenn W. Milligan and Martha C. Cooper, An examination of procedures for determining the number of clusters in a data set, Psychometrika 50(2), 1985, pages 159 to 179"
    locator: the Monte Carlo comparison of 30 stopping rules, in which the Calinski and Harabasz index did best
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 14.3.5 (the decomposition of the total point scatter into within-cluster and between-cluster parts)
---

The Calinski-Harabasz index scores a clustering of points in $\mathbb{R}^d$ by the ratio of the scatter between clusters to the scatter within clusters, each divided by its degrees of freedom:

$$\mathrm{CH} = \frac{\operatorname{tr}(B)/(k - 1)}{\operatorname{tr}(W)/(n - k)}.$$

A high value means clusters that are tight around their centroids and far from each other. Caliński and Harabasz proposed it in 1974 as the "variance ratio criterion" for choosing the number $k$ of clusters. For $d = 1$ it is the $F$ statistic of a one-way analysis of variance, which is why it is also called a pseudo-$F$ statistic. It is an internal [cluster validity](/cluster-validity/) index: it needs no true classes. It uses only centroids, so it costs $O(nd)$, but it is built on the same squared Euclidean scatter as [k-means](/k-means-problem/) and it favors round clusters.

## Definition

**Setting.** $X = \{x_1, \ldots, x_n\}$ is a set of $n$ points in $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/). A clustering $C_1, \ldots, C_k$ of $X$ is given, with $n_r = |C_r|$. The centroids are $c_r = \frac{1}{n_r} \sum_{x \in C_r} x$, and the mean of all points is $m = \frac{1}{n} \sum_{i} x_i$.

**Scatter matrices.** These are $d \times d$ matrices, $n$ times a [covariance matrix](/covariance-matrix/) in the case of $T$:

$$T = \sum_{i=1}^{n} (x_i - m)(x_i - m)^\top, \qquad W = \sum_{r=1}^{k} \sum_{x \in C_r} (x - c_r)(x - c_r)^\top, \qquad B = \sum_{r=1}^{k} n_r (c_r - m)(c_r - m)^\top.$$

**Lemma.** $T = W + B$.

*Proof.* For $x \in C_r$, write $x - m = (x - c_r) + (c_r - m)$. Then

$$(x - m)(x - m)^\top = (x - c_r)(x - c_r)^\top + (x - c_r)(c_r - m)^\top + (c_r - m)(x - c_r)^\top + (c_r - m)(c_r - m)^\top.$$

Sum over $x \in C_r$. The two middle terms vanish, because $\sum_{x \in C_r} (x - c_r) = 0$ by the definition of $c_r$. The last term does not depend on $x$, so it sums to $n_r (c_r - m)(c_r - m)^\top$. Summing over $r$ gives $T = W + B$. $\square$

The trace of $W$ is the within-cluster sum of squares $\sum_r \sum_{x \in C_r} \|x - c_r\|^2$, the objective of the [k-means problem](/k-means-problem/). The trace of $T$ does not depend on the clustering.

**The index.** For $2 \le k \le n - 1$ and $\operatorname{tr}(W) > 0$,

$$\mathrm{CH}(\mathcal{C}) = \frac{\operatorname{tr}(B)/(k - 1)}{\operatorname{tr}(W)/(n - k)} = \frac{n - k}{k - 1} \cdot \frac{\operatorname{tr}(T) - \operatorname{tr}(W)}{\operatorname{tr}(W)}.$$

It is not defined for $k = 1$ (no between scatter) or for $k = n$ (no within scatter). The implementation raises an error in these cases and when $\operatorname{tr}(W) = 0$. It works with exact fractions when the coordinates are integers or fractions.

**Choosing $k$.** Compute CH for a good clustering (for example the best of several runs of [k-means](/k-means/)) for each $k$ in a range, and take the $k$ with the largest value. Caliński and Harabasz also suggest a local maximum, or a point after which the index grows only slowly, when there is no clear maximum.

**Cost.** The centroids, the overall mean and the two traces take $O(nd)$ time. The full matrices take $O(nd^2)$.

**Properties.**

- **For a fixed $k$**, the factor $(n - k)/(k - 1)$ and $\operatorname{tr}(T)$ are constants, so the clustering with the largest CH is the one with the smallest $\operatorname{tr}(W)$, the optimal k-means clustering. The index adds something only when it compares different values of $k$.
- **ANOVA.** For $d = 1$, $\operatorname{tr}(B)$ and $\operatorname{tr}(W)$ are the between-group and within-group sums of squares, and CH is the $F$ statistic of a one-way ANOVA with $k - 1$ and $n - k$ degrees of freedom. For a clustering, the groups come from the data, so the $F$ distribution gives no valid p-value.
- **Invariance.** CH does not change under a translation, a rotation or a uniform scaling of all points, because each of these multiplies $\operatorname{tr}(W)$ and $\operatorname{tr}(B)$ by the same factor. It changes when the features are scaled by different factors.
- **Shape bias.** Like k-means, CH rewards clusters that are round and of similar spread. Two clusters with the same centroid have $\operatorname{tr}(B) = 0$, so $\mathrm{CH} = 0$, however well they are separated.
- **Milligan and Cooper** compared 30 rules for choosing $k$ on simulated data with well-separated clusters, and the Calinski-Harabasz index was the best. That result is for their kind of data, not a general guarantee.

## Examples and non-examples

**Nine points in the plane.** Take the three triangles $\{(0, 0), (2, 0), (1, 3)\}$, $\{(8, 0), (10, 0), (9, 3)\}$ and $\{(4, 8), (6, 8), (5, 11)\}$, so $n = 9$. Their centroids are $(1, 1)$, $(9, 1)$ and $(5, 9)$, and $m = (5, 11/3)$. Each triangle has the deviations $(-1, -1), (1, -1), (0, 2)$ from its centroid. So

$$W = 3 \begin{pmatrix} 2 & 0 \\ 0 & 6 \end{pmatrix} = \begin{pmatrix} 6 & 0 \\ 0 & 18 \end{pmatrix}, \qquad B = \begin{pmatrix} 96 & 0 \\ 0 & 128 \end{pmatrix}, \qquad T = \begin{pmatrix} 102 & 0 \\ 0 & 146 \end{pmatrix}.$$

For example, the first diagonal entry of $B$ is $3\,((1 - 5)^2 + (9 - 5)^2 + (5 - 5)^2) = 96$. Then $\operatorname{tr}(B) = 224$, $\operatorname{tr}(W) = 24$, and

$$\mathrm{CH} = \frac{224/2}{24/6} = \frac{112}{4} = 28.$$

**A worse clustering of the same points.** Merge the first two triangles into one cluster, so $k = 2$. Now $\operatorname{tr}(W) = 120$ and $\operatorname{tr}(B) = 128$, with the same total $\operatorname{tr}(T) = 248$. Then $\mathrm{CH} = (128/1)/(120/7) = 112/15 \approx 7.47$, much lower than 28.

**Rings.** Put 12 points evenly on a circle of radius 1 and 12 on a circle of radius 4, both centered at the origin. The clustering into the two rings has both centroids at the origin, so $\operatorname{tr}(B) = 0$ and $\mathrm{CH} = 0$. A cut into a left half and a right half gets $\mathrm{CH} \approx 9.65$. The index cannot see clusters that are nested.

**Non-examples.**

- CH is not a test. A high value does not show that clusters exist: k-means on uniform data also gives a positive CH that changes with $k$.
- CH is not defined for a general dissimilarity. It needs centroids, so it needs points in a vector space. For a general dissimilarity, use the [silhouette coefficient](/silhouette-coefficient/) or the [Dunn index](/dunn-index/).
- CH is not the ratio $\operatorname{tr}(B)/\operatorname{tr}(W)$ alone. Without the factor $(n - k)/(k - 1)$, the ratio grows with $k$ and is largest for $k = n$.

## Related definitions

- [k-means problem](/k-means-problem/): minimize $\operatorname{tr}(W)$ for a fixed $k$.
- [Elbow method](/elbow-method/): looks at $\operatorname{tr}(W)$ as a function of $k$, without the degrees of freedom.
- [Linear discriminant analysis](/linear-discriminant-analysis/): uses the same matrices $W$ and $B$ for known classes, and finds the directions with the largest ratio of between to within scatter.
- [Ward's method](/ward-method/): merges the two clusters whose union increases $\operatorname{tr}(W)$ the least.
- [Davies-Bouldin index](/davies-bouldin-index/) and [silhouette coefficient](/silhouette-coefficient/): other internal indices.
- [Cluster validity](/cluster-validity/) gives the overview of external and internal indices.

## References
